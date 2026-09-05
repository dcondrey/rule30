#!/usr/bin/env python3
"""Solver-free verification of the OBOC weighted-ranking obstructions.

Only Python integer arithmetic is used.  The listed finite multisets prove
that no bounded-below deterministic weighted-word energy on the indicated
fixed control can strictly decrease on every surviving forced macrostep.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Callable


State = tuple[int, int, int]  # T,A,B
Carry = tuple[int, int]
Transform = tuple[int, int, int, int]


def step_frontier(state: State, value: int) -> State:
    T, A, B = state
    C = value & 1
    previous = C
    for j in range(1, T + 1):
        right = ((T - 1) & 1) if j == 1 else ((B >> (j - 2)) & 1)
        current = (A >> (j - 1)) & 1
        previous ^= current | right
        C |= previous << j
    return T + 1, C, A


def parity_or(state: State) -> int:
    T, A, B = state
    aligned = A | (B << 1) | ((T - 1) & 1)
    return (aligned & ((1 << T) - 1)).bit_count() & 1


def forced_macro(state: State) -> State | None:
    middle = step_frontier(state, parity_or(state))
    if parity_or(middle) != 1:
        return None
    return step_frontier(middle, 1)


def forced_macro_reverse(state: State) -> State | None:
    """Independent deep-to-shallow implementation of the two-row macro."""
    T, A, B = state
    C = 0
    carry = 0
    for j in range(T, 0, -1):
        a = (A >> (j - 1)) & 1
        b = 1 if j == 1 else ((B >> (j - 2)) & 1)
        carry ^= a | b
        C |= carry << (j - 1)
    D = 0
    carry = 0
    for j in range(T + 1, 0, -1):
        c = (C >> (j - 1)) & 1
        a = 0 if j == 1 else ((A >> (j - 2)) & 1)
        carry ^= c | a
        D |= carry << (j - 1)
    if (D & 1) != 1:
        return None
    return T + 2, D, C


def seed_state(seed: int, length: int) -> State:
    state: State = (0, 0, 0)
    for index in range(length):
        rho = (seed >> index) & 1
        state = step_frontier(state, 1 - rho)
        state = step_frontier(state, 1)
    return state


def ordered_word(state: State) -> tuple[int, ...]:
    """Canonical aligned frontier word, in deep-to-shallow order."""
    _, A, B = state
    aligned_b = 1 | (B << 1)
    height = max(A.bit_length(), aligned_b.bit_length())
    shallow = tuple(
        2 * ((A >> j) & 1) + ((aligned_b >> j) & 1) for j in range(height)
    )
    return tuple(reversed(shallow))


def encode(carry: Carry) -> int:
    return 2 * carry[0] + carry[1]


def decode(value: int) -> Carry:
    return value >> 1, value & 1


def carry_step(carry: Carry, symbol: int) -> Carry:
    c, d = carry
    a, b = symbol >> 1, symbol & 1
    return c ^ (a | b), d ^ (c | a)


def input_transform(symbol: int) -> Transform:
    return tuple(
        encode(carry_step(decode(state), symbol)) for state in range(4)
    )


def compose(after: Transform, before: Transform) -> Transform:
    return tuple(after[before[state]] for state in range(4))


def d8_group() -> tuple[Transform, ...]:
    identity: Transform = (0, 1, 2, 3)
    found = {identity, *(input_transform(symbol) for symbol in range(4))}
    changed = True
    while changed:
        changed = False
        for left, right in product(tuple(found), repeat=2):
            value = compose(left, right)
            if value not in found:
                found.add(value)
                changed = True
    assert len(found) == 8
    assert all(sorted(transform) == [0, 1, 2, 3] for transform in found)
    return tuple(sorted(found))


@dataclass(frozen=True)
class Observer:
    name: str
    size: int
    start: int
    step: Callable[[int, int], int]


def observers() -> dict[str, Observer]:
    transforms = d8_group()
    transform_id = {value: index for index, value in enumerate(transforms)}
    identity_id = transform_id[(0, 1, 2, 3)]

    def carry_observer_step(carry: int, symbol: int) -> int:
        return encode(carry_step(decode(carry), symbol))

    def action_step(action: int, symbol: int) -> int:
        return transform_id[compose(input_transform(symbol), transforms[action])]

    def product_step(state: int, symbol: int) -> int:
        action, carry = divmod(state, 4)
        return 4 * action_step(action, symbol) + carry_observer_step(carry, symbol)

    return {
        "carry4": Observer("carry4", 4, 0, carry_observer_step),
        "d8": Observer("d8", 8, identity_id, action_step),
        "d8-carry": Observer("d8-carry", 32, 4 * identity_id, product_step),
    }


def features(observer: Observer, state: State) -> tuple[int, ...]:
    result = [0] * (5 * observer.size)
    q = observer.start
    for symbol in ordered_word(state):
        result[4 * q + symbol] += 1
        q = observer.step(q, symbol)
    result[4 * observer.size + q] = 1
    return tuple(result)


@dataclass(frozen=True)
class Entry:
    multiplicity: int
    seed_length: int
    seed_bits: str
    follow: int


CARRY_CERTIFICATE = (
    Entry(1, 4, "1010", 0),
    Entry(1, 4, "1010", 1),
)


D8_CERTIFICATE = (
    Entry(1, 4, "1010", 1),
    Entry(2, 6, "101000", 1),
    Entry(2, 6, "101000", 2),
    Entry(2, 6, "101000", 3),
    Entry(1, 6, "101000", 4),
    Entry(1, 6, "101000", 5),
    Entry(1, 6, "101000", 6),
)


def verify_certificate(observer: Observer, entries: tuple[Entry, ...]) -> None:
    nedge = 4 * observer.size
    aggregate = [0] * (nedge + observer.size)
    for entry in entries:
        assert len(entry.seed_bits) == entry.seed_length
        state = seed_state(int(entry.seed_bits, 2), entry.seed_length)
        for _ in range(entry.follow):
            nxt = forced_macro(state)
            assert nxt is not None
            assert nxt == forced_macro_reverse(state)
            state = nxt
        nxt = forced_macro(state)
        assert nxt is not None
        assert nxt == forced_macro_reverse(state)
        before = features(observer, state)
        after = features(observer, nxt)
        for coordinate, (a, b) in enumerate(zip(after, before, strict=True)):
            aggregate[coordinate] += entry.multiplicity * (a - b)
    assert all(value >= 0 for value in aggregate[:nedge])
    assert all(value == 0 for value in aggregate[nedge:])
    total = sum(entry.multiplicity for entry in entries)
    edge_gain = sum(aggregate[:nedge])
    print(
        f"{observer.name}: PASS; {len(entries)} transition types, "
        f"multiplicity={total}, aggregate edge-count gain={edge_gain}, "
        "terminal incidence=0"
    )


def main() -> None:
    family = observers()
    verify_certificate(family["carry4"], CARRY_CERTIFICATE)
    verify_certificate(family["d8"], D8_CERTIFICATE)
    verify_certificate(family["d8-carry"], D8_CERTIFICATE)

    # Starting from zero carry, the carry component is the D8 action on zero;
    # the nominal 32-state product therefore adds no reachable information.
    action = family["d8"].start
    product_state = family["d8-carry"].start
    for word_length in range(7):
        for symbols in product(range(4), repeat=word_length):
            action = family["d8"].start
            product_state = family["d8-carry"].start
            for symbol in symbols:
                action = family["d8"].step(action, symbol)
                product_state = family["d8-carry"].step(product_state, symbol)
            product_action, product_carry = divmod(product_state, 4)
            transforms = d8_group()
            assert product_action == action
            assert product_carry == transforms[action][0]
    print("d8-carry reachability: PASS; carry = action(0), so the product is redundant")


if __name__ == "__main__":
    main()

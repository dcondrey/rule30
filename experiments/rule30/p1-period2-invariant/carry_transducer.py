#!/usr/bin/env python3
"""Exact four-state carry transducer for the alternating Rule 30 macro map."""

from __future__ import annotations

from itertools import product


State = tuple[int, int, int]  # stored frontier: T,A,B
Carry = tuple[int, int]       # c,d
Transform = tuple[int, int, int, int]


def encode(carry: Carry) -> int:
    return 2 * carry[0] + carry[1]


def decode(value: int) -> Carry:
    return value >> 1, value & 1


def carry_step(carry: Carry, symbol: int, use_or: bool = True) -> tuple[Carry, int]:
    """Read q=(a,b); emit (d',c'), encoded as 2*d'+c'."""
    c, d = carry
    a, b = symbol >> 1, symbol & 1
    combine = (lambda x, y: x | y) if use_or else (lambda x, y: x ^ y)
    c_new = c ^ combine(a, b)
    d_new = d ^ combine(c, a)
    return (c_new, d_new), 2 * d_new + c_new


def terminal(carry: Carry) -> int:
    """Final shallow symbol q'_1=(D_1,B'_0)=(c XOR d,1)."""
    c, d = carry
    return 2 * (c ^ d) + 1


def input_transform(symbol: int, use_or: bool = True) -> Transform:
    return tuple(
        encode(carry_step(decode(state), symbol, use_or)[0]) for state in range(4)
    )


def compose(after: Transform, before: Transform) -> Transform:
    """Return after o before."""
    return tuple(after[before[state]] for state in range(4))


def generated_monoid(use_or: bool = True) -> set[Transform]:
    generators = [input_transform(symbol, use_or) for symbol in range(4)]
    identity: Transform = (0, 1, 2, 3)
    found = {identity, *generators}
    changed = True
    while changed:
        changed = False
        for left, right in product(tuple(found), repeat=2):
            value = compose(left, right)
            if value not in found:
                found.add(value)
                changed = True
    return found


def transform_order(transform: Transform) -> int:
    identity: Transform = (0, 1, 2, 3)
    value = identity
    for order in range(1, 25):
        value = compose(transform, value)
        if value == identity:
            return order
    raise AssertionError(transform)


def gray_inverse(word: int) -> int:
    answer = 0
    while word:
        answer ^= word
        word >>= 1
    return answer


def gray_macro(state: State) -> tuple[int, State]:
    T, A, B = state
    C = gray_inverse(A | 1 | (B << 1))
    D = gray_inverse(C | (A << 1))
    return D & 1, (T + 2, D, C)


def active_symbols(state: State) -> list[int]:
    _, A, B = state
    V = 1 | (B << 1)
    height = max(A.bit_length(), V.bit_length())
    return [2 * ((A >> j) & 1) + ((V >> j) & 1) for j in range(height)]


def transduce(state: State) -> tuple[int, State]:
    """Run the length-free transducer and reconstruct the successor pair."""
    symbols = active_symbols(state)  # shallow to deep
    carry = (0, 0)
    emitted_deep_to_shallow: list[int] = []
    for symbol in reversed(symbols):
        carry, output = carry_step(carry, symbol)
        emitted_deep_to_shallow.append(output)
    output_symbols = [terminal(carry), *reversed(emitted_deep_to_shallow)]
    A_next = 0
    B_next = 0
    for j, symbol in enumerate(output_symbols, start=1):
        A_next |= (symbol >> 1) << (j - 1)
        if j >= 2:
            B_next |= (symbol & 1) << (j - 2)
    return output_symbols[0] >> 1, (state[0] + 2, A_next, B_next)


def word_action(state: State) -> Transform:
    action: Transform = (0, 1, 2, 3)
    for symbol in reversed(active_symbols(state)):
        action = compose(input_transform(symbol), action)
    return action


def wf_step(state: State, value: int) -> State:
    T, A, B = state
    C = value & 1
    previous = C
    for j in range(1, T + 1):
        b = ((T - 1) & 1) if j == 1 else (B >> (j - 2)) & 1
        a = (A >> (j - 1)) & 1
        previous ^= a | b
        C |= previous << j
    return T + 1, C, A


def parity_or(state: State) -> int:
    T, A, B = state
    word = A | (B << 1) | ((T - 1) & 1)
    return (word & ((1 << T) - 1)).bit_count() & 1


def forced_macro(state: State) -> State | None:
    middle = wf_step(state, parity_or(state))
    if parity_or(middle) != 1:
        return None
    return wf_step(middle, 1)


def seed_state(seed: int, length: int) -> State:
    state: State = (0, 0, 0)
    for index in range(length):
        rho = (seed >> index) & 1
        state = wf_step(state, 1 - rho)
        state = wf_step(state, 1)
    return state


def exhaustive_word_crosscheck(max_T: int = 8) -> int:
    checked = 0
    for T in range(2, max_T + 1, 2):
        for A in range(1 << T):
            for B in range(1 << (T - 1)):
                state = (T, A, B)
                assert transduce(state) == gray_macro(state), state
                checked += 1
    return checked


def reachable_states(max_seed: int, max_follow: int) -> dict[State, tuple[int, int, int]]:
    origins: dict[State, tuple[int, int, int]] = {}
    for length in range(1, max_seed + 1):
        for seed in range(1 << length):
            state = seed_state(seed, length)
            for follow in range(max_follow + 1):
                origin = (length, seed, follow)
                if state not in origins or origin < origins[state]:
                    origins[state] = origin
                nxt = forced_macro(state)
                if nxt is None:
                    break
                state = nxt
    return origins


def first_action_collision(
    origins: dict[State, tuple[int, int, int]], require_same_T: bool
) -> tuple[State, State] | None:
    seen: dict[object, State] = {}
    for state in sorted(origins, key=lambda value: origins[value]):
        pin, nxt = gray_macro(state)
        if pin == 0:
            continue
        action = word_action(state)
        key: object = (state[0], action) if require_same_T else action
        previous = seen.get(key)
        if previous is None:
            seen[key] = state
            continue
        _, previous_next = gray_macro(previous)
        previous_next_pin, _ = gray_macro(previous_next)
        next_pin, _ = gray_macro(nxt)
        signature = (word_action(nxt), next_pin)
        previous_signature = (word_action(previous_next), previous_next_pin)
        if signature != previous_signature:
            return previous, state
    return None


def action_trace(state: State, depth: int) -> tuple[Transform, ...]:
    result = []
    for _ in range(depth):
        result.append(word_action(state))
        state = gray_macro(state)[1]
    return tuple(result)


def first_lookahead_collision(
    origins: dict[State, tuple[int, int, int]], depth: int
) -> tuple[State, State] | None:
    """Collision after retaining `depth` consecutive group actions."""
    seen: dict[tuple[Transform, ...], State] = {}
    for state in sorted(origins, key=lambda value: origins[value]):
        cursor = state
        accepting = True
        for _ in range(depth):
            pin, cursor = gray_macro(cursor)
            if pin == 0:
                accepting = False
                break
        if not accepting:
            continue
        summary = action_trace(state, depth)
        previous = seen.get(summary)
        if previous is None:
            seen[summary] = state
            continue
        left_cursor = previous
        right_cursor = state
        for _ in range(depth):
            left_cursor = gray_macro(left_cursor)[1]
            right_cursor = gray_macro(right_cursor)[1]
        if word_action(left_cursor) != word_action(right_cursor):
            return previous, state
    return None


def permutation_orbits(group: set[Transform]) -> list[tuple[int, ...]]:
    unseen = set(range(4))
    result = []
    while unseen:
        seed = min(unseen)
        orbit = {transform[seed] for transform in group}
        result.append(tuple(sorted(orbit)))
        unseen -= orbit
    return result


def main() -> None:
    print('Rule 30 carry table: state,input -> next/output')
    for state in range(4):
        entries = []
        for symbol in range(4):
            nxt, output = carry_step(decode(state), symbol)
            entries.append(f'{encode(nxt)}/{output}')
        print(f'  state {state}: ' + ' '.join(entries))
    print('Rule 30 input transformations:')
    for symbol in range(4):
        print(f'  {symbol}: {input_transform(symbol)}')

    rule30_group = generated_monoid(True)
    rule90_group = generated_monoid(False)
    assert all(len(set(transform)) == 4 for transform in rule30_group)
    rotation = input_transform(1)
    reflection = input_transform(0)
    rotation_inverse = compose(compose(rotation, rotation), rotation)
    assert transform_order(rotation) == 4
    assert transform_order(reflection) == 2
    assert compose(reflection, compose(rotation, reflection)) == rotation_inverse
    print(
        f'Rule 30 monoid size={len(rule30_group)}; all permutations; '
        f'orbits={permutation_orbits(rule30_group)}'
    )
    print('Rule 30 group elements (image tuple, order):')
    for transform in sorted(rule30_group):
        print(f'  {transform} order={transform_order(transform)}')
    print('presentation check: r=input 1 has order 4, s=input 0 has order 2, srs=r^-1')
    print(
        f'Rule 90 XOR-control monoid size={len(rule90_group)}; '
        f'all permutations={all(len(set(t)) == 4 for t in rule90_group)}; '
        f'orbits={permutation_orbits(rule90_group)}'
    )
    print('Rule 90 XOR-control input transformations:')
    for symbol in range(4):
        print(f'  {symbol}: {input_transform(symbol, False)}')
    checks = exhaustive_word_crosscheck()
    print(f'word-transducer crosscheck: {checks} exact frontiers PASS')

    origins = reachable_states(16, 128)
    print(f'distinct reachable states: {len(origins)}')
    for same_T in (False, True):
        collision = first_action_collision(origins, same_T)
        print(f'action closure collision same_T={same_T}: {collision is not None}')
        if collision:
            left, right = collision
            print(f'  left origin={origins[left]} state={left} action={word_action(left)}')
            print(f'  right origin={origins[right]} state={right} action={word_action(right)}')
            left_next = gray_macro(left)[1]
            right_next = gray_macro(right)[1]
            print(
                f'  successor actions={word_action(left_next)}, '
                f'{word_action(right_next)}; next pins='
                f'{gray_macro(left_next)[0]},{gray_macro(right_next)[0]}'
            )
    for depth in (1, 2):
        collision = first_lookahead_collision(origins, depth)
        print(
            f'action-lookahead depth={depth} (capacity {8**depth}) '
            f'closure collision={collision is not None}'
        )
        if collision:
            left, right = collision
            print(f'  left origin={origins[left]} state={left}')
            print(f'  right origin={origins[right]} state={right}')
            print(f'  shared trace={action_trace(left, depth)}')
            left_cursor, right_cursor = left, right
            for _ in range(depth):
                left_cursor = gray_macro(left_cursor)[1]
                right_cursor = gray_macro(right_cursor)[1]
            print(
                f'  next actions={word_action(left_cursor)}, '
                f'{word_action(right_cursor)}; pins='
                f'{gray_macro(left_cursor)[0]},{gray_macro(right_cursor)[0]}'
            )


if __name__ == '__main__':
    main()

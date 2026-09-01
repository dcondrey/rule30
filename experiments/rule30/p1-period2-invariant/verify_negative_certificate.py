#!/usr/bin/env python3
"""Stdlib verifier for the additive-ranking negative certificates.

For each locality L=1..4 the certificate is a finite multiset of exact
surviving frontier transitions.  Endpoint incidences cancel and aggregate
local-pattern counts are componentwise nonnegative.  Therefore no potential
with nonnegative local weights and an arbitrary bounded term on the recorded
prefix/suffix endpoints can strictly decrease on every transition.
"""

from __future__ import annotations

from dataclasses import dataclass


State = tuple[int, int, int]


def step_frontier(state: State, v: int) -> State:
    T, A, B = state
    C = v & 1
    previous = C
    for j in range(1, T + 1):
        right = ((T - 1) & 1) if j == 1 else ((B >> (j - 2)) & 1)
        current = (A >> (j - 1)) & 1
        previous ^= current | right
        C |= previous << j
    return T + 1, C, A


def parity_or(state: State) -> int:
    T, A, B = state
    aligned_b = (B << 1) | 1  # c_{T-1}=1 at every post-pin even T
    return ((A | aligned_b) & ((1 << T) - 1)).bit_count() & 1


def macro(state: State) -> State | None:
    middle = step_frontier(state, parity_or(state))
    T, C, A = middle
    aligned_a = A << 1  # c_T=0 for phase 01 at odd middle length T
    if ((C | aligned_a) & ((1 << T) - 1)).bit_count() % 2 != 1:
        return None
    return step_frontier(middle, 1)


def macro_reverse(state: State) -> State | None:
    """Independent deep-to-shallow cumulative-XOR implementation."""
    T, A, B = state
    C = 0
    cnext = 0
    for j in range(T, 0, -1):
        aj = (A >> (j - 1)) & 1
        bjm1 = 1 if j == 1 else ((B >> (j - 2)) & 1)
        cj = cnext ^ (aj | bjm1)
        C |= cj << (j - 1)
        cnext = cj

    D = 0
    dnext = 0
    for j in range(T + 1, 0, -1):
        cj = (C >> (j - 1)) & 1
        ajm1 = 0 if j == 1 else ((A >> (j - 2)) & 1)
        dj = dnext ^ (cj | ajm1)
        D |= dj << (j - 1)
        dnext = dj
    if (D & 1) != 1:
        return None
    return T + 2, D, C


def seed_state(seed: int, length: int) -> State:
    state: State = (0, 0, 0)
    for i in range(length):
        rho = (seed >> i) & 1
        state = step_frontier(state, 1 - rho)
        state = step_frontier(state, 1)
    return state


def word(state: State) -> tuple[int, ...]:
    T, A, B = state
    return tuple(
        2 * ((A >> (j - 1)) & 1)
        + (1 if j == 1 else ((B >> (j - 2)) & 1))
        for j in range(1, T + 1)
    )


def code(symbols: tuple[int, ...]) -> int:
    result = 0
    for symbol in symbols:
        result = 4 * result + symbol
    return result


def features(state: State, locality: int) -> list[int]:
    symbols = word(state)
    nlocal = 4**locality
    nendpoint = 1 if locality == 1 else 4 ** (locality - 1)
    result = [0] * (nlocal + 2 * nendpoint)
    for start in range(len(symbols) - locality + 1):
        result[code(symbols[start : start + locality])] += 1
    width = locality - 1
    prefix = code(symbols[:width]) if width else 0
    suffix = code(symbols[-width:]) if width else 0
    result[nlocal + prefix] += 1
    result[nlocal + nendpoint + suffix] += 1
    return result


@dataclass(frozen=True)
class Entry:
    multiplicity: int
    seed_length: int
    seed_bits: str
    follow: int


CERTIFICATES: dict[int, tuple[Entry, ...]] = {
    1: (
        Entry(1, 6, "110000", 3),
        Entry(1, 11, "00001111010", 3),
        Entry(1, 12, "110101100000", 1),
    ),
    2: (
        Entry(9, 1, "0", 1),
        Entry(1, 11, "00011100000", 7),
        Entry(1, 11, "10011101010", 1),
        Entry(1, 12, "001010000000", 1),
    ),
    3: (
        Entry(1, 7, "1011100", 2),
        Entry(1, 11, "01101011010", 2),
        Entry(3, 11, "11011001100", 3),
        Entry(1, 12, "001011111000", 2),
        Entry(1, 12, "010100110110", 3),
        Entry(1, 12, "011000100011", 2),
        Entry(3, 12, "100010111000", 6),
        Entry(2, 12, "101110101110", 2),
    ),
    4: (
        Entry(2, 8, "01010000", 3),
        Entry(2, 10, "1010100110", 4),
        Entry(2, 10, "1110000110", 4),
        Entry(5, 11, "10010100110", 5),
        Entry(1, 11, "10110101000", 3),
        Entry(1, 11, "11010101010", 3),
        Entry(5, 12, "000111000000", 3),
        Entry(4, 12, "001100111110", 4),
        Entry(3, 12, "010010100110", 4),
        Entry(3, 12, "010101100000", 6),
        Entry(3, 12, "011100011100", 3),
        Entry(3, 12, "100010111000", 5),
        Entry(2, 12, "100010111000", 6),
        Entry(4, 12, "100110110000", 3),
        Entry(1, 12, "101100111000", 3),
        Entry(2, 12, "111001100110", 6),
    ),
}


def verify() -> None:
    for locality, entries in CERTIFICATES.items():
        nlocal = 4**locality
        aggregate: list[int] | None = None
        transition_count = 0
        for entry in entries:
            assert len(entry.seed_bits) == entry.seed_length
            state = seed_state(int(entry.seed_bits, 2), entry.seed_length)
            for _ in range(entry.follow):
                state = macro(state)
                assert state is not None
            nxt = macro(state)
            assert nxt is not None
            assert nxt == macro_reverse(state)
            before = features(state, locality)
            after = features(nxt, locality)
            delta = [b - a for a, b in zip(before, after, strict=True)]
            if aggregate is None:
                aggregate = [0] * len(delta)
            for i, value in enumerate(delta):
                aggregate[i] += entry.multiplicity * value
            transition_count += entry.multiplicity
        assert aggregate is not None
        assert all(value >= 0 for value in aggregate[:nlocal])
        assert all(value == 0 for value in aggregate[nlocal:])
        gains = sum(aggregate[:nlocal])
        print(
            f"L={locality}: PASS; {len(entries)} transition types, "
            f"multiplicity={transition_count}, local-count gain={gains}, "
            "endpoint incidence=0"
        )


if __name__ == "__main__":
    verify()

#!/usr/bin/env python3
"""Solver-free verifier for the signed tile/contact negative certificate.

The certificate is a multiset of exact accepting macrotransitions.  Its
endpoint-feature changes cancel, while every normalized local edge/contact
count has nonnegative aggregate change.  Hence no nonnegative local charge
plus bounded endpoint potential can decrease strictly on every listed
transition.
"""

from __future__ import annotations


State = tuple[int, int, int]
N_LOCAL = 28
N_ENDPOINT = 12


CERTIFICATE = (
    (2, (14, 11168, 2), (32, 757762901, 429573749), (34, 1403692373, 707458389)),
    (2, (15, 24312, 0), (30, 721089907, 377654090), (32, 1499026245, 894786213)),
    (8, (15, 26048, 0), (30, 389196715, 346729050), (32, 878007653, 710585045)),
    (4, (15, 26716, 1), (32, 1386883429, 970265813), (34, 2846190421, 1563676341)),
    (1, (15, 32040, 0), (30, 336243371, 436951722), (32, 894806699, 669723306)),
    (1, (16, 12472, 0), (32, 2505526101, 1454139061), (34, 5716110165, 3597306453)),
    (1, (16, 27392, 10), (52, 2951540794981, 1480275088725), (54, 6234851202901, 3480350405813)),
    (4, (16, 28000, 0), (32, 1262578021, 1717619925), (34, 3942817139, 2323730762)),
    (2, (16, 46368, 0), (32, 2505727347, 1431515466), (34, 5726841515, 3579073882)),
    (5, (16, 49856, 3), (38, 22232606003, 11166643626), (40, 50136249259, 26477808218)),
    (3, (16, 60704, 3), (38, 24070687403, 14321796442), (40, 43648198059, 22235247402)),
    (3, (16, 63436, 0), (32, 2572243627, 1431878314), (34, 5851235941, 3533808981)),
)


def inverse_gray(word: int) -> int:
    result = 0
    while word:
        result ^= word
        word >>= 1
    return result


def macro(state: State) -> tuple[int, State]:
    T, A, B = state
    C = inverse_gray(A | 1 | (B << 1))
    D = inverse_gray(C | (A << 1))
    return D & 1, (T + 2, D, C)


def one_frontier_step(state: State, value: int) -> State:
    T, A, B = state
    C = value & 1
    previous = C
    for j in range(1, T + 1):
        b = ((T - 1) & 1) if j == 1 else (B >> (j - 2)) & 1
        a = (A >> (j - 1)) & 1
        previous ^= a | b
        C |= previous << j
    return T + 1, C, A


def frontier_or_parity(state: State) -> int:
    T, A, B = state
    word = A | (B << 1) | ((T - 1) & 1)
    return (word & ((1 << T) - 1)).bit_count() & 1


def forced_macro(state: State) -> State | None:
    middle = one_frontier_step(state, frontier_or_parity(state))
    if frontier_or_parity(middle) != 1:
        return None
    return one_frontier_step(middle, 1)


def state_at(origin: tuple[int, int, int]) -> State:
    length, seed, follow = origin
    state: State = (0, 0, 0)
    for index in range(length):
        rho = (seed >> index) & 1
        state = one_frontier_step(state, 1 - rho)
        state = one_frontier_step(state, 1)
    for _ in range(follow):
        next_state = forced_macro(state)
        assert next_state is not None
        state = next_state
    return state


def carry_step(carry: tuple[int, int], symbol: int) -> tuple[int, int]:
    c, d = carry
    a, b = symbol >> 1, symbol & 1
    return c ^ (a | b), d ^ (c | a)


def active_symbols(state: State) -> list[int]:
    _, A, B = state
    V = 1 | (B << 1)
    height = max(A.bit_length(), V.bit_length())
    return [2 * ((A >> j) & 1) + ((V >> j) & 1) for j in range(height)]


def feature(state: State) -> tuple[int, ...]:
    symbols = active_symbols(state)
    result = [0] * (N_LOCAL + N_ENDPOINT)
    carry = (0, 0)
    for symbol in reversed(symbols):
        incoming = 2 * carry[0] + carry[1]
        result[4 * incoming + symbol] += 1
        carry = carry_step(carry, symbol)
    for symbol in symbols:
        result[16 + symbol] += 1
    for component in range(2):
        bits = [symbol >> 1 if component == 0 else symbol & 1 for symbol in symbols]
        bits.append(0)
        for left, right in zip(bits, bits[1:]):
            result[20 + 4 * component + 2 * left + right] += 1
    offset = N_LOCAL
    result[offset + 2 * carry[0] + carry[1]] = 1
    result[offset + 4 + symbols[0]] = 1
    result[offset + 8 + symbols[-1]] = 1
    return tuple(result)


def main() -> None:
    aggregate = [0] * (N_LOCAL + N_ENDPOINT)
    for multiplicity, origin, before, after in CERTIFICATE:
        assert state_at(origin) == before
        pin, independently_computed_after = macro(before)
        assert pin == 1
        assert independently_computed_after == after
        change = [right - left for left, right in zip(feature(before), feature(after))]
        for index, value in enumerate(change):
            aggregate[index] += multiplicity * value

    expected = (
        2, 3, 5, 4, 0, 3, 1, 0, 1, 1, 2, 1, 1, 3, 8, 1,
        4, 10, 16, 6, 1, 13, 13, 9, 5, 15, 15, 1,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    )
    assert tuple(aggregate) == expected
    assert all(value >= 0 for value in aggregate[:N_LOCAL])
    assert all(value == 0 for value in aggregate[N_LOCAL:])
    print('certificate transitions: 12 types, multiplicity 36')
    print(f'aggregate local gain: {sum(aggregate[:N_LOCAL])}')
    print('endpoint cancellation: 12/12 zero')
    print('solver-free exact verification: PASS')


if __name__ == '__main__':
    main()

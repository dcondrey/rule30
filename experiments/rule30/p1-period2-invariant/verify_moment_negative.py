#!/usr/bin/env python3
"""Standalone exact verifier for the fixed-order moment obstruction.

Only Python's standard library is used.  The search that found the reachable
collision is not rerun: the two rho seeds and all asserted states are checked
directly from the frontier recurrence.
"""

from __future__ import annotations

from itertools import combinations


State = tuple[int, int, int]


def gray_inverse(word: int) -> int:
    out = 0
    while word:
        out ^= word
        word >>= 1
    return out


def hasse(word: int, order: int) -> int:
    answer = 0
    position = 0
    while word:
        if word & 1 and position & order == order:
            answer ^= 1
        position += 1
        word >>= 1
    return answer


def gray_macro(state: State) -> tuple[int, State]:
    T, A, B = state
    C = gray_inverse(A | 1 | (B << 1))
    D = gray_inverse(C | (A << 1))
    return D & 1, (T + 2, D, C)


def direct_macro(state: State) -> tuple[int, State]:
    T, A, B = state
    C = 0
    carry = 0
    for j in range(T, 0, -1):
        a = (A >> (j - 1)) & 1
        b = 1 if j == 1 else (B >> (j - 2)) & 1
        carry ^= a | b
        C |= carry << (j - 1)
    D = 0
    carry = 0
    for j in range(T + 1, 0, -1):
        c = (C >> (j - 1)) & 1
        a = 0 if j == 1 else (A >> (j - 2)) & 1
        carry ^= c | a
        D |= carry << (j - 1)
    return D & 1, (T + 2, D, C)


def wf_step(state: State, value: int) -> State:
    T, A, B = state
    C = value & 1
    previous = C
    for j in range(1, T + 1):
        boundary = (T - 1) & 1
        b = boundary if j == 1 else (B >> (j - 2)) & 1
        a = (A >> (j - 1)) & 1
        previous ^= a | b
        C |= previous << j
    return T + 1, C, A


def parity_or(state: State) -> int:
    T, A, B = state
    boundary = (T - 1) & 1
    word = A | (B << 1) | boundary
    return (word & ((1 << T) - 1)).bit_count() & 1


def forced_macro(state: State) -> State | None:
    middle = wf_step(state, parity_or(state))
    if parity_or(middle) != 1:
        return None
    return wf_step(middle, 1)


def seed_state(seed: int, length: int) -> State:
    state = (0, 0, 0)
    for index in range(length):
        rho = (seed >> index) & 1
        state = wf_step(state, 1 - rho)
        state = wf_step(state, 1)
    return state


def rich_variables(state: State) -> list[int]:
    _, A, B = state
    V = 1 | (B << 1)
    C = gray_inverse(A | V)
    S = A << 1
    generators = [A, V, C, S]
    values = []
    for degree in range(1, 4):
        for chosen in combinations(range(4), degree):
            value = generators[chosen[0]]
            for index in chosen[1:]:
                value &= generators[index]
            values.append(value)
    return values


def endpoint_bits(state: State, width: int = 2) -> tuple[int, ...]:
    _, A, B = state
    V = 1 | (B << 1)
    height = max(A.bit_length(), V.bit_length())
    mask = (1 << width) - 1
    shift = max(0, height - width)
    return A & mask, V & mask, (A >> shift) & mask, (V >> shift) & mask, height & 15


def rich_feature(state: State, order: int = 8) -> tuple[int, ...]:
    result = []
    for word in rich_variables(state):
        result.extend(hasse(word, k) for k in range(order + 1))
    result.extend(endpoint_bits(state))
    return tuple(result)


def check_quotient_identity() -> int:
    checks = 0
    for word in range(1 << 16):
        image = gray_inverse(word)
        for order in range(9):
            assert hasse(image, order) == hasse(word, order) ^ hasse(word, order + 1)
            checks += 1
    return checks


def check_gray_identity() -> int:
    checks = 0
    for T in range(2, 9, 2):
        for A in range(1 << T):
            for B in range(1 << (T - 1)):
                assert gray_macro((T, A, B)) == direct_macro((T, A, B))
                checks += 1
    return checks


def check_all_order_obstruction(max_order: int = 64) -> int:
    for order in range(max_order + 1):
        power = 1
        for _ in range(order + 1):
            power ^= power << 1  # multiply by 1+z over GF(2)
        perturbation = power << 1  # z(1+z)^(K+1)
        left = 1
        right = left ^ perturbation
        assert left == left | 1
        assert right == right | 1  # both are legal A OR (1+z*0) words
        assert all(hasse(left, k) == hasse(right, k) for k in range(order + 1))
        assert hasse(gray_inverse(left), order) != hasse(
            gray_inverse(right), order
        )
    return max_order + 1


def follow(seed: int, length: int, count: int) -> State:
    state = seed_state(seed, length)
    for _ in range(count):
        nxt = forced_macro(state)
        assert nxt is not None
        state = nxt
    return state


def check_reachable_collision() -> tuple[list[int], State, State]:
    left = follow(1196, 13, 3)
    right = follow(1344, 13, 3)
    assert left == (32, 358_962_517, 181_753_173)
    assert right == (32, 357_913_957, 178_957_013)
    assert rich_feature(left) == rich_feature(right)
    left_pin, left_next = gray_macro(left)
    right_pin, right_next = gray_macro(right)
    assert left_pin == right_pin == 1
    left_feature = rich_feature(left_next)
    right_feature = rich_feature(right_next)
    differences = [
        index
        for index, pair in enumerate(zip(left_feature, right_feature))
        if pair[0] != pair[1]
    ]
    assert differences
    return differences, left, right


def main() -> None:
    quotient_checks = check_quotient_identity()
    macro_checks = check_gray_identity()
    obstruction_checks = check_all_order_obstruction()
    differences, left, right = check_reachable_collision()
    print(f'Hasse quotient identity: {quotient_checks} exact checks')
    print(f'Gray macro identity: {macro_checks} exact legal frontier checks')
    print(f'truncation obstruction: K=0..{obstruction_checks - 1} verified')
    print('reachable rich K=8 collision: verified')
    print(f'  states: {left} and {right}')
    print('  both current pins pass; successor feature differences:', differences)


if __name__ == '__main__':
    main()

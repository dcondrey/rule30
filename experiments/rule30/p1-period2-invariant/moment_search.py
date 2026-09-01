#!/usr/bin/env python3
"""Exact fixed-order Hasse-moment tests for the period-two frontier map.

This is a falsification search, not a finite-horizon proof.  It also verifies
the polynomial/Gray-code form of the two reverse cumulative-XOR sweeps.
"""

from __future__ import annotations

import argparse
from itertools import combinations

from ranking_search import forced_macro, seed_state


State = tuple[int, int, int]
Origin = tuple[int, int, int]


def gray_inverse(word: int) -> int:
    """Inverse of g(x)=x XOR (x>>1), for a finite nonnegative integer."""
    out = 0
    while word:
        out ^= word
        word >>= 1
    return out


def gray_macro(state: State) -> tuple[int, State]:
    """The exact reverse macrostep; first result is the pin bit D_1."""
    T, A, B = state
    assert 0 <= A < (1 << T)
    assert 0 <= B < (1 << max(T - 1, 0))
    aligned_B = 1 | (B << 1)
    C = gray_inverse(A | aligned_B)
    D = gray_inverse(C | (A << 1))
    return D & 1, (T + 2, D, C)


def hasse(word: int, order: int) -> int:
    """H_order(sum word_n*z^n) at z=1, using Lucas modulo two."""
    answer = 0
    position = 0
    while word:
        if word & 1 and position & order == order:
            answer ^= 1
        position += 1
        word >>= 1
    return answer


def q_word(word: int) -> int:
    """Reverse cumulative XOR Q with (1+z)Q=zX+X(1)."""
    return gray_inverse(word)


def check_hasse_identity(max_length: int, max_order: int) -> int:
    checked = 0
    for word in range(1 << max_length):
        image = q_word(word)
        for order in range(max_order + 1):
            expected = hasse(word, order) ^ hasse(word, order + 1)
            assert hasse(image, order) == expected, (word, order)
            checked += 1
    return checked


def check_gray_macro(max_length: int) -> int:
    checked = 0
    # The macro boundary is after a complete zero/pin pair, so T is even and
    # B_0=1.  Odd T has the other phase boundary and is not a macro state.
    for T in range(2, max_length + 1, 2):
        for A in range(1 << T):
            for B in range(1 << (T - 1)):
                state = (T, A, B)
                pin, nxt = gray_macro(state)
                reference = forced_macro(0, state)
                assert (reference is not None) == (pin == 1), state
                if reference is not None:
                    assert reference == nxt, (state, reference, nxt)
                checked += 1
    return checked


def obstruction_word(order: int) -> int:
    """z(1+z)^(order+1) over GF(2), as a coefficient bitset."""
    power = 1
    for _ in range(order + 1):
        power ^= power << 1
    return power << 1


def check_truncation_obstructions(max_order: int) -> list[tuple[int, int, int]]:
    """Return (K,O,O') pairs equal through H_K but split after Q at H_K."""
    result = []
    for order in range(max_order + 1):
        perturbation = obstruction_word(order)
        before = 1
        after = before ^ perturbation
        assert (before & 1) == (after & 1) == 1
        assert all(
            hasse(before, k) == hasse(after, k) for k in range(order + 1)
        )
        assert hasse(q_word(before), order) != hasse(q_word(after), order)
        result.append((order, before, after))
    return result


def variables(state: State, rich: bool) -> list[int]:
    _, A, B = state
    V = 1 | (B << 1)
    if not rich:
        return [A, V, A & V]
    C = gray_inverse(A | V)
    S = A << 1
    generators = [A, V, C, S]
    values: list[int] = []
    for degree in range(1, 4):
        for chosen in combinations(range(len(generators)), degree):
            value = generators[chosen[0]]
            for index in chosen[1:]:
                value &= generators[index]
            values.append(value)
    return values


def endpoint_bits(state: State, width: int) -> tuple[int, ...]:
    if width == 0:
        return ()
    _, A, B = state
    V = 1 | (B << 1)
    height = max(A.bit_length(), V.bit_length())
    shallow_mask = (1 << width) - 1
    shallow = (A & shallow_mask, V & shallow_mask)
    shift = max(0, height - width)
    deep = ((A >> shift) & shallow_mask, (V >> shift) & shallow_mask)
    return shallow + deep + (height & 15,)


def feature(state: State, order: int, rich: bool, endpoint_width: int) -> tuple[int, ...]:
    answer = []
    for word in variables(state, rich):
        answer.extend(hasse(word, k) for k in range(order + 1))
    answer.extend(endpoint_bits(state, endpoint_width))
    return tuple(answer)


def states_from_seeds(max_seed: int, max_follow: int) -> dict[State, Origin]:
    origins: dict[State, Origin] = {}
    for length in range(1, max_seed + 1):
        for seed in range(1 << length):
            state = seed_state(seed, length)
            for follow in range(max_follow + 1):
                origin = (length, seed, follow)
                old = origins.get(state)
                if old is None or origin < old:
                    origins[state] = origin
                nxt = forced_macro(0, state)
                if nxt is None:
                    break
                state = nxt
    return origins


def transition_signature(
    state: State, order: int, rich: bool, endpoint_width: int
) -> tuple[int, tuple[int, ...] | None]:
    pin, nxt = gray_macro(state)
    return pin, feature(nxt, order, rich, endpoint_width) if pin else None


def word_pair(state: State) -> tuple[str, str]:
    _, A, B = state
    V = 1 | (B << 1)
    height = max(A.bit_length(), V.bit_length())
    return (
        ''.join(str((A >> j) & 1) for j in range(height)),
        ''.join(str((V >> j) & 1) for j in range(height)),
    )


def first_collision(
    origins: dict[State, Origin],
    order: int,
    rich: bool,
    endpoint_width: int,
    require_same_length: bool = False,
) -> tuple[State, State] | None:
    seen: dict[object, State] = {}
    for state in sorted(origins, key=lambda item: origins[item]):
        summary = feature(state, order, rich, endpoint_width)
        key: object = (state[0], summary) if require_same_length else summary
        previous = seen.get(key)
        if previous is None:
            seen[key] = state
            continue
        if transition_signature(previous, order, rich, endpoint_width) != transition_signature(
            state, order, rich, endpoint_width
        ):
            return previous, state
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-seed', type=int, default=16)
    parser.add_argument('--max-follow', type=int, default=128)
    parser.add_argument('--max-order', type=int, default=8)
    parser.add_argument('--endpoint-width', type=int, default=2)
    args = parser.parse_args()

    hasse_checks = check_hasse_identity(16, args.max_order)
    macro_checks = check_gray_macro(8)
    obstructions = check_truncation_obstructions(args.max_order)
    print(f'Hasse quotient identity: {hasse_checks} exact word/order checks')
    print(f'Gray macro identity: {macro_checks} exact legal frontier checks')
    print('fixed-truncation obstruction words:')
    for order, before, after in obstructions:
        print(f'  K={order}: O={before:b}, Oprime={after:b}')

    origins = states_from_seeds(args.max_seed, args.max_follow)
    print(f'distinct exact finite-seed states: {len(origins)}')
    for rich in (False, True):
        label = 'base(A,V,A&V)' if not rich else 'degree<=3(A,V,Q(A|V),zA)'
        for order in range(args.max_order + 1):
            keys = {
                feature(state, order, rich, args.endpoint_width) for state in origins
            }
            collision = first_collision(origins, order, rich, args.endpoint_width)
            print(
                f'{label} K={order} endpoint={args.endpoint_width}: '
                f'{len(keys)} summaries; collision={collision is not None}'
            )
            if collision is not None:
                left, right = collision
                print(f'  left origin={origins[left]} state={left} words={word_pair(left)}')
                print(
                    f'  right origin={origins[right]} state={right} words={word_pair(right)}'
                )
                left_out = transition_signature(left, order, rich, args.endpoint_width)
                right_out = transition_signature(right, order, rich, args.endpoint_width)
                if left_out[0] != right_out[0]:
                    print(f'  pin outcomes={left_out[0]},{right_out[0]}')
                else:
                    assert left_out[1] is not None and right_out[1] is not None
                    differences = [
                        i for i, pair in enumerate(zip(left_out[1], right_out[1]))
                        if pair[0] != pair[1]
                    ]
                    print(
                        f'  both pin={left_out[0]}; successor summary differs at '
                        f'{differences[:12]}'
                    )

    collision = first_collision(
        origins, args.max_order, True, args.endpoint_width, require_same_length=True
    )
    print(f'rich K={args.max_order} equal-length collision={collision is not None}')
    if collision is not None:
        left, right = collision
        print(f'  left origin={origins[left]} state={left} words={word_pair(left)}')
        print(f'  right origin={origins[right]} state={right} words={word_pair(right)}')
        left_out = transition_signature(left, args.max_order, True, args.endpoint_width)
        right_out = transition_signature(right, args.max_order, True, args.endpoint_width)
        assert left_out[1] is not None and right_out[1] is not None
        differences = [
            i for i, pair in enumerate(zip(left_out[1], right_out[1]))
            if pair[0] != pair[1]
        ]
        print(f'  pins={left_out[0]},{right_out[0]}; differing successor indices={differences}')


if __name__ == '__main__':
    main()

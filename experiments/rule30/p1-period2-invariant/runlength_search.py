#!/usr/bin/env python3
"""Exact run-length/boundary-gap formulation and registered falsifiers."""

from __future__ import annotations

from carry_transducer import (
    State,
    active_symbols,
    gray_inverse,
    gray_macro,
    reachable_states,
)


def gray(word: int) -> int:
    return word ^ (word >> 1)


def boundary_gaps(word: int) -> tuple[int, ...]:
    """Colored RLE lengths; parity of tuple length is the shallow color."""
    boundaries = gray(word)
    result = []
    previous = -1
    position = 0
    while boundaries:
        if boundaries & 1:
            result.append(position - previous)
            previous = position
        boundaries >>= 1
        position += 1
    return tuple(result)


def from_boundary_gaps(gaps: tuple[int, ...]) -> int:
    boundaries = 0
    position = -1
    for gap in gaps:
        assert gap >= 1
        position += gap
        boundaries |= 1 << position
    return gray_inverse(boundaries)


def gaps_of_support(word: int) -> tuple[int, ...]:
    result = []
    previous = -1
    position = 0
    while word:
        if word & 1:
            result.append(position - previous)
            previous = position
        word >>= 1
        position += 1
    return tuple(result)


def run_macro(state: State) -> tuple[int, State]:
    T, A, B = state
    V = 1 | (B << 1)
    gaps_C = gaps_of_support(A | V)
    C = from_boundary_gaps(gaps_C)
    gaps_D = gaps_of_support(C | (A << 1))
    D = from_boundary_gaps(gaps_D)
    assert boundary_gaps(C) == gaps_C
    assert boundary_gaps(D) == gaps_D
    return len(gaps_D) & 1, (T + 2, D, C)


def check_word_bijection(length: int = 16) -> int:
    for word in range(1 << length):
        assert from_boundary_gaps(boundary_gaps(word)) == word
    return 1 << length


def check_macro(max_T: int = 8) -> int:
    checked = 0
    for T in range(2, max_T + 1, 2):
        for A in range(1 << T):
            for B in range(1 << (T - 1)):
                state = (T, A, B)
                assert run_macro(state) == gray_macro(state)
                checked += 1
    return checked


def check_run_expansion(max_length: int = 64) -> int:
    """A single solid OR-run of length m becomes m unit RLE digits."""
    for length in range(1, max_length + 1):
        solid = (1 << length) - 1
        image = gray_inverse(solid)
        assert boundary_gaps(image) == (1,) * length
    return max_length


def pair_gaps(state: State) -> tuple[tuple[int, ...], tuple[int, ...]]:
    _, A, B = state
    return boundary_gaps(A), boundary_gaps(1 | (B << 1))


def measures(state: State) -> tuple[int, ...]:
    left, right = pair_gaps(state)
    both = left + right
    height = max(sum(left), sum(right))
    return (
        len(left) + len(right),
        sum(gap - 1 for gap in both),
        sum(gap > 1 for gap in both),
        max(both, default=0),
        sum(gap * gap for gap in both),
        height,
    )


def bounded_gaps(gaps: tuple[int, ...], endpoint: int, cap: int, modulus: int) -> tuple[int, ...]:
    clipped = tuple(min(value, cap + 1) for value in gaps)
    first = clipped[:endpoint] + (0,) * max(0, endpoint - len(clipped))
    last = clipped[-endpoint:] if endpoint else ()
    last = (0,) * max(0, endpoint - len(last)) + last
    return (
        len(gaps) % modulus,
        sum(gaps) % modulus,
        sum(value > 1 for value in gaps) % modulus,
        *first,
        *last,
    )


def bounded_summary(
    state: State, endpoint: int = 4, cap: int = 32, modulus: int = 4
) -> tuple[int, ...]:
    _, A, B = state
    V = 1 | (B << 1)
    C = gray_inverse(A | V)
    D = gray_inverse(C | (A << 1))
    words = (A, V, C, D)
    result = []
    for word in words:
        result.extend(bounded_gaps(boundary_gaps(word), endpoint, cap, modulus))
    return tuple(result)


def first_summary_collision(
    origins: dict[State, tuple[int, int, int]], require_same_T: bool
) -> tuple[State, State] | None:
    seen: dict[object, State] = {}
    for state in sorted(origins, key=lambda value: origins[value]):
        pin, nxt = gray_macro(state)
        if pin == 0:
            continue
        summary = bounded_summary(state)
        key: object = (state[0], summary) if require_same_T else summary
        previous = seen.get(key)
        if previous is None:
            seen[key] = state
            continue
        previous_next = gray_macro(previous)[1]
        left_signature = (bounded_summary(previous_next), gray_macro(previous_next)[0])
        right_signature = (bounded_summary(nxt), gray_macro(nxt)[0])
        if left_signature != right_signature:
            return previous, state
    return None


def first_next_pin_collision(
    origins: dict[State, tuple[int, int, int]], require_same_T: bool
) -> tuple[State, State] | None:
    seen: dict[object, tuple[int, State]] = {}
    for state in sorted(origins, key=lambda value: origins[value]):
        pin, nxt = gray_macro(state)
        if pin == 0:
            continue
        summary = bounded_summary(state)
        key: object = (state[0], summary) if require_same_T else summary
        next_pin = gray_macro(nxt)[0]
        previous = seen.get(key)
        if previous is not None and previous[0] != next_pin:
            return previous[1], state
        seen.setdefault(key, (next_pin, state))
    return None


def first_metric_counterexamples(
    origins: dict[State, tuple[int, int, int]]
) -> list[tuple[str, State | None, State | None, int, int]]:
    names = ('boundary_count', 'excess', 'nonunit_count', 'max_gap', 'square_sum', 'height')
    transitions = []
    for state in sorted(origins, key=lambda value: origins[value]):
        pin, nxt = gray_macro(state)
        if pin:
            transitions.append((state, nxt))
    result = []
    for index, name in enumerate(names):
        increase = next(
            ((before, after) for before, after in transitions if measures(after)[index] > measures(before)[index]),
            None,
        )
        decrease = next(
            ((before, after) for before, after in transitions if measures(after)[index] < measures(before)[index]),
            None,
        )
        result.append(
            (
                name,
                increase[0] if increase else None,
                decrease[0] if decrease else None,
                0 if increase is None else measures(increase[1])[index] - measures(increase[0])[index],
                0 if decrease is None else measures(decrease[1])[index] - measures(decrease[0])[index],
            )
        )
    return result


def lex_counterexamples(origins: dict[State, tuple[int, int, int]]) -> None:
    orders = {
        'shallow': lambda state: pair_gaps(state),
        'deep': lambda state: tuple(tuple(reversed(gaps)) for gaps in pair_gaps(state)),
        'sorted': lambda state: tuple(tuple(sorted(gaps)) for gaps in pair_gaps(state)),
    }
    transitions = []
    for state in sorted(origins, key=lambda value: origins[value]):
        pin, nxt = gray_macro(state)
        if pin:
            transitions.append((state, nxt))
    for name, key in orders.items():
        increase = next((pair for pair in transitions if key(pair[1]) > key(pair[0])), None)
        decrease = next((pair for pair in transitions if key(pair[1]) < key(pair[0])), None)
        print(
            f'lex {name}: increase origin='
            f'{None if increase is None else origins[increase[0]]}; decrease origin='
            f'{None if decrease is None else origins[decrease[0]]}'
        )


def rule30_step(config: set[int]) -> set[int]:
    if not config:
        return set()
    return {
        position
        for position in range(min(config) - 1, max(config) + 2)
        if (position - 1 in config) ^ ((position in config) or (position + 1 in config))
    }


def colored_row(config: set[int]) -> tuple[int, tuple[int, ...]]:
    assert config
    left, right = min(config), max(config)
    runs = []
    color = True  # the active finite interval starts with a black cell
    length = 0
    for position in range(left, right + 1):
        value = position in config
        if value == color:
            length += 1
        else:
            runs.append(length)
            color = value
            length = 1
    runs.append(length)
    assert len(runs) & 1  # the active interval also ends black
    return left, tuple(runs)


def adversarial_digit_pyramid() -> list[tuple[int, int, tuple[int, ...]]]:
    config = {-8, -1, 6}
    result = []
    trace = []
    for time in range(16):
        left, runs = colored_row(config)
        result.append((time, left, runs))
        trace.append(int(0 in config))
        config = rule30_step(config)
    assert all(trace[time] == (time & 1) for time in range(15))
    assert trace[15] != (15 & 1)
    return result


def main() -> None:
    print(f'RLE/word bijection: {check_word_bijection()} words PASS')
    print(f'RLE macro crosscheck: {check_macro()} exact frontiers PASS')
    print(f'one-run to unit-digit expansion: m=1..{check_run_expansion()} PASS')
    origins = reachable_states(16, 128)
    print(f'distinct reachable states: {len(origins)}')
    print('collapsed adversarial pyramid (offset; B-starting alternating run digits):')
    for time, left, runs in adversarial_digit_pyramid():
        print(f'  t={time:2d} offset={left:+d} digits={runs}')
    for name, increase, decrease, up_delta, down_delta in first_metric_counterexamples(origins):
        print(
            f'{name}: increase origin={None if increase is None else origins[increase]} '
            f'delta={up_delta}; decrease origin='
            f'{None if decrease is None else origins[decrease]} delta={down_delta}'
        )
    lex_counterexamples(origins)
    for same_T in (False, True):
        collision = first_summary_collision(origins, same_T)
        print(f'bounded RLE closure collision same_T={same_T}: {collision is not None}')
        if collision:
            left, right = collision
            print(f'  left origin={origins[left]} state={left} gaps={pair_gaps(left)}')
            print(f'  right origin={origins[right]} state={right} gaps={pair_gaps(right)}')
            left_next = gray_macro(left)[1]
            right_next = gray_macro(right)[1]
            print(
                f'  next pins={gray_macro(left_next)[0]},{gray_macro(right_next)[0]}; '
                f'next summaries equal='
                f'{bounded_summary(left_next) == bounded_summary(right_next)}'
            )
        pin_collision = first_next_pin_collision(origins, same_T)
        print(
            f'bounded RLE next-pin collision same_T={same_T}: '
            f'{pin_collision is not None}'
        )
        if pin_collision:
            left, right = pin_collision
            left_next = gray_macro(left)[1]
            right_next = gray_macro(right)[1]
            print(f'  left origin={origins[left]} state={left} gaps={pair_gaps(left)}')
            print(f'  right origin={origins[right]} state={right} gaps={pair_gaps(right)}')
            print(f'  next pins={gray_macro(left_next)[0]},{gray_macro(right_next)[0]}')


if __name__ == '__main__':
    main()

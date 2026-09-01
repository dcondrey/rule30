#!/usr/bin/env python3
"""Exact right-column hard-core constraint and finite-seed falsification."""

from __future__ import annotations

from carry_transducer import (
    State,
    forced_macro,
    gray_macro,
    parity_or,
    seed_state,
    word_action,
)


def rule30(left: int, center: int, right: int) -> int:
    return left ^ (center | right)


def rule90(left: int, center: int, right: int) -> int:
    del center
    return left ^ right


def two_phase_neighbor(
    rho: int, q_even: int, q_odd: int, rule=rule30
) -> int:
    odd_neighbor = rule(0, rho, q_even)
    return rule(1, odd_neighbor, q_odd)


def hardcore_formula(rho: int, q_even: int, q_odd: int) -> int:
    return (1 ^ rho) & (1 ^ q_even) & (1 ^ q_odd)


def check_local_identity() -> tuple[int, tuple[int, int, int] | None]:
    checked = 0
    for rho in (0, 1):
        for q_even in (0, 1):
            for q_odd in (0, 1):
                assert two_phase_neighbor(rho, q_even, q_odd) == hardcore_formula(
                    rho, q_even, q_odd
                )
                checked += 1
    xor_counterexample = next(
        (
            (rho, q_even, q_odd)
            for rho in (0, 1)
            for q_even in (0, 1)
            for q_odd in (0, 1)
            if rho == 1 and two_phase_neighbor(rho, q_even, q_odd, rule90) == 1
        ),
        None,
    )
    return checked, xor_counterexample


def update(row: set[int], rule=rule30) -> set[int]:
    if not row:
        return set()
    return {
        index
        for index in range(min(row) - 1, max(row) + 2)
        if rule(index - 1 in row, index in row, index + 1 in row)
    }


def adversarial_control() -> tuple[tuple[int, ...], int]:
    row = {-8, -1, 6}
    columns = []
    for time in range(16):
        columns.append((int(0 in row), int(1 in row), int(2 in row)))
        row = update(row)
    assert all(columns[time][0] == (time & 1) for time in range(15))
    assert columns[15][0] != (15 & 1)
    rho = tuple(columns[time][1] for time in range(0, 15, 2))
    checked = 0
    for k in range(7):
        _, current, q_even = columns[2 * k]
        _, _, q_odd = columns[2 * k + 1]
        following = columns[2 * k + 2][1]
        assert following == hardcore_formula(current, q_even, q_odd)
        assert not (current == following == 1)
        checked += 1
    return rho, checked


def hard_core(seed: int) -> bool:
    return (seed & (seed >> 1)) == 0


def forced_rho(state: State) -> int:
    # At a zero phase, zero output forces v=parity(OR word), while v=NOT rho.
    return 1 ^ parity_or(state)


def hard_core_survival(seed: int, length: int, cap: int = 128) -> tuple[int, str, State]:
    assert hard_core(seed)
    state = seed_state(seed, length)
    previous_rho = (seed >> (length - 1)) & 1
    accepted = 0
    for _ in range(cap):
        rho = forced_rho(state)
        if previous_rho == rho == 1:
            return accepted, 'hard-core', state
        next_state = forced_macro(state)
        if next_state is None:
            return accepted, 'pin', state
        accepted += 1
        previous_rho = rho
        state = next_state
    return accepted, 'cap', state


def exhaustive_hard_core(max_length: int = 16, cap: int = 128) -> list[dict[str, object]]:
    result = []
    for length in range(1, max_length + 1):
        seeds = [seed for seed in range(1 << length) if hard_core(seed)]
        records = [(hard_core_survival(seed, length, cap), seed) for seed in seeds]
        maximum = max(record[0][0] for record in records)
        witnesses = [
            (seed, outcome, final)
            for (survival, outcome, final), seed in records
            if survival == maximum
        ]
        result.append(
            {
                'length': length,
                'seeds': len(seeds),
                'maximum': maximum,
                'witness': min(witnesses, key=lambda value: value[0]),
                'caps': sum(outcome == 'cap' for (_, outcome, _), _ in records),
            }
        )
    return result


def first_action_closure_collision(
    max_length: int = 16, cap: int = 128
) -> tuple[object, ...] | None:
    """Test summary (previous rho, D8 word action) on legal hard-core paths."""
    seen: dict[object, tuple[object, ...]] = {}
    for length in range(1, max_length + 1):
        for seed in range(1 << length):
            if not hard_core(seed):
                continue
            state = seed_state(seed, length)
            previous_rho = (seed >> (length - 1)) & 1
            for follow in range(cap + 1):
                rho = forced_rho(state)
                pin, next_state = gray_macro(state)
                key = previous_rho, word_action(state)
                signature = rho, pin, word_action(next_state)
                origin = length, seed, follow
                previous = seen.get(key)
                if previous is not None and previous[0] != signature:
                    return key, previous, (signature, origin, state)
                seen.setdefault(key, (signature, origin, state))
                if previous_rho == rho == 1 or pin == 0:
                    break
                previous_rho = rho
                state = next_state
    return None


def main() -> None:
    checked, xor_counterexample = check_local_identity()
    assert xor_counterexample is not None
    print(f'Rule 30 right-column identity: {checked}/8 PASS')
    print(
        'Rule 90 no-11 implication fails at '
        f'(rho,q_even,q_odd)={xor_counterexample}'
    )
    rho, adversarial_checks = adversarial_control()
    print(
        f'adversarial rho through t=14: {rho}; '
        f'{adversarial_checks}/7 hard-core macro identities PASS'
    )
    rows = exhaustive_hard_core()
    print('length hard-core-seeds max-post-seed-survival witness outcome caps')
    for row in rows:
        seed, outcome, _ = row['witness']
        print(
            f"{row['length']:2d} {row['seeds']:5d} {row['maximum']:3d} "
            f"{seed:#x} {outcome} {row['caps']}"
        )
    collision = first_action_closure_collision()
    assert collision is not None
    key, old, new = collision
    print(f'action-summary closure collision key={key}')
    print(f'  first signature/origin/state={old}')
    print(f'  second signature/origin/state={new}')


if __name__ == '__main__':
    main()

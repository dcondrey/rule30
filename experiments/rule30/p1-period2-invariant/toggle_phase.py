#!/usr/bin/env python3
"""Exact odd-row color-toggle recoding of an alternating Rule 30 trace."""

from __future__ import annotations

from itertools import product


def rule30(left: int, center: int, right: int) -> int:
    return left ^ (center | right)


def toggled_rule(phase: int, left: int, center: int, right: int) -> int:
    """Update z_t=x_t XOR phase to z_(t+1), where phase=t mod 2."""
    return rule30(left ^ phase, center ^ phase, right ^ phase) ^ phase ^ 1


def displayed_formula(phase: int, left: int, center: int, right: int) -> int:
    if phase == 0:
        return 1 ^ left ^ (center | right)
    return left ^ (center & right)


def two_phase_center(bits: tuple[int, int, int, int, int]) -> int:
    first = tuple(toggled_rule(0, *bits[index:index + 3]) for index in range(3))
    return toggled_rule(1, *first)


def rule30_squared_center(bits: tuple[int, int, int, int, int]) -> int:
    first = tuple(rule30(*bits[index:index + 3]) for index in range(3))
    return rule30(*first)


def update(row: set[int]) -> set[int]:
    if not row:
        return set()
    result = set()
    for index in range(min(row) - 1, max(row) + 2):
        if rule30(index - 1 in row, index in row, index + 1 in row):
            result.add(index)
    return result


def main() -> None:
    checked_local = 0
    for phase, left, center, right in product((0, 1), repeat=4):
        assert toggled_rule(phase, left, center, right) == displayed_formula(
            phase, left, center, right
        )
        checked_local += 1

    checked_two_phase = 0
    for bits in product((0, 1), repeat=5):
        assert two_phase_center(bits) == rule30_squared_center(bits)
        checked_two_phase += 1

    row = {-8, -1, 6}
    toggled_centers = []
    raw_centers = []
    for time in range(16):
        raw = int(0 in row)
        raw_centers.append(raw)
        toggled_centers.append(raw ^ (time & 1))
        row = update(row)
    assert raw_centers[:15] == [time & 1 for time in range(15)]
    assert toggled_centers[:15] == [0] * 15
    assert toggled_centers[15] == 1

    print(f'phase/local identities: {checked_local}/16 PASS')
    print(f'two-phase equals F^2: {checked_two_phase}/32 PASS')
    print('adversarial toggled center: zero through t=14, one at t=15 PASS')
    print('phase 0 rule: 1 XOR left XOR (center OR right)')
    print('phase 1 rule: left XOR (center AND right)')


if __name__ == '__main__':
    main()

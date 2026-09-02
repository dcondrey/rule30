#!/usr/bin/env python3
"""Bounded falsifier for pull-row projected diagonal support.

This keeps the complete zero-prefix scenario family.  It tests only
nonfinal rows whose original forced endpoint transition is ``1 -> 2`` (a
productive queue pull).  A finite pass is evidence, not an all-length proof.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from constant_tail_bitsliced_derivative import (
    bitsliced_trace_states,
    scenario_state,
)
from constant_tail_holonomy_defect_closure import scenario_rows
from constant_tail_right_zero_prefix_selector import SELECTED_COORDINATES
from constant_tail_scale import Vector, hard_core_extension_length
from constant_tail_zero_prefix_bitsliced import (
    adjacent_scenarios_differ,
    zero_prefix_word_states,
)
from rank_zero_separator import hard_core_prefixes


@dataclass(slots=True)
class Census:
    cases: int = 0
    pull_rows: int = 0
    projected_failures: int = 0
    alpha_failures: int = 0
    diagonal_failures: int = 0
    maximum_first_displacement: int = 0
    first_projected_failure: str | None = None
    first_alpha_failure: str | None = None
    first_diagonal_failure: str | None = None


def alpha_parity_controls(max_length: int) -> int:
    """Check the exact activity-parity formula on literal raw queues."""

    checked = 0
    for length in range(1, max_length + 1):
        for word in hard_core_prefixes(length):
            for tail in (2, 3):
                for zero_prefix in range(length + 1):
                    for row in scenario_rows(word, zero_prefix, tail):
                        parity = sum(symbol != 0 for symbol in row.queue[1:]) & 1
                        expected = 1 ^ int(row.previous != 0) ^ parity
                        assert row.affine.alpha == expected
                        # Both constant tails have high bit one.  Inverting
                        # the affine map therefore forces endpoint high bit
                        # 1+alpha, independently of beta and gamma.
                        assert row.forced >> 1 == 1 ^ row.affine.alpha
                        if row.previous in (1, 2):
                            assert row.affine.alpha == parity
                        checked += 1
    return checked


def scenario_extension(
    word: Vector, tail: int
) -> tuple[Vector, tuple[tuple[int, int, int], ...], int]:
    """Compute the affine scenarios and original extension once."""

    states, mask = zero_prefix_word_states(word)
    extension, affines = bitsliced_trace_states(
        states, len(word), tail, mask
    )
    original = tuple(scenario_state(state, 0) for state in extension)
    survival = hard_core_extension_length(word, original)
    return original, affines, survival


def audit_word(word: Vector, tail: int, census: Census) -> None:
    extension, affines, survival = scenario_extension(word, tail)
    coordinates = SELECTED_COORDINATES[tail]
    previous = word[-1]
    census.cases += 1
    for row in range(survival):
        following = extension[row]
        pull = previous == 1 and following == 2
        # Only nonfinal rows are needed for an immortal continuation.
        if pull and row + 1 < survival:
            census.pull_rows += 1
            alpha_edges = {
                token
                for token in range(len(word))
                if adjacent_scenarios_differ(affines[row][0], token)
            }
            projected_edges = {
                token
                for token in range(len(word))
                if any(
                    adjacent_scenarios_differ(
                        affines[row][coordinate], token
                    )
                    for coordinate in coordinates
                )
            }
            witnesses = sorted(token for token in projected_edges if token >= row)
            alpha_witnesses = sorted(
                token for token in alpha_edges if token >= row
            )
            description = (
                f"tail={tail} W={''.join(map(str, word))} n={len(word)} "
                f"survival={survival} row={row} "
                f"projected-edges={sorted(projected_edges)} "
                f"alpha-edges={sorted(alpha_edges)}"
            )
            if not witnesses:
                census.projected_failures += 1
                if census.first_projected_failure is None:
                    census.first_projected_failure = description
            else:
                census.maximum_first_displacement = max(
                    census.maximum_first_displacement, witnesses[0] - row
                )
            if not alpha_witnesses:
                census.alpha_failures += 1
                if census.first_alpha_failure is None:
                    census.first_alpha_failure = description
            if row >= len(word) or row not in projected_edges:
                census.diagonal_failures += 1
                if census.first_diagonal_failure is None:
                    census.first_diagonal_failure = description
        previous = following


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first-length", type=int, default=1)
    parser.add_argument("--last-length", type=int, default=23)
    parser.add_argument("--parity-control-length", type=int, default=6)
    args = parser.parse_args()
    if not 1 <= args.first_length <= args.last_length:
        parser.error("length bounds must satisfy 1 <= first <= last")
    if args.parity_control_length < 0:
        parser.error("parity control length must be nonnegative")

    checked = alpha_parity_controls(args.parity_control_length)
    print(f"alpha/activity-parity controls: {checked} row states PASS")

    census = Census()
    for length in range(args.first_length, args.last_length + 1):
        before = (
            census.cases,
            census.pull_rows,
            census.projected_failures,
            census.alpha_failures,
            census.diagonal_failures,
        )
        for word in hard_core_prefixes(length):
            for tail in (2, 3):
                audit_word(word, tail, census)
        print(
            f"length={length:2d} cases={census.cases-before[0]:6d} "
            f"pull-rows={census.pull_rows-before[1]:6d} "
            f"projected-failures={census.projected_failures-before[2]:4d} "
            f"alpha-failures={census.alpha_failures-before[3]:4d} "
            f"diagonal-failures={census.diagonal_failures-before[4]:4d}",
            flush=True,
        )

    print(
        f"TOTAL cases={census.cases} pull-rows={census.pull_rows} "
        f"projected-failures={census.projected_failures} "
        f"alpha-failures={census.alpha_failures} "
        f"diagonal-failures={census.diagonal_failures} "
        f"maximum-first-displacement={census.maximum_first_displacement}"
    )
    print(
        "first alpha failure: "
        f"{census.first_alpha_failure or 'none'}"
    )
    print(
        "first projected failure: "
        f"{census.first_projected_failure or 'none'}"
    )
    print(
        "first diagonal failure: "
        f"{census.first_diagonal_failure or 'none'}"
    )
    if census.projected_failures or census.alpha_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

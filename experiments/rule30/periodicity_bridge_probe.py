"""Falsification probes for bridges from two-column to center nonperiodicity.

Kopra's width-two trace theorem is close to Rule 30 Prize Problem 1, but it
does not imply that the center column alone is nonperiodic.  This module makes
several tempting bridge claims executable before they are sent to a model or
scaled in the cloud:

* nonlinearity does not rescue the whole left-permutive ECA class;
* a time shift can agree at the center for a long finite interval while an
  adjacent column disagrees;
* the center trace does not identify a finite initial configuration; and
* the exact Rule 30 time-shift defect identity is checked independently.

All reported agreement lengths are finite counterexamples, never evidence of
eventual periodicity or nonperiodicity.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Iterable, Sequence


RULE_30 = 30
RULE_90 = 90


def rule_from_left_permutive_residual(residual: int) -> int:
    """Return the ECA rule f(a,b,c)=a XOR g(b,c), with g encoded by residual."""
    if residual < 0 or residual > 15:
        raise ValueError("the two-input residual must be in [0, 15]")
    rule = 0
    for left in (0, 1):
        for center in (0, 1):
            for right in (0, 1):
                neighborhood = (left << 2) | (center << 1) | right
                output = left ^ ((residual >> ((center << 1) | right)) & 1)
                rule |= output << neighborhood
    return rule


def residual_is_nonlinear(residual: int) -> bool:
    """Whether the algebraic normal form of the two-input residual has bc."""
    if residual < 0 or residual > 15:
        raise ValueError("the two-input residual must be in [0, 15]")
    return residual.bit_count() % 2 == 1


def evolve_rows(
    rule: int,
    max_time: int,
    initial_offsets: Iterable[int] = (0,),
) -> tuple[list[int], int]:
    """Return exact, zero-padded ECA rows and the packed center-bit index."""
    if rule < 0 or rule > 255:
        raise ValueError("rule must be an ECA number")
    if max_time < 0:
        raise ValueError("max_time must be non-negative")
    offsets = tuple(initial_offsets)
    if any(abs(offset) > max_time + 1 for offset in offsets):
        raise ValueError("initial offsets exceed the allocated causal window")

    center = max_time + 2
    width = 2 * max_time + 5
    mask = (1 << width) - 1
    row = sum(1 << (center + offset) for offset in offsets)
    rows = [row]
    for _ in range(max_time):
        left = (row << 1) & mask
        middle = row
        right = row >> 1
        next_row = 0
        for neighborhood in range(8):
            if not ((rule >> neighborhood) & 1):
                continue
            term = mask
            for source, flag in ((left, 4), (middle, 2), (right, 1)):
                term &= source if neighborhood & flag else (~source & mask)
            next_row |= term
        row = next_row & mask
        rows.append(row)
    return rows, center


def cell(rows: Sequence[int], center: int, time: int, position: int) -> int:
    return (rows[time] >> (center + position)) & 1


def center_trace(rows: Sequence[int], center: int) -> tuple[int, ...]:
    return tuple((row >> center) & 1 for row in rows)


def observed_constant_tail_start(values: Sequence[int]) -> int:
    """Start of the final constant suffix in a finite sample."""
    if not values:
        raise ValueError("values must not be empty")
    start = len(values) - 1
    while start > 0 and values[start - 1] == values[-1]:
        start -= 1
    return start


@dataclass(frozen=True)
class LeftPermutiveObservation:
    residual_bits: str
    rule: int
    nonlinear: bool
    center_prefix: str
    observed_constant_tail_start: int
    observed_constant_value: int


def classify_left_permutive_quiescent(
    max_time: int = 512,
) -> list[LeftPermutiveObservation]:
    """Classify f=a XOR g(b,c) with quiescent zero (g(0,0)=0)."""
    observations = []
    for residual in range(0, 16, 2):
        rule = rule_from_left_permutive_residual(residual)
        rows, center = evolve_rows(rule, max_time)
        trace = center_trace(rows, center)
        observations.append(
            LeftPermutiveObservation(
                residual_bits=f"{residual:04b}",
                rule=rule,
                nonlinear=residual_is_nonlinear(residual),
                center_prefix="".join(map(str, trace[:16])),
                observed_constant_tail_start=observed_constant_tail_start(trace),
                observed_constant_value=trace[-1],
            )
        )
    return observations


@dataclass(frozen=True)
class AgreementRun:
    rule: int
    shift: int
    start_time: int
    length: int
    left_defect_seen: bool
    right_defect_seen: bool


def longest_center_agreement(
    rule: int,
    horizon: int,
    max_shift: int,
) -> AgreementRun:
    """Find the longest sampled run with s(t,0)=s(t+p,0)."""
    if max_shift < 1 or max_shift > horizon:
        raise ValueError("max_shift must lie in [1, horizon]")
    rows, center = evolve_rows(rule, horizon)
    best = AgreementRun(rule, 1, 0, 0, False, False)
    for shift in range(1, max_shift + 1):
        run_start = 0
        run_length = 0
        left_defect_seen = False
        right_defect_seen = False
        for time in range(horizon - shift + 1):
            if cell(rows, center, time, 0) == cell(rows, center, time + shift, 0):
                if run_length == 0:
                    run_start = time
                    left_defect_seen = False
                    right_defect_seen = False
                run_length += 1
                left_defect_seen |= (
                    cell(rows, center, time, -1)
                    != cell(rows, center, time + shift, -1)
                )
                right_defect_seen |= (
                    cell(rows, center, time, 1)
                    != cell(rows, center, time + shift, 1)
                )
                if run_length > best.length:
                    best = AgreementRun(
                        rule,
                        shift,
                        run_start,
                        run_length,
                        left_defect_seen,
                        right_defect_seen,
                    )
            else:
                run_length = 0
    return best


def defect_identity_violations(rule: int, horizon: int, shift: int) -> list[int]:
    """Check the Rule 30 identity under two consecutive center equalities.

    With D_t(x)=s(t+p,x) XOR s(t,x), D_t(0)=D_(t+1)(0)=0 implies

        D_t(-1) = (1 XOR s(t,0)) D_t(1).
    """
    if shift < 1 or shift >= horizon:
        raise ValueError("shift must lie in [1, horizon)")
    rows, center = evolve_rows(rule, horizon)
    violations = []
    for time in range(horizon - shift):
        center_defect = cell(rows, center, time + shift, 0) ^ cell(rows, center, time, 0)
        next_center_defect = (
            cell(rows, center, time + shift + 1, 0)
            ^ cell(rows, center, time + 1, 0)
        )
        if center_defect or next_center_defect:
            continue
        left_defect = cell(rows, center, time + shift, -1) ^ cell(rows, center, time, -1)
        right_defect = cell(rows, center, time + shift, 1) ^ cell(rows, center, time, 1)
        expected = (1 ^ cell(rows, center, time, 0)) & right_defect
        if left_defect != expected:
            violations.append(time)
    return violations


def first_doubling_separation_counterexample(max_shift: int) -> int | None:
    """First p refuting the tempting claim s(p,0) != s(2p,0)."""
    if max_shift < 1:
        raise ValueError("max_shift must be positive")
    rows, center = evolve_rows(RULE_30, 2 * max_shift)
    for shift in range(1, max_shift + 1):
        if cell(rows, center, shift, 0) == cell(rows, center, 2 * shift, 0):
            return shift
    return None


def trace_collision_holds(horizon: int) -> bool:
    """Check the seed and seed-plus-right-neighbor center-trace collision."""
    seed, center = evolve_rows(RULE_30, horizon, (0,))
    perturbed, other_center = evolve_rows(RULE_30, horizon, (0, 1))
    if center != other_center:
        raise AssertionError("packed windows unexpectedly disagree")
    return center_trace(seed, center) == center_trace(perturbed, center)


def moving_collision_defect_holds(horizon: int) -> bool:
    """Check the exact observed moving defect behind the trace collision.

    At even t the configurations differ only at t+1; at odd t they differ at
    t and t+1.  This is an induction target, not merely a center-prefix match.
    """
    seed, center = evolve_rows(RULE_30, horizon, (0,))
    perturbed, _ = evolve_rows(RULE_30, horizon, (0, 1))
    for time, (base_row, changed_row) in enumerate(zip(seed, perturbed)):
        observed = base_row ^ changed_row
        positions = (time + 1,) if time % 2 == 0 else (time, time + 1)
        expected = sum(1 << (center + position) for position in positions)
        if observed != expected:
            return False
    return True


def build_report(horizon: int, max_shift: int) -> dict[str, object]:
    return {
        "horizon": horizon,
        "max_shift": max_shift,
        "left_permutive_quiescent": [
            asdict(observation)
            for observation in classify_left_permutive_quiescent(min(horizon, 512))
        ],
        "longest_center_agreement": {
            "rule30": asdict(longest_center_agreement(RULE_30, horizon, max_shift)),
            "rule90_control": asdict(longest_center_agreement(RULE_90, horizon, max_shift)),
        },
        "rule30_defect_identity_violations": defect_identity_violations(
            RULE_30, horizon, max_shift
        ),
        "first_doubling_separation_counterexample": first_doubling_separation_counterexample(
            max_shift
        ),
        "seed_plus_right_center_collision": trace_collision_holds(horizon),
        "seed_plus_right_moving_defect": moving_collision_defect_holds(horizon),
        "interpretation": (
            "Finite agreement runs are counterexamples to bounded bridge claims only; "
            "they do not establish eventual behavior."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--horizon", type=int, default=4096)
    parser.add_argument("--max-shift", type=int, default=256)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report(args.horizon, args.max_shift)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return

    print("left-permutive, quiescent-zero ECA observations")
    for item in report["left_permutive_quiescent"]:
        print(
            f"g={item['residual_bits']} rule={item['rule']:3d} "
            f"nonlinear={int(item['nonlinear'])} prefix={item['center_prefix']} "
            f"sampled_constant_tail={item['observed_constant_tail_start']}"
        )
    print("longest sampled center agreements")
    for name, item in report["longest_center_agreement"].items():
        print(
            f"{name}: length={item['length']} shift={item['shift']} "
            f"start={item['start_time']} left_defect={item['left_defect_seen']} "
            f"right_defect={item['right_defect_seen']}"
        )
    print(
        "first counterexample to s(p,0) != s(2p,0): "
        f"p={report['first_doubling_separation_counterexample']}"
    )
    print(
        "defect identity violations: "
        f"{len(report['rule30_defect_identity_violations'])}"
    )
    print(
        "seed/right-neighbor trace collision: "
        f"{report['seed_plus_right_center_collision']} "
        f"moving-defect certificate={report['seed_plus_right_moving_defect']}"
    )


if __name__ == "__main__":
    main()

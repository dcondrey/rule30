"""Exact inverse-trace probes for the Rule 30 center-column problem.

For a left-permutive elementary cellular automaton, a desired center trace and
the initial right half uniquely determine the initial left half.  At depth k,
the as-yet unknown cell at -k reaches the center through the unique fastest
path, so changing that cell flips the center at time k and cannot affect any
earlier center value.

This module uses that triangular inverse map in two ways:

* independently reconstruct finite configurations from their actual traces;
* translate a proposed periodic continuation of the Rule 30 center into the
  spatial cells it would force at a chosen orbit time.

Finite reconstruction failures are exact counterexamples to a proposed
periodic continuation.  Long successful prefixes are not evidence that the
center is eventually periodic.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Iterable, Sequence

from periodicity_bridge_probe import RULE_30, RULE_90, cell, evolve_rows


def is_left_permutive(rule: int) -> bool:
    """Return whether f(0,b,c) differs from f(1,b,c) for every b,c."""
    if rule < 0 or rule > 255:
        raise ValueError("rule must be an ECA number")
    for center in (0, 1):
        for right in (0, 1):
            low = (rule >> ((center << 1) | right)) & 1
            high = (rule >> (4 | (center << 1) | right)) & 1
            if low == high:
                return False
    return True


def evolve_once_packed(rule: int, row: int, mask: int) -> int:
    """Evolve one exact zero-padded packed row."""
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
    return next_row & mask


def center_after(rule: int, row: int, center: int, mask: int, steps: int) -> int:
    """Return the center cell after ``steps`` exact evolutions."""
    for _ in range(steps):
        row = evolve_once_packed(rule, row, mask)
    return (row >> center) & 1


def reconstruct_left(
    rule: int,
    desired_center_trace: Sequence[int],
    initial_right: Sequence[int],
) -> tuple[int, ...]:
    """Reconstruct cells -1, -2, ... from a trace and cells 0, 1, ... .

    ``desired_center_trace[k]`` is the desired center value at time k and
    ``initial_right[x]`` is the initial value at position x.  Both sequences
    must have the same nonzero length.  The returned tuple has one fewer item
    because the time-zero center already fixes position zero.
    """
    if not is_left_permutive(rule):
        raise ValueError("inverse trace reconstruction requires a left-permutive rule")
    if not desired_center_trace:
        raise ValueError("desired_center_trace must not be empty")
    if len(initial_right) != len(desired_center_trace):
        raise ValueError("initial_right and desired_center_trace must have equal length")
    if any(bit not in (0, 1) for bit in desired_center_trace):
        raise ValueError("desired_center_trace must contain only bits")
    if any(bit not in (0, 1) for bit in initial_right):
        raise ValueError("initial_right must contain only bits")
    if desired_center_trace[0] != initial_right[0]:
        raise ValueError("the time-zero center must equal initial_right[0]")

    horizon = len(desired_center_trace) - 1
    center = horizon + 2
    width = 2 * horizon + 5
    mask = (1 << width) - 1
    initial_row = 0
    for position, bit in enumerate(initial_right):
        initial_row |= bit << (center + position)

    reconstructed: list[int] = []
    for depth in range(1, horizon + 1):
        with_zero = center_after(rule, initial_row, center, mask, depth)
        forced = with_zero ^ desired_center_trace[depth]
        reconstructed.append(forced)
        initial_row |= forced << (center - depth)
    return tuple(reconstructed)


def trace_from_halves(
    rule: int,
    left: Sequence[int],
    right: Sequence[int],
) -> tuple[int, ...]:
    """Evolve a finite two-sided row and return its center trace.

    ``left[k-1]`` is position -k and ``right[x]`` is position x.
    """
    horizon = len(left)
    if len(right) != horizon + 1:
        raise ValueError("right must contain exactly len(left) + 1 cells")
    center = horizon + 2
    width = 2 * horizon + 5
    mask = (1 << width) - 1
    row = 0
    for depth, bit in enumerate(left, start=1):
        row |= bit << (center - depth)
    for position, bit in enumerate(right):
        row |= bit << (center + position)
    trace = [(row >> center) & 1]
    for _ in range(horizon):
        row = evolve_once_packed(rule, row, mask)
        trace.append((row >> center) & 1)
    return tuple(trace)


@dataclass(frozen=True)
class PeriodicReconstructionCertificate:
    rule: int
    base_time: int
    period: int
    horizon: int
    agreement_after_first_period: int
    first_temporal_mismatch: int | None
    first_spatial_mismatch: int | None
    first_forced_one_outside_actual_support: int | None


def periodic_reconstruction_certificate(
    rule: int,
    base_time: int,
    period: int,
    horizon: int,
    initial_offsets: Iterable[int] = (0,),
) -> PeriodicReconstructionCertificate:
    """Test the periodic continuation anchored at one actual orbit time.

    The period word is the actual center block at times
    ``base_time .. base_time + period - 1``.  The inverse map is based at the
    actual row at ``base_time``.  For a finite initial seed, the actual row is
    zero outside its causal support; a forced one there is therefore a direct
    spatial contradiction to that continuation.
    """
    if base_time < 0:
        raise ValueError("base_time must be non-negative")
    if period < 1:
        raise ValueError("period must be positive")
    if horizon < period:
        raise ValueError("horizon must be at least one period")
    offsets = tuple(initial_offsets)
    if not offsets:
        raise ValueError("initial_offsets must not be empty")
    support_radius = max(abs(offset) for offset in offsets) + base_time

    rows, center = evolve_rows(rule, base_time + horizon, offsets)
    actual_trace = tuple(
        cell(rows, center, base_time + depth, 0) for depth in range(horizon + 1)
    )
    word = actual_trace[:period]
    desired = tuple(word[depth % period] for depth in range(horizon + 1))
    right = tuple(
        cell(rows, center, base_time, position) for position in range(horizon + 1)
    )
    forced_left = reconstruct_left(rule, desired, right)
    actual_left = tuple(
        cell(rows, center, base_time, -depth) for depth in range(1, horizon + 1)
    )

    temporal = next(
        (depth for depth, pair in enumerate(zip(desired, actual_trace)) if pair[0] != pair[1]),
        None,
    )
    spatial = next(
        (
            depth
            for depth, pair in enumerate(zip(forced_left, actual_left), start=1)
            if pair[0] != pair[1]
        ),
        None,
    )
    outside = next(
        (
            depth
            for depth, bit in enumerate(forced_left, start=1)
            if depth > support_radius and bit
        ),
        None,
    )
    if temporal != spatial:
        raise AssertionError(
            "triangular inverse invariant failed: temporal and spatial first mismatch differ"
        )

    agreement = 0
    for depth in range(period, horizon + 1):
        if desired[depth] != actual_trace[depth]:
            break
        agreement += 1
    return PeriodicReconstructionCertificate(
        rule=rule,
        base_time=base_time,
        period=period,
        horizon=horizon,
        agreement_after_first_period=agreement,
        first_temporal_mismatch=temporal,
        first_spatial_mismatch=spatial,
        first_forced_one_outside_actual_support=outside,
    )


def build_report() -> dict[str, object]:
    """Return exact controls and the strongest known Rule 30 agreement run."""
    rule30 = periodic_reconstruction_certificate(
        RULE_30,
        base_time=1855,
        period=148,
        horizon=512,
    )
    rule90 = periodic_reconstruction_certificate(
        RULE_90,
        base_time=1,
        period=1,
        horizon=512,
    )
    return {
        "method": "left-permutive triangular inverse trace",
        "rule30_long_agreement_control": asdict(rule30),
        "rule90_periodic_center_control": asdict(rule90),
        "interpretation": (
            "A finite mismatch is an exact rejection of that proposed continuation; "
            "a successful finite prefix is not a proof of periodicity."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

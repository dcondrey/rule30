"""Exact certificates for constant Rule 30 center traces.

The primary computation here is not a forward prefix scan.  It is a closed
one-bit transducer for the triangular inverse trace map.  If ``right[j]`` is
the initial cell at position ``j > 0`` and the prescribed center trace is all
zero, the forced initial cell ``left[k]`` at position ``-k`` is

    left[2i + 1] = OR(right[1], ..., right[2i + 1])
    left[2i]     = right[2i] AND NOT OR(right[1], ..., right[2i - 1]).

Thus a first right-hand one at distance ``m`` forces a one at left depth
``m`` and then a one at every larger odd depth.  This is an infinite tail, so
no nonzero finitely supported configuration can have an all-zero future center
trace.  The all-one fiber is even simpler: independently of the positive right
half, it forces ``left[k] = 1`` exactly at positive even depths.  Hence no
finite configuration has a constant-one future center trace either.  The
forward enumerator in this file is only an independent cheap-case check of the
symbolic certificates.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Iterable, Sequence


RULE_30 = 30
RULE_90 = 90


def eca_step(configuration: set[int], rule: int = RULE_30) -> set[int]:
    """Evolve one finite ECA row with a quiescent zero exterior."""
    if rule < 0 or rule > 255:
        raise ValueError("rule must be an ECA number")
    if rule & 1:
        raise ValueError("finite-set evolution requires f(000)=0")
    if not configuration:
        return set()
    result: set[int] = set()
    for position in range(min(configuration) - 1, max(configuration) + 2):
        neighborhood = (
            (int(position - 1 in configuration) << 2)
            | (int(position in configuration) << 1)
            | int(position + 1 in configuration)
        )
        if (rule >> neighborhood) & 1:
            result.add(position)
    return result


def center_trace(
    configuration: Iterable[int], horizon: int, rule: int = RULE_30
) -> tuple[int, ...]:
    """Return center cells at times zero through ``horizon`` inclusive."""
    if horizon < 0:
        raise ValueError("horizon must be non-negative")
    row = set(configuration)
    trace = []
    for _ in range(horizon + 1):
        trace.append(int(0 in row))
        row = eca_step(row, rule)
    return tuple(trace)


def forced_zero_trace_left(right: Sequence[int], depth: int) -> tuple[int, ...]:
    """Return the exact Rule 30 left prefix forced by an all-zero trace.

    ``right`` is indexed by spatial position and must contain positions zero
    through ``depth``.  Position zero must itself be zero.  The transducer's
    sole state is whether a one has appeared in the scanned right prefix.
    """
    if depth < 0:
        raise ValueError("depth must be non-negative")
    if len(right) <= depth:
        raise ValueError("right must contain positions zero through depth")
    if right[0] != 0 or any(bit not in (0, 1) for bit in right[: depth + 1]):
        raise ValueError("right[0] must be zero and all entries must be bits")

    prefix_or = 0
    forced: list[int] = []
    for position in range(1, depth + 1):
        bit = right[position]
        if position % 2:
            prefix_or |= bit
            forced.append(prefix_or)
        else:
            forced.append(bit & (1 ^ prefix_or))
            prefix_or |= bit
    return tuple(forced)


def forced_one_trace_left(right: Sequence[int], depth: int) -> tuple[int, ...]:
    """Return the exact Rule 30 left prefix forced by an all-one trace.

    The answer is independent of the prescribed positive right half: cells at
    positive even depths are one and cells at odd depths are zero.
    """
    if depth < 0:
        raise ValueError("depth must be non-negative")
    if len(right) <= depth:
        raise ValueError("right must contain positions zero through depth")
    if right[0] != 1 or any(bit not in (0, 1) for bit in right[: depth + 1]):
        raise ValueError("right[0] must be one and all entries must be bits")
    return tuple(int(position % 2 == 0) for position in range(1, depth + 1))


def first_right_one(right: Sequence[int]) -> int | None:
    """Return the first positive index containing one, if present."""
    if not right or right[0] != 0 or any(bit not in (0, 1) for bit in right):
        raise ValueError("right[0] must be zero and all entries must be bits")
    return next((position for position, bit in enumerate(right[1:], 1) if bit), None)


def class_m_left_bit(first_one: int, depth: int) -> int:
    """Closed form for the forced left tail after the first right-hand one."""
    if first_one < 1 or depth < 1:
        raise ValueError("first_one and depth must be positive")
    if depth < first_one:
        return 0
    if depth == first_one:
        return 1
    return depth & 1


def class_m_finite_window(
    first_one: int,
    left_extent: int,
    right_bits: Sequence[int],
) -> set[int]:
    """Materialize a finite window of the invariant class C_m.

    The caller chooses a sufficiently large ``left_extent`` for the causal
    question being checked.  ``right_bits[j]`` supplies position ``j`` and
    must have its first positive one at ``first_one``.
    """
    if left_extent < first_one:
        raise ValueError("left_extent must reach the first-one depth")
    if len(right_bits) <= first_one or first_right_one(right_bits) != first_one:
        raise ValueError("right_bits must have the stated first positive one")
    row = {
        -depth
        for depth in range(1, left_extent + 1)
        if class_m_left_bit(first_one, depth)
    }
    row.update(position for position, bit in enumerate(right_bits) if bit)
    return row


def next_odd_strictly_above(value: int) -> int:
    """Return the least odd integer strictly larger than ``value``."""
    if value < 0:
        raise ValueError("value must be non-negative")
    return value + 1 + (value & 1)


def next_even_strictly_above(value: int) -> int:
    """Return the least even integer strictly larger than ``value``."""
    if value < 0:
        raise ValueError("value must be non-negative")
    return value + 1 + ((value + 1) & 1)


@dataclass(frozen=True)
class RadiusCertificate:
    support_radius: int
    exact_nonzero_space_covered: int
    maximum_zero_center_horizon: int
    forced_conflict_time: int
    extremal_witness_count: int
    canonical_extremal_offsets: tuple[int, ...]
    symbolic_survivors_including_zero_before_conflict: int
    symbolic_survivors_including_zero_at_conflict: int
    conflict_core: tuple[str, ...]


@dataclass(frozen=True)
class OneRadiusCertificate:
    support_radius: int
    exact_rows_covered: int
    maximum_one_center_horizon: int
    forced_conflict_time: int
    extremal_witness_count: int
    canonical_extremal_offsets: tuple[int, ...]
    conflict_core: tuple[str, ...]


def radius_certificate(radius: int) -> RadiusCertificate:
    """Return an exact symbolic certificate for all rows in ``[-w,w]``.

    The horizon is the largest ``H`` attained by a nonzero row with center
    zero at every time ``0 <= t <= H``.  At the next time only the all-zero
    row remains.  The certificate covers all ``2^(2w)-1`` nonzero rows whose
    time-zero center is zero.
    """
    if radius < 1:
        raise ValueError("radius must be positive")
    conflict = next_odd_strictly_above(radius)
    right = (0, 1) + (0,) * (radius - 1)
    forced = forced_zero_trace_left(right, radius)
    canonical = tuple(
        sorted([1] + [-depth for depth, bit in enumerate(forced, 1) if bit])
    )
    return RadiusCertificate(
        support_radius=radius,
        exact_nonzero_space_covered=(1 << (2 * radius)) - 1,
        maximum_zero_center_horizon=conflict - 1,
        forced_conflict_time=conflict,
        extremal_witness_count=(1 << radius) - 1,
        canonical_extremal_offsets=canonical,
        symbolic_survivors_including_zero_before_conflict=1 << radius,
        symbolic_survivors_including_zero_at_conflict=1,
        conflict_core=(
            f"support forces s(0,-{conflict})=0",
            f"a nonzero right half makes OR(s(0,1)..s(0,{radius}))=1",
            f"odd inverse recurrence forces s(0,-{conflict})=1",
        ),
    )


def one_radius_certificate(radius: int) -> OneRadiusCertificate:
    """Return the sharp finite-radius certificate for an all-one trace."""
    if radius < 1:
        raise ValueError("radius must be positive")
    conflict = next_even_strictly_above(radius)
    canonical = tuple([0] + [-depth for depth in range(2, radius + 1, 2)])
    return OneRadiusCertificate(
        support_radius=radius,
        exact_rows_covered=1 << (2 * radius),
        maximum_one_center_horizon=conflict - 1,
        forced_conflict_time=conflict,
        extremal_witness_count=1 << radius,
        canonical_extremal_offsets=tuple(sorted(canonical)),
        conflict_core=(
            f"support forces s(0,-{conflict})=0",
            "an all-one trace forces every positive even left depth to one",
            f"therefore s(0,-{conflict})=1",
        ),
    )
@dataclass(frozen=True)
class ExhaustiveCheck:
    support_radius: int
    rows_checked: int
    observed_maximum_zero_center_horizon: int
    extremal_witness_count: int
    canonical_extremal_offsets: tuple[int, ...]
    matches_symbolic_certificate: bool


def _assignment_offsets(assignment: int, radius: int) -> tuple[int, ...]:
    positions = tuple(range(-radius, 0)) + tuple(range(1, radius + 1))
    return tuple(
        position for index, position in enumerate(positions) if assignment >> index & 1
    )


def exhaustive_radius_check(radius: int) -> ExhaustiveCheck:
    """Independently forward-enumerate one cheap radius.

    This validator deliberately does not call the inverse transducer.  It is
    exponential and is not the research method used to establish the bound.
    """
    certificate = radius_certificate(radius)
    best = -1
    count = 0
    canonical: tuple[int, ...] = ()
    for assignment in range(1, 1 << (2 * radius)):
        offsets = _assignment_offsets(assignment, radius)
        trace = center_trace(offsets, certificate.forced_conflict_time)
        first_one = next((time for time, bit in enumerate(trace) if bit), None)
        horizon = (
            certificate.forced_conflict_time if first_one is None else first_one - 1
        )
        if horizon > best:
            best = horizon
            count = 1
            canonical = offsets
        elif horizon == best:
            count += 1
    matches = (
        best == certificate.maximum_zero_center_horizon
        and count == certificate.extremal_witness_count
        and canonical == certificate.canonical_extremal_offsets
    )
    return ExhaustiveCheck(
        support_radius=radius,
        rows_checked=(1 << (2 * radius)) - 1,
        observed_maximum_zero_center_horizon=best,
        extremal_witness_count=count,
        canonical_extremal_offsets=canonical,
        matches_symbolic_certificate=matches,
    )


def build_report(max_radius: int, exhaustive_through: int) -> dict[str, object]:
    if max_radius < 1:
        raise ValueError("max_radius must be positive")
    if exhaustive_through < 0 or exhaustive_through > max_radius:
        raise ValueError("exhaustive_through must lie in [0, max_radius]")
    certificates = [radius_certificate(radius) for radius in range(1, max_radius + 1)]
    one_certificates = [
        one_radius_certificate(radius) for radius in range(1, max_radius + 1)
    ]
    checks = [
        exhaustive_radius_check(radius) for radius in range(1, exhaustive_through + 1)
    ]
    rule90_trace = center_trace((-1, 1), max(32, max_radius + 2), RULE_90)
    period_two_falsifier = center_trace((-1,), 7, RULE_30)
    return {
        "status": "PROVED",
        "theorem": (
            "The zero row is the only finite Rule 30 row with all-zero center "
            "trace, and no finite row has an all-one center trace."
        ),
        "method": (
            "prefix-OR inverse transducer for zero and a fixed alternating "
            "left half for one"
        ),
        "radius_certificates": [asdict(item) for item in certificates],
        "one_radius_certificates": [asdict(item) for item in one_certificates],
        "independent_exhaustive_checks": [asdict(item) for item in checks],
        "rule90_control": {
            "initial_offsets": (-1, 1),
            "all_checked_center_bits_zero": not any(rule90_trace),
            "checked_horizon": len(rule90_trace) - 1,
        },
        "phase_labelled_generalization_falsifier": {
            "rejected_claim": (
                "a periodic word containing zero obeys the zero-trace "
                "next-odd conflict bound"
            ),
            "initial_offsets": (-1,),
            "proposed_period_word": (0, 1),
            "observed_trace_times_0_through_7": period_two_falsifier,
            "agreement_through_time": 6,
            "first_mismatch_time": 7,
        },
        "spending_usd": {"modal": 0, "model_providers": 0},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-radius", type=int, default=12)
    parser.add_argument("--exhaustive-through", type=int, default=8)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report(args.max_radius, args.exhaustive_through)
    print(json.dumps(report, indent=2, sort_keys=args.json))


if __name__ == "__main__":
    main()

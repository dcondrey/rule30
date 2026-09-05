#!/usr/bin/env python3
"""Exact defect/restart cocycle in the Boolean hard-core quotient.

This is a solver-free audit.  The evolving state is the full symbolic
frontier driver together with an idempotent survivor indicator.  Three exact
splits are retained:

* advance: survivors through the next macro versus removals at that macro;
* restart: a future-good interval split by whether the skipped macro passes;
* extension: a longer-seed interval split into matched and mismatched appends.

All three are disjoint Boolean partitions, so principal ranks add.  They are
not strict contractions: absorbed generators give literal survivor-indicator
self-loops, and matched extension preserves rank.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from interval_annihilator_audit import (
    Trace,
    equality_indicator,
    interval_indicator,
    polynomial_payload,
    principal_rank,
    product,
    trace,
)
from pivot_emission_audit import (
    ANF,
    ONE,
    ZERO,
    MacroEmission,
    SymbolicState,
    anf_xor,
    complement,
    symbolic_forced_macro,
    symbolic_seed_state,
    variable,
)


@dataclass(frozen=True)
class CocycleState:
    """The exact, closed, but width-growing cocycle state."""

    n: int
    offset: int
    frontier: SymbolicState
    previous_rho: ANF
    indicator: ANF


def good_factor(emission: MacroEmission) -> ANF:
    """Indicator that both the pin and new no-11 constraints pass."""
    return product(
        complement(emission.pin_emission),
        complement(emission.hard_core_obstruction),
    )


def initial_state(length: int) -> CocycleState:
    if length < 1:
        raise ValueError("length must be positive")
    return CocycleState(
        n=length,
        offset=0,
        frontier=symbolic_seed_state(length, hard_core_reduce=True),
        previous_rho=variable(length - 1),
        indicator=ONE,
    )


def rank_payload(value: ANF, length: int) -> dict[str, Any]:
    payload = polynomial_payload(value)
    payload["principal_rank"] = principal_rank(value, length)
    return payload


def assert_partition(parent: ANF, left: ANF, right: ANF) -> None:
    if anf_xor(left, right) != parent:
        raise AssertionError("components do not sum to their parent")
    if product(left, right) != ZERO:
        raise AssertionError("partition components overlap")


def advance(state: CocycleState) -> tuple[CocycleState, dict[str, Any]]:
    """Apply one exact formula morph F_m -> F_(m+1)."""
    emission = symbolic_forced_macro(
        state.frontier,
        state.previous_rho,
        hard_core_reduce=True,
    )
    factor = good_factor(emission)
    following = product(state.indicator, factor)
    removed = product(state.indicator, complement(factor))
    assert_partition(state.indicator, following, removed)

    before_rank = principal_rank(state.indicator, state.n)
    after_rank = principal_rank(following, state.n)
    removed_rank = principal_rank(removed, state.n)
    if before_rank != after_rank + removed_rank:
        raise AssertionError("advance ranks are not additive")

    record = {
        "n": state.n,
        "offset": state.offset,
        "frontier_depth": state.frontier.T,
        "previous_indicator": rank_payload(state.indicator, state.n),
        "pin_emission": polynomial_payload(emission.pin_emission),
        "no_11_obstruction": polynomial_payload(
            emission.hard_core_obstruction
        ),
        "good_factor": polynomial_payload(factor),
        "following_indicator": rank_payload(following, state.n),
        "removed_component": rank_payload(removed, state.n),
        "strict_rank_contraction": after_rank < before_rank,
        "absorbed_generator": following == state.indicator,
        "rank_partition": [before_rank, after_rank, removed_rank],
        "verified": True,
    }
    return (
        CocycleState(
            n=state.n,
            offset=state.offset + 1,
            frontier=emission.successor,
            previous_rho=emission.forced_rho,
            indicator=following,
        ),
        record,
    )


def advance_trace(length: int, steps: int) -> list[dict[str, Any]]:
    state = initial_state(length)
    records = []
    for _ in range(steps):
        state, record = advance(state)
        records.append(record)
    return records


def restart_split(
    length: int,
    skipped_offset: int,
    future_horizon: int,
    traced: Trace,
) -> dict[str, Any]:
    """Split a future-good interval by the preceding skipped macro."""
    future = interval_indicator(
        traced.emissions, skipped_offset + 1, future_horizon
    )
    emission = traced.emissions[skipped_offset]
    factor = good_factor(emission)
    continuous = product(future, factor)
    expected_continuous = interval_indicator(
        traced.emissions, skipped_offset, future_horizon + 1
    )
    restart = product(future, complement(factor))
    if continuous != expected_continuous:
        raise AssertionError("continuous interval identity failed")
    assert_partition(future, continuous, restart)
    ranks = tuple(
        principal_rank(value, length)
        for value in (future, continuous, restart)
    )
    if ranks[0] != ranks[1] + ranks[2]:
        raise AssertionError("restart ranks are not additive")
    return {
        "n": length,
        "skipped_offset": skipped_offset,
        "future_start": skipped_offset + 1,
        "future_horizon": future_horizon,
        "pin_emission": polynomial_payload(emission.pin_emission),
        "no_11_obstruction": polynomial_payload(
            emission.hard_core_obstruction
        ),
        "good_factor": polynomial_payload(factor),
        "future_good_parent": rank_payload(future, length),
        "continuous_component": rank_payload(continuous, length),
        "expected_continuous_interval": polynomial_payload(
            expected_continuous
        ),
        "restart_component": rank_payload(restart, length),
        "rank_partition": list(ranks),
        "verified": True,
    }


def extension_split(
    shorter_n: int,
    longer_start: int,
    horizon: int,
    shorter: Trace,
    longer: Trace,
) -> dict[str, Any]:
    """Split P_(n+1;a,H) into matched and mismatched append branches."""
    destination = interval_indicator(longer.emissions, longer_start, horizon)
    match = equality_indicator(
        variable(shorter_n), shorter.emissions[0].forced_rho
    )
    matched = product(destination, match)
    predicted = product(
        interval_indicator(
            shorter.emissions, longer_start + 1, horizon
        ),
        match,
    )
    defect = product(destination, complement(match))
    if matched != predicted:
        raise AssertionError("matched shifted-interval identity failed")
    assert_partition(destination, matched, defect)
    ranks = tuple(
        principal_rank(value, shorter_n + 1)
        for value in (destination, matched, defect)
    )
    if ranks[0] != ranks[1] + ranks[2]:
        raise AssertionError("extension ranks are not additive")
    return {
        "shorter_n": shorter_n,
        "longer_n": shorter_n + 1,
        "longer_start": longer_start,
        "shorter_start": longer_start + 1,
        "horizon": horizon,
        "destination_indicator": rank_payload(
            destination, shorter_n + 1
        ),
        "match_indicator": polynomial_payload(match),
        "matched_component": rank_payload(matched, shorter_n + 1),
        "predicted_shifted_component": polynomial_payload(predicted),
        "mismatch_defect_component": rank_payload(defect, shorter_n + 1),
        "rank_partition": list(ranks),
        "verified": True,
    }


def indicator_closure_collision(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Find equal (indicator, phase mod 3) states with unequal successors."""
    seen: dict[tuple[tuple[int, ...], int], dict[str, Any]] = {}
    for record in records:
        indicator = tuple(record["previous_indicator"]["monomial_masks"])
        key = indicator, record["offset"] % 3
        previous = seen.get(key)
        if previous is None:
            seen[key] = record
            continue
        left_successor = previous["following_indicator"]["monomial_masks"]
        right_successor = record["following_indicator"]["monomial_masks"]
        if left_successor != right_successor:
            return {
                "summary": "(exact survivor indicator, offset mod 3)",
                "left_offset": previous["offset"],
                "right_offset": record["offset"],
                "shared_indicator": previous["previous_indicator"],
                "shared_phase_mod_3": record["offset"] % 3,
                "left_good_factor": previous["good_factor"],
                "right_good_factor": record["good_factor"],
                "left_successor": previous["following_indicator"],
                "right_successor": record["following_indicator"],
                "verified": True,
            }
    raise AssertionError("expected n=10 indicator/phase closure collision missing")


def restart_lift_control(traces: dict[int, Trace]) -> dict[str, Any]:
    """The exact n=2 restart lifted by two matched appends to seed 0xa."""
    p2 = interval_indicator(traces[2].emissions, 2, 4)
    p3 = interval_indicator(traces[3].emissions, 1, 4)
    p4 = interval_indicator(traces[4].emissions, 0, 4)
    match2 = equality_indicator(
        variable(2), traces[2].emissions[0].forced_rho
    )
    match3 = equality_indicator(
        variable(3), traces[3].emissions[0].forced_rho
    )
    if product(p3, match2) != product(p2, match2):
        raise AssertionError("first matched restart lift failed")
    if product(p4, match3) != product(p3, match3):
        raise AssertionError("second matched restart lift failed")
    both_matches = product(match2, match3)
    if product(p4, both_matches) != p4:
        raise AssertionError("length-four spike is not wholly matched")
    if p2 != variable(1):
        raise AssertionError("unexpected n=2 restart interval")
    if p4 != frozenset({0b1010}):
        raise AssertionError("unexpected n=4 lifted interval")

    restart = restart_split(2, 1, 4, traces[2])
    if restart["rank_partition"] != [1, 0, 1]:
        raise AssertionError("n=2 restart control has wrong ranks")
    return {
        "description": (
            "P_(2;2,4)=rho_2 is entirely a restart after failure at "
            "offset 1; two matched appends lift it to "
            "P_(4;0,4)=rho_2*rho_4, the unique hard-core seed 0xa"
        ),
        "n2_restart_split": restart,
        "P_2_2_4": rank_payload(p2, 2),
        "P_3_1_4": rank_payload(p3, 3),
        "P_4_0_4": rank_payload(p4, 4),
        "match_2_to_3": polynomial_payload(match2),
        "match_3_to_4": polynomial_payload(match3),
        "both_matches": polynomial_payload(both_matches),
        "first_lift_left": polynomial_payload(product(p3, match2)),
        "first_lift_right": polynomial_payload(product(p2, match2)),
        "second_lift_left": polynomial_payload(product(p4, match3)),
        "second_lift_right": polynomial_payload(product(p3, match3)),
        "unique_seed_hex": "0xa",
        "verified": True,
    }


def build_result() -> dict[str, Any]:
    traces = {
        length: trace(length, 20)
        for length in (2, 3, 4, 10, 11, 12, 13, 14)
    }

    advance_records = {
        "n4": advance_trace(4, 5),
        "n10": advance_trace(10, 9),
        "n12": advance_trace(12, 7),
    }
    collision = indicator_closure_collision(advance_records["n10"])

    extension_controls = [
        extension_split(2, 1, 4, traces[2], traces[3]),
        extension_split(3, 0, 4, traces[3], traces[4]),
    ]
    for shorter_n in range(10, 14):
        extension_controls.append(
            extension_split(
                shorter_n,
                0,
                17 - shorter_n,
                traces[shorter_n],
                traces[shorter_n + 1],
            )
        )

    result = {
        "schema": "crosstalk.rule30.defect-restart-cocycle.v1",
        "method": {
            "sat": False,
            "seed_enumeration": False,
            "ring": (
                "F_2[rho_1,...,rho_n]/<rho_i^2+rho_i,"
                "rho_i*rho_(i+1)>"
            ),
            "exact_state": (
                "(symbolic frontier, previous forced rho, survivor indicator)"
            ),
            "advance": "P' = P*(1+epsilon_m)*(1+q_m)",
            "restart": (
                "P_(a+1,H) = P_(a,H+1) + "
                "P_(a+1,H)*(1+K_a)"
            ),
            "extension": (
                "P_(n+1;a,H) = matched component + mismatch defect"
            ),
        },
        "uniform_partition_lemma": {
            "statement": (
                "For every idempotent P and Boolean factor K, "
                "P=PK + P(1+K), the summands are disjoint, and their "
                "principal ranks add."
            ),
            "strictness": (
                "rank(PK)<rank(P) iff the removed component P(1+K) "
                "is nonzero"
            ),
            "proof": "Boolean distributivity and K(1+K)=0",
        },
        "advance_cocycle_controls": advance_records,
        "indicator_phase_closure_collision": collision,
        "extension_match_defect_controls": extension_controls,
        "restart_lift_control": restart_lift_control(traces),
        "conclusion": {
            "exact_full_driver_cocycle_built": True,
            "principal_rank_is_nonincreasing_at_fixed_n": True,
            "principal_rank_is_strict_at_every_macro": False,
            "indicator_plus_period_three_phase_is_closed": False,
            "matched_extension_is_rank_preserving": True,
            "restart_can_create_a_later_prefix_survivor_spike": True,
            "well_founded_uniform_rank_found": False,
            "period_two_theorem_proved": False,
            "remaining_obligation": (
                "find a symbolic compression of the growing frontier driver "
                "with a well-founded delay/restart rank, or prove such a "
                "candidate class impossible"
            ),
        },
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    result = build_result()
    for label, records in result["advance_cocycle_controls"].items():
        ranks = [records[0]["rank_partition"][0]]
        ranks.extend(record["rank_partition"][1] for record in records)
        print(f"{label} advance ranks: {ranks}")
    collision = result["indicator_phase_closure_collision"]
    print(
        "indicator/period-3 closure: FAIL at offsets "
        f"{collision['left_offset']} and {collision['right_offset']}"
    )
    lift = result["restart_lift_control"]
    print(
        "restart lift: P_(2;2,4)=rho_2 -> "
        "P_(4;0,4)=rho_2*rho_4 (seed 0xa) PASS"
    )
    print("advance/restart/extension partition identities: PASS")
    print("strict algebraic-rank contraction: FALSE")
    print("uniform mortality: OPEN")

    if args.json is not None:
        args.json.write_text(json.dumps(result, indent=2) + "\n")
        print(f"wrote {args.json}")


if __name__ == "__main__":
    main()

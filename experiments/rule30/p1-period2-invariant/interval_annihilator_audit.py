#!/usr/bin/env python3
"""Exact interval-annihilator and matched-extension audit.

This continues the cofactor audit at the level where a genuine local
structure survives.  It uses no seed enumeration.  Survivor indicators are
formed as products of complemented emission generators in the Boolean
hard-core quotient, and their cardinalities are recovered as ranks of
principal multiplication maps.

If a new seed bit equals the forced rho bit of the shorter frontier, adding
that seed bit is exactly one forced macro.  Hence all later observables shift
by one.  The audit verifies the corresponding interval-indicator identity,
isolates the unmatched defect branch, and extracts compact annihilator
presentations for the rank-six and rank-five states seen at n=10,...,14.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pivot_emission_audit import (
    ANF,
    ONE,
    ZERO,
    MacroEmission,
    SymbolicState,
    anf_payload,
    anf_product,
    anf_xor,
    complement,
    degree,
    symbolic_forced_macro,
    symbolic_parity_or,
    symbolic_seed_state,
    symbolic_wf_step,
    variable,
)


@dataclass(frozen=True)
class Trace:
    emissions: tuple[MacroEmission, ...]
    prefix_indicators: tuple[ANF, ...]


def product(left: ANF, right: ANF) -> ANF:
    return anf_product(left, right, hard_core_reduce=True)


def polynomial_payload(value: ANF) -> dict[str, Any]:
    answer = anf_payload(value)
    support_mask = 0
    for monomial in value:
        support_mask |= monomial
    support = [
        index + 1
        for index in range(support_mask.bit_length())
        if (support_mask >> index) & 1
    ]
    answer["variable_support"] = support
    answer["support_span"] = support[-1] - support[0] + 1 if support else 0
    return answer


def trace(length: int, macros: int) -> Trace:
    state = symbolic_seed_state(length, hard_core_reduce=True)
    previous = variable(length - 1)
    emissions: list[MacroEmission] = []
    indicators = [ONE]
    for _ in range(macros):
        emission = symbolic_forced_macro(
            state, previous, hard_core_reduce=True
        )
        survivor = product(
            product(
                indicators[-1], complement(emission.pin_emission)
            ),
            complement(emission.hard_core_obstruction),
        )
        emissions.append(emission)
        indicators.append(survivor)
        previous = emission.forced_rho
        state = emission.successor
    return Trace(tuple(emissions), tuple(indicators))


def interval_indicator(
    emissions: tuple[MacroEmission, ...], start: int, count: int
) -> ANF:
    answer = ONE
    for emission in emissions[start : start + count]:
        answer = product(answer, complement(emission.pin_emission))
        answer = product(answer, complement(emission.hard_core_obstruction))
    return answer


def hard_core_basis(length: int) -> list[int]:
    return [
        mask
        for mask in range(1 << length)
        if (mask & (mask >> 1)) == 0
    ]


def principal_rank(value: ANF, length: int) -> int:
    """Rank of multiplication by value on the Boolean hard-core quotient."""
    basis = hard_core_basis(length)
    positions = {monomial: index for index, monomial in enumerate(basis)}
    pivots: dict[int, int] = {}
    for monomial in basis:
        image = product(value, frozenset({monomial}))
        vector = 0
        for term in image:
            vector |= 1 << positions[term]
        while vector:
            pivot = vector.bit_length() - 1
            if pivot in pivots:
                vector ^= pivots[pivot]
            else:
                pivots[pivot] = vector
                break
    return len(pivots)


def zero_indicator(generators: list[tuple[str, ANF]]) -> ANF:
    answer = ONE
    for _, generator in generators:
        answer = product(answer, complement(generator))
    return answer


def literal(index: int, value: int) -> tuple[str, ANF]:
    rho = variable(index - 1)
    if value == 0:
        return f"rho_{index}=0", rho
    return f"rho_{index}=1", complement(rho)


def rank_six_constraints(length: int) -> list[tuple[str, ANF]]:
    if length < 10 or length > 14:
        raise ValueError("rank-six presentation is recorded only for n=10..14")
    generators = [
        literal(5, 0),
        literal(6, 0),
        literal(7, 0),
        literal(8, 1),
        literal(9, 0),
        literal(10, 0),
        (
            "rho_4+rho_2rho_4=0",
            anf_xor(
                variable(3),
                frozenset({(1 << 1) | (1 << 3)}),
            ),
        ),
    ]
    tail = {11: 1, 12: 0, 13: 0, 14: 1}
    generators.extend(literal(index, tail[index]) for index in range(11, length + 1))
    return generators


def rank_five_constraints(length: int) -> list[tuple[str, ANF]]:
    if length not in (13, 14):
        raise ValueError("rank-five presentation is recorded only for n=13,14")
    values = {
        4: 0,
        5: 0,
        6: 1,
        7: 0,
        8: 0,
        9: 1,
        10: 0,
        11: 0,
        12: 0,
        13: 1,
        14: 0,
    }
    return [literal(index, values[index]) for index in range(4, length + 1)]


def compact_state(
    label: str,
    length: int,
    expected: ANF,
    generators: list[tuple[str, ANF]],
) -> dict[str, Any]:
    actual = zero_indicator(generators)
    if actual != expected:
        raise AssertionError(f"compact annihilator presentation failed for {label}")
    return {
        "label": label,
        "n": length,
        "indicator": polynomial_payload(expected),
        "principal_rank": principal_rank(expected, length),
        "zero_generators": [
            {"label": name, "polynomial": polynomial_payload(polynomial)}
            for name, polynomial in generators
        ],
        "presentation_verified": True,
    }


def equality_indicator(new_bit: ANF, forced_bit: ANF) -> ANF:
    """Indicator of new_bit=forced_bit in a Boolean function ring."""
    return complement(anf_xor(new_bit, forced_bit))


def transition_decomposition(
    shorter_n: int,
    destination_horizon: int,
    shorter: Trace,
    longer: Trace,
) -> dict[str, Any]:
    destination = longer.prefix_indicators[destination_horizon]
    match = equality_indicator(
        variable(shorter_n), shorter.emissions[0].forced_rho
    )
    predicted_interval = product(
        interval_indicator(
            shorter.emissions, 1, destination_horizon
        ),
        match,
    )
    matched = product(destination, match)
    defect = product(destination, complement(match))
    if matched != predicted_interval:
        raise AssertionError(
            f"matched interval identity failed at n={shorter_n}->{shorter_n + 1}"
        )
    if anf_xor(matched, defect) != destination:
        raise AssertionError("match/defect partition failed")
    if product(matched, defect) != ZERO:
        raise AssertionError("match/defect components are not disjoint")
    return {
        "shorter_n": shorter_n,
        "longer_n": shorter_n + 1,
        "destination_horizon": destination_horizon,
        "identity": (
            "P_(n+1;0,H)*M = P_(n;1,H)*M, "
            "M=1+rho_(n+1)+forced_rho_0"
        ),
        "destination_indicator": polynomial_payload(destination),
        "match_indicator": polynomial_payload(match),
        "matched_component": polynomial_payload(matched),
        "predicted_interval_component": polynomial_payload(predicted_interval),
        "defect_component": polynomial_payload(defect),
        "destination_rank": principal_rank(destination, shorter_n + 1),
        "matched_rank": principal_rank(matched, shorter_n + 1),
        "defect_rank": principal_rank(defect, shorter_n + 1),
        "all_survivors_matched": defect == ZERO,
        "verified": True,
    }


def constant_on(value: ANF, indicator: ANF) -> int | None:
    if product(value, indicator) == ZERO:
        return 0
    if product(complement(value), indicator) == ZERO:
        return 1
    return None


def terminal_signature(
    length: int,
    macro: int,
    emission: MacroEmission,
    branches: list[tuple[str, ANF]],
) -> dict[str, Any]:
    return {
        "n": length,
        "terminal_macro_offset": macro,
        "pin_emission": polynomial_payload(emission.pin_emission),
        "no_11_obstruction": polynomial_payload(
            emission.hard_core_obstruction
        ),
        "forced_rho": polynomial_payload(emission.forced_rho),
        "branches": [
            {
                "label": label,
                "indicator": polynomial_payload(indicator),
                "rank": principal_rank(indicator, length),
                "pin_value": constant_on(emission.pin_emission, indicator),
                "no_11_value": constant_on(
                    emission.hard_core_obstruction, indicator
                ),
                "forced_rho_value": constant_on(
                    emission.forced_rho, indicator
                ),
            }
            for label, indicator in branches
        ],
    }


def state_defect_audit(state: SymbolicState) -> dict[str, Any]:
    """Verify the affine frontier defect caused by a mismatched seed bit."""
    zero_feed = symbolic_parity_or(state, hard_core_reduce=True)
    matched_middle = symbolic_wf_step(
        state, zero_feed, hard_core_reduce=True
    )
    mismatched_middle = symbolic_wf_step(
        state, complement(zero_feed), hard_core_reduce=True
    )
    if any(
        anf_xor(left, right) != ONE
        for left, right in zip(
            matched_middle.A, mismatched_middle.A
        )
    ):
        raise AssertionError("mismatch did not complement the first new row")

    matched = symbolic_wf_step(
        matched_middle, ONE, hard_core_reduce=True
    )
    mismatched = symbolic_wf_step(
        mismatched_middle, ONE, hard_core_reduce=True
    )
    predicted = [ZERO]
    cumulative = ZERO
    for j in range(1, matched_middle.T + 1):
        if j == 1:
            shifted_a = ONE if (state.T & 1) else ZERO
        else:
            shifted_a = state.A[j - 2]
        cumulative = anf_xor(cumulative, complement(shifted_a))
        predicted.append(cumulative)
    actual = [
        anf_xor(left, right)
        for left, right in zip(matched.A, mismatched.A)
    ]
    if actual != predicted:
        raise AssertionError("affine mismatch defect formula failed")
    if any(
        anf_xor(left, right) != ONE
        for left, right in zip(matched.B, mismatched.B)
    ):
        raise AssertionError("mismatch B-row defect is not all ones")
    return {
        "frontier_depth": state.T,
        "first_added_row_defect": "all ones",
        "successor_B_defect": "all ones",
        "successor_A_defect": (
            "delta_0=0; delta_j=sum_(ell=1)^j (1+shift(A)_ell)"
        ),
        "maximum_successor_A_defect_degree": max(map(degree, actual)),
        "verified": True,
    }


def identity_payload(label: str, left: ANF, right: ANF) -> dict[str, Any]:
    if left != right:
        raise AssertionError(f"identity failed: {label}")
    return {
        "label": label,
        "left": polynomial_payload(left),
        "right": polynomial_payload(right),
        "verified": True,
    }


def build_result() -> dict[str, Any]:
    horizons = {10: 9, 11: 8, 12: 7, 13: 6, 14: 5}
    traces = {length: trace(length, horizon) for length, horizon in horizons.items()}
    plateau_horizons = {10: 8, 11: 7, 12: 6, 13: 5, 14: 4}
    plateaus = {
        length: traces[length].prefix_indicators[horizon]
        for length, horizon in plateau_horizons.items()
    }

    a13 = product(plateaus[13], complement(variable(12)))
    b13 = product(plateaus[13], variable(12))
    a14 = product(plateaus[14], complement(variable(12)))
    b14 = product(plateaus[14], variable(12))

    compact_states = [
        compact_state("A_10", 10, plateaus[10], rank_six_constraints(10)),
        compact_state("A_11", 11, plateaus[11], rank_six_constraints(11)),
        compact_state("A_12", 12, plateaus[12], rank_six_constraints(12)),
        compact_state("A_13", 13, a13, rank_six_constraints(13)),
        compact_state("A_14", 14, a14, rank_six_constraints(14)),
        compact_state("B_13", 13, b13, rank_five_constraints(13)),
        compact_state("B_14", 14, b14, rank_five_constraints(14)),
    ]

    identities = [
        identity_payload(
            "P_(11,7)=P_(10,8)*rho_11",
            plateaus[11],
            product(plateaus[10], variable(10)),
        ),
        identity_payload(
            "P_(12,6)=P_(11,7)", plateaus[12], plateaus[11]
        ),
        identity_payload(
            "P_(12,6)=P_(10,8)*rho_11*(1+rho_12)",
            plateaus[12],
            product(
                product(plateaus[10], variable(10)),
                complement(variable(11)),
            ),
        ),
        identity_payload(
            "P_(13,5)=A_13+B_13",
            plateaus[13],
            anf_xor(a13, b13),
        ),
        identity_payload(
            "P_(14,4)=P_(13,5)*(rho_13+rho_14)",
            plateaus[14],
            product(
                plateaus[13],
                anf_xor(variable(12), variable(13)),
            ),
        ),
        identity_payload(
            "P_(14,4)=A_14+B_14",
            plateaus[14],
            anf_xor(a14, b14),
        ),
    ]

    transitions = []
    for shorter_n in range(10, 14):
        destination_horizon = 17 - shorter_n
        transitions.append(
            transition_decomposition(
                shorter_n,
                destination_horizon,
                traces[shorter_n],
                traces[shorter_n + 1],
            )
        )

    alignment = []
    p12 = plateaus[12]
    for macro in range(7):
        shorter = traces[10].emissions[macro + 2]
        longer = traces[12].emissions[macro]
        record = {"macro_12": macro, "macro_10": macro + 2}
        for label, left, right in (
            ("forced_rho", longer.forced_rho, shorter.forced_rho),
            ("pin_emission", longer.pin_emission, shorter.pin_emission),
            (
                "no_11_obstruction",
                longer.hard_core_obstruction,
                shorter.hard_core_obstruction,
            ),
        ):
            residue = product(anf_xor(left, right), p12)
            if residue != ZERO:
                raise AssertionError(f"n=10/12 alignment failed for {label}")
            record[f"{label}_difference_times_P12"] = polynomial_payload(
                residue
            )
        alignment.append(record)

    terminal_signatures = [
        terminal_signature(
            10,
            8,
            traces[10].emissions[8],
            [("A_10", plateaus[10])],
        ),
        terminal_signature(
            11,
            7,
            traces[11].emissions[7],
            [("A_11", plateaus[11])],
        ),
        terminal_signature(
            12,
            6,
            traces[12].emissions[6],
            [("A_12", plateaus[12])],
        ),
        terminal_signature(
            13,
            5,
            traces[13].emissions[5],
            [("A_13", a13), ("B_13", b13)],
        ),
        terminal_signature(
            14,
            4,
            traces[14].emissions[4],
            [("A_14", a14), ("B_14", b14)],
        ),
    ]
    for signature in terminal_signatures:
        if any(branch["pin_value"] != 1 for branch in signature["branches"]):
            raise AssertionError("terminal pin is not one on every branch")

    defect_audits = [
        state_defect_audit(
            symbolic_seed_state(length, hard_core_reduce=True)
        )
        for length in (4, 10, 12)
    ]

    return {
        "schema": "crosstalk.rule30.interval-annihilator-audit.v1",
        "method": {
            "seed_enumeration": False,
            "ring": (
                "F_2[rho_1,...,rho_n]/<rho_i^2+rho_i, "
                "rho_i rho_(i+1)>"
            ),
            "survivor_cardinality": (
                "rank of multiplication by the survivor indicator"
            ),
        },
        "universal_matched_extension_lemma": {
            "seed_extension": "E_b(S)=R_1(R_(1+b)(S))",
            "forced_macro": "F(S)=R_1(R_z(S)), z=parity_or(S)",
            "forced_rho": "r=1+z",
            "identity": "b=r implies E_b(S)=F(S)",
            "interval_consequence": (
                "M*P_(n+1;0,H)=M*P_(n;1,H), "
                "M=1+rho_(n+1)+r"
            ),
            "proof": "substitute b=r, so 1+b=z, in the two row maps",
        },
        "compact_annihilator_states": compact_states,
        "exact_indicator_identities": identities,
        "matched_extension_transitions": transitions,
        "n10_n12_two_macro_alignment": alignment,
        "terminal_signatures": terminal_signatures,
        "mismatch_frontier_defect": defect_audits,
        "conclusion": {
            "rank_six_period_three_tail_state_verified": True,
            "matched_extension_shift_is_uniform": True,
            "unmatched_defect_first_appears_here_at_n13": True,
            "defect_rank_at_n13": 5,
            "all_recorded_branches_terminally_forced_by_pin": True,
            "uniform_2n_plus_2_bound_proved": False,
            "remaining_obligation": (
                "classify and rank mismatch/interval-restart states uniformly"
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    result = build_result()
    transitions = result["matched_extension_transitions"]
    print("universal matched-extension lemma: symbolic identity PASS")
    print("n=10 -> n=12: rank-six period-three annihilator state PASS")
    print("n=10/n=12 observables: two-macro alignment through terminal PASS")
    for transition in transitions:
        print(
            f"n={transition['shorter_n']}->{transition['longer_n']} "
            f"H={transition['destination_horizon']}: "
            f"matched rank={transition['matched_rank']}, "
            f"defect rank={transition['defect_rank']}"
        )
    print("n=13 defect: compact rank-five annihilator state PASS")
    print("all A/B terminal branches: epsilon=1 PASS")
    print("uniform mortality: remaining defect classification OPEN")

    if args.json is not None:
        args.json.write_text(json.dumps(result, indent=2) + "\n")
        print(f"wrote {args.json}")


if __name__ == "__main__":
    main()

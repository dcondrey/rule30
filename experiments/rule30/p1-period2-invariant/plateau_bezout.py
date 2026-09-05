#!/usr/bin/env python3
"""Exact Boolean Bezout certificates for the n=10 mortality plateau.

All arithmetic is in the Boolean quotient rho_i^2=rho_i.  The emitted JSON
contains a full lift of each identity: dynamic cofactors plus explicit
cofactors of the initial hard-core generators rho_i rho_(i+1).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from pivot_emission_audit import (
    ANF,
    ONE,
    ZERO,
    anf_payload,
    anf_product,
    anf_xor,
    complement,
    degree,
    evaluate,
    hard_core_assignments,
    symbolic_forced_macro,
    symbolic_seed_state,
    variable,
)


N = 10
TERMINAL_OFFSET = 8


def product(left: ANF, right: ANF, *, hard_core_reduce: bool) -> ANF:
    return anf_product(left, right, hard_core_reduce=hard_core_reduce)


def emission_trace(horizon: int, *, hard_core_reduce: bool) -> list[Any]:
    state = symbolic_seed_state(N, hard_core_reduce=hard_core_reduce)
    previous = variable(N - 1)
    emissions = []
    for _ in range(horizon):
        emission = symbolic_forced_macro(
            state, previous, hard_core_reduce=hard_core_reduce
        )
        emissions.append(emission)
        previous = emission.forced_rho
        state = emission.successor
    return emissions


def dynamic_generators(emissions: list[Any], horizon: int) -> list[tuple[str, ANF]]:
    answer = []
    for offset in range(horizon):
        answer.append((f"epsilon_{offset}", emissions[offset].pin_emission))
        answer.append(
            (f"q_{offset}", emissions[offset].hard_core_obstruction)
        )
    return answer


def survivor_sets(emissions: list[Any]) -> list[list[int]]:
    alive = hard_core_assignments(N)
    answer = [alive]
    for emission in emissions:
        alive = [
            seed
            for seed in alive
            if evaluate(emission.pin_emission, seed) == 0
            and evaluate(emission.hard_core_obstruction, seed) == 0
        ]
        answer.append(alive)
    return answer


def variable_support(value: ANF) -> list[int]:
    return sorted(
        {
            index + 1
            for monomial in value
            for index in range(N)
            if (monomial >> index) & 1
        }
    )


def cofactor_payload(value: ANF) -> dict[str, Any]:
    answer = anf_payload(value)
    answer["variable_support"] = variable_support(value)
    return answer


def decompose_hard_core_remainder(remainder: ANF) -> list[ANF]:
    """Write a polynomial vanishing modulo no-11 as sum S_i rho_i rho_(i+1)."""
    cofactors: list[set[int]] = [set() for _ in range(N - 1)]
    for monomial in remainder:
        adjacent = next(
            (
                index
                for index in range(N - 1)
                if ((monomial >> index) & 3) == 3
            ),
            None,
        )
        if adjacent is None:
            raise AssertionError(
                f"remainder monomial {monomial:#x} is not hard-core reducible"
            )
        quotient = monomial & ~(3 << adjacent)
        if quotient in cofactors[adjacent]:
            cofactors[adjacent].remove(quotient)
        else:
            cofactors[adjacent].add(quotient)
    return [frozenset(cofactor) for cofactor in cofactors]


def bezout_certificate(
    *,
    target_label: str,
    target_reduced: ANF,
    target_full: ANF,
    reduced_history: list[tuple[str, ANF]],
    full_history: list[tuple[str, ANF]],
    forced_at_horizon: int,
) -> dict[str, Any]:
    """Construct 1=target+sum C_i g_i+sum S_j rho_j rho_(j+1).

    In the hard-core quotient, H=OR(g_i)=sum prefix_i*g_i is the indicator
    of the complement of V_h.  Since target=1 on V_h,

        1 = target + (1+target) H.

    The final remainder is lifted explicitly through the hard-core generators.
    """
    assert len(reduced_history) == len(full_history)
    prefix = ONE
    dynamic_entries = []
    total_full = target_full
    total_reduced = target_reduced

    for (label, generator), (full_label, full_generator) in zip(
        reduced_history, full_history
    ):
        assert label == full_label
        cofactor = product(
            complement(target_reduced), prefix, hard_core_reduce=True
        )
        total_reduced = anf_xor(
            total_reduced,
            product(cofactor, generator, hard_core_reduce=True),
        )
        total_full = anf_xor(
            total_full,
            product(cofactor, full_generator, hard_core_reduce=False),
        )
        dynamic_entries.append(
            {
                "generator": label,
                "generator_polynomial_reduced": anf_payload(generator),
                "generator_polynomial_unrestricted": anf_payload(full_generator),
                "cofactor": cofactor_payload(cofactor),
            }
        )
        prefix = product(prefix, complement(generator), hard_core_reduce=True)

    if total_reduced != ONE:
        raise AssertionError("reduced Bezout identity did not produce one")

    remainder = anf_xor(total_full, ONE)
    hard_core_cofactors = decompose_hard_core_remainder(remainder)
    verified = total_full
    hard_core_entries = []
    for index, cofactor in enumerate(hard_core_cofactors):
        generator = frozenset({3 << index})
        verified = anf_xor(
            verified, product(cofactor, generator, hard_core_reduce=False)
        )
        hard_core_entries.append(
            {
                "generator": f"rho_{index + 1}rho_{index + 2}",
                "generator_polynomial": anf_payload(generator),
                "cofactor": cofactor_payload(cofactor),
            }
        )
    if verified != ONE:
        raise AssertionError("full hard-core lift did not produce one")

    nonzero_dynamic = [
        entry for entry in dynamic_entries if entry["cofactor"]["term_count"]
    ]
    nonzero_hard_core = [
        entry for entry in hard_core_entries if entry["cofactor"]["term_count"]
    ]
    all_cofactors = nonzero_dynamic + nonzero_hard_core
    return {
        "target": target_label,
        "forced_one_on_V_h": forced_at_horizon,
        "identity": (
            "1 = target + sum(dynamic_cofactor*dynamic_generator) + "
            "sum(hard_core_cofactor*rho_i*rho_(i+1)) mod (rho_i^2+rho_i)"
        ),
        "target_reduced": anf_payload(target_reduced),
        "target_unrestricted": anf_payload(target_full),
        "dynamic_cofactors": dynamic_entries,
        "hard_core_cofactors": hard_core_entries,
        "nonzero_dynamic_generators": [
            entry["generator"] for entry in nonzero_dynamic
        ],
        "maximum_dynamic_cofactor_degree": max(
            entry["cofactor"]["degree"] for entry in nonzero_dynamic
        ),
        "maximum_lifted_cofactor_degree": max(
            entry["cofactor"]["degree"] for entry in all_cofactors
        ),
        "dynamic_cofactor_term_total": sum(
            entry["cofactor"]["term_count"] for entry in nonzero_dynamic
        ),
        "hard_core_lift_term_total": sum(
            entry["cofactor"]["term_count"] for entry in nonzero_hard_core
        ),
        "hard_core_remainder": anf_payload(remainder),
        "verified": True,
    }


def v8_basis_polynomials() -> list[tuple[str, ANF]]:
    """A compact exact vanishing basis for the six n=10 plateau seeds."""
    return [
        *[
            (f"rho_{i}rho_{i + 1}", frozenset({3 << (i - 1)}))
            for i in range(1, N)
        ],
        ("rho_5", variable(4)),
        ("rho_6", variable(5)),
        ("rho_7", variable(6)),
        ("1+rho_8", complement(variable(7))),
        ("rho_9", variable(8)),
        ("rho_10", variable(9)),
        (
            "rho_4+rho_2rho_4",
            anf_xor(variable(3), frozenset({(1 << 1) | (1 << 3)})),
        ),
    ]


def zeros_of(polynomials: list[tuple[str, ANF]]) -> list[int]:
    return [
        seed
        for seed in range(1 << N)
        if all(evaluate(polynomial, seed) == 0 for _, polynomial in polynomials)
    ]


def reduce_v8(value: ANF) -> ANF:
    """Canonical reduction by the compact V_8 basis in grevlex orientation."""
    zero_variables = sum(1 << index for index in (4, 5, 6, 8, 9))
    rho_8 = 1 << 7
    answer: set[int] = set()
    for monomial in value:
        if monomial & (monomial >> 1):
            continue
        if monomial & zero_variables:
            continue
        monomial &= ~rho_8
        # Leading monomial rho_2*rho_4 reduces to rho_4.
        if (monomial & (1 << 1)) and (monomial & (1 << 3)):
            monomial &= ~(1 << 1)
        if monomial in answer:
            answer.remove(monomial)
        else:
            answer.add(monomial)
    return frozenset(answer)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    reduced = emission_trace(TERMINAL_OFFSET + 1, hard_core_reduce=True)
    unrestricted = emission_trace(TERMINAL_OFFSET + 1, hard_core_reduce=False)
    varieties = survivor_sets(reduced)
    expected_counts = [144, 72, 28, 11, 11, 6, 6, 6, 6, 0]
    assert [len(variety) for variety in varieties] == expected_counts

    plateau_seeds = varieties[8]
    basis = v8_basis_polynomials()
    assert zeros_of(basis) == plateau_seeds

    plateau_offsets = [3, 5, 6, 7]
    residues = []
    for offset in plateau_offsets:
        pin = reduce_v8(reduced[offset].pin_emission)
        obstruction = reduce_v8(reduced[offset].hard_core_obstruction)
        assert pin == obstruction == ZERO
        residues.append(
            {
                "macro_offset": offset,
                "pin_normal_form_mod_V8": anf_payload(pin),
                "no_11_normal_form_mod_V8": anf_payload(obstruction),
            }
        )

    terminal_pin = reduce_v8(reduced[8].pin_emission)
    terminal_obstruction = reduce_v8(reduced[8].hard_core_obstruction)
    assert terminal_pin == terminal_obstruction == ONE

    pin_first = next(
        h
        for h, variety in enumerate(varieties)
        if variety and all(
            evaluate(reduced[8].pin_emission, seed) == 1 for seed in variety
        )
    )
    obstruction_first = next(
        h
        for h, variety in enumerate(varieties)
        if variety and all(
            evaluate(reduced[8].hard_core_obstruction, seed) == 1
            for seed in variety
        )
    )
    assert (pin_first, obstruction_first) == (3, 5)

    pin_certificate = bezout_certificate(
        target_label="epsilon_8",
        target_reduced=reduced[8].pin_emission,
        target_full=unrestricted[8].pin_emission,
        reduced_history=dynamic_generators(reduced, pin_first),
        full_history=dynamic_generators(unrestricted, pin_first),
        forced_at_horizon=pin_first,
    )
    obstruction_certificate = bezout_certificate(
        target_label="q_8",
        target_reduced=reduced[8].hard_core_obstruction,
        target_full=unrestricted[8].hard_core_obstruction,
        reduced_history=dynamic_generators(reduced, obstruction_first),
        full_history=dynamic_generators(unrestricted, obstruction_first),
        forced_at_horizon=obstruction_first,
    )

    result = {
        "schema": "crosstalk.rule30.n10-plateau-bezout.v1",
        "n": N,
        "variety_counts": expected_counts,
        "plateau_V8_seeds_hex": [hex(seed) for seed in plateau_seeds],
        "compact_V8_basis": [
            {"label": label, "polynomial": anf_payload(polynomial)}
            for label, polynomial in basis
        ],
        "plateau_residues": residues,
        "terminal_residues": {
            "epsilon_8_mod_V8": anf_payload(terminal_pin),
            "q_8_mod_V8": anf_payload(terminal_obstruction),
        },
        "epsilon_8_certificate": pin_certificate,
        "q_8_certificate": obstruction_certificate,
    }

    print(f"n=10 variety counts: {expected_counts}")
    print(f"V_8 seeds: {[hex(seed) for seed in plateau_seeds]}")
    print("plateau offsets 3,5,6,7: epsilon=q=0 modulo I(V_8) PASS")
    print("terminal offset 8: epsilon_8=q_8=1 modulo I(V_8) PASS")
    for certificate in (pin_certificate, obstruction_certificate):
        print(
            f"{certificate['target']}: already 1 on "
            f"V_{certificate['forced_one_on_V_h']}; "
            f"dynamic generators={certificate['nonzero_dynamic_generators']}; "
            f"max dynamic degree={certificate['maximum_dynamic_cofactor_degree']}; "
            f"max lifted degree={certificate['maximum_lifted_cofactor_degree']}; "
            "Bezout identity PASS"
        )

    if args.json is not None:
        args.json.write_text(json.dumps(result, indent=2) + "\n")
        print(f"wrote {args.json}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact quotient-ring audit of the proposed cofactor automaton.

The audit never enumerates seed assignments.  It constructs the dynamic
emission generators as Boolean ANFs, computes the survivor indicator

    P_k = product_{i<k} (1 + g_i),

in the hard-core quotient, and uses the first k for which

    (1 + target) P_k = 0.

The ordered-prefix Bezout cofactors are therefore

    C_i = (1 + target) P_i,

and obey the exact transition C_(i+1) = C_i (1 + g_i).  Translation
normalization of each whole cofactor gives an unambiguous dictionary of
shifted polynomial motifs.  The resulting graph tests the proposed closure,
degree-preservation, shift, determinism, and acyclicity claims directly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from dataclasses import dataclass
from math import comb
from pathlib import Path
from typing import Any, Iterable

from pivot_emission_audit import (
    ANF,
    ONE,
    ZERO,
    anf_payload,
    anf_product,
    anf_xor,
    complement,
    degree,
    symbolic_forced_macro,
    symbolic_seed_state,
    variable,
)


CASES = (10, 12)


@dataclass(frozen=True)
class Generator:
    label: str
    macro_offset: int
    kind: str
    polynomial: ANF


def product(left: ANF, right: ANF) -> ANF:
    return anf_product(left, right, hard_core_reduce=True)


def variable_support(value: ANF) -> list[int]:
    mask = 0
    for monomial in value:
        mask |= monomial
    return [
        index + 1
        for index in range(mask.bit_length())
        if (mask >> index) & 1
    ]


def polynomial_payload(value: ANF) -> dict[str, Any]:
    answer = anf_payload(value)
    support = variable_support(value)
    answer["variable_support"] = support
    answer["support_span"] = support[-1] - support[0] + 1 if support else 0
    return answer


def translate(value: ANF, displacement: int) -> ANF:
    """Translate every variable index, leaving the constant monomial fixed."""
    if displacement == 0:
        return value
    if displacement > 0:
        return frozenset(
            0 if monomial == 0 else monomial << displacement
            for monomial in value
        )
    shift = -displacement
    forbidden = (1 << shift) - 1
    if any(monomial & forbidden for monomial in value):
        raise ValueError("translation would cross the left boundary")
    return frozenset(
        0 if monomial == 0 else monomial >> shift for monomial in value
    )


def normalized_motif(value: ANF) -> tuple[ANF, int | None]:
    """Return the left-anchored translate and its original zero-based anchor."""
    support = variable_support(value)
    if not support:
        return value, None
    anchor = support[0] - 1
    return translate(value, -anchor), anchor


def motif_key(value: ANF) -> tuple[int, ...]:
    return tuple(sorted(value, key=lambda item: (item.bit_count(), item)))


def motif_id(value: ANF) -> str:
    encoded = ",".join(map(str, motif_key(value))).encode()
    return "motif-" + hashlib.sha256(encoded).hexdigest()[:12]


def emission_generators(length: int, maximum_macros: int) -> list[Generator]:
    state = symbolic_seed_state(length, hard_core_reduce=True)
    previous = variable(length - 1)
    answer: list[Generator] = []
    for macro in range(maximum_macros):
        emission = symbolic_forced_macro(
            state, previous, hard_core_reduce=True
        )
        answer.extend(
            (
                Generator(
                    f"epsilon_{macro}",
                    macro,
                    "pin_emission",
                    emission.pin_emission,
                ),
                Generator(
                    f"q_{macro}",
                    macro,
                    "no_11_obstruction",
                    emission.hard_core_obstruction,
                ),
            )
        )
        previous = emission.forced_rho
        state = emission.successor
    return answer


def first_unit_prefix(generators: Iterable[Generator]) -> int | None:
    prefix = ONE
    for index, generator in enumerate(generators, start=1):
        prefix = product(prefix, complement(generator.polynomial))
        if prefix == ZERO:
            return index
    return None


def first_forcing_prefix(target: ANF, generators: list[Generator]) -> int:
    prefix = ONE
    if product(complement(target), prefix) == ZERO:
        return 0
    for index, generator in enumerate(generators, start=1):
        prefix = product(prefix, complement(generator.polynomial))
        if product(complement(target), prefix) == ZERO:
            return index
    raise AssertionError("target is not forced by the supplied generators")


def certificate(
    target_label: str, target: ANF, generators: list[Generator]
) -> dict[str, Any]:
    forcing_prefix = first_forcing_prefix(target, generators)
    prefix = ONE
    total = target
    entries: list[dict[str, Any]] = []
    cofactors: list[ANF] = []

    for index, generator in enumerate(generators[:forcing_prefix]):
        cofactor = product(complement(target), prefix)
        cofactors.append(cofactor)
        total = anf_xor(total, product(cofactor, generator.polynomial))
        after = product(cofactor, complement(generator.polynomial))
        prefix = product(prefix, complement(generator.polynomial))
        assert after == product(complement(target), prefix)
        entries.append(
            {
                "generator_index": index,
                "generator": generator.label,
                "macro_offset": generator.macro_offset,
                "kind": generator.kind,
                "generator_polynomial": polynomial_payload(
                    generator.polynomial
                ),
                "cofactor": polynomial_payload(cofactor),
                "cofactor_after": polynomial_payload(after),
            }
        )

    final_cofactor = product(complement(target), prefix)
    assert final_cofactor == ZERO
    assert total == ONE

    nonzero = [value for value in cofactors if value]
    return {
        "target": target_label,
        "target_polynomial": polynomial_payload(target),
        "first_forcing_generator_prefix": forcing_prefix,
        "first_forcing_macro_horizon": (forcing_prefix + 1) // 2,
        "identity": (
            "1 = target + sum_i cofactor_i*generator_i in the Boolean "
            "hard-core quotient"
        ),
        "cofactor_recurrence": "C_(i+1) = C_i*(1+g_i)",
        "entries": entries,
        "final_cofactor": polynomial_payload(final_cofactor),
        "maximum_dynamic_cofactor_degree": max(map(degree, nonzero)),
        "maximum_dynamic_cofactor_support_span": max(
            polynomial_payload(value)["support_span"] for value in nonzero
        ),
        "nonzero_cofactor_count": len(nonzero),
        "unique_exact_cofactor_count": len(set(nonzero)),
        "verified": True,
    }


def exact_n10_reference_check(
    certificates: list[dict[str, Any]], reference_path: Path
) -> dict[str, Any]:
    data = json.loads(reference_path.read_text())
    answer: dict[str, Any] = {}
    for certificate_data in certificates:
        target = certificate_data["target"]
        reference = data[f"{target}_certificate"]
        expected = [
            (
                entry["generator"],
                tuple(entry["cofactor"]["monomial_masks"]),
            )
            for entry in reference["dynamic_cofactors"]
            if entry["cofactor"]["term_count"]
        ]
        actual = [
            (
                entry["generator"],
                tuple(entry["cofactor"]["monomial_masks"]),
            )
            for entry in certificate_data["entries"]
            if entry["cofactor"]["term_count"]
        ]
        if actual != expected:
            raise AssertionError(f"n=10 {target} cofactors differ from reference")
        answer[target] = {
            "reference_nonzero_cofactor_count": len(expected),
            "exact_match": True,
        }
    return answer


def payload_polynomial(payload: dict[str, Any]) -> ANF:
    return frozenset(payload["monomial_masks"])


def annotate_dictionary(cases: list[dict[str, Any]]) -> dict[str, Any]:
    occurrences: dict[ANF, list[dict[str, Any]]] = defaultdict(list)

    for case in cases:
        for certificate_data in case["certificates"]:
            target = certificate_data["target"]
            sequence = [
                payload_polynomial(entry["cofactor"])
                for entry in certificate_data["entries"]
            ]
            sequence.append(ZERO)
            for index, value in enumerate(sequence):
                normalized, anchor = normalized_motif(value)
                occurrences[normalized].append(
                    {
                        "n": case["n"],
                        "target": target,
                        "sequence_index": index,
                        "anchor_one_based": None if anchor is None else anchor + 1,
                        "polynomial": polynomial_payload(value),
                    }
                )

    ordered = sorted(
        occurrences,
        key=lambda item: (degree(item), len(item), motif_key(item)),
    )
    ids = {value: motif_id(value) for value in ordered}
    dictionary = [
        {
            "motif_id": ids[value],
            "normalized_polynomial": polynomial_payload(value),
            "occurrence_count": len(occurrences[value]),
            "occurrences": occurrences[value],
        }
        for value in ordered
    ]

    generator_edges: list[dict[str, Any]] = []
    macro_edges: list[dict[str, Any]] = []
    for case in cases:
        for certificate_data in case["certificates"]:
            target = certificate_data["target"]
            entries = certificate_data["entries"]
            sequence = [payload_polynomial(entry["cofactor"]) for entry in entries]
            sequence.append(ZERO)
            for entry, source, destination in zip(
                entries, sequence, sequence[1:]
            ):
                generator_edges.append(
                    transition_payload(
                        source,
                        destination,
                        ids,
                        n=case["n"],
                        target=target,
                        label=entry["generator"],
                    )
                )

            first = 0
            while first < len(entries):
                macro = entries[first]["macro_offset"]
                last = first
                while (
                    last + 1 < len(entries)
                    and entries[last + 1]["macro_offset"] == macro
                ):
                    last += 1
                labels = ",".join(
                    entry["generator"] for entry in entries[first : last + 1]
                )
                macro_edges.append(
                    transition_payload(
                        sequence[first],
                        sequence[last + 1],
                        ids,
                        n=case["n"],
                        target=target,
                        label=f"macro_{macro}[{labels}]",
                    )
                )
                first = last + 1

    graph = graph_audit(macro_edges, ids[ZERO])
    cross_n_shared = [
        ids[value]
        for value in ordered
        if value != ZERO
        and len({occurrence["n"] for occurrence in occurrences[value]}) > 1
    ]
    return {
        "normalization": (
            "translate the least supported rho index to rho_1; constants "
            "are fixed"
        ),
        "dictionary_size_including_zero": len(dictionary),
        "cross_n_shared_nonzero_motif_count": len(cross_n_shared),
        "cross_n_shared_nonzero_motifs": cross_n_shared,
        "dictionary": dictionary,
        "generator_transitions": generator_edges,
        "macro_transitions": macro_edges,
        "macro_graph_audit": graph,
    }


def transition_payload(
    source: ANF,
    destination: ANF,
    ids: dict[ANF, str],
    *,
    n: int,
    target: str,
    label: str,
) -> dict[str, Any]:
    source_normalized, source_anchor = normalized_motif(source)
    destination_normalized, destination_anchor = normalized_motif(destination)
    shift_delta = None
    if source_normalized == destination_normalized and source_anchor is not None:
        assert destination_anchor is not None
        shift_delta = destination_anchor - source_anchor
        assert translate(source, shift_delta) == destination
    return {
        "n": n,
        "target": target,
        "label": label,
        "source_motif": ids[source_normalized],
        "destination_motif": ids[destination_normalized],
        "source_degree": degree(source),
        "destination_degree": degree(destination),
        "degree_preserving": degree(source) == degree(destination),
        "is_translate": shift_delta is not None,
        "shift_delta": shift_delta,
        "right_shift": shift_delta is not None and shift_delta > 0,
        "stationary_exact": source == destination,
    }


def graph_audit(
    edges: list[dict[str, Any]], zero_motif: str
) -> dict[str, Any]:
    nonterminal = [
        edge for edge in edges if edge["destination_motif"] != zero_motif
    ]
    self_loops = [
        edge
        for edge in nonterminal
        if edge["source_motif"] == edge["destination_motif"]
    ]
    adjacency: dict[str, set[str]] = defaultdict(set)
    indegree: dict[str, int] = defaultdict(int)
    nodes: set[str] = set()
    for edge in nonterminal:
        source = edge["source_motif"]
        destination = edge["destination_motif"]
        nodes.update((source, destination))
        if destination not in adjacency[source]:
            adjacency[source].add(destination)
            indegree[destination] += 1
            indegree.setdefault(source, indegree[source])
    queue = [node for node in nodes if indegree[node] == 0]
    visited = 0
    while queue:
        source = queue.pop()
        visited += 1
        for destination in adjacency[source]:
            indegree[destination] -= 1
            if indegree[destination] == 0:
                queue.append(destination)

    destinations: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        destinations[edge["source_motif"]].add(edge["destination_motif"])
    nondeterministic = {
        source: sorted(values)
        for source, values in destinations.items()
        if len(values) > 1
    }
    return {
        "observed_transition_codomain_closed": True,
        "all_nonterminal_transitions_degree_preserving": all(
            edge["degree_preserving"] for edge in nonterminal
        ),
        "all_nonterminal_transitions_are_translates": all(
            edge["is_translate"] for edge in nonterminal
        ),
        "right_shift_transition_count": sum(
            edge["right_shift"] for edge in nonterminal
        ),
        "stationary_exact_transition_count": sum(
            edge["stationary_exact"] for edge in nonterminal
        ),
        "self_loops": self_loops,
        "acyclic": visited == len(nodes),
        "motif_only_deterministic": not nondeterministic,
        "nondeterministic_motif_destinations": nondeterministic,
        "note": (
            "codomain closure is only closure of the extracted observations; "
            "it is not a proof of closure for arbitrary n"
        ),
    }


def hard_core_degree_dimension(length: int, maximum_degree: int) -> int:
    """Number of no-adjacent square-free monomials through the given degree."""
    return sum(
        comb(length - size + 1, size)
        for size in range(min(maximum_degree, (length + 1) // 2) + 1)
    )


def build_result(reference_path: Path) -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    for length in CASES:
        generators = emission_generators(length, 2 * length + 2)
        unit_prefix = first_unit_prefix(generators)
        if unit_prefix is None:
            raise AssertionError(f"no unit prefix found for n={length}")
        terminal_macro = (unit_prefix - 1) // 2
        terminal_generators = generators[: 2 * (terminal_macro + 1)]
        epsilon = terminal_generators[2 * terminal_macro]
        obstruction = terminal_generators[2 * terminal_macro + 1]
        certificates = [
            certificate(epsilon.label, epsilon.polynomial, terminal_generators),
            certificate(
                obstruction.label,
                obstruction.polynomial,
                terminal_generators,
            ),
        ]
        case: dict[str, Any] = {
            "n": length,
            "first_unit_generator_prefix": unit_prefix,
            "first_unit_macro_horizon": terminal_macro + 1,
            "terminal_macro_offset": terminal_macro,
            "certificates": certificates,
        }
        if length == 10:
            case["n10_reference_check"] = exact_n10_reference_check(
                certificates, reference_path
            )
        cases.append(case)

    motifs = annotate_dictionary(cases)
    maximum_degrees = {
        str(case["n"]): max(
            certificate_data["maximum_dynamic_cofactor_degree"]
            for certificate_data in case["certificates"]
        )
        for case in cases
    }
    maximum_spans = {
        str(case["n"]): max(
            certificate_data["maximum_dynamic_cofactor_support_span"]
            for certificate_data in case["certificates"]
        )
        for case in cases
    }
    return {
        "schema": "crosstalk.rule30.cofactor-automaton-audit.v1",
        "method": {
            "seed_enumeration": False,
            "ring": (
                "F_2[rho_1,...,rho_n]/<rho_i^2+rho_i, "
                "rho_i rho_(i+1)>"
            ),
            "certificate_choice": "canonical ordered-prefix survivor indicator",
        },
        "cases": cases,
        "shift_normalized_motifs": motifs,
        "uniformity_audit": {
            "maximum_dynamic_cofactor_degree_by_n": maximum_degrees,
            "degree_five_cap_survives_n12": maximum_degrees["12"] <= 5,
            "maximum_dynamic_cofactor_support_span_by_n": maximum_spans,
            "bounded_spatial_footprint_established": False,
            "hard_core_degree_at_most_five_dimension": {
                str(length): hard_core_degree_dimension(length, 5)
                for length in CASES
            },
            "finite_dimension_independent_of_n_from_degree_bound": False,
        },
        "conclusion": {
            "observed_dictionary_is_degree_preserving_shift_closed": (
                motifs["macro_graph_audit"][
                    "all_nonterminal_transitions_degree_preserving"
                ]
                and motifs["macro_graph_audit"][
                    "all_nonterminal_transitions_are_translates"
                ]
            ),
            "observed_motif_graph_is_acyclic": motifs["macro_graph_audit"][
                "acyclic"
            ],
            "supports_uniform_2n_plus_2_proof": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    directory = Path(__file__).resolve().parent
    parser.add_argument(
        "--n10-reference",
        type=Path,
        default=directory / "plateau-bezout-n10.json",
    )
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    result = build_result(args.n10_reference)
    graph = result["shift_normalized_motifs"]["macro_graph_audit"]
    print("n=10 reference cofactors: exact match PASS")
    for case in result["cases"]:
        profiles = ", ".join(
            f"{item['target']}: force-prefix="
            f"{item['first_forcing_generator_prefix']}, "
            f"degree={item['maximum_dynamic_cofactor_degree']}, "
            f"span={item['maximum_dynamic_cofactor_support_span']}"
            for item in case["certificates"]
        )
        print(f"n={case['n']}: {profiles}; quotient Bezout identities PASS")
    print(
        "macro motif graph: "
        f"acyclic={graph['acyclic']}, "
        "degree-preserving="
        f"{graph['all_nonterminal_transitions_degree_preserving']}, "
        f"shift-only={graph['all_nonterminal_transitions_are_translates']}, "
        f"self-loops={len(graph['self_loops'])}, "
        f"right-shifts={graph['right_shift_transition_count']}"
    )
    print("cofactor-automaton uniformity criterion: FAIL")

    if args.json is not None:
        args.json.write_text(json.dumps(result, indent=2) + "\n")
        print(f"wrote {args.json}")


if __name__ == "__main__":
    main()

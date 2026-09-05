#!/usr/bin/env python3
"""Standalone verifier for cofactor-automaton-n10-n12.json.

This checker does not import the frontier recurrence.  It verifies every
recorded ordered-prefix Bezout identity and cofactor transition using only
the monomial masks in the artifact.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


Polynomial = frozenset[int]
ZERO: Polynomial = frozenset()
ONE: Polynomial = frozenset({0})


def polynomial(payload: dict[str, Any]) -> Polynomial:
    return frozenset(payload["monomial_masks"])


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    return left ^ right


def complement(value: Polynomial) -> Polynomial:
    return add(ONE, value)


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: set[int] = set()
    for first in left:
        for second in right:
            monomial = first | second
            if monomial & (monomial >> 1):
                continue
            if monomial in answer:
                answer.remove(monomial)
            else:
                answer.add(monomial)
    return frozenset(answer)


def verify_certificate(certificate: dict[str, Any]) -> None:
    total = polynomial(certificate["target_polynomial"])
    previous_after: Polynomial | None = None
    for entry in certificate["entries"]:
        cofactor = polynomial(entry["cofactor"])
        generator = polynomial(entry["generator_polynomial"])
        after = polynomial(entry["cofactor_after"])
        if previous_after is not None and cofactor != previous_after:
            raise AssertionError("cofactor sequence is not contiguous")
        expected_after = multiply(cofactor, complement(generator))
        if after != expected_after:
            raise AssertionError(
                f"bad transition at {certificate['target']}/{entry['generator']}"
            )
        total = add(total, multiply(cofactor, generator))
        previous_after = after
    if previous_after != ZERO:
        raise AssertionError(f"{certificate['target']} did not reach zero")
    if polynomial(certificate["final_cofactor"]) != ZERO:
        raise AssertionError("recorded final cofactor is nonzero")
    if total != ONE:
        raise AssertionError(f"bad Bezout identity for {certificate['target']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    data = json.loads(args.artifact.read_text())
    if data.get("schema") != "crosstalk.rule30.cofactor-automaton-audit.v1":
        raise AssertionError("unexpected schema")
    if data["method"]["seed_enumeration"]:
        raise AssertionError("artifact unexpectedly used seed enumeration")

    count = 0
    for case in data["cases"]:
        for certificate in case["certificates"]:
            verify_certificate(certificate)
            count += 1

    graph = data["shift_normalized_motifs"]["macro_graph_audit"]
    if graph["acyclic"] or not graph["self_loops"]:
        raise AssertionError("recorded motif graph must contain its exact loop")
    if data["uniformity_audit"]["degree_five_cap_survives_n12"]:
        raise AssertionError("recorded n=12 cofactors must break degree five")
    print(
        f"{count} quotient Bezout identities and all cofactor transitions PASS; "
        "degree-5 cap and DAG criteria FAIL as recorded"
    )


if __name__ == "__main__":
    main()

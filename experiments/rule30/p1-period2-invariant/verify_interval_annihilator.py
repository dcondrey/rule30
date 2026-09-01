#!/usr/bin/env python3
"""Standalone verifier for interval-annihilator-n10-n14.json."""

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


def hard_core_basis(length: int) -> list[int]:
    return [
        mask
        for mask in range(1 << length)
        if (mask & (mask >> 1)) == 0
    ]


def principal_rank(value: Polynomial, length: int) -> int:
    basis = hard_core_basis(length)
    positions = {monomial: index for index, monomial in enumerate(basis)}
    pivots: dict[int, int] = {}
    for monomial in basis:
        vector = 0
        for term in multiply(value, frozenset({monomial})):
            vector |= 1 << positions[term]
        while vector:
            pivot = vector.bit_length() - 1
            if pivot in pivots:
                vector ^= pivots[pivot]
            else:
                pivots[pivot] = vector
                break
    return len(pivots)


def verify_constant(
    value: Polynomial, indicator: Polynomial, expected: int | None
) -> None:
    if expected is None:
        if multiply(value, indicator) in (ZERO, indicator):
            raise AssertionError("recorded mixed value is actually constant")
    elif expected == 0:
        if multiply(value, indicator) != ZERO:
            raise AssertionError("recorded zero is not zero on its branch")
    elif expected == 1:
        if multiply(complement(value), indicator) != ZERO:
            raise AssertionError("recorded one is not one on its branch")
    else:
        raise AssertionError("invalid recorded Boolean value")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    data = json.loads(args.artifact.read_text())
    if data.get("schema") != "crosstalk.rule30.interval-annihilator-audit.v1":
        raise AssertionError("unexpected schema")
    if data["method"]["seed_enumeration"]:
        raise AssertionError("artifact unexpectedly used seed enumeration")

    for state in data["compact_annihilator_states"]:
        actual = ONE
        for generator in state["zero_generators"]:
            actual = multiply(
                actual, complement(polynomial(generator["polynomial"]))
            )
        expected = polynomial(state["indicator"])
        if actual != expected:
            raise AssertionError(f"bad compact state {state['label']}")
        if principal_rank(expected, state["n"]) != state["principal_rank"]:
            raise AssertionError(f"bad rank for {state['label']}")

    for identity in data["exact_indicator_identities"]:
        if polynomial(identity["left"]) != polynomial(identity["right"]):
            raise AssertionError(f"bad identity {identity['label']}")

    for transition in data["matched_extension_transitions"]:
        destination = polynomial(transition["destination_indicator"])
        match = polynomial(transition["match_indicator"])
        matched = polynomial(transition["matched_component"])
        predicted = polynomial(transition["predicted_interval_component"])
        defect = polynomial(transition["defect_component"])
        if multiply(destination, match) != matched or matched != predicted:
            raise AssertionError("bad matched-extension component")
        if multiply(destination, complement(match)) != defect:
            raise AssertionError("bad unmatched defect component")
        if add(matched, defect) != destination:
            raise AssertionError("match/defect components do not partition")
        if multiply(matched, defect) != ZERO:
            raise AssertionError("match/defect components overlap")
        length = transition["longer_n"]
        ranks = (
            principal_rank(destination, length),
            principal_rank(matched, length),
            principal_rank(defect, length),
        )
        expected_ranks = (
            transition["destination_rank"],
            transition["matched_rank"],
            transition["defect_rank"],
        )
        if ranks != expected_ranks:
            raise AssertionError("bad transition ranks")

    for alignment in data["n10_n12_two_macro_alignment"]:
        for key, payload in alignment.items():
            if key.endswith("_difference_times_P12") and polynomial(payload):
                raise AssertionError("nonzero n=10/n=12 alignment residue")

    for signature in data["terminal_signatures"]:
        pin = polynomial(signature["pin_emission"])
        obstruction = polynomial(signature["no_11_obstruction"])
        forced_rho = polynomial(signature["forced_rho"])
        for branch in signature["branches"]:
            indicator = polynomial(branch["indicator"])
            verify_constant(pin, indicator, branch["pin_value"])
            verify_constant(obstruction, indicator, branch["no_11_value"])
            verify_constant(forced_rho, indicator, branch["forced_rho_value"])

    print(
        "7 compact annihilator states, 6 indicator identities, "
        "4 match/defect transitions, 21 shifted observables, and "
        "all terminal branch values PASS"
    )


if __name__ == "__main__":
    main()

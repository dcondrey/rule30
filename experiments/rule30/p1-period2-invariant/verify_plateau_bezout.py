#!/usr/bin/env python3
"""Standalone verifier for plateau-bezout-n10.json.

This intentionally does not import the symbolic frontier implementation.  It
checks the expanded Boolean Bezout identities directly from the recorded
monomial masks and verifies the compact six-point plateau variety.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


Polynomial = frozenset[int]
ONE: Polynomial = frozenset({0})


def polynomial(payload: dict[str, Any]) -> Polynomial:
    return frozenset(payload["monomial_masks"])


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    return left ^ right


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: set[int] = set()
    for first in left:
        for second in right:
            monomial = first | second
            if monomial in answer:
                answer.remove(monomial)
            else:
                answer.add(monomial)
    return frozenset(answer)


def evaluate(value: Polynomial, assignment: int) -> int:
    answer = 0
    for monomial in value:
        answer ^= int((assignment & monomial) == monomial)
    return answer


def verify_certificate(certificate: dict[str, Any]) -> None:
    total = polynomial(certificate["target_unrestricted"])
    for entry in certificate["dynamic_cofactors"]:
        total = add(
            total,
            multiply(
                polynomial(entry["cofactor"]),
                polynomial(entry["generator_polynomial_unrestricted"]),
            ),
        )
    for entry in certificate["hard_core_cofactors"]:
        total = add(
            total,
            multiply(
                polynomial(entry["cofactor"]),
                polynomial(entry["generator_polynomial"]),
            ),
        )
    if total != ONE:
        raise AssertionError(f"Bezout identity failed for {certificate['target']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()
    data = json.loads(args.artifact.read_text())
    if data.get("schema") != "crosstalk.rule30.n10-plateau-bezout.v1":
        raise AssertionError("unexpected schema")

    expected_seeds = [int(value, 16) for value in data["plateau_V8_seeds_hex"]]
    basis = [
        polynomial(entry["polynomial"])
        for entry in data["compact_V8_basis"]
    ]
    actual_seeds = [
        seed
        for seed in range(1 << data["n"])
        if all(evaluate(item, seed) == 0 for item in basis)
    ]
    if actual_seeds != expected_seeds:
        raise AssertionError("compact V_8 basis has the wrong zero set")

    verify_certificate(data["epsilon_8_certificate"])
    verify_certificate(data["q_8_certificate"])
    print(
        f"compact basis: {len(actual_seeds)} exact zeros PASS; "
        "epsilon_8 and q_8 Boolean Bezout identities PASS"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Standalone verifier for a defect-restart-cocycle.v1 artifact."""

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
        if mask & (mask >> 1) == 0
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


def verify_rank(payload: dict[str, Any], length: int) -> Polynomial:
    value = polynomial(payload)
    if principal_rank(value, length) != payload["principal_rank"]:
        raise AssertionError("incorrect recorded principal rank")
    return value


def verify_partition(
    parent: Polynomial,
    left: Polynomial,
    right: Polynomial,
    ranks: list[int],
) -> None:
    if add(left, right) != parent:
        raise AssertionError("components do not sum to parent")
    if multiply(left, right) != ZERO:
        raise AssertionError("components overlap")
    if ranks[0] != ranks[1] + ranks[2]:
        raise AssertionError("partition ranks are not additive")


def verify_advance(record: dict[str, Any]) -> None:
    length = record["n"]
    parent = verify_rank(record["previous_indicator"], length)
    following = verify_rank(record["following_indicator"], length)
    removed = verify_rank(record["removed_component"], length)
    pin = polynomial(record["pin_emission"])
    obstruction = polynomial(record["no_11_obstruction"])
    factor = polynomial(record["good_factor"])
    expected_factor = multiply(complement(pin), complement(obstruction))
    if factor != expected_factor:
        raise AssertionError("bad advance good factor")
    if multiply(parent, factor) != following:
        raise AssertionError("bad following indicator")
    if multiply(parent, complement(factor)) != removed:
        raise AssertionError("bad removed component")
    verify_partition(parent, following, removed, record["rank_partition"])
    strict = record["rank_partition"][1] < record["rank_partition"][0]
    if strict != record["strict_rank_contraction"]:
        raise AssertionError("bad strictness flag")
    if (parent == following) != record["absorbed_generator"]:
        raise AssertionError("bad absorption flag")


def verify_restart(record: dict[str, Any]) -> None:
    length = record["n"]
    parent = verify_rank(record["future_good_parent"], length)
    continuous = verify_rank(record["continuous_component"], length)
    restart = verify_rank(record["restart_component"], length)
    pin = polynomial(record["pin_emission"])
    obstruction = polynomial(record["no_11_obstruction"])
    factor = polynomial(record["good_factor"])
    expected_factor = multiply(complement(pin), complement(obstruction))
    if factor != expected_factor:
        raise AssertionError("bad restart good factor")
    if multiply(parent, factor) != continuous:
        raise AssertionError("bad continuous component")
    if continuous != polynomial(record["expected_continuous_interval"]):
        raise AssertionError("bad continuous interval identity")
    if multiply(parent, complement(factor)) != restart:
        raise AssertionError("bad restart component")
    verify_partition(parent, continuous, restart, record["rank_partition"])


def verify_extension(record: dict[str, Any]) -> None:
    length = record["longer_n"]
    parent = verify_rank(record["destination_indicator"], length)
    matched = verify_rank(record["matched_component"], length)
    defect = verify_rank(record["mismatch_defect_component"], length)
    match = polynomial(record["match_indicator"])
    predicted = polynomial(record["predicted_shifted_component"])
    if multiply(parent, match) != matched or matched != predicted:
        raise AssertionError("bad matched extension component")
    if multiply(parent, complement(match)) != defect:
        raise AssertionError("bad mismatch defect component")
    verify_partition(parent, matched, defect, record["rank_partition"])


def verify_collision(
    record: dict[str, Any], advance_records: list[dict[str, Any]]
) -> None:
    by_offset = {item["offset"]: item for item in advance_records}
    left_record = by_offset[record["left_offset"]]
    right_record = by_offset[record["right_offset"]]
    if record["left_offset"] % 3 != record["right_offset"] % 3:
        raise AssertionError("collision phases differ")
    if record["shared_phase_mod_3"] != record["left_offset"] % 3:
        raise AssertionError("bad recorded collision phase")
    shared = polynomial(record["shared_indicator"])
    if polynomial(left_record["previous_indicator"]) != shared:
        raise AssertionError("left collision source is not the shared state")
    if polynomial(right_record["previous_indicator"]) != shared:
        raise AssertionError("right collision source is not the shared state")
    left = polynomial(record["left_successor"])
    right = polynomial(record["right_successor"])
    if left != polynomial(left_record["following_indicator"]):
        raise AssertionError("left collision successor is inconsistent")
    if right != polynomial(right_record["following_indicator"]):
        raise AssertionError("right collision successor is inconsistent")
    if polynomial(record["left_good_factor"]) != polynomial(
        left_record["good_factor"]
    ):
        raise AssertionError("left collision driver is inconsistent")
    if polynomial(record["right_good_factor"]) != polynomial(
        right_record["good_factor"]
    ):
        raise AssertionError("right collision driver is inconsistent")
    if left == right:
        raise AssertionError("closure collision has equal successors")


def verify_lift(record: dict[str, Any]) -> None:
    verify_restart(record["n2_restart_split"])
    p2 = verify_rank(record["P_2_2_4"], 2)
    p3 = verify_rank(record["P_3_1_4"], 3)
    p4 = verify_rank(record["P_4_0_4"], 4)
    if p2 != frozenset({0b10}) or p4 != frozenset({0b1010}):
        raise AssertionError("unexpected exact restart/lift indicators")
    if polynomial(record["first_lift_left"]) != polynomial(
        record["first_lift_right"]
    ):
        raise AssertionError("first restart lift identity failed")
    if polynomial(record["second_lift_left"]) != polynomial(
        record["second_lift_right"]
    ):
        raise AssertionError("second restart lift identity failed")
    both = polynomial(record["both_matches"])
    if multiply(p4, both) != p4:
        raise AssertionError("lifted spike is not wholly matched")
    if p3 == ZERO:
        raise AssertionError("intermediate lifted interval is empty")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    args = parser.parse_args()

    data = json.loads(args.artifact.read_text())
    if data.get("schema") != "crosstalk.rule30.defect-restart-cocycle.v1":
        raise AssertionError("unexpected schema")
    if data["method"]["sat"] or data["method"]["seed_enumeration"]:
        raise AssertionError("artifact used a prohibited finite solver/sweep")

    advances = 0
    for records in data["advance_cocycle_controls"].values():
        for record in records:
            verify_advance(record)
            advances += 1
    for record in data["extension_match_defect_controls"]:
        verify_extension(record)
    verify_collision(
        data["indicator_phase_closure_collision"],
        data["advance_cocycle_controls"]["n10"],
    )
    verify_lift(data["restart_lift_control"])

    conclusion = data["conclusion"]
    if conclusion["principal_rank_is_strict_at_every_macro"]:
        raise AssertionError("artifact incorrectly claims strict contraction")
    if conclusion["well_founded_uniform_rank_found"]:
        raise AssertionError("artifact incorrectly claims a uniform rank")
    if conclusion["period_two_theorem_proved"]:
        raise AssertionError("artifact incorrectly claims the theorem")

    print(
        f"{advances} advance partitions, "
        f"{len(data['extension_match_defect_controls'])} extension splits, "
        "the restart lift, and the closure collision PASS"
    )


if __name__ == "__main__":
    main()

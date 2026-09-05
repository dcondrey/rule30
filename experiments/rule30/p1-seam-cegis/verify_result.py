#!/usr/bin/env python3
"""Standalone replay of the stored local seam-law certificate."""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

from cegis import FIELDS, projected_collision, target, universal_counterexample
from seam_spec import decode_map, exact_map
from typed_dsl import Expr


HERE = Path(__file__).resolve().parent


def main() -> None:
    artifact = json.loads((HERE / "cegis-result.json").read_text())
    fields = tuple(artifact["minimal_sufficient_fields"])
    expression = Expr.from_data(artifact["synthesized_expression"], fields)
    assert expression.operator_cost() == artifact["operator_cost"]
    assert expression.render() == artifact["rendered_expression"]
    assert universal_counterexample(expression) is None

    collision = projected_collision(("x", "y", "z"))
    assert collision is not None
    assert all(
        left[field] == right[field] for field in ("x", "y", "z")
        for left, right in (collision,)
    )
    assert target(collision[0]) != target(collision[1])

    checked = 0
    placement_checks = 0
    maximum = max(map(int, artifact["nonzero_delta_by_length"]))
    for length in range(1, maximum + 1):
        nonzero = 0
        for source in product((1, 2), repeat=length):
            exact = exact_map(source)
            assert decode_map(exact.phases, expression) == (exact.suffix, exact.delta)
            nonzero += int(any(exact.delta))
            checked += 1
            placement_checks += len(exact.delta)
        assert artifact["nonzero_delta_by_length"][str(length)] == [
            nonzero,
            2**length,
        ]
    assert checked == artifact["full_recurrence_exhaustive_words"]
    assert placement_checks == artifact["phase_profile_split_closure_checks"]

    corpus = json.loads((HERE / "adversarial_corpus.json").read_text())
    for record in corpus:
        exact = exact_map(tuple(map(int, record["source"])))
        assert decode_map(exact.phases, expression) == (exact.suffix, exact.delta)
        if "expected_suffix" in record:
            assert "".join(map(str, exact.suffix)) == record["expected_suffix"]
        if "expected_psi" in record:
            assert "".join(map(str, exact.psi)) == record["expected_psi"]
    assert len(corpus) == artifact["archived_obstruction_words"]

    print(f"typed expression: {expression.render()} PASS")
    print("phase-free collision: PASS")
    print("Z3 universal negation: UNSAT PASS")
    print(
        f"full recurrence: {checked} words, {placement_checks} seams, "
        f"{len(corpus)} archived words PASS"
    )


if __name__ == "__main__":
    main()

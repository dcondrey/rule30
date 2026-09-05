#!/usr/bin/env python3
"""Run the Z3-first seam-law pipeline and emit replayable artifacts."""

from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path
from typing import Any

from cegis import (
    FIELDS,
    minimal_sufficient_fields,
    projected_collision,
    run_cegis,
    target,
)
from seam_spec import (
    decode_map,
    exact_map,
    join_phase_summaries,
    summarize_phases,
)


HERE = Path(__file__).resolve().parent


def as_bits(environment: dict[str, int]) -> str:
    return "".join(str(environment[field]) for field in FIELDS)


def validate_word(source: tuple[int, ...], expression: Any) -> tuple[int, bool]:
    exact = exact_map(source)
    suffix, delta = decode_map(exact.phases, expression)
    assert suffix == exact.suffix
    assert delta == exact.delta
    summaries = tuple(
        summarize_phases(exact.phases, expression, shape)
        for shape in ("left", "right", "balanced")
    )
    assert all(summary.suffix == exact.suffix for summary in summaries)
    assert all(summary.delta == exact.delta for summary in summaries)

    # Every binary split of the known phase profile closes with one correction.
    split_checks = 0
    for split in range(1, len(exact.phases)):
        left = summarize_phases(exact.phases[:split], expression)
        right = summarize_phases(exact.phases[split:], expression)
        joined = join_phase_summaries(left, right, expression)
        assert joined.suffix == exact.suffix
        assert joined.delta == exact.delta
        split_checks += 1
    return split_checks, any(exact.delta)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-source", type=int, default=9)
    parser.add_argument("--max-cost", type=int, default=5)
    parser.add_argument("--output", type=Path, default=HERE / "cegis-result.json")
    args = parser.parse_args()
    if args.max_source < 1 or args.max_cost < 0:
        parser.error("max-source must be positive and max-cost nonnegative")

    phase_free = projected_collision(("x", "y", "z"))
    assert phase_free is not None
    variables = minimal_sufficient_fields()
    result = run_cegis(variables, args.max_cost)

    exhaustive_words = 0
    split_checks = 0
    nonzero_by_length: dict[str, list[int]] = {}
    for length in range(1, args.max_source + 1):
        nonzero = 0
        total = 0
        for source in product((1, 2), repeat=length):
            word_splits, has_defect = validate_word(source, result.expression)
            split_checks += word_splits
            nonzero += int(has_defect)
            total += 1
        nonzero_by_length[str(length)] = [nonzero, total]
        exhaustive_words += total

    corpus = json.loads((HERE / "adversarial_corpus.json").read_text())
    for record in corpus:
        source = tuple(map(int, record["source"]))
        exact = exact_map(source)
        validate_word(source, result.expression)
        if "expected_suffix" in record:
            assert "".join(map(str, exact.suffix)) == record["expected_suffix"]
        if "expected_psi" in record:
            assert "".join(map(str, exact.psi)) == record["expected_psi"]

    artifact = {
        "status": "exact-local-seam-law-proved",
        "scope_warning": (
            "The phase/holonomy decoder is universal. A recursive Join law "
            "that derives the phase profile from split source intervals is still open."
        ),
        "phase_free_projection_collision": [
            {"bits": as_bits(environment), "target": None}
            for environment in phase_free
        ],
        "minimal_sufficient_fields": list(variables),
        "synthesized_expression": result.expression.to_data(),
        "rendered_expression": result.expression.render(),
        "operator_cost": result.expression.operator_cost(),
        "semantic_library_size": result.library_size,
        "rejections": [
            {
                "candidate": rejection.expression.to_data(),
                "rendered": rejection.expression.render(),
                "minimal_counterexample": {
                    "bits": as_bits(rejection.counterexample),
                    "target": None,
                },
            }
            for rejection in result.rejections
        ],
        "z3_universal_check": "UNSAT for candidate != exact D8 seam target",
        "full_recurrence_exhaustive_words": exhaustive_words,
        "phase_profile_split_closure_checks": split_checks,
        "source_interval_split_closure": (
            "OPEN: requires a recursive Join law deriving the phase profile"
        ),
        "nonzero_delta_by_length": nonzero_by_length,
        "archived_obstruction_words": len(corpus),
    }
    for environment in artifact["phase_free_projection_collision"]:
        raw = dict(zip(FIELDS, map(int, environment["bits"])))
        environment["target"] = target(raw)
    for rejection in artifact["rejections"]:
        raw = dict(zip(FIELDS, map(int, rejection["minimal_counterexample"]["bits"])))
        rejection["minimal_counterexample"]["target"] = target(raw)

    args.output.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    print(f"phase-free collision: {artifact['phase_free_projection_collision']}")
    print(f"minimal sufficient fields: {variables}")
    print(
        f"synthesized seam law: {result.expression.render()} "
        f"(cost {result.expression.operator_cost()})"
    )
    print(f"Z3 universal identity: {artifact['z3_universal_check']}")
    print(
        f"full recurrence: {exhaustive_words} words, "
        f"{split_checks} placed seams, {len(corpus)} archived words PASS"
    )
    print(f"artifact: {args.output}")


if __name__ == "__main__":
    main()

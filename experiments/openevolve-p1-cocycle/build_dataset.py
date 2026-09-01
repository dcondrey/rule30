#!/usr/bin/env python3
"""Build exact feature records for P1 cocycle potential discovery.

The source of truth is the solver-free symbolic cocycle in
``p1-period2-invariant/defect_restart_cocycle.py``.  This script computes a
state feature vector before each exact macro transition and records the
rank-preserving transitions on which a secondary delay potential must
strictly decrease.

The feature census is deliberately finite and is only a discovery set.  A
formula found on it is not a proof; it must subsequently be verified as a
uniform Boolean-ring inequality.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
INVARIANT = HERE.parent / "rule30" / "p1-period2-invariant"
sys.path.insert(0, str(INVARIANT))

from defect_restart_cocycle import (  # noqa: E402
    CocycleState,
    advance,
    initial_state,
)
from interval_annihilator_audit import polynomial_payload  # noqa: E402
from pivot_emission_audit import ANF  # noqa: E402


OUTPUT = HERE / "cocycle_features.json"
TRAIN_WIDTHS = (2, 3, 5, 6, 7, 8, 9, 11, 13, 14)
# The holdout contains both known plateau obstructions and the widest
# tractable exact symbolic run on this machine.
HOLDOUT_WIDTHS = (4, 10, 12, 15)
MAX_STEPS = 16


def poly_stats(prefix: str, value: ANF) -> dict[str, int]:
    payload = polynomial_payload(value)
    degree_hist = Counter(mask.bit_count() for mask in value)
    weights = [mask.bit_count() for mask in value]
    return {
        f"{prefix}_terms": len(value),
        f"{prefix}_degree1": payload["degree"] + 1,
        f"{prefix}_support": len(payload["variable_support"]),
        f"{prefix}_span": payload["support_span"],
        f"{prefix}_weight": sum(weights),
        f"{prefix}_constant": int(0 in value),
        f"{prefix}_linear": degree_hist[1],
        f"{prefix}_quadratic": degree_hist[2],
        f"{prefix}_higher": sum(
            count for degree, count in degree_hist.items() if degree >= 3
        ),
    }


def family_stats(prefix: str, values: Iterable[ANF]) -> dict[str, int]:
    items = tuple(values)
    nonzero = tuple(value for value in items if value)
    degrees = [max((mask.bit_count() for mask in value), default=-1) for value in items]
    supports = []
    spans = []
    for value in items:
        payload = polynomial_payload(value)
        supports.append(len(payload["variable_support"]))
        spans.append(payload["support_span"])
    return {
        f"{prefix}_components": len(items),
        f"{prefix}_nonzero": len(nonzero),
        f"{prefix}_terms": sum(len(value) for value in items),
        f"{prefix}_degree1_sum": sum(degree + 1 for degree in degrees),
        f"{prefix}_degree1_max": max((degree + 1 for degree in degrees), default=0),
        f"{prefix}_support_sum": sum(supports),
        f"{prefix}_span_sum": sum(spans),
        f"{prefix}_constant": sum(int(0 in value) for value in items),
        f"{prefix}_weight": sum(
            mask.bit_count() for value in items for mask in value
        ),
    }


def state_features(state: CocycleState, record: dict[str, Any]) -> dict[str, int]:
    """Return nonnegative, width-agnostic algebraic statistics.

    Neither the seed width nor the macro offset is exposed to evolved code.
    This prevents the easiest finite-table and countdown cheats.  Every
    feature is a nonnegative statistic of the exact current cocycle state or
    of its locally determined next good factor.
    """
    features: dict[str, int] = {
        "rank": record["previous_indicator"]["principal_rank"],
        "removed_rank": record["removed_component"]["principal_rank"],
        "frontier_depth": state.frontier.T,
    }
    features.update(poly_stats("indicator", state.indicator))
    features.update(poly_stats("previous_rho", state.previous_rho))
    features.update(family_stats("frontier_a", state.frontier.A))
    features.update(family_stats("frontier_b", state.frontier.B))

    for prefix, key in (
        ("pin", "pin_emission"),
        ("obstruction", "no_11_obstruction"),
        ("factor", "good_factor"),
    ):
        value = frozenset(record[key]["monomial_masks"])
        features.update(poly_stats(prefix, value))

    if any(not isinstance(value, int) or value < 0 for value in features.values()):
        raise AssertionError("feature vectors must be nonnegative integers")
    return features


def exact_chain(width: int, split: str) -> dict[str, Any]:
    state = initial_state(width)
    states: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    for _ in range(MAX_STEPS):
        following, record = advance(state)
        states.append(
            {
                "offset": state.offset,
                "features": state_features(state, record),
                "indicator_masks": record["previous_indicator"]["monomial_masks"],
                "good_factor_masks": record["good_factor"]["monomial_masks"],
            }
        )
        records.append(record)
        state = following
        if record["following_indicator"]["principal_rank"] == 0:
            break

    edges = []
    for index, record in enumerate(records[:-1]):
        before, after, removed = record["rank_partition"]
        if before == 0:
            continue
        edges.append(
            {
                "from": index,
                "to": index + 1,
                "kind": "plateau" if before == after else "rank_drop",
                "rank_partition": [before, after, removed],
            }
        )
    return {
        "width": width,
        "split": split,
        "states": states,
        "edges": edges,
        "first_zero_offset": len(records),
    }


def build() -> dict[str, Any]:
    chains = []
    for width in TRAIN_WIDTHS:
        chains.append(exact_chain(width, "train"))
    for width in HOLDOUT_WIDTHS:
        chains.append(exact_chain(width, "holdout"))

    feature_names = sorted(chains[0]["states"][0]["features"])
    for chain in chains:
        for state in chain["states"]:
            if sorted(state["features"]) != feature_names:
                raise AssertionError("feature schema drift")

    plateau_counts = Counter()
    for chain in chains:
        plateau_counts[chain["split"]] += sum(
            edge["kind"] == "plateau" for edge in chain["edges"]
        )

    return {
        "schema": "crosstalk.rule30.openevolve-p1-delay.v1",
        "source": "defect_restart_cocycle.advance",
        "sat": False,
        "seed_enumeration": False,
        "proof_status": "finite discovery set only",
        "measure_target": "lexicographic (principal_rank, delay_potential)",
        "feature_names": feature_names,
        "train_widths": list(TRAIN_WIDTHS),
        "holdout_widths": list(HOLDOUT_WIDTHS),
        "plateau_edge_counts": dict(plateau_counts),
        "chains": chains,
        "controls": {
            "restart_lift": {"width": 4, "from_offset": 1, "to_offset": 4},
            "closure_collision": {"width": 10, "from_offset": 5, "to_offset": 8},
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--external-width", type=int)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.external_width is not None:
        destination = args.output or HERE / f"cocycle_features_n{args.external_width}.json"
        result = {
            "schema": "crosstalk.rule30.openevolve-p1-external.v1",
            "source": "defect_restart_cocycle.advance",
            "sat": False,
            "seed_enumeration": False,
            "proof_status": "external finite holdout only",
            "chain": exact_chain(args.external_width, "external_holdout"),
        }
        destination.write_text(json.dumps(result, indent=2) + "\n")
        print(f"wrote {destination}")
        return

    result = build()
    destination = args.output or OUTPUT
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(f"wrote {destination}")
    print(f"train plateau edges: {result['plateau_edge_counts']['train']}")
    print(f"holdout plateau edges: {result['plateau_edge_counts']['holdout']}")


if __name__ == "__main__":
    main()

"""Measure whether sampled Rule 30 tiles admit small distinguishing boundaries.

For each horizon and aligned tile scale, a deterministic greedy partition
selects perimeter positions until every observed tile interior has a unique
signature.  The count is an empirical upper bound only: the selected positions
may change with the horizon, and no composition rule is implied.
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from spacetime_grammar_probe import (
    active_cone_complement,
    eca_grid,
    greedy_boundary_signature,
    random_triangle_grid,
)
from support_state_probe import RULE_30


def parse_powers(values: Sequence[int], label: str) -> list[int]:
    parsed = sorted(set(values))
    if not parsed or any(value < 2 or value & (value - 1) for value in parsed):
        raise ValueError(f"{label} must be positive powers of two")
    return parsed


def report(horizons: Sequence[int], scales: Sequence[int]) -> None:
    sources = (
        ("rule30", lambda horizon: eca_grid(RULE_30, horizon)),
        ("random", random_triangle_grid),
        (
            "rule30_zeros",
            lambda horizon: active_cone_complement(*eca_grid(RULE_30, horizon), horizon),
        ),
    )
    print(
        "source horizon scale tile_types information_lower_bound "
        "selected_bits perimeter_bits unresolved max_group positions"
    )
    for source, make_grid in sources:
        for horizon in horizons:
            bits, side = make_grid(horizon)
            for scale in scales:
                if scale > side:
                    continue
                signature = greedy_boundary_signature(bits, side, scale)
                positions = ",".join(map(str, signature.selected_bits))
                print(
                    f"{source:13s} {horizon:7d} {scale:5d} "
                    f"{signature.tile_types:10d} {signature.information_lower_bound:23d} "
                    f"{len(signature.selected_bits):13d} {4 * scale - 4:14d} "
                    f"{signature.unresolved_groups:10d} "
                    f"{signature.largest_unresolved_group:9d} {positions}"
                )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--horizons", nargs="+", type=int, default=[64, 128, 256, 512, 1024])
    parser.add_argument("--scales", nargs="+", type=int, default=[4, 8, 16, 32])
    args = parser.parse_args()
    try:
        horizons = parse_powers(args.horizons, "horizons")
        scales = parse_powers(args.scales, "scales")
    except ValueError as error:
        parser.error(str(error))
    report(horizons, scales)


if __name__ == "__main__":
    main()

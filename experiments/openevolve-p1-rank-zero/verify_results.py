#!/usr/bin/env python3
"""Independent replay of retained OpenEvolve/GA rank-zero witnesses."""

from __future__ import annotations

import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
INVARIANT_DIR = HERE.parent / "rule30" / "p1-period2-invariant"
sys.path.insert(0, str(INVARIANT_DIR))

from dyadic_periodicity_analyzer import (  # noqa: E402
    inverse_cone_diagonal,
    terminal_cone,
)
from rank_zero_separator import (  # noqa: E402
    hard_core,
    hard_core_prefix_length,
)


RESULT_FILES = (
    "ga_witness_results.json",
    "ga_scan_24_50.json",
    "ga_t96_lifted.json",
    "ga_t43_nested.json",
    "ga_tail2_results.json",
    "ga_tail3_results.json",
)


def verify_record(record: dict[str, object]) -> None:
    cutoff = int(record["cutoff"])
    horizon = int(record["horizon"])
    tail = int(record.get("tail", 0))
    endpoint_prefix = tuple(map(int, str(record["endpoint_prefix"])))
    assert len(endpoint_prefix) == cutoff
    assert hard_core(endpoint_prefix)
    cut_prefix = inverse_cone_diagonal(endpoint_prefix)
    assert "".join(map(str, cut_prefix)) == record["cut_prefix"]
    endpoint = terminal_cone(cut_prefix + (tail,) * (horizon - cutoff))
    assert endpoint[:cutoff] == endpoint_prefix
    survival = hard_core_prefix_length(endpoint)
    assert survival == record["survival"]
    assert (survival >= horizon) == record["linear_bound_falsified"]
    assert "".join(map(str, endpoint[survival : survival + 2])) == record[
        "failure_symbols"
    ]


def verify_alternating() -> int:
    checked = 0
    for cutoff in (24, 28, 32, 40, 48, 64, 80, 96):
        prefix = tuple(1 if index % 2 == 0 else 2 for index in range(cutoff))
        horizon = 4 * cutoff + 16
        cut_prefix = inverse_cone_diagonal(prefix)
        endpoint = terminal_cone(cut_prefix + (0,) * (horizon - cutoff))
        survival = hard_core_prefix_length(endpoint)
        assert survival < 2 * cutoff + 2
        checked += 1
    return checked


def main() -> None:
    records = []
    for name in RESULT_FILES:
        path = HERE / name
        if path.exists():
            records.extend(json.loads(path.read_text()))
    for record in records:
        verify_record(record)
    calibration = [
        record
        for record in records
        if record["cutoff"] == 23 and record["survival"] == 29
    ]
    assert calibration, "the GA did not retain its T=23 exact-optimum control"
    alternating = verify_alternating()
    falsifiers = [record for record in records if record["linear_bound_falsified"]]
    print(f"retained GA witnesses replayed exactly: {len(records)} PASS")
    print(f"alternating large-cutoff witnesses replayed: {alternating} PASS")
    print("T=23 exhaustive-optimum calibration (survival 29): PASS")
    print(f"retained 2T+2 falsifiers: {len(falsifiers)}")


if __name__ == "__main__":
    main()

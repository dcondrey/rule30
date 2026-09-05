#!/usr/bin/env python3
"""Cross-check fastdk_core.d_k_table_fast against brute force for
residue r in {1,2} as well as r=0, at small n (fastdk_crosscheck.py
already covers r=0 more extensively)."""
from __future__ import annotations

import sys

from continuation_image_analysis import d_k_table as d_k_table_brute
from fastdk_core import d_k_table_fast


def check(n: int, tail: int, residue: int) -> bool:
    brute_table, _images = d_k_table_brute(n, tail, residue)
    brute_max_survival = max((k for k, f, d in brute_table if d > 0), default=0)
    fast_table, rows, fast_max_survival = d_k_table_fast(n, tail, residue)
    ok = brute_table == fast_table and brute_max_survival == fast_max_survival
    print(
        f"n={n:3d} c={tail} r={residue}: {'PASS' if ok else 'FAIL'} "
        f"max_survival={fast_max_survival} rows={rows}",
        flush=True,
    )
    return ok


def main():
    ns = [int(x) for x in sys.argv[1:]] or [6, 8, 10, 12]
    all_ok = True
    for n in ns:
        for tail in (2, 3):
            for residue in (0, 1, 2):
                all_ok = check(n, tail, residue) and all_ok
    print("ALL PASS" if all_ok else "SOME FAILED")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

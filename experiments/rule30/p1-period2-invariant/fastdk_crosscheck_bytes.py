#!/usr/bin/env python3
"""Cross-check fastdk_core_bytes.d_k_table_fast against both brute force
(continuation_image_analysis) and the already-verified tuple-based
fastdk_core.d_k_table_fast, and report timing for all three."""
from __future__ import annotations

import sys
import time

from continuation_image_analysis import d_k_table as d_k_table_brute
from fastdk_core import d_k_table_fast as d_k_table_fast_tuple
from fastdk_core_bytes import d_k_table_fast as d_k_table_fast_bytes


def check(n: int, tail: int, residue: int, *, with_brute: bool) -> bool:
    ok = True
    t0 = time.perf_counter()
    if with_brute:
        brute_table, _ = d_k_table_brute(n, tail, residue)
        brute_max = max((k for k, f, d in brute_table if d > 0), default=0)
    t1 = time.perf_counter()
    tup_table, tup_rows, tup_max = d_k_table_fast_tuple(n, tail, residue)
    t2 = time.perf_counter()
    byt_table, byt_rows, byt_max = d_k_table_fast_bytes(n, tail, residue)
    t3 = time.perf_counter()

    if with_brute:
        if brute_table != tup_table or brute_max != tup_max:
            print(f"  n={n} c={tail} r={residue}: TUPLE vs BRUTE MISMATCH")
            ok = False
    if tup_table != byt_table or tup_max != byt_max:
        print(f"  n={n} c={tail} r={residue}: BYTES vs TUPLE MISMATCH")
        print(f"    tuple: {tup_table} max={tup_max}")
        print(f"    bytes: {byt_table} max={byt_max}")
        ok = False

    brute_t = f"{t1 - t0:8.2f}s" if with_brute else "   --   "
    print(
        f"n={n:3d} c={tail} r={residue}: {'PASS' if ok else 'FAIL'}  "
        f"brute={brute_t} tuple={t2 - t1:8.2f}s bytes={t3 - t2:8.2f}s  max_survival={byt_max}",
        flush=True,
    )
    return ok


def main():
    ns = [int(x) for x in sys.argv[1:]] or [8, 10, 12, 14, 16]
    all_ok = True
    for n in ns:
        for tail in (2, 3):
            all_ok = check(n, tail, 0, with_brute=(n <= 16)) and all_ok
    print("ALL PASS" if all_ok else "SOME FAILED")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

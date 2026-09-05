#!/usr/bin/env python3
"""Cross-check fastdk_core.d_k_table_fast against the brute-force
continuation_image_analysis.d_k_table at small n. Must agree on every
(k, Fib(k+1), D_k) triple and on max_survival_row, for both tail
c in {2,3}, r=0, at every n tested, before the fast method is trusted at
larger n.
"""
from __future__ import annotations

import sys
import time

from continuation_image_analysis import d_k_table as d_k_table_brute
from fastdk_core import d_k_table_fast


def check(n: int, tail: int, residue: int) -> bool:
    t0 = time.perf_counter()
    brute_table, brute_images = d_k_table_brute(n, tail, residue)
    t1 = time.perf_counter()
    brute_max_survival = max(
        (k for k, f, d in brute_table if d > 0), default=0
    )
    # brute table's D_k is 0 only if images[k] is empty i.e. nothing
    # survived to depth k; max over k with d>0 gives max survival row.

    fast_table, rows, fast_max_survival = d_k_table_fast(n, tail, residue)
    t2 = time.perf_counter()

    ok = True
    if len(brute_table) != len(fast_table):
        print(f"  LENGTH MISMATCH brute={len(brute_table)} fast={len(fast_table)}")
        ok = False
    for (k1, f1, d1), (k2, f2, d2) in zip(brute_table, fast_table):
        if (k1, f1, d1) != (k2, f2, d2):
            print(f"  MISMATCH k={k1}: brute=(Fib={f1},D={d1}) fast=(Fib={f2},D={d2})")
            ok = False
    if brute_max_survival != fast_max_survival:
        print(
            f"  MAX_SURVIVAL MISMATCH brute={brute_max_survival} fast={fast_max_survival}"
        )
        ok = False
    status = "PASS" if ok else "FAIL"
    print(
        f"n={n:3d} c={tail} r={residue}: {status}  "
        f"brute_time={t1 - t0:8.3f}s fast_time={t2 - t1:8.3f}s "
        f"max_survival={fast_max_survival}"
    )
    return ok


def main():
    ns = [int(x) for x in sys.argv[1:]] or [8, 10, 12, 14, 16]
    all_ok = True
    for n in ns:
        for tail in (2, 3):
            ok = check(n, tail, 0)
            all_ok = all_ok and ok
    print()
    print("ALL PASS" if all_ok else "SOME FAILED")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

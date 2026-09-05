#!/usr/bin/env python3
"""Grow the n = 15 BWH+ extremal suffix cylinder through the RW census at n = 15..31.

The 18 sources with constant Psi_0..Psi_15 at n = 15 (RESULTS-PSI-ANCESTRY-LAW.md
section 6) share the suffix S = 211212112.  In RW their forced continuation
begins 12211 and dies on hard-core at step 3.  This script asks whether any
longer source ending in S (all 2^(n-9) prefixes, n = 15..31, both c) has a deep
RW run, i.e. whether the BWH+ extremal structure carries over to any RW depth.
Uses `suffix_growth.cylinder_census` (bit-sliced kernel, validated in
rw_bitsliced.py).  A counterexample is deepest == n + 2 with exact_12a > 0.

Run:  cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/bwh_suffix_cylinder.py
"""

from __future__ import annotations

import argparse
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))

from suffix_growth import cylinder_census  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--suffix", type=str, default="211212112")
    ap.add_argument("--min-n", type=int, default=15)
    ap.add_argument("--max-n", type=int, default=31)
    args = ap.parse_args()
    S = args.suffix
    print(f"suffix S={S} (|S|={len(S)}); free prefix of length n-|S|; both c; need = n+2")
    print(" n   c  free  deepest  need  slack  N_k (k=0..)   12a-exact(n+2,v=0)  sample")
    worst = None
    for n in range(args.min_n, args.max_n + 1):
        m = n - len(S)
        if m < 6:
            continue
        for c in (2, 3):
            t0 = time.time()
            N, deepest, wit, e12 = cylinder_census(S, n, c, max_block=22)
            dt = time.time() - t0
            v0 = e12.get((n + 2, 0), 0)
            slack = n + 2 - deepest
            if worst is None or slack < worst[0]:
                worst = (slack, n, c, deepest)
            flag = "  <- RW COUNTEREXAMPLE" if v0 > 0 else ""
            print(f"{n:<4}{c:<3}{m:<6}{deepest:<9}{n+2:<6}{slack:<7}{','.join(map(str, N[:deepest+1])):<40} {v0:<20}{wit[:2]}{flag}  [{dt:.1f}s]")
            sys.stdout.flush()
    print(f"minimum slack in the cylinder: {worst[0]} at n={worst[1]} c={worst[2]} (deepest {worst[3]})")


if __name__ == "__main__":
    main()

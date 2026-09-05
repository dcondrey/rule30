#!/usr/bin/env python3
"""Merging of forced orbits: distinct columns over ALL sources, no constraint.

For each n, every W in {1,2}^n is run n+2 forced steps (unstopped).  At each
level k = 0..n+2 record D_k = number of distinct columns n+k-1 (window
[-(n+k), n]) over all 2^n sources, the maximal fiber size, and log2 D_k.
Also the number of distinct (Z_{n+k-2}, Z_{n+k-1}) zero-pattern pairs P_k
(equal to D_k if the pair determines the column and the column determines
its predecessor's zero pattern; otherwise P_k <= D_k).

The Moore map reads only the even-bits at retained positions, so D_k is
non-increasing in k; the question is the rate.

Run:  cd <work dir> && uv run python uc/r1-quadratic/q2_merge.py --max-n 16
"""
from __future__ import annotations

import argparse
import math
import time
from collections import Counter
from itertools import product

from qf_common import Endpoint


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-n", type=int, default=4)
    ap.add_argument("--max-n", type=int, default=16)
    args = ap.parse_args()
    for n in range(args.min_n, args.max_n + 1):
        t0 = time.time()
        L = n + 2
        cols = [Counter() for _ in range(L + 1)]
        pairs = [set() for _ in range(L + 1)]
        for src in product((1, 2), repeat=n):
            ep = Endpoint()
            for s in src:
                ep.append(s)
            prev_zero = None
            for k in range(L + 1):
                u = ep.length - 1          # column index n+k-1
                cells = tuple(ep.column[-d] if d <= 0 else ep.diagonal[d] for d in range(-(u + 1), min(u, n) + 1))
                cols[k][cells] += 1
                zero = tuple(i for i, t in enumerate(cells) if t == 0)
                if prev_zero is not None:
                    pairs[k].add((prev_zero, zero))
                prev_zero = zero
                if k == L:
                    break
                chosen = None
                for s in (1, 2):
                    _, cand = ep.peek(s)
                    if cand[n] >> 1 == 1:
                        chosen = s
                        break
                ep.append(chosen)
        print(f"n={n}  [{time.time()-t0:.1f}s]")
        print("   k   D_k     log2 D_k   drop   maxfiber   P_k")
        prev = None
        for k in range(L + 1):
            D = len(cols[k])
            lg = math.log2(D)
            drop = "" if prev is None else f"{prev - lg:5.2f}"
            print(f"  {k:>2}  {D:>6}   {lg:7.3f}   {drop:>5}   {max(cols[k].values()):>6}   {len(pairs[k]) if k > 0 else '-'}")
            prev = lg
        print(flush=True)


if __name__ == "__main__":
    main()

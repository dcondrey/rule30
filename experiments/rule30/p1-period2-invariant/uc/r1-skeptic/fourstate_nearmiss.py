#!/usr/bin/env python3
"""Near-miss census in the diagonal (four-state forced) bookkeeping.

BRIEF section 3, diagonal form: for a binary prefix W the four-state symbols
e_u (u >= n) with T[u][n] = c are forced uniquely (phi is a bijection in its
right argument).  The forced e_u is binary iff E(e_u) = 0.  Here the forced
path is followed with the true four-state symbol (so every cell T[u][n] equals
c exactly), and the number v of non-binary forced symbols among the first
n + 2 columns is counted, together with the hard-core violations among the
binary ones.  An RW counterexample at r = 0 is v = 0 with hard-core and 12a.
This is a different distance from `rw_bitsliced.py`'s E-mismatch count, which
keeps the symbol binary and lets the cell differ from c.

In (h, F) coordinates a four-state e_u has wedge cells (H, E) at depth -u-1 and
(1 - H, E) at depth -u, so the Moore trajectory starts at F = E(e_u) and the
whole F column is complemented relative to the binary choice.

Run:  cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/fourstate_nearmiss.py --min-n 10 --max-n 26
"""
from __future__ import annotations

import argparse
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rw_bitsliced import bit_patterns, build_column, const_array, forced_high, popcount  # noqa: E402


def fourstate_census(n: int, sources, c: int, K: int, nwords: int):
    prev = None
    for u in range(n):
        prev = build_column(prev, u, min(u, n - 1), sources[u], nwords)
    Ec = c & 1
    Ec_arr = const_array(nwords, Ec)
    ex = [const_array(nwords, 1), const_array(nwords, 0), const_array(nwords, 0), const_array(nwords, 0)]  # exactly v violations, v=0..3
    Hprev = sources[n - 1]
    prev_nonbinary = const_array(nwords, 0)
    Hforced = []
    for j in range(K):
        u = n + j
        Hu = forced_high(prev, u, n, nwords)
        col = build_column(prev, u, n, Hu, nwords)
        Fn = col.F[col.idx(n)]
        nonbinary = Fn ^ Ec_arr  # forced symbol has E = 1 where the binary choice misses c
        # correct the column: E(e_u) = 1 complements F at every depth
        col.F ^= nonbinary[None, :]
        hc_kill = (~Hu) & (~Hprev) & (~nonbinary) & (~prev_nonbinary)
        bad = nonbinary | hc_kill
        new = [None] * 4
        new[0] = ex[0] & ~bad
        for v in range(1, 4):
            new[v] = (ex[v] & ~bad) | (ex[v - 1] & bad)
        ex = new
        Hforced.append(Hu)
        prev = col
        Hprev = Hu
        prev_nonbinary = nonbinary
    # 12a ending for r = 0: e_{2n-1} = 1 (H=0, binary), e_{2n} = 2 (H=1, binary)
    end = (~Hforced[n - 1]) & Hforced[n]
    counts = [popcount(m) for m in ex]
    counts_end = [popcount(m & end) for m in ex]
    return counts, counts_end


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-n", type=int, default=10)
    ap.add_argument("--max-n", type=int, default=26)
    ap.add_argument("--block", type=int, default=22)
    args = ap.parse_args()
    print(" n  c   #prefixes with exactly v violations over n+2 columns, v=0,1,2,3   | same with the 12a ending   [s]")
    for n in range(args.min_n, args.max_n + 1):
        B = min(args.block, n)
        nwords = (1 << B) >> 6
        pats = bit_patterns(B)
        for c in (2, 3):
            t0 = time.time()
            tot = [0, 0, 0, 0]
            tot_end = [0, 0, 0, 0]
            for outer in range(1 << (n - B)):
                sources = [const_array(nwords, (outer >> (n - B - 1 - t)) & 1) for t in range(n - B)] + pats
                cnt, cnt_end = fourstate_census(n, sources, c, n + 2, nwords)
                tot = [a + b for a, b in zip(tot, cnt)]
                tot_end = [a + b for a, b in zip(tot_end, cnt_end)]
            flag = "  <- RW COUNTEREXAMPLE" if tot_end[0] > 0 else ""
            print(f"{n:<3}{c:<3} {tot}   | {tot_end}   [{time.time()-t0:.1f}s]{flag}")
            sys.stdout.flush()


if __name__ == "__main__":
    main()

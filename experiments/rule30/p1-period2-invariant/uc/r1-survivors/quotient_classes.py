#!/usr/bin/env python3
"""How many distinct forced continuations can 2^n binary sources produce?

The forced continuation (Q_n(W), Psi_n(W)) depends on W only through the
three-letter QUOTIENT (a,b) = ([T==0],[Lo(T)==0]) of the last source column
T[n-1][d], d = -n..n-1 (BRIEF section 2: column u is recovered from column
u-1's quotient plus the forced bit H(e_u)).  So the number of genuinely
distinct trials in the (BWH+)/(RW) census is the number of distinct quotient
words, not 2^n.

One DFS over all binary sources computes, for every u, the number of distinct
quotient words of column u over the 2^(u+1) sources of length u+1, and the
fiber-size histogram.  Independently, for n <= NPSI it counts the distinct
(Q, Psi) pairs and distinct Psi words via psi(), to check that the (Q, Psi)
classes are exactly the quotient fibers.
"""
from __future__ import annotations

import sys
from math import log2
from itertools import product
from collections import Counter

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
from psi_kernel import CONE, BOUNDARY, psi  # noqa: E402

QUOT = [(1, 1), (0, 0), (0, 1), (0, 0)]  # T -> (a,b) for T = 0,1,2,3


def quotient_key(col: list[int]) -> bytes:
    return bytes(0 if t in (1, 3) else (1 if t == 2 else 2) for t in col)


def main() -> None:
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 18
    NPSI = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    counts: list[Counter] = [Counter() for _ in range(NMAX)]

    # DFS over sources; column u stored as list index d+u+1 for d = -u-1..u
    def rec(u: int, prev: list[int] | None) -> None:
        for e in (1, 2):
            col = [0] * (2 * u + 2)
            col[0] = e
            col[1] = BOUNDARY[e]
            for d in range(-u + 1, u + 1):
                col[d + u + 1] = CONE[prev[d - 1 + u]][col[d + u]]
            counts[u][quotient_key(col[1:])] += 1  # quotient of depths -u..u (the top e itself excluded: its quotient is read by column u+1 at depth -u-1, include it too)
            if u + 1 < NMAX:
                rec(u + 1, col)

    rec(0, None)
    print("u  n=u+1   2^n   distinct quotient(col_u) [depths -u..u]   log2(distinct)   2^n/distinct   maxfiber   fiber histogram (size:count)")
    prev_log = None
    for u in range(NMAX):
        n = u + 1
        c = counts[u]
        dist = len(c)
        hist = Counter(c.values())
        lg = log2(dist)
        incr = "" if prev_log is None else f" (+{lg - prev_log:.3f})"
        prev_log = lg
        print(f"{u:2d} {n:3d} {2**n:8d} {dist:8d}  {lg:7.3f}{incr:>10}  {2**n/dist:6.2f}  {max(c.values()):4d}   " + ", ".join(f"{s}:{k}" for s, k in sorted(hist.items())[:10]))

    print("\nCross-check against (Q,Psi) classes from psi():")
    print("n   distinct quotient(col_{n-1}) incl. top e   distinct (Q,Psi)   distinct Psi   distinct Q")
    for n in range(4, NPSI + 1):
        # quotient including the top symbol e_{n-1} (depth -n): recompute directly
        qs = set()
        qp = set()
        ps = set()
        qq = set()
        for W in product((1, 2), repeat=n):
            cols = []
            for u, e in enumerate(W):
                col = [0] * (2 * u + 2)
                col[0] = e
                col[1] = BOUNDARY[e]
                prev = cols[u - 1] if u > 0 else None
                for d in range(-u + 1, u + 1):
                    col[d + u + 1] = CONE[prev[d - 1 + u]][col[d + u]]
                cols.append(col)
            qs.add(quotient_key(cols[n - 1]))
            Q, P = psi(W)
            qp.add((Q, P))
            ps.add(P)
            qq.add(Q)
        print(f"{n:2d}  {len(qs):8d}  {len(qp):8d}  {len(ps):8d}  {len(qq):8d}")


if __name__ == "__main__":
    main()

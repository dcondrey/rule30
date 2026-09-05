#!/usr/bin/env python3
"""Decompose the per-column loss of distinct endpoint states into its two
exact mechanisms in the Moore transducer (BRIEF section 2).

Column u (all depths -u-1..u) is a function of (quotient(col_{u-1}), e_u).
Two mechanisms make the source -> column map non-injective:

  (b) b-forgetting: step(h,F,a,b) = (h^1^a, F^(h&b)) reads b only when h=1,
      so the letter b_d of col_{u-1} at a depth where H(T[u][d]) = 0 leaves
      no trace in col_u.  Distinct (quotient(col_{u-1}), e_u) pairs can give
      one col_u.
  (q) quotient identification: cells 1 and 3 both read as letter (0,0), so
      distinct col_u give one quotient word, and hence one col_{u+1} family.

For u = 1..U this prints M(u) = distinct full columns, Q(u) = distinct
quotient words, P(u) = 2 Q(u-1) = distinct input pairs, and the two merge
factors P(u)/M(u) [mechanism b] and M(u)/Q(u) [mechanism q], with their
log2.  The sum of the two logs is the total loss per column
(1 + log2 Q(u-1) - log2 Q(u)).
"""
from __future__ import annotations

import sys
import time
from math import log2

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
from psi_kernel import CONE, BOUNDARY  # noqa: E402

LET = bytes([2, 0, 1, 0])  # cell -> quotient letter code: 0->(1,1)=2, 1,3->(0,0)=0, 2->(0,1)=1


def main() -> None:
    U = int(sys.argv[1]) if len(sys.argv) > 1 else 18
    print("u  n=u+1   2^n        M(u) full cols   Q(u) quotients   P(u)=2Q(u-1)   b-merge P/M  (bits)   q-merge M/Q  (bits)   total loss bits   log2 M increment")
    prevQ = None
    prevM = None
    for u in range(0, U + 1):
        t0 = time.time()
        fulls: set[bytes] = set()
        quots: set[bytes] = set()
        # iterative DFS over sources of length u+1, carrying full columns as lists
        # column representation: cells at depths -u-1..u as list indexed by d+u+1
        stack = [(0, None)]  # (next index to append, previous column list)
        # use explicit recursion via a generator to keep prefix sharing
        def rec(k: int, prev: list[int] | None) -> None:
            for e in (1, 2):
                col = [0] * (2 * k + 2)
                col[0] = e
                col[1] = BOUNDARY[e]
                for d in range(-k + 1, k + 1):
                    col[d + k + 1] = CONE[prev[d + k - 1]][col[d + k]]
                if k == u:
                    b = bytes(col)
                    fulls.add(b)
                    quots.add(bytes(LET[c] for c in col))
                else:
                    rec(k + 1, col)
        rec(0, None)
        M = len(fulls)
        Q = len(quots)
        if prevQ is None:
            print(f"{u:2d} {u+1:3d} {2**(u+1):10d} {M:12d} {Q:12d}   {'-':>12}   {'-':>8} {'-':>7}   {M/Q:8.4f} {log2(M/Q):7.4f}   {'-':>8}   {'-':>8}   ({time.time()-t0:.1f}s)")
        else:
            P = 2 * prevQ
            print(f"{u:2d} {u+1:3d} {2**(u+1):10d} {M:12d} {Q:12d}   {P:12d}   {P/M:8.4f} {log2(P/M):7.4f}   {M/Q:8.4f} {log2(M/Q):7.4f}   {1+log2(prevQ)-log2(Q):8.4f}   {log2(M)-log2(prevM):8.4f}   ({time.time()-t0:.1f}s)")
        prevQ, prevM = Q, M


if __name__ == "__main__":
    main()

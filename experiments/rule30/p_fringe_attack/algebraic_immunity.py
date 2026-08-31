"""Exact algebraic immunity of the Rule 30 iterated center-bit function.

f_t : {0,1}^(2t+1) -> {0,1} maps an initial row window (cells -t..t) to the
center cell at time t.  AI(f) = min degree of a nonzero g with f*g = 0 or
(1+f)*g = 0.  Universal bound: AI(f) <= ceil(n/2) for n variables, so here
AI(f_t) <= t+1 by construction.

Method: g of degree <= d annihilates f iff g vanishes on supp(f).  Build the
evaluation matrix of all monomials of degree <= d over the points of supp(f)
and test for a nontrivial kernel.  Columns are packed as Python big ints
(one bit per point) and eliminated over F2.
"""

from __future__ import annotations

import itertools
import sys


def center_bit(bits, t, n):
    """Evolve the length-n window t steps with zero padding; return center."""
    r = list(bits)
    for _ in range(t):
        r = [(r[i - 1] if i > 0 else 0) ^ (r[i] | (r[i + 1] if i + 1 < n else 0))
             for i in range(n)]
    return r[n // 2]


def truth_table(t):
    """f_t over its 2t+1 light-cone variables."""
    n = 2 * t + 1
    return [center_bit([(m >> i) & 1 for i in range(n)], t, n)
            for m in range(1 << n)], n


def monomials(n, d):
    for k in range(d + 1):
        yield from itertools.combinations(range(n), k)


def has_annihilator(points, n, d):
    """True iff a nonzero poly of degree <= d vanishes on every given point."""
    cols = []
    for mono in monomials(n, d):
        v = 0
        for idx, m in enumerate(points):
            ok = 1
            for var in mono:
                if not ((m >> var) & 1):
                    ok = 0
                    break
            if ok:
                v |= 1 << idx
        cols.append(v)
    ncols = len(cols)
    if ncols > len(points):
        return True                      # more unknowns than equations
    # F2 elimination on columns; nontrivial kernel iff rank < ncols
    pivots = {}
    rank = 0
    for c in cols:
        cur = c
        while cur:
            p = cur.bit_length() - 1
            if p in pivots:
                cur ^= pivots[p]
            else:
                pivots[p] = cur
                rank += 1
                break
        if cur == 0:
            return True                  # dependency => kernel vector exists
    return rank < ncols


def algebraic_immunity(t, dmax=None):
    tt, n = truth_table(t)
    supp1 = [m for m, v in enumerate(tt) if v == 1]
    supp0 = [m for m, v in enumerate(tt) if v == 0]
    cap = dmax if dmax is not None else (n + 1) // 2
    for d in range(0, cap + 1):
        if has_annihilator(supp1, n, d) or has_annihilator(supp0, n, d):
            return d, n, len(supp1)
    return None, n, len(supp1)


def main():
    tmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print("t | n=2t+1 | |supp f| | AI(f_t) | bound ceil(n/2) | deg f_t=2t-1")
    for t in range(3, tmax + 1):
        ai, n, w = algebraic_immunity(t)
        print(f"{t:2d} | {n:6d} | {w:8d} | {ai:7} | {(n+1)//2:15d} | {2*t-1:12d}",
              flush=True)


if __name__ == "__main__":
    main()

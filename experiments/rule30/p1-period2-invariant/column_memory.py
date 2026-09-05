#!/usr/bin/env python3
"""How far back does the endpoint column remember?

Discovery route (2026-09-03).  Decomposing the endpoint state showed the
column recursion is autonomous (the child column is a function of the parent
column and the appended symbol) while the diagonal is a cocycle over it, and
the counts satisfy

    |Col_{2u-1}| = |C_u|

exactly on every measured point (u = 2..22, values to 411664), where ``Col_L``
is the set of distinct columns of binary words of length ``L`` and ``C_u`` the
set of distinct full endpoint states (column and diagonal) at length ``u``.
The bijection realising it is the SUFFIX map: for every word ``w`` of length
``2u-1``, ``column(w)`` determines and is determined by the complete state of
``w[-u:]``.  Verified well-defined and onto for u = 3..8.

Consequence to test here directly.  If a column at length ``L`` is a function
of the last ``u`` symbols with ``L = 2u-1``, then the column FORGETS the first
half of the word.  This script measures the exact memory

    k(L) = least k such that column(w) is a function of w[-k:]

by complete enumeration of ``{1,2}^L``.  Predicted ``k(L) = ceil((L+1)/2)``.

This contradicts nothing in `RESULTS-RW-LINEAR-SLACK.md` 9.2 ("no effective
forgetting"), which measured survival across prefix bits, not the column map;
but it is the first exact forgetting law recorded for this kernel.
"""
from __future__ import annotations

import argparse
import math
import sys
from itertools import product

from psi_kernel import BOUNDARY, CONE


def column(w):
    col: list[int] = []
    L = 0
    for sym in w:
        nc = [0] * (L + 1)
        nc[L] = BOUNDARY[sym]
        for i in range(L - 1, -1, -1):
            nc[i] = CONE[col[i + 1]][nc[i + 1]]
        col = nc + [sym]
        L += 1
    return tuple(col)


def entry_profile(lmax: int) -> None:
    """Per-entry memory ``k(L, i)``: least ``k`` with ``column(w)[i]`` a
    function of ``w[-k:]``.  The measured law is ``k(L, i) = ceil((L-i+1)/2)``,
    i.e. it depends only on the distance ``d = L - i`` of the entry from the
    end of the column.  This is the profile the induction in section 5 of
    `RESULTS-COLUMN-DECOMPOSITION.md` runs on."""
    print("\n# k(L,i), least k with column(w)[i] a function of w[-k:]; column has L+1 entries")
    for L in range(1, lmax + 1):
        ws = list(product((1, 2), repeat=L))
        cols = [column(w) for w in ws]
        row = []
        for i in range(L + 1):
            for cand in range(0, L + 1):
                m: dict = {}
                ok = True
                for w, c in zip(ws, cols):
                    key = w[L - cand:] if cand else ()
                    if m.setdefault(key, c[i]) != c[i]:
                        ok = False
                        break
                if ok:
                    row.append(cand)
                    break
        pred = [-(-(L - i + 1) // 2) for i in range(L + 1)]
        print(f"L={L:>2} k(L,i)={row} law=ceil((L-i+1)/2) match={row == pred}")
        sys.stdout.flush()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lmax", type=int, default=18)
    ap.add_argument("--profile", type=int, default=0)
    args = ap.parse_args()
    print(f"{'L':>3} {'|Col_L|':>9} {'k(L)':>5} {'ceil((L+1)/2)':>14} {'match':>6}")
    for L in range(1, args.lmax + 1):
        cols = {}
        for w in product((1, 2), repeat=L):
            cols.setdefault(column(w), []).append(w)
        k = None
        for cand in range(1, L + 1):
            m = {}
            ok = True
            for c, ws in cols.items():
                for w in ws:
                    key = w[-cand:]
                    if m.setdefault(key, c) != c:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                k = cand
                break
        pred = math.ceil((L + 1) / 2)
        print(f"{L:>3} {len(cols):>9} {str(k):>5} {pred:>14} {str(k == pred):>6}")
        sys.stdout.flush()
    if args.profile:
        entry_profile(args.profile)


if __name__ == "__main__":
    main()

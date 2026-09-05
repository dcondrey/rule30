#!/usr/bin/env python3
"""The endpoint state splits into an autonomous column and a cocycle diagonal.

`merge_anatomy.py` found that 99.3 percent of the pairs of states that merge
under an append have IDENTICAL columns and differ only in the diagonal, at
Hamming distance one.  Since the child column is a function of the parent
column and the appended symbol alone, the column recursion is autonomous and
the diagonal is a cocycle over it.  This script measures the two factors
separately and tests the identity that decomposition exposes.

Parts.
  1. `|C_u|` (full states), `|Col_u|` (distinct columns), `|Dia_u|` (distinct
     diagonals) with growth bases, by BFS over full states.
  2. `|Col_L|` alone to large `L` (cheap: the column recursion is autonomous
     and `|Col_L|` grows like `1.33^L`), against the identity
         |Col_{2u-1}| = |C_u|.
  3. The suffix bijection realising it: for `w` of length `2u-1`,
     `column(w)` is well defined as a function of the complete endpoint state
     of `w[-u:]`, and the correspondence is onto `C_u`.

Kill for part 3: the suffix map is not well defined at some `u`, or its image
misses part of `C_u`, in which case the identity in part 2 is a numerical
coincidence and not a structural one.
"""
from __future__ import annotations

import argparse
import sys
from itertools import product

from psi_kernel import BOUNDARY, CONE


def cstep(col, sym):
    L = len(col) - 1
    nc = [0] * (L + 1)
    nc[L] = BOUNDARY[sym]
    for i in range(L - 1, -1, -1):
        nc[i] = CONE[col[i + 1]][nc[i + 1]]
    return tuple(nc) + (sym,)


def step(col, dia, sym):
    L = len(col) - 1
    nc = [0] * (L + 1)
    nc[L] = BOUNDARY[sym]
    for i in range(L - 1, -1, -1):
        nc[i] = CONE[col[i + 1]][nc[i + 1]]
    nd = [0] * (L + 1)
    nd[0] = nc[0]
    for i in range(L):
        nd[i + 1] = CONE[dia[i]][nd[i]]
    return tuple(nc) + (sym,), tuple(nd)


def state(w):
    col: list[int] = []
    dia: list[int] = []
    L = 0
    for sym in w:
        nc = [0] * (L + 1)
        nc[L] = BOUNDARY[sym]
        for i in range(L - 1, -1, -1):
            nc[i] = CONE[col[i + 1]][nc[i + 1]]
        nd = [0] * (L + 1)
        nd[0] = nc[0]
        for i in range(L):
            nd[i + 1] = CONE[dia[i]][nd[i]]
        col = nc + [sym]
        dia = nd
        L += 1
    return tuple(col), tuple(dia)


def part1(umax: int):
    print("# part 1: the two factors of the endpoint state")
    print(f"{'u':>3} {'|C_u|':>9} {'|Col_u|':>9} {'|Dia_u|':>9} {'Cbase':>7} {'ColBase':>7} {'DiaBase':>7} {'C/Col':>9}")
    cur = {((BOUNDARY[s], s), (BOUNDARY[s],)) for s in (1, 2)}
    pC = pCol = pDia = None
    for u in range(1, umax + 1):
        if u > 1:
            cur = {step(list(c), list(d), s) for (c, d) in cur for s in (1, 2)}
        C = len(cur)
        Col = len({c for c, _ in cur})
        Dia = len({d for _, d in cur})
        f = lambda x, p: x / p if p else float("nan")
        print(f"{u:>3} {C:>9} {Col:>9} {Dia:>9} {f(C, pC):>7.4f} {f(Col, pCol):>7.4f} "
              f"{f(Dia, pDia):>7.4f} {C / Col:>9.2f}")
        sys.stdout.flush()
        pC, pCol, pDia = C, Col, Dia
    return None


def part2(lmax: int, states: list[int]):
    print("\n# part 2: the column language alone, and the identity |Col_{2u-1}| = |C_u|")
    print(f"{'L':>3} {'|Col_L|':>10} {'base':>8}   {'u':>3} {'|C_u|':>10} {'identity':>9}")
    cur = {(BOUNDARY[s], s) for s in (1, 2)}
    p = None
    for L in range(1, lmax + 1):
        if L > 1:
            cur = {cstep(list(c), s) for c in cur for s in (1, 2)}
        n = len(cur)
        line = f"{L:>3} {n:>10} {n / p if p else float('nan'):>8.5f}"
        if L % 2 == 1:
            u = (L + 1) // 2
            if u - 1 < len(states):
                line += f"   {u:>3} {states[u - 1]:>10} {str(n == states[u - 1]):>9}"
        print(line)
        sys.stdout.flush()
        p = n


def part3(umax: int):
    print("\n# part 3: the suffix bijection  column(w), |w| = 2u-1   <->   state(w[-u:])")
    print(f"{'u':>3} {'|C_u|':>8} {'|Col_2u-1|':>11} {'well-defined':>13} {'onto C_u':>9}")
    for u in range(3, umax + 1):
        Cu = {state(w) for w in product((1, 2), repeat=u)}
        by: dict = {}
        for w in product((1, 2), repeat=2 * u - 1):
            by.setdefault(state(w)[0], set()).add(state(w[-u:]))
        ok = all(len(v) == 1 for v in by.values())
        img = {next(iter(v)) for v in by.values()}
        print(f"{u:>3} {len(Cu):>8} {len(by):>11} {str(ok):>13} {str(img == Cu):>9}")
        sys.stdout.flush()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--umax", type=int, default=19)
    ap.add_argument("--lmax", type=int, default=43)
    ap.add_argument("--bijmax", type=int, default=8)
    args = ap.parse_args()
    states = [2, 4, 8, 13, 23, 39, 73, 129, 232, 410, 742, 1329, 2376, 4265, 7560,
              13382, 23803, 42199, 74613, 131873, 233042, 411664]
    part1(args.umax)
    part2(args.lmax, states)
    part3(args.bijmax)


if __name__ == "__main__":
    main()

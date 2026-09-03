#!/usr/bin/env python3
"""Does the endpoint anti-diagonal have a memory law, and how wide is its channel?

PRE-REGISTERED 2026-09-03, before running.

`psi_kernel.Endpoint.peek` runs two trajectories of the SAME four-state
automaton, differing only in seed and direction:

    column   nc[L] = BOUNDARY[symbol];  nc[i]   = CONE[col[i+1]][nc[i+1]]
    diagonal nd[0] = nc[0];             nd[k+1] = CONE[dia[k]][nd[k]]

so the base (column) reaches the fibre (diagonal) through exactly ONE scalar
per append, `nc[0]`: two bits per step.  `nc[0]` is the column entry at
distance `d = L` from the end, which by `RESULTS-COLUMN-DECOMPOSITION.md`
section 5c depends on the last `ceil((L+1)/2)` symbols.  So the channel from
base to fibre is itself half-memory.

`RESULTS-COLUMN-DECOMPOSITION.md` section 5 proved the column law
`k_col(L) = ceil((L+1)/2)` and section 10 showed the column is not sufficient
for RW survival.  This script asks the matching question for the diagonal:

    k_dia(L)    = least k with diagonal(w) a function of w[-k:]
    k_dia(L, i) = the same for the single entry diagonal(w)[i]
    k_seed(L)   = least k for the coupling scalar nc[0] alone

Strong outcome: `k_dia(L) < L`, so the fibre forgets too, and the skew product
has a memory law on both factors.  Kill: `k_dia(L) = L` at every length, the
diagonal remembers everything, and the per-entry profile is flat, so no
forgetting statement can be lifted from the base to the fibre.

Either way the per-entry profile is the deliverable, because a proof about the
diagonal has to run on it the way section 5c ran on the column profile.
"""
from __future__ import annotations

import argparse
import math
import sys
from itertools import product

from psi_kernel import BOUNDARY, CONE


def run(w):
    col: list[int] = []
    dia: list[int] = []
    L = 0
    seeds: list[int] = []
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
        seeds.append(nc[0])
        L += 1
    return tuple(col), tuple(dia), seeds[-1]


def least_k(ws, vals, L):
    """least k such that w[-k:] determines vals[w]."""
    for cand in range(0, L + 1):
        m: dict = {}
        ok = True
        for w, v in zip(ws, vals):
            key = w[L - cand:] if cand else ()
            if m.setdefault(key, v) != v:
                ok = False
                break
        if ok:
            return cand
    return L


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lmax", type=int, default=14)
    args = ap.parse_args()
    print(f"{'L':>3} {'k_col':>6} {'k_dia':>6} {'k_seed':>7} {'ceil((L+1)/2)':>14} "
          f"{'|Dia_L|':>9} {'dia forgets?':>13}")
    profiles = []
    for L in range(1, args.lmax + 1):
        ws = list(product((1, 2), repeat=L))
        out = [run(w) for w in ws]
        cols = [o[0] for o in out]
        dias = [o[1] for o in out]
        seeds = [o[2] for o in out]
        kc = least_k(ws, cols, L)
        kd = least_k(ws, dias, L)
        ks = least_k(ws, seeds, L)
        pred = math.ceil((L + 1) / 2)
        print(f"{L:>3} {kc:>6} {kd:>6} {ks:>7} {pred:>14} {len(set(dias)):>9} "
              f"{str(kd < L):>13}")
        sys.stdout.flush()
        prof = [least_k(ws, [d[i] for d in dias], L) for i in range(L)]
        profiles.append((L, prof))
    print("\n# per-entry diagonal memory k_dia(L,i), i = 0..L-1")
    for L, prof in profiles:
        pred = [-(-(L - i + 1) // 2) for i in range(L)]
        print(f"L={L:>2} k_dia(L,i)={prof}  col-law would give {pred}  same={prof == pred}")


if __name__ == "__main__":
    main()

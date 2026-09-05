#!/usr/bin/env python3
"""Is the frozen zone below an infinite hit row a periodic tiling?

Under an infinite hit run the row at depth n is c^omega.  Row n-j is generated
bottom-up from row n-j+1 by the 4-state automaton r -> G(r, y) (G = inverse of
phi in its right argument) from a free first cell.  frozen_zone.log shows that
for j <= 12 every choice of first cells gives the same eventual periodic tail
up to a shift (period 1, 2, 2, 4, 4, ...).  This script pushes that to j = J
rows, records the eventual pattern P_j (canonical rotation), its period p_j,
its transient t_j (measured from a fixed long horizon), and tests whether the
sequence j -> P_j is eventually periodic (a 2D tiling), whether p_j stays
bounded, and how t_j grows.  Also checks the uniqueness of the tail: for the
chosen first-cell chain, all four first cells at each row are tried and the
number of distinct eventual tails is reported.

    cd .../p1-period2-invariant && uv run python uc/r1-potential/frozen_tiling.py
"""

from __future__ import annotations

import argparse
import sys

sys.path.insert(0, "uc/r1-potential")
sys.path.insert(0, ".")
from orbit_census import cell, hf  # noqa: E402


def G(l: int, y: int) -> int:
    hy, ey = hf(y)
    hr = hy ^ 1 ^ (1 if l == 0 else 0)
    er = ey ^ (hr & (1 if (l & 1) == 0 else 0))
    return cell(hr, er)


def drive(first: int, below: list[int]) -> list[int]:
    r = [first]
    for y in below[1:]:
        r.append(G(r[-1], y))
    return r


def period_transient(seq: list[int], max_period: int = 4096) -> tuple[int, int]:
    L = len(seq)
    for p in range(1, max_period + 1):
        t = L - p
        while t > 0 and seq[t - 1] == seq[t - 1 + p]:
            t -= 1
        if t <= L - 4 * p and t <= L // 2:
            return p, t
    return -1, -1


def canon(tail: tuple[int, ...]) -> tuple[int, ...]:
    return min(tail[i:] + tail[:i] for i in range(len(tail)))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=160)
    ap.add_argument("--cols", type=int, default=1200)
    ap.add_argument("--log", default="uc/r1-potential/frozen_tiling.log")
    args = ap.parse_args()
    with open(args.log, "w") as log:
        for target in (2, 3):
            row = [target] * args.cols
            pats: list[tuple[int, ...]] = []
            print(f"c={target}: rows n-j for j=1..{args.rows}, horizon {args.cols} columns", file=log)
            print("   j  period  transient  distinct-tails(4 first cells)  pattern(canonical)", file=log)
            for j in range(1, args.rows + 1):
                cands = [drive(lb, row) for lb in range(4)]
                tails = set()
                per_tr = []
                for r in cands:
                    p, t = period_transient(r)
                    per_tr.append((p, t))
                    if p > 0:
                        tails.add(canon(tuple(r[-p:])))
                p, t = per_tr[1]
                pat = canon(tuple(cands[1][-p:])) if p > 0 else ()
                pats.append(pat)
                tmax = max(tt for _, tt in per_tr)
                print(f"  {j:3d}  {p:5d}  {tmax:8d}  {len(tails):3d}   {''.join(map(str, pat))[:64]}", file=log)
                row = cands[1]
            # periodicity of j -> P_j
            found = None
            for q in range(1, args.rows // 3):
                for start in range(0, args.rows - 2 * q):
                    if all(pats[i] == pats[i + q] for i in range(start, args.rows - q)):
                        found = (q, start)
                        break
                if found:
                    break
            print(f"c={target}: row-pattern sequence eventually periodic in j? {found}  (vertical period, first row index)", file=log)
            print(f"c={target}: distinct patterns among rows 1..{args.rows}: {len(set(pats))}; max period {max(len(p) for p in pats)}", file=log)
            log.flush()
    print(f"log written to {args.log}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Verify the row synchronization of the pinned wedge and count its patterns.

pinned_row_periodicity_v2.log reports that row n-j below the pin becomes
periodic with period <= 4 after a preperiod of about 2j.  This script
(1) re-checks that claim directly: for random tails (D_{n-j}..D_{n-1}) at
j = 4, 8, 12, 16, 20 it builds the rows for u = n .. n+U-1 and verifies
row[t] == row[t+4] for all t >= T_j := 2j + 4, reporting violations;
(2) counts, per j, the number of distinct eventual period-4 patterns of row
n-j (cyclic words of length 4 read at u = n+T_j .. n+T_j+3, listed by phase
u mod 4) across tails, to see whether the frozen top of the wedge is universal
(one pattern) or source-dependent (many).

Usage: cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-injection/pinned_row_patterns.py
"""

from __future__ import annotations

import random
import sys
from itertools import product

sys.path.insert(0, ".")
from psi_kernel import CONE  # noqa: E402

CONE_INV = [[0] * 4 for _ in range(4)]
for _l in range(4):
    for _r in range(4):
        CONE_INV[_l][CONE[_l][_r]] = _r


def rows(D_tail, c, U):
    j = len(D_tail)
    width = j + U
    prev = [c] * width
    out = []
    for i in range(1, j + 1):
        m = j - i
        row = [None] * width
        row[m] = D_tail[m]
        for t in range(m + 1, width):
            row[t] = CONE_INV[row[t - 1]][prev[t]]
        out.append(row[j:])
        prev = row
    return out  # rows n-1 .. n-j at u = n .. n+U-1


def main() -> None:
    rng = random.Random(7)
    U = 400
    for c in (2, 3):
        print(f"c = {c}")
        for j in (4, 8, 12, 16, 20):
            tails = list(product(range(4), repeat=j)) if j <= 4 else [tuple(rng.randrange(4) for _ in range(j)) for _ in range(300)]
            T = 2 * j + 4
            viol = 0
            patterns = {i: set() for i in range(1, j + 1)}
            for D_tail in tails:
                R = rows(D_tail, c, U)
                for i in range(1, j + 1):
                    r = R[i - 1]
                    Ti = 2 * i + 4
                    if any(r[t] != r[t + 4] for t in range(Ti, U - 4)):
                        viol += 1
                    patterns[i].add(tuple(r[Ti + ((4 - Ti) % 4): Ti + ((4 - Ti) % 4) + 4]))
            counts = [len(patterns[i]) for i in range(1, j + 1)]
            print(f"   j={j:>2}: tails={len(tails):>4}, rows violating period 4 after T_i=2i+4: {viol}; distinct phase-aligned patterns per row n-1..n-j: {counts}")
            if j == 12:
                for i in (1, 2, 3, 4, 8, 12):
                    print(f"      row n-{i}: {sorted(patterns[i])}")
        sys.stdout.flush()


if __name__ == "__main__":
    main()

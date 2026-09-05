#!/usr/bin/env python3
"""The erasure front of a constant-2 run, displayed.

Prints the triangle of the all-2 endpoint 2^L (rows = depth d, columns = u),
then for a prefix p of length m the cells where the triangle of p.2^(3m)
differs from that of 2^(4m) ('#' = differs, '.' = same, '~' = differs by a
1<->3 swap only).  The front should retreat toward the bottom at 2/3 cell per
column and vanish at u = 4m-1.
"""
from __future__ import annotations

import sys

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
from psi_kernel import CONE, BOUNDARY  # noqa: E402


def triangle(endpoint):
    cols = []
    prev = None
    for k, e in enumerate(endpoint):
        col = {-k - 1: e, -k: BOUNDARY[e]}
        for d in range(-k + 1, k + 1):
            col[d] = CONE[prev[d - 1]][col[d - 1]]
        cols.append(col)
        prev = col
    return cols


def show(cols, title):
    L = len(cols)
    print(title)
    print("d\\u  " + " ".join(f"{u:2d}" for u in range(L)))
    for d in range(-L, L):
        row = []
        for u in range(L):
            row.append(f"{cols[u][d]:2d}" if d in cols[u] else " .")
        print(f"{d:4d} " + " ".join(row))


def main() -> None:
    L = 12
    show(triangle((2,) * L), f"all-2 endpoint, L={L}")
    for p in ((1, 1, 1), (1, 2, 1), (2, 1, 1)):
        m = len(p)
        A = triangle(p + (2,) * (3 * m))
        B = triangle((2,) * (4 * m))
        Lt = 4 * m
        print(f"\ndifference p={''.join(map(str,p))}.2^{3*m} vs 2^{4*m}  ('#' differ, '~' 1<->3 only, '.' same)")
        print("d\\u  " + " ".join(f"{u:2d}" for u in range(Lt)))
        for d in range(-Lt, Lt):
            row = []
            for u in range(Lt):
                if d not in A[u]:
                    row.append(" .")
                elif A[u][d] == B[u][d]:
                    row.append(" .")
                elif {A[u][d], B[u][d]} == {1, 3}:
                    row.append(" ~")
                else:
                    row.append(" #")
            print(f"{d:4d} " + " ".join(row))


if __name__ == "__main__":
    main()

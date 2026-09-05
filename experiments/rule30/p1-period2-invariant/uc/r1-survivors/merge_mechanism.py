#!/usr/bin/env python3
"""Two questions about class merging.

1. Small u: list the merging source pairs (same quotient of column u) for
   u = 2..5 and, for each merged pair, the XOR pattern of their sources and
   the cell-difference pattern of their columns u-1 (which cells differ, and
   whether the difference is a pure low-bit (F) difference or a high-bit one).

2. The n=15 survivor cylinder: at which column do the 18 sources become ONE
   class, and how many classes are they at columns 14, 15, ..., 30?
"""
from __future__ import annotations

import sys
from itertools import product, combinations
from collections import defaultdict

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
from psi_kernel import CONE, BOUNDARY, psi  # noqa: E402

LET = {0: 2, 1: 0, 2: 1, 3: 0}


def columns(endpoint) -> list[list[int]]:
    cols = []
    for u, e in enumerate(endpoint):
        col = [0] * (2 * u + 2)
        col[0] = e
        col[1] = BOUNDARY[e]
        prev = cols[u - 1] if u > 0 else None
        for d in range(-u + 1, u + 1):
            col[d + u + 1] = CONE[prev[d - 1 + u]][col[d + u]]
        cols.append(col)
    return cols


def s(x) -> str:
    return "".join(map(str, x))


def main() -> None:
    for u in range(2, 6):
        n = u + 1
        groups = defaultdict(list)
        for W in product((1, 2), repeat=n):
            cols = columns(W)
            groups[bytes(LET[t] for t in cols[u])].append((W, cols))
        merged = [g for g in groups.values() if len(g) > 1]
        print(f"\nu={u} (n={n}): {2**n} sources, {len(groups)} classes, {len(merged)} classes of size >1")
        for g in merged:
            print("  class: " + " ".join(s(W) for W, _ in g))
            for (W1, c1), (W2, c2) in combinations(g, 2):
                flips = [i for i in range(n) if W1[i] != W2[i]]
                # cell differences in column u-1 (depths -u..u-1) and column u
                diffs = []
                for uu in (u - 1, u):
                    dd = []
                    for idx in range(len(c1[uu])):
                        d = idx - uu - 1
                        a, b = c1[uu][idx], c2[uu][idx]
                        if a != b:
                            kind = "F" if (a >> 1) == (b >> 1) else ("H" if (a & 1) == (b & 1) else "HF")
                            dd.append(f"d{d}:{a}>{b}({kind})")
                    diffs.append(f"col{uu}[" + " ".join(dd) + "]")
                print(f"    {s(W1)} vs {s(W2)}: flips e_{flips}; " + "; ".join(diffs))

    # survivors at n=15
    n = 15
    suffix = tuple(map(int, "2211212112"))
    fam = []
    for pre in product((1, 2), repeat=5):
        W = pre + suffix
        Q, P = psi(W)
        if P == (1,) * 16 + (0,):
            fam.append(W)
    print(f"\nn=15 survivor cylinder: {len(fam)} sources")
    full = [W + psi(W)[0] for W in fam]
    allcols = [columns(ep) for ep in full]
    print("column u : number of distinct quotient words (depths -u-1..min(u,n-1)) among the 18, and distinct full columns")
    for u in range(10, 32):
        keys = set()
        fulls = set()
        for cols in allcols:
            col = cols[u]
            top = min(u, n - 1)
            keys.add(bytes(LET[t] for t in col[: top + u + 2]))
            fulls.add(tuple(col[: top + u + 2]))
        print(f"  u={u:2d}: {len(keys):2d} quotient classes, {len(fulls):2d} distinct columns")


if __name__ == "__main__":
    main()

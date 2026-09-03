#!/usr/bin/env python3
"""Which source symbols are load-bearing for the n=15 survivor's run?

For W = 111122211212112 (Psi = 1^16 0), flip each single symbol e_i and each
pair (e_i, e_j) and report the resulting constant-prefix length k of Psi.
Also flip single cells of the LAST SOURCE COLUMN T[14][d] (four-state, all
three alternatives) and recompute the run region by upward integration from
c = 3, reporting the first non-binary virtual top.  A local 'event' would show
as a small set of load-bearing coordinates; a global obstruction shows as
sensitivity spread over the whole column.
"""
from __future__ import annotations

import sys
from itertools import product, combinations
from collections import Counter

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-survivors")
from psi_kernel import psi, CONE, BOUNDARY  # noqa: E402
from virtual_continuation import G, first_nonbinary  # noqa: E402


def const_prefix(word) -> int:
    k = 0
    while k + 1 < len(word) and word[k + 1] == word[0]:
        k += 1
    return k


def s(x) -> str:
    return "".join(map(str, x))


def run_from_column(prev: list[int], u0: int, n: int, c: int, L: int) -> list[int]:
    """Given column u0-1 (list of T[u0-1][d], d=-u0..u0-1, index d+u0), integrate upward for u >= u0."""
    tops = []
    cols = {u0 - 1: prev}
    for u in range(u0, L):
        p = cols[u - 1]
        col = [0] * (2 * u + 2)
        col[n + u + 1] = c
        for d in range(n - 1, -u - 1, -1):
            col[d + u + 1] = G[col[d + u + 2]][p[d + u]]
        col[0] = col[1] ^ 3
        tops.append(col[0])
        cols[u] = col
    return tops


def main() -> None:
    W = tuple(map(int, "111122211212112"))
    n = len(W)
    Q, P = psi(W)
    print(f"W={s(W)} Q={s(Q)} Psi={s(P)} k={const_prefix(P)}")
    print("\nsingle flips e_i (1<->2): i -> k, Psi")
    for i in range(n):
        W2 = W[:i] + (3 - W[i],) + W[i + 1:]
        Q2, P2 = psi(W2)
        print(f"  i={i:2d}: k={const_prefix(P2):2d}  Psi={s(P2)}  Q={s(Q2)}")
    print("\npair flips: (i,j) with k >= 12")
    for i, j in combinations(range(n), 2):
        W2 = list(W)
        W2[i] = 3 - W2[i]
        W2[j] = 3 - W2[j]
        Q2, P2 = psi(tuple(W2))
        k = const_prefix(P2)
        if k >= 12:
            print(f"  ({i},{j}): k={k}  Psi={s(P2)}")
    # last source column
    cols = []
    for u, e in enumerate(W):
        col = [0] * (2 * u + 2)
        col[0] = e
        col[1] = BOUNDARY[e]
        prev = cols[u - 1] if u > 0 else None
        for d in range(-u + 1, u + 1):
            col[d + u + 1] = CONE[prev[d - 1 + u]][col[d + u]]
        cols.append(col)
    last = cols[n - 1]
    print(f"\nlast source column T[{n-1}][d], d=-{n}..{n-1}: {s(last)}")
    base = run_from_column(last, n, n, 3, 2 * n + 6)
    print(f"virtual tops from it: {s(base)}  first non-binary at {first_nonbinary(base)} (expected {const_prefix(P)+1})")
    print("\nsingle-cell perturbations of the last source column: depth d, new value -> first non-binary index of virtual tops")
    hist = Counter()
    for idx in range(len(last)):
        d = idx - n
        outs = []
        for v in range(4):
            if v == last[idx]:
                continue
            col = last[:]
            col[idx] = v
            tops = run_from_column(col, n, n, 3, 2 * n + 6)
            f = first_nonbinary(tops)
            outs.append(f"{v}:{f:2d}")
            hist[f] += 1
        print(f"  d={d:3d} (was {last[idx]}): " + "  ".join(outs))
    print("histogram of first non-binary index over all 3*2n single-cell perturbations: " + ", ".join(f"{k}:{v}" for k, v in sorted(hist.items())))


if __name__ == "__main__":
    main()

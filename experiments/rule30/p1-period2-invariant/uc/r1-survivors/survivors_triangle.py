#!/usr/bin/env python3
"""Survivor census and full-triangle dump for the simultaneous-death families.

For n in {15, 16, 18}: enumerate all binary sources W in {1,2}^n, compute
(Q_n(W), Psi_n(W)) with the validated kernel, collect the sources whose Psi
prefix is constant through the maximal k, and dump:
  * whether they share Q,
  * their full triangles T[u][d] (four-state cells) in the region needed for
    the death cell T[n+k+1][n],
  * the Moore state trajectory (h,F) of the death column and of the last
    surviving column, side by side with the letters (a,b) they read.
"""
from __future__ import annotations

import sys
from itertools import product
from collections import Counter

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
from psi_kernel import CONE, BOUNDARY, Endpoint, psi  # noqa: E402


def triangle(endpoint: tuple[int, ...]) -> list[dict[int, int]]:
    """T[u][d] for d in [-u-1, u] as a list of dicts keyed by d."""
    cols: list[dict[int, int]] = []
    for u, e in enumerate(endpoint):
        col: dict[int, int] = {-u - 1: e, -u: BOUNDARY[e]}
        prev = cols[u - 1] if u > 0 else None
        for d in range(-u + 1, u + 1):
            col[d] = CONE[prev[d - 1]][col[d - 1]]
        cols.append(col)
    return cols


def H(t: int) -> int:
    return t >> 1


def Lo(t: int) -> int:
    return t & 1


def E(t: int) -> int:
    return 1 ^ H(t) ^ Lo(t)


def a_letter(t: int) -> int:
    return int(t == 0)


def b_letter(t: int) -> int:
    return int(Lo(t) == 0)


def const_prefix(word: tuple[int, ...]) -> int:
    """Largest k with word[0] == ... == word[k]."""
    k = 0
    while k + 1 < len(word) and word[k + 1] == word[0]:
        k += 1
    return k


def survivors(n: int) -> tuple[int, list[tuple[int, ...]]]:
    best = -1
    fam: list[tuple[int, ...]] = []
    for W in product((1, 2), repeat=n):
        _, word = psi(W)
        k = const_prefix(word)
        if k > best:
            best, fam = k, []
        if k == best:
            fam.append(W)
    return best, fam


def s(seq) -> str:
    return "".join(map(str, seq))


def main() -> None:
    for n in (15, 16, 18):
        best, fam = survivors(n)
        print(f"===== n={n}: max constant prefix k={best} (Psi_0..Psi_{best} equal), {len(fam)} sources")
        qs = Counter()
        psis = Counter()
        for W in fam:
            Q, P = psi(W)
            qs[Q] += 1
            psis[P] += 1
        print(f"distinct Q among survivors: {len(qs)}")
        for Q, c in qs.items():
            print(f"  Q={s(Q)} x{c}")
        print(f"distinct Psi among survivors: {len(psis)}")
        for P, c in psis.items():
            print(f"  Psi={s(P)} x{c}")
        # longest common suffix of sources
        L = min(len(W) for W in fam)
        suf = 0
        while suf < L and len({W[-suf - 1] for W in fam}) == 1:
            suf += 1
        print(f"common source suffix length {suf}: {s(fam[0][n - suf:])}")
        print("sources:")
        for W in fam:
            print("  " + s(W))
        # Full triangle for the first survivor; death column u* = n + best + 1
        W = fam[0]
        Q, P = psi(W)
        ep = W + Q
        T = triangle(ep)
        ustar = n + best + 1
        print(f"\nfull endpoint (first survivor) = {s(ep)}  length {len(ep)}")
        print(f"death column u*={ustar}, death cell T[{ustar}][{n}] = {T[ustar][n]}  (E={E(T[ustar][n])})")
        print(f"row at depth n={n} across columns u=n..{len(ep)-1}: " + s(T[u][n] for u in range(n, len(ep))))
        # Region dump: columns n-1 .. ustar, depths -ustar-1 .. n+2
        print("\ncolumns (u across, d down); '.' = outside triangle")
        us = list(range(max(0, n - 2), len(ep)))
        print("d\\u  " + " ".join(f"{u:2d}" for u in us))
        for d in range(-len(ep), n + 3):
            row = []
            for u in us:
                row.append(f"{T[u][d]:2d}" if d in T[u] else " .")
            print(f"{d:4d} " + " ".join(row))
        # Check agreement of the region d <= u - (n - suf) - 1 across survivors... just diff the death column
        print("\ndeath column and previous column across all survivors (depths -u*-1..n):")
        cols_prev = Counter()
        cols_death = Counter()
        for W in fam:
            Q, P = psi(W)
            T2 = triangle(W + Q)
            cols_prev[s(T2[ustar - 1][d] for d in range(-ustar, n + 1))] += 1
            cols_death[s(T2[ustar][d] for d in range(-ustar - 1, n + 1))] += 1
        print(f"distinct column u*-1 words: {len(cols_prev)}; distinct death-column words: {len(cols_death)}")
        # Where do they first differ (from the bottom d=n upward)?
        if len(cols_death) > 1:
            words = list(cols_death)
            Ln = len(words[0])
            i = Ln - 1
            while i >= 0 and len({w[i] for w in words}) == 1:
                i -= 1
            print(f"death columns agree from d=n upward until index {i} -> depth d={i - ustar - 1}")
        # Moore trajectory of the death column and its predecessor
        for u in (ustar - 1, ustar):
            print(f"\nMoore trajectory of column u={u} (reads column {u-1} letters (a,b)); state (h,F) at depth d, cell:")
            line_d, line_ab, line_hF, line_cell = [], [], [], []
            for d in range(-u, n + 1):
                t = T[u][d]
                h, F = H(t), E(t)
                if d < n:
                    prv = T[u - 1][d]
                    ab = f"{a_letter(prv)}{b_letter(prv)}"
                else:
                    ab = "--"
                line_d.append(f"{d:3d}")
                line_ab.append(f"{ab:>3}")
                line_hF.append(f" {h}{F}")
                line_cell.append(f"{t:3d}")
            print("  d   " + "".join(line_d))
            print("  ab  " + "".join(line_ab))
            print("  hF  " + "".join(line_hF))
            print("  T   " + "".join(line_cell))
        print()


if __name__ == "__main__":
    main()

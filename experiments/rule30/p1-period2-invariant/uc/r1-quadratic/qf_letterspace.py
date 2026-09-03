#!/usr/bin/env python3
"""The RW hits on the full letter space of column n-1, zero pattern fixed.

Column n-1 on the window d in [-n, n-1] is a word of 2n letters from
{0, 2, x} (x = {1,3}), i.e. a pair (a, b) with a = [T == 0] <= b = [T even].
The region u >= n is a deterministic function of that word (top row pinned
at c), so the hits hit_{n+j} = [E(e_{n+j}) == 0] are Boolean functions of it.

For every zero pattern a (2^(2n) of them) the free variables are the b's at
the nonzero positions.  This script measures, for n = 3..5:

  (1) max over a of the ANF degree of hit_{n+j} in those free b's, j = 0..n+1
      (derivation predicts 1, 2, 5, 13, ... capped by the number of free b's);
  (2) letter-space survivor counts T_k = #{(a, b) : first k hits succeed},
      with and without the hard-core kill, against the independence value
      3^(2n) 2^(-k) resp. 3^(2n) 2^(-k) (3/4)^(k-1);
  (3) the number of zero patterns a on which hit_n is constant (degenerate
      classes where the affine functional has no free b).

Run:  cd <work dir> && uv run python uc/r1-quadratic/qf_letterspace.py --max-n 5
"""

from __future__ import annotations

import argparse
import time
from itertools import product

from qf_common import E, anf_degree, psi


def region_hits(word: list[int], n: int, c: int) -> tuple[list[int], list[int]]:
    """Hits and forced symbols of the region driven by column n-1 = word.

    word[i] is the cell at depth d = -n + i, i in [0, 2n).  Returns
    (hits, symbols) for u = n .. 2n+1, hits[j] = 1 iff E(e_{n+j}) == 0.
    """
    prev: dict[int, int] = {(-n + i): t for i, t in enumerate(word)}
    hits, symbols = [], []
    for u in range(n, 2 * n + 2):
        col: dict[int, int] = {n: c}
        for d in range(n - 1, -u - 2, -1):
            left = prev[d] if d in prev else 3
            col[d] = psi(left, col[d + 1])
        e = col[-u - 1]
        hits.append(1 if E(e) == 0 else 0)
        symbols.append(e)
        prev = col
    return hits, symbols


def run(n: int, c: int) -> None:
    m = 2 * n
    total = 3 ** m
    T = [0] * (n + 3)          # first k hits succeed
    Thc = [0] * (n + 3)        # first k hits succeed and hard-core holds
    maxdeg = [-1] * (n + 2)
    const_classes = 0
    classes = 0
    for a_bits in range(1 << m):
        a = [(a_bits >> i) & 1 for i in range(m)]
        free = [i for i in range(m) if a[i] == 0]
        nfree = len(free)
        tables = [[0] * (1 << nfree) for _ in range(n + 2)]
        classes += 1
        for bb in range(1 << nfree):
            word = []
            fi = 0
            for i in range(m):
                if a[i]:
                    word.append(0)
                else:
                    word.append(2 if (bb >> fi) & 1 else 1)
                    fi += 1
            hits, symbols = region_hits(word, n, c)
            for j in range(n + 2):
                tables[j][bb] = hits[j]
            k = 0
            while k < n + 2 and hits[k]:
                k += 1
            for kk in range(k + 1):
                T[kk] += 1
            # hard-core: junction with e_{n-1} = word[0] XOR 3 (cell at d = -n is e_{n-1} XOR 3)
            prev_sym = word[0] ^ 3
            k2 = 0
            while k2 < n + 2 and hits[k2]:
                if prev_sym == 1 and symbols[k2] == 1:
                    break
                prev_sym = symbols[k2]
                k2 += 1
            for kk in range(k2 + 1):
                Thc[kk] += 1
        for j in range(n + 2):
            dg = anf_degree(tables[j])
            if dg > maxdeg[j]:
                maxdeg[j] = dg
        if anf_degree(tables[0]) <= 0:
            const_classes += 1
    print(f"n={n} c={c} letter words={total}  zero-pattern classes={classes}  hit_n constant on {const_classes} classes")
    print(f"   max deg of hit_(n+j) in free b's, j=0..{n+1}: {maxdeg}")
    print("    k    T_k       3^(2n)/2^k     ratio      T_k(hc)    null(hc)     ratio")
    for k in range(n + 3):
        null = total / 2 ** k
        nullhc = total / 2 ** k * (0.75 ** max(k - 1, 0))
        print(f"   {k:>2}  {T[k]:>8}  {null:>12.1f}  {T[k]/null:>7.3f}   {Thc[k]:>8}  {nullhc:>10.1f}  {Thc[k]/nullhc:>7.3f}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-n", type=int, default=3)
    ap.add_argument("--max-n", type=int, default=5)
    args = ap.parse_args()
    for n in range(args.min_n, args.max_n + 1):
        for c in (2, 3):
            t0 = time.time()
            run(n, c)
            print(f"   [{time.time()-t0:.1f}s]")


if __name__ == "__main__":
    main()

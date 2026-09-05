#!/usr/bin/env python3
"""Affine pieces of the region map in the even-bits of column n-1 (letter space).

Fix a zero pattern Z of column n-1 (window d in [-n, n-1], bottom cell
nonzero as for any reachable column).  The free bits are w_d = [cell == 2]
at the nonzero positions.  Claims tested for every Z with n <= max_n:

  (P1) the zero pattern Z_n of column n is an affine function of w:
       the set {w : Z_n = given} is an affine subspace, and it is exactly
       {w : w at retained nonzero positions = fixed vector}, i.e. Z_n
       determines the retained w's and leaves the non-retained w's free;
  (P2) on each such piece every hit hit_{n+j} (j = 0..n+1) is constant.
       (Consequence of (P1): column n is determined by (Z, Z_n).)
  (P3) rank of the first k hits as functions of the RETAINED w's alone
       (a Boolean function of r = #retained nonzero cells bits):
       hit_n is affine with all-ones coefficients on the retained w's;
       hit_{n+1} is quadratic in the retained w's; the algebraic degree of
       hit_{n+j} in the retained w's is reported for j <= 3 (max over Z).

Run:  cd <work dir> && uv run python uc/r1-quadratic/q2_pieces.py --max-n 5
"""
from __future__ import annotations

import argparse
import time
from itertools import product

from qf_common import E, anf_degree, psi


def region_columns(word: list[int], n: int, count: int) -> list[dict[int, int]]:
    prev: dict[int, int] = {(-n + i): t for i, t in enumerate(word)}
    out = []
    for u in range(n, n + count):
        col: dict[int, int] = {n: c_global}
        for d in range(n - 1, -u - 2, -1):
            left = prev[d] if d in prev else 3
            col[d] = psi(left, col[d + 1])
        out.append(col)
        prev = col
    return out


c_global = 2


def retained_positions(a: list[int], n: int) -> list[int]:
    """Indices i (word positions) of retained nonzero cells: even-indexed nonzero from the top."""
    m = len(a)
    qs = [i for i in range(m - 1, -1, -1) if a[i] == 0]
    return [q for idx, q in enumerate(qs, start=1) if idx % 2 == 0]


def run(n: int) -> None:
    m = 2 * n
    checks = 0
    maxdeg = [-1] * 4
    for a_bits in range(1 << (m - 1)):
        a = [0] + [(a_bits >> i) & 1 for i in range(m - 1)]      # bottom cell nonzero
        free = [i for i in range(m) if a[i] == 0]
        ret = retained_positions(a, n)
        nonret = [i for i in free if i not in ret]
        # enumerate all w, group by Z_n
        groups: dict = {}
        hits_by_ret: dict = {}
        for bb in range(1 << len(free)):
            word = []
            fi = 0
            for i in range(m):
                if a[i]:
                    word.append(0)
                else:
                    word.append(2 if (bb >> fi) & 1 else 1)
                    fi += 1
            cols = region_columns(word, n, n + 2)
            Zn = tuple(d for d in range(-n - 1, n) if cols[0][d] == 0)
            wret = tuple((bb >> free.index(i)) & 1 for i in ret)
            wnon = tuple((bb >> free.index(i)) & 1 for i in nonret)
            hits = tuple(1 if E(cols[j][-n - j - 1]) == 0 else 0 for j in range(n + 2))
            groups.setdefault(Zn, set()).add((wret, wnon, hits))
            hits_by_ret.setdefault(wret, set()).add(hits)
        # (P1): each Z_n group has a single wret and all wnon
        for Zn, members in groups.items():
            wrets = {x[0] for x in members}
            assert len(wrets) == 1, ("P1", n, a, Zn, wrets)
            assert len({x[1] for x in members}) == (1 << len(nonret)), ("P1-free", n, a, Zn)
            # (P2): hits constant on the piece
            assert len({x[2] for x in members}) == 1, ("P2", n, a, Zn)
            checks += 1
        assert len(groups) == (1 << len(ret)), ("P1-count", n, a, len(groups), len(ret))
        # (P3): degrees in the retained w's
        r = len(ret)
        for j in range(min(4, n + 2)):
            table = [0] * (1 << r)
            for wret, hs in hits_by_ret.items():
                assert len(hs) == 1
                idx = sum(b << i for i, b in enumerate(wret))
                table[idx] = next(iter(hs))[j]
            dg = anf_degree(table)
            if dg > maxdeg[j]:
                maxdeg[j] = dg
            if j == 0 and r > 0:
                # affine with all-ones coefficients
                from qf_common import anf_monomials
                mons = anf_monomials(table)
                lin = sorted(mm for mm in mons if mm != 0)
                assert lin == [1 << i for i in range(r)], ("P3-affine", n, a, mons)
    print(f"n={n} c={c_global}: {checks} pieces PASS (P1, P2); hit_n affine all-ones on retained w's PASS")
    print(f"   max algebraic degree of hit_(n+j) in the retained w's, j=0..3: {maxdeg[:min(4, n+2)]}")


def main() -> None:
    global c_global
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-n", type=int, default=5)
    args = ap.parse_args()
    for n in range(2, args.max_n + 1):
        for c in (2, 3):
            c_global = c
            t0 = time.time()
            run(n)
            print(f"   [{time.time()-t0:.1f}s]", flush=True)


if __name__ == "__main__":
    main()

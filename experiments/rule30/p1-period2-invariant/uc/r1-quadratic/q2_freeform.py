#!/usr/bin/env python3
"""Phi as a quadratic form on the FREE relaxation F2^(2m) of the letter alphabet.

Letters (a_d, b_d) with a = [cell == 0], b = [cell even]; the true domain is
a <= b (three letters), the free relaxation lets all 2^(2m) pairs in.  With
the window top at n-1 and bottom at -u (m = n + u), and forced start
h0 = 1 + |N| so that the final h is 1, the BRIEF's primed form is

    Phi(a, b) = sum_d (1 + n - d) b_d + sum_d a_d + sum_{d' < d} b_{d'} a_d.

Computed exactly for m = 2..8 (window [-u, n-1] with n = m/2 rounded):
  (F1) Phi equals the Moore-machine value on the three-letter domain;
  (F2) rank of the alternating bilinear form B((a,b),(a',b')) =
       Phi(x+y) + Phi(x) + Phi(y) on F2^(2m); predicted 2(m-1) with radical
       spanned by a_bottom and b_top;
  (F3) the linear part restricted to the radical (a_bottom coefficient 1
       predicted, so the form is balanced on F2^(2m): exactly 2^(2m-1)
       zeros) and the zero count;
  (F4) zero count on the three-letter domain (predicted (3^m + 1)/2).

Run:  cd <work dir> && uv run python uc/r1-quadratic/q2_freeform.py --max-m 8
"""
from __future__ import annotations

import argparse
from itertools import product


def phi_free(a: list[int], b: list[int], n: int, lo: int) -> int:
    m = len(a)
    total = 0
    for i in range(m):
        d = lo + i
        total ^= ((1 + n - d) & 1) & b[i]
        total ^= a[i]
        for j in range(i):
            total ^= b[j] & a[i]
    return total


def phi_moore(a: list[int], b: list[int]) -> int:
    nonzero = sum(1 - x for x in a)
    h = (1 + nonzero) & 1
    F = 0
    for x, y in zip(a, b):
        F ^= h & y
        h ^= 1 ^ x
    assert h == 1
    return F


def gf2_rank(rows: list[int]) -> int:
    rank = 0
    rows = rows[:]
    while rows:
        pivot = max(rows)
        if pivot == 0:
            break
        rank += 1
        bit = 1 << (pivot.bit_length() - 1)
        rows = [r ^ pivot if r & bit else r for r in rows if r != pivot]
    return rank


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-m", type=int, default=8)
    args = ap.parse_args()
    for m in range(2, args.max_m + 1):
        n = (m + 1) // 2
        lo = n - m           # window [lo, n-1] of length m
        N = 2 * m
        def unpack(x: int) -> tuple[list[int], list[int]]:
            a = [(x >> i) & 1 for i in range(m)]
            b = [(x >> (m + i)) & 1 for i in range(m)]
            return a, b
        vals = [0] * (1 << N)
        for x in range(1 << N):
            a, b = unpack(x)
            vals[x] = phi_free(a, b, n, lo)
        # (F1) agreement on the three-letter domain
        dom = [x for x in range(1 << N) if all(aa <= bb for aa, bb in zip(*unpack(x)))]
        assert len(dom) == 3 ** m
        for x in dom:
            a, b = unpack(x)
            assert vals[x] == phi_moore(a, b), ("F1", m, a, b)
        # (F2) bilinear form matrix
        rows = []
        for i in range(N):
            row = 0
            for j in range(N):
                bij = vals[(1 << i) ^ (1 << j)] ^ vals[1 << i] ^ vals[1 << j] ^ vals[0]
                row |= bij << j
            rows.append(row)
        rank = gf2_rank(rows)
        # radical: vectors v with B(v, e_j) = 0 for all j
        radical = [x for x in range(1 << N) if all(
            (vals[x ^ (1 << j)] ^ vals[x] ^ vals[1 << j] ^ vals[0]) == 0 for j in range(N))]
        a_bottom = 1 << 0
        b_top = 1 << (m + m - 1)
        lin_on_rad = {x: vals[x] ^ vals[0] for x in radical}
        zeros_free = sum(1 for v in vals if v == 0)
        zeros_dom = sum(1 for x in dom if vals[x] == 0)
        print(f"m={m}: (F1) three-letter agreement PASS on {len(dom)} words; "
              f"(F2) rank B = {rank} (2(m-1) = {2*(m-1)}), radical size {len(radical)}, "
              f"radical = span(a_bottom, b_top): {set(radical) == {0, a_bottom, b_top, a_bottom | b_top}}; "
              f"(F3) Phi(a_bottom)+Phi(0) = {lin_on_rad[a_bottom]}, Phi(b_top)+Phi(0) = {lin_on_rad[b_top]}, "
              f"zeros on F2^(2m) = {zeros_free} (2^(2m-1) = {1 << (N-1)}); "
              f"(F4) zeros on domain = {zeros_dom} ((3^m+1)/2 = {(3**m+1)//2})")


if __name__ == "__main__":
    main()

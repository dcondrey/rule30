#!/usr/bin/env python3
"""Verifier-side checks on PROOF.md (retained-bit-form, direct proof).

V1  Corollary 5.1 as DISPLAYED:  1 + h(d) + h(d+1) = [T[u-1][d] != 0].
    Counted against the triangle built from the BRIEF section 2 recursion, all binary
    words u <= 9, every n <= u, every d in the window.  Also counts the corrected
    form  h(d) + h(d+1) = [T[u-1][d] != 0]  (equivalently 1 + h(d) + h(d+1) = [T = 0]).
V2  Transfer matrix A of PROOF.md section 8 rebuilt by hand from the Moore step and
    its characteristic polynomial recomputed by direct expansion of det(xI - A)
    over the integers (no Faddeev), plus p(1), p(3), p(-1).
V3  Lemma 10 beyond depth n: an odd-indexed nonzero replacement inside the window
    leaves ALL of column u (depths up to u) unchanged, not only [-u-1, n].
    PROOF.md proves it only on [-u-1, n]; the lemma statement says "never read by
    column u" with no depth bound.  Checked on all binary words u <= 9, n <= u.
V4  Lemma 9(iii) scope: the pair (Z_{u-1}, Z_u) does NOT determine cells of later
    columns at depth > n (a witness pair of words with equal key but different
    T[u+1][n+1]), which is why "whole forced future" must be read at depth <= n.
"""
from __future__ import annotations

import os
import sys
from itertools import product

WORK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, WORK)
from psi_kernel import CONE  # noqa: E402


def H(t: int) -> int:
    return t >> 1


def next_column(prev, e, u):
    col = {-u - 1: e, -u: e ^ 3}
    for d in range(-u + 1, u + 1):
        col[d] = CONE[prev[d - 1]][col[d - 1]]
    return col


def triangle(word):
    cols, prev = [], None
    for u, e in enumerate(word):
        prev = next_column(prev, e, u)
        cols.append(prev)
    return cols


def forced(prev, u, n):
    found = [(e, next_column(prev, e, u)) for e in (1, 2)]
    found = [(e, c) for e, c in found if H(c[n]) == 1]
    assert len(found) == 1
    return found[0]


def v1(umax: int) -> None:
    as_displayed_ok = as_displayed_bad = corrected_ok = corrected_bad = 0
    for u in range(1, umax + 1):
        for word in product((1, 2), repeat=u):
            prev = triangle(word)[u - 1]
            for n in range(1, u + 1):
                e_u, cur = forced(prev, u, n)
                for d in range(-u, n):
                    nz = 1 if prev[d] != 0 else 0
                    lhs_disp = (1 + H(cur[d]) + H(cur[d + 1])) & 1
                    lhs_corr = (H(cur[d]) + H(cur[d + 1])) & 1
                    if lhs_disp == nz:
                        as_displayed_ok += 1
                    else:
                        as_displayed_bad += 1
                    if lhs_corr == nz:
                        corrected_ok += 1
                    else:
                        corrected_bad += 1
    print(f"V1 Corollary 5.1 as displayed  '1 + h(d) + h(d+1) = [T != 0]':  holds {as_displayed_ok}, fails {as_displayed_bad}")
    print(f"V1 Corollary 5.1 corrected     'h(d) + h(d+1) = [T != 0]'    :  holds {corrected_ok}, fails {corrected_bad}")
    assert as_displayed_ok == 0 and corrected_bad == 0
    print("V1 verdict: the displayed formula is off by a complement on EVERY cell; the corrected form holds on every cell. "
          "Downstream use (h profile determines Z) is unaffected.")


def det_int(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    total = 0
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in M[1:]]
        total += (-1) ** j * M[0][j] * det_int(minor)
    return total


def poly_det(A):
    """Characteristic polynomial det(xI - A) by expansion over Z[x] (polys as coefficient lists, low to high)."""
    n = len(A)

    def padd(p, q):
        m = max(len(p), len(q))
        return [(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(m)]

    def pmul(p, q):
        out = [0] * (len(p) + len(q) - 1)
        for i, a in enumerate(p):
            for j, b in enumerate(q):
                out[i + j] += a * b
        return out

    def pneg(p):
        return [-a for a in p]

    M = [[([-A[i][j]] if i != j else [-A[i][j], 1]) for j in range(n)] for i in range(n)]

    def pdet(M):
        k = len(M)
        if k == 1:
            return M[0][0]
        acc = [0]
        for j in range(k):
            minor = [row[:j] + row[j + 1:] for row in M[1:]]
            term = pmul(M[0][j], pdet(minor))
            acc = padd(acc, term if j % 2 == 0 else pneg(term))
        return acc

    return pdet(M)


def v2() -> None:
    states = [(0, 0), (0, 1), (1, 0), (1, 1)]
    letters = [(1, 1), (0, 1), (0, 0)]  # zero cell, even cell, odd cell
    A = [[0] * 4 for _ in range(4)]
    for i, (h, F) in enumerate(states):
        for a, b in letters:
            A[i][states.index((h ^ 1 ^ a, F ^ (h & b)))] += 1
    p = poly_det(A)  # low to high
    high_to_low = p[::-1]
    pv = lambda x: sum(c * x ** k for k, c in enumerate(p))
    print(f"V2 transfer matrix rows (states 00,01,10,11): {A}")
    print(f"V2 charpoly det(xI - A), high to low: {high_to_low}; p(1)={pv(1)} p(3)={pv(3)} p(-1)={pv(-1)}")
    assert high_to_low == [1, -2, -4, 2, 3] and pv(1) == 0 and pv(3) == 0 and pv(-1) == 0
    # direct d(m) for m <= 40 from A^m, and (3^m+1)/2 count
    P = [[int(i == j) for j in range(4)] for i in range(4)]
    for m in range(1, 41):
        P = [[sum(P[i][k] * A[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
        N0 = sum(P[states.index((h0, 0))][states.index((1, 0))] for h0 in (0, 1))
        N1 = sum(P[states.index((h0, 0))][states.index((1, 1))] for h0 in (0, 1))
        assert N0 - N1 == 1 and N0 + N1 == 3 ** m and N0 == (3 ** m + 1) // 2, (m, N0, N1)
    print("V2 verdict: charpoly matches PROOF.md; d(m) = 1 and N0 = (3^m+1)/2 for m <= 40 by exact matrix power.")


def v3(umax: int) -> None:
    checked = replacements = 0
    for u in range(1, umax + 1):
        for word in product((1, 2), repeat=u):
            prev = triangle(word)[u - 1]
            for n in range(1, u + 1):
                e_u, cur = forced(prev, u, n)
                qs = [d for d in range(n - 1, -u - 1, -1) if prev[d] != 0]
                for idx, d in enumerate(qs, start=1):
                    if idx % 2 == 0:
                        continue
                    for v in (1, 2, 3):
                        if v == prev[d]:
                            continue
                        alt = dict(prev)
                        alt[d] = v
                        e2, cur2 = forced(alt, u, n)
                        assert e2 == e_u and cur2 == cur, ("V3", word, n, d, v)
                        replacements += 1
                checked += 1
    print(f"V3 Lemma 10 at ALL depths of column u (up to depth u): {checked} (word, n) pairs, {replacements} odd-index "
          f"replacements, column u identical on [-u-1, u] in every case. Extension beyond depth n holds (trivially, "
          f"since depths > n read the window only through T[u][n]).")


def v4(umax: int) -> None:
    seen = {}
    witness = None
    for u in range(2, umax + 1):
        for word in product((1, 2), repeat=u):
            prev = triangle(word)[u - 1]
            for n in range(1, u):  # need n < u so depth n+1 <= u exists in column u+1 (which has depth up to u+1)
                e_u, cur = forced(prev, u, n)
                e_next, nxt = forced(cur, u + 1, n)
                Zp = tuple(d for d in range(-u, n) if prev[d] == 0)
                Zu = tuple(d for d in range(-u - 1, n) if cur[d] == 0)
                key = (n, u, Zp, Zu)
                val = (tuple(nxt[d] for d in range(-u - 2, n + 1)), nxt[n + 1])
                if key in seen:
                    other = seen[key]
                    assert other[0] == val[0], ("V4 depth<=n disagreement", key)
                    if other[1] != val[1] and witness is None:
                        witness = (key, other[1], val[1])
                else:
                    seen[key] = val
    print(f"V4 pair (n,u,Z_(u-1),Z_u) -> column u+1 on [-u-2, n]: consistent on all keys, u <= {umax}.")
    if witness:
        print(f"V4 but T[u+1][n+1] differs for equal keys; first witness key={witness[0]}, values {witness[1]} vs {witness[2]}. "
              f"So 'whole forced future' is established at depth <= n only, as Lemma 9(iii) states.")
    else:
        print("V4 no witness of a depth n+1 disagreement found in this range.")


if __name__ == "__main__":
    v1(9)
    v2()
    v3(9)
    v4(9)
    print("verify_logic_checks: DONE")

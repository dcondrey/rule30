#!/usr/bin/env python3
"""Finite checks cited by PROOF.md for the lemma "retained-bit-form" (a)-(e).

Each check is a finite exhaustive computation.  Any AssertionError kills; the
tuple names the check and the witness.  The checks are of two kinds:

  FACTS used by the proof (finite by nature, the proof rests on them):
    S1  decoupling of the local rule CONE on all 16 argument pairs
    S2  boundary facts: BOUNDARY[s] = s XOR 3, CONE[3][r] = BOUNDARY[r],
        H(s XOR 3) = 1 + H(s), E(s XOR 3) = E(s)
    S3  psi_kernel.Endpoint realises the triangle recurrence of BRIEF section 2
        (ties the object of the lemma to the kernel)

  GATES on the derivation (the proof does not rest on them; they catch slips):
    S4  Lemma H and Lemma E (column integrals), all 4-state prefixes u <= U4,
        all binary prefixes u <= UB, every e_u in {0..3}, every d in the column
    S5  statements (a)-(d), the set form of Phi, the block read-out and the
        odd-bit invisibility, all binary prefixes u <= UB, all n <= u
    S6  statement (e) on the letter space {0,2,x}^m, m <= M: block formula
        equals the Moore Phi, the q_2 toggle is a Phi-flipping involution on
        N >= 2, the N <= 1 census matches the closed form, and the total is
        (3^m + 1)/2

Run:  cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant \
      && uv run python uc/r1-quadratic-prove-retained-bit-form-structural/rbf_structural_checks.py
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from itertools import product

WORK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, WORK)

from psi_kernel import BOUNDARY, CONE, Endpoint  # noqa: E402

MUTATE = False   # --mutate: define retained as ODD-indexed; the checks must then fire


def H(t: int) -> int:
    return t >> 1


def Lo(t: int) -> int:
    return t & 1


def E(t: int) -> int:
    return (1 + (t >> 1) + (t & 1)) & 1


# ---------------------------------------------------------------------------
# S1, S2: the finite facts the proof rests on
# ---------------------------------------------------------------------------

def s1_decoupling() -> int:
    n = 0
    for l in range(4):
        for r in range(4):
            t = CONE[l][r]
            assert H(t) == (H(r) + 1 + (1 if l == 0 else 0)) & 1, ("S1-H", l, r, t)
            assert E(t) == (E(r) + H(r) * (1 if Lo(l) == 0 else 0)) & 1, ("S1-E", l, r, t)
            n += 1
    # right-bijectivity for fixed left argument (used only for context)
    for l in range(4):
        assert sorted(CONE[l]) == [0, 1, 2, 3], ("S1-bij", l)
    return n


def s2_boundary() -> int:
    n = 0
    for s in range(4):
        assert BOUNDARY[s] == s ^ 3, ("S2-boundary", s, BOUNDARY[s])
        assert CONE[3][s] == BOUNDARY[s], ("S2-cone3", s)
        assert H(s ^ 3) == (1 + H(s)) & 1, ("S2-H", s)
        assert E(s ^ 3) == E(s), ("S2-E", s)
        n += 1
    for s in (1, 2):
        assert E(s) == 0 and E(s ^ 3) == 0, ("S2-binaryE", s)
    return n


# ---------------------------------------------------------------------------
# the triangle, two ways
# ---------------------------------------------------------------------------

def triangle(word: tuple[int, ...]) -> list[dict[int, int]]:
    """T[u][d] for u < len(word), d in [-u-1, u], by the BRIEF section 2 recurrence."""
    T: list[dict[int, int]] = []
    for u, e in enumerate(word):
        col = {-u - 1: e, -u: e ^ 3}
        for d in range(-u + 1, u + 1):
            col[d] = CONE[T[u - 1][d - 1]][col[d - 1]]
        T.append(col)
    return T


def column_of(ep: Endpoint) -> dict[int, int]:
    """T[u][d], d in [-u-1, u], for the endpoint of length u+1 held by ep."""
    col = {}
    for i, t in enumerate(ep.column):
        col[-i] = t
    for k, t in enumerate(ep.diagonal):
        col[k] = t
    return col


def s3_kernel_is_triangle(ub: int, u4: int) -> int:
    n = 0
    for alphabet, umax in (((1, 2), ub), ((0, 1, 2, 3), u4)):
        for u in range(1, umax + 1):
            for word in product(alphabet, repeat=u):
                T = triangle(word)
                ep = Endpoint()
                for k, s in enumerate(word):
                    ep.append(s)
                    assert column_of(ep) == T[k], ("S3", word, k)
                n += 1
    return n


# ---------------------------------------------------------------------------
# S4: the column integrals (Lemma H, Lemma E) on whole columns
# ---------------------------------------------------------------------------

def s4_integrals(ub: int, u4: int) -> int:
    cells = 0
    for alphabet, umax in (((1, 2), ub), ((0, 1, 2, 3), u4)):
        for u in range(1, umax + 1):
            for prefix in product(alphabet, repeat=u):
                for e_u in range(4):
                    T = triangle(prefix + (e_u,))
                    prev, cur = T[u - 1], T[u]
                    zeros = 0
                    ev = 0
                    for d in range(-u, u + 1):
                        # Lemma H
                        assert H(cur[d]) == (H(e_u) + d + u + 1 + zeros) & 1, ("S4-H", prefix, e_u, d)
                        # Lemma E
                        assert E(cur[d]) == (E(e_u) + ev) & 1, ("S4-E", prefix, e_u, d)
                        cells += 1
                        if d < u:
                            t = prev[d]
                            zeros += 1 if t == 0 else 0
                            ev += 1 if (H(cur[d]) == 1 and Lo(t) == 0) else 0
    return cells


# ---------------------------------------------------------------------------
# S5: statements (a)-(d) on binary prefixes
# ---------------------------------------------------------------------------

def analyse(prev: dict[int, int], lo: int, hi: int):
    """Ordered object of the window [lo, hi): qs from the top, retained map,
    blocks B_0..B_N as (q_i, z_i), maximal non-retained runs R_0..R_{K-1}."""
    qs = [d for d in range(hi - 1, lo - 1, -1) if prev[d] != 0]
    N = len(qs)
    retained = {}
    for i, d in enumerate(qs, start=1):
        retained[d] = (i % 2 == 0) != MUTATE
    above = True
    for d in range(hi - 1, lo - 1, -1):
        if prev[d] != 0:
            above = retained[d]
        else:
            retained[d] = above
    # blocks: z_0 zeros above q_1; block i = q_i followed by z_i zeros
    z = [0] * (N + 1)
    z[0] = sum(1 for d in range(hi - 1, (qs[0] if N else lo - 1), -1))
    for i in range(1, N + 1):
        bottom = qs[i] if i < N else lo - 1
        z[i] = qs[i - 1] - bottom - 1
    w = [None] + [1 if prev[d] == 2 else 0 for d in qs]   # w_i, i = 1..N
    runs = []
    for i in range(1, N + 1, 2):
        bottom = qs[i] if i < N else lo - 1
        runs.append(list(range(qs[i - 1], bottom, -1)))
    return qs, N, retained, z, w, runs


def phi_set_form(prev: dict[int, int], lo: int, hi: int) -> int:
    m = hi - lo
    Z = sum(1 for d in range(lo, hi) if prev[d] == 0)
    W2 = sum(1 for d in range(lo, hi) if prev[d] == 2)
    pairs = 0
    nonzero_below = 0
    for d in range(lo, hi):
        t = prev[d]
        if t == 0 or t == 2:
            pairs += nonzero_below
        if t != 0:
            nonzero_below += 1
    return ((Z + W2) * (1 + m + Z) + pairs) & 1


def column_from_window(cells: list[int]) -> tuple[int, list[int]]:
    """Kernel rule on a free window (cells at d = -u..n-1); e_u forced by H(T[u][n]) = 1.
    Returns (e_u, column u at d = -u-1..n).  Asserts the forced symbol is unique."""
    found = []
    for s in (1, 2):
        col = [s, s ^ 3]
        for t in cells:
            col.append(CONE[t][col[-1]])
        if H(col[-1]) == 1:
            found.append((s, col))
    assert len(found) == 1, ("S5-forcing", cells, [f[0] for f in found])
    return found[0]


def s5_statements(ub: int) -> dict:
    st = {"pairs": 0, "odd_flips": 0, "even_flips": 0, "keys": 0}
    pair_map: dict = {}
    for u in range(1, ub + 1):
        for word in product((1, 2), repeat=u):
            T = triangle(word)
            prev = T[u - 1]
            for n in range(1, u + 1):
                lo, hi = -u, n
                cells = [prev[d] for d in range(lo, hi)]
                e_u, colw = column_from_window(cells)
                cur = {d: colw[d + u + 1] for d in range(-u - 1, n + 1)}
                # the same column by the triangle on the extended word
                T2 = triangle(word + (e_u,))
                assert all(T2[u][d] == cur[d] for d in range(-u - 1, n + 1)), ("S5-window", word, n)
                qs, N, retained, z, w, runs = analyse(prev, lo, hi)
                assert qs[-1] == lo, ("S5-bottom-nonzero", word, n)
                # (a)
                assert (e_u == 2) == (N % 2 == 1), ("a", word, n, e_u, N)
                # (b)
                for d in range(lo, hi):
                    assert H(cur[d]) == (1 if retained[d] else 0), ("b", word, n, d)
                assert H(cur[n]) == 1, ("b-pin", word, n)
                # (c), in block form and in retained-cell form
                ret_zero = z[0] + sum(z[i] for i in range(2, N + 1, 2))
                even_two = sum(w[i] for i in range(2, N + 1, 2))
                assert (ret_zero + even_two) & 1 == E(cur[n]), ("c", word, n)
                ret_zero_direct = sum(1 for d in range(lo, hi) if prev[d] == 0 and retained[d])
                assert ret_zero_direct == ret_zero, ("c-blocks", word, n)
                # Corollary: BRIEF section 3 set form
                assert phi_set_form(prev, lo, hi) == E(cur[n]), ("c-setform", word, n)
                # (d1) Z_u is a union of complete runs; bottom cell nonzero
                assert cur[-u - 1] != 0, ("d1-bottom", word, n)
                Zu = {d for d in range(-u - 1, n) if cur[d] == 0}
                covered = set()
                F = []
                for run in runs:
                    inside = [d in Zu for d in run]
                    assert all(inside) or not any(inside), ("d1-partial", word, n, run)
                    F.append(1 if inside[0] else 0)
                    covered.update(run)
                assert Zu <= covered, ("d1-outside", word, n, sorted(Zu - covered))
                # F_k = E_u on run k, directly
                for k, run in enumerate(runs):
                    for d in run:
                        assert E(cur[d]) == F[k], ("d1-F", word, n, k, d)
                # (d2) read-out of even bits: w_{2k+2} = F_k + F_{k+1} + z_{2k+2}, F_K = 0
                K = len(runs)
                assert K == (N + 1) // 2, ("d2-K", word, n)
                for k in range(K):
                    i = 2 * k + 2
                    if i > N:
                        break
                    f_below = F[k + 1] if k + 1 < K else 0
                    assert (F[k] + f_below + z[i]) & 1 == w[i], ("d2", word, n, i)
                # (d3) the pair (Z_{u-1}, Z_u) determines column u on [-u-1, n] and e_{u+1}
                Zp = tuple(d for d in range(lo, hi) if prev[d] == 0)
                colkey = tuple(cur[d] for d in range(-u - 1, n + 1))
                e_next, _ = column_from_window([cur[d] for d in range(-u - 1, n)])
                key = (n, u, Zp, tuple(sorted(Zu)))
                val = (colkey, e_next)
                assert pair_map.setdefault(key, val) == val, ("d3", word, n, key)
                # (d5) odd-indexed even-bits are not read; even-indexed ones are
                for i, q in enumerate(qs, start=1):
                    flipped = cells[:]
                    j = q - lo
                    flipped[j] = 2 if cells[j] in (1, 3) else 1   # toggle the even-bit; 1 and 3 are both odd
                    ef, colf = column_from_window(flipped)
                    if i % 2 == 1:
                        assert (ef, colf) == (e_u, colw), ("d5-odd-read", word, n, q)
                        st["odd_flips"] += 1
                    else:
                        assert (ef, colf) != (e_u, colw), ("d5-even-blind", word, n, q)
                        st["even_flips"] += 1
                st["pairs"] += 1
    st["keys"] = len(pair_map)
    return st


# ---------------------------------------------------------------------------
# S6: the letter-space balance (e)
# ---------------------------------------------------------------------------

LETTER = {0: (1, 1), 2: (0, 1), 1: (0, 0)}   # 1 stands for x (odd cell)


def moore_phi(word: tuple[int, ...]) -> int:
    """Phi on a letter word read from the bottom (index 0 = d = -u), forced start."""
    nonzero = sum(1 for t in word if t != 0)
    h = (1 + nonzero) & 1
    F = 0
    for t in word:
        a, b = LETTER[t]
        F ^= h & b
        h ^= 1 ^ a
    assert h == 1
    return F


def block_phi(word: tuple[int, ...]) -> tuple[int, int]:
    """Phi by the block formula z_0 + sum_{i even} (z_i + w_i); also returns N."""
    top_down = word[::-1]
    qs = [j for j, t in enumerate(top_down) if t != 0]
    N = len(qs)
    z0 = qs[0] if N else len(top_down)
    phi = z0
    for i in range(2, N + 1, 2):
        q = qs[i - 1]
        nxt = qs[i] if i < N else len(top_down)
        z_i = nxt - q - 1
        w_i = 1 if top_down[q] == 2 else 0
        phi += z_i + w_i
    return phi & 1, N


def s6_balance(mmax: int, log) -> None:
    for m in range(1, mmax + 1):
        n0 = n1 = 0
        n0_small = n1_small = 0
        checked_invol = 0
        for word in product((0, 1, 2), repeat=m):
            p = moore_phi(word)
            pb, N = block_phi(word)
            assert p == pb, ("S6-block", word, p, pb)
            if p == 0:
                n0 += 1
            else:
                n1 += 1
            if N >= 2:
                top_down = list(word[::-1])
                qs = [j for j, t in enumerate(top_down) if t != 0]
                j = qs[1]
                top_down[j] = 2 if top_down[j] == 1 else 1
                partner = tuple(top_down[::-1])
                assert partner != word and moore_phi(partner) == 1 - p, ("S6-invol", word)
                # involution: applying it twice returns the word (q_2 position unchanged)
                td2 = list(partner[::-1])
                qs2 = [j for j, t in enumerate(td2) if t != 0]
                assert qs2 == qs, ("S6-invol-positions", word)
                checked_invol += 1
            else:
                if p == 0:
                    n0_small += 1
                else:
                    n1_small += 1
        # closed form for N <= 1:  N = 0 word has Phi = m mod 2;
        # N = 1 words: 2 letters times position z_0 in [0, m-1], Phi = z_0 mod 2
        exp0 = (1 if m % 2 == 0 else 0) + 2 * ((m + 1) // 2)
        exp1 = (1 if m % 2 == 1 else 0) + 2 * (m // 2)
        assert (n0_small, n1_small) == (exp0, exp1), ("S6-small", m, n0_small, n1_small, exp0, exp1)
        assert n0 - n1 == 1, ("S6-diff", m, n0, n1)
        assert n0 == (3 ** m + 1) // 2, ("S6-total", m, n0)
        print(f"  S6 m={m:<2} N0={n0:<6} N1={n1:<6} N0-N1={n0-n1}  N<=1 census (Phi=0,1)=({n0_small},{n1_small}) "
              f"matches closed form; involution checked on {checked_invol} words with N>=2", file=log, flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ub", type=int, default=12, help="binary prefixes to this length")
    ap.add_argument("--u4", type=int, default=6, help="four-state prefixes to this length")
    ap.add_argument("--m", type=int, default=10, help="letter-space length for (e)")
    ap.add_argument("--mutate", action="store_true", help="control: retained := odd-indexed; must fire")
    args = ap.parse_args()
    if args.mutate:
        global MUTATE
        MUTATE = True
    log = sys.stdout
    print(f"rbf_structural_checks.py args={vars(args)}", file=log, flush=True)
    t0 = time.time()
    n1 = s1_decoupling()
    print(f"S1 decoupling: H(phi(l,r)) = H(r)+1+[l=0], E(phi(l,r)) = E(r)+H(r)[Lo(l)=0] on all {n1} pairs; "
          f"phi right-bijective for each l PASS", file=log, flush=True)
    n2 = s2_boundary()
    print(f"S2 boundary: BOUNDARY[s]=s^3, CONE[3][r]=BOUNDARY[r], H(s^3)=1+H(s), E(s^3)=E(s) on {n2} symbols; "
          f"E(1)=E(2)=E(1^3)=E(2^3)=0 PASS", file=log, flush=True)
    n3 = s3_kernel_is_triangle(args.ub, args.u4)
    print(f"S3 kernel = triangle recurrence: {n3} words (binary u<={args.ub}, four-state u<={args.u4}), "
          f"every column PASS   [{time.time()-t0:.0f}s]", file=log, flush=True)
    n4 = s4_integrals(args.ub, args.u4)
    print(f"S4 Lemma H and Lemma E on {n4} cells (binary prefixes u<={args.ub} and four-state u<={args.u4}, "
          f"all four e_u, every d in [-u,u]) PASS   [{time.time()-t0:.0f}s]", file=log, flush=True)
    st = s5_statements(args.ub)
    print(f"S5 statements (a)(b)(c)(d1)(d2)(d3)(d5) and the set form of Phi on {st['pairs']} (word, n) pairs, "
          f"all binary words u<={args.ub}, all n<=u; forced symbol unique everywhere; "
          f"{st['keys']} distinct (n,u,Z_(u-1),Z_u) keys each with one column; "
          f"odd-indexed even-bit flips invisible: {st['odd_flips']}; even-indexed flips visible: {st['even_flips']} PASS"
          f"   [{time.time()-t0:.0f}s]", file=log, flush=True)
    s6_balance(args.m, log)
    print(f"S6 balance (e): block formula = Moore Phi, q_2 toggle flips Phi on N>=2, N<=1 census closed form, "
          f"N0-N1=1 and N0=(3^m+1)/2 for m<={args.m} PASS   [{time.time()-t0:.0f}s]", file=log, flush=True)
    print(f"ALL PASS   [{time.time()-t0:.0f}s]", file=log, flush=True)


if __name__ == "__main__":
    main()

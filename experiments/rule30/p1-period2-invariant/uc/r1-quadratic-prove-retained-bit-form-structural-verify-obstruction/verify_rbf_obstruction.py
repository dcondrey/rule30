#!/usr/bin/env python3
"""Independent adversarial verification of the lemma retained-bit-form (a)-(e).

Written from the lemma statement and BRIEF section 2 only; it shares no code
with rbf_structural_checks.py (it imports only CONE, BOUNDARY and psi from
psi_kernel).  Every AssertionError is a kill; the tuple names the check.

  V0  F1 (decoupling) determines the table: rebuild CONE from the two F1
      formulas and compare cell by cell; BOUNDARY = s XOR 3 = CONE[3][s].
  V1  (a)-(d) on every binary word u <= UB and every n <= u, with "retained"
      computed by the lemma's literal definition (parity of the number of
      nonzero window cells at or above the cell), not by blocks.
      d3 is checked as: one column u on [-u-1, n] per (n, u, Z_(u-1), Z_u),
      and one Z_(u+1) per key (the second-order recursion).
      d5 is checked on free windows with the cells above the window held
      fixed, so the whole column u on [-u-1, u] is compared, not only [-u-1, n].
  V2  (e) by brute force, own Moore implementation, m <= M, plus the
      involution and the |N| <= 1 census used in the proof.
  V3  tie to the kernel: forced continuation and hit word against
      psi_kernel.psi on every source n <= UB.
  V4  small-n sanity: the (BWH+) constants at n = 5, 6 are listed and the
      identities (a)-(d) rechecked along their forced orbits u = n..2n+1.
  V5  fibres of a single Z_(u-1) exist (consistent with the killed row
      "bare holonomy-defect word"); distinct pairs = distinct columns.
  V6  Rule 90 transport: the analogous linear kernel (OR -> XOR in the carry
      macro).  Shows F1 as stated fails there, but the analogous statement
      "column u on [-u-1, n] is an affine function of the window and e_u"
      holds; an identity of this kind constrains no periodicity.

Run:  cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant \
      && uv run python uc/r1-quadratic-prove-retained-bit-form-structural-verify-obstruction/verify_rbf_obstruction.py
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from itertools import product

WORK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, WORK)

from psi_kernel import BOUNDARY, CONE, psi  # noqa: E402


def H(t: int) -> int:
    return t >> 1


def Lo(t: int) -> int:
    return t & 1


def E(t: int) -> int:
    return (1 + (t >> 1) + (t & 1)) & 1


# ---------------------------------------------------------------------------
# V0: F1 determines the table
# ---------------------------------------------------------------------------

def v0_table() -> None:
    for l in range(4):
        for r in range(4):
            h = (H(r) + 1 + (1 if l == 0 else 0)) & 1
            e = (E(r) + H(r) * (1 if Lo(l) == 0 else 0)) & 1
            t = 2 * h + ((1 + h + e) & 1)
            assert CONE[l][r] == t, ("V0-F1-determines-CONE", l, r, CONE[l][r], t)
    for s in range(4):
        assert BOUNDARY[s] == s ^ 3 == CONE[3][s], ("V0-boundary", s)


# ---------------------------------------------------------------------------
# the triangle (own implementation)
# ---------------------------------------------------------------------------

def tri(word, table=CONE):
    """T[u][d], d in [-u-1, u], stored as dict per column."""
    T = []
    for u, e in enumerate(word):
        col = {-u - 1: e, -u: table[3][e]}
        for d in range(-u + 1, u + 1):
            col[d] = table[T[u - 1][d - 1]][col[d - 1]]
        T.append(col)
    return T


def col_from_window(win: list[int], s: int, table=CONE) -> list[int]:
    """Column u at d = -u-1 .. -u-1+len(win)+1 from symbol s and window cells (d = -u upward)."""
    col = [s, table[3][s]]
    for t in win:
        col.append(table[t][col[-1]])
    return col


def forced_symbol(win: list[int]) -> tuple[int, list[int]]:
    found = [(s, col_from_window(win, s)) for s in (1, 2)]
    found = [(s, c) for s, c in found if H(c[-1]) == 1]
    assert len(found) == 1, ("V1-forcing-unique", win, [f[0] for f in found])
    return found[0]


def retained_literal(win: list[int]) -> list[bool]:
    """Lemma definition: from the top, a cell is retained iff the number of
    nonzero cells at or above it (within the window) is even."""
    m = len(win)
    ret = [False] * m
    count = 0
    for j in range(m - 1, -1, -1):
        if win[j] != 0:
            count += 1
        ret[j] = (count % 2 == 0)
    return ret


def nonretained_runs(ret: list[bool]) -> list[tuple[int, int]]:
    runs = []
    j = 0
    m = len(ret)
    while j < m:
        if not ret[j]:
            k = j
            while k < m and not ret[k]:
                k += 1
            runs.append((j, k))
            j = k
        else:
            j += 1
    return runs


# ---------------------------------------------------------------------------
# V1: (a)-(d)
# ---------------------------------------------------------------------------

def v1_identities(ub: int, log) -> dict:
    st = {"pairs": 0, "odd_flips": 0, "even_flips": 0, "top_nonzero": 0, "top_flips": 0}
    pair_col: dict = {}
    pair_next: dict = {}
    for u in range(1, ub + 1):
        for word in product((1, 2), repeat=u):
            T = tri(word)
            prev = T[u - 1]
            full_prev = [prev[d] for d in range(-u, u)]          # column u-1 on [-u, u-1]
            for n in range(1, u + 1):
                m = n + u
                win = full_prev[:m]                                # d = -u .. n-1
                assert win[0] != 0, ("V1-bottom", word, n)
                e_u, col = forced_symbol(win)                      # col[k] = T[u][-u-1+k], k = 0..m+1
                # agreement with the triangle on the extended word
                T2 = tri(word + (e_u,))
                for k in range(m + 2):
                    assert T2[u][-u - 1 + k] == col[k], ("V1-triangle-agree", word, n, k)
                N = sum(1 for t in win if t != 0)
                Z = m - N
                # (a)
                assert (e_u == 2) == (N % 2 == 1), ("a", word, n, e_u, N)
                # H-forcing line of BRIEF section 3
                assert H(e_u) == (1 + (n + u + 1) + Z) & 1, ("a-brief", word, n)
                ret = retained_literal(win)
                # (b): H(T[u][d]) = 1 iff retained, d = -u..n-1 is col[1..m]
                for j in range(m):
                    assert H(col[j + 1]) == (1 if ret[j] else 0), ("b", word, n, -u + j)
                assert H(col[m + 1]) == 1, ("b-pin", word, n)
                # (c)
                rz = sum(1 for j in range(m) if ret[j] and win[j] == 0)
                r2 = sum(1 for j in range(m) if ret[j] and win[j] == 2)
                assert (rz + r2) & 1 == E(col[m + 1]), ("c", word, n, rz, r2, E(col[m + 1]))
                # (d1): Z_u on [-u-1, n-1] is a union of complete non-retained runs
                assert col[0] != 0, ("d1-bottom", word, n)
                zu = [col[j + 1] == 0 for j in range(m)]           # window depths only
                runs = nonretained_runs(ret)
                for (a, b) in runs:
                    vals = zu[a:b]
                    assert all(vals) or not any(vals), ("d1-partial", word, n, a, b)
                covered = [False] * m
                for (a, b) in runs:
                    for j in range(a, b):
                        covered[j] = True
                for j in range(m):
                    if zu[j]:
                        assert covered[j], ("d1-outside-run", word, n, -u + j)
                        assert not ret[j], ("d1-retained-zero", word, n, -u + j)
                # (d3): key -> column u on [-u-1, n], and key -> Z_(u+1)
                Zp = tuple(j for j in range(m) if win[j] == 0)
                Zu = tuple(j for j in range(m) if zu[j])
                key = (n, u, Zp, Zu)
                colkey = tuple(col)
                assert pair_col.setdefault(key, colkey) == colkey, ("d3-column", word, n, key)
                # Z_(u+1): zero set of column u+1 on [-u-2, n-1]; window of u+1 is column u on [-u-1, n-1] = col[0..m]
                e_next, col_next = forced_symbol(col[: m + 1])
                Znext = tuple(k for k in range(m + 2) if col_next[k] == 0)   # k = 0 is d = -u-2
                assert pair_next.setdefault(key, (e_next, Znext)) == (e_next, Znext), ("d3-next", word, n, key)
                # (d5): toggle even-bits, cells above the window held fixed, whole column [-u-1, u]
                base_full = col_from_window(full_prev, e_u)
                idx = 1
                for j in range(m - 1, -1, -1):
                    if win[j] == 0:
                        continue
                    flipped = full_prev[:]
                    flipped[j] = 2 if win[j] in (1, 3) else 1
                    fw = flipped[:m]
                    found = [(s, col_from_window(fw, s)) for s in (1, 2)]
                    found = [(s, c) for s, c in found if H(c[-1]) == 1]
                    assert len(found) == 1, ("d5-forcing", word, n, j)
                    ef = found[0][0]
                    full_f = col_from_window(flipped, ef)
                    if idx % 2 == 1:
                        assert ef == e_u and full_f == base_full, ("d5-odd-read", word, n, -u + j, idx)
                        st["odd_flips"] += 1
                        if j == m - 1:
                            st["top_flips"] += 1
                    else:
                        assert full_f[: m + 2] != base_full[: m + 2], ("d5-even-blind", word, n, -u + j, idx)
                        # the change reaches T[u][n]
                        assert full_f[m + 1] != base_full[m + 1], ("d5-even-top", word, n, -u + j, idx)
                        st["even_flips"] += 1
                    idx += 1
                if win[m - 1] != 0:
                    st["top_nonzero"] += 1
                st["pairs"] += 1
    st["keys"] = len(pair_col)
    return st


# ---------------------------------------------------------------------------
# V2: (e)
# ---------------------------------------------------------------------------

AB = {0: (1, 1), 2: (0, 1), 3: (0, 0)}   # letters 0, 2, x (x coded as 3)


def phi_moore(q: tuple[int, ...]) -> int:
    N = sum(1 for t in q if t != 0)
    h = (1 + N) & 1
    F = 0
    for t in q:
        a, b = AB[t]
        F ^= h & b
        h ^= 1 ^ a
    assert h == 1, ("V2-final-h", q)
    return F


def v2_balance(mmax: int, log) -> None:
    for m in range(1, mmax + 1):
        n0 = 0
        small = [0, 0]
        for q in product((0, 2, 3), repeat=m):
            p = phi_moore(q)
            n0 += 1 - p
            N = sum(1 for t in q if t != 0)
            if N >= 2:
                # toggle the second nonzero from the top
                qq = list(q)
                pos = [j for j in range(m - 1, -1, -1) if q[j] != 0][1]
                qq[pos] = 3 if q[pos] == 2 else 2
                assert phi_moore(tuple(qq)) == 1 - p, ("V2-involution", q)
            else:
                small[p] += 1
        n1 = 3 ** m - n0
        assert n0 == (3 ** m + 1) // 2, ("e", m, n0)
        exp0 = (1 if m % 2 == 0 else 0) + 2 * ((m + 1) // 2)
        exp1 = (1 if m % 2 == 1 else 0) + 2 * (m // 2)
        assert small == [exp0, exp1], ("V2-small", m, small, exp0, exp1)
        print(f"  V2 m={m:<2} N0={n0} N1={n1} N0-N1={n0-n1} small(N<=1)={small}", file=log, flush=True)


# ---------------------------------------------------------------------------
# V3: tie to psi_kernel.psi; V4: small-n sanity on the (BWH+) constants
# ---------------------------------------------------------------------------

def forced_orbit(source: tuple[int, ...], n: int, steps: int):
    """Append `steps` forced symbols after the source; return (symbols, hits)."""
    word = list(source)
    syms, hits = [], []
    for _ in range(steps):
        u = len(word)
        T = tri(tuple(word))
        prev = T[u - 1]
        win = [prev[d] for d in range(-u, n)]
        e_u, col = forced_symbol(win)
        word.append(e_u)
        syms.append(e_u)
        hits.append(E(col[-1]))
    return tuple(syms), tuple(hits)


def v3_psi_tie(ub: int, log) -> int:
    count = 0
    for n in range(1, ub + 1):
        for W in product((1, 2), repeat=n):
            Q, Psi = psi(W)
            syms, hits = forced_orbit(W, n, len(Q))
            assert tuple(Q) == syms, ("V3-Q", W, Q, syms)
            assert tuple(Psi) == hits, ("V3-Psi", W, Psi, hits)
            count += 1
    return count


def v4_small_n(log) -> None:
    for n in (5, 6, 7):
        consts = []
        for W in product((1, 2), repeat=n):
            Q, Psi = psi(W)
            if len(set(Psi)) == 1:
                consts.append((W, tuple(Q), tuple(Psi)))
        print(f"  V4 n={n}: {len(consts)} sources with constant Psi over {n+2} forced columns", file=log, flush=True)
        for W, Q, Psi in consts:
            # recheck (a)-(c) and the pair encoding along the orbit u = n .. 2n+1
            word = list(W)
            for u in range(n, 2 * n + 2):
                T = tri(tuple(word))
                prev = T[u - 1]
                win = [prev[d] for d in range(-u, n)]
                e_u, col = forced_symbol(win)
                N = sum(1 for t in win if t != 0)
                assert (e_u == 2) == (N % 2 == 1), ("V4-a", W, u)
                ret = retained_literal(win)
                for j in range(n + u):
                    assert H(col[j + 1]) == (1 if ret[j] else 0), ("V4-b", W, u, j)
                rz = sum(1 for j in range(n + u) if ret[j] and win[j] == 0)
                r2 = sum(1 for j in range(n + u) if ret[j] and win[j] == 2)
                assert (rz + r2) & 1 == E(col[-1]) == Psi[u - n], ("V4-c", W, u)
                assert e_u == Q[u - n], ("V4-Q", W, u)
                word.append(e_u)
            hc = all(not (Q[i] == 1 and Q[i + 1] == 1) for i in range(len(Q) - 1)) and not (W[-1] == 1 and Q[0] == 1)
            print(f"      W={''.join(map(str, W))} Q={''.join(map(str, Q))} Psi={''.join(map(str, Psi))} "
                  f"hard-core continuation: {hc}; identities (a)(b)(c) hold on every column", file=log, flush=True)


# ---------------------------------------------------------------------------
# V5: single-pattern fibres exist; pairs are lossless
# ---------------------------------------------------------------------------

def v5_fibres(nmax: int, log) -> None:
    for n in range(1, nmax + 1):
        single: dict = {}
        pairs: dict = {}
        cols_by_level: dict = {}
        for W in product((1, 2), repeat=n):
            word = list(W)
            for u in range(n, 2 * n + 2):
                T = tri(tuple(word))
                prev = T[u - 1]
                win = [prev[d] for d in range(-u, n)]
                e_u, col = forced_symbol(win)
                Zp = tuple(j for j in range(n + u) if win[j] == 0)
                Zu = tuple(j for j in range(n + u) if col[j + 1] == 0)
                single.setdefault((u, Zp), set()).add(tuple(col))
                pairs.setdefault((u, Zp, Zu), set()).add(tuple(col))
                cols_by_level.setdefault(u, set()).add(tuple(col))
                word.append(e_u)
        multi = sum(1 for v in single.values() if len(v) > 1)
        maxfib = max(len(v) for v in single.values())
        assert all(len(v) == 1 for v in pairs.values()), ("V5-pair-not-lossless", n)
        npairs_by_level = {}
        for (u, Zp, Zu) in pairs:
            npairs_by_level[u] = npairs_by_level.get(u, 0) + 1
        assert all(npairs_by_level[u] == len(cols_by_level[u]) for u in cols_by_level), ("V5-count", n)
        print(f"  V5 n={n}: Z_(u-1) alone: {len(single)} keys, {multi} with >1 column u, max fibre {maxfib}; "
              f"pairs: {len(pairs)} keys, all single; distinct pairs = distinct columns at every level "
              f"(levels u=n..2n+1: {[len(cols_by_level[u]) for u in sorted(cols_by_level)]})", file=log, flush=True)


# ---------------------------------------------------------------------------
# V6: Rule 90 transport of the argument shape
# ---------------------------------------------------------------------------

def _swap(s: int) -> int:
    return 2 * (s & 1) + (s >> 1)


def carry90(symbol: int, state: int) -> int:
    a, b = symbol >> 1, symbol & 1
    c, d = state >> 1, state & 1
    return 2 * (c ^ (a ^ b)) + (d ^ (c ^ a))      # OR replaced by XOR


def v6_rule90(ub: int, log) -> None:
    FWD = tuple(tuple(carry90(s, q) for q in range(4)) for s in range(4))
    INV = []
    for row in FWD:
        assert sorted(row) == [0, 1, 2, 3], ("V6-not-permutation", row)
        inv = [0] * 4
        for q, f in enumerate(row):
            inv[f] = q
        INV.append(tuple(inv))
    CONE90 = tuple(tuple(INV[_swap(l)][r] for r in range(4)) for l in range(4))
    # F1 as stated?
    f1_fail = 0
    for l in range(4):
        for r in range(4):
            t = CONE90[l][r]
            if H(t) != (H(r) + 1 + (1 if l == 0 else 0)) & 1 or E(t) != (E(r) + H(r) * (1 if Lo(l) == 0 else 0)) & 1:
                f1_fail += 1
    # affinity of CONE90 in the 4 input bits (H(l), Lo(l), H(r), Lo(r)) over GF(2)
    def bits(t):
        return (t >> 1, t & 1)
    affine = True
    for out in (0, 1):
        # fit affine form on the 16 points; check exactness
        vals = {}
        for l in range(4):
            for r in range(4):
                vals[bits(l) + bits(r)] = bits(CONE90[l][r])[out]
        c0 = vals[(0, 0, 0, 0)]
        coef = [vals[tuple(1 if i == k else 0 for i in range(4))] ^ c0 for k in range(4)]
        for x, y in vals.items():
            pred = c0 ^ sum(coef[k] & x[k] for k in range(4)) % 2
            if pred != y:
                affine = False
    print(f"  V6 Rule 90 analogue kernel (OR -> XOR): F1 as stated fails on {f1_fail} of 16 pairs; "
          f"CONE90 affine over GF(2) in the four input bits: {affine}", file=log, flush=True)
    # the analogous lemma: column u on [-u-1, n] is affine in (window bits, e_u); forced symbol exists
    # and is unique for H(T[u][n]) = 1 iff the coefficient of H(e_u) in H(T[u][n]) is 1.
    # Check by direct computation on all binary prefixes u <= ub: uniqueness of the forced symbol.
    unique = 0
    nonunique = 0
    for u in range(1, min(ub, 10) + 1):
        for word in product((1, 2), repeat=u):
            T = tri(word, CONE90)
            prev = T[u - 1]
            for n in range(1, u + 1):
                win = [prev[d] for d in range(-u, n)]
                found = [s for s in (1, 2) if H(col_from_window(win, s, CONE90)[-1]) == 1]
                if len(found) == 1:
                    unique += 1
                else:
                    nonunique += 1
    print(f"  V6 Rule 90 analogue: forced symbol unique on {unique} (word, n) pairs, not unique on {nonunique}; "
          f"whatever the count, the analogous statement is an identity between adjacent columns and "
          f"constrains no periodicity, exactly as the lemma does not", file=log, flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ub", type=int, default=12)
    ap.add_argument("--m", type=int, default=10)
    ap.add_argument("--fib-n", type=int, default=9)
    args = ap.parse_args()
    log = sys.stdout
    t0 = time.time()
    print(f"verify_rbf_obstruction.py args={vars(args)}", file=log, flush=True)
    v0_table()
    print("V0 F1 rebuilds CONE cell by cell on all 16 pairs; BOUNDARY[s] = s^3 = CONE[3][s] PASS", file=log, flush=True)
    st = v1_identities(args.ub, log)
    print(f"V1 (a)(b)(c)(d1)(d3)(d5) on {st['pairs']} (word, n) pairs, binary u<={args.ub}, n<=u; "
          f"{st['keys']} pair keys, one column and one (e_(u+1), Z_(u+1)) each; "
          f"odd-indexed flips invisible on the whole column [-u-1,u]: {st['odd_flips']} "
          f"(top cell nonzero in {st['top_nonzero']} windows, its flip invisible in {st['top_flips']}); "
          f"even-indexed flips change T[u][n]: {st['even_flips']} PASS   [{time.time()-t0:.0f}s]", file=log, flush=True)
    v2_balance(args.m, log)
    print(f"V2 (e) N0 = (3^m+1)/2, involution flips Phi on N>=2, N<=1 census, m<={args.m} PASS   [{time.time()-t0:.0f}s]", file=log, flush=True)
    c = v3_psi_tie(args.ub, log)
    print(f"V3 forced continuation and hit word equal psi_kernel.psi on {c} sources n<={args.ub} PASS   [{time.time()-t0:.0f}s]", file=log, flush=True)
    v4_small_n(log)
    print(f"V4 small-n sanity PASS   [{time.time()-t0:.0f}s]", file=log, flush=True)
    v5_fibres(args.fib_n, log)
    print(f"V5 fibres and lossless pairs, n<={args.fib_n} PASS   [{time.time()-t0:.0f}s]", file=log, flush=True)
    v6_rule90(args.ub, log)
    print(f"V6 Rule 90 transport DONE   [{time.time()-t0:.0f}s]", file=log, flush=True)
    print(f"ALL PASS   [{time.time()-t0:.0f}s]", file=log, flush=True)


if __name__ == "__main__":
    main()

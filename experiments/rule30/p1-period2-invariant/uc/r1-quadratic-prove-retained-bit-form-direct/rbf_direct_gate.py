#!/usr/bin/env python3
"""Bookkeeping gates for the direct proof of lemma "retained-bit-form" (PROOF.md, same dir).

The proof is a derivation from the local rule phi = psi_kernel.CONE.  These gates check
the finitely many facts the derivation consumes, and re-check the derived statements on
a triangle built here from the BRIEF section 2 recursion (own implementation, not the
kernel's Endpoint), so that an index slip in the write-up would fire an assertion.

  G0  local facts: decoupling of phi on all 16 pairs; BOUNDARY[s] = s XOR 3;
      E(s XOR 3) = E(s); E(1) = E(2) = 0; rows CONE[1] and CONE[3] coincide.
  G1  the triangle built here equals psi_kernel.Endpoint's columns (binary words, u <= GN).
  P   binary prefixes, exhaustive u <= U, every n <= u, and random at larger n:
      forcing unique; (a); (b); (c) and its set form; (d) run structure, even-bit
      read-out, pair (Z_{u-1}, Z_u) -> column u on [-u-1, n] plus FUT forced future steps.
  L   letter space {0,1,2}^m, m <= M3, and {0,1,2,3}^m, m <= M4, bottom letter free
      (relaxed): Moore prediction equals the phi recursion; (b) (c) (d); odd-indexed
      nonzero cells replaceable by any of 1, 2, 3 without changing column u; for each
      zero pattern the attainable Z_u are exactly 2^floor(N/2) and each (Z_{u-1}, Z_u)
      fibre in {0,1,2}^m has exactly 2^ceil(N/2) elements.
  E   relaxed balance: brute force m <= MB with the by-N decomposition of PROOF.md
      section 6; transfer matrix m <= MT with characteristic polynomial
      (x-1)(x-3)(x+1)^2; bottom-nonzero count 3^(m-1) - 1 + 2[m odd].

Run:  cd <work dir> && uv run python uc/r1-quadratic-prove-retained-bit-form-direct/rbf_direct_gate.py
"""
from __future__ import annotations

import argparse
import os
import random
import sys
import time
from fractions import Fraction
from itertools import product

WORK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, WORK)

from psi_kernel import BOUNDARY, CONE, Endpoint  # noqa: E402


def H(t: int) -> int:
    return t >> 1


def Lo(t: int) -> int:
    return t & 1


def E(t: int) -> int:
    return (1 + (t >> 1) + (t & 1)) & 1


# ----------------------------------------------------------------------------
# the triangle of BRIEF section 2, built from the recursion as written there
# ----------------------------------------------------------------------------

def next_column(prev: dict[int, int] | None, e: int, u: int) -> dict[int, int]:
    """Column u on d in [-u-1, u] from column u-1 (on [-u, u-1]) and endpoint symbol e."""
    col = {-u - 1: e, -u: e ^ 3}
    for d in range(-u + 1, u + 1):
        col[d] = CONE[prev[d - 1]][col[d - 1]]
    return col


def triangle(word) -> list[dict[int, int]]:
    cols: list[dict[int, int]] = []
    prev = None
    for u, e in enumerate(word):
        prev = next_column(prev, e, u)
        cols.append(prev)
    return cols


def column_of_endpoint(ep: Endpoint) -> dict[int, int]:
    col = {}
    for i, t in enumerate(ep.column):
        col[-i] = t
    for k, t in enumerate(ep.diagonal):
        col[k] = t
    return col


# ----------------------------------------------------------------------------
# retained structure of a window (PROOF.md section 2 definitions)
# ----------------------------------------------------------------------------

def analyse(cells: dict[int, int], lo: int, hi: int):
    """Window d in [lo, hi).  Returns qs (nonzero depths, top first), retained[d],
    runs R_i (i odd) as lists of depths top first, retained-zero count, w list."""
    qs = [d for d in range(hi - 1, lo - 1, -1) if cells[d] != 0]
    retained: dict[int, bool] = {}
    for i, d in enumerate(qs, start=1):
        retained[d] = (i % 2 == 0)
    above = True
    for d in range(hi - 1, lo - 1, -1):
        if cells[d] != 0:
            above = retained[d]
        else:
            retained[d] = above
    runs: list[list[int]] = []
    cur: list[int] = []
    for d in range(hi - 1, lo - 1, -1):
        if not retained[d]:
            cur.append(d)
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    ret_zero = sum(1 for d in range(lo, hi) if cells[d] == 0 and retained[d])
    w = [1 if cells[d] == 2 else 0 for d in qs]
    return qs, retained, runs, ret_zero, w


def set_form(cells: dict[int, int], lo: int, hi: int) -> int:
    m = hi - lo
    Z = sum(1 for d in range(lo, hi) if cells[d] == 0)
    W2 = sum(1 for d in range(lo, hi) if cells[d] == 2)
    pairs = 0
    nz_below = 0
    for d in range(lo, hi):
        t = cells[d]
        if t in (0, 2):
            pairs += nz_below
        if t != 0:
            nz_below += 1
    return ((Z + W2) * (1 + m + Z) + pairs) & 1


def moore(cells: dict[int, int], lo: int, hi: int, e: int) -> dict[int, int]:
    """Column u on [-u-1, n] predicted by the Moore machine (PROOF.md section 3)."""
    h, F = 1 ^ H(e), 0
    col = {lo - 1: e}
    for d in range(lo, hi):
        col[d] = 2 * h + ((1 + h + F) & 1)
        t = cells[d]
        a = 1 if t == 0 else 0
        b = 1 if t in (0, 2) else 0
        h, F = h ^ 1 ^ a, F ^ (h & b)
    col[hi] = 2 * h + ((1 + h + F) & 1)
    return col


def check_window(prev: dict[int, int], cur: dict[int, int], e_u: int, lo: int, hi: int, ctx):
    """All of (a)-(d) on one (window, column u) pair.  Returns (Z_prev, Z_cur, even w tuple)."""
    qs, retained, runs, ret_zero, w = analyse(prev, lo, hi)
    N = len(qs)
    m = hi - lo
    Z = m - N
    # (a) with the forced-symbol formula H(e_u) = m + |Z| = N (mod 2)
    assert H(e_u) == (m + Z) & 1 == N & 1, ("a", ctx, e_u, N)
    # (b)
    for d in range(lo, hi):
        assert H(cur[d]) == (1 if retained[d] else 0), ("b", ctx, d)
    assert H(cur[hi]) == 1, ("b-top", ctx)
    # (c) and the set form derived from it
    even_two = sum(w[i - 1] for i in range(2, N + 1, 2))
    pred = (ret_zero + even_two) & 1
    assert pred == E(cur[hi]), ("c", ctx, pred, E(cur[hi]))
    assert pred == set_form(prev, lo, hi), ("c-setform", ctx)
    # (d) runs are exactly (q_{i+1}, q_i] for odd i
    expect_runs = []
    for i in range(1, N + 1, 2):
        top = qs[i - 1]
        bot = qs[i] + 1 if i < N else lo
        expect_runs.append(list(range(top, bot - 1, -1)))
    assert runs == expect_runs, ("d-runs", ctx, runs, expect_runs)
    assert cur[lo - 1] != 0, ("d-bottom", ctx)
    Zu = {d for d in range(lo - 1, hi) if cur[d] == 0}
    for run in runs:
        inside = [d in Zu for d in run]
        assert all(inside) or not any(inside), ("d-partial", ctx, run)
    covered = {d for run in runs for d in run}
    assert Zu <= covered, ("d-outside", ctx, Zu - covered)
    # F_i on run i (i odd) equals [run in Z_u]; the retained cells have h = 1
    run_F = [1 if run[0] in Zu else 0 for run in runs]
    # (d) read-out w_i = F_{i-1} + F_{i+1} + z_i for even i, F_{N+1} := 0
    for k in range(len(runs)):
        i = 2 * k + 2
        if i > N:
            break
        q = qs[i - 1]
        q_next = qs[i] if i < N else lo - 1
        z_i = sum(1 for d in range(q_next + 1, q) if prev[d] == 0)
        F_above = run_F[k]
        F_below = run_F[k + 1] if k + 1 < len(runs) else 0
        assert ((F_above + F_below + z_i) & 1) == w[i - 1], ("d-readout", ctx, i)
    Zp = tuple(d for d in range(lo, hi) if prev[d] == 0)
    return Zp, tuple(sorted(Zu)), tuple(w[i - 1] for i in range(2, N + 1, 2))


# ----------------------------------------------------------------------------
# G0, G1
# ----------------------------------------------------------------------------

def gate_local(log) -> None:
    for l in range(4):
        for r in range(4):
            t = CONE[l][r]
            assert H(t) == (H(r) + 1 + (1 if l == 0 else 0)) & 1, ("G0-H", l, r)
            assert E(t) == (E(r) + H(r) * (1 if Lo(l) == 0 else 0)) & 1, ("G0-E", l, r)
    assert all(BOUNDARY[s] == s ^ 3 for s in range(4)), "G0-boundary"
    assert all(E(s ^ 3) == E(s) for s in range(4)), "G0-E-xor3"
    assert E(1) == 0 and E(2) == 0 and E(0) == 1 and E(3) == 1, "G0-E-values"
    assert CONE[1] == CONE[3], "G0-rows-1-3"
    assert all(len(set(CONE[l])) == 4 for l in range(4)), "G0-right-bijective"
    print("G0 local facts: decoupling on 16 pairs, BOUNDARY = XOR 3, E(XOR 3) = E, E(1)=E(2)=0, "
          "CONE[1] = CONE[3], right-bijective: PASS", file=log, flush=True)


def gate_kernel(gn: int, log) -> None:
    checked = 0
    for u in range(1, gn + 1):
        for word in product((1, 2), repeat=u):
            cols = triangle(word)
            ep = Endpoint()
            for s in word:
                ep.append(s)
            ref = column_of_endpoint(ep)
            mine = {d: cols[u - 1][d] for d in range(-u, u)}
            assert mine == ref, ("G1", word)
            assert cols[u - 1][-u] == word[-1], ("G1-edge", word)
            checked += 1
    print(f"G1 own triangle = psi_kernel.Endpoint on {checked} binary words, u <= {gn}: PASS",
          file=log, flush=True)


# ----------------------------------------------------------------------------
# P: binary prefixes
# ----------------------------------------------------------------------------

def forced(prev: dict[int, int], u: int, n: int) -> tuple[int, dict[int, int]]:
    found = []
    for e in (1, 2):
        col = next_column(prev, e, u)
        if H(col[n]) == 1:
            found.append((e, col))
    assert len(found) == 1, ("forcing-not-unique", u, n, [f[0] for f in found])
    return found[0]


def forced_future(prev: dict[int, int], u: int, n: int, steps: int) -> tuple:
    out = []
    for v in range(u, u + steps):
        e, col = forced(prev, v, n)
        out.append((e, col[n]))
        prev = col
    return tuple(out)


def run_prefixes(umax: int, fut: int, log) -> None:
    t0 = time.time()
    pairs = 0
    pair_map: dict = {}
    single: dict = {}
    for u in range(1, umax + 1):
        for word in product((1, 2), repeat=u):
            cols = triangle(word)
            prev = cols[u - 1]
            for n in range(1, u + 1):
                e_u, cur = forced(prev, u, n)
                Zp, Zu, weven = check_window(prev, cur, e_u, -u, n, (word, n))
                colkey = tuple(cur[d] for d in range(-u - 1, n + 1))
                future = forced_future(cur, u + 1, n, fut)
                key = (n, u, Zp, Zu)
                val = (colkey, weven, future)
                assert pair_map.setdefault(key, val) == val, ("d-pair", word, n, key)
                single.setdefault((n, u, Zp), set()).add(colkey)
                pairs += 1
        print(f"  P u={u:<3} pairs so far={pairs}   [{time.time()-t0:.0f}s]", file=log, flush=True)
    amb = sum(1 for v in single.values() if len(v) > 1)
    worst = max(len(v) for v in single.values())
    print(f"P exhaustive: all binary words u <= {umax}, all n <= u: {pairs} (word, n) pairs; forcing unique; "
          f"(a) (b) (c) (c-setform) (d-runs) (d-readout) (d-pair with {fut} future steps) PASS; "
          f"{len(pair_map)} distinct (n,u,Z_(u-1),Z_u) keys; Z_(u-1) alone {len(single)} keys, "
          f"{amb} ambiguous, max fibre {worst}", file=log, flush=True)


def run_random(ns: list[int], samples: int, seed: int, fut: int, log) -> None:
    rng = random.Random(seed)
    for n in ns:
        t0 = time.time()
        pairs = 0
        pair_map: dict = {}
        for _ in range(samples):
            word = [rng.choice((1, 2)) for _ in range(2 * n + 2)]
            cols = triangle(word)
            for u in range(n, 2 * n + 2):
                prev = cols[u - 1]
                e_u, cur = forced(prev, u, n)
                Zp, Zu, weven = check_window(prev, cur, e_u, -u, n, ("rand", n, tuple(word), u))
                colkey = tuple(cur[d] for d in range(-u - 1, n + 1))
                future = forced_future(cur, u + 1, n, fut)
                key = (n, u, Zp, Zu)
                val = (colkey, weven, future)
                assert pair_map.setdefault(key, val) == val, ("d-pair", n, u, tuple(word))
                pairs += 1
        print(f"P random n={n}: {samples} words, u in [n, 2n+1], {pairs} (word, u) pairs, all checks PASS; "
              f"{len(pair_map)} distinct pair keys   [{time.time()-t0:.0f}s]", file=log, flush=True)


# ----------------------------------------------------------------------------
# L: letter space (relaxed windows, bottom letter free)
# ----------------------------------------------------------------------------

def column_from_window(cells: list[int]) -> tuple[int, dict[int, int]]:
    """Window as list, index 0 = bottom (d = lo), forced e_u; column on [lo-1, hi]."""
    m = len(cells)
    lo, hi = 0, m
    prev = {d: cells[d] for d in range(m)}
    found = []
    for e in (1, 2):
        col = {lo - 1: e, lo: e ^ 3}
        for d in range(lo + 1, hi + 1):
            col[d] = CONE[prev[d - 1]][col[d - 1]]
        if H(col[hi]) == 1:
            found.append((e, col))
    assert len(found) == 1, ("L-forcing", cells)
    return found[0]


def run_letters(m3: int, m4: int, log) -> None:
    t0 = time.time()
    words3 = 0
    for m in range(1, m3 + 1):
        by_pattern: dict = {}
        fibre: dict = {}
        for cells in product((0, 1, 2), repeat=m):
            cells = list(cells)
            prev = {d: cells[d] for d in range(m)}
            e_u, col = column_from_window(cells)
            assert col == moore(prev, 0, m, e_u), ("L-moore", cells)
            Zp, Zu, weven = check_window(prev, col, e_u, 0, m, ("L3", tuple(cells)))
            colkey = tuple(col[d] for d in range(-1, m + 1))
            by_pattern.setdefault(Zp, {}).setdefault(Zu, set()).add(colkey)
            fibre[(Zp, Zu)] = fibre.get((Zp, Zu), 0) + 1
            # odd-indexed nonzero cells are never read: replace each by every nonzero value
            qs = [d for d in range(m - 1, -1, -1) if cells[d] != 0]
            for idx, d in enumerate(qs, start=1):
                for v in (1, 2, 3):
                    if v == cells[d]:
                        continue
                    alt = cells[:]
                    alt[d] = v
                    e2, col2 = column_from_window(alt)
                    if idx % 2 == 1:
                        assert (e2, col2) == (e_u, col), ("L-odd-read", cells, d, v)
                    elif v != 3:
                        assert (e2, col2) != (e_u, col), ("L-even-blind", cells, d, v)
                    else:
                        # 3 is the same letter as 1 in the quotient
                        assert ((e2, col2) == (e_u, col)) == (cells[d] == 1), ("L-3-vs-1", cells, d)
            words3 += 1
        for Zp, images in by_pattern.items():
            N = m - len(Zp)
            assert len(images) == 2 ** (N // 2), ("L-image-count", m, Zp, len(images))
            for Zu, colkeys in images.items():
                assert len(colkeys) == 1, ("L-pair-not-function", m, Zp, Zu)
                assert fibre[(Zp, Zu)] == 2 ** ((N + 1) // 2), ("L-fibre", m, Zp, Zu, fibre[(Zp, Zu)])
        print(f"  L3 m={m:<3} words={3**m}   [{time.time()-t0:.0f}s]", file=log, flush=True)
    words4 = 0
    for m in range(1, m4 + 1):
        for cells in product((0, 1, 2, 3), repeat=m):
            cells = list(cells)
            prev = {d: cells[d] for d in range(m)}
            e_u, col = column_from_window(cells)
            assert col == moore(prev, 0, m, e_u), ("L4-moore", cells)
            check_window(prev, col, e_u, 0, m, ("L4", tuple(cells)))
            words4 += 1
    print(f"L letter space: {words3} windows in {{0,1,2}}^m, m <= {m3}: Moore = phi recursion, (a)-(d), "
          f"odd cells unread, even cells read, image 2^floor(N/2), fibre 2^ceil(N/2) PASS; "
          f"{words4} windows in {{0..3}}^m, m <= {m4}: Moore = phi, (a)-(d) PASS   [{time.time()-t0:.0f}s]",
          file=log, flush=True)


# ----------------------------------------------------------------------------
# E: relaxed balance
# ----------------------------------------------------------------------------

def phi_letters(word: list[int]) -> int:
    nonzero = sum(1 for t in word if t != 0)
    h = (1 + nonzero) & 1
    F = 0
    for t in word:
        a = 1 if t == 0 else 0
        b = 1 if t in (0, 2) else 0
        F ^= h & b
        h ^= 1 ^ a
    assert h == 1
    return F


def charpoly(M):
    n = len(M)
    I = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    Mf = [[Fraction(x) for x in row] for row in M]
    coeffs = [Fraction(1)]
    Nm = [[Fraction(0)] * n for _ in range(n)]
    for k in range(1, n + 1):
        X = [[Nm[i][j] + coeffs[-1] * I[i][j] for j in range(n)] for i in range(n)]
        Nm = [[sum(Mf[i][t] * X[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
        coeffs.append(-sum(Nm[i][i] for i in range(n)) / k)
    return [int(c) for c in coeffs]


def run_balance(mb: int, mt: int, log) -> None:
    t0 = time.time()
    for m in range(1, mb + 1):
        zeros = 0
        by_N: dict[int, list[int]] = {}
        bottom_nonzero_zeros = 0
        per_pattern: dict = {}
        for wd in product((0, 1, 2), repeat=m):
            wd = list(wd)
            f = phi_letters(wd)
            # cross-check Phi against the phi recursion itself
            _, col = column_from_window(wd)
            assert f == E(col[m]), ("E-phi-vs-kernel", wd)
            N = sum(1 for t in wd if t != 0)
            by_N.setdefault(N, [0, 0])[f] += 1
            pat = tuple(d for d in range(m) if wd[d] == 0)
            per_pattern.setdefault(pat, [0, 0])[f] += 1
            if f == 0:
                zeros += 1
                if wd[0] != 0:
                    bottom_nonzero_zeros += 1
        assert zeros == (3 ** m + 1) // 2, ("E-total", m, zeros)
        # decomposition by N (PROOF.md section 6)
        for N, (z0, z1) in by_N.items():
            if N >= 2:
                assert z0 == z1, ("E-N>=2-balanced", m, N, z0, z1)
            elif N == 1:
                assert z0 == 2 * ((m + 1) // 2) and z0 + z1 == 2 * m, ("E-N=1", m, z0, z1)
            else:
                assert z0 + z1 == 1 and z0 == (1 if m % 2 == 0 else 0), ("E-N=0", m, z0)
        for pat, (z0, z1) in per_pattern.items():
            N = m - len(pat)
            if N >= 2:
                assert z0 == z1 == 2 ** (N - 1), ("E-pattern", m, pat, z0, z1)
        assert bottom_nonzero_zeros == 3 ** (m - 1) - 1 + 2 * (m % 2), ("E-bottom-nonzero", m, bottom_nonzero_zeros)
        print(f"  E m={m:<3} #Phi=0={zeros} = (3^m+1)/2; by-N decomposition PASS; bottom-nonzero zeros={bottom_nonzero_zeros}",
              file=log, flush=True)
    # transfer matrix
    states = [(0, 0), (0, 1), (1, 0), (1, 1)]
    letters = [(0, 0), (0, 1), (1, 1)]
    A = [[0] * 4 for _ in range(4)]
    for i, (h, F) in enumerate(states):
        for a, b in letters:
            A[i][states.index((h ^ 1 ^ a, F ^ (h & b)))] += 1
    p = charpoly(A)
    assert p == [1, -2, -4, 2, 3], ("E-charpoly", p)
    # (x-1)(x-3)(x+1)^2 = x^4 - 2x^3 - 4x^2 + 2x + 3
    prod = [1]
    for root in (1, 3, -1, -1):
        padded = prod + [0]
        prod = [padded[i] - root * (padded[i - 1] if i >= 1 else 0) for i in range(len(padded))]
    assert prod == p, ("E-factorisation", prod, p)
    P = [[int(i == j) for j in range(4)] for i in range(4)]
    for m in range(1, mt + 1):
        P = [[sum(P[i][k] * A[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
        N0 = sum(P[states.index((h0, 0))][states.index((1, 0))] for h0 in (0, 1))
        N1 = sum(P[states.index((h0, 0))][states.index((1, 1))] for h0 in (0, 1))
        assert N0 + N1 == 3 ** m and N0 - N1 == 1, ("E-transfer", m, N0, N1)
    print(f"E balance: brute force m <= {mb} through phi with the by-N decomposition PASS; transfer matrix "
          f"charpoly {p} = (x-1)(x-3)(x+1)^2, d(m) = 1 for m <= {mt} PASS   [{time.time()-t0:.0f}s]",
          file=log, flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gate-n", type=int, default=10)
    ap.add_argument("--umax", type=int, default=12)
    ap.add_argument("--fut", type=int, default=3)
    ap.add_argument("--rand-n", type=int, nargs="*", default=[30, 60, 100])
    ap.add_argument("--samples", type=int, default=200)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--letters-m3", type=int, default=10)
    ap.add_argument("--letters-m4", type=int, default=8)
    ap.add_argument("--balance-brute", type=int, default=10)
    ap.add_argument("--balance-transfer", type=int, default=60)
    ap.add_argument("--skip", nargs="*", default=[])
    args = ap.parse_args()
    log = sys.stdout
    print(f"rbf_direct_gate.py args={vars(args)}", file=log, flush=True)
    t0 = time.time()
    gate_local(log)
    gate_kernel(args.gate_n, log)
    if "P" not in args.skip:
        run_prefixes(args.umax, args.fut, log)
        run_random(args.rand_n, args.samples, args.seed, args.fut, log)
    if "L" not in args.skip:
        run_letters(args.letters_m3, args.letters_m4, log)
    if "E" not in args.skip:
        run_balance(args.balance_brute, args.balance_transfer, log)
    print(f"ALL PASS   [{time.time()-t0:.0f}s]", file=log, flush=True)


if __name__ == "__main__":
    main()

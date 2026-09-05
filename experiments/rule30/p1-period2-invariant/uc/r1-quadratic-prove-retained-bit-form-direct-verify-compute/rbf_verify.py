#!/usr/bin/env python3
"""Independent adversarial re-check of lemma retained-bit-form (COMPUTE lens).

Own code throughout; nothing is imported from rbf_direct_gate.py or the q2_* scripts.
Only psi_kernel.CONE, psi_kernel.BOUNDARY and psi_kernel.Endpoint are used, i.e. the
kernel the BRIEF names as the rule.  Everything is checked against the LITERAL wording
of the lemma (q_i listing, nearest nonzero above), and separately against the
count characterisation used in the proof, so that a slip in either would fire.

Sections (each prints PASS lines; any assertion aborts with a witness tuple):

  F    (F1) (F2) (F3) on the 16 pairs and 4 boundary values, own code; CONE printed.
  K    psi_kernel.Endpoint column u restricted to [-u-1, n] equals the window
       recursion of BRIEF section 2 applied to column u-1 on [-u, n-1]  (Lemma 1).
  A    structured binary prefixes and forced orbits at n far beyond the screened
       range (n up to 1000): (a) (b) (c) (c-primed form) (d) run structure,
       read-out, constructive rebuild of column u from (Z_{u-1}, Z_u) alone,
       forced future rebuilt from the pair for FUT steps, odd-bit blindness and
       even-bit visibility (sampled for large m).
  B    letter-space windows in {0,1,2,3}^m with free bottom letter, structured
       families and biased random, m up to 2000: same checks.
  C51  Corollary 5.1 as displayed in PROOF.md versus the corrected display.
  E    balance (e): brute force through the CONE recursion for m <= MB (own code),
       per-pattern balance for N >= 2, exact d(m) = 1 via integer matrix powers of
       an own-built transfer matrix to m <= MT, characteristic polynomial by own
       Faddeev-LeVerrier, and the bottom-nonzero count of Remark 12.2.

Run: cd <work dir> && uv run python uc/r1-quadratic-prove-retained-bit-form-direct-verify-compute/rbf_verify.py
"""
from __future__ import annotations

import argparse
import os
import random
import sys
import time
from bisect import bisect_right
from fractions import Fraction
from itertools import product

WORK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, WORK)

from psi_kernel import BOUNDARY, CONE, Endpoint  # noqa: E402

T0 = time.time()


def H(t: int) -> int:
    return t >> 1


def Lo(t: int) -> int:
    return t & 1


def E(t: int) -> int:
    return (1 + (t >> 1) + (t & 1)) & 1


def say(msg: str) -> None:
    print(f"{msg}   [{time.time()-T0:.0f}s]", flush=True)


# ----------------------------------------------------------------------------- F
def section_F() -> None:
    print("CONE[l][r] rows l=0..3:", [list(CONE[l]) for l in range(4)])
    print("BOUNDARY:", list(BOUNDARY))
    for l in range(4):
        for r in range(4):
            t = CONE[l][r]
            assert H(t) == (H(r) + 1 + (1 if l == 0 else 0)) % 2, ("F1", l, r, t)
            assert E(t) == (E(r) + H(r) * (1 if Lo(l) == 0 else 0)) % 2, ("F2", l, r, t)
    for s in range(4):
        assert BOUNDARY[s] == s ^ 3, ("F3", s)
        assert E(s ^ 3) == E(s), ("C2", s)
    assert E(1) == 0 and E(2) == 0 and E(0) == 1 and E(3) == 1, "C3"
    # T = 0 iff (H, E) = (0, 1)
    for t in range(4):
        assert (t == 0) == ((H(t), E(t)) == (0, 1)), ("C1", t)
    say("F  (F1) (F2) (F3) (C1) (C2) (C3) on all 16 pairs / 4 values: PASS")


# ----------------------------------------------------------------- window tools
def window_column(win: dict[int, int], lo: int, hi: int, e: int) -> dict[int, int]:
    """Column u on [lo-1, hi] from window win on [lo, hi) and symbol e (BRIEF section 2)."""
    col = {lo - 1: e, lo: e ^ 3}
    for d in range(lo + 1, hi + 1):
        col[d] = CONE[win[d - 1]][col[d - 1]]
    return col


def forced_from_window(win: dict[int, int], lo: int, hi: int) -> tuple[int, dict[int, int]]:
    hits = []
    for e in (1, 2):
        col = window_column(win, lo, hi, e)
        if H(col[hi]) == 1:
            hits.append((e, col))
    assert len(hits) == 1, ("forcing-not-unique", lo, hi, [h[0] for h in hits])
    return hits[0]


def literal_retained(win: dict[int, int], lo: int, hi: int):
    """The lemma's wording, verbatim.  Returns qs (top first), idx, retained dict."""
    qs = [d for d in range(hi - 1, lo - 1, -1) if win[d] != 0]
    idx = {d: i for i, d in enumerate(qs, start=1)}
    asc = qs[::-1]  # ascending depths of nonzero cells
    ret = {}
    for d in range(lo, hi):
        if win[d] != 0:
            ret[d] = (idx[d] % 2 == 0)
        else:
            j = bisect_right(asc, d)  # first nonzero depth strictly above d
            if j == len(asc):
                ret[d] = True
            else:
                ret[d] = (idx[asc[j]] % 2 == 0)
    return qs, idx, ret


def count_retained(win: dict[int, int], lo: int, hi: int) -> dict[int, bool]:
    """Proof's characterisation: retained iff #{nonzero at depth >= d} is even."""
    ret = {}
    c = 0
    for d in range(hi - 1, lo - 1, -1):
        if win[d] != 0:
            c += 1
        ret[d] = (c % 2 == 0)
    return ret


def primed_form(win: dict[int, int], lo: int, hi: int) -> int:
    """BRIEF section 3 primed form: beta (1 + alpha') + gamma'."""
    alpha = 0
    beta = 0
    gamma = 0
    nz_below = 0
    for d in range(lo, hi):
        t = win[d]
        ap = 1 if t != 0 else 0
        b = 1 if t in (0, 2) else 0
        alpha += ap
        beta += b
        gamma += nz_below * b
        nz_below += ap
    return (beta * (1 + alpha) + gamma) & 1


def maximal_runs(pred: dict[int, bool], lo: int, hi: int) -> list[tuple[int, int]]:
    """Maximal intervals [s, t] (ascending) on which pred is False."""
    runs = []
    d = lo
    while d < hi:
        if not pred[d]:
            s = d
            while d + 1 < hi and not pred[d + 1]:
                d += 1
            runs.append((s, d))
        d += 1
    return runs


def rebuild_from_pair(lo: int, hi: int, Zprev: set[int], Zu: set[int]) -> tuple[int, dict[int, int]]:
    """Column u on [lo-1, hi] from (Z_{u-1}, Z_u) ALONE, by the lemma's recipe:
    N from Z, e_u from N parity, h from the count parity, even w_i from the
    read-out w_i = F_{i-1} + F_{i+1} + z_i, F(d) integrated, cell = 2h + (1+h+F)."""
    m = hi - lo
    nz = [d for d in range(hi - 1, lo - 1, -1) if d not in Zprev]  # top first
    N = len(nz)
    e = 2 if N % 2 == 1 else 1
    ret = count_retained({d: (0 if d in Zprev else 1) for d in range(lo, hi)}, lo, hi)
    # runs R_i (i odd) top first, and F_i = [R_i subset Z_u]
    runs = maximal_runs(ret, lo, hi)[::-1]  # top first
    F_run = [1 if (s in Zu) else 0 for (s, t) in runs]
    # even bits
    w = {}
    for k in range(len(runs)):
        i = 2 * k + 2
        if i > N:
            break
        q = nz[i - 1]
        q_next = nz[i] if i < N else lo - 1
        z_i = sum(1 for d in range(q_next + 1, q) if d in Zprev)
        F_above = F_run[k]
        F_below = F_run[k + 1] if k + 1 < len(runs) else 0
        w[q] = (F_above + F_below + z_i) & 1
    # integrate
    col = {lo - 1: e}
    F = 0
    for d in range(lo, hi + 1):
        h = 1 if (d == hi or ret[d]) else 0
        col[d] = 2 * h + ((1 + h + F) & 1)
        if d < hi and h == 1:
            if d in Zprev:
                F ^= 1
            else:
                F ^= w[d]
    return e, col


def check_window(win: dict[int, int], lo: int, hi: int, ctx, e_u: int, cur: dict[int, int],
                 odd_checks: int | None = None, rng: random.Random | None = None) -> tuple:
    """Every clause of (a)-(d) on one window.  cur = column u on [lo-1, hi]."""
    m = hi - lo
    qs, idx, ret = literal_retained(win, lo, hi)
    ret2 = count_retained(win, lo, hi)
    assert ret == ret2, ("retained-two-definitions", ctx)
    N = len(qs)
    Z = [d for d in range(lo, hi) if win[d] == 0]
    # forcing formula
    assert H(cur[hi]) == 1, ("forcing", ctx)
    assert H(e_u) == (m + len(Z)) % 2 == N % 2, ("a-formula", ctx)
    # (a)
    assert (e_u == 2) == (N % 2 == 1), ("a", ctx, e_u, N)
    # (b)
    for d in range(lo, hi):
        assert H(cur[d]) == (1 if ret[d] else 0), ("b", ctx, d)
    # (c) literal, and the BRIEF primed form
    ret_zero = sum(1 for d in Z if ret[d])
    even_two = sum(1 for d in qs if idx[d] % 2 == 0 and win[d] == 2)
    assert E(cur[hi]) == (ret_zero + even_two) % 2, ("c", ctx)
    assert E(cur[hi]) == primed_form(win, lo, hi), ("c-primed", ctx)
    # (d) zero set of column u on [lo-1, hi) is a union of complete maximal non-retained runs
    assert cur[lo - 1] != 0, ("d-bottom", ctx)
    Zu = {d for d in range(lo - 1, hi) if cur[d] == 0}
    runs = maximal_runs(ret, lo, hi)
    # runs are exactly (q_{i+1}, q_i] for odd i
    expect = []
    for i in range(1, N + 1, 2):
        top = qs[i - 1]
        bot = qs[i] + 1 if i < N else lo
        expect.append((bot, top))
    assert runs[::-1] == expect, ("d-runs", ctx, runs[::-1][:5], expect[:5])
    covered = set()
    for (s, t) in runs:
        inside = [d in Zu for d in range(s, t + 1)]
        assert all(inside) or not any(inside), ("d-partial-run", ctx, (s, t))
        covered.update(range(s, t + 1))
    assert Zu <= covered, ("d-zero-outside-runs", ctx, sorted(Zu - covered)[:5])
    # F constant on each run and equal to [run in Z_u]: check via E of column u cells
    for (s, t) in runs:
        vals = {E(cur[d]) for d in range(s, t + 1)}
        assert len(vals) == 1, ("d-F-not-constant-on-run", ctx, (s, t))
        assert (vals.pop() == 1) == (s in Zu), ("d-F-vs-Zu", ctx, (s, t))
    # read-out
    runs_top_first = runs[::-1]
    F_run = [1 if s in Zu else 0 for (s, t) in runs_top_first]
    for k in range(len(runs_top_first)):
        i = 2 * k + 2
        if i > N:
            break
        q = qs[i - 1]
        q_next = qs[i] if i < N else lo - 1
        z_i = sum(1 for d in range(q_next + 1, q) if win[d] == 0)
        F_above = F_run[k]
        F_below = F_run[k + 1] if k + 1 < len(runs_top_first) else 0
        w_i = 1 if win[q] == 2 else 0
        assert (F_above + F_below + z_i) % 2 == w_i, ("d-readout", ctx, i)
    # constructive rebuild of column u from (Z_{u-1}, Z_u) alone
    e_r, col_r = rebuild_from_pair(lo, hi, set(Z), Zu)
    assert e_r == e_u, ("d-rebuild-symbol", ctx)
    for d in range(lo - 1, hi + 1):
        assert col_r[d] == cur[d], ("d-rebuild-cell", ctx, d, col_r[d], cur[d])
    # odd bits never read; even bits always read (sampled when large)
    odd_cells = [d for d in qs if idx[d] % 2 == 1]
    even_cells = [d for d in qs if idx[d] % 2 == 0]
    if odd_checks is not None and rng is not None:
        odd_cells = rng.sample(odd_cells, min(odd_checks, len(odd_cells)))
        even_cells = rng.sample(even_cells, min(odd_checks, len(even_cells)))
    for d in odd_cells:
        for v in (1, 2, 3):
            if v == win[d]:
                continue
            alt = dict(win)
            alt[d] = v
            e2, col2 = forced_from_window(alt, lo, hi)
            assert e2 == e_u and all(col2[x] == cur[x] for x in range(lo - 1, hi + 1)), ("odd-bit-read", ctx, d, v)
    for d in even_cells:
        alt = dict(win)
        alt[d] = 2 if win[d] != 2 else 1
        e2, col2 = forced_from_window(alt, lo, hi)
        assert e2 == e_u, ("even-flip-changes-symbol", ctx, d)
        assert E(col2[hi]) != E(cur[hi]), ("even-bit-blind", ctx, d)
    return tuple(Z), tuple(sorted(Zu)), N


# ----------------------------------------------------------------------------- K, A
def column_of(ep: Endpoint) -> dict[int, int]:
    col = {}
    for i, t in enumerate(ep.column):
        col[-i] = t
    for k, t in enumerate(ep.diagonal):
        col[k] = t
    return col


def forced_symbol(ep: Endpoint, n: int) -> int:
    hits = [e for e in (1, 2) if H(ep.peek(e)[1][n]) == 1]
    assert len(hits) == 1, ("kernel-forcing-not-unique", ep.length, n, hits)
    return hits[0]


def structured_prefix(kind: str, n: int, rng: random.Random) -> list[int]:
    if kind == "rand":
        return [rng.choice((1, 2)) for _ in range(n)]
    if kind == "n15":
        n15 = [1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 2, 1, 1, 2]  # the recorded n = 15 falsifier source
        return (n15 * (n // 15 + 1))[:n]
    pat = {"ones": "1", "twos": "2", "12": "12", "21": "21", "112": "112", "122": "122",
           "1122": "1122", "2111": "2111", "1112": "1112", "211212112": "211212112",
           "12112": "12112", "2212": "2212"}[kind]
    return [int(pat[i % len(pat)]) for i in range(n)]


def section_A(ns: list[int], kinds: list[str], seed: int, fut: int, odd_checks: int, extra_depth: int) -> None:
    rng = random.Random(seed)
    total = 0
    for n in ns:
        t0 = time.time()
        cols = 0
        for kind in kinds:
            W = structured_prefix(kind, n, rng)
            ep = Endpoint()
            for s in W:
                ep.append(s)
            U = 2 * n + 1 + extra_depth
            hist: list[dict[int, int]] = []
            for u in range(n, U + 1):
                prev = column_of(ep)  # column u-1 on [-u, u-1]
                e_u = forced_symbol(ep, n)
                # K: kernel column u equals the window recursion (Lemma 1)
                win = {d: prev[d] for d in range(-u, n)}
                e_w, col_w = forced_from_window(win, -u, n)
                ep.append(e_u)
                cur = column_of(ep)
                assert e_w == e_u, ("K-symbol", kind, n, u)
                for d in range(-u - 1, n + 1):
                    assert col_w[d] == cur[d], ("K-cell", kind, n, u, d)
                curwin = {d: cur[d] for d in range(-u - 1, n + 1)}
                # the O(m^2) bit-replacement checks: full below n = 40, sampled cells above,
                # and only every STRIDE-th column above n = 200 (0 = skip on this column)
                stride = 1 if n <= 200 else 25
                oc = None if n <= 40 else (odd_checks if (u - n) % stride == 0 else 0)
                check_window(win, -u, n, (kind, n, u), e_u, curwin, odd_checks=oc, rng=rng)
                hist.append(curwin)
                cols += 1
            # forced future from the pair alone: rebuild column u from (Z_{u-1}, Z_u), then
            # iterate the window recursion with forcing FUT steps and compare with the kernel
            for k in range(1, len(hist) - fut, stride):
                u = n + k
                prevcol = hist[k - 1]
                Zprev = {d for d in range(-u, n) if prevcol[d] == 0}
                Zu = {d for d in range(-u - 1, n) if hist[k][d] == 0}
                e_r, col_r = rebuild_from_pair(-u, n, Zprev, Zu)
                assert all(col_r[d] == hist[k][d] for d in range(-u - 1, n + 1)), ("pair-rebuild", kind, n, u)
                # iterate forward
                col = col_r
                for step in range(1, fut + 1):
                    v = u + step
                    win = {d: col[d] for d in range(-v, n)}
                    e_v, col = forced_from_window(win, -v, n)
                    ref = hist[k + step]
                    assert e_v == ref[-v - 1], ("future-symbol", kind, n, u, step)
                    assert all(col[d] == ref[d] for d in range(-v - 1, n + 1)), ("future-cell", kind, n, u, step)
            total += cols
        say(f"A  n={n}: kinds={len(kinds)}, columns u in [n, {2*n+1+extra_depth}], {cols} columns checked, "
             f"(a)-(d), Lemma 1, pair rebuild, {fut}-step future from the pair, odd/even bits: PASS  ({time.time()-t0:.0f}s)")
    say(f"A  total columns checked: {total}")


# ----------------------------------------------------------------------------- B
def letter_family(kind: str, m: int, rng: random.Random) -> list[int]:
    if kind.startswith("rand"):
        p = float(kind.split(":")[1])
        return [0 if rng.random() < p else rng.choice((1, 2, 3)) for _ in range(m)]
    if kind == "zeros":
        return [0] * m
    if kind == "0^{m-1}2":
        return [0] * (m - 1) + [2]
    if kind == "2 0^{m-1}":
        return [2] + [0] * (m - 1)
    if kind == "0^{m-1}x":
        return [0] * (m - 1) + [1]
    if kind == "x 0^{m-1}":
        return [3] + [0] * (m - 1)
    if kind.startswith("gap:"):
        # (v 0^k)^* with v in {1,2,3}
        _, v, k = kind.split(":")
        v, k = int(v), int(k)
        pat = [v] + [0] * k
        return [pat[i % len(pat)] for i in range(m)]
    pat = [int(ch) for ch in kind]
    return [pat[i % len(pat)] for i in range(m)]


def section_B(ms: list[int], seed: int, odd_checks: int) -> None:
    rng = random.Random(seed)
    kinds = ["zeros", "1", "2", "3", "02", "20", "01", "10", "03", "30", "13", "31", "12", "21", "23",
             "002", "020", "200", "001", "010", "0002", "0020", "0123", "3210", "0220", "0110", "0213",
             "0^{m-1}2", "2 0^{m-1}", "0^{m-1}x", "x 0^{m-1}",
             "gap:2:2", "gap:2:3", "gap:1:2", "gap:3:5", "gap:2:7", "gap:1:11",
             "rand:0.02", "rand:0.1", "rand:0.3", "rand:0.5", "rand:0.7", "rand:0.9", "rand:0.98"]
    total = 0
    for m in ms:
        t0 = time.time()
        for kind in kinds:
            cells = letter_family(kind, m, rng)
            win = {d: cells[d] for d in range(m)}
            e_u, cur = forced_from_window(win, 0, m)
            check_window(win, 0, m, ("B", kind, m), e_u, cur,
                         odd_checks=(odd_checks if m > 40 else None), rng=rng)
            total += 1
        say(f"B  m={m}: {len(kinds)} structured/biased windows in {{0,1,2,3}}^m, free bottom letter: (a)-(d) PASS  ({time.time()-t0:.0f}s)")
    say(f"B  total windows: {total}")


# ----------------------------------------------------------------------------- C51
def section_C51() -> None:
    """Corollary 5.1 of PROOF.md displays  1 + h(d) + h(d+1) = [T[u-1][d] != 0].
    Test it, and the corrected display  1 + h(d) + h(d+1) = [T[u-1][d] == 0], on all
    binary words u <= 8 and all n <= u."""
    as_written_fail = 0
    corrected_fail = 0
    first = None
    cells = 0
    for u in range(1, 9):
        for word in product((1, 2), repeat=u):
            ep = Endpoint()
            for s in word:
                ep.append(s)
            prev = column_of(ep)
            for n in range(1, u + 1):
                e_u = forced_symbol(ep, n)
                ep2 = ep.clone()
                ep2.append(e_u)
                cur = column_of(ep2)
                for d in range(-u, n):
                    lhs = (1 + H(cur[d]) + H(cur[d + 1])) % 2
                    if lhs != (1 if prev[d] != 0 else 0):
                        as_written_fail += 1
                        if first is None:
                            first = (word, n, d, prev[d], H(cur[d]), H(cur[d + 1]))
                    if lhs != (1 if prev[d] == 0 else 0):
                        corrected_fail += 1
                    cells += 1
    print(f"C51 Corollary 5.1 as written (1+h(d)+h(d+1) = [T != 0]): {as_written_fail} of {cells} cells FAIL; "
          f"first witness (word, n, d, T[u-1][d], h(d), h(d+1)) = {first}")
    print(f"C51 corrected display (1+h(d)+h(d+1) = [T == 0]): {corrected_fail} of {cells} cells fail")
    assert corrected_fail == 0
    assert as_written_fail > 0
    say("C51 the display in Corollary 5.1 is off by a complement; the corrected form holds on all cells: RECORDED")


# ----------------------------------------------------------------------------- E
def phi_via_cone(word: list[int]) -> int:
    """Phi(q) with the forced start, computed through the CONE recursion, own code."""
    m = len(word)
    win = {d: word[d] for d in range(m)}
    e, col = forced_from_window(win, 0, m)
    return E(col[m])


def own_charpoly(M: list[list[int]]) -> list[int]:
    n = len(M)
    A = [[Fraction(x) for x in row] for row in M]
    c = [Fraction(1)]
    Bm = [[Fraction(0)] * n for _ in range(n)]
    for k in range(1, n + 1):
        for i in range(n):
            Bm[i][i] += c[-1]
        AB = [[sum(A[i][t] * Bm[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
        ck = -sum(AB[i][i] for i in range(n)) / k
        c.append(ck)
        Bm = AB
    return [int(x) for x in c]


def section_E(mb: int, mt: int) -> None:
    t0 = time.time()
    for m in range(1, mb + 1):
        zeros = 0
        bottom_nonzero_zeros = 0
        per_pattern: dict = {}
        for wd in product((0, 1, 2), repeat=m):
            wd = list(wd)
            f = phi_via_cone(wd)
            pat = tuple(d for d in range(m) if wd[d] == 0)
            per_pattern.setdefault(pat, [0, 0])[f] += 1
            if f == 0:
                zeros += 1
                if wd[0] != 0:
                    bottom_nonzero_zeros += 1
        assert 2 * zeros == 3 ** m + 1, ("E-total", m, zeros)
        for pat, (z0, z1) in per_pattern.items():
            N = m - len(pat)
            if N >= 2:
                assert z0 == z1 == 2 ** (N - 1), ("E-pattern", m, pat, z0, z1)
        assert bottom_nonzero_zeros == 3 ** (m - 1) - 1 + 2 * (m % 2), ("E-bottom", m, bottom_nonzero_zeros)
        print(f"   E m={m}: #Phi=0 = {zeros} = (3^m+1)/2; N>=2 patterns balanced; bottom-nonzero zeros = {bottom_nonzero_zeros}", flush=True)
    say(f"E  brute force through CONE for m <= {mb}: PASS")
    # own transfer matrix from the Moore step (h, F) -> (h+1+a, F + h b)
    states = [(0, 0), (0, 1), (1, 0), (1, 1)]
    A = [[0] * 4 for _ in range(4)]
    for i, (h, F) in enumerate(states):
        for (a, b) in ((0, 0), (0, 1), (1, 1)):
            j = states.index(((h + 1 + a) % 2, (F + h * b) % 2))
            A[i][j] += 1
    print("   transfer matrix rows:", A)
    cp = own_charpoly(A)
    print("   characteristic polynomial coefficients (x^4 ... 1):", cp)
    assert cp == [1, -2, -4, 2, 3], ("E-charpoly", cp)
    # evaluate at 1, 3, -1 and derivative at -1
    def ev(x):
        return sum(c * x ** (4 - i) for i, c in enumerate(cp))
    assert ev(1) == 0 and ev(3) == 0 and ev(-1) == 0, "E-roots"
    dcp = [(4 - i) * c for i, c in enumerate(cp[:-1])]
    assert sum(c * (-1) ** (3 - i) for i, c in enumerate(dcp)) == 0, "E-double-root"
    P = [[int(i == j) for j in range(4)] for i in range(4)]
    for m in range(1, mt + 1):
        P = [[sum(P[i][k] * A[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
        N0 = P[0][2] + P[2][2]  # from (0,0) and (1,0) to (1,0)
        N1 = P[0][3] + P[2][3]  # to (1,1)
        assert N0 + N1 == 3 ** m and N0 - N1 == 1, ("E-transfer", m, N0, N1)
    say(f"E  transfer matrix: d(m) = 1 exactly for all m <= {mt}: PASS")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ns", type=int, nargs="*", default=[13, 15, 17, 20, 24, 31, 32, 33, 47, 64, 65, 100, 127, 128, 200, 257, 300, 500, 1000])
    ap.add_argument("--ms", type=int, nargs="*", default=[13, 14, 15, 16, 20, 25, 33, 50, 64, 100, 128, 200, 500, 1000, 2000])
    ap.add_argument("--fut", type=int, default=6)
    ap.add_argument("--odd-checks", type=int, default=6)
    ap.add_argument("--extra-depth", type=int, default=4)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--balance-brute", type=int, default=13)
    ap.add_argument("--balance-transfer", type=int, default=3000)
    args = ap.parse_args()
    print("rbf_verify.py args:", vars(args), flush=True)
    section_F()
    section_C51()
    kinds = ["ones", "twos", "12", "21", "112", "122", "1122", "2111", "1112", "211212112", "12112", "2212", "n15", "rand", "rand", "rand"]
    section_A(args.ns, kinds, args.seed, args.fut, args.odd_checks, args.extra_depth)
    section_B(args.ms, args.seed, args.odd_checks)
    section_E(args.balance_brute, args.balance_transfer)
    say("ALL PASS")


if __name__ == "__main__":
    main()

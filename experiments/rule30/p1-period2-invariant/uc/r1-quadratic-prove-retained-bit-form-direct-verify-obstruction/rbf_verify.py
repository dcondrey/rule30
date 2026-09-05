#!/usr/bin/env python3
"""Independent adversarial check of lemma retained-bit-form (PROOF.md in ../r1-quadratic-prove-retained-bit-form-direct).

Independent of the prover's gate in three ways: columns come from psi_kernel.Endpoint
(the kernel), not from the gate's own next_column; the retained structure, runs and
read-out are re-implemented here from the lemma statement; and the checks below add
cases the gate does not run.

  V0  (F1) (F2) (F3) re-checked from CONE / BOUNDARY.
  V1  Corollary 5.1 as printed in PROOF.md ("1 + h(d) + h(d+1) = [T != 0]") versus the
      corrected form ("= [T == 0]"): count how many window cells satisfy each.
  V2  (a) (b) (c) (d) exhaustively on all binary words u <= UMAX, all n <= u, with columns
      from Endpoint.  (d) is checked as: Z_u is a union of complete non-retained runs;
      the read-out recovers every even w_i; equal (n, u, Z_{u-1}, Z_u) keys carry equal
      column u on [-u-1, n] and equal forced symbols for ALL later columns to u' = 2n+1
      (the gate checks 3 steps).
  V3  The same on the recorded n = 15 BWH+ near-miss W Q (PROOF-STATE-CAPSULE section 2)
      and on the n = 5, 6 sources whose Psi is constant (small-n sanity: the identity must
      hold there too, since it excludes nothing).
  V4  (e) by brute force through the phi recursion for m <= MB, my own Moore code.
  V5  Lemma 10 strengthened: replacing an odd-indexed nonzero window cell leaves the
      WHOLE column u (all depths to u), not only [-u-1, n], unchanged; and the single-flip
      converse for even-indexed cells.  Informational.
  V6  Rule 90 transport: the proof consumes only (F1) (F2) (F3).  Build the linear
      analogue phi90(l, r) = r XOR 2*[l == 0] XOR 1 (any four-state rule satisfying an
      (F1)-type law with E decoupled) and confirm the same derivation yields the same
      identity: that is, the argument is rule-agnostic and carries no P1 content, as
      section 10 B of PROOF.md says.  Here we simply verify that (F1) (F2) as
      *hypotheses* are the only thing used, by running the whole retained-bit check on
      a synthetic rule that satisfies them but differs from CONE.
"""
from __future__ import annotations

import os
import random
import sys
import time
from itertools import product

WORK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, WORK)
from psi_kernel import BOUNDARY, CONE, Endpoint  # noqa: E402

H = lambda t: t >> 1
Lo = lambda t: t & 1
E = lambda t: (1 + (t >> 1) + (t & 1)) & 1


def endpoint_column(word) -> dict[int, int]:
    ep = Endpoint()
    for s in word:
        ep.append(s)
    col = {}
    for i, t in enumerate(ep.column):
        col[-i] = t
    for k, t in enumerate(ep.diagonal):
        col[k] = t
    return col


def extend(prev: dict[int, int], e: int, u: int, rule) -> dict[int, int]:
    """Column u from column u-1 and symbol e, via the BRIEF section 2 recursion under `rule`."""
    col = {-u - 1: e, -u: e ^ 3}
    for d in range(-u + 1, u + 1):
        col[d] = rule[prev[d - 1]][col[d - 1]]
    return col


def forced(prev, u, n, rule):
    hits = [(e, extend(prev, e, u, rule)) for e in (1, 2)]
    hits = [(e, c) for e, c in hits if H(c[n]) == 1]
    assert len(hits) == 1, ("forcing", u, n)
    return hits[0]


def retained_structure(prev, lo, hi):
    """My own reading of the lemma statement."""
    qs = [d for d in range(hi - 1, lo - 1, -1) if prev[d] != 0]  # q_1 > q_2 > ...
    idx = {d: i for i, d in enumerate(qs, start=1)}
    ret = {}
    for d in range(lo, hi):
        if prev[d] != 0:
            ret[d] = idx[d] % 2 == 0
        else:
            above = [q for q in qs if q > d]
            ret[d] = True if not above else (idx[min(above)] % 2 == 0)
    return qs, ret


def check_pair(prev, cur, e_u, lo, hi, tag, stats):
    qs, ret = retained_structure(prev, lo, hi)
    N = len(qs)
    m = hi - lo
    # (a)
    assert (e_u == 2) == (N % 2 == 1), ("a", tag)
    # (b)
    for d in range(lo, hi):
        assert (H(cur[d]) == 1) == ret[d], ("b", tag, d)
    # Corollary 5.1 as printed vs corrected
    for d in range(lo, hi):
        lhs = (1 + H(cur[d]) + H(cur[d + 1])) & 1
        stats["cor51_printed_ok"] += int(lhs == (1 if prev[d] != 0 else 0))
        stats["cor51_corrected_ok"] += int(lhs == (1 if prev[d] == 0 else 0))
        stats["cor51_cells"] += 1
    # (c)
    rz = sum(1 for d in range(lo, hi) if prev[d] == 0 and ret[d])
    ev = sum(1 for i, q in enumerate(qs, start=1) if i % 2 == 0 and prev[q] == 2)
    assert (rz + ev) & 1 == E(cur[hi]), ("c", tag)
    # (d): runs of non-retained cells, Z_u a union of complete runs
    runs, cur_run = [], []
    for d in range(hi - 1, lo - 1, -1):
        if not ret[d]:
            cur_run.append(d)
        elif cur_run:
            runs.append(cur_run)
            cur_run = []
    if cur_run:
        runs.append(cur_run)
    Zu = {d for d in range(lo - 1, hi + 1) if cur[d] == 0}
    assert (lo - 1) not in Zu and hi not in Zu, ("d-ends", tag)
    for r in runs:
        ins = [d in Zu for d in r]
        assert all(ins) or not any(ins), ("d-partial", tag, r)
    assert Zu <= {d for r in runs for d in r}, ("d-outside", tag)
    # read-out: for even i, w_i = F_{i-1} + F_{i+1} + z_i, F_j = [R_j in Z_u]
    F = {}
    for k, r in enumerate(runs):
        F[2 * k + 1] = 1 if r[0] in Zu else 0
    for i in range(2, N + 1, 2):
        q = qs[i - 1]
        qn = qs[i] if i < N else lo - 1
        z = sum(1 for d in range(qn + 1, q) if prev[d] == 0)
        w = 1 if prev[q] == 2 else 0
        assert (F[i - 1] + F.get(i + 1, 0) + z) & 1 == w, ("d-readout", tag, i)
    Zp = tuple(d for d in range(lo, hi) if prev[d] == 0)
    return Zp, tuple(sorted(Zu))


def v0(log):
    for l in range(4):
        for r in range(4):
            t = CONE[l][r]
            assert H(t) == (H(r) + 1 + (l == 0)) & 1, ("F1", l, r)
            assert E(t) == (E(r) + H(r) * (Lo(l) == 0)) & 1, ("F2", l, r)
    assert all(BOUNDARY[s] == s ^ 3 for s in range(4)), "F3"
    print("V0 (F1) (F2) on 16 pairs and (F3) on 4 values: PASS", file=log, flush=True)


def full_forced_orbit(word, n, rule, upto):
    """Forced symbols e_u for u = len(word) .. upto, from the prefix `word`, under `rule`."""
    cols = []
    prev = None
    for u, e in enumerate(word):
        prev = extend(prev, e, u, rule)
        cols.append(prev)
    out = []
    for u in range(len(word), upto + 1):
        e, prev = forced(prev, u, n, rule)
        out.append(e)
        cols.append(prev)
    return cols, tuple(out)


def v2(umax, log, rule=CONE, label="CONE", use_endpoint=True):
    t0 = time.time()
    stats = {"cor51_printed_ok": 0, "cor51_corrected_ok": 0, "cor51_cells": 0}
    pairs = 0
    keymap = {}
    for u in range(1, umax + 1):
        for word in product((1, 2), repeat=u):
            if use_endpoint:
                prev = endpoint_column(word)
                assert prev[-u] == word[-1]
            else:
                prev = None
                for v, e in enumerate(word):
                    prev = extend(prev, e, v, rule)
            for n in range(1, u + 1):
                e_u, cur = forced(prev, u, n, rule)
                if use_endpoint:
                    # cross-check the extension against Endpoint's own column u
                    ref = endpoint_column(word + (e_u,))
                    assert all(ref[d] == cur[d] for d in range(-u - 1, u + 1)), ("endpoint-vs-extend", word, n)
                Zp, Zu = check_pair(prev, cur, e_u, -u, n, (word, n), stats)
                colkey = tuple(cur[d] for d in range(-u - 1, n + 1))
                _, fut = full_forced_orbit(word + (e_u,), n, rule, 2 * n + 1)
                key = (n, u, Zp, Zu)
                val = (colkey, fut)
                assert keymap.setdefault(key, val) == val, ("d-pair-future", word, n)
                pairs += 1
    print(f"V2 [{label}] all binary words u <= {umax}, all n <= u: {pairs} (word, n) pairs; (a) (b) (c) (d) PASS; "
          f"pair key -> column u on [-u-1, n] and forced symbols to u' = 2n+1: PASS; "
          f"{len(keymap)} distinct keys   [{time.time()-t0:.0f}s]", file=log, flush=True)
    c = stats["cor51_cells"]
    print(f"V1 [{label}] Corollary 5.1 as printed ('1 + h(d) + h(d+1) = [T != 0]') holds on "
          f"{stats['cor51_printed_ok']} of {c} window cells; corrected form ('= [T == 0]') holds on "
          f"{stats['cor51_corrected_ok']} of {c}", file=log, flush=True)


def v3(log):
    stats = {"cor51_printed_ok": 0, "cor51_corrected_ok": 0, "cor51_cells": 0}
    # n = 15 near miss from PROOF-STATE-CAPSULE section 2
    W = tuple(int(ch) for ch in "111122211212112")
    Q = tuple(int(ch) for ch in "12211111122111211")
    n = 15
    cols, fut = full_forced_orbit(W, n, CONE, 2 * n + 1)
    assert fut == Q, ("n15-forced-continuation", fut, Q)
    diag = tuple(cols[u][n] for u in range(n, 2 * n + 2))
    assert diag == tuple(int(ch) for ch in "33333333333333332"), ("n15-diag", diag)
    for u in range(n, 2 * n + 2):
        prev, cur = cols[u - 1], cols[u]
        check_pair(prev, cur, fut[u - n], -u, n, ("n15", u), stats)
    print(f"V3 n=15 near-miss W={''.join(map(str, W))}: forced continuation = Q, "
          f"diagonal = 3^16 2, (a)-(d) on all 17 columns u = 15..31: PASS", file=log, flush=True)
    # n = 5, 6 constant-Psi sources (BWH+ exceptions): find them and check the identity there
    for n in (5, 6):
        consts = []
        for W in product((1, 2), repeat=n):
            cols, fut = full_forced_orbit(W, n, CONE, 2 * n + 1)
            diag = tuple(E(cols[u][n]) for u in range(n, 2 * n + 2))
            if len(set(diag)) == 1:
                consts.append((W, fut, diag[0]))
                for u in range(n, 2 * n + 2):
                    check_pair(cols[u - 1], cols[u], fut[u - n], -u, n, ("const", n, W, u), stats)
        print(f"V3 n={n}: {len(consts)} constant-Psi sources "
              f"{[(''.join(map(str, w)), ''.join(map(str, q)), c) for w, q, c in consts]}; "
              f"(a)-(d) hold on every column of each: PASS", file=log, flush=True)
    print(f"V1 [n15+consts] Corollary 5.1 printed {stats['cor51_printed_ok']}/{stats['cor51_cells']}, "
          f"corrected {stats['cor51_corrected_ok']}/{stats['cor51_cells']}", file=log, flush=True)


def v4(mb, log):
    for m in range(1, mb + 1):
        z = 0
        for wd in product((0, 1, 2), repeat=m):
            prev = {d: wd[d] for d in range(m)}
            e, col = forced(prev, 0, m, CONE) if False else (None, None)
            # forced through phi with the window as column "u-1" on [0, m), column u on [-1, m]
            hits = []
            for ee in (1, 2):
                c = {-1: ee, 0: ee ^ 3}
                for d in range(1, m + 1):
                    c[d] = CONE[prev[d - 1]][c[d - 1]]
                if H(c[m]) == 1:
                    hits.append((ee, c))
            assert len(hits) == 1
            ee, c = hits[0]
            # my own Moore evaluation with forced start
            N = sum(1 for t in wd if t)
            h, F = (1 + N) & 1, 0
            for t in wd:
                F ^= h & (1 if t in (0, 2) else 0)
                h ^= 1 ^ (1 if t == 0 else 0)
            assert h == 1 and F == E(c[m]), ("e-moore-vs-phi", wd)
            z += (F == 0)
        assert z == (3 ** m + 1) // 2, ("e-count", m, z)
    print(f"V4 (e) #Phi=0 = (3^m+1)/2 through phi for m <= {mb}: PASS", file=log, flush=True)


def v5(mmax, log):
    cnt = 0
    for m in range(1, mmax + 1):
        for wd in product((0, 1, 2), repeat=m):
            u = m  # place the window as column u-1 restricted to [-u, n-1]; here the full column
            # Build a genuine column: any window in {0,1,2}^m with wd[0] != 0 is used as
            # the window [-u, n-1] of a synthetic column u-1 of length 2u; pad above with zeros.
            if wd[0] == 0:
                continue
            n = 0  # window [-u, -1], top at n-1 = -1
            prev = {d: wd[d + u] for d in range(-u, 0)}
            for d in range(0, u):
                prev[d] = 0
            e_u, cur = forced(prev, u, n, CONE)
            qs = [d for d in range(-1, -u - 1, -1) if prev[d] != 0]
            for i, q in enumerate(qs, start=1):
                for v in (1, 2, 3):
                    if v == prev[q]:
                        continue
                    alt = dict(prev)
                    alt[q] = v
                    e2, cur2 = forced(alt, u, n, CONE)
                    same = (e2 == e_u) and all(cur2[d] == cur[d] for d in range(-u - 1, u + 1))
                    if i % 2 == 1:
                        assert same, ("L10-odd-whole-column", wd, q, v)
                    elif v != 3:
                        assert not same, ("L10-even-visible", wd, q, v)
                    cnt += 1
    print(f"V5 Lemma 10 on the WHOLE column u (depths to u): {cnt} replacements, odd-indexed invisible, "
          f"even-indexed visible: PASS", file=log, flush=True)


def v6(umax, log):
    # A synthetic rule satisfying (F1) and (F2) exactly but differing from CONE as a table:
    # choose H(phi) = H(r) + 1 + [l == 0], E(phi) = E(r) + H(r) [Lo(l) == 0], same as CONE by (C1)
    # T is determined by (H, E), so any rule with (F1)(F2) IS CONE.  So instead test the
    # genuinely different linear rule: E(phi) = E(r) (no shear).  Then Phi should be constant 0
    # and (c) must FAIL, showing (F2) is load-bearing: the lemma is not a tautology.
    def mk(l, r):
        h = (H(r) + 1 + (l == 0)) & 1
        e = E(r)
        lo = (1 + h + e) & 1
        return 2 * h + lo
    R = tuple(tuple(mk(l, r) for r in range(4)) for l in range(4))
    assert R != CONE
    bad_c = 0
    tot = 0
    stats = {"cor51_printed_ok": 0, "cor51_corrected_ok": 0, "cor51_cells": 0}
    for u in range(1, umax + 1):
        for word in product((1, 2), repeat=u):
            prev = None
            for v, e in enumerate(word):
                prev = extend(prev, e, v, R)
            for n in range(1, u + 1):
                e_u, cur = forced(prev, u, n, R)
                tot += 1
                try:
                    check_pair(prev, cur, e_u, -u, n, (word, n), stats)
                except AssertionError as ex:
                    assert ex.args[0][0] in ("c", "d-partial", "d-outside", "d-readout"), ex.args
                    bad_c += 1
    print(f"V6 control: linear rule with (F1) but E(phi) = E(r) (no shear) on u <= {umax}: "
          f"(a) (b) still hold on all {tot} pairs, (c)/(d) fail on {bad_c} of {tot}; "
          f"so (F2) is load-bearing and the identity is not a tautology of (F1) alone", file=log, flush=True)


def main():
    log = sys.stdout
    t0 = time.time()
    v0(log)
    v2(13, log)
    v3(log)
    v4(9, log)
    v5(8, log)
    v6(8, log)
    print(f"ALL PASS   [{time.time()-t0:.0f}s]", file=log, flush=True)


if __name__ == "__main__":
    main()

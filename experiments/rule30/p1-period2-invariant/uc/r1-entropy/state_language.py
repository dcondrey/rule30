#!/usr/bin/env python3
"""Entropy of the reachable column language, and the RW chains counted in states.

The forced orbit from column u onward is a function of the full column
T[u][.] (psi_kernel.Endpoint state = column + diagonal), not of the source
W.  So the effective orbit space at depth n is

    C_n = { full column n-1 : W in {1,2}^n },

and RESULTS-CLUSTER-ANATOMY.md measured |C_n| growing like 1.77^n at
n = 6..16.  This script computes |C_u| exactly by BFS over DISTINCT states
(level u states = {M(col, e) : col in C_{u-1}, e in {1,2}}, deduplicated,
with source multiplicities carried), which costs O(|C_u| u) per level
instead of O(2^u u):

  part 1: |C_u| for u = 1..umax, ratios, log2 ratios, and an exact
          linear-recurrence test (regular language <=> rational generating
          function <=> eventual linear recurrence);
  part 2: for n = nmin..nmax, both c, the E-only and joint (E + hard-core)
          survivor chains counted in STATES and in sources, against the
          state null |C_n| 2^(-k) and the state golden null
          |C_n| 2^(-k) F_{k+3}/2^(k+1); fibre sizes of survivors; and the
          first hard-core violation position in the forced word of deep
          E-survivor states.

Run:  cd <kernel dir> && uv run python uc/r1-entropy/state_language.py --umax 24 --nmin 6 --nmax 18
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from psi_kernel import Endpoint  # noqa: E402


def fib(m: int) -> int:
    a, b = 0, 1
    for _ in range(m):
        a, b = b, a + b
    return a


def key_of(col: list[int], dia: list[int]) -> tuple:
    return (tuple(col), tuple(dia))


def state_from_key(k: tuple, length: int) -> Endpoint:
    st = Endpoint()
    st.column, st.diagonal, st.length = list(k[0]), list(k[1]), length
    return st


def bfs_levels(umax: int, log):
    """Return {u: Counter(state_key -> multiplicity)} for u = 1..umax (u = prefix length)."""
    levels = {}
    cur = Counter()
    root = Endpoint()
    for s in (1, 2):
        st = root.clone()
        st.append(s)
        cur[key_of(st.column, st.diagonal)] += 1
    levels[1] = cur
    counts = [len(cur)]
    print("# part 1: reachable column language.  u = prefix length; |C_u| = distinct full columns u-1", file=log)
    print("  u      |C_u|     2^u   |C_u|/|C_{u-1}|  log2 ratio   max fibre   sec", file=log)
    print(f"  1 {len(cur):10d} {2:8d}          -           -        {max(cur.values()):5d}", file=log)
    for u in range(2, umax + 1):
        t0 = time.time()
        nxt = Counter()
        for k, mult in cur.items():
            st = state_from_key(k, u - 1)
            for s in (1, 2):
                col, dia = st.peek(s)
                nxt[(tuple(col + [s]), tuple(dia))] += mult
        assert sum(nxt.values()) == 2 ** u
        levels[u] = nxt
        counts.append(len(nxt))
        r = len(nxt) / len(cur)
        import math
        print(f"{u:3d} {len(nxt):10d} {2**u:8d}       {r:7.4f}      {math.log2(r):7.4f}     {max(nxt.values()):5d}  {time.time()-t0:5.1f}", file=log)
        log.flush()
        cur = nxt
    return levels, counts


def recurrence_test(seq: list[int], log, max_order: int = 8, transient: int = 4):
    """Exact test: does s_t = sum_{i=1..r} a_i s_{t-i} hold for all t >= transient + r?"""
    print("\n# linear recurrence test on |C_u| (exact rational arithmetic), transient skipped =", transient, file=log)
    n = len(seq)
    for r in range(1, max_order + 1):
        rows = []
        for t in range(transient + r, n):
            rows.append(([Fraction(seq[t - i]) for i in range(1, r + 1)], Fraction(seq[t])))
        if len(rows) < r + 2:
            print(f"  order {r}: not enough terms", file=log)
            continue
        # solve first r rows by Gaussian elimination
        A = [row[0][:] + [row[1]] for row in rows[:r]]
        ok = True
        for i in range(r):
            piv = next((j for j in range(i, r) if A[j][i] != 0), None)
            if piv is None:
                ok = False
                break
            A[i], A[piv] = A[piv], A[i]
            inv = 1 / A[i][i]
            A[i] = [x * inv for x in A[i]]
            for j in range(r):
                if j != i and A[j][i] != 0:
                    f = A[j][i]
                    A[j] = [x - f * y for x, y in zip(A[j], A[i])]
        if not ok:
            print(f"  order {r}: singular system", file=log)
            continue
        coef = [A[i][r] for i in range(r)]
        bad = 0
        for lhs, rhs in rows[r:]:
            if sum(a * x for a, x in zip(coef, lhs)) != rhs:
                bad += 1
        print(f"  order {r}: coefficients {[str(c) for c in coef]}; verification failures on {bad} of {len(rows) - r} held-out terms", file=log)
        if bad == 0:
            print(f"  -> order-{r} recurrence holds exactly on all available terms", file=log)
            return r
    print("  -> no exact linear recurrence of order <= %d found" % max_order, file=log)
    return None


def forced_run(st: Endpoint, n: int, c: int, prev: int, max_steps: int):
    """Follow the forced (H-forcing at depth n) continuation from state st.
    Returns (E_run, joint_run, first_hc_violation_index_or_None, symbols)."""
    e_run = 0
    j_run = 0
    joint_alive = True
    first_hc = None
    symbols = []
    for step in range(max_steps):
        chosen = None
        for s in (1, 2):
            col, dia = st.peek(s)
            if dia[n] >> 1 == 1:
                chosen = (s, col, dia)
                break
        s, col, dia = chosen
        symbols.append(s)
        hc_bad = prev == 1 and s == 1
        if hc_bad and first_hc is None:
            first_hc = step
        hit = dia[n] == c
        if not hit:
            break
        e_run += 1
        if joint_alive:
            if hc_bad:
                joint_alive = False
            else:
                j_run += 1
        nxt = Endpoint()
        nxt.column, nxt.diagonal, nxt.length = col + [s], dia, st.length + 1
        st, prev = nxt, s
    return e_run, j_run, first_hc, symbols


def part2(levels, n: int, c: int, log):
    states = levels[n]
    Cn = len(states)
    NE_st = Counter(); NE_src = Counter()
    NJ_st = Counter(); NJ_src = Counter()
    fib_E = defaultdict(list)
    deep_hc = Counter()   # first HC violation index among E-survivor states with E_run >= n-1
    deep_total = 0
    for k, mult in states.items():
        st = state_from_key(k, n)
        prev = k[0][-1]
        e_run, j_run, first_hc, symbols = forced_run(st, n, c, prev, n + 3)
        for j in range(0, e_run + 1):
            NE_st[j] += 1; NE_src[j] += mult
            fib_E[j].append(mult)
        for j in range(0, j_run + 1):
            NJ_st[j] += 1; NJ_src[j] += mult
        if e_run >= n - 1:
            deep_total += 1
            deep_hc["none" if first_hc is None else first_hc] += 1
    print(f"\n# n={n} c={c}: |C_n|={Cn} states, 2^n={2**n} sources, mean fibre {2**n/Cn:.2f}", file=log)
    print("  k   NE_st  NE_src  NJ_st  NJ_src | NE_st/(C 2^-k)  NJ_st/(C 2^-k)  NJ_st/golden_st | NE_src/2^(n-k)  NJ_src/2^(n-k) | mean fibre E-surv", file=log)
    kmax = max(max(NE_st), max(NJ_st))
    maxE = maxJ = maxJg = 0.0
    for k in range(kmax + 1):
        ne_s, ne_r = NE_st.get(k, 0), NE_src.get(k, 0)
        nj_s, nj_r = NJ_st.get(k, 0), NJ_src.get(k, 0)
        null_st = Cn * 2.0 ** (-k)
        golden_st = null_st * fib(k + 3) / 2.0 ** (k + 1)
        rE, rJ, rJg = ne_s / null_st, nj_s / null_st, nj_s / golden_st
        maxE, maxJ, maxJg = max(maxE, rE), max(maxJ, rJ), max(maxJg, rJg)
        mf = (sum(fib_E[k]) / len(fib_E[k])) if fib_E[k] else float("nan")
        print(f"{k:3d} {ne_s:7d} {ne_r:7d} {nj_s:6d} {nj_r:7d} |   {rE:8.3f}       {rJ:8.3f}        {rJg:8.3f}    |   {ne_r/2.0**(n-k):8.3f}       {nj_r/2.0**(n-k):8.3f}    |  {mf:6.2f}", file=log)
    kE = max(k for k in NE_st if NE_st[k] > 0)
    kJ = max(k for k in NJ_st if NJ_st[k] > 0)
    print(f"  deepest E-run {kE}, deepest joint run {kJ} (need {n+2}); max NE_st/(C 2^-k) = {maxE:.3f}, max NJ_st/(C 2^-k) = {maxJ:.3f}, max NJ_st/golden_st = {maxJg:.3f}", file=log)
    print(f"  first HC violation index among the {deep_total} E-survivor states with E-run >= n-1: {dict(sorted(deep_hc.items(), key=lambda kv: (isinstance(kv[0], str), kv[0])))}", file=log)
    return (n, c, Cn, kE, kJ, maxE, maxJ, maxJg)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--umax", type=int, default=22)
    ap.add_argument("--nmin", type=int, default=6)
    ap.add_argument("--nmax", type=int, default=16)
    ap.add_argument("--log", type=str, default="uc/r1-entropy/state_language.log")
    args = ap.parse_args()
    with open(args.log, "w") as log:
        levels, counts = bfs_levels(args.umax, log)
        recurrence_test(counts, log)
        summary = []
        for n in range(args.nmin, args.nmax + 1):
            for c in (2, 3):
                summary.append(part2(levels, n, c, log))
                log.flush()
        print("\n# summary: n c |C_n| deepestE deepestJ need max(NE_st/null) max(NJ_st/null) max(NJ_st/golden)", file=log)
        for n, c, Cn, kE, kJ, mE, mJ, mJg in summary:
            print(f"{n:3d} {c} {Cn:8d} {kE:4d} {kJ:4d} {n+2:4d}   {mE:7.3f}   {mJ:7.3f}   {mJg:7.3f}", file=log)
    with open(args.log) as f:
        sys.stdout.write(f.read())


if __name__ == "__main__":
    main()

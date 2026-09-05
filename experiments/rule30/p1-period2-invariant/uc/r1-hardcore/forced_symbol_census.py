#!/usr/bin/env python3
"""Census of the forced symbol sequence along the RW orbit.

For every binary prefix W in {1,2}^n the H-forcing at depth n determines a
unique continuation Q_n(W) (BRIEF section 3, orbit form).  Along that single
path each column u >= n carries two bits:

    x_u = H(e_u)            the forced symbol, 1 -> symbol 1, 2 -> symbol 2
    y_u = [E(T[u][n]) == E(c)]   the E constraint of (RW)

(RW) survival to level k is: y ok for the first k columns and the forced
symbol word hard-core (no 11, including the junction with W[n-1]).

This script measures, exhaustively over all 2^n prefixes:

  1. N_k under E only, hard-core only, both (RW), and both plus the
     actual-right factor exclusion 22222 (bits 00000).
  2. The joint law of (previous symbol, forced symbol, E ok) at each level,
     restricted to nodes surviving under E only and under RW, so that any
     vanishing combination shows up as an exact zero.
  3. The density of forced 1s among E survivors.

The forced-continuation kernel here is a direct column recursion (the Moore
machine of BRIEF section 2), gated against psi_kernel.psi for n <= 9.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
from psi_kernel import CONE, psi  # noqa: E402


def forced_path(prefix: tuple[int, ...], steps: int) -> tuple[list[int], list[int]]:
    """Return (forced symbols, defects at depth n) for `steps` forced columns."""
    n = len(prefix)
    col: list[int] = []
    for u, e in enumerate(prefix):
        new = [0] * (2 * u + 2)
        new[0] = e
        new[1] = e ^ 3
        for i in range(2, 2 * u + 2):
            new[i] = CONE[col[i - 2]][new[i - 1]]
        col = new
    # col is column n-1 on depths [-n, n-1], length 2n
    symbols: list[int] = []
    defects: list[int] = []
    for j in range(steps):
        u = n + j
        assert len(col) == n + u
        zeros = col.count(0)
        high = (n + u + zeros) & 1
        e = 2 if high else 1
        new = [0] * (n + u + 2)
        new[0] = e
        new[1] = e ^ 3
        for i in range(2, n + u + 2):
            new[i] = CONE[col[i - 2]][new[i - 1]]
        cell = new[n + u + 1]
        assert cell >> 1 == 1, (prefix, j, cell)
        symbols.append(e)
        defects.append(1 ^ (cell >> 1) ^ (cell & 1))
        col = new[: n + u + 1]
    return symbols, defects


def gate(max_n: int) -> int:
    from itertools import product

    checked = 0
    for n in range(1, max_n + 1):
        for w in product((1, 2), repeat=n):
            q, d = psi(w)
            s, e = forced_path(w, n + 2)
            assert tuple(s) == q and tuple(e) == d, (w, s, q, e, d)
            checked += 1
    return checked


def census(n: int, c: int, extra: int) -> dict:
    from itertools import product

    target_e = 0 if c == 2 else 1
    steps = n + 2 + extra
    n_e = [0] * (steps + 1)
    n_hc = [0] * (steps + 1)
    n_rw = [0] * (steps + 1)
    n_rw_ar = [0] * (steps + 1)
    n_hc_ar = [0] * (steps + 1)
    # joint[(level, prev, sym, eok)] over nodes surviving E through level-1
    joint_e: Counter = Counter()
    joint_rw: Counter = Counter()
    ones_e: defaultdict = defaultdict(int)  # level -> total forced ones among E survivors
    deepest_rw = 0
    deepest_e = 0
    witness_rw = ""
    for w in product((1, 2), repeat=n):
        syms, defs = forced_path(w, steps)
        eok = [d == target_e for d in defs]
        prev = w[-1]
        hc_ok = []
        for s in syms:
            hc_ok.append(not (prev == 1 and s == 1))
            prev = s
        # actual-right: no 22222 across junction
        full = list(w) + syms
        ar_ok = []
        for j in range(steps):
            idx = n + j
            ar_ok.append(not (idx >= 4 and all(full[idx - t] == 2 for t in range(5))))

        def first_fail(flags: list[bool]) -> int:
            for j, f in enumerate(flags):
                if not f:
                    return j
            return steps

        k_e = first_fail(eok)
        k_hc = first_fail(hc_ok)
        k_rw = min(k_e, k_hc)
        k_ar = first_fail(ar_ok)
        k_rw_ar = min(k_rw, k_ar)
        k_hc_ar = min(k_hc, k_ar)
        for k in range(steps + 1):
            if k_e >= k:
                n_e[k] += 1
            if k_hc >= k:
                n_hc[k] += 1
            if k_rw >= k:
                n_rw[k] += 1
            if k_rw_ar >= k:
                n_rw_ar[k] += 1
            if k_hc_ar >= k:
                n_hc_ar[k] += 1
        if k_rw > deepest_rw:
            deepest_rw = k_rw
            witness_rw = "".join(map(str, full[: n + k_rw]))
        deepest_e = max(deepest_e, k_e)
        prev = w[-1]
        run_ones = 0
        for j in range(steps):
            if k_e >= j:
                joint_e[(j, prev, syms[j], eok[j])] += 1
                ones_e[j] += run_ones
            if k_rw >= j:
                joint_rw[(j, prev, syms[j], eok[j])] += 1
            if syms[j] == 1:
                run_ones += 1
            prev = syms[j]
    return {
        "n": n,
        "c": c,
        "steps": steps,
        "N_E": n_e,
        "N_HC": n_hc,
        "N_RW": n_rw,
        "N_RW_AR": n_rw_ar,
        "N_HC_AR": n_hc_ar,
        "joint_e": joint_e,
        "joint_rw": joint_rw,
        "ones_e": ones_e,
        "deepest_rw": deepest_rw,
        "deepest_e": deepest_e,
        "witness_rw": witness_rw,
    }


def report(res: dict) -> None:
    n, c, steps = res["n"], res["c"], res["steps"]
    print(f"=== n={n} c={c} steps={steps} need={n+2} ===")
    print(f"deepest RW run {res['deepest_rw']}  deepest E-only run {res['deepest_e']}  witness {res['witness_rw']}")
    print(" k     N_E    N_HC    N_RW  N_RW+AR N_HC+AR   E/prev   RW/prev")
    for k in range(steps + 1):
        pe = res["N_E"][k] / res["N_E"][k - 1] if k and res["N_E"][k - 1] else float("nan")
        pr = res["N_RW"][k] / res["N_RW"][k - 1] if k and res["N_RW"][k - 1] else float("nan")
        print(
            f"{k:2d} {res['N_E'][k]:7d} {res['N_HC'][k]:7d} {res['N_RW'][k]:7d} "
            f"{res['N_RW_AR'][k]:8d} {res['N_HC_AR'][k]:7d}   {pe:6.3f}   {pr:6.3f}"
        )
    print("joint law over E survivors: level, (prev,sym) -> [#E ok, #E fail]  and density of forced 1s so far")
    for j in range(steps):
        row = []
        for prev in (1, 2):
            for sym in (1, 2):
                ok = res["joint_e"][(j, prev, sym, True)]
                bad = res["joint_e"][(j, prev, sym, False)]
                row.append(f"({prev}{sym}):{ok:6d}/{bad:6d}")
        tot = res["N_E"][j]
        dens = res["ones_e"][j] / (tot * j) if tot and j else float("nan")
        print(f"  j={j:2d} " + "  ".join(row) + f"   ones density {dens:.3f}")
    print("joint law over RW survivors: level, (prev,sym) -> [#E ok, #E fail]")
    for j in range(steps):
        row = []
        for prev in (1, 2):
            for sym in (1, 2):
                ok = res["joint_rw"][(j, prev, sym, True)]
                bad = res["joint_rw"][(j, prev, sym, False)]
                row.append(f"({prev}{sym}):{ok:6d}/{bad:6d}")
        print(f"  j={j:2d} " + "  ".join(row))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-n", type=int, default=8)
    ap.add_argument("--max-n", type=int, default=14)
    ap.add_argument("--extra", type=int, default=0, help="forced steps beyond n+2")
    ap.add_argument("--gate", type=int, default=9)
    args = ap.parse_args()
    print(f"gate: {gate(args.gate)} prefixes agree with psi_kernel.psi through n={args.gate}")
    for n in range(args.min_n, args.max_n + 1):
        for c in (2, 3):
            report(census(n, c, args.extra))
            sys.stdout.flush()


if __name__ == "__main__":
    main()

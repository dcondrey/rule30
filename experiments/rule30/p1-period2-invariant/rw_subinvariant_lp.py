#!/usr/bin/env python3
"""Subinvariant (Lyapunov) weight on the RW forced survivor graph.

PRE-REGISTERED 2026-09-03 in `PREREGISTRATION-SUBINVARIANT-CERTIFICATE.md`,
before running.  Route and literature in `ROUTE-SUBINVARIANT-CERTIFICATE.md`.

The survivor graph is a DAG with out-degree one (states strictly lengthen), so
free per-state weights make the subinvariance LP vacuous: `w = rho^depth` always
works.  The experiment is therefore the restricted class, not the inequality.

    log w(s) = sum_{k<K} x[k][dia_k(s)] + sum_{k>=K} a[dia_k(s)],  x, a >= 0

`x, a >= 0` gives `w >= 1` so `inf w = 1` holds by construction (route 3.1);
`4K+4` parameters give a finite description (route 3.2); the tail term `a`
reads every position of a growing diagonal, which is the coordinate placing
this outside the refuted fixed-radius additive class (capsule section 5 row 1).

Maximise `t = log(1/rho)` subject to `phi(s') . z - phi(s) . z <= -t` on every
survivor edge of the complete census.  Then

    alpha_hat(n) = max_{s0} phi(s0) . z / (n * t)

and `(RW-alpha)` needs `alpha_hat < 1`.  Kill conditions are in the
pre-registration: `t = 0`; `alpha_hat >= 1`; `alpha_hat` rising with `n` or the
fit violated on a held-out larger `n`.
"""

from __future__ import annotations

import argparse
import sys
import time
from itertools import product

import numpy as np
from scipy.optimize import linprog

from psi_kernel import Endpoint


def H(t: int) -> int:
    return t >> 1


def feature(dia: list[int], K: int) -> tuple[int, ...]:
    """Position/symbol counts: 4K windowed indicators plus 4 tail counts."""
    vec = [0] * (4 * K + 4)
    for k, sym in enumerate(dia):
        if k < K:
            vec[4 * k + sym] += 1
        else:
            vec[4 * K + sym] += 1
    return tuple(vec)


def survivor_edges(n: int, c: int, levels: int, K: int):
    """Complete census.  Returns (deduped edge difference vectors, s0 features).

    An edge `s_j -> s_{j+1}` is present iff every step up to and including `j`
    is hard-core and lands the target cell on `c`.  `s0` features are collected
    only for sources whose survivor path is nonempty.
    """
    diffs: set[tuple[int, ...]] = set()
    starts: set[tuple[int, ...]] = set()
    states: set[tuple[int, ...]] = set()
    for src in product((1, 2), repeat=n):
        st = Endpoint()
        for s in src:
            st.append(s)
        prev = src[-1]
        phi_prev = feature(st.diagonal, K)
        phi_start = phi_prev
        alive = False
        for _ in range(levels):
            chosen = None
            for s in (1, 2):
                col, dia = st.peek(s)
                if H(dia[n]) == 1:
                    assert chosen is None, "H-forced symbol must be unique"
                    chosen = (s, col, dia)
            assert chosen is not None, "H-forced symbol must exist"
            s, col, dia = chosen
            if (prev == 1 and s == 1) or dia[n] != c:
                break
            phi_next = feature(dia, K)
            states.add(phi_prev)
            states.add(phi_next)
            diffs.add(tuple(b - a for a, b in zip(phi_prev, phi_next)))
            phi_prev = phi_next
            alive = True
            st.column = col + [s]
            st.diagonal = dia
            st.length += 1
            prev = s
        if alive:
            starts.add(phi_start)
    return sorted(diffs), sorted(starts), sorted(states)


def longest_run(n: int, c: int, levels: int) -> int:
    """Longest actual survivor run, to compare against any claimed bound."""
    best = 0
    for src in product((1, 2), repeat=n):
        st = Endpoint()
        for sym in src:
            st.append(sym)
        prev = src[-1]
        run = 0
        for _ in range(levels):
            chosen = None
            for sym in (1, 2):
                col, dia = st.peek(sym)
                if H(dia[n]) == 1:
                    chosen = (sym, col, dia)
            sym, col, dia = chosen
            if (prev == 1 and sym == 1) or dia[n] != c:
                break
            run += 1
            st.column = col + [sym]
            st.diagonal = dia
            st.length += 1
            prev = sym
        best = max(best, run)
    return best


def solve(diffs, starts, K: int, n: int, signed: bool = False, states=None, contrast: bool = False):
    """Maximise t subject to diff.z <= -t, 0 <= z <= 1.  Returns (t, z, alpha).

    ``signed`` drops the ``z >= 0`` constraint, which drops the guarantee
    ``inf_s w > 0``.  It is a diagnostic only: a signed weight bounds nothing,
    but separating the two tells whether the binding obstruction is the
    boundedness requirement of route section 3.1 or the feature class itself.
    """
    dim = 4 * K + 4
    A = np.zeros((len(diffs), dim + 1))
    A[:, :dim] = np.array(diffs, dtype=float)
    A[:, dim] = 1.0
    obj = np.zeros(dim + 1)
    obj[dim] = -1.0
    if states is not None:
        # The weaker and correct encoding of route section 3.1: the weight need
        # only be bounded below on the reachable SURVIVOR sublanguage, which is
        # the clause `RESULTS.md:142-147` names as outside the old normal form.
        # Signed coefficients, with `log w(s) >= 0` imposed on every survivor
        # state of the census instead of on every word.
        B = np.zeros((len(states), dim + 1))
        B[:, :dim] = -np.array(states, dtype=float)
        A = np.vstack([A, B])
    lo = -1.0 if (signed or states is not None) else 0.0
    bounds = [(lo, 1.0)] * dim + [(0.0, None)]
    A_eq = b_eq = None
    if contrast:
        # Exclude the pure-length direction.  `x[k][.] = const, a[.] = -t` is
        # subinvariant for free, because every step lengthens the diagonal by
        # one; the resulting "bound" is the observed run length restated, which
        # is route section 3.2's vacuous weight again.  Requiring each position
        # block to sum to zero leaves only contrasts BETWEEN symbols, so a
        # positive `t` has to come from the state and not from the clock.
        A_eq = np.zeros((K + 1, dim + 1))
        for k in range(K + 1):
            A_eq[k, 4 * k : 4 * k + 4] = 1.0
        b_eq = np.zeros(K + 1)
    res = linprog(
        obj, A_ub=A, b_ub=np.zeros(A.shape[0]), A_eq=A_eq, b_eq=b_eq,
        bounds=bounds, method="highs",
    )
    if not res.success:
        return None, None, None
    z = res.x[:dim]
    t = res.x[dim]
    if t <= 1e-9:
        return 0.0, z, float("inf")
    S = np.array(starts, dtype=float)
    alpha = float((S @ z).max() / (n * t))
    return float(t), z, alpha


def report_weight(z, K: int) -> str:
    lines = []
    for k in range(K):
        lines.append("x[%d] = %s" % (k, " ".join(f"{z[4*k+s]:.4f}" for s in range(4))))
    lines.append("a    = %s" % " ".join(f"{z[4*K+s]:.4f}" for s in range(4)))
    return "\n".join("    " + l for l in lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-n", type=int, default=10)
    ap.add_argument("--max-n", type=int, default=14)
    ap.add_argument("--K", type=int, default=8)
    ap.add_argument("--holdout", type=int, default=0)
    ap.add_argument("--signed", action="store_true")
    ap.add_argument("--sublanguage", action="store_true")
    ap.add_argument("--contrast", action="store_true")
    ap.add_argument("--max-run", action="store_true",
                    help="print the longest actual survivor run instead of solving")
    args = ap.parse_args()

    if args.max_run:
        print(f"{'n':>3} {'c':>2} {'max run':>8} {'run/n':>8}")
        for n in range(args.min_n, args.max_n + 1):
            for c in (2, 3):
                m = longest_run(n, c, n + 4)
                print(f"{n:>3} {c:>2} {m:>8} {m/n:>8.4f}")
        return

    print("# Subinvariant weight LP on the RW forced survivor graph.")
    print(f"# K={args.K}, complete census, levels = n+4, both target cells.")
    print(f"{'n':>3} {'c':>2} {'edges':>7} {'starts':>7} {'t':>9} {'rho':>8} {'alpha_hat':>10}")
    fits = {}
    for n in range(args.min_n, args.max_n + 1):
        for c in (2, 3):
            t0 = time.time()
            diffs, starts, states = survivor_edges(n, c, n + 4, args.K)
            t, z, alpha = solve(
                diffs, starts, args.K, n, args.signed,
                states if args.sublanguage else None,
                args.contrast,
            )
            if t is None:
                print(f"{n:>3} {c:>2} {len(diffs):>7} {len(starts):>7}  INFEASIBLE")
                continue
            rho = float(np.exp(-t)) if t > 0 else 1.0
            astr = "inf" if alpha == float("inf") else f"{alpha:.4f}"
            print(
                f"{n:>3} {c:>2} {len(diffs):>7} {len(starts):>7} {t:>9.5f} {rho:>8.5f} {astr:>10}"
                f"   [{time.time()-t0:.1f}s]"
            )
            sys.stdout.flush()
            if t > 0:
                fits[(n, c)] = (z, t)

    for c in (2, 3):
        z = fits.get((args.max_n, c), (None, None))[0]
        if z is None:
            continue
        print(f"\n# Fitted weight at n={args.max_n}, c={c}:")
        print(report_weight(z, args.K))

    if args.holdout:
        print(f"\n# Holdout: the n={args.max_n} fit evaluated at n={args.holdout}, no refit.")
        for c in (2, 3):
            z, t = fits.get((args.max_n, c), (None, None))
            if z is None:
                continue
            diffs, starts, states = survivor_edges(args.holdout, c, args.holdout + 4, args.K)
            step = np.array(diffs, dtype=float) @ z
            worst = float(step.max())
            broken = int((step > -t + 1e-9).sum())
            lo = float((np.array(states, dtype=float) @ z).min())
            hi = float((np.array(starts, dtype=float) @ z).max())
            bound = (hi - lo) / t
            print(
                f"c={c}: edges={len(diffs)} worst step={worst:+.5f} (need <= {-t:+.5f}) "
                f"edges violating the fit={broken}  min log w over survivor states={lo:+.4f}  "
                f"implied run bound={bound:.2f}  alpha={bound/args.holdout:.4f}"
            )


if __name__ == "__main__":
    main()

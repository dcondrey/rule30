#!/usr/bin/env python3
"""Independence-null estimates for the RW refutation program, in states.

Inputs (all measured, cited in the docstring of the log):
  Q_n  = number of distinct forced-process states at k = 0, fitted as A rho^n
         from state_level_hits_n18-30.log (exact n = 18..24) and the
         quotient_multiplicity / state_survival logs (n <= 20);
  p    = state-level per-column survival probability of an admissible forced
         step (E-hit and hard-core), pooled over levels with >= 100 states
         from state_level_hits_n18-30.log.

Under the null every level-k state survives step k+1 independently with
probability p.  The script reports, for n in a range:
  E[#states surviving n+2 columns]  (an RW counterexample needs one, times the
                                     12a ending, taken as a further factor 1/4),
  the tail sum over n >= n0 of that expectation (both c),
  E[#states with exactly one violation in n+2 columns] (the distance-1 near-miss
                                     count, four-state bookkeeping),
  P(deepest >= log2 Q_n)            (failure of the state-halving lemma),
  P(deepest >= 0.75 n), P(deepest >= 0.8 n) as a calibration against the census.

These are model numbers, not measurements; they say how surprising the
observed census is under independence and how much a refutation beyond
n = 33 would have to depart from it.

Run:  cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/null_estimates.py
"""

from __future__ import annotations

import argparse
import math


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rho", type=float, default=1.765, help="growth rate of Q_n")
    ap.add_argument("--q24", type=int, default=1204323, help="exact Q_24 (state_level_hits_n18-30.log)")
    ap.add_argument("--p", type=float, default=0.405, help="state-level per-column survival")
    ap.add_argument("--pE", type=float, default=0.5, help="state-level E-hit probability")
    ap.add_argument("--pHC", type=float, default=0.81, help="state-level hard-core survival")
    ap.add_argument("--n0", type=int, default=34, help="first n beyond the complete census")
    ap.add_argument("--nmax", type=int, default=120)
    args = ap.parse_args()
    rho, p = args.rho, args.p
    A = args.q24 / rho**24
    print(f"Q_n ~ {A:.4f} * {rho}^n   (anchored at Q_24 = {args.q24});  p = {p} per column in states")
    print()
    print(" n     Q_n        E[#survivors at n+2]  E[#dist-1 at n+2]   P(deep>=log2Q)  P(deep>=.75n)  P(deep>=.8n)   log2Q/n")
    tail_ce = 0.0
    tail_ce_12a = 0.0
    tail_B = 0.0
    tail_d1 = 0.0
    for n in range(7, args.nmax + 1):
        Q = A * rho**n
        K = n + 2
        e_surv = Q * p**K
        e_d1 = Q * K * p ** (K - 1) * (1 - p)
        # P(max over Q independent geometric(p) depths >= m) = 1 - (1 - p^m)^Q
        def p_deep(m: float) -> float:
            m = math.ceil(m)
            return 1.0 - math.exp(Q * math.log1p(-(p**m))) if p**m < 1 else 1.0
        lq = math.log2(Q)
        pB = p_deep(lq)
        p75 = p_deep(0.75 * n)
        p80 = p_deep(0.80 * n)
        if n >= args.n0:
            tail_ce += 2 * e_surv
            tail_ce_12a += 2 * e_surv / 4
            tail_B += 2 * pB
            tail_d1 += 2 * e_d1 / 4
        if n <= 40 or n % 10 == 0:
            print(f"{n:<4} {Q:12.3e}   {e_surv:12.3e}        {e_d1:12.3e}       {pB:10.3e}     {p75:9.3e}     {p80:9.3e}    {lq/n:6.3f}")
    print()
    print(f"sum over n >= {args.n0} (both c) of E[#states surviving n+2 columns]      = {tail_ce:.3e}")
    print(f"same with the 12a ending (factor 1/4)                                 = {tail_ce_12a:.3e}")
    print(f"sum over n >= {args.n0} (both c) of E[#distance-1 states] with 12a      = {tail_d1:.3e}")
    print(f"sum over n >= {args.n0} (both c) of P(deepest >= log2 Q_n)  [Lemma B fails] = {tail_B:.3e}")
    # observed anomalies under the null
    for (n, c, m) in ((21, 3, 16), (28, 2, 21), (31, 3, 22)):
        Q = A * rho**n
        print(f"P(deepest >= {m} at n={n}) under the null = {1 - math.exp(Q * math.log1p(-(p**m))):.3e}   (observed at c={c})")
    Q21 = A * rho**21
    e = Q21 * 23 * p**22 * (1 - p) / 4
    print(f"E[#distance-1 states with 12a at n=21] = {e:.3e}; observed 1 (fiber 10) at c=3")
    tot = sum(2 * (A * rho**n) * (n + 2) * p ** (n + 1) * (1 - p) / 4 for n in range(10, 34))
    print(f"E[#distance-1-with-12a events over n=10..33, both c] = {tot:.3e}; observed 1")


if __name__ == "__main__":
    main()

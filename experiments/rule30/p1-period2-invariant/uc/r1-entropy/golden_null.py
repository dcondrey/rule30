#!/usr/bin/env python3
"""The golden-mean null for the rotated wedge, and its two factors.

Exact decomposition.  Let Gamma_{n,c}(W) in {0..3}^k be the 4-state word
(e_n^(c), ..., e_{n+k-1}^(c)) where e_u^(c) is the unique symbol making
T[u][n] = c given e[0..u).  Then

    N_k(n,c)  = #{W : Gamma(W)[:k] is binary and hard-core (with junction)}
              = sum over hard-core binary v of M(v),   M(v) = #{W : Gamma(W)[:k] = v}
    NE_k(n,c) = #{W : Gamma(W)[:k] is binary}.

The number of hard-core words of length k over {1,2} is F_{k+2} (Fibonacci,
F_1 = F_2 = 1); with the junction symbol W[n-1] = 1 it is F_{k+1}.  Under
equidistribution of Gamma the expected counts are

    NE_k ~ 2^(n-k)
    N_k  ~ 2^(n-k) * (F_{k+2} + F_{k+1}) / 2^(k+1)   (averaging over W[n-1])
         = 2^n F_{k+3} / 4^k / 2.

Reported per (n, c, k):
    rE   = NE_k / 2^(n-k)                 (E-null ratio)
    rHC  = (N_k / NE_k) / (F_{k+3} / 2^(k+1))   (hard-core cut ratio)
    rho  = rE * rHC = N_k * 2^(k+1) / (2^(n-k) F_{k+3})   (golden null ratio)

The lemma RW-spread says rho is bounded by an absolute constant.  Its kill
test is max_k rho(n, c, k) growing with n.

Run:  cd <kernel dir> && uv run python uc/r1-entropy/golden_null.py --min 8 --max 17
"""

from __future__ import annotations

import argparse
import os
import sys
from collections import Counter
from itertools import product

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from psi_kernel import Endpoint  # noqa: E402


def fib(m: int) -> int:
    a, b = 0, 1
    for _ in range(m):
        a, b = b, a + b
    return a


def forced_run(source, target, max_steps):
    n = len(source)
    st = Endpoint()
    for s in source:
        st.append(s)
    hits, symbols = [], []
    for _ in range(max_steps):
        chosen = None
        for sym in (1, 2):
            _, diag = st.peek(sym)
            if diag[n] >> 1 == 1:
                chosen = (sym, diag[n])
                break
        sym, cell = chosen
        st.append(sym)
        symbols.append(sym)
        hit = 1 if cell == target else 0
        hits.append(hit)
        if not hit:
            break
    return hits, symbols


def census(n, target):
    NE = Counter()
    N = Counter()
    for source in product((1, 2), repeat=n):
        hits, symbols = forced_run(source, target, n + 3)
        prev = source[-1]
        hc_ok = True
        NE[0] += 1
        N[0] += 1
        for j, h in enumerate(hits):
            if not h:
                break
            k = j + 1
            NE[k] += 1
            sym = symbols[j]
            if hc_ok and not (prev == 1 and sym == 1):
                N[k] += 1
            else:
                hc_ok = False
            prev = sym
    return NE, N


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min", type=int, default=8)
    ap.add_argument("--max", type=int, default=16)
    ap.add_argument("--log", type=str, default="uc/r1-entropy/golden_null.log")
    args = ap.parse_args()
    summary = []
    with open(args.log, "w") as log:
        print("# rho = N_k 2^(k+1) / (2^(n-k) F_{k+3});  rE = NE_k / 2^(n-k);  rHC = (N_k/NE_k) / (F_{k+3}/2^(k+1))", file=log)
        for n in range(args.min, args.max + 1):
            for c in (2, 3):
                NE, N = census(n, c)
                print(f"\n# n={n} c={c}", file=log)
                print("  k   NE_k    N_k      rE      rHC      rho   golden_null_N_k", file=log)
                kmax = max(k for k in N if N[k] > 0)
                rho_max = 0.0
                rho_arg = 0
                for k in range(0, kmax + 1):
                    ne, nn = NE.get(k, 0), N.get(k, 0)
                    null_ne = 2.0 ** (n - k)
                    hc_frac = fib(k + 3) / 2.0 ** (k + 1)
                    null_n = null_ne * hc_frac
                    rE = ne / null_ne
                    rHC = (nn / ne) / hc_frac if ne else float("nan")
                    rho = nn / null_n
                    if rho > rho_max:
                        rho_max, rho_arg = rho, k
                    print(f"{k:3d} {ne:7d} {nn:6d}  {rE:7.3f}  {rHC:7.3f}  {rho:7.3f}   {null_n:10.3f}", file=log)
                # k at which the golden null drops below 1
                k_null = next(k for k in range(0, 3 * n) if 2.0 ** (n - k) * fib(k + 3) / 2.0 ** (k + 1) < 1)
                print(f"max_k rho = {rho_max:.3f} at k={rho_arg}; deepest joint k={kmax}; golden null < 1 from k={k_null}; kmax/n={kmax/n:.3f}", file=log)
                summary.append((n, c, rho_max, rho_arg, kmax, k_null))
                log.flush()
        print("\n# summary: n c max_rho at_k kmax_joint k_null(golden<1) kmax/n", file=log)
        for n, c, rm, ra, km, kn in summary:
            print(f"{n:3d} {c} {rm:7.3f} {ra:3d} {km:3d} {kn:3d} {km/n:.3f}", file=log)
    with open(args.log) as f:
        sys.stdout.write(f.read())


if __name__ == "__main__":
    main()

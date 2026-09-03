#!/usr/bin/env python3
"""Clustering diagnostics for the RW survivor counts N_k(n) from the census JSON.

null_k = 2^-k * HC_k is the independence null: one E bit per column, times the
probability that k i.i.d. uniform binary forced symbols form a hard-core word
across the junction with a uniform last prefix symbol.  R_k = N_k / (2^n null_k).

Also reported: sup_k N_k 2^(lambda k - n) for lambda in {1, 1.1, 1.2, 1.3}
(a counting lemma N_k <= C 2^(n - lambda k) needs this bounded in n), and the
local kill rate log2(N_(k-1)/N_k) over the deepest four levels.

Run:  cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/null_ratio.py
"""

from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def hardcore_null(kmax: int) -> list[float]:
    # h[k][s] = number of hard-core words of length k that may follow symbol s
    h1, h2 = 1, 1  # length 0
    out = [1.0]
    for k in range(1, kmax + 1):
        n1 = h2  # after a 1 the next symbol must be 2, then anything: h_{k-1}(2)
        n2 = h1 + h2
        h1, h2 = n1, n2
        out.append((h1 + h2) / 2 ** (k + 1))
    return out


def main() -> None:
    data = {}
    for fname in sys.argv[1:] or ("census_n07_20.json", "census_n21_30.json", "census_n31_32.json"):
        path = os.path.join(HERE, fname)
        if os.path.exists(path):
            data.update(json.load(open(path)))
    HC = hardcore_null(60)
    lambdas = (1.0, 1.1, 1.2, 1.3)
    print("n  c  deepest  R_k at k=1,2,3 | R_k at the deepest four levels (k: R)            | local kill rate, deepest 4 steps | sup_k N_k 2^(lk-n) for l=" + ",".join(map(str, lambdas)))
    for key, e in sorted(data.items(), key=lambda kv: (kv[1]["n"], kv[1]["c"])):
        n, c, N = e["n"], e["c"], e["N"]
        deepest = e["deepest"]
        R = [N[k] / (2 ** n * 2 ** (-k) * HC[k]) for k in range(len(N))]
        early = " ".join(f"{R[k]:.2f}" for k in (1, 2, 3))
        deep = " ".join(f"{k}:{R[k]:.1f}" for k in range(max(1, deepest - 3), deepest + 1))
        rates = " ".join(
            f"{math.log2(N[k-1]/N[k]):.2f}" for k in range(max(2, deepest - 3), deepest + 1) if N[k] > 0
        )
        sups = " ".join(
            f"{max(N[k] * 2 ** (lam * k - n) for k in range(1, deepest + 1)):.2f}" for lam in lambdas
        )
        print(f"{n:<3}{c:<3}{deepest:<9}{early:<18}| {deep:<48}| {rates:<32}| {sups}")
    # summary: slack and deepest/n
    print("\nn   c   deepest   need(r=0)  slack   deepest/n")
    for key, e in sorted(data.items(), key=lambda kv: (kv[1]["n"], kv[1]["c"])):
        n, c, d = e["n"], e["c"], e["deepest"]
        print(f"{n:<4}{c:<4}{d:<10}{n+2:<11}{n+2-d:<8}{d/n:.3f}")


if __name__ == "__main__":
    main()

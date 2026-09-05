#!/usr/bin/env python3
"""Kill test for injection-by-source-bits: prefix and suffix fibres on S_k.

S_k = {W in {1,2}^n : the forced RW orbit hits k times} (complete enumeration,
inj_common.all_depths, gated against rw_counts_pruned at n = 8, 9).

For each (n, c, k >= 1) with N_k = |S_k| > 0:
    fib_pre  = max fibre of  W -> W[:n-k]   on S_k   (first n-k source symbols)
    fib_suf  = max fibre of  W -> W[k:]     on S_k   (last  n-k source symbols)
    fib_pre2 = max fibre of  W -> W[:n-k+2] on S_k   (two more prefix symbols)
    null: under independent survival with p = N_k / 2^n, fibre ~ Bin(2^k, p)
          over 2^(n-k) prefixes; printed is E[#prefixes with fibre >= 5]
          = 2^(n-k) * P(Bin(2^k, p) >= 5).

A lemma "fib_pre <= 3 for all n >= n0" would give N_k <= 3 * 2^(n-k) and hence
RW.  It is refuted by any (n, c, k) with fib_pre >= 4 (printed with KILL4) or
>= 5 (KILL5).

Usage: cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-injection/prefix_fibre.py --min 8 --max 20
"""

from __future__ import annotations

import argparse
import math
import sys
import time

sys.path.insert(0, "uc/r1-injection")
from inj_common import all_depths, counts_from_depths  # noqa: E402


def binom_tail_ge5(m: int, p: float) -> float:
    if p <= 0:
        return 0.0
    q = 1 - p
    acc = 0.0
    for i in range(0, 5):
        acc += math.comb(m, i) * p ** i * q ** (m - i) if m >= i else 0.0
    return max(0.0, 1 - acc)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min", type=int, default=8)
    ap.add_argument("--max", type=int, default=20)
    args = ap.parse_args()
    print(" n c  k    N_k  fib_pre fib_pre2 fib_suf   E[#pre>=5|null]   flag")
    worst = {}
    for n in range(args.min, args.max + 1):
        for c in (2, 3):
            t0 = time.time()
            depths = all_depths(n, c)
            N = counts_from_depths(depths, n)
            D = max(k for k, v in enumerate(N) if v > 0)
            for k in range(1, D + 1):
                S = [w for w, d in depths.items() if d >= k]
                pre, pre2, suf = {}, {}, {}
                for w in S:
                    pre[w[: n - k]] = pre.get(w[: n - k], 0) + 1
                    pre2[w[: n - k + 2]] = pre2.get(w[: n - k + 2], 0) + 1
                    suf[w[k:]] = suf.get(w[k:], 0) + 1
                fp, fp2, fs = max(pre.values()), max(pre2.values()), max(suf.values())
                p = N[k] / 2 ** n
                null5 = 2 ** (n - k) * binom_tail_ge5(2 ** k, p)
                flag = "KILL5" if fp >= 5 else ("KILL4" if fp >= 4 else "")
                worst[(n, c)] = max(worst.get((n, c), 0), fp)
                print(f"{n:>2} {c} {k:>2} {N[k]:>7} {fp:>7} {fp2:>8} {fs:>7}   {null5:14.3f}   {flag}")
            print(f"   (n={n}, c={c}: max fib_pre over k = {worst[(n, c)]}, {time.time() - t0:.0f}s)")
            sys.stdout.flush()


if __name__ == "__main__":
    main()

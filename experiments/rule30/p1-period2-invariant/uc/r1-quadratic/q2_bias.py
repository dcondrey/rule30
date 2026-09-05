#!/usr/bin/env python3
"""Hit biases on the reachable set (all 2^n binary sources), unstopped forced orbit.

For each n, every W in {1,2}^n is run n+2 forced steps and the defect word
h_j = E(T[n+j][n]), j = 0..n+1, recorded (this is Psi_n(W) of the capsule).

Reported:
  (B1) single-coordinate bias  b_j = #{W : h_j = 0} - 2^(n-1), j = 0..n+1,
       with the ratio |b_j| / 2^floor(n/2);
  (B2) joint prefix counts A_k(eps) = #{W : h_0 = ... = h_(k-1) = eps},
       eps = 0 (c = 2) and 1 (c = 3), no hard-core, against 2^(n-k);
  (B3) adjacent correlation d_j = #{W : h_j = h_(j+1)} - 2^(n-1).

A quadratic form of corank r on F2^n takes each value 2^(n-1) +/- 2^((n+r)/2 - 1)
times; corank 2 (n even) or 1 (n odd) gives |b| = 2^floor(n/2).

Run:  cd <work dir> && uv run python uc/r1-quadratic/q2_bias.py --max-n 15
"""
from __future__ import annotations

import argparse
import time
from itertools import product

from qf_common import forced_orbit


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-n", type=int, default=2)
    ap.add_argument("--max-n", type=int, default=15)
    args = ap.parse_args()
    for n in range(args.min_n, args.max_n + 1):
        t0 = time.time()
        L = n + 2
        zeros = [0] * L
        same = [0] * (L - 1)
        pref0 = [0] * (L + 1)
        pref1 = [0] * (L + 1)
        for src in product((1, 2), repeat=n):
            _, hits, _ = forced_orbit(src, L)
            for j in range(L):
                if hits[j] == 0:
                    zeros[j] += 1
            for j in range(L - 1):
                if hits[j] == hits[j + 1]:
                    same[j] += 1
            k = 0
            while k < L and hits[k] == 0:
                k += 1
            for kk in range(k + 1):
                pref0[kk] += 1
            k = 0
            while k < L and hits[k] == 1:
                k += 1
            for kk in range(k + 1):
                pref1[kk] += 1
        half = 1 << (n - 1)
        scale = 1 << (n // 2)
        b = [z - half for z in zeros]
        print(f"n={n}  [{time.time()-t0:.1f}s]")
        print(f"  (B1) b_j = #{{h_j=0}} - 2^(n-1):  {b}")
        print(f"       |b_j| / 2^floor(n/2):        {[round(abs(x)/scale, 3) for x in b]}")
        print(f"  (B3) d_j = #{{h_j=h_j+1}} - 2^(n-1): {[s - half for s in same]}")
        r0 = [round(pref0[k] / 2 ** (n - k), 3) for k in range(L + 1)]
        r1 = [round(pref1[k] / 2 ** (n - k), 3) for k in range(L + 1)]
        print(f"  (B2) A_k(0) = {pref0}")
        print(f"       A_k(0)/2^(n-k) = {r0}")
        print(f"       A_k(1) = {pref1}")
        print(f"       A_k(1)/2^(n-k) = {r1}", flush=True)


if __name__ == "__main__":
    main()

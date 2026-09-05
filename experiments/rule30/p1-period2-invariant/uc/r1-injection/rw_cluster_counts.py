#!/usr/bin/env python3
"""Survivor counts modulo the invisible prefix, and distinct forced words.

For each (n, c, k) with S_k the RW survivors (rw_counts_pruned.py):

  N_k        = |S_k|
  M_k(m)     = #{ W[m:] : W in S_k }      distinct suffixes after dropping
                                           the first m source symbols
  Fq_k       = #{ Q_k(W) : W in S_k }     distinct forced words of length k

against the hard-core null  null(n', k) = 2^n' A_k / 4^k  with
A_k = (Fib(k+2) + Fib(k+1)) / 2, using n' = n for N_k and Fq_k and
n' = n - m for M_k(m).  Printed per (n, c): the maximum over k >= 1 of each
ratio and its k, for m = 4.

Usage: uv run python uc/r1-injection/rw_cluster_counts.py --min 8 --max 18 --m 4
"""

from __future__ import annotations

import argparse
import sys
import time
from itertools import product

sys.path.insert(0, ".")
sys.path.insert(0, "uc/r1-injection")
from rw_counts import forced_flags  # noqa: E402


def fib(k: int) -> int:
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def null(nprime: int, k: int) -> float:
    return 2 ** nprime * (fib(k + 2) + fib(k + 1)) / 2 / 4 ** k


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min", type=int, default=8)
    parser.add_argument("--max", type=int, default=18)
    parser.add_argument("--m", type=int, default=4)
    args = parser.parse_args()
    m = args.m
    print(f" n c  D   maxN/null(k)   maxM{m}/null(k)   maxFq/null(k)   time   M{m}_k   Fq_k")
    for n in range(args.min, args.max + 1):
        for target in (2, 3):
            t0 = time.time()
            kmax = n + 2
            N = [0] * (kmax + 1)
            suffix_sets: list[set] = [set() for _ in range(kmax + 1)]
            forced_sets: list[set] = [set() for _ in range(kmax + 1)]
            for source in product((1, 2), repeat=n):
                e, h, forced = forced_flags(source, target)
                depth = 0
                for k in range(kmax):
                    if e[k] and h[k]:
                        depth += 1
                    else:
                        break
                suf = source[m:]
                for k in range(depth + 1):
                    N[k] += 1
                    suffix_sets[k].add(suf)
                    forced_sets[k].add(tuple(forced[:k]))
            M = [len(s) for s in suffix_sets]
            Fq = [len(s) for s in forced_sets]
            deepest = max(k for k in range(kmax + 1) if N[k] > 0)
            rN = max((N[k] / null(n, k), k) for k in range(1, kmax + 1))
            rM = max((M[k] / null(n - m, k), k) for k in range(1, kmax + 1))
            rF = max((Fq[k] / null(n, k), k) for k in range(1, kmax + 1))
            print(
                f"{n:>2} {target} {deepest:>3}   {rN[0]:5.2f} ({rN[1]:>2})     "
                f"{rM[0]:5.2f} ({rM[1]:>2})      {rF[0]:5.2f} ({rF[1]:>2})   "
                f"{time.time() - t0:4.0f}s   {M[1:deepest + 1]}   {Fq[1:deepest + 1]}"
            )
            sys.stdout.flush()


if __name__ == "__main__":
    main()

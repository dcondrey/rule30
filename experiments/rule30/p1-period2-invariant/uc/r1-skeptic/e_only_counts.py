#!/usr/bin/env python3
"""Exact E-only survivor counts N_k^E(n, c) (hard-core condition switched off).

Question: is the first E constraint exactly balanced, N_1^E = 2^(n-1)?  And at
which level does N_k^E first depart from 2^(n-k)?  N_k^E is the BWH+ census
restricted to one target constant, so N_{n+2}^E > 0 is exactly a BWH+ failure.

Run:  cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/e_only_counts.py --max-n 22
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rw_bitsliced import full_census  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-n", type=int, default=6)
    ap.add_argument("--max-n", type=int, default=22)
    args = ap.parse_args()
    print("n  c  N_1^E - 2^(n-1)   N_k^E / 2^(n-k) for k=1..   (deepest E-only level, count)")
    for n in range(args.min_n, args.max_n + 1):
        for c in (2, 3):
            N, *_ = full_census(n, c, 22, n + 4, want_witness_masks=False, hardcore=False)
            deepest = max(k for k in range(len(N)) if N[k] > 0)
            ratios = " ".join(f"{N[k]/2**(n-k):.2f}" for k in range(1, deepest + 1))
            print(f"{n:<3}{c:<3}{N[1]-2**(n-1):<18}{ratios}   ({deepest}, {N[deepest]})")
            sys.stdout.flush()


if __name__ == "__main__":
    main()

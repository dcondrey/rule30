#!/usr/bin/env python3
"""Survival of DISTINCT forced-process states q(W), and the BWH+ n=15 fiber check.

q(W) = quotient of column n-1 on depths [-n, n-1] (see quotient_multiplicity.py).
The forced RW future is a function of q(W) alone, so N_k = sum over surviving q
of the fiber size.  This script measures

  D_k(n)  = number of distinct q surviving k forced columns (both targets c),
  the kill rate of distinct states (bits per column),
  the mean log2 fiber size of survivors at each level (multiplicity bias),

and verifies directly that the 18 recorded BWH+ n=15 sources with constant
Psi_0..Psi_15 are exactly one fiber of q, i.e. one state with one future.

Run:  cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/state_survival.py
"""

from __future__ import annotations

import argparse
import math
import os
import sys
from collections import defaultdict
from itertools import product

KERNEL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, KERNEL_DIR)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from psi_kernel import Endpoint, psi  # noqa: E402
from quotient_multiplicity import quotient_column  # noqa: E402
from rw_bitsliced import reference_path  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-n", type=int, default=10)
    ap.add_argument("--max-n", type=int, default=16)
    args = ap.parse_args()

    # 1. BWH+ n=15 fiber check
    suffix = "211212112"
    const = []
    fib = defaultdict(list)
    for p in product("12", repeat=6):
        w = "".join(p) + suffix
        _, defect = psi(tuple(int(ch) for ch in w))
        if len(set(defect[:16])) == 1:
            const.append("".join(p))
        fib[quotient_column(w)].append("".join(p))
    biggest = max(fib.values(), key=len)
    print(f"BWH+ n=15: {len(const)} prefixes with constant Psi_0..Psi_15: {' '.join(const)}")
    print(f"           largest q-fiber over the 64 prefixes has {len(biggest)} members; identical sets: {sorted(const) == sorted(biggest)}")

    # 2. distinct-state survival
    for n in range(args.min_n, args.max_n + 1):
        K = n + 4
        fibers = defaultdict(list)
        for w in product("12", repeat=n):
            word = "".join(w)
            fibers[quotient_column(word)].append(word)
        for c in (2, 3):
            D = [0] * (K + 1)
            N = [0] * (K + 1)
            logmult = [0.0] * (K + 1)
            for q, ws in fibers.items():
                run, _, _, _ = reference_path(ws[0], c, K)
                # every member of the fiber has the same run (checked on a sample below)
                for k in range(0, min(run, K) + 1):
                    D[k] += 1
                    N[k] += len(ws)
                    logmult[k] += math.log2(len(ws))
            deepest = max(k for k in range(K + 1) if D[k] > 0)
            slopes = [math.log2(D[k] / D[k + 1]) if D[k + 1] > 0 else float("nan") for k in range(deepest)]
            avg_slope = math.log2(D[1] / D[deepest]) / (deepest - 1) if deepest > 1 else float("nan")
            print(
                f"n={n:<3} c={c} Q_n={D[0]:<6} D_k={D[:deepest+1]}  N_k={N[:deepest+1]}"
            )
            print(
                f"           mean log2 fiber of survivors by k: {[round(logmult[k]/D[k],2) for k in range(deepest+1)]}"
                f"   distinct-state kill rate k=1..deepest: {avg_slope:.3f} bits/col"
            )
        # sanity: fiber members share the run (sample)
        import random

        rng = random.Random(n)
        for q in rng.sample(list(fibers), min(50, len(fibers))):
            ws = fibers[q]
            runs = {reference_path(w, 3, K)[0] for w in ws} | {reference_path(w, 2, K)[0] + 100 for w in ws}
            assert len(runs) == (2 if len(ws) >= 1 else 0), (n, q, ws, runs)
        sys.stdout.flush()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Complete RW census for one (n, c) with the bit-sliced kernel, as a kill test for the halving lemmas.

Thin driver around `rw_bitsliced.full_census` (validated there against
psi_kernel and rw_margin) so that the two targets c = 2, 3 can run as two
processes.  Prints the same summary line as rw_bitsliced.py and writes the
per-level counts to census_n{n}_c{c}.json in this directory.

Lemma SOURCE-HALVING fails iff some N_k > 2^(n-k); Lemma STATE-HALVING fails
iff deepest > log2 Q_n (Q_n ~ 1.44 * 1.765^n).  Both are printed.

Run:  cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/census_one.py --n 34 --c 2
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))

from rw_bitsliced import common_suffix, full_census  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--c", type=int, required=True, choices=(2, 3))
    ap.add_argument("--block", type=int, default=22)
    args = ap.parse_args()
    n, c = args.n, args.c
    K = n + 4
    t0 = time.time()
    N, exact, e12, wit, near = full_census(n, c, args.block, K)
    dt = time.time() - t0
    deepest = max(k for k in range(len(N)) if N[k] > 0)
    ratios = [(N[k] / 2 ** (n - k), k) for k in range(1, len(N)) if N[k] > 0]
    rmax, kmax = max(ratios)
    lq = math.log2(1.4417 * 1.765**n)
    w = wit.get(deepest, [])
    ce = any(e12[(n + 2 + r, 0)] > 0 for r in range(3))
    print(f"n={n} c={c} deepest={deepest} need={n+2} slack={n+2-deepest} "
          f"N_k={N[:min(len(N), 26)]} max_k N_k/2^(n-k)={rmax:.3f} at k={kmax} "
          f"witnesses@deepest={len(w)} suffix={common_suffix(w)} log2Q_n~{lq:.2f} "
          f"SOURCE-HALVING={'FAIL' if rmax > 1 else 'holds'} STATE-HALVING={'FAIL' if deepest > lq else 'holds'} "
          f"RW_counterexample={ce} [{dt:.0f}s]")
    out = {
        "n": n, "c": c, "deepest": deepest, "N": N,
        "exact": {f"{k},{v}": val for (k, v), val in exact.items()},
        "exact_12a": {f"{k},{v}": val for (k, v), val in e12.items()},
        "witnesses": {str(k): v for k, v in wit.items()},
        "seconds": dt,
    }
    with open(os.path.join(HERE, f"census_n{n}_c{c}.json"), "w") as fh:
        json.dump(out, fh)


if __name__ == "__main__":
    main()

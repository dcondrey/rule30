#!/usr/bin/env python3
"""Conditional pass rates of the E constraint and the hard-core condition, per level.

For the survivors A_k of k forced columns: p_E(k) = fraction whose E bit at
column n+k matches E(c); p_HC(k) = fraction whose forced symbol at column n+k
keeps the word hard-core.  The independence null is p_E = 1/2 at every level.
A rise of p_E at the deep levels would be the clustering that could defeat a
counting lemma; a flat 1/2 is the "one bit unconditionally" behaviour the
program needs.

Run:  cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/kill_split.py --min-n 12 --max-n 26
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rw_bitsliced import full_census  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-n", type=int, default=12)
    ap.add_argument("--max-n", type=int, default=26)
    args = ap.parse_args()
    pooled = {}  # (k - deepest) offset -> [E_pass, A, HC_pass]
    pooled_abs = {}  # k -> [E_pass, A]
    for n in range(args.min_n, args.max_n + 1):
        for c in (2, 3):
            N, exact, e12, wit, near = full_census(n, c, 22, n + 4, want_witness_masks=False)
            deepest = max(k for k in range(len(N)) if N[k] > 0)
            rows = []
            for k in range(0, deepest + 1):
                A = exact.get(("A", k + 1), 0)
                E = exact.get(("E", k + 1), 0)
                H = exact.get(("HC", k + 1), 0)
                if A == 0:
                    continue
                rows.append(f"{k}:{E/A:.2f}/{H/A:.2f}")
                off = k - deepest
                pooled.setdefault(off, [0, 0, 0])
                pooled[off][0] += E
                pooled[off][1] += A
                pooled[off][2] += H
                pooled_abs.setdefault(k, [0, 0])
                pooled_abs[k][0] += E
                pooled_abs[k][1] += A
            print(f"n={n:<3} c={c} deepest={deepest:<3} p_E/p_HC by level k: " + " ".join(rows))
            sys.stdout.flush()
    print("\npooled by offset from the deepest level (k - deepest): p_E, p_HC, survivors A")
    for off in sorted(pooled):
        E, A, H = pooled[off]
        print(f"  k-deepest={off:<4} p_E={E/A:.4f} p_HC={H/A:.4f} A={A}")
    print("\npooled by absolute level k: p_E, survivors A")
    for k in sorted(pooled_abs):
        E, A = pooled_abs[k]
        print(f"  k={k:<3} p_E={E/A:.4f} A={A}")


if __name__ == "__main__":
    main()

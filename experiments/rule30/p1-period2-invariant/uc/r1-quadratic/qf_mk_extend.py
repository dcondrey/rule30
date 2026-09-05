#!/usr/bin/env python3
"""Kill test driver for the column-count lemma: M_k <= 2^(n-k) for n >= 4.

Prints, for each (n, c) in the requested range, the full M_k list, the
maximal ratio M_k / 2^(n-k) over k, and VIOLATION if any ratio exceeds 1.

Run:  cd <work dir> && uv run python uc/r1-quadratic/qf_mk_extend.py --min-n 18 --max-n 19
"""
from __future__ import annotations
import argparse, time
from qf_survivors import census

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-n", type=int, default=18)
    ap.add_argument("--max-n", type=int, default=19)
    args = ap.parse_args()
    for n in range(args.min_n, args.max_n + 1):
        for c in (2, 3):
            t0 = time.time()
            rows = census(n, c)
            ms = [M for (N, M, _, _) in rows if N > 0]
            ns = [N for (N, M, _, _) in rows if N > 0]
            ratios = [M / 2 ** (n - k) for k, (N, M, _, _) in enumerate(rows) if N > 0]
            worst = max(ratios)
            flag = "VIOLATION" if worst > 1 else "ok"
            print(f"n={n} c={c} deepest k={len(ms)-1} need={n+2}  max_k M_k/2^(n-k)={worst:.3f} at k={ratios.index(worst)}  {flag}   [{time.time()-t0:.0f}s]")
            print(f"   M_k = {ms}")
            print(f"   N_k = {ns}", flush=True)

if __name__ == "__main__":
    main()

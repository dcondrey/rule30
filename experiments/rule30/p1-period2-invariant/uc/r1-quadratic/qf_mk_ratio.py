#!/usr/bin/env python3
"""Max ratio M_k / 2^(n-k) and N_k / 2^(n-k) over k, for n = 1..max_n.

M_k = distinct quotient letter words of column n+k-1 among survivors of k
hits with hard-core (as in qf_survivors.py); N_k = surviving sources.

Run:  cd <work dir> && uv run python uc/r1-quadratic/qf_mk_ratio.py --max-n 17
"""
from __future__ import annotations
import argparse, time
from qf_survivors import census

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-n", type=int, default=16)
    args = ap.parse_args()
    print(" n  c   max_k M_k/2^(n-k) (at k)     max_k N_k/2^(n-k) (at k)    M_k list")
    for n in range(1, args.max_n + 1):
        for c in (2, 3):
            t0 = time.time()
            rows = census(n, c)
            best_m, best_n = (0.0, -1), (0.0, -1)
            for k, (N, M, _, _) in enumerate(rows):
                if N == 0:
                    continue
                rm = M / 2 ** (n - k)
                rn = N / 2 ** (n - k)
                if rm > best_m[0]:
                    best_m = (rm, k)
                if rn > best_n[0]:
                    best_n = (rn, k)
            ms = [M for (N, M, _, _) in rows if N > 0]
            print(f"{n:>2}  {c}   {best_m[0]:6.3f} (k={best_m[1]})            {best_n[0]:6.3f} (k={best_n[1]})           {ms}   [{time.time()-t0:.1f}s]")

if __name__ == "__main__":
    main()

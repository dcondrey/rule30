#!/usr/bin/env python3
"""Fiber sizes of the source-to-column map W -> quotient word of column n-1.

Reports, per n: number of distinct quotient words M_0, max fiber size, the
fiber-size histogram, and log2(M_0)/n.

Run:  cd <work dir> && uv run python uc/r1-quadratic/qf_fibers.py --max-n 18
"""
from __future__ import annotations
import argparse, math, time
from collections import Counter
from itertools import product
from qf_common import Endpoint

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-n", type=int, default=18)
    args = ap.parse_args()
    for n in range(1, args.max_n + 1):
        t0 = time.time()
        fib = Counter()
        for src in product((1, 2), repeat=n):
            st = Endpoint()
            for s in src:
                st.append(s)
            cells = [st.column[-d] if d <= 0 else st.diagonal[d] for d in range(-n, n)]
            fib["".join("0" if t == 0 else ("2" if t == 2 else "x") for t in cells)] += 1
        hist = Counter(fib.values())
        M0 = len(fib)
        print(f"n={n:<3} M_0={M0:<7} log2(M_0)/n={math.log2(M0)/n:.3f}  max fiber={max(fib.values())}  histogram={dict(sorted(hist.items()))}   [{time.time()-t0:.0f}s]", flush=True)

if __name__ == "__main__":
    main()

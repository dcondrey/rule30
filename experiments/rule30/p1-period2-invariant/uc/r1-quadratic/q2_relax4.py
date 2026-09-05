#!/usr/bin/env python3
"""Four-state-endpoint relaxation of (RW): drop the n source-side constraints.

In the diagonal form every D in {0..3}^n gives the unique word g of length
L = 2n+2 with P^n(I(g)) = c^(n+2).  (RW) asks for g binary throughout with
f[n:] hard-core (junction included) and f[-3:-1] = 12.  This script keeps
only the REGION conditions:
    (i)   e_u binary for u = n .. 2n+1,
    (ii)  hard-core on e_n .. e_{2n+1}, and the junction e_{n-1} e_n != 11,
    (iii) e_{2n-1} e_{2n} = 12,
and reports how many of the 4^n diagonals satisfy them, how many of those
also have e_{n-1} binary, and the histogram of the number of binary source
symbols among the survivors.  Counting predicts about 2^(0.585 n - 4.4)
survivors; any survivor with all n source symbols binary is an (RW)
counterexample (none expected; the search is complete).

Run:  cd <work dir> && uv run python uc/r1-quadratic/q2_relax4.py --max-n 9
"""
from __future__ import annotations

import argparse
import time
from collections import Counter
from itertools import product

from qf_common import E, endpoint_of, region


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-n", type=int, default=3)
    ap.add_argument("--max-n", type=int, default=9)
    args = ap.parse_args()
    for n in range(args.min_n, args.max_n + 1):
        for c in (2, 3):
            t0 = time.time()
            L = 2 * n + 2
            hits_only = 0
            with_hc = 0
            with_12a = 0
            bin_prev = 0
            hist = Counter()
            examples = []
            for D in product(range(4), repeat=n):
                cols = region(D, c, L)
                g = endpoint_of(cols)
                if any(E(g[u]) != 0 for u in range(n, L)):
                    continue
                hits_only += 1
                ok = True
                prev = g[n - 1]
                for u in range(n, L):
                    if prev == 1 and g[u] == 1:
                        ok = False
                        break
                    prev = g[u]
                if not ok:
                    continue
                with_hc += 1
                if not (g[L - 3] == 1 and g[L - 2] == 2):
                    continue
                with_12a += 1
                if g[n - 1] in (1, 2):
                    bin_prev += 1
                nb = sum(1 for u in range(n) if g[u] in (1, 2))
                hist[nb] += 1
                if len(examples) < 2:
                    examples.append(g)
            print(f"n={n} c={c}: 4^n={4**n}  region hits: {hits_only}  +hard-core: {with_hc}  +12a: {with_12a}  "
                  f"(of which e_(n-1) binary: {bin_prev})  binary-source-symbol histogram: {dict(sorted(hist.items()))}  "
                  f"RW counterexamples: {hist.get(n, 0)}   [{time.time()-t0:.0f}s]")
            for g in examples:
                print(f"    g = {''.join(map(str, g))}   (source {''.join(map(str, g[:n]))} | region {''.join(map(str, g[n:]))})")
            print(flush=True)


if __name__ == "__main__":
    main()

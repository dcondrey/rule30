#!/usr/bin/env python3
"""Influence matrix in the reduced diagonal coordinates x = (H(D_u))_{u<n}.

Same statistic as qf_influence.py (1) but the single-bit flips are applied
to x, the free bits of the diagonal form after the n triangular constraints
are solved, rather than to the source word W.  A bit with influence 1 at
some level would be a triangular injection coordinate.

Run:  cd <work dir> && uv run python uc/r1-quadratic/qf_influence_x.py
"""

from __future__ import annotations

import argparse
import time

from qf_common import E, endpoint_of, forced_orbit, region
from qf_degrees import reduced_diag


def survival_of_source(src: tuple[int, ...], n: int, c: int) -> int:
    symbols, hits, _ = forced_orbit(src, n + 2)
    eps = E(c)
    prev = src[-1]
    k = 0
    for j in range(n + 2):
        if hits[j] != eps:
            break
        if prev == 1 and symbols[j] == 1:
            break
        prev = symbols[j]
        k += 1
    return k


def influence_x(n: int, c: int) -> None:
    L = 2 * n + 2
    surv = {}
    for x in range(1 << n):
        diag = reduced_diag(x, n, c)
        g = endpoint_of(region(diag, c, L))
        src = g[:n]
        assert all(s in (1, 2) for s in src)
        surv[x] = survival_of_source(src, n, c)
    print(f"n={n} c={c}  influence of diagonal bit x_j on level-k outcome among level-(k-1) survivors")
    print("   k   N_(k-1)  " + " ".join(f"j={j:<2}" for j in range(n)) + "   any-bit")
    for k in range(1, n + 3):
        base = [x for x, v in surv.items() if v >= k - 1]
        if not base:
            break
        counts = [0] * n
        anyc = 0
        for x in base:
            found = False
            for j in range(n):
                y = x ^ (1 << j)
                if surv[y] >= k - 1 and ((surv[x] >= k) != (surv[y] >= k)):
                    counts[j] += 1
                    found = True
            if found:
                anyc += 1
        print(f"  {k:>2}  {len(base):>7}  " + " ".join(f"{counts[j]/len(base):4.2f}" for j in range(n)) + f"   {anyc/len(base):4.2f}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, nargs="*", default=[10, 12])
    args = ap.parse_args()
    for n in args.n:
        for c in (2, 3):
            t0 = time.time()
            influence_x(n, c)
            print(f"   [{time.time()-t0:.1f}s]")


if __name__ == "__main__":
    main()

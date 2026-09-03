#!/usr/bin/env python3
"""The screened golden null: distinct futures against the Fibonacci count.

D_k(n,c) = number of screening classes (W[m:], e[n:n+2m]), m = floor(k/2),
among joint survivors at level k (k hits T[u][n] = c at u = n..n+k-1 with
hard-core forced symbols including the junction with W[n-1]).  All members
of a class share their entire future (proved from the stencil, checked in
screening.py), so D_k is non-increasing in k and D_k = 0 iff N_k = 0.

Golden null for level k:  G(n,k) = 2^(n-k) * F_{k+3} / 2^(k+1)
(F Fibonacci, F_1 = F_2 = 1; F_{k+3}/2^(k+1) is the fraction of length-k
binary words that are hard-core, averaged over the junction symbol).

Lemma (screened golden null): D_k(n,c) <= C * G(n,k) for an absolute C.
At k = n+2 (the r = 0 requirement) G = F_{n+5} / 2^(n+5) -> 0, so the lemma
implies N_{n+2} = 0 for every n with C * G(n, n+2) < 1, i.e. RW at those n;
r = 1, 2 follow because N_k is non-increasing in k.

This script prints D_k, G, and the ratio for n in a range, the maximum
ratio per n, and the smallest n_0 from which C * G(n, n+2) < 1 for
C = 2, 4, 8, 16, 32.

Run:  cd <kernel dir> && uv run python uc/r1-entropy/screened_null.py --min 8 --max 18
"""

from __future__ import annotations

import argparse
import os
import sys
from collections import defaultdict
from itertools import product

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from psi_kernel import Endpoint  # noqa: E402


def fib(m: int) -> int:
    a, b = 0, 1
    for _ in range(m):
        a, b = b, a + b
    return a


def golden(n: int, k: int) -> float:
    return 2.0 ** (n - k) * fib(k + 3) / 2.0 ** (k + 1)


def forced_joint(source, target, max_steps):
    """Forced symbols and joint level (hits and hard-core), stopping at death."""
    n = len(source)
    st = Endpoint()
    for s in source:
        st.append(s)
    syms = []
    prev = source[-1]
    k = 0
    for _ in range(max_steps):
        for sym in (1, 2):
            _, diag = st.peek(sym)
            if diag[n] >> 1 == 1:
                break
        st.append(sym)
        syms.append(sym)
        if diag[n] != target or (prev == 1 and sym == 1):
            break
        prev = sym
        k += 1
    return syms, k


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min", type=int, default=8)
    ap.add_argument("--max", type=int, default=17)
    ap.add_argument("--log", type=str, default="uc/r1-entropy/screened_null.log")
    args = ap.parse_args()
    with open(args.log, "w") as log:
        summary = []
        for n in range(args.min, args.max + 1):
            for c in (2, 3):
                data = {}
                for W in product((1, 2), repeat=n):
                    data[W] = forced_joint(W, c, n + 3)
                kmax = max(v[1] for v in data.values())
                print(f"\n# n={n} c={c}  kmax={kmax}", file=log)
                print("  k    N_k    D_k     G(n,k)   D_k/G   N_k/G", file=log)
                worst = (0.0, 0)
                for k in range(1, kmax + 1):
                    m = k // 2
                    classes = defaultdict(int)
                    Nk = 0
                    for W, (syms, lev) in data.items():
                        if lev >= k:
                            classes[(W[m:], tuple(syms[:2 * m]))] += 1
                            Nk += 1
                    Dk = len(classes)
                    G = golden(n, k)
                    ratio = Dk / G
                    if ratio > worst[0]:
                        worst = (ratio, k)
                    print(f"{k:3d} {Nk:6d} {Dk:6d}  {G:9.3f}  {ratio:6.3f}  {Nk/G:6.3f}", file=log)
                print(f"max_k D_k/G = {worst[0]:.3f} at k={worst[1]}", file=log)
                summary.append((n, c, kmax, worst[0], worst[1]))
                log.flush()
        print("\n# summary: n c kmax max_D_ratio at_k", file=log)
        for n, c, km, r, k in summary:
            print(f"{n:3d} {c} {km:3d} {r:7.3f} {k:3d}", file=log)
        print("\n# n_0(C): smallest n from which C * G(n, n+2) < 1 for all larger n", file=log)
        for C in (2, 4, 8, 16, 32, 64):
            n0 = next(n for n in range(1, 200) if all(C * golden(m, m + 2) < 1 for m in range(n, 200)))
            print(f"C={C:3d}: n_0={n0}   (G(n,n+2)=F_(n+5)/2^(n+5): G(10,12)={golden(10,12):.4f} G(17,19)={golden(17,19):.5f})", file=log)
    with open(args.log) as f:
        sys.stdout.write(f.read())


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Class structure of the forced map: how many distinct (Q_n, Psi_n) pairs do
the 2^n binary sources produce, what are the class sizes, and does counting
survivors by CLASS instead of by source remove the R_k clustering of
PREREG-psi-constraint-counting.md?

Also: the e_0 flip.  Fraction of sources W for which (Q,Psi)(W) == (Q,Psi)(W
with e_0 flipped), per n, and the same for e_1 given e_0 flipped etc.
"""
from __future__ import annotations

import sys
from itertools import product
from collections import Counter, defaultdict

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
from psi_kernel import psi  # noqa: E402


def const_prefix(word) -> int:
    k = 0
    while k + 1 < len(word) and word[k + 1] == word[0]:
        k += 1
    return k


def main() -> None:
    nmin = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 15
    print("n  2^n   classes  2^n/classes  maxclass  e0-invariant  e1-invariant  e2-invariant  | class-based survivors: k : N_k(sources) N_k(classes) null_k=classes*2^-(k+1) R_k(class)")
    for n in range(nmin, nmax + 1):
        data = {}
        for W in product((1, 2), repeat=n):
            data[W] = psi(W)
        classes = Counter(data.values())
        inv = [0, 0, 0]
        for W, v in data.items():
            for i in range(3):
                if i < n:
                    W2 = W[:i] + (3 - W[i],) + W[i + 1:]
                    inv[i] += data[W2] == v
        N = 2 ** n
        # survivors by k
        by_src = Counter()
        by_cls = defaultdict(set)
        for W, (Q, P) in data.items():
            k = const_prefix(P)
            for kk in range(k + 1):
                by_src[kk] += 1
                by_cls[kk].add((Q, P))
        tail = []
        for k in range(n + 2):
            ns = by_src.get(k, 0)
            nc = len(by_cls.get(k, ()))
            null = len(classes) * 2.0 ** -(k + 1)
            if ns == 0:
                break
            if k >= n - 6:
                tail.append(f"{k}:{ns}/{nc}/{null:.2f}/{nc/null:.2f}")
        print(f"{n:2d} {N:6d} {len(classes):7d} {N/len(classes):6.2f} {max(classes.values()):5d}  {inv[0]/N:.4f}  {inv[1]/N:.4f}  {inv[2]/N:.4f}  | " + " ".join(tail))
        sizes = Counter(classes.values())
        print("     class-size histogram: " + ", ".join(f"{sz}:{cnt}" for sz, cnt in sorted(sizes.items())[:14]) + (" ..." if len(sizes) > 14 else ""))


if __name__ == "__main__":
    main()

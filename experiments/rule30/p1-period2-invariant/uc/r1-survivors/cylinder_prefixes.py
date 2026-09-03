#!/usr/bin/env python3
"""Within the n=15 survivor cylinder (suffix e_5..e_14 = 2211212112), tabulate
(Q, Psi) over all 32 prefixes e_0..e_4, and measure how many prefixes share
the survivors' (Q, Psi).  Then, for general n, measure the dependency cone:
for each j, the number of distinct values Psi_j takes as the prefix e_0..e_{s-1}
varies with the suffix fixed, averaged over suffixes.  The cone predicts Psi_j
is independent of e_0..e_{s-1} once s <= ceil((j-1)/2) AND the forced symbols
agree; the measurement separates the two effects.
"""
from __future__ import annotations

import sys
from itertools import product
from collections import Counter, defaultdict

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
from psi_kernel import psi  # noqa: E402


def s(x) -> str:
    return "".join(map(str, x))


def main() -> None:
    n = 15
    suffix = tuple(map(int, "2211212112"))
    print(f"n={n}, suffix e_5..e_14 = {s(suffix)}; all 32 prefixes:")
    table = Counter()
    for pre in product((1, 2), repeat=5):
        W = pre + suffix
        Q, P = psi(W)
        k = 0
        while k + 1 < len(P) and P[k + 1] == P[0]:
            k += 1
        table[(Q, P)] += 1
        print(f"  {s(pre)}|{s(suffix)}  Q={s(Q)}  Psi={s(P)}  const-prefix k={k}")
    print(f"distinct (Q,Psi) over the 32 prefixes: {len(table)}")
    for (Q, P), c in table.most_common():
        print(f"  x{c}: Q={s(Q)} Psi={s(P)}")

    # Cone measurement: for n in 8..12, s = 1..n-1, j = 0..n+1:
    # fraction of suffix classes (fixed e_s..e_{n-1}) on which Psi_j is constant across the 2^s prefixes,
    # and fraction on which (Q_0..Q_{j-1}, Psi_j) ... simpler: on which Psi_j is constant given equal Q_0..Q_{j-1}.
    for n in (10, 12):
        print(f"\nn={n}: rows s (free prefix length), cols j; entry = fraction of suffix classes with Psi_j constant over all 2^s prefixes")
        data = {}
        for W in product((1, 2), repeat=n):
            data[W] = psi(W)
        hdr = "s\\j " + " ".join(f"{j:4d}" for j in range(n + 2))
        print(hdr)
        for sfree in range(1, n):
            classes = defaultdict(list)
            for W, (Q, P) in data.items():
                classes[W[sfree:]].append(P)
            row = []
            for j in range(n + 2):
                const = sum(1 for Ps in classes.values() if len({P[j] for P in Ps}) == 1)
                row.append(f"{const / len(classes):4.2f}")
            print(f"{sfree:3d}  " + " ".join(row))
        print(f"cone prediction: Psi_j independent of e_0..e_{{s-1}} when s <= ceil((j-1)/2), i.e. j >= 2s+1... only if the forced symbols also agree")


if __name__ == "__main__":
    main()

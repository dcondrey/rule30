#!/usr/bin/env python3
"""Is the virtual continuation e*_u a fair coin in E and in H?

For each n and c, over all binary W and u in [n, n+L), tabulate:
  * P(E(e*_u) = 0) as a function of j = u - n (binary-ness, the BWH+ constraint);
  * P(H(e*_u) = 0) as a function of j (e* = 1 or 0);
  * P(e*_u = 1 and e*_{u+1} = 1 | both binary) (the hard-core kill rate);
  * lag-1..4 autocorrelations of E(e*_u) and of H(e*_u) along u;
  * the run-length distribution of binary runs in e* against geometric(1/2).
The coin null: P(E=0) = 1/2, autocorrelations 0, runs geometric.  A structured
death mechanism would show as a deviation.
"""
from __future__ import annotations

import sys
from itertools import product
from collections import Counter

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-survivors")
from virtual_continuation import virtual, E  # noqa: E402


def H(t: int) -> int:
    return t >> 1


def main() -> None:
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 64
    ns = [int(x) for x in sys.argv[2:]] or [8, 10, 12]
    for n in ns:
        for c in (2, 3):
            cntE = Counter()
            cntH = Counter()
            tot = Counter()
            pair11 = 0
            pairbin = 0
            acE = [0.0] * 5
            acH = [0.0] * 5
            nac = 0
            runs = Counter()
            for W in product((1, 2), repeat=n):
                tops, _ = virtual(W, c, n + L)
                e = [E(t) for t in tops]
                h = [H(t) for t in tops]
                for j, (x, y) in enumerate(zip(e, h)):
                    tot[j] += 1
                    cntE[j] += x == 0
                    cntH[j] += y == 0
                for j in range(len(tops) - 1):
                    if e[j] == 0 and e[j + 1] == 0:
                        pairbin += 1
                        if tops[j] == 1 and tops[j + 1] == 1:
                            pair11 += 1
                for lag in range(1, 5):
                    for j in range(len(e) - lag):
                        acE[lag] += (1 - 2 * e[j]) * (1 - 2 * e[j + lag])
                        acH[lag] += (1 - 2 * h[j]) * (1 - 2 * h[j + lag])
                nac += 1
                cur = 0
                for x in e:
                    if x == 0:
                        cur += 1
                    else:
                        if cur:
                            runs[cur] += 1
                        cur = 0
                if cur:
                    runs[cur] += 1
            N = 2 ** n
            print(f"\nn={n} c={c}, L={L}, {N} sources")
            print("  j: P(E=0)  P(H=0)   for j = 0..min(L,24)-1")
            for j in range(min(L, 24)):
                print(f"  {j:2d}: {cntE[j]/tot[j]:.3f}  {cntH[j]/tot[j]:.3f}")
            pe = sum(cntE.values()) / sum(tot.values())
            ph = sum(cntH.values()) / sum(tot.values())
            print(f"  overall P(E=0)={pe:.4f}  P(H=0)={ph:.4f}  P(11 | adjacent binary)={pair11/max(pairbin,1):.4f} (coin: 0.25)")
            M = N * (L - 1)
            print("  autocorrelation of (1-2E): " + " ".join(f"lag{l}={acE[l]/(N*(L-l)):+.4f}" for l in range(1, 5)))
            print("  autocorrelation of (1-2H): " + " ".join(f"lag{l}={acH[l]/(N*(L-l)):+.4f}" for l in range(1, 5)))
            totruns = sum(runs.values())
            print("  binary run lengths (observed fraction vs geometric 2^-r): " + ", ".join(f"{r}:{runs[r]/totruns:.3f}/{2.0**-r:.3f}" for r in range(1, 9)))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Is there a LOCAL pattern that makes a source symbol irrelevant?

For a source e_0..e_{U-1}, symbol e_i is ABSORBED at column v if
col_v(e) == col_v(e with e_i flipped) (full four-state column).  Absorption is
permanent: later columns are functions of the current column and later
symbols.  Question: does a fixed pattern P on e_{i+1}..e_{i+p} force absorption
of e_i by column i+p+q, for EVERY prefix e_0..e_{i-1} and every later suffix?

For i = 0..IMAX and p = 1..PMAX, over all sources of length U, group by the
pattern e_{i+1}..e_{i+p}; report, per pattern, the fraction of sources for
which e_i is absorbed by column U-1, and the minimum over contexts.  A pattern
with fraction 1.0 at every i tested is a candidate local-absorption law; the
smallest such p is what a growth-rate lemma would use.  Also reports the
overall absorption fraction of e_i at column U-1 (no pattern).
"""
from __future__ import annotations

import sys
from collections import defaultdict
from itertools import product

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
from psi_kernel import CONE, BOUNDARY  # noqa: E402


def column_at(endpoint: tuple[int, ...], v: int) -> bytes:
    prev = None
    for k in range(v + 1):
        e = endpoint[k]
        col = [0] * (2 * k + 2)
        col[0] = e
        col[1] = BOUNDARY[e]
        for d in range(-k + 1, k + 1):
            col[d + k + 1] = CONE[prev[d + k - 1]][col[d + k]]
        prev = col
    return bytes(prev)


def main() -> None:
    U = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    IMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    PMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    cols: dict[tuple[int, ...], bytes] = {}
    for W in product((1, 2), repeat=U):
        cols[W] = column_at(W, U - 1)
    print(f"U={U}: absorption of e_i at column {U-1} (full column equality after flipping e_i)")
    for i in range(IMAX + 1):
        absorbed = {}
        for W in cols:
            if W[i] == 1:
                W2 = W[:i] + (2,) + W[i + 1:]
                absorbed[W] = cols[W] == cols[W2]
        tot = len(absorbed)
        frac = sum(absorbed.values()) / tot
        print(f"\n i={i}: overall absorbed fraction {frac:.4f} over {tot} pairs")
        for p in range(1, PMAX + 1):
            if i + p >= U:
                break
            groups = defaultdict(lambda: [0, 0])
            for W, ok in absorbed.items():
                pat = W[i + 1:i + 1 + p]
                groups[pat][0] += ok
                groups[pat][1] += 1
            best = max(groups.items(), key=lambda kv: kv[1][0] / kv[1][1])
            perfect = [("".join(map(str, k))) for k, (a, b) in groups.items() if a == b]
            worst = min(groups.items(), key=lambda kv: kv[1][0] / kv[1][1])
            print(f"   p={p}: best pattern {''.join(map(str,best[0]))} frac {best[1][0]/best[1][1]:.4f} ({best[1][0]}/{best[1][1]}); "
                  f"perfect patterns: {perfect if perfect else 'none'}; worst {''.join(map(str,worst[0]))} {worst[1][0]/worst[1][1]:.4f}")


if __name__ == "__main__":
    main()

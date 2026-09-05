#!/usr/bin/env python3
"""Block halving on the RW survivor levels.

`RESULTS-FLIP-PAIRING.md` section 2: per-level halving `N_{j+1} <= N_j / 2`
is false at deep levels in every counting.  The weakest surviving form is
block halving: the least `k` such that `N_{j+k} <= N_j / 2` for every level
`j` with `N_j > 0`.  If that `k` is bounded in `n`, an injection may target
a block of `k` levels instead of one.  If it grows with `n`, block halving
is not a true statement either.

Reported per `(n, c)`: `k` in sources and in distinct endpoint states, the
level chain, and the least constant `C(n, lambda) = max_j N_j 2^(lambda j - n)`
for several slopes.  `N_j <= C 2^(n - lambda j)` with `lambda >= 1` and
`C < 4` is the counting form of `(RW-alpha)` (`uc/BRIEF.md` section 4);
a bounded `C(n, lambda)` for some `lambda > 1` is what a counting proof
would have to establish.
Complete census on `psi_kernel.Endpoint` via `flip_pairing.census`.
"""
from __future__ import annotations

import argparse
import sys

from flip_pairing import census


def chains(n: int, c: int, levels: int, keys, cells, hcs):
    total = 1 << n
    src = [0] * (levels + 1)
    st: list[set] = [set() for _ in range(levels + 1)]
    for w in range(total):
        d = levels
        for j in range(levels):
            if not hcs[w][j] or cells[w][j] != c:
                d = j
                break
        for j in range(d + 1):
            src[j] += 1
            st[j].add(keys[w])
    return src, [len(s) for s in st]


def least_block(N: list[int]) -> tuple[int, float]:
    last = max(j for j in range(len(N)) if N[j] > 0)
    for k in range(1, last + 2):
        worst = 0.0
        ok = True
        for j in range(last + 1):
            nxt = N[j + k] if j + k < len(N) else 0
            r = nxt / N[j]
            worst = max(worst, r)
            if nxt > N[j] / 2:
                ok = False
        if ok:
            return k, worst
    return last + 1, 1.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-n", type=int, default=9)
    ap.add_argument("--max-n", type=int, default=16)
    args = ap.parse_args()
    lams = (1.0, 1.1, 1.2, 1.3, 1.35)
    print("n c | k_src k_states | C(n,lambda) sources for lambda=" + ",".join(map(str, lams))
          + " | chain (sources) | chain (states)")
    for n in range(args.min_n, args.max_n + 1):
        levels = n + 4
        keys, syms, cells, hcs = census(n, levels)
        for c in (2, 3):
            src, sts = chains(n, c, levels, keys, cells, hcs)
            ks, ws = least_block(src)
            kt, wt = least_block(sts)
            last = max(j for j in range(len(src)) if src[j] > 0)
            consts = " ".join(f"{max(N * 2 ** (lam * j - n) for j, N in enumerate(src)):5.2f}" for lam in lams)
            print(f"{n:2d} {c} | {ks:2d} {kt:2d} | {consts} | " + " ".join(map(str, src[: last + 2]))
                  + " | " + " ".join(map(str, sts[: last + 2])))
            sys.stdout.flush()


if __name__ == "__main__":
    main()

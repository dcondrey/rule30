#!/usr/bin/env python3
"""Contraction of the deterministic window map M* along hit runs.

For each (n, c), every prefix W in {1,2}^n, and every level k of the forced
orbit (hard-core enforced, run stops at the first non-hit), count

    N_k  surviving prefixes,
    D_k  distinct cell windows (e_u plus cells at depths -u .. n-1),
    L_k  distinct letter windows (the 3-letter quotient (a, b) of the same),
    C_k  distinct cone words (e_u plus cells at depths -u .. -1),
    P_k  distinct peel columns (cells at depths 0 .. n-1),

and compare each to the independence null 2^(n-k).  Also reports, over ALL
prefixes at column n-1 (level 0), how many distinct letter windows there are,
i.e. how many bits of W the next column can see at all.

    cd .../p1-period2-invariant && uv run python uc/r1-potential/window_contraction.py
"""

from __future__ import annotations

import argparse
import math
import sys
from itertools import product

sys.path.insert(0, "uc/r1-potential")
sys.path.insert(0, ".")
from orbit_census import build_from_prefix, forced_orbit, letter  # noqa: E402


def keys(col) -> tuple[tuple, tuple, tuple, tuple]:
    u, n = col.u, col.n
    cells = col.states[:-1]  # depths -u .. n-1
    cell_key = (col.e, tuple(cells))
    letter_key = (col.e, tuple(letter(t) for t in cells))
    cone_key = (col.e, tuple(cells[:u]))  # depths -u .. -1
    peel_key = tuple(cells[u:])  # depths 0 .. n-1
    return cell_key, letter_key, cone_key, peel_key


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-n", type=int, default=6)
    ap.add_argument("--max-n", type=int, default=15)
    ap.add_argument("--log", default="uc/r1-potential/window_contraction.log")
    args = ap.parse_args()
    with open(args.log, "w") as log:
        print("level-0 letter entropy: distinct letter windows of column n-1 over all 2^n prefixes", file=log)
        for n in range(args.min_n, args.max_n + 1):
            lset = set()
            for source in product((1, 2), repeat=n):
                col = build_from_prefix(source, n)
                lset.add((col.e, tuple(letter(t) for t in col.states[:-1])))
            print(f"  n={n:2d}: 2^n={2**n:6d} distinct letter windows={len(lset):6d}  log2={math.log2(len(lset)):.2f}  bits lost={n - math.log2(len(lset)):.2f}", file=log)
        log.flush()
        worst = {}
        for n in range(args.min_n, args.max_n + 1):
            for target in (2, 3):
                max_steps = n + 3
                N = [0] * (max_steps + 1)
                D = [set() for _ in range(max_steps + 1)]
                L = [set() for _ in range(max_steps + 1)]
                C = [set() for _ in range(max_steps + 1)]
                P = [set() for _ in range(max_steps + 1)]
                for source in product((1, 2), repeat=n):
                    k = 0
                    for u, e, hit, col in forced_orbit(source, target, max_steps):
                        if not hit:
                            break
                        k += 1
                        N[k] += 1
                        ck, lk, cok, pk = keys(col)
                        D[k].add(ck)
                        L[k].add(lk)
                        C[k].add(cok)
                        P[k].add(pk)
                N[0] = 2 ** n
                print(f"n={n} c={target}", file=log)
                print("   k     N_k     D_k     L_k     C_k     P_k   N/2^(n-k)  D/2^(n-k)  L/2^(n-k)  D/N   L/D   P/D", file=log)
                for k in range(0, max_steps + 1):
                    if N[k] == 0:
                        break
                    null = 2.0 ** (n - k)
                    dk = 2 ** n if k == 0 else len(D[k])
                    lk = 2 ** n if k == 0 else len(L[k])
                    cok = 2 ** n if k == 0 else len(C[k])
                    pk = 2 ** n if k == 0 else len(P[k])
                    print(f"  {k:2d} {N[k]:7d} {dk:7d} {lk:7d} {cok:7d} {pk:7d}   {N[k]/null:8.3f}   {dk/null:8.3f}   {lk/null:8.3f}  {dk/N[k]:.3f} {lk/dk:.3f} {pk/dk:.3f}", file=log)
                    for name, val in (("N", N[k]), ("D", dk), ("L", lk)):
                        r = val / null
                        if k >= 1 and (name not in worst or r > worst[name][0]):
                            worst[name] = (r, n, target, k)
                log.flush()
        print("\nmax over n, c, k >= 1 of X_k / 2^(n-k):", file=log)
        for name in ("N", "D", "L"):
            r, n, target, k = worst[name]
            print(f"  {name}: {r:.3f} at n={n} c={target} k={k}", file=log)
    print(f"log written to {args.log}")


if __name__ == "__main__":
    main()

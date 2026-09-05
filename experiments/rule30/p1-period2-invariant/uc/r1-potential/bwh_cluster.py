#!/usr/bin/env python3
"""Do the (BWH+) near-miss families share one column window?

(BWH+) is the E-only version of RW (no hard-core).  RESULTS-PSI-ANCESTRY-LAW.md
section 6 records 18 sources at n=15, c=3 whose Psi is constant on Psi_0..Psi_15,
all sharing the suffix 211212112, dying together at Psi_16; the shared cause
was not identified.  The forced orbit depends on column n-1 only through its
3-letter quotient (a, b) = ([T==0], [Lo==0]) plus e_{n-1}, so any two sources
with the same letter window have identical futures.  This script counts, for
the E-only orbit, the number of distinct column windows among the level-k
survivors (N_k prefixes, D_k cell windows, L_k letter windows), and for the
deepest families reports how many distinct windows they occupy.

    cd .../p1-period2-invariant && uv run python uc/r1-potential/bwh_cluster.py
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from itertools import product

sys.path.insert(0, "uc/r1-potential")
sys.path.insert(0, ".")
from orbit_census import build_from_prefix, forced_step, letter  # noqa: E402


def e_only_orbit(source: tuple[int, ...], target: int, max_steps: int):
    n = len(source)
    col = build_from_prefix(source, n)
    for _ in range(max_steps):
        e, nxt = forced_step(col)
        hit = nxt.states[-1] == target
        yield nxt, hit
        if not hit:
            return
        col = nxt


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-n", type=int, default=8)
    ap.add_argument("--max-n", type=int, default=16)
    ap.add_argument("--log", default="uc/r1-potential/bwh_cluster.log")
    args = ap.parse_args()
    with open(args.log, "w") as log:
        for n in range(args.min_n, args.max_n + 1):
            for target in (2, 3):
                max_steps = n + 2
                N = Counter()
                D: dict[int, set] = defaultdict(set)
                L: dict[int, set] = defaultdict(set)
                by_depth: dict[int, list] = defaultdict(list)
                src_letter0: dict[tuple, set] = defaultdict(set)
                for source in product((1, 2), repeat=n):
                    k = 0
                    last_key = None
                    first_letter = None
                    for col, hit in e_only_orbit(source, target, max_steps):
                        if not hit:
                            break
                        k += 1
                        N[k] += 1
                        cells = col.states[:-1]
                        ck = (col.e, tuple(cells))
                        lk = (col.e, tuple(letter(t) for t in cells))
                        D[k].add(ck)
                        L[k].add(lk)
                        if k == 1:
                            first_letter = lk
                        last_key = lk
                    by_depth[k].append((source, first_letter, last_key))
                deepest = max(by_depth)
                print(f"n={n} c={target} (E-only, no hard-core): deepest={deepest} need={n+2}", file=log)
                print("   k     N_k     D_k     L_k   N/2^(n-k)  D/2^(n-k)  N/D", file=log)
                for k in range(1, max_steps + 1):
                    if N[k] == 0:
                        break
                    null = 2.0 ** (n - k)
                    print(f"  {k:2d} {N[k]:7d} {len(D[k]):7d} {len(L[k]):7d}   {N[k]/null:8.3f}   {len(D[k])/null:8.3f}  {N[k]/len(D[k]):.2f}", file=log)
                fam = by_depth[deepest]
                wins_first = {f for _, f, _ in fam}
                wins_last = {l for _, _, l in fam}
                srcs = sorted("".join(map(str, s)) for s, _, _ in fam)
                print(f"   deepest family: {len(fam)} sources, {len(wins_first)} distinct level-1 letter windows, {len(wins_last)} distinct level-{deepest} windows", file=log)
                print(f"   sources: {' '.join(srcs[:24])}{' ...' if len(srcs) > 24 else ''}", file=log)
                # multiplicity distribution of level-1 letter windows over ALL sources
                mult = Counter()
                for source in product((1, 2), repeat=n):
                    col = build_from_prefix(source, n)
                    mult[(col.e, tuple(letter(t) for t in col.states[:-1]))] += 1
                hist = Counter(mult.values())
                print(f"   level-0 letter-window multiplicities over all 2^n sources: {' '.join(f'{m}:{c}' for m, c in sorted(hist.items()))}", file=log)
                log.flush()
    print(f"log written to {args.log}")


if __name__ == "__main__":
    main()

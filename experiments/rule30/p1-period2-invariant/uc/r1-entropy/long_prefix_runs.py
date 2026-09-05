#!/usr/bin/env python3
"""Is the RW run bound a property of the dynamics or of the budget?

RW fixes prefix length = depth = n.  The "hit density at most alpha along
every admissible orbit" formulation would forbid n+2 consecutive hits at
depth n for a binary hard-core endpoint of ANY length.  This script tests
that directly: for depth n and prefix length m >= n, every binary prefix
W in {1,2}^m is followed by the forced (H-forcing at depth n) hard-core
continuation, and the deepest run of T[u][n] = c for u = m, m+1, ... is
recorded (complete search, no sampling; condition 3 of RW ignored, so the
count is an upper bound on RW-shaped runs).

Prediction before running (state accounting of RESULTS-CLUSTER-ANATOMY):
about 1.77^m distinct states at column m-1 and joint survival ~0.4 per
level give run ~0.62 m, so runs of n+2 should appear once m ~ 1.6 n + 3.
If they do, an orbit-wise density/run bound is FALSE as a statement about
the dynamics and only the budget-tied count (prefix length = depth) can be
the target.  If they never appear even at m = 2n+2 that is a surprise and a
genuine all-orbits lemma candidate.

Run:  cd <kernel dir> && uv run python uc/r1-entropy/long_prefix_runs.py --nmin 5 --nmax 9
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from itertools import product

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from psi_kernel import Endpoint  # noqa: E402


def deepest_from_prefix_length(n: int, m: int, c: int, cap: int):
    """Complete search over W in {1,2}^m; forced HC continuation; hits at depth n."""
    best = 0
    full = 0
    witness = ""

    def walk(state: Endpoint, prev: int, depth: int, word: list[int]) -> None:
        nonlocal best, full, witness
        if depth > best:
            best, witness = depth, "".join(map(str, word))
        if depth >= cap:
            full += 1
            return
        for s in (1, 2):
            if prev == 1 and s == 1:
                continue
            col, dia = state.peek(s)
            if dia[n] != c:
                continue
            nxt = Endpoint()
            nxt.column, nxt.diagonal, nxt.length = col + [s], dia, state.length + 1
            walk(nxt, s, depth + 1, word + [s])
            # dia[n] has H=1 for exactly one s, so at most one branch survives

    for src in product((1, 2), repeat=m):
        st = Endpoint()
        for s in src:
            st.append(s)
        walk(st, src[-1], 0, list(src))
    return best, full, witness


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--nmin", type=int, default=5)
    ap.add_argument("--nmax", type=int, default=9)
    ap.add_argument("--mmax-extra", type=int, default=2, help="m runs up to 2n + this")
    ap.add_argument("--mcap", type=int, default=19, help="absolute cap on m (2^m prefixes)")
    ap.add_argument("--log", type=str, default="uc/r1-entropy/long_prefix_runs.log")
    args = ap.parse_args()
    with open(args.log, "w") as log:
        print("# depth n, prefix length m, target c: deepest run of c at depth n from column m,", file=log)
        print("# need = n+2 (RW r=0), full = number of prefixes reaching need, deepest/m, seconds", file=log)
        print("  n   m  c  deepest  need  full   deepest/m   witness(first 40)   sec", file=log)
        for n in range(args.nmin, args.nmax + 1):
            need = n + 2
            for m in range(n, min(2 * n + args.mmax_extra, args.mcap) + 1):
                for c in (2, 3):
                    t0 = time.time()
                    best, full, wit = deepest_from_prefix_length(n, m, c, need)
                    dt = time.time() - t0
                    mark = "  <- FULL RUN" if best >= need else ""
                    print(f"{n:3d} {m:3d}  {c}  {best:6d}  {need:4d}  {full:5d}   {best/m:8.3f}   {wit[:40]:<40} {dt:6.1f}{mark}", file=log)
                    log.flush()
    with open(args.log) as f:
        sys.stdout.write(f.read())


if __name__ == "__main__":
    main()

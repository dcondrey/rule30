#!/usr/bin/env python3
"""Exhaustive check of the two facts behind the coalescence mechanism of L1.

(1) Light cone.  Flipping e_j (1 <-> 2) in a binary prefix of length u
    changes column u-1 = T[u-1][.] only at depths d >= u-2-2j
    (T[u][d] depends on e_j only if j >= (u-d-1)/2).
(2) Upper set.  Within a column the set of changed cells is an upper set
    {d >= d_min}: phi is a bijection in its right (same-column) argument,
    so a difference propagates upward unless cancelled by a simultaneous
    left-argument difference; the check records how often such a
    cancellation actually occurs (a gap inside the difference set).

Over all binary prefixes of length u <= umax and all j < u.  Failures of (1)
are counted and would be a bug in the derivation; gaps in (2) are reported
as a count (they are allowed by the local rule, the question is whether
they occur).

Run:  cd <kernel dir> && uv run python uc/r1-entropy/lightcone_check.py --umax 12
"""
from __future__ import annotations

import argparse
import os
import sys
from itertools import product

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from psi_kernel import Endpoint  # noqa: E402


def column(w):
    st = Endpoint()
    for s in w:
        st.append(s)
    # depth-indexed: column[i] = T[u-1][-i] for i=0..u-1, column[u] = e_{u-1} at depth -u; diagonal[k] = T[u-1][k]
    u = len(w)
    cells = {}
    for i in range(u):
        cells[-i] = st.column[i]
    cells[-u] = st.column[u]
    for k in range(u):
        cells[k] = st.diagonal[k]
    return cells


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--umax", type=int, default=12)
    ap.add_argument("--log", type=str, default="uc/r1-entropy/lightcone_check.log")
    args = ap.parse_args()
    with open(args.log, "w") as log:
        print("# u  pairs  lightcone_failures  columns_with_gap  dead_defects  min_dmin_minus_bound", file=log)
        for u in range(2, args.umax + 1):
            pairs = 0
            lc_fail = 0
            gaps = 0
            dead = 0
            min_slack = 10**9
            cache = {}
            for w in product((1, 2), repeat=u):
                cache[w] = column(w)
            for w in cache:
                cw = cache[w]
                for j in range(u):
                    w2 = w[:j] + (3 - w[j],) + w[j + 1:]
                    if w2 < w:
                        continue
                    pairs += 1
                    c2 = cache[w2]
                    diff = sorted(d for d in cw if cw[d] != c2[d])
                    if not diff:
                        dead += 1
                        continue
                    bound = (u - 1) - 1 - 2 * j   # d >= u-2-2j for column u-1
                    if diff[0] < bound:
                        lc_fail += 1
                    min_slack = min(min_slack, diff[0] - bound)
                    # upper set test
                    top = u - 1
                    if diff != list(range(diff[0], top + 1)):
                        gaps += 1
            print(f"{u:3d} {pairs:8d} {lc_fail:8d} {gaps:10d} {dead:10d} {min_slack:8d}", file=log)
    with open(args.log) as f:
        sys.stdout.write(f.read())


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Anatomy of the deepest survivors and of the dependency cone.

Part 1 (cone).  Exhaustive check of the claim: flipping the source symbol
W_j changes only cells T[u][d] with u - d <= 2j + 1.  Checked on every
binary W of length n for n <= NCONE over the full triangle of the endpoint
W plus its forced continuation (so that the forced symbols are part of the
check: two sources differing in W_j only must have identical forced symbols
e_u for u >= n + 2j + 2 whenever they agree on e_n..e_{n+2j+1} and on the
hits there).  A failure prints the offending (n, j, u, d).

Part 2 (tail).  For each (n, c) in the requested range, list every source
that reaches the deepest joint level kmax and the deepest E-only level,
with its forced continuation word, the cause of death (E miss or hard-core),
and the cluster structure: which coordinates vary within the cluster.

Run:  cd <kernel dir> && uv run python uc/r1-entropy/tail_anatomy.py --min 9 --max 17
"""

from __future__ import annotations

import argparse
import os
import sys
from collections import defaultdict
from itertools import product

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from psi_kernel import CONE, Endpoint  # noqa: E402


def triangle(endpoint):
    """Full triangle T[u][d] for d in [-u-1, u], as dict of lists."""
    L = len(endpoint)
    T = []
    for u in range(L):
        col = [0] * (2 * u + 2)  # index i <-> depth d = i - u - 1
        col[0] = endpoint[u]
        col[1] = endpoint[u] ^ 3
        for i in range(2, 2 * u + 2):
            d = i - u - 1
            left = T[u - 1][(d - 1) + (u - 1) + 1]
            col[i] = CONE[left][col[i - 1]]
        T.append(col)
    return T


def cone_check(nmax, log):
    bad = 0
    checked = 0
    for n in range(2, nmax + 1):
        for W in product((1, 2), repeat=n):
            TW = triangle(W)
            for j in range(n):
                W2 = list(W)
                W2[j] = 3 - W2[j]
                T2 = triangle(tuple(W2))
                for u in range(n):
                    for i in range(2 * u + 2):
                        d = i - u - 1
                        if TW[u][i] != T2[u][i] and u - d > 2 * j + 1:
                            bad += 1
                            if bad <= 5:
                                print(f"CONE VIOLATION n={n} j={j} u={u} d={d}", file=log)
                        checked += 1
    print(f"cone check: {checked} cell comparisons, {bad} violations (claim: W_j touches only u-d <= 2j+1)", file=log)


def forced(source, target, max_steps):
    n = len(source)
    st = Endpoint()
    for s in source:
        st.append(s)
    hits, syms = [], []
    for _ in range(max_steps):
        for sym in (1, 2):
            _, diag = st.peek(sym)
            if diag[n] >> 1 == 1:
                break
        st.append(sym)
        syms.append(sym)
        hits.append(1 if diag[n] == target else 0)
    return hits, syms


def levels(hits, syms, prev):
    """(joint level, E-only level, cause of joint death)."""
    kE = 0
    while kE < len(hits) and hits[kE]:
        kE += 1
    k = 0
    cause = "?"
    p = prev
    while k < len(hits):
        if not hits[k]:
            cause = "Emiss"
            break
        if p == 1 and syms[k] == 1:
            cause = "HC"
            break
        p = syms[k]
        k += 1
    return k, kE, cause


def tail(n, c, log):
    max_steps = n + 3
    rows = []
    for W in product((1, 2), repeat=n):
        h, s = forced(W, c, max_steps)
        k, kE, cause = levels(h, s, W[-1])
        rows.append((W, k, kE, cause, s, h))
    kmax = max(r[1] for r in rows)
    kEmax = max(r[2] for r in rows)
    print(f"\n# n={n} c={c}: deepest joint k={kmax}, deepest E-only k={kEmax}", file=log)
    deep = [r for r in rows if r[1] == kmax]
    print(f"joint survivors at k={kmax}: {len(deep)}", file=log)
    for W, k, kE, cause, s, h in deep:
        print(f"  W={''.join(map(str, W))} cont={''.join(map(str, s[:kE+1]))} hits={''.join(map(str, h[:kE+1]))} kE={kE} death={cause}", file=log)
    varying = [j for j in range(n) if len({r[0][j] for r in deep}) > 1]
    print(f"  coordinates varying within the joint-deepest set: {varying}", file=log)
    deepE = [r for r in rows if r[2] == kEmax]
    print(f"E-only survivors at kE={kEmax}: {len(deepE)}", file=log)
    groups = defaultdict(list)
    for r in deepE:
        groups[tuple(r[4][:kEmax])].append(r)
    for cont, members in groups.items():
        varying = [j for j in range(n) if len({m[0][j] for m in members}) > 1]
        print(f"  cont={''.join(map(str, cont))} hc={'legal' if '11' not in ''.join(map(str, cont)) and not (members[0][0][-1]==1 and cont[0]==1) else 'ILLEGAL'} members={len(members)} varying_coords={varying} example W={''.join(map(str, members[0][0]))}", file=log)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min", type=int, default=9)
    ap.add_argument("--max", type=int, default=16)
    ap.add_argument("--ncone", type=int, default=9)
    ap.add_argument("--log", type=str, default="uc/r1-entropy/tail_anatomy.log")
    args = ap.parse_args()
    with open(args.log, "w") as log:
        cone_check(args.ncone, log)
        log.flush()
        for n in range(args.min, args.max + 1):
            for c in (2, 3):
                tail(n, c, log)
                log.flush()
    with open(args.log) as f:
        sys.stdout.write(f.read())


if __name__ == "__main__":
    main()

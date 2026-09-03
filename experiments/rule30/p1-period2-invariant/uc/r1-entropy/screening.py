#!/usr/bin/env python3
"""Screening classes: the exact cluster structure of the survivor sets.

Proved identity (stencil): the source symbol W_j = e_j enters the triangle at
depth -j-1 of column j, and a cell T[u][d] depends on e_j only if
u - d <= 2j + 1.  Hence two sources W, W' that agree on W[m:] and whose
forced continuations agree on e_n .. e_{n+2m-1} produce identical cells at
every (u, d) with u - d >= 2m, so identical forced symbols and hits from
column n + 2m on.  (Checked exhaustively in tail_anatomy.py, 0 violations.)

Consequence: at level k the joint survivors split into classes indexed by
(W[m:], v[:2m]) with m = floor(k/2) that share their entire future.  The
class size is at most 2^m.  This script measures, per (n, c, k):

    D_k        number of classes (distinct futures)
    smax_k     largest class
    N_k / D_k  mean class size

and verifies the identity on the survivors (all members of a class have the
same continuation and the same death level).  A growing smax with n means
the constant in any counting lemma N_k <= C 2^(n - lambda k) is not
absolute.

Run:  cd <kernel dir> && uv run python uc/r1-entropy/screening.py --min 10 --max 17
"""

from __future__ import annotations

import argparse
import os
import sys
from collections import defaultdict
from itertools import product

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from psi_kernel import Endpoint  # noqa: E402


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


def joint_level(hits, syms, prev):
    k = 0
    p = prev
    while k < len(hits) and hits[k] and not (p == 1 and syms[k] == 1):
        p = syms[k]
        k += 1
    return k


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min", type=int, default=10)
    ap.add_argument("--max", type=int, default=16)
    ap.add_argument("--log", type=str, default="uc/r1-entropy/screening.log")
    args = ap.parse_args()
    with open(args.log, "w") as log:
        summary = []
        for n in range(args.min, args.max + 1):
            for c in (2, 3):
                max_steps = n + 3
                data = {}
                for W in product((1, 2), repeat=n):
                    h, s = forced(W, c, max_steps)
                    data[W] = (h, s, joint_level(h, s, W[-1]))
                kmax = max(v[2] for v in data.values())
                print(f"\n# n={n} c={c}  (kmax={kmax})", file=log)
                print("  k    N_k    D_k  smax  N_k/D_k  identity_violations", file=log)
                smax_overall = 0
                for k in range(1, kmax + 1):
                    m = k // 2
                    classes = defaultdict(list)
                    for W, (h, s, lev) in data.items():
                        if lev >= k:
                            classes[(W[m:], tuple(s[:2 * m]))].append(W)
                    Nk = sum(len(v) for v in classes.values())
                    Dk = len(classes)
                    smax = max(len(v) for v in classes.values())
                    smax_overall = max(smax_overall, smax)
                    viol = 0
                    for members in classes.values():
                        futures = {(tuple(data[W][1][2 * m:]), tuple(data[W][0][2 * m:]), data[W][2]) for W in members}
                        if len(futures) > 1:
                            viol += 1
                    print(f"{k:3d} {Nk:6d} {Dk:6d} {smax:5d}  {Nk/Dk:7.2f}   {viol}", file=log)
                summary.append((n, c, kmax, smax_overall))
                log.flush()
        print("\n# summary: n c kmax smax_overall", file=log)
        for n, c, km, sm in summary:
            print(f"{n:3d} {c} {km:3d} {sm:4d}", file=log)
    with open(args.log) as f:
        sys.stdout.write(f.read())


if __name__ == "__main__":
    main()

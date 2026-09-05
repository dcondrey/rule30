#!/usr/bin/env python3
"""Reachable retained-bit vectors per zero pattern of column n-1.

Group the 2^n binary sources by the zero pattern Z of column n-1 (window
[-n, n-1]).  Within a class the forced future depends only on the retained
even-bits w_ret in F2^r (r = number of even-indexed nonzero cells from the
top).  Report per n: number of classes, class-size histogram summary, the
number of classes on which hit_n (the all-ones functional on w_ret) is
constant although the class has >= 2 distinct w_ret vectors, and the
distribution of (affine rank of the reachable w_ret set) - r.  A class whose
reachable w_ret vectors span a proper affine subspace on which the all-ones
functional is constant is a class the E-pin cannot halve.

Run:  cd <work dir> && uv run python uc/r1-quadratic/q2_classes.py --max-n 16
"""
from __future__ import annotations

import argparse
import time
from collections import Counter
from itertools import product

from qf_common import Endpoint, E


def gf2_rank(rows: list[int]) -> int:
    rank = 0
    rows = rows[:]
    while rows:
        pivot = max(rows)
        if pivot == 0:
            break
        rank += 1
        bit = 1 << (pivot.bit_length() - 1)
        rows = [r ^ pivot if r & bit else r for r in rows if r != pivot]
    return rank


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-n", type=int, default=4)
    ap.add_argument("--max-n", type=int, default=16)
    args = ap.parse_args()
    for n in range(args.min_n, args.max_n + 1):
        t0 = time.time()
        classes: dict = {}
        for src in product((1, 2), repeat=n):
            ep = Endpoint()
            for s in src:
                ep.append(s)
            cells = [ep.column[-d] if d <= 0 else ep.diagonal[d] for d in range(-n, n)]
            Z = tuple(i for i, t in enumerate(cells) if t == 0)
            qs = [i for i in range(2 * n - 1, -1, -1) if cells[i] != 0]
            ret = [q for idx, q in enumerate(qs, start=1) if idx % 2 == 0]
            wret = sum((1 if cells[q] == 2 else 0) << k for k, q in enumerate(ret))
            classes.setdefault(Z, [len(ret), Counter()])[1][wret] += 1
        sizes = Counter()
        const_bad = 0
        multi = 0
        rankdef = Counter()
        balance = []
        for Z, (r, ctr) in classes.items():
            distinct = len(ctr)
            sizes[distinct] += 1
            if distinct >= 2:
                multi += 1
                vals = {bin(w).count("1") & 1 for w in ctr}
                if len(vals) == 1:
                    const_bad += 1
                base = next(iter(ctr))
                rk = gf2_rank([w ^ base for w in ctr])
                rankdef[r - rk] += 1
                z = sum(cnt for w, cnt in ctr.items() if bin(w).count("1") % 2 == 0)
                tot = sum(ctr.values())
                balance.append(z / tot)
        print(f"n={n}: classes={len(classes)}  with >=2 distinct w_ret: {multi}  "
              f"all-ones constant on such a class: {const_bad}  "
              f"distinct-w_ret histogram (top): {sorted(sizes.items())[:8]}  "
              f"(r - affine rank) histogram: {dict(sorted(rankdef.items()))}  "
              f"mean hit fraction over multi classes: {sum(balance)/max(1,len(balance)):.3f}   [{time.time()-t0:.0f}s]", flush=True)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Candidate uniform block-contraction lemma at the exact half-depth prefix state.

PRE-REGISTERED 2026-09-03, before running.

`prefix_cylinder_loss.py` found block ratio 1.0 at short blocks and at deep
conditioning points (`p = 2n/3`).  `mass_decomposition.py` found that at
`p = n/2` and block `b = 8` no state exceeded ratio `0.056` at any level, with
essentially no mass in below-threshold states.  This script tests that
directly and without any threshold, as the clean uniform statement:

    R(n, p, c, b) = max over prefix states s at depth p,
                    over levels j with N_s(j) > 0,
                    of  N_s(j+b) / N_s(j)

where `N_s(j)` counts the sources with prefix state `s` surviving `j` forced
RW levels.  No thresholds, no mass splitting, no aggregation: the maximum is
over every state and every level.

Candidate lemma: there are `b` and `lambda < 1` with `R(n, n/2, c, b) <=
lambda` for every `n` and both `c`.

Kill (pre-registered): `R` reaches 1.0 at the block length under test, or
climbs toward 1 as `n` grows.  Either means no uniform block contraction holds
at this state definition and the exceptional states must be classified before
any counting argument can proceed.

The conditioning depth `p` is swept as well, since the earlier runs showed the
statement is sensitive to it: the claim is about `p = floor(n/2)` and the other
depths are reported to show where it fails.
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from itertools import product

from psi_kernel import Endpoint
from flip_pairing import census


def prefix_state(src, p):
    st = Endpoint()
    for s in src[:p]:
        st.append(s)
    return (tuple(st.column), tuple(st.diagonal))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-n", type=int, default=10)
    ap.add_argument("--max-n", type=int, default=16)
    ap.add_argument("--bmax", type=int, default=10)
    ap.add_argument("--all-p", action="store_true")
    args = ap.parse_args()

    print("# R(n,p,c,b) = max over prefix states and levels of N_s(j+b)/N_s(j).")
    print("# No threshold and no aggregation: the max is over every state and every level.")
    hdr = "  ".join(f"b={b}" for b in range(1, args.bmax + 1))
    print(f"{'n':>3} {'p':>3} {'c':>2} {'states':>7} | {hdr}")
    for n in range(args.min_n, args.max_n + 1):
        levels = n + 4
        keys, syms, cells, hcs = census(n, levels)
        srcs = list(product((1, 2), repeat=n))
        ps = list(range(2, n)) if args.all_p else [n // 2]
        for p in ps:
            groups = defaultdict(list)
            for idx, w in enumerate(srcs):
                groups[prefix_state(w, p)].append(idx)
            for c in (2, 3):
                span = levels + args.bmax + 2
                per = []
                for s, members in groups.items():
                    row = [0] * span
                    for idx in members:
                        d = levels
                        cl, hc = cells[idx], hcs[idx]
                        for j in range(levels):
                            if not hc[j] or cl[j] != c:
                                d = j
                                break
                        for j in range(d + 1):
                            row[j] += 1
                    per.append(row)
                cells_out = []
                for b in range(1, args.bmax + 1):
                    worst = 0.0
                    for row in per:
                        for j in range(span - b):
                            if row[j] > 0:
                                r = row[j + b] / row[j]
                                if r > worst:
                                    worst = r
                    cells_out.append(f"{worst:.3f}")
                print(f"{n:>3} {p:>3} {c:>2} {len(groups):>7} | " + "  ".join(cells_out))
                sys.stdout.flush()


if __name__ == "__main__":
    main()

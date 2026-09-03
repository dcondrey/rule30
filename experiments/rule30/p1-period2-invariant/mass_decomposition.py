#!/usr/bin/env python3
"""Can a per-state contraction plus a controlled remainder be iterated?

PRE-REGISTERED 2026-09-03, before running.

`prefix_cylinder_loss.py` showed the uniform block contraction is false at the
exact prefix state: some states have block ratio 1.0.  But every such state
holds a tiny survivor count (`1 -> 1`, `3 -> 3`, `4 -> 4`), while states above
a count threshold contract hard (max ratio `<= 0.17` at block `b = 6`).  That
is the "generic loss plus exceptional family" shape, and it is only worth
pursuing if the exceptional mass is small enough to be absorbed.

The arithmetic a proof would use.  Split the prefix states at level `j` into
BIG (`row_s[j] >= delta * N_j`) and SMALL.  If every BIG state obeys
`row_s[j+b] <= lambda * row_s[j]`, and SMALL states are bounded only by the
trivial `row_s[j+b] <= row_s[j]`, then

    N_{j+b} <= lambda * (1 - mu) * N_j + mu * N_j
             = (lambda + mu * (1 - lambda)) * N_j

where `mu` is the fraction of `N_j` held by SMALL states.  Write
`B = lambda + mu (1 - lambda)` for that bound.

Reported per `(n, p, c, b, delta)`: `lambda` (max block ratio over BIG states),
`mu` (max SMALL mass fraction over levels), the resulting `B`, and the true
aggregate ratio `max_j N_{j+b}/N_j` for comparison.

Strong outcome: `B` bounded away from 1 uniformly in `n`, `p` and `j` for some
`(b, delta)`.  That is a rate-bearing statement and the first candidate block
lemma this program has had.
Kill: `B -> 1` because `mu -> 1` at deep levels, i.e. the survivors at depth
are all held in small states, so the exceptional family carries everything and
absorbing it is impossible.
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
    ap.add_argument("--min-n", type=int, default=12)
    ap.add_argument("--max-n", type=int, default=16)
    ap.add_argument("--blocks", type=str, default="4,6")
    ap.add_argument("--deltas", type=str, default="0.001,0.01,0.05")
    args = ap.parse_args()
    blocks = [int(x) for x in args.blocks.split(",")]
    deltas = [float(x) for x in args.deltas.split(",")]

    for n in range(args.min_n, args.max_n + 1):
        levels = n + 4
        keys, syms, cells, hcs = census(n, levels)
        srcs = list(product((1, 2), repeat=n))
        for p in (n // 2, (2 * n) // 3):
            groups = defaultdict(list)
            for idx, w in enumerate(srcs):
                groups[prefix_state(w, p)].append(idx)
            for c in (2, 3):
                per = {}
                for s, members in groups.items():
                    row = [0] * (levels + 2)
                    for idx in members:
                        d = levels
                        cl, hc = cells[idx], hcs[idx]
                        for j in range(levels):
                            if not hc[j] or cl[j] != c:
                                d = j
                                break
                        for j in range(d + 1):
                            row[j] += 1
                    per[s] = row
                N = [sum(row[j] for row in per.values()) for j in range(levels + 2)]
                for b in blocks:
                    for delta in deltas:
                        lam = 0.0
                        mu = 0.0
                        agg = 0.0
                        worst_j = None
                        for j in range(levels):
                            if N[j] == 0:
                                break
                            thr = delta * N[j]
                            small = sum(row[j] for row in per.values() if row[j] < thr)
                            m = small / N[j]
                            l = 0.0
                            for row in per.values():
                                if row[j] >= thr and row[j] > 0:
                                    l = max(l, row[j + b] / row[j])
                            a = N[j + b] / N[j]
                            if l > lam:
                                lam = l
                            if m > mu:
                                mu, worst_j = m, j
                            agg = max(agg, a)
                        B = lam + mu * (1 - lam)
                        print(f"n={n:>2} p={p:>2} c={c} b={b} delta={delta:<6} | "
                              f"lambda={lam:.3f} mu={mu:.3f}(j={worst_j}) B={B:.3f} | "
                              f"aggregate max N_(j+b)/N_j = {agg:.3f}")
                        sys.stdout.flush()


if __name__ == "__main__":
    main()

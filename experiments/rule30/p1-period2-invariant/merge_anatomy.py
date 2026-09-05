#!/usr/bin/env python3
"""What actually merges in the reachable column language?

``|C_u|`` grows like ``1.765^u``, so about ``2|C_u| - |C_{u+1}| = 0.235|C_u|``
appends collide at every step.  ``column_quotient.py`` shows the exact
congruence ``CONE[1] == CONE[3]`` is only a 5.7 percent constant-factor
collapse, so it is not the reason the base is below 2.  Before designing an
induction on single-position richness, measure whether merging parents differ
in ONE position or in many.

The append stores the symbol literally as the last column entry, so two states
merge only under the same appended symbol.  For every child with more than one
parent this script records the Hamming distance between parents on the column
and on the diagonal, and, for distance-one column pairs, which symbol pair
collapsed and what the successor trajectory state was at that position.

Discriminator (pre-registered).  If single-position pairs carry most of the
merge mass, an induction "a positive fraction of ``C_u`` has a single-position
partner" can give ``|C_{u+1}| <= (2 - delta)|C_u|`` and hence a PROVED base
below 2.  Kill: merging parents are typically far apart in Hamming distance,
in which case the dominant mechanism is multi-position and single-position
richness is the wrong induction.
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict

from psi_kernel import BOUNDARY, CONE


def step(col, dia, sym):
    L = len(col) - 1
    nc = [0] * (L + 1)
    nc[L] = BOUNDARY[sym]
    for i in range(L - 1, -1, -1):
        nc[i] = CONE[col[i + 1]][nc[i + 1]]
    nd = [0] * (L + 1)
    nd[0] = nc[0]
    for i in range(L):
        nd[i + 1] = CONE[dia[i]][nd[i]]
    return tuple(nc) + (sym,), tuple(nd)


def start():
    return [((BOUNDARY[s], s), (BOUNDARY[s],)) for s in (1, 2)]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--umax", type=int, default=17)
    args = ap.parse_args()
    cur = set(start())
    print("# u -> u+1 append.  merges = 2|C_u| - |C_{u+1}|.")
    print("# dist = Hamming distance between two parents of one child (column, diagonal).")
    for u in range(1, args.umax + 1):
        kids = defaultdict(list)
        for st in cur:
            for s in (1, 2):
                kids[step(list(st[0]), list(st[1]), s)].append(st)
        C, Cn = len(cur), len(kids)
        merges = 2 * C - Cn
        coldist = Counter()
        diadist = Counter()
        pairs = 0
        onepos_syms = Counter()
        fanout = Counter()
        for ch, ps in kids.items():
            fanout[len(ps)] += 1
            if len(ps) < 2:
                continue
            for i in range(len(ps)):
                for j in range(i + 1, len(ps)):
                    a, b = ps[i], ps[j]
                    dc = sum(x != y for x, y in zip(a[0], b[0]))
                    dd = sum(x != y for x, y in zip(a[1], b[1]))
                    coldist[dc] += 1
                    diadist[dd] += 1
                    pairs += 1
                    if dc == 1:
                        p = next(k for k, (x, y) in enumerate(zip(a[0], b[0])) if x != y)
                        onepos_syms[tuple(sorted((a[0][p], b[0][p])))] += 1
        one = coldist.get(1, 0)
        print(
            f"u={u:>3} |C_u|={C:>8} |C_u+1|={Cn:>8} merges={merges:>7} "
            f"pairs={pairs:>7} coldist1={one:>7} share={one / pairs if pairs else 0:>6.3f} "
            f"coldist={dict(sorted(coldist.items())[:6])} diadist1={diadist.get(1, 0):>7} "
            f"fanout={dict(sorted(fanout.items()))} onepos={dict(onepos_syms)}"
        )
        sys.stdout.flush()
        cur = set(kids)


if __name__ == "__main__":
    main()

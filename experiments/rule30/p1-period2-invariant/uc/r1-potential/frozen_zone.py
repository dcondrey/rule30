#!/usr/bin/env python3
"""Which cells of a run column are determined by the hits alone?

For each (n, c, k) and each depth d of column u = n+k-1, count the distinct
values T[u][d] takes over all level-k survivors.  A depth with one value is
"frozen" by the k hits.  Also prints the run region of the longest orbits and
the frozen-row transient for rows far above the hit row with free boundaries.

    cd .../p1-period2-invariant && uv run python uc/r1-potential/frozen_zone.py
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from itertools import product

sys.path.insert(0, "uc/r1-potential")
sys.path.insert(0, ".")
from orbit_census import cell, forced_orbit, hf  # noqa: E402


def G(l: int, y: int) -> int:
    hy, ey = hf(y)
    hr = hy ^ 1 ^ (1 if l == 0 else 0)
    er = ey ^ (hr & (1 if (l & 1) == 0 else 0))
    return cell(hr, er)


def row_transients(target: int, rows: int, cols: int, log) -> None:
    """Bottom-up rows over an infinite hit row, all 4^rows boundary chains
    are too many, so track for each row the set of (boundary-dependent)
    words reachable, collapsing by exact word identity."""
    words = {tuple([target] * cols)}
    print(f"c={target}: rows above the hit row, number of distinct eventual words over all boundary chains", file=log)
    for depth in range(1, rows + 1):
        nxt = set()
        for w in words:
            for lb in range(4):
                r = [lb]
                for y in w[1:]:
                    r.append(G(r[-1], y))
                nxt.add(tuple(r))
        words = nxt
        # transient: first column index from which all words agree
        agree_from = cols
        for i in range(cols):
            if len({w[i] for w in words}) == 1 and all(len({w[j] for w in words}) == 1 for j in range(i, cols)):
                agree_from = i
                break
        # eventual period of a representative
        rep = next(iter(words))
        tail = rep[cols // 2 :]
        per = next((p for p in range(1, len(tail)) if all(tail[i] == tail[i + p] for i in range(len(tail) - p))), None)
        distinct_tails = len({w[cols // 2 :] for w in words})
        print(f"  row n-{depth:2d}: distinct words={len(words):4d} all-agree-from-offset={agree_from} period={per} distinct-tails={distinct_tails}", file=log)
        if len(words) > 4096:
            print("  (stopping, too many words)", file=log)
            break


def frozen_census(n: int, target: int, log) -> None:
    max_steps = n + 3
    by_level: dict[int, list] = defaultdict(list)
    longest = []
    best = -1
    for source in product((1, 2), repeat=n):
        k = 0
        cols = []
        for u, e, hit, col in forced_orbit(source, target, max_steps):
            if not hit:
                break
            k += 1
            cols.append(col)
            by_level[k].append(col)
        if k > best:
            best, longest = k, [(source, cols)]
        elif k == best:
            longest.append((source, cols))
    print(f"n={n} c={target} deepest={best}", file=log)
    for k in sorted(by_level):
        cols = by_level[k]
        u = n + k - 1
        m = u + n + 1  # states at depths -u .. n
        distinct_per_depth = []
        for i in range(m):
            distinct_per_depth.append(len({c.states[i] for c in cols}))
        frozen = [i for i, d in enumerate(distinct_per_depth) if d == 1]
        # longest frozen suffix (from depth n upward)
        suf = 0
        while suf < m and distinct_per_depth[m - 1 - suf] == 1:
            suf += 1
        e_distinct = len({c.e for c in cols})
        line = "".join(str(d) for d in distinct_per_depth)
        print(f"  k={k:2d} u={u:2d} N={len(cols):5d} frozen-suffix-from-depth-n={suf:2d} of {m} cells, frozen-total={len(frozen)}, e_u-distinct={e_distinct}", file=log)
        print(f"        distinct-per-depth (top=-u .. bottom=n): {line}", file=log)
    # region print for one longest orbit
    source, cols = longest[0]
    print(f"  region of longest orbit W={''.join(map(str, source))}: columns u=n..{n+best-1}, rows printed top depth -(n+best) .. n", file=log)
    top = -(n + best)
    for d in range(top, n + 1):
        row = []
        for col in cols:
            u = col.u
            if d < -u - 1:
                row.append(" ")
            elif d == -u - 1:
                row.append(str(col.e))
            else:
                row.append(str(col.states[d + u]))
        print(f"    d={d:4d}: {''.join(row)}", file=log)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-n", type=int, default=8)
    ap.add_argument("--max-n", type=int, default=14)
    ap.add_argument("--log", default="uc/r1-potential/frozen_zone.log")
    args = ap.parse_args()
    with open(args.log, "w") as log:
        for target in (2, 3):
            row_transients(target, 40, 96, log)
        for n in range(args.min_n, args.max_n + 1):
            for target in (2, 3):
                frozen_census(n, target, log)
                log.flush()
    print(f"log written to {args.log}")


if __name__ == "__main__":
    main()

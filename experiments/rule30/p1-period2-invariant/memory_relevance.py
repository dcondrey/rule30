#!/usr/bin/env python3
"""G3 relevance audit: does the column-memory state control future RW survival?

PRE-REGISTERED 2026-09-03, before running.

`RESULTS-COLUMN-DECOMPOSITION.md` section 5c proves the column of a length-`L`
word depends only on its last `ceil((L+1)/2)` symbols, giving
`|Col_L| <= 2^ceil((L+1)/2)`.  That is an exact invariant of the column map.
It is NOT automatically a rate statement.  The gate it must pass first is
whether the invariant distinguishes future behaviour at all.

Test A (same-memory divergent continuation).  Partition `{1,2}^n` by the
column alone.  Within a class, compare the RW death level (least `j` with the
forced symbol non-hard-core or the forced cell `T[n+j][n] != c`).  A class
containing two sources with different death levels shows the column is not a
sufficient statistic for future survival.

Bounded augmentation.  If Test A fires, find the least `t` such that
partitioning by `(column, diagonal[:t])` -- and separately by
`(column, diagonal[-t:])` -- makes the death level constant on every class.
The user's stop condition: if no bounded `t` restores uniformity by depth 18,
the memory-based rate route is abandoned.

Control.  Partitioning by the FULL state `(column, diagonal)` must give death
level constant on every class, since the forced orbit is a function of the
state.  A failure of the control is a bug in this script, not a result.

Strong outcome for the memory route: Test A does not fire, or `t` is bounded
in `n`.  Kill: Test A fires and `t` grows with `n`.
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from itertools import product

from flip_pairing import census


def death_levels(n: int, levels: int, cells, hcs, c: int):
    total = 1 << n
    out = [levels] * total
    for idx in range(total):
        cl, hc = cells[idx], hcs[idx]
        for j in range(levels):
            if not hc[j] or cl[j] != c:
                out[idx] = j
                break
    return out


def spread(groups, death):
    """(#classes, #divergent classes, max spread, a witness class)."""
    div = 0
    worst = 0
    wit = None
    for key, members in groups.items():
        ds = {death[m] for m in members}
        if len(ds) > 1:
            div += 1
            s = max(ds) - min(ds)
            if s > worst:
                worst, wit = s, (key, members)
    return len(groups), div, worst, wit


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-n", type=int, default=8)
    ap.add_argument("--max-n", type=int, default=15)
    ap.add_argument("--witness", action="store_true")
    args = ap.parse_args()

    for n in range(args.min_n, args.max_n + 1):
        levels = n + 4
        keys, syms, cells, hcs = census(n, levels)
        cols = [k[0] for k in keys]
        dias = [k[1] for k in keys]
        srcs = list(product((1, 2), repeat=n))
        for c in (2, 3):
            death = death_levels(n, levels, cells, hcs, c)

            bycol = defaultdict(list)
            for i, cl in enumerate(cols):
                bycol[cl].append(i)
            ncl, div, worst, wit = spread(bycol, death)

            byfull = defaultdict(list)
            for i in range(1 << n):
                byfull[(cols[i], dias[i])].append(i)
            _, cdiv, _, _ = spread(byfull, death)

            tpre = tsuf = None
            for t in range(0, n + 1):
                if tpre is None:
                    g = defaultdict(list)
                    for i in range(1 << n):
                        g[(cols[i], dias[i][:t])].append(i)
                    if spread(g, death)[1] == 0:
                        tpre = t
                if tsuf is None:
                    g = defaultdict(list)
                    for i in range(1 << n):
                        g[(cols[i], dias[i][n - t:] if t else ())].append(i)
                    if spread(g, death)[1] == 0:
                        tsuf = t
                if tpre is not None and tsuf is not None:
                    break

            print(
                f"n={n:>2} c={c} | column classes={ncl:>6} divergent={div:>6} "
                f"({div / ncl:>5.1%}) max death spread={worst:>3} | "
                f"full-state control divergent={cdiv} | least t: prefix={tpre} suffix={tsuf} "
                f"(diagonal has {n} entries)"
            )
            sys.stdout.flush()
            if args.witness and wit is not None and c == 3:
                key, members = wit
                a = min(members, key=lambda m: death[m])
                b = max(members, key=lambda m: death[m])
                print(f"  witness n={n} c={c}")
                print(f"    memory_state (column) : {key}")
                print(f"    prefix_x              : {''.join(map(str, srcs[a]))}")
                print(f"    prefix_y              : {''.join(map(str, srcs[b]))}")
                print(f"    x_extension_depth     : {death[a]}")
                print(f"    y_extension_depth     : {death[b]}")
                print(f"    diagonal_x            : {dias[a]}")
                print(f"    diagonal_y            : {dias[b]}")
                print(f"    forced_syms_x         : {syms[a][:death[b] + 1]}")
                print(f"    forced_syms_y         : {syms[b][:death[b] + 1]}")
                print(f"    cells_x               : {cells[a][:death[b] + 1]}")
                print(f"    cells_y               : {cells[b][:death[b] + 1]}")
                sys.stdout.flush()


if __name__ == "__main__":
    main()

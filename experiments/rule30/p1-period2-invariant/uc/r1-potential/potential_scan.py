#!/usr/bin/env python3
"""Scan column statistics against the remaining hit-run length.

For every (n, c), every prefix W and every column u >= n-1 on its forced orbit
that is followed by at least one more hit, record rem(u) = number of further
hits, and a family of statistics of the window of column u (depths -u .. n-1
plus e_u, exactly the input of the next forced step).  Report, per statistic,
the worst value of rem - stat (a potential candidate must have rem <= stat + C
with small C and stat(col_{n-1}) <= alpha n) and the distribution of the step
difference stat(col_{u+1}) - stat(col_u) over consecutive hit pairs.

    cd .../p1-period2-invariant && uv run python uc/r1-potential/potential_scan.py
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from itertools import product

sys.path.insert(0, "uc/r1-potential")
sys.path.insert(0, ".")
from orbit_census import forced_orbit  # noqa: E402


def window(col) -> list[int]:
    """Cells at depths -u-1 .. n-1: e_u first, then states above depth n."""
    return [col.e] + list(col.states[:-1])


def stats(w: list[int]) -> dict[str, int]:
    m = len(w)
    z = [i for i, t in enumerate(w) if t == 0]
    n2 = sum(1 for t in w if t == 2)
    n1 = sum(1 for t in w if t == 1)
    n3 = sum(1 for t in w if t == 3)
    out = {
        "len": m,
        "Z": len(z),
        "N1": n1,
        "N2": n2,
        "N3": n3,
        "Lo0": len(z) + n2,
        "top0": (z[0] if z else m),
        "bot0": (m - 1 - z[-1] if z else m),
        "zero_runs": sum(1 for i in z if i == 0 or w[i - 1] != 0),
    }
    # nonzero-index statistics read from the bottom (depth n-1 upward)
    p = 0
    e_even2 = 0
    e_odd2 = 0
    z_even = 0
    z_odd = 0
    for t in reversed(w):
        if t == 0:
            if p == 0:
                z_even += 1
            else:
                z_odd += 1
        else:
            if t == 2:
                if p == 0:
                    e_even2 += 1
                else:
                    e_odd2 += 1
            p ^= 1
    out["twos_after_even_nz"] = e_even2
    out["twos_after_odd_nz"] = e_odd2
    out["zeros_after_even_nz"] = z_even
    out["zeros_after_odd_nz"] = z_odd
    out["E_parity_terms"] = z_even + e_odd2
    # longest run of nonzero cells, longest run of {1,3}
    best = cur = 0
    for t in w:
        cur = cur + 1 if t != 0 else 0
        best = max(best, cur)
    out["max_nonzero_run"] = best
    best = cur = 0
    for t in w:
        cur = cur + 1 if t in (1, 3) else 0
        best = max(best, cur)
    out["max_13_run"] = best
    # zeros in the top half / bottom half
    half = m // 2
    out["Z_top_half"] = sum(1 for i in z if i < half)
    out["Z_bot_half"] = sum(1 for i in z if i >= half)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-n", type=int, default=6)
    ap.add_argument("--max-n", type=int, default=13)
    ap.add_argument("--log", default="uc/r1-potential/potential_scan.log")
    args = ap.parse_args()
    worst: dict[str, tuple[int, tuple]] = {}
    diffs: dict[str, Counter] = defaultdict(Counter)
    death_diffs: dict[str, Counter] = defaultdict(Counter)
    start_max: dict[tuple, dict[str, int]] = {}
    rem_hist: Counter = Counter()
    with open(args.log, "w") as log:
        for n in range(args.min_n, args.max_n + 1):
            for target in (2, 3):
                smax: dict[str, int] = defaultdict(int)
                for source in product((1, 2), repeat=n):
                    cols = []
                    dead = None
                    for u, e, hit, col in forced_orbit(source, target, n + 3):
                        if hit:
                            cols.append(col)
                        else:
                            dead = col
                    # cols[i] is column n+i, hit; rem for column n+i is len(cols)-1-i
                    # the starting column n-1 (from W) is not in cols; its window is
                    # the input to column n; skip it for stats except via W itself
                    k = len(cols)
                    prev_st = None
                    for i, col in enumerate(cols):
                        rem = k - 1 - i
                        st = stats(window(col))
                        if i == 0:
                            for key, val in st.items():
                                smax[key] = max(smax[key], val)
                        if rem >= 1:
                            rem_hist[(n, target, rem)] += 1
                            for key, val in st.items():
                                gap = rem - val
                                if key not in worst or gap > worst[key][0]:
                                    worst[key] = (gap, (n, target, "".join(map(str, source)), col.u, rem, val))
                        if prev_st is not None:
                            for key in st:
                                diffs[key][st[key] - prev_st[key]] += 1
                        prev_st = st
                    if dead is not None and cols:
                        st = stats(window(dead))
                        for key in st:
                            death_diffs[key][st[key] - prev_st[key]] += 1
                start_max[(n, target)] = dict(smax)
        print("== max of each statistic over first hit columns (u = n), per (n, c) ==", file=log)
        keys = sorted(next(iter(start_max.values())).keys())
        print("n c " + " ".join(f"{k:>18s}" for k in keys), file=log)
        for (n, target), sm in sorted(start_max.items()):
            print(f"{n:2d} {target} " + " ".join(f"{sm[k]:18d}" for k in keys), file=log)
        print("\n== worst gap rem - stat over all hit columns with rem >= 1 (n, c, W, u, rem, stat) ==", file=log)
        for key in keys:
            print(f"{key:>20s}: {worst[key][0]:4d}  at {worst[key][1]}", file=log)
        print("\n== step differences stat(col_{u+1}) - stat(col_u) over consecutive hit pairs ==", file=log)
        for key in keys:
            d = diffs[key]
            tot = sum(d.values())
            desc = " ".join(f"{v:+d}:{d[v]}" for v in sorted(d))
            print(f"{key:>20s}: {desc}   (pairs={tot})", file=log)
        print("\n== step differences at the death step (last hit column -> failing column) ==", file=log)
        for key in keys:
            d = death_diffs[key]
            desc = " ".join(f"{v:+d}:{d[v]}" for v in sorted(d))
            print(f"{key:>20s}: {desc}", file=log)
    print(f"log written to {args.log}")


if __name__ == "__main__":
    main()

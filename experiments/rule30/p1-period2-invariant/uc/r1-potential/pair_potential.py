#!/usr/bin/env python3
"""Ordered (pair-count) quantities along consecutive hits.

The hit condition is the parity of an ORDERED pair count (BRIEF section 3,
set form): Phi = (|Z|+|W2|)(1+m+|Z|) + #{(x,y): x<y, x in N, y in Z or W2}.
potential_scan.py tested only zeroth-order counts.  This script tests the
integer-valued ordered pair counts themselves, on the window of column u
(e_u first, then depths -u .. n-1), for monotonicity along consecutive hits.

Quantities (all integers, all of unbounded radius, none a sum of local terms):
    G_NE   #{x<y : x nonzero, y even (0 or 2)}
    G_NZ   #{x<y : x nonzero, y == 0}
    G_N2   #{x<y : x nonzero, y == 2}
    G_EN   #{x<y : x even, y nonzero}
    X_NE   2*G_NE - |N|*|Even|          (ordering excess, 0 = random order)
    G_cc, G_cp, G_pp   G_NE restricted to (cone,cone), (cone,peel), (peel,peel)
    S_even  sum of positions (from the top) of even cells
    S_zero  sum of positions of zero cells
    S_even_bot  sum of positions from the bottom of even cells

For each quantity: distribution of stat(u+1)-stat(u) over consecutive hit
pairs, the same at the death step, and the worst value of rem(u)-stat(u).

    cd .../p1-period2-invariant && uv run python uc/r1-potential/pair_potential.py
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
    return [col.e] + list(col.states[:-1])


def pair_stats(w: list[int], u: int) -> dict[str, int]:
    m = len(w)
    cone_len = u + 1  # e_u plus depths -u .. -1
    out: dict[str, int] = {}
    nz_before = 0
    ev_before = 0
    g_ne = g_nz = g_n2 = g_en = 0
    g_cc = g_cp = g_pp = 0
    nz_cone = 0
    n_count = ev_count = 0
    s_even = s_zero = s_even_bot = 0
    for i, t in enumerate(w):
        even = (t & 1) == 0
        nonzero = t != 0
        in_cone = i < cone_len
        if even:
            g_ne += nz_before
            if t == 0:
                g_nz += nz_before
                s_zero += i
            else:
                g_n2 += nz_before
            if in_cone:
                g_cc += nz_before
            else:
                g_cp += nz_cone
                g_pp += nz_before - nz_cone
            s_even += i
            s_even_bot += m - 1 - i
            ev_before += 1
            ev_count += 1
        if nonzero:
            g_en += ev_before
            nz_before += 1
            n_count += 1
            if in_cone:
                nz_cone += 1
    out["G_NE"] = g_ne
    out["G_NZ"] = g_nz
    out["G_N2"] = g_n2
    out["G_EN"] = g_en
    out["X_NE"] = 2 * g_ne - n_count * ev_count
    out["G_cc"] = g_cc
    out["G_cp"] = g_cp
    out["G_pp"] = g_pp
    out["S_even"] = s_even
    out["S_zero"] = s_zero
    out["S_even_bot"] = s_even_bot
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-n", type=int, default=6)
    ap.add_argument("--max-n", type=int, default=13)
    ap.add_argument("--log", default="uc/r1-potential/pair_potential.log")
    args = ap.parse_args()
    worst: dict[str, tuple[int, tuple]] = {}
    diffs: dict[str, Counter] = defaultdict(Counter)
    death_diffs: dict[str, Counter] = defaultdict(Counter)
    sign_by_n: dict[tuple, dict[str, list[int]]] = {}
    with open(args.log, "w") as log:
        for n in range(args.min_n, args.max_n + 1):
            for target in (2, 3):
                signs: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0])  # neg, zero, pos over hit pairs
                for source in product((1, 2), repeat=n):
                    cols = []
                    dead = None
                    for u, e, hit, col in forced_orbit(source, target, n + 3):
                        if hit:
                            cols.append(col)
                        else:
                            dead = col
                    k = len(cols)
                    prev = None
                    for i, col in enumerate(cols):
                        rem = k - 1 - i
                        st = pair_stats(window(col), col.u)
                        if rem >= 1:
                            for key, val in st.items():
                                gap = rem - val
                                if key not in worst or gap > worst[key][0]:
                                    worst[key] = (gap, (n, target, "".join(map(str, source)), col.u, rem, val))
                        if prev is not None:
                            for key in st:
                                d = st[key] - prev[key]
                                diffs[key][d] += 1
                                signs[key][1 if d == 0 else (0 if d < 0 else 2)] += 1
                        prev = st
                    if dead is not None and prev is not None:
                        st = pair_stats(window(dead), dead.u)
                        for key in st:
                            death_diffs[key][st[key] - prev[key]] += 1
                sign_by_n[(n, target)] = dict(signs)
        keys = sorted(diffs)
        print("== sign of stat(u+1) - stat(u) over consecutive hit pairs, per (n, c): neg/zero/pos ==", file=log)
        for key in keys:
            print(f"[{key}]", file=log)
            for (n, target), signs in sorted(sign_by_n.items()):
                s = signs.get(key, [0, 0, 0])
                tot = sum(s) or 1
                print(f"   n={n:2d} c={target}: {s[0]:6d} {s[1]:6d} {s[2]:6d}   frac_pos={s[2]/tot:.3f} frac_neg={s[0]/tot:.3f}", file=log)
        print("\n== worst gap rem - stat over all hit columns with rem >= 1 (n, c, W, u, rem, stat) ==", file=log)
        for key in keys:
            print(f"{key:>12s}: {worst[key][0]:5d}  at {worst[key][1]}", file=log)
        print("\n== pooled step differences over consecutive hit pairs (compact: min, quartiles, max) ==", file=log)
        for key in keys:
            d = diffs[key]
            vals = sorted(d.elements())
            q = lambda p: vals[min(len(vals) - 1, int(p * len(vals)))]
            print(f"{key:>12s}: n={len(vals)} min={vals[0]} q25={q(0.25)} med={q(0.5)} q75={q(0.75)} max={vals[-1]}  zero-frac={d[0]/len(vals):.3f}", file=log)
        print("\n== pooled step differences at the death step ==", file=log)
        for key in keys:
            d = death_diffs[key]
            vals = sorted(d.elements())
            q = lambda p: vals[min(len(vals) - 1, int(p * len(vals)))]
            print(f"{key:>12s}: n={len(vals)} min={vals[0]} q25={q(0.25)} med={q(0.5)} q75={q(0.75)} max={vals[-1]}", file=log)
    print(f"log written to {args.log}")


if __name__ == "__main__":
    main()

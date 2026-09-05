#!/usr/bin/env python3
"""Eventual periodicity in u of the region rows d = n-1, n-2, ... (top down).

In the diagonal form the region u >= n is driven by the constant row d = n
and the left boundary column n-1.  Row d is produced from row d+1 by the
transducer T[u][d] = psi(T[u-1][d], T[u][d+1]) along u, so it is eventually
periodic in u.  This measures the eventual period p(d) and the transient
length t(d) (first u at which the periodic regime starts) for the top rows,
for several column n-1 words, with u running to n + horizon.

Run:  cd <work dir> && uv run python uc/r1-quadratic/qf_rows.py --n 8 --horizon 600 --rows 24
"""

from __future__ import annotations

import argparse
from itertools import product

from qf_common import forward_columns, psi


def region_rows(col_nm1: dict[int, int], n: int, horizon: int, rows: int) -> dict[int, list[int]]:
    """Rows d = n-1 .. n-rows of the region for u = n .. n+horizon-1."""
    out: dict[int, list[int]] = {n - j: [] for j in range(1, rows + 1)}
    prev = dict(col_nm1)
    for u in range(n, n + horizon):
        col: dict[int, int] = {n: c_global}
        for d in range(n - 1, -u - 2, -1):
            left = prev[d] if d in prev else 3
            col[d] = psi(left, col[d + 1])
        for j in range(1, rows + 1):
            d = n - j
            if d >= -u - 1:
                out[d].append(col[d])
        prev = col
    return out


def eventual_period(seq: list[int]) -> tuple[int, int]:
    """(period, transient) of an eventually periodic sequence, or (-1, -1)."""
    L = len(seq)
    for p in range(1, L // 3 + 1):
        # find smallest t such that seq[t:] is p-periodic
        t = L - p
        while t > 0 and seq[t - 1] == seq[t - 1 + p]:
            t -= 1
        if t <= L // 3:
            return p, t
    return -1, -1


c_global = 2


def main() -> None:
    global c_global
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--horizon", type=int, default=600)
    ap.add_argument("--rows", type=int, default=24)
    ap.add_argument("--sources", type=int, default=4)
    args = ap.parse_args()
    n = args.n
    srcs = list(product((1, 2), repeat=n))
    step = max(1, len(srcs) // args.sources)
    for c in (2, 3):
        c_global = c
        print(f"n={n} c={c}: row d: (period, transient) per source column n-1; horizon {args.horizon}")
        for src in srcs[::step][: args.sources]:
            col = forward_columns(src)[n - 1]
            rows = region_rows(col, n, args.horizon, args.rows)
            desc = []
            for j in range(1, args.rows + 1):
                d = n - j
                p, t = eventual_period(rows[d])
                desc.append(f"d={d}:({p},{t})")
            print(f"  W={''.join(map(str, src))}: " + " ".join(desc))


if __name__ == "__main__":
    main()

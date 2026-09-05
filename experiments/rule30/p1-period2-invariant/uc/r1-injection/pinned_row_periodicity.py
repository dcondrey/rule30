#!/usr/bin/env python3
"""Top-down structure of the pinned wedge: row n-j below the pin is eventually
periodic in u, with a preperiod that grows with j.  How fast?

Diagonal form (BRIEF section 3): T[u][n] = c for u >= n, T[m][m] = D_m for
m < n, and T[u][d] = CONE_INV[T[u-1][d]][T[u][d+1]] below.  Row n-j of the
pinned wedge (u >= n) depends only on D_{n-j}..D_{n-1}, so it is a
deterministic 4-state walk driven by the row above.  Each row is eventually
periodic in u; this script measures, for every choice of (D_{n-j}, ..., D_{n-1})
at j <= 6 and for random choices at j <= 14, the preperiod t_j and period p_j
of row n-j (u from n onward), and prints the maximum over choices.

If t_j grows exponentially in j then only O(log k) rows below the pin are in
their periodic regime by column n+k, while the edge symbol e_u sits n+u+1 rows
below the pin: the top-down triangular structure never reaches the constraint.
That is obstruction A (the O(log t) wall) in the diagonal form.

Usage: cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-injection/pinned_row_periodicity.py
"""

from __future__ import annotations

import random
import sys
from itertools import product

sys.path.insert(0, ".")
from psi_kernel import CONE  # noqa: E402

CONE_INV = [[0] * 4 for _ in range(4)]
for _l in range(4):
    for _r in range(4):
        CONE_INV[_l][CONE[_l][_r]] = _r


def rows_below_pin(D_tail: tuple[int, ...], c: int, U: int) -> list[list[int]]:
    """Rows n-1, n-2, ..., n-j of the pinned wedge at columns u = n .. n+U-1.

    D_tail = (D_{n-j}, ..., D_{n-1}).  Row n-i at column u = n+t is
    T[n+t][n-i]; we also need the left part T[u][n-i] for n-i <= u < n, which
    depends on D_{n-i}..D_{n-1} only, and is computed the same way.
    """
    j = len(D_tail)
    # grid[i][t]: T[u][n-i] with u = n - j + t, for t = 0 .. j + U - 1
    width = j + U
    grid = [[None] * width for _ in range(j + 1)]
    for t in range(width):
        u = width - 1  # unused
    # row i = 0 is the pin row d = n: defined for u >= n, i.e. t >= j
    for t in range(j, width):
        grid[0][t] = c
    for i in range(1, j + 1):
        d = -i  # depth n - i
        m = j - i  # column index (t) where the diagonal cell sits: u = n - i => t = j - i
        grid[i][m] = D_tail[m]
        for t in range(m + 1, width):
            above = grid[i - 1][t]
            if above is None:
                # above the pin row at columns u < n: the cell T[u][n-i+1] for u >= n-i+1
                raise RuntimeError("missing cell")
            grid[i][t] = CONE_INV[grid[i][t - 1]][above]
    return [row[j:] for row in grid[1:]]  # rows n-1 .. n-j at u >= n


def preperiod_period(seq: list[int]) -> tuple[int, int]:
    """Smallest (t, p) with seq[s] == seq[s+p] for all s >= t, inside the sample."""
    L = len(seq)
    best = None
    for p in range(1, L // 2):
        t = L - p
        while t > 0 and seq[t - 1] == seq[t - 1 + p]:
            t -= 1
        # require the periodic tail to cover at least half the sample
        if L - t >= 2 * p + 8:
            if best is None or t < best[0] or (t == best[0] and p < best[1]):
                best = (t, p)
            if t == 0:
                break
    return best if best else (-1, -1)


def main() -> None:
    U = 4096
    rng = random.Random(1)
    print("row n-j below the pin: max preperiod t_j and the periods seen, over all D tails (j<=6) or 200 random (j<=14)")
    for c in (2, 3):
        print(f"c = {c}")
        for j in range(1, 15):
            if j <= 6:
                tails = list(product(range(4), repeat=j))
            else:
                tails = [tuple(rng.randrange(4) for _ in range(j)) for _ in range(200)]
            tmax, periods = 0, set()
            for D_tail in tails:
                rows = rows_below_pin(D_tail, c, U)
                t, p = preperiod_period(rows[j - 1])
                if t < 0:
                    print(f"   j={j}: no period detected within U={U} for tail {D_tail}")
                    tmax = 10 ** 9
                    break
                tmax = max(tmax, t)
                periods.add(p)
            print(f"   j={j:>2}: max preperiod = {tmax:>5}, periods = {sorted(periods)}, tails checked = {len(tails)}")
            sys.stdout.flush()


if __name__ == "__main__":
    main()

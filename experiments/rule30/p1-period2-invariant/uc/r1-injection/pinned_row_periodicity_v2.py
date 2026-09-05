#!/usr/bin/env python3
"""Top-down structure of the pinned wedge: row n-j below the pin is eventually
periodic in u; measure preperiod t_j and period p_j versus j.

Diagonal form (BRIEF section 3): T[u][n] = c for u >= n, T[m][m] = D_m for
m < n, T[u][d] = CONE_INV[T[u-1][d]][T[u][d+1]] below.  Row n-j at columns
u >= n depends only on D_{n-j}..D_{n-1}, and is a 4-state walk driven by the
row above; with the row above periodic of period P from some column on, the
pair (u mod P, cell) determines the future, so the first repeat of that pair
gives the exact preperiod and a period (reduced to its minimal divisor).

Exhaustive over all 4^j tails for j <= 5, random tails for j <= 12.  Prints
max t_j and the set of minimal periods.  If t_j grows exponentially in j then
only O(log k) rows below the pin are periodic by column n+k, while the edge
symbol e_u is n+u+1 rows below the pin: obstruction A in the diagonal form.

v2 replaces pinned_row_periodicity.py, which used an O(L^2) detector and a
`timeout` binary this machine lacks; that file never ran.

Usage: cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-injection/pinned_row_periodicity_v2.py
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


def minimal_period(seq: list[int], start: int, p: int) -> int:
    """Reduce a known period p of seq[start:] to the minimal one."""
    tail = seq[start:]
    for q in range(1, p + 1):
        if p % q:
            continue
        if all(tail[i] == tail[i + q] for i in range(len(tail) - q)):
            return q
    return p


def row_periodicity(D_tail: tuple[int, ...], c: int, U: int):
    """For rows n-1..n-j: (preperiod, period) at columns u >= n, or None if not found within U."""
    j = len(D_tail)
    width = j + U
    prev = [c] * width  # pin row, defined at t >= j (u >= n); left part unused
    prev_pre, prev_per = 0, 1
    out = []
    for i in range(1, j + 1):
        m = j - i
        row = [None] * width
        row[m] = D_tail[m]
        for t in range(m + 1, width):
            row[t] = CONE_INV[row[t - 1]][prev[t]]
        # periodicity of row[t] for t >= j (u >= n), driven by prev with period prev_per after prev_pre
        seen = {}
        pre = per = None
        for t in range(j + prev_pre, width):
            key = ((t - j - prev_pre) % prev_per, row[t])
            if key in seen:
                pre, per = seen[key] - j, t - seen[key]
                break
            seen[key] = t
        if pre is None:
            return out + [None] * (j - i + 1)
        per = minimal_period(row[j:], pre, per)
        out.append((pre, per))
        prev, prev_pre, prev_per = row, pre, per
    return out


def main() -> None:
    rng = random.Random(1)
    for c in (2, 3):
        print(f"c = {c}: row n-j, max preperiod t_j over tails, minimal periods seen")
        for j in range(1, 13):
            if j <= 5:
                tails = list(product(range(4), repeat=j))
            else:
                tails = [tuple(rng.randrange(4) for _ in range(j)) for _ in range(60)]
            U = 40000 if j <= 10 else 200000
            tmax, periods, fails = 0, set(), 0
            for D_tail in tails:
                res = row_periodicity(D_tail, c, U)
                r = res[j - 1]
                if r is None:
                    fails += 1
                    continue
                tmax = max(tmax, r[0])
                periods.add(r[1])
            print(f"   j={j:>2}: tails={len(tails):>4}  max t_j={tmax:>7}  periods={sorted(periods)}  undetected(within U={U})={fails}")
            sys.stdout.flush()


if __name__ == "__main__":
    main()

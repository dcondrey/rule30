#!/usr/bin/env python3
"""Three-part decomposition of the forced column window along real RW runs (v2: corrected bookkeeping).

At level k the survivors carry column u = n+k-1, which satisfies T[u][n] = c
for k >= 1 and is therefore on the monoid tower.  Its window [-u-1, n) has
2n+k cells; the top 2k cells (depths <= u-2n) are determined by Q[:k]; the
bottom j* rows are universal; the middle has 2n - k - j* cells.

For a survivor at level k (column u = n+k, window depths [-u-1, n)):

  top     depths [-u-1, k-n]      2k+2 cells, a function of Q[:k+1] only
                                  (light cone: T[u][d] depends on e_j, j >= ceil((u-d-1)/2))
  bottom  depths (n-j*, n)        rows n-1..n-j* already in the universal
                                  period-4, 4-phase regime of the monoid tower
  middle  the rest                the only part that still depends on W

Part 1 checks that the four joint phase classes of the universal pattern are
its four cyclic shifts in u, and that the universal pattern is eventually
periodic in the row index j as well (computed from one seed with a long tail).

Part 2 replays the complete RW search (n = 8..13, both c) and, for every
survivor at every level, measures j*(k) = number of bottom rows matching the
universal pattern (best phase), the middle length m_k = 2n+k+1 - (2k+2) - j*,
and reports min/mean/max over survivors.  If m_k reaches 0 before the run
ends, the tail of that run is a finite-state system fed by Q.
"""

from __future__ import annotations

import sys
from itertools import product

import numpy as np

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-transducer")

from psi_kernel import Endpoint  # noqa: E402
from d8_kernel import allowed_set, column_cells, holonomy  # noqa: E402
from peel_tower_phase import PSI  # noqa: E402


def universal_pattern(c: int, J: int, K: int) -> np.ndarray:
    """rows[j-1, i] = x_{n+i}(n-j) from the all-zero seed column."""
    rows = np.empty((J, K), dtype=np.int8)
    below = np.full(K, c, dtype=np.int8)
    for j in range(1, J + 1):
        prev = 0
        for i in range(K):
            prev = int(PSI[below[i], prev])
            rows[j - 1, i] = prev
        below = rows[j - 1]
    return rows


def part1(c: int) -> np.ndarray:
    J, K = 60, 400
    U = universal_pattern(c, J, K)
    # phase classes are shifts?  compare the exhaustive 4 joint tails (rows 1..9) with shifts of U
    from peel_tower_phase import tower

    rows = tower(c, 9, 120)
    block = np.stack(rows, axis=1)  # (M, 9, 120)
    tails = {row.tobytes(): row for row in block[:, :, 60:100].reshape(block.shape[0], -1)}
    shifts = set()
    for s in range(4):
        shifts.add(U[:9, 60 + s : 100 + s].reshape(-1).tobytes())
    print(f"c={c}: exhaustive joint tails {len(tails)}, shifts of the one-seed pattern {len(shifts)}, "
          f"equal as sets: {set(tails) == shifts}")
    # periodicity in j of the universal 4-tuple at columns beyond every transient
    col0 = 300  # beyond transient 1.8*60 = 108
    tuples = [tuple(int(v) for v in U[j - 1, col0 : col0 + 4]) for j in range(1, J + 1)]
    per = None
    for p in range(1, J // 2):
        if all(tuples[j] == tuples[j + p] for j in range(4, J - p)):
            per = p
            break
    print(f"c={c}: universal 4-tuples by row j (columns {col0}..{col0 + 3}):")
    for j in range(1, 25):
        print(f"   j={j:2d} {tuples[j - 1]}")
    print(f"c={c}: period in j of the universal pattern (rows >= 5): {per}")
    return U


def matched_rows(window_bottom_up: list[int], U: np.ndarray, u_index: int) -> int:
    """window_bottom_up[j-1] = x_u(n-j).  Best phase count of contiguous matches from the bottom."""
    best = 0
    for phase in range(4):
        col = 200 + ((u_index + phase) % 4)
        cnt = 0
        for j in range(1, len(window_bottom_up) + 1):
            if j > U.shape[0]:
                break
            if window_bottom_up[j - 1] == U[j - 1, col]:
                cnt += 1
            else:
                break
        best = max(best, cnt)
    return best


def part2(n: int, c: int, U: np.ndarray) -> None:
    allowed = set(allowed_set(c))
    level = []
    for W in product((1, 2), repeat=n):
        ep = Endpoint()
        for s in W:
            ep.append(s)
        level.append((ep, list(W)))
    k = 0
    print(f"\nn={n} c={c}")
    print("  k   N_k   window  top   j*: min mean max   middle m_k: min mean max")
    while level and k < n + 2:
        js = []
        nxt = []
        for ep, word in level:
            u = ep.length - 1
            cells = column_cells(ep)
            window = cells[: n + u + 1]
            # bottom-up list: x_u(n-1), x_u(n-2), ... : depth n-j is index (n-j)+u+1
            bottom_up = [window[(n - j) + u + 1] for j in range(1, n + u + 2)]
            js.append(matched_rows(bottom_up, U, u))
            g = holonomy(window)
            if g in allowed:
                forced = [s for s in (1, 2) if ep.peek(s)[1][n] == c][0]
                if word[-1] == 1 and forced == 1:
                    continue
                col, diag = ep.peek(forced)
                nep = Endpoint()
                nep.column = col + [forced]
                nep.diagonal = diag
                nep.length = ep.length + 1
                nxt.append((nep, word + [forced]))
        wlen = 2 * n + k
        top = 2 * k
        mids = [wlen - top - j for j in js]
        print(f"{k:3d} {len(level):6d} {wlen:6d} {top:5d}   {min(js):3d} {np.mean(js):5.1f} {max(js):3d}"
              f"        {min(mids):3d} {np.mean(mids):5.1f} {max(mids):3d}")
        level = nxt
        k += 1


def main() -> None:
    pats = {c: part1(c) for c in (2, 3)}
    for n in (8, 10, 12, 13, 14):
        for c in (2, 3):
            part2(n, c, pats[c])


if __name__ == "__main__":
    main()

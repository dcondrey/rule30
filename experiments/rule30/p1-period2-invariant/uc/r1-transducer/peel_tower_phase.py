#!/usr/bin/env python3
"""Phase bits of the peel-side monoid tower under a constant row n = c^*.

Along an admissible RW run the peel-side window [0, n] of the forced columns
is autonomous: row n is c^*, and row n-j (u >= n) is the orbit
    x_u(n-j) = psi_{x_u(n-j+1)}(x_{u-1}(n-j)),   psi_y(x) = lam(x)^{-1} . y,
seeded by column n-1's cell x_{n-1}(n-j).  The maps psi_y generate the
13-element inverse-lift monoid (capsule section 3), which has only one- and
two-cycles, so every row becomes eventually periodic in u and forgets its seed
up to finitely many phase bits.

Measured here, over ALL 4^J seed columns (x_{n-1}(n-J), ..., x_{n-1}(n-1)):
  P_j(tau)   number of distinct tails (x_u(n-j))_{u in [n+tau, n+tau+32)}
  P_j        min over tau of P_j(tau): the number of phase classes of row n-j
  tau_j      the first tau attaining P_j: the transient of row n-j
If log2 P_j grows linearly in j, the bottom of the window is NOT a bounded
state and the "universal bottom" idea is dead; if it stays bounded the bottom
is a finite-state object.
"""

from __future__ import annotations

import sys

import numpy as np

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-transducer")

from d8_kernel import LAM, act, cell_of, inv, state  # noqa: E402

PSI = np.array(
    [[cell_of(act(inv(LAM[x]), state(y))) for x in range(4)] for y in range(4)], dtype=np.int8
)  # PSI[y, x] = psi_y(x)


def tower(c: int, J: int, K: int) -> list[np.ndarray]:
    M = 4 ** J
    idx = np.arange(M)
    seeds = [((idx // 4 ** j) % 4).astype(np.int8) for j in range(J)]  # seeds[j-1] = x_{n-1}(n-j)
    rows = []  # rows[j-1][:, i] = x_{n+i}(n-j)
    below = np.full((M, K), c, dtype=np.int8)  # row n
    for j in range(1, J + 1):
        row = np.empty((M, K), dtype=np.int8)
        prev = seeds[j - 1]
        for i in range(K):
            prev = PSI[below[:, i], prev]
            row[:, i] = prev
        rows.append(row)
        below = row
    return rows


def phase_classes(row: np.ndarray, window: int) -> tuple[int, int, list[int]]:
    K = row.shape[1]
    counts = []
    for tau in range(0, K - window + 1):
        seg = row[:, tau : tau + window]
        packed = np.zeros(seg.shape[0], dtype=np.int64)
        for i in range(window):
            packed = packed * 4 + seg[:, i]
        counts.append(len(np.unique(packed)))
    best = min(counts)
    return best, counts.index(best), counts


def main() -> None:
    J, K, window = 9, 72, 32
    for c in (2, 3):
        print(f"\nc = {c}: rows n-j, all 4^{J} seeds, tails of length {window}")
        print("  j   phase classes P_j   log2   transient tau_j   P_j(tau) for tau=0..7")
        rows = tower(c, J, K)
        for j, row in enumerate(rows, start=1):
            best, tau, counts = phase_classes(row, window)
            print(f"{j:3d} {best:14d} {np.log2(best):8.2f} {tau:12d}      {counts[:8]}")


if __name__ == "__main__":
    main()

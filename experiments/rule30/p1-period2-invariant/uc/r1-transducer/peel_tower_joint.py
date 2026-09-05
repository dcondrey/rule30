#!/usr/bin/env python3
"""Joint phase classes and periods of the peel-side monoid tower.

Extends peel_tower_phase.py with a longer tail window (64) and more columns
(160) and reports, for rows n-j0 .. n-J taken TOGETHER, the number of distinct
joint tails over all 4^J seeds, plus the eventual period of each row and of
the joint block.  If the joint count stays at 4 the whole bottom block of the
forced window is a 2-bit object after its transient.
"""

from __future__ import annotations

import sys

import numpy as np

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-transducer")

from peel_tower_phase import tower  # noqa: E402


def distinct_tails(block: np.ndarray, tau: int, window: int) -> int:
    seg = block[:, :, tau : tau + window].reshape(block.shape[0], -1)
    packed = np.zeros(seg.shape[0], dtype=object)
    # hash rows exactly
    return len({row.tobytes() for row in seg})


def period(tail: np.ndarray) -> int:
    for p in range(1, len(tail) // 2 + 1):
        if np.array_equal(tail[:-p], tail[p:]):
            return p
    return -1


def main() -> None:
    J, K, window = 9, 160, 64
    for c in (2, 3):
        rows = tower(c, J, K)
        block = np.stack(rows, axis=1)  # (M, J, K), block[:, j-1, i] = x_{n+i}(n-j)
        tau_all = 40
        print(f"\nc = {c}: J = {J} rows, K = {K} columns, tail window {window}, tails taken from tau = {tau_all}")
        print("  j   P_j(tau=40)   period of row n-j (seed 0)   periods over all seeds")
        for j in range(1, J + 1):
            pj = distinct_tails(block[:, j - 1 : j, :], tau_all, window)
            pers = set()
            for s in range(0, block.shape[0], max(1, block.shape[0] // 4096)):
                pers.add(period(block[s, j - 1, tau_all:]))
            print(f"{j:3d} {pj:12d}   {period(block[0, j - 1, tau_all:]):8d}                {sorted(pers)}")
        print("  joint block rows n-j0..n-J:")
        print("  j0   distinct joint tails (tau=40)   joint period (seed 0)")
        for j0 in range(1, J + 1):
            pj = distinct_tails(block[:, j0 - 1 : J, :], tau_all, window)
            joint = block[0, j0 - 1 : J, tau_all:]
            per = -1
            for p in range(1, (K - tau_all) // 2 + 1):
                if np.array_equal(joint[:, :-p], joint[:, p:]):
                    per = p
                    break
            print(f"{j0:4d} {pj:16d}                {per:6d}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact-hash version of the peel-tower kill test (all 4^J seeds, one row at a time).

Replaces the transient column of kill_tests.py --tower, whose 48-symbol int64
packing overflowed (4^47 > 2^63) and therefore ignored the first 16 symbols
of every window.  Here windows are 32 symbols (4^32 = 2^64 wraps injectively
in int64) and the transient tau_j is the first column t at which the number
of distinct 32-symbol windows [t, t+32) over all seeds equals its eventual
value.  Joint classes and periods are recomputed as well.
"""

from __future__ import annotations

import sys
import time

import numpy as np

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-transducer")

from peel_tower_phase import PSI  # noqa: E402


def pack32(seg: np.ndarray) -> np.ndarray:
    p = np.zeros(seg.shape[0], dtype=np.int64)
    for i in range(32):
        p = p * 4 + seg[:, i]
    return p


def main(J: int, K: int = 128, tau: int = 80) -> None:
    M = 4 ** J
    idx = np.arange(M, dtype=np.int64)
    for c in (2, 3):
        t0 = time.time()
        below = np.full((M, K), c, dtype=np.int8)
        joint = np.zeros(M, dtype=np.int64)
        for j in range(1, J + 1):
            prev = ((idx // 4 ** (j - 1)) % 4).astype(np.int8)
            row = np.empty((M, K), dtype=np.int8)
            for i in range(K):
                prev = PSI[below[:, i], prev]
                row[:, i] = prev
            _, per_row = np.unique(pack32(row[:, tau : tau + 32]), return_inverse=True)
            n_row = int(per_row.max()) + 1
            trans = next(
                (t for t in range(0, tau + 1) if len(np.unique(pack32(row[:, t : t + 32]))) == n_row), None
            )
            joint = joint * n_row + per_row
            _, joint = np.unique(joint, return_inverse=True)
            n_joint = int(joint.max()) + 1
            tail = row[0, tau:]
            per = next((p for p in range(1, 33) if np.array_equal(tail[:-p], tail[p:])), -1)
            print(f"tower c={c} J={J} row j={j}: classes={n_row} joint={n_joint} transient={trans} period={per}",
                  flush=True)
            below = row
        print(f"tower c={c} J={J} done [{time.time() - t0:.0f}s]", flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]))

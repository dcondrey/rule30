#!/usr/bin/env python3
"""Equidistribution of the D8 holonomy of the last free column over binary W.

For W in {1,2}^n let G(W) in D8 be the holonomy of column n-1 over depths
[-n, n-1] (the whole column, from the endpoint symbol e_{n-1} to the peel
diagonal).  The forced symbol e_n is t . G^{-1} . x_c, so the k = 1 rotated
wedge constraint is G(W) in A_c, a 4-element subset.

Measured, exhaustively over all 2^n W with a vectorised column build:

  dev_n = max_g | #{W : G(W) = g} - 2^(n-3) |

and its ratio to 2^(n/2).  If dev_n <= C 2^(theta n) with theta < 1 the first
constraint is asymptotically one bit.  Square-root cancellation is theta = 1/2.

Also, with the FOUR-STATE forced continuation (every forced symbol is the
unique symbol in {0..3} giving T[u][n] = c, no binary requirement), the vector
(E(e_n), ..., E(e_{n+k-1})) in Z_2^k is histogrammed for k = 1..4 and c = 2, 3,
and dev_{n,k} = max_v | count(v) - 2^(n-k) | is reported the same way.

Cross-check: the k = 1, c = 2 count of v = 0 must equal E_0 of
rw_holonomy_census.py (that census reports 4020 at n = 13, c = 2).
"""

from __future__ import annotations

import sys
import time

import numpy as np

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-transducer")

from psi_kernel import BOUNDARY, CONE  # noqa: E402
from d8_kernel import D8, LAM, T10, act, allowed_set, inv, mul, state, cell_of  # noqa: E402

CONE_T = np.array(CONE, dtype=np.int8)  # CONE_T[l, r]
BOUND = np.array(BOUNDARY, dtype=np.int8)
IDX = {g: i for i, g in enumerate(D8)}
# MUL[i, j] = index of D8[i] . D8[j]
MUL = np.array([[IDX[mul(D8[i], D8[j])] for j in range(8)] for i in range(8)], dtype=np.int8)
LAMI = np.array([IDX[LAM[c]] for c in range(4)], dtype=np.int8)
# forced 4-state symbol from holonomy index and c: cell(t . g^-1 . x_c)
FORCED = np.array(
    [[cell_of(act(T10, act(inv(D8[i]), state(c)))) for c in range(4)] for i in range(8)],
    dtype=np.int8,
)
E_OF = np.array([1, 0, 0, 1], dtype=np.int8)  # E(cell)


class Columns:
    """All endpoint prefixes at once: cells[:, j] holds one depth for every W."""

    def __init__(self, words: np.ndarray) -> None:
        # words: (M, n) int8 in {0..3}
        self.M = words.shape[0]
        self.cells = None  # (M, 2u+2): depths -u-1 .. u
        for j in range(words.shape[1]):
            self.append(words[:, j])

    def append(self, sym: np.ndarray) -> None:
        if self.cells is None:
            top = np.stack([sym, BOUND[sym]], axis=1).astype(np.int8)
            self.cells = top
            return
        prev = self.cells  # depths -u .. u-1 of column u-1  (u-1 = old index)
        L = prev.shape[1]
        new = np.empty((self.M, L + 2), dtype=np.int8)
        new[:, 0] = sym
        new[:, 1] = BOUND[sym]
        for j in range(L):
            # depth of new[:, j+2] is (-u-1) + j + 2 = -u + 1 + j ; parent left is prev[:, j]
            new[:, j + 2] = CONE_T[prev[:, j], new[:, j + 1]]
        self.cells = new

    def holonomy_to_depth(self, n: int) -> np.ndarray:
        """Index of lam(cells[n-1]) ... lam(cells[top]) : depths -u-1 .. n-1."""
        u = self.cells.shape[1] // 2 - 1
        stop = n - 1 + u + 1  # column index of depth n-1
        g = np.zeros(self.M, dtype=np.int8)
        for j in range(stop + 1):
            g = MUL[LAMI[self.cells[:, j]], g]
        return g


def binary_words(n: int) -> np.ndarray:
    M = 1 << n
    idx = np.arange(M, dtype=np.int64)
    bits = ((idx[:, None] >> np.arange(n)[None, :]) & 1).astype(np.int8)
    return bits + 1  # {1,2}


def main() -> None:
    kmax = 4
    print(" n      dev1   dev1/2^(n/2)  dev1/2^(0.75n)   | k=2 c2 c3 | k=3 c2 c3 | k=4 c2 c3   (dev_k / 2^(n/2))   E0(c=2)")
    for n in range(6, 21):
        t0 = time.time()
        words = binary_words(n)
        cols = Columns(words)
        g = cols.holonomy_to_depth(n)
        hist = np.bincount(g, minlength=8)
        dev1 = int(np.abs(hist - (1 << (n - 3))).max())
        line = f"{n:2d} {dev1:9d} {dev1 / 2 ** (n / 2):12.3f} {dev1 / 2 ** (0.75 * n):14.4f}   |"
        e0 = None
        for k in range(2, kmax + 1):
            line += " "
            for c in (2, 3):
                run = Columns(words)
                vec = np.zeros(cols.M, dtype=np.int64)
                for step in range(k):
                    gg = run.holonomy_to_depth(n)
                    sym = FORCED[gg, c]
                    vec |= E_OF[sym].astype(np.int64) << step
                    run.append(sym)
                    if k == 2 and c == 2 and step == 0:
                        e0 = int((E_OF[sym] == 0).sum())
                h = np.bincount(vec, minlength=1 << k)
                dev = int(np.abs(h - (1 << (n - k))).max())
                line += f" {dev / 2 ** (n / 2):6.2f}"
            line += " |"
        line += f"   {e0}   ({time.time() - t0:.1f}s)"
        print(line, flush=True)


if __name__ == "__main__":
    main()

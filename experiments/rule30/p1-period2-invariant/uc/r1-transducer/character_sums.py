#!/usr/bin/env python3
"""Exact character sums of the forced defect vector over binary W.

v_k(W) = (E(e_n), ..., E(e_{n+k-1})) in Z_2^k along the four-state forced
continuation (e_u the unique symbol with T[u][n] = c).  For a in Z_2^k \\ 0,

    S_k(a) = sum_{W in {1,2}^n} (-1)^{<a, v_k(W)>}.

Reported per (n, c): max_a |S_k(a)| / 2^(n/2) for k = 1..6, the argmax a,
and the deviation of the two (BWH+)-relevant cells, v = 0^k (all forced
symbols binary, c = 2 side) and, for c = 3, also v = 0^k (same meaning: the
forced symbols binary).  A growth of max|S|/2^(n/2) like 2^(theta' n) with
theta' > 0 means the spectral exponent theta = 1/2 + theta' exceeds 1/2.
"""

from __future__ import annotations

import sys
import time

import numpy as np

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-transducer")

from holonomy_equidistribution import Columns, FORCED, E_OF, binary_words  # noqa: E402


def walsh(h: np.ndarray) -> np.ndarray:
    a = h.astype(np.int64).copy()
    n = a.shape[0]
    step = 1
    while step < n:
        for i in range(0, n, 2 * step):
            x = a[i : i + step].copy()
            y = a[i + step : i + 2 * step].copy()
            a[i : i + step] = x + y
            a[i + step : i + 2 * step] = x - y
        step *= 2
    return a


def main(nmin: int, nmax: int, kmax: int) -> None:
    print(" n  c   k: max|S_k|/2^(n/2) [argmax]  ...   zero-cell dev/2^(n/2) for k=1..kmax")
    for n in range(nmin, nmax + 1):
        words = binary_words(n)
        for c in (2, 3):
            t0 = time.time()
            run = Columns(words)
            vec = np.zeros(run.M, dtype=np.int64)
            line = f"{n:2d}  {c}  "
            zero = []
            for k in range(1, kmax + 1):
                gg = run.holonomy_to_depth(n)
                sym = FORCED[gg, c]
                vec |= E_OF[sym].astype(np.int64) << (k - 1)
                run.append(sym)
                h = np.bincount(vec, minlength=1 << k)
                S = walsh(h)
                S[0] = 0
                a = int(np.abs(S).argmax())
                line += f" k{k}:{np.abs(S).max() / 2 ** (n / 2):5.2f}[{a:0{k}b}]"
                zero.append((h[0] - (1 << (n - k))) / 2 ** (n / 2))
            line += "   zero:" + " ".join(f"{z:+.2f}" for z in zero)
            print(line + f"  [{time.time() - t0:.0f}s]", flush=True)


if __name__ == "__main__":
    nmin = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    kmax = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    main(nmin, nmax, kmax)

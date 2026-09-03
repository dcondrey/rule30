#!/usr/bin/env python3
"""Kill tests for the three lemmas of the composite-transducer lens.

  --nerode K       Nerode classes of the K-fold column composite (expect 4^K).
  --tower J        joint phase classes / period of the peel tower with ALL 4^J
                   seeds, memory-lean (one row at a time).  Expect 4 classes,
                   joint period 4, transient tau_J <= 2J.
  --equi N         cell deviation of the forced defect vector at n = N for
                   k = 1..6, both c, as a multiple of 2^(n/2).  Expect <= 3.
"""

from __future__ import annotations

import argparse
import sys
import time

import numpy as np

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-transducer")


def nerode_test(K: int) -> None:
    from composite_nerode import nerode, quotient_letter
    from d8_kernel import cell_of

    t0 = time.time()
    c1, r1 = nerode(K, cell_of)
    print(f"nerode K={K}: classes(cell out)={c1} 4^K={4**K} rounds={r1}  [{time.time() - t0:.0f}s]", flush=True)
    t0 = time.time()
    c2, r2 = nerode(K, quotient_letter)
    print(f"nerode K={K}: classes(quotient out)={c2} 4^K={4**K} rounds={r2}  [{time.time() - t0:.0f}s]", flush=True)


def tower_test(J: int, K: int = 120, tau: int = 64, window: int = 48) -> None:
    from peel_tower_phase import PSI

    M = 4 ** J
    idx = np.arange(M, dtype=np.int64)
    for c in (2, 3):
        t0 = time.time()
        below = np.full((M, K), c, dtype=np.int8)
        joint = np.zeros(M, dtype=np.int64)  # running label of joint tail classes
        for j in range(1, J + 1):
            prev = ((idx // 4 ** (j - 1)) % 4).astype(np.int8)
            row = np.empty((M, K), dtype=np.int8)
            for i in range(K):
                prev = PSI[below[:, i], prev]
                row[:, i] = prev
            # per-row tail classes and transient
            seg = row[:, tau : tau + window]
            packed = np.zeros(M, dtype=np.int64)
            for i in range(window):
                packed = packed * 4 + seg[:, i]
            _, per_row = np.unique(packed, return_inverse=True)
            n_row = per_row.max() + 1
            # transient: first t with the same number of classes as at tau
            trans = None
            for t in range(0, tau + 1):
                seg_t = row[:, t : t + window]
                p_t = np.zeros(M, dtype=np.int64)
                for i in range(window):
                    p_t = p_t * 4 + seg_t[:, i]
                if len(np.unique(p_t)) == n_row:
                    trans = t
                    break
            # joint classes
            joint = joint * n_row + per_row
            _, joint = np.unique(joint, return_inverse=True)
            n_joint = joint.max() + 1
            # period of row (seed 0) beyond tau
            tail = row[0, tau:]
            per = next((p for p in range(1, 33) if np.array_equal(tail[:-p], tail[p:])), -1)
            print(f"tower c={c} J={J} row j={j}: classes={n_row} joint={n_joint} transient={trans} period={per}",
                  flush=True)
            below = row
        print(f"tower c={c} J={J} done [{time.time() - t0:.0f}s]", flush=True)


def equi_test(N: int) -> None:
    from holonomy_equidistribution import Columns, FORCED, E_OF, binary_words

    words = binary_words(N)
    for c in (2, 3):
        t0 = time.time()
        run = Columns(words)
        vec = np.zeros(run.M, dtype=np.int64)
        line = f"equi n={N} c={c}:"
        for k in range(1, 7):
            gg = run.holonomy_to_depth(N)
            sym = FORCED[gg, c]
            vec |= E_OF[sym].astype(np.int64) << (k - 1)
            run.append(sym)
            h = np.bincount(vec, minlength=1 << k)
            dev = int(np.abs(h - (1 << (N - k))).max())
            line += f"  k={k} dev/2^(n/2)={dev / 2 ** (N / 2):.2f}"
        print(line + f"  [{time.time() - t0:.0f}s]", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nerode", type=int, nargs="*", default=[])
    ap.add_argument("--tower", type=int, nargs="*", default=[])
    ap.add_argument("--equi", type=int, nargs="*", default=[])
    a = ap.parse_args()
    for K in a.nerode:
        nerode_test(K)
    for J in a.tower:
        tower_test(J)
    for N in a.equi:
        equi_test(N)


if __name__ == "__main__":
    main()

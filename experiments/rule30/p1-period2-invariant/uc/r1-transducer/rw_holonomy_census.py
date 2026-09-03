#!/usr/bin/env python3
"""Holonomy and residual-state census along the complete RW search tree.

For each (n, c) the search of rw_margin.py is replayed level by level.  At
level k the survivors are the binary W in {1,2}^n whose first k forced symbols
are binary and hard-core (junction included).  Recorded per level:

  N_k        survivors
  E_k        survivors whose NEXT forced symbol is binary (E = 0), before the
             hard-core test; E_k / N_k is the conditional E-hit rate that the
             independence heuristic puts at 1/2
  N_{k+1}    survivors after the hard-core test too
  keys_k     number of distinct residual states.  The cell T[n+k][n] depends on
             e_j only for j >= ceil((k-1)/2) (light cone of the triangle), so
             two survivors with the same (e_{ceil((k-1)/2)}, ..., e_{n+k-1})
             have identical futures.  max_class is the largest such class.
  D8 hist    distribution of the holonomy G_u of the last column (u = n+k-1)
             over survivors, in the order id t T01 T11 s ts sigma T11s.

The light-cone claim is also checked directly: for random four-state endpoint
words the cell T[n+k][n] is recomputed after scrambling e_0..e_{ceil((k-1)/2)-1}.
"""

from __future__ import annotations

import random
import sys
from itertools import product

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-transducer")

from psi_kernel import Endpoint  # noqa: E402
from d8_kernel import (  # noqa: E402
    D8, ID, S, SIGMA, T01, T10, T11, TS, allowed_set, column_cells, holonomy, mul, state,
)

ORDER = [ID, T10, T01, T11, S, TS, SIGMA, mul(T11, S)]


def light_cone_check(trials: int, rng: random.Random) -> int:
    done = 0
    for _ in range(trials):
        n = rng.randint(2, 9)
        k = rng.randint(0, n + 2)
        L = n + k + 1
        e = [rng.randrange(4) for _ in range(L)]
        ep = Endpoint()
        for s in e:
            ep.append(s)
        cell = ep.diagonal[n]
        cut = (k - 1 + 1) // 2 if k >= 1 else 0  # ceil((k-1)/2)
        cut = max(cut, 0)
        f = e[:]
        for j in range(cut):
            f[j] = rng.randrange(4)
        ep2 = Endpoint()
        for s in f:
            ep2.append(s)
        assert ep2.diagonal[n] == cell, (n, k, e, f)
        done += 1
    return done


def census(n: int, c: int) -> None:
    allowed = set(allowed_set(c))
    level = []  # list of (Endpoint, word list)
    for W in product((1, 2), repeat=n):
        ep = Endpoint()
        for s in W:
            ep.append(s)
        level.append((ep, list(W)))
    k = 0
    need = n + 2
    print(f"\nn={n} c={c}")
    print("  k     N_k    E_k  E_k/N_k   N_k+1   keys  maxcls   D8 hist (id t T01 T11 s ts sig T11s)")
    while level and k < need:
        hist = {g: 0 for g in D8}
        keys = {}
        nxt = []
        e_hits = 0
        for ep, word in level:
            u = ep.length - 1
            cells = column_cells(ep)
            window = cells[: n + u + 1]
            g = holonomy(window)
            hist[g] += 1
            cut = max((k - 1 + 1) // 2, 0)
            key = tuple(word[cut:])
            keys[key] = keys.get(key, 0) + 1
            hit = g in allowed
            if hit:
                e_hits += 1
                forced = [s for s in (1, 2) if ep.peek(s)[1][n] == c]
                assert len(forced) == 1
                s = forced[0]
                if word[-1] == 1 and s == 1:
                    continue
                col, diag = ep.peek(s)
                nep = Endpoint()
                nep.column = col + [s]
                nep.diagonal = diag
                nep.length = ep.length + 1
                nxt.append((nep, word + [s]))
        N = len(level)
        print(
            f"{k:3d} {N:7d} {e_hits:6d} {e_hits / N:8.4f} {len(nxt):7d} {len(keys):6d} {max(keys.values()):6d}   "
            + " ".join(f"{hist[g]:5d}" for g in ORDER)
        )
        level = nxt
        k += 1


def main() -> None:
    rng = random.Random(30)
    print(f"light cone: {light_cone_check(3000, rng)} random four-state endpoints PASS")
    for n in range(4, 14):
        for c in (2, 3):
            census(n, c)


if __name__ == "__main__":
    main()

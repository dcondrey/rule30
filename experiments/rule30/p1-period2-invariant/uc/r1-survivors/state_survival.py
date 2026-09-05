#!/usr/bin/env python3
"""State-level survival census for RW (kill test of the state-coin bound).

Level-0 state of a binary source W in {1,2}^n: the three-letter quotient of
column n-1 on depths [-n, n-1] (BRIEF section 2: it determines the forced
orbit).  Every source in a class has the same forced orbit, so the RW run
depth is a class property.  For each n and c this prints
   S_0            = number of level-0 states,
   S'_k           = number of level-0 states whose RW orbit (forced H, hit
                    E(T[u][n]) = E(c), hard-core including the junction) reaches
                    depth >= k,
   ratio_k        = S'_k * 2^k / S_0,
and the maximum ratio over k with S'_k >= 1.  The bound under test is
S'_k <= C * S_0 * 2^-k with C = 4 (and the slack version C = 8).
Also prints log2 S_0 against the fit 0.8212 u + 1.31 (u = n-1) from
quotient_bfs_u27.log, and the deepest k against 0.83 n + 3.3.
"""
from __future__ import annotations

import sys
import time
from itertools import product
from math import log2

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
from psi_kernel import Endpoint  # noqa: E402

LET = bytes([2, 0, 1, 0])


def run_depth(state: Endpoint, prev: int, n: int, c: int, need: int) -> int:
    depth = 0
    while depth < need:
        chosen = None
        for s in (1, 2):
            col, dia = state.peek(s)
            if dia[n] >> 1 == 1:
                chosen = (s, col, dia)
        if chosen is None:
            return depth
        s, col, dia = chosen
        if prev == 1 and s == 1:
            return depth
        if dia[n] != c:
            return depth
        nxt = Endpoint()
        nxt.column, nxt.diagonal, nxt.length = col + [s], dia, state.length + 1
        state, prev = nxt, s
        depth += 1
    return depth


def main() -> None:
    nmin = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 18
    Cs = (4, 8)
    worst = {C: (0.0, None) for C in Cs}
    for n in range(nmin, nmax + 1):
        t0 = time.time()
        reps: dict[bytes, tuple[Endpoint, int, int]] = {}
        for W in product((1, 2), repeat=n):
            st = Endpoint()
            for e in W:
                st.append(e)
            # quotient of column n-1 on depths [-n, n-1]: column[i] = T[n-1][-i], i=0..n ; diagonal[k]=T[n-1][k], k=0..n-1
            key = bytes(LET[x] for x in st.column[1:][::-1]) + bytes(LET[x] for x in st.diagonal)
            if key not in reps:
                reps[key] = (st, W[-1], 1)
            else:
                a, b, cnt = reps[key]
                reps[key] = (a, b, cnt + 1)
        S0 = len(reps)
        for c in (2, 3):
            need = n + 2
            depths = []
            for st, prev, cnt in reps.values():
                depths.append((run_depth(st.clone(), prev, n, c, need), cnt))
            deepest = max(d for d, _ in depths)
            line = []
            maxratio = 0.0
            argk = None
            for k in range(1, deepest + 1):
                Sk = sum(1 for d, _ in depths if d >= k)
                Nk = sum(cnt for d, cnt in depths if d >= k)
                r = Sk * 2 ** k / S0
                if r > maxratio:
                    maxratio, argk = r, k
                line.append(f"k{k}:{Nk}/{Sk}/{r:.2f}")
            for C in Cs:
                if maxratio > worst[C][0]:
                    worst[C] = (maxratio, (n, c, argk))
            print(f"n={n:2d} c={c}: S_0={S0} (log2 {log2(S0):.2f}, fit {0.8212*(n-1)+1.31:.2f})  deepest={deepest} (0.83n+3.3={0.83*n+3.3:.1f}, need={need})  max S'_k 2^k/S_0 = {maxratio:.2f} at k={argk}  [{time.time()-t0:.0f}s]")
            print("      N_k/S'_k/ratio: " + " ".join(line))
    for C in Cs:
        print(f"bound S'_k <= {C} S_0 2^-k: max ratio {worst[C][0]:.2f} at (n,c,k)={worst[C][1]} -> {'HELD' if worst[C][0] <= C else 'VIOLATED'}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Is the hit language anchored?  Late hit runs along a fixed forced orbit.

For a fixed depth n and source W, the forced continuation (e_u in {1,2}
with H(T[u][n]) = 1) is an infinite deterministic orbit.  RW only looks at
the INITIAL run of hits T[u][n] = c starting at u = n.  A shift-invariant
(subshift) formulation would also count runs starting at later columns
u_0 > n.  This script follows each orbit for M columns and records the
longest hit run anywhere (E-only) and the longest hit run whose forced
symbols are hard-core (joint), together with the initial run.  If late runs
longer than n+2 appear routinely, then any "no long run anywhere along any
orbit" statement is false and the entropy object must be anchored at the
apex (column n), which is not a shift-invariant object.

Run:  cd <kernel dir> && uv run python uc/r1-entropy/late_runs.py --n 5 6 7 --steps 1500
"""

from __future__ import annotations

import argparse
import os
import sys
from itertools import product

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from psi_kernel import Endpoint  # noqa: E402


def orbit_runs(source, target, steps):
    n = len(source)
    st = Endpoint()
    for s in source:
        st.append(s)
    prev = source[-1]
    initial = None
    bestE = (0, -1)
    bestJ = (0, -1)
    curE = 0
    curJ = 0
    startE = startJ = n
    for i in range(steps):
        u = n + i
        for sym in (1, 2):
            _, diag = st.peek(sym)
            if diag[n] >> 1 == 1:
                break
        st.append(sym)
        hit = diag[n] == target
        legal = not (prev == 1 and sym == 1)
        prev = sym
        if hit:
            if curE == 0:
                startE = u
            curE += 1
            if curE > bestE[0]:
                bestE = (curE, startE)
        else:
            if initial is None:
                initial = curE if startE == n else 0
            curE = 0
        if hit and legal:
            if curJ == 0:
                startJ = u
            curJ += 1
            if curJ > bestJ[0]:
                bestJ = (curJ, startJ)
        else:
            curJ = 0
    if initial is None:
        initial = curE if startE == n else 0
    return initial, bestE, bestJ


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, nargs="+", default=[5, 6, 7])
    ap.add_argument("--steps", type=int, default=1500)
    ap.add_argument("--max-sources", type=int, default=64)
    ap.add_argument("--log", type=str, default="uc/r1-entropy/late_runs.log")
    args = ap.parse_args()
    with open(args.log, "w") as log:
        for n in args.n:
            for c in (2, 3):
                need = n + 2
                worstE = (0, -1, None)
                worstJ = (0, -1, None)
                n_lateE = 0
                n_lateJ = 0
                count = 0
                for W in product((1, 2), repeat=n):
                    if count >= args.max_sources:
                        break
                    count += 1
                    initial, bestE, bestJ = orbit_runs(W, c, args.steps)
                    if bestE[0] >= need and bestE[1] > n:
                        n_lateE += 1
                    if bestJ[0] >= need and bestJ[1] > n:
                        n_lateJ += 1
                    if bestE[0] > worstE[0]:
                        worstE = (bestE[0], bestE[1], W)
                    if bestJ[0] > worstJ[0]:
                        worstJ = (bestJ[0], bestJ[1], W)
                print(f"n={n} c={c} steps={args.steps} sources={count} need={need}: "
                      f"sources with a LATE E-run >= need: {n_lateE}; with a LATE joint (HC) run >= need: {n_lateJ}; "
                      f"longest E-run {worstE[0]} at column {worstE[1]} (W={''.join(map(str, worstE[2]))}); "
                      f"longest joint run {worstJ[0]} at column {worstJ[1]} (W={''.join(map(str, worstJ[2]))})", file=log)
                log.flush()
    with open(args.log) as f:
        sys.stdout.write(f.read())


if __name__ == "__main__":
    main()

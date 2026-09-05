#!/usr/bin/env python3
"""Fill the exact gaps left by rw_sat_r_grid_20260903.log: that run stopped

after (n=29, r=2, c=2) took 12747s, exceeding its 3600s informational
budget, before reaching (29, r=2, c=3) or any of n=30. No timeout is
enforced here -- these instances are run to their real answer, however
long that takes, since a timeout is not an UNSAT result.

Targets, in ascending expected-cost order:
  (29, 2, 3)
  (30, 1, 2), (30, 1, 3), (30, 2, 2), (30, 2, 3)
"""
from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rw_sat import encode  # noqa: E402
from pysat.solvers import Cadical153  # noqa: E402

TARGETS = [
    (29, 2, 3),
    (30, 1, 2),
    (30, 1, 3),
    (30, 2, 2),
    (30, 2, 3),
]


def main() -> None:
    print(" n  r  c   vars    clauses   result   seconds")
    sys.stdout.flush()
    for n, r, c in TARGETS:
        cnf, s, _ = encode(n, r, c)
        t0 = time.time()
        with Cadical153(bootstrap_with=cnf.clauses) as slv:
            ok = slv.solve()
            dt = time.time() - t0
            model = slv.get_model() if ok else None
        res = "SAT  <- RW COUNTEREXAMPLE" if ok else "UNSAT"
        word = "".join("2" if model[v - 1] > 0 else "1" for v in s) if ok else ""
        print(f"{n:<3}{r:<3}{c:<4}{cnf.nv:<8}{len(cnf.clauses):<10}{res:<8} {dt:8.2f}  {word}")
        sys.stdout.flush()


if __name__ == "__main__":
    main()

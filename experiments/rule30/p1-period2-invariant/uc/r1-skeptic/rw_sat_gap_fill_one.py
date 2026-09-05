#!/usr/bin/env python3
"""Solve exactly one (n, r, c) RW SAT instance, no timeout, for parallel

dispatch across the five gap-fill targets (see rw_sat_gap_fill.py's
docstring for why these five: n=29 r=2 c=3, and all of n=30, were never
attempted by rw_sat_r_grid_20260903.log).
"""
from __future__ import annotations

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rw_sat import encode  # noqa: E402
from pysat.solvers import Cadical153  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("n", type=int)
    ap.add_argument("r", type=int)
    ap.add_argument("c", type=int)
    args = ap.parse_args()

    cnf, s, _ = encode(args.n, args.r, args.c)
    t0 = time.time()
    with Cadical153(bootstrap_with=cnf.clauses) as slv:
        ok = slv.solve()
        dt = time.time() - t0
        model = slv.get_model() if ok else None
    res = "SAT  <- RW COUNTEREXAMPLE" if ok else "UNSAT"
    word = "".join("2" if model[v - 1] > 0 else "1" for v in s) if ok else ""
    print(f"{args.n:<3}{args.r:<3}{args.c:<4}{cnf.nv:<8}{len(cnf.clauses):<10}"
          f"{res:<8} {dt:8.2f}  {word}")
    sys.stdout.flush()


if __name__ == "__main__":
    main()

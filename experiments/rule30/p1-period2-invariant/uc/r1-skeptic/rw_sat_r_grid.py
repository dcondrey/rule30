#!/usr/bin/env python3
"""RW SAT scan over r in {1, 2}, reusing rw_sat.encode/solve unmodified.

Requested explicitly (not a proposed/unprompted extension): the r=1,2 grid
that PATH.md's r=0 scan never covered. Same instance family as rw_sat.py's
scan(), just varying r instead of hardcoding r=0.

Run: cd experiments/rule30/p1-period2-invariant && \
  uv run --with python-sat python uc/r1-skeptic/rw_sat_r_grid.py --min-n 8 --max-n 20 --rs 1 2
"""
from __future__ import annotations

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rw_sat import encode  # noqa: E402
from pysat.solvers import Cadical153  # noqa: E402


def scan(min_n: int, max_n: int, rs: list[int], timeout: float) -> None:
    print(" n  r  c   vars    clauses   result   seconds")
    sys.stdout.flush()
    for n in range(min_n, max_n + 1):
        for r in rs:
            for c in (2, 3):
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
                if dt > timeout:
                    print(f"stopping: {dt:.1f}s exceeds the per-instance budget {timeout}s")
                    return


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-n", type=int, default=8)
    ap.add_argument("--max-n", type=int, default=20)
    ap.add_argument("--rs", type=int, nargs="+", default=[1, 2])
    ap.add_argument("--timeout", type=float, default=3600.0)
    args = ap.parse_args()
    scan(args.min_n, args.max_n, args.rs, args.timeout)


if __name__ == "__main__":
    main()

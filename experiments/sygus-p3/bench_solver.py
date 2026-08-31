"""Cadical vs Z3 on identical CNF, and the (m, k) feasibility curve.

The instance is pure CNF with no theory content, so a raw SAT solver should
beat an SMT solver that has to bit-blast and preprocess it.  This measures
that rather than assuming it.
"""

import sys
import time

from pysat.formula import IDPool
from pysat.solvers import Cadical195

from rule30 import truth_table
from synth import encode


def bench_pair(tt, m, k):
    pool = IDPool()
    cnf = encode(tt, m, k, pool)
    nv, nc = pool.top, len(cnf)

    t0 = time.time()
    with Cadical195(bootstrap_with=cnf) as s:
        sat_c = s.solve()
    t_cad = time.time() - t0

    import z3
    t0 = time.time()
    zs = z3.Solver()
    v = {i: z3.Bool(f"v{i}") for i in range(1, nv + 1)}
    for cl in cnf:
        zs.add(z3.Or([v[abs(x)] if x > 0 else z3.Not(v[abs(x)]) for x in cl]))
    sat_z = zs.check() == z3.sat
    t_z3 = time.time() - t0

    assert sat_c == sat_z, "solvers disagree"
    return nv, nc, sat_c, t_cad, t_z3


def main():
    print("solver comparison, Rule 30 centre column, m=4, identical CNF")
    print(f"{'k':>3} {'vars':>7} {'clauses':>8} {'res':>5} {'cadical':>9} {'z3':>9}")
    tt = truth_table(30, 4)
    for k in range(4, 8):
        nv, nc, sat, tc, tz = bench_pair(tt, 4, k)
        print(f"{k:3d} {nv:7d} {nc:8d} {'SAT' if sat else 'UNSAT':>5} "
              f"{tc:8.3f}s {tz:8.3f}s")


if __name__ == "__main__":
    main()

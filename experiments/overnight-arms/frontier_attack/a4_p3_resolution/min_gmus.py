"""R9/A4: SMALLEST (not merely deletion-minimal) sufficient cell set.

Why this exists.  The only sound bridge from the stored GMUS probe to a
derivation-length bound is:

  Let S be the axiom set used by a resolution refutation of F_n /\ ~c_n, and
  G(S) the set of cells S touches.  Enforcing the rule on all of G(S) implies
  every clause of S, so F_n restricted to G(S) is already unsatisfiable with
  ~c_n, i.e. G(S) is a SUFFICIENT cell set.  Hence |S| >= |G(S)| >= mu(n),
  where mu(n) is the size of the SMALLEST sufficient cell set.  A refutation
  DAG with L distinct leaves has >= L-1 binary internal nodes, so

      refutation length >= mu(n) - 1,   derivation length >= mu(n) - 2.

The stored probe (RESULTS-proof-complexity-probe.md) measured a DELETION-
MINIMAL sufficient set, which upper-bounds nothing and lower-bounds nothing:
minimal != minimum.  mu(n) is the quantity the bound actually needs.  This
script computes mu(n) exactly at small n by the implicit-hitting-set SMUS
algorithm (Ignatiev, Previti, Janota, Marques-Silva, CP 2015) and compares it
to the stored deletion-minimal numbers.

Ground set: cells (t,x) of D_n with t >= 1.  Encoding identical to
experiments/rule30/proof-complexity/mus_probe.py.

Run:
    uv run python min_gmus.py --rule 30 --ns 4 6 8 10 --out smus30.json
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time

from pysat.examples.rc2 import RC2
from pysat.formula import WCNF
from pysat.solvers import Solver

from derivation_upper_bound import RULES, diamond, simulate


def build(rule: int, n: int):
    """Selector-per-cell encoding.  Returns (clauses, cells, sel, var, truth)."""
    reads, f = RULES[rule]
    truth = simulate(rule, n)
    cone = diamond(n)
    var = {c: i + 1 for i, c in enumerate(cone)}
    cells = [c for c in cone if c[0] >= 1]
    sel = {c: len(cone) + 1 + i for i, c in enumerate(cells)}
    clauses = [[var[(0, 0)]]]
    for (t, x) in cells:
        parents = [(t - 1, x - 1), (t - 1, x), (t - 1, x + 1)]
        pv = [var.get(p) for p in parents]
        idx = [i for i in reads if pv[i] is not None]
        for m in range(1 << len(idx)):
            asn = [0, 0, 0]
            for j, i in enumerate(idx):
                asn[i] = (m >> j) & 1
            out = f(*asn)
            lits = [-pv[i] if asn[i] else pv[i] for i in idx]
            lits.append(var[(t, x)] if out else -var[(t, x)])
            clauses.append(lits + [-sel[(t, x)]])
    # wrong-value unit, hard: the instance under study is the refutation one
    wrong = 1 - truth[(n, 0)]
    clauses.append([var[(n, 0)]] if wrong else [-var[(n, 0)]])
    return clauses, cells, sel, var, truth


def cell_satisfied(model: dict, rule: int, cell, var, ) -> bool:
    reads, f = RULES[rule]
    t, x = cell
    parents = [(t - 1, x - 1), (t - 1, x), (t - 1, x + 1)]
    asn = [0, 0, 0]
    for i in reads:
        p = parents[i]
        asn[i] = model[var[p]] if p in var else 0
    return f(*asn) == model[var[cell]]


def smus(rule: int, n: int, budget_s: float):
    clauses, cells, sel, var, truth = build(rule, n)
    solver = Solver(name="cd15", bootstrap_with=clauses)
    # sanity: full cell set must be UNSAT, empty set must be SAT
    assert not solver.solve(assumptions=[sel[c] for c in cells]), "full set must be UNSAT"
    assert solver.solve(assumptions=[-sel[c] for c in cells]), "empty set must be SAT"

    correction_sets = []  # lists of cells
    t0 = time.time()
    it = 0
    while True:
        it += 1
        if time.time() - t0 > budget_s:
            solver.delete()
            return None, it, time.time() - t0, len(correction_sets)
        # minimum hitting set of correction_sets
        w = WCNF()
        for K in correction_sets:
            w.append([sel[c] for c in K])
        for c in cells:
            w.append([-sel[c]], weight=1)
        with RC2(w) as rc2:
            m = rc2.compute()
        hs = set()
        if m is not None:
            pos = {lit for lit in m if lit > 0}
            hs = {c for c in cells if sel[c] in pos}
        assumptions = [sel[c] if c in hs else -sel[c] for c in cells]
        if not solver.solve(assumptions=assumptions):
            solver.delete()
            return sorted(hs), it, time.time() - t0, len(correction_sets)
        # SAT: grow to a satisfiable superset using the model, then add the
        # complement as a correction set
        mdl = solver.get_model()
        model = {abs(lit): (1 if lit > 0 else 0) for lit in mdl}
        sat_cells = {c for c in cells if cell_satisfied(model, rule, c, var)}
        assert hs <= sat_cells
        K = [c for c in cells if c not in sat_cells]
        assert K, "satisfiable full set contradicts the UNSAT check"
        correction_sets.append(K)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule", type=int, default=30)
    ap.add_argument("--ns", type=int, nargs="+", default=[4, 6, 8, 10])
    ap.add_argument("--budget", type=float, default=900.0)
    ap.add_argument("--out", default="smus.json")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)

    rows = []
    for n in a.ns:
        cone = diamond(n)
        ground = len([c for c in cone if c[0] >= 1])
        res, it, secs, ncs = smus(a.rule, n, a.budget)
        row = {
            "rule": a.rule,
            "n": n,
            "diamond_cells": len(cone),
            "ground_cells": ground,
            "mu": None if res is None else len(res),
            "iterations": it,
            "correction_sets": ncs,
            "seconds": round(secs, 1),
            "smus_cells": res,
        }
        rows.append(row)
        logging.info(
            "rule %d n=%-3d ground=%-5d mu=%-6s iters=%-5d %.1fs",
            a.rule, n, ground, row["mu"], it, secs,
        )
        with open(a.out, "w") as f:
            json.dump(rows, f, indent=1)
    logging.info("wrote %s", a.out)


if __name__ == "__main__":
    main()

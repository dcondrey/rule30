"""R9/A4: EXACT, machine-checked resolution derivation of the centre unit c_n
from the light-cone CNF, for rules 30 and 90.

Purpose in the arm: this is the UPPER bound that caps route R9.  PATH.md R9
asserts "row simulation gives O(n^2)-size resolution derivations of the centre
value" without a checked construction.  This script produces the derivation,
verifies EVERY resolution step mechanically, and reports the exact step count
as a function of n, together with the exact formula size.  It also emits the
refutation of F_n AND (wrong-value unit), establishing the derivation <->
refutation equivalence at an explicit additive cost of 1 step.

Encoding matches experiments/rule30/proof-complexity/mus_probe.py exactly
(read-only reference, not imported): one variable per cell of
D_n = {(t,x) : |x| <= min(t, n-t)} (backward diamond of (n,0) intersected with
the forward light cone of the lone seed); for each cell with t >= 1 the full
truth-table clause set over its in-diamond parents (out-of-diamond parents are
constant 0, which is exact because they lie outside the forward light cone);
one unit clause fixing the seed s(0,0)=1.

Ground truth for rule 30 is cross-checked against
experiments/overnight-arms/common/rule30.py (read-only import).

Run:
    uv run python derivation_upper_bound.py --out upper_bound.json
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import logging
import sys

REPO = "/Volumes/A/researchpapers/13-rule30"

# name: (parent indices actually read, f(a,b,c)) with a=left, b=centre, c=right
RULES = {
    30: ((0, 1, 2), lambda a, b, c: a ^ (b | c)),
    90: ((0, 2), lambda a, b, c: a ^ c),
}


def simulate(rule: int, n: int) -> dict[tuple[int, int], int]:
    _, f = RULES[rule]
    cells = {(0, 0): 1}
    row = {0: 1}
    for t in range(1, n + 1):
        new = {}
        for x in range(-t, t + 1):
            v = f(row.get(x - 1, 0), row.get(x, 0), row.get(x + 1, 0))
            new[x] = v
            cells[(t, x)] = v
        row = new
    return cells


def diamond(n: int) -> list[tuple[int, int]]:
    return [
        (t, x)
        for t in range(n + 1)
        for x in range(-min(t, n - t), min(t, n - t) + 1)
    ]


def build_cnf(rule: int, n: int):
    """Return (axioms, var, truth).  axioms is a list of frozenset[int]."""
    reads, f = RULES[rule]
    truth = simulate(rule, n)
    cone = diamond(n)
    var = {c: i + 1 for i, c in enumerate(cone)}
    axioms = [frozenset({var[(0, 0)]})]
    for (t, x) in cone:
        if t == 0:
            continue
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
            axioms.append(frozenset(lits))
    return axioms, var, truth


def resolvent(c1: frozenset, c2: frozenset, v: int) -> frozenset:
    assert v in c1 and -v in c2, "pivot orientation"
    return frozenset((c1 - {v}) | (c2 - {-v}))


def derive(rule: int, n: int):
    """Build the unit-propagation resolution derivation of the centre unit.

    Returns (axioms, steps, clauses, target).  steps is a list of
    (i, j, pivot) index pairs into `clauses`; clauses[k] is the k-th clause,
    axioms first then derived ones.
    """
    reads, f = RULES[rule]
    axioms, var, truth = build_cnf(rule, n)
    axiom_index = {}
    for i, c in enumerate(axioms):
        axiom_index.setdefault(c, i)

    clauses = list(axioms)
    steps = []  # (i, j, pivot)
    unit_of = {}  # cell -> index in `clauses` of its derived/axiom unit clause

    unit_of[(0, 0)] = 0  # the seed axiom
    for (t, x) in diamond(n):
        if t == 0:
            continue
        parents = [(t - 1, x - 1), (t - 1, x), (t - 1, x + 1)]
        pv = [var.get(p) for p in parents]
        idx = [i for i in reads if pv[i] is not None]
        asn = [0, 0, 0]
        for i in idx:
            asn[i] = truth[parents[i]]
        out = f(*asn)
        lits = [-pv[i] if asn[i] else pv[i] for i in idx]
        lits.append(var[(t, x)] if out else -var[(t, x)])
        cur = axiom_index[frozenset(lits)]
        # resolve away each in-diamond parent literal against that parent's unit
        for i in idx:
            p = parents[i]
            pu = unit_of[p]
            plit = var[p] if truth[p] else -var[p]  # literal true in the model
            # clauses[pu] == {plit}; clauses[cur] contains -plit
            r = resolvent(clauses[pu], clauses[cur], plit)
            steps.append((pu, cur, plit))
            clauses.append(r)
            cur = len(clauses) - 1
        unit_of[(t, x)] = cur
    target_lit = var[(n, 0)] if truth[(n, 0)] else -var[(n, 0)]
    return axioms, steps, clauses, unit_of[(n, 0)], target_lit, var, truth


def check(axioms, steps, clauses, final_idx, target_lit) -> None:
    """Mechanically verify every resolution step and the final clause."""
    na = len(axioms)
    for k, (i, j, piv) in enumerate(steps):
        out = na + k
        assert i < out and j < out, f"step {k} uses a clause not yet derived"
        c1, c2 = clauses[i], clauses[j]
        assert piv in c1, f"step {k}: pivot not positive in first premise"
        assert -piv in c2, f"step {k}: pivot not negative in second premise"
        assert clauses[out] == resolvent(c1, c2, piv), f"step {k}: bad resolvent"
    assert clauses[final_idx] == frozenset({target_lit}), "final clause is not the target unit"


def rule30_ground_truth(n: int) -> list[int]:
    spec = importlib.util.spec_from_file_location(
        "arm_rule30", f"{REPO}/experiments/overnight-arms/common/rule30.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.center_column_bits(n + 1)


def run(rule: int, ns: list[int]) -> list[dict]:
    rows = []
    gt = rule30_ground_truth(max(ns)) if rule == 30 else None
    for n in ns:
        axioms, steps, clauses, fin, tlit, var, truth = derive(rule, n)
        check(axioms, steps, clauses, fin, tlit)
        if gt is not None:
            assert truth[(n, 0)] == gt[n], f"n={n}: centre disagrees with common/rule30.py"
        # refutation: one more step against the wrong-value unit
        wrong_unit = frozenset({-tlit})
        empty = resolvent(clauses[fin], wrong_unit, tlit)
        assert empty == frozenset(), "refutation step did not yield the empty clause"
        # Closed forms, asserted so that every number quoted in prose is
        # machine-checked, not eyeballed off the table.
        nv_expect = n * n // 2 + n + 1
        assert len(var) == nv_expect, f"variable count: {len(var)} != {nv_expect}"
        if rule == 30:
            st_expect = (3 * n * n) // 2
            ax_expect = 4 * n * n - 2 * n + 3 - 2 * (n % 2)
        else:
            st_expect = 2 * (n * n // 2)
            ax_expect = 4 * (n * n // 2) + 2
        assert len(steps) == st_expect, f"steps: {len(steps)} != {st_expect}"
        assert len(axioms) == ax_expect, f"axioms: {len(axioms)} != {ax_expect}"
        rows.append(
            {
                "rule": rule,
                "n": n,
                "diamond_cells": len(var),
                "axiom_clauses": len(axioms),
                "derivation_steps": len(steps),
                "refutation_steps": len(steps) + 1,
                "centre_value": truth[(n, 0)],
                "steps_over_n2": len(steps) / (n * n),
                "steps_over_axioms": len(steps) / len(axioms),
            }
        )
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ns", type=int, nargs="+",
                    default=[4, 8, 16, 32, 64, 96, 128])
    ap.add_argument("--out", default="upper_bound.json")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)

    out = {"rules": {}}
    for rule in (30, 90):
        rows = run(rule, a.ns)
        out["rules"][str(rule)] = rows
        logging.info("rule %d  (every resolution step machine-checked)", rule)
        logging.info(
            "%6s %10s %10s %10s %10s %10s",
            "n", "cells", "axioms", "steps", "steps/n^2", "steps/|F|",
        )
        for r in rows:
            logging.info(
                "%6d %10d %10d %10d %10.4f %10.4f",
                r["n"], r["diamond_cells"], r["axiom_clauses"],
                r["derivation_steps"], r["steps_over_n2"], r["steps_over_axioms"],
            )
        logging.info("")
    with open(a.out, "w") as f:
        json.dump(out, f, indent=1)
    logging.info("wrote %s", a.out)


if __name__ == "__main__":
    main()

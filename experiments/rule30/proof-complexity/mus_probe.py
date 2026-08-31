"""R9 probe: how does the minimal sufficient constraint set for deriving the
centre cell scale with n?

Encodes the lone-seed light cone of an ECA as CNF (one variable per cell in
the backward diamond of (n,0), truth-table clauses per cell, seed unit, and a
unit asserting the WRONG centre value at row n), verifies UNSAT, then measures
two core notions:

  clause-level MUS  -- one selector per clause.  Expected to be degenerate
                       (see RESULTS doc): the firing clauses alone form a MUS
                       of size ~ the whole diamond for ANY rule.
  cell-level GMUS   -- one selector per cell (all its clauses share it).  A
                       set of cells G is UNSAT iff enforcing the local rule
                       exactly on G pins the centre value.  The deletion-
                       minimal G is the structural quantity.  For rule 90,
                       linearity makes the GMUS unique and equal to the set of
                       diamond cells with an odd path count into (n,0)
                       (binomial parity); the pipeline must reproduce that.

Cells outside the backward diamond of (n,0) cannot belong to any MUS (their
clauses are never necessary: the diamond alone still derives the centre), so
the encoding restricts to the diamond; this is exact, not an approximation.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

from pysat.solvers import Solver

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from center_column import center_column  # noqa: E402

RULES = {
    # name: (reads, f(a, b, c)) with a = left parent, b = centre, c = right.
    30: ((0, 1, 2), lambda a, b, c: a ^ (b | c)),
    90: ((0, 2), lambda a, b, c: a ^ c),
}


def simulate(rule: int, n: int) -> dict[tuple[int, int], int]:
    """Independent dense simulation of the lone seed, cross-checked for rule 30
    against the repo's bit-parallel generator."""
    _, f = RULES[rule]
    cells = {(0, 0): 1}
    row = {0: 1}
    for t in range(1, n + 1):
        new = {}
        for x in range(-t, t + 1):
            v = f(row.get(x - 1, 0), row.get(x, 0), row.get(x + 1, 0))
            if v or abs(x) <= t:
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


def build(rule: int, n: int, group: str):
    """Build clauses with selector literals.  Returns (solver-ready hard
    clauses, {selector: payload}, var of centre cell, truth dict)."""
    reads, f = RULES[rule]
    truth = simulate(rule, n)
    cone = diamond(n)
    var = {cell: i + 1 for i, cell in enumerate(cone)}
    nvar = len(cone)
    clauses = []  # (selector_key, clause_without_selector)
    for (t, x) in cone:
        if t == 0:
            continue
        parents = [(t - 1, x - 1), (t - 1, x), (t - 1, x + 1)]
        pv = [var.get(p) for p in parents]  # None => constant 0 outside cone
        idx = [i for i in reads if pv[i] is not None]
        consts = [0, 0, 0]
        for m in range(1 << len(idx)):
            asn = list(consts)
            for j, i in enumerate(idx):
                asn[i] = (m >> j) & 1
            out = f(*asn)
            lits = [-pv[i] if asn[i] else pv[i] for i in idx]
            lits.append(var[(t, x)] if out else -var[(t, x)])
            key = (t, x) if group == "cell" else (t, x, m)
            clauses.append((key, lits))
    sel = {}
    out_clauses = [[var[(0, 0)]]]
    next_sel = nvar + 1
    key_to_sel = {}
    for key, lits in clauses:
        if key not in key_to_sel:
            key_to_sel[key] = next_sel
            sel[next_sel] = key
            next_sel += 1
        out_clauses.append(lits + [-key_to_sel[key]])
    # Wrong-value unit rides its own selector so the encoding can be
    # validated (rule clauses alone must reproduce the simulated diagram)
    # before the refutation instance is formed by assuming wsel.
    wsel = next_sel
    wrong = 1 - truth[(n, 0)]
    out_clauses.append(([var[(n, 0)]] if wrong else [-var[(n, 0)]]) + [-wsel])
    return out_clauses, sel, wsel, var, truth


def deletion_mus(solver, selectors: list[int], wsel: int, rng: random.Random):
    """Deletion-based MUS over selector assumptions with core refinement.
    Elements proven necessary stay necessary under shrinking supersets.
    The wrong-value selector wsel is always assumed (hard in spirit)."""
    order = selectors[:]
    rng.shuffle(order)
    core = order
    assert not solver.solve(assumptions=core + [wsel]), "candidate not UNSAT"
    got = solver.get_core()
    if got is not None:
        keep = set(got)
        core = [s for s in core if s in keep]
    i = 0
    calls = 0
    while i < len(core):
        test = core[:i] + core[i + 1 :]
        calls += 1
        if solver.solve(assumptions=test + [wsel]):
            i += 1
        else:
            got = set(solver.get_core() or test)
            core = core[:i] + [s for s in core[i:] if s != core[i] and s in got]
    return core, calls


def rule90_odd_set(n: int) -> set[tuple[int, int]]:
    """Cells of the diamond with odd path count into (n,0) under rule 90.
    Coefficient of cell (t,x) is C(n-t, (n-t+x)/2) mod 2 when parity admits."""
    out = set()
    for (t, x) in diamond(n):
        d = n - t
        if (d + x) % 2:
            continue
        k = (d + x) // 2
        if (d - k) & k == 0:  # Kummer: C(d,k) odd iff k AND (d-k) == 0
            out.add((t, x))
    return out


def run_one(rule: int, n: int, group: str, seeds: int, timeout_s: float):
    t0 = time.time()
    clauses, sel, wsel, var, truth = build(rule, n, group)
    with Solver(name="cd15", bootstrap_with=clauses) as s:
        all_sel = list(sel)
        # Encoding self-check 1: rule clauses alone are SAT and reproduce the
        # simulated diagram exactly (seed unit + propagation, no search room).
        assert s.solve(assumptions=all_sel), "rule clauses must be SAT"
        model = set(s.get_model())
        for cell, v in var.items():
            want = v if truth[cell] else -v
            assert want in model, f"encoding deviates from simulation at {cell}"
        # Encoding self-check 2: adding the wrong-value unit refutes.
        assert not s.solve(assumptions=all_sel + [wsel]), "must be UNSAT"
        core0 = [c for c in (s.get_core() or all_sel) if c != wsel]
        trimmed = core0
        while True:
            assert not s.solve(assumptions=trimmed + [wsel])
            nxt = [c for c in (s.get_core() or trimmed) if c != wsel]
            if len(nxt) >= len(trimmed):
                break
            trimmed = nxt
        results = []
        for seed in range(seeds):
            if time.time() - t0 > timeout_s:
                break
            mus, calls = deletion_mus(s, list(trimmed), wsel, random.Random(seed))
            cells = {sel[m] if group == "cell" else sel[m][:2] for m in mus}
            results.append(
                {
                    "seed": seed,
                    "mus_selectors": len(mus),
                    "mus_cells": len(cells),
                    "calls": calls,
                    "cells": sorted(cells),
                }
            )
    return {
        "rule": rule,
        "n": n,
        "group": group,
        "diamond_cells": len(var),
        "trimmed_core": len(trimmed),
        "seconds": round(time.time() - t0, 2),
        "runs": results,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule", type=int, choices=[30, 90], required=True)
    ap.add_argument("--group", choices=["cell", "clause"], default="cell")
    ap.add_argument("--ns", type=int, nargs="+", required=True)
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--timeout", type=float, default=1200.0)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    # Ground truth cross-check (rule 30): dense simulation vs bit-parallel
    # generator; PREREGISTRATION.md records the generator's OEIS A051023 match.
    dense = simulate(30, 64)
    gen = center_column(65)
    assert all(dense[(t, 0)] == gen[t] for t in range(65)), "generator mismatch"

    out = []
    for n in args.ns:
        r = run_one(args.rule, n, args.group, args.seeds, args.timeout)
        if args.rule == 90 and args.group == "cell" and r["runs"]:
            odd = rule90_odd_set(n)
            for run in r["runs"]:
                run["matches_odd_binomial_set"] = (
                    {tuple(c) for c in run["cells"]} == odd
                )
            r["odd_binomial_cells"] = len(odd)
        for run in r["runs"]:
            prof = {}
            left = right = centre = 0
            for (t, x) in run.pop("cells"):
                prof[t] = prof.get(t, 0) + 1
                if x < 0:
                    left += 1
                elif x > 0:
                    right += 1
                else:
                    centre += 1
            run["left_right_centre"] = [left, right, centre]
            run["depth_profile"] = prof
        out.append(r)
        args.out.write_text(json.dumps(out, indent=1))  # checkpoint per band
        print(json.dumps({k: v for k, v in r.items() if k != "runs"}), flush=True)
        for run in r["runs"]:
            print(
                f"  seed={run['seed']} mus_cells={run['mus_cells']} "
                f"sel={run['mus_selectors']} calls={run['calls']} "
                f"lrc={run['left_right_centre']}",
                flush=True,
            )
        if not r["runs"]:
            print(f"  n={n}: no seed finished inside timeout; stopping ladder")
            break
    args.out.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()

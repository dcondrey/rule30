#!/usr/bin/env python3
"""Fusion #1 (SAT proof mining): does the UNSAT reason for RW have a small,

repeating core as n grows, rather than genuinely needing the whole instance?

rw_sat.encode's triangular (u,d) cell structure for u<n is shared, structural
dependency wiring -- always necessary. The only per-(n,r,c) additions are the
per-column target/hard-core constraints for u in [n, n+need) and the 12a
ending constraints. This reproduces that same construction but gates each of
those additions behind a fresh selector literal, so a minimal UNSAT core
(via Cadical's get_core() under all-selectors-true assumptions) tells us
exactly which target columns are jointly necessary -- not the whole
instance, and not a raw, unminimized DRAT derivation.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rw_sat import CNF  # noqa: E402
from pysat.solvers import Cadical153  # noqa: E402


def encode_with_selectors(n: int, r: int, c: int):
    """Same construction as rw_sat.encode, with a selector per gated group."""

    L = 2 * n + r + 2
    need = n + r + 2
    cnf = CNF()
    s = [cnf.var() for _ in range(L)]
    cells: dict[tuple[int, int], tuple[int, int]] = {}
    zero = cnf.const(False)
    for u in range(L):
        top = min(u, n)
        cells[(u, -u - 1)] = (s[u], zero)
        nots = cnf.xor2(s[u], cnf.const(True))
        cells[(u, -u)] = (nots, zero)
        for d in range(-u, top):
            hL, FL = cells[(u - 1, d)]
            h, F = cells[(u, d)]
            a = cnf.and2(cnf.xor2(hL, cnf.const(True)), FL)
            b = cnf.xor2(hL, FL)
            hn = cnf.xor2(cnf.xor2(h, a), cnf.const(True))
            Fn = cnf.xor2(F, cnf.and2(h, b))
            cells[(u, d + 1)] = (hn, Fn)

    Ec = c & 1
    selectors: dict[str, int] = {}
    for u in range(n, n + need):
        sel = cnf.var()
        selectors[f"col{u}"] = sel
        h, F = cells[(u, n)]
        cnf.clauses.append([-sel, h])
        cnf.clauses.append([-sel, F] if Ec else [-sel, -F])
        cnf.clauses.append([-sel, s[u - 1], s[u]])

    sel_end = cnf.var()
    selectors["ending"] = sel_end
    cnf.clauses.append([-sel_end, -s[L - 3]])
    cnf.clauses.append([-sel_end, s[L - 2]])

    return cnf, s, selectors


def find_core(n: int, r: int, c: int) -> tuple[list[str], int, int]:
    cnf, _, selectors = encode_with_selectors(n, r, c)
    slv = Cadical153(bootstrap_with=cnf.clauses)
    assumptions = list(selectors.values())
    ok = slv.solve(assumptions=assumptions)
    assert not ok, f"expected UNSAT at n={n} r={r} c={c}, got SAT"
    core_lits = set(slv.get_core())
    slv.delete()
    name_by_lit = {v: k for k, v in selectors.items()}
    core_names = sorted(
        (name_by_lit[lit] for lit in core_lits if lit in name_by_lit),
        key=lambda name: (name != "ending", int(name[3:]) if name != "ending" else -1),
    )
    return core_names, len(selectors), cnf.nv


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--ns", type=int, nargs="+", default=[10, 12, 14, 16, 18, 20])
    ap.add_argument("--r", type=int, default=0)
    ap.add_argument("--c", type=int, default=2)
    args = ap.parse_args()

    for n in args.ns:
        core, total, nv = find_core(n, args.r, args.c)
        # Report core columns relative to the tail end (u - (n + r + 2)),
        # so a "repeating reason" would show up as a stable relative shape.
        cols = [name for name in core if name != "ending"]
        col_offsets = [int(name[3:]) - n for name in cols]
        has_ending = "ending" in core
        print(
            f"n={n:3d} r={args.r} c={args.c}  vars={nv:6d}  "
            f"core size={len(core)}/{total}  "
            f"core col-offsets (from n)={col_offsets}  ending in core={has_ending}"
        )
        sys.stdout.flush()


if __name__ == "__main__":
    main()

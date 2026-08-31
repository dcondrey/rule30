"""Why a SAT solver's proof length is the WRONG instrument for R9's upper bound.

F_n AND (wrong-value unit at (n,0)) is refuted by unit propagation at decision
level 0.  CDCL therefore learns nothing and emits a near-empty DRUP proof.
Reading that lemma count as "derivation length" would manufacture a spurious
sub-quadratic result out of nothing.  The honest number is the expansion of the
single final RUP step into resolution inferences, which is exactly the level-0
propagation chain, i.e. Theta(diamond area).

This script measures all three quantities side by side.

Run:
    /Volumes/A/researchpapers/.venv/bin/python p3_drup_trap.py --out drup.json
"""

from __future__ import annotations

import argparse
import json
import logging

import p3_core as P


def propagation_chain(rule: int, n: int) -> int:
    """Number of distinct literals unit propagation assigns at level 0, i.e.
    the size of the implication graph the single RUP step stands for."""
    inst = P.Instance(rule, n)
    return len(inst.cone)  # every cell is forced; see gate below


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ns", type=int, nargs="+", default=[4, 8, 16, 32, 64])
    ap.add_argument("--out", default="drup.json")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    from pysat.solvers import Solver

    out = []
    for rule in (30, 90):
        for n in a.ns:
            inst = P.Instance(rule, n)
            cls = [list(c) for c in inst.axioms]
            wrong = [-list(inst.target())[0]]
            s = Solver(name="glucose4", bootstrap_with=cls + [wrong], with_proof=True)
            sat = s.solve()
            proof = s.get_proof() or []
            s.delete()
            # every cell forced at level 0: propagate the seed unit through the
            # rule clauses alone and count the implied literals.
            seed = list(inst.axioms[0])[0]
            s2 = Solver(name="glucose4", bootstrap_with=[list(c) for c in inst.axioms[1:]])
            ok, trail = s2.propagate(assumptions=[seed])
            s2.delete()
            base, _ = P.derive_full(rule, n)
            rec = {
                "rule": rule,
                "n": n,
                "unsat": not sat,
                "drup_lemmas": len(proof),
                "level0_forced": len(trail),
                "cells": len(inst.cone),
                "checked_resolution_steps": base.length,
            }
            out.append(rec)
            logging.info(
                "rule %d n=%-3d UNSAT=%s  DRUP lemmas=%-4d  level-0 forced literals=%-6d"
                "  cells=%-6d  checked resolution steps=%d",
                rule, n, not sat, len(proof), len(trail), len(inst.cone), base.length,
            )
    with open(a.out, "w") as f:
        json.dump(out, f, indent=1)
    logging.info("wrote %s", a.out)
    logging.info(
        "READ THIS: DRUP lemma count is NOT a resolution length here; the whole "
        "refutation lives in the level-0 propagation trail."
    )


if __name__ == "__main__":
    main()

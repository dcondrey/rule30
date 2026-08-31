"""Exact PC-degree of the light-cone system S_n(rule), by degree-d closure.

For each rule and each n, run the closure at d = 0, 1, 2, ... until 1 is
derived.  The first d that works is the exact PC refutation degree; the failures
below it are the exactness witnesses (1 not in V_{d-1}), so the number is a
measurement, not an upper bound.

    uv run python pc_degree_measure.py --ns 2 3 4 5 6 7 8 --out degrees.json
"""

from __future__ import annotations

import argparse
import json
import logging
import time

from pc_core import ONE, System, closure_degree, pdeg


def measure(n: int, rule: int, dmax: int, budget: float) -> dict:
    s = System(n, rule)
    ax = s.all_axioms()
    rec: dict = {
        "n": n,
        "rule": rule,
        "nvars": s.nvars,
        "naxioms": len(ax),
        "max_axiom_degree": s.max_axiom_degree(),
        "axiom_degree_hist": {},
        "levels": [],
        "pc_degree": None,
        "c_n": s.truth[(n, 0)],
    }
    hist: dict[int, int] = {}
    for p in ax:
        hist[pdeg(p)] = hist.get(pdeg(p), 0) + 1
    rec["axiom_degree_hist"] = {str(k): v for k, v in sorted(hist.items())}

    for d in range(dmax + 1):
        t0 = time.time()
        ok, dim, rounds = closure_degree(ax, s.nvars, d)
        dt = time.time() - t0
        rec["levels"].append(
            {"d": d, "one_in_Vd": ok, "dim_Vd": dim, "rounds": rounds, "secs": round(dt, 3)}
        )
        if ok:
            rec["pc_degree"] = d
            return rec
        if dt > budget:
            rec["wall"] = f"d={d} took {dt:.1f}s > budget {budget}s; stopped"
            return rec
    return rec


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ns", type=int, nargs="+", default=[2, 3, 4, 5, 6, 7, 8])
    ap.add_argument("--rules", type=int, nargs="+", default=[30, 90, 160, 128])
    ap.add_argument("--dmax", type=int, default=4)
    ap.add_argument("--budget", type=float, default=300.0)
    ap.add_argument("--out", default="degrees.json")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    log = logging.getLogger("pc")
    out = []
    for rule in args.rules:
        log.info("")
        log.info("rule %d   (exact PC refutation degree, closure to fixpoint)", rule)
        log.info(
            "%6s %7s %8s %7s %10s  %s", "n", "vars", "axioms", "maxdeg", "PC-degree",
            "dim V_d per level"
        )
        for n in args.ns:
            rec = measure(n, rule, args.dmax, args.budget)
            out.append(rec)
            dims = " ".join(
                f"d{l['d']}:{l['dim_Vd']}{'*' if l['one_in_Vd'] else ''}"
                for l in rec["levels"]
            )
            log.info(
                "%6d %7d %8d %7d %10s  %s",
                n, rec["nvars"], rec["naxioms"], rec["max_axiom_degree"],
                rec["pc_degree"] if rec["pc_degree"] is not None else rec.get("wall", "?"),
                dims,
            )
    with open(args.out, "w") as f:
        json.dump(out, f, indent=1)
    log.info("")
    log.info("wrote %s   ('*' marks the level at which 1 was derived)", args.out)


if __name__ == "__main__":
    main()

"""Mechanically counted, every-step-machine-checked resolution derivation
lengths for the three candidate families, rules 30 and 90.

Family 0  baseline   row simulation, all read parents.
Family 1  sliced     antecedent-minimal + backward slice (the OR-latch shortcut).
Family 2  k-step     block doubling: units only on rows divisible by k, with the
                     k-step composed clause DERIVED from the one-step axioms.
Family 3  backward   backward elimination chain: no intermediate unit at all,
                     one resolution per ancestor cell.  Exactly the optimum
                     found by the min-tree search at n=2,3.
Family 4  bwd+slice  family 3 restricted to the antecedent-minimal slice.

Run:
    /Volumes/A/researchpapers/.venv/bin/python p3_tables.py --out derivations.json
"""

from __future__ import annotations

import argparse
import json
import logging
import math

import p3_core as P


def fit(ns, ys):
    xs = [math.log(n) for n in ns]
    ls = [math.log(y) for y in ys]
    k = len(xs)
    mx, my = sum(xs) / k, sum(ls) / k
    den = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ls)) / den


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ns", type=int, nargs="+", default=[4, 8, 16, 32, 64, 128])
    ap.add_argument("--ks", type=int, nargs="+", default=[2, 4, 8, 16])
    ap.add_argument("--out", default="derivations.json")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    P.gate_ground_truth(512)
    logging.info("GATE: centre column == experiments/rule30/center_column.py to n=512")

    out = {}
    for rule in (30, 90):
        rows = []
        logging.info("")
        logging.info("rule %d  (every resolution step machine-checked)", rule)
        logging.info(
            "%6s %8s %10s %8s %9s %10s %8s %8s %8s %10s",
            "n", "cells", "baseline", "sliced", "backward", "bwd+slice",
            "base/n2", "slic/n2", "bwd/n2", "bwd/cells",
        )
        for n in a.ns:
            P.gate_encoding(rule, n)
            inst = P.Instance(rule, n)
            tgt = inst.target()
            b, bm = P.derive_full(rule, n)
            b.check(tgt)
            s, sm = P.derive_sliced(rule, n)
            s.check(tgt)
            w, wm = P.derive_backward(rule, n, False)
            w.check(tgt)
            ws, _ = P.derive_backward(rule, n, True)
            ws.check(tgt)
            rec = {
                "n": n, "diamond": len(inst.cone), "axioms": len(inst.axioms),
                "baseline": b.length, "sliced": s.length,
                "backward": w.length, "backward_sliced": ws.length,
                "slice_cells": sm["slice"],
                "backward_over_n2": w.length / n**2,
                "baseline_over_n2": b.length / n**2,
                "sliced_over_n2": s.length / n**2,
                "kstep": {},
            }
            for k in a.ks:
                if k > n // 2:
                    continue
                pf, _ = P.derive_kstep(rule, n, k)
                pf.check(tgt)
                rec["kstep"][str(k)] = pf.length
            rows.append(rec)
            logging.info(
                "%6d %8d %10d %8d %9d %10d %8.4f %8.4f %8.4f %10.4f",
                n, len(inst.cone), b.length, s.length, w.length, ws.length,
                rec["baseline_over_n2"], rec["sliced_over_n2"],
                rec["backward_over_n2"], w.length / len(inst.cone),
            )
        logging.info(
            "  fitted exponent: baseline %.4f   sliced %.4f   backward %.4f",
            fit([r["n"] for r in rows], [r["baseline"] for r in rows]),
            fit([r["n"] for r in rows], [r["sliced"] for r in rows]),
            fit([r["n"] for r in rows], [r["backward"] for r in rows]),
        )
        logging.info(
            "  k-step composition (block doubling), length / BEST family "
            "(backward).  k=1 is the row-simulation baseline at %.2fx.",
            rows[-1]["baseline"] / rows[-1]["backward"],
        )
        for k in a.ks:
            cells = [(r["n"], r["kstep"].get(str(k)), r["backward"]) for r in rows]
            txt = "  ".join(
                f"n={n}:{v / b:.2f}x" for n, v, b in cells if v is not None
            )
            logging.info("    k=%-3d %s", k, txt)
        out[str(rule)] = rows

    with open(a.out, "w") as f:
        json.dump(out, f, indent=1)
    logging.info("wrote %s", a.out)


if __name__ == "__main__":
    main()

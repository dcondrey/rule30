"""Encoding robustness + the numeric transfer analysis.

Part A. The ANF encoding of pc_core is the natural algebraic one and has
degree-2 axioms for rule 30.  A reader may object that the low PC degree is an
artifact of choosing the algebraic encoding.  So the same measurement is redone
over the *CNF-translation* encoding used by a4/a13: each cell contributes the
full truth-table clause set over its in-diamond parents, and a clause C is
translated to the polynomial prod_{x in C} (x + 1)^{[x positive]} x^{[x negative]},
whose axioms have degree up to 4.  If PC degree still does not grow, the verdict
is not an artifact of the encoding.

Part B. Plug the measured degree into the published size-degree relations and
report the resulting size bound as a number.

    uv run python pc_robustness.py --ns 2 3 4 5 6 --out robustness.json
"""

from __future__ import annotations

import argparse
import itertools
import json
import logging

from pc_core import System, apply_rule, closure_degree, padd, pdeg

ONE_P = frozenset({frozenset()})


def pmul(p, q):
    out: set = set()
    for a in p:
        for b in q:
            m = a | b
            if m in out:
                out.discard(m)
            else:
                out.add(m)
    return frozenset(out)


def clause_poly(clause) -> frozenset:
    """clause = list of (var, sign); sign True = positive literal.

    A clause is falsified iff every literal is false, so its polynomial is the
    product of the *negations* of its literals: positive x -> (x+1), negative -> x.
    Requiring that product to be 0 is exactly the clause.
    """
    p = ONE_P
    for v, sign in clause:
        f = frozenset({frozenset({v}), frozenset()}) if sign else frozenset({frozenset({v})})
        p = pmul(p, f)
    return p


def cnf_axioms(s: System, relevant_only: bool = True) -> list:
    """Full truth-table clause set per cell, translated to polynomials.

    relevant_only=True reproduces a13's convention exactly ("8 clauses per
    rule-30 cell, 4 per rule-90 cell"): a parent the rule's ANF does not depend
    on is dropped.  relevant_only=False keeps all three parents, which is the
    redundant variant; both are measured.
    """
    dep = set().union(*s.anf) if s.anf else set()
    ax = [frozenset({frozenset({s.idx[(0, 0)]}), frozenset()})]  # seed: s(0,0)+1
    for (t, x), _ in s.cell_axioms:
        v = s.idx[(t, x)]
        pars = [s._parent(t, x, w) for w in (0, 1, 2)]
        live = [
            (i, p)
            for i, p in enumerate(pars)
            if p is not None and (not relevant_only or i in dep)
        ]
        for bits in itertools.product((0, 1), repeat=len(live)):
            vals = [0, 0, 0]
            for (i, _), b in zip(live, bits):
                vals[i] = b
            out = apply_rule(s.rule, vals[0], vals[1], vals[2])
            # clause: NOT(parents = bits) OR (cell = out)
            cl = [(p, b == 0) for (_, p), b in zip(live, bits)]
            cl.append((v, out == 1))
            ax.append(clause_poly(cl))
    cn = s.truth[(s.n, 0)]
    ax.append(clause_poly([(s.idx[(s.n, 0)], cn == 0)]))  # negation unit
    return ax


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ns", type=int, nargs="+", default=[2, 3, 4, 5, 6])
    ap.add_argument("--rules", type=int, nargs="+", default=[30, 90, 160])
    ap.add_argument("--dmax", type=int, default=4)
    ap.add_argument("--out", default="robustness.json")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    log = logging.getLogger("rob")

    out = {"cnf_encoding": [], "transfer": []}
    for relevant_only in (True, False):
        tag = "a13 convention (relevant parents only)" if relevant_only else "redundant variant (all 3 parents)"
        for rule in args.rules:
            log.info("")
            log.info("rule %d -- CNF-TRANSLATION encoding, %s", rule, tag)
            log.info("%6s %7s %8s %8s %10s", "n", "vars", "axioms", "maxdeg", "PC-degree")
            for n in args.ns:
                s = System(n, rule)
                ax = cnf_axioms(s, relevant_only)
                md = max(pdeg(p) for p in ax)
                deg = None
                for d in range(args.dmax + 1):
                    ok, _, _ = closure_degree(ax, s.nvars, d)
                    if ok:
                        deg = d
                        break
                rec = {"rule": rule, "n": n, "nvars": s.nvars, "naxioms": len(ax),
                       "relevant_only": relevant_only,
                       "max_axiom_degree": md, "pc_degree": deg}
                out["cnf_encoding"].append(rec)
                log.info("%6d %7d %8d %8d %10s", n, s.nvars, len(ax), md, deg)

    # ---- Part B: numeric transfer ----------------------------------------
    log.info("")
    log.info("TRANSFER: published size-degree relations evaluated at the measured degree")
    log.info("  ANF encoding -> IPS Cor 5.3 (hypothesis: inconsistent CONSTANT-DEGREE")
    log.info("  polynomials; satisfied here).  CNF encoding -> Miksa-Nordstrom Thm 2.2")
    log.info("  (stated for a CNF formula with W(F) = clause width).  Each relation is")
    log.info("  applied only where its own hypothesis is literally met.")
    log.info("%6s %6s %8s %6s %-30s %6s %6s %-26s", "rule", "n", "N(vars)",
             "d_ANF", "IPS  M >= 2^(d^2/N)", "d_CNF", "W(F)", "MN  exp((d-W)^2/N)")
    for rule, d_anf, d_cnf in ((30, 2, 4), (90, 1, 3), (160, 2, 3), (128, 3, 4)):
        for n in (8, 64, 512, 4096):
            N = n * n // 2 + n + 1
            ips = 2.0 ** (d_anf * d_anf / N)
            mn = 2.0 ** (max(0, d_cnf - d_cnf) ** 2 / N)  # W(F) == d_cnf, measured
            out["transfer"].append({"rule": rule, "n": n, "N": N,
                                    "d_anf": d_anf, "ips_bound_anf": ips,
                                    "d_cnf": d_cnf, "W_F": d_cnf, "mn_bound_cnf": mn})
            log.info("%6d %6d %8d %6d %-30s %6d %6d %-26s", rule, n, N, d_anf,
                     f"{ips:.10f}", d_cnf, d_cnf, f"{mn:.10f}")

    with open(args.out, "w") as f:
        json.dump(out, f, indent=1)
    log.info("")
    log.info("wrote %s", args.out)


if __name__ == "__main__":
    main()

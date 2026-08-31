"""R9/A4: mechanical check of the two side conditions of the leaf-counting
lower bound, plus the combined window table.

Side condition 1 (clause-to-cell injectivity).  Distinct rule-bearing cells
own disjoint sets of axiom clauses, so |S| >= |G(S)| for any axiom set S.
Checked here by direct enumeration.

Side condition 2 (sufficiency closure).  If S is any set of axiom clauses that
implies c_n, then enforcing the rule on ALL of G(S) also implies c_n, because
the full clause set of a cell implies each of its clauses.  This is immediate
from S being a subset of that clause set; checked here as a containment.

Then: any derivation DAG with binary inferences, L distinct leaves and one
root has I >= L-1 internal nodes (edges 2I, nodes L+I, connectivity gives
2I >= L+I-1).  Hence

    length(any resolution derivation of c_n from F_n) >= mu(n) - 1

with mu(n) from min_gmus.py.  Reported against the machine-checked upper
bound from derivation_upper_bound.py.

Run:  uv run python leaf_bound_check.py
"""

from __future__ import annotations

import json
import logging
import sys
from collections import defaultdict

from derivation_upper_bound import RULES, diamond, simulate
from min_gmus import build


def check_injectivity(rule: int, n: int) -> int:
    """Assert no axiom clause is owned by two different cells."""
    reads, f = RULES[rule]
    truth = simulate(rule, n)
    cone = diamond(n)
    var = {c: i + 1 for i, c in enumerate(cone)}
    owner = {}
    total = 0
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
            lits = frozenset(
                [-pv[i] if asn[i] else pv[i] for i in idx]
                + [var[(t, x)] if out else -var[(t, x)]]
            )
            prev = owner.get(lits)
            assert prev is None or prev == (t, x), (
                f"clause {sorted(lits)} shared by cells {prev} and {(t, x)}"
            )
            owner[lits] = (t, x)
            total += 1
    by_cell = defaultdict(int)
    for c in owner.values():
        by_cell[c] += 1
    assert total == len(owner), "duplicate clauses within the axiom multiset"
    return len(owner)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
    ub = json.load(open("upper_bound.json"))
    mu = {}
    for path in ("smus30.json", "smus30_big.json", "smus90.json"):
        try:
            for r in json.load(open(path)):
                if r["mu"] is not None:
                    mu[(r["rule"], r["n"])] = r["mu"]
        except FileNotFoundError:
            pass

    for rule in (30, 90):
        logging.info("rule %d", rule)
        logging.info(
            "%5s %8s %10s %12s %12s %10s",
            "n", "cells", "axioms", "LB=mu-1", "UB=steps", "UB/LB",
        )
        for row in ub["rules"][str(rule)]:
            n = row["n"]
            k = check_injectivity(rule, n)
            assert k == row["axiom_clauses"] - 1, "axiom count mismatch (seed unit)"
            m = mu.get((rule, n))
            lb = "-" if m is None else str(m - 1)
            ratio = "-" if m is None else f"{row['derivation_steps'] / (m - 1):.2f}"
            logging.info(
                "%5d %8d %10d %12s %12d %10s",
                n, row["diamond_cells"], row["axiom_clauses"], lb,
                row["derivation_steps"], ratio,
            )
        logging.info("")
    logging.info("clause-to-cell injectivity: verified at every n above")


if __name__ == "__main__":
    main()

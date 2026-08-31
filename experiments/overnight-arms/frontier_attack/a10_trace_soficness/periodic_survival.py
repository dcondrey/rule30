"""How long do PERIODIC width-2 words survive in the column subshift?

Motivation: the textbook route to non-soficness is a pumped family x y^j z with
pairwise distinct follower sets.  That route needs y^j to stay in the language
for unboundedly many j.  This script measures, for every block u with
|u| <= 4 over Sigma = {0,1}^2, the largest j with u^j in L (checked inside the
EXACT language L_N).

Sigma letters: a = c_0(t) + 2*c_1(t), so 0=(0,0) 1=(1,0) 2=(0,1) 3=(1,1).

Run: uv run python periodic_survival.py --N 14 --rule 30
"""

from __future__ import annotations

import argparse
import itertools
import json
import logging
import pathlib

import numpy as np

from pump_search import cached_language, encode

log = logging.getLogger(__name__)
K = 2


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=14)
    ap.add_argument("--rules", type=str, default="30,90")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    here = pathlib.Path(__file__).parent
    N = args.N

    out = {}
    for rule in args.rules.split(","):
        words = cached_language(N, rule, here)
        pref = {n: set(int(w) & ((1 << (K * n)) - 1) for w in words)
                for n in range(1, N + 1)}
        rows = []
        for ulen in (1, 2, 3, 4):
            for u in itertools.product(range(4), repeat=ulen):
                jmax = 0
                for j in range(1, N // ulen + 1):
                    letters = list(u) * j
                    if encode(letters) in pref[len(letters)]:
                        jmax = j
                    else:
                        break
                rows.append({"u": list(u), "reps": jmax,
                             "length": jmax * ulen,
                             "capped": jmax * ulen > N - ulen})
        best = max(r["length"] for r in rows if not r["capped"]) if any(
            not r["capped"] for r in rows) else None
        uncapped = [r for r in rows if not r["capped"]]
        capped = [r for r in rows if r["capped"]]
        log.info("rule %s (exact L_%d):", rule, N)
        log.info("  blocks |u|<=4 whose powers DIE inside the window: %d/%d; "
                 "longest surviving power among them = %s letters",
                 len(uncapped), len(rows), best)
        log.info("  blocks whose powers reach the window edge (undecided): %d -> %s",
                 len(capped), [r["u"] for r in capped][:20])
        out[rule] = rows
    (here / "out" / f"periodic_survival_N{N}.json").write_text(json.dumps(
        {"note": "reps = max j with u^j in the exact language L_N; capped=True "
                 "means the window ran out, so that block is UNDECIDED here",
         "N": N, "results": out}, indent=1))
    log.info("wrote out/periodic_survival_N%d.json", N)


if __name__ == "__main__":
    main()

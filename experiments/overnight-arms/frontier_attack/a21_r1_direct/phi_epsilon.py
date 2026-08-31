"""a21 step 4: the full err(m,t) matrix, and whether eps(m) = lim_t err(m,t) -> 0.

err(m,t) = the exact minimum error, over the uniform measure on all 2^t
realisable centre prefixes, of ANY predictor of r_t from the m most recent
centre values c_{t-m}..c_{t-1}.  err(m,t) = 0 for some m < t would open the
bounded-window route to Lemma Z.  This script asks the quantitative form:

    does eps(m) := lim_t err(m,t) tend to 0 as m grows?

eps(m) -> 0 would say "arbitrarily long bounded windows come arbitrarily close",
which is not enough for Lemma Z (which needs exactness) but would make the
obstruction quantitative rather than structural.  eps(m) bounded away from 0
would be the stronger, structural statement.

OBSTRUCTION H APPLIES TO EVERY NUMBER BELOW.  This is a bounded computation.
It can refute "bounded window suffices at t <= TMAX"; it cannot establish
anything about the limit.  The limit column is an extrapolation and is labelled.

Usage: uv run python phi_epsilon.py [tmax] > phi_epsilon_output.txt
"""

from __future__ import annotations

import json
import sys

from phi_anf import build_table
from phi_reach import window_error


def main() -> None:
    tmax = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    print("a21 / phi_epsilon.py -- exact err(m,t) matrix for r_t | c_{t-m}..c_{t-1}")
    print(f"tmax = {tmax}\n")
    out = {}
    for rule in (30, 90):
        print(f"=== rule {rule}: err(m,t), rows t, columns m ===")
        hdr = "   t |" + "".join(f" m={m:<2d}   " for m in range(1, min(tmax, 12) + 1))
        print(hdr)
        mat = {}
        for t in range(1, tmax + 1):
            table, ok = build_table(t, rule)
            assert ok, (rule, t)
            we = window_error(table, t)
            mat[t] = we
            cells = []
            for m in range(1, min(tmax, 12) + 1):
                cells.append(f"{we[m]:.4f} " if m <= t else "  --   ")
            zero = next((m for m in range(t + 1) if we[m] == 0.0), None)
            print(f"  {t:2d} |{''.join(cells)}| first m with err=0: {zero}")
            sys.stdout.flush()
        out[str(rule)] = mat
        print()
        print(f"--- rule {rule}: err(m, t=tmax) as a function of m (EXTRAPOLATION ROW) ---")
        we = mat[tmax]
        for m in range(1, tmax + 1):
            print(f"    m={m:2d}  err(m,{tmax}) = {we[m]:.6f}")
        print()
    with open("phi_epsilon_results.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote phi_epsilon_results.json")


if __name__ == "__main__":
    main()

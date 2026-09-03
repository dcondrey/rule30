#!/usr/bin/env python3
"""Deepest E-only survivors (BWH+ near-misses) and the hard-core structure of their forced words.

For each (n, c) the E-only census (hard-core off) is run to K = n + 2 columns.
For survivors at the deepest E-only levels the forced continuation Q is printed
with the positions of its `11` factors and the junction, to see how far the
E-constant states are from the hard-core condition that RW adds.

Run:  cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/e_only_witnesses.py --min-n 12 --max-n 26
"""
from __future__ import annotations

import argparse
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rw_bitsliced import full_census, reference_path  # noqa: E402
from quotient_multiplicity import quotient_column  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-n", type=int, default=12)
    ap.add_argument("--max-n", type=int, default=26)
    args = ap.parse_args()
    print("n  c  E-deepest  need  states  min #11 in Q[:k] (junction incl.)  example W -> Q (E-only run k)")
    for n in range(args.min_n, args.max_n + 1):
        for c in (2, 3):
            N, exact, e12, wit, near = full_census(n, c, 22, n + 2, want_witness_masks=True, hardcore=False)
            deepest = max(k for k in range(len(N)) if N[k] > 0)
            ws = wit.get(deepest, [])
            states = {}
            for w in ws:
                states.setdefault(quotient_column(w), w)
            rows = []
            for q, w in states.items():
                run, forced, ebits, viol = reference_path(w, c, n + 2)
                # hard-core violations inside the E-run, junction included
                seg = w[-1] + forced[:deepest]
                pos = [i for i in range(len(seg) - 1) if seg[i] == seg[i + 1] == "1"]
                rows.append((len(pos), w, forced, pos))
            rows.sort()
            best = rows[0]
            print(f"{n:<3}{c:<3}{deepest:<11}{n+2:<6}{len(states):<8}{best[0]:<34}{best[1]} -> {best[2]}  11 at {best[3]}")
            sys.stdout.flush()


if __name__ == "__main__":
    main()

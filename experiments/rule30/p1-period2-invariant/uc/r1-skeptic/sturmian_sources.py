#!/usr/bin/env python3
"""RW admissible runs for Sturmian (Fibonacci-word) and related aperiodic hard-core sources.

Periodic sources of period <= 20 have RW runs that stay O(1) up to n = 200
(periodic_family_p20.log).  The next structured family with a hard-core
guarantee is the Fibonacci word 0100101001001... (no two consecutive 1s),
read as a binary source under both letter maps (0 -> 2, 1 -> 1) and
(0 -> 1, 1 -> 2; not hard-core), plus the length-n factors of each (Sturmian
words of slope 1/phi^2, n+1 distinct factors per n).  For every such source
of length n = 8..--max-n and both c the admissible run (E-hit and hard-core
per column, binary bookkeeping) is computed with the reference path of
rw_bitsliced.reference_path (psi_kernel), and the maximum run and run/n are
reported.  A counterexample is run >= n + 2.

Run:  cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/sturmian_sources.py --max-n 64
"""

from __future__ import annotations

import argparse
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))

from rw_bitsliced import reference_path  # noqa: E402


def fibonacci_word(length: int) -> str:
    a, b = "0", "01"
    while len(b) < length:
        a, b = b, b + a
    return b[:length]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-n", type=int, default=64)
    args = ap.parse_args()
    fw = fibonacci_word(4 * args.max_n)
    maps = {"0->2,1->1 (hard-core)": {"0": "2", "1": "1"}, "0->1,1->2": {"0": "1", "1": "2"}}
    t0 = time.time()
    print(" n   map                    #factors  max run  run/n  need  slack  best factor")
    overall = {}
    for n in range(8, args.max_n + 1):
        factors = sorted({fw[i : i + n] for i in range(len(fw) - n)})
        for name, mp in maps.items():
            best = (-1, None, None)
            for f in factors:
                w = "".join(mp[ch] for ch in f)
                for c in (2, 3):
                    run, _, _, _ = reference_path(w, c, n + 2)
                    if run > best[0]:
                        best = (run, w, c)
            run, w, c = best
            overall[name] = max(overall.get(name, 0), run - 0.0)
            flag = "  <- RW COUNTEREXAMPLE" if run >= n + 2 else ""
            if n % 4 == 0 or run >= n + 2:
                print(f"{n:<4} {name:<22} {len(factors):<9} {run:<8} {run/n:5.2f}  {n+2:<5} {n+2-run:<6} c={c} {w[:40]}{flag}")
    print(f"max run over all n, per map: {overall}   [{time.time()-t0:.1f}s]")


if __name__ == "__main__":
    main()

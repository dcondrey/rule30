#!/usr/bin/env python3
"""Kill test for the window-halving lemma.

Definitions (BRIEF section 2 coordinates; psi_kernel.Endpoint conventions):
  Lambda(n)  = number of distinct level-0 letter windows over W in {1,2}^n,
               a level-0 letter window being (e_{n-1}, ((a,b) of T[n-1][d]
               for d = -(n-1) .. n-1)) with a = [T == 0], b = [Lo(T) == 0].
  D_k(n, c)  = number of distinct cell windows (e_u, T[u][-u .. n-1]) at column
               u = n+k-1 over the prefixes whose forced orbit hits (T[u'][n] = c)
               at every column u' = n .. n+k-1 with the forced word hard-core
               (no e_{u'-1} = e_{u'} = 1, junction with e_{n-1} included).
  D^E_k(n,c) = the same without the hard-core condition (the (BWH+) ablation).

Lemma (window halving): D_k(n, c) <= C * Lambda(n) * 2^(-k) for all n >= n0,
c in {2,3}, k >= 1, with an absolute constant C < 4.  Since Lambda(n) <= 2^n,
D_{n+2} <= C/4 < 1, so no prefix hits n+2 times: this is (RW) at r = 0, hence
all r.  The script prints rho(n,c,k) = D_k 2^k / Lambda(n) and its max over k,
for RW and for the E-only ablation; any rho > C is a kill.

    cd .../p1-period2-invariant && uv run python uc/r1-potential/window_halving.py --min-n 3 --max-n 18
"""

from __future__ import annotations

import argparse
import math
import sys
from collections import defaultdict
from itertools import product

sys.path.insert(0, "uc/r1-potential")
sys.path.insert(0, ".")
from orbit_census import build_from_prefix, forced_step, letter  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-n", type=int, default=3)
    ap.add_argument("--max-n", type=int, default=17)
    ap.add_argument("--log", default="uc/r1-potential/window_halving.log")
    args = ap.parse_args()
    overall = {"RW": (0.0, None), "E": (0.0, None)}
    with open(args.log, "w") as log:
        print("rho(n,c,k) = D_k * 2^k / Lambda(n); lemma needs rho <= C < 4 for all k >= 1 (RW column).", file=log)
        print("  n   Lambda  log2Lam  loss | c | RW: deepest, max_k rho, argmax k, rho at deepest | E-only: deepest, max_k rho, argmax k", file=log)
        for n in range(args.min_n, args.max_n + 1):
            max_steps = n + 3
            lam_set = set()
            per_c = {}
            for target in (2, 3):
                per_c[target] = {
                    "D": defaultdict(set), "DE": defaultdict(set), "N": defaultdict(int), "NE": defaultdict(int),
                }
            for source in product((1, 2), repeat=n):
                col0 = build_from_prefix(source, n)
                lam_set.add((col0.e, tuple(letter(t) for t in col0.states[:-1])))
                for target in (2, 3):
                    rec = per_c[target]
                    col = col0
                    prev_e = source[-1]
                    hc_ok = True
                    for k in range(1, max_steps + 1):
                        e, nxt = forced_step(col)
                        if nxt.states[-1] != target:
                            break
                        if prev_e == 1 and e == 1:
                            hc_ok = False
                        key = (nxt.e, tuple(nxt.states[:-1]))
                        rec["DE"][k].add(key)
                        rec["NE"][k] += 1
                        if hc_ok:
                            rec["D"][k].add(key)
                            rec["N"][k] += 1
                        col, prev_e = nxt, e
            lam = len(lam_set)
            line = f"{n:3d} {lam:8d} {math.log2(lam):7.2f} {n - math.log2(lam):5.2f}"
            for target in (2, 3):
                rec = per_c[target]
                rows = []
                for name in ("D", "DE"):
                    dk = rec[name]
                    deepest = max(dk) if dk else 0
                    best = (0.0, 0)
                    for k, s in dk.items():
                        rho = len(s) * 2 ** k / lam
                        if rho > best[0]:
                            best = (rho, k)
                    rho_deep = len(dk[deepest]) * 2 ** deepest / lam if deepest else 0.0
                    rows.append((deepest, best, rho_deep))
                    tag = "RW" if name == "D" else "E"
                    if best[0] > overall[tag][0]:
                        overall[tag] = (best[0], (n, target, best[1]))
                (d1, b1, r1), (d2, b2, _) = rows
                print(f"{line} | {target} | {d1:2d} {b1[0]:6.3f} k={b1[1]:2d} rho_deep={r1:6.3f} | {d2:2d} {b2[0]:7.3f} k={b2[1]:2d}", file=log)
                # full table for this (n, c)
                print(f"      k:  " + " ".join(f"{k:6d}" for k in sorted(rec['D'])), file=log)
                print(f"      D_k:" + " ".join(f"{len(rec['D'][k]):6d}" for k in sorted(rec['D'])), file=log)
                print(f"      rho:" + " ".join(f"{len(rec['D'][k]) * 2 ** k / lam:6.2f}" for k in sorted(rec['D'])), file=log)
                print(f"      N_k:" + " ".join(f"{rec['N'][k]:6d}" for k in sorted(rec['D'])), file=log)
            log.flush()
        print(f"\nmax rho over n, c, k:  RW: {overall['RW'][0]:.3f} at (n, c, k) = {overall['RW'][1]};  E-only: {overall['E'][0]:.3f} at {overall['E'][1]}", file=log)
    print(f"log written to {args.log}")


if __name__ == "__main__":
    main()

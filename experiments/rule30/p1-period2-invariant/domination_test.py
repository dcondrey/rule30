#!/usr/bin/env python3
"""Domination test for RESULTS-CROSS-METHOD-INVARIANT-AUDIT.md section 6b.

Target: is the true per-step survival weight of `literal_extension`'s forced
continuation dominated by the null transfer matrix M = [[0,1/4],[1/4,1/4]]
(leading eigenvalue phi/4), uniformly enough to give 2*lambda < 1?

If S_k = number of source words surviving k forced rows, the induction
needs S_{k+1} <= lambda * S_k with lambda < 1/2, giving S_n <= (2 lambda)^n.
Raw (unweighted) domination is predicted to FAIL by the null model itself:
from a node whose last symbol is 2 both extensions are legal, so the null
one-step survival there is exactly 1/2, at the threshold before any
fluctuation. The reason phi/4 < 1/2 is the alternation with state 1
(survival 1/4). So the informative test is the WEIGHTED one, with weights
w = Perron eigenvector of M = (w(last=1), w(last=2)) = (1, phi).

This builds the exact survivor tree from the REAL `literal_extension`
(not psi_kernel -- that distinction is the naming collision recorded in
BACKLOG.md section 17), splits the surviving population by last symbol at
every depth, and reports:
  - the raw per-depth ratio S_{k+1}/S_k  (and its max)
  - the weighted ratio under w=(1,phi)   (and its max)
  - the LP-optimal weight w2 minimizing the max weighted ratio
Throwaway experiment script; not wired into any pipeline.
"""
from __future__ import annotations

import argparse
from itertools import product

from late_pull_diagonal_sat import literal_extension

PHI = (1 + 5 ** 0.5) / 2


def transfer_counts(n: int, tail: int, rows: int):
    """Per-depth surviving counts split by last symbol, plus transition counts.

    Returns list over depth k of dict with A (last==1), B (last==2) and the
    transition counts n12 (from 1 -> 2), n21 (2 -> 1), n22 (2 -> 2).
    Depth 0 is the junction symbol (last symbol of the source word).
    """
    # state[k] accumulates counts; we walk each source word down the tree.
    per_depth: list[dict[str, int]] = [
        {"A": 0, "B": 0, "n12": 0, "n21": 0, "n22": 0} for _ in range(rows + 1)
    ]
    for word in product((1, 2), repeat=n):
        cont = literal_extension(word, tail, rows)
        prev = word[-1]
        # depth 0 population is the junction symbol itself
        per_depth[0]["A" if prev == 1 else "B"] += 1
        for k, value in enumerate(cont):
            if value not in (1, 2):
                break
            if prev == 1 and value == 1:
                break
            # legal transition prev -> value
            if prev == 1:
                per_depth[k]["n12"] += 1
            elif value == 1:
                per_depth[k]["n21"] += 1
            else:
                per_depth[k]["n22"] += 1
            per_depth[k + 1]["A" if value == 1 else "B"] += 1
            prev = value
    return per_depth


def ratios(per_depth, w2: float):
    """Raw and weighted per-depth contraction ratios. w1 fixed to 1."""
    raw, weighted = [], []
    for k in range(len(per_depth) - 1):
        cur, nxt = per_depth[k], per_depth[k + 1]
        s_cur = cur["A"] + cur["B"]
        s_nxt = nxt["A"] + nxt["B"]
        if s_cur == 0:
            continue
        raw.append((k, s_nxt / s_cur, s_cur, s_nxt))
        wc = cur["A"] * 1.0 + cur["B"] * w2
        wn = nxt["A"] * 1.0 + nxt["B"] * w2
        if wc > 0:
            weighted.append((k, wn / wc, s_cur))
    return raw, weighted


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-n", type=int, default=10)
    ap.add_argument("--max-n", type=int, default=16)
    ap.add_argument("--min-count", type=int, default=0,
                    help="ignore depths whose surviving population is below this "
                         "(0 = use every depth, which is what a proof needs)")
    args = ap.parse_args()

    all_cases = []
    for n in range(args.min_n, args.max_n + 1):
        for tail in (2, 3):
            rows = n + 4
            pd = transfer_counts(n, tail, rows)
            all_cases.append((n, tail, pd))
            raw, _ = ratios(pd, PHI)
            shown = [(k, round(r, 4)) for k, r, sc, sn in raw if sc >= 1]
            print(f"n={n} c={tail}: raw S_(k+1)/S_k = {shown}")

    print()
    print("=" * 70)
    print("RAW (unweighted) domination:  need max_k S_(k+1)/S_k < 0.5")
    worst = []
    for n, tail, pd in all_cases:
        raw, _ = ratios(pd, PHI)
        for k, r, sc, sn in raw:
            if sc >= args.min_count:
                worst.append((r, n, tail, k, sc, sn))
    worst.sort(reverse=True)
    print(f"  max raw ratio = {worst[0][0]:.4f} at n={worst[0][1]} c={worst[0][2]} "
          f"depth={worst[0][3]} (S_k={worst[0][4]} -> S_(k+1)={worst[0][5]})")
    print("  top 8 violators:")
    for r, n, tail, k, sc, sn in worst[:8]:
        flag = "  <-- EXCEEDS 0.5" if r >= 0.5 else ""
        print(f"    {r:.4f}  n={n} c={tail} depth={k}  {sc} -> {sn}{flag}")
    print(f"  => raw domination {'HOLDS' if worst[0][0] < 0.5 else 'FAILS'}")

    print()
    print("=" * 70)
    print(f"WEIGHTED domination, w=(1, phi={PHI:.6f}) (Perron eigenvector of M)")
    wworst = []
    for n, tail, pd in all_cases:
        _, wt = ratios(pd, PHI)
        for k, r, sc in wt:
            if sc >= args.min_count:
                wworst.append((r, n, tail, k, sc))
    wworst.sort(reverse=True)
    print(f"  max weighted ratio = {wworst[0][0]:.4f} at n={wworst[0][1]} "
          f"c={wworst[0][2]} depth={wworst[0][3]} (S_k={wworst[0][4]})")
    print("  top 8 violators:")
    for r, n, tail, k, sc in wworst[:8]:
        flag = "  <-- EXCEEDS 0.5" if r >= 0.5 else ""
        print(f"    {r:.4f}  n={n} c={tail} depth={k}  S_k={sc}{flag}")
    print(f"  => weighted domination {'HOLDS' if wworst[0][0] < 0.5 else 'FAILS'}")

    print()
    print("=" * 70)
    print("LP: minimize over w2 the max weighted ratio (w1 = 1)")
    best = None
    w2 = 0.05
    while w2 <= 8.0:
        m = 0.0
        for n, tail, pd in all_cases:
            _, wt = ratios(pd, w2)
            for k, r, sc in wt:
                if sc >= args.min_count:
                    m = max(m, r)
        if best is None or m < best[1]:
            best = (w2, m)
        w2 += 0.01
    print(f"  best w2 = {best[0]:.2f}  ->  lambda_min = {best[1]:.4f}")
    print(f"  (phi = {PHI:.4f} for comparison)")
    print(f"  => LP domination {'HOLDS' if best[1] < 0.5 else 'FAILS'} "
          f"(need lambda < 0.5)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Check the state-halving lemma D_k <= Q_n 2^-k on every logged (n, c, k).

Reads the per-level tables of state_level_hits_*.log and state_count_*.log in
this directory (D_k = number of distinct level-k states among survivors) and
the exact Q_n = D_0 lines (n <= 28), fitting Q_n = A * rho^n on the exact values
for n = 21..28 and using the fit only for n = 29..31 (marked *).  Prints, per
(n, c), the minimum over logged k of log2(Q_n) - k - log2(D_k) (the lemma holds
iff this is >= 0) and the level attaining it, and the deepest-level margin
log2 Q_n - deepest.  Also verifies N_k <= 2^(n-k) on the same rows.

Run:  cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/state_halving_check.py
"""

from __future__ import annotations

import glob
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    q: dict[int, int] = {}
    tables: dict[tuple[int, int], dict[int, tuple[int, int]]] = {}
    deep: dict[tuple[int, int], int] = {}
    for path in sorted(glob.glob(os.path.join(HERE, "state_level_hits_n*.log")) + glob.glob(os.path.join(HERE, "state_count_n*.log"))):
        cur = None
        for line in open(path):
            m = re.match(r"^n=(\d+) c=(\d) deepest=(\d+)(?: Q_n=D_0=(\d+))?", line)
            if m:
                n, c, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
                cur = (n, c)
                deep[cur] = d
                if m.group(4):
                    q[n] = int(m.group(4))
                tables.setdefault(cur, {})
                continue
            m = re.match(r"^\s+(\d+)\s+(\d+)\s+(\d+)\s+", line)
            if m and cur is not None:
                k, N, D = int(m.group(1)), int(m.group(2)), int(m.group(3))
                tables[cur][k] = (N, D)
    exact = sorted(n for n in q if n >= 21)
    rho = (q[exact[-1]] / q[exact[0]]) ** (1.0 / (exact[-1] - exact[0]))
    A = q[exact[-1]] / rho ** exact[-1]
    print(f"exact Q_n: {dict(sorted(q.items()))}")
    print(f"fit on n={exact[0]}..{exact[-1]}: Q_n = {A:.4f} * {rho:.4f}^n")
    print()
    print(" n  c  deepest  log2Q_n   deep-margin   min_k margin (k)   source-halving max N_k/2^(n-k) (k)")
    worst = (1e9, None)
    for (n, c) in sorted(tables):
        if n in q:
            lq, mark = math.log2(q[n]), " "
        else:
            lq, mark = math.log2(A) + n * math.log2(rho), "*"
        rows = tables[(n, c)]
        if not rows:
            print(f"{n:<3}{c:<3}{deep[(n,c)]:<8} {lq:6.2f}{mark}  {lq - deep[(n,c)]:6.2f}     (no per-level rows logged)")
            continue
        margins = [(lq - k - math.log2(D), k) for k, (N, D) in rows.items() if D > 0]
        mm, mk = min(margins)
        src = max((N / 2 ** (n - k), k) for k, (N, D) in rows.items() if N > 0)
        print(f"{n:<3}{c:<3}{deep[(n,c)]:<8} {lq:6.2f}{mark}  {lq - deep[(n,c)]:6.2f}      {mm:6.2f} ({mk:<2})         {src[0]:6.3f} ({src[1]})")
        if n >= 10 and mm < worst[0]:
            worst = (mm, (n, c, mk))
    print()
    print(f"minimum logged margin log2(Q_n 2^-k / D_k) over n >= 10: {worst[0]:.2f} at (n, c, k) = {worst[1]}  [lemma holds iff >= 0]")


if __name__ == "__main__":
    main()

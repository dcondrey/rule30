#!/usr/bin/env python3
"""Which (C, lambda) does the RW census support?  Parses rw_counts logs.

Two nulls per (n, k):

  null_E(n, k)  = 2^(n-k)                       one bit per E constraint
  null_HC(n, k) = 2^n * A_k / 4^k               two bits per pinned cell,
                                                 hard-core continuation

with A_k = (Fib(k+2) + Fib(k+1)) / 2 the mean number of hard-core words of
length k over {1,2} given a uniformly random previous symbol (previous = 2
allows Fib(k+2) words, previous = 1 allows Fib(k+1)).

For each (n, c) and the RW-mode counts N_k, the script prints
  rho_E  = max_k N_k / null_E        (k >= 1)
  rho_HC = max_k N_k / null_HC       (k >= 1)
and the argmax k, plus the least-squares slope of log2 N_k over k with
N_k >= 8, and the smallest C such that N_k <= C * 2^(n - lambda k) holds for
every k, for lambda in (1.0, 1.2, 1.306, 1.4).

Usage: uv run python uc/r1-injection/rw_rate_fit.py uc/r1-injection/rw_counts_n3-13.log uc/r1-injection/rw_counts_n14-17.log
"""

from __future__ import annotations

import ast
import math
import sys


def fib(k: int) -> int:
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def parse(paths: list[str]) -> dict[tuple[int, int], list[int]]:
    table: dict[tuple[int, int], list[int]] = {}
    for path in paths:
        with open(path) as fh:
            for line in fh:
                if not line.startswith("RW"):
                    continue
                head, _, tail = line.partition("[")
                parts = head.split()
                n, c = int(parts[1]), int(parts[2])
                table[(n, c)] = ast.literal_eval("[" + tail.strip())
    return table


def main() -> None:
    table = parse(sys.argv[1:])
    lambdas = (1.0, 1.2, 1.306, 1.4)
    print(" n c  rho_E(k*)     rho_HC(k*)    slope   " + "  ".join(f"C(l={l})" for l in lambdas))
    for (n, c) in sorted(table):
        vals = table[(n, c)]
        rho_e, ke = max((v / 2 ** (n - k), k) for k, v in enumerate(vals) if k >= 1)
        rho_h, kh = max(
            (v / (2 ** n * (fib(k + 2) + fib(k + 1)) / 2 / 4 ** k), k)
            for k, v in enumerate(vals)
            if k >= 1
        )
        pts = [(k, math.log2(v)) for k, v in enumerate(vals) if v >= 8]
        if len(pts) >= 3:
            m = len(pts)
            sx = sum(k for k, _ in pts)
            sy = sum(y for _, y in pts)
            sxx = sum(k * k for k, _ in pts)
            sxy = sum(k * y for k, y in pts)
            slope = (m * sxy - sx * sy) / (m * sxx - sx * sx)
        else:
            slope = float("nan")
        cs = []
        for lam in lambdas:
            cs.append(max(v / 2 ** (n - lam * k) for k, v in enumerate(vals)))
        print(
            f"{n:>2} {c}  {rho_e:6.2f} ({ke:>2})   {rho_h:6.2f} ({kh:>2})   {slope:6.3f}   "
            + "  ".join(f"{x:8.2f}" for x in cs)
        )


if __name__ == "__main__":
    main()

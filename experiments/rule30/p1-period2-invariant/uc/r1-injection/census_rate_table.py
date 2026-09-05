#!/usr/bin/env python3
"""Which (C, lambda) does the complete RW census support, n = 3..33?

Sources of N_k (RW mode, r = 0, both c), all complete searches:
  n = 3..13   uc/r1-injection/rw_counts_n3-13.log        (rw_counts.py, RW rows)
  n = 14..17  uc/r1-injection/rw_counts_n14-17.log       (rw_counts.py, RW rows)
  n = 18..22  uc/r1-injection/rw_counts_pruned_n18-22.log (rw_counts_pruned.py)
  n = 21..33  uc/r1-skeptic/census_n21_30.json, census_n31.json, census_n32.json,
              census_n33.json (rw_bitsliced.py, field "N"); n = 21, 22 overlap the
              pruned log and are checked to agree exactly.

For each lambda in LAMBDAS and each (n, c) the script prints
    C_n(lambda) = max_{k >= 1, N_k > 0} N_k / 2^(n - lambda k)
and the k attaining it.  A bounded C_n(lambda) across n is what a counting
lemma N_k <= C 2^(n - lambda k) needs; a C_n that grows with n kills that
lambda.  Also printed: the fibre-run check  log2 N_D + D <= n + log2 3  at the
deepest level D (the tail form of the lambda = 1 bound with C = 3).

Usage: cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-injection/census_rate_table.py
"""

from __future__ import annotations

import ast
import json
import math
import re

DIR = "uc/r1-injection/"
SKEPTIC = "uc/r1-skeptic/"
LAMBDAS = (1.0, 1.1, 1.2, 1.3, 1.415)


def parse_rw_counts(path: str, table: dict) -> None:
    with open(path) as fh:
        for line in fh:
            if not line.startswith("RW"):
                continue
            head, _, arr = line.partition("[")
            parts = head.split()
            n, c = int(parts[1]), int(parts[2])
            vals = ast.literal_eval("[" + arr.strip())
            table[(n, c)] = vals


def parse_pruned(path: str, table: dict) -> None:
    with open(path) as fh:
        for line in fh:
            m = re.match(r"\s*(\d+)\s+(\d)\s+\d+\s+[\d.]+ \(\s*\d+\)\s+[\d.]+ \(\s*\d+\)\s+\d+s\s+(\[.*\])", line)
            if not m:
                continue
            n, c = int(m.group(1)), int(m.group(2))
            table[(n, c)] = ast.literal_eval(m.group(3))


def parse_skeptic(table: dict) -> dict:
    out = {}
    for name in ("census_n21_30.json", "census_n31.json", "census_n32.json", "census_n33.json"):
        with open(SKEPTIC + name) as fh:
            data = json.load(fh)
        for _, rec in data.items():
            n, c, N = rec["n"], rec["c"], rec["N"]
            if (n, c) in table:
                assert table[(n, c)][: len(N)] == N[: len(table[(n, c)])] or all(
                    a == b for a, b in zip(table[(n, c)], N)
                ), ("census mismatch", n, c, table[(n, c)], N)
                out[(n, c)] = "agree"
            table[(n, c)] = N
    return out


def main() -> None:
    table: dict[tuple[int, int], list[int]] = {}
    parse_rw_counts(DIR + "rw_counts_n3-13.log", table)
    parse_rw_counts(DIR + "rw_counts_n14-17.log", table)
    parse_pruned(DIR + "rw_counts_pruned_n18-22.log", table)
    overlap = parse_skeptic(table)
    print(f"loaded N_k for {len(table)} (n, c) pairs; skeptic/pruned overlap checks: {overlap}")
    hdr = " n c  D  N_D   " + "  ".join(f"C(l={l:.3f})@k" for l in LAMBDAS) + "   D+log2(N_D)-n  (<=1.585 needed)"
    print(hdr)
    worst = {l: (0.0, None) for l in LAMBDAS}
    worst_ge10 = {l: (0.0, None) for l in LAMBDAS}
    tail_worst = (-99.0, None)
    for (n, c) in sorted(table):
        N = table[(n, c)]
        D = max(k for k, v in enumerate(N) if v > 0)
        cells = []
        for l in LAMBDAS:
            best = (0.0, 0)
            for k in range(1, D + 1):
                r = N[k] / 2 ** (n - l * k)
                if r > best[0]:
                    best = (r, k)
            cells.append(f"{best[0]:9.2f}@{best[1]:<3}")
            if best[0] > worst[l][0]:
                worst[l] = (best[0], (n, c, best[1]))
            if n >= 10 and best[0] > worst_ge10[l][0]:
                worst_ge10[l] = (best[0], (n, c, best[1]))
        tail = D + math.log2(N[D]) - n
        if tail > tail_worst[0]:
            tail_worst = (tail, (n, c))
        print(f"{n:>2} {c} {D:>2} {N[D]:>5}  " + "  ".join(cells) + f"   {tail:6.2f}")
    print()
    for l in LAMBDAS:
        print(f"lambda={l:.3f}: max C over all n = {worst[l][0]:.2f} at {worst[l][1]};  over n>=10: {worst_ge10[l][0]:.2f} at {worst_ge10[l][1]}")
    print(f"tail form: max over (n,c) of D + log2 N_D - n = {tail_worst[0]:.2f} at {tail_worst[1]}  (lambda=1, C=3 needs <= 1.585; C=1 needs <= 0)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""RW-mode survivor counts N_k by pruned search (fast; kill test driver).

Same quantity as the RW rows of rw_counts.py (sources W in {1,2}^n whose
forced orbit satisfies E_1..E_k and HC_1..HC_k), computed by stopping each
source at its first failure.  Also computes, per (n, c):

  rho_E  = max_{k>=1} N_k / 2^(n-k)
  rho_HC = max_{k>=1} N_k / (2^n A_k / 4^k),  A_k = (Fib(k+2)+Fib(k+1))/2

and checks the shift inequality N_k(n) <= 2 N_{k-2}(n+1) when both n and
n+1 are in range (a proved statement; the check is a gate on the code).

Kill tests (uc/r1-injection lemmas):
  lemma prefix-null-one-bit : rho_E  <= 1 for every n >= 10
  lemma hc-null-constant-4  : rho_HC <= 4 for every n >= 10

Usage: uv run python uc/r1-injection/rw_counts_pruned.py --min 18 --max 20
"""

from __future__ import annotations

import argparse
import sys
import time
from itertools import product

sys.path.insert(0, ".")
from psi_kernel import Endpoint  # noqa: E402


def fib(k: int) -> int:
    a, b = 0, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def depth_of(source: tuple[int, ...], target: int) -> int:
    n = len(source)
    state = Endpoint()
    for s in source:
        state.append(s)
    previous = source[-1]
    depth = 0
    for _ in range(n + 2):
        chosen = None
        for symbol in (1, 2):
            column, diagonal = state.peek(symbol)
            if diagonal[n] >> 1 == 1:
                chosen = (symbol, diagonal[n], column, diagonal)
                break
        assert chosen is not None
        symbol, cell, column, diagonal = chosen
        if cell != target or (previous == 1 and symbol == 1):
            return depth
        nxt = Endpoint()
        nxt.column = column + [symbol]
        nxt.diagonal = diagonal
        nxt.length = state.length + 1
        state = nxt
        previous = symbol
        depth += 1
    return depth


def counts(n: int, target: int) -> list[int]:
    hist = [0] * (n + 3)
    for source in product((1, 2), repeat=n):
        hist[depth_of(source, target)] += 1
    vals = [0] * (n + 3)
    acc = 0
    for k in range(n + 2, -1, -1):
        acc += hist[k]
        vals[k] = acc
    return vals


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min", type=int, default=18)
    parser.add_argument("--max", type=int, default=20)
    args = parser.parse_args()
    table: dict[tuple[int, int], list[int]] = {}
    print(" n c deepest  rho_E(k)   rho_HC(k)   time   N_k")
    for n in range(args.min, args.max + 1):
        for target in (2, 3):
            t0 = time.time()
            vals = counts(n, target)
            table[(n, target)] = vals
            deepest = max(k for k, v in enumerate(vals) if v > 0)
            rho_e, ke = max((v / 2 ** (n - k), k) for k, v in enumerate(vals) if k >= 1)
            rho_h, kh = max(
                (v / (2 ** n * (fib(k + 2) + fib(k + 1)) / 2 / 4 ** k), k)
                for k, v in enumerate(vals)
                if k >= 1
            )
            flag = ""
            if n >= 10 and rho_e > 1:
                flag += "  KILL prefix-null-one-bit"
            if n >= 10 and rho_h > 4:
                flag += "  KILL hc-null-constant-4"
            print(
                f"{n:>2} {target} {deepest:>7}  {rho_e:5.2f} ({ke:>2})  {rho_h:5.2f} ({kh:>2})  "
                f"{time.time() - t0:5.0f}s  {vals}{flag}"
            )
            sys.stdout.flush()
    for (n, c), vals in sorted(table.items()):
        nxt = table.get((n + 1, c))
        if nxt is None:
            continue
        bad = [k for k in range(2, len(vals)) if vals[k] > 2 * nxt[k - 2]]
        print(f"shift inequality N_k({n}) <= 2 N_(k-2)({n + 1}), c={c}: "
              + ("PASS" if not bad else f"FAIL at k={bad}"))


if __name__ == "__main__":
    main()

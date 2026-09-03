#!/usr/bin/env python3
"""Distinct forced words among RW survivors, by pruned search (kill driver).

For each (n, c): Fq_k = #{Q_k(W) : W in S_k} where Q_k(W) is the forced
continuation (first k forced symbols) and S_k the RW survivors; also N_k and
the ratio Fq_k / null(n, k) with null(n, k) = 2^n A_k / 4^k,
A_k = (Fib(k+2) + Fib(k+1)) / 2.  The deepest level's forced words are
listed with their multiplicities.

Kill test (uc/r1-injection lemma forced-word-hc-null): max_k Fq_k / null > 4
for some n >= 10.

Usage: uv run python uc/r1-injection/rw_forced_words.py --min 19 --max 21
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


def null(n: int, k: int) -> float:
    return 2 ** n * (fib(k + 2) + fib(k + 1)) / 2 / 4 ** k


def forced_prefix(source: tuple[int, ...], target: int) -> tuple[int, ...]:
    """Forced symbols up to (not including) the first RW failure."""
    n = len(source)
    state = Endpoint()
    for s in source:
        state.append(s)
    previous = source[-1]
    out: list[int] = []
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
            break
        nxt = Endpoint()
        nxt.column = column + [symbol]
        nxt.diagonal = diagonal
        nxt.length = state.length + 1
        state = nxt
        previous = symbol
        out.append(symbol)
    return tuple(out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min", type=int, default=19)
    parser.add_argument("--max", type=int, default=21)
    args = parser.parse_args()
    print(" n c  D  max Fq/null (k)   N_k(D)  Fq_k(D)   time   deepest forced words x multiplicity")
    for n in range(args.min, args.max + 1):
        for target in (2, 3):
            t0 = time.time()
            kmax = n + 2
            N = [0] * (kmax + 1)
            words: list[dict] = [dict() for _ in range(kmax + 1)]
            for source in product((1, 2), repeat=n):
                q = forced_prefix(source, target)
                for k in range(len(q) + 1):
                    N[k] += 1
                    key = q[:k]
                    words[k][key] = words[k].get(key, 0) + 1
            deepest = max(k for k in range(kmax + 1) if N[k] > 0)
            ratios = [(len(words[k]) / null(n, k), k) for k in range(1, kmax + 1)]
            rF, kF = max(ratios)
            flag = "  KILL forced-word-hc-null" if (n >= 10 and rF > 4) else ""
            listing = "  ".join(
                f"{''.join(map(str, q))}x{m}" for q, m in sorted(words[deepest].items())
            )
            print(
                f"{n:>2} {target} {deepest:>2}   {rF:5.2f} ({kF:>2})      {N[deepest]:>5}  "
                f"{len(words[deepest]):>6}   {time.time() - t0:4.0f}s   {listing}{flag}"
            )
            print("      Fq_k: " + str([len(words[k]) for k in range(1, deepest + 1)])
                  + "   N_k: " + str(N[1:deepest + 1]))
            sys.stdout.flush()


if __name__ == "__main__":
    main()

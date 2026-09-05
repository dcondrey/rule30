#!/usr/bin/env python3
"""Print the full hit table for small n, with column n-1 letter words.

Also counts, per n: distinct full columns n-1 and distinct quotient letter
words of column n-1 across the 2^n binary sources (is W -> q_{n-1} injective?).

Run:  cd <work dir> && uv run python uc/r1-quadratic/qf_smalltable.py
"""

from __future__ import annotations

import argparse
from itertools import product

from qf_common import E, forced_orbit, forward_columns


def letters(col: dict[int, int], lo: int, hi: int) -> str:
    out = []
    for d in range(lo, hi):
        t = col[d]
        out.append({0: "0", 2: "2", 1: "x", 3: "x"}[t])
    return "".join(out)


def cells(col: dict[int, int], lo: int, hi: int) -> str:
    return "".join(str(col[d]) for d in range(lo, hi))


def table(n: int, c: int) -> None:
    eps = E(c)
    print(f"n={n} c={c}  (hit bit = E(T[n+j][n]) XOR E(c); 0 means hit)")
    print("  W        col n-1 cells [-n..n-1]  letters      forced     hits(xor eps)  survive")
    counts = []
    for src in product((1, 2), repeat=n):
        symbols, hits, _ = forced_orbit(src, n + 2)
        cols = forward_columns(src)
        col = cols[n - 1]
        hb = [h ^ eps for h in hits]
        surv = 0
        prev = src[-1]
        for j in range(n + 2):
            if hb[j] != 0:
                break
            if prev == 1 and symbols[j] == 1:
                break
            prev = symbols[j]
            surv += 1
        counts.append(surv)
        print(
            f"  {''.join(map(str, src)):<9}{cells(col, -n, n):<26}{letters(col, -n, n):<13}"
            f"{''.join(map(str, symbols)):<11}{''.join(map(str, hb)):<15}{surv}"
        )
    for k in range(1, n + 3):
        nk = sum(1 for s in counts if s >= k)
        print(f"  N_{k} = {nk}   (2^(n-k) = {2 ** (n - k) if k <= n else 2 ** (n - k):.3g})")


def injectivity(max_n: int) -> None:
    print("injectivity of W -> column n-1 (full cells / quotient letters), window [-n, n-1]")
    for n in range(1, max_n + 1):
        full = set()
        quot = set()
        for src in product((1, 2), repeat=n):
            col = forward_columns(src)[n - 1]
            full.add(cells(col, -n, n))
            quot.add(letters(col, -n, n))
        print(f"  n={n:<3} sources={2**n:<7} distinct full={len(full):<7} distinct letters={len(quot)}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tables", type=int, nargs="*", default=[3, 4])
    ap.add_argument("--max-inj", type=int, default=14)
    args = ap.parse_args()
    for n in args.tables:
        for c in (2, 3):
            table(n, c)
    injectivity(args.max_inj)


if __name__ == "__main__":
    main()

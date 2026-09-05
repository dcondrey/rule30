#!/usr/bin/env python3
"""Print the four-state triangle of the deepest RW witnesses.

For each (n, c) the deepest survivors of the RW search (rw_counts.py, RW
mode) are recomputed and their triangles printed column by column with the
window [-u, n-1] marked, so the structure of long survivors can be inspected
by eye.  Rows are depths (top = depth n, the pinned row), columns are u.

Usage: uv run python uc/r1-injection/rw_witness_triangles.py --n 12 --c 2
"""

from __future__ import annotations

import argparse
import sys
from itertools import product

sys.path.insert(0, ".")
from psi_kernel import Endpoint  # noqa: E402


def run(source: tuple[int, ...], target: int) -> tuple[int, Endpoint, list[int]]:
    """Run the forced orbit while RW holds; return depth, final state, symbols."""
    n = len(source)
    state = Endpoint()
    for s in source:
        state.append(s)
    previous = source[-1]
    depth = 0
    word = list(source)
    for _ in range(n + 2):
        chosen = None
        for symbol in (1, 2):
            column, diagonal = state.peek(symbol)
            if diagonal[n] >> 1 == 1:
                chosen = (symbol, diagonal[n], column, diagonal)
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
        word.append(symbol)
        depth += 1
    return depth, state, word


def triangle(word: list[int]) -> dict[tuple[int, int], int]:
    """Cells T[u][d] of the endpoint word, d in [-u-1, u]."""
    cells: dict[tuple[int, int], int] = {}
    L = len(word)
    for u in range(L):
        cells[(u, -u - 1)] = word[u]
        cells[(u, -u)] = word[u] ^ 3
    from psi_kernel import CONE

    for u in range(L):
        for d in range(-u + 1, u + 1):
            cells[(u, d)] = CONE[cells[(u - 1, d - 1)]][cells[(u, d - 1)]]
    return cells


def show(word: list[int], n: int, depth: int) -> None:
    cells = triangle(word)
    L = len(word)
    print(f"word = {''.join(map(str, word))}  (source {''.join(map(str, word[:n]))}, "
          f"forced {''.join(map(str, word[n:]))}, depth {depth})")
    print("      u: " + "".join(f"{u % 10}" for u in range(L)))
    for d in range(n, -L - 1, -1):
        row = []
        for u in range(L):
            if -u - 1 <= d <= u:
                row.append(str(cells[(u, d)]))
            else:
                row.append(" ")
        mark = " <- pinned row n" if d == n else ""
        print(f"d={d:>4}: " + "".join(row) + mark)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=12)
    parser.add_argument("--c", type=int, default=2)
    parser.add_argument("--top", type=int, default=3)
    args = parser.parse_args()
    n, target = args.n, args.c
    best: list[tuple[int, list[int]]] = []
    for source in product((1, 2), repeat=n):
        depth, _, word = run(source, target)
        best.append((depth, word))
    best.sort(key=lambda t: -t[0])
    top_depth = best[0][0]
    shown = 0
    for depth, word in best:
        if depth < top_depth or shown >= args.top:
            break
        show(word, n, depth)
        print()
        shown += 1
    print(f"n={n} c={target}: {sum(1 for d, _ in best if d == top_depth)} sources reach depth {top_depth}")


if __name__ == "__main__":
    main()

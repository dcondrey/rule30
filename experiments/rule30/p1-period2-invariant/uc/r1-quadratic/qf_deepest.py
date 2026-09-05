#!/usr/bin/env python3
"""Print the deepest RW survivors and their region triangles (cells and letters).

For each (n, c) lists every source reaching the maximal run, the forced
continuation, and the columns n-1 .. n+k of the region as words over
{0,1,2,3} on the window [-(u+1), n], top to bottom printed left to right.

Run:  cd <work dir> && uv run python uc/r1-quadratic/qf_deepest.py --cases 9:3 13:3 14:2 15:2 15:3
"""

from __future__ import annotations

import argparse
from itertools import product

from qf_common import E, Endpoint


def column_word(state: Endpoint, n: int) -> str:
    u = state.length - 1
    cells = []
    for d in range(min(u, n), -(u + 1) - 1, -1):
        cells.append(state.column[-d] if d <= 0 else state.diagonal[d])
    return "".join(map(str, cells))


def deepest(n: int, c: int) -> tuple[int, list[tuple[tuple[int, ...], list[int], list[str]]]]:
    best = -1
    witnesses: list[tuple[tuple[int, ...], list[int], list[str]]] = []

    def walk(state: Endpoint, previous: int, depth: int, symbols: list[int], cols: list[str], src) -> None:
        nonlocal best, witnesses
        if depth > best:
            best = depth
            witnesses = []
        if depth == best:
            witnesses.append((src, list(symbols), list(cols)))
        if depth == n + 2:
            return
        for symbol in (1, 2):
            if previous == 1 and symbol == 1:
                continue
            column, diagonal = state.peek(symbol)
            if diagonal[n] != c:
                continue
            nxt = Endpoint()
            nxt.column = column + [symbol]
            nxt.diagonal = diagonal
            nxt.length = state.length + 1
            walk(nxt, symbol, depth + 1, symbols + [symbol], cols + [column_word(nxt, n)], src)

    for source in product((1, 2), repeat=n):
        state = Endpoint()
        for symbol in source:
            state.append(symbol)
        walk(state, source[-1], 0, [], [column_word(state, n)], source)
    return best, witnesses


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cases", nargs="*", default=["9:3", "13:3", "14:2", "15:2", "15:3"])
    args = ap.parse_args()
    for case in args.cases:
        n, c = map(int, case.split(":"))
        best, wit = deepest(n, c)
        print(f"n={n} c={c} deepest run={best} (need {n+2}); {len(wit)} sources attain it")
        seen = set()
        for src, symbols, cols in wit:
            key = tuple(cols)
            tag = "" if key not in seen else "  (same region as above)"
            seen.add(key)
            print(f"  W={''.join(map(str, src))} forced={''.join(map(str, symbols))}{tag}")
            if tag:
                continue
            for k, w in enumerate(cols):
                u = n - 1 + k
                zeros = w.count("0")
                print(f"     col u={u:<3} depth n..-(u+1): {w:<44} zeros={zeros:<3} e_u={w[-1]}")
        print()


if __name__ == "__main__":
    main()

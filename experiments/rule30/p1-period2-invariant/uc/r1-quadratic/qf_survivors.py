#!/usr/bin/env python3
"""Survivor census in terms of distinct columns, and zero-pattern statistics.

For each (n, c), walk the complete RW search tree (as rw_margin.py does, with
hard-core pruning and the E hit at depth n).  At each level k record:

  N_k   surviving sources (prefixes of length n whose forced orbit has k hits)
  M_k   distinct letter words of column n+k-1 among those survivors
  Z_k   mean number of zero cells in column n+k-1 (window [-(n+k), n-1])
  R_k   mean number of retained positions {h_{n+k} = 1} in that window

Also the collapse ratio M_k / N_k, and the per-step decay of M_k.

Run:  cd <work dir> && uv run python uc/r1-quadratic/qf_survivors.py --max-n 14
"""

from __future__ import annotations

import argparse
import time
from itertools import product

from qf_common import E, Endpoint, a_letter, b_letter


def letters_of(column: list[int], lo_index: int, hi_index: int) -> str:
    # column[i] = T[u][-i]; window d in [lo, hi) maps to indices i = -d
    return "".join("0" if t == 0 else ("2" if t == 2 else "x") for t in column[lo_index:hi_index])


def census(n: int, c: int) -> list[tuple[int, int, float, float]]:
    eps = E(c)
    levels: list[dict] = [dict(N=0, cols=set(), zeros=0, retained=0) for _ in range(n + 3)]

    def record(k: int, state: Endpoint) -> None:
        # column u = n+k-1 is state.column (index i <-> depth -i) plus state.diagonal
        u = state.length - 1
        # window [-(u+1), n-1] = whole column below depth n
        cells = []
        for d in range(-(u + 1), n):
            cells.append(state.column[-d] if d <= 0 else state.diagonal[d])
        word = "".join("0" if t == 0 else ("2" if t == 2 else "x") for t in cells)
        lv = levels[k]
        lv["N"] += 1
        lv["cols"].add(word)
        lv["zeros"] += sum(1 for t in cells if t == 0)
        # retained set for column u+1: h_{u+1}(d) = 1 + N[d, n) (nonzero count above)
        nz = 0
        ret = 0
        for d in range(n - 1, -(u + 1) - 1, -1):
            t = cells[d + u + 1]
            if t != 0:
                nz ^= 1
            if (1 + nz) & 1 == 1:
                ret += 1
        lv["retained"] += ret

    def walk(state: Endpoint, previous: int, depth: int) -> None:
        record(depth, state)
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
            walk(nxt, symbol, depth + 1)

    for source in product((1, 2), repeat=n):
        state = Endpoint()
        for symbol in source:
            state.append(symbol)
        walk(state, source[-1], 0)

    out = []
    for k in range(n + 3):
        lv = levels[k]
        if lv["N"] == 0:
            out.append((0, 0, 0.0, 0.0))
        else:
            out.append((lv["N"], len(lv["cols"]), lv["zeros"] / lv["N"], lv["retained"] / lv["N"]))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-n", type=int, default=6)
    ap.add_argument("--max-n", type=int, default=14)
    args = ap.parse_args()
    for n in range(args.min_n, args.max_n + 1):
        for c in (2, 3):
            t0 = time.time()
            rows = census(n, c)
            print(f"n={n} c={c}   [{time.time()-t0:.1f}s]")
            print("   k    N_k     M_k   M_k/N_k   log2(N_k-1/N_k)  log2(M_k-1/M_k)   zeros/col  retained/window")
            for k, (N, M, z, r) in enumerate(rows):
                if N == 0:
                    print(f"  {k:>2}  {0:>6}  {0:>6}")
                    continue
                dn = f"{__import__('math').log2(rows[k-1][0] / N):.2f}" if k > 0 and rows[k-1][0] else "   "
                dm = f"{__import__('math').log2(rows[k-1][1] / M):.2f}" if k > 0 and rows[k-1][1] else "   "
                print(f"  {k:>2}  {N:>6}  {M:>6}   {M/N:.3f}        {dn:>5}            {dm:>5}       {z:6.2f}      {r:6.2f} / {n + n + k}")


if __name__ == "__main__":
    main()

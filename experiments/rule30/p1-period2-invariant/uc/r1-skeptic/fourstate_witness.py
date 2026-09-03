#!/usr/bin/env python3
"""Print the four-state forced path of given prefixes (pure Python, psi_kernel).

For each prefix W and target c: at each column u >= n choose the unique
four-state symbol e_u with T[u][n] = c (psi_kernel Endpoint.peek over all four
symbols), append it, and report the symbol word, which symbols are non-binary,
and the hard-core violations among binary symbols.  Used to display the v=1
near-misses found by fourstate_nearmiss.py.

Run:  cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/fourstate_witness.py --n 21 --c 3
"""
from __future__ import annotations

import argparse
import os
import sys
from itertools import product

KERNEL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, KERNEL_DIR)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from psi_kernel import Endpoint  # noqa: E402
from quotient_multiplicity import quotient_column  # noqa: E402


def fourstate_path(word: str, c: int, K: int):
    n = len(word)
    ep = Endpoint()
    for ch in word:
        ep.append(int(ch))
    forced = []
    for j in range(K):
        chosen = [s for s in range(4) if ep.peek(s)[1][n] == c]
        assert len(chosen) == 1, chosen
        forced.append(chosen[0])
        ep.append(chosen[0])
    return forced


def violations(word: str, forced: list[int]) -> list[str]:
    out = []
    prev = int(word[-1])
    for j, s in enumerate(forced):
        if s in (0, 3):
            out.append(f"col n+{j}: non-binary symbol {s}")
        elif s == 1 and prev == 1:
            out.append(f"col n+{j}: hard-core 11")
        prev = s
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, default=21)
    ap.add_argument("--c", type=int, default=3)
    ap.add_argument("--max-viol", type=int, default=1)
    args = ap.parse_args()
    n, c = args.n, args.c
    K = n + 2
    found = 0
    states = set()
    for w in product("12", repeat=n):
        word = "".join(w)
        forced = fourstate_path(word, c, K)
        v = violations(word, forced)
        if len(v) <= args.max_viol:
            found += 1
            q = quotient_column(word)
            states.add(q)
            fw = "".join(map(str, forced))
            ending = fw[n - 1 : n + 1]
            print(f"W={word} forced={fw} ending(e_2n-1,e_2n)={ending} violations={v}")
    print(f"n={n} c={c}: {found} prefixes with <= {args.max_viol} violations over {K} columns, {len(states)} distinct states")


if __name__ == "__main__":
    main()

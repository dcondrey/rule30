#!/usr/bin/env python3
"""How many distinct forced futures do the 2^n binary prefixes actually start?

Fact used (BRIEF section 2): column u is a function of the quotient letters
(a, b) = ([T==0], [Lo(T)==0]) of column u-1 plus H(e_u); cells 1 and 3 share
the letter (0,0).  For u >= n the symbol e_u is forced and only T[u][n] is
read, which needs column u-1 on depths [-u, n-1] only.  Hence the whole RW
future of a prefix W (forced symbols, E word, run, 12a ending) is a function of

    q(W) = quotient of column n-1 restricted to depths [-n, n-1].

This script measures the fiber structure of W -> q(W): the number Q_n of
distinct reachable q, the multiplicity distribution, and whether the deepest
RW witnesses (and the recorded n=15 BWH+ extremal set) are single fibers.

Run:  cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/quotient_multiplicity.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from itertools import product

KERNEL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, KERNEL_DIR)
HERE = os.path.dirname(os.path.abspath(__file__))

from psi_kernel import Endpoint  # noqa: E402

QUOT = {0: "Z", 1: "N", 2: "T", 3: "N"}  # zero, nonzero-with-Lo=1 (1 or 3), two


def quotient_column(word: str) -> str:
    """q(W): quotient of column n-1 on depths [-n, n-1], as a string."""
    ep = Endpoint()
    for ch in word:
        ep.append(int(ch))
    n = len(word)
    # psi_kernel: column[k] = T[n-1][-k] for k = 0..n-1, column[n] = e_{n-1} (depth -n);
    # diagonal[i] = T[n-1][i] for i = 0..n-1.
    cells = [ep.column[-d] for d in range(-n, 0)] + [ep.diagonal[i] for i in range(0, n)]
    assert len(cells) == 2 * n
    return "".join(QUOT[x] for x in cells)


def fibers(n: int) -> dict[str, list[str]]:
    fib = defaultdict(list)
    for w in product("12", repeat=n):
        word = "".join(w)
        fib[quotient_column(word)].append(word)
    return fib


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-n", type=int, default=16)
    args = ap.parse_args()
    print("n   2^n      Q_n     Q_n/2^n   max fiber   fiber-size histogram (size:count)")
    for n in range(4, args.max_n + 1):
        fib = fibers(n)
        sizes = Counter(len(v) for v in fib.values())
        mx = max(sizes)
        hist = " ".join(f"{s}:{sizes[s]}" for s in sorted(sizes))
        print(f"{n:<4}{2**n:<9}{len(fib):<8}{len(fib)/2**n:<10.4f}{mx:<12}{hist}")
        sys.stdout.flush()
    # e_0 flip test: how often does flipping e_0 leave q unchanged?
    print("\ne_0 flip: fraction of W with q(W) == q(W with e_0 flipped)")
    for n in range(4, args.max_n + 1):
        same = 0
        total = 0
        for w in product("12", repeat=n - 1):
            a = "1" + "".join(w)
            b = "2" + "".join(w)
            total += 1
            if quotient_column(a) == quotient_column(b):
                same += 1
        print(f"n={n:<3} same={same}/{total} = {same/total:.4f}")
    # the recorded n=15 BWH+ extremal set: suffix 211212112, all 64 prefixes
    print("\nn=15 BWH+ extremal suffix 211212112: distinct q over the 64 six-symbol prefixes")
    groups = defaultdict(list)
    for p in product("12", repeat=6):
        word = "".join(p) + "211212112"
        groups[quotient_column(word)].append("".join(p))
    for q, ps in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        print(f"  fiber size {len(ps):<3} prefixes {' '.join(ps)}")
    # deepest RW witnesses from the census JSON, if present
    for fname in ("census_n07_20.json", "census_n21_30.json"):
        path = os.path.join(HERE, fname)
        if not os.path.exists(path):
            continue
        data = json.load(open(path))
        print(f"\nDeepest RW witnesses in {fname}: distinct q per witness set")
        for key, e in sorted(data.items(), key=lambda kv: (kv[1]["n"], kv[1]["c"])):
            n, c = e["n"], e["c"]
            if n > 24:
                continue
            k = str(e["deepest"])
            ws = e["witnesses"].get(k, [])
            qs = Counter(quotient_column(w) for w in ws)
            print(f"  n={n:<3} c={c} deepest={k:<3} witnesses={len(ws):<4} distinct q={len(qs):<3} fiber sizes={sorted(qs.values(), reverse=True)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Ablate the hard-core condition from RW to see which condition carries the slack.

RW pins the full Moore state (H=1, E=E(c)) at depth n AND requires the forced
continuation to be hard-core (no 11).  Dropping hard-core leaves exactly the
BWH+ statement, so this ablation doubles as a gate: the no-hard-core column must
reproduce BWH+'s known exceptions (a constant at n=6, the n+1 near-miss at
n=15, c=3).  It does.
"""
from __future__ import annotations
import argparse
from itertools import product
from psi_kernel import Endpoint


def deepest(n: int, c: int, hardcore: bool) -> tuple[int, str, list[int]]:
    best = 0
    witness = ""
    counts = [0] * (3 * n)

    def walk(state: Endpoint, prev: int, word: list[int], depth: int) -> None:
        nonlocal best, witness
        counts[depth] += 1
        if depth > best:
            best, witness = depth, "".join(map(str, word))
        if depth >= 2 * n + 2:
            return
        for s in (1, 2):
            if hardcore and prev == 1 and s == 1:
                continue
            col, dia = state.peek(s)
            if dia[n] != c:
                continue
            nxt = Endpoint()
            nxt.column, nxt.diagonal, nxt.length = col + [s], dia, state.length + 1
            walk(nxt, s, word + [s], depth + 1)

    for src in product((1, 2), repeat=n):
        st = Endpoint()
        for s in src:
            st.append(s)
        walk(st, src[-1], list(src), 0)
    return best, witness, counts


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--min-source", type=int, default=6)
    p.add_argument("--max-source", type=int, default=16)
    a = p.parse_args()
    print(" n  c   deepest(HC)  deepest(noHC)  need   slack(noHC)")
    for n in range(a.min_source, a.max_source + 1):
        for c in (2, 3):
            bh, _, _ = deepest(n, c, True)
            bn, _, _ = deepest(n, c, False)
            print(f"{n:<3}{c:<4}{bh:<13}{bn:<15}{n+2:<7}{n+2-bn}", flush=True)


if __name__ == "__main__":
    main()

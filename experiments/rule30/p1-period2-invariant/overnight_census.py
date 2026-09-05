#!/usr/bin/env python3
"""Single-pass census for PREREGISTRATION-OVERNIGHT-EXTENSION.md.

For one (n, tail): walks every source word once and computes, from the same
forced continuation, all of:
  - |H_r(n)| for r = 0,1,2   (survival through n+r+2 rows AND terminal pull)
  - D_k  = distinct surviving continuation prefixes at depth k
  - S_k  = source words surviving k rows (with multiplicity)
  - max survival row, and the extinction margin (n+2) - max_survival_row

Memory-light by design: keeps only prefix sets (thousands of tuples) and
counters; never stores per-word continuations. Prints incrementally and
flushes, so a killed run still leaves usable partial output.
"""
from __future__ import annotations

import argparse
import sys
import time
from itertools import product

from late_pull_diagonal_sat import literal_extension


def legal(prev: int, v: int) -> bool:
    return v in (1, 2) and not (prev == 1 and v == 1)


def check_prefix_property(tail: int) -> None:
    """Control: literal_extension(W,c,L) must be a prefix of the L'>L version."""
    for n in (4, 5, 6):
        for word in product((1, 2), repeat=n):
            short = literal_extension(word, tail, n + 2)
            long_ = literal_extension(word, tail, n + 4)
            assert tuple(long_[: len(short)]) == tuple(short), (word, short, long_)
    print(f"# control OK: literal_extension is prefix-consistent (tail={tail})",
          flush=True)


def run(n: int, tail: int) -> dict:
    rows = n + 4
    sets: list[set] = [set() for _ in range(rows + 2)]
    S = [0] * (rows + 2)
    H = {0: 0, 1: 0, 2: 0}
    max_row = 0
    t0 = time.time()

    for word in product((1, 2), repeat=n):
        cont = literal_extension(word, tail, rows)
        prev = word[-1]
        pref = [prev]
        sets[0].add((prev,))
        S[0] += 1
        k = 0
        for v in cont:
            if not legal(prev, v):
                break
            pref.append(v)
            prev = v
            k += 1
            sets[k].add(tuple(pref))
            S[k] += 1
        if k > max_row:
            max_row = k
        # H_r: needs survival through exactly n+r+2 rows plus terminal pull
        for r in (0, 1, 2):
            need = n + r + 2
            if k >= need and tuple(cont[need - 3:need - 1]) == (1, 2):
                H[r] += 1

    D = [len(s) for s in sets]
    last = max(i for i in range(len(D)) if D[i] > 0)
    return {
        "n": n, "tail": tail,
        "D": D[: last + 2],
        "S": S[: last + 2],
        "H": H,
        "max_row": max_row,
        "margin": (n + 2) - max_row,
        "secs": round(time.time() - t0, 1),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tail", type=int, required=True)
    ap.add_argument("--ns", type=int, nargs="+", required=True)
    ap.add_argument("--skip-control", action="store_true")
    args = ap.parse_args()

    if not args.skip_control:
        check_prefix_property(args.tail)
        # regression: n=16 c=2 must reproduce the committed D array
        if args.tail == 2:
            r16 = run(16, 2)
            expect = [2, 3, 5, 8, 13, 21, 27, 20, 6, 3, 1, 0]
            ok = r16["D"][: len(expect)] == expect
            print(f"# regression n=16 c=2: D={r16['D'][:len(expect)]} "
                  f"MATCH={ok}", flush=True)
            if not ok:
                print("# ABORT: n=16 regression failed", flush=True)
                sys.exit(1)

    for n in args.ns:
        r = run(n, args.tail)
        print(f"RESULT n={r['n']} c={r['tail']} "
              f"H0={r['H'][0]} H1={r['H'][1]} H2={r['H'][2]} "
              f"max_row={r['max_row']} margin={r['margin']} "
              f"secs={r['secs']}", flush=True)
        print(f"   D={r['D']}", flush=True)
        print(f"   S={r['S']}", flush=True)


if __name__ == "__main__":
    main()

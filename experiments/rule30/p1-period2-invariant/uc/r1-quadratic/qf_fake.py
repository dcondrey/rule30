#!/usr/bin/env python3
"""Count letter words of column n-1 whose region alone satisfies every RW condition.

A letter word is any q in {0, 2, x}^(2n) on the window d in [-n, n-1]
(x stands for an odd cell; the region only reads the quotient letters).  The
region u >= n is built with the top row pinned at c.  The word is a FAKE
COUNTEREXAMPLE if all n+2 forced symbols e_n .. e_{2n+1} are binary
(E = 0), hard-core including the junction with e_{n-1} = q[0] (which must
then be odd, i.e. an x read as 1, or 2), and f[-3:-1] = 12.  Reachability
from a binary source is tested against the exact set of reachable columns.

Early exit at the first failing column makes n = 7 feasible in Python.

Run:  cd <work dir> && uv run python uc/r1-quadratic/qf_fake.py --n 5 6 7
"""
from __future__ import annotations
import argparse, time
from itertools import product
from qf_common import E, forward_columns, psi


def fake_count(n: int, c: int) -> tuple[int, int, int, list]:
    reach = set()
    for src in product((1, 2), repeat=n):
        col = forward_columns(src)[n - 1]
        reach.add(tuple({0: 0, 2: 2, 1: 1, 3: 1}[col[d]] for d in range(-n, n)))
    total_hits = 0      # all n+2 hits (no hard-core, no 12a)
    total_hc = 0        # plus hard-core
    total_12a = 0       # plus 12a
    reachable = 0
    examples = []
    for word in product((0, 1, 2), repeat=2 * n):
        prev = {(-n + i): t for i, t in enumerate(word)}
        prev_sym = word[0]           # e_{n-1}: 0 impossible for reachable, x read as 1
        symbols = []
        ok_hits = True
        ok_hc = True
        for u in range(n, 2 * n + 2):
            col = {n: c}
            for d in range(n - 1, -u - 2, -1):
                left = prev[d] if d in prev else 3
                col[d] = psi(left, col[d + 1])
            e = col[-u - 1]
            if E(e) != 0:
                ok_hits = False
                break
            if prev_sym == 1 and e == 1:
                ok_hc = False
            prev_sym = e
            symbols.append(e)
            prev = col
        if not ok_hits:
            continue
        total_hits += 1
        if not ok_hc:
            continue
        total_hc += 1
        if not (symbols[-3] == 1 and symbols[-2] == 2):
            continue
        total_12a += 1
        if word in reach:
            reachable += 1
        if len(examples) < 2:
            examples.append((word, symbols))
    return total_hits, total_hc, total_12a, reachable, examples


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, nargs="*", default=[5, 6, 7])
    args = ap.parse_args()
    for n in args.n:
        for c in (2, 3):
            t0 = time.time()
            th, thc, t12, r, ex = fake_count(n, c)
            print(f"n={n} c={c}: words={3**(2*n)}  all {n+2} hits: {th}  +hard-core: {thc}  +12a: {t12}  reachable among +12a: {r}   [{time.time()-t0:.0f}s]")
            for word, symbols in ex:
                print(f"    col n-1 (d=-n..n-1) = {''.join(map(str, word))}   forced e_n..e_2n+1 = {''.join(map(str, symbols))}")
            print(flush=True)

if __name__ == "__main__":
    main()

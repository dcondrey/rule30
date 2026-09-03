#!/usr/bin/env python3
"""Tails of the forced symbol strings of region-only survivors (letter space).

For every letter word q of column n-1 whose region has all n+2 hits with
hard-core forced symbols, tabulate (i) the last three forced symbols
e_{2n-1} e_{2n} e_{2n+1}, (ii) the full forced string counts, (iii) the
number of 1's among forced symbols.  Purpose: explain why the +12a count is
0 at n = 5, 7 but positive at n = 6 (qf_fake.log).

Run:  cd <work dir> && uv run python uc/r1-quadratic/qf_fake_tails.py --n 4 5 6 7
"""
from __future__ import annotations
import argparse, time
from collections import Counter
from itertools import product
from qf_common import E, psi


def survivors(n: int, c: int):
    for word in product((0, 1, 2), repeat=2 * n):
        prev = {(-n + i): t for i, t in enumerate(word)}
        prev_sym = word[0]
        symbols = []
        ok = True
        for u in range(n, 2 * n + 2):
            col = {n: c}
            for d in range(n - 1, -u - 2, -1):
                left = prev[d] if d in prev else 3
                col[d] = psi(left, col[d + 1])
            e = col[-u - 1]
            if E(e) != 0 or (prev_sym == 1 and e == 1):
                ok = False
                break
            prev_sym = e
            symbols.append(e)
            prev = col
        if ok:
            yield word, tuple(symbols)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, nargs="*", default=[4, 5, 6, 7])
    args = ap.parse_args()
    for n in args.n:
        for c in (2, 3):
            t0 = time.time()
            tails = Counter()
            strings = Counter()
            ones = Counter()
            total = 0
            for word, symbols in survivors(n, c):
                total += 1
                tails["".join(map(str, symbols[-3:]))] += 1
                strings["".join(map(str, symbols))] += 1
                ones[symbols.count(1)] += 1
            print(f"n={n} c={c}: region-only survivors (hits+hard-core) = {total}   [{time.time()-t0:.0f}s]")
            print(f"   last-three tails: {dict(sorted(tails.items()))}")
            print(f"   number of 1s among forced symbols: {dict(sorted(ones.items()))}")
            print(f"   distinct forced strings: {len(strings)}; most common: {strings.most_common(6)}", flush=True)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Region-only RW solutions with a LEGAL bottom cell q[0] in {1, 2} (= e_{n-1}).

Same as qf_fake.py but restricted to letter words whose bottom cell (depth
-n, which is the endpoint symbol e_{n-1} itself) is 1 or 2, as any reachable
column must have.  Reports counts with all hits + hard-core, and + 12a.

Run:  cd <work dir> && uv run python uc/r1-quadratic/qf_fake_legal.py --n 5 6 7
"""
from __future__ import annotations
import argparse, time
from itertools import product
from qf_common import E, psi

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, nargs="*", default=[5, 6])
    args = ap.parse_args()
    for n in args.n:
        for c in (2, 3):
            t0 = time.time()
            hc = 0; t12 = 0; ex = []
            for rest in product((0, 1, 2), repeat=2 * n - 1):
                for first in (1, 2):
                    word = (first,) + rest
                    prev = {(-n + i): t for i, t in enumerate(word)}
                    prev_sym = first
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
                    if not ok:
                        continue
                    hc += 1
                    if symbols[-3] == 1 and symbols[-2] == 2:
                        t12 += 1
                        if len(ex) < 2:
                            ex.append((word, symbols))
            print(f"n={n} c={c}: legal-bottom words with all {n+2} hits + hard-core: {hc}; + 12a: {t12}   [{time.time()-t0:.0f}s]")
            for word, symbols in ex:
                print(f"    col n-1 (d=-n..n-1) = {''.join(map(str, word))}   forced = {''.join(map(str, symbols))}")
            print(flush=True)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Random-source run of the zero-pattern gate (G1..G4 of q2_gate.py) at larger n.

For each n in the list, draw `samples` uniformly random binary sources, run
the forced orbit n+2 steps for both c, and check on every column u = n..2n+1:
  (G1) H(T[u][d]) = 1 exactly at even-indexed nonzero cells of column u-1
       (from the top) and at zeros whose nearest nonzero above is even-indexed
       or absent;
  (G2) e_u = 2 iff the number of nonzero cells of column u-1 in [-u, n-1] is odd;
  (G3) E(T[u][n]) = #{retained zeros} + #{even-indexed nonzero cells equal to 2} (mod 2);
  (G4) (Z_{u-1}, Z_u) -> column u is single valued across all samples.
A failure prints the offending source and aborts.

Run:  cd <work dir> && uv run python uc/r1-quadratic/q2_gate_random.py --n 18 22 26 --samples 1500
"""
from __future__ import annotations

import argparse
import random
import time

from qf_common import E, H, forced_orbit, forward_columns


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, nargs="*", default=[18, 22, 26])
    ap.add_argument("--samples", type=int, default=1500)
    ap.add_argument("--seed", type=int, default=20260903)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    for n in args.n:
        t0 = time.time()
        pair_to_col: dict = {}
        cols_checked = 0
        for _ in range(args.samples):
            src = tuple(rng.choice((1, 2)) for _ in range(n))
            for c in (2, 3):
                symbols, hits, cells = forced_orbit(src, n + 2)
                word = src + tuple(symbols)
                cols = forward_columns(word)
                for j in range(n + 2):
                    u = n + j
                    prev, cur = cols[u - 1], cols[u]
                    qs = [d for d in range(n - 1, -u - 1, -1) if prev[d] != 0]
                    status = {}
                    for i, d in enumerate(qs, start=1):
                        status[d] = 1 if i % 2 == 0 else 0
                    above = 1
                    for d in range(n - 1, -u - 1, -1):
                        if prev[d] != 0:
                            above = status[d]
                        else:
                            status[d] = above
                    for d in range(-u, n):
                        assert H(cur[d]) == status[d], ("G1", n, c, src, j, d)
                    assert (word[u] == 2) == (len(qs) % 2 == 1), ("G2", n, c, src, j)
                    ret_zero = sum(1 for d in range(-u, n) if prev[d] == 0 and status[d] == 1)
                    ret_two = sum(1 for i, d in enumerate(qs, start=1) if i % 2 == 0 and prev[d] == 2)
                    assert ((ret_zero + ret_two) & 1) == E(cur[n]) == E(cells[j]), ("G3", n, c, src, j)
                    Zp = tuple(d for d in range(-u, n) if prev[d] == 0)
                    Zc = tuple(d for d in range(-u - 1, n) if cur[d] == 0)
                    colkey = tuple(cur[d] for d in range(-u - 1, n + 1))
                    assert pair_to_col.setdefault((n, c, u, Zp, Zc), colkey) == colkey, ("G4", n, c, src, j)
                    cols_checked += 1
        print(f"n={n}: {args.samples} random sources x 2 targets, {cols_checked} columns: G1..G4 PASS; "
              f"{len(pair_to_col)} distinct zero-pattern pairs   [{time.time()-t0:.0f}s]", flush=True)


if __name__ == "__main__":
    main()

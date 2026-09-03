#!/usr/bin/env python3
"""Gate for the retained-parity form of the RW hit and the reduced-state bijection.

Claims checked on every binary source W in {1,2}^n, n <= max_n, along the
forced orbit (columns u = n .. 2n+1, window d in [-u, n-1] of column u-1):

  (R1) R_u := {d : #{d' in [d, n) : T[u-1][d'] != 0} is even} equals
       {d : H(T[u][d]) = 1}, the positions where column u has h = 1;
  (R2) hit_u  <=>  E(c) + sum_{d in R_u} [T[u-1][d] even]  == 0  (mod 2);
  (R3) H(e_u) = 1 iff -u is NOT in R_u  (so e_u = 1 iff the bottom position
       is retained), and hard-core at (u-1, u) <=> not (-u in R_u and
       T[u-1][-u] odd), since T[u-1][-u] = e_{u-1} and e_{u-1} = 1 is odd;
  (R4) on reachable pairs, column u on [-u-1, n] and the pair
       (a_{u-1} on the window, b_{u-1} restricted to R_u) determine each other.

Run:  cd <work dir> && uv run python uc/r1-quadratic/qf_retained.py --max-n 9
"""
from __future__ import annotations
import argparse
from itertools import product
from qf_common import E, H, forced_orbit, forward_columns


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-n", type=int, default=9)
    args = ap.parse_args()
    checks = 0
    pairs_forward: dict = {}
    pairs_backward: dict = {}
    for n in range(1, args.max_n + 1):
        for c in (2, 3):
            eps = E(c)
            for src in product((1, 2), repeat=n):
                symbols, hits, cells = forced_orbit(src, n + 2)
                word = tuple(src) + tuple(symbols)
                cols = forward_columns(word)
                for j in range(n + 2):
                    u = n + j
                    prev, cur = cols[u - 1], cols[u]
                    # retained set from nonzero counts
                    R = set()
                    nz = 0
                    for d in range(n - 1, -u - 1, -1):
                        if prev[d] != 0:
                            nz ^= 1
                        if nz == 0:
                            R.add(d)
                    # (R1)
                    for d in range(-u, n):
                        assert (d in R) == (H(cur[d]) == 1), ("R1", src, c, j, d)
                    # (R2)
                    par = eps
                    for d in R:
                        par ^= 1 - (prev[d] & 1)
                    assert (hits[j] == eps) == (par == 0), ("R2", src, c, j)
                    # (R3)
                    e_u = word[u]
                    assert (H(e_u) == 1) == (-u not in R), ("R3a", src, c, j)
                    junction_ok = not (word[u - 1] == 1 and e_u == 1)
                    assert junction_ok == (not (-u in R and prev[-u] % 2 == 1)), ("R3b", src, c, j)
                    # (R4)
                    a = tuple(1 if prev[d] == 0 else 0 for d in range(-u, n))
                    beta = tuple((d, 1 - (prev[d] & 1)) for d in sorted(R))
                    key = (n, c, u, a, beta)
                    colkey = (n, c, u, tuple(cur[d] for d in range(-u - 1, n + 1)))
                    assert pairs_forward.setdefault(key, colkey) == colkey, ("R4f", key)
                    assert pairs_backward.setdefault(colkey, key) == key, ("R4b", colkey)
                    checks += 1
    print(f"retained-parity gate: {checks} column steps PASS (R1..R4), n <= {args.max_n}, c in {{2,3}}")
    print(f"distinct reduced states (a, beta) seen: {len(pairs_forward)}; distinct columns: {len(pairs_backward)}")

if __name__ == "__main__":
    main()

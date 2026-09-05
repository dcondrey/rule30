#!/usr/bin/env python3
"""Kill test and sharpening of the constant-run synchronization law.

Law (from absorption_scaling.log Part B): for every m >= 1, all 2^m binary
prefixes p followed by 2^(3m) give ONE full column at index 4m-1, and 3m is
minimal.  With 1^(3m+1) likewise at index 4m.

(1) Kill test to m = MMAX: distinct full columns of p . 2^(3m) at index 4m-1
    (must be 1) and at index 4m-2 (must be > 1 for minimality).
(2) Partial erasure: for prefix length M and run length L = 0..3M, the number
    of distinct full columns of p . 2^L at index M+L-1, against the candidate
    2^(M - floor(L/3)) (a run of L twos erases exactly the earliest floor(L/3)
    prefix symbols) and against 2^(M - ceil(L/3)).
(3) Four-state prefixes: does 2^(3m) also erase prefixes over {0,1,2,3}?
"""
from __future__ import annotations

import sys
from itertools import product
from math import log2

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
from psi_kernel import Endpoint  # noqa: E402


def full_column(endpoint) -> bytes:
    st = Endpoint()
    for e in endpoint:
        st.append(e)
    # depths -u-1..u : column[i] = T[u][-i] (i = 0..u+1), diagonal[k] = T[u][k]
    return bytes(list(reversed(st.column)) + list(st.diagonal[1:]))


def distinct(prefix_alphabet, M: int, tail) -> int:
    seen = set()
    for p in product(prefix_alphabet, repeat=M):
        seen.add(full_column(p + tail))
    return len(seen)


def main() -> None:
    MMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    print("(1) kill test: distinct columns of p.2^(3m) at index 4m-1 (want 1) and 4m-2 (want >1); p.1^(3m+1) at 4m (want 1), 4m-1 (want >1)")
    for m in range(1, MMAX + 1):
        a = distinct((1, 2), m, (2,) * (3 * m))
        b = distinct((1, 2), m, (2,) * (3 * m - 1))
        c = distinct((1, 2), m, (1,) * (3 * m + 1))
        d = distinct((1, 2), m, (1,) * (3 * m))
        print(f"  m={m:2d}: 2-run: at 4m-1 -> {a} distinct, at 4m-2 -> {b};   1-run: at 4m -> {c}, at 4m-1 -> {d}   {'OK' if a == 1 and b > 1 and c == 1 and d > 1 else 'VIOLATION'}")
    print("\n(2) partial erasure: distinct columns of p.2^L, prefix length M, vs 2^(M-floor(L/3)) and 2^(M-ceil(L/3))")
    for M in (4, 6, 8):
        row = []
        for L in range(0, 3 * M + 1):
            n = distinct((1, 2), M, (2,) * L)
            row.append(f"L={L}:{n}(2^{log2(n):.2f})")
        print(f"  M={M}: " + " ".join(row))
        print(f"        floor law 2^(M-floor(L/3)): " + " ".join(f"L={L}:{2**(M-L//3)}" for L in range(0, 3*M+1)))
    print("\n(3) four-state prefixes over {0,1,2,3}: distinct columns of p.2^L at the end, L = 3m and the least L giving 1")
    for m in range(1, 6):
        least = None
        for L in range(1, 8 * m + 1):
            if distinct(range(4), m, (2,) * L) == 1:
                least = L
                break
        print(f"  m={m}: least L with one column = {least}  (binary law: {3*m})")


if __name__ == "__main__":
    main()

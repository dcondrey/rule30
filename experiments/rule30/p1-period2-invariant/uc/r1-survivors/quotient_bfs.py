#!/usr/bin/env python3
"""Kill test for the quotient-collapse lemma: class-level BFS to large u.

Level u holds the distinct quotient words of column u (depths -u-1..u, top
included) with source multiplicities.  Children are computed from the parent
quotient alone (BRIEF section 2), so the cost per level is O(N_q(u) * u), not
O(2^u * u).  Prints N_q(u), log2 N_q(u) and the increment per level.  The
lemma under test: increment <= 0.85 for all u >= 8.  A failure is any printed
increment above 0.85 (or a rising trend back toward 1).
"""
from __future__ import annotations

import sys
import time
from math import log2
from collections import defaultdict

AB = {0: (0, 0), 1: (0, 1), 2: (1, 1)}


def child(key: bytes, e: int) -> bytes:
    """Quotient of column u+1 (depths -u-2..u+1) from the quotient of column u (depths -u-1..u)."""
    He = e >> 1
    h, F = 1 - He, 0
    out = bytearray(len(key) + 2)
    out[0] = 0 if e == 1 else 1
    idx = 1
    for code in key:
        out[idx] = 2 if (h == 0 and F == 1) else (1 if h != F else 0)
        idx += 1
        a, b = AB[code]
        h, F = h ^ 1 ^ a, F ^ (h & b)
    out[idx] = 2 if (h == 0 and F == 1) else (1 if h != F else 0)
    return bytes(out)


def main() -> None:
    UMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    level: dict[bytes, int] = {bytes([0, 1]): 1, bytes([1, 0]): 1}  # column 0: e=1 -> cells (1,2) letters (0,1); e=2 -> (2,1) letters (1,0)
    prev = None
    print("u  n=u+1  N_q(u)   log2   increment   2^n/N_q   elapsed_s")
    t0 = time.time()
    for u in range(0, UMAX + 1):
        N = len(level)
        lg = log2(N)
        inc = "" if prev is None else f"{lg - prev:.4f}"
        prev = lg
        print(f"{u:2d} {u+1:3d} {N:9d} {lg:8.4f} {inc:>9} {2**(u+1)/N:8.3f} {time.time()-t0:8.1f}", flush=True)
        if u == UMAX:
            break
        nxt: dict[bytes, int] = defaultdict(int)
        for key, m in level.items():
            nxt[child(key, 1)] += m
            nxt[child(key, 2)] += m
        level = nxt


if __name__ == "__main__":
    main()

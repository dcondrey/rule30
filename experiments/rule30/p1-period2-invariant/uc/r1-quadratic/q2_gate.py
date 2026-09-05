#!/usr/bin/env python3
"""Gate for the zero-pattern description of the forced orbit.

All claims are checked on every binary source W in {1,2}^n, n <= max_n,
c in {2,3}, along the forced orbit columns u = n .. 2n+1 (column u-1 read on
the window d in [-u, n-1]; the endpoint symbol e_{u-1} sits at d = -u).

  (G1) retained-run structure.  Let q_1 > q_2 > ... be the depths of the
       nonzero cells of column u-1 in the window, from the top.  Then
       H(T[u][q_i]) = 1 iff i is even; a zero cell has the same H(T[u][.])
       as the nearest nonzero cell above it, and H = 1 if there is none.
  (G2) forced symbol: e_u = 2 iff the number of nonzero cells in the window
       is odd.
  (G3) top read-out: E(T[u][n]) = [T[u][q_1] == 0] + #{zeros of column u-1
       above q_1}  (mod 2).
  (G4) the pair of zero patterns (Z_{u-1}, Z_u) determines column u on
       [-u-1, n], hence the whole forced future; Z_{u-1} alone does not
       (count the collisions).
  (G5) letter-space balance: #{q in {0,2,x}^m : Phi(q) = 0} for m <= 10 by
       brute force, and the same number from the D8 transfer matrix for
       m <= 40.  Phi is evaluated with the forced start h0 = 1 + |N| (mod 2)
       so that the final h is 1.

Run:  cd <work dir> && uv run python uc/r1-quadratic/q2_gate.py --max-n 9
"""
from __future__ import annotations

import argparse
import time
from itertools import product

from qf_common import E, H, forced_orbit, forward_columns


def window_cells(col: dict[int, int], lo: int, hi: int) -> list[tuple[int, int]]:
    return [(d, col[d]) for d in range(lo, hi)]


def check_orbits(max_n: int) -> None:
    g1 = g2 = g3 = g4 = 0
    pair_to_col: dict = {}
    single_to_cols: dict = {}
    for n in range(1, max_n + 1):
        for c in (2, 3):
            for src in product((1, 2), repeat=n):
                symbols, hits, cells = forced_orbit(src, n + 2)
                word = tuple(src) + tuple(symbols)
                cols = forward_columns(word)
                for j in range(n + 2):
                    u = n + j
                    prev, cur = cols[u - 1], cols[u]
                    # nonzero cells from the top
                    qs = [d for d in range(n - 1, -u - 1, -1) if prev[d] != 0]
                    status = {}
                    for i, d in enumerate(qs, start=1):
                        status[d] = 1 if i % 2 == 0 else 0
                    # zeros copy the status of the nearest nonzero above
                    above = 1
                    for d in range(n - 1, -u - 1, -1):
                        if prev[d] != 0:
                            above = status[d]
                        else:
                            status[d] = above
                    for d in range(-u, n):
                        assert H(cur[d]) == status[d], ("G1", n, c, src, j, d)
                    g1 += 1
                    e_u = word[u]
                    assert (e_u == 2) == (len(qs) % 2 == 1), ("G2", n, c, src, j)
                    g2 += 1
                    q1 = qs[0]
                    zeros_above = sum(1 for d in range(q1 + 1, n) if prev[d] == 0)
                    pred = ((1 if cur[q1] == 0 else 0) + zeros_above) & 1
                    assert pred == E(cur[n]) == E(cells[j]), ("G3", n, c, src, j)
                    g3 += 1
                    Zp = tuple(d for d in range(-u, n) if prev[d] == 0)
                    Zc = tuple(d for d in range(-u - 1, n) if cur[d] == 0)
                    colkey = tuple(cur[d] for d in range(-u - 1, n + 1))
                    key = (n, c, u, Zp, Zc)
                    assert pair_to_col.setdefault(key, colkey) == colkey, ("G4", key)
                    single_to_cols.setdefault((n, c, u, Zp), set()).add(colkey)
                    g4 += 1
    collisions = sum(1 for v in single_to_cols.values() if len(v) > 1)
    worst = max(len(v) for v in single_to_cols.values())
    print(f"G1 retained-run structure: {g1} columns PASS")
    print(f"G2 forced symbol = parity of nonzero count: {g2} columns PASS")
    print(f"G3 top read-out of E(T[u][n]): {g3} columns PASS")
    print(f"G4 (Z_(u-1), Z_u) -> column u well defined: {g4} columns PASS; "
          f"{len(pair_to_col)} distinct pairs")
    print(f"    Z_(u-1) alone: {len(single_to_cols)} keys, {collisions} with >1 column, max {worst} columns per key")


def phi_letters(word: list[int], n: int) -> int:
    """Phi on a letter word (0 = zero cell, 2 = even nonzero, 1 = odd); window top at n-1."""
    m = len(word)
    nonzero = sum(1 for t in word if t != 0)
    h = (1 + nonzero) & 1          # h0 so that final h = h0 + nonzero = 1
    F = 0
    for t in word:
        a = 1 if t == 0 else 0
        b = 1 if t in (0, 2) else 0
        F ^= h & b
        h ^= 1 ^ a
    assert h == 1
    return F


def balance_bruteforce(max_m: int) -> list[tuple[int, int]]:
    out = []
    for m in range(1, max_m + 1):
        zeros = sum(1 for w in product((0, 1, 2), repeat=m) if phi_letters(list(w), m) == 0)
        out.append((m, zeros))
    return out


def balance_transfer(max_m: int) -> list[tuple[int, int]]:
    """Counts via the 4-state Moore matrix: states (h, F), letters act as permutations."""
    letters = [(0, 0), (0, 1), (1, 1)]   # odd, two, zero
    def step(state, letter):
        h, F = state
        a, b = letter
        return (h ^ 1 ^ a, F ^ (h & b))
    out = []
    for m in range(1, max_m + 1):
        total = 0
        # h0 depends on the word's nonzero count, so split by (h0, parity of nonzero count)
        for h0 in (0, 1):
            # count words with final (1, 0) from (h0, 0); final h = h0 + nonzero, so
            # words counted here automatically have nonzero parity = 1 + h0.
            dist = {(h0, 0): 1}
            for _ in range(m):
                nxt: dict = {}
                for st, cnt in dist.items():
                    for L in letters:
                        s2 = step(st, L)
                        nxt[s2] = nxt.get(s2, 0) + cnt
                dist = nxt
            total += dist.get((1, 0), 0)
        out.append((m, total))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-n", type=int, default=9)
    ap.add_argument("--max-m-brute", type=int, default=10)
    ap.add_argument("--max-m-transfer", type=int, default=40)
    args = ap.parse_args()
    t0 = time.time()
    check_orbits(args.max_n)
    print(f"   [{time.time()-t0:.1f}s]")
    bf = dict(balance_bruteforce(args.max_m_brute))
    tr = dict(balance_transfer(args.max_m_transfer))
    print("G5 letter-space balance: m, #Phi=0, 3^m, 2*#Phi=0 - 3^m   (brute force vs transfer matrix)")
    for m in range(1, args.max_m_transfer + 1):
        t = tr[m]
        b = bf.get(m)
        tag = "" if b is None else ("  brute=" + str(b) + (" PASS" if b == t else " FAIL"))
        print(f"   m={m:<3} zeros={t:<22} 3^m={3**m:<22} 2*zeros-3^m={2*t-3**m}{tag}")


if __name__ == "__main__":
    main()

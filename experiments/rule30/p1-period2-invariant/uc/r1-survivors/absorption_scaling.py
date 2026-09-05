#!/usr/bin/env python3
"""Absorption time of source symbol e_i, and the synchronizing-run question.

Part A.  For u = 2..U, over all 2^(u+1) sources, P_u(i) = fraction of sources
for which flipping e_i leaves the full column col_u unchanged (i = 0..IMAX).
Prints the table and, per i, the smallest u with P_u(i) >= 1/2 and >= 0.9.
If the half-absorption column grows like c*i, the retained information is
about (1 - 1/c) bits per symbol, which is the measured state growth exponent
0.82 (merge_decomposition.log) if c is about 5.5.

Part B.  Exact synchronizing runs.  For m = 1..MMAX and a pattern s in
{2, 1, 21, 12, 221, 211}: the least L such that ALL 2^m prefixes followed by
s repeated to length >= L give one column at the end (full column equality),
searched to LMAX.  A finite L(m) means the run erases every prefix of length
m; its growth in m is the cost of a local reset.

Part C.  Hand-checkable law: e_1 = e_2 = 2 implies col_u independent of e_0
for every u >= 3 (checked for all sources to length U3), and e_1 = 2,
e_2 = 2 is the ONLY length-2 pattern with that property.
"""
from __future__ import annotations

import sys
from itertools import product

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
from psi_kernel import CONE, BOUNDARY  # noqa: E402


def all_columns(endpoint):
    cols = []
    prev = None
    for k, e in enumerate(endpoint):
        col = [0] * (2 * k + 2)
        col[0] = e
        col[1] = BOUNDARY[e]
        for d in range(-k + 1, k + 1):
            col[d + k + 1] = CONE[prev[d + k - 1]][col[d + k]]
        cols.append(bytes(col))
        prev = col
    return cols


def part_a(U: int, IMAX: int) -> None:
    print("Part A: P_u(i) = P(col_u unchanged when e_i is flipped), all sources of length u+1")
    header = "  u   " + " ".join(f"i={i:<5d}" for i in range(IMAX + 1))
    print(header)
    half = {}
    ninety = {}
    for u in range(1, U + 1):
        cols = {}
        def rec(k, prev, W):
            for e in (1, 2):
                col = [0] * (2 * k + 2)
                col[0] = e
                col[1] = BOUNDARY[e]
                for d in range(-k + 1, k + 1):
                    col[d + k + 1] = CONE[prev[d + k - 1]][col[d + k]]
                if k == u:
                    cols[W + (e,)] = bytes(col)
                else:
                    rec(k + 1, col, W + (e,))
        rec(0, None, ())
        row = []
        for i in range(IMAX + 1):
            if i > u:
                row.append("   -   ")
                continue
            same = 0
            tot = 0
            for W, c in cols.items():
                if W[i] == 1:
                    W2 = W[:i] + (2,) + W[i + 1:]
                    tot += 1
                    same += c == cols[W2]
            p = same / tot
            row.append(f"{p:7.4f}")
            if p >= 0.5 and i not in half:
                half[i] = u
            if p >= 0.9 and i not in ninety:
                ninety[i] = u
        print(f" {u:2d}   " + " ".join(row))
    print("  first u with P_u(i) >= 0.5: " + ", ".join(f"i={i}:u={half[i]}" for i in sorted(half)))
    print("  first u with P_u(i) >= 0.9: " + ", ".join(f"i={i}:u={ninety[i]}" for i in sorted(ninety)))


def part_b(MMAX: int, LMAX: int) -> None:
    print("\nPart B: least run length L of pattern s erasing every prefix of length m (full-column equality at the last column)")
    pats = [(2,), (1,), (2, 1), (1, 2), (2, 2, 1), (2, 1, 1)]
    for s in pats:
        line = []
        for m in range(1, MMAX + 1):
            found = None
            for L in range(1, LMAX + 1):
                tail = tuple((s * (L // len(s) + 1))[:L])
                seen = set()
                for pre in product((1, 2), repeat=m):
                    seen.add(all_columns(pre + tail)[-1])
                    if len(seen) > 1:
                        break
                if len(seen) == 1:
                    found = L
                    break
            line.append(f"m={m}:L={found if found is not None else '>' + str(LMAX)}")
        print(f"  s={''.join(map(str, s))}: " + "  ".join(line))


def part_c(U3: int) -> None:
    print("\nPart C: which length-2 patterns on (e_1, e_2) make every col_u, u >= 3, independent of e_0?")
    for pat in product((1, 2), repeat=2):
        ok = True
        bad = None
        for L in range(4, U3 + 1):
            for rest in product((1, 2), repeat=L - 3):
                W1 = (1,) + pat + rest
                W2 = (2,) + pat + rest
                c1 = all_columns(W1)
                c2 = all_columns(W2)
                for u in range(3, L):
                    if c1[u] != c2[u]:
                        ok = False
                        bad = (W1, u)
                        break
                if not ok:
                    break
            if not ok:
                break
        print(f"  (e_1,e_2)={''.join(map(str,pat))}: {'LAW HOLDS for all u in [3, ' + str(U3-1) + ']' if ok else 'fails, e.g. ' + ''.join(map(str,bad[0])) + ' at u=' + str(bad[1])}")
    # the hand derivation: column 2 for pattern 22 is (2,1,2,1,2,x) with x in {1,3}
    for e0 in (1, 2):
        c = all_columns((e0, 2, 2))
        print(f"  e_0={e0}, e_1=e_2=2: col_1 = {list(c[1])}, col_2 = {list(c[2])}  (depths -u-1..u)")


if __name__ == "__main__":
    U = int(sys.argv[1]) if len(sys.argv) > 1 else 19
    part_a(U, 8)
    part_b(7, 40)
    part_c(13)

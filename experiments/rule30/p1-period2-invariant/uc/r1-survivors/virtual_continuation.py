#!/usr/bin/env python3
"""The virtual four-state continuation V_c(W).

Fix c in {2,3} and a binary source W in {1,2}^n.  Imposing T[u][n] = c for
every u >= n determines the whole run region {T[u][d]: u >= n, d <= n} by
upward integration (phi is a bijection in its right argument), and hence a
unique FOUR-STATE endpoint continuation e*_n, e*_{n+1}, ... .  The binary
wedge (BWH+) asks how long the prefix of e* stays in {1,2}; the forced binary
continuation Q_n(W) agrees with e* up to the first non-binary symbol.

This script computes e* to length LMAX for every W (n in a range) and reports:
  * the first non-binary index (the BWH+ death), checked against psi();
  * whether e* is eventually periodic within LMAX, and its period/transient;
  * the longest binary run anywhere in e* (not only at the start), and the
    longest hard-core (no 11) run anywhere;
  * the row periods p_d of the run region (period in u of d -> T[u][d]).
"""
from __future__ import annotations

import sys
from itertools import product
from collections import Counter

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
from psi_kernel import CONE, BOUNDARY, psi  # noqa: E402

# g[y][l] = r with CONE[l][r] = y  (upward step)
G = [[None] * 4 for _ in range(4)]
for l in range(4):
    for r in range(4):
        G[CONE[l][r]][l] = r
for y in range(4):
    assert all(G[y][l] is not None for l in range(4))


def E(t: int) -> int:
    return 1 ^ (t >> 1) ^ (t & 1)


def virtual(W: tuple[int, ...], c: int, L: int) -> tuple[list[int], list[list[int]]]:
    """Return (e*, columns) where columns[u] is the list of T[u][d], d=-u-1..u (index d+u+1).

    Columns u < n are computed forward from W; columns u >= n are computed
    upward from T[u][n] = c.  Cells below depth n in the run region are not
    needed for the tops and are not computed (they are the zero triangle).
    """
    n = len(W)
    cols: list[list[int]] = []
    for u, e in enumerate(W):
        col = [0] * (2 * u + 2)
        col[0] = e
        col[1] = BOUNDARY[e]
        prev = cols[u - 1] if u > 0 else None
        for d in range(-u + 1, u + 1):
            col[d + u + 1] = CONE[prev[d - 1 + u]][col[d + u]]
        cols.append(col)
    tops: list[int] = []
    for u in range(n, L):
        prev = cols[u - 1]
        col = [0] * (2 * u + 2)
        # only depths -u-1..n are meaningful; keep the array shape anyway
        col[n + u + 1] = c
        for d in range(n - 1, -u - 1, -1):
            # T[u][d] = g_{T[u][d+1]}(T[u-1][d]);  prev index of depth d is d + u (since prev has u-1)
            col[d + u + 1] = G[col[d + u + 2]][prev[d + u]]
        top = col[0 + 0] if False else None
        # depth -u is index 1; e* = T[u][-u] XOR 3 at index 0
        col[0] = col[1] ^ 3
        tops.append(col[0])
        cols.append(col)
    return tops, cols


def first_nonbinary(seq: list[int]) -> int:
    for i, x in enumerate(seq):
        if x in (0, 3):
            return i
    return len(seq)


def eventual_period(seq: list[int], min_repeats: int = 3) -> tuple[int, int] | None:
    """Smallest (transient, period) such that seq[t:] is periodic with >= min_repeats*period tail."""
    L = len(seq)
    for p in range(1, L // min_repeats + 1):
        # find the smallest t with seq[i] == seq[i+p] for all i >= t
        t = L - p
        while t > 0 and seq[t - 1] == seq[t - 1 + p]:
            t -= 1
        if L - t >= min_repeats * p:
            return t, p
    return None


def longest_run(seq: list[int], ok) -> int:
    best = cur = 0
    for x in seq:
        cur = cur + 1 if ok(x) else 0
        best = max(best, cur)
    return best


def longest_hardcore_binary(seq: list[int]) -> int:
    best = cur = 0
    prev = None
    for x in seq:
        if x in (1, 2) and not (prev == 1 and x == 1):
            cur += 1
        elif x in (1, 2):
            cur = 1
        else:
            cur = 0
        best = max(best, cur)
        prev = x
    return best


def s(seq) -> str:
    return "".join(map(str, seq))


def main() -> None:
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    nmin = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    nmax = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    print(f"virtual continuation e* to length L={L}, n={nmin}..{nmax}")
    print("g[y][l] (upward step r = g[y][l], CONE[l][r] = y):")
    for y in range(4):
        print(f"  y={y}: " + " ".join(str(G[y][l]) for l in range(4)))
    for n in range(nmin, nmax + 1):
        for c in (2, 3):
            deaths = Counter()
            periods = Counter()
            transients = Counter()
            nonper = 0
            maxbin = 0
            maxhc = 0
            maxbin_w = None
            per_all_binary = 0
            mismatch = 0
            for W in product((1, 2), repeat=n):
                tops, cols = virtual(W, c, L)
                fnb = first_nonbinary(tops)
                # consistency with the kernel: Q agrees with e* before the death, and Psi constant there
                Q, P = psi(W)
                k = min(fnb, n + 2)
                if tuple(tops[:k]) != Q[:k] or any(P[j] != E(c) ^ 1 if False else P[j] != (c & 1) for j in range(k)):
                    mismatch += 1
                deaths[fnb] += 1
                ep = eventual_period(tops)
                if ep is None:
                    nonper += 1
                else:
                    t, p = ep
                    periods[p] += 1
                    transients[t] += 1
                    if all(x in (1, 2) for x in tops[t:t + p]):
                        per_all_binary += 1
                lb = longest_run(tops, lambda x: x in (1, 2))
                if lb > maxbin:
                    maxbin, maxbin_w = lb, W
                maxhc = max(maxhc, longest_hardcore_binary(tops))
            print(f"\nn={n} c={c}: {2**n} sources, kernel mismatches={mismatch}")
            print(f"  first non-binary index distribution: " + ", ".join(f"{k}:{v}" for k, v in sorted(deaths.items())))
            print(f"  max first non-binary = {max(deaths)} (BWH+ needs >= {n+2})")
            print(f"  eventually periodic within L: {2**n - nonper}/{2**n}; periods: " + ", ".join(f"{p}:{v}" for p, v in sorted(periods.items())))
            if transients:
                print(f"  transient max={max(transients)}, distribution: " + ", ".join(f"{t}:{v}" for t, v in sorted(transients.items())[:12]) + (" ..." if len(transients) > 12 else ""))
            print(f"  periodic parts entirely binary: {per_all_binary}")
            print(f"  longest binary run anywhere in e*: {maxbin} (W={s(maxbin_w)}); longest hard-core binary run anywhere: {maxhc}")


if __name__ == "__main__":
    main()

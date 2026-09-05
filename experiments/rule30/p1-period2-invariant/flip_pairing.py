#!/usr/bin/env python3
"""Single-source-flip pairing on the RW survivor levels.

Question (pre-registered 2026-09-03).  The full-degree result kills every
bounded-arity seam law for the E defect but not injection arguments.  The
missing fact behind a halving bound is that the E constraint is balanced on
every survivor level, not merely on average.  An injection proof would pair
each source that passes level j with a source at the same level that fails
the E constraint there.  The endpoint-flip cocycle says one source flip
rewrites the cut only on a bounded interval; nobody has tried those flips as
the pairing.

Setting.  Binary source W in {1,2}^n.  For j >= 0 the symbol e_{n+j} is
H-forced by column n+j-1 (unique symbol with H(T[n+j][n]) = 1).  W is alive
at level j (in S_j) if for every j' < j the forced cell T[n+j'][n] equals c
and the forced symbol is hard-core (no 11, junction with W[n-1] included).
D_j is the strict E-failure set: alive at j, forced symbol hard-core at j,
forced cell has the wrong E.  Level j is balanced iff |S_{j+1}| <= |D_j|.

Flip test.  For W in S_{j+1} and i in [0, n), W' = W with e_i toggled is a
valid partner if W' in D_j and the forced symbol at level j agrees
(s_j(W') = s_j(W)).  Also recorded: partners whose entire forced word
s_0..s_j agrees ("full").  delta = n-1-i is the flip depth back from the
last free symbol; the row distance to the target row n+j is delta + j + 1.

Strong outcome.  Every W in S_{j+1} has a valid partner at bounded delta and
the flip graph S_{j+1} -> D_j has a matching saturating S_{j+1} (a genuine
injection).  Kill.  A level where a fixed fraction of S_{j+1} has no partner,
or where max-over-W of the minimal delta grows with n, or where the maximum
matching falls short of |S_{j+1}|.  Balance failure (|S_{j+1}| > |D_j|) kills
any injection at that level regardless of pairing rule.

Complete census on the validated kernel (psi_kernel.Endpoint), nothing
sampled.  Levels j = 0..n+3 cover every r in {0,1,2}.
"""

from __future__ import annotations

import argparse
import sys
import time
from collections import Counter, deque
from itertools import product

from psi_kernel import Endpoint


def E(t: int) -> int:
    return 1 ^ (t >> 1) ^ (t & 1)


def H(t: int) -> int:
    return t >> 1


def forced_orbit(src: tuple[int, ...], n: int, levels: int):
    """Forced continuation of src.  Returns (state_key, syms, cells, hc)."""
    st = Endpoint()
    for s in src:
        st.append(s)
    key = (tuple(st.column), tuple(st.diagonal))
    prev = src[-1]
    syms: list[int] = []
    cells: list[int] = []
    hcs: list[bool] = []
    for _ in range(levels):
        chosen = None
        for s in (1, 2):
            col, dia = st.peek(s)
            if H(dia[n]) == 1:
                assert chosen is None, "H-forced symbol must be unique"
                chosen = (s, col, dia)
        assert chosen is not None, "H-forced symbol must exist"
        s, col, dia = chosen
        syms.append(s)
        cells.append(dia[n])
        hcs.append(not (prev == 1 and s == 1))
        st.column = col + [s]
        st.diagonal = dia
        st.length += 1
        prev = s
    return key, syms, cells, hcs


def hopcroft_karp(left_adj: list[list[int]], n_right: int) -> int:
    """Maximum matching size; left_adj[l] lists right ids."""
    n_left = len(left_adj)
    match_l = [-1] * n_left
    match_r = [-1] * n_right
    INF = 1 << 30
    dist = [0] * n_left

    def bfs() -> bool:
        q = deque()
        found = False
        for l in range(n_left):
            if match_l[l] == -1:
                dist[l] = 0
                q.append(l)
            else:
                dist[l] = INF
        while q:
            l = q.popleft()
            for r in left_adj[l]:
                m = match_r[r]
                if m == -1:
                    found = True
                elif dist[m] == INF:
                    dist[m] = dist[l] + 1
                    q.append(m)
        return found

    def dfs(l: int) -> bool:
        for r in left_adj[l]:
            m = match_r[r]
            if m == -1 or (dist[m] == dist[l] + 1 and dfs(m)):
                match_l[l] = r
                match_r[r] = l
                return True
        dist[l] = INF
        return False

    size = 0
    sys.setrecursionlimit(max(10000, 4 * n_left + 100))
    while bfs():
        for l in range(n_left):
            if match_l[l] == -1 and dfs(l):
                size += 1
    return size


def census(n: int, levels: int):
    t0 = time.time()
    total = 1 << n
    keys: list = [None] * total
    syms: list = [None] * total
    cells: list = [None] * total
    hcs: list = [None] * total
    for idx, src in enumerate(product((1, 2), repeat=n)):
        # bit i of idx is set iff src[i] == 2 (product order, MSB first)
        k, s, c, h = forced_orbit(src, n, levels)
        keys[idx] = k
        syms[idx] = s
        cells[idx] = c
        hcs[idx] = h
    print(f"# n={n}: forced orbits for {total} sources in {time.time() - t0:.1f}s")
    sys.stdout.flush()
    return keys, syms, cells, hcs


def analyse(n: int, c: int, levels: int, keys, syms, cells, hcs, verbose: bool):
    total = 1 << n
    ec = E(c)
    # death level and cause
    death = [levels] * total
    cause = [""] * total  # "E" strict E-miss, "HC" hard-core kill, "" survived all
    for idx in range(total):
        cl = cells[idx]
        hc = hcs[idx]
        for j in range(levels):
            if not hc[j]:
                death[idx] = j
                cause[idx] = "HC"
                break
            if cl[j] != c:
                death[idx] = j
                cause[idx] = "E"
                break
    print(f"## n={n} c={c} (E target {ec}); levels j=0..{levels - 1}")
    print("j |S_j| |S_j+1| |D_j| |Dall_j| ratio balE balAll | strict: cover full maxmin match | "
          "lenient: cover maxmin match | freeH cover | states cov_strict cov_lenient | strict min-delta histogram")
    summary = []
    for j in range(levels):
        S_j = [w for w in range(total) if death[w] >= j]
        S_j1 = [w for w in S_j if death[w] >= j + 1]
        D_j = [w for w in S_j if death[w] == j and cause[w] == "E"]
        Dall_j = [w for w in S_j if death[w] == j]
        if not S_j1:
            print(f"{j:2d} {len(S_j):7d} {0:7d} {len(D_j):7d} {len(Dall_j):7d}  (no survivors past level {j})")
            break
        D_set = {w: r for r, w in enumerate(D_j)}
        Dall_set = {w: r for r, w in enumerate(Dall_j)}
        covered = covered_full = covered_len = covered_free = 0
        min_delta = []
        min_delta_len = []
        adj: list[list[int]] = []
        adj_len: list[list[int]] = []
        state_cov: dict = {}
        state_cov_len: dict = {}
        for w in S_j1:
            sw = syms[w]
            partners = []
            partners_len = []
            best = best_len = None
            full = False
            free = False
            for i in range(n):
                bit = 1 << (n - 1 - i)  # product order: src[i] is bit n-1-i
                w2 = w ^ bit
                r_all = Dall_set.get(w2)
                if r_all is None:
                    continue
                free = True
                if syms[w2][j] != sw[j]:
                    continue
                delta = n - 1 - i
                partners_len.append(r_all)
                if best_len is None or delta < best_len:
                    best_len = delta
                r = D_set.get(w2)
                if r is None:
                    continue
                partners.append(r)
                if best is None or delta < best:
                    best = delta
                if syms[w2][: j + 1] == sw[: j + 1]:
                    full = True
            adj.append(partners)
            adj_len.append(partners_len)
            k = keys[w]
            state_cov.setdefault(k, False)
            state_cov_len.setdefault(k, False)
            if partners:
                covered += 1
                min_delta.append(best)
                state_cov[k] = True
            if partners_len:
                covered_len += 1
                min_delta_len.append(best_len)
                state_cov_len[k] = True
            if full:
                covered_full += 1
            if free:
                covered_free += 1
        match = hopcroft_karp(adj, len(D_j)) if D_j else 0
        match_len = hopcroft_karp(adj_len, len(Dall_j)) if Dall_j else 0
        n_states = len(state_cov)
        n_states_cov = sum(1 for v in state_cov.values() if v)
        n_states_cov_len = sum(1 for v in state_cov_len.values() if v)
        hist = Counter(min_delta)
        hist_s = " ".join(f"{d}:{hist[d]}" for d in sorted(hist))
        m = len(S_j1)
        ratio = m / len(S_j)
        balanced = m <= len(D_j)
        balanced_all = m <= len(Dall_j)
        maxmin = max(min_delta) if min_delta else -1
        maxmin_len = max(min_delta_len) if min_delta_len else -1
        cover = covered / m
        cover_len = covered_len / m
        print(
            f"{j:2d} {len(S_j):7d} {m:7d} {len(D_j):7d} {len(Dall_j):7d} {ratio:5.3f} "
            f"{'Y' if balanced else 'N':>4s} {'Y' if balanced_all else 'N':>6s} | "
            f"{cover:5.3f} {covered_full / m:5.3f} {maxmin:3d} {match:6d}/{m:<6d} | "
            f"{cover_len:5.3f} {maxmin_len:3d} {match_len:6d}/{m:<6d} | {covered_free / m:5.3f} | "
            f"{n_states:6d} {n_states_cov:6d} {n_states_cov_len:6d} | {hist_s}"
        )
        sys.stdout.flush()
        summary.append((j, len(S_j), m, len(D_j), balanced, cover, match, maxmin,
                        len(Dall_j), balanced_all, cover_len, match_len, maxmin_len))
        if verbose and not balanced_all:
            print(f"   level {j} unbalanced even against all deaths: |S_{j + 1}|={m} > |Dall_{j}|={len(Dall_j)}")
    return summary


def death_profile(n: int, c: int, levels: int, cells, hcs, max_level: int = 6) -> None:
    """For W in S_{j+1} and each single flip at depth delta = n-1-i: the
    probability that W' is still alive at level j, split by delta, and the
    distribution of the level at which W' dies (capped at j).  A flip that
    acted only on a bounded interval near the target row would show a delta
    profile concentrated at small delta; a flip that is a fresh coin on every
    level shows a flat profile at about 0.4^j."""
    total = 1 << n
    death = [levels] * total
    for w in range(total):
        for j in range(levels):
            if not hcs[w][j] or cells[w][j] != c:
                death[w] = j
                break
    print(f"## death profile n={n} c={c}: for W in S_(j+1) and each single flip at depth delta, "
          f"P(W' alive at level j) by delta=0..{n - 1}, and the death level of W' capped at j")
    for j in range(max_level):
        S1 = [w for w in range(total) if death[w] >= j + 1]
        if not S1:
            break
        alive = Counter()
        tot = Counter()
        dd = Counter()
        for w in S1:
            for i in range(n):
                d = n - 1 - i
                w2 = w ^ (1 << (n - 1 - i))
                tot[d] += 1
                if death[w2] >= j:
                    alive[d] += 1
                dd[min(death[w2], j)] += 1
        row = " ".join(f"{alive[d] / tot[d]:.2f}" for d in range(n))
        dist = " ".join(f"{k}:{dd[k] / len(S1) / n:.2f}" for k in sorted(dd))
        print(f" j={j} |S_j+1|={len(S1):6d}  P(alive@j | delta): {row}")
        print(f"        death level of W': {dist}")
    sys.stdout.flush()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-n", type=int, default=9)
    ap.add_argument("--max-n", type=int, default=16)
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--profile", action="store_true", help="death profile only, no pairing census")
    args = ap.parse_args()
    grand = {}
    for n in range(args.min_n, args.max_n + 1):
        levels = n + 4
        keys, syms, cells, hcs = census(n, levels)
        for c in (2, 3):
            if args.profile:
                death_profile(n, c, levels, cells, hcs)
            else:
                grand[(n, c)] = analyse(n, c, levels, keys, syms, cells, hcs, args.verbose)
    if args.profile:
        return
    print("## summary per (n, c), bulk levels = |S_j+1| >= 8: strict (E-death partner) and lenient "
          "(any-death partner) min cover / min match fraction / max minimal delta; unbalanced levels")
    for (n, c), rows in sorted(grand.items()):
        bulk = [r for r in rows if r[2] >= 8]
        unbal = [r[0] for r in rows if not r[4]]
        unbal_all = [r[0] for r in rows if not r[9]]
        if not bulk:
            continue
        print(f"n={n:2d} c={c}: bulk j={bulk[0][0]}..{bulk[-1][0]}  "
              f"strict cover>={min(r[5] for r in bulk):.3f} match>={min(r[6] / r[2] for r in bulk):.3f} "
              f"delta<={max(r[7] for r in bulk)}  |  "
              f"lenient cover>={min(r[10] for r in bulk):.3f} match>={min(r[11] / r[2] for r in bulk):.3f} "
              f"delta<={max(r[12] for r in bulk)}  |  unbalanced E-only={unbal} any-death={unbal_all}")


if __name__ == "__main__":
    main()

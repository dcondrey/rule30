#!/usr/bin/env python3
"""Independent verifier for the lemma retained-bit-form (a)-(e), LOGIC lens.

Written from the LEMMA TEXT, not from PROOF.md's block decomposition:
retained is decided by "nearest nonzero cell above", runs are computed as
maximal contiguous intervals of non-retained cells, and the "whole forced
future" is checked literally (every later forced symbol and every later hit
to u = 2n+2) across ALL sources sharing a (n, u, Z_{u-1}, Z_u) key.

V1  (a)(b)(c)(d-runs) on every forced orbit, every binary source n <= NB,
    u = n .. 2n+2, plus pair-key determinism of column u on [-u-1, n] AND the
    forced future (symbols e_{u+1..2n+2}, hits E(T[u'][n]) for u' in [u, 2n+2]).
V2  Fibre probe for the sentence in PROOF.md section 6 Remark / section 9
    ("Z_{u-1} does not determine column u because the odd-indexed even-bits
    are discarded"): within each (n, u, Z_{u-1}) fibre, the number of
    distinct columns u equals the number of distinct EVEN-indexed even-bit
    vectors, and windows differing only in ODD-indexed even-bits give the
    same column.  So the non-determination is caused by the even-indexed
    bits (read), and the odd-indexed bits (discarded) are exactly what does
    NOT obstruct it.
V3  Lemma H and Lemma E (by-product form: arbitrary four-state prefix, all
    four e_u, constant E(e_u)) on random four-state prefixes of length U4R,
    every d in [-u, u].  Independent of the proof's small-u exhaustive gate.
V4  Theorem E by the bare Moore machine only (no block formula), m <= M.

Any AssertionError kills.  Run from the work directory:
  uv run python uc/r1-quadratic-prove-retained-bit-form-structural-verify-logic/verify_logic.py
"""
from __future__ import annotations

import argparse
import os
import random
import sys
import time
from itertools import product

WORK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, WORK)
from psi_kernel import CONE  # noqa: E402


def H(t: int) -> int:
    return t >> 1


def E(t: int) -> int:
    return (1 + (t >> 1) + (t & 1)) & 1


def next_column(prev: dict, u: int, e_u: int, dmax: int) -> dict:
    """Column u on [-u-1, dmax] from column u-1 by the BRIEF section 2 recurrence."""
    col = {-u - 1: e_u, -u: e_u ^ 3}
    for d in range(-u + 1, dmax + 1):
        col[d] = CONE[prev[d - 1]][col[d - 1]]
    return col


def forced_orbit(source: tuple, n: int, U: int):
    """Columns T[0..U] (full, d in [-u-1, u]) and symbols e_0..e_U; e_u forced for u >= n."""
    cols, syms = [], []
    for u in range(U + 1):
        if u < n:
            e = source[u]
        else:
            found = [s for s in (1, 2) if H(next_column(cols[u - 1], u, s, n)[n]) == 1]
            assert len(found) == 1, ("forcing-not-unique", source, n, u, found)
            e = found[0]
        prev = cols[u - 1] if u else None
        cols.append(next_column(prev, u, e, u) if u else {-1: e, 0: e ^ 3})
        syms.append(e)
    return cols, syms


def retained_map(prev: dict, lo: int, hi: int):
    """Lemma text: q_1 > q_2 > ... nonzero depths from the top; retained iff q_i with i even,
    or a zero whose nearest nonzero ABOVE is q_i with i even, or a zero with none above."""
    qs = [d for d in range(hi - 1, lo - 1, -1) if prev[d] != 0]
    idx = {d: i for i, d in enumerate(qs, start=1)}
    ret = {}
    for d in range(lo, hi):
        if prev[d] != 0:
            ret[d] = idx[d] % 2 == 0
        else:
            above = [q for q in qs if q > d]
            ret[d] = True if not above else (idx[min(above)] % 2 == 0)
    return qs, ret


def maximal_runs(ret: dict, lo: int, hi: int):
    runs, cur = [], []
    for d in range(hi - 1, lo - 1, -1):
        if not ret[d]:
            cur.append(d)
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    return runs


def v1_v2(nb: int, log) -> None:
    t0 = time.time()
    checked = 0
    pair_map: dict = {}
    fibre: dict = {}   # (n, u, Z_{u-1}) -> {column: set of (even_w, odd_w)}
    for n in range(1, nb + 1):
        U = 2 * n + 2
        for source in product((1, 2), repeat=n):
            cols, syms = forced_orbit(source, n, U)
            hits = [E(cols[v][n]) for v in range(n, U + 1)]
            for u in range(n, U + 1):
                prev, cur = cols[u - 1], cols[u]
                lo, hi = -u, n
                qs, ret = retained_map(prev, lo, hi)
                N = len(qs)
                assert qs and qs[-1] == lo, ("bottom-nonzero", source, n, u)
                # (a)
                assert (syms[u] == 2) == (N % 2 == 1), ("a", source, n, u)
                # (b)
                for d in range(lo, hi):
                    assert H(cur[d]) == (1 if ret[d] else 0), ("b", source, n, u, d)
                assert H(cur[n]) == 1, ("pin", source, n, u)
                # (c)
                rz = sum(1 for d in range(lo, hi) if prev[d] == 0 and ret[d])
                ew = sum(1 for i, q in enumerate(qs, start=1) if i % 2 == 0 and prev[q] == 2)
                assert E(cur[n]) == (rz + ew) & 1, ("c", source, n, u)
                # (d) Z_u is a union of complete maximal non-retained runs
                Zu = {d for d in range(-u - 1, n) if cur[d] == 0}
                runs = maximal_runs(ret, lo, hi)
                covered = set()
                for run in runs:
                    ins = [d in Zu for d in run]
                    assert all(ins) or not any(ins), ("d-partial-run", source, n, u, run)
                    covered.update(run)
                assert Zu <= covered, ("d-zero-outside-runs", source, n, u)
                # (d) the pair determines column u on [-u-1, n] and the WHOLE forced future
                Zp = frozenset(d for d in range(lo, hi) if prev[d] == 0)
                key = (n, u, Zp, frozenset(Zu))
                val = (tuple(cur[d] for d in range(-u - 1, n + 1)),
                       tuple(syms[u + 1:]), tuple(hits[u - n:]))
                old = pair_map.setdefault(key, val)
                assert old == val, ("d-pair-future", source, n, u)
                # V2 fibre data
                even_w = tuple(1 if prev[q] == 2 else 0 for i, q in enumerate(qs, start=1) if i % 2 == 0)
                odd_w = tuple(1 if prev[q] == 2 else 0 for i, q in enumerate(qs, start=1) if i % 2 == 1)
                fibre.setdefault((n, u, Zp), {}).setdefault(val[0], set()).add((even_w, odd_w))
                checked += 1
    print(f"V1 (a)(b)(c)(d) on {checked} (source, u) pairs, all binary sources n<={nb}, u=n..2n+2; "
          f"{len(pair_map)} distinct (n,u,Z_(u-1),Z_u) keys, each with one column u on [-u-1,n] and one "
          f"forced future (symbols and hits to u=2n+2) PASS   [{time.time()-t0:.0f}s]", file=log, flush=True)
    # V2
    multi = 0
    total_cols = 0
    odd_only_merges = 0
    for key, bycol in fibre.items():
        cols_here = len(bycol)
        evens = set()
        for col, ws in bycol.items():
            ev = {e for e, _ in ws}
            assert len(ev) == 1, ("V2-column-with-two-even-vectors", key, col)
            evens |= ev
            if len(ws) > 1:
                odd_only_merges += 1
        assert len(evens) == cols_here, ("V2-even-vectors-vs-columns", key, len(evens), cols_here)
        total_cols += cols_here
        if cols_here > 1:
            multi += 1
    print(f"V2 fibre probe: {len(fibre)} (n,u,Z_(u-1)) fibres, {multi} with more than one column u; in every "
          f"fibre #distinct columns == #distinct even-indexed even-bit vectors, every column carries exactly one "
          f"even-indexed vector, and {odd_only_merges} columns are shared by windows differing only in odd-indexed "
          f"even-bits.  So Z_(u-1) fails to determine column u because of the even-indexed bits (read), not the "
          f"odd-indexed ones (discarded) PASS", file=log, flush=True)


def v3_integrals(u4r: int, samples: int, seed: int, log) -> None:
    t0 = time.time()
    rng = random.Random(seed)
    cells = 0
    for _ in range(samples):
        u = u4r
        prefix = [rng.randrange(4) for _ in range(u)]
        cols = []
        for k, e in enumerate(prefix):
            cols.append(next_column(cols[k - 1], k, e, k) if k else {-1: e, 0: e ^ 3})
        prev = cols[u - 1]
        for e_u in range(4):
            cur = next_column(prev, u, e_u, u)
            zeros = ev = 0
            for d in range(-u, u + 1):
                assert H(cur[d]) == (H(e_u) + d + u + 1 + zeros) & 1, ("V3-H", prefix, e_u, d)
                assert E(cur[d]) == (E(e_u) + ev) & 1, ("V3-E", prefix, e_u, d)
                cells += 1
                if d < u:
                    zeros += 1 if prev[d] == 0 else 0
                    ev += 1 if (H(cur[d]) == 1 and (prev[d] & 1) == 0) else 0
    print(f"V3 Lemma H and Lemma E on {cells} cells: {samples} random four-state prefixes of length {u4r} "
          f"(seed {seed}), all four e_u, every d in [-u,u] PASS   [{time.time()-t0:.0f}s]", file=log, flush=True)


def v4_balance(mmax: int, log) -> None:
    t0 = time.time()
    AB = {0: (1, 1), 2: (0, 1), 1: (0, 0)}   # letter -> (a, b); 1 stands for x
    for m in range(1, mmax + 1):
        n0 = 0
        for word in product((0, 1, 2), repeat=m):
            nz = sum(1 for t in word if t)
            h, F = (1 + nz) & 1, 0
            for t in word:
                a, b = AB[t]
                F ^= h & b
                h ^= 1 ^ a
            assert h == 1, ("V4-final-h", word)
            n0 += 1 - F
        assert n0 == (3 ** m + 1) // 2, ("V4-count", m, n0)
    print(f"V4 Theorem E by the bare Moore machine: N0(m) = (3^m+1)/2 for m<={mmax} "
          f"(3^{mmax} = {3**mmax} words at the top) PASS   [{time.time()-t0:.0f}s]", file=log, flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--nb", type=int, default=11)
    ap.add_argument("--u4r", type=int, default=40)
    ap.add_argument("--samples", type=int, default=300)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--m", type=int, default=13)
    args = ap.parse_args()
    log = sys.stdout
    print(f"verify_logic.py args={vars(args)}", file=log, flush=True)
    t0 = time.time()
    v1_v2(args.nb, log)
    v3_integrals(args.u4r, args.samples, args.seed, log)
    v4_balance(args.m, log)
    print(f"ALL PASS   [{time.time()-t0:.0f}s]", file=log, flush=True)


if __name__ == "__main__":
    main()

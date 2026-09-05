#!/usr/bin/env python3
"""Kill test for the lemma "retained-bit-form" (a)-(e), on the kernel psi_kernel.Endpoint.

The lemma is stated for ANY binary prefix e_0..e_{u-1} in {1,2}^u with u >= n,
not only for forced-orbit prefixes.  q2_gate.py / q2_gate_random.py test the
forced-orbit corpus only.  This script tests the broader statement:

  corpus X (exhaustive): every binary word of length u, 1 <= u <= U, every n in [1, u];
  corpus R (random):     random binary words of length 2n+2 at larger n, every u in [n, 2n+1];
  corpus L (letter space): every column u-1 window in {0,1,2}^m (and {0..3}^m for small m),
                           column u computed by the kernel rule phi = CONE directly with e_u forced.

For each (word, n) with u = len(word): column u-1 on the window d in [-u, n-1],
column u on [-u-1, n] with e_u the unique symbol giving H(T[u][n]) = 1.
Checks (any AssertionError kills; the tuple names the tag and the witness):
  A  e_u = 2 iff N (number of nonzero window cells) is odd
  B  H(T[u][d]) = 1 iff cell d of column u-1 is retained, d in [-u, n-1]
  C  E(T[u][n]) = #retained zeros + #{i even : T[u-1][q_i] = 2} (mod 2)
  C' the same value equals the BRIEF section 3 set form of Phi (gate on the code, not the lemma)
  D1 Z_u on [-u-1, n-1] is a union of complete maximal non-retained runs of column u-1
  D2 explicit read-out: w_{2i} = E_u(run above) + E_u(run below) + #retained zeros between
  D3 (Z_{u-1}, Z_u) -> column u on [-u-1, n] and the next FUT forced symbols is single valued
  D4 (letter space) flipping the even-bit of an odd-indexed nonzero cell leaves column u unchanged,
     flipping an even-indexed one changes it; cells 1 and 3 are interchangeable
  E  #{q in {0,2,x}^m : Phi(q) = 0} = (3^m + 1)/2, brute force via the kernel rule for m <= MB and
     via the (h,F) transfer matrix for m <= MT

Gates against references before any claim: columns from Endpoint agree with
psi_column_map.forced_columns and qf_common.forward_columns / forced_orbit, and
the forced continuation agrees with psi_kernel.psi.

Run:  cd <work dir> && uv run python uc/r1-quadratic-screen-retained-bit-form/rbf_kill.py --umax 15 --rand-n 30 40 --samples 200
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
sys.path.insert(0, os.path.join(WORK, "uc", "r1-quadratic"))

from psi_kernel import CONE, BOUNDARY, Endpoint, psi as kernel_psi  # noqa: E402


MUTATE = False


def H(t: int) -> int:
    return t >> 1


def E(t: int) -> int:
    return (1 + (t >> 1) + (t & 1)) & 1


# ----------------------------------------------------------------------------
# columns from the kernel
# ----------------------------------------------------------------------------

def column_of(ep: Endpoint) -> dict[int, int]:
    """T[u][d], d in [-u-1, u], for the endpoint of length u+1 held by ep."""
    col = {}
    for i, t in enumerate(ep.column):
        col[-i] = t
    for k, t in enumerate(ep.diagonal):
        col[k] = t
    return col


def forced_symbol(ep: Endpoint, n: int) -> tuple[int, dict[int, int]]:
    """e_u with H(T[u][n]) = 1 for the prefix held by ep (length u >= n), and column u."""
    chosen = None
    for s in (1, 2):
        column, diagonal = ep.peek(s)
        if diagonal[n] >> 1 == 1:
            assert chosen is None, ("forcing not unique", n)
            chosen = (s, column, diagonal)
    assert chosen is not None, ("forcing empty", n)
    s, column, diagonal = chosen
    col = {}
    for i, t in enumerate(column + [s]):
        col[-i] = t
    for k, t in enumerate(diagonal):
        col[k] = t
    return s, col


# ----------------------------------------------------------------------------
# retained structure of a window
# ----------------------------------------------------------------------------

def analyse_window(prev: dict[int, int], lo: int, hi: int):
    """Window d in [lo, hi) of column u-1.  Returns
    qs (nonzero depths from the top), retained[d], runs (list of (top, bottom) maximal
    non-retained runs, as depth lists), retained_zero_count, even_bits list w_i."""
    qs = [d for d in range(hi - 1, lo - 1, -1) if prev[d] != 0]
    retained = {}
    for i, d in enumerate(qs, start=1):
        retained[d] = (i % 2 == 0) != MUTATE
    above = True
    for d in range(hi - 1, lo - 1, -1):
        if prev[d] != 0:
            above = retained[d]
        else:
            retained[d] = above
    runs = []
    cur: list[int] = []
    for d in range(hi - 1, lo - 1, -1):
        if not retained[d]:
            cur.append(d)
        else:
            if cur:
                runs.append(cur)
                cur = []
    if cur:
        runs.append(cur)
    ret_zero = sum(1 for d in range(lo, hi) if prev[d] == 0 and retained[d])
    w = [1 if prev[d] == 2 else 0 for d in qs]   # w_i = [T[u-1][q_i] == 2], i = 1..N
    return qs, retained, runs, ret_zero, w


def phi_set_form(prev: dict[int, int], lo: int, hi: int) -> int:
    """BRIEF section 3 set form, evaluated from scratch (independent of the lemma)."""
    m = hi - lo
    Z = sum(1 for d in range(lo, hi) if prev[d] == 0)
    W2 = sum(1 for d in range(lo, hi) if prev[d] == 2)
    pairs = 0
    nonzero_below = 0
    for d in range(lo, hi):
        t = prev[d]
        if t == 0 or t == 2:
            pairs += nonzero_below
        if t != 0:
            nonzero_below += 1
    return ((Z + W2) * (1 + m + Z) + pairs) & 1


# ----------------------------------------------------------------------------
# the checks on one (word, n)
# ----------------------------------------------------------------------------

def check_pair(prev: dict[int, int], cur: dict[int, int], e_u: int, n: int, u: int,
               tag_ctx, stats: dict) -> tuple:
    lo, hi = -u, n
    qs, retained, runs, ret_zero, w = analyse_window(prev, lo, hi)
    N = len(qs)
    # A
    assert (e_u == 2) == (N % 2 == 1), ("A", tag_ctx, n, u, e_u, N)
    # B
    for d in range(lo, hi):
        assert H(cur[d]) == (1 if retained[d] else 0), ("B", tag_ctx, n, u, d)
    # C
    even_two = sum(w[i - 1] for i in range(2, N + 1, 2))
    predicted = (ret_zero + even_two) & 1
    assert predicted == E(cur[n]), ("C", tag_ctx, n, u, predicted, E(cur[n]))
    assert predicted == phi_set_form(prev, lo, hi), ("C-setform", tag_ctx, n, u)
    # D1: Z_u is a union of complete maximal non-retained runs; -u-1 never zero
    assert cur[-u - 1] != 0, ("D1-bottom", tag_ctx, n, u)
    Zu = {d for d in range(-u - 1, n) if cur[d] == 0}
    in_run = {}
    for k, run in enumerate(runs):
        inside = [d in Zu for d in run]
        assert all(inside) or not any(inside), ("D1-partial", tag_ctx, n, u, run)
        for d in run:
            in_run[d] = k
    for d in Zu:
        assert d in in_run, ("D1-outside", tag_ctx, n, u, d)
    run_E = [1 if run[0] in Zu else 0 for run in runs]
    # D2: explicit read-out of even bits.  Runs are ordered from the top; run k contains
    # q_{2k+1}.  Retained q_{2k+2} sits between run k (above) and run k+1 (below).
    for k in range(len(runs)):
        i = 2 * k + 2
        if i > N:
            break
        q = qs[i - 1]
        e_above = run_E[k]
        e_below = run_E[k + 1] if k + 1 < len(runs) else 0
        q_next = qs[i] if i < N else lo - 1
        zeros_between = sum(1 for d in range(q_next + 1, q) if prev[d] == 0)
        assert ((e_above + e_below + zeros_between) & 1) == w[i - 1], ("D2", tag_ctx, n, u, i)
    stats["cols"] += 1
    stats["slack_zero_runs"] += len(runs)
    Zp = tuple(d for d in range(lo, hi) if prev[d] == 0)
    return Zp, tuple(sorted(Zu)), tuple(w[i - 1] for i in range(2, N + 1, 2))


def forced_future(ep: Endpoint, n: int, steps: int) -> tuple:
    ep = ep.clone()
    out = []
    for _ in range(steps):
        s, col = forced_symbol(ep, n)
        ep.append(s)
        out.append((s, col[n]))
    return tuple(out)


# ----------------------------------------------------------------------------
# corpora
# ----------------------------------------------------------------------------

def run_exhaustive(umax: int, fut: int, log) -> dict:
    stats = {"cols": 0, "slack_zero_runs": 0}
    pair_map: dict = {}
    single_map: dict = {}
    t0 = time.time()
    for u in range(1, umax + 1):
        for word in product((1, 2), repeat=u):
            ep = Endpoint()
            for s in word:
                ep.append(s)
            prev = column_of(ep)
            for n in range(1, u + 1):
                e_u, cur = forced_symbol(ep, n)
                Zp, Zu, weven = check_pair(prev, cur, e_u, n, u, word, stats)
                colkey = tuple(cur[d] for d in range(-u - 1, n + 1))
                ep2 = ep.clone()
                ep2.append(e_u)
                future = forced_future(ep2, n, fut)
                key = (n, u, Zp, Zu)
                val = (colkey, future, weven)
                old = pair_map.setdefault(key, val)
                assert old == val, ("D3", word, n, u, key, old, val)
                single_map.setdefault((n, u, Zp), set()).add(colkey)
        print(f"  X u={u:<3} words={2**u:<7} columns so far={stats['cols']}   [{time.time()-t0:.0f}s]", file=log, flush=True)
    coll = sum(1 for v in single_map.values() if len(v) > 1)
    worst = max(len(v) for v in single_map.values())
    stats["pairs"] = len(pair_map)
    stats["single_keys"] = len(single_map)
    stats["single_collisions"] = coll
    stats["single_worst"] = worst
    return stats


def run_random(ns: list[int], samples: int, seed: int, log) -> dict:
    rng = random.Random(seed)
    out = {}
    for n in ns:
        stats = {"cols": 0, "slack_zero_runs": 0}
        pair_map: dict = {}
        t0 = time.time()
        for _ in range(samples):
            word = tuple(rng.choice((1, 2)) for _ in range(2 * n + 2))
            ep = Endpoint()
            for s in word[:n]:
                ep.append(s)
            for u in range(n, 2 * n + 2):
                prev = column_of(ep)
                e_u, cur = forced_symbol(ep, n)
                Zp, Zu, weven = check_pair(prev, cur, e_u, n, u, ("rand", n, word), stats)
                colkey = tuple(cur[d] for d in range(-u - 1, n + 1))
                key = (n, u, Zp, Zu)
                assert pair_map.setdefault(key, (colkey, weven)) == (colkey, weven), ("D3", n, u, word)
                ep.append(word[u])
        stats["pairs"] = len(pair_map)
        out[n] = stats
        print(f"  R n={n:<3} samples={samples} columns={stats['cols']} distinct pairs={stats['pairs']}   [{time.time()-t0:.0f}s]", file=log, flush=True)
    return out


def column_from_letters(prev_cells: list[int], n: int) -> tuple[int, list[int]]:
    """Kernel rule on a free column window: cells prev_cells at d = -u .. n-1 (m = n+u),
    e_u forced by H(T[u][n]) = 1.  Returns (e_u, cells of column u at d = -u-1 .. n)."""
    m = len(prev_cells)
    for s in (1, 2):
        col = [s, BOUNDARY[s]]
        for i in range(m):
            col.append(CONE[prev_cells[i]][col[-1]])
        if col[-1] >> 1 == 1:
            return s, col
    raise AssertionError("no forced symbol")


def moore_column(prev_cells: list[int], n: int) -> tuple[int, list[int]]:
    m = len(prev_cells)
    nz = sum(1 for t in prev_cells if t != 0)
    h_e = nz & 1                       # H(e_u) = |N| mod 2  (claim A)
    e_u = 2 if h_e else 1
    h, F = 1 - h_e, 0
    col = [e_u]
    for t in prev_cells:
        col.append(2 * h + ((1 + h + F) & 1))
        a = 1 if t == 0 else 0
        b = 1 - (t & 1)
        h, F = h ^ 1 ^ a, F ^ (h & b)
    col.append(2 * h + ((1 + h + F) & 1))
    return e_u, col


def run_letters(mmax: int, m4max: int, log) -> dict:
    """Letter-space checks D4 and the kernel/Moore agreement on free columns."""
    stats = {"words": 0, "odd_flips": 0, "even_flips": 0, "words4": 0}
    t0 = time.time()
    for m in range(1, mmax + 1):
        n = (m + 1) // 2           # any split n + u = m with u >= n; the checks do not depend on n
        for cells in product((0, 1, 2), repeat=m):
            cells = list(cells)
            e_u, col = column_from_letters(cells, n)
            e2, col2 = moore_column(cells, n)
            assert (e_u, col) == (e2, col2), ("moore-vs-kernel", cells)
            stats["words"] += 1
            # retained structure: index positions i = 0..m-1 map to d = -u + i; top is i = m-1
            qs = [i for i in range(m - 1, -1, -1) if cells[i] != 0]
            for idx, i in enumerate(qs, start=1):
                flipped = cells[:]
                flipped[i] = 2 if cells[i] == 1 else 1
                ef, colf = column_from_letters(flipped, n)
                if idx % 2 == 1:
                    assert (ef, colf) == (e_u, col), ("D4-odd-read", cells, i)
                    stats["odd_flips"] += 1
                else:
                    assert (ef, colf) != (e_u, col), ("D4-even-blind", cells, i)
                    stats["even_flips"] += 1
        print(f"  L m={m:<3} words={3**m}   [{time.time()-t0:.0f}s]", file=log, flush=True)
    for m in range(1, m4max + 1):
        n = (m + 1) // 2
        for cells in product((0, 1, 2, 3), repeat=m):
            cells = list(cells)
            e_u, col = column_from_letters(cells, n)
            quot = [1 if t == 3 else t for t in cells]
            assert (e_u, col) == column_from_letters(quot, n), ("D4-3-vs-1", cells)
            stats["words4"] += 1
    print(f"  L four-state words checked={stats['words4']} (3 interchangeable with 1)   [{time.time()-t0:.0f}s]", file=log, flush=True)
    return stats


def balance(mb: int, mt: int, log) -> None:
    letters = [(0, 0), (0, 1), (1, 1)]
    def step(st, L):
        h, F = st
        a, b = L
        return (h ^ 1 ^ a, F ^ (h & b))
    for m in range(1, mt + 1):
        total = 0
        for h0 in (0, 1):
            dist = {(h0, 0): 1}
            for _ in range(m):
                nxt: dict = {}
                for st, cnt in dist.items():
                    for L in letters:
                        s2 = step(st, L)
                        nxt[s2] = nxt.get(s2, 0) + cnt
                dist = nxt
            total += dist.get((1, 0), 0)
        expected = (3 ** m + 1) // 2
        line = f"  E m={m:<3} transfer={total} expected={expected}"
        if m <= mb:
            brute = 0
            for cells in product((0, 1, 2), repeat=m):
                _, col = column_from_letters(list(cells), (m + 1) // 2)
                if E(col[-1]) == 0:
                    brute += 1
            line += f" brute(kernel)={brute}"
            assert brute == expected, ("E-brute", m, brute, expected)
        assert total == expected, ("E-transfer", m, total, expected)
        print(line, file=log, flush=True)


# ----------------------------------------------------------------------------
# gates against references
# ----------------------------------------------------------------------------

def gate(max_n: int, log) -> None:
    from psi_column_map import forced_columns
    from qf_common import forced_orbit, forward_columns
    checked = 0
    for n in range(1, max_n + 1):
        for src in product((1, 2), repeat=n):
            ref = forced_columns(src)
            symbols, hits, cells = forced_orbit(src, n + 2)
            q, psi_w = kernel_psi(src)
            assert tuple(symbols) == tuple(q), ("gate-psi-Q", src)
            assert tuple(hits) == tuple(psi_w), ("gate-psi-Psi", src)
            word = tuple(src) + tuple(symbols)
            cols_ref = forward_columns(word)
            ep = Endpoint()
            for s in src:
                ep.append(s)
            for j in range(n + 2):
                u = n + j
                assert column_of(ep) == cols_ref[u - 1], ("gate-col", src, j)
                e_u, cur = forced_symbol(ep, n)
                assert e_u == symbols[j], ("gate-forced", src, j)
                assert cur == cols_ref[u], ("gate-cur", src, j)
                assert [cur[d] for d in range(0, n + 1)] == ref[j + 1][: n + 1], ("gate-fc", src, j)
                assert cur[n] == cells[j], ("gate-cell", src, j)
                ep.append(e_u)
                checked += 1
    print(f"GATE: {checked} forced columns agree with psi_column_map.forced_columns, qf_common and psi_kernel.psi, n <= {max_n}", file=log, flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--umax", type=int, default=12)
    ap.add_argument("--fut", type=int, default=4)
    ap.add_argument("--rand-n", type=int, nargs="*", default=[30, 40])
    ap.add_argument("--samples", type=int, default=200)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--letters-m", type=int, default=10)
    ap.add_argument("--letters-m4", type=int, default=7)
    ap.add_argument("--balance-brute", type=int, default=10)
    ap.add_argument("--balance-transfer", type=int, default=60)
    ap.add_argument("--gate-n", type=int, default=8)
    ap.add_argument("--skip", nargs="*", default=[])
    ap.add_argument("--mutate", action="store_true",
                    help="sanity: define retained as ODD-indexed; the test must then fire")
    args = ap.parse_args()
    if args.mutate:
        global MUTATE
        MUTATE = True
    log = sys.stdout
    print(f"rbf_kill.py args={vars(args)}", file=log, flush=True)
    t0 = time.time()
    if "gate" not in args.skip:
        gate(args.gate_n, log)
    if "X" not in args.skip:
        st = run_exhaustive(args.umax, args.fut, log)
        print(f"X exhaustive: all binary words of length u <= {args.umax}, all n <= u: {st['cols']} (word, n) pairs, "
              f"checks A B C C' D1 D2 D3 PASS; {st['pairs']} distinct (n,u,Z_(u-1),Z_u) keys; "
              f"Z_(u-1) alone: {st['single_keys']} keys, {st['single_collisions']} with >1 column, max {st['single_worst']}; "
              f"mean non-retained runs per column {st['slack_zero_runs']/st['cols']:.3f}", file=log, flush=True)
    if "R" not in args.skip:
        st = run_random(args.rand_n, args.samples, args.seed, log)
        for n, s in st.items():
            print(f"R random n={n}: {s['cols']} (word, n) pairs, checks A B C C' D1 D2 D3 PASS; {s['pairs']} distinct pair keys; "
                  f"mean non-retained runs per column {s['slack_zero_runs']/s['cols']:.3f}", file=log, flush=True)
    if "L" not in args.skip:
        st = run_letters(args.letters_m, args.letters_m4, log)
        print(f"L letter space: {st['words']} three-letter windows m <= {args.letters_m}: Moore = kernel PASS; "
              f"odd-indexed even-bit flips {st['odd_flips']} all invisible PASS; even-indexed flips {st['even_flips']} all visible PASS; "
              f"{st['words4']} four-state windows m <= {args.letters_m4}: 3 = 1 PASS", file=log, flush=True)
    if "E" not in args.skip:
        balance(args.balance_brute, args.balance_transfer, log)
        print(f"E balance: #Phi=0 on {{0,2,x}}^m equals (3^m+1)/2 for m <= {args.balance_transfer} (transfer), "
              f"brute force through the kernel rule for m <= {args.balance_brute} PASS", file=log, flush=True)
    print(f"ALL PASS   [{time.time()-t0:.0f}s]", file=log, flush=True)


if __name__ == "__main__":
    main()

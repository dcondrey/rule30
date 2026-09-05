#!/usr/bin/env python3
"""Adversarial compute check of the lemma retained-bit-form (a) to (e), written
independently of rbf_structural_checks.py and of qf_common.py.

Everything is recomputed from scratch here: the rule CONE is rebuilt from the
carry-action definition and compared with psi_kernel.CONE; the triangle is a
fresh list-based implementation; the lemma's predictions are computed from the
window alone and compared with the actual next column; the pair (Z_(u-1), Z_u)
is decoded by the explicit D2/D3 formulas (not by a collision dictionary) and
the decoded column is compared cell by cell; the second-order recursion
Z_(u+1) = Psi(Z_(u-1), Z_u) is checked by decoding, extending, and comparing.

Families (all beyond the screened range u <= 14 of S5 and n <= 9 of q2_gate):
  A  random binary sources, forced orbit to u = 4n              (n = 20..100)
  B  structured sources (constant, periodic, Thue-Morse, Fibonacci, hard-core,
     the n = 15 falsifier and its continuation), forced orbit to u = 3n + 2
  C  arbitrary binary words (not forced), random u in [30, 60], all n <= u
  D  four-state random prefixes, all four e_u: Lemma H and Lemma E (by-product)
  E  exhaustive forced orbits n = NE_LO..NE_HI, u = n .. 2n + 3   (--exhaustive)
  F  relaxed balance (e): exact transfer matrix to m = 400, brute-force
     involution census to m = 13
  G  controls: --mutate odd (retained := odd-indexed) and --mutate const
     (drop the retained-zero constant) must fire

Any AssertionError kills.  The tuple names the check and the witness.

Run:  cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant \
      && uv run python uc/r1-quadratic-prove-retained-bit-form-structural-verify-compute/rbf_adversarial.py
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

import psi_kernel  # noqa: E402

MUTATE = None   # None, "odd", "const"

# ---------------------------------------------------------------------------
# 0. the rule, rebuilt from the carry action and compared with the kernel
# ---------------------------------------------------------------------------


def _carry(symbol: int, state: int) -> int:
    a, b = symbol >> 1, symbol & 1
    c, d = state >> 1, state & 1
    return 2 * (c ^ (a | b)) + (d ^ (c | a))


def _swap(s: int) -> int:
    return 2 * (s & 1) + (s >> 1)


def rebuild_cone():
    forward = [[_carry(sym, st) for st in range(4)] for sym in range(4)]
    inverse = []
    for row in forward:
        inv = [0] * 4
        for st, nxt in enumerate(row):
            inv[nxt] = st
        inverse.append(inv)
    cone = tuple(tuple(inverse[_swap(l)][r] for r in range(4)) for l in range(4))
    boundary = tuple(inverse[3])
    return cone, boundary


CONE, BOUNDARY = rebuild_cone()


def H(t: int) -> int:
    return t >> 1


def Lo(t: int) -> int:
    return t & 1


def E(t: int) -> int:
    return (1 + (t >> 1) + (t & 1)) & 1


def check_rule() -> None:
    assert CONE == tuple(tuple(r) for r in psi_kernel.CONE), ("rule", CONE, psi_kernel.CONE)
    assert BOUNDARY == tuple(psi_kernel.BOUNDARY), ("boundary", BOUNDARY)
    for l in range(4):
        for r in range(4):
            t = CONE[l][r]
            assert H(t) == (H(r) + 1 + (l == 0)) & 1, ("F1-H", l, r, t)
            assert E(t) == (E(r) + H(r) * (Lo(l) == 0)) & 1, ("F1-E", l, r, t)
    for s in range(4):
        assert BOUNDARY[s] == s ^ 3 == CONE[3][s], ("F2", s)


# ---------------------------------------------------------------------------
# 1. the triangle: column u is a list col with col[d + u + 1] = T[u][d], d in [-u-1, u]
# ---------------------------------------------------------------------------


def next_column(prev: list[int], e: int) -> list[int]:
    """Column u from column u-1 (prev, length 2u) and the symbol e_u."""
    u = len(prev) // 2
    new = [e, e ^ 3]
    for d in range(-u + 1, u + 1):
        new.append(CONE[prev[d - 1 + u]][new[-1]])
    return new


def columns_of(word) -> list[list[int]]:
    cols = []
    prev: list[int] = []
    for e in word:
        prev = next_column(prev, e)
        cols.append(prev)
    return cols


def forced_symbol(prev: list[int], n: int) -> tuple[int, list[int]]:
    """The unique binary e_u with H(T[u][n]) = 1, and column u; asserts uniqueness."""
    u = len(prev) // 2
    assert n <= u, ("n>u", n, u)
    found = []
    for s in (1, 2):
        col = next_column(prev, s)
        if H(col[n + u + 1]) == 1:
            found.append((s, col))
    assert len(found) == 1, ("forcing-not-unique", n, u, [f[0] for f in found])
    return found[0]


# ---------------------------------------------------------------------------
# 2. the lemma's ordered object on a window (index j = d + u, bottom j = 0)
# ---------------------------------------------------------------------------


class Window:
    __slots__ = ("m", "N", "qs", "retained", "z", "w", "runs", "F", "K")

    def __init__(self, cells: list[int]):
        m = len(cells)
        qs = [j for j in range(m - 1, -1, -1) if cells[j] != 0]
        N = len(qs)
        retained = [False] * m
        for i, j in enumerate(qs, start=1):
            retained[j] = (i % 2 == 0) if MUTATE != "odd" else (i % 2 == 1)
        above = True
        for j in range(m - 1, -1, -1):
            if cells[j] != 0:
                above = retained[j]
            else:
                retained[j] = above
        z = [0] * (N + 1)
        z[0] = (m - 1 - qs[0]) if N else m
        for i in range(1, N + 1):
            bottom = qs[i] if i < N else -1
            z[i] = qs[i - 1] - bottom - 1
        w = [None] + [1 if cells[j] == 2 else 0 for j in qs]
        runs = []
        for i in range(1, N + 1, 2):
            bottom = qs[i] if i < N else -1
            runs.append(list(range(qs[i - 1], bottom, -1)))
        K = len(runs)
        F = []
        for k in range(K):
            F.append(sum(z[2 * j] + w[2 * j] for j in range(k + 1, N // 2 + 1)) & 1)
        self.m, self.N, self.qs, self.retained, self.z, self.w, self.runs, self.F, self.K = \
            m, N, qs, retained, z, w, runs, F, K

    def phi(self) -> int:
        v = self.z[0] + sum(self.z[i] + self.w[i] for i in range(2, self.N + 1, 2))
        if MUTATE == "const":
            v += self.z[0]
        return v & 1


def predicted_zero_set(win: Window, u: int) -> set[int]:
    """Z_u on [-u-1, n-1] as a set of depths: the runs R_k with F_k = 1."""
    out = set()
    for k, run in enumerate(win.runs):
        if win.F[k] == 1:
            out.update(j - u for j in run)
    return out


def decode_pair(n: int, u: int, Zprev: set[int], Zu: set[int]) -> list[int]:
    """D2/D3: column u on [-u-1, n] from the two zero patterns alone (depth sets).
    Returns a list col with col[d + u + 1] = T[u][d] for d in [-u-1, n]."""
    m = n + u
    pseudo = [0 if (j - u) in Zprev else 1 for j in range(m)]
    win = Window(pseudo)
    # F_k read from Z_u: R_k entirely inside or entirely outside
    F = []
    for run in win.runs:
        inside = [(j - u) in Zu for j in run]
        assert all(inside) or not any(inside), ("decode-partial-run", n, u, run)
        F.append(1 if inside[0] else 0)
    for d in Zu:
        j = d + u
        assert 0 <= j < m and not win.retained[j], ("decode-zero-outside-runs", n, u, d)
    F.append(0)   # F_K = 0
    w = [None] * (win.N + 1)
    for k in range(win.K):
        i = 2 * k + 2
        if i > win.N:
            break
        w[i] = (F[k] + F[k + 1] + win.z[i]) & 1
    # E profile by (6.1); H profile by (b)
    head_index = {j: i for i, j in enumerate(win.qs, start=1)}
    col = [1 + (win.N % 2)]          # e_u = 1 + [N odd]
    Eacc = 0
    for j in range(m):
        h = 1 if win.retained[j] else 0
        col.append(2 * h + ((1 + h + Eacc) & 1))
        if win.retained[j]:
            if pseudo[j] == 0:
                Eacc ^= 1
            else:
                i = head_index[j]
                assert i % 2 == 0
                Eacc ^= w[i]
    col.append(2 + Eacc)             # T[u][n]: H = 1, E = Phi
    return col


# ---------------------------------------------------------------------------
# 3. the per-column check of (a) to (d)
# ---------------------------------------------------------------------------


def check_column(prev: list[int], n: int, do_toggles: bool, stats: dict, tag) -> list[int]:
    """prev = column u-1 (list, length 2u).  Returns actual column u (forced)."""
    u = len(prev) // 2
    m = n + u
    window = prev[:m]
    assert window[0] != 0, ("bottom-zero", tag)
    e_u, cur = forced_symbol(prev, n)
    win = Window(window)
    # (a)
    assert (e_u == 2) == (win.N % 2 == 1), ("a", tag, n, u, e_u, win.N)
    # (b)
    for j in range(m):
        assert H(cur[j + 1]) == (1 if win.retained[j] else 0), ("b", tag, n, u, j - u)
    assert H(cur[m + 1]) == 1, ("b-pin", tag, n, u)
    # (c)
    assert win.phi() == E(cur[m + 1]), ("c", tag, n, u)
    # (d1) zero set of column u on [-u-1, n-1] = runs with F_k = 1
    actual_Zu = {d for d in range(-u - 1, n) if cur[d + u + 1] == 0}
    assert actual_Zu == predicted_zero_set(win, u), ("d1", tag, n, u, sorted(actual_Zu))
    # E_u constant on runs, equal to F_k
    for k, run in enumerate(win.runs):
        for j in run:
            assert E(cur[j + 1]) == win.F[k], ("d1-F", tag, n, u, k, j - u)
    # (d2, d3) decode the pair and compare the column on [-u-1, n]
    Zprev = {j - u for j in range(m) if window[j] == 0}
    decoded = decode_pair(n, u, Zprev, actual_Zu)
    assert decoded == cur[: m + 2], ("d3", tag, n, u, decoded, cur[: m + 2])
    # second-order recursion: decoded column u on [-u-1, n-1] is the next window
    e_next, nxt = forced_symbol(cur, n)
    win2 = Window(decoded[: m + 1])
    assert (e_next == 2) == (win2.N % 2 == 1), ("psi-e", tag, n, u)
    actual_Znext = {d for d in range(-u - 2, n) if nxt[d + u + 2] == 0}
    assert actual_Znext == predicted_zero_set(win2, u + 1), ("psi-Z", tag, n, u)
    stats["columns"] += 1
    stats["zeros_prev"] += len(Zprev)
    stats["N"] += win.N
    # (d5) toggles of the even-bits on the full column u-1, free window
    if do_toggles:
        for i, j in enumerate(win.qs, start=1):
            mod = prev[:]
            mod[j] = 2 if mod[j] in (1, 3) else 1
            e_m, col_m = forced_symbol(mod, n)
            assert e_m == e_u, ("d5-symbol", tag, n, u, i)
            if i % 2 == 1:
                assert col_m == cur, ("d5-odd-read", tag, n, u, i, j - u)
                stats["odd_flips"] += 1
            else:
                assert col_m[: j + 2] == cur[: j + 2], ("d5-even-below", tag, n, u, i)
                assert all(col_m[k] != cur[k] for k in range(j + 2, m + 2)), ("d5-even-above", tag, n, u, i)
                stats["even_flips"] += 1
    return cur


def new_stats() -> dict:
    return {"columns": 0, "zeros_prev": 0, "N": 0, "odd_flips": 0, "even_flips": 0, "sources": 0}


def run_orbit(src, n: int, u_max: int, stats: dict, toggle_every: int, tag) -> None:
    cols = columns_of(src)
    prev = cols[-1]
    u = len(src)
    assert u == n
    k = 0
    while u <= u_max:
        cur = check_column(prev, n, do_toggles=(toggle_every > 0 and k % toggle_every == 0), stats=stats, tag=tag)
        prev = cur
        u += 1
        k += 1
    stats["sources"] += 1


# ---------------------------------------------------------------------------
# 4. families
# ---------------------------------------------------------------------------


def family_A(log, rng: random.Random) -> None:
    plan = [(20, 300), (30, 150), (45, 80), (64, 40), (100, 12)]
    for n, samples in plan:
        st = new_stats()
        t0 = time.time()
        for s in range(samples):
            src = tuple(rng.choice((1, 2)) for _ in range(n))
            run_orbit(src, n, 4 * n, st, toggle_every=7, tag=("A", n, s))
        print(f"A n={n:<4} {samples} random sources, forced orbit u=n..4n: {st['columns']} columns, "
              f"mean zeros/window={st['zeros_prev']/st['columns']:.2f}, mean |N|={st['N']/st['columns']:.1f}, "
              f"odd flips invisible {st['odd_flips']}, even flips visible {st['even_flips']} PASS  [{time.time()-t0:.0f}s]",
              file=log, flush=True)


def thue_morse(n: int):
    return tuple(1 + (bin(i).count("1") & 1) for i in range(n))


def fibonacci_word(n: int):
    a, b = (1,), (1, 2)
    while len(b) < n:
        a, b = b, b + a
    return b[:n]


def hardcore_random(n: int, rng: random.Random):
    out = []
    for i in range(n):
        if out and out[-1] == 1:
            out.append(2)
        else:
            out.append(rng.choice((1, 2)))
    return tuple(out)


def structured_sources(n: int, rng: random.Random):
    yield "1^n", (1,) * n
    yield "2^n", (2,) * n
    yield "(12)*", tuple(1 + (i % 2) for i in range(n))
    yield "(21)*", tuple(2 - (i % 2) for i in range(n))
    yield "(112)*", tuple((1, 1, 2)[i % 3] for i in range(n))
    yield "(122)*", tuple((1, 2, 2)[i % 3] for i in range(n))
    yield "(1122)*", tuple((1, 1, 2, 2)[i % 4] for i in range(n))
    yield "(1222)*", tuple((1, 2, 2, 2)[i % 4] for i in range(n))
    yield "(211212112)*", tuple((2, 1, 1, 2, 1, 2, 1, 1, 2)[i % 9] for i in range(n))
    yield "2^(n-1)1", (2,) * (n - 1) + (1,)
    yield "12^(n-1)", (1,) + (2,) * (n - 1)
    yield "1^(n-1)2", (1,) * (n - 1) + (2,)
    yield "thue-morse", thue_morse(n)
    yield "fibonacci", fibonacci_word(n)
    yield "hardcore-random", hardcore_random(n, rng)


def family_B(log, rng: random.Random) -> None:
    for n in (16, 24, 33, 50, 71, 100):
        st = new_stats()
        t0 = time.time()
        names = []
        for name, src in structured_sources(n, rng):
            assert len(src) == n
            run_orbit(src, n, 3 * n + 2, st, toggle_every=5, tag=("B", name, n))
            names.append(name)
        print(f"B n={n:<4} {len(names)} structured sources, forced orbit u=n..3n+2: {st['columns']} columns, "
              f"odd flips invisible {st['odd_flips']}, even flips visible {st['even_flips']} PASS  [{time.time()-t0:.0f}s]",
              file=log, flush=True)
    # the recorded n = 15 falsifier of the sharp bound, with its continuation as a prefix
    src = tuple(map(int, "111122211212112"))
    cont = tuple(map(int, "12211111122111211"))
    st = new_stats()
    run_orbit(src, 15, 60, st, toggle_every=1, tag=("B", "falsifier", 15))
    # its 32-symbol word as an arbitrary binary prefix for every n <= 32
    cols = columns_of(src + cont)
    for n in range(1, 33):
        check_column(cols[31], n, True, st, ("B", "falsifier-prefix", n))
    print(f"B n=15 falsifier 111122211212112 orbit to u=60 and its 32-symbol word for all n<=32: "
          f"{st['columns']} columns, odd flips invisible {st['odd_flips']}, even flips visible {st['even_flips']} PASS",
          file=log, flush=True)


def family_C(log, rng: random.Random) -> None:
    st = new_stats()
    t0 = time.time()
    words = 0
    for s in range(150):
        u = rng.randint(30, 60)
        word = tuple(rng.choice((1, 2)) for _ in range(u))
        cols = columns_of(word)
        prev = cols[u - 1]
        for n in range(1, u + 1):
            check_column(prev, n, do_toggles=(n % 6 == 0), stats=st, tag=("C", s, n))
        words += 1
    print(f"C {words} arbitrary binary words u in [30,60], every n<=u: {st['columns']} (word, n) pairs, "
          f"odd flips invisible {st['odd_flips']}, even flips visible {st['even_flips']} PASS  [{time.time()-t0:.0f}s]",
          file=log, flush=True)


def family_D(log, rng: random.Random) -> None:
    cells = 0
    t0 = time.time()
    for s in range(200):
        u = rng.randint(20, 40)
        prefix = tuple(rng.randrange(4) for _ in range(u))
        prev = columns_of(prefix)[-1]
        for e_u in range(4):
            cur = next_column(prev, e_u)
            zeros = 0
            ev = 0
            for d in range(-u, u + 1):
                t = cur[d + u + 1]
                assert H(t) == (H(e_u) + d + u + 1 + zeros) & 1, ("LemmaH", s, e_u, d)
                assert E(t) == (E(e_u) + ev) & 1, ("LemmaE", s, e_u, d)
                cells += 1
                if d < u:
                    left = prev[d + u]
                    zeros += left == 0
                    ev += (H(t) == 1 and Lo(left) == 0)
    print(f"D Lemma H and Lemma E on {cells} cells of 200 random four-state prefixes u in [20,40], all four e_u PASS  "
          f"[{time.time()-t0:.0f}s]", file=log, flush=True)


def family_E(log, lo: int, hi: int) -> None:
    for n in range(lo, hi + 1):
        st = new_stats()
        t0 = time.time()
        for src in product((1, 2), repeat=n):
            run_orbit(src, n, 2 * n + 3, st, toggle_every=0, tag=("E", n))
        print(f"E n={n:<3} exhaustive {st['sources']} sources, forced orbit u=n..2n+3: {st['columns']} columns PASS  "
              f"[{time.time()-t0:.0f}s]", file=log, flush=True)


def family_F(log, m_transfer: int, m_brute: int) -> None:
    # exact transfer matrix on states (h, F); letters odd (0,0), two (0,1), zero (1,1)
    letters = [(0, 0), (0, 1), (1, 1)]
    states = [(0, 0), (0, 1), (1, 0), (1, 1)]
    idx = {s: i for i, s in enumerate(states)}
    A = [[0] * 4 for _ in range(4)]
    for s in states:
        h, F = s
        for a, b in letters:
            t = (h ^ 1 ^ a, F ^ (h & b))
            A[idx[s]][idx[t]] += 1
    P = [[int(i == j) for j in range(4)] for i in range(4)]
    for m in range(1, m_transfer + 1):
        P = [[sum(P[i][k] * A[k][j] for k in range(4)) for j in range(4)] for i in range(4)]
        n0 = sum(P[idx[(h0, 0)]][idx[(1, 0)]] for h0 in (0, 1))
        n1 = sum(P[idx[(h0, 0)]][idx[(1, 1)]] for h0 in (0, 1))
        assert n0 + n1 == 3 ** m, ("F-total", m)
        assert n0 == (3 ** m + 1) // 2 and n0 - n1 == 1, ("F-transfer", m, n0, n1)
    print(f"F (e) transfer matrix: N0 = (3^m+1)/2 exactly for every m <= {m_transfer} (exact integers) PASS", file=log, flush=True)
    # brute force with the involution and the block formula, independent of Window
    for m in range(1, m_brute + 1):
        n0 = n1 = 0
        small = [0, 0]
        for word in product((0, 1, 2), repeat=m):    # bottom first; 1 = odd letter x
            N = sum(1 for t in word if t)
            h, F = (1 + N) & 1, 0
            for t in word:
                a, b = (t == 0), (t != 1)
                F ^= h & b
                h ^= 1 ^ a
            assert h == 1
            win = Window(list(word))
            assert win.phi() == F, ("F-block", word)
            if F == 0:
                n0 += 1
            else:
                n1 += 1
            if N >= 2:
                j = win.qs[1]
                partner = list(word)
                partner[j] = 2 if partner[j] == 1 else 1
                assert Window(partner).phi() == 1 - F, ("F-invol", word)
            else:
                small[F] += 1
        assert small == [(m % 2 == 0) + 2 * ((m + 1) // 2), (m % 2 == 1) + 2 * (m // 2)], ("F-small", m, small)
        assert n0 - n1 == 1 and n0 == (3 ** m + 1) // 2, ("F-brute", m, n0, n1)
    print(f"F (e) brute force with block formula and q_2 involution to m = {m_brute} "
          f"({3 ** m_brute} words at the top) PASS", file=log, flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--families", default="ABCDF")
    ap.add_argument("--exhaustive", nargs=2, type=int, metavar=("LO", "HI"), default=None)
    ap.add_argument("--m-transfer", type=int, default=400)
    ap.add_argument("--m-brute", type=int, default=13)
    ap.add_argument("--mutate", choices=["odd", "const"], default=None)
    args = ap.parse_args()
    global MUTATE
    MUTATE = args.mutate
    log = sys.stdout
    print(f"rbf_adversarial.py args={vars(args)}", file=log, flush=True)
    t0 = time.time()
    check_rule()
    print("rule: CONE rebuilt from the carry action equals psi_kernel.CONE; F1 decoupling and F2 boundary on all 16 pairs PASS",
          file=log, flush=True)
    rng = random.Random(args.seed)
    if "A" in args.families:
        family_A(log, rng)
    if "B" in args.families:
        family_B(log, rng)
    if "C" in args.families:
        family_C(log, rng)
    if "D" in args.families:
        family_D(log, rng)
    if "F" in args.families:
        family_F(log, args.m_transfer, args.m_brute)
    if args.exhaustive:
        family_E(log, args.exhaustive[0], args.exhaustive[1])
    print(f"ALL PASS  [{time.time()-t0:.0f}s]", file=log, flush=True)


if __name__ == "__main__":
    main()

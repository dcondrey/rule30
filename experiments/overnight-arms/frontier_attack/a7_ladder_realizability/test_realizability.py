"""Tests for the two lemmas the construction rests on, plus regressions.

Lemma P (left permutivity, control form): flipping s(0,-t) flips s(t,0) and
changes no s(t',0) with t' < t.
Lemma W (wedge automaticity): with s(0,x)=0 for -2k <= x <= -1, s(0,0)=1 and
s(0,x)=0 for x >= 1, every ladder wedge/edge check on columns x in [-k,R]
takes its lone-seed value for EVERY assignment of the free bits x <= -(2k+1).
"""

from __future__ import annotations

import itertools
import random

import numpy as np

import ladder_copy as L
from realize import build, min_eventual_period, rowsim

RULES = (30, 90)


def evolve(rule, row0, lo, T):
    """row0 is a dict x -> bit; simulate on [lo, lo+len] wide enough."""
    hi = max(row0) + T + 4
    lo = lo - T - 4
    n = hi - lo + 1
    row = np.zeros(n, dtype=np.uint8)
    for x, v in row0.items():
        if lo <= x <= hi:
            row[x - lo] = v
    out = []
    for t in range(T + 1):
        out.append(row.copy())
        l, r = np.roll(row, 1), np.roll(row, -1)
        row = (l ^ (row | r)) if rule == 30 else (l ^ r)
        row[0] = 0
        row[-1] = 0
    return out, lo


def test_lemma_permutivity_flip():
    rng = random.Random(7)
    for rule in RULES:
        for _ in range(40):
            T = 12
            base = {x: rng.randint(0, 1) for x in range(-2 * T, T + 2)}
            g, lo = evolve(rule, base, -2 * T, T)
            for t in range(1, T + 1):
                alt = dict(base)
                alt[-t] ^= 1
                h, lo2 = evolve(rule, alt, -2 * T, T)
                assert h[t][0 - lo2] != g[t][0 - lo], (rule, t)
                for tp in range(t):
                    assert h[tp][0 - lo2] == g[tp][0 - lo], (rule, t, tp)


def test_lemma_wedge_automatic_exhaustive():
    """All 2^m free-bit assignments leave every wedge/edge check at its
    lone-seed value, for k = 1,2,3 and R up to 6."""
    for rule in RULES:
        for k in (1, 2, 3):
            m = 8
            R = 6
            for bits in itertools.product((0, 1), repeat=m):
                row0 = {0: 1}
                for x in range(1, R + 4):
                    row0[x] = 0
                for x in range(-2 * k, 0):
                    row0[x] = 0
                for i, bv in enumerate(bits):
                    row0[-(2 * k + 1) - i] = bv
                g, lo = evolve(rule, row0, -(2 * k + m + 2), R + 2)
                for x in range(-k, R + 1):
                    ax = abs(x)
                    for t in range(ax + 1):
                        v = int(g[t][x - lo])
                        assert v == (1 if t == ax else 0), (rule, k, x, t, bits)


def test_construction_matches_row_simulation():
    for rule in RULES:
        for k in (1, 2, 3):
            for w in ("01", "0011", "1"):
                word = tuple(int(c) for c in w)
                T = 300
                xlo, xhi = -k - 2, 10
                b = build(rule, k, word, T, xlo, xhi)
                sim = rowsim(rule, b["row0"], T, xlo, xhi, margin=4)
                for x in range(xlo, xhi + 1):
                    assert np.array_equal(sim[x], b["cols"][x][:T + 1]), (rule, k, w, x)


def test_centre_hits_target():
    for rule in RULES:
        for k in (1, 2, 4):
            for w in ("01", "001", "01011"):
                word = tuple(int(c) for c in w)
                b = build(rule, k, word, 600, -k - 2, 8)
                T0 = b["T0"]
                assert T0 == 2 * k + 1
                for t in range(T0, 601):
                    assert b["cols"][0][t] == word[(t - T0) % len(word)]


def test_real_ladder_accepts_prefix():
    """Drive the untouched ladder engine; safety is decided by t < saturate."""
    for rule in RULES:
        for k in (1, 2, 3):
            word = (0, 1)
            b = build(rule, k, word, 400, -k - 2, 14)
            for R in range(1, 12):
                P = L.Params(rule=rule, right_depth=R, left_depth=k,
                             period_word=word, diff_q=1)
                window, cnt = (), 0
                for t in range(P.saturate + 8):
                    letter = (int(b["cols"][R - 1][t]) << 1) | int(b["cols"][R][t])
                    hit = L.step_window(window, cnt, letter, P)
                    assert hit is not None, (rule, k, R, t)
                    window = hit[0]
                    cnt += 1


def test_p1_calibrations_reproduce_rung0():
    """w=1 and w=0 must make col_-1 eventually 1-periodic (mode-ii EMPTY at
    p=1), and w=1 must give the checkerboard left half (register row 26)."""
    b1 = build(30, 2, (1,), 800, -6, 6)
    m1 = b1["cols"][-1]
    assert np.all(m1[9:] == 0)
    for x in range(-5, 1):
        assert int(b1["cols"][x][790]) == (1 if x % 2 == 0 else 0)
    b0 = build(30, 2, (0,), 800, -6, 6)
    c1 = b0["cols"][1]
    assert np.all(c1[9:] == c1[9])
    assert min_eventual_period(b0["cols"][-1], 64, 9) == 1


def test_p2_col_m1_has_no_short_eventual_period():
    """Finite-horizon: not a proof of aperiodicity, a regression pin."""
    b = build(30, 2, (0, 1), 4000, -4, 6)
    assert min_eventual_period(b["cols"][-1], 256, 9) is None

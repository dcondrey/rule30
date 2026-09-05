"""Shared helpers for the r1-r1zero lens (forward Rule 30 diagram, zero set).

Rule 30 convention used throughout this repo:
    s(t+1, x) = s(t, x-1) XOR (s(t, x) OR s(t, x+1)).
Rows are Python ints; bit index i holds s(t, i - OFF) for the full diagram.
"""
from __future__ import annotations

import random


def rule30_step(row: int) -> int:
    return (row << 1) ^ (row | (row >> 1))


def rule90_step(row: int) -> int:
    return (row << 1) ^ (row >> 1)


def lone_seed_rows(T: int, step=rule30_step):
    """Yield (t, row, off) for t = 0..T with the seed at bit ``off``."""
    off = T + 2
    row = 1 << off
    for t in range(T + 1):
        yield t, row, off
        row = step(row)


def lone_seed_columns(T: int, xs, step=rule30_step):
    """Return {x: [s(t,x) for t in 0..T]} for the requested columns."""
    cols = {x: [] for x in xs}
    for t, row, off in lone_seed_rows(T, step):
        for x in xs:
            cols[x].append((row >> (off + x)) & 1)
    return cols


def driven_rhp(c, T: int, step=rule30_step):
    """Right half-plane x >= 1 driven by boundary c_t at x = 0, zero initial data.

    Returns list of rows (ints) with bit x = s(t, x) for x >= 0 (bit 0 = c_t).
    Caller passes c as a callable t -> bit or a sequence of length > T.
    """
    rows = []
    row = c(0) if callable(c) else c[0]
    for t in range(T + 1):
        rows.append(row)
        nxt = step(row)
        ct1 = c(t + 1) if callable(c) else c[t + 1]
        nxt = (nxt & ~1) | ct1
        row = nxt
    return rows


def driven_lhp(c, T: int):
    """Left half-plane x <= -1 driven by boundary c_t at x = 0, zero initial data.

    Bit index i holds s(t, -i); bit 0 = c_t.  Rule in mirrored index:
        new[i] = old[i+1] XOR (old[i] OR old[i-1]).
    Returns list of rows.
    """
    rows = []
    row = c(0) if callable(c) else c[0]
    for t in range(T + 1):
        rows.append(row)
        nxt = (row >> 1) ^ (row | (row << 1))
        ct1 = c(t + 1) if callable(c) else c[t + 1]
        nxt = (nxt & ~1) | ct1
        row = nxt
    return rows


def eventual_period(seq, max_period: int, min_tail_frac: float = 0.5):
    """Smallest q <= max_period such that seq[i] == seq[i+q] for all i >= onset,
    with onset <= (1 - min_tail_frac) * len(seq).  Returns (q, onset) or None.
    """
    n = len(seq)
    limit = int((1 - min_tail_frac) * n)
    for q in range(1, max_period + 1):
        onset = 0
        for i in range(n - q - 1, -1, -1):
            if seq[i] != seq[i + q]:
                onset = i + 1
                break
        if onset <= limit and n - onset >= 4 * q:
            return q, onset
    return None


def longest_shift_agreement(seq, max_shift: int):
    """For each shift q, the longest run of i with seq[i] == seq[i+q]; return max over q."""
    n = len(seq)
    best = (0, 0, 0)
    for q in range(1, max_shift + 1):
        run = 0
        for i in range(n - q):
            if seq[i] == seq[i + q]:
                run += 1
                if run > best[0]:
                    best = (run, q, i - run + 1)
            else:
                run = 0
    return best


def bernoulli(n: int, seed: int):
    rng = random.Random(seed)
    return [rng.getrandbits(1) for _ in range(n)]

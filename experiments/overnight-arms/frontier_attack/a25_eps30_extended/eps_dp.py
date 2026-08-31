"""a25: exact eps_30(m) far past m=16, by a prefix-trie dynamic program.

DEFINITION (identical to a21 `eps_theorem.py::eps` and a22
`independent_eps_check.py::eps_independent`; see PATH.md 9.4/9.5):

    Let g = (g_0..g_{m-1}) be the observed centre-column window
    (g_j = c_{t-m+j} = s(t-m+j, 0)) and let h = (h_0..h_m) be the hidden block
    (h_i = s(t-m, 1+i)).  Under Theorem U both are uniform and independent for
    t >= 2m+1.  Iterating the quarter-plane x >= 1 forward m steps driven by
    the boundary column g yields r_t = s(t,1) as a function F_g(h).  Then

        eps(m) = sum_{g} min(N(g), 2^{m+1}-N(g)) / 2^{2m+1},
        N(g)   = #{h : F_g(h) = 1}.

WHY THIS IS FASTER.  a21 and a22 both loop over all 2^m windows g and, for
each, evaluate over all 2^{m+1} hidden states: cost Theta(m^2 * 2^{2m+1}).
But the m windows are consumed one time step at a time, and after j steps the
surviving row has only m+1-j cells.  So walk the trie of window PREFIXES
breadth-first, carrying at each node a COUNT vector over rows of length
m+1-j.  At depth j there are 2^j nodes each holding 2^{m+1-j} counts:
exactly 2^{m+1} integers per level, independent of j.  Total work is
m * 2^{m+2} instead of 2^{2m+1}.  m=24 becomes cheaper than a21's m=13.

Rows are packed as integers, bit i = cell i, so one time step is

    R' = (((R << 1) | b) ^ (R | (R >> 1))) & ((1 << (L-1)) - 1)     [rule 30]
    R' = (((R << 1) | b) ^        (R >> 1)) & ((1 << (L-1)) - 1)     [rule 90]

ARITHMETIC.  All counts are exact machine integers (int64 / int32, never
float): the pushforward is done by stable-argsort + integer cumulative sums,
NOT by np.bincount(weights=...) which silently returns float64.  eps(m) is
returned as an exact (numerator, denominator=2^{2m+1}) pair and converted to
fractions.Fraction by the caller.

RULE 90 IS THE ORACLE.  eps_90(m) = 1/2 exactly at every m, i.e. numerator
exactly 2^{2m}.  Every rule-30 run is accompanied by the rule-90 run at the
same m, which catches masking / edge-handling errors at m values where no
published rule-30 reference value exists.

Usage:
    uv run python eps_dp.py selftest
    uv run python eps_dp.py run MMIN MMAX [--dtype 32|64]
"""

from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction

import numpy as np


def step_map(L: int, b: int, rule: int) -> np.ndarray:
    """Array T of length 2^L with T[R] = image of row R under one time step
    with boundary bit b.  Result rows have length L-1."""
    R = np.arange(1 << L, dtype=np.int64)
    mask = (1 << (L - 1)) - 1
    left = (R << 1) | b
    if rule == 30:
        mid = R | (R >> 1)
    elif rule == 90:
        mid = R >> 1
    else:
        raise ValueError(rule)
    return ((left ^ mid) & mask).astype(np.int64)


def _pushforward(C: np.ndarray, T: np.ndarray, nout: int) -> np.ndarray:
    """C has shape (nodes, 2^L).  Return (nodes, nout) with
    out[n, r] = sum_{R : T[R] = r} C[n, R].  Exact integer arithmetic."""
    order = np.argsort(T, kind="stable")
    sizes = np.bincount(T, minlength=nout)          # int64, no weights
    starts = np.concatenate(([0], np.cumsum(sizes)[:-1]))
    S = np.zeros((C.shape[0], C.shape[1] + 1), dtype=C.dtype)
    np.cumsum(C[:, order], axis=1, out=S[:, 1:])
    return S[:, starts + sizes] - S[:, starts]


def eps_exact(m: int, rule: int, dtype=np.int64, verbose: bool = False):
    """Return (numerator, denominator) of eps(m), exact."""
    L = m + 1
    # depth 0: one node (empty prefix), every hidden state has count 1.
    C = np.ones((1, 1 << L), dtype=dtype)
    for j in range(m):
        L = m + 1 - j
        nout = 1 << (L - 1)
        parts = [_pushforward(C, step_map(L, b, rule), nout) for b in (0, 1)]
        C = np.concatenate(parts, axis=0)   # node index = b * 2^j + old
        del parts
        if verbose:
            print(f"    depth {j+1}: C {C.shape}", file=sys.stderr, flush=True)
    assert C.shape == (1 << m, 2)
    tot = 1 << (m + 1)
    ones = C[:, 1].astype(object)
    assert int(C[:, 0].sum(dtype=np.int64) + C[:, 1].sum(dtype=np.int64)) == (1 << (2 * m + 1))
    num = int(np.minimum(C[:, 1], tot - C[:, 1]).sum(dtype=np.int64))
    del ones
    return num, 1 << (2 * m + 1)


# published values, copied verbatim from a22/independent_eps_check.py
# (which itself copied them from a21's eps_theorem_results.json).
PUBLISHED_NUM = [
    2, 8, 28, 112, 416, 1644, 6280, 24612,
    95840, 380412, 1507680, 5969532, 23733628, 94203568, 374847204, 1488690544,
]


def selftest() -> None:
    # 1. brute force, fully independent of the DP, for m <= 9.
    def brute(m: int, rule: int) -> tuple[int, int]:
        num = 0
        for g in range(1 << m):
            ones = 0
            for h in range(1 << (m + 1)):
                row = [(h >> i) & 1 for i in range(m + 1)]
                for j in range(m):
                    gj = (g >> j) & 1
                    new = []
                    for i in range(len(row) - 1):
                        left = gj if i == 0 else row[i - 1]
                        if rule == 30:
                            new.append(left ^ (row[i] | row[i + 1]))
                        else:
                            new.append(left ^ row[i + 1])
                    row = new
                ones += row[0]
            num += min(ones, (1 << (m + 1)) - ones)
        return num, 1 << (2 * m + 1)

    for rule in (30, 90):
        for m in range(1, 10):
            assert eps_exact(m, rule) == brute(m, rule), (rule, m)
    print("selftest: DP == brute force, m=1..9, rules 30 and 90  OK")

    # 2. published rule-30 numerators, m=1..16.
    bad = []
    for m in range(1, 17):
        num, den = eps_exact(m, 30)
        if num != PUBLISHED_NUM[m - 1]:
            bad.append((m, num, PUBLISHED_NUM[m - 1]))
    assert not bad, bad
    print("selftest: DP == published a21/a22 numerators, m=1..16  OK")

    # 3. rule 90 oracle.
    for m in range(1, 19):
        num, den = eps_exact(m, 90)
        assert num * 2 == den, (m, num, den)
    print("selftest: eps_90(m) == 1/2 exactly, m=1..18  OK")


def run(mmin: int, mmax: int, dtype) -> None:
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eps30_values.json")
    try:
        with open(path) as fh:
            store = json.load(fh)
    except FileNotFoundError:
        store = {"30": {}, "90": {}}
    for m in range(mmin, mmax + 1):
        for rule in (30, 90):
            t0 = time.time()
            num, den = eps_exact(m, rule, dtype=dtype, verbose=(m >= 22))
            dt = time.time() - t0
            f = Fraction(num, den)
            store[str(rule)][str(m)] = {"num": num, "den": den, "secs": round(dt, 3)}
            tag = ""
            if rule == 90:
                tag = "  [ORACLE ok]" if f == Fraction(1, 2) else "  [ORACLE FAIL]"
                assert f == Fraction(1, 2), (m, num, den)
            if rule == 30 and m <= 16:
                tag = "  [matches published]" if num == PUBLISHED_NUM[m - 1] else "  [MISMATCH]"
                assert num == PUBLISHED_NUM[m - 1], (m, num)
            print(f"rule {rule}  m={m:2d}  eps={float(f):.12f}  = {num}/{den}"
                  f"  ({dt:.2f}s){tag}", flush=True)
        with open(path, "w") as fh:
            json.dump(store, fh, indent=1, sort_keys=True)
    print(f"wrote {path}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        selftest()
    elif len(sys.argv) > 1 and sys.argv[1] == "run":
        dt = np.int32 if "--dtype" in sys.argv and sys.argv[sys.argv.index("--dtype") + 1] == "32" else np.int64
        run(int(sys.argv[2]), int(sys.argv[3]), dt)
    else:
        print(__doc__)

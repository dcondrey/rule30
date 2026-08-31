"""Explicit half-plane realizability for the R7 periodicity ladder.

Construction.  Fix a left depth k and a target tail word w.  Take the initial
row

    s(0,x) = 0            for x >= 1          (ladder right wedge)
    s(0,0) = 1                                 (seed)
    s(0,x) = 0            for -2k <= x <= -1   (matches the lone seed)
    s(0,x)               free  for x <= -(2k+1)

Rule 30 is left permutive, so s(t,0) = s(0,-t) XOR H_t(s(0,-t+1 .. t)):
flipping the bit at x = -t flips col_0(t) and disturbs no earlier time.  So
for t >= 2k+1 the free bit s(0,-t) can be chosen to force col_0(t) to any
prescribed value.  Every wedge/edge check the ladder imposes on columns
x in [-k, R] reads a cell s(t,x) with t <= |x| <= max(k,R), and such a cell
depends only on s(0, [-2k, 0]), so it equals its lone-seed value whatever the
free bits are.

Implementation is by diagonals.  With D_j(u) = s(u, u-j),

    D_j(u+1) = D_j(u) XOR (D_{j-1}(u) OR D_{j-2}(u))          [rule 30]
    D_j(u+1) = D_j(u) XOR  D_{j-2}(u)                          [rule 90]

and col_x(t) = D_{t-x}(t).  Streaming over j keeps memory O(T).
"""

from __future__ import annotations

import argparse
import json

import numpy as np


def diag_step_series(prev1: np.ndarray, prev2: np.ndarray, d0: int, rule: int) -> np.ndarray:
    """D_j given D_{j-1}, D_{j-2} and the seed bit D_j(0) = d0.

    D_j(u) = d0 XOR (XOR_{v<u} g(D_{j-1}(v), D_{j-2}(v))).
    """
    if rule == 30:
        g = prev1 | prev2
    elif rule == 90:
        g = prev2
    else:
        raise ValueError(rule)
    out = np.empty_like(prev1)
    out[0] = d0
    np.bitwise_xor.accumulate(g[:-1], out=out[1:])
    out[1:] ^= d0
    return out


def build(rule: int, k: int, word: tuple[int, ...], T: int, xlo: int, xhi: int,
          phase0: int = 0):
    """Greedy construction.

    Returns dict with the chosen free bits, the recorded columns col_x for
    x in [xlo, xhi], and the target col_0.

    col_0(t) is left at its lone-seed value for t < T0 = 2k+1 and forced to
    word[(t - T0 + phase0) % p] for t >= T0.
    """
    T0 = 2 * k + 1
    p = len(word)
    jmax = T + max(0, -xlo) + 2          # need D_j up to j = T - xlo
    n = jmax + 2                         # time samples 0..n-1

    # D_j for j < 0 is identically zero (right of the seed diagonal).
    zero = np.zeros(n, dtype=np.uint8)
    prev2 = zero.copy()                  # D_{j-2}
    prev1 = zero.copy()                  # D_{j-1}

    cols = {x: np.zeros(T + 1, dtype=np.uint8) for x in range(xlo, xhi + 1)}
    row0 = {}
    target = np.zeros(T + 1, dtype=np.uint8)

    for j in range(0, jmax + 1):
        if j == 0:
            d0 = 1
        elif j <= 2 * k:
            d0 = 0
        else:
            # free bit: force col_0(j) = D_j(j) = word[(j - T0 + phase0) % p]
            base = diag_step_series(prev1, prev2, 0, rule)
            want = int(word[(j - T0 + phase0) % p])
            d0 = int(base[j]) ^ want if j < n else 0
        cur = diag_step_series(prev1, prev2, d0, rule)
        row0[-j] = d0
        # col_x(t) = D_{t-x}(t)  ->  this diagonal supplies t = j + x
        for x in range(xlo, xhi + 1):
            t = j + x
            if 0 <= t <= T:
                cols[x][t] = cur[t]
        prev2, prev1 = prev1, cur

    for t in range(T + 1):
        target[t] = word[(t - T0 + phase0) % p] if t >= T0 else cols[0][t]
    return {"row0": row0, "cols": cols, "target": target, "T0": T0}


def rowsim(rule: int, row0: dict[int, int], T: int, xlo: int, xhi: int, margin: int):
    """Independent check: plain row-by-row simulation on a wide window."""
    lo = xlo - T - margin
    hi = xhi + T + margin
    n = hi - lo + 1
    row = np.zeros(n, dtype=np.uint8)
    for x in range(lo, hi + 1):
        row[x - lo] = row0.get(x, 0)
    cols = {x: np.zeros(T + 1, dtype=np.uint8) for x in range(xlo, xhi + 1)}
    for t in range(T + 1):
        for x in range(xlo, xhi + 1):
            cols[x][t] = row[x - lo]
        l = np.roll(row, 1)
        r = np.roll(row, -1)
        if rule == 30:
            row = l ^ (row | r)
        else:
            row = l ^ r
        row[0] = 0
        row[-1] = 0
    return cols


def min_eventual_period(seq: np.ndarray, qmax: int, drop: int):
    """Smallest q <= qmax with seq[t] == seq[t-q] for all t in the tail."""
    tail = seq[drop:]
    for q in range(1, qmax + 1):
        if len(tail) <= q:
            break
        if np.array_equal(tail[q:], tail[:-q]):
            return q
    return None


def diff_q_events(seq: np.ndarray, q: int, drop: int) -> int:
    tail = seq[drop:]
    if len(tail) <= q:
        return 0
    return int(np.count_nonzero(tail[q:] != tail[:-q]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule", type=int, default=30)
    ap.add_argument("-k", type=int, default=2)
    ap.add_argument("-w", default="01")
    ap.add_argument("-T", type=int, default=20000)
    ap.add_argument("--rmax", type=int, default=12)
    ap.add_argument("--qmax", type=int, default=256)
    ap.add_argument("--phase", type=int, default=0)
    ap.add_argument("--verify-T", type=int, default=1500)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()

    word = tuple(int(c) for c in a.w)
    k, T = a.k, a.T
    xlo, xhi = -k - 2, a.rmax + 1
    b = build(a.rule, k, word, T, xlo, xhi, a.phase)
    cols, T0 = b["cols"], b["T0"]

    rep = {"rule": a.rule, "k": k, "w": a.w, "T": T, "T0": T0, "phase": a.phase}

    # ---- 1. centre column hits the prescribed tail -------------------------
    ok_centre = bool(np.array_equal(cols[0], b["target"]))
    rep["centre_matches_target"] = ok_centre
    print(f"[centre] col_0 == lone-seed prefix + tail {a.w} from t={T0}: {ok_centre}")

    # ---- 2. independent row simulation ------------------------------------
    Tv = min(a.verify_T, T)
    sim = rowsim(a.rule, b["row0"], Tv, xlo, xhi, margin=4)
    mism = {x: int(np.count_nonzero(sim[x] != cols[x][:Tv + 1]))
            for x in range(xlo, xhi + 1)}
    bad = {x: v for x, v in mism.items() if v}
    rep["rowsim_T"] = Tv
    rep["rowsim_mismatches"] = bad
    print(f"[rowsim] diagonal vs row simulation, x in [{xlo},{xhi}], T={Tv}: "
          f"{'0 mismatches' if not bad else bad}")

    # ---- 3. wedge / edge on the modelled columns --------------------------
    wedge_bad = []
    unconstrained = []
    for x in range(xlo, xhi + 1):
        if x < -k:
            ax = abs(x)
            for t in range(0, min(ax, T) + 1):
                v = int(cols[x][t])
                if (t < ax and v != 0) or (t == ax and v != 1):
                    unconstrained.append((x, t, v))
            continue
        ax = abs(x)
        for t in range(0, min(ax, T) + 1):
            v = int(cols[x][t])
            if t < ax and v != 0:
                wedge_bad.append((x, t, v, 0))
            if t == ax and v != 1:
                wedge_bad.append((x, t, v, 1))
    rep["wedge_violations"] = wedge_bad
    rep["outside_ladder_scope"] = unconstrained
    print(f"[wedge] light-cone + both edges on the ladder-modelled columns "
          f"x in [{-k},{xhi}]: {len(wedge_bad)} violations "
          f"({len(unconstrained)} deviations at x < -k, outside ladder scope)")

    # ---- 4. col_{-1} periodicity and Diff_q -------------------------------
    m1 = cols[-1]
    drop = T0 + 4
    mp = min_eventual_period(m1, a.qmax, drop)
    rep["col_m1_min_eventual_period_le_qmax"] = mp
    rep["qmax"] = a.qmax
    diffs = {q: diff_q_events(m1, q, drop) for q in range(1, min(a.qmax, 32) + 1)}
    rep["diff_events"] = diffs
    print(f"[col_-1] smallest eventual period <= {a.qmax} on t>={drop}: {mp}")
    print(f"[col_-1] Diff_q event counts q=1..8: "
          f"{[diffs[q] for q in range(1, 9)]}")

    # ---- 5. the i.o. lemma's finite shadow: col_1 on the col_0 zero set ----
    if len(word) == 2:
        zs = np.where(cols[0][drop:] == 0)[0] + drop
        ones = int(np.count_nonzero(cols[1][zs]))
        rep["col1_on_centre_zeroset"] = {"n": int(len(zs)), "ones": ones,
                                         "density": ones / max(1, len(zs))}
        last = int(zs[np.where(cols[1][zs] == 1)[0][-1]]) if ones else None
        rep["col1_last_one_on_zeroset"] = last
        print(f"[io-lemma] col_1 = 1 on {ones}/{len(zs)} of the col_0 zero set "
              f"(density {ones/max(1,len(zs)):.4f}), last at t={last}")
    # w = 0 calibration: col_1 eventually constant?
    if word == (0,):
        c1 = cols[1]
        rep["col1_min_eventual_period_le_qmax"] = min_eventual_period(c1, a.qmax, drop)
        tailconst = bool(np.all(c1[drop:] == c1[drop]))
        rep["col1_eventually_constant"] = tailconst
        print(f"[calib w=0] col_1 eventually constant from t={drop}: {tailconst} "
              f"(value {int(c1[drop])})")
    if word == (1,):
        rep["col_m1_eventually_zero"] = bool(np.all(m1[drop:] == 0))
        print(f"[calib w=1] col_-1 eventually 0: {rep['col_m1_eventually_zero']}")
        # checkerboard left half at late time
        tl = T - 2
        cb = {x: int(cols[x][tl]) for x in range(xlo, 1)}
        rep["late_row_left"] = cb
        print(f"[calib w=1] row t={tl}, x in [{xlo},0]: {cb}")

    if a.json:
        with open(a.json, "w") as f:
            json.dump(rep, f, indent=1, default=str)
    return rep


if __name__ == "__main__":
    main()

"""R7 mode (ii) probe: does inclusion S_k(p) subset {col_-1 eventually periodic
with period <= Q} hold, or does it fail because S_k(p) (proved nonempty for
every R,k by a7's Theorem A) contains witnesses whose col_-1 is NOT eventually
periodic (or has unboundedly growing period as k grows)?

This is read-only reuse of the construction from
experiments/overnight-arms/frontier_attack/a7_ladder_realizability/realize.py
(Theorem A, Lemma P/W).  The build()/min_eventual_period() functions below are
copied verbatim (not imported, to avoid writing any __pycache__ into a7's
directory) from that file so this probe writes only inside a22_r7_mode2/.

We are not re-deriving Theorem A (nonemptiness of S_k(p)) -- that is proved
and machine-verified in a7.  We ARE asking a question a7 did not sweep
end-to-end as its primary variable: for the p=2 tail w=01 (rung 0/1's
characterized case), does the eventual-period search on col_-1 --- over a
GROWING left depth k --- show a trend?  Flat "never found, for any k" is the
signal this probe is built to detect; a growing minimal period as a function
of k would be the "unbounded period" refutation of inclusion described in the
task.
"""

from __future__ import annotations

import json

import numpy as np


def diag_step_series(prev1: np.ndarray, prev2: np.ndarray, d0: int, rule: int) -> np.ndarray:
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
    T0 = 2 * k + 1
    p = len(word)
    jmax = T + max(0, -xlo) + 2
    n = jmax + 2

    zero = np.zeros(n, dtype=np.uint8)
    prev2 = zero.copy()
    prev1 = zero.copy()

    cols = {x: np.zeros(T + 1, dtype=np.uint8) for x in range(xlo, xhi + 1)}
    target = np.zeros(T + 1, dtype=np.uint8)

    for j in range(0, jmax + 1):
        if j == 0:
            d0 = 1
        elif j <= 2 * k:
            d0 = 0
        else:
            base = diag_step_series(prev1, prev2, 0, rule)
            want = int(word[(j - T0 + phase0) % p])
            d0 = int(base[j]) ^ want if j < n else 0
        cur = diag_step_series(prev1, prev2, d0, rule)
        for x in range(xlo, xhi + 1):
            t = j + x
            if 0 <= t <= T:
                cols[x][t] = cur[t]
        prev2, prev1 = prev1, cur

    for t in range(T + 1):
        target[t] = word[(t - T0 + phase0) % p] if t >= T0 else cols[0][t]
    return {"cols": cols, "target": target, "T0": T0}


def min_eventual_period(seq: np.ndarray, qmax: int, drop: int):
    tail = seq[drop:]
    for q in range(1, qmax + 1):
        if len(tail) <= q:
            break
        if np.array_equal(tail[q:], tail[:-q]):
            return q
    return None


def probe(rule: int, k: int, word: str, T: int, qmax: int, phase: int = 0):
    w = tuple(int(c) for c in word)
    xlo, xhi = -k - 2, 1
    b = build(rule, k, w, T, xlo, xhi, phase)
    m1 = b["cols"][-1]
    drop = b["T0"] + 4
    mp = min_eventual_period(m1, qmax, drop)
    return {"rule": rule, "k": k, "w": word, "T": T, "qmax": qmax, "phase": phase,
            "T0": b["T0"], "col_m1_min_eventual_period_le_qmax": mp,
            "tail_len": T - drop}


def main():
    results = []

    # Trend sweep: p=2 word "01", k growing, moderate T/qmax (cheap).
    for k in [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]:
        r = probe(30, k, "01", T=20000, qmax=2048)
        results.append(r)
        print(f"k={k:3d}  T0={r['T0']:4d}  min_eventual_period<=2048: "
              f"{r['col_m1_min_eventual_period_le_qmax']}")

    # Horizon-robustness check at fixed k=2: does a much longer horizon /
    # larger qmax change the verdict a7 already reported at T=50000?
    print("\n-- horizon robustness at k=2 --")
    for T in [20000, 100000, 400000]:
        r = probe(30, 2, "01", T=T, qmax=4096)
        results.append(r)
        print(f"T={T:7d}  min_eventual_period<=4096: "
              f"{r['col_m1_min_eventual_period_le_qmax']}")

    # Second phase, to rule out a phase-specific accidental periodicity.
    print("\n-- phase 1, k growing --")
    for k in [2, 8, 16, 32]:
        r = probe(30, k, "01", T=20000, qmax=2048, phase=1)
        results.append(r)
        print(f"k={k:3d} phase=1  min_eventual_period<=2048: "
              f"{r['col_m1_min_eventual_period_le_qmax']}")

    with open("mode2_probe_out.json", "w") as f:
        json.dump(results, f, indent=1, default=str)


if __name__ == "__main__":
    main()

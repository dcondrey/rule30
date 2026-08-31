"""Headless column-0 patch scan: how tall can a period-p consistent band be?

Measures the realizability quantity named as the remaining gap in
`RESULTS-ladder-rung1.md` section 6, in a representation independent of the
Buchi ladder.

Definition.  Fix a period `p` and a half-width `w`.  A *patch* is a maximal set
of consecutive times `t` on which the band `x in [-w, w]` is entirely
`p`-consistent, i.e.

    s(t, x) == s(t + p, x)   for every x in [-w, w].

`H(p, w)` is the largest patch height found with `t + p + H <= T`.  A patch of
height `H` containing column 0 is exactly a witness that the centre strip of
half-width `w` *looks* eventually `p`-periodic for `H` steps.

Reading the result.  `H(p, w)` bounded in `w`, or decaying, is the phase slip of
`RESULTS-ladder-rung0.md` in a fourth representation and supports the
half-plane branch of rung 1.  `H(p, w)` growing like `log T` is the `O(log t)`
wall of `PATH.md` 3.1 in a fifth encoding.  Growth in `T` at fixed `w` would be
the surprising outcome and would point the other way.

This is a MEASUREMENT, not a decision procedure.  A finite scan cannot
distinguish "no patch exists" from "none exists below depth T", and it excludes
nothing that the published 10^9-bit centre column does not already exclude.

Frame convention matches the repo and the Patch Finder artifact: rows are
carried in the shifted frame `b' = (b << 2) ^ ((b << 1) | b)`, so `s(t, x)` is
bit `x + t` of `b_t`.  Rule 90 control: `b' = (b << 2) ^ b`.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from center_column import center_column  # noqa: E402

# Gate reference, taken from the repo's generator rather than a hand-typed
# constant.  `PREREGISTRATION.md` records that its first 30 terms were checked
# against OEIS A051023 via the OEIS API, not from memory.  A literal typed here
# was wrong on first attempt, which is the reason for the indirection.
A051023 = list(center_column(30))


def step(b: int, rule: int) -> int:
    """One row of the lone-seed evolution in the shifted frame."""
    if rule == 30:
        return (b << 2) ^ ((b << 1) | b)
    if rule == 90:
        return (b << 2) ^ b
    raise ValueError(rule)


def scan(rule: int, T: int, periods: list[int], wmax: int) -> dict:
    """Return H(p, w) for every p in `periods` and every w in 0..wmax.

    One pass.  For each time `t` we compute the largest half-width that is
    `p`-consistent at that time, `mw[t]`; then `H(p, w)` is the longest run of
    consecutive `t` with `mw[t] >= w`, which is a suffix-max sweep over the run
    lengths.  This is exact, not sampled.
    """
    pmax = max(periods)
    window = (1 << (2 * wmax + 1)) - 1

    # Rolling buffer of the last pmax+1 rows, indexed by t % (pmax+1).
    buf: list[int] = [0] * (pmax + 1)
    b = 1
    buf[0] = b
    for t in range(1, pmax + 1):
        b = step(b, rule)
        buf[t] = b

    # run[p][w] = length of the current run at half-width w; best[p][w] = max.
    best = {p: [0] * (wmax + 1) for p in periods}
    best_at: dict[int, list[int]] = {p: [-1] * (wmax + 1) for p in periods}
    # A run at half-width w breaks exactly when mw[t] < w, and mw[t] < w implies
    # mw[t] < w' for every w' > w, so one pass with early exit is exact.
    runs = {p: [0] * (wmax + 1) for p in periods}

    checked_gate = False
    centre_bits: list[int] = []

    t = 0
    while t + pmax <= T:
        b_t = buf[t % (pmax + 1)]
        if len(centre_bits) < len(A051023):
            centre_bits.append((b_t >> t) & 1)

        for p in periods:
            b_ahead = buf[(t + p) % (pmax + 1)]
            # Align: s(t+p, x) is bit x+t+p of b_{t+p}, so shift right by p.
            d = b_t ^ (b_ahead >> p)
            # Extract bits [t-wmax, t+wmax]; centre bit sits at index wmax.
            shift = t - wmax
            win = (d >> shift) & window if shift >= 0 else (d << -shift) & window
            if win & (1 << wmax):
                mw = -1                      # centre itself inconsistent
            else:
                # Distance to the nearest set bit on each side, capped at wmax.
                left = win & ((1 << wmax) - 1)          # bits below centre
                right = win >> (wmax + 1)               # bits above centre
                dl = wmax if left == 0 else wmax - left.bit_length()
                dr = wmax if right == 0 else (right & -right).bit_length() - 1
                mw = dl if dl < dr else dr
            r = runs[p]
            for w in range(0, wmax + 1):
                if mw >= w:
                    r[w] += 1
                    if r[w] > best[p][w]:
                        best[p][w] = r[w]
                        best_at[p][w] = t - r[w] + 1
                else:
                    r[w] = 0
                    # mw < w implies mw < w' for all w' > w; stop early.
                    for w2 in range(w + 1, wmax + 1):
                        r[w2] = 0
                    break

        t += 1
        b = step(b, rule)
        buf[(t + pmax) % (pmax + 1)] = b

    if rule == 30:
        checked_gate = centre_bits == A051023
    else:
        checked_gate = centre_bits[0] == 1 and not any(centre_bits[1:])

    return {
        "rule": rule,
        "T": T,
        "wmax": wmax,
        "gate_ok": checked_gate,
        "H": {str(p): best[p] for p in periods},
        "at": {str(p): best_at[p] for p in periods},
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule", type=int, default=30)
    ap.add_argument("--steps", type=int, default=200_000)
    ap.add_argument("--wmax", type=int, default=24)
    ap.add_argument("--periods", default="1,2,3,4")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    periods = [int(x) for x in a.periods.split(",")]

    t0 = time.time()
    res = scan(a.rule, a.steps, periods, a.wmax)
    res["seconds"] = round(time.time() - t0, 1)

    assert res["gate_ok"], f"gate FAILED for rule {a.rule}: centre column mismatch"

    print(f"rule {res['rule']}  T={res['T']}  wmax={res['wmax']}  "
          f"gate={'OK' if res['gate_ok'] else 'FAIL'}  {res['seconds']}s")
    print()
    header = "| p \\ w | " + " | ".join(str(w) for w in range(0, a.wmax + 1)) + " |"
    print(header)
    print("|" + "---|" * (a.wmax + 2))
    for p in periods:
        row = res["H"][str(p)]
        print(f"| p={p} | " + " | ".join(str(v) for v in row) + " |")

    if a.out:
        with open(a.out, "w") as fh:
            json.dump(res, fh, indent=1)
        print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()

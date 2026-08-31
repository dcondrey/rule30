"""R8 / Problem 2: how long can the lone-seed band look TIME-PERIODIC?

Motivation.  R8's sufficient target is: every vertical-shift-invariant measure on
Y assigns the centre cell density 1/2.  The concrete threats are invariant
measures supported on vertical-shift-PERIODIC points of Y, because those have a
centre density that is a rational read off one orbit and is generically not 1/2.
The p = 1 case is exactly the obstruction register row 47 names as proved: the
all-zeros and checkerboard fixed points.

Universal statistic, replacing an enumeration of candidate orbits.  For each
half-width W and period p define

    Per(W, p, T) = max H such that the lone-seed band [-W,W] has H consecutive
                   rows in [0,T) that are periodic in time with period p.

If ANY vertical-p-periodic configuration lies in Y, then Per(W, p, T) must grow
without bound in T for every W (its patches must recur at every height).  So a
bound on Per(W, p, T), uniform in T, would exclude every p-periodic point of the
vertical shift from Y at once.  Measuring the growth of Per is therefore the
cheapest disconfirming test for the whole periodic-orbit threat family, and it
subsumes the all-zeros / checkerboard families of band_census.py.

Pre-registered asymmetry (fixed before looking at numbers).  Growth of Per(W,p,T)
with T at fixed (W,p) is evidence that a p-periodic point lies in Y and refutes
R8's sufficient target.  Boundedness up to T is INCONCLUSIVE: it is a measured
bound, not a proved one.

Rule 90 control.  The Rule 90 lone-seed band is identically zero on time
intervals of length Theta(T), so Per(W, p, T) = Theta(T) for every W and p, and
the all-zeros fixed point IS in its Y.  That is the degenerate invariant measure
that makes R8 false for Rule 90, and the pipeline must show it.

Run:  uv run python periodic_windows.py [--steps N]
"""

from __future__ import annotations

import argparse
import json
import os

import numpy as np

from band_census import HERE, WMAX, band_series

PMAX = 8


def per_by_horizon(band: np.ndarray, w: int, p: int, horizons: list[int]) -> dict:
    """max run of t with band_w[t] == band_w[t+p], + p, restricted to [w, T)."""
    bw = 2 * w + 1
    codes = (band >> (WMAX - w)) & ((1 << bw) - 1)
    hit = codes[:-p] == codes[p:]
    idx = np.flatnonzero(hit)
    runs = []
    if idx.size:
        brk = np.flatnonzero(np.diff(idx) != 1)
        starts = np.concatenate(([idx[0]], idx[brk + 1]))
        ends = np.concatenate((idx[brk], [idx[-1]]))
        runs = list(zip(starts.tolist(), (ends - starts + 1).tolist()))
    out = {}
    for T in horizons:
        best = 0
        arg = -1
        for s, ln in runs:
            lo = max(s, w)
            hi = min(s + ln, T - p)
            if hi - lo > best:
                best = hi - lo
                arg = lo
        out[str(T)] = {"height": int(best + p) if best else 0, "argmax_t": int(arg)}
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=2_000_000)
    args = ap.parse_args()
    steps = args.steps
    horizons = [2 ** j for j in range(10, 64) if 2 ** j <= steps]
    if horizons[-1] != steps:
        horizons.append(steps)

    res = {"steps": steps, "horizons": horizons, "rules": {}}
    for rule in ("30", "90"):
        band = band_series(rule, steps)
        tab = {}
        for w in range(0, WMAX + 1):
            for p in range(1, PMAX + 1):
                tab[f"W{w}_p{p}"] = per_by_horizon(band, w, p, horizons)
        res["rules"][rule] = tab
        print(f"rule {rule}: Per(W,p,T={steps})")
        print("     " + "".join(f"p={p:<8d}" for p in range(1, PMAX + 1)))
        for w in range(0, WMAX + 1):
            row = "".join(
                f"{tab[f'W{w}_p{p}'][str(steps)]['height']:<10d}"
                for p in range(1, PMAX + 1)
            )
            print(f"  W={w} {row}")
    path = os.path.join(HERE, "periodic_windows.json")
    with open(path, "w") as fh:
        json.dump(res, fh, indent=1)
    print("wrote", path)


if __name__ == "__main__":
    main()

"""R8 / Problem 2: does the lone-seed band's fixed-point patch height GROW?

This is the decision step.  band_census.py and periodic_windows.py measure, at a
ladder of horizons T, the maximal height of the all-zeros / checkerboard-A /
checkerboard-B patches and of time-p-periodic windows in the band [-W,W].

Decision logic, pre-registered:

  * height(W, family, T) growing without bound in T  =>  every finite patch of
    that fixed point occurs in the lone-seed diagram at arbitrarily large times,
    so the fixed point lies in Y, so its Dirac measure is a vertical-shift-
    invariant measure on Y with centre density 0 or 1.  R8's SUFFICIENT TARGET
    IS FALSE, and unique ergodicity of Y is false a fortiori.
  * height bounded, uniformly in T  =>  inconclusive; a finite prefix cannot
    certify a forbidden patch.  This is where the missing lemma would go.

Growth law expected under the natural null.  Uniform Bernoulli is Rule 30
invariant (Taati arXiv:1505.06464 sec 2.4).  Under an ensemble Rule 30 orbit the
first row of a band costs 2^-(2W+1) and each further row costs about 4^-1 (the
rule determines the 2W-1 interior cells of the next row; only the two edge cells
are free), so

    max height over T rows  ~  log4(T) + const,

i.e. LINEAR IN log2(T) WITH SLOPE ~ 1/2, independent of W.  A slope
significantly above zero is growth; a slope of zero across a 2^11 range of
horizons is the bounded case.

Ensemble null implemented here: 20 seeds, random initial row on a cycle of
width q, Rule 30 iterated, identical statistics on the same band.

*** THIS NULL IS REJECTED; USE exact_null.py INSTEAD. ***  Rule 30 on Z/q is NOT
surjective, so uniform Bernoulli is not preserved by the cyclic map: after 10^5
steps on a 4096-cycle the orbit sits deep in an attractor whose patch statistics
are not the invariant-measure ones.  It shows it: this null gives an all-zero
band height of 14 at W=1, T=2^17, against the EXACT uniform-Bernoulli value 8
computed in exact_null.py.  The slopes reported below for the lone seed are
still valid (they are read off band_census.json); the "null" columns are kept
only to document the rejected control.

Run:  uv run python growth_fit.py [--null-steps N] [--null-seeds K]
"""

from __future__ import annotations

import argparse
import json
import math
import os

import numpy as np

from band_census import HERE, WMAX, family_targets, max_run_by_horizon
from periodic_windows import PMAX, per_by_horizon


def fit_slope(horizons: list[int], heights: list[int]) -> float:
    """Least-squares slope of height against log2(T), over horizons with h > 0."""
    xs = [math.log2(t) for t, h in zip(horizons, heights) if h > 0]
    ys = [float(h) for h in heights if h > 0]
    if len(xs) < 3:
        return float("nan")
    x = np.array(xs)
    y = np.array(ys)
    return float(np.polyfit(x, y, 1)[0])


def ensemble_null(steps: int, seeds: int, q: int = 4096) -> np.ndarray:
    """Band [-WMAX,WMAX] of Rule 30 orbits from random cyclic initial rows.

    Returns shape (seeds, steps) uint32 band codes.  Cyclic width q; the band
    sits at the centre of the cycle so the boundary is q/2 away and cannot reach
    it within `steps` only if steps < q/2 -- for larger steps this is a genuine
    cyclic ensemble orbit, which is the intended null.
    """
    words = q // 64
    out = np.zeros((seeds, steps), dtype=np.uint32)
    mask = np.uint64(0xFFFFFFFFFFFFFFFF)
    for s in range(seeds):
        rng = np.random.default_rng(s)
        row = rng.integers(0, 1 << 64, size=words, dtype=np.uint64)
        for t in range(steps):
            # band at cells [q/2 - WMAX, q/2 + WMAX]
            i = q // 2 - WMAX
            w, b = divmod(i, 64)
            v = int(row[w]) >> b
            if b:
                v |= int(row[(w + 1) % words]) << (64 - b)
            out[s, t] = v & ((1 << (2 * WMAX + 1)) - 1)
            # cyclic Rule 30: new bit i = old(i-1) XOR (old(i) OR old(i+1))
            left = (row << np.uint64(1)) & mask
            left[1:] |= row[:-1] >> np.uint64(63)
            left[0] |= row[-1] >> np.uint64(63)
            right = row >> np.uint64(1)
            right[:-1] |= (row[1:] << np.uint64(63)) & mask
            right[-1] |= (row[0] << np.uint64(63)) & mask
            row = left ^ (row | right)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--null-steps", type=int, default=131072)
    ap.add_argument("--null-seeds", type=int, default=20)
    args = ap.parse_args()

    with open(os.path.join(HERE, "band_census_rule30.json")) as fh:
        bc30 = json.load(fh)
    with open(os.path.join(HERE, "band_census_rule90.json")) as fh:
        bc90 = json.load(fh)
    with open(os.path.join(HERE, "periodic_windows.json")) as fh:
        pw = json.load(fh)

    res: dict = {
        "steps_rule30": bc30["steps"],
        "null_steps": args.null_steps,
        "null_seeds": args.null_seeds,
    }
    hz = bc30["horizons"]

    # ---- families: heights by horizon and slope, Rule 30 and Rule 90
    fam = {}
    for tag, bc in (("30", bc30), ("90", bc90)):
        for name in ("all_zeros", "checker_A", "checker_B"):
            for w in range(WMAX + 1):
                h = [
                    bc["families"][name][str(w)]["by_horizon"][str(t)]["max_height"]
                    for t in bc["horizons"]
                ]
                fam[f"rule{tag}_{name}_W{w}"] = {
                    "horizons": bc["horizons"],
                    "heights": h,
                    "slope_per_log2T": round(fit_slope(bc["horizons"], h), 3),
                }
    res["families"] = fam

    # ---- periodic windows: slope of Per(W,p,T) in log2 T
    per = {}
    for tag in ("30", "90"):
        for w in range(WMAX + 1):
            for p in range(1, PMAX + 1):
                h = [pw["rules"][tag][f"W{w}_p{p}"][str(t)]["height"]
                     for t in pw["horizons"]]
                per[f"rule{tag}_W{w}_p{p}"] = {
                    "heights": h,
                    "slope_per_log2T": round(fit_slope(pw["horizons"], h), 3),
                }
    res["periodic_windows"] = per
    res["periodic_horizons"] = pw["horizons"]

    # ---- ensemble null
    print(f"generating ensemble null: {args.null_seeds} seeds x {args.null_steps}")
    null = ensemble_null(args.null_steps, args.null_seeds)
    nh = [t for t in hz if t <= args.null_steps]
    nullres = {}
    for name in ("all_zeros", "checker_A", "checker_B"):
        for w in range(WMAX + 1):
            bw = 2 * w + 1
            target = family_targets(w)[name]
            per_seed = []
            for s in range(args.null_seeds):
                codes = (null[s] >> (WMAX - w)) & ((1 << bw) - 1)
                hit = codes == target
                bh = max_run_by_horizon(hit, nh, 0)
                per_seed.append([bh[str(t)]["max_height"] for t in nh])
            arr = np.array(per_seed)
            nullres[f"{name}_W{w}"] = {
                "horizons": nh,
                "mean": arr.mean(axis=0).round(2).tolist(),
                "max": arr.max(axis=0).tolist(),
                "slope_mean_per_log2T": round(fit_slope(nh, arr.mean(axis=0).tolist()), 3),
            }
    res["ensemble_null_families"] = nullres

    nullper = {}
    for w in range(WMAX + 1):
        for p in range(1, PMAX + 1):
            per_seed = []
            for s in range(args.null_seeds):
                bh = per_by_horizon(null[s], w, p, nh)
                per_seed.append([bh[str(t)]["height"] for t in nh])
            arr = np.array(per_seed)
            nullper[f"W{w}_p{p}"] = {
                "mean": arr.mean(axis=0).round(2).tolist(),
                "max": arr.max(axis=0).tolist(),
                "slope_mean_per_log2T": round(fit_slope(nh, arr.mean(axis=0).tolist()), 3),
            }
    res["ensemble_null_periodic"] = {"horizons": nh, "cells": nullper}

    path = os.path.join(HERE, "growth_fit.json")
    with open(path, "w") as fh:
        json.dump(res, fh, indent=1)

    # ---- report
    print("\nRULE 30 lone seed: max patch height by horizon (T = 2^10 .. %d)" % bc30["steps"])
    for name in ("all_zeros", "checker_A", "checker_B"):
        print(f"  {name}")
        for w in range(WMAX + 1):
            k = fam[f"rule30_{name}_W{w}"]
            nl = nullres[f"{name}_W{w}"]
            print(f"    W={w} heights={k['heights']} slope={k['slope_per_log2T']}"
                  f"  | null mean slope={nl['slope_mean_per_log2T']}"
                  f" null max@{nh[-1]}={nl['max'][-1]}")
    print("\nRULE 90 control: max patch height by horizon")
    for name in ("all_zeros", "checker_A", "checker_B"):
        for w in (0, 1, 4, 8):
            k = fam[f"rule90_{name}_W{w}"]
            print(f"  {name} W={w} heights={k['heights']} slope={k['slope_per_log2T']}")
    print("\nwrote", path)


if __name__ == "__main__":
    main()

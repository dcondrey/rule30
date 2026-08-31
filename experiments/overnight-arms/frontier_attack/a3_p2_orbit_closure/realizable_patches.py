"""R8 / Problem 2: is the lone-seed band language FULL?

Y is the closure of the vertical shifts of the lone-seed diagram.  Let Omega be
the full two-sided Rule 30 spacetime subshift (all bi-infinite orbits).  Always
Y is a subset of Omega.  If the lone-seed band language equals Omega's band
language at every (W,H) -- i.e. every REALIZABLE (2W+1) x H patch actually occurs
in columns [-W,W] of the lone-seed diagram, and recurs -- then Y = Omega, and
Omega carries invariant measures with centre density 0 and 1 (the all-zeros and
checkerboard fixed points).  R8's sufficient target would then be FALSE.

So the quantified claim this script tests is:

    P(W,H)  ==  R(W,H)  ?

  P(W,H) = number of DISTINCT (2W+1) x H patches observed in columns [-W,W] of
           the lone-seed diagram over t < T   (from band_census.py)
  R(W,H) = number of realizable (2W+1) x H patches, computed EXACTLY by
           enumerating every initial row of width 2W + 2H - 1 and running H
           steps.  That width is exactly the dependency cone of the patch, so
           this enumeration is complete: a patch is a window of some Rule 30
           orbit iff it appears here.

Note R(W,H) < 2^(2W+1) * 4^(H-1), the naive "two free edge cells per row" bound,
because of the OR latch: when s(t,W) = 1 the cell s(t+1,W) is pinned to
NOT s(t,W-1) regardless of what lies to the right.  The gap is measured below and
is a Rule-30-specific quantity -- for Rule 90 the naive bound is exact.

Run:  uv run python realizable_patches.py [--maxbits 22]
"""

from __future__ import annotations

import argparse
import json
import os

import numpy as np

from band_census import HERE


def realizable_count(rule: str, w: int, h: int) -> tuple[int, int]:
    """(R(W,H), naive bound).  Exact enumeration over the dependency cone."""
    n = 2 * w + 2 * h - 1  # width of the initial row
    bw = 2 * w + 1
    rows = np.arange(1 << n, dtype=np.uint64)
    mask = np.uint64((1 << n) - 1)
    key = np.zeros(1 << n, dtype=np.uint64)
    cur = rows
    for i in range(h):
        # band of row i occupies cells [h-1-i + ... ] : after i steps the
        # reliable region is [i, n-1-i]; the band [-w,w] sits at offset h-1.
        lo = h - 1
        seg = (cur >> np.uint64(lo)) & np.uint64((1 << bw) - 1)
        key |= seg << np.uint64(bw * i)
        if rule == "30":
            cur = ((cur << np.uint64(1)) ^ (cur | (cur >> np.uint64(1)))) & mask
        elif rule == "90":
            cur = ((cur << np.uint64(1)) ^ (cur >> np.uint64(1))) & mask
        else:
            raise ValueError(rule)
    return int(np.unique(key).size), int(2 ** bw * 4 ** (h - 1))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--maxbits", type=int, default=22)
    args = ap.parse_args()

    out: dict = {"maxbits": args.maxbits, "rules": {}}
    for rule in ("30", "90"):
        with open(os.path.join(HERE, f"band_census_rule{rule}.json")) as fh:
            bc = json.load(fh)
        tab = {}
        for w in range(0, 4):
            for h in range(1, 25):
                n = 2 * w + 2 * h - 1
                if n > args.maxbits:
                    break
                bw = 2 * w + 1
                if bw * h > 63:
                    break
                R, naive = realizable_count(rule, w, h)
                obs = bc["patch_census"].get(str(w), {}).get(str(h))
                cell = {
                    "R_realizable": R,
                    "naive_bound": naive,
                    "all_patches": 2 ** (bw * h),
                }
                if obs:
                    cell["P_observed"] = obs["distinct"]
                    cell["samples"] = obs["samples"]
                    cell["P_over_R"] = round(obs["distinct"] / R, 6)
                    # sampling-limited? expected coverage if patches were drawn
                    # uniformly at random from R possibilities
                    cell["sample_limited"] = bool(obs["samples"] < 5 * R)
                tab[f"W{w}_H{h}"] = cell
                print(f"rule {rule} W={w} H={h}: R={R} naive={naive}"
                      + (f" P={cell.get('P_observed')} P/R={cell.get('P_over_R')}"
                         f" sample_limited={cell.get('sample_limited')}" if obs else ""))
        out["rules"][rule] = tab
    path = os.path.join(HERE, "realizable_patches.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote", path)


if __name__ == "__main__":
    main()

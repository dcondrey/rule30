"""Are the patches missing from the lone-seed band FORBIDDEN, or just rare?

At the frontier of the census, P(W,H) drops just below R(W,H) (e.g. W=1, H=9:
13925 observed of 13928 realizable).  A missing patch is either (a) a sampling
tail -- the diagram is 2e6 rows and the rarest realizable patches have expected
counts of order 1 -- or (b) genuinely FORBIDDEN in the lone-seed diagram, which
would be a real structural constraint on Y and would matter.

This script settles it, per cell, three ways:

 1. Low-count histogram.  Number of realizable patches seen 0, 1, 2, ... times.
    If #(seen 0) is small relative to #(seen once), the misses are the ordinary
    tail of a heavy-tailed count distribution, not a prohibition.
 2. Prefix counts.  For each missing patch, how often its (H-1)-row prefix
    occurred.  A patch whose prefix occurred a handful of times is expected to
    be missed; one whose prefix occurred thousands of times and never continued
    is a forbidden-patch candidate.
 3. Persistence across horizons.  A patch missing at T = 10^6 but present at
    T = 2*10^6 was never forbidden.

Run:  uv run python forbidden_check.py [--steps N]   (uses the cached band)
"""

from __future__ import annotations

import argparse
import json
import os

import numpy as np

from band_census import HERE, WMAX, band_series
from realizable_patches import realizable_count


def realizable_keys(rule: str, w: int, h: int) -> np.ndarray:
    """The exact set of realizable patch keys (same encoding as the census)."""
    n = 2 * w + 2 * h - 1
    bw = 2 * w + 1
    cur = np.arange(1 << n, dtype=np.uint64)
    mask = np.uint64((1 << n) - 1)
    key = np.zeros(1 << n, dtype=np.uint64)
    for i in range(h):
        seg = (cur >> np.uint64(h - 1)) & np.uint64((1 << bw) - 1)
        key |= seg << np.uint64(bw * i)
        if rule == "30":
            cur = ((cur << np.uint64(1)) ^ (cur | (cur >> np.uint64(1)))) & mask
        else:
            cur = ((cur << np.uint64(1)) ^ (cur >> np.uint64(1))) & mask
    return np.unique(key)


def observed_keys(band: np.ndarray, w: int, h: int, t_start: int = WMAX):
    bw = 2 * w + 1
    codes = ((band >> (WMAX - w)) & ((1 << bw) - 1)).astype(np.uint64)[t_start:]
    key = np.zeros(len(codes) - h + 1, dtype=np.uint64)
    for i in range(h):
        key |= codes[i:len(codes) - h + 1 + i] << np.uint64(bw * i)
    return key


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=2_000_000)
    args = ap.parse_args()
    band = band_series("30", args.steps)
    cells = [(0, 11), (1, 9), (1, 10), (2, 8), (2, 9), (3, 7), (3, 8)]
    out = {"steps": args.steps, "cells": {}}
    for w, h in cells:
        R = realizable_keys("30", w, h)
        obs = observed_keys(band, w, h)
        uniq, cnt = np.unique(obs, return_counts=True)
        # map observed counts onto the realizable set
        pos = np.searchsorted(uniq, R)
        pos = np.clip(pos, 0, len(uniq) - 1)
        counts = np.where(uniq[pos] == R, cnt[pos], 0)
        assert np.isin(uniq, R).all(), "observed a NON-realizable patch"
        hist = {str(c): int((counts == c).sum()) for c in range(0, 6)}
        missing = R[counts == 0]
        # prefix counts for the missing patches
        pre_info = []
        if missing.size:
            bw = 2 * w + 1
            preobs = observed_keys(band, w, h - 1)
            pu, pc = np.unique(preobs, return_counts=True)
            for m in missing.tolist():
                pre = m & ((1 << (bw * (h - 1))) - 1)
                j = np.searchsorted(pu, pre)
                n_pre = int(pc[j]) if j < len(pu) and pu[j] == pre else 0
                suf = m >> np.uint64(bw)
                j2 = np.searchsorted(pu, suf)
                n_suf = int(pc[j2]) if j2 < len(pu) and pu[j2] == suf else 0
                pre_info.append({"patch_key": int(m), "prefix_count": n_pre,
                                 "suffix_count": n_suf})
        # horizon persistence: how many are missing at T/2 but present at T
        obs_half = observed_keys(band[: args.steps // 2], w, h)
        uh = np.unique(obs_half)
        ph = np.searchsorted(uh, R)
        ph = np.clip(ph, 0, len(uh) - 1)
        miss_half = int((uh[ph] != R).sum())
        out["cells"][f"W{w}_H{h}"] = {
            "R": int(R.size),
            "P": int(uniq.size),
            "missing": int(missing.size),
            "missing_at_half_horizon": miss_half,
            "recovered_between_T_half_and_T": miss_half - int(missing.size),
            "count_histogram_0_to_5": hist,
            "min_positive_count": int(counts[counts > 0].min()),
            "missing_detail": pre_info[:20],
        }
        print(f"W={w} H={h}: R={R.size} P={uniq.size} missing={missing.size} "
              f"(missing at T/2: {miss_half}) hist(0..5)={hist}")
        for d in pre_info[:8]:
            print(f"    missing key {d['patch_key']}: prefix seen "
                  f"{d['prefix_count']}x, suffix seen {d['suffix_count']}x")
    path = os.path.join(HERE, "forbidden_check.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote", path)


if __name__ == "__main__":
    main()

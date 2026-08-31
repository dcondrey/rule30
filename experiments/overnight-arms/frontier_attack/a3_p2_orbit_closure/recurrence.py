"""R8 / Problem 2: recurrence, and the diagonal (W = H) test for Y membership.

Membership in Y (the closure of the VERTICAL shifts of the lone-seed diagram)
needs BOTH dimensions of the window to grow along one sequence of times: z lies
in Y iff there are t_k -> infinity with the (2k+1) x k patch of the diagram at
time t_k equal to that of z.  So the decisive statistic is the diagonal one,

    K(f, T) = max k such that the (2k+1) x k patch of fixed point f occurs
              in the lone-seed diagram at some t < T,

not the max height at fixed W.  K -> infinity  <=>  f lies in Y.

This script also reports LATE occurrences (t >= T/2) for every height, because
Y is a closure of the forward orbit: only occurrences at arbitrarily large times
put a configuration in Y.  Occurrences confined to small t would not.

Run:  uv run python recurrence.py [--steps N]   (reuses the cached band)
"""

from __future__ import annotations

import argparse
import json
import os

import numpy as np

from band_census import HERE, WMAX, band_series, family_targets


def runs_of(hit: np.ndarray) -> list[tuple[int, int]]:
    idx = np.flatnonzero(hit)
    if not idx.size:
        return []
    brk = np.flatnonzero(np.diff(idx) != 1)
    starts = np.concatenate(([idx[0]], idx[brk + 1]))
    ends = np.concatenate((idx[brk], [idx[-1]]))
    return list(zip(starts.tolist(), (ends - starts + 1).tolist()))


def height_profile(hit: np.ndarray, steps: int, t_start: int) -> dict:
    """For each height h: total occurrences, occurrences with t >= steps/2, and
    the largest start time."""
    prof = {}
    rs = [(s, ln) for s, ln in runs_of(hit) if s + ln > t_start]
    if not rs:
        return prof
    hmax = max(ln for s, ln in rs)
    half = steps // 2
    prof["_hmax"] = hmax  # Rule 90 reaches ~T/2; the per-height table is capped
    for h in range(1, min(hmax, 64) + 1):
        tot = 0
        late = 0
        last = -1
        for s, ln in rs:
            lo = max(s, t_start)
            hi = s + ln - h  # inclusive last start
            if hi < lo:
                continue
            tot += hi - lo + 1
            if hi >= half:
                late += hi - max(lo, half) + 1
            last = max(last, hi)
        if tot:
            prof[str(h)] = {"occurrences": tot, "late_occurrences": late,
                            "last_start_t": last}
    return prof


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
        entry: dict = {"height_profile": {}, "diagonal_K": {}}
        for name in ("all_zeros", "checker_A", "checker_B"):
            for w in range(WMAX + 1):
                bw = 2 * w + 1
                codes = (band >> (WMAX - w)) & ((1 << bw) - 1)
                hit = codes == family_targets(w)[name]
                entry["height_profile"][f"{name}_W{w}"] = height_profile(
                    hit, steps, w
                )
            # diagonal: need the (2k+1) x k patch, i.e. W = k and height >= k
            diag = {}
            for T in horizons:
                best = 0
                argt = -1
                for k in range(0, WMAX + 1):
                    bw = 2 * k + 1
                    codes = (band[:T] >> (WMAX - k)) & ((1 << bw) - 1)
                    hit = codes == family_targets(k)[name]
                    ok = False
                    for s, ln in runs_of(hit):
                        if s < k:
                            s2, ln2 = k, ln - (k - s)
                        else:
                            s2, ln2 = s, ln
                        if ln2 >= max(k, 1):
                            ok = True
                            argt = s2
                            break
                    if ok:
                        best = k
                    else:
                        break
                diag[str(T)] = {"K": best, "witness_t": argt}
            entry["diagonal_K"][name] = diag
        res["rules"][rule] = entry
        print(f"rule {rule}: diagonal K(f,T) = max k with the (2k+1) x k patch present")
        for name in ("all_zeros", "checker_A", "checker_B"):
            ks = [entry["diagonal_K"][name][str(T)]["K"] for T in horizons]
            print(f"  {name:10s} T=2^10..{steps}: {ks}")

    path = os.path.join(HERE, "recurrence.json")
    with open(path, "w") as fh:
        json.dump(res, fh, indent=1)
    print("wrote", path)


if __name__ == "__main__":
    main()

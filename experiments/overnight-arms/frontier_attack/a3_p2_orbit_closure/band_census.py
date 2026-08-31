"""R8 / prize Problem 2: 2D window recurrence in the lone-seed vertical orbit closure.

Object.  Y = closure of the VERTICAL (time) shifts of the lone-seed spacetime
diagram in {0,1}^{Z^2}.  A configuration z lies in Y iff for every half-width W
and every height H the (2W+1) x H patch of z at columns [-W,W] occurs in the
lone-seed diagram at arbitrarily large time offsets.  Note the spatial anchor is
FIXED at column 0: only time shifts are taken.

What this script measures.  The band language of the lone-seed diagram: for each
half-width W and height H, which (2W+1) x H patches occur in columns [-W,W], and
in particular the maximal height of the three patch families that would kill R8:

  * all-zeros            (delta_{0} is vertical-shift-invariant, centre density 0)
  * checkerboard phase A (s(t,x) = 1 iff x even)  -- centre density 1
  * checkerboard phase B (s(t,x) = 1 iff x odd)   -- centre density 0

All three of these configurations are FIXED POINTS of Rule 30 in the time
direction (verified exactly below), hence each carries a vertical-shift-invariant
Dirac measure whose centre-cell density is 0 or 1, not 1/2.  So R8's sufficient
target holds only if none of them lies in Y.

The measurement is ASYMMETRIC and this is pre-registered before looking at the
numbers: growth of a family's maximal height with the horizon is evidence that
the corresponding fixed point lies in Y and REFUTES R8's sufficient target;
boundedness up to horizon T is INCONCLUSIVE, because a finite prefix cannot
certify a forbidden patch.

Rule 90 control.  For Rule 90 the R8 claim is FALSE, and the pipeline must show
it.  Closed form checked here: for t in [2^k, 2^{k+1}) the band |x| <= W of the
Rule 90 lone-seed diagram is identically zero for all t with 2^k - (t - 2^k) > W,
i.e. the all-zero band height grows like Theta(T).

Run:  uv run python band_census.py [--steps N]
Writes band_census_rule30.json / band_census_rule90.json next to this file.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
COMMON = os.path.abspath(os.path.join(HERE, "..", "..", "common"))
sys.path.insert(0, COMMON)

import rule30 as r30common  # noqa: E402  (shared substrate, reused not reimplemented)

WMAX = 8
BAND = 2 * WMAX + 1  # 17 columns, x = -8..8, bit (x + WMAX)


# ---------------------------------------------------------------- generation


CACHE = os.environ.get(
    "A3_BAND_CACHE",
    "/private/tmp/claude-501/-Volumes-A-researchpapers-13-rule30/"
    "ed534796-4b7d-4631-8362-2e60223b917f/scratchpad",
)


def band_series(rule: str, steps: int, wmax: int = WMAX) -> np.ndarray:
    """Cached wrapper around _band_series (generation is O(steps^2))."""
    path = os.path.join(CACHE, f"band_rule{rule}_{steps}_{wmax}.npy")
    if os.path.exists(path):
        return np.load(path)
    band = _band_series(rule, steps, wmax)
    try:
        os.makedirs(CACHE, exist_ok=True)
        np.save(path, band)
    except OSError:
        pass
    return band


def _band_series(rule: str, steps: int, wmax: int = WMAX) -> np.ndarray:
    """Columns [-wmax, wmax] of the lone-seed diagram for t = 0..steps-1.

    Internal frame b_t(i) = s(t, i - t) as in common/rule30.py, stored as packed
    uint64 words so the cone can grow to 2*steps cells.  Returns uint32 codes
    with bit (x + wmax) = s(t, x).
    """
    words = (2 * steps + 2 * wmax + 128) // 64 + 4
    row = np.zeros(words, dtype=np.uint64)
    row[0] = np.uint64(1)
    out = np.zeros(steps, dtype=np.uint32)
    mask = (1 << (2 * wmax + 1)) - 1
    s1 = np.empty(words, dtype=np.uint64)
    s2 = np.empty(words, dtype=np.uint64)
    live = 1  # number of words that can be nonzero; grows by 1 per 32 steps
    for t in range(steps):
        i = t - wmax
        if i >= 0:
            w, b = divmod(i, 64)
            v = int(row[w]) >> b
            if b:
                v |= int(row[w + 1]) << (64 - b)
            out[t] = v & mask
        else:
            # t < wmax: read from bit 0 upward and shift the window right.
            v = int(row[0]) | (int(row[1]) << 64)
            out[t] = (v << (-i)) & mask
        live = min(words, (2 * t + 2 * wmax + 128) // 64 + 2)
        r = row[:live]
        a1 = s1[:live]
        a2 = s2[:live]
        np.left_shift(r, np.uint64(1), out=a1)
        a1[1:] |= r[:-1] >> np.uint64(63)
        if rule == "30":
            np.left_shift(r, np.uint64(2), out=a2)
            a2[1:] |= r[:-1] >> np.uint64(62)
            np.bitwise_or(a1, r, out=a1)
            np.bitwise_xor(a2, a1, out=r)
        elif rule == "90":
            # b_{t+1} = (b_t << 2) ^ b_t
            np.left_shift(r, np.uint64(2), out=a2)
            a2[1:] |= r[:-1] >> np.uint64(62)
            np.bitwise_xor(a2, r, out=r)
        else:
            raise ValueError(rule)
    return out


# ---------------------------------------------------------------- validation


def validate(rule: str, band: np.ndarray) -> dict:
    """Exact cross-checks against independent implementations."""
    checks = {}
    n = 4096
    centre = ((band >> WMAX) & 1).astype(np.uint8)

    # 1. centre column vs common/rule30.py (rule 30) or the closed form (rule 90)
    if rule == "30":
        ref = np.array(r30common.center_column_bits(n), dtype=np.uint8)
        checks["centre_vs_common_rule30"] = bool((centre[:n] == ref).all())
    else:
        # Rule 90 lone seed: centre is 1 at t=0 and 0 thereafter.
        checks["centre_vs_closed_form_rule90"] = bool(
            centre[0] == 1 and not centre[1:].any()
        )

    # 2. full band vs the naive dict simulator in common/rule30.py
    grid = r30common.simulate_seed({0: 1}, 512) if rule == "30" else None
    if grid is not None:
        ok = True
        for t in range(512):
            code = 0
            for x in range(-WMAX, WMAX + 1):
                if grid[t].get(x, 0):
                    code |= 1 << (x + WMAX)
            ok &= code == int(band[t])
        checks["band_vs_naive_simulator"] = bool(ok)
    else:
        # Rule 90 band vs Kummer/Lucas: s(t,x)=1 iff (t+x) even and
        # C(t,(t+x)/2) odd, i.e. m = (t+x)/2 is a submask of t.
        ok = True
        for t in range(512):
            code = 0
            for x in range(-WMAX, WMAX + 1):
                if (t + x) % 2 == 0:
                    m = (t + x) // 2
                    if 0 <= m <= t and (m & (t - m)) == 0:
                        code |= 1 << (x + WMAX)
            ok &= code == int(band[t])
        checks["band_vs_lucas_rule90"] = bool(ok)

    # 3. centre column vs the stored 2e6-byte column from experiments/rule30
    stored = os.path.abspath(
        os.path.join(HERE, "..", "..", "..", "rule30", "orbit-closure",
                     f"col{rule}_2000000.bin")
    )
    if os.path.exists(stored):
        col = np.fromfile(stored, dtype=np.uint8, count=len(centre))
        k = min(len(col), len(centre))
        checks["centre_vs_stored_bin"] = bool((col[:k] == centre[:k]).all())
        checks["centre_vs_stored_bin_len"] = int(k)

    # 4. the three fixed-point claims, verified exactly on a width-64 window
    checks["fixed_points"] = fixed_point_check()
    return checks


def fixed_point_check() -> dict:
    """Exact check that all-zeros and both checkerboard phases are Rule 30
    fixed points in the time direction, and that they are NOT Rule 90 fixed
    points (which is why the Rule 90 failure mode is a different one)."""
    out = {}
    n = 65
    for name, f in (
        ("all_zeros", lambda x: 0),
        ("checker_A", lambda x: 1 - (x & 1)),  # 1 iff x even
        ("checker_B", lambda x: x & 1),        # 1 iff x odd
    ):
        r = [f(x) for x in range(-n, n + 1)]
        nxt30 = [
            r[i - 1] ^ (r[i] | r[i + 1]) for i in range(1, len(r) - 1)
        ]
        nxt90 = [r[i - 1] ^ r[i + 1] for i in range(1, len(r) - 1)]
        out[name] = {
            "rule30_fixed": nxt30 == r[1:-1],
            "rule90_fixed": nxt90 == r[1:-1],
            "centre_density": float(f(0)),
        }
    return out


# ------------------------------------------------------------ patch families


def family_targets(w: int) -> dict[str, int]:
    """The band code of each fixed-point row at half-width w."""
    a = 0
    b = 0
    for x in range(-w, w + 1):
        if x % 2 == 0:
            a |= 1 << (x + w)
        else:
            b |= 1 << (x + w)
    return {"all_zeros": 0, "checker_A": a, "checker_B": b}


def max_run_by_horizon(hit: np.ndarray, horizons: list[int], t_start: int) -> dict:
    """For each horizon T, the max number of CONSECUTIVE True entries of hit
    inside [t_start, T), plus total hits and the last hit time in that range."""
    res = {}
    idx = np.flatnonzero(hit)
    # run-length encode the True runs once
    runs = []  # (start, length)
    if idx.size:
        brk = np.flatnonzero(np.diff(idx) != 1)
        starts = np.concatenate(([idx[0]], idx[brk + 1]))
        ends = np.concatenate((idx[brk], [idx[-1]]))
        runs = list(zip(starts.tolist(), (ends - starts + 1).tolist()))
    for T in horizons:
        best = 0
        arg = -1
        for s, ln in runs:
            lo = max(s, t_start)
            hi = min(s + ln, T)
            if hi - lo > best:
                best = hi - lo
                arg = lo
        sel = idx[(idx >= t_start) & (idx < T)]
        res[str(T)] = {
            "max_height": int(best),
            "argmax_t": int(arg),
            "n_rows_hit": int(sel.size),
            "last_hit_t": int(sel[-1]) if sel.size else -1,
        }
    return res


def gap_stats(hit: np.ndarray, t_start: int) -> dict:
    """Return-time distribution of the single-row event, for recurrence."""
    idx = np.flatnonzero(hit)
    idx = idx[idx >= t_start]
    if idx.size < 2:
        return {"n": int(idx.size), "gaps": None}
    g = np.diff(idx)
    return {
        "n": int(idx.size),
        "gap_mean": float(g.mean()),
        "gap_max": int(g.max()),
        "gap_p50": float(np.percentile(g, 50)),
        "gap_p99": float(np.percentile(g, 99)),
        "last_t": int(idx[-1]),
    }


# --------------------------------------------------------------- patch census


def patch_census(band: np.ndarray, w: int, hmax: int, t_start: int) -> dict:
    """Number of DISTINCT (2w+1) x H patches occurring in columns [-w,w]."""
    bw = 2 * w + 1
    codes = ((band >> (WMAX - w)) & ((1 << bw) - 1)).astype(np.uint64)
    codes = codes[t_start:]
    out = {}
    for H in range(1, hmax + 1):
        if bw * H > 63 or len(codes) <= H:
            break
        key = np.zeros(len(codes) - H + 1, dtype=np.uint64)
        for i in range(H):
            key |= codes[i:len(codes) - H + 1 + i] << np.uint64(bw * i)
        n = int(np.unique(key).size)
        out[str(H)] = {
            "distinct": n,
            "samples": int(key.size),
            "all_patches": float(2 ** (bw * H)),
            "rule_consistent_bound": float(2 ** bw * 4 ** (H - 1)),
            "saturated": n >= int(key.size) * 0.5 or n >= 2 ** (bw * H),
        }
    return out


# ---------------------------------------------------------------------- main


def analyse(rule: str, steps: int) -> dict:
    t0 = time.time()
    band = band_series(rule, steps)
    gen_s = time.time() - t0
    res = {
        "rule": rule,
        "steps": steps,
        "generation_seconds": round(gen_s, 2),
        "validation": validate(rule, band),
    }
    horizons = [2 ** j for j in range(10, 64) if 2 ** j <= steps]
    if horizons[-1] != steps:
        horizons.append(steps)
    res["horizons"] = horizons

    fam = {}
    for w in range(0, WMAX + 1):
        bw = 2 * w + 1
        codes = (band >> (WMAX - w)) & ((1 << bw) - 1)
        t_start = w  # band fully inside the light cone; avoids the t<W edge
        for name, target in family_targets(w).items():
            hit = codes == target
            fam.setdefault(name, {})[str(w)] = {
                "by_horizon": max_run_by_horizon(hit, horizons, t_start),
                "returns": gap_stats(hit, t_start),
            }
    res["families"] = fam

    res["patch_census"] = {
        str(w): patch_census(band, w, 20, WMAX) for w in range(0, 4)
    }
    return res


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=2_000_000)
    args = ap.parse_args()
    for rule in ("30", "90"):
        res = analyse(rule, args.steps)
        path = os.path.join(HERE, f"band_census_rule{rule}.json")
        with open(path, "w") as fh:
            json.dump(res, fh, indent=1)
        print(f"rule {rule}: wrote {path} ({res['generation_seconds']}s gen)")
        print("  validation:", json.dumps(res["validation"], sort_keys=True)[:400])
        for name in ("all_zeros", "checker_A", "checker_B"):
            row = [
                res["families"][name][str(w)]["by_horizon"][str(args.steps)][
                    "max_height"
                ]
                for w in range(0, WMAX + 1)
            ]
            print(f"  {name:10s} max height by W=0..8: {row}")


if __name__ == "__main__":
    main()

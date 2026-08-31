"""a22: push a3's checkerboard/all-zero patch-growth measurement further.

Context (read in full, not re-derived here): a3_p2_orbit_closure/p2_orbit_closure.md
already established that all three vertical-shift fixed points (all-zeros,
checkerboard A, checkerboard B) grow their maximal band-patch height at every
half-width W over 11 horizon doublings up to T = 2e6, matching the exact
uniform-Bernoulli reference law to within one row at 23/27 cells, and that the
diagonal statistic K(f,T) -- the largest k such that the (2k+1) x k patch occurs
by time T, which is what Y-membership actually needs -- grew for all three
families (checker_A: 2,2,2,4,4,4,4,5,6,6,6,6 at T=2^10..2e6). a3's own
pre-registration states growth REFUTES R8 (evidence the fixed point lies in Y);
it fired the kill condition and marked route R8 dead. See section header note
in this script's companion report for a discrepancy with this task's framing.

This arm (a22) does two things, cheaper first:

(a) Extend the SAME measurement (diagonal K, per-W height) to a larger horizon
    T and a larger half-width cap WMAX (a3 capped WMAX=8 for a uint32 output
    word; here we use WMAX=15, still uint32-safe at 2*15+1=31 bits, giving more
    headroom before the W-cap can bind the diagonal statistic). Reuses a3's
    exact generation kernel `_band_series` via import (read-only), not
    reimplemented.

(b) A structural (non-simulation) lemma about how a single defect against a
    checkerboard background propagates under one Rule 30 step -- see
    `defect_propagation.py` in this directory.

Nothing outside a22_p2_checkerboard_growth/ is written. a3's files are only
imported, never modified.
"""

from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
A3 = os.path.abspath(os.path.join(HERE, "..", "a3_p2_orbit_closure"))
sys.path.insert(0, A3)

from band_census import _band_series  # noqa: E402  (a3's exact kernel, read-only import)

CACHE = os.path.join(HERE, "cache")
os.makedirs(CACHE, exist_ok=True)

WMAX = 15  # 2*15+1 = 31 bits, still fits the uint32 band code a3's kernel emits


def band_series(rule: str, steps: int, wmax: int = WMAX) -> np.ndarray:
    path = os.path.join(CACHE, f"band_rule{rule}_{steps}_{wmax}.npy")
    if os.path.exists(path):
        return np.load(path)
    t0 = time.time()
    band = _band_series(rule, steps, wmax)
    dt = time.time() - t0
    print(f"generated rule {rule} steps={steps} wmax={wmax} in {dt:.1f}s")
    np.save(path, band)
    return band


def family_targets(w: int) -> dict[str, int]:
    a = 0
    b = 0
    for x in range(-w, w + 1):
        if x % 2 == 0:
            a |= 1 << (x + w)
        else:
            b |= 1 << (x + w)
    return {"all_zeros": 0, "checker_A": a, "checker_B": b}


def runs_of(hit: np.ndarray) -> list[tuple[int, int]]:
    idx = np.flatnonzero(hit)
    if not idx.size:
        return []
    brk = np.flatnonzero(np.diff(idx) != 1)
    starts = np.concatenate(([idx[0]], idx[brk + 1]))
    ends = np.concatenate((idx[brk], [idx[-1]]))
    return list(zip(starts.tolist(), (ends - starts + 1).tolist()))


def max_height(band: np.ndarray, w: int, name: str, wmax: int) -> int:
    bw = 2 * w + 1
    codes = (band >> (wmax - w)) & ((1 << bw) - 1)
    hit = codes == family_targets(w)[name]
    runs = runs_of(hit)
    return max((ln for _, ln in runs), default=0)


def diagonal_K(band: np.ndarray, name: str, wmax: int, horizons: list[int]) -> dict:
    diag = {}
    for T in horizons:
        best = 0
        argt = -1
        for k in range(0, wmax + 1):
            bw = 2 * k + 1
            codes = (band[:T] >> (wmax - k)) & ((1 << bw) - 1)
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
        diag[str(T)] = {"K": best, "witness_t": argt, "capped_at_wmax": best == wmax}
    return diag


def H_star(w: int, T: int, per_row_factor: float) -> int:
    """Largest H with T * 2^{-(2w+1)} * per_row_factor^{-(H-1)} >= 1 (exact_null.py's law)."""
    import math
    log2T = math.log2(T)
    # T * 2^-(2w+1) * f^-(H-1) >= 1  <=>  (H-1) <= (log2T - (2w+1)) / log2(f)
    budget = log2T - (2 * w + 1)
    if budget < 0:
        return 0
    H = 1 + int(budget / math.log2(per_row_factor))
    return max(H, 0)


def main() -> None:
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 4_000_000
    horizons = [2 ** j for j in range(10, 40) if 2 ** j <= steps]
    if horizons[-1] != steps:
        horizons.append(steps)
    # include a3's own horizons for a direct overlap check
    horizons = sorted(set(horizons) | {2_000_000} if steps >= 2_000_000 else set(horizons))

    band = band_series("30", steps, WMAX)

    res = {"steps": steps, "wmax": WMAX, "horizons": horizons, "families": {}}
    for name, factor in (
        ("all_zeros", 4.0),
        ("checker_A", 2.0),
        ("checker_B", 2.0),
    ):
        heights = {w: max_height(band[:steps], w, name, WMAX) for w in range(WMAX + 1)}
        diag = diagonal_K(band, name, WMAX, horizons)
        hstar_at_T = {
            w: H_star(w, steps, factor) for w in range(WMAX + 1)
        }
        res["families"][name] = {
            "max_height_by_W_at_T": heights,
            "diagonal_K": diag,
            "exact_bernoulli_Hstar_by_W_at_T": hstar_at_T,
            "height_minus_Hstar": {
                w: heights[w] - hstar_at_T[w] for w in range(WMAX + 1)
            },
        }
        ks = [diag[str(T)]["K"] for T in horizons]
        capped = [diag[str(T)]["capped_at_wmax"] for T in horizons]
        print(f"{name:10s} K(T) over horizons {horizons}: {ks}  capped={capped}")

    out_path = os.path.join(HERE, f"extend_growth_{steps}.json")
    with open(out_path, "w") as fh:
        json.dump(res, fh, indent=1)
    print("wrote", out_path)


if __name__ == "__main__":
    main()

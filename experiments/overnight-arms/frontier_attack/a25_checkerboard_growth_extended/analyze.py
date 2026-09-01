"""a25: recurrence-RATE analysis of the three vertical-shift fixed points in the
lone-seed Rule 30 centre band.

Why not just push a3/a22's diagonal K further.  K(T) = max k such that the
(2k+1) x k patch occurs by T.  Under a3's own exact reference law the cost of a
(2k+1) x k checkerboard patch is 2^-(2k+1) for the first row times 2^-(k-1) per
further row, so K is expected near the k solving 3k <= log2 T: K advances by ONE
per EIGHT-fold increase in T.  a3 says the same thing in its own words ("K = 20
would need T ~ 2^60"; 3*20 = 60).  a22 moved T from 2e6 to 4e6, i.e. 2^21 ->
2^22, and could not have moved K by more than 1 in expectation.  Its
INCONCLUSIVE was forced by the statistic, not by the horizon.

What Y-membership actually needs.  z in Y iff for every (W,H) the (2W+1) x H
patch of z occurs in the lone-seed diagram at ARBITRARILY LARGE times.  So the
decisive question per cell (W,h) is not "does it occur" but "does it keep
occurring".  That is a RATE, estimated from millions of occurrences, not a max
over the whole prefix estimated from one.  This script measures, per family,
per half-width W, per height h:

  n_runs(W,h)       maximal runs of length >= h        (clump-corrected count)
  n_overlap(W,h)    overlapping start times            (a3's convention)
  last_start(W,h)   latest start time of an occurrence
  window_counts     n_runs restricted to J disjoint equal time windows

and, as the honest fluctuation band for the MAX statistics that a3/a22 reported,
the per-window maximum run length (J independent draws of the same random
variable whose growth with T was being read as a trend).

All quantities are properties of the single lone-seed orbit.  The uniform
Bernoulli law is used as a reference SCALE only, never as a null hypothesis
(a3 explicitly rejected an ensemble null; Rule 30 on Z/q is not surjective).
Every band reported here is estimated from the orbit's own data across disjoint
time windows.

usage: uv run python analyze.py BAND.bin OUT.json [--windows 32]
"""

from __future__ import annotations

import argparse
import json
import math
import os

import numpy as np

WMAX = 15
FAMILIES = ("all_zeros", "checker_A", "checker_B")
PER_ROW_FACTOR = {"all_zeros": 4.0, "checker_A": 2.0, "checker_B": 2.0}


def family_targets(w: int) -> dict[str, int]:
    a = 0
    b = 0
    for x in range(-w, w + 1):
        if x % 2 == 0:
            a |= 1 << (x + w)
        else:
            b |= 1 << (x + w)
    return {"all_zeros": 0, "checker_A": a, "checker_B": b}


def runs_of(hit: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """(starts, lengths) of maximal runs of True."""
    idx = np.flatnonzero(hit)
    if not idx.size:
        return np.empty(0, np.int64), np.empty(0, np.int64)
    brk = np.flatnonzero(np.diff(idx) != 1)
    starts = np.concatenate(([idx[0]], idx[brk + 1]))
    ends = np.concatenate((idx[brk], [idx[-1]]))
    return starts.astype(np.int64), (ends - starts + 1).astype(np.int64)


def hits(band: np.ndarray, w: int, name: str) -> np.ndarray:
    bw = 2 * w + 1
    codes = (band >> np.uint32(WMAX - w)) & np.uint32((1 << bw) - 1)
    return codes == np.uint32(family_targets(w)[name])


def H_star(w: int, T: int, f: float) -> int:
    budget = math.log2(T) - (2 * w + 1)
    if budget < 0:
        return 0
    return max(1 + int(budget / math.log2(f)), 0)


def analyse_cell(starts, lengths, T, J, hmax_report):
    """Per-height statistics from the run-length encoding of one (family, W)."""
    L = T // J
    out = {}
    if starts.size == 0:
        return out, [0] * J
    # per-window max run length, using the window the run STARTS in
    wid = np.minimum(starts // L, J - 1)
    win_hmax = np.zeros(J, np.int64)
    np.maximum.at(win_hmax, wid, lengths)
    hi = int(lengths.max())
    for h in range(1, min(hi, hmax_report) + 1):
        sel = lengths >= h
        n_runs = int(sel.sum())
        n_overlap = int((lengths[sel] - h + 1).sum())
        last_start = int((starts[sel] + lengths[sel] - h).max())
        wc = np.bincount(wid[sel], minlength=J)[:J]
        out[h] = {
            "n_runs": n_runs,
            "n_overlap": n_overlap,
            "last_start": last_start,
            "window_counts": wc.tolist(),
        }
    return out, win_hmax.tolist()


def diagonal_K(hit_by_w, T0, T1):
    """Largest k with a (2k+1) x k occurrence starting in [T0, T1)."""
    best, wt = 0, -1
    for k in range(0, WMAX + 1):
        s, ln = hit_by_w[k]
        need = max(k, 1)
        lo = np.maximum(s, T0)
        hi = np.minimum(s + ln, T1)
        sel = (hi - lo) >= need
        if not sel.any():
            break
        best = k
        wt = int((hi[sel] - need).max())
    return {"K": best, "latest_start": wt, "capped": best == WMAX}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("band")
    ap.add_argument("out")
    ap.add_argument("--windows", type=int, default=32)
    ap.add_argument("--hmax-report", type=int, default=40)
    a = ap.parse_args()

    band = np.fromfile(a.band, dtype=np.uint32)
    T = int(band.size)
    J = a.windows
    res = {"T": T, "windows": J, "window_len": T // J, "wmax": WMAX, "families": {}}
    dyadic = [2 ** j for j in range(10, 40) if 2 ** j <= T]
    if dyadic[-1] != T:
        dyadic.append(T)
    res["dyadic_horizons"] = dyadic

    for name in FAMILIES:
        fam = {"by_W": {}}
        rle = {}
        for w in range(WMAX + 1):
            s, ln = runs_of(hits(band, w, name))
            rle[w] = (s, ln)
            per_h, win_hmax = analyse_cell(s, ln, T, J, a.hmax_report)
            fam["by_W"][w] = {
                "hmax_at_T": int(ln.max()) if ln.size else 0,
                "Hstar_at_T": H_star(w, T, PER_ROW_FACTOR[name]),
                "window_hmax": win_hmax,
                "hmax_by_horizon": {
                    str(Tj): int(
                        np.max(np.minimum(ln, np.maximum(Tj - s, 0)), initial=0)
                    )
                    for Tj in dyadic
                },
                "per_h": {str(h): v for h, v in per_h.items()},
            }
        fam["diagonal_K_by_horizon"] = {
            str(Tj): diagonal_K(rle, 0, Tj) for Tj in dyadic
        }
        # K restricted to each disjoint window: J independent draws of the same
        # random variable, which is the fluctuation band for K itself.
        L = T // J
        fam["diagonal_K_by_window"] = [
            diagonal_K(rle, j * L, (j + 1) * L)["K"] for j in range(J)
        ]
        res["families"][name] = fam
        print(f"{name}: K(T)={fam['diagonal_K_by_horizon'][str(T)]}  "
              f"K per window={fam['diagonal_K_by_window']}")

    with open(a.out, "w") as fh:
        json.dump(res, fh)
    print("wrote", a.out, os.path.getsize(a.out), "bytes")


if __name__ == "__main__":
    main()

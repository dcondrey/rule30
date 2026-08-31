"""The Rule 90 control, done exactly and without a width cap.

THEOREM (proved here, verified numerically below).  In the Rule 90 lone-seed
diagram, write t = 2^k + j with 0 <= j < 2^k.  Then

    min { |x| : s(t,x) = 1 }  =  2^k - j.

Proof.  s(t,x) = 1 iff t + x is even and C(t, (t+x)/2) is odd, and by Kummer
C(t,m) is odd iff m is a submask of t.  The bits of t are {k} union bits(j) with
j < 2^k, so the submasks are m = e*2^k + j' with e in {0,1} and j' a submask of
j.  Then x = 2m - t = (2e - 1) 2^k + 2j' - j.  For e = 0, x = 2j' - j - 2^k which
lies in [-j - 2^k, j - 2^k], so |x| >= 2^k - j with equality at j' = j.  For
e = 1, x = 2^k + 2j' - j >= 2^k - j, again with equality at j' = 0.  QED

COROLLARY.  For every half-width W, the band [-W,W] of the Rule 90 lone-seed
diagram is identically ZERO for all t in [2^k, 2^{k+1} - W), an interval of
length 2^k - W.  Hence the all-zero (2W+1) x H patch occurs for every H, and
along the sequence t_k = 2^k the (2k+1) x k all-zero patch occurs for every k.
Therefore

    0^{Z^2} lies in Y_90,

and delta_0 is a vertical-shift-invariant measure on Y_90 assigning the centre
cell density 0.  R8's sufficient target is FALSE for Rule 90 -- exactly, with no
finite-horizon extrapolation.  This is the inverted control the Rule 90 filter
(PATH.md section 0) demands: the route's own concession, made into a witness.

The Rule 30 arm in band_census.py / recurrence.py cannot be proved this way.  It
is measured, and its kill is empirical.  That asymmetry is the honest finding.

Run:  uv run python rule90_exact.py [--steps N]
"""

from __future__ import annotations

import argparse
import json
import os

import numpy as np

from band_census import HERE


def minabs_bruteforce(t: int) -> int:
    """min |2m - t| over submasks m of t.  Independent of the theorem."""
    if t == 0:
        return 0
    best = None
    m = t
    while True:  # standard submask enumeration
        v = abs(2 * m - t)
        best = v if best is None else min(best, v)
        if m == 0:
            break
        m = (m - 1) & t
    return best


def minabs_formula(t: np.ndarray) -> np.ndarray:
    """2^k - j where t = 2^k + j.  Vectorised."""
    k = np.floor(np.log2(t)).astype(np.int64)
    return (np.int64(1) << k) * 2 - t


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=2_000_000)
    ap.add_argument("--verify-to", type=int, default=200_000)
    args = ap.parse_args()

    # ---- verify the theorem against brute-force submask enumeration
    ts = list(range(1, 4096)) + [
        int(x) for x in np.unique(
            np.random.default_rng(0).integers(4096, args.verify_to, size=4000)
        )
    ]
    bad = [t for t in ts
           if minabs_bruteforce(t) != int(minabs_formula(np.array([t]))[0])]
    print(f"theorem verified on {len(ts)} values of t (1..{args.verify_to}); "
          f"mismatches: {len(bad)}")
    assert not bad, bad[:10]

    T = args.steps
    t = np.arange(1, T, dtype=np.int64)
    ma = minabs_formula(t)  # min |x| of a one in row t

    res = {"steps": T, "theorem_mismatches": len(bad), "n_verified": len(ts)}

    def measured_run(W: int, H: int) -> int:
        """Longest run of consecutive t in [1,H) with minabs(t) > W."""
        idx = np.flatnonzero(ma[: H - 1] > W)
        if not idx.size:
            return 0
        brk = np.flatnonzero(np.diff(idx) != 1)
        starts = np.concatenate(([idx[0]], idx[brk + 1]))
        ends = np.concatenate((idx[brk], [idx[-1]]))
        return int((ends - starts + 1).max())

    def closed_form_run(W: int, H: int) -> int:
        """Same quantity from the theorem: on block [2^a, 2^(a+1)) the zero band
        runs from 2^a to 2^(a+1) - W - 1, truncated at H."""
        if W == 0:
            # minabs(t) >= 1 for every t >= 1, so the centre column is zero
            # throughout: the blocks join into one run.
            return H - 1
        best = 0
        a = 0
        while 2 ** a < H:
            lo = 2 ** a
            hi = min(2 ** (a + 1) - W, H)
            best = max(best, hi - lo)
            a += 1
        return best

    # ---- all-zero band height at half-width W, no cap on W
    heights = {}
    for W in [0, 1, 2, 4, 8, 16, 32, 64, 128, 1024, 8192, 65536]:
        heights[str(W)] = {
            "measured": measured_run(W, T),
            "closed_form": closed_form_run(W, T),
        }
    res["allzero_band_height"] = heights
    assert all(v["measured"] == v["closed_form"] for v in heights.values()), heights

    # ---- diagonal K: max k with a (2k+1) x k all-zero patch, UNCAPPED in k
    horizons = [2 ** j for j in range(10, 64) if 2 ** j <= T]
    if horizons[-1] != T:
        horizons.append(T)
    diag = {}
    for H in horizons:
        lo, hi = 0, H  # monotone in k, binary search on the closed form
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if closed_form_run(mid, H) >= mid:
                lo = mid
            else:
                hi = mid - 1
        # spot-check the closed form against the measured runs at the answer
        assert measured_run(lo, H) == closed_form_run(lo, H)
        diag[str(H)] = lo
    res["diagonal_K_rule90"] = diag
    print("rule 90 diagonal K (UNCAPPED in k), T = 2^10 ..", T)
    print("  ", [diag[str(H)] for H in horizons])
    print("  all-zero band height by W:",
          {w: heights[w] for w in ("0", "1", "8", "64", "1024", "65536")})

    path = os.path.join(HERE, "rule90_exact.json")
    with open(path, "w") as fh:
        json.dump(res, fh, indent=1)
    print("wrote", path)


if __name__ == "__main__":
    main()

"""a25: turn analyze.py's JSON into the tables the verdict needs.

Four questions.  Every band is estimated from the single orbit's own data across
J disjoint time windows -- never from an assumed distribution.  The uniform
Bernoulli law appears as a reference SCALE only (a3 explicitly rejected an
ensemble null: Rule 30 on Z/q is not surjective).

Q1  BAND ON THE MAX STATISTICS a3/a22 REPORTED.  K(T) and h_max(W,T) are maxima
    over the prefix.  Bootstrapping the J windows gives the sampling band of
    those maxima.  If a22's observed change over one horizon doubling sits
    inside that band, the change -- in either direction -- was not evidence.

Q2  DOES IT KEEP OCCURRING (the thing Y-membership actually needs).  Per (W,h):
    counts of maximal runs of length >= h in each of J disjoint windows.
    Saturation = the late windows' rate collapsing.  Tested three ways:
    second-half/first-half with dispersion estimated from the data, a Spearman
    trend over all J windows, and the last window's count on its own.

Q3  PRE-REGISTERED DISCONFIRMING SIGNATURE.  log2 rate(W,h) against h.  The
    reference predicts a straight line.  Saturation shows as downward
    CURVATURE: the effective per-row cost steepening with h.  This can fire
    negative inside the measured range, which is what makes it a test.

Q4  DISTINGUISHABILITY.  Growth rate of h_max(W,.) in rows per doubling of T,
    fitted over the dyadic horizons, against the band from Q1; and the horizon
    at which the diagonal K would separate from flat at 3 sigma.

usage: uv run python report.py ANALYSIS.json [--json OUT.json]
"""

from __future__ import annotations

import argparse
import json
import math

import numpy as np

FAMILIES = ("all_zeros", "checker_A", "checker_B")
FACTOR = {"all_zeros": 4.0, "checker_A": 2.0, "checker_B": 2.0}
RNG = np.random.default_rng(20260831)
NBOOT = 20000
# Theta(T^2) kernel constant, fitted from this arm's own C-kernel checkpoints
# (402.7 s at T = 4,194,304 on one core of an Apple M4).
KCONST = 402.7 / 4194304.0 ** 2


def boot_max(win_vals: np.ndarray) -> tuple[float, float, list]:
    """Bootstrap band for max over the J windows (resample windows w/ repl.)."""
    J = win_vals.size
    idx = RNG.integers(0, J, size=(NBOOT, J))
    mx = win_vals[idx].max(axis=1)
    return float(mx.mean()), float(mx.std(ddof=1)), [float(np.percentile(mx, 2.5)),
                                                     float(np.percentile(mx, 97.5))]


def scale_growth(win_vals: np.ndarray):
    """Growth of a MAX statistic per doubling of horizon, from disjoint windows.

    The J windows are independent replicates of the same length L.  Grouping
    them into blocks of 2^m consecutive windows and taking the block max gives
    an unbiased estimate of E[max over a horizon of length 2^m * L].  Regressing
    that mean on m gives d(statistic)/d(doubling of T) with a bootstrap CI --
    unlike a regression of the PREFIX max on log2 T, whose points are nested
    samples and whose OLS standard error is therefore meaningless.

    Returns (slope, [lo, hi] 95% CI, per-scale means).
    """
    J = win_vals.size
    # Only scales with >= 4 blocks.  The top scale has a single block, i.e. the
    # prefix max itself, which caps the fit and biases the slope DOWNWARD; this
    # estimator is therefore a lower bound on the growth rate, and the
    # rate-slope estimator (-1/slope of log2 rate vs h) is the primary one.
    M = max(int(math.log2(J)) - 2, 1)

    def fit(v):
        g = []
        for m in range(M + 1):
            blocks = v[: (J // 2 ** m) * 2 ** m].reshape(-1, 2 ** m)
            g.append(blocks.max(axis=1).mean())
        xs = np.arange(M + 1, dtype=float)
        ys = np.array(g)
        A = np.vstack([xs, np.ones_like(xs)]).T
        return float(np.linalg.lstsq(A, ys, rcond=None)[0][0]), ys

    slope, g = fit(win_vals)
    idx = RNG.integers(0, J, size=(2000, J))
    bs = np.array([fit(win_vals[i])[0] for i in idx])
    return slope, [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], g.tolist()


def halves_test(c: np.ndarray):
    J = c.size
    a, b = c[: J // 2], c[J // 2:]
    ma, mb, m = a.mean(), b.mean(), c.mean()
    if m == 0:
        return float("nan"), float("nan"), float("nan")
    phi = max(c.var(ddof=1) / m, 1.0)  # floor at Poisson: conservative
    se = math.sqrt(phi * m * (1.0 / a.size + 1.0 / b.size))
    return (mb / ma if ma > 0 else float("inf")), ((mb - ma) / se if se > 0 else float("nan")), phi


def spearman(c: np.ndarray) -> tuple[float, float]:
    J = c.size
    x = np.arange(J, dtype=float)
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(c)).astype(float)
    rho = np.corrcoef(rx, ry)[0, 1]
    z = rho * math.sqrt(J - 1)  # approx, |z|>3 is the flag
    return float(rho), float(z)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("analysis")
    ap.add_argument("--min-count", type=int, default=40)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    with open(a.analysis) as fh:
        R = json.load(fh)
    T, J, L = R["T"], R["windows"], R["window_len"]
    hor = [int(x) for x in R["dyadic_horizons"]]
    out = {"T": T, "J": J, "L": L, "families": {}}
    print(f"# a25 report   T={T:,}  J={J} disjoint windows of {L:,}  "
          f"bootstrap B={NBOOT}\n")

    for name in FAMILIES:
        fam = R["families"][name]
        f = FACTOR[name]
        fo = {}
        print(f"\n{'='*78}\n## {name}\n")

        # ------------------------------------------------ Q1a diagonal K
        kb = fam["diagonal_K_by_horizon"]
        kw = np.array(fam["diagonal_K_by_window"], dtype=float)
        bm, bsd, bci = boot_max(kw)
        Kf = kb[str(T)]["K"]
        ks = [kb[str(h)]["K"] for h in hor]
        print("K(T), dyadic horizons " + " ".join(f"2^{int(round(math.log2(h)))}" if (h & (h-1)) == 0 else f"{h}" for h in hor))
        print("      " + " ".join(f"{k:>{max(3,len(str(h)))}d}" for k, h in zip(ks, hor)))
        print(f"  K(T) = {Kf};  LATEST occurrence start t = "
              f"{kb[str(T)]['latest_start']:,} = {kb[str(T)]['latest_start']/T:.3f} T")
        print(f"  per-window K (J={J} draws): {[int(v) for v in kw]}")
        print(f"  BAND on K(T): bootstrap over windows -> mean {bm:.2f}, sd {bsd:.2f}, "
              f"95% [{bci[0]:.0f}, {bci[1]:.0f}]")
        ksl, kci, kg = scale_growth(kw)
        ref = 1 / 6 if name == "all_zeros" else 1 / 3
        print(f"  GROWTH of K per doubling of horizon (block-max over disjoint "
              f"windows, bootstrap CI):\n    dK/d(doubling) = {ksl:+.4f} "
              f"[{kci[0]:+.4f}, {kci[1]:+.4f}]   reference law {ref:+.4f}   "
              f"FLAT would be 0.0000")
        print(f"    per-scale mean block-max K, scales L*2^m: "
              f"{[round(v,3) for v in kg]}")
        dks = np.diff([kb[str(h)]["K"] for h in hor if (h & (h - 1)) == 0])
        print(f"    dyadic doublings with delta-K = 0: {int((dks==0).sum())}/"
              f"{dks.size}  -- a single doubling showing 'flat' is the MODAL "
              f"outcome under growth")
        nat = int((kw == Kf).sum())
        lastw = int(np.max(np.flatnonzero(kw == Kf), initial=-1))
        print(f"  windows attaining K(T): {nat}/{J}; latest such window {lastw} "
              f"(t in [{lastw*L:,}, {(lastw+1)*L:,}))")
        fo["K"] = {"K_at_T": Kf, "latest_start": kb[str(T)]["latest_start"],
                   "by_horizon": {str(h): kb[str(h)]["K"] for h in hor},
                   "per_window": [int(v) for v in kw], "boot_sd": bsd, "boot_ci": bci,
                   "windows_attaining": nat, "latest_window_attaining": lastw}

        # ------------------------------------------------ Q1b h_max(W,T)
        print("\n  W  h_max  boot band       rows/doubling: blockmax[95%CI] "
              "(lower bd)   descriptive   h_late  n_runs   Hstar")
        fo["by_W"] = {}
        for w in range(16):
            d = fam["by_W"][str(w)]
            if d["hmax_at_T"] == 0:
                continue
            wh = np.array(d["window_hmax"], dtype=float)
            m2, sd2, ci2 = boot_max(wh)
            # growth rate: h_max vs log2 T over dyadic horizons (T >= 2^14)
            rate, (rlo, rhi), _g = scale_growth(wh)
            # descriptive: OLS of the PREFIX max on log2 T over dyadic horizons.
            # Nested samples, so no valid CI -- reported only as corroboration
            # of the rate-slope estimator, never as an interval.
            xs = np.array([math.log2(h) for h in hor if h >= 2 ** 12], float)
            ys = np.array([d["hmax_by_horizon"][str(h)] for h in hor
                           if h >= 2 ** 12], float)
            desc = float(np.polyfit(xs, ys, 1)[0])
            hl, nl = 0, 0
            for hs, v in d["per_h"].items():
                if v["last_start"] >= T - L and int(hs) > hl:
                    hl, nl = int(hs), v["n_runs"]
            print(f"  {w:2d}  {d['hmax_at_T']:5d}  {sd2:4.2f}[{ci2[0]:.0f},{ci2[1]:.0f}]"
                  f"   {rate:+6.3f} [{rlo:+.3f},{rhi:+.3f}]        {desc:+6.3f}"
                  f"   {hl:4d} {nl:8d} {d['Hstar_at_T']:5d}")
            fo["by_W"][w] = {"h_max": d["hmax_at_T"], "boot_sd": sd2, "boot_ci": ci2,
                             "rows_per_doubling_blockmax": rate,
                             "rpd_blockmax_ci": [rlo, rhi],
                             "rows_per_doubling_descriptive": desc,
                             "h_late": hl, "n_runs_h_late": nl,
                             "Hstar": d["Hstar_at_T"],
                             "hmax_by_horizon": d["hmax_by_horizon"]}

        # ------------------------------------------------ Q2 rate stability
        cells, seen = [], set()
        for w in range(16):
            d = fam["by_W"][str(w)]
            for hs in sorted(d["per_h"], key=int):
                v = d["per_h"][hs]
                if v["n_runs"] < a.min_count:
                    continue
                key = tuple(v["window_counts"])
                dup = key in seen
                seen.add(key)
                c = np.array(v["window_counts"], dtype=float)
                ratio, z, phi = halves_test(c)
                rho, zs_ = spearman(c)
                lastc = c[-1]
                exp_last = c[:-1].mean()
                cells.append({"W": w, "h": int(hs), "n_runs": v["n_runs"],
                              "rate_per_1e6": v["n_runs"] / T * 1e6, "phi": phi,
                              "ratio": ratio, "z": z, "rho": rho, "z_spearman": zs_,
                              "last_window_count": float(lastc),
                              "mean_earlier_windows": float(exp_last),
                              "last_start_frac": v["last_start"] / T,
                              "duplicate_of_earlier_cell": dup})
        uniq = [c for c in cells if not c["duplicate_of_earlier_cell"]]
        zs = np.array([c["z"] for c in uniq if np.isfinite(c["z"])])
        zsp = np.array([c["z_spearman"] for c in uniq if np.isfinite(c["z_spearman"])])
        print(f"\n  rate stability over {len(cells)} cells with n_runs>={a.min_count} "
              f"({len(uniq)} with distinct window-count vectors; the rest are exact "
              f"diagonal duplicates, W+h const)")
        print(f"    halves z:   mean {zs.mean():+.3f}  sd {zs.std(ddof=1):.3f}  "
              f"range [{zs.min():+.2f},{zs.max():+.2f}]   z<-3 (DECLINE): "
              f"{int((zs < -3).sum())}   |z|>3: {int((np.abs(zs) > 3).sum())} "
              f"(expected ~{0.0027*zs.size:.2f} over the distinct cells; the "
              f"effective number of independent cells is smaller still, since "
              f"neighbouring W overlap)")
        print(f"    Spearman z: mean {zsp.mean():+.3f}  sd {zsp.std(ddof=1):.3f}  "
              f"range [{zsp.min():+.2f},{zsp.max():+.2f}]   z<-3: "
              f"{int((zsp < -3).sum())}")
        print(f"    dispersion phi: median {np.median([c['phi'] for c in uniq]):.2f} "
              "(1.0 = Poisson; the test floors phi at 1, so it is conservative)")
        # the deepest cells, where saturation would show first
        deep = sorted(uniq, key=lambda c: c["n_runs"])[:8]
        print("    deepest cells (smallest n_runs):")
        print("      W   h  n_runs  last_win  mean_earlier   ratio      z   "
              "last_start/T")
        for c in deep:
            print(f"      {c['W']:2d} {c['h']:3d} {c['n_runs']:7d} "
                  f"{c['last_window_count']:9.0f} {c['mean_earlier_windows']:13.2f} "
                  f"{c['ratio']:7.3f} {c['z']:6.2f}   {c['last_start_frac']:.4f}")
        fo["cells"] = cells

        # ------------------------------------------------ Q3 curvature
        print(f"\n  log2(rate) vs h  (reference slope {-math.log2(f):+.0f} for W>=1)")
        print("  The slope IS the growth law: rate(W,h) ~ 2^(slope*h) means the")
        print("  max height at half-width W grows by -1/slope rows per doubling of T.")
        print("  Saturation = downward curvature.  A quadratic saturating term")
        print("  log2 r = slope*h - delta*h^2/2 has 2nd difference -delta, so the")
        print("  curvature column bounds delta; |slope|/delta is how many further")
        print("  rows the linear law would have to hold before the growth rate halves.")
        print("   W  h-range   slope +/- se   rows/doubling   curvature +/- se   "
              "z    delta_bound(3se)  rows before rate halves")
        print("  se and curvature-se are ACROSS-WINDOW spreads (J independent "
              "refits), not\n  OLS residual errors: the counts are nested in h.")
        fo["slopes"] = {}
        for w in range(16):
            d = fam["by_W"][str(w)]
            hh, rr = [], []
            for hs in sorted(d["per_h"], key=int):
                v = d["per_h"][hs]
                if v["n_runs"] >= a.min_count:
                    hh.append(int(hs))
                    rr.append(math.log2(v["n_runs"] / T))
            if len(hh) < 5:
                continue
            hx = np.array(hh, float)
            ry = np.array(rr, float)
            A = np.vstack([hx, np.ones_like(hx)]).T
            coef = np.linalg.lstsq(A, ry, rcond=None)[0]
            d2 = np.diff(ry, 2)
            # ERROR BARS FROM THE DISJOINT WINDOWS, NOT FROM THE FIT.
            # n_runs(h) counts runs of length >= h, so the point at h+1 is a
            # SUBSET of the point at h: consecutive points are nested and an
            # OLS residual standard error on the pooled fit is meaningless.
            # Refit inside each of the J windows independently and take the
            # spread across windows.  Restrict to the h-range where every
            # window has at least MINW counts, so no window contributes a log
            # of a small or zero count.
            MINW = 5
            wc = np.array([d["per_h"][str(hv)]["window_counts"] for hv in hh],
                          dtype=float)  # (n_h, J)
            okh = (wc >= MINW).all(axis=1)
            if okh.sum() >= 4:
                hw = hx[okh]
                lw = np.log2(wc[okh] / (T / J))
                Aw = np.vstack([hw, np.ones_like(hw)]).T
                sw = np.array([np.linalg.lstsq(Aw, lw[:, j], rcond=None)[0][0]
                               for j in range(lw.shape[1])])
                d2w = np.array([np.diff(lw[:, j], 2).mean()
                                for j in range(lw.shape[1])])
                se = sw.std(ddof=1) / math.sqrt(sw.size)
                cse = d2w.std(ddof=1) / math.sqrt(d2w.size)
                nwin_h = int(okh.sum())
            else:
                se = cse = float("nan")
                nwin_h = 0
            rpd = -1.0 / coef[0]
            rpd_se = se / coef[0] ** 2
            dbound = 3 * cse + max(0.0, -d2.mean())  # one-sided bound on delta
            halve = abs(coef[0]) / dbound if dbound > 0 else float("inf")
            zc = d2.mean() / cse if cse > 0 else float("nan")
            print(f"  {w:2d}  {hh[0]:2d}..{hh[-1]:2d}   {coef[0]:+.4f}+/-{se:.4f}"
                  f"   {rpd:.4f}+/-{rpd_se:.4f}   {d2.mean():+.4f}+/-{cse:.4f} "
                  f"{zc:+5.2f}   {dbound:.4f}   {halve:8.1f}")
            fo["slopes"][w] = {"h_lo": hh[0], "h_hi": hh[-1], "slope": coef[0],
                               "slope_se": se, "rows_per_doubling": rpd,
                               "rpd_se": rpd_se, "curv": float(d2.mean()),
                               "curv_se": float(cse), "n_curv": int(d2.size),
                               "window_fit_h_points": nwin_h,
                               "delta_bound_3se": dbound, "rows_before_halving": halve}
        out["families"][name] = fo

    # ------------------------------------------------ Q4 distinguishability
    print(f"\n{'='*78}\n## Q4 how much further would K alone need to go\n")
    print("  Reference law: a checkerboard (2k+1) x k patch costs 2^-(2k+1) for its")
    print("  first row and 2^-(k-1) per further row, so K advances by 1 per 8x in T")
    print("  (3k <= log2 T).  a3 states the same thing as 'K=20 needs T ~ 2^60'.")
    print("  dK/d(doubling of T) = 1/3 for the checkerboards, 1/6 for all-zeros")
    print("  (per-row factor 4 -> 2k+1+2(k-1) <= log2 T).\n")
    print("  K is integer-valued and moves in steps of 1.  Under the growth")
    print("  hypothesis its increments over D doublings are ~Poisson with mean")
    print("  s*D.  To make 'K did not move at all' improbable (P < 0.05) needs")
    print("  s*D > 3, i.e. D > 3/s doublings.  Generation is Theta(T^2) with the")
    print(f"  constant fitted from this arm's own C-kernel checkpoints, "
          f"{KCONST:.3g} s per step^2.\n")
    print("  family       s=dK/doubling   D needed   T needed      single-core "
          "kernel time")
    for name in FAMILIES:
        s = 1 / 6 if name == "all_zeros" else 1 / 3
        D = 3 / s
        Tn = T * 2 ** D
        secs = KCONST * Tn ** 2
        print(f"  {name:11s}  {s:11.3f}   {D:8.0f}   {Tn:9.3e}   "
              f"{secs/86400/365.25:12.3g} core-years")
    print("\n  So the diagonal K cannot be made decisive by any horizon: the cost")
    print("  of one more unit of K is 8x the horizon and therefore 64x the")
    print("  compute, and several units are needed before 'flat' is excluded.")
    print("  Cost of the next few units of K from this arm's horizon:")
    print("    +dK   T needed      kernel time")
    for dk in (1, 2, 3):
        Tn = T * 8 ** dk
        print(f"    +{dk}    {Tn:9.3e}   {KCONST*Tn**2/86400:12.4g} days")
    print("\n  The rate statistic is what makes the question answerable at a")
    print("  horizon that fits in hours: it uses up to 1e6 occurrences per cell")
    print("  instead of one maximum, so its precision improves as sqrt(T) rather")
    print("  than log(T).")

    if a.json:
        with open(a.json, "w") as fh:
            json.dump(out, fh, indent=1)
        print("\nwrote", a.json)


if __name__ == "__main__":
    main()

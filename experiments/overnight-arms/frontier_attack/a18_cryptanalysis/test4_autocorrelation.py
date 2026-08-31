"""Test 4 (PREREG.md): autocorrelation at every lag 1..100,000.

A(l) = (1/(T-l)) * sum_t (-1)^(c_t XOR c_{t+l}) = (1/(T-l)) * sum_t x_t x_{t+l}
with x_t = 1 - 2 c_t in {+1,-1}.  Under i.i.d. Bernoulli(1/2), A(l) is
asymptotically N(0, 1/(T-l)), so z(l) = A(l) * sqrt(T-l) ~ N(0,1).

Computed by FFT (linear, zero-padded), which is exact for the raw lag products.

A keystream with a detectable autocorrelation peak is a broken cipher, so this
is the single cheapest cryptanalytic distinguisher and it is run at every lag,
not a sampled subset.

Run: uv run python test4_autocorrelation.py
"""

from __future__ import annotations

import json
import logging
import pathlib

import numpy as np
from scipy import stats

HERE = pathlib.Path(__file__).resolve().parent
SEQ = HERE / "seq"
LMAX = 100_000
BONF_Z = 5.032  # PREREG global Bonferroni threshold, alpha=0.05 over N=100,838

log = logging.getLogger("t4")


def acf_z(bits: np.ndarray, lmax: int) -> np.ndarray:
    """z(l) for l=1..lmax."""
    T = bits.size
    x = (1.0 - 2.0 * bits.astype(np.float64))
    n = 1 << int(np.ceil(np.log2(2 * T)))
    f = np.fft.rfft(x, n)
    r = np.fft.irfft(f * np.conj(f), n)[: lmax + 1]
    lags = np.arange(1, lmax + 1)
    a = r[1:] / (T - lags)
    return a * np.sqrt(T - lags)


def summarize(name: str, z: np.ndarray) -> dict:
    absz = np.abs(z)
    imax = int(np.argmax(absz))
    p_raw = 2.0 * stats.norm.sf(absz)
    ks = stats.kstest(z, "norm")
    return {
        "sequence": name,
        "lags": int(z.size),
        "max_abs_z": float(absz[imax]),
        "argmax_lag": imax + 1,
        "p_raw_at_max": float(p_raw[imax]),
        "p_bonferroni_at_max": float(min(1.0, p_raw[imax] * 100_838)),
        "n_exceed_bonferroni_5.032": int((absz > BONF_Z).sum()),
        "frac_abs_z_gt_1.96": float((absz > 1.96).mean()),
        "frac_abs_z_gt_2.58": float((absz > 2.5758).mean()),
        "mean_z": float(z.mean()),
        "sd_z": float(z.std(ddof=1)),
        "ks_stat_vs_N01": float(ks.statistic),
        "ks_p_vs_N01": float(ks.pvalue),
        "verdict": ("REJECT (bias detected)" if (absz > BONF_Z).any() else "no lag survives Bonferroni"),
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    names = ["rule30", "rule90", "lfsr32", "bern51", "lag1000", "copy1000"] + [f"iid_{k:02d}" for k in range(20)]
    out: dict = {"lmax": LMAX, "bonferroni_z": BONF_Z, "global_N": 100_838, "results": {}}
    z30 = None
    for name in names:
        bits = np.load(SEQ / f"{name}.npy")
        z = acf_z(bits, LMAX)
        if name == "rule30":
            z30 = z
        s = summarize(name, z)
        out["results"][name] = s
        log.info("%-9s max|z|=%10.3f at lag %6d  n>%.3f: %d  frac>1.96=%.4f  KS p=%.3g  %s",
                 name, s["max_abs_z"], s["argmax_lag"], BONF_Z,
                 s["n_exceed_bonferroni_5.032"], s["frac_abs_z_gt_1.96"], s["ks_p_vs_N01"],
                 s["verdict"])

    # i.i.d. null band on max|z|, the operative threshold (row 8 convention).
    iid_max = [out["results"][f"iid_{k:02d}"]["max_abs_z"] for k in range(20)]
    out["iid_null_band_max_abs_z"] = {
        "min": float(np.min(iid_max)), "max": float(np.max(iid_max)),
        "mean": float(np.mean(iid_max)), "sd": float(np.std(iid_max, ddof=1)),
    }
    out["rule30_vs_iid_seed_max"] = bool(
        out["results"]["rule30"]["max_abs_z"] > np.max(iid_max))
    log.info("iid null band on max|z| over 20 seeds: [%.3f, %.3f]; rule30 exceeds seed max: %s",
             np.min(iid_max), np.max(iid_max), out["rule30_vs_iid_seed_max"])

    assert z30 is not None
    np.save(HERE / "test4_rule30_z.npy", z30.astype(np.float32))
    (HERE / "test4_autocorrelation_output.json").write_text(json.dumps(out, indent=2))
    lines = [f"Test 4: autocorrelation, lags 1..{LMAX}, T=2^20, Bonferroni |z|>{BONF_Z} (N=100838)", ""]
    lines.append(f"{'sequence':<9} {'max|z|':>12} {'lag':>7} {'#>bonf':>8} {'>1.96':>8} {'>2.58':>8} {'KS p':>10}")
    for name in names:
        s = out["results"][name]
        lines.append(f"{name:<9} {s['max_abs_z']:>12.3f} {s['argmax_lag']:>7d} "
                     f"{s['n_exceed_bonferroni_5.032']:>8d} {s['frac_abs_z_gt_1.96']:>8.4f} "
                     f"{s['frac_abs_z_gt_2.58']:>8.4f} {s['ks_p_vs_N01']:>10.3g}")
    lines += ["", f"iid null band max|z|: [{np.min(iid_max):.3f}, {np.max(iid_max):.3f}]",
              f"rule30 exceeds iid seed max: {out['rule30_vs_iid_seed_max']}",
              f"rule30 verdict: {out['results']['rule30']['verdict']}"]
    (HERE / "test4_autocorrelation_output.txt").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()

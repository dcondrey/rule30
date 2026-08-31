"""Depth extension to T = 2^21 = 2,097,152, past register row 8's T >= 2,000,000.

The pre-registered ledger is at T = 2^20 and that remains the primary result:
re-scoring the whole battery at a new depth and reporting whichever depth looks
better would defeat the pre-registration.  This is a SEPARATE confirmation at
greater depth, with the SAME statistics and the SAME thresholds, reported apart
from the N = 100,838 ledger.

Extended: test 4 (autocorrelation, all 100,000 lags) and test 2 (correlation
attack, the same 780-cell grid), the two tests whose power scales with T.  Test 3
is unchanged by construction -- its block protocol reads the first 10^6 bits
either way -- and test 1 already ran to n = 2^20 in test1b audit B.

The i.i.d. null band is regenerated at the same T so the comparison is like for
like.

Run: uv run python depth_extension.py     (about 8 minutes; generation is
quadratic, so 2^21 costs 4x the 2^20 run)
"""

from __future__ import annotations

import importlib.util
import json
import logging
import pathlib
import time

import numpy as np
from scipy import stats

from gen_sequences import centre_column
from test2_correlation_attack import KS, eps_for, lags_for, windows
from test4_autocorrelation import acf_z

HERE = pathlib.Path(__file__).resolve().parent
SEQ = HERE / "seq"
REPO = HERE.parents[3]
T2 = 1 << 21
GATE_BITS = 1 << 16
LMAX = 100_000
BONF_Z = 5.032
N_NULL = 20

log = logging.getLogger("deep")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    cache = SEQ / "rule30_2pow21.npy"
    if cache.exists():
        c30 = np.load(cache)
    else:
        t0 = time.time()
        c30 = centre_column(30, T2)
        log.info("generated %d centre bits in %.1f s", T2, time.time() - t0)
        np.save(cache, c30)
    assert c30.size == T2

    # GATE, again, at the new depth.
    spec = importlib.util.spec_from_file_location(
        "repo_truth2", REPO / "experiments/rule30/center_column.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    truth = np.fromiter(mod.center_column(GATE_BITS), dtype=np.uint8, count=GATE_BITS)
    gate = bool(np.array_equal(c30[:GATE_BITS], truth))
    log.info("GATE vs repo center_column.py (%d bits): %s", GATE_BITS, "MATCH" if gate else "DIVERGE")
    if not gate:
        raise SystemExit("gate failed at depth 2^21")

    out: dict = {"T": T2, "row8_depth_reference": 2_000_000, "gate": gate,
                 "in_registered_ledger": False,
                 "ones": int(c30.sum()), "density": float(c30.mean())}
    log.info("density at T=2^21: %.7f", c30.mean())

    nulls = [np.random.default_rng(7_000_000 + k).integers(0, 2, size=T2, dtype=np.uint8)
             for k in range(N_NULL)]

    # ---- test 4 at 2^21 ---------------------------------------------------
    z30 = acf_z(c30, LMAX)
    nmax = [float(np.abs(acf_z(a, LMAX)).max()) for a in nulls]
    a30 = np.abs(z30)
    p_at_max = float(2 * stats.norm.sf(a30.max()))
    out["test4"] = {
        "lags": LMAX, "max_abs_z": float(a30.max()), "argmax_lag": int(a30.argmax()) + 1,
        "p_raw_at_max": p_at_max, "p_bonferroni_at_max": float(min(1.0, p_at_max * 100_838)),
        "n_exceed_5.032": int((a30 > BONF_Z).sum()),
        "frac_gt_1.96": float((a30 > 1.96).mean()), "frac_gt_2.58": float((a30 > 2.5758).mean()),
        "ks_p_vs_N01": float(stats.kstest(z30, "norm").pvalue),
        "iid_seed_max_band": [float(np.min(nmax)), float(np.max(nmax))],
        "exceeds_iid_seed_max": bool(a30.max() > np.max(nmax)),
    }
    log.info("test4 @2^21: max|z|=%.3f at lag %d, %d lags > %.3f, iid band [%.3f, %.3f], exceeds=%s",
             a30.max(), a30.argmax() + 1, (a30 > BONF_Z).sum(), BONF_Z,
             np.min(nmax), np.max(nmax), out["test4"]["exceeds_iid_seed_max"])

    # ---- test 2 at 2^21 ---------------------------------------------------
    eps30: dict[str, float] = {}
    epsn: dict[int, list[list[float]]] = {}
    for k in KS:
        w30 = windows(c30, k)
        wn = [windows(a, k) for a in nulls]
        ds = lags_for(k)
        epsn[k] = []
        for d in ds:
            eps30[f"k{k}_d{d}"] = eps_for(c30, w30, k, d)
            epsn[k].append([eps_for(nulls[i], wn[i], k, d) for i in range(N_NULL)])
        log.info("test2 @2^21: k=%d done", k)

    rows = []
    for k in KS:
        pooled = np.array(epsn[k]).ravel()
        m, sd = float(pooled.mean()), float(pooled.std(ddof=1))
        seedmax = float(np.array(epsn[k]).max(axis=0).max())
        for i, d in enumerate(lags_for(k)):
            e = eps30[f"k{k}_d{d}"]
            z = (e - m) / sd
            rows.append({"k": k, "delta": d, "eps": e, "z": z,
                         "p_raw_onesided": float(stats.norm.sf(z)),
                         "exceeds_iid_seed_max": bool(e > seedmax)})
    rows.sort(key=lambda r: -r["z"])
    out["test2"] = {
        "ledger": len(rows), "max_z": rows[0]["z"], "at": {"k": rows[0]["k"], "delta": rows[0]["delta"]},
        "eps_at_max": rows[0]["eps"], "p_raw_onesided_at_max": rows[0]["p_raw_onesided"],
        "p_bonferroni_at_max": float(min(1.0, rows[0]["p_raw_onesided"] * 100_838)),
        "n_surviving_bonferroni": sum(1 for r in rows if r["p_raw_onesided"] * 100_838 < 0.05),
        "n_exceeding_iid_seed_max": sum(1 for r in rows if r["exceeds_iid_seed_max"]),
        "all_rows": rows,
    }
    log.info("test2 @2^21: max z=%.3f at k=%d d=%d, #bonf=%d, #>seedmax=%d",
             rows[0]["z"], rows[0]["k"], rows[0]["delta"],
             out["test2"]["n_surviving_bonferroni"], out["test2"]["n_exceeding_iid_seed_max"])

    clean = (out["test4"]["n_exceed_5.032"] == 0 and out["test2"]["n_surviving_bonferroni"] == 0)
    out["verdict"] = (
        f"NO BIAS FOUND at T = 2^21 = {T2}, which exceeds register row 8's T >= 2,000,000. "
        f"Autocorrelation max |z| = {out['test4']['max_abs_z']:.3f} over 100,000 lags "
        f"(Bonferroni-adjusted p = {out['test4']['p_bonferroni_at_max']:.3f}); correlation-attack "
        f"max z = {out['test2']['max_z']:.3f} over 780 cells "
        f"(adjusted p = {out['test2']['p_bonferroni_at_max']:.3f}). Doubling the depth moved "
        f"nothing. As everywhere in this arm, finite data bounds a test's power at that "
        f"depth and cannot establish an infinite statement (obstruction H)."
        if clean else
        f"DEVIATION AT T = 2^21: test4 exceedances {out['test4']['n_exceed_5.032']}, "
        f"test2 Bonferroni survivors {out['test2']['n_surviving_bonferroni']}. Audit before reporting.")
    log.info("%s", out["verdict"])

    (HERE / "depth_extension_output.json").write_text(json.dumps(out, indent=2))
    lines = [f"Depth extension: T = 2^21 = {T2} (row 8 reference: T >= 2,000,000)",
             f"GATE vs repo center_column.py: {'MATCH' if gate else 'DIVERGE'}",
             f"density = {out['density']:.7f}  ({out['ones']} ones)",
             "NOT part of the N = 100,838 pre-registered ledger; same statistics, same thresholds.", "",
             "test 4 (autocorrelation, 100,000 lags):",
             f"  max |z|              {out['test4']['max_abs_z']:.3f} at lag {out['test4']['argmax_lag']}",
             f"  Bonferroni-adjusted  {out['test4']['p_bonferroni_at_max']:.4f}",
             f"  lags > 5.032         {out['test4']['n_exceed_5.032']} of {LMAX}",
             f"  frac |z| > 1.96      {out['test4']['frac_gt_1.96']:.4f} (expected 0.0500)",
             f"  KS vs N(0,1)         p = {out['test4']['ks_p_vs_N01']:.4f}",
             f"  iid seed max band    [{out['test4']['iid_seed_max_band'][0]:.3f}, "
             f"{out['test4']['iid_seed_max_band'][1]:.3f}]; exceeds = {out['test4']['exceeds_iid_seed_max']}",
             "", "test 2 (correlation attack, 780 cells):",
             f"  max z                {out['test2']['max_z']:.3f} at k={out['test2']['at']['k']}, "
             f"Delta={out['test2']['at']['delta']}, eps={out['test2']['eps_at_max']:.6f}",
             f"  Bonferroni-adjusted  {out['test2']['p_bonferroni_at_max']:.4f}",
             f"  surviving Bonferroni {out['test2']['n_surviving_bonferroni']} of 780",
             f"  exceeding seed max   {out['test2']['n_exceeding_iid_seed_max']} of 780",
             "", out["verdict"]]
    (HERE / "depth_extension_output.txt").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()

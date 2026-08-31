"""Global multiple-comparison correction over the pre-registered ledger.

PREREG.md fixes the global hypothesis count before data:

    N = 18 (test 1) + 780 (test 2) + 40 (test 3) + 100,000 (test 4) = 100,838

This script assembles every rule30 p-value into that single ledger and applies

  * Bonferroni at family-wise alpha = 0.05  -> per-hypothesis 4.959e-7 (headline)
  * Benjamini-Hochberg FDR at q = 0.05      -> reported alongside, since
    Bonferroni over 10^5 autocorrelation lags is very conservative

and does the same for every control sequence, so the power claims are corrected
on identical terms.

Test 1's 18 hypotheses use the test-1b EMPIRICAL p-values, not the test-1
z-scores: the z-scores were shown to be invalid for a lattice-valued statistic
(see test1b).  Empirical p-values on 500 seeds have a floor of 1/501, which
CANNOT reach the Bonferroni threshold.  That is a stated power limit of test 1,
not a pass.

Run: uv run python combine.py
"""

from __future__ import annotations

import json
import logging
import math
import pathlib

import numpy as np
from scipy import stats

HERE = pathlib.Path(__file__).resolve().parent
GLOBAL_N = 100_838
ALPHA = 0.05
Q = 0.05
SEQS = ["rule30", "rule90", "lfsr32", "bern51", "lag1000", "copy1000"]

log = logging.getLogger("combine")


def ledger_for(name: str, t1b, t2, t3, t4) -> list[dict]:
    rows: list[dict] = []

    # --- test 1: 18 hypotheses (9 prefixes x {G, J}), empirical p-values -----
    if name == "rule30":
        for n, v in t1b["audit_A"].items():
            rows.append({"family": "t1_bm_profile", "id": f"G@{n}", "p": v["empirical_p_G"],
                         "floor": t1b["empirical_p_floor"]})
            rows.append({"family": "t1_bm_profile", "id": f"J@{n}", "p": v["empirical_p_J"],
                         "floor": t1b["empirical_p_floor"]})
    else:
        # Controls only have the 20-seed z from test 1; recorded but flagged.
        d = json.loads((HERE / "test1_bm_profile_output.json").read_text())
        for z in d["sequences"][name].get("z_vs_iid", []):
            if not math.isfinite(z["z"]):
                p = 0.0
            else:
                p = float(2 * stats.norm.sf(abs(z["z"])))
            rows.append({"family": "t1_bm_profile", "id": f"{z['stat']}@{z['n']}", "p": p,
                         "note": "20-seed normal z; invalid for lattice statistics, see test1b"})

    # --- test 2: 780 hypotheses --------------------------------------------
    s2 = t2["sequences"][name]
    # top5 holds the extremes; recompute the full list from stored z is not
    # possible, so use the max and the counts, and pad the rest at p=1 which is
    # conservative for Bonferroni (it can only reduce rejections, never add).
    rows.append({"family": "t2_correlation", "id": f"max k={s2['at']['k']} d={s2['at']['delta']}",
                 "p": s2["p_raw_onesided_at_max"]})
    n_pad = 780 - 1
    rows.append({"family": "t2_correlation", "id": f"({n_pad} remaining, all p > p_max)",
                 "p": 1.0, "count": n_pad,
                 "note": "padded at p=1; only the extreme can survive any correction"})

    # --- test 3: 40 hypotheses ---------------------------------------------
    s3 = t3["sequences"][name]
    for stream in t3["streams"]:
        m = s3["block_meta"][stream]
        k, npass = m["K"], m["n_pass_at_0.01"]
        p_binom = float(stats.binomtest(npass, k, 0.99).pvalue)
        rows.append({"family": "t3_nist", "id": f"{stream}/pass_proportion", "p": p_binom})
        rows.append({"family": "t3_nist", "id": f"{stream}/uniformity_chi2", "p": m["P_T"]})
        rows.append({"family": "t3_nist", "id": f"{stream}/uniformity_ks", "p": m["ks_p"]})
        w = s3["whole"][stream]
        rows.append({"family": "t3_nist", "id": f"{stream}/whole_sequence",
                     "p": 1.0 if w is None else float(w)})

    # --- test 4: 100,000 hypotheses ----------------------------------------
    s4 = t4["results"][name]
    rows.append({"family": "t4_autocorr", "id": f"lag {s4['argmax_lag']}",
                 "p": s4["p_raw_at_max"]})
    rows.append({"family": "t4_autocorr", "id": "(99,999 remaining, all p > p_max)",
                 "p": 1.0, "count": 99_999,
                 "note": "padded at p=1; only the extreme can survive Bonferroni"})

    # Pad the test-1 family to its registered size of 18. Controls carry 15
    # (5 prefixes x 3 statistics inside the i.i.d. band) and rule30 carries 18.
    n_t1 = sum(int(r.get("count", 1)) for r in rows if r["family"] == "t1_bm_profile")
    if n_t1 < 18:
        rows.append({"family": "t1_bm_profile", "id": f"({18 - n_t1} unpopulated)",
                     "p": 1.0, "count": 18 - n_t1,
                     "note": "padded at p=1 to the registered family size"})
    return rows


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    t1b = json.loads((HERE / "test1b_bm_null_mc_output.json").read_text())
    t2 = json.loads((HERE / "test2_correlation_attack_output.json").read_text())
    t3 = json.loads((HERE / "test3_nist_output.json").read_text())
    t4 = json.loads((HERE / "test4_autocorrelation_output.json").read_text())

    thr = ALPHA / GLOBAL_N
    out: dict = {"global_N": GLOBAL_N, "alpha": ALPHA, "bonferroni_threshold": thr,
                 "fdr_q": Q, "sequences": {}}

    # exact z-array for rule30 test 4, so BH sees all 100,000 real p-values
    z30 = np.load(HERE / "test4_rule30_z.npy").astype(np.float64)
    p30_t4 = 2.0 * stats.norm.sf(np.abs(z30))

    for name in SEQS:
        rows = ledger_for(name, t1b, t2, t3, t4)
        ps: list[float] = []
        for r in rows:
            if name == "rule30" and r["family"] == "t4_autocorr":
                continue  # rule30 uses the exact 100,000-lag p-value array below
            ps.extend([r["p"]] * int(r.get("count", 1)))
        if name == "rule30":
            ps.extend(p30_t4.tolist())
        p = np.asarray(ps, dtype=float)
        assert p.size == GLOBAL_N, (name, p.size)

        bonf = [r for r in rows if r["p"] * GLOBAL_N < ALPHA and r.get("count", 1) == 1]
        order = np.sort(p)
        k = np.arange(1, p.size + 1)
        bh_ok = order <= Q * k / p.size
        n_bh = int(np.max(np.nonzero(bh_ok)[0]) + 1) if bh_ok.any() else 0
        bh_cut = float(order[n_bh - 1]) if n_bh else 0.0

        rec = {
            "min_p_raw": float(p.min()),
            "min_p_bonferroni_adjusted": float(min(1.0, p.min() * GLOBAL_N)),
            "n_bonferroni_rejections": len(bonf),
            "bonferroni_rejections": [{"family": r["family"], "id": r["id"], "p_raw": r["p"],
                                       "p_adj": min(1.0, r["p"] * GLOBAL_N)} for r in bonf][:20],
            "n_bh_rejections_q0.05": n_bh,
            "bh_cutoff_p": bh_cut,
            "verdict": ("NO BIAS FOUND" if not bonf and n_bh == 0
                        else "BIAS FOUND"),
        }
        out["sequences"][name] = rec
        log.info("%-9s min p_raw=%.3e  Bonferroni-adjusted=%.3e  #Bonf=%d  #BH(q=.05)=%d  -> %s",
                 name, rec["min_p_raw"], rec["min_p_bonferroni_adjusted"],
                 rec["n_bonferroni_rejections"], rec["n_bh_rejections_q0.05"], rec["verdict"])

    out["test1_power_limit"] = (
        f"Test 1's 18 hypotheses use empirical p-values on {t1b['n_seeds']} seeds, floor "
        f"1/{t1b['n_seeds']+1} = {t1b['empirical_p_floor']:.5f}. That floor is "
        f"{t1b['empirical_p_floor']/thr:.0f}x the Bonferroni threshold, so test 1 "
        "CANNOT produce a Bonferroni-surviving rejection at this seed count. It "
        "refutes; it does not confirm. Stated, not hidden.")
    out["headline"] = out["sequences"]["rule30"]["verdict"]
    (HERE / "combine_output.json").write_text(json.dumps(out, indent=2))

    lines = [f"Global correction over the pre-registered ledger, N = {GLOBAL_N}",
             f"Bonferroni FWER alpha = {ALPHA} -> per-hypothesis threshold {thr:.4e}",
             f"Benjamini-Hochberg FDR q = {Q}", "",
             f"{'sequence':<10}{'min p_raw':>13}{'p_adj':>13}{'#Bonf':>7}{'#BH':>7}  verdict"]
    for name in SEQS:
        r = out["sequences"][name]
        lines.append(f"{name:<10}{r['min_p_raw']:>13.3e}{r['min_p_bonferroni_adjusted']:>13.3e}"
                     f"{r['n_bonferroni_rejections']:>7d}{r['n_bh_rejections_q0.05']:>7d}  {r['verdict']}")
    lines += ["", out["test1_power_limit"], "", f"HEADLINE (rule30): {out['headline']}"]
    (HERE / "combine_output.txt").write_text("\n".join(lines) + "\n")
    log.info("HEADLINE (rule30): %s", out["headline"])


if __name__ == "__main__":
    main()

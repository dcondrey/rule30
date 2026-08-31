"""Test 2b: SUPPLEMENTARY power check for test 2, outside the registered ledger.

Why this exists.  The `copy1000` power control was registered to fire on BOTH
test 4 (autocorrelation) and test 2 (correlation attack).  It fired on test 4 at
lag 1000 with z = 20.7.  It did NOT fire on test 2 -- but not because test 2
lacks power: the pre-registered lag grid for test 2 is
{k..128} union {256, 512, 1024, 2048, 4096}, which does not contain 1000.  The
planted correlation sits in a gap of the grid.

That is a COVERAGE gap in the pre-registration, not a power failure, and the
distinction is only credible if it is demonstrated.  This script evaluates
eps(k, Delta = 1000) directly.  It is reported SEPARATELY and is NOT added to the
N = 100,838 ledger, because it was chosen after seeing test 2's output; folding
it in would be exactly the multiple-comparison abuse the pre-registration exists
to prevent.

Run: uv run python test2b_power_check.py
"""

from __future__ import annotations

import json
import logging
import pathlib

import numpy as np
from scipy import stats

from test2_correlation_attack import eps_for, windows

HERE = pathlib.Path(__file__).resolve().parent
SEQ = HERE / "seq"
DELTA = 1000
KS = (1, 2, 3, 4, 6, 8)
IID = [f"iid_{k:02d}" for k in range(20)]

log = logging.getLogger("t2b")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    names = ["rule30", "copy1000"] + IID
    seqs = {n: np.load(SEQ / f"{n}.npy") for n in names}
    eps: dict[str, dict[int, float]] = {n: {} for n in names}
    for k in KS:
        w = {n: windows(a, k) for n, a in seqs.items()}
        for n, a in seqs.items():
            eps[n][k] = eps_for(a, w[n], k, DELTA)

    out: dict = {"delta": DELTA, "ks": list(KS), "in_registered_ledger": False,
                 "reason": "Delta=1000 is not on the pre-registered grid; reported "
                           "separately so it cannot inflate the ledger", "rows": {}}
    for k in KS:
        null = np.array([eps[s][k] for s in IID])
        m, sd = float(null.mean()), float(null.std(ddof=1))
        row = {"null_mean": m, "null_sd": sd,
               "null_band": [float(null.min()), float(null.max())]}
        for n in ("rule30", "copy1000"):
            z = (eps[n][k] - m) / sd
            row[n] = {"eps": eps[n][k], "z": z, "p_raw_onesided": float(stats.norm.sf(z))}
        out["rows"][str(k)] = row
        log.info("k=%d  null %.6f+-%.6f | rule30 eps=%.6f z=%6.2f | copy1000 eps=%.6f z=%8.2f",
                 k, m, sd, eps["rule30"][k], row["rule30"]["z"],
                 eps["copy1000"][k], row["copy1000"]["z"])

    zc = max(out["rows"][str(k)]["copy1000"]["z"] for k in KS)
    zr = max(out["rows"][str(k)]["rule30"]["z"] for k in KS)
    out["verdict"] = (
        f"Test 2 HAS power at a planted correlation: copy1000 reaches z = {zc:.1f} at "
        f"Delta = 1000, far past the Bonferroni line, while rule30 reaches only "
        f"z = {zr:.2f} at the same lag. The control's absence from the registered "
        f"test-2 result is a lag-grid coverage gap, not a lack of sensitivity."
        if zc > 5.032 else
        f"INCONCLUSIVE: copy1000 only reaches z = {zc:.1f} at Delta = 1000; test 2's "
        f"power at a planted correlation is NOT established.")
    log.info("%s", out["verdict"])

    (HERE / "test2b_power_check_output.json").write_text(json.dumps(out, indent=2))
    lines = [f"Test 2b: supplementary power check at Delta = {DELTA} (NOT in the N=100,838 ledger)",
             "", f"{'k':>3}{'null mean':>12}{'null sd':>11}{'rule30 eps':>13}{'z':>9}"
                 f"{'copy1000 eps':>15}{'z':>11}"]
    for k in KS:
        r = out["rows"][str(k)]
        lines.append(f"{k:>3}{r['null_mean']:>12.6f}{r['null_sd']:>11.6f}"
                     f"{r['rule30']['eps']:>13.6f}{r['rule30']['z']:>9.2f}"
                     f"{r['copy1000']['eps']:>15.6f}{r['copy1000']['z']:>11.2f}")
    lines += ["", out["verdict"]]
    (HERE / "test2b_power_check_output.txt").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()

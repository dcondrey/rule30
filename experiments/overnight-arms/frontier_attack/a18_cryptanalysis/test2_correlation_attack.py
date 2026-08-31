"""Test 2 (PREREG.md): the correlation-attack statistic, evaluated ALONG THE ORBIT.

For window length k and lag Delta, with w = (c_t,...,c_{t+k-1}) and y = c_{t+Delta},
the maximum over ALL Boolean functions g:{0,1}^k -> {0,1} of Pr[g(w)=y] - 1/2 is
attained by the maximum-likelihood g and equals

    eps(k,Delta) = (1/2) * sum_w | Pr[w, y=1] - Pr[w, y=0] |

computed in one pass over the joint histogram.  This is the standard quantity a
correlation attack on a nonlinear combiner maximizes.

DISTINCT FROM ROW 43.  Row 43 analysed the ANF/Walsh spectrum of the iterated
centre-bit FUNCTION f_t over ALL 2^(2t+1) inputs (obstruction G territory).  This
measures correlation along the SINGLE ACTUAL ORBIT of the lone seed, which is a
measure-zero subset of that input space and is the object P1/P2 are about.

FRAMING-ARTIFACT GUARD (pre-registered).  c_{t+Delta} is determined by row-t cells
in [-Delta, Delta], and the output window c_t..c_{t+k-1} OVERLAPS the target when
Delta < k, which would return eps = 1/2 by construction.  Only Delta >= k is
admissible and the script asserts it.

Run: uv run python test2_correlation_attack.py
"""

from __future__ import annotations

import json
import logging
import pathlib

import numpy as np
from scipy import stats

HERE = pathlib.Path(__file__).resolve().parent
SEQ = HERE / "seq"
KS = (1, 2, 3, 4, 6, 8)
FAR = (256, 512, 1024, 2048, 4096)
GLOBAL_N = 100_838
CONTROLS = ["rule30", "rule90", "lfsr32", "bern51", "lag1000", "copy1000"]
IID = [f"iid_{k:02d}" for k in range(20)]

log = logging.getLogger("t2")


def lags_for(k: int) -> list[int]:
    return [d for d in range(k, 129)] + list(FAR)


def windows(bits: np.ndarray, k: int) -> np.ndarray:
    """w_t = sum_{j<k} c_{t+j} 2^j, for t = 0 .. T-k."""
    T = bits.size
    w = np.zeros(T - k + 1, dtype=np.int64)
    for j in range(k):
        w += bits[j : T - k + 1 + j].astype(np.int64) << j
    return w


def eps_for(bits: np.ndarray, w: np.ndarray, k: int, delta: int) -> float:
    assert delta >= k, "Delta < k overlaps the target: framing artifact, refused"
    T = bits.size
    n = T - delta  # t runs 0..T-delta-1; window end t+k-1 <= t+delta-1 < T
    ww = w[:n]
    y = bits[delta : delta + n].astype(np.int64)
    h = np.bincount(ww * 2 + y, minlength=(1 << k) * 2).astype(np.float64)
    h /= n
    p1 = h[1::2]
    p0 = h[0::2]
    return float(0.5 * np.abs(p1 - p0).sum())


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    seqs = {n: np.load(SEQ / f"{n}.npy") for n in CONTROLS + IID}
    eps: dict[str, dict[str, float]] = {n: {} for n in seqs}
    n_hyp = 0
    for k in KS:
        wcache = {n: windows(a, k) for n, a in seqs.items()}
        for d in lags_for(k):
            n_hyp += 1
            for n, a in seqs.items():
                eps[n][f"k{k}_d{d}"] = eps_for(a, wcache[n], k, d)
        log.info("k=%d done (%d lags)", k, len(lags_for(k)))
    log.info("ledger size for test 2: %d (PREREG registered 780)", n_hyp)

    # Null: pooled per k over the 20 i.i.d. seeds and all admissible lags.
    # eps depends on k and the sample size, not on Delta, so pooling gives a
    # ~2700-sample null per k instead of 20.  Correlation across Delta within a
    # seed is weak (disjoint lags); the empirical seed max is also reported as
    # the operative threshold, per the row 8 convention.
    null: dict[int, dict] = {}
    for k in KS:
        vals = np.array([eps[s][f"k{k}_d{d}"] for s in IID for d in lags_for(k)])
        per_seed_max = np.array([max(eps[s][f"k{k}_d{d}"] for d in lags_for(k)) for s in IID])
        null[k] = {
            "n_samples": int(vals.size), "mean": float(vals.mean()),
            "sd": float(vals.std(ddof=1)), "pooled_max": float(vals.max()),
            "seed_max_band": [float(per_seed_max.min()), float(per_seed_max.max())],
        }

    results: dict = {"ledger_size": n_hyp, "global_N": GLOBAL_N, "null": null, "sequences": {}}
    for name in CONTROLS:
        rows = []
        for k in KS:
            m, s = null[k]["mean"], null[k]["sd"]
            for d in lags_for(k):
                e = eps[name][f"k{k}_d{d}"]
                z = (e - m) / s
                rows.append({"k": k, "delta": d, "eps": e, "z": z,
                             "p_raw_onesided": float(stats.norm.sf(z))})
        rows.sort(key=lambda r: -r["z"])
        top = rows[0]
        n_bonf = sum(1 for r in rows if r["p_raw_onesided"] * GLOBAL_N < 0.05)
        n_over_seedmax = sum(1 for r in rows if r["eps"] > null[r["k"]]["seed_max_band"][1])
        results["sequences"][name] = {
            "max_z": top["z"], "at": {"k": top["k"], "delta": top["delta"], "eps": top["eps"]},
            "p_raw_onesided_at_max": top["p_raw_onesided"],
            "p_bonferroni_at_max": float(min(1.0, top["p_raw_onesided"] * GLOBAL_N)),
            "n_surviving_bonferroni": n_bonf,
            "n_exceeding_iid_seed_max": n_over_seedmax,
            # Full 780-row ledger, so a reader can redo any correction. PREREG
            # promises raw p-values for every hypothesis; this is that promise.
            "all_rows": rows,
            "top5": rows[:5],
            "verdict": "REJECT (bias detected)" if n_bonf else "no (k,Delta) survives Bonferroni",
        }
        log.info("%-9s max z=%9.3f at k=%d Delta=%d eps=%.6f  #bonf=%d  #>seedmax=%d  %s",
                 name, top["z"], top["k"], top["delta"], top["eps"], n_bonf,
                 n_over_seedmax, results["sequences"][name]["verdict"])

    (HERE / "test2_correlation_attack_output.json").write_text(json.dumps(results, indent=2))
    lines = ["Test 2: correlation-attack statistic eps(k,Delta) along the lone-seed orbit",
             f"k in {KS}; Delta in [k,128] U {FAR}; ledger {n_hyp}; global N {GLOBAL_N}",
             "Delta >= k enforced (overlap would give eps = 1/2 by construction).", "",
             f"{'sequence':<9} {'max z':>10} {'k':>3} {'Delta':>6} {'eps':>10} {'#bonf':>6} {'#>seedmax':>10}"]
    for name in CONTROLS:
        r = results["sequences"][name]
        lines.append(f"{name:<9} {r['max_z']:>10.3f} {r['at']['k']:>3d} {r['at']['delta']:>6d} "
                     f"{r['at']['eps']:>10.6f} {r['n_surviving_bonferroni']:>6d} "
                     f"{r['n_exceeding_iid_seed_max']:>10d}")
    lines += ["", "i.i.d. null, pooled per k:"]
    for k in KS:
        d = null[k]
        lines.append(f"  k={k}: n={d['n_samples']} mean={d['mean']:.6f} sd={d['sd']:.6f} "
                     f"seed-max band [{d['seed_max_band'][0]:.6f}, {d['seed_max_band'][1]:.6f}]")
    lines += ["", f"rule30 verdict: {results['sequences']['rule30']['verdict']}"]
    (HERE / "test2_correlation_attack_output.txt").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()

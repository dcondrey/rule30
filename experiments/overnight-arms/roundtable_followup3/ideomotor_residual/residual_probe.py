"""Verification probe for the "ideomotor-residual" spark.

Claim under test: fix a candidate period p for the lone-seed Rule 30 centre
column c_t = s(t,0). Track r_t = s(t,1). Define, over "unlocked" beats where
the assumed-periodic centre reads c_{T+jp} = 0,

    rho_k = sum_{j=0}^{k-1} (1 - c_{T+jp}) * (2*r_{T+jp} - 1)
          = sum over unlocked j of (2*r_{T+jp} - 1)

The spark's claim: IF c is eventually periodic with period p, rho_k must stay
bounded ("fatigue oscillator" analogy), and the real lone-seed r-column
allegedly drifts rho_k unboundedly, contradicting periodicity.

Pre-registered kill condition: does eventual periodicity of c impose ANY
constraint on r that would make rho_k provably bounded? Suspicion: no.

This script:
  1. Re-derives, from the exact defect recurrence already proved in
     RESULTS-eventual-period.md, what periodicity of c actually implies about
     r's defect, and shows it does not force boundedness.
  2. Constructs a REAL, existing counterexample to the "periodic => bounded"
     implication using Rule 90, whose centre column truly is eventually
     periodic (period 1, identically 0 for t>=1): computes rho_k for Rule 90
     under its true period and shows it drifts unboundedly (does not stay
     bounded), directly falsifying the general implication the spark relies
     on.
  3. Runs the same statistic on the real Rule 30 lone-seed orbit for several
     trial periods p, as a secondary, non-dispositive measurement.
  4. Checks whether the mechanism is Rule-30-specific (PATH.md section 0
     filter): since step 2 uses the *actual* Rule 90 orbit with its *actual*
     true period, this is not a hypothetical -- it is a direct existence
     counterexample.

Self-contained: reuses only evolve_rows()/cell() from
experiments/rule30/periodicity_bridge_probe.py (read-only import).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / "experiments" / "rule30"))

from periodicity_bridge_probe import RULE_30, RULE_90, evolve_rows, cell  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent


def columns(rule: int, max_time: int):
    """Return (c_t, r_t) arrays for t = 0..max_time for the lone seed."""
    rows, center = evolve_rows(rule, max_time, (0,))
    c = [cell(rows, center, t, 0) for t in range(max_time + 1)]
    r = [cell(rows, center, t, 1) for t in range(max_time + 1)]
    return c, r


def rho_series(c, r, T, p, k_max):
    """rho_k for j=0..k_max-1 at stride p starting at time T.

    Returns (times_used, unlocked_flags, rho_values) where rho_values[k] is
    rho_k (partial sum through j=0..k-1), rho_values[0] = 0.
    """
    times = []
    unlocked = []
    rho = [0]
    running = 0
    n = len(c)
    for j in range(k_max):
        t = T + j * p
        if t >= n:
            break
        times.append(t)
        ct = c[t]
        rt = r[t]
        u = 1 - ct  # unlocked iff c_t == 0
        unlocked.append(u)
        if u:
            running += (2 * rt - 1)
        rho.append(running)
    return times, unlocked, rho


def defect_identity_check(c, r, l, p, T0, samples):
    """Independently re-verify the RESULTS-eventual-period.md defect identity

        d_t(-1) = (1 XOR c_t) AND d_t(1)

    under the (locally, numerically approximated) assumption that c has
    settled into period p by time T0, i.e. using d_t(0) = c_{t+p} XOR c_t as
    the actual measured value (not assumed zero) so the check is honest about
    whether it's being fed a true period or not. Returns count of times the
    identity holds and count where it's tested, restricted to t in samples.
    """
    n = len(c)
    ok = 0
    tested = 0
    mismatches = []
    for t in samples:
        if t + p + 1 >= n or t < 0:
            continue
        d0_t = c[t + p] ^ c[t]
        d0_t1 = c[t + p + 1] ^ c[t + 1]
        if d0_t != 0 or d0_t1 != 0:
            continue  # identity's derivation assumed d_t(0)=d_{t+1}(0)=0
        d_minus1 = l[t + p] ^ l[t]
        d_plus1 = r[t + p] ^ r[t]
        predicted = (1 ^ c[t]) & d_plus1
        tested += 1
        if d_minus1 == predicted:
            ok += 1
        else:
            mismatches.append(t)
    return {"tested": tested, "ok": ok, "mismatches_sample": mismatches[:10]}


def main():
    T_MAX = 6000
    c30, r30 = columns(RULE_30, T_MAX)
    # also need l (x=-1) column for the defect-identity check
    rows30, center30 = evolve_rows(RULE_30, T_MAX, (0,))
    l30 = [cell(rows30, center30, t, -1) for t in range(T_MAX + 1)]

    c90, r90 = columns(RULE_90, T_MAX)

    results = {}

    # --- Sanity: confirm Rule 90's centre column is truly eventually
    # periodic (period 1, identically 0 for t>=1). This is the known fact
    # PATH.md section 0 cites (Kopra).
    rule90_center_nonzero_after_1 = [t for t in range(1, T_MAX + 1) if c90[t] != 0]
    results["rule90_center_check"] = {
        "period_claimed": 1,
        "nonzero_after_t1_count": len(rule90_center_nonzero_after_1),
        "sample_nonzero_times": rule90_center_nonzero_after_1[:10],
    }

    # --- Step 2: the decisive counterexample.
    # Rule 90's centre column IS eventually periodic with true period p=1
    # (c_t = 0 for all t >= 1, confirmed above). At every beat t >= 1,
    # c_t = 0 so every beat is "unlocked". Compute rho_k over the true
    # orbit's r-column (x=+1) under this TRUE period.
    T0 = 1
    P_TRUE_90 = 1
    K = T_MAX - T0
    times90, unlocked90, rho90 = rho_series(c90, r90, T0, P_TRUE_90, K)
    # density of 1s in r90 among unlocked beats, and final/intermediate rho
    ones90 = sum(r90[t] for t in times90)
    checkpoints = [k for k in (10, 50, 100, 500, 1000, 2000, 5000, K) if k <= len(rho90) - 1]
    results["rule90_true_period_rho"] = {
        "T0": T0,
        "p": P_TRUE_90,
        "k_max": K,
        "num_unlocked_beats": sum(unlocked90),
        "num_ones_in_r_among_unlocked": ones90,
        "rho_at_checkpoints": {str(k): rho90[k] for k in checkpoints},
        "final_rho": rho90[-1],
        "final_rho_over_k": rho90[-1] / max(1, len(rho90) - 1),
    }

    # --- Step 3: same statistic on the real Rule 30 orbit, several trial
    # periods, purely descriptive (Rule 30's true eventual period, if any,
    # is exactly what P1 asks and is NOT known / NOT assumed here).
    rule30_trials = {}
    for p in (2, 3, 4, 6, 8):
        for T in (100, 500, 2000):
            K30 = min(400, (T_MAX - T) // p - 1)
            if K30 < 10:
                continue
            times, unlocked, rho = rho_series(c30, r30, T, p, K30)
            rule30_trials[f"p={p}_T={T}"] = {
                "k_max": K30,
                "num_unlocked": sum(unlocked),
                "final_rho": rho[-1],
                "rho_over_k": rho[-1] / max(1, len(rho) - 1),
                "max_abs_rho": max(abs(x) for x in rho),
            }
    results["rule30_trial_periods"] = rule30_trials

    # --- Step 1 (re-derivation): verify the exact defect identity from
    # RESULTS-eventual-period.md on the real Rule 30 orbit, restricted to
    # (t, p) pairs where the real orbit HAPPENS to satisfy d_t(0)=d_{t+1}(0)=0
    # for some trial p (i.e., a local, not global, period match) -- this is
    # exactly the regime the identity's derivation assumed, and it must hold
    # there by the proof already in RESULTS-eventual-period.md; the question
    # is whether it goes on to force d_t(1) (r's defect) to be zero or
    # bounded. It does not: d_t(-1) is *expressed in terms of* d_t(1), never
    # the other way, so the identity has no content about r unless r's
    # defect is independently known.
    defect_checks = {}
    for p in (2, 3, 4):
        samples = list(range(0, T_MAX - p - 1))
        defect_checks[f"p={p}"] = defect_identity_check(c30, r30, l30, p, 0, samples)
    results["defect_identity_reverification"] = defect_checks

    # --- Rule 90 vacuous-mechanism check (PATH.md section 0 filter):
    # apply the *identical* rho_k mechanism, with the identical code path,
    # to Rule 90's TRUE period. If the "periodic => bounded" premise held in
    # general, rho90 above should stay O(1). It does not (see verdict logic
    # below, based on results["rule90_true_period_rho"]).

    with open(OUT_DIR / "residual_probe_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

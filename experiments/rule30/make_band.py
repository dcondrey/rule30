"""Emit a committed hidden-test file and challenge file for one n-band.

Cases are 64 pseudo-random n drawn from [lo, hi) with a fixed seed so the band
is reproducible; the chance floor for `all_cases_correct` on a one-bit output
is 2^-64.
"""
import json, random, sys
from center_column import center_column

lo, hi, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
count = int(sys.argv[4]) if len(sys.argv) > 4 else 64
col = center_column(hi)
rng = random.Random(seed)
ns = sorted(rng.sample(range(lo, hi), count))
cases = [{"input": n, "expected": int(col[n])} for n in ns]
band = f"{lo}-{hi}"
json.dump(
    {"schema": "crosstalk.wasm-i64-tests.v1", "export_name": "solve", "cases": cases},
    open(f"hidden-{band}.json", "w"),
    indent=2,
)
spec = {
    "id": f"rule30-centre-column-{band}",
    "version": "1",
    "description": f"Metered effort to return bit n of OEIS A051023 for n in [{lo},{hi})",
    "metrics": [
        {"name": "accuracy", "unit": "ratio", "direction": "Maximize", "reproduction_tolerance": 0.0},
        {"name": "fuel_consumed", "unit": "fuel", "direction": "Minimize", "reproduction_tolerance": 0.0},
    ],
    "hard_constraints": ["all_cases_correct", "resource_limit_not_hit"],
    "timeout_secs": 1800,
    "deterministic": True,
    "independent_reproduction_required": True,
    "reproduction_evaluator_id": "wasm-i64-reproduction",
    "distinct_attestation_keys_required": False,
}
print(json.dumps({
    "schema": "crosstalk.algorithm-challenge-file.v1",
    "id": f"rule30-effort-{band}-v1",
    "title": f"Rule 30 centre column: metered effort, n in [{lo},{hi})",
    "evaluator_id": "wasm-i64-primary",
    "evaluation": spec,
    "primary_metric": "fuel_consumed",
    "minimum_improvement": 1.0,
    "hidden_test_commitment_sha256": "PLACEHOLDER",
    "baseline_id": "naive",
    "max_candidates": 8,
}, indent=2), file=open(f"challenge-{band}.json", "w"))
print(band, len(cases), "ones:", sum(c["expected"] for c in cases))

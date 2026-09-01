"""
Measure the direct-simulation baseline's empirical scaling exponent for
each evaluator profile, and cache it to baseline_exponent.json so
evaluator.py doesn't have to re-measure it on every single candidate
evaluation (the baseline itself doesn't change).

Uses the SAME timing methodology as evaluator._measure_scaling (median of
repeated calls per n, log-log least squares fit) so the baseline number is
directly comparable to what candidates are scored against. Run this once
after editing the profiles in evaluator.py's PROFILES dict, or if the
measuring machine changes.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import evaluator as ev  # noqa: E402
from initial_program import center_cell as baseline_center_cell  # noqa: E402


def measure_profile(profile_name: str) -> dict:
    ev.PROFILE = profile_name
    ev.CFG = ev.PROFILES[profile_name]
    scaling = ev._measure_scaling(baseline_center_cell)
    return {
        "tail_exponent": scaling["tail_exponent"],
        "exponent": scaling["exponent"],
        "r2": scaling["r2"],
        "tail_consistency": scaling.get("tail_consistency"),
        "usable_ns": scaling["usable_ns"],
        "dropped": scaling["dropped"],
        "scaling_ns_config": ev.CFG["scaling_ns"],
        "repeats": ev.CFG["repeats"],
    }


def main() -> None:
    # "full" profile times the pure-Python O(n^2) baseline up to n=32000
    # (~1e9 inner-loop iterations for the largest point, times `repeats`) --
    # that's minutes, not seconds. Don't measure it by default; this script
    # is meant to be cheap. Pass --full to measure it explicitly when doing
    # a real (non-smoke) run.
    profiles = list(ev.PROFILES) if "--full" in sys.argv else ["smoke"]
    out = {}
    if (HERE / "baseline_exponent.json").exists():
        out = json.loads((HERE / "baseline_exponent.json").read_text())
    for profile in profiles:
        print(f"measuring baseline exponent for profile={profile} ...")
        result = measure_profile(profile)
        out[profile] = result
        print(f"  tail_exponent={result['tail_exponent']} exponent={result['exponent']} "
              f"r2={result['r2']} usable_ns={result['usable_ns']} dropped={result['dropped']}")
    (HERE / "baseline_exponent.json").write_text(json.dumps(out, indent=2))
    print(f"wrote {HERE / 'baseline_exponent.json'}")


if __name__ == "__main__":
    main()

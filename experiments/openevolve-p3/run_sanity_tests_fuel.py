"""Re-run the four pre-registered sanity candidates under the DETERMINISTIC
FUEL instrument (evaluator_fuel.py) instead of the wall clock.

Required outcomes, unchanged from PREREGISTRATION.md:
  (a) correct naive baseline        -> correct, flat ~0.2 credit, no exponent win
  (b) deliberately wrong            -> exactly 0.0
  (c) bit-packed constant-factor    -> correct, NOT in the exponent-improvement band
  (d) lookup-table cheat            -> exactly 0.0

(c) is the whole point: if it shows an exponent improvement under fuel
counting, the cost model is undercharging big-integer operations and the
instrument is broken. The fix is the cost model, never the threshold.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import evaluator_fuel as ef  # noqa: E402

CANDIDATES = [
    ("a_correct (expect: correct, flat ~0.2 credit)", "sanity_candidates/candidate_a_correct.py"),
    ("b_wrong (expect: 0.0)", "sanity_candidates/candidate_b_wrong.py"),
    ("c_bitpacked (expect: correct, flat credit, NOT exponent-band)", "sanity_candidates/candidate_c_bitpacked.py"),
    ("d_lookup_table (expect: 0.0)", "sanity_candidates/candidate_d_lookup_table.py"),
]

if __name__ == "__main__":
    print(f"profile={ef.PROFILE} ns={ef.CFG['scaling_ns']} "
          f"baseline_tail={ef._load_baseline_tail():.6f}")
    for label, path in CANDIDATES:
        print(f"\n=== {label} ===")
        r = ef.evaluate(str(HERE / path))
        print("metrics:", json.dumps(r.metrics, indent=2, default=str))
        print("artifacts:", json.dumps(r.artifacts, indent=2, default=str))

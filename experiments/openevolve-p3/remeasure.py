"""Re-measure a candidate's tail exponent N independent times.

Required by PREREGISTRATION.md's "Held-out verification protocol": a single
timing sample is not trustworthy (see measurement-methodology bug #2), so any
claimed exponent improvement must reproduce across >= 3 independent runs.

Also used to measure the BASELINE >= 3 times under the same conditions, which
is what turns "matches baseline within noise" into an actual measured noise
band rather than an assertion.

Usage:
    RULE30_P3_PROFILE=smoke python remeasure.py <program.py> [<program.py> ...] [--runs 3]

Does not modify the evaluator or the scoring; it just calls evaluate().
"""
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from evaluator import evaluate  # noqa: E402


def main() -> None:
    args = [a for a in sys.argv[1:]]
    runs = 3
    if "--runs" in args:
        i = args.index("--runs")
        runs = int(args[i + 1])
        del args[i : i + 2]
    if not args:
        print(__doc__)
        sys.exit(1)

    out = {}
    for path in args:
        rows = []
        for k in range(runs):
            res = evaluate(path)
            m = res.metrics
            arts = res.artifacts or {}
            rows.append(
                {
                    "run": k,
                    # Load-critical: which n the tail was actually computed
                    # over. Two candidates with different usable_ns are NOT
                    # comparable, and nothing in the metrics reveals that.
                    "usable_ns": arts.get("scaling_usable_ns"),
                    "dropped": arts.get("scaling_dropped"),
                    "combined_score": m.get("combined_score"),
                    "tail_exponent": m.get("measured_tail_exponent"),
                    "global_exponent": m.get("measured_global_exponent"),
                    "r2": m.get("fit_r2"),
                    "tail_consistency": m.get("tail_consistency"),
                    "error": m.get("error"),
                }
            )
            print(f"{path} run {k}: {rows[-1]}", flush=True)
        tails = [r["tail_exponent"] for r in rows if r["tail_exponent"] not in (None, -1.0)]
        summary = {"runs": rows}
        if len(tails) >= 2:
            summary["tail_mean"] = statistics.mean(tails)
            summary["tail_stdev"] = statistics.stdev(tails)
            summary["tail_min"] = min(tails)
            summary["tail_max"] = max(tails)
        out[path] = summary
        print(f"--- {path}: {json.dumps({k: v for k, v in summary.items() if k != 'runs'})}", flush=True)

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()

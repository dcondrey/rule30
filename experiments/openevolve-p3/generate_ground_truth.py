"""
Generate ground-truth c(n) values for the Rule 30 P3 harness.

Produces ground_truth.json with two DISJOINT sets of (n -> c(n)) pairs:

  - "evolve":  n values the evaluator is allowed to score candidates against
               DURING evolution. OpenEvolve (and the LLM proposing edits)
               can see these scores and adapt to them.
  - "holdout": n values used ONLY for the final reported fitness, never
               exposed as feedback during the evolutionary loop. A candidate
               cannot win by curve-fitting or hardcoding against this set
               because it never sees per-n feedback on it.

Both sets are log-spaced over the same range (10 <= n <= 20000) and
interleaved from a single sorted anchor list, so neither set is
systematically easier/harder -- this avoids confounding "generalizes past
the training range" with "the evolve set happened to be the easy half".

All values are computed by simple_reference.py (n <= 3000, where its O(n^2)
pure-Python loop is still fast) or bigint_reference.py (n > 3000), and
bigint_reference.py is cross-validated exactly against simple_reference.py
in reference/test_reference.py before being trusted here.

A third, un-persisted "trap" set (see evaluator.py TRAP_NS) is computed
fresh at evaluation time and never written to any file evolution can read,
specifically to catch a candidate that embeds a lookup table sized to cover
only the n values it has seen on disk.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).parent / "reference"))
from simple_reference import center_column as simple_center_column  # noqa: E402
from bigint_reference import center_column as bigint_center_column  # noqa: E402

OUT_PATH = Path(__file__).parent / "ground_truth.json"

# N_MAX is capped at 3000 deliberately: this range is used for the
# CORRECTNESS gate (evaluator.py), which must stay cheap even for a
# straightforward-but-unoptimized O(n^2) candidate (the kind OpenEvolve will
# propose constantly). At n=3000, direct simulation costs a few seconds in
# pure Python; at n=16000+ a single call can cost over a minute (measured).
# Large-n correctness (up to the top of the scaling-exponent range) is
# instead checked inline during scaling measurement itself -- see
# evaluator._measure_scaling, which compares each timed call's output
# against bigint_reference truth computed on the fly.
N_MIN = 10
N_MAX = 3_000
NUM_ANCHORS = 30
SIMPLE_CUTOFF = 3000  # above this, use bigint_reference (already validated)


def anchor_ns() -> list[int]:
    """Log-spaced integer n values from N_MIN to N_MAX, deduplicated."""
    ratios = [
        N_MIN * (N_MAX / N_MIN) ** (i / (NUM_ANCHORS - 1)) for i in range(NUM_ANCHORS)
    ]
    ns = sorted({int(round(r)) for r in ratios})
    return ns


def truth_for(n: int) -> int:
    if n <= SIMPLE_CUTOFF:
        return simple_center_column(n)[-1]
    return bigint_center_column(n)[-1]


def main() -> None:
    anchors = anchor_ns()
    evolve_ns = anchors[0::2]
    holdout_ns = anchors[1::2]
    assert not (set(evolve_ns) & set(holdout_ns)), "evolve/holdout overlap!"

    evolve = {str(n): truth_for(n) for n in evolve_ns}
    holdout = {str(n): truth_for(n) for n in holdout_ns}

    data = {
        "n_min": N_MIN,
        "n_max": N_MAX,
        "simple_cutoff": SIMPLE_CUTOFF,
        "evolve": evolve,
        "holdout": holdout,
    }
    OUT_PATH.write_text(json.dumps(data, indent=2, sort_keys=True))
    print(f"wrote {OUT_PATH} : {len(evolve)} evolve ns, {len(holdout)} holdout ns")
    print("evolve  ns:", evolve_ns)
    print("holdout ns:", holdout_ns)


if __name__ == "__main__":
    main()

"""
Fuel-metered evaluator for the Rule 30 P3 task.

This is a PARALLEL INSTRUMENT, not an amendment. `evaluator.py`,
`PREREGISTRATION.md` and `baseline_exponent.json` are untouched: the
pre-registered wall-clock evaluator still exists exactly as registered, and
this file is a second, deterministic way of estimating the same quantity
(the tail exponent of cost vs n). It reuses the pre-registered scoring
function, correctness gates, trap set and literal scan BY IMPORT, so the
thresholds and the kill condition cannot drift.

The only thing replaced is the instrument. Instead of

    t0 = perf_counter(); center_cell(n); t1 = perf_counter()

it measures

    fuel = exact count of the work center_cell(n) performs

under the word-RAM cost model in `fuel.py`. See that module for the cost
model in full; the load-bearing part is that variable-width operations
(big-integer arithmetic above all) are charged proportionally to their
operand width, so a bit-packed constant-factor implementation cannot read
as an exponent improvement.

Three structural differences from `evaluator.py` follow from determinism:

  * `repeats` is 1. Repeating an exact measurement adds nothing.
  * The per-point wall-clock timeout is replaced by a FUEL BUDGET. A point
    is dropped for exceeding a fixed fuel budget, which is a property of
    the candidate, not of the machine -- so the same candidate always gets
    the same measurement window, and the failure mode that truncated the
    naive control's window to a transient segment cannot happen.
  * Correctness gates run on the UNINSTRUMENTED module (~50x cheaper);
    only the scaling measurement is instrumented. `check_instrumentation`
    below is the differential test that instrumentation preserves
    semantics.
"""
from __future__ import annotations

import json
import math
import os
import sys
import traceback
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "reference"))

import fuel as fuelmod  # noqa: E402
from bigint_reference import center_column as _bigint_center_column  # noqa: E402

# Reuse the PRE-REGISTERED gates and scoring verbatim. Importing rather than
# copying is deliberate: it makes threshold drift impossible.
from evaluator import (  # noqa: E402
    CORRECTNESS_TIMEOUT,
    TRAP_NS,
    _check_correctness,
    _combined_score,
    _load_ground_truth,
    _scan_literals,
)
from openevolve.evaluation_result import EvaluationResult  # noqa: E402

BASELINE_FUEL_PATH = HERE / "baseline_fuel.json"

# Scaling ladders. These are much smaller n than the wall-clock profiles
# need, and that is a consequence of the instrument, not a compromise:
# the wall-clock range had to reach n=16000 to escape a Python-interpreter
# overhead transient that made the bit-packed control read ~1.1. Fuel does
# not charge interpreter overhead at all, so that transient does not exist
# here -- see the window sweep in the write-up, where every adjacent window
# from 250->500 upward already reads ~2.0 for BOTH controls.
PROFILES = {
    "fuel_smoke": {"scaling_ns": [250, 500, 1000, 2000], "fuel_budget": 2 * 10**9},
    "fuel_wide": {"scaling_ns": [250, 500, 1000, 2000, 4000], "fuel_budget": 2 * 10**9},
    "fuel_tiny": {"scaling_ns": [60, 125, 250, 500], "fuel_budget": 2 * 10**9},
}
PROFILE = os.environ.get("RULE30_P3_FUEL_PROFILE", "fuel_wide")
CFG = PROFILES[PROFILE]


def _load_baseline_tail() -> float:
    if BASELINE_FUEL_PATH.exists():
        data = json.loads(BASELINE_FUEL_PATH.read_text())
        if PROFILE in data and data[PROFILE].get("tail_exponent") is not None:
            return float(data[PROFILE]["tail_exponent"])
    return 2.0  # theoretical exponent for direct simulation


def measure_scaling_fuel(program_path, check_correctness: bool = True) -> dict:
    """Count fuel for center_cell(n) across the profile's n ladder.

    A FRESH instrumented module per n: a candidate that memoised across
    calls would otherwise make later, larger n artificially cheap and
    manufacture a sub-quadratic slope.
    """
    ns = CFG["scaling_ns"]
    budget = CFG["fuel_budget"]

    log_ns, log_fs, usable_ns, fuels, dropped = [], [], [], [], []
    setup_fuels = []
    for n in ns:
        try:
            f, got, setup = fuelmod.measure_fuel(program_path, n, limit=budget)
            setup_fuels.append(int(setup))
        except fuelmod.FuelExhausted as e:
            dropped.append((n, f"fuel budget exceeded: {e}"))
            continue
        except fuelmod.FuelModelError as e:
            return {
                "usable_ns": usable_ns, "fuels": fuels, "dropped": dropped,
                "exponent": None, "tail_exponent": None, "r2": None,
                "const_log": None, "correct": False,
                "correctness_detail": f"unmodelled construct: {e}",
                "model_error": str(e),
            }
        except Exception as e:
            dropped.append((n, f"call failed: {type(e).__name__}: {e}"))
            continue

        if check_correctness:
            truth = _bigint_center_column(n)[-1]
            if got not in (0, 1) or int(got) != int(truth):
                return {
                    "usable_ns": usable_ns, "fuels": fuels, "dropped": dropped,
                    "exponent": None, "tail_exponent": None, "r2": None,
                    "const_log": None, "correct": False,
                    "correctness_detail": f"n={n}: got {got!r}, expected {truth}",
                }
        if f <= 0:
            dropped.append((n, "non-positive fuel"))
            continue
        usable_ns.append(n)
        fuels.append(int(f))
        log_ns.append(math.log(n))
        log_fs.append(math.log(f))

    result = {
        "usable_ns": usable_ns, "fuels": fuels, "dropped": dropped,
        "setup_fuels": setup_fuels,
        "exponent": None, "tail_exponent": None, "r2": None,
        "const_log": None, "correct": True, "correctness_detail": "ok",
    }
    if len(usable_ns) < 2:
        return result

    result["tail_exponent"] = (log_fs[-1] - log_fs[-2]) / (log_ns[-1] - log_ns[-2])
    # Every adjacent window, so the write-up can show convergence rather
    # than assert it.
    result["window_exponents"] = [
        {
            "from": usable_ns[i - 1],
            "to": usable_ns[i],
            "slope": (log_fs[i] - log_fs[i - 1]) / (log_ns[i] - log_ns[i - 1]),
        }
        for i in range(1, len(usable_ns))
    ]

    if len(usable_ns) >= 3:
        a_ns, a_fs = np.array(log_ns), np.array(log_fs)
        slope, intercept = np.polyfit(a_ns, a_fs, 1)
        pred = slope * a_ns + intercept
        ss_res = float(np.sum((a_fs - pred) ** 2))
        ss_tot = float(np.sum((a_fs - np.mean(a_fs)) ** 2))
        result["exponent"] = float(slope)
        result["r2"] = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
        result["const_log"] = float(intercept)
        prior = (log_fs[-2] - log_fs[-3]) / (log_ns[-2] - log_ns[-3])
        result["prior_segment_exponent"] = float(prior)
        result["tail_consistency"] = float(abs(result["tail_exponent"] - prior))
    return result


def check_instrumentation(program_path, ns=(0, 1, 2, 3, 7, 20, 61, 137, 250)) -> tuple[bool, str]:
    """Differential test: the instrumented build must return exactly what
    the uninstrumented one returns. A transformer bug that changes
    semantics is otherwise invisible."""
    plain = fuelmod.load_plain(program_path)
    for n in ns:
        want = plain.center_cell(n)
        _, got, _ = fuelmod.measure_fuel(program_path, n)
        if got != want:
            return False, f"n={n}: instrumented {got!r} != uninstrumented {want!r}"
    return True, "ok"


def evaluate(program_path: str) -> EvaluationResult:
    try:
        source = Path(program_path).read_text()
    except Exception as e:
        return EvaluationResult(
            metrics={"combined_score": 0.0, "error": f"cannot read program: {e}"},
            artifacts={"error_type": "ReadError"},
        )

    hard_fail, literal_findings = _scan_literals(source)
    if hard_fail:
        return EvaluationResult(
            metrics={"combined_score": 0.0, "error": "embedded-table-sized literal detected"},
            artifacts={"error_type": "SuspiciousLiteral", "findings": literal_findings},
        )

    # --- correctness gates, on the UNINSTRUMENTED module ------------------
    try:
        module = fuelmod.load_plain(program_path)
    except Exception as e:
        return EvaluationResult(
            metrics={"combined_score": 0.0, "error": f"import failed: {e}"},
            artifacts={"error_type": type(e).__name__, "traceback": traceback.format_exc()},
        )
    if not hasattr(module, "center_cell"):
        return EvaluationResult(
            metrics={"combined_score": 0.0, "error": "missing center_cell(n) function"},
            artifacts={"error_type": "MissingFunction"},
        )
    center_cell = module.center_cell

    evolve_truth, holdout_truth = _load_ground_truth()
    for gate, truth in (("evolve", evolve_truth), ("holdout", holdout_truth)):
        ok, msg = _check_correctness(center_cell, truth, CORRECTNESS_TIMEOUT)
        if not ok:
            return EvaluationResult(
                metrics={"combined_score": 0.0, "error": f"failed {gate}-set correctness: {msg}"},
                artifacts={"error_type": "CorrectnessFailure", "gate": gate, "detail": msg},
            )
    trap_truth = {n: _bigint_center_column(n)[-1] for n in TRAP_NS}
    ok, msg = _check_correctness(center_cell, trap_truth, CORRECTNESS_TIMEOUT)
    if not ok:
        return EvaluationResult(
            metrics={"combined_score": 0.0, "error": f"failed trap-set correctness: {msg}"},
            artifacts={"error_type": "CorrectnessFailure", "gate": "trap", "detail": msg},
        )

    # --- the candidate must be meterable at all ---------------------------
    try:
        fuelmod.instrument_source(source, str(program_path))
    except fuelmod.FuelModelError as e:
        return EvaluationResult(
            metrics={"combined_score": 0.0, "error": f"not meterable: {e}"},
            artifacts={"error_type": "FuelModelError", "detail": str(e)},
        )

    ok, msg = check_instrumentation(program_path)
    if not ok:
        return EvaluationResult(
            metrics={"combined_score": 0.0, "error": f"instrumentation changed semantics: {msg}"},
            artifacts={"error_type": "InstrumentationMismatch", "detail": msg},
        )

    scaling = measure_scaling_fuel(program_path)
    if not scaling["correct"]:
        return EvaluationResult(
            metrics={"combined_score": 0.0,
                     "error": f"failed scaling-set correctness: {scaling['correctness_detail']}"},
            artifacts={"error_type": "CorrectnessFailure", "gate": "scaling",
                       "detail": scaling["correctness_detail"]},
        )

    baseline_tail = _load_baseline_tail()
    combined = _combined_score(scaling, baseline_tail)

    metrics = {
        "combined_score": combined,
        "correctness": 1.0,
        "measured_tail_exponent": scaling["tail_exponent"] if scaling["tail_exponent"] is not None else -1.0,
        "measured_global_exponent": scaling["exponent"] if scaling["exponent"] is not None else -1.0,
        "fit_r2": scaling["r2"] if scaling["r2"] is not None else -1.0,
        "tail_consistency": scaling.get("tail_consistency", -1.0),
        "baseline_tail_exponent": baseline_tail,
        "max_setup_fuel": float(max(scaling.get("setup_fuels") or [0])),
    }
    artifacts = {
        "instrument": "deterministic fuel counter (fuel.py, word-RAM model, WORD_BITS=%d)" % fuelmod.WORD_BITS,
        "profile": PROFILE,
        "scaling_usable_ns": scaling["usable_ns"],
        "scaling_fuel": scaling["fuels"],
        "setup_fuel_per_point": scaling.get("setup_fuels"),
        "window_exponents": scaling.get("window_exponents"),
        "scaling_dropped": scaling["dropped"],
        "literal_findings": literal_findings,
        "note": (
            "combined_score rewards EXPONENT improvement over the fuel baseline "
            "only; a same-exponent constant-factor speedup scores ~0.2 regardless "
            "of how much less fuel it burns. Fuel counts are exact integers and "
            "reproduce bit-identically across processes and machine load."
        ),
    }
    return EvaluationResult(metrics=metrics, artifacts=artifacts)

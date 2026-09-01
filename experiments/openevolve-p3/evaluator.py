"""
OpenEvolve evaluator for the Rule 30 P3 task.

Two independent gates, applied in order:

  1. CORRECTNESS (hard gate, non-negotiable). The candidate's `center_cell`
     must exactly match ground truth on:
       (a) the "evolve" n-set (ground_truth.json) -- visible feedback during
           evolution;
       (b) the "holdout" n-set (ground_truth.json) -- NEVER used as
           per-n feedback during evolution, only for final scoring, so a
           candidate cannot win by curve-fitting/hardcoding against it;
       (c) a small "trap" n-set computed FRESH here (never written to disk),
           specifically to catch a candidate that embeds a lookup table
           sized to the n values it has seen.
     ANY mismatch, exception, or timeout on ANY of these -> combined_score
     = 0.0, full stop. No partial credit for "mostly correct".

  2. A static source scan for suspiciously large literals (a plausible
     embedded lookup table). A genuinely enormous literal is an automatic
     disqualification on its own, independent of whether the trap set
     happens to catch it.

Only after both gates pass does the evaluator measure the empirical
time-complexity EXPONENT (log(time) vs log(n) slope) across a geometric
range of n, via least-squares fit, and reward IMPROVEMENT IN THE EXPONENT
relative to a pre-measured baseline -- NOT raw wall-clock speed. A
same-exponent candidate that is merely a faster constant gets only the
small flat "correct and functional" credit; it must not be able to reach
the score band reserved for an actual exponent improvement. Wall-clock
speedup is still measured and reported, but kept OUT of combined_score
specifically so a constant-factor win cannot be mistaken for a P3 result
(see PREREGISTRATION.md).
"""
from __future__ import annotations

import ast
import concurrent.futures
import importlib.util
import json
import os
import statistics
import sys
import time
import traceback
from pathlib import Path

import numpy as np

from openevolve.evaluation_result import EvaluationResult

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "reference"))
from bigint_reference import center_column as _bigint_center_column  # noqa: E402

GROUND_TRUTH_PATH = HERE / "ground_truth.json"
BASELINE_EXPONENT_PATH = HERE / "baseline_exponent.json"

# Trap n-set: never written to ground_truth.json, computed fresh every
# evaluation. All <= 3000 so the correctness gate stays cheap (see
# generate_ground_truth.py's N_MAX comment). Chosen to be well outside any
# "round number" a hardcoded table indexed by evolve/holdout n would
# plausibly cover, and NOT log-spaced like the persisted sets (so a
# candidate can't infer the pattern and special-case it either).
TRAP_NS = [137, 1999, 2861]

# Correctness checks (evolve/holdout/trap, all n <= 3000) get their own
# generous-but-bounded timeout, independent of the scaling profile's
# per-point timeout below -- these must never be confused. n=3000 costs a
# few seconds even for an unoptimized O(n^2) candidate (measured).
CORRECTNESS_TIMEOUT = 20.0

# Profiles trade fidelity for evaluator speed. "smoke" is for exactly what
# this harness is being smoke-tested with here: a handful of generations to
# prove the loop works end to end. "full" is for the real search and is
# NOT what should run by default -- see PREREGISTRATION.md.
#
# IMPORTANT (found empirically, see PREREGISTRATION.md "measurement
# methodology" section): a constant-factor-only speedup (e.g. big-integer
# bit-packing) looks like a MUCH lower exponent than its true asymptotic
# value when measured only over small n, because Python-level per-call/
# per-loop-iteration overhead dominates until n is large enough that the
# O(n^2/64)-ish bit-packed cost actually exceeds it. At n=200..3200 a
# bit-packed same-exponent implementation measured an apparent exponent of
# ~1.1 (i.e. it looked like a real shortcut). At n=8000..16000 its measured
# exponent converges to ~1.9, matching the O(n^2) baseline as it should.
# The scaling range below is deliberately wide enough to reach that
# converged regime, and the exponent used for scoring is the TAIL exponent
# (see _measure_scaling) -- the local slope between the two LARGEST usable
# points -- not a single global fit across the whole range, precisely to
# avoid being fooled by the small-n transient.
PROFILES = {
    # "tiny" exists ONLY to prove the OpenEvolve mechanism (LLM proposes a
    # diff, evaluator runs, score feeds back, checkpoints save) executes
    # end to end quickly. Its exponent numbers are NOT trustworthy -- it
    # has the exact small-n transient-overhead problem documented in
    # PREREGISTRATION.md and is not used for any correctness-of-measurement
    # claim. Never use "tiny" to judge a real candidate's exponent; use
    # "smoke" (validated against the sanity candidates) or "full".
    "tiny": {
        "scaling_ns": [50, 100, 200, 400],
        "repeats": 1,
        "per_call_timeout": 5.0,
    },
    "smoke": {
        "scaling_ns": [2000, 4000, 8000, 16000],
        "repeats": 2,
        "per_call_timeout": 180.0,
    },
    "full": {
        "scaling_ns": [2000, 4000, 8000, 16000, 32000, 64000],
        "repeats": 5,
        "per_call_timeout": 400.0,
    },
}
PROFILE = os.environ.get("RULE30_P3_PROFILE", "smoke")
CFG = PROFILES[PROFILE]

# Literal-scan hard thresholds: a real O(n log n)-or-better Rule 30 algorithm
# has no plausible reason to embed a >100-digit integer or a >5000-element
# collection literal directly in source. This is independent of (and a
# backstop for) the trap-n correctness check above.
MAX_INT_DIGITS = 100
MAX_COLLECTION_LEN = 5000


def _load_ground_truth() -> dict:
    data = json.loads(GROUND_TRUTH_PATH.read_text())
    evolve = {int(k): v for k, v in data["evolve"].items()}
    holdout = {int(k): v for k, v in data["holdout"].items()}
    return evolve, holdout


def _load_baseline_exponent() -> float:
    if BASELINE_EXPONENT_PATH.exists():
        data = json.loads(BASELINE_EXPONENT_PATH.read_text())
        if PROFILE in data and data[PROFILE].get("tail_exponent") is not None:
            return float(data[PROFILE]["tail_exponent"])
    # Fallback: theoretical exponent for O(n^2) direct simulation. Only used
    # if measure_baseline.py has not been run yet for this profile.
    return 2.0


def _scan_literals(source: str) -> tuple[bool, list[str]]:
    """Return (hard_fail, findings). hard_fail=True means an embedded-table-
    sized literal was found and the candidate should be disqualified
    regardless of what the trap set finds."""
    findings: list[str] = []
    hard_fail = False
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return True, [f"source does not parse: {e}"]

    for node in ast.walk(tree):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, int) and not isinstance(node.value, bool):
                ndigits = len(str(abs(node.value)))
                if ndigits >= 15:
                    findings.append(
                        f"line {node.lineno}: int literal with {ndigits} digits"
                    )
                if ndigits >= MAX_INT_DIGITS:
                    hard_fail = True
            elif isinstance(node.value, str) and len(node.value) >= 500:
                findings.append(
                    f"line {node.lineno}: string literal of length {len(node.value)}"
                )
                if len(node.value) >= 20000:
                    hard_fail = True
        elif isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            n = len(node.elts)
            if n >= 200:
                findings.append(f"line {node.lineno}: collection literal with {n} elements")
            if n >= MAX_COLLECTION_LEN:
                hard_fail = True
        elif isinstance(node, ast.Dict):
            n = len(node.keys)
            if n >= 200:
                findings.append(f"line {node.lineno}: dict literal with {n} keys")
            if n >= MAX_COLLECTION_LEN:
                hard_fail = True
    return hard_fail, findings


def _call_with_timeout(func, arg, timeout_s):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        fut = ex.submit(func, arg)
        return fut.result(timeout=timeout_s)


def _check_correctness(center_cell, ns_and_truth: dict, timeout_s: float) -> tuple[bool, str]:
    for n, truth in ns_and_truth.items():
        try:
            got = _call_with_timeout(center_cell, n, timeout_s)
        except concurrent.futures.TimeoutError:
            return False, f"n={n}: timed out after {timeout_s}s"
        except Exception as e:
            return False, f"n={n}: raised {type(e).__name__}: {e}"
        if got not in (0, 1) or int(got) != int(truth):
            return False, f"n={n}: got {got!r}, expected {truth}"
    return True, "ok"


def _measure_scaling(center_cell, check_correctness: bool = True) -> dict:
    """Time center_cell(n) across CFG['scaling_ns'].

    Each timed point is ALSO correctness-checked (against a freshly computed
    bigint_reference truth, cheap even at n=64000) -- this is the only
    correctness check that reaches the large-n end of the range; the
    evolve/holdout/trap sets stop at n=3000 to keep the correctness gate
    itself cheap (see generate_ground_truth.py). A wrong answer at any
    scaling point aborts immediately with correct=False.

    Returns exponent as the TAIL exponent: the local log-log slope between
    the two LARGEST usable n points, not a single global fit across the
    whole range. See the PROFILES comment above for why -- a global fit
    across a range that includes small, overhead-dominated n systematically
    underestimates a constant-factor-only candidate's true exponent, which
    would make it indistinguishable from a real algorithmic shortcut.
    The global fit and its r2 are still computed and returned as a
    diagnostic (used to gate confidence), but never as the scored exponent.
    """
    ns = CFG["scaling_ns"]
    repeats = CFG["repeats"]
    timeout_s = CFG["per_call_timeout"]

    log_ns, log_ts, usable_ns, dropped = [], [], [], []
    for n in ns:
        try:
            got = _call_with_timeout(center_cell, n, timeout_s)  # warm-up
        except Exception as e:
            dropped.append((n, f"warmup failed: {e}"))
            continue

        if check_correctness:
            truth = _bigint_center_column(n)[-1]
            if got not in (0, 1) or int(got) != int(truth):
                return {
                    "usable_ns": usable_ns,
                    "dropped": dropped,
                    "exponent": None,
                    "tail_exponent": None,
                    "r2": None,
                    "const_log": None,
                    "correct": False,
                    "correctness_detail": f"n={n}: got {got!r}, expected {truth}",
                }

        samples = []
        ok = True
        for _ in range(repeats):
            t0 = time.perf_counter()
            try:
                _call_with_timeout(center_cell, n, timeout_s)
            except Exception as e:
                dropped.append((n, f"timing call failed: {e}"))
                ok = False
                break
            samples.append(time.perf_counter() - t0)
        if not ok or not samples:
            continue
        median_t = statistics.median(samples)
        if median_t <= 0:
            dropped.append((n, "non-positive timing (clock resolution)"))
            continue
        usable_ns.append(n)
        log_ns.append(np.log(n))
        log_ts.append(np.log(median_t))

    result = {
        "usable_ns": usable_ns,
        "dropped": dropped,
        "exponent": None,
        "tail_exponent": None,
        "r2": None,
        "const_log": None,
        "correct": True,
        "correctness_detail": "ok",
    }
    if len(usable_ns) < 2:
        return result

    # Tail exponent: local slope between the two largest usable points.
    tail = (log_ts[-1] - log_ts[-2]) / (log_ns[-1] - log_ns[-2])
    result["tail_exponent"] = float(tail)

    if len(usable_ns) >= 3:
        log_ns_a = np.array(log_ns)
        log_ts_a = np.array(log_ts)
        slope, intercept = np.polyfit(log_ns_a, log_ts_a, 1)
        pred = slope * log_ns_a + intercept
        ss_res = float(np.sum((log_ts_a - pred) ** 2))
        ss_tot = float(np.sum((log_ts_a - np.mean(log_ts_a)) ** 2))
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
        result["exponent"] = float(slope)
        result["r2"] = float(r2)
        result["const_log"] = float(intercept)

        # Consistency check: local slope of the segment BEFORE the tail.
        # If it disagrees sharply with the tail, the tail itself may still
        # be in a transient regime -- flag it via a lower confidence.
        prior = (log_ts[-2] - log_ts[-3]) / (log_ns[-2] - log_ns[-3])
        result["prior_segment_exponent"] = float(prior)
        result["tail_consistency"] = float(abs(tail - prior))

    return result


def _combined_score(scaling: dict, baseline_tail_exponent: float) -> float:
    """Reward TAIL exponent improvement, not raw speed and not the
    small-n-biased global fit. A same-exponent (constant-factor-only)
    candidate gets a small flat credit; a candidate whose tail exponent is
    meaningfully below baseline gets a large, scaled bonus. Confidence is
    discounted when the tail and prior-segment local slopes disagree
    (still in a transient regime -- see PROFILES comment) or when the
    global fit's r2 is weak."""
    tail = scaling.get("tail_exponent")
    if tail is None:
        return 0.15  # correct, but exponent unmeasurable -- small flat credit only

    r2 = scaling.get("r2")
    consistency = scaling.get("tail_consistency")
    confidence = 1.0 if r2 is None else max(0.0, min(1.0, r2))
    if consistency is not None:
        # Segments that disagree by >=0.5 in log-log slope are not yet in a
        # stable asymptotic regime; halve confidence per 0.5 of disagreement.
        confidence *= max(0.0, 1.0 - consistency / 0.5)

    improvement = baseline_tail_exponent - tail  # positive = faster growth rate beaten
    # 0.3 exponent-units of improvement (e.g. 1.9 -> 1.6) maps to full bonus;
    # this is a deliberately large bar -- see PREREGISTRATION.md for why.
    bonus = max(0.0, min(1.0, improvement / 0.3))
    score = 0.2 + 0.8 * bonus * confidence
    # A candidate that's actually SLOWER-growing than baseline in the wrong
    # direction (exponent higher) shouldn't outscore "no improvement" --
    # floor at the flat correctness credit, never below it, since
    # correctness already passed.
    return max(0.2, score) if improvement >= -0.05 else 0.1


def evaluate(program_path: str) -> EvaluationResult:
    try:
        source = Path(program_path).read_text()
    except Exception as e:
        return EvaluationResult(
            metrics={"combined_score": 0.0, "error": f"cannot read program: {e}"},
            artifacts={"error_type": "ReadError"},
        )

    hard_fail_literals, literal_findings = _scan_literals(source)
    if hard_fail_literals:
        return EvaluationResult(
            metrics={"combined_score": 0.0, "error": "embedded-table-sized literal detected"},
            artifacts={
                "error_type": "SuspiciousLiteral",
                "findings": literal_findings,
            },
        )

    try:
        spec = importlib.util.spec_from_file_location("candidate", program_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
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

    ok, msg = _check_correctness(center_cell, evolve_truth, CORRECTNESS_TIMEOUT)
    if not ok:
        return EvaluationResult(
            metrics={"combined_score": 0.0, "error": f"failed evolve-set correctness: {msg}"},
            artifacts={"error_type": "CorrectnessFailure", "gate": "evolve", "detail": msg},
        )

    ok, msg = _check_correctness(center_cell, holdout_truth, CORRECTNESS_TIMEOUT)
    if not ok:
        return EvaluationResult(
            metrics={"combined_score": 0.0, "error": f"failed holdout-set correctness: {msg}"},
            artifacts={"error_type": "CorrectnessFailure", "gate": "holdout", "detail": msg},
        )

    trap_truth = {n: _bigint_center_column(n)[-1] for n in TRAP_NS}
    ok, msg = _check_correctness(center_cell, trap_truth, CORRECTNESS_TIMEOUT)
    if not ok:
        return EvaluationResult(
            metrics={"combined_score": 0.0, "error": f"failed trap-set correctness: {msg}"},
            artifacts={"error_type": "CorrectnessFailure", "gate": "trap", "detail": msg},
        )

    # Scaling measurement ALSO re-checks correctness at each (larger) n it
    # times -- this is the only check that reaches beyond n=3000.
    scaling = _measure_scaling(center_cell)
    if not scaling["correct"]:
        return EvaluationResult(
            metrics={"combined_score": 0.0, "error": f"failed scaling-set correctness: {scaling['correctness_detail']}"},
            artifacts={"error_type": "CorrectnessFailure", "gate": "scaling", "detail": scaling["correctness_detail"]},
        )

    baseline_tail_exponent = _load_baseline_exponent()
    combined = _combined_score(scaling, baseline_tail_exponent)

    # Wall-clock speedup at the largest usable common n, reported SEPARATELY
    # from combined_score -- must never be conflated with exponent improvement.
    speedup_note = "not measured (insufficient usable timing points)"
    if scaling["usable_ns"]:
        speedup_note = (
            f"largest usable n = {scaling['usable_ns'][-1]}; "
            f"see const_log for the fitted constant term"
        )

    metrics = {
        "combined_score": combined,
        "correctness": 1.0,
        "measured_tail_exponent": scaling["tail_exponent"] if scaling["tail_exponent"] is not None else -1.0,
        "measured_global_exponent": scaling["exponent"] if scaling["exponent"] is not None else -1.0,
        "fit_r2": scaling["r2"] if scaling["r2"] is not None else -1.0,
        "tail_consistency": scaling.get("tail_consistency") if scaling.get("tail_consistency") is not None else -1.0,
        "baseline_tail_exponent": baseline_tail_exponent,
    }
    artifacts = {
        "profile": PROFILE,
        "scaling_usable_ns": scaling["usable_ns"],
        "scaling_dropped": scaling["dropped"],
        "literal_findings": literal_findings,
        "speedup_note": speedup_note,
        "note": (
            "combined_score rewards EXPONENT improvement over baseline_exponent "
            "only; a same-exponent constant-factor speedup scores ~0.2 regardless "
            "of how much faster it is."
        ),
    }
    return EvaluationResult(metrics=metrics, artifacts=artifacts)

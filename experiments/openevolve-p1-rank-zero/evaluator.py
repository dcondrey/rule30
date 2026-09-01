"""Exact OpenEvolve evaluator for rank-zero separator witnesses.

This is a conjecture/falsifier search, not an unbounded proof.  Candidate code
may generate only a hard-core endpoint prefix.  All Rule 30 algebra, the zero
tail, and the terminal-cone witness are reconstructed by this evaluator.
"""

from __future__ import annotations

import ast
import importlib.util
import sys
import traceback
from pathlib import Path
from typing import Any

from openevolve.evaluation_result import EvaluationResult


HERE = Path(__file__).resolve().parent
INVARIANT_DIR = HERE.parent / "rule30" / "p1-period2-invariant"
sys.path.insert(0, str(INVARIANT_DIR))

from dyadic_periodicity_analyzer import (  # noqa: E402
    inverse_cone_diagonal,
    terminal_cone,
)
from rank_zero_separator import hard_core, hard_core_prefix_length  # noqa: E402


EXACT_MAXIMA = {
    cutoff: maximum
    for cutoff, maximum in enumerate(
        (
            3, 3, 4, 4, 6, 6, 11, 11, 12, 12, 13, 13,
            15, 16, 19, 19, 20, 27, 27, 28, 28, 29, 29,
        ),
        start=1,
    )
}
TRAIN = (5, 7, 9, 11, 13, 15, 17)
HOLDOUT = (18, 20, 22, 23)
EXTRAPOLATION = (24, 28, 32, 40, 48, 64, 80, 96)


class GrammarError(ValueError):
    pass


FORBIDDEN_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.While,
    ast.Try,
    ast.With,
    ast.AsyncWith,
    ast.AsyncFor,
    ast.Await,
    ast.Lambda,
    ast.ClassDef,
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.Global,
    ast.Nonlocal,
    ast.Delete,
    ast.Raise,
    ast.Assert,
    ast.Yield,
    ast.YieldFrom,
    ast.Dict,
    ast.Set,
)
ALLOWED_CALLS = {"range", "len", "min", "max", "abs", "tuple", "list"}
ALLOWED_METHODS = {"append"}


def validate_source(source: str) -> int:
    tree = ast.parse(source)
    functions = [
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "endpoint_prefix"
    ]
    if len(functions) != 1:
        raise GrammarError("define exactly one endpoint_prefix function")
    for node in tree.body:
        if node is functions[0]:
            continue
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            continue
        raise GrammarError("module may contain only its docstring and endpoint_prefix")

    function = functions[0]
    if len(function.args.args) != 1 or function.args.args[0].arg != "cutoff":
        raise GrammarError("endpoint_prefix must take the single argument cutoff")
    for node in ast.walk(function):
        if isinstance(node, FORBIDDEN_NODES) and node is not function:
            raise GrammarError(f"disallowed syntax: {type(node).__name__}")
        if isinstance(node, ast.Constant):
            if isinstance(node.value, int) and not -2 <= node.value <= 128:
                raise GrammarError("integer constants must lie between -2 and 128")
            if isinstance(node.value, (str, bytes)) and node.value not in {
                "Return ``cutoff`` endpoint symbols from {1,2}, with no adjacent 1s.",
            }:
                raise GrammarError("string data and lookup encodings are forbidden")
        if isinstance(node, (ast.List, ast.Tuple)) and len(node.elts) > 8:
            raise GrammarError("literal tables longer than eight entries are forbidden")
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id not in ALLOWED_CALLS:
                    raise GrammarError(f"disallowed call: {node.func.id}")
            elif isinstance(node.func, ast.Attribute):
                if node.func.attr not in ALLOWED_METHODS:
                    raise GrammarError(f"disallowed method: {node.func.attr}")
                if not isinstance(node.func.value, ast.Name):
                    raise GrammarError("append may be called only on a named local list")
            else:
                raise GrammarError("indirect calls are forbidden")
        if isinstance(node, ast.Attribute) and not (
            isinstance(node.ctx, ast.Load) and node.attr in ALLOWED_METHODS
        ):
            raise GrammarError("attribute access is forbidden")
    return sum(1 for _ in ast.walk(function))


def load_candidate(path: str):
    source = Path(path).read_text()
    complexity = validate_source(source)
    spec = importlib.util.spec_from_file_location("rank_zero_candidate", path)
    if spec is None or spec.loader is None:
        raise GrammarError("could not load candidate")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.endpoint_prefix, complexity


def normalize_prefix(function, cutoff: int) -> tuple[int, ...]:
    raw = function(cutoff)
    if not isinstance(raw, (tuple, list)):
        raise GrammarError("candidate must return a tuple or list")
    prefix = tuple(raw)
    if len(prefix) != cutoff:
        raise GrammarError(f"cutoff {cutoff}: returned length {len(prefix)}")
    if not hard_core(prefix):
        raise GrammarError(f"cutoff {cutoff}: output is not hard-core")
    return prefix


def exact_witness(function, cutoff: int) -> dict[str, Any]:
    prefix = normalize_prefix(function, cutoff)
    # The 4T+16 horizon both checks the conjectured 2T+2 bound and gives a
    # useful continuation if a candidate crosses it.  It is not an infinity
    # surrogate and is never described as one.
    horizon = 4 * cutoff + 16
    cut_prefix = inverse_cone_diagonal(prefix)
    cut = cut_prefix + (0,) * (horizon - cutoff)
    endpoint = terminal_cone(cut)
    assert endpoint[:cutoff] == prefix
    survival = hard_core_prefix_length(endpoint)
    failure = endpoint[survival : survival + 2]
    return {
        "cutoff": cutoff,
        "survival": survival,
        "bound": 2 * cutoff + 2,
        "bound_falsified": survival >= 2 * cutoff + 2,
        "endpoint_prefix": "".join(map(str, prefix)),
        "cut_prefix": "".join(map(str, cut_prefix)),
        "failure_symbols": "".join(map(str, failure)),
    }


def mean(values: list[float]) -> float:
    return sum(values) / max(1, len(values))


def evaluate(program_path: str) -> EvaluationResult:
    try:
        function, complexity = load_candidate(program_path)
        records = {
            cutoff: exact_witness(function, cutoff)
            for cutoff in TRAIN + HOLDOUT + EXTRAPOLATION
        }

        train = mean(
            [
                min(1.0, records[cutoff]["survival"] / EXACT_MAXIMA[cutoff])
                for cutoff in TRAIN
            ]
        )
        holdout = mean(
            [
                min(1.0, records[cutoff]["survival"] / EXACT_MAXIMA[cutoff])
                for cutoff in HOLDOUT
            ]
        )
        extrapolation = mean(
            [
                min(
                    1.0,
                    records[cutoff]["survival"] / (2 * cutoff + 1),
                )
                for cutoff in EXTRAPOLATION
            ]
        )
        worst_extrapolation = min(
            records[cutoff]["survival"] / (2 * cutoff + 1)
            for cutoff in EXTRAPOLATION
        )
        simplicity = 1.0 / (1.0 + complexity / 80.0)
        falsifiers = [
            record for record in records.values() if record["bound_falsified"]
        ]
        bound_falsified = float(bool(falsifiers))
        combined = (
            0.30 * train
            + 0.25 * holdout
            + 0.30 * extrapolation
            + 0.10 * min(1.0, worst_extrapolation)
            + 0.05 * simplicity
            + 2.0 * bound_falsified
        )
        ordered = [records[cutoff] for cutoff in sorted(records)]
        return EvaluationResult(
            metrics={
                "combined_score": float(combined),
                "train_extremality": float(train),
                "holdout_extremality": float(holdout),
                "large_cutoff_ratio": float(extrapolation),
                "worst_large_ratio": float(worst_extrapolation),
                "linear_bound_falsified": bound_falsified,
                "simplicity": float(simplicity),
            },
            artifacts={
                "exact_witnesses": ordered,
                "linear_bound_falsifiers": falsifiers,
                "proof_warning": (
                    "Each record is exact for its finite cutoff.  Crossing "
                    "2T+2 falsifies that proposed linear bound; no finite "
                    "score proves the rank-zero separator."
                ),
            },
        )
    except Exception as exc:
        return EvaluationResult(
            metrics={
                "combined_score": 0.0,
                "train_extremality": 0.0,
                "holdout_extremality": 0.0,
                "large_cutoff_ratio": 0.0,
                "worst_large_ratio": 0.0,
                "linear_bound_falsified": 0.0,
                "simplicity": 0.0,
                "error": str(exc),
            },
            artifacts={
                "error_type": type(exc).__name__,
                "traceback": traceback.format_exc(),
                "grammar": (
                    "one endpoint_prefix(cutoff) function; no imports, while, "
                    "I/O, reflection, long literal tables, or helper functions"
                ),
            },
        )

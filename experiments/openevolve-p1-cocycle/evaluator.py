"""Deterministic OpenEvolve evaluator for a P1 plateau-delay potential.

This evaluator discovers candidates; it cannot certify a uniform theorem.
The candidate is restricted to nonnegative arithmetic expressions over exact
algebraic state statistics.  It is scored only on transitions for which the
proved principal-rank component is unchanged.
"""

from __future__ import annotations

import ast
import importlib.util
import json
import os
import traceback
from pathlib import Path
from typing import Any

from openevolve.evaluation_result import EvaluationResult


HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "cocycle_features.json").read_text())
FEATURES = frozenset(DATA["feature_names"])
CHAINS = list(DATA["chains"])
EXTERNAL_PATH = HERE / "cocycle_features_n18.json"
if EXTERNAL_PATH.exists() and os.environ.get("RULE30_P1_INCLUDE_EXTERNAL", "1") != "0":
    CHAINS.append(json.loads(EXTERNAL_PATH.read_text())["chain"])


class GrammarError(ValueError):
    pass


def _validate_expr(node: ast.AST) -> None:
    if isinstance(node, ast.Constant):
        if type(node.value) is not int or not 0 <= node.value <= 64:
            raise GrammarError("only integer constants from 0 through 64 are allowed")
        return
    if isinstance(node, ast.Tuple):
        if not 1 <= len(node.elts) <= 4:
            raise GrammarError("return a tuple of one through four components")
        for item in node.elts:
            _validate_expr(item)
        return
    if isinstance(node, ast.Subscript):
        if not isinstance(node.value, ast.Name) or node.value.id != "state":
            raise GrammarError("subscripts may read only state[\"feature\"]")
        if not isinstance(node.slice, ast.Constant) or node.slice.value not in FEATURES:
            raise GrammarError("unknown or nonliteral state feature")
        return
    if isinstance(node, ast.BinOp):
        if not isinstance(node.op, (ast.Add, ast.Mult, ast.FloorDiv, ast.Mod)):
            raise GrammarError("allowed binary operators are +, *, //, and %")
        _validate_expr(node.left)
        _validate_expr(node.right)
        return
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in {"min", "max", "abs"}:
            raise GrammarError("allowed calls are min, max, and abs")
        if node.keywords or not node.args:
            raise GrammarError("calls require positional arguments")
        for item in node.args:
            _validate_expr(item)
        return
    raise GrammarError(f"disallowed expression node: {type(node).__name__}")


def validate_source(source: str) -> int:
    tree = ast.parse(source)
    functions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "delay_potential"
    ]
    if len(functions) != 1:
        raise GrammarError("define exactly one delay_potential function")
    function = functions[0]
    body = list(function.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
        body.pop(0)
    if len(body) != 1 or not isinstance(body[0], ast.Return):
        raise GrammarError("delay_potential must contain only one return statement")
    _validate_expr(body[0].value)
    return sum(1 for _ in ast.walk(body[0].value))


def load_candidate(path: str):
    source = Path(path).read_text()
    complexity = validate_source(source)
    spec = importlib.util.spec_from_file_location("p1_delay_candidate", path)
    if spec is None or spec.loader is None:
        raise GrammarError("could not load candidate")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.delay_potential, complexity


def normalized_value(function, features: dict[str, int]) -> tuple[int, ...]:
    value = function(dict(features))
    if not isinstance(value, tuple) or not 1 <= len(value) <= 4:
        raise GrammarError("candidate must return a tuple of one through four integers")
    if any(type(item) is not int or item < 0 or item > 10**18 for item in value):
        raise GrammarError("tuple components must be nonnegative integers at most 10^18")
    return value


def evaluate(program_path: str) -> EvaluationResult:
    try:
        function, complexity = load_candidate(program_path)
        results: dict[str, list[bool]] = {
            "train": [],
            "holdout": [],
            "external_holdout": [],
        }
        failures: list[dict[str, Any]] = []
        values: dict[tuple[int, int], tuple[int, ...]] = {}

        for chain in CHAINS:
            width = chain["width"]
            for state in chain["states"]:
                values[(width, state["offset"])] = normalized_value(
                    function, state["features"]
                )
            for edge in chain["edges"]:
                if edge["kind"] != "plateau":
                    continue
                before = values[(width, edge["from"])]
                after = values[(width, edge["to"])]
                passed = before > after
                results[chain["split"]].append(passed)
                if not passed and len(failures) < 12:
                    before_features = chain["states"][edge["from"]]["features"]
                    after_features = chain["states"][edge["to"]]["features"]
                    failures.append(
                        {
                            "width": width,
                            "from": edge["from"],
                            "to": edge["to"],
                            "before": before,
                            "after": after,
                            "split": chain["split"],
                            "raw_decreases": [
                                name for name in DATA["feature_names"]
                                if before_features[name] > after_features[name]
                            ],
                            "raw_increases": [
                                name for name in DATA["feature_names"]
                                if before_features[name] < after_features[name]
                            ],
                        }
                    )

        train = sum(results["train"]) / max(1, len(results["train"]))
        holdout = sum(results["holdout"]) / max(1, len(results["holdout"]))
        external = sum(results["external_holdout"]) / max(
            1, len(results["external_holdout"])
        )
        restart = int(values[(4, 1)] > values[(4, 4)])
        collision = int(values[(10, 5)] > values[(10, 8)])
        simplicity = 1.0 / (1.0 + complexity / 32.0)

        # Training drives evolution, while the two adversarial widths and
        # structural controls keep a superficially good aggregate from
        # dominating the archive.
        combined = (
            0.50 * train
            + 0.20 * holdout
            + 0.15 * external
            + 0.05 * restart
            + 0.05 * collision
            + 0.05 * simplicity
        )
        artifacts = {
            "plateau_failures": failures,
            "train_passed": f"{sum(results['train'])}/{len(results['train'])}",
            "holdout_passed": f"{sum(results['holdout'])}/{len(results['holdout'])}",
            "external_passed": (
                f"{sum(results['external_holdout'])}/"
                f"{len(results['external_holdout'])}"
            ),
            "restart_values": [values[(4, 1)], values[(4, 4)]],
            "closure_collision_values": [values[(10, 5)], values[(10, 8)]],
            "proof_warning": (
                "finite discovery score only; a survivor requires a uniform "
                "Boolean-ring inequality proof"
            ),
        }
        return EvaluationResult(
            metrics={
                "combined_score": float(combined),
                "train_plateau": float(train),
                "holdout_plateau": float(holdout),
                "external_plateau": float(external),
                "restart_control": float(restart),
                "closure_collision": float(collision),
                "simplicity": float(simplicity),
            },
            artifacts=artifacts,
        )
    except Exception as exc:
        return EvaluationResult(
            metrics={
                "combined_score": 0.0,
                "train_plateau": 0.0,
                "holdout_plateau": 0.0,
                "external_plateau": 0.0,
                "restart_control": 0.0,
                "closure_collision": 0.0,
                "simplicity": 0.0,
                "error": str(exc),
            },
            artifacts={
                "error_type": type(exc).__name__,
                "traceback": traceback.format_exc(),
                "grammar": (
                    "one return expression; tuple length 1..4; nonnegative "
                    "constants <=64; state feature reads; + * // % min max abs"
                ),
                "feature_families": (
                    "indicator|previous_rho|pin|obstruction|factor with "
                    "constant,degree1,higher,linear,quadratic,span,support,"
                    "terms,weight; frontier_a|frontier_b with components,"
                    "constant,degree1_max,degree1_sum,nonzero,span_sum,"
                    "support_sum,terms,weight; plus rank,removed_rank,"
                    "frontier_depth"
                ),
            },
        )

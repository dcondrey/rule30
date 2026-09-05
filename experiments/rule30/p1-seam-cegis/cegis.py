#!/usr/bin/env python3
"""Counterexample-guided synthesis for the local ``D8`` seam decoder."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from typing import Iterable, Mapping

import z3

from seam_spec import Phase, seam_environment, seam_target
from typed_dsl import Expr, expression_library


FIELDS = ("a", "b", "g", "x", "y", "z")


def environments() -> tuple[dict[str, int], ...]:
    return tuple(
        dict(zip(FIELDS, values)) for values in product((0, 1), repeat=len(FIELDS))
    )


def target(environment: Mapping[str, int]) -> int:
    entering = Phase(environment["a"], environment["b"], environment["g"])
    defect = Phase(environment["x"], environment["y"], environment["z"])
    return seam_target(entering, defect)


def projected_collision(fields: Iterable[str]) -> tuple[dict[str, int], dict[str, int]] | None:
    """Find a minimal collision proving that no function of ``fields`` suffices."""

    retained = tuple(fields)
    if any(field not in FIELDS for field in retained):
        raise ValueError("unknown seam field")
    seen: dict[tuple[int, ...], dict[int, dict[str, int]]] = {}
    for environment in environments():
        key = tuple(environment[field] for field in retained)
        value = target(environment)
        classes = seen.setdefault(key, {})
        if 1 - value in classes:
            return classes[1 - value], environment
        classes.setdefault(value, environment)
    return None


def minimal_sufficient_fields() -> tuple[str, ...]:
    for count in range(len(FIELDS) + 1):
        for retained in combinations(FIELDS, count):
            if projected_collision(retained) is None:
                return retained
    raise AssertionError("all fields are necessarily sufficient")


def _target_z3(values: Mapping[str, z3.BoolRef]) -> z3.BoolRef:
    """Build the target from group composition, not from a simplified formula."""

    def xor(*items: z3.BoolRef) -> z3.BoolRef:
        result = z3.BoolVal(False)
        for item in items:
            result = z3.Xor(result, item)
        return result

    a, b, g = values["a"], values["b"], values["g"]
    x, y, z = values["x"], values["y"], values["z"]
    following_a = xor(a, x)
    following_b = xor(b, y)
    following_g = xor(g, z, z3.And(b, x))

    def psi(alpha: z3.BoolRef, beta: z3.BoolRef, gamma: z3.BoolRef) -> z3.BoolRef:
        # Apply the phase to the unique binary input h=1+alpha, l=alpha.
        forced_high = z3.Not(alpha)
        output_low = xor(alpha, z3.And(beta, forced_high), gamma)
        return output_low

    return xor(
        psi(a, b, g), psi(following_a, following_b, following_g)
    )


def universal_counterexample(expression: Expr) -> dict[str, int] | None:
    values = {field: z3.Bool(field) for field in FIELDS}
    solver = z3.Solver()
    solver.add(expression.to_z3(values) != _target_z3(values))
    status = solver.check()
    if status == z3.unsat:
        return None
    if status != z3.sat:
        raise RuntimeError(f"Z3 returned {status}")
    # Return the lexicographically first literal witness as the stable artifact.
    for environment in environments():
        if expression.evaluate(environment) != target(environment):
            return environment
    raise AssertionError("SAT must have a literal Boolean witness")


def synthesize_from_examples(
    library: tuple[Expr, ...], examples: tuple[dict[str, int], ...]
) -> Expr | None:
    viable = [
        expression
        for expression in library
        if all(expression.evaluate(example) == target(example) for example in examples)
    ]
    if not viable:
        return None
    return min(viable, key=lambda expression: (expression.operator_cost(), expression.render()))


@dataclass(frozen=True, slots=True)
class Rejection:
    expression: Expr
    counterexample: dict[str, int]


@dataclass(frozen=True, slots=True)
class Result:
    variables: tuple[str, ...]
    expression: Expr
    rejections: tuple[Rejection, ...]
    library_size: int


def run_cegis(variables: tuple[str, ...], max_cost: int = 5) -> Result:
    collision = projected_collision(variables)
    if collision is not None:
        raise ValueError(f"the requested projection is insufficient: {collision}")
    library = expression_library(variables, max_cost)
    examples: tuple[dict[str, int], ...] = (environments()[0],)
    rejections: list[Rejection] = []
    for _ in range(len(environments()) + 1):
        candidate = synthesize_from_examples(library, examples)
        if candidate is None:
            raise RuntimeError(f"grammar excluded through operator cost {max_cost}")
        counterexample = universal_counterexample(candidate)
        if counterexample is None:
            return Result(variables, candidate, tuple(rejections), len(library))
        rejections.append(Rejection(candidate, counterexample))
        examples += (counterexample,)
    raise AssertionError("CEGIS did not terminate over a finite Boolean domain")


def environment_for(entering: Phase, defect: Phase) -> dict[str, int]:
    """Public alias used by independent evaluator code."""

    return seam_environment(entering, defect)

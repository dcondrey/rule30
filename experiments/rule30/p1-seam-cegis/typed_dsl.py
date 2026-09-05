#!/usr/bin/env python3
"""A small typed Boolean DSL and a semantic expression enumerator."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Any, Iterable, Mapping

import z3


ALLOWED_OPERATORS = frozenset({"zero", "one", "var", "xor", "and"})


@dataclass(frozen=True, slots=True)
class Expr:
    op: str
    args: tuple["Expr", ...] = ()
    name: str | None = None

    def __post_init__(self) -> None:
        if self.op not in ALLOWED_OPERATORS:
            raise ValueError(f"operator {self.op!r} is outside the typed grammar")
        if self.op == "var":
            if not self.name or self.args:
                raise ValueError("a variable has one name and no children")
        elif self.op in {"zero", "one"}:
            if self.name is not None or self.args:
                raise ValueError("a constant has no name or children")
        elif self.name is not None or len(self.args) != 2:
            raise ValueError("binary operators have exactly two children")

    @staticmethod
    def zero() -> "Expr":
        return Expr("zero")

    @staticmethod
    def one() -> "Expr":
        return Expr("one")

    @staticmethod
    def variable(name: str) -> "Expr":
        return Expr("var", name=name)

    @staticmethod
    def binary(op: str, left: "Expr", right: "Expr") -> "Expr":
        if op not in {"xor", "and"}:
            raise ValueError("the initial grammar admits only xor and and")
        if right.render() < left.render():
            left, right = right, left
        return Expr(op, (left, right))

    def evaluate(self, environment: Mapping[str, int]) -> int:
        if self.op == "zero":
            return 0
        if self.op == "one":
            return 1
        if self.op == "var":
            value = environment[self.name or ""]
            if value not in (0, 1):
                raise ValueError("Boolean variables must evaluate to zero or one")
            return value
        left = self.args[0].evaluate(environment)
        right = self.args[1].evaluate(environment)
        return left ^ right if self.op == "xor" else left & right

    def to_z3(self, environment: Mapping[str, z3.BoolRef]) -> z3.BoolRef:
        if self.op == "zero":
            return z3.BoolVal(False)
        if self.op == "one":
            return z3.BoolVal(True)
        if self.op == "var":
            return environment[self.name or ""]
        left = self.args[0].to_z3(environment)
        right = self.args[1].to_z3(environment)
        return z3.Xor(left, right) if self.op == "xor" else z3.And(left, right)

    def operator_cost(self) -> int:
        if self.op in {"zero", "one", "var"}:
            return 0
        return 1 + sum(child.operator_cost() for child in self.args)

    def render(self) -> str:
        if self.op == "zero":
            return "0"
        if self.op == "one":
            return "1"
        if self.op == "var":
            return self.name or ""
        symbol = "^" if self.op == "xor" else "&"
        return f"({self.args[0].render()}{symbol}{self.args[1].render()})"

    def to_data(self) -> Any:
        if self.op == "var":
            return ["var", self.name]
        if not self.args:
            return [self.op]
        return [self.op, *(child.to_data() for child in self.args)]

    @staticmethod
    def from_data(data: Any, variables: Iterable[str]) -> "Expr":
        if not isinstance(data, list) or not data or not isinstance(data[0], str):
            raise ValueError("DSL nodes are nonempty JSON lists headed by an operator")
        op = data[0]
        variable_set = frozenset(variables)
        if op == "var" and len(data) == 2 and data[1] in variable_set:
            return Expr.variable(data[1])
        if op in {"zero", "one"} and len(data) == 1:
            return Expr(op)
        if op in {"xor", "and"} and len(data) == 3:
            return Expr.binary(
                op,
                Expr.from_data(data[1], variable_set),
                Expr.from_data(data[2], variable_set),
            )
        raise ValueError("malformed or untyped DSL expression")


def assignments(variables: tuple[str, ...]) -> tuple[dict[str, int], ...]:
    return tuple(
        dict(zip(variables, values)) for values in product((0, 1), repeat=len(variables))
    )


def signature(expression: Expr, variables: tuple[str, ...]) -> int:
    result = 0
    for index, environment in enumerate(assignments(variables)):
        result |= expression.evaluate(environment) << index
    return result


def expression_library(
    variables: tuple[str, ...], max_cost: int
) -> tuple[Expr, ...]:
    """Enumerate one smallest AST for every reached Boolean function."""

    if max_cost < 0 or not variables or len(set(variables)) != len(variables):
        raise ValueError("invalid grammar variables or cost")
    bases = (Expr.zero(), Expr.one(), *(Expr.variable(name) for name in variables))
    by_cost: list[list[Expr]] = [[] for _ in range(max_cost + 1)]
    best: dict[int, Expr] = {}
    for expression in bases:
        value = signature(expression, variables)
        if value not in best:
            best[value] = expression
            by_cost[0].append(expression)

    for cost in range(1, max_cost + 1):
        candidates: dict[int, Expr] = {}
        for left_cost in range(cost):
            right_cost = cost - 1 - left_cost
            for left in by_cost[left_cost]:
                for right in by_cost[right_cost]:
                    for op in ("xor", "and"):
                        expression = Expr.binary(op, left, right)
                        value = signature(expression, variables)
                        if value in best:
                            continue
                        previous = candidates.get(value)
                        if previous is None or expression.render() < previous.render():
                            candidates[value] = expression
        for value, expression in sorted(
            candidates.items(), key=lambda item: item[1].render()
        ):
            best[value] = expression
            by_cost[cost].append(expression)
    return tuple(best.values())


"""Measure an exact center-observational quotient with reduced BDDs.

For horizon h, let F_h map the 2h+1 input cells in a causal neighborhood to
the single center cell h steps later.  A reduced ordered binary decision
diagram (ROBDD) canonically merges input histories that have the same effect on
that one query.  This deliberately retains less information than an exact
spacetime tile.

The probe compares several variable orders and ECA controls.  Constructing an
ROBDD is not itself a shortcut; useful evidence would be polylogarithmic node
growth plus an exact dyadic way to construct the diagram without expanding all
intermediate cells.
"""

from __future__ import annotations

import argparse
import math
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass


class NodeLimitExceeded(RuntimeError):
    pass


class Robdd:
    ZERO = 0
    ONE = 1

    def __init__(self, max_nodes: int = 2_000_000) -> None:
        self.nodes: dict[int, tuple[int, int, int]] = {}
        self.unique: dict[tuple[int, int, int], int] = {}
        self.apply_cache: dict[tuple[str, int, int], int] = {}
        self.not_cache: dict[int, int] = {self.ZERO: self.ONE, self.ONE: self.ZERO}
        self.rule_cache: dict[tuple[int, int, int, int], int] = {}
        self.max_nodes = max_nodes

    def make(self, variable: int, low: int, high: int) -> int:
        if low == high:
            return low
        key = (variable, low, high)
        identifier = self.unique.get(key)
        if identifier is not None:
            return identifier
        if len(self.nodes) >= self.max_nodes:
            raise NodeLimitExceeded(f"ROBDD exceeded {self.max_nodes} nonterminal nodes")
        identifier = len(self.nodes) + 2
        self.nodes[identifier] = key
        self.unique[key] = identifier
        return identifier

    def variable(self, rank: int) -> int:
        return self.make(rank, self.ZERO, self.ONE)

    def negate(self, node: int) -> int:
        cached = self.not_cache.get(node)
        if cached is not None:
            return cached
        variable, low, high = self.nodes[node]
        result = self.make(variable, self.negate(low), self.negate(high))
        self.not_cache[node] = result
        self.not_cache[result] = node
        return result

    def apply(self, operation: str, left: int, right: int) -> int:
        if operation not in ("and", "or", "xor"):
            raise ValueError("unsupported Boolean operation")
        if left > right:
            left, right = right, left
        if operation == "and":
            if left == self.ZERO or right == self.ZERO:
                return self.ZERO
            if left == self.ONE:
                return right
            if left == right:
                return left
        elif operation == "or":
            if left == self.ZERO:
                return right
            if right == self.ONE:
                return self.ONE
            if left == right:
                return left
        else:
            if left == self.ZERO:
                return right
            if left == right:
                return self.ZERO
            if right == self.ONE:
                return self.negate(left)
        key = (operation, left, right)
        cached = self.apply_cache.get(key)
        if cached is not None:
            return cached
        left_variable = self.nodes[left][0] if left >= 2 else math.inf
        right_variable = self.nodes[right][0] if right >= 2 else math.inf
        top = int(min(left_variable, right_variable))
        left_low, left_high = (
            self.nodes[left][1:] if left_variable == top else (left, left)
        )
        right_low, right_high = (
            self.nodes[right][1:] if right_variable == top else (right, right)
        )
        result = self.make(
            top,
            self.apply(operation, left_low, right_low),
            self.apply(operation, left_high, right_high),
        )
        self.apply_cache[key] = result
        return result

    def eca(self, rule: int, left: int, center: int, right: int) -> int:
        key = (rule, left, center, right)
        cached = self.rule_cache.get(key)
        if cached is not None:
            return cached
        if rule == 30:
            result = self.apply("xor", left, self.apply("or", center, right))
        elif rule == 90:
            result = self.apply("xor", left, right)
        else:
            result = self.ZERO
            for neighborhood in range(8):
                if not (rule >> neighborhood) & 1:
                    continue
                term = self.ONE
                for node, flag in ((left, 4), (center, 2), (right, 1)):
                    literal = node if neighborhood & flag else self.negate(node)
                    term = self.apply("and", term, literal)
                result = self.apply("or", result, term)
        self.rule_cache[key] = result
        return result

    def reachable_nodes(self, root: int) -> int:
        return sum(self.reachable_profile(root).values())

    def reachable_profile(self, root: int) -> dict[int, int]:
        pending = [root]
        seen: set[int] = set()
        while pending:
            node = pending.pop()
            if node < 2 or node in seen:
                continue
            seen.add(node)
            _, low, high = self.nodes[node]
            pending.extend((low, high))
        profile: dict[int, int] = {}
        for node in seen:
            variable = self.nodes[node][0]
            profile[variable] = profile.get(variable, 0) + 1
        return profile

    def evaluate(self, root: int, assignment: Mapping[int, int]) -> int:
        node = root
        while node >= 2:
            variable, low, high = self.nodes[node]
            node = high if assignment[variable] else low
        return node


VARIABLE_ORDERS = ("left_to_right", "right_to_left", "center_out", "outside_in", "bit_reversal")


def variable_ranks(horizon: int, order: str) -> dict[int, int]:
    positions = list(range(-horizon, horizon + 1))
    if order == "left_to_right":
        ordered = positions
    elif order == "right_to_left":
        ordered = list(reversed(positions))
    elif order == "center_out":
        ordered = sorted(positions, key=lambda position: (abs(position), position > 0))
    elif order == "outside_in":
        ordered = sorted(positions, key=lambda position: (-abs(position), position > 0))
    elif order == "bit_reversal":
        bits = max(1, (len(positions) - 1).bit_length())

        def reverse(index: int) -> int:
            value = 0
            for _ in range(bits):
                value = (value << 1) | (index & 1)
                index >>= 1
            return value

        ordered = [position for _, position in sorted((reverse(i), p) for i, p in enumerate(positions))]
    else:
        raise ValueError(f"unknown variable order: {order}")
    return {position: rank for rank, position in enumerate(ordered)}


@dataclass(frozen=True)
class CenterFunction:
    rule: int
    horizon: int
    order: str
    root: int
    reachable_nodes: int
    maximum_width: int
    allocated_nodes: int
    diagram: Robdd
    ranks: dict[int, int]


def build_center_function(
    rule: int, horizon: int, order: str, max_nodes: int = 2_000_000
) -> CenterFunction:
    if not 0 <= rule <= 255 or horizon < 1:
        raise ValueError("invalid ECA rule or horizon")
    ranks = variable_ranks(horizon, order)
    diagram = Robdd(max_nodes)
    row = [diagram.variable(ranks[position]) for position in range(-horizon, horizon + 1)]
    for _ in range(horizon):
        row = [diagram.eca(rule, row[index], row[index + 1], row[index + 2]) for index in range(len(row) - 2)]
    root = row[0]
    profile = diagram.reachable_profile(root)
    return CenterFunction(
        rule,
        horizon,
        order,
        root,
        sum(profile.values()),
        max(profile.values(), default=0),
        len(diagram.nodes),
        diagram,
        ranks,
    )


def direct_center(rule: int, horizon: int, inputs: Mapping[int, int]) -> int:
    row = [inputs[position] for position in range(-horizon, horizon + 1)]
    for _ in range(horizon):
        row = [
            (rule >> (4 * row[index] + 2 * row[index + 1] + row[index + 2])) & 1
            for index in range(len(row) - 2)
        ]
    return row[0]


def fit_growth(points: Sequence[tuple[int, int]], x_transform: Callable[[int], float]) -> float:
    xs = [x_transform(horizon) for horizon, _ in points]
    ys = [math.log(nodes) for _, nodes in points]
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    denominator = sum((x - mean_x) ** 2 for x in xs)
    return sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / denominator


def report(rules: Sequence[int], horizons: Sequence[int], orders: Sequence[str], max_nodes: int) -> None:
    measurements: dict[tuple[int, str], list[tuple[int, int]]] = {}
    print("rule horizon order reachable_nodes maximum_width allocated_nodes status")
    for rule in rules:
        for order in orders:
            points: list[tuple[int, int]] = []
            measurements[(rule, order)] = points
            for horizon in horizons:
                try:
                    result = build_center_function(rule, horizon, order, max_nodes)
                except NodeLimitExceeded:
                    print(
                        f"{rule:4d} {horizon:7d} {order:14s} {max_nodes:15d} "
                        f"{max_nodes:13d} {max_nodes:15d} LIMIT"
                    )
                    break
                points.append((horizon, result.reachable_nodes))
                print(
                    f"{rule:4d} {horizon:7d} {order:14s} {result.reachable_nodes:15d} "
                    f"{result.maximum_width:13d} {result.allocated_nodes:15d} OK"
                )
    print("\nrule order power_exponent exponential_base")
    for (rule, order), points in measurements.items():
        if len(points) < 2:
            continue
        power = fit_growth(points, math.log)
        exponential_base = math.exp(fit_growth(points, float))
        print(f"{rule:4d} {order:14s} {power:14.6f} {exponential_base:16.6f}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rules", nargs="+", type=int, default=[90, 22, 30, 110])
    parser.add_argument("--horizons", nargs="+", type=int, default=[2, 4, 6, 8, 10, 12, 14, 16])
    parser.add_argument("--orders", nargs="+", choices=VARIABLE_ORDERS, default=list(VARIABLE_ORDERS))
    parser.add_argument("--max-nodes", type=int, default=2_000_000)
    args = parser.parse_args()
    if any(not 0 <= rule <= 255 for rule in args.rules):
        parser.error("rules must be ECA numbers in [0, 255]")
    if any(horizon < 1 for horizon in args.horizons):
        parser.error("horizons must be positive")
    if args.max_nodes < 1:
        parser.error("max-nodes must be positive")
    report(args.rules, sorted(set(args.horizons)), args.orders, args.max_nodes)


if __name__ == "__main__":
    main()

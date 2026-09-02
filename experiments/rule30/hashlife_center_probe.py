"""Exact one-dimensional Hashlife probe for the Rule 30 center cell.

A level-k node represents a row block of length ``2**k``.  ``advance(node)``
returns its centered half after ``2**(k-2)`` generations.  Equal reachable row
blocks are hash-consed, and equal time-jump calls are memoized.  Thus the probe
does not first construct the spacetime triangle; its work statistic is the
number of distinct reachable time-jump calls needed for one center query.

This is an algorithmic falsifier for P3, not a lower-bound instrument.  A
sublinear all-scale bound on cache misses, together with an arbitrary-n wrapper
and a Turing-machine cost analysis, would give a negative answer to P3.  A
finite superlinear fit proves no lower bound and closes only this literal
Hashlife representation at the measured scales.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass


class Node:
    __slots__ = ("level", "left", "right", "identifier")

    def __init__(
        self,
        level: int,
        left: Node | None,
        right: Node | None,
        identifier: int,
    ) -> None:
        self.level = level
        self.left = left
        self.right = right
        self.identifier = identifier


@dataclass(frozen=True)
class QueryRecord:
    rule: int
    time: int
    center: int
    advance_cache_misses: int
    interned_nonleaf_nodes: int


class Hashlife1D:
    """Hash-consed centered time jumps for an elementary cellular automaton."""

    def __init__(self, rule: int) -> None:
        if not 0 <= rule < 256:
            raise ValueError("an elementary rule must be in [0, 255]")
        self.rule = rule
        self.leaves = (
            Node(0, None, None, 0),
            Node(0, None, None, 1),
        )
        self._next_identifier = 2
        self._intern: dict[tuple[int, int], Node] = {}
        self._advance_cache: dict[int, Node] = {}
        self._zero_nodes = [self.leaves[0]]

    def join(self, left: Node, right: Node) -> Node:
        if left.level != right.level:
            raise ValueError("children must have the same level")
        key = (left.identifier, right.identifier)
        found = self._intern.get(key)
        if found is None:
            found = Node(
                left.level + 1,
                left,
                right,
                self._next_identifier,
            )
            self._next_identifier += 1
            self._intern[key] = found
        return found

    def zero(self, level: int) -> Node:
        while len(self._zero_nodes) <= level:
            previous = self._zero_nodes[-1]
            self._zero_nodes.append(self.join(previous, previous))
        return self._zero_nodes[level]

    def set_bit(self, node: Node, index: int) -> Node:
        if not 0 <= index < (1 << node.level):
            raise IndexError(index)
        if node.level == 0:
            return self.leaves[1]
        assert node.left is not None and node.right is not None
        half = 1 << (node.level - 1)
        if index < half:
            return self.join(self.set_bit(node.left, index), node.right)
        return self.join(node.left, self.set_bit(node.right, index - half))

    def bit_at(self, node: Node, index: int) -> int:
        if not 0 <= index < (1 << node.level):
            raise IndexError(index)
        while node.level:
            assert node.left is not None and node.right is not None
            half = 1 << (node.level - 1)
            if index < half:
                node = node.left
            else:
                index -= half
                node = node.right
        return node.identifier

    def bits(self, node: Node) -> list[int]:
        return [self.bit_at(node, index) for index in range(1 << node.level)]

    def local(self, left: int, center: int, right: int) -> int:
        neighborhood = 4 * left + 2 * center + right
        return (self.rule >> neighborhood) & 1

    def advance(self, node: Node) -> Node:
        """Return the centered half after ``2**(level-2)`` generations."""

        if node.level < 2:
            raise ValueError("advance requires a node of level at least two")
        cached = self._advance_cache.get(node.identifier)
        if cached is not None:
            return cached

        assert node.left is not None and node.right is not None
        if node.level == 2:
            assert node.left.left is not None and node.left.right is not None
            assert node.right.left is not None and node.right.right is not None
            a = node.left.left.identifier
            b = node.left.right.identifier
            c = node.right.left.identifier
            d = node.right.right.identifier
            result = self.join(
                self.leaves[self.local(a, b, c)],
                self.leaves[self.local(b, c, d)],
            )
        else:
            assert node.left.left is not None and node.left.right is not None
            assert node.right.left is not None and node.right.right is not None
            a, b = node.left.left, node.left.right
            c, d = node.right.left, node.right.right

            first = self.advance(self.join(a, b))
            middle = self.advance(self.join(b, c))
            last = self.advance(self.join(c, d))
            result = self.join(
                self.advance(self.join(first, middle)),
                self.advance(self.join(middle, last)),
            )

        self._advance_cache[node.identifier] = result
        return result

    @property
    def advance_cache_misses(self) -> int:
        return len(self._advance_cache)

    @property
    def interned_nonleaf_nodes(self) -> int:
        return len(self._intern)


def query_power_of_two(rule: int, time: int) -> QueryRecord:
    if time < 1 or time & (time - 1):
        raise ValueError("time must be a positive power of two")
    exponent = time.bit_length() - 1
    engine = Hashlife1D(rule)

    # A length-4t zero block has enough margin for t generations.  Its seed is
    # at position 2t.  advance returns original positions [t,3t), so the same
    # spatial center is output position t.
    root = engine.set_bit(engine.zero(exponent + 2), 2 * time)
    future = engine.advance(root)
    center = engine.bit_at(future, time)
    return QueryRecord(
        rule=rule,
        time=time,
        center=center,
        advance_cache_misses=engine.advance_cache_misses,
        interned_nonleaf_nodes=engine.interned_nonleaf_nodes,
    )


def fitted_exponent(records: list[QueryRecord]) -> float:
    if len(records) < 2:
        raise ValueError("need at least two records for a fit")
    xs = [math.log2(row.time) for row in records]
    ys = [math.log2(row.advance_cache_misses) for row in records]
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    denominator = sum((x - x_mean) ** 2 for x in xs)
    return numerator / denominator


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rules", type=int, nargs="+", default=[90, 30])
    parser.add_argument("--min-k", type=int, default=4)
    parser.add_argument("--max-k", type=int, default=12)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.min_k < 0 or args.max_k < args.min_k:
        parser.error("require 0 <= min-k <= max-k")

    report = {}
    for rule in args.rules:
        found = [query_power_of_two(rule, 1 << k) for k in range(args.min_k, args.max_k + 1)]
        report[str(rule)] = {
            "records": [asdict(row) for row in found],
            "fitted_cache_miss_exponent": fitted_exponent(found),
        }

    if args.json:
        print(json.dumps(report, indent=2))
        return
    for rule in args.rules:
        item = report[str(rule)]
        print(f"## rule {rule}")
        print("time center advance_cache_misses interned_nonleaf_nodes")
        for row in item["records"]:
            print(
                f"{row['time']:8d} {row['center']:6d} "
                f"{row['advance_cache_misses']:20d} "
                f"{row['interned_nonleaf_nodes']:22d}"
            )
        print(f"fitted exponent: {item['fitted_cache_miss_exponent']:.6f}")


if __name__ == "__main__":
    main()

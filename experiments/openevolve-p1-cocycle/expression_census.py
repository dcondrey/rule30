#!/usr/bin/env python3
"""Deterministic short-expression census for plateau-delay conjectures.

This is a finite discovery tool, not a proof procedure.  It enumerates raw
features, small quotients/residues, pairwise sums/products/minima/maxima, and
small positive weighted sums, then asks whether one or two such expressions
strictly order every recorded plateau edge lexicographically.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable


HERE = Path(__file__).resolve().parent


def load_edges() -> tuple[list[str], list[dict[str, int]], list[tuple[int, int, int, int]]]:
    data = json.loads((HERE / "cocycle_features.json").read_text())
    chains = list(data["chains"])
    external = HERE / "cocycle_features_n18.json"
    if external.exists():
        chains.append(json.loads(external.read_text())["chain"])
    states: list[dict[str, int]] = []
    edges: list[tuple[int, int, int, int]] = []
    for chain in chains:
        for edge in chain["edges"]:
            if edge["kind"] != "plateau":
                continue
            left = len(states)
            states.append(chain["states"][edge["from"]]["features"])
            right = len(states)
            states.append(chain["states"][edge["to"]]["features"])
            edges.append((left, right, chain["width"], edge["from"]))
    return data["feature_names"], states, edges


def expression_library(
    names: list[str], states: list[dict[str, int]], *, allow_mod: bool
) -> dict[tuple[int, ...], str]:
    base = {name: tuple(state[name] for state in states) for name in names}
    expressions: dict[tuple[int, ...], str] = {}

    def add(label: str, values: tuple[int, ...]) -> None:
        if max(values, default=0) <= 10**18:
            expressions.setdefault(values, label)

    for name, values in base.items():
        add(f'state["{name}"]', values)
        for constant in range(2, 17):
            add(
                f'state["{name}"] // {constant}',
                tuple(value // constant for value in values),
            )
            if allow_mod:
                add(
                    f'state["{name}"] % {constant}',
                    tuple(value % constant for value in values),
                )

    pair_ops: tuple[tuple[str, Callable[[int, int], int]], ...] = (
        ("+", lambda x, y: x + y),
        ("*", lambda x, y: x * y),
        ("min", min),
        ("max", max),
    )
    for index, left_name in enumerate(names):
        left = base[left_name]
        for right_name in names[index:]:
            right = base[right_name]
            for operation, function in pair_ops:
                if operation in {"min", "max"}:
                    label = (
                        f'{operation}(state["{left_name}"], '
                        f'state["{right_name}"])'
                    )
                else:
                    label = (
                        f'state["{left_name}"] {operation} '
                        f'state["{right_name}"]'
                    )
                add(label, tuple(function(x, y) for x, y in zip(left, right)))
            for left_coefficient, right_coefficient in (
                (1, 2), (1, 3), (1, 4), (2, 1), (3, 1), (4, 1)
            ):
                add(
                    f'{left_coefficient} * state["{left_name}"] + '
                    f'{right_coefficient} * state["{right_name}"]',
                    tuple(
                        left_coefficient * x + right_coefficient * y
                        for x, y in zip(left, right)
                    ),
                )
    return expressions


def comparisons(
    values: tuple[int, ...], edges: list[tuple[int, int, int, int]]
) -> tuple[int, ...]:
    return tuple(
        (values[left] > values[right]) - (values[left] < values[right])
        for left, right, _, _ in edges
    )


def find_lex_pair(
    expressions: dict[tuple[int, ...], str],
    edges: list[tuple[int, int, int, int]],
) -> tuple[str, ...] | None:
    candidates = []
    for values, label in expressions.items():
        signs = comparisons(values, edges)
        if any(sign < 0 for sign in signs):
            continue
        if all(sign > 0 for sign in signs):
            return (label,)
        resolved = sum(sign > 0 for sign in signs)
        if resolved:
            candidates.append((-resolved, len(label), label, signs))

    second_signs = [
        (len(label), label, comparisons(values, edges))
        for values, label in expressions.items()
    ]
    for _, __, first_label, first in sorted(candidates):
        unresolved = tuple(index for index, sign in enumerate(first) if sign == 0)
        for _, second_label, second in sorted(second_signs):
            if all(second[index] > 0 for index in unresolved):
                return first_label, second_label
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-mod", action="store_true")
    args = parser.parse_args()
    names, states, edges = load_edges()
    expressions = expression_library(names, states, allow_mod=not args.no_mod)
    answer = find_lex_pair(expressions, edges)
    print(f"plateau edges: {[(width, offset) for _, _, width, offset in edges]}")
    print(f"unique expressions: {len(expressions)}")
    print(f"lexicographic pair: {answer}")


if __name__ == "__main__":
    main()

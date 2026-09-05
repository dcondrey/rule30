#!/usr/bin/env python3
"""Audit a right-language-aware two-coordinate zero-prefix certificate.

The actual alternating-center right trace uniformly avoids five consecutive
zero bits.  In endpoint symbols this means that an actual-right source block
has no factor ``22222``.  This audit combines that proved restriction with a
smaller zero-prefix affine selector:

* tail 2 uses only ``(alpha,beta)`` and sources avoiding ``22222``;
* tail 3 uses only ``(alpha,gamma)`` on the full hard-core language.

The experiment is a bounded falsifier for the corresponding greedy lemma.
It is not an all-length proof.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

from constant_tail_bitsliced_derivative import (
    bitsliced_trace_states,
    scenario_state,
)
from constant_tail_scale import Vector, hard_core_extension_length
from constant_tail_zero_prefix_bitsliced import (
    adjacent_scenarios_differ,
    zero_prefix_word_states,
)
from constant_tail_zero_prefix_matching import greedy_matching
from rank_zero_separator import hard_core_prefixes


SELECTED_COORDINATES = {2: (0, 1), 3: (0, 2)}


def source_allowed(word: Vector, tail: int) -> bool:
    """Apply only the proved actual-right restriction needed by tail 2."""

    return tail == 3 or all(
        word[index : index + 5] != (2, 2, 2, 2, 2)
        for index in range(max(0, len(word) - 4))
    )


def selected_graph(word: Vector, tail: int) -> tuple[dict[int, set[int]], int]:
    states, mask = zero_prefix_word_states(word)
    extension, affines = bitsliced_trace_states(
        states, len(word), tail, mask
    )
    original = tuple(scenario_state(state, 0) for state in extension)
    survival = hard_core_extension_length(word, original)
    coordinates = SELECTED_COORDINATES[tail]
    graph = {
        step: {
            token
            for token in range(len(word))
            if any(
                adjacent_scenarios_differ(affines[step][coordinate], token)
                for coordinate in coordinates
            )
        }
        for step in range(survival)
    }
    return graph, survival


@dataclass(slots=True)
class Census:
    cases: int = 0
    failures: int = 0
    deadline_failures: int = 0
    minimum_deadline_slack: int = 10**9
    first_failure: str | None = None
    first_deadline_failure: str | None = None
    diagonal_failures: int = 0
    first_diagonal_failure: str | None = None


def audit_word(word: Vector, tail: int, census: Census) -> None:
    graph, survival = selected_graph(word, tail)
    pairs = greedy_matching(graph)
    required = survival if tail == 2 else max(0, survival - 1)
    description = (
        f"tail={tail} W={''.join(map(str, word))} n={len(word)} "
        f"s={survival} required={required} pairs={sorted(pairs.items())}"
    )
    census.cases += 1
    if len(pairs) < required:
        census.failures += 1
        if census.first_failure is None:
            census.first_failure = description

    for step in range(required):
        if not any(token >= step for token in graph[step]):
            census.diagonal_failures += 1
            if census.first_diagonal_failure is None:
                census.first_diagonal_failure = (
                    f"{description} step={step} edges={sorted(graph[step])}"
                )

    for step in range(required):
        if step not in pairs:
            continue
        deadline = len(word) - required + step
        slack = deadline - pairs[step]
        census.minimum_deadline_slack = min(
            census.minimum_deadline_slack, slack
        )
        if slack < 0:
            census.deadline_failures += 1
            if census.first_deadline_failure is None:
                census.first_deadline_failure = (
                    f"{description} step={step} token={pairs[step]} "
                    f"deadline={deadline}"
                )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-length", type=int, default=22)
    parser.add_argument("--first-length", type=int, default=1)
    parser.add_argument("--random-per-length", type=int, default=0)
    parser.add_argument("--unrestricted-tail2", action="store_true")
    parser.add_argument("--only-tail2-with-22222", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.first_length <= args.max_length:
        parser.error("length bounds must satisfy 1 <= first <= max")

    census = Census()
    for length in range(args.first_length, args.max_length + 1):
        before = (
            census.cases,
            census.failures,
            census.deadline_failures,
            census.diagonal_failures,
        )
        for word in hard_core_prefixes(length):
            for tail in (2, 3):
                if args.only_tail2_with_22222:
                    allowed = tail == 2 and not source_allowed(word, tail)
                else:
                    allowed = args.unrestricted_tail2 or source_allowed(
                        word, tail
                    )
                if allowed:
                    audit_word(word, tail, census)
        print(
            f"length={length:2d} cases={census.cases-before[0]:6d} "
            f"failures={census.failures-before[1]:4d} "
            f"deadline-failures={census.deadline_failures-before[2]:4d} "
            f"diagonal-failures={census.diagonal_failures-before[3]:4d}"
        )

    generator = random.Random(30030)

    def random_word(length: int) -> Vector:
        word = []
        for _ in range(length):
            word.append(
                2 if word and word[-1] == 1 else generator.choice((1, 2))
            )
        return tuple(word)

    for length in (24, 32, 48, 64):
        before = census.diagonal_failures
        for _ in range(args.random_per_length):
            value = random_word(length)
            audit_word(value, 3, census)
            value = random_word(length)
            while not source_allowed(value, 2):
                value = random_word(length)
            audit_word(value, 2, census)
        print(
            f"random-length={length:2d} requested={args.random_per_length:5d} "
            f"diagonal-failures={census.diagonal_failures-before:4d}"
        )

    print(
        f"TOTAL cases={census.cases} failures={census.failures} "
        f"deadline-failures={census.deadline_failures} "
        f"diagonal-failures={census.diagonal_failures} "
        f"minimum-deadline-slack={census.minimum_deadline_slack}"
    )
    print(f"first failure: {census.first_failure or 'none'}")
    print(
        "first deadline failure: "
        f"{census.first_deadline_failure or 'none'}"
    )
    print(
        "first diagonal failure: "
        f"{census.first_diagonal_failure or 'none'}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Held-out bit-sliced validation of left-to-right cumulative matching."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from constant_tail_bitsliced_derivative import (
    BitAffine,
    BitState,
    bitsliced_trace_states,
    scenario_state,
)
from constant_tail_cumulative_matching import cumulative_graph
from constant_tail_ordered_matching import (
    correction_count,
    maximum_matching,
    maximum_ordered_real_matching,
)
from constant_tail_scale import Vector, hard_core_extension_length
from rank_zero_separator import hard_core_prefixes


def cumulative_word_states(
    word: Vector, direction: str
) -> tuple[list[BitState], tuple[int, ...], int]:
    sources = [index for index, value in enumerate(word) if value == 2]
    if direction == "right-to-left":
        sources.reverse()
    elif direction != "left-to-right":
        raise ValueError(direction)
    token_of_source = {source: token for token, source in enumerate(sources)}
    mask = (1 << (len(sources) + 1)) - 1
    states = []
    for index, value in enumerate(word):
        if value == 1:
            states.append((0, mask))
        else:
            token = token_of_source[index]
            # Scenario k has flipped tokens 0,...,k-1.  This source remains
            # state 2 in scenarios 0,...,token and is state 1 thereafter.
            high = (1 << (token + 1)) - 1
            states.append((high, mask ^ high))
    return states, tuple(sources), mask


def adjacent_scenarios_differ(bits: int, token: int) -> bool:
    return ((bits >> token) ^ (bits >> (token + 1))) & 1 == 1


def cumulative_bitsliced_graph(
    word: Vector, tail: int, direction: str
) -> tuple[dict[int, set[int]], int, tuple[int, ...]]:
    word_states, sources, mask = cumulative_word_states(word, direction)
    extension, affines = bitsliced_trace_states(
        word_states, len(word), tail, mask
    )
    original_extension = tuple(scenario_state(state, 0) for state in extension)
    survival = hard_core_extension_length(word, original_extension)
    graph = {step: set() for step in range(survival)}
    for step in range(survival):
        affine: BitAffine = affines[step]
        value = extension[step]
        for token in range(len(sources)):
            if (
                any(adjacent_scenarios_differ(bits, token) for bits in affine)
                or adjacent_scenarios_differ(value[0], token)
                or adjacent_scenarios_differ(value[1], token)
            ):
                graph[step].add(token)
    return graph, survival, sources


def slow_controls(max_length: int) -> int:
    checked = 0
    for length in range(1, max_length + 1):
        for word in hard_core_prefixes(length):
            for tail in (2, 3):
                for direction in ("left-to-right", "right-to-left"):
                    fast = cumulative_bitsliced_graph(word, tail, direction)
                    slow = cumulative_graph(word, tail, direction)
                    assert fast == slow
                    checked += sum(len(neighbors) for neighbors in fast[0].values())
    return checked


@dataclass(slots=True)
class Census:
    cases: int = 0
    ordinary_failures: int = 0
    ordered_failures: int = 0
    first_ordinary: str | None = None
    first_ordered: str | None = None
    greedy_failures: int = 0
    first_greedy: str | None = None


def greedy_matching(graph: dict[int, set[int]]) -> dict[int, int]:
    """Match each step to its least available later token, without backtracking."""

    last = -1
    answer = {}
    for step in sorted(graph):
        candidates = [token for token in graph[step] if token > last]
        if not candidates:
            continue
        token = min(candidates)
        assert token > last and token in graph[step]
        answer[step] = token
        last = token
    assert tuple(answer.values()) == tuple(sorted(answer.values()))
    return answer


def audit_word(
    word: Vector, tail: int, census: Census
) -> tuple[int, int, int, int]:
    graph, survival, _ = cumulative_bitsliced_graph(
        word, tail, "left-to-right"
    )
    credits = correction_count(word, tail)
    ordinary = len(maximum_matching(graph, credits))
    ordered = maximum_ordered_real_matching(graph) + credits
    greedy = len(greedy_matching(graph)) + credits
    description = (
        f"tail={tail} W={''.join(map(str, word))} s={survival} "
        f"#2={word.count(2)} credits={credits} "
        f"ordinary={ordinary} ordered={ordered} greedy={greedy}"
    )
    census.cases += 1
    if ordinary < survival:
        census.ordinary_failures += 1
        if census.first_ordinary is None:
            census.first_ordinary = description
    if ordered < survival:
        census.ordered_failures += 1
        if census.first_ordered is None:
            census.first_ordered = description
    if greedy < survival:
        census.greedy_failures += 1
        if census.first_greedy is None:
            census.first_greedy = description
    return survival, ordinary, ordered, greedy


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--control-length", type=int, default=7)
    parser.add_argument("--first-length", type=int, default=17)
    parser.add_argument("--last-length", type=int, default=22)
    args = parser.parse_args()
    if not (0 <= args.control_length and 1 <= args.first_length <= args.last_length):
        parser.error("invalid length bounds")

    controls = slow_controls(args.control_length)
    print(f"slow/bit-sliced cumulative controls: {controls} edges PASS")

    census = Census()
    for length in range(args.first_length, args.last_length + 1):
        before_cases = census.cases
        before_ordinary = census.ordinary_failures
        before_ordered = census.ordered_failures
        before_greedy = census.greedy_failures
        for word in hard_core_prefixes(length):
            for tail in (2, 3):
                audit_word(word, tail, census)
        print(
            f"length={length:2d} cases={census.cases-before_cases:6d} "
            f"ordinary-failures="
            f"{census.ordinary_failures-before_ordinary:4d} "
            f"ordered-failures={census.ordered_failures-before_ordered:4d} "
            f"greedy-failures={census.greedy_failures-before_greedy:4d}"
        )

    specials = (
        ("repair", tuple(map(int, "12212121212121212")), 2),
        ("derivative adversary", tuple(map(int, "122212222222221212122")), 2),
    )
    for label, word, tail in specials:
        survival, ordinary, ordered, greedy = audit_word(word, tail, census)
        print(
            f"special={label} survival={survival} "
            f"ordinary={ordinary} ordered={ordered} greedy={greedy}"
        )

    print(
        f"TOTAL cases={census.cases} "
        f"ordinary-failures={census.ordinary_failures} "
        f"ordered-failures={census.ordered_failures} "
        f"greedy-failures={census.greedy_failures}"
    )
    print(f"first ordinary: {census.first_ordinary or 'none'}")
    print(f"first ordered: {census.first_ordered or 'none'}")
    print(f"first greedy: {census.first_greedy or 'none'}")


if __name__ == "__main__":
    main()

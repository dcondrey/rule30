#!/usr/bin/env python3
"""Held-out bit-sliced validation of zero-prefix scale matching."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from constant_tail_bitsliced_derivative import (
    BitAffine,
    BitState,
    bitsliced_trace_states,
    scenario_state,
)
from constant_tail_cumulative_matrix import ordered_pairs
from constant_tail_ordered_matching import maximum_matching
from constant_tail_scale import Vector, hard_core_extension_length
from constant_tail_zero_prefix_matching import (
    correction,
    greedy_matching,
    zero_prefix_graph,
)
from rank_zero_separator import hard_core_prefixes


def zero_prefix_word_states(word: Vector) -> tuple[list[BitState], int]:
    mask = (1 << (len(word) + 1)) - 1
    states = []
    for index, value in enumerate(word):
        present = (1 << (index + 1)) - 1
        states.append(
            (
                present if value >> 1 else 0,
                present if value & 1 else 0,
            )
        )
    return states, mask


def adjacent_scenarios_differ(bits: int, token: int) -> bool:
    return ((bits >> token) ^ (bits >> (token + 1))) & 1 == 1


def zero_prefix_bitsliced_graph(
    word: Vector, tail: int
) -> tuple[dict[int, set[int]], int]:
    states, mask = zero_prefix_word_states(word)
    extension, affines = bitsliced_trace_states(states, len(word), tail, mask)
    original_extension = tuple(scenario_state(state, 0) for state in extension)
    survival = hard_core_extension_length(word, original_extension)
    graph = {step: set() for step in range(survival)}
    for step in range(survival):
        affine: BitAffine = affines[step]
        value = extension[step]
        for token in range(len(word)):
            if (
                any(adjacent_scenarios_differ(bits, token) for bits in affine)
                or adjacent_scenarios_differ(value[0], token)
                or adjacent_scenarios_differ(value[1], token)
            ):
                graph[step].add(token)
    return graph, survival


def slow_controls(max_length: int) -> int:
    checked = 0
    for length in range(1, max_length + 1):
        for word in hard_core_prefixes(length):
            for tail in (2, 3):
                fast = zero_prefix_bitsliced_graph(word, tail)
                slow = zero_prefix_graph(word, tail)
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
    nonfinal_miss_failures: int = 0
    first_nonfinal_miss: str | None = None


def audit_word(
    word: Vector, tail: int, census: Census
) -> tuple[int, int, int, int]:
    graph, survival = zero_prefix_bitsliced_graph(word, tail)
    budget = correction(tail)
    ordinary = len(maximum_matching(graph, budget))
    ordered = len(ordered_pairs(graph)) + budget
    greedy_pairs = greedy_matching(graph)
    greedy = len(greedy_pairs) + budget
    description = (
        f"tail={tail} W={''.join(map(str, word))} s={survival} "
        f"n={len(word)} K={budget} ordinary={ordinary} ordered={ordered} "
        f"greedy={greedy}"
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
    nonfinal_misses = [
        step
        for step in range(max(0, survival - 1))
        if step not in greedy_pairs
    ]
    if nonfinal_misses:
        census.nonfinal_miss_failures += 1
        if census.first_nonfinal_miss is None:
            census.first_nonfinal_miss = (
                f"{description} nonfinal-misses={nonfinal_misses}"
            )
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
    print(f"slow/bit-sliced zero-prefix controls: {controls} edges PASS")
    census = Census()
    for length in range(args.first_length, args.last_length + 1):
        before_cases = census.cases
        before_ordinary = census.ordinary_failures
        before_ordered = census.ordered_failures
        before_greedy = census.greedy_failures
        before_nonfinal = census.nonfinal_miss_failures
        for word in hard_core_prefixes(length):
            for tail in (2, 3):
                audit_word(word, tail, census)
        print(
            f"length={length:2d} cases={census.cases-before_cases:6d} "
            f"ordinary-failures="
            f"{census.ordinary_failures-before_ordinary:4d} "
            f"ordered-failures={census.ordered_failures-before_ordered:4d} "
            f"greedy-failures={census.greedy_failures-before_greedy:4d} "
            f"nonfinal-miss-failures="
            f"{census.nonfinal_miss_failures-before_nonfinal:4d}"
        )

    specials = (
        ("tail-3 sharp", (1, 2, 1), 3),
        ("tail-2 repair", tuple(map(int, "12212121212121212")), 2),
        (
            "derivative adversary",
            tuple(map(int, "122212222222221212122")),
            2,
        ),
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
        f"greedy-failures={census.greedy_failures} "
        f"nonfinal-miss-failures={census.nonfinal_miss_failures}"
    )
    print(f"first ordinary: {census.first_ordinary or 'none'}")
    print(f"first ordered: {census.first_ordered or 'none'}")
    print(f"first greedy: {census.first_greedy or 'none'}")
    print(
        f"first nonfinal miss: {census.first_nonfinal_miss or 'none'}"
    )


if __name__ == "__main__":
    main()

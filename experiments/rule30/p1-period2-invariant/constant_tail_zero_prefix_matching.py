#!/usr/bin/env python3
"""Test zero-prefix telescoping certificates for coarse scale bounds."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from constant_tail_cumulative_matrix import ordered_pairs
from constant_tail_ordered_matching import forced_trace, maximum_matching
from constant_tail_scale import Vector, hard_core_extension_length
from rank_zero_separator import hard_core_prefixes


def zero_prefix_graph(
    word: Vector, tail: int
) -> tuple[dict[int, set[int]], int]:
    extension, previous_trace = forced_trace(word, tail)
    survival = hard_core_extension_length(word, extension)
    graph = {step: set() for step in range(survival)}
    current = list(word)
    for token in range(len(word)):
        current[token] = 0
        _, following_trace = forced_trace(tuple(current), tail)
        for step in range(survival):
            if (
                previous_trace[step].affine != following_trace[step].affine
                or previous_trace[step].forced != following_trace[step].forced
            ):
                graph[step].add(token)
        previous_trace = following_trace
    return graph, survival


def correction(tail: int) -> int:
    return int(tail == 3)


@dataclass(slots=True)
class Audit:
    cases: int = 0
    ordinary_failures: int = 0
    ordered_failures: int = 0
    first_ordinary: str | None = None
    first_ordered: str | None = None
    greedy_failures: int = 0
    first_greedy: str | None = None


def greedy_matching(graph: dict[int, set[int]]) -> dict[int, int]:
    last = -1
    answer = {}
    for step in sorted(graph):
        candidates = [token for token in graph[step] if token > last]
        if not candidates:
            continue
        token = min(candidates)
        assert token in graph[step] and token > last
        answer[step] = token
        last = token
    assert tuple(answer.values()) == tuple(sorted(answer.values()))
    return answer


def audit_word(
    word: Vector, tail: int, audit: Audit
) -> tuple[int, int, int, int]:
    graph, survival = zero_prefix_graph(word, tail)
    ordinary = len(maximum_matching(graph, correction(tail)))
    ordered = len(ordered_pairs(graph)) + correction(tail)
    greedy = len(greedy_matching(graph)) + correction(tail)
    description = (
        f"tail={tail} W={''.join(map(str, word))} s={survival} n={len(word)} "
        f"K={correction(tail)} ordinary={ordinary} ordered={ordered} "
        f"greedy={greedy}"
    )
    audit.cases += 1
    if ordinary < survival:
        audit.ordinary_failures += 1
        if audit.first_ordinary is None:
            audit.first_ordinary = description
    if ordered < survival:
        audit.ordered_failures += 1
        if audit.first_ordered is None:
            audit.first_ordered = description
    if greedy < survival:
        audit.greedy_failures += 1
        if audit.first_greedy is None:
            audit.first_greedy = description
    return survival, ordinary, ordered, greedy


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-length", type=int, default=16)
    args = parser.parse_args()
    if args.max_length < 1:
        parser.error("max length must be positive")

    specials = (
        ("tail-3 sharp", (1, 2, 1), 3),
        ("tail-2 repair", tuple(map(int, "12212121212121212")), 2),
        (
            "derivative adversary",
            tuple(map(int, "122212222222221212122")),
            2,
        ),
    )
    gate = Audit()
    for label, word, tail in specials:
        survival, ordinary, ordered, greedy = audit_word(word, tail, gate)
        print(
            f"gate={label} survival={survival} ordinary={ordinary} "
            f"ordered={ordered} greedy={greedy}"
        )
    if gate.ordinary_failures or gate.ordered_failures or gate.greedy_failures:
        print("immediate gate KILLED")
        print(f"first ordinary: {gate.first_ordinary or 'none'}")
        print(f"first ordered: {gate.first_ordered or 'none'}")
        print(f"first greedy: {gate.first_greedy or 'none'}")
        return

    audit = Audit()
    for length in range(1, args.max_length + 1):
        before_ordinary = audit.ordinary_failures
        before_ordered = audit.ordered_failures
        before_greedy = audit.greedy_failures
        for word in hard_core_prefixes(length):
            for tail in (2, 3):
                audit_word(word, tail, audit)
        print(
            f"length={length:2d} "
            f"ordinary-failures={audit.ordinary_failures-before_ordinary:4d} "
            f"ordered-failures={audit.ordered_failures-before_ordered:4d} "
            f"greedy-failures={audit.greedy_failures-before_greedy:4d}"
        )
    print(
        f"TOTAL cases={audit.cases} ordinary-failures={audit.ordinary_failures} "
        f"ordered-failures={audit.ordered_failures} "
        f"greedy-failures={audit.greedy_failures}"
    )
    print(f"first ordinary: {audit.first_ordinary or 'none'}")
    print(f"first ordered: {audit.first_ordered or 'none'}")
    print(f"first greedy: {audit.first_greedy or 'none'}")


if __name__ == "__main__":
    main()

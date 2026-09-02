#!/usr/bin/env python3
"""Test cumulative left/right intervention chains at the registered gate."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from constant_tail_ordered_matching import (
    correction_count,
    forced_trace,
    maximum_matching,
    maximum_ordered_real_matching,
)
from constant_tail_scale import Vector, hard_core_extension_length
from rank_zero_separator import hard_core_prefixes


def cumulative_graph(
    word: Vector, tail: int, direction: str
) -> tuple[dict[int, set[int]], int, tuple[int, ...]]:
    extension, previous_trace = forced_trace(word, tail)
    survival = hard_core_extension_length(word, extension)
    sources = [index for index, value in enumerate(word) if value == 2]
    if direction == "right-to-left":
        sources.reverse()
    elif direction != "left-to-right":
        raise ValueError(direction)

    graph = {step: set() for step in range(survival)}
    current = list(word)
    for token, source in enumerate(sources):
        current[source] = 1
        _, following_trace = forced_trace(tuple(current), tail)
        for step in range(survival):
            if (
                previous_trace[step].affine != following_trace[step].affine
                or previous_trace[step].forced != following_trace[step].forced
            ):
                graph[step].add(token)
        previous_trace = following_trace
    return graph, survival, tuple(sources)


@dataclass(slots=True)
class Audit:
    cases: int = 0
    ordinary_failures: int = 0
    ordered_failures: int = 0
    first_ordinary: str | None = None
    first_ordered: str | None = None


def audit_case(word: Vector, tail: int, direction: str, audit: Audit) -> None:
    graph, survival, _ = cumulative_graph(word, tail, direction)
    credits = correction_count(word, tail)
    ordinary = len(maximum_matching(graph, credits))
    ordered = maximum_ordered_real_matching(graph) + credits
    description = (
        f"direction={direction} tail={tail} W={''.join(map(str, word))} "
        f"s={survival} #2={word.count(2)} credits={credits} "
        f"ordinary={ordinary} ordered={ordered}"
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-length", type=int, default=16)
    args = parser.parse_args()
    if args.max_length < 1:
        parser.error("max length must be positive")

    word = tuple(map(int, "122212222222221212122"))
    tail = 2
    credits = correction_count(word, tail)
    print(
        f"gate W={''.join(map(str, word))} tail={tail} "
        f"#2={word.count(2)} credits={credits}"
    )
    any_cover = False
    for direction in ("left-to-right", "right-to-left"):
        graph, survival, sources = cumulative_graph(word, tail, direction)
        ordinary = maximum_matching(graph, credits)
        ordered = maximum_ordered_real_matching(graph) + credits
        covered = len(ordinary) == survival
        any_cover |= covered
        print(
            f"direction={direction} survival={survival} "
            f"ordinary={len(ordinary)}/{survival} "
            f"ordered={ordered}/{survival} "
            f"chain={sources}"
        )
        print(
            "  neighborhoods="
            + repr({step: sorted(tokens) for step, tokens in graph.items()})
        )
    print(
        "gate outcome: "
        + ("at least one direction survives" if any_cover else "both directions KILLED")
    )
    if not any_cover:
        return

    audits = {
        direction: Audit()
        for direction in ("left-to-right", "right-to-left")
    }
    for length in range(1, args.max_length + 1):
        before = {
            direction: (
                audit.ordinary_failures,
                audit.ordered_failures,
            )
            for direction, audit in audits.items()
        }
        for source_word in hard_core_prefixes(length):
            for source_tail in (2, 3):
                for direction, audit in audits.items():
                    audit_case(source_word, source_tail, direction, audit)
        fields = []
        for direction, audit in audits.items():
            prior_ordinary, prior_ordered = before[direction]
            fields.append(
                f"{direction}:ordinary-failures="
                f"{audit.ordinary_failures-prior_ordinary} "
                f"ordered-failures={audit.ordered_failures-prior_ordered}"
            )
        print(f"length={length:2d} " + " | ".join(fields))

    repair = tuple(map(int, "12212121212121212"))
    for direction, audit in audits.items():
        audit_case(repair, 2, direction, audit)
        print(
            f"TOTAL direction={direction} cases={audit.cases} "
            f"ordinary-failures={audit.ordinary_failures} "
            f"ordered-failures={audit.ordered_failures}"
        )
        print(f"  first ordinary: {audit.first_ordinary or 'none'}")
        print(f"  first ordered: {audit.first_ordered or 'none'}")


if __name__ == "__main__":
    main()

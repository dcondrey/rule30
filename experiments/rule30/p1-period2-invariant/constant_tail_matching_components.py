#!/usr/bin/env python3
"""Exploratory ablation of the ordered scale-matching edge relation.

The preregistered graph joins a survival step to a source-2 intervention when
either the affine boundary state or the forced endpoint symbol changes.  This
post-registered diagnostic asks whether a single scalar component already
supports the same covering.  A positive component is a possible algebraic
proof coordinate; a bounded pass is not a proof.
"""

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


COMPONENTS = (
    "forced",
    "alpha",
    "beta",
    "gamma",
    "a^b",
    "a^g",
    "b^g",
    "a^b^g",
    "ab",
    "ag",
    "bg",
    "affine",
    "union",
)


@dataclass(slots=True)
class Result:
    ordinary_failures: int = 0
    ordered_failures: int = 0
    first_ordinary: str | None = None
    first_ordered: str | None = None


def changed(component: str, original: object, intervened: object) -> bool:
    left = original  # Step, kept generic to make this table visibly exhaustive.
    right = intervened
    if component == "forced":
        return left.forced != right.forced  # type: ignore[attr-defined]
    if component == "alpha":
        return left.affine.alpha != right.affine.alpha  # type: ignore[attr-defined]
    if component == "beta":
        return left.affine.beta != right.affine.beta  # type: ignore[attr-defined]
    if component == "gamma":
        return left.affine.gamma != right.affine.gamma  # type: ignore[attr-defined]
    differences = (
        left.affine.alpha != right.affine.alpha,  # type: ignore[attr-defined]
        left.affine.beta != right.affine.beta,  # type: ignore[attr-defined]
        left.affine.gamma != right.affine.gamma,  # type: ignore[attr-defined]
    )
    if component == "a^b":
        return differences[0] ^ differences[1]
    if component == "a^g":
        return differences[0] ^ differences[2]
    if component == "b^g":
        return differences[1] ^ differences[2]
    if component == "a^b^g":
        return differences[0] ^ differences[1] ^ differences[2]
    if component == "ab":
        return differences[0] or differences[1]
    if component == "ag":
        return differences[0] or differences[2]
    if component == "bg":
        return differences[1] or differences[2]
    if component == "affine":
        return left.affine != right.affine  # type: ignore[attr-defined]
    if component == "union":
        return (
            left.affine != right.affine  # type: ignore[attr-defined]
            or left.forced != right.forced  # type: ignore[attr-defined]
        )
    raise ValueError(component)


def component_graphs(
    word: Vector, tail: int, survival: int
) -> dict[str, dict[int, set[int]]]:
    _, original = forced_trace(word, tail)
    graphs = {
        component: {step: set() for step in range(survival)}
        for component in COMPONENTS
    }
    for source, value in enumerate(word):
        if value != 2:
            continue
        intervened = word[:source] + (1,) + word[source + 1 :]
        _, trace = forced_trace(intervened, tail)
        for step in range(survival):
            for component in COMPONENTS:
                if changed(component, original[step], trace[step]):
                    graphs[component][step].add(source)
    return graphs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-length", type=int, default=12)
    args = parser.parse_args()
    if args.max_length < 1:
        parser.error("max length must be positive")

    results = {component: Result() for component in COMPONENTS}
    cases = 0
    for length in range(1, args.max_length + 1):
        for word in hard_core_prefixes(length):
            for tail in (2, 3):
                extension, _ = forced_trace(word, tail)
                survival = hard_core_extension_length(word, extension)
                credits = correction_count(word, tail)
                graphs = component_graphs(word, tail, survival)
                cases += 1
                for component, graph in graphs.items():
                    ordinary = len(maximum_matching(graph, credits))
                    ordered = maximum_ordered_real_matching(graph) + credits
                    result = results[component]
                    description = (
                        f"tail={tail} W={''.join(map(str, word))} "
                        f"s={survival} #2={word.count(2)} credits={credits}"
                    )
                    if ordinary < survival:
                        result.ordinary_failures += 1
                        if result.first_ordinary is None:
                            result.first_ordinary = (
                                f"{description} matching={ordinary}"
                            )
                    if ordered < survival:
                        result.ordered_failures += 1
                        if result.first_ordered is None:
                            result.first_ordered = (
                                f"{description} ordered-capacity={ordered}"
                            )
        print(f"completed length={length}")

    print(f"cases={cases}")
    for component in COMPONENTS:
        result = results[component]
        print(
            f"component={component:6s} "
            f"ordinary-failures={result.ordinary_failures:5d} "
            f"ordered-failures={result.ordered_failures:5d}"
        )
        print(f"  first ordinary: {result.first_ordinary or 'none'}")
        print(f"  first ordered:  {result.first_ordered or 'none'}")

    specials = (
        ("tail-2 repair", tuple(map(int, "12212121212121212")), 2),
        ("tail-3 sharp", (1, 2, 1), 3),
    )
    for label, word, tail in specials:
        extension, _ = forced_trace(word, tail)
        survival = hard_core_extension_length(word, extension)
        credits = correction_count(word, tail)
        graphs = component_graphs(word, tail, survival)
        print(
            f"special={label} W={''.join(map(str, word))} "
            f"s={survival} #2={word.count(2)} credits={credits}"
        )
        for component, graph in graphs.items():
            print(
                f"  component={component:7s} "
                f"ordinary={len(maximum_matching(graph, credits))}/{survival} "
                f"ordered={maximum_ordered_real_matching(graph)+credits}/{survival}"
            )


if __name__ == "__main__":
    main()

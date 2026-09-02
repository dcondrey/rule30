#!/usr/bin/env python3
"""Test an intervention-based ancestry matching for the scale charges.

This is the preregistered experiment in
``PREREGISTRATION-ORDERED-SCALE-MATCHING.md``.  It does not prove the scale
inequalities.  Its purpose is to decide whether one-symbol Boolean
sensitivity supplies a plausible injective certificate for them.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from constant_tail_scale import (
    Affine,
    Vector,
    affine_coordinates,
    append_dependency_edge,
    hard_core_extension_length,
    newest_cut_permutation,
    scale_extension_with_padding,
)
from rank_zero_separator import hard_core_prefixes


@dataclass(frozen=True, slots=True)
class Step:
    affine: Affine
    forced: int


def forced_trace(word: Vector, tail: int) -> tuple[Vector, tuple[Step, ...]]:
    """Return ``R_tail(word)`` and its exact newest-boundary states."""

    endpoint: list[int] = []
    edge: Vector = ()
    for value in (0,) * len(word) + word:
        edge = append_dependency_edge(
            edge, endpoint[-1] if endpoint else None, value
        )
        endpoint.append(value)

    extension: list[int] = []
    steps: list[Step] = []
    for _ in range(2 * len(word)):
        outcomes: list[tuple[int, Vector]] = []
        permutation: list[int] = []
        for value in range(4):
            following = append_dependency_edge(edge, endpoint[-1], value)
            permutation.append(following[-1])
            if following[-1] == tail:
                outcomes.append((value, following))
        affine = affine_coordinates(tuple(permutation))  # type: ignore[arg-type]
        assert affine.permutation() == tuple(permutation)
        assert len(outcomes) == 1
        value, edge = outcomes[0]
        steps.append(Step(affine, value))
        endpoint.append(value)
        extension.append(value)
    return tuple(extension), tuple(steps)


def influence_graph(
    word: Vector, tail: int, survival: int
) -> tuple[dict[int, set[int]], tuple[Step, ...]]:
    """Build the frozen intervention graph from output steps to source 2s."""

    _, original = forced_trace(word, tail)
    sources = [index for index, value in enumerate(word) if value == 2]
    changed: dict[int, tuple[Step, ...]] = {}
    for source in sources:
        intervened = word[:source] + (1,) + word[source + 1 :]
        _, changed[source] = forced_trace(intervened, tail)

    graph = {step: set() for step in range(survival)}
    for step in range(survival):
        for source in sources:
            if (
                changed[source][step].affine != original[step].affine
                or changed[source][step].forced != original[step].forced
            ):
                graph[step].add(source)
    return graph, original


def correction_count(word: Vector, tail: int) -> int:
    if tail == 3:
        return 3
    return int(any(left == right == 2 for left, right in zip(word, word[1:])))


def maximum_matching(
    graph: dict[int, set[int]], credits: int
) -> dict[int, tuple[str, int]]:
    """Return a maximum matching, adding universal correction vertices."""

    right_to_left: dict[tuple[str, int], int] = {}
    left_to_right: dict[int, tuple[str, int]] = {}
    adjacency = {
        left: tuple(("source", source) for source in sorted(sources))
        + tuple(("credit", credit) for credit in range(credits))
        for left, sources in graph.items()
    }

    def augment(left: int, seen: set[tuple[str, int]]) -> bool:
        for right in adjacency[left]:
            if right in seen:
                continue
            seen.add(right)
            previous = right_to_left.get(right)
            if previous is None or augment(previous, seen):
                right_to_left[right] = left
                left_to_right[left] = right
                return True
        return False

    for left in graph:
        augment(left, set())
    return left_to_right


def maximum_ordered_real_matching(graph: dict[int, set[int]]) -> int:
    """Maximum noncrossing matching between ordered steps and sources."""

    steps = tuple(sorted(graph))
    sources = tuple(sorted({source for adjacent in graph.values() for source in adjacent}))
    table = [[0] * (len(sources) + 1) for _ in range(len(steps) + 1)]
    for i, step in enumerate(steps, start=1):
        for k, source in enumerate(sources, start=1):
            best = max(table[i - 1][k], table[i][k - 1])
            if source in graph[step]:
                best = max(best, table[i - 1][k - 1] + 1)
            table[i][k] = best
    return table[-1][-1]


def replay_matched_edges(
    word: Vector,
    tail: int,
    matching: dict[int, tuple[str, int]],
    original: tuple[Step, ...],
) -> int:
    """Independently recompute every selected non-credit intervention edge."""

    checked = 0
    for step, (kind, source) in matching.items():
        if kind == "credit":
            continue
        intervened = word[:source] + (1,) + word[source + 1 :]
        _, changed = forced_trace(intervened, tail)
        assert (
            changed[step].affine != original[step].affine
            or changed[step].forced != original[step].forced
        )
        checked += 1
    return checked


def literal_controls(max_length: int) -> int:
    checked = 0
    for length in range(1, max_length + 1):
        for word in hard_core_prefixes(length):
            for tail in (2, 3):
                extension, steps = forced_trace(word, tail)
                assert extension == scale_extension_with_padding(
                    word, tail, (0,) * length
                )

                endpoint = (0,) * length + word
                for index, step in enumerate(steps):
                    literal = newest_cut_permutation(endpoint)
                    assert step.affine.permutation() == literal
                    assert literal[step.forced] == tail
                    endpoint += (step.forced,)
                    checked += 1
    return checked


@dataclass(slots=True)
class Audit:
    words: int = 0
    steps: int = 0
    replayed: int = 0
    ordinary_failures: int = 0
    ordered_failures: int = 0
    real_capacity_failures: int = 0
    credit_essential: int = 0
    empty_step_neighborhoods: int = 0
    first_ordinary: str | None = None
    first_ordered: str | None = None
    first_real_capacity: str | None = None


def audit_word(word: Vector, tail: int, audit: Audit, label: str = "") -> str:
    extension, _ = forced_trace(word, tail)
    survival = hard_core_extension_length(word, extension)
    graph, original = influence_graph(word, tail, survival)
    credits = correction_count(word, tail)
    real_matching = maximum_matching(graph, 0)
    matching = maximum_matching(graph, credits)
    ordered_real = maximum_ordered_real_matching(graph)
    ordinary_ok = len(matching) == survival
    ordered_ok = ordered_real + credits >= survival

    audit.words += 1
    audit.steps += survival
    audit.empty_step_neighborhoods += sum(not adjacent for adjacent in graph.values())
    real_ceiling = min(survival, word.count(2))
    if len(real_matching) < real_ceiling:
        audit.real_capacity_failures += 1
        if audit.first_real_capacity is None:
            audit.first_real_capacity = (
                f"tail={tail} W={''.join(map(str, word))} s={survival} "
                f"#2={word.count(2)} real-matching={len(real_matching)} "
                f"ceiling={real_ceiling}"
            )
    if survival > len(real_matching):
        audit.credit_essential += 1
    if ordinary_ok:
        audit.replayed += replay_matched_edges(
            word, tail, matching, original
        )
    else:
        audit.ordinary_failures += 1
        if audit.first_ordinary is None:
            audit.first_ordinary = (
                f"tail={tail} W={''.join(map(str, word))} s={survival} "
                f"#2={word.count(2)} credits={credits} "
                f"matching={len(matching)} R={''.join(map(str, extension))}"
            )
    if not ordered_ok:
        audit.ordered_failures += 1
        if audit.first_ordered is None:
            audit.first_ordered = (
                f"tail={tail} W={''.join(map(str, word))} s={survival} "
                f"#2={word.count(2)} credits={credits} "
                f"ordered-real={ordered_real} R={''.join(map(str, extension))}"
            )

    pairs = ",".join(
        f"{step}->{kind[0]}{index}"
        for step, (kind, index) in sorted(matching.items())
    )
    prefix = f"{label}: " if label else ""
    return (
        f"{prefix}tail={tail} W={''.join(map(str, word))} s={survival} "
        f"real={len(real_matching)}/{real_ceiling} "
        f"ordinary={len(matching)}/{survival} ordered-real={ordered_real} "
        f"credits={credits} matching=[{pairs}]"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-length", type=int, default=16)
    parser.add_argument("--literal-control-length", type=int, default=5)
    args = parser.parse_args()
    if args.max_length < 1 or args.literal_control_length < 0:
        parser.error("length bounds must be nonnegative and max length positive")

    controls = literal_controls(args.literal_control_length)
    print(f"literal cone/diagonal/affine controls: {controls} steps PASS")

    audit = Audit()
    for length in range(1, args.max_length + 1):
        before = Audit(
            words=audit.words,
            steps=audit.steps,
            replayed=audit.replayed,
            ordinary_failures=audit.ordinary_failures,
            ordered_failures=audit.ordered_failures,
            real_capacity_failures=audit.real_capacity_failures,
            credit_essential=audit.credit_essential,
            empty_step_neighborhoods=audit.empty_step_neighborhoods,
        )
        for word in hard_core_prefixes(length):
            for tail in (2, 3):
                audit_word(word, tail, audit)
        print(
            f"length={length:2d} words={audit.words-before.words:5d} "
            f"survival-steps={audit.steps-before.steps:6d} "
            f"ordinary-failures={audit.ordinary_failures-before.ordinary_failures:5d} "
            f"ordered-failures={audit.ordered_failures-before.ordered_failures:5d} "
            f"real-capacity-failures="
            f"{audit.real_capacity_failures-before.real_capacity_failures:5d}"
        )

    print(audit_word(tuple(map(int, "12212121212121212")), 2, audit, "repair witness"))
    print(audit_word((1, 2, 1), 3, audit, "tail-3 sharp witness"))
    print(
        f"TOTAL words={audit.words} survival-steps={audit.steps} "
        f"replayed-edges={audit.replayed} "
        f"ordinary-failures={audit.ordinary_failures} "
        f"ordered-failures={audit.ordered_failures} "
        f"real-capacity-failures={audit.real_capacity_failures} "
        f"credit-essential={audit.credit_essential} "
        f"empty-step-neighborhoods={audit.empty_step_neighborhoods}"
    )
    print(f"first ordinary failure: {audit.first_ordinary or 'none'}")
    print(f"first ordered failure: {audit.first_ordered or 'none'}")
    print(f"first real-capacity failure: {audit.first_real_capacity or 'none'}")


if __name__ == "__main__":
    main()

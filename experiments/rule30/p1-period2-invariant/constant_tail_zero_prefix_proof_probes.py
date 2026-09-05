#!/usr/bin/env python3
"""Probe simple proof-strengthenings of zero-prefix greedy matching."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from constant_tail_ordered_matching import forced_trace
from constant_tail_scale import Vector, hard_core_extension_length
from constant_tail_zero_prefix_matching import greedy_matching, zero_prefix_graph
from rank_zero_separator import hard_core_prefixes


def affine_label(step: object) -> tuple[int, int, int]:
    return (step.affine.alpha, step.affine.beta, step.affine.gamma)  # type: ignore[attr-defined]


def scenario_traces(word: Vector, tail: int) -> tuple[tuple[object, ...], ...]:
    current = list(word)
    traces = [forced_trace(tuple(current), tail)[1]]
    for token in range(len(word)):
        current[token] = 0
        traces.append(forced_trace(tuple(current), tail)[1])
    return tuple(traces)


@dataclass(slots=True)
class Audit:
    rows: int = 0
    endpoint_failures: int = 0
    first_endpoint_failure: str | None = None
    single_change_failures: int = 0
    first_single_change_failure: str | None = None


def audit_word(word: Vector, tail: int, audit: Audit) -> None:
    extension, _ = forced_trace(word, tail)
    survival = hard_core_extension_length(word, extension)
    graph, checked_survival = zero_prefix_graph(word, tail)
    assert survival == checked_survival
    greedy = greedy_matching(graph)
    traces = scenario_traces(word, tail)
    last = -1
    for row in range(survival):
        must_match = tail == 2 or row + 1 < survival
        if not must_match:
            continue
        audit.rows += 1
        left_scenario = last + 1
        left = affine_label(traces[left_scenario][row])
        right = affine_label(traces[len(word)][row])
        if left == right:
            audit.endpoint_failures += 1
            if audit.first_endpoint_failure is None:
                audit.first_endpoint_failure = (
                    f"tail={tail} W={''.join(map(str, word))} row={row} "
                    f"last={last} scenario={left_scenario} label={left} "
                    f"changes={sorted(k for k in graph[row] if k>last)}"
                )
        later_changes = [token for token in graph[row] if token > last]
        if len(later_changes) != 1:
            audit.single_change_failures += 1
            if audit.first_single_change_failure is None:
                audit.first_single_change_failure = (
                    f"tail={tail} W={''.join(map(str, word))} row={row} "
                    f"last={last} changes={sorted(later_changes)}"
                )
        assert row in greedy
        last = greedy[row]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-length", type=int, default=12)
    args = parser.parse_args()
    audit = Audit()
    for length in range(1, args.max_length + 1):
        for word in hard_core_prefixes(length):
            for tail in (2, 3):
                audit_word(word, tail, audit)
    for word, tail in (
        (tuple(map(int, "12212121212121212")), 2),
        (tuple(map(int, "122212222222221212122")), 2),
        ((1, 2, 1), 3),
    ):
        audit_word(word, tail, audit)
    print(
        f"rows={audit.rows} endpoint-failures={audit.endpoint_failures} "
        f"single-change-failures={audit.single_change_failures}"
    )
    print(f"first endpoint failure: {audit.first_endpoint_failure or 'none'}")
    print(
        f"first single-change failure: "
        f"{audit.first_single_change_failure or 'none'}"
    )


if __name__ == "__main__":
    main()

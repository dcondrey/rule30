#!/usr/bin/env python3
"""Display cumulative change matrices and optimal noncrossing matchings."""

from __future__ import annotations

from constant_tail_cumulative_matching import cumulative_graph
from constant_tail_ordered_matching import correction_count, forced_trace
from constant_tail_scale import Vector, hard_core_extension_length


def ordered_pairs(graph: dict[int, set[int]]) -> tuple[tuple[int, int], ...]:
    steps = tuple(sorted(graph))
    tokens = tuple(sorted({token for values in graph.values() for token in values}))
    table = [[0] * (len(tokens) + 1) for _ in range(len(steps) + 1)]
    for i, step in enumerate(steps, start=1):
        for k, token in enumerate(tokens, start=1):
            table[i][k] = max(table[i - 1][k], table[i][k - 1])
            if token in graph[step]:
                table[i][k] = max(
                    table[i][k], table[i - 1][k - 1] + 1
                )

    pairs = []
    i, k = len(steps), len(tokens)
    while i and k:
        step, token = steps[i - 1], tokens[k - 1]
        if (
            token in graph[step]
            and table[i][k] == table[i - 1][k - 1] + 1
        ):
            pairs.append((step, token))
            i -= 1
            k -= 1
        elif table[i - 1][k] >= table[i][k - 1]:
            i -= 1
        else:
            k -= 1
    pairs.reverse()
    assert len(pairs) == table[-1][-1]
    return tuple(pairs)


def cumulative_labels(
    word: Vector, tail: int
) -> tuple[tuple[str, ...], ...]:
    sources = [index for index, value in enumerate(word) if value == 2]
    current = list(word)
    traces = []
    extension, trace = forced_trace(tuple(current), tail)
    survival = hard_core_extension_length(word, extension)
    traces.append(trace)
    for source in sources:
        current[source] = 1
        _, trace = forced_trace(tuple(current), tail)
        traces.append(trace)
    return tuple(
        tuple(
            f"{trace[step].affine.alpha}{trace[step].affine.beta}"
            f"{trace[step].affine.gamma}:{trace[step].forced}"
            for trace in traces
        )
        for step in range(survival)
    )


def show(label: str, word: Vector, tail: int) -> None:
    graph, survival, sources = cumulative_graph(word, tail, "left-to-right")
    pairs = ordered_pairs(graph)
    labels = cumulative_labels(word, tail)
    matched = dict(pairs)
    print(
        f"{label}: tail={tail} W={''.join(map(str, word))} "
        f"s={survival} #2={len(sources)} K={correction_count(word, tail)}"
    )
    print(f"sources={sources}")
    print(f"optimal ordered pairs={pairs}")
    for step, row in enumerate(labels):
        changes = "".join("1" if token in graph[step] else "0" for token in range(len(sources)))
        print(
            f"j={step:2d} edge={changes} match={matched.get(step, '-'):>2} "
            + " ".join(row)
        )


def main() -> None:
    show("tail-2 repair", tuple(map(int, "12212121212121212")), 2)
    show(
        "derivative adversary",
        tuple(map(int, "122212222222221212122")),
        2,
    )
    show("tail-3 sharp", (1, 2, 1), 3)


if __name__ == "__main__":
    main()

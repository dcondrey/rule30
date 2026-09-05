#!/usr/bin/env python3
"""Exact zero-tail dual for the ``011`` period-three carry signature.

An infinite surviving signature is coded by one free parity bit per
three-step macro.  The inverse macro branches prepend the binary blocks
``000`` or ``111`` and leave a section automorphism.  If the coded signature
is a nonnegative integer, its high base-eight digits are eventually zero.
Those zero digits drive the dual word map implemented here.

The finite weighted-graph check proves a lexicographic monotonicity theorem
for that dual map.  It does not prove that every dual orbit terminates.
"""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
from itertools import product

GeneratorWord = tuple[int, ...]
GraphState = tuple[int, int, int, int, int, int]
Vector = tuple[int, ...]

# Labels 0,1,2 denote the inverses of the three carry automorphisms.  Acting
# on one binary input bit gives the output xor and the indicated section.
ROOT_XOR = (0, 1, 1)
SECTION = ((0, 2), (2, 0), (2, 1))

# For the 011 schedule at phase zero, one inverse macro branch has low block
# 000 and section word 200; the other has low block 111 and section word 202.
BRANCH_BLOCK = (0, 7)
BRANCH_SECTION = ((2, 0, 0), (2, 0, 2))

# These internal factors were obtained one at a time.  At each stage the
# preceding factors are held equal, and the next factor count never rises.
LEX_FACTORS = (
    (0, 1, 0),
    (0, 1, 1),
    (0, 1, 2),
    (0, 0, 1),
    (2, 0, 1),
    (1, 0, 1),
    (1, 1, 1),
    (2, 1, 1),
    (1, 1, 0),
    (1, 1, 2),
    (2, 2, 0),
)


def generator_action(symbol: int, value: int, bits: int = 3) -> tuple[int, int]:
    """Act on ``bits`` low bits and return the output and final section."""

    if symbol not in range(3) or value not in range(1 << bits):
        raise ValueError("invalid generator action")
    output = 0
    for bit in range(bits):
        old = (value >> bit) & 1
        output |= (old ^ ROOT_XOR[symbol]) << bit
        symbol = SECTION[symbol][old]
    return output, symbol


def word_action(word: GeneratorWord, value: int, bits: int = 3) -> tuple[int, GeneratorWord]:
    """Act by a generator word and return its coordinatewise section word."""

    section = []
    for symbol in word:
        value, following = generator_action(symbol, value, bits)
        section.append(following)
    return value, tuple(section)


def zero_transition(word: GeneratorWord) -> tuple[int, GeneratorWord] | None:
    """Return the unique branch emitting a zero base-eight digit, if any."""

    choices = []
    for branch, block in enumerate(BRANCH_BLOCK):
        output, section = word_action(word, block)
        if output == 0:
            choices.append((branch, BRANCH_SECTION[branch] + section))
    if len(choices) > 1:
        raise AssertionError("an automorphism mapped two inputs to zero")
    return choices[0] if choices else None


def factor_vector(word: GeneratorWord) -> Vector:
    """Count the ordered theorem factors in one dual word."""

    return tuple(
        sum(word[index : index + 3] == factor for index in range(len(word) - 2))
        for factor in LEX_FACTORS
    )


def finite_lex_control(max_length: int = 10) -> None:
    """Directly check the lexicographic inequality on a finite word census."""

    for length in range(max_length + 1):
        for word in product(range(3), repeat=length):
            first = zero_transition(word)
            if first is None or zero_transition(first[1]) is None:
                continue
            assert factor_vector(first[1]) <= factor_vector(word)


@dataclass(frozen=True)
class WeightedGraph:
    initial: GraphState
    states: tuple[GraphState, ...]
    edges: dict[GraphState, tuple[tuple[GraphState, Vector], ...]]
    terminals: frozenset[GraphState]


def _edge_vector(input_triple: tuple[int, int, int], output_triple: tuple[int, int, int]) -> Vector:
    return tuple(
        int(output_triple == factor) - int(input_triple == factor)
        for factor in LEX_FACTORS
    )


def build_graph(first_branch: int, second_branch: int) -> WeightedGraph:
    """Build the exact regular path graph for two consecutive zero digits."""

    second_start, _ = word_action(
        BRANCH_SECTION[first_branch], BRANCH_BLOCK[second_branch]
    )
    # Context symbol 3 is a boundary marker unequal to every generator.  The
    # theorem counts internal trigrams only, so its incident vectors are zero.
    initial: GraphState = (
        BRANCH_BLOCK[first_branch],
        second_start,
        3,
        3,
        BRANCH_SECTION[first_branch][-2],
        BRANCH_SECTION[first_branch][-1],
    )
    states = {initial}
    queue = deque([initial])
    edges: dict[GraphState, tuple[tuple[GraphState, Vector], ...]] = {}
    while queue:
        state = queue.popleft()
        q1, q2, input_first, input_second, output_first, output_second = state
        outgoing = []
        for symbol in range(3):
            next_q1, emitted = generator_action(symbol, q1)
            next_q2, _ = generator_action(emitted, q2)
            following = (
                next_q1,
                next_q2,
                input_second,
                symbol,
                output_second,
                emitted,
            )
            vector = _edge_vector(
                (input_first, input_second, symbol),
                (output_first, output_second, emitted),
            )
            outgoing.append((following, vector))
            if following not in states:
                states.add(following)
                queue.append(following)
        edges[state] = tuple(outgoing)
    terminals = frozenset(state for state in states if state[0] == state[1] == 0)
    return WeightedGraph(initial, tuple(states), edges, terminals)


def _maximum_weight(graph: WeightedGraph, coordinate: int) -> tuple[int, dict[GraphState, int]]:
    """Return the all-path maximum, rejecting a positive reachable cycle."""

    distance: dict[GraphState, int | None] = {state: None for state in graph.states}
    distance[graph.initial] = 0
    for _ in range(len(graph.states)):
        changed = False
        for source in graph.states:
            if distance[source] is None:
                continue
            for target, vector in graph.edges[source]:
                candidate = distance[source] + vector[coordinate]
                if distance[target] is None or candidate > distance[target]:
                    distance[target] = candidate
                    changed = True
        if not changed:
            exact = {state: value for state, value in distance.items() if value is not None}
            return max(exact[state] for state in graph.terminals), exact
    raise AssertionError("positive cycle in a factor-count comparison graph")


def restrict_equality(graph: WeightedGraph, coordinate: int) -> tuple[WeightedGraph, int]:
    """Prove nonincrease and retain exactly the equality paths."""

    maximum, distance = _maximum_weight(graph, coordinate)
    if maximum > 0:
        raise AssertionError(
            f"factor {LEX_FACTORS[coordinate]} can increase by {maximum}"
        )
    tight_edges: dict[GraphState, list[tuple[GraphState, Vector]]] = {
        state: [] for state in graph.states
    }
    reverse: dict[GraphState, list[GraphState]] = {state: [] for state in graph.states}
    for source in graph.states:
        if source not in distance:
            continue
        for target, vector in graph.edges[source]:
            if distance[target] == distance[source] + vector[coordinate]:
                tight_edges[source].append((target, vector))
                reverse[target].append(source)
    terminals = {
        state for state in graph.terminals if distance.get(state) == 0
    }
    useful = set(terminals)
    queue = deque(useful)
    while queue:
        target = queue.popleft()
        for source in reverse[target]:
            if source not in useful:
                useful.add(source)
                queue.append(source)
    if graph.initial not in useful:
        return WeightedGraph(
            graph.initial, (), {}, frozenset()
        ), maximum
    restricted = WeightedGraph(
        graph.initial,
        tuple(useful),
        {
            source: tuple(
                edge for edge in tight_edges[source] if edge[0] in useful
            )
            for source in useful
        },
        frozenset(terminals),
    )
    return restricted, maximum


def verify_lex_theorem() -> list[tuple[tuple[int, int, int], int, int]]:
    """Verify all-length lexicographic nonincrease by finite graph closure."""

    graphs = [build_graph(first, second) for first in range(2) for second in range(2)]
    report = []
    for coordinate, factor in enumerate(LEX_FACTORS):
        maxima = []
        following = []
        for graph in graphs:
            if not graph.states:
                following.append(graph)
                maxima.append(-1)
                continue
            restricted, maximum = restrict_equality(graph, coordinate)
            maxima.append(maximum)
            following.append(restricted)
        graphs = following
        report.append((factor, max(maxima), sum(len(graph.states) for graph in graphs)))
    return report


def verify_equality_is_zero_language() -> tuple[int, ...]:
    """Prove that full lexicographic equality has no counted factor.

    After all eleven equality restrictions, every remaining accepting path
    is a word whose factor vector is zero.  It is enough to inspect useful
    edges: the graph state retains the preceding two input symbols, so every
    internal trigram is exposed on exactly one edge.
    """

    counts = []
    for first_branch in range(2):
        for second_branch in range(2):
            graph = build_graph(first_branch, second_branch)
            for coordinate in range(len(LEX_FACTORS)):
                graph, maximum = restrict_equality(graph, coordinate)
                if maximum > 0:
                    raise AssertionError("lexicographic restriction failed")
            for source, outgoing in graph.edges.items():
                input_prefix = source[2:4]
                for target, _vector in outgoing:
                    input_triple = input_prefix + (target[3],)
                    if input_triple in LEX_FACTORS:
                        raise AssertionError(
                            "a full-equality path contains a counted factor"
                        )
            counts.append(len(graph.states))
    return tuple(counts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--control-length", type=int, default=10)
    args = parser.parse_args()
    if args.control_length < 0:
        parser.error("control length must be nonnegative")
    finite_lex_control(args.control_length)
    print("finite direct dual control: PASS")
    print("factor maximum_on_prior_equal equality_states")
    for factor, maximum, states in verify_lex_theorem():
        print(f"{''.join(map(str, factor))} {maximum:22d} {states:15d}")
    print("all-length lexicographic nonincrease: PASS")
    equality_states = verify_equality_is_zero_language()
    print(
        "full equality implies zero factor vector: "
        f"PASS states={equality_states}"
    )


if __name__ == "__main__":
    main()

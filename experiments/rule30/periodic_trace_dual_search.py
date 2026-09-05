#!/usr/bin/env python3
"""Exact factor-ranking search for one-zero periodic trace duals.

For a trace ``0 1^(p-1)`` the inverse signature macro has two branches.
This program derives their low ``p``-bit blocks and common/different section
words directly from the checked inverse carry automaton.  It then builds the
finite weighted graph for two consecutive zero-tail transitions and greedily
searches for lexicographically nonincreasing factor counts.  Every accepted
ranking coordinate is an arbitrary-word theorem; the search never substitutes
a bounded word census for graph closure.

The program is a proof-discovery instrument.  A nonempty equality graph is an
obstruction, not a mortality proof.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from dataclasses import dataclass
from itertools import product

from z3 import Int, Real, SolverFor, sat

from period3_zero_tail_dual import generator_action, word_action

Word = tuple[int, ...]
State = tuple[int, ...]


def inverse_generator(symbol: int, value: int, bits: int) -> int:
    """Apply one inverse carry generator on exactly ``bits`` low bits."""

    if bits == 0:
        return 0
    return generator_action(symbol, value & ((1 << bits) - 1), bits)[0]


def inverse_macro_value(period: Word, branch: int, value: int, bits: int) -> int:
    """Invert one driven macro modulo ``2^bits``.

    ``period`` must contain exactly one zero, at phase zero.  ``branch`` is
    the otherwise-free parity at that phase.
    """

    if not period or period[0] != 0 or period.count(0) != 1:
        raise ValueError("period must have its unique zero at phase zero")
    result = value & ((1 << bits) - 1)
    for phase in reversed(range(len(period))):
        center = period[phase]
        following = period[(phase + 1) % len(period)]
        parity = branch if center == 0 else 1 ^ following
        boundary = 2 if parity else center
        result = (
            (inverse_generator(boundary, result, max(bits - 1, 0)) << 1)
            | parity
        ) & ((1 << bits) - 1)
    return result


def derive_branch_data(period: Word, check_bits: int = 7) -> tuple[Word, tuple[Word, Word]]:
    """Return the two low blocks and their exact section-generator words."""

    width = len(period)
    blocks = tuple(inverse_macro_value(period, branch, 0, width) for branch in (0, 1))
    sections: list[Word] = []
    signatures = []
    for branch in (0, 1):
        signatures.append(
            tuple(
                inverse_macro_value(period, branch, value, width + check_bits) >> width
                for value in range(1 << check_bits)
            )
        )
    candidates = list(product(range(3), repeat=width))
    for signature in signatures:
        matches = [
            candidate
            for candidate in candidates
            if tuple(
                word_action(candidate, value, check_bits)[0]
                for value in range(1 << check_bits)
            )
            == signature
        ]
        if len(matches) != 1:
            raise AssertionError(f"section-word identification is not unique: {matches}")
        sections.append(matches[0])

    # An independent deeper check guards against an accidental shallow-level
    # collision between distinct automorphisms.
    deeper = check_bits + 3
    for branch, section in enumerate(sections):
        for value in range(1 << deeper):
            expected = inverse_macro_value(period, branch, value, width + deeper) >> width
            actual = word_action(section, value, deeper)[0]
            if actual != expected:
                raise AssertionError("derived section word failed the deeper check")
    return blocks, (sections[0], sections[1])


def factor_delta(prefix: Word, before: Word, after: Word, factor: Word) -> int:
    """Local count delta, including factors wholly inside ``prefix``."""

    width = len(factor)
    internal = sum(
        prefix[index : index + width] == factor
        for index in range(len(prefix) - width + 1)
    )
    return internal + int(after == factor) - int(before == factor)


@dataclass
class Graph:
    initial: State
    states: set[State]
    edges: dict[State, list[tuple[State, Word, Word]]]
    terminals: set[State]
    offset: dict[Word, int]


def build_graph(
    bits: int,
    blocks: Word,
    sections: tuple[Word, Word],
    first_branch: int,
    second_branch: int,
    factor_width: int,
) -> Graph:
    """Build the exact path graph for two consecutive dual transitions."""

    marker = 3
    context = factor_width - 1
    first_prefix = sections[first_branch]
    second_start, _ = word_action(first_prefix, blocks[second_branch], bits)
    input_seed = (marker,) * context
    output_seed = first_prefix[-context:] if context else ()
    initial = (blocks[first_branch], second_start, *input_seed, *output_seed)
    states = {initial}
    queue = deque([initial])
    edges: dict[State, list[tuple[State, Word, Word]]] = {}
    while queue:
        state = queue.popleft()
        q1, q2 = state[:2]
        input_context = state[2 : 2 + context]
        output_context = state[2 + context :]
        outgoing = []
        for symbol in range(3):
            next_q1, emitted = generator_action(symbol, q1, bits)
            next_q2, _ = generator_action(emitted, q2, bits)
            input_window = (*input_context, symbol)
            output_window = (*output_context, emitted)
            next_input = input_window[-context:] if context else ()
            next_output = output_window[-context:] if context else ()
            following = (next_q1, next_q2, *next_input, *next_output)
            outgoing.append((following, input_window, output_window))
            if following not in states:
                states.add(following)
                queue.append(following)
        edges[state] = outgoing
    terminals = {state for state in states if state[0] == state[1] == 0}
    reverse: dict[State, list[State]] = {state: [] for state in states}
    for source, outgoing in edges.items():
        for target, _before, _after in outgoing:
            reverse[target].append(source)
    useful = set(terminals)
    queue = deque(useful)
    while queue:
        target = queue.popleft()
        for source in reverse[target]:
            if source not in useful:
                useful.add(source)
                queue.append(source)
    states = useful
    terminals &= useful
    edges = {
        source: [edge for edge in edges[source] if edge[0] in useful]
        for source in useful
    }
    offset = {
        factor: sum(
            first_prefix[index : index + factor_width] == factor
            for index in range(len(first_prefix) - factor_width + 1)
        )
        for factor in product(range(3), repeat=factor_width)
    }
    return Graph(initial, states, edges, terminals, offset)


def restrict_factor(graph: Graph, factor: Word) -> tuple[Graph, int]:
    """Prove nonincrease and retain exactly total-delta-zero paths."""

    minus_inf = -10**18
    # Reject positive cycles with a difference-constraints certificate before
    # computing longest distances.  This is much faster than waiting for a
    # Bellman relaxation to traverse a pump thousands of times.
    ordered_states = tuple(graph.states)
    index = {state: position for position, state in enumerate(ordered_states)}
    potential = [Int(f"p_{position}") for position in range(len(ordered_states))]
    solver = SolverFor("QF_IDL")
    solver.add(potential[index[graph.initial]] == 0)
    for source, outgoing in graph.edges.items():
        for target, before, after in outgoing:
            weight = int(after == factor) - int(before == factor)
            solver.add(potential[index[target]] >= potential[index[source]] + weight)
    if solver.check() != sat:
        return graph, 1

    distance = {state: minus_inf for state in graph.states}
    distance[graph.initial] = graph.offset[factor]
    queue = deque([graph.initial])
    queued = {graph.initial}
    relaxations = Counter()
    while queue:
        source = queue.popleft()
        queued.discard(source)
        for target, before, after in graph.edges.get(source, ()):
            weight = int(after == factor) - int(before == factor)
            candidate = distance[source] + weight
            if candidate <= distance[target]:
                continue
            distance[target] = candidate
            relaxations[target] += 1
            if relaxations[target] > len(graph.states):
                # Every state is co-accessible, so this reachable positive
                # cycle pumps an accepting path.
                return graph, 1
            if target not in queued:
                queue.append(target)
                queued.add(target)

    maximum = max((distance[state] for state in graph.terminals), default=minus_inf)
    if maximum > 0:
        return graph, maximum

    tight: dict[State, list[tuple[State, Word, Word]]] = {
        state: [] for state in graph.states
    }
    reverse: dict[State, list[State]] = {state: [] for state in graph.states}
    for source in graph.states:
        if distance[source] == minus_inf:
            continue
        for edge in graph.edges.get(source, ()):
            target, before, after = edge
            weight = int(after == factor) - int(before == factor)
            if distance[target] == distance[source] + weight:
                tight[source].append(edge)
                reverse[target].append(source)
    terminals = {state for state in graph.terminals if distance[state] == 0}
    useful = set(terminals)
    queue = deque(useful)
    while queue:
        target = queue.popleft()
        for source in reverse[target]:
            if source not in useful:
                useful.add(source)
                queue.append(source)
    if graph.initial not in useful:
        return Graph(graph.initial, set(), {}, set(), graph.offset), maximum
    return Graph(
        graph.initial,
        useful,
        {
            source: [edge for edge in tight[source] if edge[0] in useful]
            for source in useful
        },
        terminals,
        # Earlier coordinates are now exactly equal, so only the new
        # factor's fixed-prefix contribution is relevant on the next pass.
        graph.offset,
    ), maximum


def greedy_ranking(period: Word, factor_width: int, candidates: tuple[Word, ...] | None = None) -> None:
    blocks, sections = derive_branch_data(period)
    print(f"period={''.join(map(str, period))}")
    print("blocks=" + ",".join(format(block, f"0{len(period)}b")[::-1] for block in blocks))
    print("sections=" + ",".join("".join(map(str, word)) for word in sections))
    graphs = [
        build_graph(len(period), blocks, sections, first, second, factor_width)
        for first in (0, 1)
        for second in (0, 1)
    ]
    remaining = set(candidates or product(range(3), repeat=factor_width))
    chosen: list[Word] = []
    while remaining and any(graph.states for graph in graphs):
        options = []
        for factor in remaining:
            following = []
            maxima = []
            valid = True
            for graph in graphs:
                if not graph.states:
                    following.append(graph)
                    maxima.append(-10**18)
                    continue
                restricted, maximum = restrict_factor(graph, factor)
                if maximum > 0:
                    valid = False
                    break
                following.append(restricted)
                maxima.append(maximum)
            if valid:
                options.append((sum(len(graph.states) for graph in following), factor, following, maxima))
        if not options:
            break
        state_count, factor, graphs, maxima = min(options, key=lambda row: (row[0], row[1]))
        remaining.remove(factor)
        chosen.append(factor)
        print(
            f"factor={''.join(map(str, factor))} maxima={maxima} "
            f"equality_states={state_count}"
        )
    edge_labels = Counter()
    for graph in graphs:
        for outgoing in graph.edges.values():
            for _target, before, _after in outgoing:
                edge_labels[before] += 1
    print("ranking=" + ",".join("".join(map(str, factor)) for factor in chosen))
    print(f"final_states={sum(len(graph.states) for graph in graphs)}")
    print("remaining_input_factors=" + ",".join(
        "".join(map(str, factor)) for factor in sorted(edge_labels)
    ))


def synthesize_strict_additive(period: Word, factor_width: int, weight_bound: int) -> None:
    """Synthesize a bounded-below strict additive ranking, if one exists.

    The certificate is wholly finite.  De Bruijn-graph potentials certify
    that the factor sum is bounded below on all finite words.  Product-graph
    potentials certify a decrease of at least one on every transition that
    has a following transition, which is enough to exclude an infinite orbit.
    """

    bits = len(period)
    blocks, sections = derive_branch_data(period)
    factors = tuple(product(range(3), repeat=factor_width))
    weights = {factor: Real("w_" + "".join(map(str, factor))) for factor in factors}
    solver = SolverFor("QF_LRA")
    for weight in weights.values():
        solver.add(weight >= -weight_bound, weight <= weight_bound)

    context_width = factor_width - 1
    contexts = tuple(product(range(3), repeat=context_width)) if context_width else ((),)
    lower = {context: Real("a_" + ("".join(map(str, context)) or "empty")) for context in contexts}
    solver.add(lower[contexts[0]] == 0)
    for context in contexts:
        for symbol in range(3):
            factor = (*context, symbol)
            following = factor[-context_width:] if context_width else ()
            solver.add(weights[factor] + lower[context] - lower[following] >= 0)

    graphs = []
    for first in (0, 1):
        for second in (0, 1):
            graph = build_graph(bits, blocks, sections, first, second, factor_width)
            graphs.append((first, second, graph))
            ordered = tuple(graph.states)
            rank = {
                state: Real(f"p_{first}_{second}_{index}")
                for index, state in enumerate(ordered)
            }
            solver.add(rank[graph.initial] == 0)
            for source, outgoing in graph.edges.items():
                for target, before, after in outgoing:
                    delta = weights[after]
                    if all(symbol < 3 for symbol in before):
                        delta -= weights[before]
                    solver.add(delta + rank[source] - rank[target] <= 0)
            prefix_weight = sum(
                count * weights[factor]
                for factor, count in graph.offset.items()
                if count
            )
            for terminal in graph.terminals:
                solver.add(prefix_weight + rank[terminal] - rank[graph.initial] <= -1)

    print(f"strict additive synthesis: period={''.join(map(str, period))} k={factor_width}")
    result = solver.check()
    print(f"solver={result}")
    if result != sat:
        return
    model = solver.model()
    certificate = {
        factor: str(model.eval(weight, model_completion=True))
        for factor, weight in weights.items()
    }
    print("weights=" + ",".join(
        f"{''.join(map(str, factor))}:{value}"
        for factor, value in certificate.items()
        if value != "0"
    ))
    print("strict bounded-below additive ranking: FOUND")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--period", type=int, default=5, help="length of 0 followed by ones")
    parser.add_argument("--factor-width", type=int, default=2)
    parser.add_argument(
        "--candidates",
        help="comma-separated factors of the selected width (search filter only)",
    )
    parser.add_argument("--synthesize-strict", action="store_true")
    parser.add_argument("--weight-bound", type=int, default=32)
    args = parser.parse_args()
    if args.period < 2 or args.factor_width < 1:
        parser.error("period must be at least 2 and factor width positive")
    candidates = None
    if args.candidates:
        candidates = tuple(tuple(map(int, factor)) for factor in args.candidates.split(","))
        if any(len(factor) != args.factor_width for factor in candidates):
            parser.error("every candidate must have factor-width digits")
    period = (0,) + (1,) * (args.period - 1)
    if args.synthesize_strict:
        synthesize_strict_additive(period, args.factor_width, args.weight_bound)
    else:
        greedy_ranking(period, args.factor_width, candidates)


if __name__ == "__main__":
    main()

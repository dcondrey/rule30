#!/usr/bin/env python3
"""Synthesize an all-length bounded-below potential for pull events.

For a normalized invariant queue ``R``, let ``V(R)`` be the sum of rational
weights of its width-``w`` factors after distinct left/right padding.  This
script asks for two finite weighted-automaton certificates:

1. every successful queue update satisfies

       V(R) - V(Q(R)) >= [R ends in 2 and R != (2,)];

2. the interior factor weights have no negative cycle on the invariant SFT.

The second condition makes ``V`` bounded below over queues of arbitrary
length.  Together the conditions would prove that every finite queue orbit
has only finitely many pulls.  The graphs below contain every word of every
length; satisfiability is therefore an all-length certificate, not a bounded
queue census.
"""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass

import z3

from constant_tail_language_cocycle import SFT_TRANSITIONS
from constant_tail_queue import LIFT_GENERATORS, SYMBOL_QUOTIENT


LEFT = 8
RIGHT = 9
Factor = tuple[int, ...]
Suffix = tuple[int, ...]
TransitionState = tuple[int, Suffix, Suffix, int, int]
BoundState = tuple[Suffix, int]


def shifted(suffix: Suffix, symbol: int, width: int) -> Suffix:
    if width == 1:
        return ()
    return (suffix + (symbol,))[-(width - 1) :]


def factor(suffix: Suffix, symbol: int) -> Factor:
    return suffix + (symbol,)


def initial_suffix(tail: int, width: int) -> Suffix:
    if width == 1:
        return ()
    return ((LEFT,) * (width - 1) + (tail,))[-(width - 1) :]


def initial_context(tail: int) -> int:
    # Tail 2 leaves the SFT automaton in its last-2 state.  Leading tail 3 is
    # a scan initializer outside the normalized interior alphabet.
    return 3 if tail == 2 else 0


def legal_boundary(last: int, scan: int) -> int | None:
    if last == 1 and scan == 0:
        return 2
    if last in (1, 2) and scan == 2:
        return 1
    return None


@dataclass(frozen=True, slots=True)
class Edge:
    source: TransitionState
    target: TransitionState
    source_factor: Factor
    output_factor: Factor


@dataclass(frozen=True, slots=True)
class Terminal:
    state: TransitionState
    source_trailer: tuple[Factor, ...]
    output_trailer: tuple[Factor, ...]
    pull: int


def transition_graph(
    tail: int, width: int
) -> tuple[TransitionState, tuple[Edge, ...], tuple[Terminal, ...]]:
    suffix = initial_suffix(tail, width)
    # The last entry is -1 until at least one interior symbol has been read;
    # the one-symbol queue (2,) is successful but is never a pull.
    start: TransitionState = (
        tail,
        suffix,
        suffix,
        initial_context(tail),
        -1,
    )
    found = {start}
    frontier = deque((start,))
    edges: list[Edge] = []
    while frontier:
        state = frontier.popleft()
        scan, source_suffix, output_suffix, context, _last = state
        for source_symbol in range(3):
            following_context = SFT_TRANSITIONS[context][source_symbol]
            if following_context == 4:
                continue
            following_scan = LIFT_GENERATORS[scan][source_symbol]
            output_symbol = SYMBOL_QUOTIENT[following_scan]
            following: TransitionState = (
                following_scan,
                shifted(source_suffix, source_symbol, width),
                shifted(output_suffix, output_symbol, width),
                following_context,
                source_symbol,
            )
            edges.append(
                Edge(
                    state,
                    following,
                    factor(source_suffix, source_symbol),
                    factor(output_suffix, output_symbol),
                )
            )
            if following not in found:
                found.add(following)
                frontier.append(following)

    terminals = []
    for state in found:
        scan, source_suffix, output_suffix, _context, last = state
        if last < 0:
            continue
        boundary = legal_boundary(last, scan)
        if boundary is None:
            continue

        source_trailer = []
        output_trailer = [factor(output_suffix, boundary)]
        output_suffix = shifted(output_suffix, boundary, width)
        for _ in range(width - 1):
            source_trailer.append(factor(source_suffix, RIGHT))
            output_trailer.append(factor(output_suffix, RIGHT))
            source_suffix = shifted(source_suffix, RIGHT, width)
            output_suffix = shifted(output_suffix, RIGHT, width)
        terminals.append(
            Terminal(
                state,
                tuple(source_trailer),
                tuple(output_trailer),
                int(last == 2),
            )
        )
    return start, tuple(edges), tuple(terminals)


def boundedness_graph(
    width: int,
) -> tuple[
    tuple[BoundState, ...],
    tuple[tuple[BoundState, BoundState, Factor], ...],
]:
    starts = tuple(
        (initial_suffix(tail, width), initial_context(tail))
        for tail in (2, 3)
    )
    found = set(starts)
    frontier = deque(starts)
    edges = []
    while frontier:
        source = frontier.popleft()
        suffix, context = source
        for symbol in range(3):
            following_context = SFT_TRANSITIONS[context][symbol]
            if following_context == 4:
                continue
            following = (shifted(suffix, symbol, width), following_context)
            edges.append((source, following, factor(suffix, symbol)))
            if following not in found:
                found.add(following)
                frontier.append(following)
    return tuple(found), tuple(edges)


def weight(
    item: Factor, weights: dict[Factor, z3.ArithRef]
) -> z3.ArithRef:
    if item not in weights:
        weights[item] = z3.Real("w_" + "_".join(map(str, item)))
    return weights[item]


def synthesize(width: int) -> tuple[z3.CheckSatResult, int, int, int]:
    weights: dict[Factor, z3.ArithRef] = {}
    solver = z3.SolverFor("QF_LRA")

    # A reduced-cost certificate on the invariant-word graph proves that no
    # interior factor cycle has negative total weight.  Consequently the
    # complete padded potential has a finite global lower bound.
    bound_states, bound_edges = boundedness_graph(width)
    bound_height = {
        state: z3.Real(f"b_{index}")
        for index, state in enumerate(bound_states)
    }
    for source, following, item in bound_edges:
        solver.add(
            weight(item, weights)
            + bound_height[source]
            - bound_height[following]
            >= 0
        )

    transition_states = 0
    transition_edges = 0
    terminal_count = 0
    for tail in (2, 3):
        start, edges, terminals = transition_graph(tail, width)
        states = {start}
        for edge in edges:
            states.add(edge.source)
            states.add(edge.target)
        height = {
            state: z3.Real(f"h_{tail}_{index}")
            for index, state in enumerate(states)
        }
        solver.add(height[start] == 0)
        for edge in edges:
            cost = weight(edge.source_factor, weights) - weight(
                edge.output_factor, weights
            )
            solver.add(cost + height[edge.source] - height[edge.target] >= 0)
        for terminal in terminals:
            trailer = z3.Sum(
                *(weight(item, weights) for item in terminal.source_trailer)
            ) - z3.Sum(
                *(weight(item, weights) for item in terminal.output_trailer)
            )
            solver.add(
                height[terminal.state] + trailer - terminal.pull >= 0
            )
        transition_states += len(states)
        transition_edges += len(edges)
        terminal_count += len(terminals)

    status = solver.check()
    print(
        f"width={width} status={status} weights={len(weights)} "
        f"bound-states={len(bound_states)} bound-edges={len(bound_edges)} "
        f"transition-states={transition_states} "
        f"transition-edges={transition_edges} terminals={terminal_count}",
        flush=True,
    )
    if status == z3.sat:
        model = solver.model()
        nonzero = []
        for item, variable in weights.items():
            value = model.eval(variable, model_completion=True)
            if value.numerator_as_long() != 0:
                nonzero.append((item, value))
        print(f"nonzero-weights={len(nonzero)}")
        for item, value in sorted(nonzero):
            print("  " + "".join(map(str, item)) + f": {value}")
    return status, transition_states, transition_edges, terminal_count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first-width", type=int, default=1)
    parser.add_argument("--last-width", type=int, default=8)
    args = parser.parse_args()
    if not 1 <= args.first_width <= args.last_width:
        parser.error("invalid width interval")
    for width in range(args.first_width, args.last_width + 1):
        status, _states, _edges, _terminals = synthesize(width)
        if status == z3.sat:
            break


if __name__ == "__main__":
    main()

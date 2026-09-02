#!/usr/bin/env python3
"""One exact rank-synthesis attempt for the TP3-011 residual language.

After the eleven-component defect vector stabilizes, the zero-tail dual word
avoids ``01``, ``11``, and ``220``.  This script asks for the most general
nonnegative additive rank carried by the four live states of that SFT and by
the current zero-branch phase ``d in {0,1}``:

    R_d(w) = constant[d]
             + sum edge_weight[d, s_i, w_i]
             + terminal_weight[d, s_final].

It requires ``R_d2(successor) <= R_d1(word)-1`` for every residual-language
word with two consecutive zero transitions of branch types ``d1,d2``.
Because every post-initial word begins with ``200`` or ``202``, the exact
finite product also retains that prefix.  Difference-graph potentials encode
the universal all-length inequality; this is not a word-length census.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from pathlib import Path
import sys

try:
    from z3 import Int, Solver, sat, unsat
except ImportError as error:  # pragma: no cover - dependency diagnostic
    raise SystemExit("z3-solver is required") from error

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from period3_011_zero_tail_dual import (  # noqa: E402
    BRANCH_BLOCK,
    BRANCH_SECTION,
    generator_action,
    word_action,
)


SFT_START = 0
SFT_AFTER_ZERO_OR_ONE = 1
SFT_SINGLE_TWO = 2
SFT_MULTIPLE_TWO = 3
SFT_DEAD = -1

# The four live states remember exactly the suffix needed to forbid
# 01, 11, and 220.  START is distinct only before the first symbol.
SFT_TRANSITIONS = (
    (SFT_AFTER_ZERO_OR_ONE, SFT_AFTER_ZERO_OR_ONE, SFT_SINGLE_TWO),
    (SFT_AFTER_ZERO_OR_ONE, SFT_DEAD, SFT_SINGLE_TWO),
    (SFT_AFTER_ZERO_OR_ONE, SFT_AFTER_ZERO_OR_ONE, SFT_MULTIPLE_TWO),
    (SFT_DEAD, SFT_AFTER_ZERO_OR_ONE, SFT_MULTIPLE_TWO),
)

ProductState = tuple[int, int, int, int]


def sft_step(state: int, symbol: int) -> int:
    if state not in range(4) or symbol not in range(3):
        raise ValueError("invalid SFT state or symbol")
    return SFT_TRANSITIONS[state][symbol]


def sft_prefix(symbols: tuple[int, ...]) -> int:
    state = SFT_START
    for symbol in symbols:
        state = sft_step(state, symbol)
        if state == SFT_DEAD:
            raise ValueError("forbidden factor in fixed prefix")
    return state


@dataclass(frozen=True)
class CaseGraph:
    prior_prefix: int
    first_branch: int
    second_branch: int
    initial: ProductState
    initial_symbols: tuple[tuple[int, int, int, int], ...]
    states: tuple[ProductState, ...]
    edges: dict[ProductState, tuple[tuple[ProductState, int, int], ...]]
    terminals: frozenset[ProductState]


def build_case(
    prior_prefix: int, first_branch: int, second_branch: int
) -> CaseGraph:
    """Build one exact useful product for a pair of zero transitions."""

    input_prefix = BRANCH_SECTION[prior_prefix]
    output_prefix = BRANCH_SECTION[first_branch]

    q1 = BRANCH_BLOCK[first_branch]
    q2, _unused = word_action(output_prefix, BRANCH_BLOCK[second_branch])
    input_state = sft_prefix(input_prefix)
    output_state = sft_prefix(output_prefix)

    # Each entry records (rank phase, SFT source, symbol, sign), where sign is
    # +1 for successor rank and -1 for source rank.
    initial_symbols: list[tuple[int, int, int, int]] = []
    state = SFT_START
    for symbol in output_prefix:
        initial_symbols.append((second_branch, state, symbol, 1))
        state = sft_step(state, symbol)
    state = SFT_START
    for symbol in input_prefix:
        initial_symbols.append((first_branch, state, symbol, -1))
        state = sft_step(state, symbol)

    # Process the fixed input prefix through both consecutive dual scans.
    for symbol in input_prefix:
        q1, emitted = generator_action(symbol, q1)
        q2, _next_emitted = generator_action(emitted, q2)
        initial_symbols.append((second_branch, output_state, emitted, 1))
        output_state = sft_step(output_state, emitted)
        if output_state == SFT_DEAD:
            raise AssertionError("fixed post-initial prefix left the residual SFT")

    initial = (q1, q2, input_state, output_state)
    reachable = {initial}
    queue = deque((initial,))
    raw_edges: dict[
        ProductState, list[tuple[ProductState, int, int]]
    ] = {}
    while queue:
        source = queue.popleft()
        source_q1, source_q2, source_input, source_output = source
        outgoing = []
        for symbol in range(3):
            following_input = sft_step(source_input, symbol)
            if following_input == SFT_DEAD:
                continue
            following_q1, emitted = generator_action(symbol, source_q1)
            following_output = sft_step(source_output, emitted)
            if following_output == SFT_DEAD:
                continue
            following_q2, _ = generator_action(emitted, source_q2)
            target = (
                following_q1,
                following_q2,
                following_input,
                following_output,
            )
            outgoing.append((target, symbol, emitted))
            if target not in reachable:
                reachable.add(target)
                queue.append(target)
        raw_edges[source] = outgoing

    raw_terminals = {
        state for state in reachable if state[0] == state[1] == 0
    }
    reverse: dict[ProductState, list[ProductState]] = {
        state: [] for state in reachable
    }
    for source, outgoing in raw_edges.items():
        for target, _symbol, _emitted in outgoing:
            reverse[target].append(source)
    useful = set(raw_terminals)
    queue = deque(raw_terminals)
    while queue:
        target = queue.popleft()
        for source in reverse[target]:
            if source not in useful:
                useful.add(source)
                queue.append(source)
    if initial not in useful:
        return CaseGraph(
            prior_prefix,
            first_branch,
            second_branch,
            initial,
            tuple(initial_symbols),
            (),
            {},
            frozenset(),
        )
    return CaseGraph(
        prior_prefix,
        first_branch,
        second_branch,
        initial,
        tuple(initial_symbols),
        tuple(sorted(useful)),
        {
            source: tuple(edge for edge in raw_edges[source] if edge[0] in useful)
            for source in useful
        },
        frozenset(raw_terminals & useful),
    )


def synthesize() -> tuple[str, dict[str, int], tuple[tuple[int, ...], ...]]:
    """Solve the bounded phase-aware additive-rank constraints exactly."""

    cases = tuple(
        build_case(prior, first, second)
        for prior in range(2)
        for first in range(2)
        for second in range(2)
    )
    solver = Solver()
    constants = tuple(Int(f"constant_{phase}") for phase in range(2))
    terminal = tuple(
        tuple(Int(f"terminal_{phase}_{state}") for state in range(4))
        for phase in range(2)
    )
    weights = tuple(
        tuple(
            tuple(Int(f"weight_{phase}_{state}_{symbol}") for symbol in range(3))
            for state in range(4)
        )
        for phase in range(2)
    )
    for variable in constants:
        solver.add(variable >= 0)
    for phase in range(2):
        for state in range(4):
            solver.add(terminal[phase][state] >= 0)
            for symbol in range(3):
                if sft_step(state, symbol) != SFT_DEAD:
                    solver.add(weights[phase][state][symbol] >= 0)

    state_counts = []
    for case_index, graph in enumerate(cases):
        state_counts.append(len(graph.states))
        if not graph.states:
            continue
        first = graph.first_branch
        second = graph.second_branch
        distance = {
            state: Int(f"distance_{case_index}_{index}")
            for index, state in enumerate(graph.states)
        }
        initial_delta = constants[second] - constants[first]
        for phase, state, symbol, sign in graph.initial_symbols:
            initial_delta += sign * weights[phase][state][symbol]
        solver.add(distance[graph.initial] == initial_delta)
        for source, outgoing in graph.edges.items():
            input_state = source[2]
            output_state = source[3]
            for target, symbol, emitted in outgoing:
                delta = (
                    weights[second][output_state][emitted]
                    - weights[first][input_state][symbol]
                )
                solver.add(distance[target] >= distance[source] + delta)
        for state in graph.terminals:
            final_delta = (
                terminal[second][state[3]] - terminal[first][state[2]]
            )
            solver.add(distance[state] + final_delta <= -1)

    result = solver.check()
    if result == unsat:
        return "UNSAT", {}, tuple(tuple(state_counts[i : i + 4]) for i in range(0, 8, 4))
    if result != sat:
        raise AssertionError(f"unexpected solver result: {result}")
    model = solver.model()
    assignment = {
        str(variable): model.eval(variable, model_completion=True).as_long()
        for variable in (
            *constants,
            *(item for row in terminal for item in row),
            *(item for phase in weights for row in phase for item in row),
        )
        if model.eval(variable, model_completion=True).as_long()
    }
    return "SAT", assignment, tuple(tuple(state_counts[i : i + 4]) for i in range(0, 8, 4))


def main() -> None:
    result, assignment, state_counts = synthesize()
    print(f"TP3-011 SFT-product phase-aware additive rank: {result}")
    print(f"useful product states by prior/first/second phase: {state_counts}")
    if assignment:
        for name, value in sorted(assignment.items()):
            print(f"{name}={value}")


if __name__ == "__main__":
    main()

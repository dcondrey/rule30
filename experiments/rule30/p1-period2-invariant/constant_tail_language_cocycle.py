#!/usr/bin/env python3
"""Exact regular-language cocycle for constant-tail queue mortality.

For tail ``c``, let ``L_h(c)`` be the normalized invariant queues that can
survive at least ``h`` further queue updates.  The reversed-diagonal queue is
a deterministic sequential transducer, so

    L_(h+1)(c) = Base(c) intersect Q_c^-1(L_h(c)).

This script constructs that regular preimage exactly, removes unreachable
states, minimizes the DFA, and reports its minimum accepted word length.  The
operator is uniform in ``h``.  Running it through a finite horizon is an audit
of the morphism and a falsifier for proposed rank recurrences, not a proof of
mortality for all horizons.

The key negative is visible immediately: minimized state count grows as
``4^(h+1)+1`` in the nontrivial range, while accepting states have Fibonacci
count.  Thus ordinary DFA rank expands rather than contracts.  The useful
candidate is the minimum accepted length; proving that it tends to infinity
would establish queue mortality.
"""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass

from constant_tail_queue import NORMALIZED_FORBIDDEN, SYMBOL_QUOTIENT
from peel_lift_monoid import LIFT_GENERATORS


Alphabet = range(3)


@dataclass(frozen=True, slots=True)
class DFA:
    transitions: tuple[tuple[int, int, int], ...]
    start: int
    accepting: frozenset[int]


# Suffix-context automaton for 20, 22, 011.  States are:
# default, last-0, suffix-01, last-2, dead.
SFT_TRANSITIONS: tuple[tuple[int, int, int], ...] = (
    (1, 0, 3),
    (1, 2, 3),
    (1, 4, 3),
    (4, 0, 4),
    (4, 4, 4),
)


def reachable_minimize(automaton: DFA) -> DFA:
    """Remove unreachable states and apply exact Moore minimization."""

    order = {automaton.start: 0}
    frontier = deque((automaton.start,))
    while frontier:
        state = frontier.popleft()
        for following in automaton.transitions[state]:
            if following not in order:
                order[following] = len(order)
                frontier.append(following)

    transitions = tuple(
        tuple(order[following] for following in automaton.transitions[state])
        for state in order
    )
    accepting = {
        order[state] for state in order if state in automaton.accepting
    }
    start = order[automaton.start]

    blocks = [accepting, set(range(len(transitions))) - accepting]
    blocks = [block for block in blocks if block]
    while True:
        block_index = {
            state: index for index, block in enumerate(blocks) for state in block
        }
        refined = []
        for block in blocks:
            groups: dict[tuple[int, int, int], set[int]] = {}
            for state in block:
                signature = tuple(
                    block_index[following] for following in transitions[state]
                )
                groups.setdefault(signature, set()).add(state)
            refined.extend(groups.values())
        if len(refined) == len(blocks):
            break
        blocks = refined

    block_index = {
        state: index for index, block in enumerate(blocks) for state in block
    }
    minimized = tuple(
        tuple(
            block_index[transitions[next(iter(block))][symbol]]
            for symbol in Alphabet
        )
        for block in blocks
    )
    return DFA(
        minimized,
        block_index[start],
        frozenset(block_index[state] for state in accepting),
    )


def base_language(tail: int) -> DFA:
    """Normalized invariant queues with a valid current endpoint boundary."""

    # The DFA reads the suffix after the fixed leading tail symbol.  Keep the
    # SFT context and the last queue symbol; last=3 means no suffix symbol has
    # been read in the tail-3 mode.
    states = tuple((context, last) for context in range(5) for last in range(4))
    index = {state: position for position, state in enumerate(states)}
    transitions = tuple(
        tuple(
            index[(SFT_TRANSITIONS[context][symbol], symbol)]
            for symbol in Alphabet
        )
        for context, _last in states
    )
    start_state = (3, 2) if tail == 2 else (0, 3)
    accepting = {
        index[(context, last)]
        for context in range(4)
        for last in (1, 2)
    }
    # The one-symbol queue (2) is a valid tail-2 boundary.
    if tail == 2:
        accepting.add(index[start_state])
    return reachable_minimize(
        DFA(transitions, index[start_state], frozenset(accepting))
    )


def emitted_boundary(last: int, final_scan_state: int) -> int | None:
    """Return B(next endpoint), or None when the hard-core decoder fails."""

    if last == 1:
        if final_scan_state == 0:
            return 2
        if final_scan_state == 2:
            return 1
        return None
    if last == 2 and final_scan_state == 2:
        return 1
    return None


def regular_preimage(target: DFA, tail: int) -> DFA:
    """Construct ``Base(tail) intersect Q_tail^-1(target)`` exactly."""

    base_start = (3, 2) if tail == 2 else (0, 3)
    start_tuple = (tail, target.start, *base_start)
    index = {start_tuple: 0}
    frontier = deque((start_tuple,))
    transitions: list[tuple[int, int, int]] = []
    accepting: set[int] = set()

    while frontier:
        scan_state, target_state, context, last = frontier.popleft()
        row = []
        for symbol in Alphabet:
            next_scan = LIFT_GENERATORS[scan_state][symbol]
            next_target = target.transitions[target_state][
                SYMBOL_QUOTIENT[next_scan]
            ]
            following = (
                next_scan,
                next_target,
                SFT_TRANSITIONS[context][symbol],
                symbol,
            )
            if following not in index:
                index[following] = len(index)
                frontier.append(following)
            row.append(index[following])
        transitions.append(tuple(row))  # type: ignore[arg-type]

        boundary = emitted_boundary(last, scan_state)
        if (
            context != 4
            and boundary is not None
            and target.transitions[target_state][boundary] in target.accepting
        ):
            accepting.add(index[(scan_state, target_state, context, last)])

    return reachable_minimize(
        DFA(tuple(transitions), 0, frozenset(accepting))
    )


def shortest_full_word(automaton: DFA, tail: int) -> tuple[int, ...] | None:
    """Return a shortest accepted queue, including its fixed leading tail."""

    frontier = deque((automaton.start,))
    parent: dict[int, tuple[int, int] | None] = {automaton.start: None}
    while frontier:
        state = frontier.popleft()
        if state in automaton.accepting:
            suffix = []
            while parent[state] is not None:
                previous, symbol = parent[state]
                suffix.append(symbol)
                state = previous
            return (tail,) + tuple(reversed(suffix))
        for symbol, following in enumerate(automaton.transitions[state]):
            if following not in parent:
                parent[following] = (state, symbol)
                frontier.append(following)
    return None


def fibonacci(index: int) -> int:
    left, right = 0, 1
    for _ in range(index):
        left, right = right, left + right
    return left


EXPECTED_MINIMUM = {
    2: (1, 1, 3, 5, 5, 5, 10, 10, 10),
    3: (2, 2, 3, 5, 5, 5, 10, 10, 10),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-horizon", type=int, default=6)
    args = parser.parse_args()
    if not 0 <= args.max_horizon <= 8:
        parser.error("max horizon must lie between 0 and 8")

    assert NORMALIZED_FORBIDDEN == ((2, 0), (2, 2), (0, 1, 1))
    for tail in (2, 3):
        automaton = base_language(tail)
        for horizon in range(args.max_horizon + 1):
            states = len(automaton.transitions)
            accepting = len(automaton.accepting)
            witness = shortest_full_word(automaton, tail)
            minimum = len(witness) if witness is not None else None
            if horizon == 0:
                assert states == (5 if tail == 2 else 6)
                assert accepting == 3
            else:
                assert states == 4 ** (horizon + 1) + 1
                assert accepting == fibonacci(horizon + 4)
            if horizon < len(EXPECTED_MINIMUM[tail]):
                assert minimum == EXPECTED_MINIMUM[tail][horizon]
            print(
                f"tail={tail} horizon={horizon:2d} states={states:6d} "
                f"accepting={accepting:4d} min-length={minimum} "
                f"w={''.join(map(str, witness)) if witness else '-'}"
            )
            if horizon < args.max_horizon:
                automaton = regular_preimage(automaton, tail)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact checks for the reconstructed-tail density and active-core routes.

Finite enumeration in this file is a falsifier, never a proof of the density
inequality.  The active-core conjugacy, on the other hand, is an exact word
identity: reversing a fixed-width aligned frontier turns one forced macro
into a four-carry subsequential transduction, one leading deep zero, and one
terminal shallow symbol.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass

from carry_transducer import (
    Carry,
    State,
    carry_step,
    forced_macro,
    parity_or,
    seed_state,
    terminal,
    wf_step,
    word_action,
)


def hard_core_words(length: int):
    """Yield chronological no-11 words as tuples."""

    def visit(prefix: tuple[int, ...]):
        if len(prefix) == length:
            yield prefix
            return
        yield from visit(prefix + (0,))
        if not prefix or prefix[-1] == 0:
            yield from visit(prefix + (1,))

    return visit(())


def append_macro(state: State, rho: int) -> tuple[State, tuple[int, int]]:
    """Append one seed bit and return the two new deepest left-tail bits."""
    old_depth = state[0]
    state = wf_step(state, 1 - rho)
    first = (state[1] >> old_depth) & 1
    old_depth = state[0]
    state = wf_step(state, 1)
    second = (state[1] >> old_depth) & 1
    return state, (first, second)


def density_enumeration(max_length: int) -> list[dict[str, object]]:
    frontier = [(0, (0, 0, 0), 0, 0)]
    rows: list[dict[str, object]] = []
    for length in range(1, max_length + 1):
        following = []
        for previous, state, weight, seed in frontier:
            for rho in (0, 1):
                if previous == rho == 1:
                    continue
                successor, emitted = append_macro(state, rho)
                following.append(
                    (
                        rho,
                        successor,
                        weight + sum(emitted),
                        seed | (rho << (length - 1)),
                    )
                )
        frontier = following
        minimum = min(item[2] for item in frontier)
        witnesses = [item[3] for item in frontier if item[2] == minimum]
        slack = 7 * minimum - 2 * length + 2
        if slack < 0:
            raise AssertionError(
                f"density counterexample n={length} seed={witnesses[0]:#x}"
            )
        rows.append(
            {
                "length": length,
                "words": len(frontier),
                "minimum_weight": minimum,
                "minimum_slack": slack,
                "witness_count": len(witnesses),
                "first_witness": min(witnesses),
            }
        )
    return rows


def cyclic_rule30(word: tuple[int, ...]) -> tuple[int, ...]:
    size = len(word)
    return tuple(
        word[(index - 1) % size]
        ^ (word[index] | word[(index + 1) % size])
        for index in range(size)
    )


def wallpaper_control() -> tuple[tuple[int, ...], ...]:
    rows = [(1, 0, 0, 0, 0, 0, 0)]
    for _ in range(4):
        rows.append(cyclic_rule30(rows[-1]))
    expected = (
        (1, 0, 0, 0, 0, 0, 0),
        (1, 1, 0, 0, 0, 0, 1),
        (0, 0, 1, 0, 0, 1, 1),
        (1, 1, 1, 1, 1, 1, 0),
        (1, 0, 0, 0, 0, 0, 0),
    )
    assert tuple(rows) == expected

    state: State = (0, 0, 0)
    emitted: list[int] = []
    for rho in (0, 1) * 14:
        state, pair = append_macro(state, rho)
        emitted.extend(pair)
    assert tuple(emitted[:28]) == tuple(
        int(index % 7 == 0) for index in range(28)
    )
    return tuple(rows)


def aligned_word(state: State) -> tuple[int, ...]:
    """The fixed-width aligned word, shallow to deep (including deep zeroes)."""
    depth, first, second = state
    return tuple(
        2 * ((first >> (index - 1)) & 1)
        + (
            ((depth - 1) & 1)
            if index == 1
            else ((second >> (index - 2)) & 1)
        )
        for index in range(1, depth + 1)
    )


def core_step(core: tuple[int, ...]) -> tuple[tuple[int, ...], Carry]:
    carry: Carry = (0, 0)
    output = []
    for symbol in core:
        carry, emitted = carry_step(carry, symbol)
        output.append(emitted)
    return tuple(output) + (terminal(carry),), carry


def strip_deep_zeroes(state: State) -> tuple[int, ...]:
    word = list(reversed(aligned_word(state)))
    while word and word[0] == 0:
        word.pop(0)
    return tuple(word)


def verify_core_conjugacy(max_seed_length: int) -> int:
    """Cross-check the exact reversed-word identity on reachable frontiers."""
    checked = 0
    for length in range(1, max_seed_length + 1):
        for bits in hard_core_words(length):
            seed = sum(bit << index for index, bit in enumerate(bits))
            state = seed_state(seed, length)
            successor = forced_macro(state)
            if successor is None:
                continue

            reversed_word = tuple(reversed(aligned_word(state)))
            transformed, carry = core_step(reversed_word)
            expected = (0,) + transformed
            assert tuple(reversed(aligned_word(successor))) == expected
            assert (carry[0] ^ carry[1]) == 1
            assert (1 ^ carry[0]) == (1 ^ parity_or(state))

            core = strip_deep_zeroes(state)
            successor_core, core_carry = core_step(core)
            assert core_carry == carry
            assert strip_deep_zeroes(successor) == successor_core
            assert core and core[-1] == 3
            assert successor_core[-1] == 3
            checked += 1
    return checked


@dataclass(frozen=True)
class ObserverEdge:
    source: tuple[object, ...]
    destination: tuple[object, ...]
    cost: int
    origin: tuple[int, int, int, State, tuple[int, int]]


def observer_negative_cycle(max_length: int = 16) -> list[ObserverEdge]:
    """Return a negative cycle in the registered phase/rho/D8 observer."""
    frontier = [(0, (0, 0, 0))]
    unique: dict[tuple[object, ...], ObserverEdge] = {}
    for length in range(max_length):
        following = []
        for previous, state in frontier:
            source = (length % 7, previous, word_action(state))
            for rho in (0, 1):
                if previous == rho == 1:
                    continue
                successor, emitted = append_macro(state, rho)
                destination = (
                    (length + 1) % 7,
                    rho,
                    word_action(successor),
                )
                cost = 7 * sum(emitted) - 2
                key = source, destination, cost
                unique.setdefault(
                    key,
                    ObserverEdge(
                        source,
                        destination,
                        cost,
                        (length, previous, rho, state, emitted),
                    ),
                )
                following.append((rho, successor))
        frontier = following

    edges = list(unique.values())
    nodes = {edge.source for edge in edges} | {
        edge.destination for edge in edges
    }
    distance = {node: 0 for node in nodes}
    predecessor: dict[tuple[object, ...], ObserverEdge] = {}
    changed: tuple[object, ...] | None = None
    for _ in range(len(nodes)):
        changed = None
        for edge in edges:
            candidate = distance[edge.source] + edge.cost
            if candidate < distance[edge.destination]:
                distance[edge.destination] = candidate
                predecessor[edge.destination] = edge
                changed = edge.destination
        if changed is None:
            raise AssertionError("registered observer unexpectedly has no negative cycle")
    assert changed is not None
    cursor = changed
    for _ in range(len(nodes)):
        cursor = predecessor[cursor].source
    cycle = []
    start = cursor
    while True:
        edge = predecessor[cursor]
        cycle.append(edge)
        cursor = edge.source
        if cursor == start:
            break
    cycle.reverse()
    assert all(
        left.destination == right.source
        for left, right in zip(cycle, cycle[1:] + cycle[:1])
    )
    assert sum(edge.cost for edge in cycle) < 0
    return cycle


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=24)
    parser.add_argument("--core-max-seed", type=int, default=12)
    args = parser.parse_args()

    rows = density_enumeration(args.max_length)
    print("n words min-weight min-slack witnesses first")
    for row in rows:
        print(
            f"{row['length']:2d} {row['words']:7d} "
            f"{row['minimum_weight']:2d} {row['minimum_slack']:2d} "
            f"{row['witness_count']:4d} {row['first_witness']:#x}"
        )

    wallpaper_control()
    print("period-7 / time-4 wallpaper and sparse-phase alignment: PASS")

    core_checks = verify_core_conjugacy(args.core_max_seed)
    print(f"active-core conjugacy: {core_checks} reachable macros PASS")

    cycle = observer_negative_cycle()
    weights = Counter(edge.cost for edge in cycle)
    print(
        "phase/rho/D8 observer: exact negative cycle "
        f"length={len(cycle)} cost={sum(edge.cost for edge in cycle)} "
        f"weights={dict(sorted(weights.items()))}"
    )
    for edge in cycle:
        length, previous, rho, state, emitted = edge.origin
        print(
            f"  n={length} previous={previous} rho={rho} "
            f"state={state} emitted={emitted} cost={edge.cost}"
        )


if __name__ == "__main__":
    main()

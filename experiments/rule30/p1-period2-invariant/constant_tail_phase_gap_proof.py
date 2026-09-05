#!/usr/bin/env python3
"""All-length finite-state proof of the phase-gap retreat cover."""

from __future__ import annotations

from collections import deque

from constant_tail_language_cocycle import (
    DFA,
    SFT_TRANSITIONS,
    emitted_boundary,
    reachable_minimize,
    regular_preimage,
)
from constant_tail_queue import LIFT_GENERATORS, SYMBOL_QUOTIENT


Vector = tuple[int, ...]
ProductState = tuple[int, ...]


def dangerous_predecessor_dfa() -> DFA:
    """Read the suffix of `P = 211 ([12]1[12]1)*` after fixed tail 2."""

    # Raw states 0..5 recognize `11 ([12]1[12]1)*`; state 6 is dead.
    transitions = (
        (6, 1, 6),
        (6, 2, 6),
        (6, 3, 3),
        (6, 4, 6),
        (6, 5, 5),
        (6, 2, 6),
        (6, 6, 6),
    )
    return reachable_minimize(
        DFA(transitions, 0, frozenset((2,)))
    )


def zero_free_pair_graph(tail: int):
    """Build `(scan(p),scan(q),last(p))` while reading zero-free `p`."""

    start = (tail, tail, tail)
    reachable = {start}
    frontier = deque((start,))
    edges = []
    while frontier:
        scan_p, scan_q, previous = frontier.popleft()
        for source in (1, 2):
            if previous == source == 2:
                continue
            next_p = LIFT_GENERATORS[scan_p][source]
            if next_p == 0:
                # Then q has a zero inherited coordinate.
                continue
            emitted = SYMBOL_QUOTIENT[next_p]
            next_q = LIFT_GENERATORS[scan_q][emitted]
            following = (next_p, next_q, source)
            edges.append(((scan_p, scan_q, previous), source, emitted, following))
            if following not in reachable:
                reachable.add(following)
                frontier.append(following)

    accepting = {
        state
        for state in reachable
        if state[0] == 2 and LIFT_GENERATORS[state[1]][1] == 0
    }
    return start, reachable, tuple(edges), frozenset(accepting)


def classification_control() -> tuple[int, int]:
    """Prove the exact language of a zero-free pair ending in a retreat."""

    start3, reachable3, _edges3, accepting3 = zero_free_pair_graph(3)
    assert start3 in reachable3 and len(reachable3) == 1 and not accepting3

    start, reachable, edges, accepting = zero_free_pair_graph(2)
    target = (2, 3, 1)
    assert accepting == frozenset((target,))
    assert len(reachable) == 9

    coaccessible = set(accepting)
    changed = True
    while changed:
        changed = False
        for source_state, _source, _emitted, following in edges:
            if following in coaccessible and source_state not in coaccessible:
                coaccessible.add(source_state)
                changed = True
    assert len(coaccessible) == 7
    useful = tuple(
        edge
        for edge in edges
        if edge[0] in coaccessible and edge[3] in coaccessible
    )
    assert len(useful) == 9

    # Every accepting path starts with source/output `11/12` and thereafter
    # returns to the unique accepting state in four-coordinate loops.
    first_paths = tuple(
        (source, emitted, following)
        for state, source, emitted, following in useful
        if state == start
    )
    assert first_paths == ((1, 1, (1, 1, 1)),)
    second_paths = tuple(
        (source, emitted, following)
        for state, source, emitted, following in useful
        if state == (1, 1, 1) and following == target
    )
    assert second_paths == ((1, 2, target),)

    adjacency: dict[tuple[int, int, int], list[tuple[int, int, tuple[int, int, int]]]] = {}
    for state, source, emitted, following in useful:
        adjacency.setdefault(state, []).append((source, emitted, following))

    returns = []

    def visit(
        state: tuple[int, int, int],
        source_word: Vector,
        output_word: Vector,
    ) -> None:
        if state == target and source_word:
            returns.append((source_word, output_word))
            return
        assert len(source_word) < 4
        for source, emitted, following in adjacency.get(state, ()):
            visit(
                following,
                source_word + (source,),
                output_word + (emitted,),
            )

    for source, emitted, following in adjacency[target]:
        visit(following, (source,), (emitted,))
    assert set(returns) == {
        (tuple(map(int, source)), (1, 2, 1, 2))
        for source in ("1111", "1121", "2111", "2121")
    }
    # Hence p=211([12]1[12]1)* and q=2.12(1212)*.1=(2121)+.
    return len(reachable), len(useful)


def direct_nested_preimage_final_count(target: DFA, depth: int) -> tuple[int, int]:
    """Independent unminimized product for `Base(2) intersect Q^-depth(target)`."""

    if depth < 1:
        raise ValueError("depth must be positive")
    # scans, target state, SFT context, last source symbol
    start: ProductState = (2,) * depth + (target.start, 3, 2)
    index = {start: 0}
    frontier = deque((start,))
    finals = 0
    while frontier:
        state = frontier.popleft()
        scans = list(state[:depth])
        target_state, context, last = state[depth:]
        if context != 4:
            terminal_scans = scans[:]
            terminal_target = target_state
            terminal_last = last
            valid = True
            for level in range(depth):
                boundary = emitted_boundary(
                    terminal_last, terminal_scans[level]
                )
                if boundary is None:
                    valid = False
                    break
                emitted = boundary
                for higher in range(level + 1, depth):
                    terminal_scans[higher] = LIFT_GENERATORS[
                        terminal_scans[higher]
                    ][emitted]
                    emitted = SYMBOL_QUOTIENT[terminal_scans[higher]]
                terminal_target = target.transitions[terminal_target][emitted]
                terminal_last = boundary
            if valid and terminal_target in target.accepting:
                finals += 1

        for source in range(3):
            emitted = source
            following_scans = []
            for scan in scans:
                next_scan = LIFT_GENERATORS[scan][emitted]
                following_scans.append(next_scan)
                emitted = SYMBOL_QUOTIENT[next_scan]
            following_target = target.transitions[target_state][emitted]
            following = tuple(following_scans) + (
                following_target,
                SFT_TRANSITIONS[context][source],
                source,
            )
            if following not in index:
                index[following] = len(index)
                frontier.append(following)
    return len(index), finals


def preimage_controls() -> tuple[tuple[int, int], ...]:
    target = dangerous_predecessor_dfa()
    first = regular_preimage(target, 2)
    second = regular_preimage(first, 2)
    assert (len(target.transitions), len(target.accepting)) == (6, 1)
    assert (len(first.transitions), len(first.accepting)) == (20, 2)
    assert (len(second.transitions), len(second.accepting)) == (1, 0)

    direct = tuple(
        direct_nested_preimage_final_count(target, depth)
        for depth in (1, 2)
    )
    assert direct[0][1] > 0
    assert direct[1][1] == 0
    return direct


def retreat_boundary_control() -> int:
    checked = 0
    for last in (1, 2):
        for final_scan in range(4):
            boundary = emitted_boundary(last, final_scan)
            retreat = boundary == 2
            assert retreat == (last == 1 and final_scan == 0)
            if retreat:
                # The final inherited output is zero and the append is two.
                assert SYMBOL_QUOTIENT[final_scan] == 0
            checked += 1
    return checked


def main() -> None:
    boundary_cases = retreat_boundary_control()
    states, useful_edges = classification_control()
    direct = preimage_controls()
    print(
        f"retreat decoder and nonconsecutivity: {boundary_cases} terminal cases PASS"
    )
    print(
        "zero-free dangerous pair: tail 3 empty; tail 2 "
        f"states={states}, coaccessible-edges={useful_edges}, "
        "P=211([12]1[12]1)* and q=(2121)+ PASS"
    )
    print(
        "dangerous predecessor basin: minimized states/accepting "
        "6/1 -> 20/2 -> 1/0 PASS"
    )
    print(
        "independent nested products: "
        + ", ".join(
            f"depth={depth} reachable={reachable} finals={finals}"
            for depth, (reachable, finals) in enumerate(direct, start=1)
        )
        + " PASS"
    )
    print(
        "THEOREM: one boundary credit plus phase-labelled zero blocks at "
        "times t-1/t injectively covers every retreat"
    )


if __name__ == "__main__":
    main()

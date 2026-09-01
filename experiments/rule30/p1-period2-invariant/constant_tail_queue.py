#!/usr/bin/env python3
"""Exact growing queue cocycle for the two constant inverse-cut tails.

Let ``D_m`` be the right-edge diagonal of the inverse-terminal triangle after
an endpoint word of length ``m`` has been read, so its final cell is the newly
exposed inverse-cut symbol.  Appending endpoint symbol ``q`` gives

    D'0 = B(q)
    D'1 = phi(previous_endpoint, D'0)
    D'k = phi(D[k-2], D'[k-1])  (2 <= k <= m).

If the final cut symbol is fixed to ``c`` and the diagonal is reversed to a
queue ``R``, right-permutivity turns this growing formula into a prefix scan:

    S0 = c
    Si = g_(S[i-1])(R[i])
    R' = S . B(next_endpoint).

The last scan state uniquely decodes the next endpoint symbol.  Requiring it
to be hard-core makes this a deterministic partial map.  Thus a hard-core
endpoint over an eventually constant cut tail would give an immortal orbit
of this queue map.

The conjugacy and hard-core decoder below are uniform.  The arbitrary-queue
census is only a bounded falsifier for the stronger queue-mortality theorem;
it is not an induction over queue length.
"""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
from itertools import product

from dyadic_periodicity_analyzer import BOUNDARY, cone_local, inverse_cone_diagonal
from peel_lift_monoid import LIFT_GENERATORS


Vector = tuple[int, ...]
SYMBOL_QUOTIENT = (0, 1, 2, 1)
NORMALIZED_FORBIDDEN = ((2, 0), (2, 2), (0, 1, 1))


def append_diagonal(
    diagonal: Vector, previous_endpoint: int, endpoint: int
) -> Vector:
    """Update the complete right-edge formula after appending ``endpoint``."""

    following = [BOUNDARY[endpoint]]
    if not diagonal:
        return tuple(following)
    following.append(cone_local(previous_endpoint, following[0]))
    for index in range(2, len(diagonal) + 1):
        following.append(
            cone_local(diagonal[index - 2], following[index - 1])
        )
    return tuple(following)


def diagonal_from_endpoint(endpoint: Vector) -> Vector:
    diagonal: Vector = ()
    previous = 0
    for symbol in endpoint:
        diagonal = append_diagonal(diagonal, previous, symbol)
        previous = symbol
    return diagonal


def forced_endpoint(
    diagonal: Vector, previous_endpoint: int, tail: int
) -> tuple[int, Vector]:
    """Append the unique endpoint symbol exposing final cut symbol ``tail``."""

    candidates = tuple(
        (symbol, following)
        for symbol in range(4)
        if (following := append_diagonal(diagonal, previous_endpoint, symbol))[-1]
        == tail
    )
    assert len(candidates) == 1
    return candidates[0]


def hard_core_pair(previous: int, following: int) -> bool:
    return following in (1, 2) and not (previous == following == 1)


def normalize_queue(queue: Vector, tail: int) -> Vector:
    """Collapse scan-indistinguishable input symbols 1 and 3.

    The leading tail symbol initializes the scan and is not read as input, so
    it remains ``tail`` even when ``tail == 3``.
    """

    if not queue or queue[0] != tail:
        raise ValueError("a reversed diagonal must begin with its tail symbol")
    return (tail,) + tuple(SYMBOL_QUOTIENT[symbol] for symbol in queue[1:])


@dataclass(frozen=True, slots=True)
class QueueStep:
    queue: Vector
    endpoint: int
    final_scan_state: int


def queue_step(queue: Vector, tail: int) -> QueueStep | None:
    """Apply one constant-tail update, rejecting a non-hard-core endpoint."""

    if tail not in (2, 3):
        raise ValueError("the first-infinite-tail modes are exactly 2 and 3")
    if not queue or queue[0] != tail:
        raise ValueError("a reversed diagonal must begin with its tail symbol")
    if queue[-1] not in (1, 2):
        return None

    # The final reversed-diagonal cell is B(previous_endpoint).  On the
    # hard-core alphabet B interchanges states 1 and 2.
    previous_endpoint = 3 - queue[-1]
    state = tail
    scan = [tail]
    for symbol in queue[1:]:
        state = LIFT_GENERATORS[state][symbol]
        scan.append(state)

    candidates = tuple(
        endpoint
        for endpoint in range(4)
        if cone_local(previous_endpoint, BOUNDARY[endpoint]) == state
    )
    assert len(candidates) == 1
    endpoint = candidates[0]
    if not hard_core_pair(previous_endpoint, endpoint):
        return None
    return QueueStep(tuple(scan) + (BOUNDARY[endpoint],), endpoint, state)


def literal_controls(max_endpoint_length: int) -> tuple[int, int]:
    """Match the queue scan to the full inverse-cone triangle on all words."""

    diagonal_checked = 0
    queue_checked = 0
    for length in range(1, max_endpoint_length + 1):
        for endpoint in product(range(4), repeat=length):
            diagonal = diagonal_from_endpoint(endpoint)
            assert tuple(
                diagonal_from_endpoint(endpoint[: index + 1])[-1]
                for index in range(length)
            ) == inverse_cone_diagonal(endpoint)
            diagonal_checked += 1
            if endpoint[-1] not in (1, 2):
                continue
            for tail in (2, 3):
                if diagonal[-1] != tail:
                    continue
                following_endpoint, following_diagonal = forced_endpoint(
                    diagonal, endpoint[-1], tail
                )
                scanned = queue_step(tuple(reversed(diagonal)), tail)
                if hard_core_pair(endpoint[-1], following_endpoint):
                    assert scanned is not None
                    assert scanned.endpoint == following_endpoint
                    assert scanned.queue == tuple(reversed(following_diagonal))
                else:
                    assert scanned is None
                queue_checked += 1
    return diagonal_checked, queue_checked


def quotient_controls(max_length: int = 7) -> int:
    """Verify that ``3 -> 1`` exactly semiconjugates every queue update."""

    assert all(
        LIFT_GENERATORS[state][1] == LIFT_GENERATORS[state][3]
        for state in range(4)
    )
    checked = 0
    for tail in (2, 3):
        for length in range(1, max_length + 1):
            if length == 1:
                words = ((tail,),) if tail in (1, 2) else ()
            else:
                words = (
                    (tail,) + middle + (last,)
                    for middle in product(range(4), repeat=length - 2)
                    for last in (1, 2)
                )
            for queue in words:
                normalized = normalize_queue(queue, tail)
                literal = queue_step(queue, tail)
                quotient = queue_step(normalized, tail)
                assert (literal is None) == (quotient is None)
                if literal is not None:
                    assert quotient is not None
                    assert literal.endpoint == quotient.endpoint
                    assert literal.final_scan_state == quotient.final_scan_state
                    assert literal.queue == quotient.queue
                checked += 1
    return checked


def image_sft_automaton_control() -> int:
    """Prove the normalized scan image avoids exactly 20, 22, and 011.

    Subset determinization of the four scan states gives the five-state DFA
    below (including the dead state).  It is exactly the suffix automaton for
    the three displayed forbidden factors, so this is an all-word graph
    identity rather than a bounded factor census.
    """

    adjacency = {
        state: {
            LIFT_GENERATORS[state][symbol] for symbol in range(3)
        }
        for state in range(4)
    }

    def advance(states: frozenset[int], label: int) -> frozenset[int]:
        return frozenset(
            following
            for state in states
            for following in adjacency[state]
            if SYMBOL_QUOTIENT[following] == label
        )

    start = frozenset(range(4))
    zero = frozenset((0,))
    one = frozenset((1, 3))
    zero_one = frozenset((3,))
    two = frozenset((2,))
    dead = frozenset()
    expected = {
        start: (zero, one, two),
        one: (zero, one, two),
        zero: (zero, zero_one, two),
        zero_one: (zero, dead, two),
        two: (dead, one, dead),
        dead: (dead, dead, dead),
    }
    assert all(
        tuple(advance(state, label) for label in range(3)) == transitions
        for state, transitions in expected.items()
    )

    # Independently close the reachable subset construction and ensure that
    # the expected table contains every nondead state.
    found = {start}
    frontier = deque((start,))
    while frontier:
        state = frontier.popleft()
        for label in range(3):
            following = advance(state, label)
            if following and following not in found:
                found.add(following)
                frontier.append(following)
    assert found == {start, zero, one, zero_one, two}

    # The hard-core boundary append is 2 after final state 0 and 1 after
    # final state 2.  Check that it preserves the same forbidden-factor DFA
    # at the only possible terminal transitions.
    terminal_triples = {
        (SYMBOL_QUOTIENT[before], SYMBOL_QUOTIENT[final], boundary)
        for final, boundary in ((0, 2), (2, 1))
        for before in range(4)
        for symbol in range(3)
        if LIFT_GENERATORS[before][symbol] == final
    }
    assert terminal_triples == {(0, 0, 2), (1, 0, 2), (0, 2, 1), (1, 2, 1)}
    assert all(
        tuple(word[index : index + len(factor)]) != factor
        for word in terminal_triples
        for factor in NORMALIZED_FORBIDDEN
        for index in range(len(word) - len(factor) + 1)
    )
    return len(expected)


def lifetime(queue: Vector, tail: int, cap: int) -> int | None:
    """Return successful updates before failure, or ``None`` at the cap."""

    for step in range(cap):
        following = queue_step(queue, tail)
        if following is None:
            return step
        queue = normalize_queue(following.queue, tail)
    return None


EXPECTED_MAXIMA = {
    2: (1, 0, 2, 2, 5, 4, 3, 5, 4, 9, 8, 8, 9, 9, 9),
    3: (None, 1, 2, 1, 5, 4, 3, 4, 5, 8, 7, 10, 9, 10, 11),
}


def arbitrary_queue_census(length: int, tail: int, cap: int):
    """Maximize lifetime over every queue with the required two boundaries."""

    maximum = -1
    witness: Vector = ()
    capped: Vector | None = None
    if length == 1:
        words = ((tail,),) if tail in (1, 2) else ()
    else:
        # Every four-symbol middle word has exactly the same future as its
        # 3->1 normalization, so the ternary representatives are exhaustive.
        words = (
            (tail,) + middle + (last,)
            for middle in product(range(3), repeat=length - 2)
            for last in (1, 2)
        )
    count = 0
    for queue in words:
        count += 1
        survival = lifetime(queue, tail, cap)
        if survival is None:
            capped = queue
            break
        if survival > maximum:
            maximum = survival
            witness = queue
    return count, maximum, witness, capped


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--control-length", type=int, default=7)
    parser.add_argument("--max-queue-length", type=int, default=10)
    parser.add_argument("--orbit-cap", type=int, default=1000)
    args = parser.parse_args()
    if (
        args.control_length < 1
        or args.max_queue_length < 1
        or args.orbit_cap < 1
    ):
        parser.error("all bounds must be positive")

    diagonal_checked, queue_checked = literal_controls(args.control_length)
    print(
        "right-edge diagonal controls: "
        f"{diagonal_checked} arbitrary endpoint words PASS"
    )
    print(f"reversed constant-tail queue controls: {queue_checked} PASS")
    quotient_checked = quotient_controls()
    print(f"exact 3->1 queue quotient controls: {quotient_checked} PASS")
    image_states = image_sft_automaton_control()
    print(
        "normalized successor language: "
        f"{image_states}-state DFA forbids 20,22,011 PASS"
    )
    for length in range(1, args.max_queue_length + 1):
        fields = []
        for tail in (2, 3):
            count, maximum, witness, capped = arbitrary_queue_census(
                length, tail, args.orbit_cap
            )
            expected = (
                EXPECTED_MAXIMA[tail][length - 1]
                if length <= len(EXPECTED_MAXIMA[tail])
                else "unrecorded"
            )
            if expected is not None and expected != "unrecorded":
                assert capped is None and maximum == expected
            fields.append(
                f"tail={tail} words={count} max={maximum} "
                f"w={''.join(map(str, witness)) or '-'} "
                f"capped={''.join(map(str, capped)) if capped else '-'}"
            )
        print(f"length={length:2d} " + " | ".join(fields))


if __name__ == "__main__":
    main()

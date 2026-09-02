#!/usr/bin/env python3
"""All-length rightmost-pivot rewrite and pull/retreat controls."""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass

from constant_tail_origin_prefix_hall import feature_starts
from constant_tail_queue import (
    LIFT_GENERATORS,
    SYMBOL_QUOTIENT,
    Vector,
    normalize_queue,
    queue_step,
)
from constant_tail_retreat_budget import invariant_queues


def equal_edges(scan: int) -> tuple[tuple[int, int], ...]:
    """Return input/next-scan edges whose normalized output is unchanged."""

    return tuple(
        (symbol, following)
        for symbol in range(3)
        if SYMBOL_QUOTIENT[
            following := LIFT_GENERATORS[scan][symbol]
        ]
        == symbol
    )


def legal_boundary(last: int, scan: int) -> int | None:
    """Decode the appended normalized boundary, or reject the scan."""

    if last == 1 and scan == 0:
        return 2
    if last in (1, 2) and scan == 2:
        return 1
    return None


def suffix_language_control() -> tuple[int, int]:
    """Prove the complete legal equality suffixes after a changed pivot."""

    # A changed input 1 can emit only normalized 0/raw 0 or normalized 2/raw
    # 2.  Starting from either raw state, close every equality edge.  States
    # 1 and 3 have no outgoing equality edge, so the useful graph is finite
    # apart from the raw-0 zero loop.
    assert tuple(
        (scan, LIFT_GENERATORS[scan][1])
        for scan in range(4)
        if SYMBOL_QUOTIENT[LIFT_GENERATORS[scan][1]] != 1
    ) == ((1, 2), (3, 0))
    assert equal_edges(0) == ((0, 0), (1, 3), (2, 2))
    assert equal_edges(1) == ()
    assert equal_edges(2) == ((1, 1),)
    assert equal_edges(3) == ()

    # Quotient the only unbounded loop by remembering whether at least one
    # zero has been read.  Exhausting this graph proves that the legal suffix
    # language is empty or 0*2 after raw pivot state 0, and only empty after
    # raw pivot state 2.
    accepted = set()
    reachable = set()
    frontier = deque()
    for pivot_scan in (0, 2):
        state = (pivot_scan, pivot_scan, "")
        reachable.add(state)
        frontier.append(state)
    while frontier:
        pivot_scan, scan, shape = frontier.popleft()
        if shape == "":
            last = 1
        elif shape == "0*":
            last = 0
        else:
            last = int(shape[-1])
        boundary = legal_boundary(last, scan)
        if boundary is not None:
            accepted.add((pivot_scan, shape, scan, boundary))

        for symbol, following in equal_edges(scan):
            if shape == "":
                if symbol == 0:
                    next_shape = "0*"
                elif symbol == 2:
                    next_shape = "0*2"
                else:
                    next_shape = "1"
            elif shape == "0*" and symbol == 0:
                next_shape = "0*"
            elif shape == "0*" and symbol == 2:
                next_shape = "0*2"
            else:
                next_shape = shape + str(symbol)
            state = (pivot_scan, following, next_shape)
            if state not in reachable:
                reachable.add(state)
                frontier.append(state)

    expected = {
        (0, "", 0, 2),
        (0, "0*2", 2, 1),
        (2, "", 2, 1),
    }
    assert accepted == expected, (accepted, expected)
    return len(reachable), len(accepted)


@dataclass(slots=True)
class OrbitCensus:
    queues: int = 0
    updates: int = 0
    retreats: int = 0
    pulls: int = 0
    productive_pulls: int = 0
    pull_hall_failures: int = 0
    temporal_hall_failures: int = 0
    minimum_pull_delta: int = 10**9
    first_failure: str | None = None


def audit_orbit(queue: Vector, tail: int, cap: int, census: OrbitCensus) -> None:
    initial = queue
    origins = list(range(len(queue)))
    starts = feature_starts(queue)
    retreat_origins = []
    pull_origins = []
    pull_indices = []
    pending_pull: int | None = None
    productive_pulls = 0

    for _time in range(cap):
        following = queue_step(queue, tail)
        if following is None:
            break
        inherited = normalize_queue(following.queue[:-1], tail)
        differences = tuple(
            index
            for index in range(1, len(queue))
            if inherited[index] != queue[index]
        )
        if differences:
            pivot = differences[-1]
            assert queue[pivot] == 1
            origin = origins[pivot]
        else:
            assert queue == (2,)
            pivot = 0
            origin = 0

        successor = normalize_queue(following.queue, tail)
        origins.append(origin)
        retreat = successor[-1] == 2
        pull = queue[-1] == 2 and queue != (2,)

        if retreat:
            assert pivot == len(queue) - 1
            assert queue[pivot:] == (1,)
            assert successor[pivot:] == (0, 2)
            retreat_origins.append(origin)
            census.retreats += 1
            if pending_pull is not None:
                assert pending_pull == origin
                census.productive_pulls += 1
                productive_pulls += 1
                pending_pull = None
        elif pull:
            suffix = queue[pivot:]
            assert suffix[0] == 1 and suffix[-1] == 2
            assert all(symbol == 0 for symbol in suffix[1:-1])
            assert successor[pivot:] == (0,) * (len(suffix) - 1) + (2, 1)
            pull_origins.append(origin)
            if pull_indices:
                census.minimum_pull_delta = min(
                    census.minimum_pull_delta, pivot - pull_indices[-1]
                )
            pull_indices.append(pivot)
            pending_pull = origin
            census.pulls += 1
        else:
            if queue == (2,):
                assert successor == (2, 1)
            else:
                assert queue[-1] == 1
                assert pivot == len(queue) - 1
                assert queue[pivot:] == (1,)
                assert successor[pivot:] == (2, 1)
                if pending_pull is not None:
                    assert origin == pending_pull

        queue = successor
        census.updates += 1
    else:
        raise AssertionError("orbit reached the audit cap")

    # Every retreat is either the first retreat descended from the initial
    # terminal 1, or is paired with the unique preceding productive pull.
    initial_credit = int(initial[-1] == 1)
    assert len(retreat_origins) <= productive_pulls + initial_credit

    for rank, origin in enumerate(sorted(pull_origins), start=1):
        if sum(start <= origin for start in starts) < rank:
            census.pull_hall_failures += 1
            census.first_failure = census.first_failure or (
                f"pull Hall tail={tail} R={''.join(map(str, initial))} "
                f"pulls={pull_origins} starts={starts}"
            )
            break
    for rank, origin in enumerate(retreat_origins, start=1):
        if sum(start <= origin for start in starts) < rank:
            census.temporal_hall_failures += 1
            census.first_failure = census.first_failure or (
                f"temporal Hall tail={tail} R={''.join(map(str, initial))} "
                f"retreats={retreat_origins} starts={starts}"
            )
            break
    census.queues += 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-length", type=int, default=14)
    parser.add_argument("--orbit-cap", type=int, default=1_000)
    args = parser.parse_args()
    if args.max_length < 1 or args.orbit_cap < 1:
        parser.error("bounds must be positive")

    states, finals = suffix_language_control()
    print(
        f"equality-suffix product states={states} legal-finals={finals}: "
        "A:1->02, B:1->21, C:10^m2->0^(m+1)21 PROVED"
    )
    census = OrbitCensus()
    for length in range(1, args.max_length + 1):
        for tail in (2, 3):
            for queue in invariant_queues(length, tail):
                audit_orbit(queue, tail, args.orbit_cap, census)
    print(
        f"orbit regression queues={census.queues} updates={census.updates} "
        f"retreats={census.retreats} pulls={census.pulls} "
        f"productive-pulls={census.productive_pulls} "
        f"minimum-pull-delta={census.minimum_pull_delta} "
        f"pull-Hall-failures={census.pull_hall_failures} "
        f"temporal-Hall-failures={census.temporal_hall_failures}"
    )
    print(f"first failure: {census.first_failure or 'none'}")


if __name__ == "__main__":
    main()

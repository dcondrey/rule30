#!/usr/bin/env python3
"""Falsifiers and a stored counterexample for pull-root coordinate depth.

The proposed all-length theorem was that a successful pull node of depth h
and positive initial root r satisfies r >= 2*h-1.  It is false.  The stored
tail-3 queue ``3001 0^382 2`` reaches depth three from root three.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from typing import Iterator

from constant_tail_language_cocycle import SFT_TRANSITIONS
from constant_tail_mixed_run_budget import weighted_invariant_queue
from constant_tail_origin_prefix_hall import feature_starts
from constant_tail_queue import Vector, normalize_queue, queue_step
from constant_tail_retreat_budget import invariant_queues, random_invariant_queue


FEATURE_COUNTEREXAMPLE = tuple(
    map(
        int,
        "30000000000000000000000000000001"
        "000000000000000000000000000000000000000000002",
    )
)
COORDINATE_COUNTEREXAMPLE = (3, 0, 0, 1) + (0,) * 382 + (2,)


@dataclass(slots=True)
class Census:
    queues: int = 0
    updates: int = 0
    pulls: int = 0
    maximum_depth: int = 0
    coordinate_failures: int = 0
    feature_failures: int = 0
    capped: int = 0
    minimum_coordinate_slack: int = 10**9
    first_coordinate_failure: str | None = None


def update_type(source: Vector, successor: Vector) -> str:
    if successor[-1] == 2:
        return "A"
    if source[-1] == 2 and source != (2,):
        return "C"
    return "B"


def feature_prefix_counts(queue: Vector) -> tuple[int, ...]:
    starts = set(feature_starts(queue))
    count = 0
    answer = []
    for index in range(len(queue)):
        count += int(index in starts)
        answer.append(count)
    return tuple(answer)


def audit(queue: Vector, tail: int, cap: int, census: Census) -> str:
    initial = queue
    feature_counts = feature_prefix_counts(initial)
    roots = list(range(len(queue)))
    depths = [0] * len(queue)
    events = []

    for time in range(cap):
        following = queue_step(queue, tail)
        if following is None:
            census.queues += 1
            return "".join(events)
        successor = normalize_queue(following.queue, tail)
        inherited = successor[:-1]
        differences = [
            index
            for index in range(1, len(queue))
            if inherited[index] != queue[index]
        ]
        pivot = differences[-1] if differences else 0
        kind = update_type(queue, successor)
        events.append(kind)

        root = roots[pivot]
        depth = depths[pivot] + int(kind == "C")
        roots.append(root)
        depths.append(depth)
        if kind == "C":
            census.pulls += 1
            census.maximum_depth = max(census.maximum_depth, depth)
            coordinate_slack = (root + 1) // 2 - depth
            census.minimum_coordinate_slack = min(
                census.minimum_coordinate_slack, coordinate_slack
            )
            if coordinate_slack < 0:
                census.coordinate_failures += 1
                census.first_coordinate_failure = (
                    census.first_coordinate_failure
                    or f"tail={tail} R={''.join(map(str, initial))} "
                    f"time={time} pivot={pivot} root={root} depth={depth} "
                    f"capacity={(root + 1) // 2} events={''.join(events)}"
                )
            if depth > feature_counts[root]:
                census.feature_failures += 1

        queue = successor
        census.updates += 1

    census.queues += 1
    census.capped += 1
    return "".join(events)


def sparse_invariant_queues(
    length: int, tail: int, maximum_features: int
) -> Iterator[Vector]:
    """Generate every invariant word with at most the stated feature count."""

    if length == 1:
        if tail == 2:
            yield (2,)
        return

    start_context = 3 if tail == 2 else 0

    def extend(prefix: Vector, context: int, features: int) -> Iterator[Vector]:
        if len(prefix) == length:
            if prefix[-1] in (1, 2):
                yield prefix
            return
        for symbol in range(3):
            following = SFT_TRANSITIONS[context][symbol]
            if following == 4:
                continue
            if len(prefix) == length - 1 and symbol not in (1, 2):
                continue
            added = int(
                symbol == 1 or (symbol == 0 and prefix[-1] != 0)
            )
            if features + added <= maximum_features:
                yield from extend(
                    prefix + (symbol,), following, features + added
                )

    yield from extend((tail,), start_context, 0)


def feature_counterexample_control() -> tuple[int, int, int, int]:
    census = Census()
    events = audit(FEATURE_COUNTEREXAMPLE, 3, 1_000, census)
    assert len(FEATURE_COUNTEREXAMPLE) == 77
    assert events == "CBACACBACBA"
    assert (census.updates, census.pulls, census.maximum_depth) == (11, 4, 3)
    assert census.feature_failures >= 1
    assert census.coordinate_failures == census.capped == 0
    assert census.minimum_coordinate_slack == 13
    return (
        census.updates,
        census.pulls,
        census.maximum_depth,
        census.minimum_coordinate_slack,
    )


def coordinate_counterexample_control() -> tuple[int, int, int, int]:
    census = Census()
    events = audit(COORDINATE_COUNTEREXAMPLE, 3, 1_000, census)
    assert len(COORDINATE_COUNTEREXAMPLE) == 387
    assert events == "CBACACBACA"
    assert (census.updates, census.pulls, census.maximum_depth) == (10, 4, 3)
    assert census.coordinate_failures == 1
    assert census.minimum_coordinate_slack == -1
    assert census.first_coordinate_failure is not None
    assert "time=8" in census.first_coordinate_failure
    assert "root=3 depth=3 capacity=2" in census.first_coordinate_failure
    return (
        census.updates,
        census.pulls,
        census.maximum_depth,
        census.minimum_coordinate_slack,
    )


def zero_run_root_depth(run: int) -> tuple[int, str]:
    queue: Vector = (3, 0, 0, 1) + (0,) * run + (2,)
    roots = list(range(len(queue)))
    depths = [0] * len(queue)
    maximum = 0
    events = []
    for _time in range(100):
        following = queue_step(queue, 3)
        if following is None:
            return maximum, "".join(events)
        successor = normalize_queue(following.queue, 3)
        differences = [
            index
            for index in range(1, len(queue))
            if successor[index] != queue[index]
        ]
        pivot = differences[-1] if differences else 0
        kind = update_type(queue, successor)
        root = roots[pivot]
        depth = depths[pivot] + int(kind == "C")
        roots.append(root)
        depths.append(depth)
        events.append(kind)
        if kind == "C" and root == 3:
            maximum = max(maximum, depth)
        queue = successor
    raise AssertionError("zero-run resonance control reached its cap")


def zero_run_resonance_control(limit: int = 4_096) -> tuple[int, int, int]:
    """Verify the recorded dyadic threshold classes on one finite interval."""

    at_least_two = set()
    at_least_three = set()
    at_least_four = set()
    for run in range(limit):
        depth, _events = zero_run_root_depth(run)
        if depth >= 2:
            at_least_two.add(run)
        if depth >= 3:
            at_least_three.add(run)
        if depth >= 4:
            at_least_four.add(run)
    assert at_least_two == {run for run in range(limit) if run % 8 == 6}
    assert at_least_three == {
        run for run in range(limit) if run % 512 in (382, 390)
    }
    assert at_least_four == {
        run for run in range(limit) if run % 2_048 == 390
    }
    return len(at_least_two), len(at_least_three), len(at_least_four)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exact-length", type=int, default=19)
    parser.add_argument("--sparse-max-length", type=int, default=128)
    parser.add_argument("--maximum-features", type=int, default=5)
    parser.add_argument("--random-per-tail", type=int, default=10_000)
    parser.add_argument("--orbit-cap", type=int, default=1_000)
    parser.add_argument("--seed", type=int, default=30137)
    args = parser.parse_args()
    if (
        args.exact_length < 1
        or args.sparse_max_length < 1
        or args.maximum_features < 0
        or args.random_per_tail < 0
        or args.orbit_cap < 1
    ):
        parser.error("invalid audit bound")

    updates, pulls, depth, slack = feature_counterexample_control()
    print(
        "feature counterexample: length=77 events=CBACACBACBA "
        f"updates={updates} pulls={pulls} depth={depth} "
        f"coordinate-slack={slack} PASS",
        flush=True,
    )
    updates, pulls, depth, slack = coordinate_counterexample_control()
    print(
        "coordinate counterexample: length=387 R=3001(0^382)2 "
        "events=CBACACBACA "
        f"updates={updates} pulls={pulls} depth={depth} "
        f"coordinate-slack={slack} CLAIM FALSE",
        flush=True,
    )
    resonance = zero_run_resonance_control()
    print(
        "zero-run resonance 0<=m<4096: "
        f"depth>=2/3/4 counts={resonance} dyadic classes PASS",
        flush=True,
    )

    census = Census()
    before = census.queues
    for tail in (2, 3):
        for queue in invariant_queues(args.exact_length, tail):
            audit(queue, tail, args.orbit_cap, census)
    print(
        f"exact length={args.exact_length} queues={census.queues-before} "
        f"coordinate-failures={census.coordinate_failures} "
        f"minimum-slack={census.minimum_coordinate_slack}",
        flush=True,
    )

    before = census.queues
    for length in range(1, args.sparse_max_length + 1):
        for tail in (2, 3):
            for queue in sparse_invariant_queues(
                length, tail, args.maximum_features
            ):
                audit(queue, tail, args.orbit_cap, census)
        if length % 16 == 0 or length == args.sparse_max_length:
            print(
                f"sparse through length={length} "
                f"queues={census.queues-before} "
                f"coordinate-failures={census.coordinate_failures}",
                flush=True,
            )

    generator = random.Random(args.seed)
    for length in (24, 32, 48, 64, 96, 128, 192, 256):
        before = census.queues
        for tail in (2, 3):
            for _ in range(args.random_per_tail):
                audit(
                    random_invariant_queue(length, tail, generator),
                    tail,
                    args.orbit_cap,
                    census,
                )
                audit(
                    weighted_invariant_queue(length, tail, generator),
                    tail,
                    args.orbit_cap,
                    census,
                )
        print(
            f"sample length={length} queues={census.queues-before} "
            f"coordinate-failures={census.coordinate_failures}",
            flush=True,
        )

    print(
        f"TOTAL queues={census.queues} updates={census.updates} "
        f"pulls={census.pulls} maximum-depth={census.maximum_depth} "
        f"coordinate-failures={census.coordinate_failures} "
        f"feature-failures={census.feature_failures} capped={census.capped} "
        f"minimum-coordinate-slack={census.minimum_coordinate_slack}"
    )
    print(
        "first coordinate failure: "
        f"{census.first_coordinate_failure or 'none'}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Parent-forest proof controls and held-out pull-depth falsifiers."""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

from constant_tail_mixed_run_budget import weighted_invariant_queue
from constant_tail_origin_prefix_hall import feature_starts
from constant_tail_queue import Vector, normalize_queue, queue_step
from constant_tail_retreat_budget import invariant_queues, random_invariant_queue


@dataclass(frozen=True, slots=True)
class Node:
    parent: int | None
    root: int
    pull_depth: int
    time: int
    update_type: str


@dataclass(frozen=True, slots=True)
class Pull:
    time: int
    node: int
    root: int
    depth: int


@dataclass(slots=True)
class Census:
    queues: int = 0
    updates: int = 0
    pulls: int = 0
    maximum_depth: int = 0
    feature_failures: int = 0
    temporal_failures: int = 0
    capped: int = 0
    minimum_slack: int = 10**9
    first_failure: str | None = None


def invariant_prefix_counts(queue: Vector) -> tuple[int, ...]:
    starts = set(feature_starts(queue))
    count = 0
    answer = []
    for index in range(len(queue)):
        count += int(index in starts)
        answer.append(count)
    return tuple(answer)


def chain(nodes: list[Node], node: int) -> tuple[tuple[int, str, int], ...]:
    answer = []
    while nodes[node].parent is not None:
        current = nodes[node]
        answer.append((current.time, current.update_type, current.pull_depth))
        node = current.parent
    return tuple(answer)


def update_type(source: Vector, successor: Vector) -> str:
    if successor[-1] == 2:
        return "A"
    if source[-1] == 2 and source != (2,):
        return "C"
    return "B"


def temporal_recurrence(pulls: tuple[Pull, ...]) -> bool:
    """Check the exact depth recurrence implied by third-last pull pivots."""

    for index in range(1, len(pulls)):
        current = pulls[index]
        previous = pulls[index - 1]
        gap = current.time - previous.time
        if gap < 2:
            return False
        if gap >= 3:
            expected = previous.depth + 1
        else:
            expected = 1 + (pulls[index - 2].depth if index >= 2 else 0)
        if current.depth != expected:
            return False
        if current.depth < (index + 2) // 2:
            return False
    return True


def audit(queue: Vector, tail: int, cap: int, census: Census) -> None:
    initial = queue
    prefix_counts = invariant_prefix_counts(initial)
    nodes = [Node(None, index, 0, -1, "I") for index in range(len(queue))]
    coordinates = list(range(len(queue)))
    pulls = []

    for time in range(cap):
        following = queue_step(queue, tail)
        if following is None:
            break
        successor = normalize_queue(following.queue, tail)
        inherited = successor[:-1]
        differences = tuple(
            index
            for index in range(1, len(queue))
            if inherited[index] != queue[index]
        )
        if differences:
            pivot = differences[-1]
        else:
            assert queue == (2,)
            pivot = 0

        kind = update_type(queue, successor)
        parent = coordinates[pivot]
        parent_node = nodes[parent]
        node = len(nodes)
        nodes.append(
            Node(
                parent,
                parent_node.root,
                parent_node.pull_depth + int(kind == "C"),
                time,
                kind,
            )
        )
        coordinates.append(node)
        if kind == "C":
            current = nodes[node]
            pull = Pull(time, node, current.root, current.pull_depth)
            pulls.append(pull)
            available = prefix_counts[current.root]
            slack = available - current.pull_depth
            census.minimum_slack = min(census.minimum_slack, slack)
            census.maximum_depth = max(census.maximum_depth, current.pull_depth)
            if slack < 0:
                census.feature_failures += 1
                census.first_failure = census.first_failure or (
                    f"feature tail={tail} R={''.join(map(str, initial))} "
                    f"time={time} root={current.root} depth={current.pull_depth} "
                    f"available={available} chain={chain(nodes, node)}"
                )

        queue = successor
        census.updates += 1
    else:
        census.capped += 1

    profile = tuple(pulls)
    if not temporal_recurrence(profile):
        census.temporal_failures += 1
        census.first_failure = census.first_failure or (
            f"temporal tail={tail} R={''.join(map(str, initial))} "
            f"pulls={profile}"
        )
    if profile:
        assert len(profile) <= 2 * max(pull.depth for pull in profile)
    census.queues += 1
    census.pulls += len(profile)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exact-length", type=int, default=19)
    parser.add_argument("--random-per-tail", type=int, default=50_000)
    parser.add_argument("--sparse-per-tail", type=int, default=50_000)
    parser.add_argument("--orbit-cap", type=int, default=1_000)
    args = parser.parse_args()
    if (
        args.exact_length < 1
        or args.random_per_tail < 0
        or args.sparse_per_tail < 0
        or args.orbit_cap < 1
    ):
        parser.error("invalid audit bound")

    census = Census()
    before = census.queues
    for tail in (2, 3):
        for queue in invariant_queues(args.exact_length, tail):
            audit(queue, tail, args.orbit_cap, census)
    print(
        f"exact length={args.exact_length} queues={census.queues-before} "
        f"feature-failures={census.feature_failures} "
        f"temporal-failures={census.temporal_failures} "
        f"minimum-slack={census.minimum_slack}",
        flush=True,
    )

    generator = random.Random(30133)
    for length in (24, 32, 48, 64, 96):
        before = census.queues
        for tail in (2, 3):
            for _ in range(args.random_per_tail):
                audit(
                    random_invariant_queue(length, tail, generator),
                    tail,
                    args.orbit_cap,
                    census,
                )
        print(
            f"random length={length} queues={census.queues-before} "
            f"feature-failures={census.feature_failures} "
            f"temporal-failures={census.temporal_failures}",
            flush=True,
        )

    for length in (24, 32, 48, 64, 96, 128):
        before = census.queues
        for tail in (2, 3):
            for _ in range(args.sparse_per_tail):
                audit(
                    weighted_invariant_queue(length, tail, generator),
                    tail,
                    args.orbit_cap,
                    census,
                )
        print(
            f"sparse length={length} queues={census.queues-before} "
            f"feature-failures={census.feature_failures} "
            f"temporal-failures={census.temporal_failures}",
            flush=True,
        )

    print(
        f"TOTAL queues={census.queues} updates={census.updates} "
        f"pulls={census.pulls} maximum-depth={census.maximum_depth} "
        f"feature-failures={census.feature_failures} "
        f"temporal-failures={census.temporal_failures} "
        f"capped={census.capped} minimum-slack={census.minimum_slack}"
    )
    print(f"first failure: {census.first_failure or 'none'}")


if __name__ == "__main__":
    main()

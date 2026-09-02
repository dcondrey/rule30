#!/usr/bin/env python3
"""Falsifiers for the stabilized pull-ray crossing conjecture."""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

from constant_tail_mixed_run_budget import weighted_invariant_queue
from constant_tail_origin_prefix_hall import feature_starts
from constant_tail_queue import Vector, normalize_queue, queue_step
from constant_tail_retreat_budget import invariant_queues, random_invariant_queue


@dataclass(frozen=True, slots=True)
class Pull:
    time: int
    pivot: int

    @property
    def intercept(self) -> int:
        return self.pivot - self.time


def pull_profile(queue: Vector, tail: int, cap: int) -> tuple[Pull, ...]:
    pulls = []
    for time in range(cap):
        following = queue_step(queue, tail)
        if following is None:
            return tuple(pulls)
        inherited = normalize_queue(following.queue[:-1], tail)
        differences = tuple(
            index
            for index in range(1, len(queue))
            if inherited[index] != queue[index]
        )
        if differences:
            pivot = differences[-1]
            assert queue[pivot] == 1
        else:
            assert queue == (2,)
            pivot = 0
        if queue[-1] == 2 and queue != (2,):
            pulls.append(Pull(time, pivot))
        queue = normalize_queue(following.queue, tail)
    raise AssertionError("orbit reached the audit cap")


@dataclass(slots=True)
class Census:
    queues: int = 0
    pulls: int = 0
    stabilization_failures: int = 0
    crossing_failures: int = 0
    capped: int = 0
    minimum_slack: int = 10**9
    first_failure: str | None = None


def audit(queue: Vector, tail: int, cap: int, census: Census) -> None:
    try:
        pulls = pull_profile(queue, tail, cap)
    except AssertionError as error:
        if "audit cap" not in str(error):
            raise
        census.queues += 1
        census.capped += 1
        return

    census.queues += 1
    census.pulls += len(pulls)
    if not pulls:
        return

    intercept = pulls[1].intercept if len(pulls) >= 2 else pulls[0].intercept
    if any(pull.intercept != intercept for pull in pulls[1:]):
        census.stabilization_failures += 1
        census.first_failure = census.first_failure or (
            f"stabilization tail={tail} R={''.join(map(str, queue))} "
            f"pulls={pulls}"
        )
        return

    available = sum(start <= intercept for start in feature_starts(queue))
    slack = available - len(pulls)
    census.minimum_slack = min(census.minimum_slack, slack)
    if slack < 0:
        census.crossing_failures += 1
        census.first_failure = census.first_failure or (
            f"crossing tail={tail} R={''.join(map(str, queue))} "
            f"pulls={pulls} d={intercept} available={available}"
        )


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
    controls = (
        (3, tuple(map(int, "3000000000000000010100000010000002"))),
        (2, tuple(map(int, "211012110000000001"))),
    )
    for tail, queue in controls:
        before = (
            census.stabilization_failures,
            census.crossing_failures,
            census.capped,
        )
        audit(queue, tail, args.orbit_cap, census)
        assert before == (
            census.stabilization_failures,
            census.crossing_failures,
            census.capped,
        )
        print(
            f"control tail={tail} n={len(queue)} pull-ray PASS",
            flush=True,
        )

    before = census.queues
    for tail in (2, 3):
        for queue in invariant_queues(args.exact_length, tail):
            audit(queue, tail, args.orbit_cap, census)
    print(
        f"exact length={args.exact_length} queues={census.queues-before} "
        f"stabilization-failures={census.stabilization_failures} "
        f"crossing-failures={census.crossing_failures} "
        f"minimum-slack={census.minimum_slack}",
        flush=True,
    )

    generator = random.Random(30132)
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
            f"stabilization-failures={census.stabilization_failures} "
            f"crossing-failures={census.crossing_failures} "
            f"minimum-slack={census.minimum_slack}",
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
            f"stabilization-failures={census.stabilization_failures} "
            f"crossing-failures={census.crossing_failures} "
            f"minimum-slack={census.minimum_slack}",
            flush=True,
        )

    print(
        f"TOTAL queues={census.queues} pulls={census.pulls} "
        f"stabilization-failures={census.stabilization_failures} "
        f"crossing-failures={census.crossing_failures} "
        f"capped={census.capped} minimum-slack={census.minimum_slack}"
    )
    print(f"first failure: {census.first_failure or 'none'}")


if __name__ == "__main__":
    main()

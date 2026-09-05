#!/usr/bin/env python3
"""Falsifiers for the mixed initial-one/zero-run retreat budget."""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

from constant_tail_language_cocycle import SFT_TRANSITIONS
from constant_tail_queue import Vector, normalize_queue, queue_step
from constant_tail_retreat_budget import (
    invariant_queues,
    random_invariant_queue,
)


def zero_run_count(queue: Vector) -> int:
    return sum(
        symbol == 0 and (index == 0 or queue[index - 1] != 0)
        for index, symbol in enumerate(queue)
    )


def mixed_budget(queue: Vector) -> int:
    return queue[1:].count(1) + zero_run_count(queue)


def retreat_count(queue: Vector, tail: int, cap: int) -> tuple[int, bool]:
    retreats = 0
    for _ in range(cap):
        following = queue_step(queue, tail)
        if following is None:
            return retreats, False
        queue = normalize_queue(following.queue, tail)
        retreats += int(queue[-1] == 2)
    return retreats, True


@dataclass(slots=True)
class Census:
    queues: int = 0
    updates_capped: int = 0
    failures: int = 0
    maximum_excess: int = -10**9
    minimum_positive_slack: int = 10**9
    first_failure: str | None = None
    tight_positive: str | None = None


def audit(queue: Vector, tail: int, cap: int, census: Census) -> None:
    retreats, capped = retreat_count(queue, tail, cap)
    budget = mixed_budget(queue)
    excess = retreats - budget
    census.queues += 1
    census.updates_capped += int(capped)
    census.maximum_excess = max(census.maximum_excess, excess)
    if retreats:
        census.minimum_positive_slack = min(
            census.minimum_positive_slack, budget - retreats
        )
    description = (
        f"tail={tail} n={len(queue)} R={''.join(map(str, queue))} "
        f"retreats={retreats} #1={queue[1:].count(1)} "
        f"zero-runs={zero_run_count(queue)} budget={budget}"
    )
    if excess > 0:
        census.failures += 1
        if census.first_failure is None:
            census.first_failure = description
    if retreats and excess == 0 and census.tight_positive is None:
        census.tight_positive = description


def weighted_invariant_queue(
    length: int, tail: int, generator: random.Random
) -> Vector:
    """Generate a valid queue biased toward sparse colors and long gaps."""

    if length == 1:
        if tail != 2:
            raise ValueError("tail 3 has no length-one invariant queue")
        return (2,)
    while True:
        prefix = [tail]
        context = 3 if tail == 2 else 0
        for index in range(1, length):
            choices = [
                symbol
                for symbol in range(3)
                if SFT_TRANSITIONS[context][symbol] != 4
                and (index < length - 1 or symbol in (1, 2))
            ]
            if not choices:
                break
            weights = [
                12 if symbol == 0 else 1 if symbol == 1 else 4
                for symbol in choices
            ]
            symbol = generator.choices(choices, weights=weights, k=1)[0]
            prefix.append(symbol)
            context = SFT_TRANSITIONS[context][symbol]
        if len(prefix) == length:
            return tuple(prefix)


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
        parser.error("bounds and sample counts must be nonnegative")

    census = Census()
    controls = (
        (3, tuple(map(int, "3000000000000000010100000010000002"))),
        (2, tuple(map(int, "211012110000000001"))),
    )
    for tail, queue in controls:
        audit(queue, tail, args.orbit_cap, census)
        assert census.failures == 0 and not census.updates_capped
        print(
            f"control tail={tail} n={len(queue)} retreats/budget="
            f"{retreat_count(queue, tail, args.orbit_cap)[0]}/"
            f"{mixed_budget(queue)} PASS"
        )

    before = (census.queues, census.failures)
    for tail in (2, 3):
        for queue in invariant_queues(args.exact_length, tail):
            audit(queue, tail, args.orbit_cap, census)
    print(
        f"exact length={args.exact_length} "
        f"queues={census.queues-before[0]} "
        f"failures={census.failures-before[1]} "
        f"maximum-excess={census.maximum_excess}"
    )

    generator = random.Random(30130)
    for length in (24, 32, 48, 64, 96):
        before = (census.queues, census.failures)
        for tail in (2, 3):
            for _ in range(args.random_per_tail):
                audit(
                    random_invariant_queue(length, tail, generator),
                    tail,
                    args.orbit_cap,
                    census,
                )
        print(
            f"random length={length} queues={census.queues-before[0]} "
            f"failures={census.failures-before[1]} "
            f"maximum-excess={census.maximum_excess}"
        )

    for length in (24, 32, 48, 64, 96, 128):
        before = (census.queues, census.failures)
        for tail in (2, 3):
            for _ in range(args.sparse_per_tail):
                audit(
                    weighted_invariant_queue(length, tail, generator),
                    tail,
                    args.orbit_cap,
                    census,
                )
        print(
            f"sparse length={length} queues={census.queues-before[0]} "
            f"failures={census.failures-before[1]} "
            f"maximum-excess={census.maximum_excess}"
        )

    print(
        f"TOTAL queues={census.queues} failures={census.failures} "
        f"capped={census.updates_capped} maximum-excess={census.maximum_excess} "
        f"minimum-positive-slack={census.minimum_positive_slack}"
    )
    print(f"first failure: {census.first_failure or 'none'}")
    print(f"first tight positive: {census.tight_positive or 'none'}")


if __name__ == "__main__":
    main()

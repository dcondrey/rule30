#!/usr/bin/env python3
"""Falsify the proposed boundary-retreat ancestry budget."""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from typing import Iterator

from constant_tail_language_cocycle import SFT_TRANSITIONS
from constant_tail_queue import Vector, normalize_queue, queue_step


@dataclass(slots=True)
class Census:
    cases: int = 0
    updates: int = 0
    failures: int = 0
    capped: int = 0
    maximum_excess: int = -10**9
    first_failure: str | None = None
    first_capped: str | None = None


def invariant_queues(length: int, tail: int) -> Iterator[Vector]:
    """Generate the exact normalized SFT queues without rejected products."""

    if length == 1:
        if tail == 2:
            yield (2,)
        return

    start_context = 3 if tail == 2 else 0

    def extend(prefix: Vector, context: int) -> Iterator[Vector]:
        index = len(prefix)
        if index == length:
            if prefix[-1] in (1, 2):
                yield prefix
            return
        for symbol in range(3):
            following = SFT_TRANSITIONS[context][symbol]
            if following == 4:
                continue
            if index == length - 1 and symbol not in (1, 2):
                continue
            yield from extend(prefix + (symbol,), following)

    yield from extend((tail,), start_context)


def audit_queue(queue: Vector, tail: int, cap: int, census: Census) -> None:
    initial = queue
    budget = queue[1:].count(1) + 1
    retreats = 0
    maximum_excess = -budget
    boundary = []

    for _step in range(cap):
        following = queue_step(queue, tail)
        if following is None:
            census.cases += 1
            census.maximum_excess = max(
                census.maximum_excess, maximum_excess
            )
            return
        queue = normalize_queue(following.queue, tail)
        boundary.append(queue[-1])
        retreats += int(queue[-1] == 2)
        maximum_excess = max(maximum_excess, retreats - budget)
        census.updates += 1
        if retreats > budget:
            census.failures += 1
            census.cases += 1
            census.maximum_excess = max(
                census.maximum_excess, maximum_excess
            )
            if census.first_failure is None:
                census.first_failure = (
                    f"tail={tail} R={''.join(map(str, initial))} "
                    f"budget={budget} retreats={retreats} "
                    f"boundary={''.join(map(str, boundary))}"
                )
            return

    census.cases += 1
    census.capped += 1
    census.maximum_excess = max(census.maximum_excess, maximum_excess)
    if census.first_capped is None:
        census.first_capped = (
            f"tail={tail} R={''.join(map(str, initial))} cap={cap} "
            f"retreats={retreats} budget={budget}"
        )


def random_invariant_queue(
    length: int, tail: int, generator: random.Random
) -> Vector:
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
            symbol = generator.choice(choices)
            prefix.append(symbol)
            context = SFT_TRANSITIONS[context][symbol]
        if len(prefix) == length:
            return tuple(prefix)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first-length", type=int, default=16)
    parser.add_argument("--last-length", type=int, default=18)
    parser.add_argument("--random-per-tail", type=int, default=20_000)
    parser.add_argument("--orbit-cap", type=int, default=1_000)
    args = parser.parse_args()
    if not 1 <= args.first_length <= args.last_length:
        parser.error("invalid exact length interval")
    if args.random_per_tail < 0 or args.orbit_cap < 1:
        parser.error("invalid random count or orbit cap")

    # The exploratory counterexample proves that the uncredited #1 bound is
    # false and that the registered one-credit repair is sharp.
    control = Census()
    audit_queue((2, 0, 0, 0, 1), 2, args.orbit_cap, control)
    assert control.failures == 0 and control.maximum_excess == 0

    counterexample = tuple(map(int, "3000000000000000010100000010000002"))
    killed = Census()
    audit_queue(counterexample, 3, args.orbit_cap, killed)
    assert killed.failures == 1
    assert killed.first_failure is not None
    print(f"registered claim KILLED: {killed.first_failure}")

    census = Census()
    for length in range(args.first_length, args.last_length + 1):
        before = Census(census.cases, census.updates, census.failures, census.capped)
        for tail in (2, 3):
            for queue in invariant_queues(length, tail):
                audit_queue(queue, tail, args.orbit_cap, census)
        print(
            f"length={length:2d} cases={census.cases-before.cases:8d} "
            f"updates={census.updates-before.updates:8d} "
            f"failures={census.failures-before.failures:4d} "
            f"capped={census.capped-before.capped:4d} "
            f"maximum-excess={census.maximum_excess}",
            flush=True,
        )

    generator = random.Random(30030)
    for length in (24, 32, 48, 64, 96):
        before = Census(census.cases, census.updates, census.failures, census.capped)
        for tail in (2, 3):
            for _ in range(args.random_per_tail):
                audit_queue(
                    random_invariant_queue(length, tail, generator),
                    tail,
                    args.orbit_cap,
                    census,
                )
        print(
            f"random-length={length:2d} "
            f"cases={census.cases-before.cases:7d} "
            f"updates={census.updates-before.updates:8d} "
            f"failures={census.failures-before.failures:4d} "
            f"capped={census.capped-before.capped:4d} "
            f"maximum-excess={census.maximum_excess}",
            flush=True,
        )

    print(
        f"TOTAL cases={census.cases} updates={census.updates} "
        f"failures={census.failures} capped={census.capped} "
        f"maximum-excess={census.maximum_excess}"
    )
    print(f"first failure: {census.first_failure or 'none'}")
    print(f"first capped: {census.first_capped or 'none'}")


if __name__ == "__main__":
    main()

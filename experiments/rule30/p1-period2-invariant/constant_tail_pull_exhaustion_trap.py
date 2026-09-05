#!/usr/bin/env python3
"""Stored falsifiers for the coordinate-reserve pull exhaustion trap.

The registered claim was that, once a successful pull creates a node with
zero reserve ``ceil(root/2)-pull_depth``, no later successful update is a
pull.  It is false at ``3001 0^62 2``.  At ``3001 0^382 2`` the later pulls
also falsify the coordinate-depth bound itself.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from typing import Iterator

from constant_tail_language_cocycle import SFT_TRANSITIONS
from constant_tail_mixed_run_budget import weighted_invariant_queue
from constant_tail_pull_coordinate_depth import (
    COORDINATE_COUNTEREXAMPLE,
    FEATURE_COUNTEREXAMPLE,
    update_type,
)
from constant_tail_queue import Vector, normalize_queue, queue_step
from constant_tail_retreat_budget import invariant_queues, random_invariant_queue


@dataclass(slots=True)
class Census:
    queues: int = 0
    updates: int = 0
    pulls: int = 0
    exhaustions: int = 0
    later_pull_failures: int = 0
    negative_reserve_failures: int = 0
    zero_suffix_failures: int = 0
    zero_raw_three_failures: int = 0
    capped: int = 0
    first_failure: str | None = None


def reserve(root: int, depth: int) -> int | None:
    if root == 0:
        return None
    return (root + 1) // 2 - depth


def describe(
    initial: Vector,
    tail: int,
    time: int,
    events: list[str],
    detail: str,
) -> str:
    return (
        f"tail={tail} R={''.join(map(str, initial))} time={time} "
        f"events={''.join(events)} {detail}"
    )


def audit(queue: Vector, tail: int, cap: int, census: Census) -> str:
    initial = queue
    raw_queue = queue
    roots = list(range(len(queue)))
    depths = [0] * len(queue)
    events: list[str] = []
    exhausted = False

    for time in range(cap):
        zero_positions = []
        for index, (raw, root, depth) in enumerate(
            zip(raw_queue, roots, depths, strict=True)
        ):
            remaining = reserve(root, depth)
            if remaining is None:
                continue
            if remaining < 0:
                census.negative_reserve_failures += 1
                census.first_failure = census.first_failure or describe(
                    initial,
                    tail,
                    time,
                    events,
                    f"negative index={index} raw={raw} root={root} "
                    f"depth={depth} reserve={remaining}",
                )
            if remaining == 0:
                zero_positions.append(index)
                if raw == 3:
                    census.zero_raw_three_failures += 1
                    census.first_failure = census.first_failure or describe(
                        initial,
                        tail,
                        time,
                        events,
                        f"zero-raw-three index={index} root={root} "
                        f"depth={depth}",
                    )

        if exhausted:
            expected = list(range(zero_positions[0], len(queue)))
            if not zero_positions or zero_positions != expected:
                census.zero_suffix_failures += 1
                census.first_failure = census.first_failure or describe(
                    initial,
                    tail,
                    time,
                    events,
                    f"zero-positions={zero_positions}",
                )

        following = queue_step(queue, tail)
        if following is None:
            census.queues += 1
            return "".join(events)
        successor = normalize_queue(following.queue, tail)
        differences = [
            index
            for index in range(1, len(queue))
            if successor[index] != queue[index]
        ]
        pivot = differences[-1] if differences else 0
        kind = update_type(queue, successor)
        events.append(kind)
        census.updates += 1
        census.pulls += int(kind == "C")

        if exhausted and kind == "C":
            census.later_pull_failures += 1
            census.first_failure = census.first_failure or describe(
                initial,
                tail,
                time,
                events,
                f"later-pull pivot={pivot} parent-root={roots[pivot]} "
                f"parent-depth={depths[pivot]}",
            )

        child_root = roots[pivot]
        child_depth = depths[pivot] + int(kind == "C")
        child_reserve = reserve(child_root, child_depth)
        roots.append(child_root)
        depths.append(child_depth)
        if kind == "C" and child_reserve == 0 and not exhausted:
            exhausted = True
            census.exhaustions += 1

        raw_queue = following.queue
        queue = successor

    census.queues += 1
    census.capped += 1
    return "".join(events)


def legal_prefixes(max_length: int, tail: int) -> Iterator[Vector]:
    """Generate every invariant-SFT prefix beginning with the fixed tail."""

    start_context = 3 if tail == 2 else 0

    def extend(prefix: Vector, context: int) -> Iterator[Vector]:
        yield prefix
        if len(prefix) == max_length:
            return
        for symbol in range(3):
            following = SFT_TRANSITIONS[context][symbol]
            if following != 4:
                yield from extend(prefix + (symbol,), following)

    yield from extend((tail,), start_context)


def adversarial_first_pull_queues(
    max_prefix_length: int, zero_runs: tuple[int, ...]
) -> Iterator[tuple[int, Vector]]:
    """Generate legal ``U 1 0^m 2`` queues whose first update is a pull."""

    seen: set[Vector] = set()
    for tail in (2, 3):
        for prefix in legal_prefixes(max_prefix_length, tail):
            for run in zero_runs:
                queue = prefix + (1,) + (0,) * run + (2,)
                if queue in seen:
                    continue
                seen.add(queue)
                following = queue_step(queue, tail)
                if following is None:
                    continue
                successor = normalize_queue(following.queue, tail)
                if update_type(queue, successor) == "C":
                    yield tail, queue


def failed(census: Census) -> bool:
    return any(
        (
            census.later_pull_failures,
            census.negative_reserve_failures,
            census.zero_suffix_failures,
            census.zero_raw_three_failures,
            census.capped,
        )
    )


def falsification_controls() -> tuple[str, str]:
    exhaustion_counterexample = (3, 0, 0, 1) + (0,) * 62 + (2,)
    exhaustion = Census()
    exhaustion_events = audit(exhaustion_counterexample, 3, 1_000, exhaustion)
    assert len(exhaustion_counterexample) == 67
    assert exhaustion_events == "CBACACBBA"
    assert exhaustion.exhaustions == 1
    assert exhaustion.later_pull_failures == 1

    coordinate = Census()
    coordinate_events = audit(COORDINATE_COUNTEREXAMPLE, 3, 1_000, coordinate)
    assert coordinate_events == "CBACACBACA"
    assert coordinate.exhaustions == 1
    assert coordinate.later_pull_failures == 2
    assert coordinate.negative_reserve_failures > 0
    return exhaustion_events, coordinate_events


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exact-length", type=int, default=19)
    parser.add_argument("--max-prefix-length", type=int, default=10)
    parser.add_argument("--random-per-kind", type=int, default=5_000)
    parser.add_argument("--orbit-cap", type=int, default=2_000)
    parser.add_argument("--seed", type=int, default=901_237)
    args = parser.parse_args()
    if (
        args.exact_length < 1
        or args.max_prefix_length < 1
        or args.random_per_kind < 0
        or args.orbit_cap < 1
    ):
        parser.error("invalid audit bound")

    exhaustion_events, coordinate_events = falsification_controls()
    print(
        "exhaustion counterexample: length=67 R=3001(0^62)2 "
        f"events={exhaustion_events} ET FALSE",
        flush=True,
    )
    print(
        "coordinate counterexample: length=387 R=3001(0^382)2 "
        f"events={coordinate_events} CD FALSE",
        flush=True,
    )

    control = Census()
    events = audit(FEATURE_COUNTEREXAMPLE, 3, args.orbit_cap, control)
    assert events == "CBACACBACBA"
    assert control.exhaustions == 0
    assert not failed(control)
    print(
        "feature counterexample: old feature reserve fails, "
        "coordinate exhaustion trap PASS",
        flush=True,
    )

    census = Census()
    before = census.queues
    for tail in (2, 3):
        for queue in invariant_queues(args.exact_length, tail):
            audit(queue, tail, args.orbit_cap, census)
    print(
        f"exact length={args.exact_length} queues={census.queues-before} "
        f"exhaustions={census.exhaustions} failures="
        f"{census.later_pull_failures+census.negative_reserve_failures+census.zero_suffix_failures+census.zero_raw_three_failures}",
        flush=True,
    )

    zero_runs = (0, 1, 2, 3, 4, 7, 15, 31, 63, 127, 255, 511)
    before = census.queues
    for tail, queue in adversarial_first_pull_queues(
        args.max_prefix_length, zero_runs
    ):
        audit(queue, tail, args.orbit_cap, census)
    print(
        f"adversarial prefix<={args.max_prefix_length} "
        f"zero-run<=511 queues={census.queues-before} "
        f"exhaustions={census.exhaustions}",
        flush=True,
    )

    generator = random.Random(args.seed)
    for length in (24, 32, 48, 64, 96, 128, 192, 256, 384, 512):
        before = census.queues
        for tail in (2, 3):
            for queue_generator in (
                random_invariant_queue,
                weighted_invariant_queue,
            ):
                for _ in range(args.random_per_kind):
                    audit(
                        queue_generator(length, tail, generator),
                        tail,
                        args.orbit_cap,
                        census,
                    )
        print(
            f"random/sparse length={length} queues={census.queues-before} "
            f"exhaustions={census.exhaustions}",
            flush=True,
        )

    failures = (
        census.later_pull_failures
        + census.negative_reserve_failures
        + census.zero_suffix_failures
        + census.zero_raw_three_failures
    )
    print(
        f"TOTAL queues={census.queues} updates={census.updates} "
        f"pulls={census.pulls} exhaustions={census.exhaustions} "
        f"later-pull-failures={census.later_pull_failures} "
        f"negative-reserve-failures={census.negative_reserve_failures} "
        f"zero-suffix-failures={census.zero_suffix_failures} "
        f"zero-raw-three-failures={census.zero_raw_three_failures} "
        f"capped={census.capped} failures={failures}"
    )
    print(f"first failure: {census.first_failure or 'none'}")


if __name__ == "__main__":
    main()

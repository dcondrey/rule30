#!/usr/bin/env python3
"""Falsifiers for pull depth on hard-core-endpoint-derived queues.

Passing this program is bounded evidence only.  Every ``cut`` variable below
is the current inverse-cone right-edge diagonal, not the temporal cut formed
by the last cells of successive diagonals.  Its construction and queue replay
are exact.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from typing import Iterator

from constant_tail_pull_coordinate_depth import (
    COORDINATE_COUNTEREXAMPLE,
    Census as PullCensus,
    audit,
    update_type,
)
from constant_tail_queue import append_diagonal, normalize_queue, queue_step
from dyadic_periodicity_analyzer import BOUNDARY, cone_local
from rank_zero_separator import hard_core


Vector = tuple[int, ...]
ACTUAL_DEPTH_FOUR_ENDPOINT = tuple(
    map(
        int,
        "22221212121221212212212212122122"
        "21212121221222121222122221212122",
    )
)


@dataclass(slots=True)
class Census:
    endpoints: int = 0
    tail_queues: int = 0
    updates: int = 0
    pulls: int = 0
    maximum_depth: int = 0
    failures: int = 0
    capped: int = 0
    first_failure: str | None = None


def endpoint_diagonals(length: int) -> Iterator[tuple[Vector, Vector]]:
    """Generate all length-``length`` hard-core words and diagonals."""

    def extend(endpoint: Vector, diagonal: Vector) -> Iterator[tuple[Vector, Vector]]:
        if len(endpoint) == length:
            yield endpoint, diagonal
            return
        previous = endpoint[-1] if endpoint else 0
        for symbol in (1, 2):
            if previous == symbol == 1:
                continue
            yield from extend(
                endpoint + (symbol,),
                append_diagonal(diagonal, previous, symbol),
            )

    yield from extend((), ())


def random_endpoint(length: int, generator: random.Random) -> Vector:
    answer = []
    for _ in range(length):
        answer.append(
            2 if answer and answer[-1] == 1 else generator.choice((1, 2))
        )
    return tuple(answer)


def diagonal(endpoint: Vector) -> Vector:
    """Return the current right-edge diagonal after reading ``endpoint``."""
    answer: Vector = ()
    previous = 0
    for symbol in endpoint:
        answer = append_diagonal(answer, previous, symbol)
        previous = symbol
    return answer


def audit_derived(
    endpoint: Vector,
    cut: Vector,
    cap: int,
    census: Census,
) -> None:
    census.endpoints += 1
    tail = cut[-1]
    if tail not in (2, 3):
        return
    queue = normalize_queue(tuple(reversed(cut)), tail)
    local = PullCensus()
    audit(queue, tail, cap, local)
    census.tail_queues += 1
    census.updates += local.updates
    census.pulls += local.pulls
    census.maximum_depth = max(census.maximum_depth, local.maximum_depth)
    census.failures += local.coordinate_failures
    census.capped += local.capped
    if local.coordinate_failures and census.first_failure is None:
        census.first_failure = (
            f"endpoint={''.join(map(str, endpoint))} "
            f"cut={''.join(map(str, cut))} "
            f"{local.first_coordinate_failure}"
        )


def root_band_regression(max_length: int = 9) -> int:
    """Check the uniform last-three-root proof on every short endpoint."""

    checked = 0
    for length in range(3, max_length + 1):
        for _endpoint, cut in endpoint_diagonals(length):
            tail = cut[-1]
            if tail not in (2, 3):
                continue
            queue = normalize_queue(tuple(reversed(cut)), tail)
            roots = list(range(length))
            for time in range(100):
                following = queue_step(queue, tail)
                if following is None:
                    break
                successor = normalize_queue(following.queue, tail)
                differences = [
                    index
                    for index in range(1, len(queue))
                    if successor[index] != queue[index]
                ]
                pivot = differences[-1] if differences else 0
                kind = update_type(queue, successor)
                if time == 0 and kind == "C":
                    assert cut[:3] == (2, 0, 3)
                    assert queue[-3:] == (1, 0, 2)
                    assert pivot == length - 3
                child_root = roots[pivot]
                assert child_root >= length - 3
                roots.append(child_root)
                queue = successor
                checked += 1
    return checked


def controls(cap: int) -> tuple[str, int, int]:
    # Uniform time-zero root localization: a hard-core endpoint ending 21
    # gives current right-edge diagonal prefix 203, hence normalized reversed
    # queue suffix 102 and pull pivot N-3.
    assert BOUNDARY[1] == 2
    assert cone_local(2, 2) == 0
    assert BOUNDARY[2] == 1
    assert cone_local(1, 0) == 3
    for prefix in ((1,), (2,), (1, 2), (2, 2)):
        endpoint = prefix + (2, 1)
        assert diagonal(endpoint)[:3] == (2, 0, 3)
    assert root_band_regression() > 0

    # The normalized counterexample has no raw ambiguity in these cells.
    counter_prefix = tuple(reversed(COORDINATE_COUNTEREXAMPLE))[:3]
    assert counter_prefix == (2, 0, 0)
    assert counter_prefix != (2, 0, 3)

    endpoint = ACTUAL_DEPTH_FOUR_ENDPOINT
    assert len(endpoint) == 64 and hard_core(endpoint)
    cut = diagonal(endpoint)
    local = Census()
    audit_derived(endpoint, cut, cap, local)
    assert local.tail_queues == 1
    assert local.maximum_depth == 4
    assert local.failures == local.capped == 0
    return "".join(map(str, counter_prefix)), cut[-1], local.maximum_depth


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exact-length", type=int, default=26)
    parser.add_argument("--random-per-length", type=int, default=2_000)
    parser.add_argument("--orbit-cap", type=int, default=2_000)
    parser.add_argument("--seed", type=int, default=730_921)
    args = parser.parse_args()
    if (
        args.exact_length < 1
        or args.random_per_length < 0
        or args.orbit_cap < 1
    ):
        parser.error("invalid audit bound")

    bad_prefix, actual_tail, actual_depth = controls(args.orbit_cap)
    print(
        "controls: abstract coordinate counterexample diagonal-prefix="
        f"{bad_prefix} (hard-core pull requires 203); "
        f"actual endpoint tail={actual_tail} "
        f"maximum-depth={actual_depth} PASS",
        flush=True,
    )

    census = Census()
    for endpoint, cut in endpoint_diagonals(args.exact_length):
        audit_derived(endpoint, cut, args.orbit_cap, census)
    print(
        f"exact endpoint length={args.exact_length} "
        f"endpoints={census.endpoints} tail-queues={census.tail_queues} "
        f"failures={census.failures}",
        flush=True,
    )

    generator = random.Random(args.seed)
    for length in (64, 96, 128, 192, 256, 384, 512):
        before_endpoints = census.endpoints
        before_queues = census.tail_queues
        for _ in range(args.random_per_length):
            endpoint = random_endpoint(length, generator)
            audit_derived(endpoint, diagonal(endpoint), args.orbit_cap, census)
        print(
            f"random endpoint length={length} "
            f"endpoints={census.endpoints-before_endpoints} "
            f"tail-queues={census.tail_queues-before_queues} "
            f"failures={census.failures}",
            flush=True,
        )

    print(
        f"TOTAL endpoints={census.endpoints} tail-queues={census.tail_queues} "
        f"updates={census.updates} pulls={census.pulls} "
        f"maximum-depth={census.maximum_depth} failures={census.failures} "
        f"capped={census.capped}"
    )
    print(f"first failure: {census.first_failure or 'none'}")
    if census.failures or census.capped:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

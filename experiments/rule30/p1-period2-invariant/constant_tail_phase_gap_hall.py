#!/usr/bin/env python3
"""Solver-free Hall reduction for phase-labelled zero-gap retreat cover.

The finite product in ``zero_free_product`` proves the classification of a
successful zero-free-to-zero-free queue update for words of every length.
The orbit census is only a regression control for the remaining global
one-epoch lemma.
"""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass

from constant_tail_fanout_gaps import zero_blocks
from constant_tail_queue import (
    LIFT_GENERATORS,
    SYMBOL_QUOTIENT,
    Vector,
    normalize_queue,
    queue_step,
)
from constant_tail_retreat_budget import invariant_queues
from dyadic_periodicity_analyzer import BOUNDARY, cone_local


@dataclass(frozen=True, slots=True)
class ProductState:
    scan: int
    last_input: int
    length_parity: int
    output_has_zero: bool
    alternating_violation: bool


def decoded_endpoint(last_input: int, scan: int) -> int | None:
    if last_input not in (1, 2):
        return None
    previous = 3 - last_input
    candidates = tuple(
        endpoint
        for endpoint in (1, 2)
        if cone_local(previous, BOUNDARY[endpoint]) == scan
        and not (previous == endpoint == 1)
    )
    assert len(candidates) <= 1
    return candidates[0] if candidates else None


def zero_free_product(tail: int) -> tuple[int, int]:
    """Prove the complete zero-free-to-zero-free transition classification."""

    start = ProductState(tail, tail, 1, False, False)
    reachable = {start}
    frontier = deque((start,))
    finals = 0
    while frontier:
        state = frontier.popleft()
        endpoint = decoded_endpoint(state.last_input, state.scan)
        if endpoint is not None and not state.output_has_zero:
            boundary = BOUNDARY[endpoint]
            # The boundary is appended at index equal to the current input
            # length, whose parity is stored in ``length_parity``.
            boundary_position = state.length_parity
            expected_boundary = 2 if boundary_position == 0 else 1
            violation = (
                state.alternating_violation
                or tail != 2
                or boundary != expected_boundary
            )
            assert not violation
            assert endpoint == 2
            assert boundary == 1
            assert state.length_parity == 1
            finals += 1

        for symbol in (1, 2):
            if state.last_input == symbol == 2:
                continue
            scan = LIFT_GENERATORS[state.scan][symbol]
            output = SYMBOL_QUOTIENT[scan]
            position = state.length_parity
            expected = 2 if position == 0 else 1
            following = ProductState(
                scan,
                symbol,
                state.length_parity ^ 1,
                state.output_has_zero or output == 0,
                state.alternating_violation or output != expected,
            )
            if following not in reachable:
                reachable.add(following)
                frontier.append(following)
    if tail == 2:
        assert finals
    else:
        assert finals == 0
    return len(reachable), finals


@dataclass(frozen=True, slots=True)
class OrbitProfile:
    retreats: tuple[int, ...]
    eventless_retreats: tuple[int, ...]
    matched: tuple[tuple[int, tuple[int, int]], ...]


def canonical_profile(queue: Vector, tail: int, cap: int) -> OrbitProfile:
    events_by_time: dict[int, tuple[tuple[int, int], ...]] = {}
    retreats = []
    for time in range(cap):
        events_by_time[time] = tuple(
            (time, index) for index, _block in enumerate(zero_blocks(queue))
        )
        following = queue_step(queue, tail)
        if following is None:
            break
        queue = normalize_queue(following.queue, tail)
        if queue[-1] == 2:
            retreats.append(time)
    else:
        raise AssertionError("orbit reached the audit cap")

    assert all(
        right - left >= 2 for left, right in zip(retreats, retreats[1:])
    )
    eventless = []
    matched = []
    used = set()
    for retreat in retreats:
        candidates = events_by_time.get(retreat - 1, ()) + events_by_time.get(
            retreat, ()
        )
        if not candidates:
            eventless.append(retreat)
            continue
        event = candidates[0]
        # Retreat separation makes the two-row windows disjoint.
        assert event not in used
        used.add(event)
        matched.append((retreat, event))
    assert len(matched) == len(retreats) - len(eventless)
    return OrbitProfile(tuple(retreats), tuple(eventless), tuple(matched))


def orbit_control(max_length: int, cap: int) -> tuple[int, int, int]:
    queues = 0
    retreats = 0
    maximum_eventless = 0
    for length in range(1, max_length + 1):
        for tail in (2, 3):
            for queue in invariant_queues(length, tail):
                profile = canonical_profile(queue, tail, cap)
                queues += 1
                retreats += len(profile.retreats)
                maximum_eventless = max(
                    maximum_eventless, len(profile.eventless_retreats)
                )
                assert len(profile.eventless_retreats) <= 1
    return queues, retreats, maximum_eventless


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-length", type=int, default=12)
    parser.add_argument("--orbit-cap", type=int, default=128)
    args = parser.parse_args()
    if args.max_length < 1 or args.orbit_cap < 1:
        parser.error("bounds must be positive")

    for tail in (2, 3):
        states, finals = zero_free_product(tail)
        print(
            f"zero-free product tail={tail}: states={states} "
            f"zero-free-success finals={finals} PASS"
        )
    queues, retreats, maximum = orbit_control(
        args.max_length, args.orbit_cap
    )
    print(
        f"orbit control: queues={queues} retreats={retreats} "
        f"maximum-eventless-retreats={maximum} PASS"
    )


if __name__ == "__main__":
    main()

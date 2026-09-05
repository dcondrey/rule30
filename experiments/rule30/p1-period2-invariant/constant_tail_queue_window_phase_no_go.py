#!/usr/bin/env python3
"""Verify the all-window queue-phase nonclosure families.

For every requested end-window radius, the two families in
``RESULTS-QUEUE-WINDOW-PHASE-NO-GO.md`` give legal normalized queues with
the same length, end windows, endpoint/event data, and total D8 word action.
One legal queue update gives successors with different total D8 actions.

The all-radius proof is symbolic: the only choices are ``k`` odd for tail 2
and ``k == 2 (mod 4)`` for tail 3.  This program independently checks the
local D8 identities, the complete residue cycles, and concrete instances.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from constant_tail_queue import (
    NORMALIZED_FORBIDDEN,
    QueueStep,
    normalize_queue,
    queue_step,
)
from dyadic_periodicity_analyzer import IDENTITY, compose
from peel_lift_monoid import QUEUE_INPUT_ACTIONS


Vector = tuple[int, ...]
Transform = tuple[int, int, int, int]
NORMALIZE = (0, 1, 2, 1)


def word_action(word: Vector) -> Transform:
    """Return the exact D8 action of a normalized input word."""

    action = IDENTITY
    for symbol in word:
        action = compose(QUEUE_INPUT_ACTIONS[symbol], action)
    return action


def scan(start: int, word: Vector) -> tuple[Vector, int]:
    """Scan ``word`` from ``start`` and normalize the emitted row."""

    state = start
    emitted = []
    for symbol in word:
        state = QUEUE_INPUT_ACTIONS[symbol][state]
        emitted.append(NORMALIZE[state])
    return tuple(emitted), state


def avoids_invariant_factors(word: Vector) -> bool:
    return all(
        tuple(word[index : index + len(factor)]) != factor
        for factor in NORMALIZED_FORBIDDEN
        for index in range(len(word) - len(factor) + 1)
    )


def normalized_successor(queue: Vector, tail: int) -> tuple[Vector, QueueStep]:
    step = queue_step(queue, tail)
    assert step is not None
    return normalize_queue(step.queue, tail), step


@dataclass(frozen=True, slots=True)
class WindowPhaseSummary:
    length: int
    tail: int
    prefix: Vector
    suffix: Vector
    previous_endpoint: int
    final_scan_state: int
    emitted_endpoint: int
    event_boundary: int
    action: Transform


def summary(queue: Vector, tail: int, radius: int) -> WindowPhaseSummary:
    assert radius >= 0
    step = queue_step(queue, tail)
    assert step is not None
    nonleading = queue[1:]
    action = word_action(nonleading)
    assert action[tail] == step.final_scan_state
    return WindowPhaseSummary(
        length=len(queue),
        tail=tail,
        prefix=queue[:radius],
        suffix=queue[len(queue) - radius :] if radius else (),
        previous_endpoint=3 - queue[-1],
        final_scan_state=step.final_scan_state,
        emitted_endpoint=step.endpoint,
        event_boundary=step.queue[-1],
        action=action,
    )


def tail_two_pair(radius: int) -> tuple[int, Vector, Vector]:
    k = max(1, radius)
    if k % 2 == 0:
        k += 1
    common_left = (1,) * k
    common_right = (2,) + (1,) * k
    left = (2,) + common_left + (0, 0) + common_right
    right = (2,) + common_left + (1, 1) + common_right
    return k, left, right


def tail_three_pair(radius: int) -> tuple[int, Vector, Vector]:
    k = max(2, radius)
    k += (2 - k) % 4
    common_left = (1,) * k
    common_right = (0, 1) * k
    left = (3,) + common_left + (0, 0) + common_right
    right = (3,) + common_left + (1, 1) + common_right
    return k, left, right


def local_identity_control() -> None:
    h0, h1, h2 = QUEUE_INPUT_ACTIONS[:3]
    assert compose(h0, h0) == IDENTITY
    assert compose(h1, h1) == IDENTITY

    assert scan(1, (0, 0)) == ((1, 1), 1)
    assert scan(1, (1, 1)) == ((2, 1), 1)
    assert word_action((1, 1)) != word_action((2, 1))

    assert scan(3, (0, 0)) == ((2, 1), 3)
    assert scan(3, (1, 1)) == ((0, 1), 3)
    assert word_action((2, 1)) != word_action((0, 1))

    # The common post-core words use these two finite group cycles.  Their
    # displayed residues certify every k in the two infinite families.
    assert tuple(h1[h1[state]] for state in range(4)) == tuple(range(4))
    pair_action = compose(h1, h0)
    state = 3
    tail_three_cycle = []
    for residue in range(4):
        entering = state
        following = entering
        for _ in range(residue):
            following = pair_action[following]
        tail_three_cycle.append((residue, entering, following))
        state = h1[state]
    assert tuple(tail_three_cycle) == (
        (0, 3, 3),
        (1, 0, 3),
        (2, 3, 2),
        (3, 0, 2),
    )
    assert h2[1] == 3 and h1[3] == 0


def family_control(radius: int, tail: int) -> tuple[int, int]:
    if tail == 2:
        k, left, right = tail_two_pair(radius)
        assert k % 2 == 1
        assert avoids_invariant_factors(left)
        assert avoids_invariant_factors(right)
    else:
        k, left, right = tail_three_pair(radius)
        assert k % 4 == 2
        # The exceptional leading 3 initializes the scan and is not a
        # normalized input symbol.
        assert avoids_invariant_factors(left[1:])
        assert avoids_invariant_factors(right[1:])

    assert summary(left, tail, radius) == summary(right, tail, radius)
    following_left, step_left = normalized_successor(left, tail)
    following_right, step_right = normalized_successor(right, tail)
    assert step_left.endpoint == step_right.endpoint
    assert step_left.final_scan_state == step_right.final_scan_state

    # Equal neutral-block exit states make the post-core emitted suffixes
    # identical.  The unequal local emitted-block actions survive common
    # left and right D8 multiplication by cancellation.
    assert following_left[:radius] == following_right[:radius]
    if radius:
        assert following_left[-radius:] == following_right[-radius:]
    assert len(following_left) == len(following_right)
    assert word_action(following_left[1:]) != word_action(
        following_right[1:]
    )
    return k, len(left)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-window", type=int, default=64)
    args = parser.parse_args()
    if args.max_window < 0:
        parser.error("--max-window must be nonnegative")

    local_identity_control()
    last = {}
    for radius in range(args.max_window + 1):
        for tail in (2, 3):
            last[tail] = family_control(radius, tail)

    print("neutral blocks 00/11 and residue cycles: PASS")
    print(
        f"all end windows 0..{args.max_window}: PASS "
        f"(last tail-2 k/length={last[2]}, "
        f"tail-3 k/length={last[3]})"
    )


if __name__ == "__main__":
    main()

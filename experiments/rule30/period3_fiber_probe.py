#!/usr/bin/env python3
"""Exact finite-left fiber probes for primitive period-three Rule 30 traces.

There are two primitive binary necklaces of length three, represented here by
``001`` and ``011``.  For a prescribed center trace ``c`` and right column
``r``, Rule 30 reconstructs the column immediately to the left by

    l_t = c_(t+1) XOR (c_t OR r_t).

Consequently a zero phase has one freely selectable ``l_t`` while a one phase
has the fixed value ``1 XOR c_(t+1)``.  The complete left reconstruction is
tracked by two anti-diagonals.  Once the requested finite left depth has been
passed, a zero phase has a unique zero-emitting choice and a one phase is a
pure parity check.

The bounded searches in this file are falsifiers and finite certificates.  A
finite table is not a proof of either period-three exclusion.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import product


Vector = tuple[int, ...]
Frontier = tuple[int, int, int]


PERIOD_WORDS: tuple[Vector, ...] = ((0, 0, 1), (0, 1, 1))


def rule30_step(row: dict[int, int]) -> dict[int, int]:
    """Advance one finite dictionary row, retaining a harmless zero margin."""

    return {
        position: row.get(position - 1, 0)
        ^ (row.get(position, 0) | row.get(position + 1, 0))
        for position in range(min(row) - 1, max(row) + 2)
    }


def stroboscopic_local_fiber(word: Vector) -> tuple[Vector, ...]:
    """Return radius-three words producing ``word + word[0]`` at the center."""

    if word not in PERIOD_WORDS:
        raise ValueError("word must be 001 or 011")
    answer = []
    for bits in product((0, 1), repeat=7):
        row = {position: bits[position + 3] for position in range(-3, 4)}
        trace = []
        for _ in range(4):
            trace.append(row.get(0, 0))
            row = rule30_step(row)
        if tuple(trace) == word + (word[0],):
            answer.append(bits)
    return tuple(answer)


def frontier_step(word: Vector, frontier: Frontier, value: int) -> Frontier:
    """Feed one reconstructed column-minus-one value into the exact frontier.

    If ``frontier=(T,A,B)``, bit ``j-1`` of ``A`` is ``x(T-j,-j)`` and bit
    ``j-1`` of ``B`` is ``x(T-1-j,-j)``.  The returned newest anti-diagonal
    has length ``T+1``.
    """

    time, newest, older = frontier
    current = value & 1
    previous = current
    for depth in range(1, time + 1):
        right = (
            word[(time - 1) % len(word)]
            if depth == 1
            else (older >> (depth - 2)) & 1
        )
        center = (newest >> (depth - 1)) & 1
        previous ^= center | right
        current |= previous << depth
    return time + 1, current, newest


def or_parity(word: Vector, frontier: Frontier) -> int:
    """Parity making the next newly exposed initial-left cell zero."""

    time, newest, older = frontier
    if time == 0:
        return 0
    or_word = newest | (older << 1) | word[(time - 1) % len(word)]
    return (or_word & ((1 << time) - 1)).bit_count() & 1


def deepest_output(frontier: Frontier) -> int:
    time, newest, _ = frontier
    if time == 0:
        raise ValueError("the empty frontier has no output")
    return newest >> (time - 1) & 1


def direct_left(word: Vector, left_values: Vector) -> Vector:
    """Reconstruct initial left cells directly from a finite ``l`` column."""

    center = tuple(word[time % len(word)] for time in range(len(left_values) + 2))
    previous = center
    current = left_values
    answer = [current[0]]
    while len(current) >= 2:
        following = tuple(
            current[time + 1] ^ (current[time] | previous[time])
            for time in range(len(current) - 1)
        )
        previous, current = current, following
        answer.append(current[0])
    return tuple(answer)


def frontier_left(word: Vector, left_values: Vector) -> Vector:
    frontier: Frontier = (0, 0, 0)
    answer = []
    for value in left_values:
        frontier = frontier_step(word, frontier, value)
        answer.append(deepest_output(frontier))
    return tuple(answer)


@dataclass(frozen=True)
class Certificate:
    word: str
    left_depth: int
    first_empty_time: int | None
    peak_states: int
    zero_phase_forcings: int
    one_phase_checks: int


def certify_depth(word: Vector, depth: int, cap: int = 512) -> Certificate:
    """Exhaust the exact frontier tree for one finite-left depth."""

    states: set[Frontier] = {(0, 0, 0)}
    peak = 1
    zero_forcings = 0
    one_checks = 0
    for time in range(cap):
        center = word[time % len(word)]
        next_center = word[(time + 1) % len(word)]
        post_knee = time + 1 > depth
        following: set[Frontier] = set()
        for frontier in states:
            if center == 0:
                values = (or_parity(word, frontier),) if post_knee else (0, 1)
            else:
                fixed = 1 ^ next_center
                if post_knee and or_parity(word, frontier) != fixed:
                    continue
                values = (fixed,)
            for value in values:
                candidate = frontier_step(word, frontier, value)
                if not post_knee or deepest_output(candidate) == 0:
                    following.add(candidate)
        if post_knee:
            if center == 0:
                zero_forcings += len(states)
            else:
                one_checks += len(states)
        states = following
        peak = max(peak, len(states))
        if not states:
            return Certificate(
                "".join(map(str, word)),
                depth,
                time + 1,
                peak,
                zero_forcings,
                one_checks,
            )
    return Certificate(
        "".join(map(str, word)),
        depth,
        None,
        peak,
        zero_forcings,
        one_checks,
    )


def controls() -> None:
    expected = {
        (0, 0, 1): {
            "011010", "011011", "100001", "110000",
        },
        (0, 1, 1): {"000010", "000011", "111000", "111001"},
    }
    for word in PERIOD_WORDS:
        fiber = stroboscopic_local_fiber(word)
        assert len(fiber) == 8
        assert {"".join(map(str, bits[:6])) for bits in fiber} == expected[word]

    for word in PERIOD_WORDS:
        for length in range(1, 11):
            for values in product((0, 1), repeat=length):
                assert frontier_left(word, values) == direct_left(word, values)

    for word in PERIOD_WORDS:
        for length in range(1, 10):
            for values in product((0, 1), repeat=length):
                frontier: Frontier = (0, 0, 0)
                for value in values:
                    expected_output = value ^ or_parity(word, frontier)
                    frontier = frontier_step(word, frontier, value)
                    assert deepest_output(frontier) == expected_output

    # Fixed finite rows from the exact radius-three local fibers independently
    # reproduce the requested four center symbols.
    for word in PERIOD_WORDS:
        for bits in stroboscopic_local_fiber(word):
            row = {position: bits[position + 3] for position in range(-3, 4)}
            trace = []
            for _ in range(4):
                trace.append(row.get(0, 0))
                row = rule30_step(row)
            assert tuple(trace) == word + (word[0],)

    print("period-three controls: local fibers, direct/frontier, parity PASS")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-depth-011", type=int, default=36)
    parser.add_argument("--max-depth-001", type=int, default=24)
    parser.add_argument("--cap", type=int, default=512)
    args = parser.parse_args()
    if min(args.max_depth_011, args.max_depth_001) < 0 or args.cap < 1:
        parser.error("depths must be nonnegative and cap must be positive")

    controls()
    for word, maximum in (
        ((0, 1, 1), args.max_depth_011),
        ((0, 0, 1), args.max_depth_001),
    ):
        print(f"trace={''.join(map(str, word))}")
        for depth in range(maximum + 1):
            result = certify_depth(word, depth, args.cap)
            status = (
                f"empty@{result.first_empty_time}"
                if result.first_empty_time is not None
                else f"SURVIVES_CAP_{args.cap}"
            )
            print(
                f"  d={depth:2d} {status:>17s} peak={result.peak_states:7d} "
                f"zero-forcings={result.zero_phase_forcings:7d} "
                f"one-checks={result.one_phase_checks:7d}"
            )


if __name__ == "__main__":
    main()

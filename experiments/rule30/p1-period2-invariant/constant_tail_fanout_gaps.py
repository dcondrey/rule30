#!/usr/bin/env python3
"""Audit exact fan-out blocks, gap ranks, and retreat matching."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field

from constant_tail_queue import (
    LIFT_GENERATORS,
    SYMBOL_QUOTIENT,
    Vector,
    normalize_queue,
    queue_step,
)
from constant_tail_retreat_budget import invariant_queues


def raw_scan(queue: Vector, tail: int) -> Vector:
    state = tail
    answer = []
    for symbol in queue[1:]:
        state = LIFT_GENERATORS[state][symbol]
        answer.append(state)
    return tuple(answer)


def zero_block_formula(state: int, length: int) -> tuple[Vector, int]:
    """Return the exact raw output and exit state on ``0^length``."""

    output = []
    for _ in range(length):
        state = LIFT_GENERATORS[state][0]
        output.append(state)
    return tuple(output), state


def formula_controls(max_length: int = 64) -> int:
    for length in range(1, max_length + 1):
        assert zero_block_formula(0, length) == ((0,) * length, 0)
        assert zero_block_formula(1, length) == ((1,) * length, 1)
        expected_2 = tuple(3 if index % 2 == 0 else 2 for index in range(length))
        expected_3 = tuple(2 if index % 2 == 0 else 3 for index in range(length))
        assert zero_block_formula(2, length) == (
            expected_2,
            3 if length % 2 else 2,
        )
        assert zero_block_formula(3, length) == (
            expected_3,
            2 if length % 2 else 3,
        )

        queue = (2, 1) + (0,) * length + (1,)
        assert raw_scan(queue, 2) == (1,) * (length + 1) + (2,)
        following = queue_step(queue, 2)
        assert following is not None
        normalized = normalize_queue(following.queue, 2)
        assert normalized[:-1] == (2,) + (1,) * (length + 1) + (2,)
    return max_length


def zero_runs(word: Vector) -> tuple[int, ...]:
    runs = []
    index = 0
    while index < len(word):
        if word[index] != 0:
            index += 1
            continue
        following = index + 1
        while following < len(word) and word[following] == 0:
            following += 1
        runs.append(following - index)
        index = following
    return tuple(runs)


def zero_blocks(word: Vector) -> tuple[tuple[int, int], ...]:
    answer = []
    index = 0
    while index < len(word):
        if word[index] != 0:
            index += 1
            continue
        following = index + 1
        while following < len(word) and word[following] == 0:
            following += 1
        answer.append((index, following - index))
        index = following
    return tuple(answer)


def gap_encode(word: Vector) -> tuple[Vector, tuple[int, ...]]:
    """Losslessly encode nonzero colors and zero gaps following each color."""

    if not word or word[0] == 0:
        raise ValueError("a constant-tail queue starts with a nonzero symbol")
    colors = []
    gaps = []
    for symbol in word:
        if symbol:
            colors.append(symbol)
            gaps.append(0)
        else:
            gaps[-1] += 1
    return tuple(colors), tuple(gaps)


def gap_decode(encoded: tuple[Vector, tuple[int, ...]]) -> Vector:
    colors, gaps = encoded
    if len(colors) != len(gaps) or not colors:
        raise ValueError("gap colors and lengths must be nonempty and aligned")
    answer = []
    for color, gap in zip(colors, gaps):
        if color == 0 or gap < 0:
            raise ValueError("invalid zero-gap code")
        answer.append(color)
        answer.extend((0,) * gap)
    return tuple(answer)


def fanout_blocks(queue: Vector, tail: int) -> tuple[tuple[int, int], ...]:
    """Return ``(start,length)`` for zero runs entered in scan state 1."""

    state = tail
    answer = []
    index = 1
    while index < len(queue):
        if queue[index] != 0:
            state = LIFT_GENERATORS[state][queue[index]]
            index += 1
            continue
        following = index + 1
        while following < len(queue) and queue[following] == 0:
            following += 1
        if state == 1:
            answer.append((index, following - index))
        for _ in range(index, following):
            state = LIFT_GENERATORS[state][0]
        index = following
    return tuple(answer)


def next_power_of_two(value: int) -> int:
    return 1 << (value - 1).bit_length()


def gap_measures(word: Vector) -> tuple[object, ...]:
    runs = zero_runs(word)
    levels = tuple(sorted((value.bit_length() for value in runs), reverse=True))
    return (
        max(runs, default=0),
        sum(runs),
        sum(value.bit_length() for value in runs),
        sum(next_power_of_two(value) for value in runs),
        levels,
    )


MEASURE_NAMES = (
    "max-gap",
    "zero-total",
    "log-sum",
    "dyadic-capacity",
    "log-multiset",
)


@dataclass(slots=True)
class MeasureAudit:
    transitions: int = 0
    nonstrict_one: list[int] = field(default_factory=lambda: [0] * len(MEASURE_NAMES))
    increases_one: list[int] = field(default_factory=lambda: [0] * len(MEASURE_NAMES))
    first_nonstrict_one: list[str | None] = field(
        default_factory=lambda: [None] * len(MEASURE_NAMES)
    )
    two_step_transitions: int = 0
    nonstrict_two: list[int] = field(default_factory=lambda: [0] * len(MEASURE_NAMES))
    increases_two: list[int] = field(default_factory=lambda: [0] * len(MEASURE_NAMES))
    first_nonstrict_two: list[str | None] = field(
        default_factory=lambda: [None] * len(MEASURE_NAMES)
    )


def compare_measures(
    source: Vector,
    target: Vector,
    audit: MeasureAudit,
    two_step: bool,
) -> None:
    before = gap_measures(source)
    after = gap_measures(target)
    nonstrict = audit.nonstrict_two if two_step else audit.nonstrict_one
    increases = audit.increases_two if two_step else audit.increases_one
    first = audit.first_nonstrict_two if two_step else audit.first_nonstrict_one
    for index, (left, right) in enumerate(zip(before, after)):
        if not right < left:  # type: ignore[operator]
            nonstrict[index] += 1
            if first[index] is None:
                first[index] = (
                    f"source={''.join(map(str, source))} "
                    f"target={''.join(map(str, target))} "
                    f"before={left} after={right}"
                )
        if right > left:  # type: ignore[operator]
            increases[index] += 1


def audit_transition(queue: Vector, tail: int, audit: MeasureAudit) -> None:
    if not fanout_blocks(queue, tail):
        return
    following = queue_step(queue, tail)
    if following is None:
        return
    normalized = normalize_queue(following.queue, tail)
    inherited = normalized[:-1]
    assert len(inherited) == len(queue)
    assert inherited == (tail,) + tuple(
        SYMBOL_QUOTIENT[state] for state in raw_scan(queue, tail)
    )
    audit.transitions += 1
    compare_measures(queue, inherited, audit, False)

    second = queue_step(normalized, tail)
    if second is None:
        return
    normalized_second = normalize_queue(second.queue, tail)
    inherited_twice = normalized_second[:-2]
    assert len(inherited_twice) == len(queue)
    audit.two_step_transitions += 1
    compare_measures(queue, inherited_twice, audit, True)


@dataclass(slots=True)
class CoverAudit:
    queues: int = 0
    updates: int = 0
    retreats: int = 0
    fanouts: int = 0
    failures: int = 0
    capped: int = 0
    first_failure: str | None = None


def maximum_temporal_matching(
    retreat_times: tuple[int, ...], fanouts: tuple[tuple[int, int], ...]
) -> int:
    """Match retreats to distinct fan-out occurrences at time t or t-1."""

    right_to_left: dict[tuple[int, int], int] = {}

    def augment(retreat: int, seen: set[tuple[int, int]]) -> bool:
        for event in fanouts:
            if event[0] not in (retreat - 1, retreat) or event in seen:
                continue
            seen.add(event)
            previous = right_to_left.get(event)
            if previous is None or augment(previous, seen):
                right_to_left[event] = retreat
                return True
        return False

    return sum(augment(retreat, set()) for retreat in retreat_times)


def audit_orbit(
    queue: Vector,
    tail: int,
    cap: int,
    audit: CoverAudit,
    all_phase_gaps: bool = False,
) -> None:
    initial = queue
    retreat_times = []
    events = []
    for time in range(cap):
        blocks = (
            zero_blocks(queue) if all_phase_gaps else fanout_blocks(queue, tail)
        )
        events.extend((time, index) for index in range(len(blocks)))
        following = queue_step(queue, tail)
        if following is None:
            break
        queue = normalize_queue(following.queue, tail)
        if queue[-1] == 2:
            retreat_times.append(time)
        audit.updates += 1
    else:
        audit.capped += 1

    # One universal boundary credit may cover any one retreat.
    required = max(0, len(retreat_times) - 1)
    matched = maximum_temporal_matching(tuple(retreat_times), tuple(events))
    audit.queues += 1
    audit.retreats += len(retreat_times)
    audit.fanouts += len(events)
    if matched < required:
        audit.failures += 1
        if audit.first_failure is None:
            audit.first_failure = (
                f"tail={tail} R={''.join(map(str, initial))} "
                f"retreat-times={retreat_times} fanout-events={events} "
                f"matched={matched} required={required}"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first-length", type=int, default=1)
    parser.add_argument("--max-length", type=int, default=14)
    parser.add_argument("--orbit-cap", type=int, default=128)
    args = parser.parse_args()
    if not 1 <= args.first_length <= args.max_length or args.orbit_cap < 1:
        parser.error("invalid bounds")

    controls = formula_controls()
    print(f"zero-block and fan-out formulas: m=1..{controls} PASS")

    measures = MeasureAudit()
    cover = CoverAudit()
    phase_cover = CoverAudit()
    for length in range(args.first_length, args.max_length + 1):
        before = (cover.queues, cover.failures, phase_cover.failures)
        for tail in (2, 3):
            for queue in invariant_queues(length, tail):
                assert gap_decode(gap_encode(queue)) == queue
                audit_transition(queue, tail, measures)
                audit_orbit(queue, tail, args.orbit_cap, cover)
                audit_orbit(
                    queue,
                    tail,
                    args.orbit_cap,
                    phase_cover,
                    all_phase_gaps=True,
                )
        print(
            f"length={length:2d} queues={cover.queues-before[0]:7d} "
            f"fanout-cover-failures={cover.failures-before[1]:4d} "
            f"phase-gap-cover-failures="
            f"{phase_cover.failures-before[2]:4d}"
        )

    witness = tuple(map(int, "211012110000000001"))
    audit_orbit(witness, 2, args.orbit_cap, cover)
    audit_orbit(
        witness, 2, args.orbit_cap, phase_cover, all_phase_gaps=True
    )

    print(
        f"MEASURES fanout-transitions={measures.transitions} "
        f"two-step={measures.two_step_transitions}"
    )
    for index, name in enumerate(MEASURE_NAMES):
        print(
            f"  {name}: one-nonstrict={measures.nonstrict_one[index]} "
            f"one-increases={measures.increases_one[index]} "
            f"two-nonstrict={measures.nonstrict_two[index]} "
            f"two-increases={measures.increases_two[index]}"
        )
        print(
            f"    first-one={measures.first_nonstrict_one[index] or 'none'}"
        )
        print(
            f"    first-two={measures.first_nonstrict_two[index] or 'none'}"
        )

    print(
        f"COVER queues={cover.queues} updates={cover.updates} "
        f"retreats={cover.retreats} fanouts={cover.fanouts} "
        f"failures={cover.failures} capped={cover.capped}"
    )
    print(f"first cover failure: {cover.first_failure or 'none'}")
    print(
        f"PHASE-GAP-COVER queues={phase_cover.queues} "
        f"updates={phase_cover.updates} retreats={phase_cover.retreats} "
        f"events={phase_cover.fanouts} failures={phase_cover.failures} "
        f"capped={phase_cover.capped}"
    )
    print(
        "first phase-gap cover failure: "
        f"{phase_cover.first_failure or 'none'}"
    )


if __name__ == "__main__":
    main()

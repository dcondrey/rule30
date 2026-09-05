#!/usr/bin/env python3
"""Exact SAT minima for the invariant constant-tail queue language.

The regular-language cocycle has ``4^(h+1)`` states at horizon ``h``.  This
local spacetime encoding instead asks whether a normalized queue of length
``n`` survives ``h`` exact updates.  It is useful for extending the shortest-
survivor sequence, but every reported horizon is still finite evidence.

Run in the existing PySAT environment, for example

    uv run --project experiments/sygus-p3 python constant_tail_queue_sat.py
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from pysat.solvers import Solver

from constant_tail_queue import lifetime
from mortality_sat import Encoder
from peel_lift_monoid import LIFT_GENERATORS


OneHot = tuple[int, int, int, int]
Vector = tuple[int, ...]


@dataclass(frozen=True, slots=True)
class QueueInstance:
    length: int
    horizon: int
    tail: int
    encoder: Encoder
    initial: tuple[OneHot, ...]


def one_hot(encoder: Encoder, label: str) -> OneHot:
    variables = tuple(encoder.new(f"{label}.{state}") for state in range(4))
    encoder.add(*variables)
    for left in range(4):
        for right in range(left + 1, 4):
            encoder.add(-variables[left], -variables[right])
    return variables  # type: ignore[return-value]


def fix(encoder: Encoder, value: OneHot, state: int) -> None:
    encoder.add(value[state])


def build_instance(length: int, horizon: int, tail: int) -> QueueInstance:
    if length < 1 or horizon < 0 or tail not in (2, 3):
        raise ValueError("require length >= 1, horizon >= 0, tail in {2,3}")
    encoder = Encoder()
    rows = [
        tuple(one_hot(encoder, f"r.0.{index}") for index in range(length))
    ]
    initial = rows[0]
    fix(encoder, initial[0], tail)
    for value in initial[1:]:
        encoder.add(-value[3])
    encoder.add(initial[-1][1], initial[-1][2])
    encoder.add(-initial[-1][1], -initial[-1][2])

    # The invariant normalized queue language avoids 20, 22, and 011.
    for left, right in zip(initial, initial[1:]):
        encoder.add(-left[2], -right[0])
        encoder.add(-left[2], -right[2])
    for first, second, third in zip(initial, initial[1:], initial[2:]):
        encoder.add(-first[0], -second[1], -third[1])

    for time in range(horizon):
        current = rows[-1]
        following = tuple(
            one_hot(encoder, f"r.{time + 1}.{index}")
            for index in range(len(current) + 1)
        )
        rows.append(following)
        fix(encoder, following[0], tail)

        scan = tuple(
            one_hot(encoder, f"s.{time}.{index}")
            for index in range(len(current))
        )
        fix(encoder, scan[0], tail)
        for index in range(1, len(current)):
            previous = scan[index - 1]
            symbol = current[index]
            output = scan[index]
            for previous_state in range(4):
                for input_state in range(3):
                    output_state = LIFT_GENERATORS[previous_state][input_state]
                    encoder.add(
                        -previous[previous_state],
                        -symbol[input_state],
                        output[output_state],
                    )
            for raw_state in range(4):
                normalized = 1 if raw_state == 3 else raw_state
                encoder.add(-output[raw_state], following[index][normalized])

        last = current[-1]
        final = scan[-1]
        boundary = following[-1]
        allowed_pairs = {(1, 0), (1, 2), (2, 2)}
        for last_state in range(4):
            for final_state in range(4):
                if (last_state, final_state) not in allowed_pairs:
                    encoder.add(-last[last_state], -final[final_state])
        # (last,final)=(1,0) appends 2; either final-2 case appends 1.
        encoder.add(-last[1], -final[0], boundary[2])
        encoder.add(-final[2], boundary[1])

    return QueueInstance(length, horizon, tail, encoder, initial)


def solve(instance: QueueInstance) -> Vector | None:
    with Solver(
        name="cadical195", bootstrap_with=instance.encoder.clauses
    ) as solver:
        if not solver.solve():
            return None
        positive = {literal for literal in solver.get_model() if literal > 0}
    word = tuple(
        next(state for state, literal in enumerate(value) if literal in positive)
        for value in instance.initial
    )
    survived = lifetime(word, instance.tail, instance.horizon)
    assert survived is None or survived >= instance.horizon
    return word


EXPECTED_MINIMUM = {
    2: (
        1, 1, 3, 5, 5, 5, 10, 10, 10, 10, 17, 18, 18, 18, 22, 23, 23,
        26, 26, 30, 33,
    ),
    3: (
        2, 2, 3, 5, 5, 5, 10, 10, 10, 13, 14, 15, 16, 16, 24, 24, 26,
        26, 31, 31, 32,
    ),
}


def minimum_length(
    horizon: int, tail: int, start: int, maximum: int
) -> tuple[int, Vector]:
    for length in range(start, maximum + 1):
        word = solve(build_instance(length, horizon, tail))
        if word is not None:
            return length, word
    raise RuntimeError(
        f"no survivor found through length {maximum}: tail={tail}, h={horizon}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-horizon", type=int, default=11)
    parser.add_argument("--max-length", type=int, default=30)
    args = parser.parse_args()
    if args.max_horizon < 0 or args.max_length < 1:
        parser.error("bounds must be nonnegative and max length positive")

    for tail in (2, 3):
        start = 1 if tail == 2 else 2
        for horizon in range(args.max_horizon + 1):
            minimum, word = minimum_length(
                horizon, tail, start, args.max_length
            )
            if horizon < len(EXPECTED_MINIMUM[tail]):
                assert minimum == EXPECTED_MINIMUM[tail][horizon]
            print(
                f"tail={tail} horizon={horizon:2d} min-length={minimum:2d} "
                f"w={''.join(map(str, word))}"
            )
            start = minimum


if __name__ == "__main__":
    main()

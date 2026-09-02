#!/usr/bin/env python3
"""Describe exact source cylinders surviving to the charged midpoint.

This is an exploratory structural diagnostic for the deterministic halving
recurrence.  It reports, but does not assume, uniqueness of the right half and
of the forced continuation prefix.
"""

from __future__ import annotations

import argparse

from constant_tail_bitsliced_derivative import (
    append_edge_bits,
    bit_state,
    forced_value_bits,
    newest_affine_bits,
    scenario_state,
)
from constant_tail_scale import Vector
from rank_zero_separator import hard_core_prefixes


def midpoint_trace(word: Vector, tail: int) -> Vector | None:
    """Return the legal forced prefix through ``ceil(n/2)+1``, if any."""

    endpoint = []
    edge = ()
    for value in (0,) * len(word) + word:
        state = bit_state(value, 1)
        edge = append_edge_bits(
            edge, endpoint[-1] if endpoint else None, state, 1
        )
        endpoint.append(state)

    horizon = (len(word) + 1) // 2 + 1
    previous = word[-1]
    answer = []
    for _ in range(horizon):
        affine = newest_affine_bits(edge, endpoint[-1], 1)
        state = forced_value_bits(affine, tail, 1)
        value = scenario_state(state, 0)
        if value not in (1, 2) or previous == value == 1:
            return None
        edge = append_edge_bits(edge, endpoint[-1], state, 1)
        endpoint.append(state)
        answer.append(value)
        previous = value
    return tuple(answer)


def common_suffix(words: list[Vector]) -> Vector:
    if not words:
        return ()
    length = 0
    while length < len(words[0]) and len(
        {word[-1 - length] for word in words}
    ) == 1:
        length += 1
    return words[0][len(words[0]) - length :]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first-length", type=int, default=1)
    parser.add_argument("--last-length", type=int, default=18)
    args = parser.parse_args()
    if not 1 <= args.first_length <= args.last_length:
        parser.error("invalid length interval")

    for length in range(args.first_length, args.last_length + 1):
        cut = length // 2
        for tail in (2, 3):
            survivors: list[Vector] = []
            continuations: set[Vector] = set()
            for word in hard_core_prefixes(length):
                trace = midpoint_trace(word, tail)
                if trace is not None:
                    survivors.append(word)
                    continuations.add(trace)
            if not survivors:
                continue
            right_halves = {word[cut:] for word in survivors}
            suffix = common_suffix(survivors)
            print(
                f"length={length:2d} tail={tail} "
                f"horizon={(length+1)//2+1:2d} "
                f"survivors={len(survivors):5d} "
                f"left-halves={len({word[:cut] for word in survivors}):5d} "
                f"right-halves={len(right_halves):3d} "
                f"continuations={len(continuations):3d} "
                f"free-prefix={length-len(suffix):2d} "
                f"common-suffix={''.join(map(str, suffix))}"
            )
            if len(right_halves) == 1:
                print(
                    "  unique-right="
                    f"{''.join(map(str, next(iter(right_halves))))}"
                )
            if len(continuations) == 1:
                print(
                    "  unique-continuation="
                    f"{''.join(map(str, next(iter(continuations))))}"
                )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Falsify the proposed one-credit scale-halving recurrence."""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from functools import lru_cache

from constant_tail_bitsliced_derivative import (
    bit_state,
    bitsliced_trace_states,
    scenario_state,
)
from constant_tail_scale import Vector, hard_core_extension_length
from rank_zero_separator import hard_core_prefixes


@lru_cache(maxsize=None)
def survival(word: Vector, tail: int) -> int:
    if not word:
        return 0
    extension, _ = bitsliced_trace_states(
        [bit_state(value, 1) for value in word], len(word), tail, 1
    )
    literal = tuple(scenario_state(state, 0) for state in extension)
    return hard_core_extension_length(word, literal)


@dataclass(slots=True)
class Census:
    cases: int = 0
    failures: int = 0
    maximum_excess: int = -10**9
    first_failure: str | None = None
    deterministic_failures: int = 0
    deterministic_maximum_excess: int = -10**9
    deterministic_first_failure: str | None = None


def audit_word(word: Vector, census: Census) -> None:
    length = len(word)
    cut = length // 2
    halves = (word[:cut], word[cut:])
    inherited = max(
        survival(half, tail) for half in halves for tail in (2, 3)
    )
    bound = (length + 1) // 2 + 1 + inherited
    deterministic_bound = (
        (length + 1) // 2 + 1 + survival(halves[0], 2)
    )
    for tail in (2, 3):
        value = survival(word, tail)
        excess = value - bound
        census.cases += 1
        census.maximum_excess = max(census.maximum_excess, excess)
        if excess > 0:
            census.failures += 1
            if census.first_failure is None:
                census.first_failure = (
                    f"tail={tail} W={''.join(map(str, word))} "
                    f"s={value} bound={bound} inherited={inherited} "
                    f"half-data="
                    f"{[( ''.join(map(str, half)), survival(half, 2), survival(half, 3)) for half in halves]}"
                )
        deterministic_excess = value - deterministic_bound
        if length >= 4:
            census.deterministic_maximum_excess = max(
                census.deterministic_maximum_excess,
                deterministic_excess,
            )
        if length >= 4 and deterministic_excess > 0:
            census.deterministic_failures += 1
            if census.deterministic_first_failure is None:
                census.deterministic_first_failure = (
                    f"tail={tail} W={''.join(map(str, word))} "
                    f"s={value} deterministic-bound={deterministic_bound} "
                    f"left={''.join(map(str, halves[0]))} "
                    f"left-tail2={survival(halves[0], 2)}"
                )


def random_hard_core(length: int, generator: random.Random) -> Vector:
    word = []
    for _ in range(length):
        word.append(
            2 if word and word[-1] == 1 else generator.choice((1, 2))
        )
    return tuple(word)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first-length", type=int, default=21)
    parser.add_argument("--last-length", type=int, default=23)
    parser.add_argument("--random-per-length", type=int, default=1000)
    args = parser.parse_args()
    if not 1 <= args.first_length <= args.last_length:
        parser.error("invalid exhaustive length interval")

    census = Census()
    for length in range(args.first_length, args.last_length + 1):
        before = (
            census.cases,
            census.failures,
            census.deterministic_failures,
        )
        for word in hard_core_prefixes(length):
            audit_word(word, census)
        print(
            f"length={length:2d} cases={census.cases-before[0]:7d} "
            f"failures={census.failures-before[1]:4d} "
            f"maximum-excess={census.maximum_excess} "
            f"deterministic-failures="
            f"{census.deterministic_failures-before[2]:4d} "
            f"deterministic-maximum-excess="
            f"{census.deterministic_maximum_excess}"
        )

    generator = random.Random(30030)
    for length in (24, 32, 48, 64):
        before = (census.failures, census.deterministic_failures)
        for _ in range(args.random_per_length):
            audit_word(random_hard_core(length, generator), census)
        print(
            f"random-length={length:2d} cases={2*args.random_per_length:5d} "
            f"failures={census.failures-before[0]:4d} "
            f"deterministic-failures="
            f"{census.deterministic_failures-before[1]:4d} "
            f"maximum-excess={census.maximum_excess} "
            f"deterministic-maximum-excess="
            f"{census.deterministic_maximum_excess}"
        )

    print(
        f"TOTAL cases={census.cases} failures={census.failures} "
        f"maximum-excess={census.maximum_excess} "
        f"deterministic-failures={census.deterministic_failures} "
        f"deterministic-maximum-excess="
        f"{census.deterministic_maximum_excess}"
    )
    print(f"first failure: {census.first_failure or 'none'}")
    print(
        "first deterministic failure: "
        f"{census.deterministic_first_failure or 'none'}"
    )


if __name__ == "__main__":
    main()

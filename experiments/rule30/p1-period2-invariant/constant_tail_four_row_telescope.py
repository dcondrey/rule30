#!/usr/bin/env python3
"""Falsify the projected four-row endpoint telescope."""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

from constant_tail_bitsliced_derivative import (
    bitsliced_trace_states,
    scenario_affine,
    scenario_state,
)
from constant_tail_scale import Vector, hard_core_extension_length
from constant_tail_zero_prefix_bitsliced import zero_prefix_word_states
from rank_zero_separator import hard_core_prefixes


SELECTED_COORDINATES = {2: (0, 1), 3: (0, 2)}
WINDOW = 4


@dataclass(slots=True)
class Census:
    cases: int = 0
    windows: int = 0
    failures: int = 0
    first_failure: str | None = None


def audit_word(word: Vector, tail: int, census: Census) -> None:
    states, mask = zero_prefix_word_states(word)
    extension, affines = bitsliced_trace_states(
        states, len(word), tail, mask
    )
    original = tuple(scenario_state(state, 0) for state in extension)
    survival = hard_core_extension_length(word, original)
    coordinates = SELECTED_COORDINATES[tail]
    census.cases += 1

    for start in range(max(0, survival - WINDOW + 1)):
        census.windows += 1
        if start >= len(word):
            failure = "window starts beyond the last zero-prefix token"
        else:
            signature = tuple(
                scenario_affine(affines[row], start)[coordinate]
                for row in range(start, start + WINDOW)
                for coordinate in coordinates
            )
            all_zero = tuple(
                scenario_affine(affines[row], len(word))[coordinate]
                for row in range(start, start + WINDOW)
                for coordinate in coordinates
            )
            failure = (
                "four-row signatures coincide"
                if signature == all_zero
                else None
            )
        if failure is not None:
            census.failures += 1
            if census.first_failure is None:
                census.first_failure = (
                    f"tail={tail} W={''.join(map(str, word))} "
                    f"n={len(word)} s={survival} start={start}: {failure}"
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
    parser.add_argument("--first-length", type=int, default=17)
    parser.add_argument("--last-length", type=int, default=23)
    parser.add_argument("--random-per-length", type=int, default=1000)
    args = parser.parse_args()
    if not 1 <= args.first_length <= args.last_length:
        parser.error("invalid exhaustive length interval")

    census = Census()
    for length in range(args.first_length, args.last_length + 1):
        before = Census(census.cases, census.windows, census.failures)
        for word in hard_core_prefixes(length):
            for tail in (2, 3):
                audit_word(word, tail, census)
        print(
            f"length={length:2d} cases={census.cases-before.cases:7d} "
            f"windows={census.windows-before.windows:7d} "
            f"failures={census.failures-before.failures:4d}",
            flush=True,
        )

    generator = random.Random(30030)
    for length in (24, 32, 48, 64):
        before = Census(census.cases, census.windows, census.failures)
        for _ in range(args.random_per_length):
            for tail in (2, 3):
                audit_word(random_hard_core(length, generator), tail, census)
        print(
            f"random-length={length:2d} "
            f"cases={census.cases-before.cases:5d} "
            f"windows={census.windows-before.windows:6d} "
            f"failures={census.failures-before.failures:4d}",
            flush=True,
        )

    print(
        f"TOTAL cases={census.cases} windows={census.windows} "
        f"failures={census.failures}"
    )
    print(f"first failure: {census.first_failure or 'none'}")


if __name__ == "__main__":
    main()

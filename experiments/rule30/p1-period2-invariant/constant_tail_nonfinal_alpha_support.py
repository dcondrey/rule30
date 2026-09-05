#!/usr/bin/env python3
"""Held-out falsifier for nonfinal alpha diagonal support.

A finite pass is evidence only.  The candidate theorem is stated in
PREREGISTRATION-NONFINAL-ALPHA-SUPPORT.md.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

from constant_tail_pull_row_projected_support import scenario_extension
from constant_tail_zero_prefix_bitsliced import adjacent_scenarios_differ
from rank_zero_separator import hard_core_prefixes


Vector = tuple[int, ...]


@dataclass(slots=True)
class Census:
    cases: int = 0
    rows: int = 0
    failures: int = 0
    first_failure: str | None = None


def audit(word: Vector, tail: int, census: Census) -> None:
    _extension, affines, survival = scenario_extension(word, tail)
    census.cases += 1
    for row in range(max(0, survival - 1)):
        census.rows += 1
        alpha = affines[row][0]
        support = tuple(
            token
            for token in range(row, len(word))
            if adjacent_scenarios_differ(alpha, token)
        )
        if support:
            continue
        census.failures += 1
        if census.first_failure is None:
            census.first_failure = (
                f"tail={tail} W={''.join(map(str, word))} "
                f"n={len(word)} survival={survival} row={row}"
            )


def random_hard_core(length: int, generator: random.Random) -> Vector:
    word: list[int] = []
    for _ in range(length):
        word.append(
            2 if word and word[-1] == 1 else generator.choice((1, 2))
        )
    return tuple(word)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first-length", type=int, default=18)
    parser.add_argument("--last-length", type=int, default=23)
    parser.add_argument("--random-per-length", type=int, default=2_000)
    parser.add_argument("--seed", type=int, default=30042)
    args = parser.parse_args()
    if not 1 <= args.first_length <= args.last_length:
        parser.error("invalid exact length range")
    if args.random_per_length < 0:
        parser.error("random count must be nonnegative")

    census = Census()
    for length in range(args.first_length, args.last_length + 1):
        before = Census(census.cases, census.rows, census.failures)
        for word in hard_core_prefixes(length):
            for tail in (2, 3):
                audit(word, tail, census)
        print(
            f"length={length:3d} cases={census.cases-before.cases:7d} "
            f"nonfinal-rows={census.rows-before.rows:7d} "
            f"failures={census.failures-before.failures}",
            flush=True,
        )

    generator = random.Random(args.seed)
    for length in (24, 32, 48, 64, 96, 128):
        before = Census(census.cases, census.rows, census.failures)
        for _ in range(args.random_per_length):
            word = random_hard_core(length, generator)
            for tail in (2, 3):
                audit(word, tail, census)
        print(
            f"random-length={length:3d} "
            f"cases={census.cases-before.cases:7d} "
            f"nonfinal-rows={census.rows-before.rows:7d} "
            f"failures={census.failures-before.failures}",
            flush=True,
        )

    print(
        f"TOTAL cases={census.cases} nonfinal-rows={census.rows} "
        f"failures={census.failures}"
    )
    print(f"first failure: {census.first_failure or 'none'}")
    if census.failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

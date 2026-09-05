#!/usr/bin/env python3
"""Deterministic evolutionary falsifier for the binary-wedge bound.

This searches for a binary source W whose constant-cut continuation stays
binary for more than ``len(W)+1`` cells.  Failure to find one is finite
evidence only.  Any reported violation can be replayed literally by
``late_pull_diagonal_sat.literal_extension``.
"""

from __future__ import annotations

import argparse
import random

from binary_wedge_horizon import first_nonbinary
from constant_tail_bitsliced_derivative import (
    bitsliced_trace_states,
    scenario_state,
)
from constant_tail_late_pull_horizon import pack_words
from constant_tail_scale import Vector
from late_pull_diagonal_sat import literal_extension


def scores(words: list[Vector], tail: int) -> list[int]:
    packed, mask = pack_words(words)
    extension, _affines = bitsliced_trace_states(
        packed, len(words[0]), tail, mask
    )
    return [
        first_nonbinary(extension, scenario)
        for scenario in range(len(words))
    ]


def mutate(
    word: Vector, mate: Vector, generator: random.Random
) -> Vector:
    n = len(word)
    cut = generator.randrange(n + 1)
    child = list(word[:cut] + mate[cut:])
    flips = 1
    while generator.random() < 0.45:
        flips += 1
    for _ in range(flips):
        position = generator.randrange(n)
        child[position] = 3 - child[position]
    return tuple(child)


def initial_population(
    n: int, size: int, generator: random.Random
) -> list[Vector]:
    seeds: list[Vector] = [
        (1,) * n,
        (2,) * n,
        tuple(1 + index % 2 for index in range(n)),
        tuple(2 - index % 2 for index in range(n)),
    ]
    while len(seeds) < size:
        seeds.append(tuple(generator.choice((1, 2)) for _ in range(n)))
    return seeds[:size]


def search(
    n: int,
    tail: int,
    population_size: int,
    generations: int,
    generator: random.Random,
) -> tuple[int, Vector, int]:
    population = initial_population(n, population_size, generator)
    best_score = -1
    best_word: Vector = ()
    evaluations = 0

    for _generation in range(generations):
        fitness = scores(population, tail)
        evaluations += len(population)
        ranked = sorted(
            zip(fitness, population), reverse=True
        )
        if ranked[0][0] > best_score:
            best_score, best_word = ranked[0]
        elite_count = max(4, population_size // 8)
        elite = [word for _score, word in ranked[:elite_count]]
        following = elite.copy()
        while len(following) < population_size:
            following.append(
                mutate(
                    generator.choice(elite),
                    generator.choice(elite),
                    generator,
                )
            )
        population = following

    literal = literal_extension(best_word, tail, 2 * n)
    expected = next(
        (
            index
            for index, state in enumerate(literal)
            if state not in (1, 2)
        ),
        len(literal),
    )
    assert expected == best_score
    packed, mask = pack_words([best_word])
    replay, _affines = bitsliced_trace_states(packed, n, tail, mask)
    assert all(
        scenario_state(state, 0) == literal[index]
        for index, state in enumerate(replay)
    )
    return best_score, best_word, evaluations


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--lengths", type=int, nargs="+", default=(24, 32, 48, 64, 96, 128)
    )
    parser.add_argument("--population", type=int, default=256)
    parser.add_argument("--generations", type=int, default=350)
    parser.add_argument("--seed", type=int, default=30044)
    args = parser.parse_args()
    if (
        not args.lengths
        or min(args.lengths) < 1
        or args.population < 4
        or args.generations < 1
    ):
        parser.error("invalid search parameters")

    generator = random.Random(args.seed)
    failures = 0
    for n in args.lengths:
        for tail in (2, 3):
            maximum, word, evaluations = search(
                n,
                tail,
                args.population,
                args.generations,
                generator,
            )
            failures += int(maximum > n + 1)
            print(
                f"n={n:3d} c={tail} M={maximum:3d} "
                f"evaluations={evaluations} "
                f"W={''.join(map(str, word))}",
                flush=True,
            )

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

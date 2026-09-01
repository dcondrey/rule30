#!/usr/bin/env python3
"""Bit-level genetic search for long-lived rank-zero endpoint witnesses.

This is a solver-free falsifier/conjecture probe.  Every genome is a
hard-core endpoint prefix.  Fitness is recomputed from its inverse cut with an
exact zero tail; GA state never enters the Rule 30 verifier.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from functools import lru_cache
from pathlib import Path


HERE = Path(__file__).resolve().parent
INVARIANT_DIR = HERE.parent / "rule30" / "p1-period2-invariant"
sys.path.insert(0, str(INVARIANT_DIR))

from dyadic_periodicity_analyzer import (  # noqa: E402
    inverse_cone_diagonal,
    terminal_cone,
)
from rank_zero_separator import hard_core_prefix_length  # noqa: E402


Genome = tuple[int, ...]


def repair(values: list[int]) -> Genome:
    """Deterministically replace the second symbol of every `11` by `2`."""

    for index in range(1, len(values)):
        if values[index - 1] == values[index] == 1:
            values[index] = 2
    return tuple(values)


def impose_prefix(genome: Genome, prefix: Genome | None) -> Genome:
    if not prefix:
        return genome
    values = list(prefix + genome[len(prefix) :])
    return repair(values)


def random_genome(cutoff: int, rng: random.Random) -> Genome:
    values = []
    for _ in range(cutoff):
        if values and values[-1] == 1:
            values.append(2)
        else:
            values.append(1 if rng.random() < 0.48 else 2)
    return tuple(values)


def seed_population(
    cutoff: int,
    size: int,
    rng: random.Random,
    initial_pattern: Genome | None = None,
) -> list[Genome]:
    seeds = [
        tuple(1 if index % 2 == 0 else 2 for index in range(cutoff)),
        (2,) * cutoff,
        tuple((1, 2, 2)[index % 3] for index in range(cutoff)),
        tuple((1, 2, 2, 2)[index % 4] for index in range(cutoff)),
        repair(
            [1 if (index & (index + 1)) == 0 else 2 for index in range(cutoff)]
        ),
    ]
    if initial_pattern:
        repeated = tuple(
            initial_pattern[index % len(initial_pattern)]
            for index in range(cutoff)
        )
        seeds.append(repair(list(repeated)))
        # Populate the initial basin with nearby phase-slip variants instead
        # of relying on crossover to rediscover it from unrelated genomes.
        for _ in range(max(4, size // 6)):
            seeds.append(mutate(seeds[-1], rng, 0.035))
    while len(seeds) < size:
        seeds.append(random_genome(cutoff, rng))
    return list(dict.fromkeys(seeds))


def crossover(left: Genome, right: Genome, rng: random.Random) -> Genome:
    if len(left) < 2:
        return left
    first = rng.randrange(1, len(left))
    if rng.random() < 0.35:
        second = rng.randrange(first, len(left))
        values = list(left[:first] + right[first:second] + left[second:])
    else:
        values = list(left[:first] + right[first:])
    return repair(values)


def mutate(genome: Genome, rng: random.Random, rate: float) -> Genome:
    values = list(genome)
    for index in range(len(values)):
        if rng.random() >= rate:
            continue
        if values[index] == 1:
            values[index] = 2
        elif (index == 0 or values[index - 1] != 1) and (
            index + 1 == len(values) or values[index + 1] != 1
        ):
            values[index] = 1
    # A phase slip is a useful nonlocal mutation in an alternating parent.
    if values and rng.random() < 0.25:
        start = rng.randrange(len(values))
        stop = min(len(values), start + rng.randrange(1, min(9, len(values)) + 1))
        values[start:stop] = reversed(values[start:stop])
    return repair(values)


def search(
    cutoff: int,
    population_size: int,
    generations: int,
    mutation_rate: float,
    seed: int,
    initial_pattern: Genome | None = None,
    fixed_prefix: Genome | None = None,
    tail: int = 0,
) -> dict[str, object]:
    rng = random.Random(seed)
    horizon = 2 * cutoff + 2

    @lru_cache(maxsize=None)
    def fitness(genome: Genome) -> int:
        cut_prefix = inverse_cone_diagonal(genome)
        endpoint = terminal_cone(cut_prefix + (tail,) * (horizon - cutoff))
        assert endpoint[:cutoff] == genome
        return hard_core_prefix_length(endpoint)

    population = seed_population(
        cutoff, population_size, rng, initial_pattern=initial_pattern
    )
    population = [impose_prefix(genome, fixed_prefix) for genome in population]
    while len(population) < population_size:
        population.append(impose_prefix(random_genome(cutoff, rng), fixed_prefix))

    best = max(population, key=lambda genome: (fitness(genome), genome))
    history = [(0, fitness(best))]
    stagnant = 0
    for generation in range(1, generations + 1):
        ranked = sorted(
            set(population),
            key=lambda genome: (fitness(genome), genome),
            reverse=True,
        )
        if fitness(ranked[0]) > fitness(best):
            best = ranked[0]
            history.append((generation, fitness(best)))
            stagnant = 0
        else:
            stagnant += 1
        if fitness(best) >= horizon:
            break

        elite_count = max(4, population_size // 8)
        elites = ranked[:elite_count]
        following = list(elites)
        # Immigrants keep the population from collapsing onto one wallpaper.
        immigrant_count = max(2, population_size // 12)
        following.extend(
            impose_prefix(random_genome(cutoff, rng), fixed_prefix)
            for _ in range(immigrant_count)
        )
        adaptive_rate = mutation_rate * (1.8 if stagnant >= 15 else 1.0)
        pool = ranked[: max(elite_count, len(ranked) // 2)]
        while len(following) < population_size:
            competitors = rng.sample(pool, min(4, len(pool)))
            left = max(competitors, key=lambda genome: fitness(genome))
            competitors = rng.sample(pool, min(4, len(pool)))
            right = max(competitors, key=lambda genome: fitness(genome))
            child = crossover(left, right, rng)
            child = mutate(child, rng, adaptive_rate)
            following.append(impose_prefix(child, fixed_prefix))
        population = following

    cut_prefix = inverse_cone_diagonal(best)
    endpoint = terminal_cone(cut_prefix + (tail,) * (horizon - cutoff))
    survival = hard_core_prefix_length(endpoint)
    return {
        "cutoff": cutoff,
        "tail": tail,
        "horizon": horizon,
        "survival": survival,
        "linear_bound_falsified": survival >= horizon,
        "endpoint_prefix": "".join(map(str, best)),
        "cut_prefix": "".join(map(str, cut_prefix)),
        "failure_symbols": "".join(map(str, endpoint[survival : survival + 2])),
        "evaluations": fitness.cache_info().misses,
        "improvements": history,
        "seed": seed,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cutoffs", type=int, nargs="+", default=[23, 32, 48, 64])
    parser.add_argument("--population", type=int, default=96)
    parser.add_argument("--generations", type=int, default=100)
    parser.add_argument("--mutation-rate", type=float, default=0.045)
    parser.add_argument("--seed", type=int, default=30047)
    parser.add_argument(
        "--tail",
        type=int,
        choices=(0, 2, 3),
        default=0,
        help="exact eventual cut tail (0 for rank zero; 2/3 after first-infinite-tail)",
    )
    parser.add_argument(
        "--initial-pattern",
        help="optional hard-core 1/2 word, repeated to seed every cutoff",
    )
    parser.add_argument(
        "--fixed-prefix",
        help="optional hard-core 1/2 prefix held fixed under every mutation",
    )
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    if args.population < 8 or args.generations < 1:
        parser.error("population must be >=8 and generations must be positive")
    initial_pattern = None
    if args.initial_pattern is not None:
        if set(args.initial_pattern) - {"1", "2"} or "11" in args.initial_pattern:
            parser.error("initial pattern must be a nonempty hard-core 1/2 word")
        if not args.initial_pattern:
            parser.error("initial pattern must not be empty")
        initial_pattern = tuple(map(int, args.initial_pattern))
    fixed_prefix = None
    if args.fixed_prefix is not None:
        if set(args.fixed_prefix) - {"1", "2"} or "11" in args.fixed_prefix:
            parser.error("fixed prefix must be a nonempty hard-core 1/2 word")
        if not args.fixed_prefix:
            parser.error("fixed prefix must not be empty")
        fixed_prefix = tuple(map(int, args.fixed_prefix))
        if any(len(fixed_prefix) > cutoff for cutoff in args.cutoffs):
            parser.error("fixed prefix cannot be longer than a requested cutoff")

    results = []
    for offset, cutoff in enumerate(args.cutoffs):
        result = search(
            cutoff,
            args.population,
            args.generations,
            args.mutation_rate,
            args.seed + offset,
            initial_pattern=initial_pattern,
            fixed_prefix=fixed_prefix,
            tail=args.tail,
        )
        results.append(result)
        print(
            f"tail={args.tail} T={cutoff:3d} survival={result['survival']:3d}/"
            f"{result['horizon']:3d} evals={result['evaluations']:5d} "
            f"endpoint={result['endpoint_prefix']}"
        )
    if args.json is not None:
        args.json.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
        print(f"wrote {args.json}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact finite census for two binary-wedge horizon candidates.

For every packed source word, force a constant cut and measure the initial
continuation prefix contained in states {1,2}.  The preregistered sharp bound
``M_c(n) <= n`` is known to fail.  The sufficient repaired bound
``M_c(n) <= n+1`` remains open.  Finite success is evidence, not a proof.
"""

from __future__ import annotations

import argparse
import itertools
import random
from dataclasses import dataclass

from constant_tail_bitsliced_derivative import (
    bitsliced_trace_states,
    scenario_state,
)
from constant_tail_late_pull_horizon import pack_words
from constant_tail_scale import Vector
from late_pull_diagonal_sat import literal_extension


@dataclass(slots=True)
class Maximum:
    length: int = -1
    word: Vector = ()


def first_nonbinary(states, scenario: int) -> int:
    for index, state in enumerate(states):
        if scenario_state(state, scenario) not in (1, 2):
            return index
    return len(states)


def audit_batch(words: list[Vector], tail: int, maximum: Maximum) -> None:
    if not words:
        return
    n = len(words[0])
    packed, mask = pack_words(words)
    extension, _affines = bitsliced_trace_states(packed, n, tail, mask)
    for scenario, word in enumerate(words):
        horizon = first_nonbinary(extension, scenario)
        if horizon > maximum.length:
            maximum.length = horizon
            maximum.word = word


def literal_controls(max_length: int = 7) -> int:
    checked = 0
    for n in range(1, max_length + 1):
        words = list(itertools.product((1, 2), repeat=n))
        packed, mask = pack_words(words)
        for tail in (2, 3):
            extension, _affines = bitsliced_trace_states(
                packed, n, tail, mask
            )
            for scenario, word in enumerate(words):
                literal = literal_extension(word, tail, 2 * n)
                assert tuple(
                    scenario_state(state, scenario) for state in extension
                ) == literal
                expected = next(
                    (
                        index
                        for index, state in enumerate(literal)
                        if state not in (1, 2)
                    ),
                    len(literal),
                )
                assert first_nonbinary(extension, scenario) == expected
                checked += len(literal)
    return checked


def random_words(
    length: int, count: int, generator: random.Random
) -> list[Vector]:
    return [
        tuple(generator.choice((1, 2)) for _ in range(length))
        for _ in range(count)
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exact-first", type=int, default=11)
    parser.add_argument("--exact-last", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=20_000)
    parser.add_argument("--random-per-length", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=30043)
    args = parser.parse_args()
    if not 1 <= args.exact_first <= args.exact_last:
        parser.error("invalid exact range")
    if args.batch_size < 1 or args.random_per_length < 0:
        parser.error("invalid batch or random count")

    controls = literal_controls()
    print(f"literal/bit-sliced controls: {controls} cells PASS", flush=True)

    sharp_failures = 0
    sufficient_failures = 0
    for n in range(args.exact_first, args.exact_last + 1):
        maxima = {2: Maximum(), 3: Maximum()}
        iterator = itertools.product((1, 2), repeat=n)
        while True:
            batch = list(itertools.islice(iterator, args.batch_size))
            if not batch:
                break
            for tail in (2, 3):
                audit_batch(batch, tail, maxima[tail])
        fields = []
        for tail in (2, 3):
            maximum = maxima[tail]
            sharp_failures += int(n >= 7 and maximum.length > n)
            sufficient_failures += int(
                n >= 7 and maximum.length > n + 1
            )
            fields.append(
                f"c{tail}=M{maximum.length} "
                f"W={''.join(map(str, maximum.word))}"
            )
        print(f"exact n={n:3d} " + " | ".join(fields), flush=True)

    generator = random.Random(args.seed)
    for n in (24, 32, 48, 64, 96, 128):
        maxima = {2: Maximum(), 3: Maximum()}
        remaining = args.random_per_length
        while remaining:
            count = min(args.batch_size, remaining)
            batch = random_words(n, count, generator)
            for tail in (2, 3):
                audit_batch(batch, tail, maxima[tail])
            remaining -= count
        fields = []
        for tail in (2, 3):
            maximum = maxima[tail]
            sharp_failures += int(maximum.length > n)
            sufficient_failures += int(maximum.length > n + 1)
            fields.append(
                f"c{tail}=M{maximum.length} "
                f"W={''.join(map(str, maximum.word))}"
            )
        print(f"random n={n:3d} " + " | ".join(fields), flush=True)

    print(
        f"sharp-bound failures: {sharp_failures}; "
        f"sufficient-bound failures: {sufficient_failures}",
        flush=True,
    )
    if sufficient_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

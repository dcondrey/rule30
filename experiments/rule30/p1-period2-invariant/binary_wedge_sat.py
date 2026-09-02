#!/usr/bin/env python3
"""Exact SAT falsifier for the repaired binary-wedge horizon.

The formula is SAT iff a binary source of length ``n`` has at least ``n+2``
binary forced endpoint symbols while every newly exposed inverse-cut symbol
equals ``c``.  SAT gives a literal counterexample to BWH+; finite UNSAT is
not an all-length proof.
"""

from __future__ import annotations

import argparse
import itertools
import time
from dataclasses import dataclass
from typing import Iterable

from pysat.solvers import Solver

from late_pull_diagonal_sat import (
    append_edge,
    constrain_tail,
    literal_extension,
)
from mortality_sat import Encoder


BitPair = tuple[int, int]
Vector = tuple[int, ...]


@dataclass(slots=True)
class Instance:
    n: int
    tail: int
    encoder: Encoder
    source_high: tuple[int, ...]


def build_instance(n: int, tail: int) -> Instance:
    if n < 1 or tail not in (2, 3):
        raise ValueError("require n>=1 and tail in {2,3}")
    encoder = Encoder()
    source: list[BitPair] = []
    source_high = []
    for index in range(n):
        high = encoder.new(f"source.{index}.high")
        source.append((high, -high))
        source_high.append(high)

    edge: tuple[BitPair, ...] = ()
    endpoint: list[BitPair] = []
    zero = (encoder.zero, encoder.zero)
    for index, value in enumerate([zero] * n + source):
        edge = append_edge(
            encoder,
            edge,
            endpoint[-1] if endpoint else None,
            value,
            f"initial.{index}",
        )
        endpoint.append(value)

    for row in range(n + 2):
        high = encoder.new(f"extension.{row}.high")
        value = (high, -high)
        edge = append_edge(
            encoder, edge, endpoint[-1], value, f"extension.{row}"
        )
        constrain_tail(encoder, edge[-1], tail)
        endpoint.append(value)

    return Instance(n, tail, encoder, tuple(source_high))


def decode_source(instance: Instance, model: Iterable[int]) -> Vector:
    positive = {literal for literal in model if literal > 0}
    return tuple(
        2 if variable in positive else 1
        for variable in instance.source_high
    )


def direct_witness(word: Vector, tail: int) -> bool:
    extension = literal_extension(word, tail, len(word) + 2)
    return all(value in (1, 2) for value in extension)


def solve(n: int, tail: int) -> tuple[bool, Vector | None, float]:
    instance = build_instance(n, tail)
    started = time.perf_counter()
    with Solver(
        name="cadical195", bootstrap_with=instance.encoder.clauses
    ) as solver:
        sat = solver.solve()
        model = solver.get_model() if sat else None
    elapsed = time.perf_counter() - started
    if not sat:
        return False, None, elapsed
    assert model is not None
    word = decode_source(instance, model)
    assert direct_witness(word, tail)
    return True, word, elapsed


def controls(max_n: int = 7) -> int:
    checked = 0
    for n in range(1, max_n + 1):
        for tail in (2, 3):
            direct = any(
                direct_witness(word, tail)
                for word in itertools.product((1, 2), repeat=n)
            )
            sat, word, _elapsed = solve(n, tail)
            assert sat == direct
            if sat:
                assert word is not None and direct_witness(word, tail)
            checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first-n", type=int, default=7)
    parser.add_argument("--last-n", type=int, default=30)
    parser.add_argument("--control-n", type=int, default=7)
    args = parser.parse_args()
    if not 1 <= args.first_n <= args.last_n or args.control_n < 0:
        parser.error("invalid length range")

    print(f"SAT/direct controls: {controls(args.control_n)} PASS", flush=True)
    counterexamples = 0
    for n in range(args.first_n, args.last_n + 1):
        fields = []
        for tail in (2, 3):
            sat, word, elapsed = solve(n, tail)
            if sat:
                counterexamples += 1
                assert word is not None
                status = f"SAT W={''.join(map(str, word))}"
            else:
                status = "UNSAT"
            fields.append(f"c{tail}={status} t={elapsed:.3f}s")
        print(f"n={n:3d} " + " | ".join(fields), flush=True)
    if counterexamples:
        raise SystemExit(1)


if __name__ == "__main__":
    main()


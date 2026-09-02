#!/usr/bin/env python3
"""Diagnose which binary-source assumptions refute BWH+ at finite length.

Each source cell is initially four-state.  One assumption per position
restricts it to states {1,2}.  The script reports an inclusion-minimal UNSAT
assumption core.  Core positions and sizes are diagnostics, not theorems.
"""

from __future__ import annotations

import argparse
import time

from pysat.solvers import Solver

from late_pull_diagonal_sat import append_edge, constrain_tail
from mortality_sat import Encoder


BitPair = tuple[int, int]


def build_instance(n: int, tail: int) -> tuple[Encoder, tuple[int, ...]]:
    encoder = Encoder()
    source: list[BitPair] = []
    assumptions = []
    for index in range(n):
        high = encoder.new(f"source.{index}.high")
        low = encoder.new(f"source.{index}.low")
        binary = encoder.new(f"source.{index}.binary")
        encoder.add(-binary, high, low)
        encoder.add(-binary, -high, -low)
        source.append((high, low))
        assumptions.append(binary)

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
    return encoder, tuple(assumptions)


def minimize_core(solver: Solver, core: list[int]) -> list[int]:
    index = 0
    while index < len(core):
        trial = core[:index] + core[index + 1 :]
        if not solver.solve(assumptions=trial):
            core = trial
        else:
            index += 1
    return core


def audit(n: int, tail: int) -> str:
    encoder, assumptions = build_instance(n, tail)
    started = time.perf_counter()
    with Solver(
        name="cadical195", bootstrap_with=encoder.clauses
    ) as solver:
        assert solver.solve(), "four-state source control must be SAT"
        assert not solver.solve(assumptions=assumptions)
    with Solver(name="glucose4", bootstrap_with=encoder.clauses) as solver:
        assert not solver.solve(assumptions=assumptions)
        core = minimize_core(solver, list(solver.get_core() or ()))
        assert core and not solver.solve(assumptions=core)
        for index in range(len(core)):
            assert solver.solve(
                assumptions=core[:index] + core[index + 1 :]
            )
    positions = tuple(sorted(assumptions.index(value) for value in core))
    return f"c{tail}=core{positions} t={time.perf_counter()-started:.3f}s"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first-n", type=int, default=7)
    parser.add_argument("--last-n", type=int, default=13)
    args = parser.parse_args()
    if not 1 <= args.first_n <= args.last_n:
        parser.error("invalid length range")
    for n in range(args.first_n, args.last_n + 1):
        print(
            f"n={n:2d} "
            + " | ".join(audit(n, tail) for tail in (2, 3)),
            flush=True,
        )


if __name__ == "__main__":
    main()


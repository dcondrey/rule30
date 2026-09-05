#!/usr/bin/env python3
"""Audit hard-core assumption cores in the late-pull diagonal CNFs.

Finite UNSAT cores are diagnostics.  They do not prove the all-length DLP
family.
"""

from __future__ import annotations

import argparse
import time

from pysat.solvers import Solver

from late_pull_diagonal_sat import (
    build_instance,
    decode_extension,
    decode_source,
    literal_witness,
)


def hard_core_activations(instance):
    """Guard every continuation no-11 clause by a fresh assumption."""

    activations = []
    previous = instance.source_bits[-1][0]
    for position, current in enumerate(instance.endpoint_high):
        activation = instance.encoder.new(f"hard-core.{position}")
        instance.encoder.add(-activation, previous, current)
        activations.append(activation)
        previous = current
    return tuple(activations)


def minimize_core(solver: Solver, core: list[int]) -> list[int]:
    """Return an inclusion-minimal assumption core."""

    index = 0
    while index < len(core):
        trial = core[:index] + core[index + 1 :]
        if not solver.solve(assumptions=trial):
            core = trial
        else:
            index += 1
    return core


def audit_formula(n: int, tail: int, residue: int) -> str:
    instance = build_instance(
        n,
        tail,
        residue,
        hard_core_continuation=False,
    )
    activations = hard_core_activations(instance)
    started = time.perf_counter()

    # Most formulas are already contradictory without any no-11 clause.
    # Detect that case with CaDiCaL before asking Glucose for an assumption
    # core; this avoids deriving and then minimizing an irrelevant core of
    # the stronger formula.
    with Solver(
        name="cadical195", bootstrap_with=instance.encoder.clauses
    ) as base_solver:
        base_sat = base_solver.solve()
        base_model = base_solver.get_model() if base_sat else None
    if not base_sat:
        elapsed = time.perf_counter() - started
        return f"c{tail}r{residue}=base-UNSAT t{elapsed:.3f}"

    assert base_model is not None
    word = decode_source(instance, base_model)
    extension = decode_extension(instance, base_model)
    assert literal_witness(word, tail, residue, hard_core=False)
    combined = (word[-1],) + extension
    violations = tuple(
        position
        for position, (left, right) in enumerate(
            zip(combined, combined[1:])
        )
        if left == right == 1
    )
    assert violations

    # Glucose exposes stable assumption cores through PySAT.  CaDiCaL 1.9.5
    # solves these formulas but its Python core wrapper raises on an empty
    # core, which is precisely the common case in this audit.
    with Solver(
        name="glucose4", bootstrap_with=instance.encoder.clauses
    ) as solver:
        assert not solver.solve(assumptions=activations)
        core = minimize_core(solver, list(solver.get_core() or ()))
        positions = tuple(sorted(activations.index(value) for value in core))
        assert core
        assert solver.solve()
        assert not solver.solve(assumptions=core)
        for index in range(len(core)):
            assert solver.solve(
                assumptions=core[:index] + core[index + 1 :]
            )
        status = (
            f"core={positions} relaxed-W={''.join(map(str, word))} "
            f"violations={violations}"
        )

    elapsed = time.perf_counter() - started
    return f"c{tail}r{residue}={status} t{elapsed:.3f}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first-n", type=int, default=1)
    parser.add_argument("--last-n", type=int, default=20)
    args = parser.parse_args()
    if not 1 <= args.first_n <= args.last_n:
        parser.error("require 1 <= first-n <= last-n")

    for n in range(args.first_n, args.last_n + 1):
        fields = [
            audit_formula(n, tail, residue)
            for tail in (2, 3)
            for residue in (0, 1, 2)
        ]
        print(f"n={n:2d} " + " | ".join(fields), flush=True)


if __name__ == "__main__":
    main()

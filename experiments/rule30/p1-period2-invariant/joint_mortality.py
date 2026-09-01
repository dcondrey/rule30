#!/usr/bin/env python3
"""Exact joint left-finite/right-realizable alternating-fiber CNF.

``J(n,H)`` is SAT exactly when a genuine Rule 30 right half-plane supplies a
rho word of length ``n+H`` whose first ``n`` bits reconstruct a finite left
frontier and whose next ``H`` forced macros all emit the required deep zero
and pass the alternating center pin.

Finite UNSAT instances are falsification evidence only.  This module does not
turn a width sweep into an induction.
"""

from __future__ import annotations

import argparse
import time
from dataclasses import dataclass

from pysat.solvers import Solver

from carry_transducer import forced_macro, parity_or, seed_state
from mortality_sat import BitState, Encoder
from right_trace_forbidden import numeric_rho


@dataclass
class JointInstance:
    n: int
    horizon: int
    encoder: Encoder
    seed: list[int]
    trace: list[int]
    right_initial: list[int]


def equivalent(encoder: Encoder, left: int, right: int) -> None:
    encoder.add(-left, right)
    encoder.add(left, -right)


def right_trace(encoder: Encoder, length: int) -> tuple[list[int], list[int]]:
    """Encode the minimal genuine right light cone for ``length`` rho bits."""
    initial = [
        encoder.new(f"right.initial.{position}")
        for position in range(1, 2 * length)
    ]
    row = list(initial)
    trace: list[int] = []
    for time_index in range(2 * length - 1):
        if time_index % 2 == 0:
            trace.append(row[0])
        if len(row) == 1:
            break
        following = []
        for position in range(len(row) - 1):
            if position == 0:
                left = encoder.one if time_index % 2 else encoder.zero
            else:
                left = row[position - 1]
            joined = encoder.or_gate(
                row[position],
                row[position + 1],
                f"right.{time_index}.or.{position}",
            )
            following.append(
                encoder.xor_gate(
                    left,
                    joined,
                    f"right.{time_index + 1}.cell.{position}",
                )
            )
        row = following
    assert len(trace) == length
    return trace, initial


def build_joint_instance(n: int, horizon: int) -> JointInstance:
    if n < 1 or horizon < 0:
        raise ValueError("require n >= 1 and horizon >= 0")
    encoder = Encoder()
    seed = [encoder.new(f"seed.rho.{index}") for index in range(n)]

    state = BitState(0, (), ())
    for index, rho in enumerate(seed):
        state = encoder.wf_step(state, -rho, f"seed.{index}.zero")
        state = encoder.wf_step(state, encoder.one, f"seed.{index}.pin")

    trace = list(seed)
    for follow in range(horizon):
        feed = encoder.new(f"follow.{follow}.zero-feed")
        middle = encoder.wf_step(state, feed, f"follow.{follow}.zero")
        encoder.add(-middle.A[-1])
        state = encoder.wf_step(middle, encoder.one, f"follow.{follow}.pin")
        encoder.add(-state.A[-1])
        trace.append(-feed)

    actual, right_initial = right_trace(encoder, n + horizon)
    for forced, realized in zip(trace, actual):
        equivalent(encoder, forced, realized)
    return JointInstance(n, horizon, encoder, seed, trace, right_initial)


def solve_joint(
    instance: JointInstance,
) -> tuple[bool, list[int] | None, float]:
    started = time.perf_counter()
    with Solver(
        name="cadical195", bootstrap_with=instance.encoder.clauses
    ) as solver:
        satisfiable = solver.solve()
        model = solver.get_model() if satisfiable else None
    return satisfiable, model, time.perf_counter() - started


def decode(literals: list[int], model: list[int]) -> str:
    positive = {literal for literal in model if literal > 0}
    return "".join(
        "1"
        if (
            (literal > 0 and literal in positive)
            or (literal < 0 and -literal not in positive)
        )
        else "0"
        for literal in literals
    )


def replay(seed_word: str, continuation: str) -> None:
    seed = sum(int(bit) << index for index, bit in enumerate(seed_word))
    state = seed_state(seed, len(seed_word))
    observed = []
    for expected in continuation:
        observed.append(str(1 ^ parity_or(state)))
        following = forced_macro(state)
        if following is None:
            raise AssertionError("decoded joint model failed its pin replay")
        state = following
    if "".join(observed) != continuation:
        raise AssertionError("decoded joint model failed its rho replay")


def sweep(max_n: int, horizon: int) -> None:
    for n in range(1, max_n + 1):
        instance = build_joint_instance(n, horizon)
        satisfiable, model, seconds = solve_joint(instance)
        witness = ""
        if satisfiable:
            assert model is not None
            whole = decode(instance.trace, model)
            replay(whole[:n], whole[n:])
            right_word = decode(instance.right_initial, model)
            right_seed = sum(
                int(bit) << index for index, bit in enumerate(right_word)
            )
            if numeric_rho(right_seed, len(whole)) != whole:
                raise AssertionError("decoded right light cone failed replay")
            witness = f" rho={whole}"
        print(
            f"J({n},{horizon})={'SAT' if satisfiable else 'UNSAT'} "
            f"vars={instance.encoder.top} "
            f"clauses={len(instance.encoder.clauses)} "
            f"seconds={seconds:.3f}{witness}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=20)
    parser.add_argument("--horizon", type=int, default=8)
    args = parser.parse_args()
    sweep(args.max_n, args.horizon)


if __name__ == "__main__":
    main()

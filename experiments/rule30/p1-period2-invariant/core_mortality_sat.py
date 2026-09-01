#!/usr/bin/env python3
"""Exact local CNF for the stronger active-core diagonal conjecture.

``C(m,H)`` is SAT exactly when some aligned core word of length ``m`` ending
in terminal symbol 3 passes ``H`` pins and its forced rho sequence has no
adjacent ones.  Finite diagonal UNSAT instances are falsification evidence,
not an induction in ``m``.
"""

from __future__ import annotations

import argparse
import time
from dataclasses import dataclass
from itertools import product

from pysat.solvers import Solver

from mortality_sat import Encoder
from tail_density import core_step


@dataclass
class CoreInstance:
    length: int
    horizon: int
    encoder: Encoder
    initial: list[tuple[int, int]]


def build_core_instance(
    length: int, horizon: int, *, hard_core: bool = True
) -> CoreInstance:
    if length < 1 or horizon < 0:
        raise ValueError("require length >= 1 and horizon >= 0")
    encoder = Encoder()
    word = [
        (
            encoder.new(f"word.0.{index}.high"),
            encoder.new(f"word.0.{index}.low"),
        )
        for index in range(length)
    ]
    initial = list(word)
    encoder.add(word[-1][0])
    encoder.add(word[-1][1])

    previous_carry_high: int | None = None
    for time_index in range(horizon):
        carry_high = encoder.zero
        carry_low = encoder.zero
        output = []
        for position, (high, low) in enumerate(word):
            joined = encoder.or_gate(
                high, low, f"time.{time_index}.{position}.input-or"
            )
            high_next = encoder.xor_gate(
                carry_high,
                joined,
                f"time.{time_index}.{position}.carry-high",
            )
            joined = encoder.or_gate(
                carry_high,
                high,
                f"time.{time_index}.{position}.carry-or",
            )
            low_next = encoder.xor_gate(
                carry_low,
                joined,
                f"time.{time_index}.{position}.carry-low",
            )
            carry_high, carry_low = high_next, low_next
            output.append((low_next, high_next))

        # The pin passes exactly when the two terminal carry bits differ.
        encoder.add(carry_high, carry_low)
        encoder.add(-carry_high, -carry_low)

        # Forced rho is NOT carry_high.  Two consecutive rho ones are
        # therefore excluded by (previous_high OR current_high).
        if hard_core and previous_carry_high is not None:
            encoder.add(previous_carry_high, carry_high)
        previous_carry_high = carry_high
        word = output + [(encoder.one, encoder.one)]

    return CoreInstance(length, horizon, encoder, initial)


def solve_core(
    instance: CoreInstance,
) -> tuple[bool, list[int] | None, dict[str, int | float]]:
    started = time.perf_counter()
    with Solver(
        name="cadical195", bootstrap_with=instance.encoder.clauses
    ) as solver:
        satisfiable = solver.solve()
        model = solver.get_model() if satisfiable else None
        stats: dict[str, int | float] = dict(solver.accum_stats())
    stats["seconds"] = time.perf_counter() - started
    return satisfiable, model, stats


def decode_word(instance: CoreInstance, model: list[int]) -> tuple[int, ...]:
    positive = {literal for literal in model if literal > 0}
    return tuple(
        2 * int(high in positive) + int(low in positive)
        for high, low in instance.initial
    )


def direct_survival(word: tuple[int, ...], cap: int) -> tuple[int, str]:
    previous_rho: int | None = None
    for survived in range(cap):
        following, carry = core_step(word)
        if carry[0] == carry[1]:
            return survived, "pin"
        rho = 1 - carry[0]
        if previous_rho == rho == 1:
            return survived, "hard-core"
        previous_rho = rho
        word = following
    return cap, "cap"


def validate(max_length: int = 7) -> int:
    checked = 0
    for length in range(1, max_length + 1):
        words = [prefix + (3,) for prefix in product(range(4), repeat=length - 1)]
        maxima = [direct_survival(word, 64)[0] for word in words]
        maximum = max(maxima)
        for horizon in range(maximum + 2):
            instance = build_core_instance(length, horizon)
            satisfiable, model, _ = solve_core(instance)
            assert satisfiable == (horizon <= maximum)
            if satisfiable:
                assert model is not None
                word = decode_word(instance, model)
                assert word[-1] == 3
                assert direct_survival(word, max(64, horizon))[0] >= horizon
            checked += 1
    return checked


def no_hard_core_control() -> tuple[tuple[int, ...], int]:
    instance = build_core_instance(6, 7, hard_core=False)
    satisfiable, model, _ = solve_core(instance)
    assert satisfiable and model is not None
    word = decode_word(instance, model)

    previous_rho: int | None = None
    saw_adjacent_ones = False
    current = word
    for _ in range(7):
        current, carry = core_step(current)
        assert carry[0] != carry[1]
        rho = 1 - carry[0]
        saw_adjacent_ones |= previous_rho == rho == 1
        previous_rho = rho
    assert saw_adjacent_ones
    return word, 7


def diagonal_sweep(max_length: int) -> None:
    for length in range(1, max_length + 1):
        instance = build_core_instance(length, length + 1)
        satisfiable, model, stats = solve_core(instance)
        witness = ""
        if satisfiable:
            assert model is not None
            word = decode_word(instance, model)
            witness = " word=" + "".join(map(str, word))
        print(
            f"C({length},{length + 1})="
            f"{'SAT' if satisfiable else 'UNSAT'} "
            f"vars={instance.encoder.top} "
            f"clauses={len(instance.encoder.clauses)} "
            f"seconds={stats['seconds']:.3f}{witness}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-length", type=int, default=20)
    parser.add_argument("--max-validate", type=int, default=7)
    args = parser.parse_args()

    checks = validate(args.max_validate)
    print(f"core CNF/direct thresholds: {checks} PASS")
    word, horizon = no_hard_core_control()
    print(
        "dropped no-11 control: "
        f"C(6,{horizon})=SAT word={''.join(map(str, word))} PASS"
    )
    diagonal_sweep(args.max_length)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact ANF audit of the inverse-Gray pivot and dynamic Boolean ideals.

The script works in the Boolean ring on the rho seed variables.  With
``hard_core=True`` it also reduces modulo the monomial ideal

    <rho_i rho_(i+1) : i >= 0>,

which is exact on no-11 seeds.  It checks the symbolic frontier against the
canonical integer recurrence, prints post-knee emissions, and can trace the
survivor variety through ``2n+2`` macros.  The optional SAT check counts seed
projections of the independent Tseitin recurrence.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from bilateral_hardcore import forced_rho, hard_core, hard_core_survival
from carry_transducer import parity_or, seed_state, wf_step


# A Boolean ANF is a frozenset of square-free monomial masks.  Membership of a
# mask means coefficient one; mask zero is the constant monomial.
ANF = frozenset[int]
ZERO: ANF = frozenset()
ONE: ANF = frozenset({0})


def anf_xor(left: ANF, right: ANF) -> ANF:
    return left ^ right


def hard_core_monomial(mask: int) -> bool:
    return (mask & (mask >> 1)) == 0


def anf_product(left: ANF, right: ANF, *, hard_core_reduce: bool) -> ANF:
    answer: set[int] = set()
    for first in left:
        for second in right:
            monomial = first | second
            if hard_core_reduce and not hard_core_monomial(monomial):
                continue
            if monomial in answer:
                answer.remove(monomial)
            else:
                answer.add(monomial)
    return frozenset(answer)


def anf_or(left: ANF, right: ANF, *, hard_core_reduce: bool) -> ANF:
    return anf_xor(
        anf_xor(left, right),
        anf_product(left, right, hard_core_reduce=hard_core_reduce),
    )


def variable(index: int) -> ANF:
    return frozenset({1 << index})


def complement(value: ANF) -> ANF:
    return anf_xor(ONE, value)


def evaluate(value: ANF, assignment: int) -> int:
    answer = 0
    for monomial in value:
        answer ^= int((assignment & monomial) == monomial)
    return answer


def degree(value: ANF) -> int:
    return max((monomial.bit_count() for monomial in value), default=-1)


def format_anf(value: ANF) -> str:
    def format_monomial(monomial: int) -> str:
        if monomial == 0:
            return "1"
        return "".join(
            f"rho_{index + 1}"
            for index in range(monomial.bit_length())
            if (monomial >> index) & 1
        )

    if not value:
        return "0"
    ordered = sorted(value, key=lambda item: (item.bit_count(), item))
    return " + ".join(format_monomial(item) for item in ordered)


@dataclass(frozen=True)
class SymbolicState:
    T: int
    A: tuple[ANF, ...]
    B: tuple[ANF, ...]


def symbolic_wf_step(
    state: SymbolicState, value: ANF, *, hard_core_reduce: bool
) -> SymbolicState:
    """The exact shallow-to-deep recurrence from carry_transducer.wf_step."""
    assert state.T == len(state.A)
    assert len(state.B) == max(0, state.T - 1)
    current = value
    word = [current]
    for j in range(1, state.T + 1):
        if j == 1:
            b = ONE if ((state.T - 1) & 1) else ZERO
        else:
            b = state.B[j - 2]
        joined = anf_or(
            state.A[j - 1], b, hard_core_reduce=hard_core_reduce
        )
        current = anf_xor(current, joined)
        word.append(current)
    return SymbolicState(state.T + 1, tuple(word), state.A)


def symbolic_parity_or(
    state: SymbolicState, *, hard_core_reduce: bool
) -> ANF:
    """Return XOR_j (A_j OR B_(j-1)), including the phase bit B_0."""
    answer = ZERO
    for j in range(1, state.T + 1):
        if j == 1:
            b = ONE if ((state.T - 1) & 1) else ZERO
        else:
            b = state.B[j - 2]
        answer = anf_xor(
            answer,
            anf_or(state.A[j - 1], b, hard_core_reduce=hard_core_reduce),
        )
    return answer


def symbolic_seed_state(length: int, *, hard_core_reduce: bool) -> SymbolicState:
    state = SymbolicState(0, (), ())
    for index in range(length):
        state = symbolic_wf_step(
            state, complement(variable(index)), hard_core_reduce=hard_core_reduce
        )
        state = symbolic_wf_step(state, ONE, hard_core_reduce=hard_core_reduce)
    return state


@dataclass(frozen=True)
class MacroEmission:
    forced_rho: ANF
    zero_emission: ANF
    pin_emission: ANF
    hard_core_obstruction: ANF
    successor: SymbolicState


def symbolic_forced_macro(
    state: SymbolicState,
    previous_rho: ANF,
    *,
    hard_core_reduce: bool,
) -> MacroEmission:
    zero_feed = symbolic_parity_or(state, hard_core_reduce=hard_core_reduce)
    next_rho = complement(zero_feed)
    middle = symbolic_wf_step(
        state, zero_feed, hard_core_reduce=hard_core_reduce
    )
    # The deepest zero-phase output cancels identically by choice of feed.
    zero_emission = middle.A[-1]
    pin_emission = complement(
        symbolic_parity_or(middle, hard_core_reduce=hard_core_reduce)
    )
    successor = symbolic_wf_step(
        middle, ONE, hard_core_reduce=hard_core_reduce
    )
    assert zero_emission == ZERO
    assert successor.A[-1] == pin_emission
    obstruction = anf_product(
        previous_rho, next_rho, hard_core_reduce=hard_core_reduce
    )
    return MacroEmission(
        next_rho, zero_emission, pin_emission, obstruction, successor
    )


def state_value(state: SymbolicState, assignment: int) -> tuple[int, int, int]:
    A = sum(evaluate(bit, assignment) << index for index, bit in enumerate(state.A))
    B = sum(evaluate(bit, assignment) << index for index, bit in enumerate(state.B))
    return state.T, A, B


def gf2_rank(rows: list[int]) -> int:
    work = rows[:]
    rank = 0
    while work:
        pivot = max(work)
        if pivot == 0:
            break
        rank += 1
        bit = 1 << (pivot.bit_length() - 1)
        work = [row ^ pivot if row & bit else row for row in work if row != pivot]
    return rank


def inverse_gray_kernel(width: int) -> list[int]:
    return [
        sum((((min(i, j) + 1) & 1) << j) for j in range(width))
        for i in range(width)
    ]


def crosscheck(max_length: int, macros: int) -> int:
    checked = 0
    for length in range(1, max_length + 1):
        for seed in range(1 << length):
            if not hard_core(seed):
                continue
            symbolic = symbolic_seed_state(length, hard_core_reduce=True)
            numeric = seed_state(seed, length)
            assert state_value(symbolic, seed) == numeric
            previous_symbolic = variable(length - 1)
            previous_numeric = (seed >> (length - 1)) & 1
            for _ in range(macros):
                emission = symbolic_forced_macro(
                    symbolic,
                    previous_symbolic,
                    hard_core_reduce=True,
                )
                rho_numeric = forced_rho(numeric)
                assert evaluate(emission.forced_rho, seed) == rho_numeric
                assert evaluate(emission.zero_emission, seed) == 0
                middle_numeric = wf_step(numeric, parity_or(numeric))
                pin_emission_numeric = 1 ^ parity_or(middle_numeric)
                assert evaluate(emission.pin_emission, seed) == pin_emission_numeric
                assert evaluate(emission.hard_core_obstruction, seed) == (
                    previous_numeric & rho_numeric
                )
                numeric = wf_step(middle_numeric, 1)
                symbolic = emission.successor
                previous_numeric = rho_numeric
                previous_symbolic = emission.forced_rho
                checked += 1
    return checked


def print_initial_emissions(count: int) -> None:
    state = SymbolicState(0, (), ())
    print("one-row emissions, reduced on no-11 seeds:")
    for T in range(count):
        value = complement(variable(T // 2)) if T % 2 == 0 else ONE
        state = symbolic_wf_step(state, value, hard_core_reduce=True)
        output = state.A[-1]
        print(
            f"  T={T:2d} L_{T + 1} = {format_anf(output)} "
            f"(degree {degree(output)})"
        )


def initial_emission(row: int, *, hard_core_reduce: bool) -> ANF:
    state = SymbolicState(0, (), ())
    for T in range(row + 1):
        value = complement(variable(T // 2)) if T % 2 == 0 else ONE
        state = symbolic_wf_step(
            state, value, hard_core_reduce=hard_core_reduce
        )
    return state.A[-1]


def print_post_knee(length: int, macros: int) -> None:
    state = symbolic_seed_state(length, hard_core_reduce=True)
    previous = variable(length - 1)
    print(f"post-knee macro emissions for n={length}:")
    for offset in range(macros):
        emission = symbolic_forced_macro(
            state, previous, hard_core_reduce=True
        )
        print(f"  macro T=n+{offset}")
        print(f"    rho_(n+{offset + 1}) = {format_anf(emission.forced_rho)}")
        print(f"    zero emission   = {format_anf(emission.zero_emission)}")
        print(f"    pin emission    = {format_anf(emission.pin_emission)}")
        print(
            "    no-11 obstruction = "
            f"{format_anf(emission.hard_core_obstruction)}"
        )
        previous = emission.forced_rho
        state = emission.successor


def anf_payload(value: ANF) -> dict[str, Any]:
    ordered = sorted(value, key=lambda item: (item.bit_count(), item))
    return {
        "degree": degree(value),
        "term_count": len(value),
        "monomial_masks": ordered,
        "monomials_one_based": [
            [
                index + 1
                for index in range(monomial.bit_length())
                if (monomial >> index) & 1
            ]
            for monomial in ordered
        ],
        "formatted": format_anf(value),
    }


def hard_core_assignments(length: int) -> list[int]:
    return [seed for seed in range(1 << length) if hard_core(seed)]


def numeric_variety_counts(length: int, horizon: int) -> list[int]:
    """Independent counts from the canonical integer survivor recurrence."""
    deaths = [
        hard_core_survival(seed, length, horizon)[0]
        for seed in hard_core_assignments(length)
    ]
    return [sum(survival >= h for survival in deaths) for h in range(horizon + 1)]


def sat_projected_seed_count(
    length: int, horizon: int, solver_name: str
) -> int:
    """Count seed projections of the independent Tseitin recurrence CNF."""
    try:
        from mortality_sat import build_instance
        from pysat.solvers import Solver
    except ImportError as error:
        raise RuntimeError(
            "SAT cross-check requires the experiments/sygus-p3 environment"
        ) from error

    instance = build_instance(length, horizon)
    count = 0
    with Solver(name=solver_name, bootstrap_with=instance.clauses) as solver:
        while solver.solve():
            positive = {literal for literal in (solver.get_model() or []) if literal > 0}
            blocking_clause = [
                -variable if variable in positive else variable
                for variable in instance.seed_literals
            ]
            solver.add_clause(blocking_clause)
            count += 1
    return count


def trace_boolean_variety(
    length: int,
    horizon: int,
    *,
    emit_polynomials: bool,
) -> dict[str, Any]:
    """Trace V_h in the Boolean/hard-core quotient for h=0..horizon.

    V_h contains the initial hard-core seeds satisfying the first h pin and
    forced-rho hard-core generators.  In this finite Boolean function ring,
    the generated ideal is the unit ideal exactly when V_h is empty.
    """
    state = symbolic_seed_state(length, hard_core_reduce=True)
    previous = variable(length - 1)
    alive = hard_core_assignments(length)
    numeric_counts = numeric_variety_counts(length, horizon)
    assert len(alive) == numeric_counts[0]
    records: list[dict[str, Any]] = []

    for offset in range(horizon):
        emission = symbolic_forced_macro(
            state, previous, hard_core_reduce=True
        )
        alive = [
            seed
            for seed in alive
            if evaluate(emission.pin_emission, seed) == 0
            and evaluate(emission.hard_core_obstruction, seed) == 0
        ]
        count = len(alive)
        if count != numeric_counts[offset + 1]:
            raise AssertionError(
                f"variety mismatch n={length} h={offset + 1}: "
                f"ANF={count}, integer={numeric_counts[offset + 1]}"
            )
        record: dict[str, Any] = {
            "macro_offset": offset,
            "survival_horizon": offset + 1,
            "survivor_count": count,
            "unit_ideal": count == 0,
            "forced_rho": anf_payload(emission.forced_rho),
            "pin_emission": anf_payload(emission.pin_emission),
            "no_11_obstruction": anf_payload(emission.hard_core_obstruction),
        }
        records.append(record)
        if emit_polynomials:
            print(f"n={length} h={offset + 1}")
            print(f"  rho = {format_anf(emission.forced_rho)}")
            print(f"  epsilon = {format_anf(emission.pin_emission)}")
            print(
                "  no-11 = "
                f"{format_anf(emission.hard_core_obstruction)}"
            )
            print(f"  |V_h| = {count}")
        previous = emission.forced_rho
        state = emission.successor

    first_empty = next(
        (record["survival_horizon"] for record in records if record["unit_ideal"]),
        None,
    )
    return {
        "n": length,
        "requested_horizon": horizon,
        "initial_hard_core_count": numeric_counts[0],
        "variety_counts": [numeric_counts[0], *[r["survivor_count"] for r in records]],
        "first_unit_ideal_horizon": first_empty,
        "steps": records,
    }


def run_variety_sweep(
    first: int,
    last: int,
    *,
    emit_polynomials: bool,
    sat_crosscheck: bool,
    solver_name: str,
) -> dict[str, Any]:
    if first < 1 or last < first:
        raise ValueError("require 1 <= MIN_N <= MAX_N")
    traces = []
    for length in range(first, last + 1):
        horizon = 2 * length + 2
        trace = trace_boolean_variety(
            length, horizon, emit_polynomials=emit_polynomials
        )
        if sat_crosscheck:
            sat_counts = [
                sat_projected_seed_count(length, h, solver_name)
                for h in range(horizon + 1)
            ]
            if sat_counts != trace["variety_counts"]:
                raise AssertionError(
                    f"SAT count mismatch n={length}: "
                    f"SAT={sat_counts}, ANF={trace['variety_counts']}"
                )
            trace["sat_projected_counts"] = sat_counts
            trace["sat_crosscheck"] = True
        else:
            trace["sat_crosscheck"] = False
        traces.append(trace)
        counts = ",".join(map(str, trace["variety_counts"]))
        print(
            f"n={length:2d}: |V_0..V_{horizon}|={counts}; "
            f"1 in I at h={trace['first_unit_ideal_horizon']}"
        )
    return {
        "schema": "crosstalk.rule30.dynamic-boolean-ideal.v1",
        "conventions": {
            "V_h": "hard-core length-n seeds surviving at least h post-knee macros",
            "I_h": (
                "Boolean field equations, initial no-11 generators, and the first "
                "h pin/no-11 emission generators"
            ),
            "unit_ideal_equivalence": "1 in I_h iff |V_h|=0",
            "horizon": "2n+2",
        },
        "traces": traces,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-length", type=int, default=4)
    parser.add_argument("--post-macros", type=int, default=3)
    parser.add_argument("--initial-rows", type=int, default=8)
    parser.add_argument("--crosscheck-length", type=int, default=8)
    parser.add_argument(
        "--variety-sweep",
        nargs=2,
        type=int,
        metavar=("MIN_N", "MAX_N"),
        help="trace exact Boolean survivor varieties through horizon 2n+2",
    )
    parser.add_argument("--variety-json", type=Path)
    parser.add_argument(
        "--emit-polynomials",
        action="store_true",
        help="print every exact forced-rho, pin, and no-11 ANF in the sweep",
    )
    parser.add_argument(
        "--sat-crosscheck",
        action="store_true",
        help="independently count projected models of mortality_sat.py CNFs",
    )
    parser.add_argument("--solver", default="cadical195")
    args = parser.parse_args()

    for width in range(1, 17):
        kernel = inverse_gray_kernel(width)
        assert gf2_rank(kernel) == width
        diagonal = tuple((kernel[i] >> i) & 1 for i in range(width))
        assert diagonal == tuple((i + 1) & 1 for i in range(width))
    print("K=P^T P: full rank through width 16; diagonal is 1,0,1,0,... PASS")

    checks = crosscheck(args.crosscheck_length, args.post_macros)
    print(f"symbolic/integer hard-core frontier checks: {checks} PASS")
    unrestricted = initial_emission(15, hard_core_reduce=False)
    assert degree(unrestricted) == 8
    print(
        "unrestricted L_16 degree: "
        f"{degree(unrestricted)} ({len(unrestricted)} ANF terms) PASS"
    )
    print_initial_emissions(args.initial_rows)
    print_post_knee(args.seed_length, args.post_macros)
    if args.variety_sweep is not None:
        result = run_variety_sweep(
            *args.variety_sweep,
            emit_polynomials=args.emit_polynomials,
            sat_crosscheck=args.sat_crosscheck,
            solver_name=args.solver,
        )
        if args.variety_json is not None:
            args.variety_json.write_text(json.dumps(result, indent=2) + "\n")
            print(f"wrote {args.variety_json}")
    elif args.variety_json is not None:
        parser.error("--variety-json requires --variety-sweep")


if __name__ == "__main__":
    main()

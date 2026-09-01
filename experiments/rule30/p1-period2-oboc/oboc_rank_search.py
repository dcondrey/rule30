#!/usr/bin/env python3
"""Exact sampled kill test for ordered finite-control Rule 30 rankings.

This is a counterexample finder, not a finite-horizon proof.  For each fixed
observer topology it asks whether an energy of the form

    E(w) = sum_e u_e count_e(w) + beta(final_state(w)),  u_e >= 0,

can strictly decrease on every sampled surviving forced macro transition.
The nonnegative reduced edge weights make E bounded below on *all* finite
words.  The observer reads aligned frontier symbols deep-to-shallow, so the
edge counts retain order through its finite control.

If a nonnegative multiset of exact transitions has nonnegative aggregate edge
increments and zero aggregate terminal-state incidence, that multiset is an
exact Farkas obstruction to every such ranking for the topology.  Sampling is
used only to find this finite obstruction; the printed certificate is checked
with integer arithmetic.
"""

from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Callable

from z3 import Bool, Real, Solver, Sum, sat, unsat


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "p1-period2-invariant"
sys.path.insert(0, str(SOURCE))

from carry_transducer import (  # noqa: E402
    active_symbols,
    carry_step,
    compose,
    decode,
    encode,
    forced_macro,
    generated_monoid,
    gray_macro,
    input_transform,
    reachable_states,
)


State = tuple[int, int, int]
Transform = tuple[int, int, int, int]


@dataclass(frozen=True)
class Observer:
    name: str
    size: int
    start: int
    step: Callable[[int, int], int]


@dataclass(frozen=True)
class Witness:
    multiplicity: int
    seed_length: int
    seed: int
    follow: int
    before: State
    after: State


def observer_family() -> list[Observer]:
    transforms = sorted(generated_monoid())
    transform_id = {value: index for index, value in enumerate(transforms)}
    identity: Transform = (0, 1, 2, 3)

    def action_step(action: int, symbol: int) -> int:
        value = compose(input_transform(symbol), transforms[action])
        return transform_id[value]

    def carry_state_step(carry: int, symbol: int) -> int:
        nxt, _ = carry_step(decode(carry), symbol)
        return encode(nxt)

    def d8_parity_step(state: int, symbol: int) -> int:
        action, parity = divmod(state, 2)
        return 2 * action_step(action, symbol) + (parity ^ 1)

    def d8_carry_step(state: int, symbol: int) -> int:
        action, carry = divmod(state, 4)
        return 4 * action_step(action, symbol) + carry_state_step(carry, symbol)

    identity_id = transform_id[identity]
    return [
        Observer("carry4", 4, 0, carry_state_step),
        Observer("d8", 8, identity_id, action_step),
        Observer("d8-parity", 16, 2 * identity_id, d8_parity_step),
        Observer("d8-carry", 32, 4 * identity_id, d8_carry_step),
    ]


def ordered_word(state: State) -> tuple[int, ...]:
    """Return aligned symbols in the transducer's deep-to-shallow order."""
    return tuple(reversed(active_symbols(state)))


def features(observer: Observer, state: State) -> tuple[int, ...]:
    edge_count = [0] * (4 * observer.size)
    q = observer.start
    for symbol in ordered_word(state):
        edge_count[4 * q + symbol] += 1
        q = observer.step(q, symbol)
    terminal = [0] * observer.size
    terminal[q] = 1
    return tuple(edge_count + terminal)


def vector_delta(after: tuple[int, ...], before: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a - b for a, b in zip(after, before, strict=True))


def sampled_transitions(max_seed: int, max_follow: int) -> list[Witness]:
    origins = reachable_states(max_seed, max_follow)
    witnesses: list[Witness] = []
    for state, origin in sorted(origins.items(), key=lambda item: item[1]):
        pin, gray_next = gray_macro(state)
        exact_next = forced_macro(state)
        assert (pin == 1) == (exact_next is not None), (state, pin, exact_next)
        if exact_next is None:
            continue
        assert gray_next == exact_next, (state, gray_next, exact_next)
        length, seed, follow = origin
        witnesses.append(Witness(1, length, seed, follow, state, exact_next))
    return witnesses


def unique_deltas(
    observer: Observer, witnesses: list[Witness]
) -> tuple[list[tuple[int, ...]], list[Witness]]:
    representative: dict[tuple[int, ...], Witness] = {}
    for witness in witnesses:
        before = features(observer, witness.before)
        after = features(observer, witness.after)
        delta = vector_delta(after, before)
        representative.setdefault(delta, witness)
    return list(representative), list(representative.values())


def immediate_obstruction(
    observer: Observer,
    deltas: list[tuple[int, ...]],
    witnesses: list[Witness],
) -> list[Witness] | None:
    nedge = 4 * observer.size
    for delta, witness in zip(deltas, witnesses, strict=True):
        if all(value >= 0 for value in delta[:nedge]) and all(
            value == 0 for value in delta[nedge:]
        ):
            return [witness]
    return None


def as_fraction(value: object) -> Fraction:
    text = str(value)
    if text.endswith("?"):
        raise ValueError(f"inexact algebraic value: {text}")
    if "/" in text:
        numerator, denominator = text.split("/", 1)
        return Fraction(int(numerator), int(denominator))
    return Fraction(int(text), 1)


def farkas_obstruction(
    observer: Observer,
    deltas: list[tuple[int, ...]],
    witnesses: list[Witness],
    timeout_ms: int,
) -> list[Witness] | None:
    """Find an exact nonnegative rational combination and scale to integers."""
    nedge = 4 * observer.size
    variables = [Real(f"m_{i}") for i in range(len(deltas))]
    solver = Solver()
    solver.set(timeout=timeout_ms)
    solver.add(*(variable >= 0 for variable in variables))
    solver.add(Sum(variables) == 1)
    for coordinate in range(nedge):
        solver.add(
            Sum(
                variables[index] * delta[coordinate]
                for index, delta in enumerate(deltas)
            )
            >= 0
        )
    for coordinate in range(nedge, nedge + observer.size):
        solver.add(
            Sum(
                variables[index] * delta[coordinate]
                for index, delta in enumerate(deltas)
            )
            == 0
        )
    if solver.check() != sat:
        return None
    model = solver.model()
    values = [as_fraction(model.eval(variable, model_completion=True)) for variable in variables]
    scale = 1
    for value in values:
        scale = math.lcm(scale, value.denominator)
    multiplicities = [int(value * scale) for value in values]
    divisor = 0
    for value in multiplicities:
        divisor = math.gcd(divisor, value)
    multiplicities = [value // divisor for value in multiplicities]
    result = [
        Witness(
            multiplicity,
            witness.seed_length,
            witness.seed,
            witness.follow,
            witness.before,
            witness.after,
        )
        for multiplicity, witness in zip(multiplicities, witnesses, strict=True)
        if multiplicity
    ]
    verify_obstruction(observer, result)
    return result


def verify_obstruction(observer: Observer, obstruction: list[Witness]) -> None:
    nedge = 4 * observer.size
    aggregate = [0] * (nedge + observer.size)
    for witness in obstruction:
        before = features(observer, witness.before)
        after = features(observer, witness.after)
        delta = vector_delta(after, before)
        for coordinate, value in enumerate(delta):
            aggregate[coordinate] += witness.multiplicity * value
    assert all(value >= 0 for value in aggregate[:nedge]), aggregate[:nedge]
    assert all(value == 0 for value in aggregate[nedge:]), aggregate[nedge:]
    assert sum(witness.multiplicity for witness in obstruction) > 0


def search_rank_or_core(
    observer: Observer,
    deltas: list[tuple[int, ...]],
    timeout_ms: int,
) -> tuple[str, object]:
    """Find a sampled rank or a small exact infeasible subsystem."""
    nedge = 4 * observer.size
    edges = [Real(f"u_{i}") for i in range(nedge)]
    terminal = [Real(f"beta_{i}") for i in range(observer.size)]
    solver = Solver()
    solver.set(timeout=timeout_ms)
    solver.add(*(edge >= 0 for edge in edges))
    solver.add(terminal[observer.start] == 0)
    labels = []
    for index, delta in enumerate(deltas):
        label = Bool(f"descent_{index}")
        labels.append(label)
        solver.assert_and_track(
            Sum(
                [delta[index] * edges[index] for index in range(nedge)]
                + [
                    delta[nedge + index] * terminal[index]
                    for index in range(observer.size)
                ]
            ) <= -1,
            label,
        )
    result = solver.check()
    if result == sat:
        model = solver.model()
        return "sat", (
            [as_fraction(model.eval(edge, model_completion=True)) for edge in edges],
            [as_fraction(model.eval(value, model_completion=True)) for value in terminal],
        )
    if result == unsat:
        core_names = {str(value) for value in solver.unsat_core()}
        core = [index for index, label in enumerate(labels) if str(label) in core_names]
        return "unsat", core
    return "unknown", solver.reason_unknown()


def seed_bits(witness: Witness) -> str:
    return format(witness.seed, f"0{witness.seed_length}b")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-seed", type=int, default=12)
    parser.add_argument("--max-follow", type=int, default=64)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument(
        "--observer",
        choices=[observer.name for observer in observer_family()] + ["all"],
        default="all",
    )
    args = parser.parse_args()
    assert 1 <= args.max_seed <= 12
    assert 1 <= args.max_follow <= 64
    assert 1 <= args.timeout_seconds <= 600
    timeout_ms = 1000 * args.timeout_seconds

    transitions = sampled_transitions(args.max_seed, args.max_follow)
    print(
        f"exact surviving transitions: {len(transitions)} "
        f"(seed length <= {args.max_seed}, follow <= {args.max_follow})"
    )
    for observer in observer_family():
        if args.observer != "all" and observer.name != args.observer:
            continue
        deltas, representatives = unique_deltas(observer, transitions)
        print(
            f"{observer.name}: states={observer.size}, "
            f"unique feature deltas={len(deltas)}"
        )
        obstruction = immediate_obstruction(observer, deltas, representatives)
        if obstruction is not None:
            verify_obstruction(observer, obstruction)
            print(
                f"  KILLED: exact Farkas obstruction with "
                f"{len(obstruction)} transition types and total "
                f"multiplicity {sum(item.multiplicity for item in obstruction)}"
            )
            for item in obstruction:
                print(
                    f"    {item.multiplicity} * "
                    f"(length={item.seed_length}, seed={seed_bits(item)}, "
                    f"follow={item.follow})"
                )
            continue
        status, payload = search_rank_or_core(observer, deltas, timeout_ms)
        if status == "sat":
            rank = payload
            assert isinstance(rank, tuple)
            nonzero_edges = sum(value != 0 for value in rank[0])
            print(
                f"  SAMPLE FIT ONLY: bounded-below rank with "
                f"{nonzero_edges} nonzero reduced edge weights; "
                "requires exact all-word verification"
            )
            continue
        if status == "unknown":
            print(f"  INCONCLUSIVE: primal solver returned unknown ({payload})")
            continue
        core_indices = payload
        assert isinstance(core_indices, list)
        core_deltas = [deltas[index] for index in core_indices]
        core_witnesses = [representatives[index] for index in core_indices]
        print(f"  primal UNSAT; extracting dual from a {len(core_indices)}-row core")
        obstruction = farkas_obstruction(
            observer, core_deltas, core_witnesses, timeout_ms
        )
        if obstruction is None:
            print("  INCONCLUSIVE: exact dual extraction timed out or failed")
            continue
        verify_obstruction(observer, obstruction)
        print(
            f"  KILLED: exact Farkas obstruction with "
            f"{len(obstruction)} transition types and total "
            f"multiplicity {sum(item.multiplicity for item in obstruction)}"
        )
        for item in obstruction:
            print(
                f"    {item.multiplicity} * "
                f"(length={item.seed_length}, seed={seed_bits(item)}, "
                f"follow={item.follow})"
            )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Condition the constant-tail frontier graph on genuine right realizability.

For a hard-core endpoint over states ``{1,2}``, state 1 encodes rho bit 1 and
state 2 encodes rho bit 0.  This script retains only endpoints belonging to
the complete finite alternating-center Rule 30 right-cone language.  It then
measures source-to-terminal distances in the existing frontier graph and
tracks the exact D8 action accumulated on its newest fiber.

The terminal construction and graph transitions are uniform.  Every printed
horizon is finite evidence, not a proof of distance divergence.
"""

from __future__ import annotations

import argparse
from collections import deque
from functools import lru_cache
from itertools import product

from constant_tail_frontier_graph import (
    EXPECTED_FIBER_GROUP,
    FIBER_PERMUTATIONS,
    Vector,
    affine_coordinates,
    frontier_step,
    hard_core_words,
    shortest_queue,
    survives,
    terminal_frontiers,
)
from constant_tail_language_cocycle import SFT_TRANSITIONS
from constant_tail_right_filter import (
    PROVED_FORBIDDEN,
    right_trace_realizable,
)
from dyadic_periodicity_analyzer import IDENTITY, compose, inverse_cone_diagonal
from right_trace_forbidden import realized_language
from right_trace_forbidden import numeric_rho


Transform = tuple[int, int, int, int]


def endpoint_bits(endpoint: Vector) -> str:
    """Translate endpoint states 1/2 to the corresponding rho bits 1/0."""

    if any(state not in (1, 2) for state in endpoint):
        raise ValueError("an endpoint word must use only states 1 and 2")
    return "".join("1" if state == 1 else "0" for state in endpoint)


@lru_cache(maxsize=None)
def actual_bits(bits: str) -> bool:
    return right_trace_realizable(bits)


@lru_cache(maxsize=None)
def actual_right_endpoints(length: int) -> tuple[Vector, ...]:
    if length < 1:
        raise ValueError("endpoint length must be positive")
    return tuple(
        endpoint
        for endpoint in hard_core_words(length)
        if actual_bits(endpoint_bits(endpoint))
    )


def actual_terminal_frontiers(horizon: int) -> dict[Vector, Vector]:
    """Map complete-right-realizable endpoints to inverse-cone diagonals."""

    if horizon < 0:
        raise ValueError("horizon must be nonnegative")
    answer = {
        inverse_cone_diagonal(endpoint): endpoint
        for endpoint in actual_right_endpoints(horizon + 1)
    }
    assert len(answer) == len(actual_right_endpoints(horizon + 1))
    assert set(answer).issubset(terminal_frontiers(horizon))
    return answer


@lru_cache(maxsize=None)
def actual_right_seed(bits: str) -> int:
    """Extract a SAT witness and replay it with the independent bit kernel."""

    from joint_mortality import right_trace
    from mortality_sat import Encoder
    from pysat.solvers import Solver

    encoder = Encoder()
    trace, initial = right_trace(encoder, len(bits))
    for literal, bit in zip(trace, bits, strict=True):
        encoder.add(literal if bit == "1" else -literal)
    with Solver(
        name="cadical195", bootstrap_with=encoder.clauses
    ) as solver:
        if not solver.solve():
            raise AssertionError("reported actual-right endpoint is UNSAT")
        model = solver.get_model()
    assert model is not None
    positive = {literal for literal in model if literal > 0}
    seed = sum(
        int(literal in positive) << index
        for index, literal in enumerate(initial)
    )
    assert numeric_rho(seed, len(bits)) == bits
    return seed


def direct_language_control(max_length: int = 6) -> int:
    """Compare SAT membership with complete initial-row enumeration."""

    checked = 0
    for length in range(1, max_length + 1):
        direct = realized_language(length)
        by_sat = set()
        for word in map("".join, product("01", repeat=length)):
            if actual_bits(word):
                by_sat.add(word)
            checked += 1
        assert by_sat == direct
        assert all("11" not in word for word in direct)
        endpoint_language = {
            endpoint_bits(endpoint)
            for endpoint in actual_right_endpoints(length)
        }
        assert endpoint_language == direct
        assert all(
            pattern not in word
            for word in direct
            for pattern in PROVED_FORBIDDEN
        )
    return checked


def projection_control(max_horizon: int) -> tuple[int, list[tuple[int, bool]]]:
    """Audit inclusion and equality under deletion of the last coordinate."""

    checked = 0
    results = []
    low = set(actual_terminal_frontiers(0))
    for horizon in range(1, max_horizon + 1):
        high = set(actual_terminal_frontiers(horizon))
        projected = {frontier[:-1] for frontier in high}
        assert projected.issubset(low)
        results.append((horizon, projected == low))
        checked += len(high)
        low = high
    return checked, results


def shortest_actual_queue(
    tail: int, horizon: int
) -> tuple[Vector, Vector, int]:
    """Return a shortest queue reaching an actual-right terminal frontier."""

    targets = actual_terminal_frontiers(horizon)
    start = (tail,) * (horizon + 1)
    pending = deque((start,))
    parent: dict[Vector, tuple[Vector, int] | None] = {start: None}
    terminal: Vector | None = None

    while pending:
        state = pending.popleft()
        if state in targets:
            terminal = state
            break
        for symbol in range(3):
            following = frontier_step(state, symbol)
            if following not in parent:
                parent[following] = (state, symbol)
                pending.append(following)

    if terminal is None:
        raise AssertionError("no actual-right terminal frontier is reachable")
    suffix = []
    state = terminal
    while parent[state] is not None:
        previous, symbol = parent[state]
        suffix.append(symbol)
        state = previous
    queue = (tail,) + tuple(reversed(suffix))
    endpoint = targets[terminal]
    assert survives(queue, tail, horizon)
    assert actual_bits(endpoint_bits(endpoint))
    return queue, endpoint, len(parent)


def shortest_actual_invariant_queue(
    tail: int, horizon: int
) -> tuple[Vector, Vector, int]:
    """Shortest actual-target queue also avoiding 20, 22, and 011."""

    targets = actual_terminal_frontiers(horizon)
    start_frontier = (tail,) * (horizon + 1)
    start = (start_frontier, 3 if tail == 2 else 0)
    pending = deque((start,))
    parent: dict[
        tuple[Vector, int], tuple[tuple[Vector, int], int] | None
    ] = {start: None}
    terminal: tuple[Vector, int] | None = None

    while pending:
        state = pending.popleft()
        vertical, context = state
        if vertical in targets and context != 4:
            terminal = state
            break
        for symbol in range(3):
            following = (
                frontier_step(vertical, symbol),
                SFT_TRANSITIONS[context][symbol],
            )
            if following not in parent:
                parent[following] = (state, symbol)
                pending.append(following)

    if terminal is None:
        raise AssertionError("no invariant actual-right terminal is reachable")
    suffix = []
    state = terminal
    while parent[state] is not None:
        previous, symbol = parent[state]
        suffix.append(symbol)
        state = previous
    queue = (tail,) + tuple(reversed(suffix))
    endpoint = targets[terminal[0]]
    assert survives(queue, tail, horizon)
    return queue, endpoint, len(parent)


def update_action(
    frontier: Vector, following: Vector, action: Transform, tail: int
) -> Transform:
    """Advance the exact newest-fiber monodromy along one graph edge."""

    if len(frontier) < 2 or len(following) != len(frontier):
        raise ValueError("monodromy requires a frontier of height at least two")
    generator = FIBER_PERMUTATIONS[following[-2]]
    updated = compose(generator, action)
    assert following[-1] == updated[tail]
    return updated


def monodromy_minima(
    tail: int, horizon: int
) -> tuple[dict[Transform, int], dict[Transform, int], int, bool]:
    """Minimum queue lengths by D8 action for hard and actual terminals.

    The augmented graph is searched in breadth-first order.  Search stops
    after every group element has reached both target families, or after the
    complete finite augmented graph is exhausted.
    """

    hard = set(terminal_frontiers(horizon))
    actual = set(actual_terminal_frontiers(horizon))
    group = EXPECTED_FIBER_GROUP
    start_frontier = (tail,) * (horizon + 1)
    start = (start_frontier, IDENTITY)
    pending = deque((start,))
    distance = {start: 0}
    hard_minimum: dict[Transform, int] = {}
    actual_minimum: dict[Transform, int] = {}

    while pending:
        frontier, action = pending.popleft()
        depth = distance[(frontier, action)]
        # Queue length includes the fixed leading tail.
        if frontier in hard:
            hard_minimum.setdefault(action, depth + 1)
        if frontier in actual:
            actual_minimum.setdefault(action, depth + 1)
        if set(hard_minimum) == group and set(actual_minimum) == group:
            return hard_minimum, actual_minimum, len(distance), False

        for symbol in range(3):
            following = frontier_step(frontier, symbol)
            next_action = update_action(frontier, following, action, tail)
            state = (following, next_action)
            if state not in distance:
                distance[state] = depth + 1
                pending.append(state)

    return hard_minimum, actual_minimum, len(distance), True


def format_minima(minima: dict[Transform, int]) -> str:
    fields = []
    for action in sorted(EXPECTED_FIBER_GROUP, key=affine_coordinates):
        label = "".join(map(str, affine_coordinates(action)))
        fields.append(f"{label}:{minima.get(action, '-')}")
    return ",".join(fields)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-horizon", type=int, default=12)
    parser.add_argument("--monodromy-horizon", type=int, default=10)
    parser.add_argument("--direct-control-length", type=int, default=6)
    args = parser.parse_args()
    if not 1 <= args.max_horizon <= 12:
        parser.error("max horizon must lie between 1 and 12")
    if not 0 <= args.monodromy_horizon <= args.max_horizon:
        parser.error("monodromy horizon must lie between 0 and max horizon")
    if not 1 <= args.direct_control_length <= 6:
        parser.error("direct control length must lie between 1 and 6")

    direct = direct_language_control(args.direct_control_length)
    print(f"right-language SAT/direct controls: {direct} words PASS")
    projections, projection_rows = projection_control(args.max_horizon)
    if not all(equal for _horizon, equal in projection_rows):
        failed = [horizon for horizon, equal in projection_rows if not equal]
        raise AssertionError(f"actual terminal projection equality failed: {failed}")
    print(
        "actual-terminal height projections: "
        f"{projections} frontiers, equality through h={args.max_horizon} PASS"
    )

    for horizon in range(1, args.max_horizon + 1):
        hard_count = len(terminal_frontiers(horizon))
        actual_count = len(actual_terminal_frontiers(horizon))
        print(
            f"h={horizon:2d} terminals hard={hard_count:4d} "
            f"actual={actual_count:4d}"
        )
        for tail in (2, 3):
            hard_queue, _hard_endpoint, _hard_seen = shortest_queue(
                tail, horizon
            )
            queue, endpoint, discovered = shortest_actual_queue(tail, horizon)
            invariant, invariant_endpoint, invariant_seen = (
                shortest_actual_invariant_queue(tail, horizon)
            )
            assert len(hard_queue) <= len(queue) <= len(invariant)
            assert actual_bits(endpoint_bits(invariant_endpoint))
            right_seed = actual_right_seed(endpoint_bits(endpoint))
            fields = (
                f"  tail={tail} hard-min={len(hard_queue):2d} "
                f"actual-min={len(queue):2d} delta={len(queue)-len(hard_queue):2d} "
                f"actual-sft-min={len(invariant):2d} "
                f"seen={discovered:7d} "
                f"word={''.join(map(str, queue))} "
                f"endpoint={''.join(map(str, endpoint))} "
                f"rho={endpoint_bits(endpoint)} right-seed={right_seed:#x} "
                f"sft-seen={invariant_seen:7d} "
                f"sft-word={''.join(map(str, invariant))}"
            )
            if horizon <= args.monodromy_horizon:
                hard_phase, actual_phase, phase_seen, exhausted = (
                    monodromy_minima(tail, horizon)
                )
                fields += (
                    f" phase-seen={phase_seen} exhausted={exhausted}\n"
                    f"    hard-D8={format_minima(hard_phase)}\n"
                    f"    actual-D8={format_minima(actual_phase)}"
                )
            print(fields)


if __name__ == "__main__":
    main()

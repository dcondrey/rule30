#!/usr/bin/env python3
"""Solver-free graph audit of the proposed dyadic-period mismatch.

There are three different graphs in this question and they must not be
conflated:

* the raw four-carry input graph;
* the triangular cascade obtained by composing ``feed`` generators on the
  zero cut; and
* the second-order graph induced by the inverse terminal cone on a periodic
  hard-core endpoint.

The cascade has only dyadic eventual periods.  The other two statements
needed by the proposed mismatch do not hold: the raw graph has a three-cycle,
and the accepted cut ``1212...`` has minimal period two.
"""

from __future__ import annotations

import argparse
from collections import Counter
from collections.abc import Callable, Iterable, Sequence
from itertools import product
from math import isqrt


State = int
Transform = tuple[State, State, State, State]
Vector = tuple[State, ...]
ConeState = tuple[Vector, Vector]


def swap(state: State) -> State:
    """Swap the two bits of a carry code."""
    return 2 * (state & 1) + (state >> 1)


def carry_action(symbol: State, state: State) -> State:
    """The exact Rule 30 carry action, encoded as ``2*c' + d'``."""
    a, b = symbol >> 1, symbol & 1
    c, d = state >> 1, state & 1
    return 2 * (c ^ (a | b)) + (d ^ (c | a))


FORWARD: tuple[Transform, ...] = tuple(
    tuple(carry_action(symbol, state) for state in range(4))
    for symbol in range(4)
)


def invert(transform: Transform) -> Transform:
    inverse = [0] * 4
    for state, following in enumerate(transform):
        inverse[following] = state
    return tuple(inverse)  # type: ignore[return-value]


INVERSE: tuple[Transform, ...] = tuple(map(invert, FORWARD))
IDENTITY: Transform = (0, 1, 2, 3)


def compose(after: Transform, before: Transform) -> Transform:
    """Return ``after o before``."""
    return tuple(after[before[state]] for state in range(4))  # type: ignore[return-value]


def tarjan_scc(adjacency: dict[int, set[int]]) -> list[tuple[int, ...]]:
    """Return the SCCs of a small directed graph in canonical order."""
    index = 0
    indices: dict[int, int] = {}
    lowlink: dict[int, int] = {}
    stack: list[int] = []
    on_stack: set[int] = set()
    answer: list[tuple[int, ...]] = []

    def visit(node: int) -> None:
        nonlocal index
        indices[node] = lowlink[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)
        for following in sorted(adjacency[node]):
            if following not in indices:
                visit(following)
                lowlink[node] = min(lowlink[node], lowlink[following])
            elif following in on_stack:
                lowlink[node] = min(lowlink[node], indices[following])
        if lowlink[node] != indices[node]:
            return
        component = []
        while True:
            member = stack.pop()
            on_stack.remove(member)
            component.append(member)
            if member == node:
                break
        answer.append(tuple(sorted(component)))

    for node in sorted(adjacency):
        if node not in indices:
            visit(node)
    return sorted(answer)


def raw_graph() -> dict[int, set[int]]:
    return {
        state: {FORWARD[symbol][state] for symbol in range(4)}
        for state in range(4)
    }


def simple_cycle_lengths(adjacency: dict[int, set[int]]) -> set[int]:
    """Enumerate simple cycle lengths; sufficient here because |Q|=4."""
    lengths: set[int] = set()
    for start in sorted(adjacency):
        stack: list[tuple[int, tuple[int, ...]]] = [(start, (start,))]
        while stack:
            node, path = stack.pop()
            for following in adjacency[node]:
                if following == start:
                    lengths.add(len(path))
                elif following not in path and following >= start:
                    stack.append((following, path + (following,)))
    return lengths


def labelled_cycle_witness(target_length: int) -> tuple[tuple[int, int, int], ...]:
    """Find one raw carry cycle as triples (state, label, next state)."""
    for start in range(4):
        stack: list[tuple[int, tuple[int, ...], tuple[tuple[int, int, int], ...]]] = [
            (start, (start,), ())
        ]
        while stack:
            state, path, edges = stack.pop()
            if len(edges) == target_length:
                if state == start:
                    return edges
                continue
            for symbol in range(4):
                following = FORWARD[symbol][state]
                closes_at_target = (
                    following == start and len(edges) + 1 == target_length
                )
                extends_simple_path = following not in path
                if closes_at_target or extends_simple_path:
                    stack.append(
                        (
                            following,
                            path + (() if following == start else (following,)),
                            edges + ((state, symbol, following),),
                        )
                    )
    raise AssertionError(target_length)


def fiber_transform(incoming: State) -> Transform:
    """Update one cascade coordinate above an already-updated prefix.

    ``incoming`` is the preceding new cut coordinate.  Its bit swap is the
    carry entering the current ``feed`` symbol.
    """
    return tuple(
        swap(FORWARD[symbol][swap(incoming)]) for symbol in range(4)
    )  # type: ignore[return-value]


FIBER_GENERATORS: tuple[Transform, ...] = tuple(
    fiber_transform(incoming) for incoming in range(4)
)


def transformation_monoid(generators: Iterable[Transform]) -> set[Transform]:
    """Close a finite transformation set under composition."""
    found = {IDENTITY, *generators}
    changed = True
    while changed:
        changed = False
        current = tuple(found)
        for left, right in product(current, repeat=2):
            value = compose(left, right)
            if value not in found:
                found.add(value)
                changed = True
    return found


FIBER_MONOID = transformation_monoid(FIBER_GENERATORS)
EXPECTED_FIBER_MONOID: set[Transform] = {
    (0, 0, 0, 0),
    (0, 1, 1, 1),
    (0, 1, 2, 3),
    (0, 1, 3, 3),
    (1, 0, 0, 0),
    (1, 1, 1, 1),
    (1, 1, 3, 3),
    (2, 2, 2, 2),
    (2, 3, 1, 1),
    (2, 3, 3, 3),
    (3, 2, 2, 2),
    (3, 3, 1, 1),
    (3, 3, 3, 3),
}


def transformation_cycles(transform: Transform) -> tuple[tuple[int, ...], ...]:
    cycles: list[tuple[int, ...]] = []
    finished: set[int] = set()
    for root in range(4):
        if root in finished:
            continue
        path: list[int] = []
        position: dict[int, int] = {}
        state = root
        while state not in finished and state not in position:
            position[state] = len(path)
            path.append(state)
            state = transform[state]
        if state in position:
            cycles.append(tuple(path[position[state] :]))
        finished.update(path)
    return tuple(cycles)


def cascade_step(word: int, width: int) -> tuple[int, State]:
    """One spatial-layer step of a width-``width`` feed cascade."""
    carry = 0
    following = 0
    for position in range(width):
        symbol = (word >> (2 * position)) & 3
        carry = FORWARD[symbol][carry]
        following |= swap(carry) << (2 * position)
    return following, carry


def least_period(block: Sequence[object]) -> int:
    for period in range(1, len(block) + 1):
        if len(block) % period == 0 and all(
            block[index] == block[index % period]
            for index in range(len(block))
        ):
            return period
    raise AssertionError("nonempty finite block has no period")


def cascade_scc_summary(width: int) -> tuple[Counter[int], Counter[int], int]:
    """Exact functional-graph SCC summary for the triangular map T_width."""
    size = 1 << (2 * width)
    finished = bytearray(size)
    state_cycles: Counter[int] = Counter()
    output_cycles: Counter[int] = Counter()
    cyclic_vertices = 0
    for root in range(size):
        if finished[root]:
            continue
        path: list[int] = []
        position: dict[int, int] = {}
        state = root
        while not finished[state] and state not in position:
            position[state] = len(path)
            path.append(state)
            state = cascade_step(state, width)[0]
        if state in position:
            cycle = path[position[state] :]
            period = len(cycle)
            outputs = [cascade_step(member, width)[1] for member in cycle]
            state_cycles[period] += 1
            output_cycles[least_period(outputs)] += 1
            cyclic_vertices += period
        for member in path:
            finished[member] = 1
    # Every noncyclic vertex is a singleton SCC in a functional graph.
    return state_cycles, output_cycles, size - cyclic_vertices


def feed(states: Vector, symbol: State, start: int = 0) -> Vector:
    following = list(states)
    for layer in range(start, len(states)):
        following[layer] = FORWARD[symbol][states[layer]]
        symbol = swap(following[layer])
    return tuple(following)


def unfeed(states: Vector, symbol: State, start: int = 0) -> Vector:
    previous = list(states)
    for layer in range(start, len(states)):
        previous[layer] = INVERSE[symbol][states[layer]]
        symbol = swap(states[layer])
    return tuple(previous)


def terminal_cone(states: Vector) -> Vector:
    following = feed(states, 3)
    for layer in range(1, len(states)):
        following = feed(following, 3, layer)
    return following


def inverse_terminal_cone(states: Vector) -> Vector:
    previous = states
    for layer in range(len(states) - 1, 0, -1):
        previous = unfeed(previous, 3, layer)
    return unfeed(previous, 3)


BOUNDARY: Transform = INVERSE[3]


def cone_local(left: State, right: State) -> State:
    """Local rule phi(l,r)=tau_(swap(l))^-1(r)."""
    return INVERSE[swap(left)][right]


def inverse_cone_diagonal(endpoint: Vector) -> Vector:
    """Compute the inverse cone with the second-order diagonal recurrence."""
    length = len(endpoint)
    older = tuple(BOUNDARY[value] for value in endpoint)
    answer = [older[0]]
    if length == 1:
        return tuple(answer)
    newer = tuple(
        cone_local(endpoint[index], BOUNDARY[endpoint[index + 1]])
        for index in range(length - 1)
    )
    answer.append(newer[0])
    for time in range(2, length):
        current = tuple(
            cone_local(older[index + 1], newer[index + 1])
            for index in range(length - time)
        )
        answer.append(current[0])
        older, newer = newer, current
    return tuple(answer)


def cone_graph_step(state: ConeState) -> ConeState:
    """The exact finite graph G_p for an endpoint of spatial period p."""
    older, newer = state
    period = len(older)
    current = tuple(
        cone_local(older[(index + 1) % period], newer[(index + 1) % period])
        for index in range(period)
    )
    return newer, current


def periodic_cone_initial(endpoint: Vector) -> ConeState:
    period = len(endpoint)
    older = tuple(BOUNDARY[value] for value in endpoint)
    newer = tuple(
        cone_local(endpoint[index], BOUNDARY[endpoint[(index + 1) % period]])
        for index in range(period)
    )
    return older, newer


def orbit_period(
    initial: ConeState,
    output: Callable[[ConeState], object],
    cap: int | None = None,
) -> tuple[int, int, int, tuple[object, ...]]:
    """Return state preperiod, state period, minimal output period, block."""
    seen: dict[ConeState, int] = {}
    outputs: list[object] = []
    state = initial
    while state not in seen:
        if cap is not None and len(seen) >= cap:
            raise RuntimeError(f"orbit exceeded explicit cap {cap}")
        seen[state] = len(outputs)
        outputs.append(output(state))
        state = cone_graph_step(state)
    preperiod = seen[state]
    state_period = len(outputs) - preperiod
    state_block = outputs[preperiod:]
    output_period = least_period(state_block)
    return (
        preperiod,
        state_period,
        output_period,
        tuple(state_block[:output_period]),
    )


def hard_core_cycle(endpoint: Vector) -> bool:
    return all(value in (1, 2) for value in endpoint) and all(
        not (endpoint[index] == endpoint[(index + 1) % len(endpoint)] == 1)
        for index in range(len(endpoint))
    )


def primitive_cycle(endpoint: Vector) -> bool:
    return least_period(endpoint) == len(endpoint)


def canonical_rotation(endpoint: Vector) -> bool:
    return endpoint == min(
        endpoint[index:] + endpoint[:index] for index in range(len(endpoint))
    )


def hard_core_necklaces(period: int) -> Iterable[Vector]:
    for endpoint in product((1, 2), repeat=period):
        if (
            hard_core_cycle(endpoint)
            and primitive_cycle(endpoint)
            and canonical_rotation(endpoint)
        ):
            yield endpoint


def prime_factors(value: int) -> tuple[int, ...]:
    factors = []
    divisor = 2
    while divisor <= isqrt(value):
        if value % divisor:
            divisor += 1
            continue
        factors.append(divisor)
        while value % divisor == 0:
            value //= divisor
    if value > 1:
        factors.append(value)
    return tuple(factors)


def crosscheck(max_length: int = 7) -> int:
    """Exhaustively match both cone formulations on arbitrary endpoints."""
    checked = 0
    for length in range(1, max_length + 1):
        for endpoint in product(range(4), repeat=length):
            direct = inverse_terminal_cone(endpoint)
            diagonal = inverse_cone_diagonal(endpoint)
            assert direct == diagonal
            assert terminal_cone(direct) == endpoint
            checked += 1
    return checked


def audit(cascade_width: int, endpoint_period: int) -> None:
    assert all(set(action) == set(range(4)) for action in FORWARD)

    raw = raw_graph()
    raw_sccs = tarjan_scc(raw)
    raw_lengths = simple_cycle_lengths(raw)
    odd_witness = labelled_cycle_witness(3)
    assert raw_sccs == [(0, 1, 2, 3)]
    assert raw_lengths == {1, 2, 3, 4}
    assert odd_witness[0][0] == odd_witness[-1][2]
    print("raw carry graph")
    print(f"  FORWARD={FORWARD}")
    print(f"  SCCs={raw_sccs}; simple-cycle-lengths={sorted(raw_lengths)}")
    print(f"  odd-cycle-witness={odd_witness}")

    assert FIBER_MONOID == EXPECTED_FIBER_MONOID
    monoid_cycle_lengths = {
        len(cycle)
        for transform in FIBER_MONOID
        for cycle in transformation_cycles(transform)
    }
    assert monoid_cycle_lengths == {1, 2}
    print("triangular zero-ray cascade")
    print(f"  fiber-generators={FIBER_GENERATORS}")
    print(f"  fiber-monoid-size={len(FIBER_MONOID)}")
    print(f"  fiber-cycle-lengths={sorted(monoid_cycle_lengths)}")
    for transform in sorted(FIBER_MONOID):
        print(
            f"    transform={transform} cyclic-SCCs="
            f"{transformation_cycles(transform)}"
        )
    for width in range(cascade_width + 1):
        state_cycles, output_cycles, transient_sccs = cascade_scc_summary(width)
        assert all(period & (period - 1) == 0 for period in state_cycles)
        assert all(period & (period - 1) == 0 for period in output_cycles)
        print(
            f"  width={width}: state-cycles={dict(sorted(state_cycles.items()))} "
            f"output-cycles={dict(sorted(output_cycles.items()))} "
            f"transient-singleton-SCCs={transient_sccs}"
        )

    checks = crosscheck()
    print(f"inverse-terminal recurrence: {checks} arbitrary endpoints PASS")
    print("periodic hard-core endpoint census")
    dyadic_accepted: list[tuple[Vector, tuple[int, int, int, tuple[object, ...]]]] = []
    for period in range(1, endpoint_period + 1):
        histogram: Counter[int] = Counter()
        examples: dict[int, Vector] = {}
        preperiods: dict[int, int] = {}
        for endpoint in hard_core_necklaces(period):
            orbit = orbit_period(
                periodic_cone_initial(endpoint), lambda state: state[0][0]
            )
            preperiod, _, output_period, _ = orbit
            histogram[output_period] += 1
            examples.setdefault(output_period, endpoint)
            preperiods[output_period] = max(
                preperiods.get(output_period, 0), preperiod
            )
            if output_period & (output_period - 1) == 0:
                dyadic_accepted.append((endpoint, orbit))
        print(
            f"  endpoint-period={period}: output-periods="
            f"{dict(sorted(histogram.items()))} examples={examples} "
            f"prime-factors="
            f"{dict((value, prime_factors(value)) for value in sorted(histogram))} "
            f"max-preperiod-by-output={preperiods}"
        )

    endpoint = (2,)
    counterexample = orbit_period(
        periodic_cone_initial(endpoint), lambda state: state[0][0]
    )
    assert counterexample == (0, 2, 2, (1, 2))
    assert all(
        value == 2
        for value in terminal_cone(tuple(1 + index % 2 for index in range(64)))
    )
    assert dyadic_accepted and dyadic_accepted[0] == (endpoint, counterexample)
    family_checks = 0
    for length in range(1, 9):
        for prefix in product((1, 2), repeat=length):
            if any(left == right == 1 for left, right in zip(prefix, prefix[1:])):
                continue
            finite_endpoint = prefix + (2,) * (length + 16)
            accepted_cut = inverse_cone_diagonal(finite_endpoint)
            assert all(
                accepted_cut[index] == 1 + index % 2
                for index in range(2 * length, len(accepted_cut))
            )
            family_checks += 1
    print("mismatch verdict")
    print(
        "  COUNTEREXAMPLE: endpoint 2^omega has inverse-terminal cut "
        "(12)^omega, of minimal period 2."
    )
    print(
        "  Eventually-2 hard-core endpoints give infinitely many distinct "
        "accepted cuts eventually equal to (12)^omega; "
        f"{family_checks} finite-prefix controls PASS."
    )
    print(
        "  Therefore reachable-period and accepted-period spectra overlap; "
        "periodicity alone does not prove mortality."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cascade-width",
        type=int,
        default=8,
        help="largest exact triangular cascade SCC graph (default: 8)",
    )
    parser.add_argument(
        "--endpoint-period",
        type=int,
        default=10,
        help="largest primitive hard-core endpoint period (default: 10)",
    )
    args = parser.parse_args()
    if args.cascade_width < 0 or args.endpoint_period < 1:
        parser.error("bounds must be nonnegative/positive")
    return args


if __name__ == "__main__":
    arguments = parse_args()
    audit(arguments.cascade_width, arguments.endpoint_period)

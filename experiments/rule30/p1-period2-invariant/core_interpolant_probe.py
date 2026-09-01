#!/usr/bin/env python3
"""Exact projected-cut probes for active-core diagonal mortality.

The finite separator calculations in this file are conjecture/falsification
tools.  They are not an induction in the horizon.
"""

from __future__ import annotations

from collections.abc import Iterable
from itertools import combinations, product

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

from tail_density import core_step


def swap(state: int) -> int:
    return 2 * (state & 1) + (state >> 1)


def carry_action(symbol: int, state: int) -> int:
    a, b = symbol >> 1, symbol & 1
    c, d = state >> 1, state & 1
    return 2 * (c ^ (a | b)) + (d ^ (c | a))


FORWARD = tuple(
    tuple(carry_action(symbol, state) for state in range(4))
    for symbol in range(4)
)
INVERSE = []
for action in FORWARD:
    inverse = [0] * 4
    for state, following in enumerate(action):
        inverse[following] = state
    INVERSE.append(tuple(inverse))
INVERSE = tuple(INVERSE)


def feed(
    states: tuple[int, ...], symbol: int, start: int = 0
) -> tuple[int, ...]:
    """Feed a core symbol upward through a vertical carry cut."""
    following = list(states)
    for layer in range(start, len(following)):
        following[layer] = FORWARD[symbol][following[layer]]
        symbol = swap(following[layer])
    return tuple(following)


def unfeed(
    states: tuple[int, ...], symbol: int, start: int = 0
) -> tuple[int, ...]:
    """Invert ``feed`` for a prescribed input symbol."""
    previous = list(states)
    for layer in range(start, len(previous)):
        previous[layer] = INVERSE[symbol][states[layer]]
        symbol = swap(states[layer])
    return tuple(previous)


def terminal_cone(states: tuple[int, ...]) -> tuple[int, ...]:
    """Feed the terminal 3 and flush the triangular string of later 3s."""
    following = feed(states, 3)
    for layer in range(1, len(following)):
        following = feed(following, 3, layer)
    return following


def inverse_terminal_cone(states: tuple[int, ...]) -> tuple[int, ...]:
    previous = states
    for layer in range(len(previous) - 1, 0, -1):
        previous = unfeed(previous, 3, layer)
    return unfeed(previous, 3)


def hard_core_endpoints(horizon: int) -> Iterable[tuple[int, ...]]:
    for states in product((1, 2), repeat=horizon):
        if all(
            left != 1 or right != 1
            for left, right in zip(states, states[1:])
        ):
            yield states


def reachable_cut(horizon: int) -> set[tuple[int, ...]]:
    """Cuts reachable by a prefix of length at most ``horizon-2``."""
    reached = {(0,) * horizon}
    frontier = reached
    for _ in range(max(0, horizon - 2)):
        frontier = {
            feed(states, symbol)
            for states in frontier
            for symbol in range(4)
        }
        reached |= frontier
    return reached


def accepting_cut(horizon: int) -> set[tuple[int, ...]]:
    return {
        inverse_terminal_cone(states)
        for states in hard_core_endpoints(horizon)
    }


def direct_survives(word: tuple[int, ...], horizon: int) -> bool:
    previous_rho: int | None = None
    for _ in range(horizon):
        word, carry = core_step(word)
        state = 2 * carry[0] + carry[1]
        rho = 1 - carry[0]
        if state not in (1, 2) or previous_rho == rho == 1:
            return False
        previous_rho = rho
    return True


def cascade_crosscheck(max_length: int = 6) -> int:
    checked = 0
    for length in range(1, max_length + 1):
        horizon = length + 1
        reached = reachable_cut(horizon)
        accepting = accepting_cut(horizon)
        for prefix in product(range(4), repeat=length - 1):
            word = prefix + (3,)
            states = (0,) * horizon
            for symbol in prefix:
                states = feed(states, symbol)
            projected = states in accepting
            direct = direct_survives(word, horizon)
            assert projected == direct
            assert states in reached
            checked += 1
        assert not reached & accepting
    return checked


def bit_mask(states: tuple[int, ...]) -> int:
    return sum(
        (((state >> 1) & 1) << (2 * index))
        | ((state & 1) << (2 * index + 1))
        for index, state in enumerate(states)
    )


def monomials(variable_count: int, degree: int) -> list[int]:
    answer = [0]
    for size in range(1, degree + 1):
        answer.extend(
            sum(1 << variable for variable in support)
            for support in combinations(range(variable_count), size)
        )
    return answer


def add_row(
    basis: dict[int, tuple[int, int]], coefficients: int, right: int
) -> bool:
    while coefficients:
        pivot = coefficients.bit_length() - 1
        if pivot in basis:
            row, value = basis[pivot]
            coefficients ^= row
            right ^= value
        else:
            basis[pivot] = coefficients, right
            return True
    return right == 0


def separator_degree(
    reached: set[tuple[int, ...]],
    accepting: set[tuple[int, ...]],
    horizon: int,
    maximum: int = 4,
) -> int | None:
    labelled = [(states, 0) for states in reached]
    labelled.extend((states, 1) for states in accepting)
    for degree in range(maximum + 1):
        terms = monomials(2 * horizon, degree)
        index = {term: position for position, term in enumerate(terms)}
        basis: dict[int, tuple[int, int]] = {}
        consistent = True
        for states, label in labelled:
            assignment = bit_mask(states)
            ones = [
                variable
                for variable in range(2 * horizon)
                if assignment & (1 << variable)
            ]
            row = 1  # constant monomial
            for size in range(1, min(degree, len(ones)) + 1):
                for support in combinations(ones, size):
                    term = sum(1 << variable for variable in support)
                    row |= 1 << index[term]
            if not add_row(basis, row, label):
                consistent = False
                break
        if consistent:
            return degree
    return None


def evaluated_monomials(
    assignment: int,
    terms: list[int],
) -> int:
    return sum(
        1 << index
        for index, term in enumerate(terms)
        if assignment & term == term
    )


def local_ansatz_exists(
    radius: int,
    degree: int,
    cuts: dict[
        int,
        tuple[set[tuple[int, ...]], set[tuple[int, ...]]],
    ],
) -> bool:
    """Test a translated local ANF plus two boundary ANFs."""
    terms = monomials(2 * radius, degree)
    block = len(terms)
    basis: dict[int, tuple[int, int]] = {}
    for horizon, (reached, accepting) in cuts.items():
        if horizon < max(5, radius):
            continue
        labelled = [(states, 0) for states in reached]
        labelled.extend((states, 1) for states in accepting)
        for states, label in labelled:
            row = 0
            for position in range(horizon - radius + 1):
                assignment = bit_mask(states[position : position + radius])
                row ^= evaluated_monomials(assignment, terms)
            left = evaluated_monomials(bit_mask(states[:radius]), terms)
            right = evaluated_monomials(bit_mask(states[-radius:]), terms)
            row |= left << block
            row |= right << (2 * block)
            if not add_row(basis, row, label):
                return False
    return True


def minimum_clause(
    reached: list[int], target: int, variable_count: int, cap: int = 6
) -> tuple[int, tuple[int, ...]] | None:
    # A clause falsified by ``target`` and valid on every reached point is a
    # hitting set of the bit-difference supports ``reached XOR target``.
    difference_clauses = [
        [
            variable + 1
            for variable in range(variable_count)
            if difference & (1 << variable)
        ]
        for difference in (state ^ target for state in reached)
    ]
    for width in range(1, cap + 1):
        cardinality = CardEnc.atmost(
            lits=list(range(1, variable_count + 1)),
            bound=width,
            top_id=variable_count,
            encoding=EncType.seqcounter,
        )
        with Solver(
            name="cadical195",
            bootstrap_with=difference_clauses + cardinality.clauses,
        ) as solver:
            if not solver.solve():
                continue
            positive = {
                literal
                for literal in solver.get_model() or []
                if 0 < literal <= variable_count
            }
        support = tuple(literal - 1 for literal in sorted(positive))
        assert len(support) <= width
        assert all(
            any(
                (state ^ target) & (1 << variable)
                for variable in support
            )
            for state in reached
        )
        return width, support
    return None


def sweep(max_horizon: int = 12) -> None:
    print(f"cascade/direct diagonal controls: {cascade_crosscheck()} PASS")
    cuts = {
        horizon: (reachable_cut(horizon), accepting_cut(horizon))
        for horizon in range(3, max_horizon + 1)
    }
    for horizon in range(3, max_horizon + 1):
        reached, accepting = cuts[horizon]
        assert all(
            terminal_cone(inverse_terminal_cone(endpoint)) == endpoint
            for endpoint in hard_core_endpoints(horizon)
        )
        assert not reached & accepting
        degree = separator_degree(reached, accepting, horizon)
        clause_histogram: dict[int | None, int] = {}
        maximum_span = 0
        if horizon >= 5:
            reached_bits = list(map(bit_mask, reached))
            for target in map(bit_mask, accepting):
                result = minimum_clause(reached_bits, target, 2 * horizon)
                width = result[0] if result is not None else None
                clause_histogram[width] = clause_histogram.get(width, 0) + 1
                if result is not None:
                    support = result[1]
                    maximum_span = max(
                        maximum_span,
                        max(support) // 2 - min(support) // 2,
                    )
        print(
            f"H={horizon} R={len(reached)} S={len(accepting)} "
            f"minimum-ANF-degree={degree} "
            f"minimum-clause-widths={clause_histogram or '-'} "
            f"maximum-position-span={maximum_span}"
        )
    for radius in range(1, 7):
        exists = local_ansatz_exists(radius, 3, cuts)
        assert not exists
        print(
            "translated local degree<=3 separator: "
            f"radius={radius} INCONSISTENT"
        )


if __name__ == "__main__":
    sweep()

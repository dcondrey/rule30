#!/usr/bin/env python3
"""Exact finite audit of inverse lifts through the Peel operator.

For ``P(y)_t = phi(y_t, y_(t+1))``, right-permutivity of ``phi`` gives

    y_(t+1) = g_(P(y)_t)(y_t).

The four maps ``g_q`` generate a 13-element transformation monoid.  Every
cycle of every element has length one or two.  Consequently an ultimately
periodic Peel image of period ``p`` has only ultimately periodic lifts, with
eventual period dividing ``2*p``.  The exact doubling language also shows
that two consecutive strict period doublings are impossible.

Currying the same table in the other direction gives four permutations
``h_r(q)=g_q(r)``.  They are exactly the inverses of the local right actions
``u -> phi(r,u)`` and generate the familiar eight-element dihedral group.
Thus the nonpermutation lift monoid and the queue/affine ``D8`` action are
two orientations of one local table, not competing models.
"""

from __future__ import annotations

from collections import deque
from itertools import product

from dyadic_periodicity_analyzer import (
    BOUNDARY,
    IDENTITY,
    compose,
    cone_local,
    transformation_cycles,
)


Transform = tuple[int, int, int, int]
DoublingLanguageState = tuple[str, int]


def lift_transform(output: int) -> Transform:
    """Return ``g_output(l)``, the unique ``r`` with ``phi(l,r)=output``."""

    values = []
    for left in range(4):
        preimages = [
            right
            for right in range(4)
            if cone_local(left, right) == output
        ]
        assert len(preimages) == 1
        values.append(preimages[0])
    return tuple(values)  # type: ignore[return-value]


LIFT_GENERATORS: tuple[Transform, ...] = tuple(
    lift_transform(output) for output in range(4)
)


def right_generated_monoid(generators: tuple[Transform, ...]) -> set[Transform]:
    """Close under appending generators on the right of an output word."""

    found = {IDENTITY}
    frontier = [IDENTITY]
    while frontier:
        before = frontier.pop()
        for generator in generators:
            following = compose(generator, before)
            if following not in found:
                found.add(following)
                frontier.append(following)
    return found


LIFT_MONOID = right_generated_monoid(LIFT_GENERATORS)

EXPECTED_LIFT_MONOID: set[Transform] = {
    (0, 0, 0, 0),
    (0, 1, 2, 3),
    (0, 2, 2, 2),
    (0, 3, 2, 3),
    (1, 1, 1, 1),
    (1, 2, 3, 2),
    (1, 3, 3, 3),
    (2, 0, 0, 0),
    (2, 2, 2, 2),
    (2, 3, 2, 3),
    (3, 1, 1, 1),
    (3, 2, 3, 2),
    (3, 3, 3, 3),
}

EXPECTED_DOUBLING_TRANSFORMS: set[Transform] = {
    (1, 2, 3, 2),
    (2, 0, 0, 0),
    (3, 2, 3, 2),
}


def inverse_permutation(transform: Transform) -> Transform:
    """Invert a four-state permutation."""

    assert set(transform) == set(range(4))
    return tuple(transform.index(state) for state in range(4))  # type: ignore[return-value]


QUEUE_INPUT_ACTIONS: tuple[Transform, ...] = tuple(
    tuple(LIFT_GENERATORS[output][right] for output in range(4))
    for right in range(4)
)  # type: ignore[assignment]

LOCAL_RIGHT_ACTIONS: tuple[Transform, ...] = tuple(
    tuple(cone_local(left, right) for right in range(4))
    for left in range(4)
)  # type: ignore[assignment]


def has_two_cycle(transform: Transform) -> bool:
    """Return whether a block return map admits a period-doubling lift."""

    return any(
        len(cycle) == 2 for cycle in transformation_cycles(transform)
    )


def append_output(transform: Transform, output: int) -> Transform:
    """Append one Peel-output symbol to a block return transformation."""

    return compose(LIFT_GENERATORS[output], transform)


def doubling_language_step(
    state: DoublingLanguageState, output: int
) -> DoublingLanguageState:
    """Advance the claimed parity-pure language for doubling blocks.

    ``zero`` means that only zeroes have been read.  ``one`` and ``three``
    mean that the nonzero alphabet has been committed to ``{0,1}`` or
    ``{0,3}``; the second coordinate is the parity of that nonzero symbol.
    ``dead`` records a 2 or a mixture of 1 and 3.
    """

    mode, parity = state
    if mode == "dead":
        return state
    if output == 2:
        return ("dead", 0)
    if mode == "zero":
        if output == 0:
            return state
        if output == 1:
            return ("one", 1)
        assert output == 3
        return ("three", 1)
    if mode == "one":
        if output == 0:
            return state
        if output == 1:
            return ("one", parity ^ 1)
        return ("dead", 0)
    assert mode == "three"
    if output == 0:
        return state
    if output == 3:
        return ("three", parity ^ 1)
    return ("dead", 0)


def parity_pure_doubling_state(state: DoublingLanguageState) -> bool:
    """Accept ``{0,1}*``/odd-1 or ``{0,3}*``/odd-3 words."""

    mode, parity = state
    return mode in {"one", "three"} and parity == 1


def period_doubling_language_control() -> int:
    """Prove the all-word characterization by DFA product equivalence.

    The first automaton is the complete 13-element return-transformation
    monoid, accepting precisely transformations with a two-cycle.  The
    second recognizes the claimed parity-pure regular language.  Exhausting
    their finite synchronous product and finding no acceptance mismatch is
    an all-word proof, not a bounded word census.
    """

    start = (IDENTITY, ("zero", 0))
    frontier = deque([start])
    reachable = {start}
    while frontier:
        transform, language_state = frontier.popleft()
        assert has_two_cycle(transform) == parity_pure_doubling_state(
            language_state
        )
        if parity_pure_doubling_state(language_state):
            mode, _ = language_state
            two_cycles = {
                frozenset(cycle)
                for cycle in transformation_cycles(transform)
                if len(cycle) == 2
            }
            # A {0,1} odd-parity driver alternates lift states 2 and 3;
            # a {0,3} odd-parity driver alternates states 0 and 2.
            expected = (
                {frozenset((2, 3))}
                if mode == "one"
                else {frozenset((0, 2))}
            )
            assert two_cycles == expected
        for output in range(4):
            following = (
                append_output(transform, output),
                doubling_language_step(language_state, output),
            )
            if following not in reachable:
                reachable.add(following)
                frontier.append(following)
    return len(reachable)


def table_orientation_control() -> int:
    """Identify the queue-input orientation with the inverse local D8 action."""

    assert QUEUE_INPUT_ACTIONS == tuple(
        inverse_permutation(local) for local in LOCAL_RIGHT_ACTIONS
    )
    assert QUEUE_INPUT_ACTIONS == (
        (0, 1, 3, 2),
        (3, 2, 1, 0),
        (2, 3, 1, 0),
        (3, 2, 1, 0),
    )
    group = right_generated_monoid(QUEUE_INPUT_ACTIONS)
    assert len(group) == 8
    assert all(set(transform) == set(range(4)) for transform in group)
    assert {
        len(cycle)
        for transform in group
        for cycle in transformation_cycles(transform)
    } == {1, 2, 4}
    return len(group)


def isolated_doubling_control() -> None:
    """Check the local alphabet mechanism forbidding adjacent doublings."""

    # On the unique two-cycle for a {0,1} driver, 0 fixes both states and 1
    # swaps them.  Odd 1 parity therefore makes both 2 and 3 occur.
    assert tuple(LIFT_GENERATORS[0][state] for state in (2, 3)) == (2, 3)
    assert tuple(LIFT_GENERATORS[1][state] for state in (2, 3)) == (3, 2)

    # The {0,3} family behaves identically on its two-cycle {0,2}.
    assert tuple(LIFT_GENERATORS[0][state] for state in (0, 2)) == (0, 2)
    assert tuple(LIFT_GENERATORS[3][state] for state in (0, 2)) == (2, 0)

    # In either case the doubled lift contains state 2.  The all-word
    # language equivalence then rejects it as the driver of another strict
    # doubling on the immediately following lift.


def append_dependency_edge(
    edge: tuple[int, ...], previous: int | None, value: int
) -> tuple[int, ...]:
    """Append one endpoint symbol to its newest dependency diagonal."""

    following = [BOUNDARY[value]]
    if not edge:
        assert previous is None
        return tuple(following)
    assert previous is not None
    following.append(cone_local(previous, following[-1]))
    for order in range(2, len(edge) + 1):
        following.append(cone_local(edge[order - 2], following[-1]))
    return tuple(following)


def inverse_newest_holonomy(
    edge: tuple[int, ...], previous: int | None
) -> Transform:
    """Return the inverse newest-cut map as a reversed-queue D8 scan."""

    inverse_boundary = inverse_permutation(BOUNDARY)
    values = []
    for desired_cut in range(4):
        state = desired_cut
        if edge:
            assert previous is not None
            # The old final cut cell initializes the forced tail and is not
            # scanned.  Read every older diagonal cell from shallow to deep.
            for symbol in reversed(edge[:-1]):
                state = QUEUE_INPUT_ACTIONS[symbol][state]
            state = QUEUE_INPUT_ACTIONS[previous][state]
        else:
            assert previous is None
        values.append(inverse_boundary[state])
    return tuple(values)  # type: ignore[return-value]


def holonomy_controls(max_endpoint_length: int = 6) -> int:
    """Check the affine/newest permutation against its exact D8 holonomy."""

    checked = 0
    frontier = [((), (), None)]
    for length in range(max_endpoint_length + 1):
        following_frontier = []
        for endpoint, edge, previous in frontier:
            newest = tuple(
                append_dependency_edge(edge, previous, value)[-1]
                for value in range(4)
            )
            assert inverse_newest_holonomy(edge, previous) == inverse_permutation(
                newest  # type: ignore[arg-type]
            )
            checked += 1
            if length < max_endpoint_length:
                for value in range(4):
                    following_frontier.append(
                        (
                            endpoint + (value,),
                            append_dependency_edge(edge, previous, value),
                            value,
                        )
                    )
        frontier = following_frontier
    return checked


def lift(output: tuple[int, ...], initial: int) -> tuple[int, ...]:
    """Lift a finite Peel-output word after choosing its first input cell."""

    answer = [initial]
    for symbol in output:
        answer.append(LIFT_GENERATORS[symbol][answer[-1]])
    return tuple(answer)


def local_controls(max_output_length: int = 7) -> int:
    """Check the recurrence literally on every short output word."""

    checked = 0
    for length in range(max_output_length + 1):
        for output in product(range(4), repeat=length):
            for initial in range(4):
                values = lift(output, initial)
                assert tuple(
                    cone_local(values[index], values[index + 1])
                    for index in range(length)
                ) == output
                checked += 1
    return checked


def main() -> None:
    assert LIFT_GENERATORS == (
        (0, 3, 2, 3),
        (1, 2, 3, 2),
        (3, 1, 1, 1),
        (2, 0, 0, 0),
    )
    assert LIFT_MONOID == EXPECTED_LIFT_MONOID
    doubling_transforms = {
        transform for transform in LIFT_MONOID if has_two_cycle(transform)
    }
    assert doubling_transforms == EXPECTED_DOUBLING_TRANSFORMS
    cycle_lengths = {
        len(cycle)
        for transform in LIFT_MONOID
        for cycle in transformation_cycles(transform)
    }
    assert cycle_lengths == {1, 2}

    checked = local_controls()
    product_states = period_doubling_language_control()
    group_size = table_orientation_control()
    isolated_doubling_control()
    holonomies = holonomy_controls()
    print(f"Peel lift generators: {LIFT_GENERATORS}")
    print(f"13-element lift monoid: exact closure PASS")
    print(f"all monoid cycle lengths: {sorted(cycle_lengths)} PASS")
    print(
        "period-doubling blocks: parity-pure language equivalence "
        f"on {product_states} reachable product states PASS"
    )
    print(
        "strict period doublings are never consecutive: "
        "exact two-cycle alphabet check PASS"
    )
    print(
        "opposite table orientation: inverse local actions generate "
        f"D8 of size {group_size} PASS"
    )
    print(
        "newest affine inverse = reversed-queue D8 holonomy: "
        f"{holonomies} endpoint prefixes PASS"
    )
    print(f"literal local lifts checked: {checked} PASS")


if __name__ == "__main__":
    main()

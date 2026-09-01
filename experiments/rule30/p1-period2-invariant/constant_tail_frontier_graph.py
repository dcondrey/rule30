#!/usr/bin/env python3
"""Exact frontier-graph reduction of constant-tail queue mortality.

Stack ``h+1`` successive queue rows above a common input column.  If the
current vertical frontier is ``v`` and the next normalized bottom symbol is
``a``, the next frontier is

    w[0] = a,
    w[j] = g_(v[j])(w[j-1]).

For a hard-core endpoint word ``e`` of length ``h+1``, its inverse-cone
diagonal is exactly one legal terminal frontier.  Consequently the shortest
arbitrary normalized queue surviving ``h`` updates is one plus the directed
distance from the constant frontier to this Fibonacci-sized terminal set.
Taking the product with the ``20,22,011`` suffix DFA gives the corresponding
minimum inside the invariant queue language.

This is an exact all-h reduction.  The displayed distances are finite audits,
not a proof that the distances diverge.
"""

from __future__ import annotations

import argparse
from collections import deque
from itertools import product

from constant_tail_queue import normalize_queue, queue_step
from constant_tail_language_cocycle import SFT_TRANSITIONS
from dyadic_periodicity_analyzer import (
    IDENTITY,
    compose,
    cone_local,
    inverse_cone_diagonal,
    terminal_cone,
)
from peel_lift_monoid import LIFT_GENERATORS


Vector = tuple[int, ...]
Transform = tuple[int, int, int, int]


# If a height-H frontier is split as (base,z), the next last coordinate is a
# permutation K_t(z), where t is the last coordinate of the updated base.
FIBER_PERMUTATIONS: tuple[Transform, ...] = tuple(
    tuple(LIFT_GENERATORS[state][incoming] for state in range(4))
    for incoming in range(4)
)

EXPECTED_FIBER_GROUP: set[Transform] = {
    (0, 1, 2, 3),
    (0, 1, 3, 2),
    (1, 0, 2, 3),
    (1, 0, 3, 2),
    (2, 3, 0, 1),
    (2, 3, 1, 0),
    (3, 2, 0, 1),
    (3, 2, 1, 0),
}


def frontier_step(frontier: Vector, symbol: int) -> Vector:
    """Read one normalized queue symbol in the height-preserving graph."""

    following = [symbol]
    for previous_row_state in frontier[1:]:
        following.append(
            LIFT_GENERATORS[previous_row_state][following[-1]]
        )
    return tuple(following)


def peel(frontier: Vector) -> Vector:
    return tuple(
        cone_local(frontier[index], frontier[index + 1])
        for index in range(len(frontier) - 1)
    )


def frontier_peel_control(max_height: int = 6) -> int:
    """Check the uniform edge identity ``P(T_a(v))=shift(v)``."""

    checked = 0
    for height in range(1, max_height + 1):
        for frontier in product(range(4), repeat=height):
            for symbol in range(3):
                assert peel(frontier_step(frontier, symbol)) == frontier[1:]
                checked += 1
    return checked


def endpoint_delay_negative_control(max_length: int = 8) -> int:
    """Check the uniform counterfamily to first-defect Lipschitz control.

    For hard-core ``e`` beginning in state 1, let ``y=I(e)`` and
    ``v=0.P(y)``.  Then ``T_2(v)=y``.  The endpoint of ``v`` is illegal at
    coordinate zero, whereas the endpoint of ``y`` is the arbitrary word
    ``e``.
    """

    checked = 0
    for length in range(1, max_length + 1):
        for endpoint in hard_core_words(length):
            if endpoint[0] != 1:
                continue
            target = inverse_cone_diagonal(endpoint)
            predecessor = (0,) + peel(target)
            assert frontier_step(predecessor, 2) == target
            assert terminal_cone(predecessor)[0] == 3
            assert terminal_cone(target) == endpoint
            checked += 1
    return checked


def projection_control(max_height: int = 6) -> int:
    """Check that edge and terminal graphs commute with height projection."""

    checked = 0
    for height in range(2, max_height + 1):
        for frontier in product(range(4), repeat=height):
            for symbol in range(3):
                assert frontier_step(frontier, symbol)[:-1] == frontier_step(
                    frontier[:-1], symbol
                )
                checked += 1
        high = set(terminal_frontiers(height - 1))
        low = set(terminal_frontiers(height - 2))
        assert {frontier[:-1] for frontier in high} == low
    return checked


def transformation_group(generators: tuple[Transform, ...]) -> set[Transform]:
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


def affine_coordinates(permutation: Transform) -> tuple[int, int, int]:
    """Encode ``(h,l)->(h+a,l+b*h+g)`` over F2."""

    alpha = permutation[0] >> 1
    gamma = permutation[0] & 1
    beta = (permutation[2] & 1) ^ gamma
    rebuilt = tuple(
        2 * ((state >> 1) ^ alpha)
        + ((state & 1) ^ (beta & (state >> 1)) ^ gamma)
        for state in range(4)
    )
    assert rebuilt == permutation
    return alpha, beta, gamma


def path_monodromy(tail: int, word: Vector, height: int) -> Transform:
    """Return the D8 action on the last fiber along the projected path."""

    if height < 2:
        raise ValueError("a fiber monodromy requires height at least two")
    projected = (tail,) * (height - 1)
    action = IDENTITY
    for symbol in word:
        projected = frontier_step(projected, symbol)
        action = compose(FIBER_PERMUTATIONS[projected[-1]], action)
    return action


def vertical_driver_step(driver: Vector, tail: int) -> Vector:
    """Advance all horizontal path states by one frontier coordinate."""

    following = []
    previous = tail
    for state in driver:
        previous = LIFT_GENERATORS[previous][state]
        following.append(previous)
    return tuple(following)


def vertical_driver_control(
    max_height: int = 6, max_word_length: int = 4
) -> int:
    """Match the fixed-word 4^d-state driver to literal frontier columns."""

    checked = 0
    for tail in (2, 3):
        for length in range(1, max_word_length + 1):
            for word in product(range(3), repeat=length):
                literal = (tail,) * max_height
                for symbol in word:
                    literal = frontier_step(literal, symbol)
                driver = word
                outputs = [driver[-1]]
                for _ in range(1, max_height):
                    driver = vertical_driver_step(driver, tail)
                    outputs.append(driver[-1])
                assert tuple(outputs) == literal
                checked += 1
    return checked


def monodromy_control(max_height: int = 5, max_word_length: int = 4) -> int:
    """Compare the three-bit path cocycle with literal full frontiers."""

    assert tuple(map(affine_coordinates, FIBER_PERMUTATIONS)) == (
        (0, 1, 0),
        (1, 0, 1),
        (1, 1, 0),
        (1, 0, 1),
    )
    checked = 0
    for height in range(2, max_height + 1):
        for tail in (2, 3):
            for length in range(max_word_length + 1):
                for word in product(range(3), repeat=length):
                    full = (tail,) * height
                    for symbol in word:
                        full = frontier_step(full, symbol)
                    action = path_monodromy(tail, word, height)
                    assert full[-1] == action[tail]
                    checked += 1
    return checked


def fiber_cover_control(max_height: int = 6) -> int:
    """Check the uniform four-sheeted D8 permutation-cover identity."""

    assert FIBER_PERMUTATIONS == (
        (0, 1, 3, 2),
        (3, 2, 1, 0),
        (2, 3, 1, 0),
        (3, 2, 1, 0),
    )
    assert transformation_group(FIBER_PERMUTATIONS) == EXPECTED_FIBER_GROUP
    checked = 0
    for height in range(2, max_height + 1):
        for vertical in product(range(4), repeat=height):
            base, fiber = vertical[:-1], vertical[-1]
            for symbol in range(3):
                following = frontier_step(vertical, symbol)
                base_following = frontier_step(base, symbol)
                assert following[:-1] == base_following
                assert following[-1] == FIBER_PERMUTATIONS[
                    base_following[-1]
                ][fiber]
                checked += 1
    return checked


def hard_core_words(length: int):
    """Generate the words over {1,2} with no adjacent pair 11."""

    for word in product((1, 2), repeat=length):
        if all(word[index : index + 2] != (1, 1) for index in range(length - 1)):
            yield word


def terminal_frontiers(horizon: int) -> dict[Vector, Vector]:
    """Map every legal inverse-cone diagonal to its hard-core endpoint."""

    answer = {
        inverse_cone_diagonal(endpoint): endpoint
        for endpoint in hard_core_words(horizon + 1)
    }
    # The right boundary decoder reconstructs the endpoint, so the diagonal
    # map is injective on this language.
    assert len(answer) == fibonacci(horizon + 3)
    return answer


def shortest_queue(tail: int, horizon: int) -> tuple[Vector, Vector, int]:
    """Return a shortest queue, its endpoint target, and vertices discovered."""

    targets = terminal_frontiers(horizon)
    start = (tail,) * (horizon + 1)
    frontier = deque((start,))
    parent: dict[Vector, tuple[Vector, int] | None] = {start: None}
    terminal: Vector | None = None

    while frontier:
        state = frontier.popleft()
        if state in targets:
            terminal = state
            break
        for symbol in range(3):
            following = frontier_step(state, symbol)
            if following not in parent:
                parent[following] = (state, symbol)
                frontier.append(following)

    if terminal is None:
        raise AssertionError("finite graph has no reachable terminal frontier")
    suffix = []
    state = terminal
    while parent[state] is not None:
        previous, symbol = parent[state]
        suffix.append(symbol)
        state = previous
    queue = (tail,) + tuple(reversed(suffix))
    return queue, targets[terminal], len(parent)


def shortest_invariant_queue(
    tail: int, horizon: int
) -> tuple[Vector, Vector, int]:
    """Shortest queue whose full word also avoids 20, 22, and 011."""

    targets = terminal_frontiers(horizon)
    start_frontier = (tail,) * (horizon + 1)
    start = (start_frontier, 3 if tail == 2 else 0)
    frontier = deque((start,))
    parent: dict[
        tuple[Vector, int], tuple[tuple[Vector, int], int] | None
    ] = {start: None}
    terminal: tuple[Vector, int] | None = None

    while frontier:
        state = frontier.popleft()
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
                frontier.append(following)

    if terminal is None:
        raise AssertionError("no invariant terminal frontier is reachable")
    suffix = []
    state = terminal
    while parent[state] is not None:
        previous, symbol = parent[state]
        suffix.append(symbol)
        state = previous
    queue = (tail,) + tuple(reversed(suffix))
    return queue, targets[terminal[0]], len(parent)


def survives(queue: Vector, tail: int, horizon: int) -> bool:
    """Check a graph witness against the literal growing queue cocycle."""

    for _ in range(horizon):
        step = queue_step(queue, tail)
        if step is None:
            return False
        queue = normalize_queue(step.queue, tail)
    return True


def frontier_language_control(
    max_horizon: int = 5, max_suffix_length: int = 6
) -> int:
    """Compare graph acceptance with every short literal normalized queue."""

    checked = 0
    for horizon in range(1, max_horizon + 1):
        targets = terminal_frontiers(horizon)
        for tail in (2, 3):
            start = (tail,) * (horizon + 1)
            for length in range(max_suffix_length + 1):
                for suffix in product(range(3), repeat=length):
                    state = start
                    for symbol in suffix:
                        state = frontier_step(state, symbol)
                    queue = (tail,) + suffix
                    assert (state in targets) == survives(queue, tail, horizon)
                    checked += 1
    return checked


def fibonacci(index: int) -> int:
    left, right = 0, 1
    for _ in range(index):
        left, right = right, left + right
    return left


EXPECTED_ARBITRARY_MINIMUM = {
    2: (1, 1, 3, 5, 5, 5, 10, 10, 10, 10, 16, 16, 18),
    3: (1, 2, 3, 5, 5, 5, 10, 10, 10, 12, 12, 15, 16),
}

EXPECTED_INVARIANT_MINIMUM = {
    2: (1, 1, 3, 5, 5, 5, 10, 10, 10, 10, 17, 18, 18, 18),
    3: (2, 2, 3, 5, 5, 5, 10, 10, 10, 13, 14, 15, 16, 16),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-horizon", type=int, default=12)
    args = parser.parse_args()
    if not 1 <= args.max_horizon <= 18:
        parser.error("max horizon must lie between 1 and 18")

    identities = frontier_peel_control()
    print(f"frontier/Peel edge identity: {identities} finite controls PASS")
    delay_checks = endpoint_delay_negative_control()
    print(
        "one-lift endpoint-delay counterfamily: "
        f"{delay_checks} finite controls PASS"
    )
    projections = projection_control()
    print(f"frontier height projections: {projections} finite controls PASS")
    covers = fiber_cover_control()
    print(
        "four-sheeted D8 fiber cover: "
        f"{covers} finite controls, group-size=8 PASS"
    )
    monodromies = monodromy_control()
    print(
        "three-bit affine path monodromy: "
        f"{monodromies} finite controls PASS"
    )
    drivers = vertical_driver_control()
    print(f"fixed-word vertical drivers: {drivers} finite controls PASS")
    languages = frontier_language_control()
    print(f"frontier/queue language identity: {languages} finite controls PASS")

    for horizon in range(1, args.max_horizon + 1):
        terminals = terminal_frontiers(horizon)
        for tail in (2, 3):
            queue, endpoint, discovered = shortest_queue(tail, horizon)
            invariant, invariant_endpoint, invariant_discovered = (
                shortest_invariant_queue(tail, horizon)
            )
            assert survives(queue, tail, horizon)
            assert survives(invariant, tail, horizon)
            expected = EXPECTED_ARBITRARY_MINIMUM[tail]
            if horizon < len(expected):
                assert len(queue) == expected[horizon]
            invariant_expected = EXPECTED_INVARIANT_MINIMUM[tail]
            if horizon < len(invariant_expected):
                assert len(invariant) == invariant_expected[horizon]
            print(
                f"h={horizon:2d} tail={tail} "
                f"any-min={len(queue):2d} any-seen={discovered:7d} "
                f"sft-min={len(invariant):2d} sft-seen={invariant_discovered:7d} "
                f"terminal={len(terminals):3d} "
                f"any-w={''.join(map(str, queue))} "
                f"any-e={''.join(map(str, endpoint))} "
                f"sft-w={''.join(map(str, invariant))} "
                f"sft-e={''.join(map(str, invariant_endpoint))}"
            )


if __name__ == "__main__":
    main()

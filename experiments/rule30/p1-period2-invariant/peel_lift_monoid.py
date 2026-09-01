#!/usr/bin/env python3
"""Exact finite audit of inverse lifts through the Peel operator.

For ``P(y)_t = phi(y_t, y_(t+1))``, right-permutivity of ``phi`` gives

    y_(t+1) = g_(P(y)_t)(y_t).

The four maps ``g_q`` generate a 13-element transformation monoid.  Every
cycle of every element has length one or two.  Consequently an ultimately
periodic Peel image of period ``p`` has only ultimately periodic lifts, with
eventual period dividing ``2*p``.
"""

from __future__ import annotations

from itertools import product

from dyadic_periodicity_analyzer import (
    IDENTITY,
    compose,
    cone_local,
    transformation_cycles,
)


Transform = tuple[int, int, int, int]


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
    cycle_lengths = {
        len(cycle)
        for transform in LIFT_MONOID
        for cycle in transformation_cycles(transform)
    }
    assert cycle_lengths == {1, 2}

    checked = local_controls()
    print(f"Peel lift generators: {LIFT_GENERATORS}")
    print(f"13-element lift monoid: exact closure PASS")
    print(f"all monoid cycle lengths: {sorted(cycle_lengths)} PASS")
    print(f"literal local lifts checked: {checked} PASS")


if __name__ == "__main__":
    main()

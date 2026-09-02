#!/usr/bin/env python3
"""Solver-free controls for the Peel/Craig endpoint morph.

The proof-level statement is the four-entry section table checked by
``section_table``.  The longer enumerations are controls for the symbolic
argument, not an induction in the endpoint length.
"""

from __future__ import annotations

import argparse
from itertools import product

from dyadic_periodicity_analyzer import (
    BOUNDARY,
    cone_local,
    feed,
    inverse_terminal_cone,
    terminal_cone,
)


Vector = tuple[int, ...]

# The endpoint output section induced by prepending state 2.
TWO_SECTION = (1, 0, 2, 3)


def peel(values: Vector) -> Vector:
    return tuple(
        cone_local(values[index], values[index + 1])
        for index in range(len(values) - 1)
    )


def hard_core(values: Vector) -> bool:
    return all(value in (1, 2) for value in values) and all(
        not (left == right == 1)
        for left, right in zip(values, values[1:])
    )


def endpoint_morph(endpoint: Vector) -> Vector:
    """Return ``F(e)=T(P(I(e)))``."""

    return terminal_cone(peel(inverse_terminal_cone(endpoint)))


def section_table() -> tuple[tuple[int, int, int, int, bool], ...]:
    """Check the bounded local diagram proving ``F(2e)=g(e_0)F(e)``.

    Write ``x=I(e)``, ``y=P(x)=I(F(e))``, and

        I(2e) = (B(2), phi(2,x_0)) . P(x).

    Peeling the right side gives two leading cells followed by ``P(y)``.
    The table below identifies those cells with the endpoint-prefix grammar
    for ``g(e_0).F(e)``.  Equality of the two phi rows makes the diagram
    independent of the unbounded suffix.
    """

    records = []
    for first_endpoint in range(4):
        first_cut = BOUNDARY[first_endpoint]
        middle = cone_local(2, first_cut)
        output = TWO_SECTION[first_endpoint]
        boundary_ok = BOUNDARY[output] == cone_local(1, middle)
        row_ok = all(
            cone_local(output, following) == cone_local(middle, following)
            for following in range(4)
        )
        assert boundary_ok and row_ok
        records.append(
            (first_endpoint, first_cut, middle, output, row_ok)
        )
    return tuple(records)


def section_control(max_length: int) -> int:
    checked = 0
    for length in range(1, max_length + 1):
        for endpoint in product(range(4), repeat=length):
            expected = (
                TWO_SECTION[endpoint[0]],
            ) + endpoint_morph(endpoint)
            assert endpoint_morph((2,) + endpoint) == expected
            checked += 1
    return checked


def causal_projection_control(max_length: int) -> int:
    """Check the cut, terminal cone, and generator prefix identities."""

    checked = 0
    for length in range(2, max_length + 1):
        for values in product(range(4), repeat=length):
            assert inverse_terminal_cone(values)[:-1] == (
                inverse_terminal_cone(values[:-1])
            )
            assert terminal_cone(values)[:-1] == terminal_cone(values[:-1])
            for symbol in range(4):
                assert feed(values, symbol)[:-1] == feed(
                    values[:-1], symbol
                )
            checked += 1
    return checked


def hard_core_control(max_length: int) -> int:
    """Check the corollary that Peel preserves only the all-2 endpoint."""

    checked = 0
    for length in range(2, max_length + 1):
        for endpoint in product((1, 2), repeat=length):
            if not hard_core(endpoint):
                continue
            following = endpoint_morph(endpoint)
            assert hard_core(following) == (endpoint == (2,) * length)
            if endpoint == (2,) * length:
                assert following == (2,) * (length - 1)
            else:
                first_one = endpoint.index(1)
                if first_one == 0:
                    assert following[0] == 3
                else:
                    assert following[:first_one] == (
                        (2,) * (first_one - 1) + (0,)
                    )
            checked += 1
    return checked


def accepting_cuts(length: int) -> set[Vector]:
    return {
        inverse_terminal_cone(endpoint)
        for endpoint in product((1, 2), repeat=length)
        if hard_core(endpoint)
    }


def accepting_peel_control(max_length: int) -> int:
    checked = 0
    for length in range(2, max_length + 1):
        source = accepting_cuts(length)
        target = accepting_cuts(length - 1)
        overlap = {peel(cut) for cut in source} & target
        exceptional = {
            inverse_terminal_cone((2,) * (length - 1)),
        }
        assert overlap == exceptional
        checked += len(source)
    return checked


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-length", type=int, default=8)
    args = parser.parse_args()
    if args.max_length < 2:
        parser.error("max length must be at least two")

    print("two-section local table:")
    for endpoint, cut, middle, output, row_ok in section_table():
        print(
            f"  e0={endpoint} B(e0)={cut} a={middle} "
            f"g(e0)={output} phi-row-equal={row_ok}"
        )
    print(
        "two-section all-word control: "
        f"{section_control(args.max_length)} cases PASS"
    )
    print(
        "height-prefix causal controls: "
        f"{causal_projection_control(min(args.max_length, 7))} cases PASS"
    )
    print(
        "hard-core endpoint morph: "
        f"{hard_core_control(args.max_length)} cases PASS"
    )
    print(
        "accepting-cut Peel overlap: "
        f"{accepting_peel_control(args.max_length)} cases PASS"
    )


if __name__ == "__main__":
    main()

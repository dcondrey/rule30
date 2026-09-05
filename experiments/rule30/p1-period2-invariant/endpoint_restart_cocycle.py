#!/usr/bin/env python3
"""Exact zero/two sections and the four-phase endpoint restart cocycle.

Put ``F = T o P o I``, where ``I`` is the inverse terminal cone, ``T`` its
inverse, and ``P`` is Peel.  The existing Craig calculation gives the
section of ``F`` below a leading endpoint symbol 2.  This checker proves and
tests the complementary leading-0 section and the resulting all-length
restart law

    F^t(2^k 12 v) begins 2^(k-t) p_(t mod 4),  0 <= t <= k,

where ``p_0,p_1,p_2,p_3 = 12,03,10,00``.

The exhaustive loops are regression controls.  The proof-level claims are
the finite local section table and the symbolic prefix induction described
in ``RESULTS-ENDPOINT-RESTART-COCYCLE.md``.
"""

from __future__ import annotations

import argparse
from itertools import product

from core_craig_morph import endpoint_morph, hard_core
from dyadic_periodicity_analyzer import (
    BOUNDARY,
    cone_local,
    inverse_terminal_cone,
    terminal_cone,
)


Vector = tuple[int, ...]

ZERO_SECTION: Vector = (2, 3, 1, 0)
TWO_SECTION: Vector = (1, 0, 2, 3)
SECTIONS = {0: ZERO_SECTION, 2: TWO_SECTION}

FIRST_OUTPUT: tuple[Vector, ...] = (
    (2, 3, 1, 0),
    (0, 1, 3, 2),
    (1, 0, 2, 3),
    (3, 2, 0, 1),
)

RESTART_PHASES: tuple[Vector, ...] = (
    (1, 2),
    (0, 3),
    (1, 0),
    (0, 0),
)


def first_output(prefix: int, following: int) -> int:
    """First symbol of ``F(prefix, following, ...)`` from the local square."""

    middle = cone_local(prefix, BOUNDARY[following])
    first_cut = cone_local(BOUNDARY[prefix], middle)
    return BOUNDARY[first_cut]


def section_table_control() -> int:
    """Prove the leading-0 and leading-2 sections by the local diagram."""

    checked = 0
    assert tuple(
        tuple(first_output(prefix, following) for following in range(4))
        for prefix in range(4)
    ) == FIRST_OUTPUT

    for prefix, section in SECTIONS.items():
        for following, output in enumerate(section):
            first_cut = BOUNDARY[following]
            middle = cone_local(prefix, first_cut)

            # These are exactly the two cells required by the endpoint
            # prefix grammar for output . F(following suffix).
            assert BOUNDARY[output] == cone_local(
                BOUNDARY[prefix], middle
            )
            assert all(
                cone_local(output, right) == cone_local(middle, right)
                for right in range(4)
            )
            checked += 1
    return checked


def section_word_control(max_suffix: int) -> int:
    """Cross-check both exact sections on arbitrary finite suffixes."""

    checked = 0
    for length in range(1, max_suffix + 1):
        for endpoint in product(range(4), repeat=length):
            for prefix, section in SECTIONS.items():
                expected = (section[endpoint[0]],) + endpoint_morph(endpoint)
                assert endpoint_morph((prefix,) + endpoint) == expected
                checked += 1
    return checked


def iterate_endpoint_morph(endpoint: Vector, power: int) -> Vector:
    for _ in range(power):
        endpoint = endpoint_morph(endpoint)
    return endpoint


def inverse_endpoint_branch(output: Vector, first: int) -> Vector:
    """The unique ``v`` with ``v[0]=first`` and ``F(v)=output``.

    If ``y=I(output)`` and ``x=I(v)``, then ``P(x)=y`` and
    ``x[0]=B(first)``.  Every row of ``phi`` is a permutation, so these
    data determine ``x`` from left to right.
    """

    cut_output = inverse_terminal_cone(output)
    cut_input = [BOUNDARY[first]]
    for symbol in cut_output:
        following = [
            candidate
            for candidate in range(4)
            if cone_local(cut_input[-1], candidate) == symbol
        ]
        assert len(following) == 1
        cut_input.append(following[0])
    answer = terminal_cone(tuple(cut_input))
    assert answer[0] == first
    assert endpoint_morph(answer) == output
    return answer


def exceptional_fiber_control(max_length: int) -> int:
    """Finite controls for the exact fiber ``F^-1(T(0^omega))``.

    The all-length proof uses only row-permutativity of ``phi``.  If the
    first endpoint symbol is 1, the first cut symbol is ``B(1)=2``;
    the unique lift of the zero cut is consequently ``2^omega``.
    """

    assert all(
        sorted(cone_local(left, right) for right in range(4))
        == list(range(4))
        for left in range(4)
    )
    checked = 0
    for length in range(1, max_length + 1):
        zero_endpoint = terminal_cone((0,) * length)
        expected = terminal_cone((2,) * (length + 1))
        assert inverse_endpoint_branch(zero_endpoint, 1) == expected
        for suffix in product(range(4), repeat=length):
            endpoint = (1,) + suffix
            assert (endpoint_morph(endpoint) == zero_endpoint) == (
                endpoint == expected
            )
            checked += 1
    return checked


def tail_step(word: Vector) -> Vector:
    """Update a fixed prefix of ``W_k`` where ``U_k=2^k W_k``.

    From the leading-2 section,

        W_k = g(W_(k+1)[0]) . F(W_(k+1)).

    Thus a length-L prefix evolves without any information beyond length L.
    """

    first = TWO_SECTION.index(word[0])
    following = inverse_endpoint_branch(word[1:], first)
    assert (TWO_SECTION[following[0]],) + endpoint_morph(following) == word
    return following


def exceptional_tail_cycle_control() -> tuple[int, int, tuple[Vector, ...]]:
    """Return the exact cycle of the five-symbol exceptional tail."""

    word = terminal_cone((2,) * 5)
    orbit: list[Vector] = []
    seen: dict[Vector, int] = {}
    while word not in seen:
        seen[word] = len(orbit)
        orbit.append(word)
        word = tail_step(word)
    preperiod = seen[word]
    period = len(orbit) - preperiod
    phase_zero = tuple(orbit[index] for index in range(0, len(orbit), 4))
    assert preperiod == 0
    assert period == 32
    assert phase_zero == (
        (1, 2, 0, 0, 3),
        (1, 2, 3, 2, 1),
        (1, 2, 1, 1, 1),
        (1, 2, 2, 1, 1),
        (1, 2, 0, 1, 2),
        (1, 2, 3, 3, 2),
        (1, 2, 1, 0, 3),
        (1, 2, 2, 0, 3),
    )
    assert all(not hard_core(word) for word in phase_zero)
    return preperiod, period, phase_zero


def restart_control(max_leading_twos: int, max_suffix: int) -> int:
    """Check the four-phase prefix law on arbitrary suffix words."""

    checked = 0
    suffixes = [
        suffix
        for length in range(max_suffix + 1)
        for suffix in product(range(4), repeat=length)
    ]
    for leading in range(max_leading_twos + 1):
        for suffix in suffixes:
            endpoint = (2,) * leading + (1, 2) + suffix
            for power in range(leading + 1):
                following = iterate_endpoint_morph(endpoint, power)
                expected = (
                    (2,) * (leading - power)
                    + RESTART_PHASES[power % 4]
                )
                assert following[: len(expected)] == expected
                checked += 1
    return checked


def phase_boundary_control(max_power: int) -> int:
    """Check the sharp leading-symbol obstruction at the moving boundary."""

    for power in range(max_power + 1):
        phase = RESTART_PHASES[power % 4]
        # At the instant the defect reaches the first coordinate its value
        # is 0 or 1, never the zero-cut endpoint boundary state 3.
        assert phase[0] != 3

        # One step later the first value is 3 exactly in phase zero.
        after = first_output(*phase)
        assert (after == 3) == (power % 4 == 0)
    return max_power + 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-leading-twos", type=int, default=9)
    parser.add_argument("--max-suffix", type=int, default=4)
    parser.add_argument("--max-phase-power", type=int, default=128)
    parser.add_argument("--max-fiber-length", type=int, default=6)
    args = parser.parse_args()
    if (
        args.max_leading_twos < 0
        or args.max_suffix < 1
        or args.max_phase_power < 0
        or args.max_fiber_length < 1
    ):
        parser.error("invalid nonnegative control bound")

    local = section_table_control()
    words = section_word_control(args.max_suffix)
    restarts = restart_control(args.max_leading_twos, args.max_suffix)
    phases = phase_boundary_control(args.max_phase_power)
    fibers = exceptional_fiber_control(args.max_fiber_length)
    preperiod, period, phase_zero = exceptional_tail_cycle_control()
    print(f"zero/two section local squares: {local} PASS")
    print(f"zero/two section arbitrary-word controls: {words} PASS")
    print(f"four-phase restart prefix controls: {restarts} PASS")
    print(f"moving-boundary phase controls: {phases} PASS")
    print("restart cycle: 12 -> 03 -> 10 -> 00 -> 12 PASS")
    print(f"zero-cut exceptional fiber controls: {fibers} PASS")
    print(
        "five-symbol exceptional-tail orbit: "
        f"preperiod {preperiod}, period {period}, "
        f"{len(phase_zero)} phase-zero states PASS"
    )


if __name__ == "__main__":
    main()

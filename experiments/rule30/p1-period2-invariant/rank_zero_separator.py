#!/usr/bin/env python3
"""Exact controls for the finite-rank-to-rank-zero reduction.

The proof-level reduction is symbolic and uses the rotated Peel identity.
The support-cutoff census is deliberately finite evidence for the remaining
rank-zero separator, not a proof for arbitrary support.
"""

from __future__ import annotations

import argparse

from dyadic_periodicity_analyzer import (
    BOUNDARY,
    cone_local,
    inverse_cone_diagonal,
    terminal_cone,
)


Vector = tuple[int, ...]


def peel(values: Vector) -> Vector:
    return tuple(
        cone_local(values[index], values[index + 1])
        for index in range(len(values) - 1)
    )


def peel_power(values: Vector, power: int) -> Vector:
    for _ in range(power):
        values = peel(values)
    return values


def hard_core(values: Vector) -> bool:
    return all(value in (1, 2) for value in values) and all(
        not (left == right == 1)
        for left, right in zip(values, values[1:])
    )


def hard_core_prefixes(length: int) -> list[Vector]:
    frontier: list[Vector] = [()]
    for _ in range(length):
        frontier = [
            prefix + (value,)
            for prefix in frontier
            for value in (1, 2)
            if not (prefix and prefix[-1] == value == 1)
        ]
    return frontier


def hard_core_prefix_length(values: Vector) -> int:
    for index, value in enumerate(values):
        if value not in (1, 2):
            return index
        if index and values[index - 1] == value == 1:
            return index
    return len(values)


def cutoff_census(cutoff: int) -> tuple[int, Vector, Vector]:
    """Maximize the hard-core endpoint prefix for a cut zero after cutoff.

    Triangular bijectivity allows enumeration by the endpoint prefix: every
    candidate with a hard-core prefix of length ``cutoff`` occurs exactly
    once.  Its cut prefix is computed, followed by an exact zero ray.
    """

    horizon = 2 * cutoff + 2
    best_length = -1
    best_endpoint: Vector = ()
    best_cut: Vector = ()
    for endpoint_prefix in hard_core_prefixes(cutoff):
        cut_prefix = inverse_cone_diagonal(endpoint_prefix)
        cut = cut_prefix + (0,) * (horizon - cutoff)
        endpoint = terminal_cone(cut)
        assert endpoint[:cutoff] == endpoint_prefix
        length = hard_core_prefix_length(endpoint)
        if length > best_length:
            best_length = length
            best_endpoint = endpoint_prefix
            best_cut = cut_prefix
    assert best_length < horizon
    return best_length, best_endpoint, best_cut


def endpoint_prefix_identity_control(max_length: int = 7) -> int:
    """Check the exact cut grammar for prepending one endpoint symbol.

    If ``x=I(e)`` and ``q`` is prepended to ``e``, then

        I(qe) = (B(q), phi(q,x_0)) . P(x).
    """

    from itertools import product

    checked = 0
    for length in range(1, max_length + 1):
        for endpoint in product(range(4), repeat=length):
            cut = inverse_cone_diagonal(endpoint)
            for value in range(4):
                expected = (
                    BOUNDARY[value],
                    cone_local(value, cut[0]),
                ) + peel(cut)
                assert inverse_cone_diagonal((value,) + endpoint) == expected
                checked += 1
    return checked


def halving_identity_control(max_length: int = 9) -> int:
    """Check ``P^n I(sigma^n e)=sigma^(2n) I(e)`` on all short words."""

    from itertools import product

    checked = 0
    for length in range(2, max_length + 1):
        for endpoint in product(range(4), repeat=length):
            cut = inverse_cone_diagonal(endpoint)
            for shift in range(1, length // 2 + 1):
                tail_cut = inverse_cone_diagonal(endpoint[shift:])
                assert peel_power(tail_cut, shift) == cut[2 * shift :]
                checked += 1
    return checked


EXPECTED_MAXIMA = (
    3,
    3,
    4,
    4,
    6,
    6,
    11,
    11,
    12,
    12,
    13,
    13,
    15,
    16,
    19,
    19,
    20,
    27,
    27,
    28,
    28,
    29,
    29,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-cutoff", type=int, default=20)
    args = parser.parse_args()
    if not 1 <= args.max_cutoff <= len(EXPECTED_MAXIMA):
        parser.error(f"max cutoff must lie in 1..{len(EXPECTED_MAXIMA)}")

    prefix_checks = endpoint_prefix_identity_control()
    halving_checks = halving_identity_control()
    print(f"endpoint-prefix cut grammar: {prefix_checks} cases PASS")
    print(f"iterated halving identity: {halving_checks} cases PASS")

    for cutoff in range(1, args.max_cutoff + 1):
        maximum, endpoint, cut = cutoff_census(cutoff)
        assert maximum == EXPECTED_MAXIMA[cutoff - 1]
        print(
            f"cutoff={cutoff:2d} candidates={len(hard_core_prefixes(cutoff)):6d} "
            f"max-hard-core={maximum:2d} "
            f"endpoint={''.join(map(str, endpoint))} "
            f"cut={''.join(map(str, cut))}"
        )


if __name__ == "__main__":
    main()

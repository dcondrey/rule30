#!/usr/bin/env python3
"""Exact checks for the rotated inverse-cone/Peel identity.

The proof-level identity is uniform.  The reverse-period census is deliberately
parameter bounded; it is a guardrail for the proposed dyadic locking route,
not an induction over the period.
"""

from __future__ import annotations

import argparse
from itertools import product

from dyadic_periodicity_analyzer import (
    cone_local,
    inverse_cone_diagonal,
    least_period,
)


Vector = tuple[int, ...]


def peel(values: Vector) -> Vector:
    """The zero-indexed version of Peel: ``P(x)_t=phi(x_t,x_(t+1))``."""

    return tuple(
        cone_local(values[index], values[index + 1])
        for index in range(len(values) - 1)
    )


def hard_core(values: Vector) -> bool:
    return all(value in (1, 2) for value in values) and all(
        not (left == right == 1)
        for left, right in zip(values, values[1:])
    )


def rotated_identity_control(max_length: int) -> int:
    """Check ``P(I(shift e))=shift^2(I(e))`` on arbitrary endpoints."""

    checked = 0
    for length in range(2, max_length + 1):
        for endpoint in product(range(4), repeat=length):
            left = peel(inverse_cone_diagonal(endpoint[1:]))
            right = inverse_cone_diagonal(endpoint)[2:]
            assert left == right
            checked += 1
    return checked


def triangular_bijection_control(max_prefix: int) -> int:
    """Check that the newest cut cell is a permutation of the new endpoint.

    This is the finite triangular manifestation of right-permutivity of
    ``phi``.  It makes each reverse-period continuation unique over the full
    four-state alphabet.
    """

    checked = 0
    for length in range(max_prefix + 1):
        for prefix in product(range(4), repeat=length):
            outputs = tuple(
                inverse_cone_diagonal(prefix + (value,))[-1]
                for value in range(4)
            )
            assert set(outputs) == set(range(4))
            checked += 1
    return checked


def finite_support_control() -> tuple[int, ...]:
    """Return ``phi(s,0)`` and check preservation of a last nonzero cell."""

    boundary = tuple(cone_local(state, 0) for state in range(4))
    assert boundary == (0, 3, 3, 3)

    checked = 0
    for length in range(1, 8):
        for values in product(range(4), repeat=length):
            if values[-1] == 0:
                continue
            following = peel(values + (0,))
            assert following[-1] != 0
            checked += 1
    assert checked == sum(3 * 4 ** (length - 1) for length in range(1, 8))
    return boundary


def exact_period_lock(period: int) -> tuple[int, int]:
    """Return the peak frontier and the exact locking depth for one period.

    A frontier consists of hard-core endpoint prefixes whose inverse cut is
    exactly ``period``-periodic wherever both sides of the equality have been
    exposed.  Once the sole surviving prefix is all state 2, triangular
    bijectivity makes its continuation unique, and ``2^omega`` supplies that
    continuation for every even period.
    """

    frontier: list[Vector] = [()]
    peak = 1
    # The displayed periods lock far below this guard.  The guard is part of
    # the bounded control, not a claimed all-period estimate.
    for length in range(1, 4 * period + 8):
        following = []
        for endpoint in frontier:
            for value in (1, 2):
                candidate = endpoint + (value,)
                if not hard_core(candidate):
                    continue
                cut = inverse_cone_diagonal(candidate)
                if length <= period or cut[-1] == cut[-1 - period]:
                    following.append(candidate)
        frontier = following
        peak = max(peak, len(frontier))

        if period == 1 and not frontier:
            return peak, length
        if (
            period % 2 == 0
            and frontier == [(2,) * length]
            and length > period
        ):
            return peak, length
    raise AssertionError(f"period {period} did not lock inside bounded guard")


def reverse_period_controls() -> tuple[tuple[int, int, int], ...]:
    records = []
    for period in (1, 2, 4, 8, 16):
        peak, lock = exact_period_lock(period)
        records.append((period, peak, lock))

    # Essential negative control: hard-core endpoint (12)^omega has an
    # inverse cut of primitive period 28.  The locking observation is special
    # to the tested dyadic periods, not to all even periods.
    endpoint = (1, 2) * 98
    cut = inverse_cone_diagonal(endpoint)
    assert len(cut) % 28 == 0
    assert least_period(cut) == 28
    return tuple(records)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-identity-length", type=int, default=8)
    parser.add_argument("--max-bijection-prefix", type=int, default=7)
    args = parser.parse_args()
    if args.max_identity_length < 2 or args.max_bijection_prefix < 0:
        parser.error("identity length must be >=2 and prefix must be nonnegative")

    identities = rotated_identity_control(args.max_identity_length)
    print(
        "rotated Peel identity: "
        f"{identities} arbitrary endpoints through length "
        f"{args.max_identity_length} PASS"
    )

    bijections = triangular_bijection_control(args.max_bijection_prefix)
    print(
        "new-endpoint/new-cut triangular bijection: "
        f"{bijections} prefixes through length "
        f"{args.max_bijection_prefix} PASS"
    )

    boundary = finite_support_control()
    print(f"rightmost-nonzero preservation row phi(s,0): {boundary} PASS")

    records = reverse_period_controls()
    print(f"exact reverse-period locks (period, peak, depth): {records} PASS")
    print("non-dyadic control: endpoint (12)^omega -> primitive cut period 28 PASS")


if __name__ == "__main__":
    main()

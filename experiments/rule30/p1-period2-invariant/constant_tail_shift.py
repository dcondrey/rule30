#!/usr/bin/env python3
"""Exact spatial-shift dynamics for eventually constant inverse cuts.

If ``x=I(e)`` and ``y=I(sigma e)``, the rotated Peel identity says

    P(y) = sigma^2 x.

The first two cells of ``x`` uniquely decode the next hard-core endpoint
symbol, when that symbol exists.  Right-permutivity of ``P`` then determines
all of ``y``.  Thus endpoint shift is a deterministic partial map on exact
eventually-periodic cuts.  This script implements that map with canonical
lassos and audits the two tail modes left by the first-infinite-tail lemma.

Every census here is finite evidence.  Absence of a lasso cycle through a
bounded cutoff is not a proof that no such cycle exists at arbitrary cutoff.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from dyadic_periodicity_analyzer import (
    BOUNDARY,
    cone_local,
    inverse_cone_diagonal,
    least_period,
)
from peel_lift_monoid import LIFT_GENERATORS
from rank_zero_separator import hard_core_prefixes


Vector = tuple[int, ...]


@dataclass(frozen=True, slots=True)
class Lasso:
    """A canonical one-sided eventually-periodic four-state sequence."""

    prefix: Vector
    cycle: Vector

    @staticmethod
    def canonical(prefix: Vector, cycle: Vector) -> "Lasso":
        if not cycle:
            raise ValueError("a lasso cycle must be nonempty")
        period = least_period(cycle)
        cycle = cycle[:period]
        prefix = tuple(prefix)

        # Move the onset of periodicity left whenever the cell immediately
        # before the cycle already agrees with its periodic predecessor.
        while prefix and prefix[-1] == cycle[-1]:
            prefix = prefix[:-1]
            cycle = cycle[-1:] + cycle[:-1]
        return Lasso(prefix, cycle)

    @property
    def preperiod(self) -> int:
        return len(self.prefix)

    @property
    def period(self) -> int:
        return len(self.cycle)

    def value(self, index: int) -> int:
        if index < 0:
            raise IndexError(index)
        if index < self.preperiod:
            return self.prefix[index]
        return self.cycle[(index - self.preperiod) % self.period]

    def take(self, length: int) -> Vector:
        return tuple(self.value(index) for index in range(length))

    def shifted(self, amount: int) -> "Lasso":
        if amount < 0:
            raise ValueError(amount)
        if amount < self.preperiod:
            return Lasso.canonical(self.prefix[amount:], self.cycle)
        phase = (amount - self.preperiod) % self.period
        cycle = self.cycle[phase:] + self.cycle[:phase]
        return Lasso.canonical((), cycle)


def decode_next_boundary(cut: Lasso) -> int | None:
    """Decode ``B(e_1)`` if the first endpoint edge is hard-core.

    Put ``a_j=B(e_j)``.  Hard-core endpoints have ``a_j in {1,2}`` and
    forbid ``a_j=a_(j+1)=2``.  The exact first-diagonal equation is

        x_1 = phi(B(a_0), a_1).

    The admissible ``a_1`` is unique whenever it exists.
    """

    first = cut.value(0)
    if first not in (1, 2):
        return None
    candidates = tuple(
        following
        for following in (1, 2)
        if not (first == following == 2)
        and cone_local(BOUNDARY[first], following) == cut.value(1)
    )
    assert len(candidates) <= 1
    return candidates[0] if candidates else None


def lift_lasso(output: Lasso, initial: int) -> Lasso:
    """Return the unique ``y`` with ``y_0=initial`` and ``P(y)=output``."""

    values = [initial]
    state = initial

    # Consume the nonperiodic driver before cycle detection.  At recurrence
    # time t, ``state`` is y_t and ``output[t]`` determines y_(t+1).
    for time in range(output.preperiod):
        state = LIFT_GENERATORS[output.value(time)][state]
        values.append(state)

    seen: dict[tuple[int, int], int] = {}
    time = output.preperiod
    while True:
        phase_state = ((time - output.preperiod) % output.period, state)
        if phase_state in seen:
            onset = seen[phase_state]
            return Lasso.canonical(
                tuple(values[:onset]), tuple(values[onset:time])
            )
        seen[phase_state] = time
        state = LIFT_GENERATORS[output.value(time)][state]
        values.append(state)
        time += 1


def endpoint_shift(cut: Lasso) -> Lasso | None:
    """Apply ``I(e) -> I(sigma e)`` on the hard-core domain, if defined."""

    following_boundary = decode_next_boundary(cut)
    if following_boundary is None:
        return None
    # P(I(sigma e)) = sigma^2 I(e).
    return lift_lasso(cut.shifted(2), following_boundary)


@dataclass(frozen=True, slots=True)
class OrbitResult:
    survival: int | None
    steps_to_cycle: int | None
    cycle_length: int | None
    maximum_preperiod: int
    maximum_period: int
    period_trace: tuple[int, ...]


def hard_core_orbit(cut: Lasso, cap: int | None = None) -> OrbitResult:
    """Iterate endpoint shift until hard-core failure or a lasso cycle."""

    seen: dict[Lasso, int] = {}
    maximum_preperiod = cut.preperiod
    maximum_period = cut.period
    period_trace: list[int] = []
    step = 0
    while True:
        if cut.value(0) not in (1, 2):
            return OrbitResult(
                step,
                None,
                None,
                maximum_preperiod,
                maximum_period,
                tuple(period_trace),
            )
        if cut in seen:
            return OrbitResult(
                None,
                seen[cut],
                step - seen[cut],
                maximum_preperiod,
                maximum_period,
                tuple(period_trace),
            )
        if cap is not None and step >= cap:
            raise RuntimeError(f"orbit exceeded explicit cap {cap}")
        seen[cut] = step
        period_trace.append(cut.period)
        maximum_preperiod = max(maximum_preperiod, cut.preperiod)
        maximum_period = max(maximum_period, cut.period)

        following = endpoint_shift(cut)
        if following is None:
            # The current endpoint symbol is valid; the next one is the first
            # invalid symbol or creates the forbidden hard-core pair 11.
            return OrbitResult(
                step + 1,
                None,
                None,
                maximum_preperiod,
                maximum_period,
                tuple(period_trace),
            )
        cut = following
        step += 1


def literal_controls(max_endpoint_length: int = 10) -> int:
    """Match lasso shifts to direct inverse diagonals on every short word."""

    checked = 0
    for length in range(2, max_endpoint_length + 1):
        for endpoint in hard_core_prefixes(length):
            finite_cut = inverse_cone_diagonal(endpoint)
            # Any continuation works for the prefix control.  Four constant
            # tails also exercise canonical lasso normalization.
            for tail in range(4):
                cut = Lasso.canonical(finite_cut, (tail,))
                for shift in range(length - 1):
                    expected = inverse_cone_diagonal(endpoint[shift:])
                    assert cut.take(len(expected)) == expected
                    following = endpoint_shift(cut)
                    assert following is not None
                    cut = following
                    checked += 1
    return checked


def cutoff_census(cutoff: int, tail: int) -> tuple[int, Vector, OrbitResult]:
    """Maximize hard-core survival over the exact cutoff-``tail`` fiber."""

    maximum = -1
    witness: Vector = ()
    best: OrbitResult | None = None
    for endpoint in hard_core_prefixes(cutoff):
        cut_prefix = inverse_cone_diagonal(endpoint)
        cut = Lasso.canonical(cut_prefix, (tail,))
        result = hard_core_orbit(cut)
        if result.survival is None:
            raise AssertionError(
                "an exact eventually-constant hard-core lasso cycle was found: "
                f"tail={tail}, cutoff={cutoff}, endpoint={endpoint}, result={result}"
            )
        if result.survival > maximum:
            maximum = result.survival
            witness = endpoint
            best = result
    assert best is not None
    return maximum, witness, best


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-cutoff", type=int, default=20)
    parser.add_argument("--control-length", type=int, default=9)
    args = parser.parse_args()
    if args.max_cutoff < 1:
        parser.error("max cutoff must be positive")

    checked = literal_controls(args.control_length)
    print(f"literal endpoint-shift controls: {checked} cases PASS")
    for cutoff in range(1, args.max_cutoff + 1):
        fields = []
        for tail in (2, 3):
            maximum, endpoint, result = cutoff_census(cutoff, tail)
            fields.append(
                f"tail={tail} max={maximum:2d} "
                f"max-mu={result.maximum_preperiod:2d} "
                f"max-p={result.maximum_period:2d} "
                f"periods={','.join(map(str, result.period_trace))} "
                f"e={''.join(map(str, endpoint))}"
            )
        print(f"cutoff={cutoff:2d} " + " | ".join(fields))


if __name__ == "__main__":
    main()

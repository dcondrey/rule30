#!/usr/bin/env python3
"""Exact audit of the proposed radius-two Bellman energy.

The proposed constraints are inconsistent.  This file verifies that fact in
two independent ways:

1. Z3's exact QF_LRA tactic checks the posted truncated system.
2. A hard-coded Farkas certificate, evaluated with ``Fraction`` arithmetic,
   cancels every energy variable and derives ``-2 >= 0``.

The Farkas certificate uses only one length-three hard-core initialization
and peel inequalities on words of length at most five.  It is therefore a
subset of both posted systems (the original N=7 system and the optimized
N=5 system).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import Iterable

from z3 import Real, Sum, Tactic, unsat


Word = tuple[int, ...]
Variable = tuple[str, Word | int]


def peel(q: Word) -> Word:
    return tuple(
        2 * (a & 1) + ((b & 1) ^ ((a & 1) | (a >> 1)))
        for a, b in zip(q, q[1:])
    )


def hard_core_words(length: int) -> Iterable[Word]:
    for rho in product((0, 1), repeat=length):
        if all(not (a == b == 1) for a, b in zip(rho, rho[1:])):
            yield rho


def init(rho: Word) -> Word:
    return tuple(symbol for bit in rho for symbol in (1 - bit, 3))


def encode(word: Word) -> int:
    value = 0
    for symbol in word:
        value = 4 * value + symbol
    return value


def z3_check() -> None:
    """Reproduce the optimized posted system and require exact UNSAT."""

    radius = 2
    weights = [Real(f"w{radius}_{index}") for index in range(4**radius)]
    prefixes = [Real(f"p{radius}_{index}") for index in range(4)]
    suffixes = [Real(f"s{radius}_{index}") for index in range(4)]
    short = {
        word: Real(f"u{radius}_{len(word)}_{encode(word)}")
        for length in range(radius)
        for word in product(range(4), repeat=length)
    }

    def energy(word: Word):
        if len(word) < radius:
            return short[word]
        return (
            Sum(
                weights[encode(word[index : index + radius])]
                for index in range(len(word) - radius + 1)
            )
            + prefixes[word[0]]
            + suffixes[word[-1]]
        )

    solver = Tactic("qflra").solver()
    solver.add(short[()] == 0)
    for length in range(1, 6):
        for word in product(range(4), repeat=length):
            solver.add(
                energy(word)
                <= 2 * (word[0] & 1) + energy(peel(word))
            )
    for length in range(1, 9):
        for rho in hard_core_words(length):
            solver.add(energy(init(rho)) >= sum(rho))

    result = solver.check()
    assert result == unsat, f"expected unsat, got {result}"


@dataclass(frozen=True)
class Affine:
    coefficients: dict[Variable, Fraction]
    constant: Fraction = Fraction(0)

    def __add__(self, other: "Affine") -> "Affine":
        coefficients = dict(self.coefficients)
        for variable, coefficient in other.coefficients.items():
            coefficients[variable] = (
                coefficients.get(variable, Fraction(0)) + coefficient
            )
            if coefficients[variable] == 0:
                del coefficients[variable]
        return Affine(coefficients, self.constant + other.constant)

    def __sub__(self, other: "Affine") -> "Affine":
        return self + (-1) * other

    def __rmul__(self, scalar: int | Fraction) -> "Affine":
        scalar = Fraction(scalar)
        return Affine(
            {
                variable: scalar * coefficient
                for variable, coefficient in self.coefficients.items()
                if scalar * coefficient
            },
            scalar * self.constant,
        )


def symbolic_energy(word: Word) -> Affine:
    """Return E(word) as an exact affine expression in W, P, S, and U."""

    if len(word) < 2:
        return Affine({("U", word): Fraction(1)})

    coefficients: dict[Variable, Fraction] = {
        ("P", word[0]): Fraction(1),
        ("S", word[-1]): Fraction(1),
    }
    for left, right in zip(word, word[1:]):
        variable = ("W", 4 * left + right)
        coefficients[variable] = coefficients.get(variable, Fraction(0)) + 1
    return Affine(coefficients)


def peel_gap(word: Word) -> Affine:
    """The asserted nonnegative gap D(word)."""

    return (
        symbolic_energy(peel(word))
        - symbolic_energy(word)
        + Affine({}, Fraction(2 * (word[0] & 1)))
    )


def initial_gap(rho: Word) -> Affine:
    """The asserted nonnegative gap I(rho)."""

    return symbolic_energy(init(rho)) + Affine({}, Fraction(-sum(rho)))


# Multiplying the Z3 core by two gives this integer Farkas certificate.
# Every coefficient of I or D is nonnegative.
FARKAS_TERMS: tuple[tuple[int, str, Word], ...] = (
    (16, "I", (1, 0, 1)),
    (4, "D", (0, 1, 3, 0, 3)),
    (1, "D", (1, 3, 1, 2)),
    (14, "D", (1, 3, 0, 3)),
    (8, "D", (0, 3, 1, 2)),
    (10, "D", (0, 2, 3, 1)),
    (2, "D", (0, 1, 2, 3)),
    (15, "D", (2, 3, 1)),
    (1, "D", (0, 2, 2)),
    (1, "D", (0, 1, 2)),
    (6, "D", (0, 0, 3)),
    (2, "D", (0, 0, 0)),
    (14, "D", (0, 2)),
    (2, "D", (0, 0)),
    (16, "D", (0,)),
)


def verify_farkas_certificate() -> None:
    """Check that the proposed nonnegative gaps sum identically to -2."""

    total = Affine({})
    for multiplier, kind, word in FARKAS_TERMS:
        assert multiplier >= 0
        gap = initial_gap(word) if kind == "I" else peel_gap(word)
        total += multiplier * gap

    # The equality U(empty)=0 may be added with arbitrary multiplier.  Its
    # coefficient -16 cancels the sole remaining symbolic coefficient.
    total += -16 * symbolic_energy(())

    assert total.coefficients == {}, total.coefficients
    assert total.constant == -2, total.constant


def main() -> None:
    z3_check()
    verify_farkas_certificate()
    print("posted radius-2 QF_LRA system: UNSAT")
    print("exact Farkas certificate: -2 >= 0 (contradiction)")
    print("maximum peel-word length in certificate: 5")
    print("only hard-core initialization in certificate: 101")


if __name__ == "__main__":
    main()

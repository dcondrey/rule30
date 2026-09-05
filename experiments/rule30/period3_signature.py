#!/usr/bin/env python3
"""Finite carry-signature conjugacy for primitive period-three cores.

Delete the phase-dependent boundary append from the quotient transducer and
call the resulting length-preserving map ``interior_step``.  Its parity
sequence is finite: every two iterations increase the inert leading-zero
prefix by at least one symbol.  Packing those parities as the low-to-high
bits of an integer converts the full driven word map into a partial map on
nonnegative integers.

This is an exact conjugacy on signatures, not an all-length mortality proof.
"""

from __future__ import annotations

import argparse
from itertools import product

from period3_active_core import (
    normalize_deep,
    pair_parity,
    quotient_driven_step,
    quotient_step,
)
from period3_fiber_probe import PERIOD_WORDS
from period3_survival_automaton import propagate_symbol

QuotientCore = tuple[int, ...]


def interior_step(core: QuotientCore) -> QuotientCore:
    """Apply the quotient scan without normalization or boundary append."""

    carry = 0
    output = []
    for symbol in core:
        if not 0 <= symbol < 3:
            raise ValueError("quotient symbols must lie in [0,2]")
        output.append(2 if carry else int(symbol == 2))
        carry ^= int(symbol != 0)
    return tuple(output)


def leading_zeros(core: QuotientCore) -> int:
    """Count the inert deep prefix without changing the word length."""

    return next((index for index, symbol in enumerate(core) if symbol), len(core))


def signature(core: QuotientCore) -> int:
    """Pack ``parity(interior_step**j(core))`` into bit ``j``."""

    current = normalize_deep(core)
    result = 0
    for layer in range(2 * len(current)):
        result |= pair_parity(current) << layer
        current = interior_step(current)
    if any(current):
        raise AssertionError("interior transducer exceeded its nilpotence bound")
    return result


def signature_step(value: int, center: int) -> int:
    """Advance one free quotient step directly on its finite signature."""

    if value < 0:
        raise ValueError("signature must be nonnegative")
    parity = value & 1
    boundary = 2 if parity else (center & 1)
    tail = value >> 1
    # A nonzero input signal crossing an eventually-zero carry ray stops after
    # at most two extra layers.  This horizon therefore gives the exact finite
    # integer, including both possible terminal one bits.
    return propagate_symbol(tail, boundary, tail.bit_length() + 3)


def signature_driven_step(
    value: int, period: tuple[int, ...], phase: int
) -> int | None:
    """Apply one period-driven step, or reject a failed one-phase pin."""

    center = period[phase % len(period)]
    following = period[(phase + 1) % len(period)]
    parity = value & 1
    if center == 1 and parity != (1 ^ following):
        return None
    return signature_step(value, center)


def exhaustive_control(max_length: int = 8) -> None:
    """Cross-check nilpotence and both signature conjugacies exhaustively."""

    for length in range(max_length + 1):
        for core in product(range(3), repeat=length):
            first = interior_step(core)
            second = interior_step(first)
            assert leading_zeros(second) >= min(
                length, leading_zeros(core) + 1
            )

            value = signature(core)
            for center in (0, 1):
                following = quotient_step(core, center)
                assert signature(following) == signature_step(value, center)

            for period in PERIOD_WORDS:
                for phase in range(len(period)):
                    word_result = quotient_driven_step(core, period, phase)
                    integer_result = signature_driven_step(value, period, phase)
                    assert (word_result is None) == (integer_result is None)
                    if word_result is not None:
                        assert integer_result == signature(word_result)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--control-length", type=int, default=8)
    args = parser.parse_args()
    if args.control_length < 0:
        parser.error("control length must be nonnegative")
    exhaustive_control(args.control_length)
    print(
        "period-three finite carry signature: "
        f"complete control through length {args.control_length} PASS"
    )


if __name__ == "__main__":
    main()

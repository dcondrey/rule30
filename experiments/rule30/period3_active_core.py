#!/usr/bin/env python3
"""Exact active-core conjugacy for primitive period-three Rule 30 traces.

The anti-diagonal frontier in ``period3_fiber_probe`` consists of pairs
``q_j=(A_j,B_(j-1))`` read from the shallow end toward the deep end.  After
the finite-left knee, survival forces the next deepest output to zero.  The
input value is therefore the parity of the nonzero pair-symbols.  With that
choice, one frontier step is a two-state sequential transducer and any deep
``00`` suffix is inert and may be stripped exactly.

This file pins that conjugacy and explores mortality of the resulting finite
word map.  A bounded census is not an all-length period-three proof.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import product
from typing import Iterable

from period3_fiber_probe import (
    PERIOD_WORDS,
    Frontier,
    frontier_step,
    or_parity,
)

Core = tuple[int, ...]
QuotientCore = tuple[int, ...]


def normalize(core: Iterable[int]) -> Core:
    """Remove the maximal inert deep ``00`` suffix."""

    result = list(core)
    if any(not 0 <= symbol < 4 for symbol in result):
        raise ValueError("pair symbols must lie in [0,3]")
    while result and result[-1] == 0:
        result.pop()
    return tuple(result)


def pair_parity(core: Core) -> int:
    """Parity of ``a OR b`` over pair-symbols ``2*a+b``."""

    return sum(symbol != 0 for symbol in core) & 1


def frontier_pairs(period: tuple[int, ...], frontier: Frontier) -> Core:
    """Encode a literal frontier as shallow-to-deep pair-symbols."""

    time, newest, older = frontier
    if time == 0:
        return ()
    boundary = period[(time - 1) % len(period)]
    symbols = []
    for depth in range(1, time + 1):
        a = (newest >> (depth - 1)) & 1
        b = boundary if depth == 1 else (older >> (depth - 2)) & 1
        symbols.append(2 * a + b)
    return tuple(symbols)


def core_step(core: Core, center: int) -> Core:
    """Advance one zero-emitting frontier step and normalize its deep tail."""

    core = normalize(core)
    carry = pair_parity(core)
    output = [2 * carry + (center & 1)]
    for symbol in core:
        a, b = symbol >> 1, symbol & 1
        carry ^= a | b
        output.append(2 * carry + a)
    if carry:
        raise AssertionError("parity-selected scan did not finish at zero")
    return normalize(output)


def raw_symbol_quotient(symbol: int) -> int:
    """Map ``00,01,10,11`` to the exact quotient ``0,1,2,2``."""

    if not 0 <= symbol < 4:
        raise ValueError("pair symbols must lie in [0,3]")
    return 2 if symbol & 2 else symbol & 1


def deep_quotient(core: Core) -> QuotientCore:
    """Return the normalized core in deep-to-shallow quotient orientation."""

    return tuple(raw_symbol_quotient(symbol) for symbol in reversed(normalize(core)))


def normalize_deep(core: Iterable[int]) -> QuotientCore:
    """Strip the inert leading zeros in deep-to-shallow orientation."""

    result = tuple(core)
    if any(not 0 <= symbol < 3 for symbol in result):
        raise ValueError("quotient symbols must lie in [0,2]")
    first = next((index for index, symbol in enumerate(result) if symbol), len(result))
    return result[first:]


def quotient_step(core: QuotientCore, center: int) -> QuotientCore:
    """Advance the exact three-symbol core quotient by one free step."""

    core = normalize_deep(core)
    carry = 0
    output = []
    for symbol in core:
        output.append(2 if carry else int(symbol == 2))
        if symbol:
            carry ^= 1
    parity = pair_parity(core)
    if carry != parity:
        raise AssertionError("quotient scan parity mismatch")
    output.append(2 if parity else (center & 1))
    return normalize_deep(output)


def driven_step(core: Core, period: tuple[int, ...], phase: int) -> Core | None:
    """Apply one period-driven step, returning ``None`` on a failed pin."""

    center = period[phase % len(period)]
    following = period[(phase + 1) % len(period)]
    parity = pair_parity(core)
    if center == 1 and parity != (1 ^ following):
        return None
    return core_step(core, center)


def quotient_driven_step(
    core: QuotientCore, period: tuple[int, ...], phase: int
) -> QuotientCore | None:
    """Apply a checked period-driven step to the three-symbol quotient."""

    center = period[phase % len(period)]
    following = period[(phase + 1) % len(period)]
    parity = pair_parity(core)
    if center == 1 and parity != (1 ^ following):
        return None
    return quotient_step(core, center)


@dataclass(frozen=True)
class Lifetime:
    steps: int | None
    maximum_length: int
    final_core: Core


def lifetime(
    core: Core,
    period: tuple[int, ...],
    phase: int,
    cap: int = 1024,
) -> Lifetime:
    """Run one normalized core until a pin fails or a finite cap is reached."""

    if cap < 1:
        raise ValueError("cap must be positive")
    current = normalize(core)
    maximum = len(current)
    for elapsed in range(1, cap + 1):
        following = driven_step(current, period, phase + elapsed - 1)
        if following is None:
            return Lifetime(elapsed, maximum, current)
        current = following
        maximum = max(maximum, len(current))
    return Lifetime(None, maximum, current)


def normalized_cores(length: int) -> Iterable[Core]:
    """Enumerate each normalized core of one exact length once."""

    if length < 0:
        raise ValueError("length must be nonnegative")
    if length == 0:
        yield ()
        return
    for prefix in product(range(4), repeat=length - 1):
        for final in (1, 2, 3):
            yield (*prefix, final)


def check_frontier_conjugacy(max_input_length: int = 9) -> None:
    """Cross-check the word map against the independent integer frontier."""

    for period in PERIOD_WORDS:
        for length in range(max_input_length + 1):
            for values in product((0, 1), repeat=length):
                frontier: Frontier = (0, 0, 0)
                for value in values:
                    frontier = frontier_step(period, frontier, value)
                time = frontier[0]
                pairs = frontier_pairs(period, frontier)
                assert pair_parity(pairs) == or_parity(period, frontier)

                selected = pair_parity(pairs)
                literal = frontier_step(period, frontier, selected)
                assert normalize(frontier_pairs(period, literal)) == core_step(
                    normalize(pairs), period[time % len(period)]
                )


def census(period: tuple[int, ...], maximum_length: int, cap: int) -> None:
    print(f"trace={''.join(map(str, period))}")
    for length in range(maximum_length + 1):
        count = 0
        survivors = 0
        longest = -1
        witness: tuple[int, Core] | None = None
        maximum_growth = 0
        for phase in range(len(period)):
            for core in normalized_cores(length):
                count += 1
                result = lifetime(core, period, phase, cap)
                maximum_growth = max(maximum_growth, result.maximum_length)
                if result.steps is None:
                    survivors += 1
                elif result.steps > longest:
                    longest = result.steps
                    witness = phase, core
        print(
            f"  length={length:2d} cores={count:8d} survivors={survivors:3d} "
            f"max_lifetime={longest:4d} max_length={maximum_growth:3d} "
            f"witness={witness}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-length", type=int, default=8)
    parser.add_argument("--cap", type=int, default=512)
    parser.add_argument("--frontier-check-length", type=int, default=9)
    args = parser.parse_args()
    if args.max_length < 0 or args.frontier_check_length < 0 or args.cap < 1:
        parser.error("lengths must be nonnegative and cap positive")

    check_frontier_conjugacy(args.frontier_check_length)
    print("period-three active-core/frontier conjugacy: PASS")
    for period in PERIOD_WORDS[::-1]:
        census(period, args.max_length, args.cap)


if __name__ == "__main__":
    main()

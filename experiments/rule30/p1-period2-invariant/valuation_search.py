#!/usr/bin/env python3
"""Screen the natural (1+x)-adic ranks of the forced frontier map.

For a finite Boolean word P, one cumulative-XOR sweep is polynomial division
by 1+x after the parity remainder is supplied.  This makes root multiplicity
at x=1 the canonical non-additive rank to test after local energies fail.
Every reported failure is an exact transition of the frontier recurrence.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from ranking_search import (  # noqa: E402
    Transition,
    frontier_word,
    reachable_transitions,
)


def divide_by_one_plus_x(poly: int) -> tuple[int, int]:
    """Return quotient,remainder for a GF(2) polynomial bit mask."""
    if poly == 0:
        return 0, 0
    degree = poly.bit_length() - 1
    if degree == 0:
        return 0, poly & 1
    quotient = 0
    carry = (poly >> degree) & 1
    if degree:
        quotient |= carry << (degree - 1)
    for exponent in range(degree - 1, 0, -1):
        carry ^= (poly >> exponent) & 1
        quotient |= carry << (exponent - 1)
    remainder = carry ^ (poly & 1)
    assert poly == (quotient ^ (quotient << 1) ^ remainder)
    return quotient, remainder


def valuation(poly: int, cap: int = 10_000) -> int:
    if poly == 0:
        return cap
    value = 0
    while value < cap:
        quotient, remainder = divide_by_one_plus_x(poly)
        if remainder:
            return value
        value += 1
        poly = quotient
        if poly == 0:
            return cap
    return cap


def polynomial(word: tuple[int, ...], table: int) -> int:
    result = 0
    for exponent, symbol in enumerate(word):
        result |= ((table >> symbol) & 1) << exponent
    return result


def measures(word: tuple[int, ...], table: int) -> tuple[int, int, int, int]:
    poly = polynomial(word, table)
    degree = poly.bit_length()
    nu = valuation(poly, len(word) + 1)
    return nu, degree, degree - min(nu, degree), len(word) - degree


@dataclass
class Score:
    table: int
    measure_index: int
    direction: int
    violations: int
    equals: int
    first_violation: Transition | None
    before_value: int | None
    after_value: int | None


def screen(transitions: list[Transition]) -> list[Score]:
    scores: list[Score] = []
    for table in range(1, 15):  # omit the two constant Boolean functions
        for measure_index in range(4):
            for direction in (-1, 1):
                violations = 0
                equals = 0
                first = None
                first_values = (None, None)
                for tr in sorted(
                    transitions,
                    key=lambda item: (item.seed_length, item.seed, item.survival_step),
                ):
                    before = measures(frontier_word(0, tr.before), table)[measure_index]
                    after = measures(frontier_word(0, tr.after), table)[measure_index]
                    change = direction * (after - before)
                    if change >= 0:  # desired direction is strict decrease
                        violations += 1
                        equals += int(change == 0)
                        if first is None:
                            first = tr
                            first_values = before, after
                scores.append(
                    Score(
                        table, measure_index, direction, violations, equals,
                        first, first_values[0], first_values[1],
                    )
                )
    return scores


def table_label(table: int) -> str:
    return "".join(str((table >> symbol) & 1) for symbol in range(4))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-seed", type=int, default=12)
    parser.add_argument("--max-follow", type=int, default=64)
    args = parser.parse_args()

    # Exhaust the polynomial division identity over every polynomial of
    # degree below 12 before using the valuation.
    for poly in range(1 << 12):
        quotient, remainder = divide_by_one_plus_x(poly)
        assert remainder == (poly.bit_count() & 1)
        assert poly == (quotient ^ (quotient << 1) ^ remainder)
    print("GF(2) division by 1+x: PASS (4096/4096 polynomials)")

    transitions = reachable_transitions(args.max_seed, args.max_follow)
    scores = sorted(screen(transitions), key=lambda item: (item.violations, item.equals))
    names = ("valuation", "degree", "degree-minus-valuation", "deep-zero-run")
    for score in scores[:12]:
        tr = score.first_violation
        direction = "increasing rank" if score.direction == -1 else "decreasing rank"
        if tr is None:
            print(
                f"table={table_label(score.table)} measure={names[score.measure_index]} "
                f"orientation={direction} SURVIVES all {len(transitions)} transitions"
            )
            continue
        print(
            f"table={table_label(score.table)} measure={names[score.measure_index]} "
            f"orientation={direction} violations={score.violations}/"
            f"{len(transitions)} equals={score.equals}; first="
            f"seed_length={tr.seed_length} seed={tr.seed:0{tr.seed_length}b} "
            f"follow={tr.survival_step} values={score.before_value}->{score.after_value}"
        )
    useful = [score for score in scores if score.direction == 1 and score.violations == 0]
    if useful:
        print("strict decreasing candidate survives; requires independent/global verification")
    else:
        print(
            "no strict decreasing nonnegative (1+x)-adic/degree rank survives; "
            "the zero-violation entries above are unbounded growth diagnostics"
        )


if __name__ == "__main__":
    main()

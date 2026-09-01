#!/usr/bin/env python3
"""Exact cutoff census for the first-infinite-tail reduction.

Every rank-zero hard-core counterexample would yield an endpoint tail whose
inverse cut is eventually constant 2 or 3.  This script enumerates those two
constant-tail fibers by endpoint prefix, using triangular bijectivity.  Its
finite cutoff table is a falsifier/control for the remaining uniform lemma,
not an induction over the cutoff.
"""

from __future__ import annotations

import argparse

from dyadic_periodicity_analyzer import inverse_cone_diagonal, terminal_cone
from rank_zero_separator import (
    hard_core_prefix_length,
    hard_core_prefixes,
)


Vector = tuple[int, ...]

EXPECTED_MAXIMA = {
    2: (
        2, 2, 5, 5, 6, 7, 10, 10, 10, 11, 13, 14,
        16, 18, 19, 19, 19, 20, 22, 24, 24, 26, 28,
    ),
    3: (
        1, 3, 3, 5, 5, 10, 10, 10, 10, 12, 13, 14,
        15, 18, 18, 19, 26, 26, 26, 26, 26, 26, 29,
    ),
}


def constant_tail_census(
    cutoff: int, tail: int
) -> tuple[int, Vector, Vector, Vector]:
    if tail not in (2, 3):
        raise ValueError("the first-infinite-tail modes are exactly 2 and 3")
    horizon = 2 * cutoff + 2
    best_length = -1
    best_prefix: Vector = ()
    best_cut: Vector = ()
    best_failure: Vector = ()
    for endpoint_prefix in hard_core_prefixes(cutoff):
        cut_prefix = inverse_cone_diagonal(endpoint_prefix)
        cut = cut_prefix + (tail,) * (horizon - cutoff)
        endpoint = terminal_cone(cut)
        assert endpoint[:cutoff] == endpoint_prefix
        length = hard_core_prefix_length(endpoint)
        if length > best_length:
            best_length = length
            best_prefix = endpoint_prefix
            best_cut = cut_prefix
            best_failure = endpoint[length : length + 2]
    return best_length, best_prefix, best_cut, best_failure


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-cutoff", type=int, default=20)
    args = parser.parse_args()
    if args.max_cutoff < 1:
        parser.error("max cutoff must be positive")

    for cutoff in range(1, args.max_cutoff + 1):
        fields = []
        for tail in (2, 3):
            maximum, endpoint, cut, failure = constant_tail_census(cutoff, tail)
            if cutoff <= len(EXPECTED_MAXIMA[tail]):
                assert maximum == EXPECTED_MAXIMA[tail][cutoff - 1]
            fields.append(
                f"tail={tail} max={maximum:2d} "
                f"e={''.join(map(str, endpoint))} "
                f"x={''.join(map(str, cut))} "
                f"fail={''.join(map(str, failure))}"
            )
        print(f"cutoff={cutoff:2d} " + " | ".join(fields))


if __name__ == "__main__":
    main()

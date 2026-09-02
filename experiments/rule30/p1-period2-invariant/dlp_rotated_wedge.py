#!/usr/bin/env python3
"""Exact controls for the rotated-wedge form of late-pull exclusion.

The proof-level content is the already proved iterated rotated-Peel identity.
This checker independently verifies that the padded scale formulation and the
unpadded finite-word formulation agree on every small source word.  The
enumeration is a control for the conjugacy, not an all-length proof of DLP.
"""

from __future__ import annotations

import argparse
import itertools

from constant_tail_scale import Vector
from late_pull_diagonal_sat import literal_extension, literal_witness
from rank_zero_separator import peel_power
from dyadic_periodicity_analyzer import inverse_cone_diagonal


def rotated_wedge_witness(word: Vector, tail: int, residue: int) -> bool:
    """Return the exact unpadded DLP predicate for one binary source."""

    n = len(word)
    target = n + residue
    continuation = literal_extension(word, tail, target + 2)
    finite_endpoint = word + continuation
    assert len(finite_endpoint) == 2 * n + residue + 2

    # The appended endpoint, including its junction with W, must survive as
    # a hard-core word.  W itself is only required to use states 1 and 2.
    surviving = all(
        value in (1, 2)
        and not (
            index >= n
            and finite_endpoint[index - 1] == value == 1
        )
        for index, value in enumerate(finite_endpoint)
        if index >= n
    )
    if not surviving:
        return False

    cut = peel_power(inverse_cone_diagonal(finite_endpoint), n)
    expected_length = n + residue + 2
    assert len(cut) == expected_length
    constant_row = cut == (tail,) * expected_length
    terminal_pull = finite_endpoint[-3:-1] == (1, 2)
    return constant_row and terminal_pull


def padded_cut_identity(word: Vector, tail: int, residue: int) -> bool:
    """Check the cellwise rotated identity on the finite DLP wedge."""

    n = len(word)
    target = n + residue
    continuation = literal_extension(word, tail, target + 2)
    padded = (0,) * n + word + continuation
    unpadded = word + continuation
    left = peel_power(inverse_cone_diagonal(unpadded), n)
    right = inverse_cone_diagonal(padded)[2 * n :]
    return left == right == (tail,) * (target + 2)


def controls(max_length: int) -> tuple[int, int]:
    identities = 0
    predicates = 0
    for n in range(1, max_length + 1):
        for word in itertools.product((1, 2), repeat=n):
            for tail in (2, 3):
                for residue in (0, 1, 2):
                    assert padded_cut_identity(word, tail, residue)
                    identities += n + residue + 2
                    direct = literal_witness(word, tail, residue)
                    rotated = rotated_wedge_witness(word, tail, residue)
                    assert direct == rotated
                    predicates += 1
    return identities, predicates


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-length", type=int, default=7)
    args = parser.parse_args()
    if args.max_length < 1:
        parser.error("max length must be positive")

    identities, predicates = controls(args.max_length)
    print(
        f"rotated finite-wedge cells: {identities} PASS; "
        f"DLP predicate equivalences: {predicates} PASS"
    )


if __name__ == "__main__":
    main()

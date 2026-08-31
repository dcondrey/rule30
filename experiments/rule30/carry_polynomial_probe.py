"""Falsify the carry-polynomial matrix contract from Crosstalk run 3.

The proposed contract represents polynomials in GF(2)[z]/(z**k) as bitsets and
asserts

    s_n(0) = e1.T * product_j B(bit_j(n), j) * e1, evaluated at z = 0,

with

    B(0, 0) = [[1+z, z], [z, 1]],
    B(1, 0) = [[1+z, 1+z], [z, 1+z]],
    B(0, j+1) = B(0, j)^2,
    B(1, j+1) = B(1, j) B(0, j).

This is the candidate's formula, implemented literally.  Its constant-term
matrices already expose the defect: B(0, j)|z=0 is the identity and
B(1, j)|z=0 is upper triangular with a one in position (0, 0), so the claimed
center bit is 1 for every n.  Rule 30's center bit is 0 at n=2.
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from center_column import center_column


Matrix = tuple[tuple[int, int], tuple[int, int]]
KNOWN_PREFIX = b"11011100110001011001001110101110"
DEFAULT_TARGETS = (1, 2, 3, 4, 5, 31, 64, 511, 1000, 4045, 8113, 10000)


def poly_multiply(left: int, right: int, degree_bound: int) -> int:
    mask = (1 << degree_bound) - 1
    product = 0
    while right:
        low_bit = right & -right
        product ^= left << (low_bit.bit_length() - 1)
        right ^= low_bit
    return product & mask


def matrix_multiply(left: Matrix, right: Matrix, degree_bound: int) -> Matrix:
    def entry(row: int, column: int) -> int:
        return poly_multiply(left[row][0], right[0][column], degree_bound) ^ poly_multiply(
            left[row][1], right[1][column], degree_bound
        )

    return ((entry(0, 0), entry(0, 1)), (entry(1, 0), entry(1, 1)))


def candidate_center(n: int) -> int:
    if n < 1:
        raise ValueError("the proposed bit-decomposition contract only defines n >= 1")
    bit_length = n.bit_length()
    degree_bound = 2 * bit_length**2
    one = 1
    z = 2
    zero_matrix: Matrix = ((one ^ z, z), (z, one))
    one_matrix: Matrix = ((one ^ z, one ^ z), (z, one ^ z))
    accumulator: Matrix = ((one, 0), (0, one))

    for bit_index in range(bit_length):
        block = one_matrix if (n >> bit_index) & 1 else zero_matrix
        accumulator = matrix_multiply(accumulator, block, degree_bound)
        one_matrix = matrix_multiply(one_matrix, zero_matrix, degree_bound)
        zero_matrix = matrix_multiply(zero_matrix, zero_matrix, degree_bound)

    # e1.T * accumulator * e1 is entry (0, 0); evaluating at z=0 is
    # extraction of polynomial bit zero.
    return accumulator[0][0] & 1


def probe(targets: Sequence[int]) -> list[tuple[int, int, int]]:
    if not targets or min(targets) < 1:
        raise ValueError("targets must contain positive n")
    truth = center_column(max(max(targets) + 1, len(KNOWN_PREFIX)))
    observed_prefix = bytes(ord("1") if bit else ord("0") for bit in truth[: len(KNOWN_PREFIX)])
    assert observed_prefix == KNOWN_PREFIX, "Rule 30 ground-truth prefix mismatch"
    return [(n, candidate_center(n), truth[n]) for n in targets]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("n", nargs="*", type=int, default=list(DEFAULT_TARGETS))
    args = parser.parse_args()
    rows = probe(args.n)

    print("n candidate ground_truth match")
    for n, candidate, truth in rows:
        print(f"{n:5d} {candidate:9d} {truth:12d} {candidate == truth}")
    mismatches = [(n, candidate, truth) for n, candidate, truth in rows if candidate != truth]
    if mismatches:
        n, candidate, truth = mismatches[0]
        print(f"KILL: first mismatch at n={n}: candidate={candidate}, ground_truth={truth}")
        raise SystemExit(1)
    print("SURVIVED: no mismatch on supplied targets")


if __name__ == "__main__":
    main()

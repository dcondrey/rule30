"""Falsify the only executable contract from the bounded ARM8 Crosstalk run.

The candidate stores a polynomial p in GF(2)[x]/(x^k) and a parity bit q,
squares p for doubling, and derives a correction vector alpha from only k
initial rows.  The functions below preserve the submitted pseudocode so its
first disagreement with the independent bit-parallel oracle is reproducible.
"""

from __future__ import annotations

import argparse

from support_state_probe import RULE_30, eca_rows


def gf2_poly_square_mod(polynomial: int, width: int) -> int:
    result = 0
    for index in range(width):
        if (polynomial >> index) & 1:
            exponent = 2 * index
            if exponent < width:
                result ^= 1 << exponent
    return result


def correction_coefficients(width: int) -> int:
    row_width = 2 * width + 3
    center = width + 1
    row = [0] * row_width
    row[center] = 1
    alpha = 0
    for time in range(1, width + 1):
        row = [0] + [
            row[index - 1] ^ (row[index] | row[index + 1])
            for index in range(1, row_width - 1)
        ] + [0]
        alpha |= row[center - time] << (time - 1)
    return alpha


def compose(state: tuple[int, int], width: int, alpha: int) -> tuple[int, int]:
    polynomial, parity = state
    squared = gf2_poly_square_mod(polynomial, width)
    correction = (polynomial & alpha).bit_count() & 1
    return squared, parity ^ correction


def candidate_center_bit(index: int) -> int:
    if index < 1:
        raise ValueError("the submitted contract begins at n=1")
    width = index.bit_length() + 2
    alpha = correction_coefficients(width)
    digits: list[int] = []
    remaining = index
    while remaining > 1:
        digits.append(remaining & 1)
        remaining >>= 1
    state = (1, 1)
    for digit in reversed(digits):
        state = compose(state, width, alpha)
        if digit:
            polynomial, parity = state
            next_polynomial = (polynomial >> 1) | (
                (polynomial & alpha & 1) << (width - 1)
            )
            next_parity = parity ^ (polynomial & 1)
            state = next_polynomial & ((1 << width) - 1), next_parity & 1
    return state[1] & 1


def oracle_center_bits(max_index: int) -> list[int]:
    center = max_index + 1
    return [(row >> center) & 1 for row in eca_rows(RULE_30, max_index)]


def first_mismatch(max_index: int) -> tuple[int, int, int] | None:
    oracle = oracle_center_bits(max_index)
    for index in range(1, max_index + 1):
        candidate = candidate_center_bit(index)
        if candidate != oracle[index]:
            return index, candidate, oracle[index]
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-index", type=int, default=4096)
    args = parser.parse_args()
    if args.max_index < 1:
        parser.error("max-index must be positive")
    mismatch = first_mismatch(args.max_index)
    if mismatch is None:
        print(f"first_mismatch=None checked=1..{args.max_index}")
    else:
        index, candidate, oracle = mismatch
        print(f"first_mismatch={index} candidate={candidate} oracle={oracle}")


if __name__ == "__main__":
    main()

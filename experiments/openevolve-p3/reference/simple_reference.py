"""
Dead-simple, obviously-correct Rule 30 center-column simulator.

THIS FILE IS THE GROUND-TRUTH AUTHORITY. It is never touched by evolution
and never optimized. It exists to be trivially readable and checked by eye
against Wolfram's definition:

    cell(t+1, i) = cell(t, i-1) XOR ( cell(t, i) OR cell(t, i+1) )

starting from a single 1 cell on an infinite background of 0s. c(n) is the
value of the cell directly above the seed after n steps (the "center
column").

Deliberately plain Python, list of ints, no bit tricks, no numpy. O(n^2)
time and O(n) space per row. Only used for n in the low thousands (see
generate_ground_truth.py) -- large-n ground truth is produced by
bigint_reference.py, which is cross-validated against this file.
"""
from __future__ import annotations


def _step(row: list[int]) -> list[int]:
    """Apply one Rule 30 step to a row with implicit 0 boundary."""
    width = len(row)
    new_row = [0] * width
    for i in range(width):
        left = row[i - 1] if i - 1 >= 0 else 0
        mid = row[i]
        right = row[i + 1] if i + 1 < width else 0
        new_row[i] = left ^ (mid | right)
    return new_row


def center_column(n_max: int) -> list[int]:
    """Return [c(0), c(1), ..., c(n_max)] for the single-cell Rule 30 seed.

    The activated light cone after n steps has radius <= n from the seed,
    so a row of width 2*n_max + 3 with the seed centered never touches its
    (implicit-zero) boundary and the simulation is exact.
    """
    if n_max < 0:
        raise ValueError("n_max must be >= 0")
    width = 2 * n_max + 3
    center = width // 2
    row = [0] * width
    row[center] = 1
    out = [row[center]]
    for _ in range(n_max):
        row = _step(row)
        out.append(row[center])
    return out


def center_cell(n: int) -> int:
    """Single-value convenience wrapper (recomputes from scratch -- slow)."""
    return center_column(n)[-1]


if __name__ == "__main__":
    # Sanity print: first 20 terms should match Wolfram's published sequence
    # 1,1,1,0,1,1,0,1,1,1,0,0,0,0,1,0,0,1,1,0,... (OEIS A051023 partial match
    # for the well-known Rule 30 center column, printed for a human to eyeball).
    print(center_column(20))

"""
Fast (but still exact) Rule 30 center-column simulator, used only to extend
ground truth beyond what simple_reference.py can practically compute, and as
the "constant-factor-faster, same-exponent" sanity-test candidate for the
evaluator.

Encodes an entire row as the bits of a single Python integer and implements
the Rule 30 update with bitwise ops:

    new = left XOR (mid OR right)
        = (row << 1) XOR (row OR (row >> 1))

(left-shift moves the row one position "left" in index space -- i.e. cell
i-1's value lands under position i -- and right-shift does the symmetric
thing for the right neighbor; see _step for the precise bit convention.)

This is still O(n) big-integer word operations per step, i.e. O(n^2 / w) for
w-bit words -- the SAME asymptotic exponent as simple_reference.py, just a
much better constant (CPython's bignum arithmetic is implemented in C).
It must never be reported as a P3 result on its own; it is a constant-factor
optimization, not an algorithmic shortcut. It is cross-validated against
simple_reference.py in test_reference.py before being trusted for anything.
"""
from __future__ import annotations


def center_column(n_max: int) -> list[int]:
    if n_max < 0:
        raise ValueError("n_max must be >= 0")
    width = 2 * n_max + 3
    center_bit = width // 2  # bit index of the seed / center column, MSB-first convention below

    # Represent the row as an integer with `width` bits; bit position k
    # (from the left, i.e. bit (width-1-k) in Python's integer, so that
    # left-shift-by-one-bit-position corresponds to shifting the spatial
    # pattern towards increasing index) -- to keep this simple we instead
    # just store the row LSB = rightmost cell, and use the standard
    # left_neighbor = row >> 1 (shifts bits towards lower index positions
    # i.e. towards the LSB end representing higher spatial index)...
    #
    # To avoid any convention confusion (and the risk of an off-by-one that
    # would silently produce a WRONG but plausible sequence), we use the
    # simplest possible mapping and verify it exhaustively against
    # simple_reference.py for many n in test_reference.py:
    #
    #   bit i of the Python int  <->  row[i]  (row as in simple_reference.py)
    #   row[i-1] (the "left" spatial neighbor, lower index) <-> bit (i-1)
    #     -> obtained from `row_int` by a LEFT shift by 1 bit (<< 1), since
    #        that moves the value at bit (i-1) up into bit i.
    #   row[i+1] (the "right" spatial neighbor, higher index) <-> bit (i+1)
    #     -> obtained from `row_int` by a RIGHT shift by 1 bit (>> 1).
    mask = (1 << width) - 1
    row_int = 1 << center_bit

    out = [(row_int >> center_bit) & 1]
    for _ in range(n_max):
        left = (row_int << 1) & mask
        right = row_int >> 1
        row_int = (left ^ (row_int | right)) & mask
        out.append((row_int >> center_bit) & 1)
    return out


def center_cell(n: int) -> int:
    return center_column(n)[-1]


if __name__ == "__main__":
    print(center_column(20))

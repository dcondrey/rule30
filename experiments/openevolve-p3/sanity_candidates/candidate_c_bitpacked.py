"""Sanity candidate (c): correct, and a large CONSTANT-FACTOR speedup via
big-integer bit-packing (same technique as reference/bigint_reference.py),
but the SAME O(n^2) asymptotic exponent as direct simulation. Must be
recognized as fully correct, but must NOT score in the "exponent
improvement" band -- if the evaluator can't tell this apart from a real
algorithmic win, the evaluator is broken."""
def center_cell(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    width = 2 * n + 3
    center_bit = width // 2
    mask = (1 << width) - 1
    row = 1 << center_bit
    for _ in range(n):
        left = (row << 1) & mask
        right = row >> 1
        row = (left ^ (row | right)) & mask
    return (row >> center_bit) & 1

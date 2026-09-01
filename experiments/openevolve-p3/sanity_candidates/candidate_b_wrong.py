"""Sanity candidate (b): deliberately wrong (uses AND instead of OR in the
Rule 30 update rule). Must score exactly 0.0 -- this is the hard
correctness gate's negative-control test."""
def center_cell(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    width = 2 * n + 3
    center = width // 2
    row = [0] * width
    row[center] = 1
    if n == 0:
        return row[center]
    for _ in range(n):
        new_row = [0] * width
        for i in range(width):
            left = row[i - 1] if i - 1 >= 0 else 0
            mid = row[i]
            right = row[i + 1] if i + 1 < width else 0
            new_row[i] = left ^ (mid & right)  # BUG: should be OR, not AND
        row = new_row
    return row[center]

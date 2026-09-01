"""Sanity candidate (a): correct baseline, same algorithm as initial_program.py.
Should pass all correctness gates and score the flat ~0.2 credit (no
exponent improvement over itself)."""
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
            new_row[i] = left ^ (mid | right)
        row = new_row
    return row[center]

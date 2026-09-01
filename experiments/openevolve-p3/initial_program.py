"""
OpenEvolve seed program for the Rule 30 P3 task.

Wolfram's P3: is there a shortcut algorithm that computes c(n), the n-th
cell of the Rule 30 center column, asymptotically faster than direct
simulation (which requires ~n^2 cell updates because the light cone after n
steps has width ~2n)?

This file defines `center_cell(n) -> int`, computing c(n) for the standard
single 1-cell seed. Only the code inside the EVOLVE-BLOCK markers is subject
to mutation by OpenEvolve; the harness (evaluator.py, reference/*) is fixed
and never touched.

The seed here is the obvious baseline: direct cellular-automaton
simulation, one row at a time, using a Python list. It is deliberately NOT
optimized (no bit-packing, no numpy) so that any improvement OpenEvolve
finds -- whether a real algorithmic shortcut or "just" a faster constant --
is visible against a plain starting point. The evaluator's exponent fit
is what tells the two apart, not this file.
"""
# EVOLVE-BLOCK-START
def center_cell(n: int) -> int:
    """Return c(n): the value of the center cell after n Rule 30 steps
    from a single 1-cell seed on an infinite 0 background.

    Direct simulation baseline: O(n) rows, O(n) cells per row => O(n^2)
    total cell updates.
    """
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
# EVOLVE-BLOCK-END


if __name__ == "__main__":
    for n in [0, 1, 2, 3, 10, 100]:
        print(n, center_cell(n))

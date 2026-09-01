"""Sanity candidate (e): correct, wide-operand, and deliberately Theta(n^3).

Purpose is instrument calibration, NOT a plausible search candidate. Both
existing discriminating tests check the fuel instrument against a true exponent
of 2; this one checks it against a true exponent of 3, so that "the instrument
recovers the known exponent" is not a claim only ever tested at a single point.

Construction: bit-packed rows exactly as candidate (c), but the row is rebuilt
from the seed at every outer step instead of being carried forward. Cost is
    sum_{t=1..n} t * ceil(width / WORD_BITS),  width = 2n+3
which is Theta(n^3) under a word-RAM model and Theta(n^2) under a flat
per-operation count -- the two models disagree by a full exponent-unit, which is
what makes it discriminating.

The wasted work is real work on wide operands, not a sleep or a spin: every
inner step is the same bignum update candidate (c) performs.
"""
def center_cell(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    width = 2 * n + 3
    center_bit = width // 2
    mask = (1 << width) - 1

    row = 1 << center_bit
    for t in range(n):
        # Rebuild the row after t+1 steps, from the seed, every time.
        row = 1 << center_bit
        for _ in range(t + 1):
            left = (row << 1) & mask
            right = row >> 1
            row = (left ^ (row | right)) & mask

    return (row >> center_bit) & 1

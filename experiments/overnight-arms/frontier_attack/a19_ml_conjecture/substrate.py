"""a19 substrate: exact space-time windows around column 0, for Rule 30 and Rule 90.

Frame convention (matches experiments/overnight-arms/common/rule30.py):
    b_t(i) = s(t, i - t), so s(t, x) = bit (x + t) of b_t.
    Rule 30: b_{t+1} = (b_t << 2) XOR ((b_t << 1) OR b_t)
    Rule 90: b_{t+1} = (b_t << 2) XOR b_t

TRUNCATION LEMMA (used to keep this linear-ish instead of quadratic):
bit i of b_{t+1} depends only on bits i-2, i-1, i of b_t, i.e. only on indices
<= i.  So the set of low bits [0, M] is forward-closed: masking b_t to M+1 bits
after every step leaves bits [0, M] of every later row EXACT.  Since the window
around column 0 at time t occupies bits [t-W, t+W], masking at M = n + W is
lossless for all t < n.

Everything here is exact integer computation.  No approximation anywhere.

Self-test: uv run python substrate.py
"""

from __future__ import annotations

import numpy as np

RULES = ("30", "90")


def _step(row: int, rule: str) -> int:
    if rule == "30":
        return (row << 2) ^ ((row << 1) | row)
    if rule == "90":
        return (row << 2) ^ row
    raise ValueError(rule)


def windows(n: int, W: int, rule: str = "30") -> np.ndarray:
    """(n, 2W+1) uint8 array A with A[t, W + x] = s(t, x) for x in [-W, W].

    Rows t = 0 .. n-1.  Exact.
    """
    mask = (1 << (n + W + 4)) - 1
    span = 2 * W + 1
    wmask = (1 << span) - 1
    out = np.zeros((n, span), dtype=np.uint8)
    row = 1
    nbytes = (span + 7) // 8
    for t in range(n):
        lo = t - W
        if lo >= 0:
            w = (row >> lo) & wmask
        else:
            w = (row & ((1 << (t + W + 1)) - 1)) << (-lo)
        buf = np.frombuffer(w.to_bytes(nbytes, "little"), dtype=np.uint8)
        out[t] = np.unpackbits(buf, bitorder="little")[:span]
        row = _step(row, rule) & mask
    return out


def center_column(n: int, rule: str = "30") -> np.ndarray:
    """s(t, 0) for t = 0 .. n-1, uint8."""
    mask = (1 << (n + 4)) - 1
    out = np.zeros(n, dtype=np.uint8)
    row = 1
    for t in range(n):
        out[t] = (row >> t) & 1
        row = _step(row, rule) & mask
    return out


def _selftest() -> None:
    import importlib.util
    import sys

    sys.path.insert(
        0, "/Volumes/A/researchpapers/13-rule30/experiments/overnight-arms/common"
    )
    from rule30 import center_column_bits, simulate_seed  # type: ignore

    n, W = 3000, 12
    A = windows(n, W, "30")
    c = center_column(n, "30")
    truth = center_column_bits(n)
    assert list(c) == truth, "center column disagrees with shared substrate"
    assert list(A[:, W]) == truth, "window centre column disagrees"

    # Independent naive simulator over the full window, 400 rows.
    grid = simulate_seed({0: 1}, 400)
    for t in range(400):
        for x in range(-W, W + 1):
            assert A[t, W + x] == grid[t].get(x, 0), (t, x)

    # Rule 30 local law holds inside the window (interior columns).
    B = A.astype(int)
    lhs = B[1:, 1 : 2 * W]
    rhs = B[:-1, 0 : 2 * W - 1] ^ (B[:-1, 1 : 2 * W] | B[:-1, 2 : 2 * W + 1])
    assert (lhs == rhs).all(), "rule 30 local law violated in window"

    # Rule 90 control: centre column is 1 then 0 forever.
    c90 = center_column(n, "90")
    assert c90[0] == 1 and c90[1:].sum() == 0, "rule 90 centre column not trivial"

    # Truncation lemma regression: masking must not change any low bit.
    small = windows(600, W, "30")
    assert (small == A[:600]).all(), "truncation changed low bits"

    print(f"OK substrate: n={n} W={W}; rule30 centre matches A051023; "
          f"local law exact; rule90 centre = 1 then zeros")


if __name__ == "__main__":
    _selftest()

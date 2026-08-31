"""Right-cone diagonals of Rule 30 as purely periodic sequences.

Index a finite row `a` with right endpoint `B` by its right-cone diagonals
`E_j[t] = s(t, B + t - j)`, so `E_j[0] = a(B-j)` and `E_j == 0` for `j < 0`.
The Rule 30 recursion becomes

    E_j[t] = E_j[t-1] XOR (E_{j-1}[t-1] OR E_{j-2}[t-1]),

which makes `E_j` the running parity of the OR of the two diagonals above it.
Running parity is computable on a whole time range at once by the standard
doubling trick, so `E_j` out to time `T` costs `O(log T)` bigint operations
rather than `O(T)` cell updates.

**Known result, re-derived, not new.**  That the Rule 30 diagonals on the
regular side are periodic with power-of-two periods doubling at irregular
intervals is published; `docs/rule30/RESULTS-diagonal-periodicity.md` records
the citation and the first thirty published terms, which
`test_diagonal_period_probe.py` reproduces.  Treat this module as validation
plus an exact period oracle, not as a discovery.

The center column is `c_t = E_{t+B}[t]`: it reads diagonal `t+B` at time `t`.
"""

from __future__ import annotations

import argparse
import json


def prefix_parity(g: int, nbits: int) -> int:
    """Bit ``t`` of the result is the XOR of bits ``0..t`` of ``g``."""
    p = g
    sh = 1
    while sh < nbits:
        p ^= p << sh
        sh <<= 1
    return p & ((1 << nbits) - 1)


def from_cells(cells: frozenset[int]) -> tuple[dict[int, int], int]:
    """``(a_left, B)`` with ``a_left[j] = a(B-j)`` for a nonempty finite row."""
    b = max(cells)
    return {j: (1 if (b - j) in cells else 0) for j in range(0, b - min(cells) + 1)}, b


def diagonals(a_left: dict[int, int], jmax: int, horizon: int) -> list[int]:
    """``E_j`` for ``j=0..jmax`` as ints over ``t=0..horizon``."""
    nb = horizon + 1
    ones = (1 << nb) - 1
    d2 = d1 = 0
    out = []
    for j in range(jmax + 1):
        g = ((d1 | d2) << 1) & ones
        d = prefix_parity(g, nb) ^ (ones if a_left.get(j, 0) else 0)
        out.append(d)
        d2, d1 = d1, d
    return out


def _tile(pat: int, q: int, target: int) -> int:
    out, n = pat, q
    while n < target:
        out |= out << n
        n <<= 1
    return out & ((1 << target) - 1)


def diagonal_patterns(a_left: dict[int, int], jmax: int) -> list[tuple[int, int]]:
    """``(Q_j, pattern)`` for ``j=0..jmax``: the exact period and one period of it.

    Exact because each diagonal is purely periodic: the OR of the two diagonals
    above it is purely periodic with period ``q = max(Q_{j-1}, Q_{j-2})``, and a
    running parity of a purely periodic sequence is purely periodic with period
    ``q`` when the sequence has even weight over a period and ``2q`` when odd.
    """
    q2 = q1 = 1
    p2 = p1 = 0
    out = []
    for j in range(jmax + 1):
        q = max(q1, q2)
        a = _tile(p1, q1, q) | _tile(p2, q2, q)
        if a.bit_count() % 2:
            q *= 2
            a = _tile(a, q // 2, q)
        mask = (1 << q) - 1
        run = prefix_parity(a, q)
        pat = ((run << 1) & mask) ^ (mask if a_left.get(j, 0) else 0)
        out.append((q, pat))
        q2, p2, q1, p1 = q1, p1, q, pat
    return out


def diagonal_periods(a_left: dict[int, int], jmax: int) -> list[int]:
    return [q for q, _ in diagonal_patterns(a_left, jmax)]


def center_column(a_left: dict[int, int], b: int, n: int) -> list[int]:
    """``c_0..c_n`` read off the diagonals, ``c_t = E_{t+b}[t]``."""
    ds = diagonals(a_left, n + b, n)
    return [(ds[t + b] >> t) & 1 for t in range(n + 1)]


def regular_width(periods: list[int], t: int) -> int:
    """How many diagonals have completed a period by time ``t``."""
    return sum(1 for q in periods if q <= t)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jmax", type=int, default=64)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    periods = diagonal_periods({0: 1}, args.jmax)
    if args.json:
        print(json.dumps({
            "seed": [0],
            "periods": periods,
            "log2_periods": [q.bit_length() - 1 for q in periods],
            "regular_width": {str(1 << e): regular_width(periods, 1 << e)
                              for e in range(0, 28, 2)},
        }, indent=2))
        return
    print("  j      Q_j  log2  Q_j>j")
    for j, q in enumerate(periods):
        print("%3d %8d %5d  %s" % (j, q, q.bit_length() - 1, q > j))
    print()
    print("regular width (diagonals with a completed period) by time t:")
    for e in range(0, 28, 2):
        print("  t=2^%-2d  width %d" % (e, regular_width(periods, 1 << e)))


if __name__ == "__main__":
    main()

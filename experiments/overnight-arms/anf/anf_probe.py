"""anf arm, cheapest disconfirming test (PREREG-anf.md).

Exact ANF of f_t (center bit at time t as a function of the 2t+1 light-cone cells)
for t = 1..8. Gates:
  - replicate ARM4 SS3 table exactly (deg, terms) at t = 1,3,5,7  [validation]
  - Rule 90 control: deg = 1 at every t                           [control]
  - probe L1 (linear in leftmost var), L2 (top-two degrees vacant),
    L3 (structure of the degree-(2t-1) monomial set)               [questions]
Run: uv run python experiments/overnight-arms/anf/anf_probe.py
"""

from __future__ import annotations

import logging

import numpy as np

log = logging.getLogger(__name__)


def truth_table(t: int, rule30: bool = True) -> np.ndarray:
    """Truth table of f_t over 2^(2t+1) inputs; variable i is cell i - t."""
    n = 2 * t + 1
    idx = np.arange(1 << n, dtype=np.uint32)
    cells = [((idx >> i) & 1).astype(np.uint8) for i in range(n)]
    for _step in range(t):
        nxt = []
        for j in range(1, len(cells) - 1):
            left, c, r = cells[j - 1], cells[j], cells[j + 1]
            nxt.append(left ^ (c | r) if rule30 else left ^ r)  # rule 90: l^r
        cells = nxt
    assert len(cells) == 1
    return cells[0]


def mobius(tt: np.ndarray) -> np.ndarray:
    """In-place GF(2) Moebius transform: truth table -> ANF coefficients."""
    a = tt.copy()
    n = a.size.bit_length() - 1
    for i in range(n):
        step = 1 << i
        for base in range(0, a.size, step << 1):
            a[base + step : base + (step << 1)] ^= a[base : base + step]
    return a


def popcounts(m: int) -> np.ndarray:
    idx = np.arange(1 << m, dtype=np.uint32)
    pc = np.zeros(1 << m, dtype=np.uint8)
    for i in range(m):
        pc += ((idx >> i) & 1).astype(np.uint8)
    return pc


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    arm4 = {1: (2, 4), 3: (5, 30), 5: (9, 346), 7: (13, 4852)}
    for t in range(1, 9):
        n = 2 * t + 1
        tt = truth_table(t)
        anf = mobius(tt)
        pc = popcounts(n)
        deg = int(pc[anf == 1].max())
        terms = int(anf.sum())
        # L1: linear in leftmost variable (index 0 = cell -t)?
        flipped = tt.reshape(-1, 2)[:, ::-1].reshape(-1)  # flip bit 0
        l1 = bool(np.all(tt ^ flipped == 1))
        # L2: coefficients at degree 2t+1 and 2t all zero?
        l2 = bool(np.all(anf[pc >= 2 * t] == 0))
        # L3: degree-(2t-1) monomials = complements of pairs {i,j}; list the pairs.
        top = np.flatnonzero((anf == 1) & (pc == 2 * t - 1))
        full = (1 << n) - 1
        pairs = sorted(
            tuple(i for i in range(n) if not (m >> i) & 1) for m in map(int, top)
        )
        g90 = mobius(truth_table(t, rule30=False))
        deg90 = int(popcounts(n)[g90 == 1].max())
        ok = "" if t not in arm4 else ("  ARM4-match" if (deg, terms) == arm4[t] else "  ARM4-MISMATCH!")
        log.info(
            "t=%2d deg=%2d terms=%6d L1=%s L2=%s r90deg=%d%s", t, deg, terms, l1, l2, deg90, ok
        )
        log.info("   top-degree missing-pairs (%d): %s", len(pairs), pairs)


if __name__ == "__main__":
    main()

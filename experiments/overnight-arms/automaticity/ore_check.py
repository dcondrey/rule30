"""Independent check of the Ore/Frobenius reduction ladder for A051023.

A relation of order n, height d is P_{-1}(x) + sum_{i=0}^{n} P_i(x)*F(x^(2^i)) = 0 in F_2[[x]],
with all P of degree <= d, not all zero. Over F_2, F(x)^(2^i) = F(x^(2^i)).

Coefficient of x^m contributed by unknown P_i[j] is a((m-j)/2^i) when 2^i | (m-j), else 0;
for the inhomogeneous term P_{-1}[j] it is [j == m].

S(0) is exactly "not eventually periodic" = Wolfram P1.
Nullity 0 at (n,d) for a single N proves no exact relation of order <= n, height <= d exists
(a real relation would satisfy every truncation). One-sided and monotone in N.

Calibration targets (must FIND relations): Thue-Morse at (1,3); Rule 90 center column at (0,0).

Run: uv run python experiments/overnight-arms/automaticity/ore_check.py
"""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)


def rule_column(rule: str, n: int) -> list[int]:
    row = 1
    out = []
    for t in range(n):
        out.append((row >> t) & 1)
        row = (row << 2) ^ ((row << 1) | row) if rule == "30" else (row << 2) ^ row
    return out


def thue_morse(n: int) -> list[int]:
    return [bin(t).count("1") & 1 for t in range(n)]


def nullity(seq: list[int], n_ord: int, d: int, N: int) -> int:
    """dim of nullspace of the truncated relation system, over F_2, via bitset elimination."""
    cols = []  # each unknown -> column as an int bitmask over rows m=0..N-1
    # inhomogeneous P_{-1}[j]
    for j in range(d + 1):
        cols.append(1 << j if j < N else 0)
    # P_i[j] for i = 0..n_ord
    for i in range(n_ord + 1):
        step = 1 << i
        for j in range(d + 1):
            v = 0
            for m in range(j, N):
                r = m - j
                if r % step == 0:
                    idx = r // step
                    if idx < len(seq) and seq[idx]:
                        v |= 1 << m
            cols.append(v)
    # Gaussian elimination on columns: count pivots
    pivots = []
    rank = 0
    for c in cols:
        cur = c
        for p in pivots:
            low = p & -p
            if cur & low:
                cur ^= p
        if cur:
            pivots.append(cur)
            rank += 1
    return len(cols) - rank


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    log.info("== calibration (relations MUST be found) ==")
    tm = thue_morse(4000)
    for d in (2, 3):
        nl = nullity(tm, 1, d, 4 * 2 * (d + 1) + 60)
        log.info("Thue-Morse (n=1,d=%d): nullity=%d %s", d, nl, "FOUND" if nl else "none")
    r90 = rule_column("90", 4000)
    nl = nullity(r90, 0, 0, 200)
    log.info("Rule 90 center (n=0,d=0): nullity=%d %s", nl, "FOUND" if nl else "none")
    nl = nullity(r90, 1, 5, 400)
    log.info("Rule 90 center (n=1,d=5): nullity=%d %s", nl, "FOUND" if nl else "none")

    log.info("== Rule 30 center column A051023 ==")
    r30 = rule_column("30", 40000)
    assert "".join(map(str, r30[:16])) == "1101110011000101", "ground-truth prefix mismatch"
    for n_ord, ds in ((0, (50, 200, 800)), (1, (20, 60, 120)), (2, (20, 40)), (3, (20,))):
        for d in ds:
            N = min(4 * (n_ord + 2) * (d + 1) + 200, 39000)
            nl = nullity(r30, n_ord, d, N)
            log.info(
                "Rule 30 (n=%d,d=%4d,N=%5d): nullity=%d %s",
                n_ord, d, N, nl, "RELATION EXISTS" if nl else "none -> S(n,d) certified",
            )


if __name__ == "__main__":
    main()

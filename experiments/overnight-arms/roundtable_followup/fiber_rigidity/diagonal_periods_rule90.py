"""Check whether Rule 90's right-cone diagonals are exactly periodic, the way
Rowland proved for Rule 30 (RESULTS-diagonal-periodicity.md).  Rowland's
Lemma 2 needs only that the rule be "right bijective" (bijective in the third
argument for fixed first two); f_90(a,b,c)=a XOR c qualifies exactly as
f_30(a,b,c)=a XOR (b OR c) does, so the theorem should be generic and this
should come out periodic for Rule 90 too.  Checked directly rather than
assumed, because this is exactly what pins down whether "asymptotic phase
forced near the boundary" can be a Rule-30-specific fact.
"""
from __future__ import annotations

from edge_periodicity_probe import evolve_lone_seed


def diagonal_periods(rule: int, steps: int, jmax: int) -> list[int | None]:
    rows = evolve_lone_seed(rule, steps)
    center = steps
    periods: list[int | None] = []
    for j in range(jmax + 1):
        seq = []
        for t in range(steps + 1):
            x = t - j  # right-cone diagonal E_j[t] = s(t, t-j), B=0
            idx = center + x
            seq.append(rows[t][idx] if 0 <= idx < len(rows[t]) else 0)
        n = len(seq)
        found = None
        for p in range(1, n):
            if all(seq[i] == seq[i - p] for i in range(p, n)):
                found = p
                break
        periods.append(found)
    return periods


def main() -> None:
    print("rule 30 diagonal periods j=0..20:", diagonal_periods(30, 300, 20))
    print("rule 90 diagonal periods j=0..20:", diagonal_periods(90, 300, 20))


if __name__ == "__main__":
    main()

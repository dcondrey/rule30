"""a21 helper: read phi_epsilon_results.json and show where err(m,t) stabilises
in t.  Theorem S predicts stabilisation for t >= 2m+1.

Usage: uv run python eps_stability.py > eps_stability.txt
"""

from __future__ import annotations

import json


def main() -> None:
    d = json.load(open("phi_epsilon_results.json"))["30"]
    ts = sorted(int(k) for k in d)
    print("rule 30: err(m,t) as t grows, per m  (looking for stabilisation)")
    print("Theorem S predicts err(m,t) constant for t >= 2m+1.")
    for m in range(1, 16):
        row = [(t, d[str(t)][m]) for t in ts if m <= t]
        tail = [f"{t}:{v:.6f}" for t, v in row[-8:]]
        stable = (
            len(row) >= 3
            and abs(row[-1][1] - row[-2][1]) < 1e-9
            and abs(row[-2][1] - row[-3][1]) < 1e-9
        )
        first = next(
            (
                t
                for i, (t, v) in enumerate(row)
                if all(abs(v2 - v) < 1e-12 for _, v2 in row[i:])
            ),
            None,
        )
        print(
            f" m={m:2d} stable={stable}  first constant t={first} (2m+1={2*m+1})  "
            + "  ".join(tail)
        )


if __name__ == "__main__":
    main()

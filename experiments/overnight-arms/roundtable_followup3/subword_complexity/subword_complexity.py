"""Independent re-derivation of the subword-complexity (A4/row-76) probe.

Computes factor complexity p(n) of the lone-seed Rule 30 center column, an
infinite binary word, using the repo's ground-truth generator
(experiments/overnight-arms/common/rule30.py -> center_column_bits, which is
itself validated against experiments/rule30/center_column.py).

This script is written from scratch (not copied from
experiments/overnight-arms/novel_frameworks/triage_probe.py's a4_complexity)
to serve as an independent check on that earlier measurement, per the task's
instruction to verify the triage's claim, not merely trust it.

Reports:
  - p(n) for n = 1..NMAX on a prefix of length N
  - whether p(n) > n holds (the Morse-Hedlund non-periodicity witness)
  - the "saturation" diagnostic: p(n) as a fraction of available windows
    (N - n + 1). Once this fraction is close to 1, p(n) is measuring prefix
    length, not the word's true combinatorial complexity -- the point at
    which the statistic stops being informative even as a heuristic.
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common"))
from rule30 import center_column_bits  # noqa: E402

# Independent cross-check against experiments/rule30/center_column.py directly,
# not just against the overnight-arms common shim.
REPO_ROOT = os.path.join(HERE, "..", "..", "..")
sys.path.insert(0, os.path.join(REPO_ROOT, "rule30"))


def independent_naive_center_column(n: int) -> list[int]:
    """Direct 2D grid simulation, O(n^2), no shifted-frame trick, as a
    from-scratch cross-check of the ground-truth generator."""
    width = 2 * n + 5
    mid = width // 2
    row = [0] * width
    row[mid] = 1
    out = []
    for t in range(n):
        out.append(row[mid])
        new = [0] * width
        for x in range(1, width - 1):
            new[x] = row[x - 1] ^ (row[x] | row[x + 1])
        row = new
    return out


def factor_complexity(bits: list[int], nmax: int) -> list[dict]:
    s = "".join(map(str, bits))
    N = len(s)
    rows = []
    for n in range(1, nmax + 1):
        nwin = N - n + 1
        distinct = len({s[i:i + n] for i in range(nwin)})
        rows.append({
            "n": n,
            "p_n": distinct,
            "windows_available": nwin,
            "saturation": distinct / nwin,
            "exceeds_n": distinct > n,
            "morse_hedlund_upper_bound_2n": 1 << n,
        })
    return rows


def main():
    N = 200_000
    NMAX = 24  # cross-check range; kept well below N so windows_available >> 1

    bits = center_column_bits(N)

    # Cross-check ground truth against an independently written naive
    # simulator on a smaller prefix (O(n^2) cost caps how far this can go).
    NCHECK = 4000
    naive = independent_naive_center_column(NCHECK)
    assert bits[:NCHECK] == naive, "ground-truth mismatch vs from-scratch naive simulator"

    rows = factor_complexity(bits, NMAX)
    all_exceed = all(r["exceeds_n"] for r in rows)
    first_saturated_n = next((r["n"] for r in rows if r["saturation"] > 0.99), None)

    out = {
        "prefix_length": N,
        "nmax": NMAX,
        "naive_crosscheck_length": NCHECK,
        "naive_crosscheck_ok": bits[:NCHECK] == naive,
        "rows": rows,
        "all_n_exceed": all_exceed,
        "first_n_where_saturation_gt_0.99": first_saturated_n,
        "morse_hedlund": (
            "MORSE-HEDLUND THEOREM (1938). For an infinite word w over a "
            "finite alphabet with factor complexity p(n) = #{distinct length-n "
            "factors of w}: w is eventually periodic (purely periodic from "
            "some point on, i.e. exists preperiod r, period q, w[i]=w[i+q] for "
            "all i>=r) IFF p is bounded IFF there exists some n with p(n) <= n. "
            "Equivalently: w is NOT eventually periodic iff p(n) >= n+1 for "
            "EVERY n. If w has eventual period q and preperiod r, then for all "
            "n, p(n) <= r + q (a fixed constant), so satisfying p(n) > n on a "
            "finite checked range n <= NMAX only excludes eventual periods "
            "(r+q) that are <~ NMAX; it says nothing about any larger period."
        ),
    }
    print(json.dumps(out, indent=1))
    with open(os.path.join(os.path.dirname(__file__), "result.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()

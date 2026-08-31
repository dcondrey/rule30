"""Close gap 2, deeper layer: the K=2e6 ensemble run (ensemble_control.py,
ensemble_control_zeroset.py) shows test_err SIGNIFICANTLY ABOVE eps_30(m)
for m=12,14,16, with the deviation getting WORSE (not better) at K=2e6 than
K=1e6 -- backwards from what majority-vote consistency predicts as sample
size grows. a21's own eps_theorem.py cross-checks eps(m) against direct
enumeration only for t < 22, i.e. m <= 10 (2*11+1=23 > 22, so the check
silently no-ops for m >= 11). So eps_30(12), eps_30(14), eps_30(16) --
the exact values this whole arm and PATH.md 9.4 cite -- were NEVER
independently verified for m >= 11.

This script is a DELIBERATELY DIFFERENT implementation of eps(m): explicit
numpy boolean-array simulation over all 2^(m+1) hidden states for each of
2^m windows, rather than eps_theorem.py's big-int bitmask packing. Same
math, different code path, to catch an implementation bug rather than
re-deriving the same bug twice.

Usage: uv run python independent_eps_check.py [mmax] > independent_eps_check_output.txt
"""

from __future__ import annotations

import sys

import numpy as np


def eps_independent(m: int) -> tuple[int, int]:
    """Exact eps(m) for Rule 30, via explicit array simulation.

    row state: array of shape (2**(m+1),) bool, position i represents
    s(t-m, 1+i) for i=0..m, over all 2**(m+1) equally likely hidden
    assignments (enumerated as the bits of the array's own index -- i.e.
    hidden state h in [0, 2**(m+1)) has s(t-m,1+i) = bit i of h).
    """
    nh = m + 1
    size = 1 << nh
    idx = np.arange(size, dtype=np.uint32)
    row = np.stack([((idx >> i) & 1).astype(bool) for i in range(nh)], axis=0)
    # row.shape = (nh, size); row[i, h] = s(t-m, 1+i) for hidden assignment h

    total_err = 0
    for g in range(1 << m):
        cur = row.copy()
        for j in range(m):
            gj = bool((g >> j) & 1)
            new_rows = []
            for i in range(cur.shape[0] - 1):
                left = np.full(size, gj) if i == 0 else cur[i - 1]
                new_rows.append(left ^ (cur[i] | cur[i + 1]))
            cur = np.stack(new_rows, axis=0)
        assert cur.shape[0] == 1
        ones = int(cur[0].sum())
        total_err += min(ones, size - ones)
    return total_err, 1 << (2 * m + 1)


def main() -> None:
    mmax = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    print("a22 / independent_eps_check.py -- independent re-derivation of "
          "eps_30(m), array-based, not the bitmask-packing method\n")
    # values from a21's eps_theorem_results.json / r1_direct_attempt.md,
    # copied verbatim for comparison (NOT imported/trusted as code)
    EPS30_NUM = [
        2, 8, 28, 112, 416, 1644, 6280, 24612,
        95840, 380412, 1507680, 5969532, 23733628, 94203568, 374847204, 1488690544,
    ]
    a21_claimed = {m: EPS30_NUM[m - 1] / (2 ** (2 * m + 1)) for m in range(1, 17)}

    print(f"{'m':>3} {'a21 claimed':>14} {'independent':>14} {'match?':>8}")
    for m in range(1, mmax + 1):
        num, den = eps_independent(m)
        val = num / den
        claimed = a21_claimed[m]
        match = "MATCH" if abs(val - claimed) < 1e-12 else "MISMATCH"
        print(f"{m:3d} {claimed:14.9f} {val:14.9f} {match:>8}   ({num}/{den})")
        sys.stdout.flush()


if __name__ == "__main__":
    main()

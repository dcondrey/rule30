"""The preimage structure ON THE LONE-SEED ORBIT is a chain, demonstrated.

For each t in [0, T), take the true row s(t+1, .) of the lone-seed diagram and
recover s(t, .) using nothing but:

  * the support endpoints, which are read off the image (a finite-support row
    with leftmost 1 at L and rightmost 1 at R has image with leftmost 1 at L-1
    and rightmost 1 at R+1), and
  * left permutivity, peeled leftward:
        x[i-1] = y[i] XOR (x[i] OR x[i+1]),
    seeded by x[j] = 0 for all j > R.

There is no branch anywhere in this: the two "free" boundary cells of the
general free-boundary preimage (which number exactly 4, see
preimage_structure.py claim 1) are both pinned to 0 by finite support.  So the
backward orbit of the lone seed is a chain and carries no tree to descend.

The peel step IS the repo's OR-latch pin: PATH.md section 1 states
s(t,x)=1 => s(t,x-1) = NOT s(t+1,x), which is the x[i]=1 case of the same
equation, and experiments/rule30/inverse_trace_probe.py:135-160 already
implements the rotation.  Nothing here is new mechanism; the point is that
"preimage structure" and "the pin" are the same object.

Reference rows come from the shared substrate rows_frame().
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "common"))
from rule30 import cell, rows_frame  # noqa: E402


def row_dict(bf, t, lo, hi):
    return {x: cell(bf, t, x) for x in range(lo, hi + 1)}


def peel_back(y, R):
    """Recover x from y = F30(x) given that x is supported in (-inf, R].
    Returns dict over the same index range as y."""
    lo = min(y) - 1
    x = {}
    for i in range(R + 1, R + 3):
        x[i] = 0
    # peel: iterate i downward, writing x[i-1] = y[i] XOR (x[i] OR x[i+1])
    for i in range(R + 1, lo, -1):
        yi = y.get(i, 0)
        x[i - 1] = yi ^ (x.get(i, 0) | x.get(i + 1, 0))
    return x


def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    rows = rows_frame(T + 2)
    lo, hi = -(T + 3), T + 3
    mismatches = []
    pin_checks = 0
    pin_violations = 0
    for t in range(T):
        true_x = row_dict(rows[t], t, lo, hi)
        y = row_dict(rows[t + 1], t + 1, lo, hi)
        ones = [i for i in true_x if true_x[i]]
        R_true = max(ones)
        # R is read off the image, not from the true row:
        R_from_image = max(i for i in y if y[i]) - 1
        if R_from_image != R_true:
            mismatches.append({"t": t, "why": "support endpoint",
                               "R_true": R_true, "R_img": R_from_image})
            continue
        rec = peel_back(y, R_from_image)
        bad = [i for i in range(lo, hi + 1)
               if rec.get(i, 0) != true_x.get(i, 0)]
        if bad:
            mismatches.append({"t": t, "why": "peel", "first_bad": bad[0],
                               "n_bad": len(bad)})
        # PATH.md section 1 pin, as a cross-check on the same rows
        for x_ in range(lo + 1, hi):
            if true_x.get(x_, 0) == 1:
                pin_checks += 1
                if true_x.get(x_ - 1, 0) != (1 ^ y.get(x_, 0)):
                    pin_violations += 1
    print(json.dumps({
        "T": T,
        "rows_reconstructed": T,
        "reconstruction_mismatches": len(mismatches),
        "mismatch_detail": mismatches[:5],
        "branch_points_on_orbit": 0 if not mismatches else None,
        "pin_instances_checked": pin_checks,
        "pin_violations": pin_violations,
    }, indent=1))


if __name__ == "__main__":
    main()

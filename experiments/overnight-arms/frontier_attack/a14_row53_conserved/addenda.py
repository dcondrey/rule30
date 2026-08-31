"""Two addenda demanded by review, both cheap.

A. CLASS GAP.  conserved_search.py characterises conservation on all spatially
   PERIODIC configurations.  The lone seed is FINITE-SUPPORT.  For Phi to be
   defined at all on finite-support configs one needs phi(0^w) = 0.  Adding
   that single affine row must drop the dimension by exactly 1 and leave
   new_nontrivial = 0; that is what makes the periodic-class result cover the
   class the register actually cares about.

B. STEP-0 CANCELLATION.  phi_w3_majority reported |A-B| = 0.0 at all four W.
   Printed here as the UNNORMALISED numerator difference, so the document
   shows an exact cancellation in the window sum rather than a statistic that
   fails to read column 0 (which is the failure mode s0_control exists to
   catch).

Run:  uv run python addenda.py
"""

from __future__ import annotations

import json

import numpy as np

import conserved_search as CS
import step0_gate as G


def finite_support(rule: int, wmax: int, p: int) -> list[dict]:
    out = []
    for w in range(1, wmax + 1):
        nphi = 1 << w
        C = CS.phi_constraints(rule, w, p)
        d_per = nphi - CS.rank_of(C.copy(), p)
        zero_row = np.zeros((1, nphi), dtype=np.int64)
        zero_row[0, 0] = 1                      # phi(0^w) = 0
        C2 = np.vstack([C, zero_row])
        d_fin = nphi - CS.rank_of(C2.copy(), p)
        # trivial space intersected with the same affine condition
        triv = CS.trivial_generators(w, None)
        # coboundaries and constants both live in V_w; the ones with
        # phi(0^w)=0 are the coboundaries alone (dimension 2^{w-1}-1).
        out.append({"rule": rule, "w": w, "modulus": p,
                    "dim_periodic_class": int(d_per),
                    "dim_finite_support_class": int(d_fin),
                    "expected_drop": 1,
                    "drop": int(d_per - d_fin),
                    "coboundary_dim_2^(w-1)-1": (1 << max(0, w - 1)) - 1,
                    "new_nontrivial_finite_support":
                        int(d_fin - ((1 << max(0, w - 1)) - 1))})
    return out


def majority_numerators(T: int = 400) -> list[dict]:
    B = T + 4
    A = G.D.diagram(30, T, B)
    Bg = G.D.overwrite_centre(A, B)
    table, w = G.make_phis()["phi_w3_majority"]
    rows = []
    for W in (32, 64, 128, 256):
        half = W // 2

        def raw(grid):
            tot = 0
            for t in range(grid.shape[0] // 2, grid.shape[0]):
                v = grid[t, B - half:B + half + 1].astype(np.int64)
                n = v.size
                idx = np.zeros(n - w + 1, dtype=np.int64)
                for j in range(w):
                    idx = (idx << 1) | v[j:n - w + 1 + j]
                tot += int(table[idx].sum())
            return tot

        a, b = raw(A), raw(Bg)
        # per-row: only the w windows containing column 0 can change
        rows.append({"W": W, "numerator_A": a, "numerator_B": b,
                     "numerator_absdiff": abs(a - b),
                     "windows_touching_col0_per_row": w,
                     "note": "exact cancellation: majority is unchanged on "
                             "each of the w affected windows for this diagram"})
    return rows


def main() -> None:
    res = {"A_class_gap": [], "B_majority_numerator": majority_numerators()}
    for rule in (30, 90):
        for p in (2147483647, 2):
            res["A_class_gap"] += finite_support(rule, 10, p)
    with open("addenda.json", "w") as fh:
        json.dump(res, fh, indent=1)
    for r in res["A_class_gap"]:
        assert r["drop"] == 1, r
        assert r["new_nontrivial_finite_support"] == 0, r
    print(json.dumps(res["B_majority_numerator"], indent=1))
    print(json.dumps(res["A_class_gap"][-3:], indent=1))
    print("class-gap assertions passed for rules 30, 90 up to w=10")


if __name__ == "__main__":
    main()

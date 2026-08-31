"""STEP 0 GATE for arm A8 (backward dynamics / preimage descent).

PATH.md section 0.1 single-column sensitivity filter, run on the candidate
quantity of this arm BEFORE any descent machinery is built.

CANDIDATE QUANTITY, defined precisely.
  S4_cyclic_preimage(grid, B, W) = mean over the second half of rows t of
      log2(1 + N_W(row_t))
  where row_t is the length-W window of row t centred on column 0, READ AS A
  RING of circumference W, and N_W is the number of x in {0,1}^W with
      row_t[i] = x[i-1] XOR (x[i] OR x[i+1])   (indices mod W)
  computed exactly as the trace of a product of 4x4 transfer matrices over the
  states (x[i-1], x[i]).

  Cyclic (not free) boundary is deliberate: register row 60's non-bijectivity
  measurement ("non-bijective at every N from 3 to 14, up to 3 preimages") is a
  measurement on Z_N.  With FREE boundary the count is identically 4 for every
  left-permutive rule (see free_boundary_count.py), so the free-boundary
  variant is constant and could not move at all.

CONTROLS.
  S0_control_col0  reads only column 0 (from the read-only discriminator).
  Two overwrite variants of the field, not one:
    B_per  column 0 overwritten with the periodic word 0101...
    B_rnd  column 0 overwritten with a fixed-seed RANDOM word.
  The mandated gate asks only about B_per.  B_rnd is added because a quantity
  that moves equally for both detects that column 0 was TAMPERED WITH, not that
  it is PERIODIC, and column-sensitivity without periodicity-sensitivity still
  decides nothing about P1.

PREDICTION, RECORDED BEFORE THE RUN (2026-08-30).
  (a) |S4(A) - S4(B_per)| will NOT be O(1/W): the ring count is a trace over a
      product of W matrices and one flipped factor can move the count between
      0 and 3, so a single-cell change per row is expected to move S4 by O(1).
      So S4 is expected to PASS the mandated step-0 gate.
  (b) |S4(A) - S4(B_per)| ~ |S4(A) - S4(B_rnd)|, i.e. S4 is tamper-sensitive
      and periodicity-blind.  KILL CONDITION for the arm at this second gate:
      the two deltas agree to within the row-to-row noise.
  (c) S4(A) vs S4(C=Rule 90) will separate, and per PATH.md section 0 that is
      worth nothing on its own.

ADDED AFTER THE FIRST RUN, and labelled as such rather than folded in:
prediction (a) was FALSE -- the deltas were 0.0 exactly for W >= 64.  A zero
delta from a statistic that is CONSTANT on generic inputs is degeneracy, not
column-blindness, so a saturation control was added (fraction of uniform-random
length-W words with a unique cyclic preimage) and the width sweep was extended
downward to 8, where S4 still has range.  The kill must be readable off
non-degenerate widths.
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from discriminator_local import diagram, overwrite_centre, s0_control  # noqa: E402


def _transfer(yi):
    """4x4 0/1 matrix over states (a,b)=(x[i-1],x[i]) -> (b,c)=(x[i],x[i+1]),
    allowed iff  yi == a XOR (b OR c)."""
    M = np.zeros((4, 4), dtype=np.int64)
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                if (a ^ (b | c)) == yi:
                    M[2 * a + b, 2 * b + c] = 1
    return M


_T = {0: _transfer(0), 1: _transfer(1)}


def cyclic_preimage_count(word):
    """Exact number of length-W cyclic preimages of `word` under Rule 30."""
    P = np.eye(4, dtype=np.int64)
    for v in word:
        P = P @ _T[int(v)]
    return int(np.trace(P))


def s4_cyclic_preimage(grid, B, W):
    T = grid.shape[0]
    half = W // 2
    vals = []
    for t in range(T // 2, T):
        w = grid[t, B - half:B - half + W]
        vals.append(np.log2(1.0 + cyclic_preimage_count(w)))
    return float(np.mean(vals))


def overwrite_centre_random(grid, B, seed=12345):
    rng = np.random.default_rng(seed)
    g = grid.copy()
    g[:, B] = rng.integers(0, 2, size=g.shape[0]).astype(g.dtype)
    return g


def main():
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    B = T + 4
    A = diagram(30, T, B)
    Bp = overwrite_centre(A, B)
    Br = overwrite_centre_random(A, B)
    C = diagram(90, T, B)
    for name, G in (("B_per", Bp), ("B_rnd", Br)):
        assert (A != G).sum() == (A[:, B] != G[:, B]).sum(), \
            f"{name} must differ from A on column 0 only"
    out = {"T": T, "cells": int(A.size),
           "cells_changed_A_to_B_per": int((A[:, B] != Bp[:, B]).sum()),
           "cells_changed_A_to_B_rnd": int((A[:, B] != Br[:, B]).sum())}
    # Saturation control: is S4 constant on GENERIC words at this width?  If
    # almost every length-W word has a unique cyclic preimage then S4 == 1.0
    # identically and a zero delta is degeneracy, not column-blindness.
    rng = np.random.default_rng(7)
    sat = {}
    for W in (8, 12, 16, 24, 32, 64, 128):
        ws = rng.integers(0, 2, size=(2000, W))
        cs = [cyclic_preimage_count(w) for w in ws]
        sat[W] = {"frac_count_eq_1": float(np.mean([c == 1 for c in cs])),
                  "frac_count_eq_0": float(np.mean([c == 0 for c in cs])),
                  "mean_log2_1p": float(np.mean(np.log2(1.0 + np.array(cs))))}
    out["saturation_control_random_words"] = sat
    print(json.dumps(out), flush=True)
    for W in (8, 12, 16, 24, 32, 64, 128, 256):
        row = {"W": W}
        for name, fn in (("S0_control_col0", s0_control),
                         ("S4_cyclic_preimage", s4_cyclic_preimage)):
            a = fn(A, B, W)
            bp = fn(Bp, B, W)
            br = fn(Br, B, W)
            c = fn(C, B, W)
            row[name] = {
                "A": float(f"{a:.10g}"), "B_per": float(f"{bp:.10g}"),
                "B_rnd": float(f"{br:.10g}"), "C_rule90": float(f"{c:.10g}"),
                "absA_Bper": float(f"{abs(a - bp):.4g}"),
                "absA_Brnd": float(f"{abs(a - br):.4g}"),
                "relA_Bper": float(f"{abs(a-bp)/max(abs(a),1e-12):.4g}"),
                "relA_C": float(f"{abs(a-c)/max(abs(a),1e-12):.4g}")}
        print(json.dumps(row), flush=True)


if __name__ == "__main__":
    main()

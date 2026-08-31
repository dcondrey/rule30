"""STEP 0 GATE for register row 53 (conserved window functions).

PATH.md section 0.1 / obstruction C.  A conserved window quantity is
    Phi(s) = sum_x phi(s(x), ..., s(x+w-1))
i.e. a SPATIAL AGGREGATE over a row.  Read as a statistic on a width-W window
about the centre it is normalised, Phi_W(s) = (1/W) sum_{x in window} phi(...),
which is the only reading on which "does it move when column 0 is overwritten"
is a meaningful question.

ANALYTIC PREDICTION, recorded before running.  Overwriting column 0 changes
exactly one cell per row.  That cell lies inside at most w of the W window
terms, so

    |Phi_W(A) - Phi_W(B)|  <=  w * (max phi - min phi) / W  =  O(1/W).

This is a theorem about the whole family, not a property of one candidate.
KILL CONDITION for step 0: if the measured |A-B| decays like 1/W across
W = 32,64,128,256 while the s0_control (which reads column 0) moves by ~96%,
the family is column-blind and cannot decide P1 or P2.
DISCONFIRMING OUTCOME that would keep the arm alive: any phi whose |A-B| stays
flat (or decays slower than 1/W) as W doubles.

Six representative phi are run, spanning the class the search will enumerate:
constant-free additive (w=1 density), the two nonlinear low-width monomials,
a random nonlinear w=5 function, and the block-entropy-style indicator that a
latent-space generator would most plausibly emit.

Run:  uv run python step0_gate.py [T]
"""

from __future__ import annotations

import importlib.util
import json
import sys

import numpy as np

DISC_PATH = ("/Volumes/A/researchpapers/13-rule30/experiments/rule30/"
             "p_geometric_attack/discriminator.py")


def _load_discriminator():
    """READ-ONLY import of the repo's mandated discriminator harness."""
    spec = importlib.util.spec_from_file_location("repo_discriminator", DISC_PATH)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


D = _load_discriminator()


def window_stat(phi_table: np.ndarray, w: int):
    """Return S(grid,B,W) = mean over the second half of rows of the
    W-normalised window sum (1/W) sum_x phi(s(x..x+w-1))."""

    def stat(grid, B, W):
        T = grid.shape[0]
        half = W // 2
        vals = []
        for t in range(T // 2, T):
            v = grid[t, B - half:B + half + 1].astype(np.int64)
            n = v.size
            if n < w:
                continue
            idx = np.zeros(n - w + 1, dtype=np.int64)
            for j in range(w):
                idx = (idx << 1) | v[j:n - w + 1 + j]
            vals.append(phi_table[idx].sum() / W)
        return float(np.mean(vals))

    return stat


def make_phis():
    """Representative members of the class the row-53 search enumerates."""
    rng = np.random.default_rng(30)
    phis = {}

    # w=1: additive density.  The canonical "additive conserved quantity"
    # candidate of Hattori-Takesue / Boccara-Fuks number-conserving theory.
    phis["phi_w1_density"] = (np.array([0, 1], dtype=np.int64), 1)

    # w=2: block indicator 11 (nonlinear, degree 2).
    t2 = np.zeros(4, dtype=np.int64)
    t2[0b11] = 1
    phis["phi_w2_block11"] = (t2, 2)

    # w=3: the nonlinear monomial v0*v1*v2.
    t3 = np.zeros(8, dtype=np.int64)
    t3[0b111] = 1
    phis["phi_w3_monomial"] = (t3, 3)

    # w=3: majority, a non-additive symmetric function.
    t3m = np.array([bin(i).count("1") >= 2 for i in range(8)], dtype=np.int64)
    phis["phi_w3_majority"] = (t3m, 3)

    # w=5: a random integer-valued nonlinear window function in [-3,3], the
    # generic member of the search space (phi(0^w)=0 for well-definedness).
    t5 = rng.integers(-3, 4, size=32).astype(np.int64)
    t5[0] = 0
    phis["phi_w5_random"] = (t5, 5)

    # w=5: run-length indicator, the shape a latent-space candidate generator
    # most plausibly emits (row 53's ML half).
    t5r = np.zeros(32, dtype=np.int64)
    for i in range(32):
        b = format(i, "05b")
        t5r[i] = max(len(r) for r in b.replace("0", " ").split()) if "1" in b else 0
    phis["phi_w5_maxrun"] = (t5r, 5)

    return phis


def main() -> None:
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    B = T + 4
    A = D.diagram(30, T, B)
    Bg = D.overwrite_centre(A, B)
    C = D.diagram(90, T, B)
    assert (A != Bg).sum() == (A[:, B] != Bg[:, B]).sum(), \
        "B must differ from A on column 0 only"
    ndiff = int((A[:, B] != Bg[:, B]).sum())
    print(json.dumps({"gate": "row53_conserved_window_family", "T": T,
                      "cells": int(A.size), "cells_changed_A_to_B": ndiff,
                      "fraction_changed": round(ndiff / A.size, 8)}), flush=True)

    stats = {"S0_control_col0": D.s0_control}
    for name, (table, w) in make_phis().items():
        stats[name] = window_stat(table, w)

    for W in (32, 64, 128, 256):
        row = {"W": W}
        for name, fn in stats.items():
            a, b, c = fn(A, B, W), fn(Bg, B, W), fn(C, B, W)
            row[name] = {
                "A": float(f"{a:.10g}"), "B": float(f"{b:.10g}"),
                "C": float(f"{c:.10g}"),
                "absAB": float(f"{abs(a - b):.4g}"),
                "relAB": float(f"{abs(a - b) / max(abs(a), 1e-12):.4g}"),
                "relAC": float(f"{abs(a - c) / max(abs(a), 1e-12):.4g}"),
            }
        print(json.dumps(row), flush=True)


if __name__ == "__main__":
    main()

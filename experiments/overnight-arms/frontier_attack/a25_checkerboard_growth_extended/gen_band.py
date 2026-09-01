"""Generation only: cache the wmax=15 centre band of the lone-seed Rule 30
diagram for a given horizon, using a3's exact kernel (read-only import).

usage: uv run python gen_band.py STEPS [OUTDIR]
"""

from __future__ import annotations

import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
A3 = os.path.abspath(os.path.join(HERE, "..", "a3_p2_orbit_closure"))
sys.path.insert(0, A3)
from band_census import _band_series  # noqa: E402

WMAX = 15

if __name__ == "__main__":
    steps = int(float(sys.argv[1]))
    outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "cache")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, f"band_rule30_{steps}_{WMAX}.npy")
    if os.path.exists(path):
        print("already exists", path)
        sys.exit(0)
    t0 = time.time()
    band = _band_series("30", steps, WMAX)
    dt = time.time() - t0
    np.save(path + ".tmp.npy", band)
    os.replace(path + ".tmp.npy", path)
    print(f"numpy kernel steps={steps} wmax={WMAX} seconds={dt:.1f}")

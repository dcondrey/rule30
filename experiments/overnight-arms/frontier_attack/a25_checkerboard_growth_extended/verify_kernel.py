"""Bit-exactness gate for the C kernel: band30 must reproduce a3's numpy
`_band_series` exactly.  Checked against the cached a22 bands at T=200_000 and
T=4_000_000 (the latter is 4e6*32 bits of the actual lone-seed diagram, so this
is a strong check, not a smoke test).

usage: uv run python verify_kernel.py BIN_PATH NPY_PATH
"""

from __future__ import annotations

import sys

import numpy as np

if __name__ == "__main__":
    binp, npyp = sys.argv[1], sys.argv[2]
    c = np.fromfile(binp, dtype=np.uint32)
    p = np.load(npyp)
    n = min(c.size, p.size)
    same = np.array_equal(c[:n], p[:n].astype(np.uint32))
    sys.stderr.write(f"{'PASS' if same else 'FAIL'} n={n} c={c.size} npy={p.size}\n")
    if not same:
        bad = np.flatnonzero(c[:n] != p[:n])
        sys.stderr.write(f"first mismatch at t={bad[0]}: c={c[bad[0]]} npy={p[bad[0]]}\n")
    sys.exit(0 if same else 1)

"""a25 step 1: REPRODUCTION GATE.

Before extending anything, establish bit-exactly that this session regenerates
the same lone-seed Rule 30 band data that a3 and a22 used, and that a22's
reported numbers fall out of its own cached band.

Three checks, cheapest first:

  X1  a22's cached band (T=4e6, wmax=15) reduced to wmax=8 must equal a3's
      independently generated cached band (T=2e6, wmax=8) on their common
      prefix.  Two separate generation runs, different wmax, same diagram.
  X2  a fresh regeneration here (T=200_000, wmax=15) with a3's kernel must be
      array-identical to a22's cached T=200_000 band.
  X3  recompute a22's published table (diagonal K and per-W max heights at
      T=2e6 and T=4e6) from the cached 4e6 band using a22's own code path,
      and compare against the numbers printed in a22's report.

If any of these fails, STOP; a reproduction failure outranks any extension.
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FA = os.path.abspath(os.path.join(HERE, ".."))
A3 = os.path.join(FA, "a3_p2_orbit_closure")
A22 = os.path.join(FA, "a22_p2_checkerboard_growth")
sys.path.insert(0, A3)
sys.path.insert(0, A22)

A3_CACHE = (
    "/private/tmp/claude-501/-Volumes-A-researchpapers-13-rule30/"
    "ed534796-4b7d-4631-8362-2e60223b917f/scratchpad"
)
A22_CACHE = os.path.join(A22, "cache")

from band_census import _band_series  # noqa: E402

fails = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {detail}")
    if not ok:
        fails.append(name)


# ---------------------------------------------------------------- X1
b22 = np.load(os.path.join(A22_CACHE, "band_rule30_4000000_15.npy"))
b3 = np.load(os.path.join(A3_CACHE, "band_rule30_2000000_8.npy"))
n = min(b22.size, b3.size)
red = ((b22[:n] >> np.uint32(7)) & np.uint32(0x1FFFF)).astype(np.uint32)
check("X1 a22(wmax15) reduced == a3(wmax8)", np.array_equal(red, b3[:n].astype(np.uint32)),
      f"(n={n})")

# ---------------------------------------------------------------- X2
fresh = _band_series("30", 200_000, 15)
cached200k = np.load(os.path.join(A22_CACHE, "band_rule30_200000_15.npy"))
check("X2 fresh regen(200k,wmax15) == a22 cache", np.array_equal(fresh, cached200k))

# ---------------------------------------------------------------- X3
import extend_growth as eg  # noqa: E402

band = b22
report = {}
for name in ("all_zeros", "checker_A", "checker_B"):
    diag = eg.diagonal_K(band, name, 15, [2_000_000, 4_000_000])
    heights = {w: eg.max_height(band, w, name, 15) for w in range(16)}
    report[name] = {"diag": diag, "heights": heights}
    print(f"  {name}: K(2e6)={diag['2000000']['K']} K(4e6)={diag['4000000']['K']} "
          f"witness4e6={diag['4000000']['witness_t']}")
    print(f"    heights W=0..15: {[heights[w] for w in range(16)]}")

# a22's report table, transcribed from p2_checkerboard_growth.md sections 2
expect_K = {"all_zeros": (4, 5), "checker_A": (6, 6), "checker_B": (5, 6)}
expect_h = {
    "all_zeros": [20, 9, 8, 7, 6, 5, 4, 3, 2, 1] + [0] * 6,
    "checker_A": [23, 17, 16, 13, 12, 9, 8, 5, 4, 2, 1] + [0] * 5,
    "checker_B": [20, 17, 14, 13, 11, 10, 7, 6, 2, 1] + [0] * 6,
}
for name in expect_K:
    d = report[name]["diag"]
    got = (d["2000000"]["K"], d["4000000"]["K"])
    check(f"X3 K {name}", got == expect_K[name], f"got {got} want {expect_K[name]}")
    goth = [report[name]["heights"][w] for w in range(16)]
    check(f"X3 heights {name}", goth == expect_h[name], f"got {goth}")

# also check a22's own json agrees with what we just recomputed
with open(os.path.join(A22, "extend_growth_4000000.json")) as fh:
    j = json.load(fh)
for name in expect_K:
    jj = j["families"][name]
    goth = [jj["max_height_by_W_at_T"][str(w)] for w in range(16)]
    check(f"X3b json heights {name}", goth == [report[name]["heights"][w] for w in range(16)])

print()
print("REPRODUCTION:", "PASS" if not fails else f"FAIL {fails}")
sys.exit(1 if fails else 0)

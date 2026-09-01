"""Correctness gate for the bit-packed C generator (gen30.c).

Three independent cross-checks, all must pass before any long run is trusted:
  1. OEIS A051023 b-file (100,001 terms, offset 0) -- external ground truth.
  2. This repo's existing generator (experiments/overnight-arms/common/rule30.py
     center_column_bits), i.e. the exact prefix the row-76 measurement used.
  3. A dead-simple from-scratch naive O(n^2) 2D-grid simulator written here.

  4. Wolfram's own published "A Million Bits of the Center Column of the Rule 30
     Cellular Automaton" (Wolfram Data Repository, 2017,
     doi:10.24097/wolfram.25316.data), CSV export -- the exact artifact the
     prize announcement points at. This is the strongest available gate:
     10^6 bits against the prize-setter's own data.

Usage: uv run python verify.py <bitstream.bin> <oeis_b_file> [wolfram_million.csv]

The Wolfram CSV is fetched anonymously from
https://www.wolframcloud.com/objects/5dff9a81-4a7a-406d-af85-8f8d479298e2
(linked from the repository landing page's Data Downloads section).
"""
from __future__ import annotations
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "overnight-arms", "common"))
from rule30 import center_column_bits  # noqa: E402


def naive_center_column(n: int) -> list[int]:
    """Direct 2D grid, no frame trick, no bit packing. s(t+1,x)=s(t,x-1)^(s(t,x)|s(t,x+1))."""
    width = 2 * n + 5
    mid = width // 2
    row = [0] * width
    row[mid] = 1
    out = []
    for _ in range(n):
        out.append(row[mid])
        row = [0] + [row[x - 1] ^ (row[x] | row[x + 1]) for x in range(1, width - 1)] + [0]
    return out


def unpack(path: str, nbits: int) -> list[int]:
    with open(path, "rb") as f:
        data = f.read((nbits + 7) // 8)
    return [(data[i >> 3] >> (i & 7)) & 1 for i in range(nbits)]


def main():
    binpath, oeispath = sys.argv[1], sys.argv[2]

    with open(oeispath) as f:
        oeis = [int(line.split()[1]) for line in f if line.strip()]
    n_oeis = len(oeis)
    print(f"OEIS A051023 terms loaded: {n_oeis}")

    got = unpack(binpath, n_oeis)
    ok_oeis = got == oeis
    print(f"[1] gen30 vs OEIS A051023, {n_oeis} bits: {'PASS' if ok_oeis else 'FAIL'}")
    if not ok_oeis:
        bad = next(i for i in range(n_oeis) if got[i] != oeis[i])
        print(f"    first mismatch at index {bad}: got {got[bad]} want {oeis[bad]}")

    repo = center_column_bits(n_oeis)
    ok_repo = got == repo
    print(f"[2] gen30 vs repo center_column_bits, {n_oeis} bits: {'PASS' if ok_repo else 'FAIL'}")
    ok_repo_oeis = repo == oeis
    print(f"[2b] repo generator vs OEIS, {n_oeis} bits: {'PASS' if ok_repo_oeis else 'FAIL'}")

    NN = 5000
    nv = naive_center_column(NN)
    ok_naive = got[:NN] == nv
    print(f"[3] gen30 vs from-scratch naive O(n^2) grid, {NN} bits: {'PASS' if ok_naive else 'FAIL'}")

    ok_wolf = True
    if len(sys.argv) > 3:
        with open(sys.argv[3]) as f:
            wolf = [int(x) for x in f.read().strip().split(",")]
        mine = unpack(binpath, len(wolf))
        ok_wolf = mine == wolf
        print(f"[4] gen30 vs Wolfram A-Million-Bits, {len(wolf)} bits: "
              f"{'PASS' if ok_wolf else 'FAIL'}")
    else:
        print("[4] Wolfram million-bit CSV not supplied; skipped")

    allok = ok_oeis and ok_repo and ok_repo_oeis and ok_naive and ok_wolf
    print("ALL CHECKS PASS" if allok else "SOME CHECK FAILED")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())

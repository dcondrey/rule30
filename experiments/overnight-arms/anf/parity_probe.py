"""anf arm: parity-invariant probe for the reduction lemma (PREREG-anf.md Addendum 1).

The degree theorem reduces to parity claims about adjacent-tuple AND functions.
For the pair P = s(t,0) AND s(t,1) on window cells -t..t+1 (var v = cell + t):
  C1: parity of #{y : y_0 = 0, P(y) = 1}                 -- claim 1 (odd)
  C2(k): parity of #{y : y_0 = 0, y_k = 0, P(y) = 1}     -- claim 0 for all k >= 1
Also, closure-hunting: full and codim-1 restricted parities of the j-tuple
all-ones AND for j = 1..4, t = 2..12. Writes runs/overnight/anf/parity.json.

Run: uv run --with numpy python experiments/overnight-arms/anf/parity_probe.py
"""

from __future__ import annotations

import json
import logging
import pathlib

import numpy as np

log = logging.getLogger(__name__)
OUT = pathlib.Path("/Volumes/A/researchpapers/13-rule30/runs/overnight/anf/parity.json")
FULL = np.uint64(0xFFFFFFFFFFFFFFFF)


def packed_var(i: int, n: int) -> np.ndarray:
    words = 1 << max(n - 6, 0)
    if i >= 6:
        j = np.arange(words, dtype=np.uint64)
        return np.where((j >> np.uint64(i - 6)) & np.uint64(1) == 1, FULL, np.uint64(0))
    period = 1 << i
    bits = ([0] * period + [1] * period) * (64 // (2 * period))
    word = sum(b << k for k, b in enumerate(bits))
    return np.full(words, np.uint64(word), dtype=np.uint64)


def tuple_and(t: int, j: int) -> tuple[np.ndarray, int]:
    """Packed table of s(t,0) AND ... AND s(t,j-1) on window cells -t..t+j-1."""
    n = 2 * t + j
    assert n >= 6
    cells = [packed_var(i, n) for i in range(n)]
    for _ in range(t):
        cells = [cells[k - 1] ^ (cells[k] | cells[k + 1]) for k in range(1, len(cells) - 1)]
    assert len(cells) == j
    acc = cells[0]
    for c in cells[1:]:
        acc = acc & c
    return acc, n


def zero_mask(k: int, n: int) -> np.ndarray:
    """Packed mask selecting positions whose bit k is 0."""
    words = 1 << max(n - 6, 0)
    if k >= 6:
        wj = np.arange(words, dtype=np.uint64)
        return np.where((wj >> np.uint64(k - 6)) & np.uint64(1) == 0, FULL, np.uint64(0))
    period = 1 << k
    bits = ([1] * period + [0] * period) * (64 // (2 * period))
    word = sum(b << i for i, b in enumerate(bits))
    return np.full(words, np.uint64(word), dtype=np.uint64)


def parity(packed: np.ndarray) -> int:
    return int(np.unpackbits(packed.view(np.uint8)).sum() & 1)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    results = []
    for t in range(2, 13):
        row: dict = {"t": t}
        # C1 / C2 from the pair function
        p2, n2 = tuple_and(t, 2)
        m0 = zero_mask(0, n2)
        c1 = parity(p2 & m0)
        c2 = [parity(p2 & m0 & zero_mask(k, n2)) for k in range(1, n2)]
        row["C1"] = c1
        row["C2_nonzero_vars"] = [k for k, v in enumerate(c2, start=1) if v]
        # closure hunt: full + codim-1 parities for j = 1..4
        for j in range(1, 5):
            if 2 * t + j < 6:
                continue
            pj, nj = tuple_and(t, j)
            row[f"T{j}_full"] = parity(pj)
            row[f"T{j}_codim1"] = [parity(pj & zero_mask(k, nj)) for k in range(nj)]
        results.append(row)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(results, indent=1))
        log.info(
            "t=%2d C1=%d C2!=0 at %s | T_full j1..4: %s",
            t, c1, row["C2_nonzero_vars"],
            [row.get(f"T{j}_full") for j in range(1, 5)],
        )
        for j in range(1, 5):
            if f"T{j}_codim1" in row:
                log.info("   T%d codim1: %s", j, "".join(map(str, row[f"T{j}_codim1"])))


if __name__ == "__main__":
    main()

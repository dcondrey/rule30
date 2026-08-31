"""anf arm, main sweep (PREREG-anf.md + Addendum 1).

Packed-bit exact ANF of f_t for t = 2..13: deg, term count, L1/L2 checks,
missing-sets of the top two occupied degree layers (2t-1, 2t-2), and exact
Walsh max |coefficient| for t <= 12 (t = 13 attempted, guarded).
Writes JSON per t to runs/overnight/anf/sweep.json (incremental).

Run: uv run --with numpy python experiments/overnight-arms/anf/anf_sweep.py
"""

from __future__ import annotations

import json
import logging
import pathlib

import numpy as np

log = logging.getLogger(__name__)
OUT = pathlib.Path("/Volumes/A/researchpapers/13-rule30/runs/overnight/anf/sweep.json")


def packed_var(i: int, n: int) -> np.ndarray:
    """Variable i's truth table over 2^n inputs, packed 64 bits/word."""
    words = 1 << max(n - 6, 0)
    if i >= 6:
        j = np.arange(words, dtype=np.uint64)
        return np.where((j >> np.uint64(i - 6)) & np.uint64(1) == 1,
                        np.uint64(0xFFFFFFFFFFFFFFFF), np.uint64(0))
    period = 1 << i
    bits = ([0] * period + [1] * period) * (64 // (2 * period))
    word = sum(b << k for k, b in enumerate(bits))
    return np.full(words, np.uint64(word), dtype=np.uint64)


def truth_table_packed(t: int) -> np.ndarray:
    n = 2 * t + 1
    cells = [packed_var(i, n) for i in range(n)]
    for _ in range(t):
        cells = [cells[j - 1] ^ (cells[j] | cells[j + 1]) for j in range(1, len(cells) - 1)]
    return cells[0]


def mobius_packed(a: np.ndarray, n: int) -> np.ndarray:
    a = a.copy()
    for i in range(min(n, 6)):
        sh = np.uint64(1 << i)
        mask_clear = np.uint64(sum(1 << b for b in range(64) if not (b >> i) & 1))
        a ^= (a & mask_clear) << sh
    for i in range(6, n):
        step = 1 << (i - 6)
        for base in range(0, a.size, step << 1):
            a[base + step : base + (step << 1)] ^= a[base : base + step]
    return a


def index_popcount_chunk(start: int, count: int, n: int) -> np.ndarray:
    idx = np.arange(start, start + count, dtype=np.uint64)
    pc = np.zeros(count, dtype=np.uint8)
    for i in range(n):
        pc += ((idx >> np.uint64(i)) & np.uint64(1)).astype(np.uint8)
    return pc


def analyze(t: int, do_walsh: bool) -> dict:
    n = 2 * t + 1
    tt = truth_table_packed(t)
    anf = mobius_packed(tt, n)
    bits = np.unpackbits(anf.view(np.uint8), bitorder="little")
    ones = np.flatnonzero(bits).astype(np.uint64)
    terms = int(ones.size)
    pc = np.zeros(ones.size, dtype=np.uint8)
    for i in range(n):
        pc += ((ones >> np.uint64(i)) & np.uint64(1)).astype(np.uint8)
    deg = int(pc.max())
    l2 = not np.any(pc >= 2 * t)

    def missing_sets(d: int) -> list[list[int]]:
        sel = ones[pc == d]
        return sorted(
            [i for i in range(n) if not (int(m) >> i) & 1] for m in sel
        )

    top1, top2 = missing_sets(2 * t - 1), missing_sets(2 * t - 2)
    # L1: f XOR (f with bit0 flipped) == all ones  (packed: flip = swap odd/even bits)
    flip = ((tt & np.uint64(0x5555555555555555)) << np.uint64(1)) | (
        (tt & np.uint64(0xAAAAAAAAAAAAAAAA)) >> np.uint64(1)
    )
    l1 = bool(np.all((tt ^ flip) == np.uint64(0xFFFFFFFFFFFFFFFF)))

    walsh_max = None
    if do_walsh:
        f = np.unpackbits(tt.view(np.uint8), bitorder="little").astype(np.int32)
        f = 1 - 2 * f
        for i in range(n):
            f = f.reshape(-1, 2 << i)
            half = 1 << i
            a, b = f[:, :half].copy(), f[:, half:].copy()
            f[:, :half], f[:, half:] = a + b, a - b
        walsh_max = int(np.abs(f).max())
    return {
        "t": t, "n": n, "deg": deg, "terms": terms, "L1": l1, "L2": l2,
        "top_missing_sets": top1, "second_missing_sets_count": len(top2),
        "second_missing_sets": top2 if len(top2) <= 40 else top2[:40],
        "walsh_max": walsh_max,
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    # t >= 3 only: the packed representation is exact only for n = 2t+1 >= 6
    # (at t = 2 the 32 valid bits share a word with 32 garbage bits).
    results = json.loads(OUT.read_text()) if OUT.exists() else []
    done = {r["t"] for r in results}
    for t in range(3, 14):
        if t in done:
            continue
        do_walsh = True
        try:
            r = analyze(t, do_walsh)
        except MemoryError:
            log.info("t=%d: MemoryError, stopping sweep", t)
            break
        results.append(r)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(results, indent=1))
        log.info(
            "t=%2d deg=%2d terms=%8d L1=%s L2=%s top=%s |2nd|=%d walsh_max=%s",
            t, r["deg"], r["terms"], r["L1"], r["L2"],
            r["top_missing_sets"], r["second_missing_sets_count"], r["walsh_max"],
        )


if __name__ == "__main__":
    main()

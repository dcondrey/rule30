"""Measure the longest centre-column self-agreement run at T = 1e9.

PREREG-zeroset-3e9.md section 0 argues the 3e9 band should NOT be spent on an
agreement-window sweep, because a1's seed-pair construction already produced
4000-step exact agreement while a self-overlap at depth T produces only
~log2(T). That constant is load-bearing for the argument, so it is measured
here on Wolfram's real 1e9 bits rather than asserted from theory.

For a period p, the agreement run is a maximal run of t with c_t = c_{t+p},
i.e. a maximal run of 0s in c XOR shift(c, p).

Bit order is MSB-first, matching the WDR payload and deep_gen.py.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WDR = os.path.join(HERE, "ref", "wdr_billion.bin")
OFFSET, NBYTES = 239, 125_000_000     # re-derived and asserted by crosscheck_wdr.py


def shift_msb(arr: np.ndarray, p: int, out_bytes: int) -> np.ndarray:
    """Bytes of the MSB-first bit stream starting at bit `p`.

    In MSB-first packing bit b of a byte is mask 0x80 >> b, so shifting a byte
    LEFT by r brings bit (b + r) into position b -- i.e. left shift looks
    ahead, which is the direction we need.
    """
    q, r = divmod(p, 8)
    if r == 0:
        return arr[q:q + out_bytes]
    hi = arr[q:q + out_bytes].astype(np.uint16) << r
    lo = arr[q + 1:q + 1 + out_bytes].astype(np.uint16) >> (8 - r)
    return ((hi | lo) & 0xFF).astype(np.uint8)


def longest_zero_run(x: np.ndarray, chunk: int = 1 << 22) -> int:
    """Longest run of 0 bits in the MSB-first bit stream of packed bytes `x`."""
    best = run = 0
    for i in range(0, len(x), chunk):
        bits = np.unpackbits(x[i:i + chunk], bitorder="big")
        ones = np.flatnonzero(bits)
        if ones.size == 0:
            run += bits.size
            best = max(best, run)
            continue
        best = max(best, run + int(ones[0]))
        if ones.size > 1:
            best = max(best, int(np.diff(ones).max()) - 1)
        run = int(bits.size - ones[-1] - 1)
    return max(best, run)


def _self_test() -> None:
    """A wrong shift silently yields wrong run lengths, so pin it."""
    rng = np.random.default_rng(30)
    bits = rng.integers(0, 2, 4096, dtype=np.uint8)
    packed = np.packbits(bits, bitorder="big")
    for p in (0, 1, 7, 8, 9, 33, 64, 100):
        got = np.unpackbits(shift_msb(packed, p, 256), bitorder="big")[:2000]
        assert np.array_equal(got, bits[p:p + 2000]), f"shift_msb wrong at p={p}"

    # longest_zero_run against a slow reference, including cross-chunk runs
    for trial in range(20):
        b = (rng.random(5000) < 0.7).astype(np.uint8)
        b[1000:1200] = 0                      # a planted long run
        pk = np.packbits(b, bitorder="big")
        s = "".join(map(str, np.unpackbits(pk, bitorder="big")))
        assert longest_zero_run(pk, chunk=7) == max(map(len, s.split("1"))), \
            f"longest_zero_run wrong on trial {trial}"
    print("self-test OK: shift_msb and longest_zero_run pinned", flush=True)


def main() -> int:
    _self_test()
    if "--self-test" in sys.argv:
        return 0

    blob = np.fromfile(WDR, dtype=np.uint8, count=OFFSET + NBYTES)
    pay = blob[OFFSET:]
    T = NBYTES * 8
    assert np.unpackbits(pay[:8], bitorder="big")[:8].tolist() == [1, 1, 0, 1, 1, 1, 0, 0]
    print(f"WDR centre column loaded: T = {T:,} bits", flush=True)

    # log-spaced periods, byte-aligned and not, spanning six decades
    ps = sorted({int(v) for v in np.unique(np.geomspace(64, 5e8, 28).astype(np.int64))}
                | {1, 2, 3, 7, 13, 101, 1001, 65537, 999983})
    rows = []
    for p in ps:
        n_out = (T - p) // 8 - 1
        if n_out < 1000:
            continue
        x = shift_msb(pay, p, n_out)
        np.bitwise_xor(x, pay[:n_out], out=x)
        run = longest_zero_run(x)
        cmps = n_out * 8
        rows.append({"p": p, "comparisons": cmps, "longest_agreement_run": run,
                     "log2_comparisons": float(np.log2(cmps))})
        print(f"p={p:>12,}  comparisons={cmps:>15,}  longest agreement run={run:>4}"
              f"  log2(n)={np.log2(cmps):.1f}", flush=True)

    runs = np.array([r["longest_agreement_run"] for r in rows])
    l2 = np.array([r["log2_comparisons"] for r in rows])
    out = {
        "source": "Wolfram Data Repository 1e9 centre-column bits",
        "n_periods": len(rows),
        "max_over_all_p": int(runs.max()),
        "median_longest_run": float(np.median(runs)),
        "mean_ratio_run_over_log2n": float(np.mean(runs / l2)),
        "a1_seed_pair_window_for_comparison": 4000,
        "rows": rows,
    }
    print(f"\nmax over {len(rows)} sampled periods: {out['max_over_all_p']}"
          f"   median {out['median_longest_run']:.1f}"
          f"   mean run/log2(n) = {out['mean_ratio_run_over_log2n']:.2f}")
    print(f"a1's seed-pair construction already gave exact agreement over 4000 steps.")
    p = os.path.join(HERE, "agreement_runs_1e9.json")
    json.dump(out, open(p, "w"), indent=2)
    print(f"-> {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

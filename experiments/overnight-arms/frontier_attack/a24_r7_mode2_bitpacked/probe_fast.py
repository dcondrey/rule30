"""a24_r7_mode2_bitpacked: extended sweep using the verified bit-packed
build_words()/probe() from bitpacked.py. Same measurement a22_r7_mode2
was running -- min eventual period of col_-1 for rule=30, w="01", as a
function of left-depth k -- pushed to larger T than a22's O(T^2) stall
at T=400,000.

Correctness of build_words() vs. the original build_old() is established
separately in bitpacked.py's main() (0 mismatches across 273,098 cells,
10 configurations spanning rule in {30,90}, k up to 16, p in {2,3,4},
phases 0/1). This script does NOT re-verify correctness; it only runs
the (already-verified) fast path.

This is a NUMERICAL EXTENSION, not a proof. Flat/no-period-found at a
larger T is still not evidence of eventual periodicity failing to exist
beyond the horizon tested, and R7 mode (ii) stays open regardless of the
outcome here.
"""

from __future__ import annotations

import json
import sys
import time

from bitpacked import probe, build_words


def run(label, **kwargs):
    t0 = time.time()
    r = probe(build_words, **kwargs)
    dt = time.time() - t0
    r["wall_s"] = round(dt, 2)
    r["label"] = label
    print(f"[{label}] " + " ".join(f"{k}={v}" for k, v in r.items() if k != "label"),
          flush=True)
    return r


def main():
    results = []
    t_start = time.time()

    print("== 1. trend sweep: k growing, T=200000, qmax=4096, rule=30, w=01 ==",
          flush=True)
    for k in [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]:
        r = run("trend", rule=30, k=k, word="01", T=200_000, qmax=4096)
        results.append(r)

    print("\n== 2. horizon robustness at k=2, rule=30, w=01, qmax=4096 ==", flush=True)
    for T in [20_000, 100_000, 400_000, 1_000_000, 2_000_000]:
        r = run("horizon_k2", rule=30, k=2, word="01", T=T, qmax=4096)
        results.append(r)
        with open("probe_fast_out.json", "w") as f:
            json.dump(results, f, indent=1, default=str)

    print("\n== 3. phase 1 check, T=200000, qmax=2048 ==", flush=True)
    for k in [2, 8, 16, 32]:
        r = run("phase1", rule=30, k=k, word="01", T=200_000, qmax=2048, phase=1)
        results.append(r)

    print("\n== 4. deepest-depth push at largest feasible T ==", flush=True)
    for k in [2, 16, 64]:
        r = run("deep_k", rule=30, k=k, word="01", T=2_000_000, qmax=2048)
        results.append(r)
        with open("probe_fast_out.json", "w") as f:
            json.dump(results, f, indent=1, default=str)

    total = time.time() - t_start
    print(f"\nTOTAL wall time: {total:.1f} s", flush=True)

    with open("probe_fast_out.json", "w") as f:
        json.dump(results, f, indent=1, default=str)


if __name__ == "__main__":
    main()

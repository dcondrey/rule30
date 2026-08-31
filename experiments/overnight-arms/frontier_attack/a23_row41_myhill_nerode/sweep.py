"""a23: driver for the pre-registered kseed sweep (see PREREGISTRATION.md).

Runs mn_index.mn_index_sweep for a given `kind` ('30' or '90') across
KSEEDS, both phases, and prints the headline table (index_lower_bound at
s = pairs-1) plus, for the largest kseed only, the full per-s curve.
"""
from __future__ import annotations

import argparse
import time

from mn_index import mn_index_sweep

KSEEDS = [6, 8, 10, 12, 14, 16]


def sweep(kind: str, pairs: int = 20, W: int = 30, kseeds=KSEEDS):
    print(f"\n=== rule {kind} sweep: pairs={pairs} W={W} kseeds={kseeds} ===")
    headline = {}
    for kseed in kseeds:
        t0 = time.time()
        row = {}
        for phase in (0, 1):
            row[phase] = mn_index_sweep(kind, phase, kseed, pairs, W)
        dt = time.time() - t0
        s_last = pairs - 1
        headline[kseed] = row
        for phase in (0, 1):
            r = row[phase][s_last]
            tag = "01" if phase == 0 else "10"
            print(f"  kseed={kseed:2d} (d={2*kseed:2d}) phase={tag}  "
                  f"index({s_last})={r['index']:7d}  n_seeds={r['n_seeds']:7d}  "
                  f"n_prefixes={r['n_prefixes']:7d}  "
                  f"anomalies={r['n_anomalous_prefixes']:5d}  "
                  f"[{dt:.1f}s]")
    print("\n  headline table: kseed, d, phase, index_lower_bound(s=pairs-1)")
    print("  kseed   d  phase   index")
    for kseed in kseeds:
        for phase in (0, 1):
            tag = "01" if phase == 0 else "10"
            r = headline[kseed][phase][pairs - 1]
            print(f"  {kseed:5d}  {2*kseed:3d}   {tag}   {r['index']:6d}")
    print("\n  full per-s curve at the largest kseed tested:")
    kseed = kseeds[-1]
    for phase in (0, 1):
        tag = "01" if phase == 0 else "10"
        print(f"  phase {tag}:")
        for s in range(pairs):
            r = headline[kseed][phase][s]
            print(f"    s={s:3d}  index={r['index']:7d}  "
                  f"n_prefixes={r['n_prefixes']:7d}  "
                  f"anomalies={r['n_anomalous_prefixes']:5d}")
    return headline


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", choices=["30", "90"], default="30")
    ap.add_argument("--pairs", type=int, default=20)
    ap.add_argument("--W", type=int, default=30)
    ap.add_argument("--kseeds", type=int, nargs="+", default=KSEEDS)
    a = ap.parse_args()
    sweep(a.kind, a.pairs, a.W, a.kseeds)


if __name__ == "__main__":
    main()

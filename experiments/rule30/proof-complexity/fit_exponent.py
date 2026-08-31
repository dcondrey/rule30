"""Fit log(mus_cells) vs log(n) for a ladder JSON; report per-seed spread."""
import json
import logging
import sys

import numpy as np

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("fit")


def main(paths):
    for p in paths:
        bands = json.load(open(p))
        rows = []
        for b in bands:
            if not b["runs"]:
                continue
            sizes = [r["mus_cells"] for r in b["runs"]]
            rows.append((b["n"], min(sizes), max(sizes), b["diamond_cells"],
                         b["trimmed_core"], b["seconds"]))
        log.info(f"\n{p}  (rule {bands[0]['rule']}, group {bands[0]['group']})")
        log.info("   n   mus_min  mus_max  diamond  trimmed   sec   fill%")
        for n, lo, hi, d, tc, sec in rows:
            log.info(f"{n:5d}  {lo:7d}  {hi:7d}  {d:7d}  {tc:7d}  {sec:6.1f}"
                  f"  {100*hi/d:5.1f}")
        pts = [(n, (lo + hi) / 2) for n, lo, hi, *_ in rows if n >= 16]
        if len(pts) >= 3:
            x = np.log([p_[0] for p_ in pts])
            y = np.log([p_[1] for p_ in pts])
            slope = np.polyfit(x, y, 1)[0]
            top = np.polyfit(x[-3:], y[-3:], 1)[0]
            log.info(f"exponent (all n>=16): {slope:.3f}   local (top 3): {top:.3f}")
        else:
            log.info("fewer than 3 bands with n>=16; no fit")


if __name__ == "__main__":
    main(sys.argv[1:])

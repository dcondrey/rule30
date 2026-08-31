"""Bit-parallel size of the backward slice of the row-simulation derivation.

The sliced derivation (p3_core.derive_sliced) costs a fixed 2-3 resolution
steps per RETAINED cell, so its length is Theta(|slice|).  This script measures
|slice(n)| far past the range where the full proof object can be built, for
rule 30 and the rule 90 control, under three antecedent-choice policies.

Validated against the explicit set from p3_core.backward_slice at small n.

Run:
    /Volumes/A/researchpapers/.venv/bin/python p3_slice_ladder.py --out slice.json
"""

from __future__ import annotations

import argparse
import json
import logging
import math


def truth_rows(rule: int, n: int) -> list[int]:
    """rows[t] = int whose bit (x + n) is s(t,x)."""
    off = n
    row = 1 << off
    rows = [row]
    full = (1 << (2 * n + 3)) - 1
    for _ in range(n):
        if rule == 30:
            row = ((row << 1) ^ (row | (row >> 1))) & full
        else:
            row = ((row << 1) ^ (row >> 1)) & full
        rows.append(row)
    return rows


def band(n: int, t: int) -> int:
    """Mask of the diamond cells in row t: |x| <= min(t, n-t)."""
    w = min(t, n - t)
    return ((1 << (2 * w + 1)) - 1) << (n - w)


def slice_size(rule: int, n: int, policy: str = "adaptive") -> tuple[int, list[int]]:
    rows = truth_rows(rule, n)
    need = 1 << n  # (n, 0)
    total = 1
    per_row = [0] * (n + 1)
    per_row[n] = 1
    for t in range(n, 0, -1):
        R = rows[t - 1]
        M = R  # truth at x
        Rr = R >> 1  # truth at x + 1
        N = need
        if rule == 90:
            nxt = (N >> 1) | (N << 1)
        else:
            both = N & M & Rr
            onlym = N & M & ~Rr
            onlyr = N & ~M & Rr
            none = N & ~M & ~Rr
            base = (N >> 1) | onlym | none | ((onlyr | none) << 1)
            if policy == "centre":
                nxt = base | both
            elif policy == "right":
                nxt = base | (both << 1)
            else:  # adaptive: reuse a parent that is already needed
                take_m = both & base
                rest = both & ~base
                take_r = rest & (base >> 1)
                rest2 = rest & ~(base >> 1)
                nxt = base | take_m | rest2 | (take_r << 1)
        nxt &= band(n, t - 1)
        need = nxt
        c = bin(need).count("1")
        per_row[t - 1] = c
        total += c
    return total, per_row


def diamond_cells(n: int) -> int:
    return sum(2 * min(t, n - t) + 1 for t in range(n + 1))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ns", type=int, nargs="+",
                    default=[16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192])
    ap.add_argument("--out", default="slice.json")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    # validation against the explicit construction
    import p3_core as P
    for rule in (30, 90):
        for n in (4, 8, 16, 32):
            ref = len(P.backward_slice(rule, n, "greedy"))
            got, _ = slice_size(rule, n, "centre")
            assert got == ref, (rule, n, got, ref)
    logging.info("VALIDATION ok: bit-parallel slice == explicit slice (policy centre)")

    out = {}
    for rule in (30, 90):
        rows = []
        for n in a.ns:
            d = diamond_cells(n)
            rec = {"n": n, "diamond": d}
            for pol in ("centre", "right", "adaptive"):
                s, _ = slice_size(rule, n, pol)
                rec[pol] = s
            rec["best"] = min(rec[p] for p in ("centre", "right", "adaptive"))
            rec["fill"] = rec["best"] / d
            rows.append(rec)
            logging.info(
                "rule %d n=%-5d diamond=%-9d centre=%-9d right=%-9d adaptive=%-9d "
                "fill=%.4f",
                rule, n, d, rec["centre"], rec["right"], rec["adaptive"], rec["fill"],
            )
        # least-squares exponent of best vs n
        xs = [math.log(r["n"]) for r in rows]
        ys = [math.log(r["best"]) for r in rows]
        k = len(xs)
        mx, my = sum(xs) / k, sum(ys) / k
        slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum(
            (x - mx) ** 2 for x in xs
        )
        loc = (ys[-1] - ys[-3]) / (xs[-1] - xs[-3]) if k >= 3 else float("nan")
        logging.info("rule %d fitted exponent %.4f  local (top 3) %.4f", rule, slope, loc)
        out[str(rule)] = {"rows": rows, "exponent": slope, "local_exponent": loc}
    with open(a.out, "w") as f:
        json.dump(out, f, indent=1)
    logging.info("wrote %s", a.out)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fiber dump, missing-block census, and extremal-continuation census for
the D_k image analysis (items 1-3 of the fiber/extremal-family follow-up).

Computes table+images once per (n,tail) via continuation_image_analysis.d_k_table
and derives everything else from that single pass (no separate re-derivation
per section, to keep n=16 runs affordable).
"""
from __future__ import annotations

import json

from continuation_image_analysis import d_k_table, fib
from rank_zero_separator import hard_core_prefixes


def fmt(word):
    return "".join(map(str, word))


def longest_common_suffix(words):
    if not words:
        return ()
    minlen = min(len(w) for w in words)
    suffix = []
    for i in range(1, minlen + 1):
        vals = {w[-i] for w in words}
        if len(vals) == 1:
            suffix.append(next(iter(vals)))
        else:
            break
    return tuple(reversed(suffix))


def analyze(n, tail, residue=0, fiber_depths=4):
    table, images = d_k_table(n, tail, residue)
    nonzero_ks = [k for k, f, d in table if d > 0]
    k_star = next((k for k, f, d in table if d < f), None)
    k_max = nonzero_ks[-1] if nonzero_ks else None

    # --- item 1: fiber dump at the last few nonzero depths ---
    dump_ks = nonzero_ks[-fiber_depths:] if nonzero_ks else []
    fibers = {}
    for k in dump_ks:
        entries = []
        for C, ws in images[k].items():
            suffix = longest_common_suffix(ws)
            residuals = sorted({fmt(w[: len(w) - len(suffix)]) for w in ws})
            entries.append(
                {
                    "C": fmt(C),
                    "fiber_size": len(ws),
                    "fiber_words": sorted(fmt(w) for w in ws),
                    "common_suffix": fmt(suffix),
                    "residual_prefixes": residuals,
                }
            )
        entries.sort(key=lambda e: -e["fiber_size"])
        fibers[k] = entries

    # --- item 2: missing-block census at k_star ---
    missing = None
    present = None
    if k_star is not None:
        hc = {fmt(w) for w in hard_core_prefixes(k_star)}
        present = sorted(fmt(c) for c in images[k_star].keys())
        missing = sorted(hc - set(present))

    # --- item 3: extremal continuation(s) at k_max ---
    extremal = sorted(fmt(c) for c in images[k_max].keys()) if k_max else []
    extremal_fiber_sizes = (
        {fmt(c): len(ws) for c, ws in images[k_max].items()} if k_max else {}
    )

    return {
        "n": n,
        "tail": tail,
        "table": table,
        "k_star": k_star,
        "k_max": k_max,
        "dump_ks": dump_ks,
        "fibers": fibers,
        "missing_at_k_star": missing,
        "present_at_k_star": present,
        "extremal_at_k_max": extremal,
        "extremal_fiber_sizes": extremal_fiber_sizes,
    }


def main():
    ns = list(range(10, 17))
    tails = (2, 3)
    out = {}
    for tail in tails:
        for n in ns:
            key = f"n{n}_c{tail}"
            print(f"analyzing {key} ...", flush=True)
            out[key] = analyze(n, tail)
            print(
                f"  k_star={out[key]['k_star']} k_max={out[key]['k_max']} "
                f"extremal={out[key]['extremal_at_k_max']} "
                f"missing_count={len(out[key]['missing_at_k_star'] or [])}",
                flush=True,
            )
    with open("fiber_full_analysis.json", "w") as f:
        json.dump(out, f, indent=1)
    print("wrote fiber_full_analysis.json")


if __name__ == "__main__":
    main()

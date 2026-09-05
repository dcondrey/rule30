#!/usr/bin/env python3
"""Fresh recompute of D_k tables, k_star(n), fibers at the last nonzero
depths, missing-block sets, and extremal-continuation census for the
fiber/extremal-family follow-up (RESULTS-FIBER-EXTREMAL-FAMILY.md).

Deliberately re-derives everything from continuation_image_analysis.d_k_table
(itself built directly on late_pull_diagonal_sat.literal_extension) rather
than trusting any previously reported table.
"""
from __future__ import annotations

import json
from itertools import product

from continuation_image_analysis import d_k_table, fib


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


def is_hard_core(word):
    return all(v in (1, 2) for v in word) and all(
        not (a == 1 and b == 1) for a, b in zip(word, word[1:])
    )


def hard_core_words(k):
    return [w for w in product((1, 2), repeat=k) if is_hard_core(w)]


def scan(n, tail, residue=0):
    table, images = d_k_table(n, tail, residue)
    k_star = next((k for k, f, d in table if d < f), None)
    return table, images, k_star


def main():
    ns = list(range(10, 17))
    tails = (2, 3)
    summary = {}
    for tail in tails:
        for n in ns:
            table, images, k_star = scan(n, tail)
            summary[(n, tail)] = {
                "table": table,
                "k_star": k_star,
                "images": images,
            }
            print(f"n={n:2d} c={tail} k_star={k_star}  "
                  f"table={[(k,f,d) for k,f,d in table]}")
    # dump raw (n,tail)->table for reuse by other scripts without recompute
    out = {
        f"n{n}_c{tail}": {
            "table": summary[(n, tail)]["table"],
            "k_star": summary[(n, tail)]["k_star"],
        }
        for n in ns for tail in tails
    }
    with open("fiber_extremal_scan_summary.json", "w") as f:
        json.dump(out, f, indent=1)
    print("wrote fiber_extremal_scan_summary.json")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Throwaway check (not wired into pipeline): does dropping one endpoint
coordinate at position p from a length-n endpoint sequence give a length-
(n-1) endpoint whose diagonal reproduces the FULL-length endpoint's DEEPEST
cut coordinate (the one H_r(n)/RW actually reads) at some fixed index that
depends only on (n, p), not on the sequence's values?

Earlier version of this script used a weak criterion (any partial-overlap
agreement under any shift) and reported 100% match at every n for
drop-first -- that was checking only a small fixed-size window near the
START of the diagonal (the shift left almost no overlap in range), not the
deep coordinate the reduction actually needs. Fixed here: check the single
deepest entry only, against the real Endpoint class (psi_kernel.py).
"""
from __future__ import annotations

from itertools import product

from psi_kernel import Endpoint


def build(seq):
    st = Endpoint()
    for s in seq:
        st.append(s)
    return st


def check(n: int):
    seqs = list(product(range(4), repeat=n))
    results = {}
    for p in range(n):
        # For each candidate target index m in short's diagonal (0..n-2),
        # count how many sequences have short.diagonal[m] == full.diagonal[-1].
        counts = [0] * (n - 1)
        for seq in seqs:
            full = build(seq)
            short_seq = seq[:p] + seq[p + 1 :]
            short = build(short_seq)
            target = full.diagonal[-1]
            for m in range(n - 1):
                if short.diagonal[m] == target:
                    counts[m] += 1
        best_m = max(range(n - 1), key=lambda m: counts[m])
        results[p] = (best_m, counts[best_m])
    return results, len(seqs)


def main():
    for n in range(2, 9):
        results, total = check(n)
        best_p = max(results, key=lambda p: results[p][1])
        best_m, best_count = results[best_p]
        print(
            f"n={n:2d} total={total:6d} best_drop_pos={best_p} "
            f"best_target_index={best_m} exact_match_count={best_count:6d} "
            f"(fraction={best_count / total:.4f})  all={results}"
        )


if __name__ == "__main__":
    main()

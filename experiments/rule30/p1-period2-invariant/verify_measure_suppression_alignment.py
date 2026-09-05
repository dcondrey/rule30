#!/usr/bin/env python3
"""Throwaway V3(b) cross-check for PREREGISTRATION-MEASURE-SUPPRESSION.md.

Not wired into any pipeline. Confirms rw_population_h.survival_curve's
alive_after[j] (hard-core survival of late_pull_diagonal_sat.literal_extension's
forced continuation) equals block_halving.chains' src[j] (hard-core AND
cells[w][j]==c survival of the independently-coded psi_kernel/flip_pairing
forced continuation), at the SAME index j -- the two conditions are the same
composite once literal_extension's exact-tail-match forcing is decomposed
into (H==1, low bit==tail), since both tails in use (2,3) have H==1. Does
not modify rw_population_h.py, flip_pairing.py or block_halving.py; only
imports and calls them as-is.
"""
from __future__ import annotations

from rw_population_h import survival_curve, forward_filter
from late_pull_diagonal_sat import literal_extension
from flip_pairing import census as fp_census
from block_halving import chains
from itertools import product


def check_alignment(n_values=(9, 10, 11, 12), tails=(2, 3)) -> None:
    for n in n_values:
        levels = n + 4
        keys, syms, cells, hcs = fp_census(n, levels)
        for tail in tails:
            # survival_curve(n, tail, residue) internally sets rows = n+residue+2 and
            # iterates literal_extension(word, tail, rows) that far; residue only
            # extends the array length (more forced rows appended past the shared
            # prefix), it does not change any already-computed alive_after[j] for
            # j <= rows, so residue=0 here gives a prefix valid for comparison at
            # any j within its own length regardless of which residue is later used.
            alive = survival_curve(n, tail, 0)
            src, _sts = chains(n, tail, levels, keys, cells, hcs)
            m = min(len(alive), len(src))
            match = all(alive[j] == src[j] for j in range(m))
            print(f"n={n} tail={tail}: alive_after[:{m}] == src[:{m}]  -> {match}")
            print("   alive_after:", alive[:m])
            print("   src        :", src[:m])


def check_word_level_alignment(n_values=(9, 10), tails=(2, 3)) -> None:
    """Per-word check: does literal_extension's own death level match
    flip_pairing/block_halving's death level for the SAME word (indexed the
    same way census() indexes it: bit i of idx set iff src[i]==2, per
    census()'s own comment), not just the same count at each level?
    """
    for n in n_values:
        levels = n + 4
        keys, syms, cells, hcs = fp_census(n, levels)
        for tail in tails:
            # literal_extension-side death level per word, same indexing as
            # product((1,2), repeat=n) / census()'s idx convention.
            le_death = []
            for word in product((1, 2), repeat=n):
                continuation = literal_extension(word, tail, levels)
                previous = word[-1]
                d = levels
                for j, value in enumerate(continuation):
                    if value not in (1, 2) or previous == value == 1:
                        d = j
                        break
                    previous = value
                le_death.append(d)
            # flip_pairing-side death level per word (chains()'s own predicate,
            # kept per-word instead of aggregated).
            fp_death = []
            total = 1 << n
            for w in range(total):
                d = levels
                for j in range(levels):
                    if not hcs[w][j] or cells[w][j] != tail:
                        d = j
                        break
                fp_death.append(d)
            mismatches = sum(1 for a, b in zip(le_death, fp_death) if a != b)
            print(
                f"n={n} tail={tail}: word-level death-level mismatches = "
                f"{mismatches}/{total}"
            )
            if mismatches:
                for idx, (a, b) in enumerate(zip(le_death, fp_death)):
                    if a != b:
                        print(f"    first mismatch idx={idx}: literal_extension={a} flip_pairing={b}")
                        break


def check_subset_bound(n_values=range(1, 6), tails=(2, 3), residues=(0, 1, 2)) -> None:
    for n in n_values:
        for tail in tails:
            for r in residues:
                rows = n + r + 2
                alive = survival_curve(n, tail, r)
                n_full = alive[rows] if rows < len(alive) else None
                hr = sum(1 for w in product((1, 2), repeat=n) if forward_filter(w, tail, r))
                print(f"n={n} tail={tail} r={r} rows={rows} N_[rows]={n_full} |H_r(n)|={hr} subset_ok={hr <= (n_full or 0)}")


if __name__ == "__main__":
    check_alignment()
    check_word_level_alignment()
    check_subset_bound()

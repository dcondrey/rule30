#!/usr/bin/env python3
"""Analyze the continuation map Phi_k: {1,2}^n survivors -> hard-core words
of length k, built directly from late_pull_diagonal_sat.literal_extension.

D_k = |image(Phi_k)| (distinct forced-continuation prefixes of length k
among still-alive source words). Compares against the exact hard-core
language size Fib(k+1) (2,3,5,8,13,21,34,...): D_k == Fib(k+1) means Phi_k
is surjective onto the whole hard-core shift at that depth.
"""
from __future__ import annotations

from itertools import product

from late_pull_diagonal_sat import literal_extension


def fib(k: int) -> int:
    a, b = 1, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def full_continuations(n: int, tail: int, residue: int):
    """Return, for every W, its full forced continuation up to the point
    it dies (or the full requested length if it survives to the end)."""
    target = n + residue
    rows = target + 2
    out = []
    for w in product((1, 2), repeat=n):
        cont = literal_extension(w, tail, rows)
        prev = w[-1]
        fail_at = None
        for i, v in enumerate(cont):
            if v not in (1, 2) or (prev == 1 and v == 1):
                fail_at = i
                break
            prev = v
        survived = rows if fail_at is None else fail_at
        out.append((w, cont[:survived], survived))
    return out, rows


def d_k_table(n: int, tail: int, residue: int, kmax: int | None = None):
    data, rows = full_continuations(n, tail, residue)
    kmax = kmax or rows
    images = {k: {} for k in range(1, kmax + 1)}  # k -> {prefix: [W,...]}
    for w, cont, survived in data:
        for k in range(1, min(survived, kmax) + 1):
            prefix = cont[:k]
            images[k].setdefault(prefix, []).append(w)
    table = []
    for k in range(1, kmax + 1):
        table.append((k, fib(k + 1), len(images[k])))
    return table, images


def main():
    import sys

    n = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    tail = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    residue = int(sys.argv[3]) if len(sys.argv) > 3 else 0

    table, images = d_k_table(n, tail, residue)
    print(f"n={n} c={tail} r={residue}")
    print(" k   Fib(k+1)   D_k   surjective?")
    for k, f, d in table:
        print(f"{k:3d}   {f:8d}   {d:5d}   {'yes' if d == f else 'no'}")

    # first non-surjective k
    k_star = next((k for k, f, d in table if d < f), None)
    print(f"\nk_star (first non-surjective depth) = {k_star}")


if __name__ == "__main__":
    main()

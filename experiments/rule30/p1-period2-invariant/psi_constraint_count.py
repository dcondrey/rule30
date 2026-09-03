#!/usr/bin/env python3
"""Constraint-satisfaction count for the binary-wedge defect word.

Runs the statistic pre-registered in ``PREREG-psi-constraint-counting.md``:
for each source length ``n`` and each prefix length ``k``, count the binary
sources whose defect word ``Psi_n(W)`` is constant on ``Psi_0..Psi_k``, and
compare against the independence null ``2^(n-k)``.

The null matters because it is not obviously wrong.  ``Psi`` has ``n+2``
coordinates and the source has ``n`` bits, so a coin-flip model predicts a
constant-``Psi`` source for a fixed positive fraction of every ``n``, hence
infinitely many counterexamples to ``(BWH+)``.  Measuring the ratio decides
whether the recorded empty census is structure or luck.
"""

from __future__ import annotations

import argparse
from itertools import product

from psi_kernel import psi


def counts(length: int) -> list[int]:
    """``N_k`` for ``k = 0 .. length+1``, pooled over both constant values."""
    tallies = [0] * (length + 2)
    for source in product((1, 2), repeat=length):
        _, word = psi(source)
        run = 1
        while run < len(word) and word[run] == word[0]:
            run += 1
        # Constant on Psi_0..Psi_k exactly for k < run.
        for k in range(run):
            tallies[k] += 1
    return tallies


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-source", type=int, default=7)
    parser.add_argument("--max-source", type=int, default=18)
    args = parser.parse_args()

    print("n   k   N_k        null=2^(n-k)   R_k")
    for length in range(args.min_source, args.max_source + 1):
        tallies = counts(length)
        for k, value in enumerate(tallies):
            null = 2.0 ** (length - k)
            ratio = value / null
            flag = "" if value else "   <- empty"
            print(f"{length:<4}{k:<4}{value:<11}{null:<15.4g}{ratio:.4f}{flag}")
            if value == 0:
                break
        print()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Algebraic degree of Psi and Delta as Boolean functions of the source.

`PROOF-STATE-CAPSULE.md` section 7 makes the fallback to DLP/RW conditional on
the complete-state recursion fanning out.  Full algebraic degree is the exact
form of that condition for a bounded-arity seam law: if `Delta_j` has degree
`n` in the `n` source bits, no recursion of bounded arity computes it.

Encodes symbol `1` as bit `0` and `2` as bit `1`, takes the Moebius transform
of each coordinate over all `2^n` sources, and reports the largest monomial
weight with a nonzero coefficient.
"""

from __future__ import annotations

import argparse

from psi_kernel import psi


def moebius(values: list[int]) -> list[int]:
    coefficients = values[:]
    step = 1
    while step < len(coefficients):
        for block in range(0, len(coefficients), step * 2):
            for index in range(block, block + step):
                coefficients[index + step] ^= coefficients[index]
        step *= 2
    return coefficients


def degrees(length: int) -> tuple[list[int], list[int]]:
    size = 1 << length
    words = []
    for index in range(size):
        source = tuple(2 if (index >> k) & 1 else 1 for k in range(length))
        words.append(psi(source)[1])

    def degree(column: list[int]) -> int:
        anf = moebius(column)
        return max((bin(m).count("1") for m in range(size) if anf[m]), default=0)

    psi_degrees = [degree([w[j] for w in words]) for j in range(length + 2)]
    delta_degrees = [
        degree([w[j] ^ w[j + 1] for w in words]) for j in range(length + 1)
    ]
    return psi_degrees, delta_degrees


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-source", type=int, default=4)
    parser.add_argument("--max-source", type=int, default=15)
    args = parser.parse_args()
    for length in range(args.min_source, args.max_source + 1):
        psi_degrees, delta_degrees = degrees(length)
        print(
            f"n={length:<3} deg(Psi) in [{min(psi_degrees)},{max(psi_degrees)}]"
            f"   max deg(Delta)={max(delta_degrees)}   (n={length})"
        )


if __name__ == "__main__":
    main()

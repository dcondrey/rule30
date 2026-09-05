#!/usr/bin/env python3
"""Section 4 measurement for PREREGISTRATION-RW-FORCED-TERMINAL-DEFECT.md.

H_r(n) = {W in {1,2}^n : literal_extension(W, c, n+r+2) survives the
hard-core and 12a-terminal checks in rotated_wedge_witness}, i.e. the
population for which an RW witness is even a live possibility, before
asking about constancy.  Reports |H_r(n)| and |H_r(n)| / 2^n for each
(n, r, c).

Control #1 (prereg section 5): H_r(n) is computed two independent ways
per word and the two must agree exactly on every W:
  - ``forward_filter``: a fresh hard-core/12a filter over the word
    ``word + literal_extension(word, tail, target + 2)``, written without
    reference to dlp_rotated_wedge.
  - ``via_rotated``: dlp_rotated_wedge.rotated_wedge_population's own
    ``surviving``/``terminal_pull`` booleans, unmodified.
Control #3: report the exact count alongside the ratio, not the ratio
alone.
"""

from __future__ import annotations

import argparse
import time
from itertools import product

from constant_tail_scale import Vector
from late_pull_diagonal_sat import literal_extension
from dlp_rotated_wedge import rotated_wedge_population


def forward_filter(word: Vector, tail: int, residue: int) -> bool:
    """Independent hard-core + 12a-terminal filter, not via rotated_wedge_population."""

    n = len(word)
    target = n + residue
    continuation = literal_extension(word, tail, target + 2)
    assert len(continuation) == target + 2

    previous = word[-1]
    for value in continuation:
        if value not in (1, 2):
            return False
        if previous == value == 1:
            return False
        previous = value

    return continuation[-3:-1] == (1, 2)


def via_rotated(word: Vector, tail: int, residue: int) -> bool:
    surviving, terminal_pull, _ = rotated_wedge_population(word, tail, residue)
    return surviving and terminal_pull


def survival_curve(n: int, tail: int, residue: int) -> list[int]:
    """Return alive_after[k] = count of W in {1,2}^n whose continuation

    survives hard-core through its first k appended rows (alive_after[0] is
    all 2^n words; alive_after[len(rows)] is exactly |H_r(n)|, restricted to
    the hard-core condition only -- the terminal_pull check is applied
    separately since it only concerns the last two rows).  Diagnostic for
    whether the decay is a smooth per-row rate or has a parity/offset
    structure, not itself a control target.
    """

    target = n + residue
    rows = target + 2
    alive_after = [0] * (rows + 1)
    for word in product((1, 2), repeat=n):
        continuation = literal_extension(word, tail, rows)
        previous = word[-1]
        fail_at = None
        for i, value in enumerate(continuation):
            if value not in (1, 2) or previous == value == 1:
                fail_at = i
                break
            previous = value
        survived_through = rows if fail_at is None else fail_at
        for k in range(1, survived_through + 1):
            alive_after[k] += 1
    # alive_after[0] should equal 2**n (every word is "alive" before row 0)
    alive_after[0] = 2 ** n
    return alive_after


def fit_geometric_rate(alive_after: list[int]) -> float | None:
    """Least-squares log-linear rate of alive_after, ignoring zero/short tail."""

    import math

    points = [(k, math.log(v)) for k, v in enumerate(alive_after) if v > 0]
    if len(points) < 3:
        return None
    n = len(points)
    sx = sum(k for k, _ in points)
    sy = sum(y for _, y in points)
    sxx = sum(k * k for k, _ in points)
    sxy = sum(k * y for k, y in points)
    denom = n * sxx - sx * sx
    if denom == 0:
        return None
    slope = (n * sxy - sx * sy) / denom
    return math.exp(slope)


def census(max_source: int, tail: int, residue: int):
    """Yield (n, count, 2**n) as each n finishes, instead of batching."""
    for n in range(1, max_source + 1):
        count = 0
        for word in product((1, 2), repeat=n):
            direct = forward_filter(word, tail, residue)
            rotated = via_rotated(word, tail, residue)
            assert direct == rotated, (
                "H_r(n) constructions disagree",
                word,
                tail,
                residue,
                direct,
                rotated,
            )
            if direct:
                count += 1
        yield (n, count, 2 ** n)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-source", type=int, default=18)
    parser.add_argument("--residues", type=int, nargs="+", default=[0, 1, 2])
    parser.add_argument("--tails", type=int, nargs="+", default=[2, 3])
    parser.add_argument("--curve-n", type=int, default=0)
    args = parser.parse_args()

    for residue in args.residues:
        for tail in args.tails:
            print(f"\n--- r={residue} c={tail} (both constructions agree per-word) ---", flush=True)
            print(" n   |H_r(n)|   2^n        ratio", flush=True)
            start = time.time()
            for n, count, total in census(args.max_source, tail, residue):
                ratio = count / total
                n_elapsed = time.time() - start
                print(f"{n:3d}   {count:8d}   {total:10d}   {ratio:.6f}   ({n_elapsed:.1f}s cum)", flush=True)
            elapsed = time.time() - start
            print(f"  ({elapsed:.1f}s)", flush=True)

            if args.curve_n:
                curve = survival_curve(args.curve_n, tail, residue)
                rate = fit_geometric_rate(curve)
                print(f"  per-row hard-core survival curve, n={args.curve_n}:")
                print("   row  alive_after   row_ratio")
                prev = curve[0]
                for k, count in enumerate(curve):
                    ratio = count / prev if prev else float("nan")
                    print(f"  {k:5d}  {count:10d}   {ratio:.4f}")
                    prev = count
                if rate is not None:
                    print(f"  fitted per-row geometric rate: {rate:.4f}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Actual-right refinement of the constant-tail scale obstruction.

The rank-lowering prefix ``2^m`` destroys literal right-trace realizability,
but only in a finite endpoint prefix.  Starting from a genuine period-two
counterexample, every sufficiently late scale block is therefore still a
factor of a genuine alternating-center right trace.  This script intersects
the scale map ``R_c`` with that right language in two exact stages:

* a cheap regular over-approximation by every proved minimal forbidden factor
  through length 11; and
* optional SAT membership in the complete finite right-light-cone language.

All scale and SAT bounds printed here are finite evidence.  The eventual-
actual-right reduction is uniform; the censuses are not its proof.
"""

from __future__ import annotations

import argparse
from collections.abc import Iterable

from constant_tail_scale import scale_extension


Vector = tuple[int, ...]

# Each word was excluded by complete right-light-cone enumeration.  Because
# advancing one rho coordinate is a two-time-step shift, the alternating
# center phase is preserved and every forbidden prefix is a forbidden factor.
PROVED_FORBIDDEN = (
    "11",
    "00000",
    "101001",
    "0100101",
    "010010001",
    "0101000101",
    "0101010000",
    "01010001001",
    "10010001001",
)


def legal_append(word: str, bit: str) -> bool:
    following = word + bit
    return all(not following.endswith(pattern) for pattern in PROVED_FORBIDDEN)


def filtered_words(length: int) -> list[tuple[Vector, str]]:
    frontier: list[tuple[Vector, str]] = [((), "")]
    for _ in range(length):
        frontier = [
            (word + (state,), bits + bit)
            for word, bits in frontier
            for state, bit in ((1, "1"), (2, "0"))
            if legal_append(bits, bit)
        ]
    return frontier


def filtered_survival(bits: str, extension: Vector) -> tuple[int, str]:
    continuation = []
    for index, state in enumerate(extension):
        if state not in (1, 2):
            return index, "".join(continuation)
        bit = "1" if state == 1 else "0"
        if not legal_append(bits, bit):
            return index, "".join(continuation)
        bits += bit
        continuation.append(bit)
    return len(extension), "".join(continuation)


def filtered_candidates(
    length: int, tail: int
) -> list[tuple[int, str, str]]:
    answer = []
    for word, bits in filtered_words(length):
        survival, continuation = filtered_survival(
            bits, scale_extension(word, tail)
        )
        answer.append((survival, bits, continuation))
    return sorted(answer, reverse=True)


def right_trace_realizable(bits: str) -> bool:
    """Decide exact membership by the complete finite right light cone."""

    # These dependencies live in the existing PySAT project.  Keeping the
    # import lazy lets the regular prefilter run with the standard library.
    from joint_mortality import right_trace
    from mortality_sat import Encoder
    from pysat.solvers import Solver

    encoder = Encoder()
    trace, _ = right_trace(encoder, len(bits))
    for literal, bit in zip(trace, bits, strict=True):
        encoder.add(literal if bit == "1" else -literal)
    with Solver(
        name="cadical195", bootstrap_with=encoder.clauses
    ) as solver:
        return solver.solve()


def actual_census(
    candidates: Iterable[tuple[int, str, str]]
) -> tuple[int, str, int]:
    """Return exact actual-right survival, witness, and SAT query count."""

    best = -1
    witness = ""
    queries = 0
    for upper, bits, continuation in candidates:
        if upper <= best:
            break
        for length in range(upper, best, -1):
            queries += 1
            whole = bits + continuation[:length]
            if right_trace_realizable(whole):
                best = length
                witness = whole
                break
    return best, witness, queries


EXPECTED_ACTUAL = {
    10: {2: 4, 3: 5},
    15: {2: 4, 3: 3},
    20: {2: 4, 3: 4},
    24: {2: 4, 3: 5},
    27: {2: 5, 3: 5},
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-scale", type=int, default=18)
    parser.add_argument("--actual-scales", type=int, nargs="*", default=[])
    args = parser.parse_args()
    if args.max_scale < 1 or any(length < 1 for length in args.actual_scales):
        parser.error("scale lengths must be positive")

    actual = set(args.actual_scales)
    requested = sorted(set(range(1, args.max_scale + 1)) | actual)
    for length in requested:
        count = len(filtered_words(length))
        fields = []
        for tail in (2, 3):
            candidates = filtered_candidates(length, tail)
            maximum, bits, continuation = candidates[0]
            field = (
                f"tail={tail} filtered-max={maximum:2d} "
                f"W={bits} continuation={continuation}"
            )
            if length in actual:
                best, witness, queries = actual_census(candidates)
                if length in EXPECTED_ACTUAL:
                    assert best == EXPECTED_ACTUAL[length][tail]
                field += (
                    f" actual-max={best:2d} SAT-queries={queries} "
                    f"actual-witness={witness}"
                )
            fields.append(field)
        print(f"scale={length:2d} filtered-inputs={count:6d} " + " | ".join(fields))


if __name__ == "__main__":
    main()

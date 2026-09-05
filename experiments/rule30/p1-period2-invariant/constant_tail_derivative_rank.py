#!/usr/bin/env python3
"""Exact F2-rank audit of affine intervention derivatives at scale."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from constant_tail_ordered_matching import correction_count, forced_trace
from constant_tail_scale import Vector, hard_core_extension_length
from rank_zero_separator import hard_core_prefixes


COORDINATE_SETS = {
    "a": ("alpha",),
    "b": ("beta",),
    "g": ("gamma",),
    "ab": ("alpha", "beta"),
    "ag": ("alpha", "gamma"),
    "bg": ("beta", "gamma"),
    "abg": ("alpha", "beta", "gamma"),
}


def binary_rank(vectors: list[int]) -> int:
    """Rank of binary vectors represented as nonnegative integers."""

    basis: dict[int, int] = {}
    for vector in vectors:
        while vector:
            pivot = vector.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = vector
                break
            vector ^= basis[pivot]
    return len(basis)


def derivative_coordinate_rows(
    word: Vector, tail: int, survival: int
) -> tuple[dict[str, list[int]], int]:
    """Return all three coordinate row families and the source-column count."""

    _, original = forced_trace(word, tail)
    sources = [index for index, value in enumerate(word) if value == 2]
    rows = {
        coordinate: [0] * survival
        for coordinate in ("alpha", "beta", "gamma")
    }
    for column, source in enumerate(sources):
        intervened = word[:source] + (1,) + word[source + 1 :]
        _, changed = forced_trace(intervened, tail)
        for step in range(survival):
            for coordinate in rows:
                if getattr(original[step].affine, coordinate) != getattr(
                    changed[step].affine, coordinate
                ):
                    rows[coordinate][step] |= 1 << column
    return rows, len(sources)


def column_rank(rows: list[int], columns: int) -> int:
    """Independent transpose construction for the registered small control."""

    vectors = [0] * columns
    for row_index, row in enumerate(rows):
        for column in range(columns):
            if row & (1 << column):
                vectors[column] |= 1 << row_index
    return binary_rank(vectors)


@dataclass(slots=True)
class Result:
    cases: int = 0
    failures: int = 0
    minimum_slack: int = 10**9
    minimum_witness: str = ""
    maximum_nullity: int = -1
    nullity_witness: str = ""
    prefix_failures: int = 0
    minimum_prefix_slack: int = 10**9
    first_prefix_failure: str | None = None
    first_failure: str | None = None


def audit_case(
    word: Vector,
    tail: int,
    results: dict[str, Result],
    cross_check: bool,
) -> dict[str, tuple[int, int, int]]:
    extension, _ = forced_trace(word, tail)
    survival = hard_core_extension_length(word, extension)
    correction = correction_count(word, tail)
    target = max(0, survival - correction)
    answer: dict[str, tuple[int, int, int]] = {}
    coordinate_rows, columns = derivative_coordinate_rows(word, tail, survival)
    for name, coordinates in COORDINATE_SETS.items():
        rows = [
            coordinate_rows[coordinate][step]
            for step in range(survival)
            for coordinate in coordinates
        ]
        rank = binary_rank(rows)
        if cross_check:
            assert rank == column_rank(rows, columns)
        slack = rank - target
        nullity = columns - rank
        description = (
            f"tail={tail} W={''.join(map(str, word))} s={survival} "
            f"K={correction} #2={columns} rank={rank} target={target} "
            f"slack={slack}"
        )
        result = results[name]
        result.cases += 1
        if slack < result.minimum_slack:
            result.minimum_slack = slack
            result.minimum_witness = description
        if nullity > result.maximum_nullity:
            result.maximum_nullity = nullity
            result.nullity_witness = description
        if slack < 0:
            result.failures += 1
            if result.first_failure is None:
                result.first_failure = description
        width = len(coordinates)
        for prefix in range(survival + 1):
            prefix_rank = binary_rank(rows[: prefix * width])
            prefix_target = max(0, prefix - correction)
            prefix_slack = prefix_rank - prefix_target
            if prefix_slack < result.minimum_prefix_slack:
                result.minimum_prefix_slack = prefix_slack
            if prefix_slack < 0:
                result.prefix_failures += 1
                if result.first_prefix_failure is None:
                    result.first_prefix_failure = (
                        f"{description} prefix={prefix} "
                        f"prefix-rank={prefix_rank} "
                        f"prefix-target={prefix_target}"
                    )
        answer[name] = (rank, target, slack)
    return answer


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-length", type=int, default=16)
    parser.add_argument("--cross-check-length", type=int, default=6)
    args = parser.parse_args()
    if args.max_length < 1 or args.cross_check_length < 0:
        parser.error("length bounds must be nonnegative and max length positive")

    results = {name: Result() for name in COORDINATE_SETS}
    for length in range(1, args.max_length + 1):
        for word in hard_core_prefixes(length):
            for tail in (2, 3):
                audit_case(
                    word,
                    tail,
                    results,
                    cross_check=length <= args.cross_check_length,
                )
        fields = " ".join(
            f"{name}:min={results[name].minimum_slack}"
            for name in COORDINATE_SETS
        )
        print(f"completed length={length:2d} {fields}")

    specials = (
        ("tail-2 repair", tuple(map(int, "12212121212121212")), 2),
        ("tail-3 sharp", (1, 2, 1), 3),
    )
    for label, word, tail in specials:
        values = audit_case(word, tail, results, cross_check=True)
        print(
            f"special={label} W={''.join(map(str, word))} "
            + " ".join(
                f"{name}:rank/target/slack={rank}/{target}/{slack}"
                for name, (rank, target, slack) in values.items()
            )
        )

    for name, result in results.items():
        print(
            f"coordinates={name:3s} cases={result.cases:5d} "
            f"failures={result.failures:5d} min-slack={result.minimum_slack:3d} "
            f"prefix-failures={result.prefix_failures:5d} "
            f"min-prefix-slack={result.minimum_prefix_slack:3d} "
            f"max-nullity={result.maximum_nullity:3d}"
        )
        print(f"  minimum: {result.minimum_witness}")
        print(f"  nullity: {result.nullity_witness}")
        print(f"  first failure: {result.first_failure or 'none'}")
        print(f"  first prefix failure: {result.first_prefix_failure or 'none'}")


if __name__ == "__main__":
    main()

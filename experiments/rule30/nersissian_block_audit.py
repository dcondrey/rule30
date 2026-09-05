"""Audit the published masked-block support recurrence for Rule 30.

This is a clean-room transcription of the mathematical operations in
Nersissian (2026), not a claimed fast center-column algorithm.  Its purpose is
to separate two costs:

* evaluating a bit after a compressed support row has been supplied; and
* constructing the support row S_(n+1) required for center bit c(n).

The first is cheap per block.  The published recurrence for the second still
advances successively through every row up to n+1.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from time import perf_counter
from typing import Iterable, Iterator, Sequence

from center_column import center_column

Block = tuple[int, int]


def subset_zeta(values: Sequence[int]) -> list[int]:
    """Boolean subset-zeta transform on a power-of-two truth table."""

    if not values or len(values) & (len(values) - 1):
        raise ValueError("zeta input length must be a positive power of two")
    transformed = [int(value) & 1 for value in values]
    for bit in range(len(transformed).bit_length() - 1):
        flag = 1 << bit
        for index in range(len(transformed)):
            if index & flag:
                transformed[index] ^= transformed[index ^ flag]
    return transformed


def increment_truth_table(values: Sequence[int]) -> list[int]:
    """Shift a finite support indicator from ``r`` to ``r+1``."""

    if not values:
        raise ValueError("increment input must be nonempty")
    return [0, *[int(value) & 1 for value in values[:-1]]]


def exclusive_prefix_xor(values: Sequence[int]) -> list[int]:
    """Return ``p[n] = XOR_(0 <= y < n) values[y]``."""

    result: list[int] = []
    running = 0
    for value in values:
        result.append(running)
        running ^= int(value) & 1
    return result


def or_convolution_truth_tables(
    left: Sequence[int], right: Sequence[int]
) -> list[int]:
    """Literal parity convolution under bitwise OR for small audit tables."""

    if len(left) != len(right) or not left or len(left) & (len(left) - 1):
        raise ValueError("OR-convolution inputs must have equal power-of-two length")
    result = [0] * len(left)
    for a, left_value in enumerate(left):
        if not (int(left_value) & 1):
            continue
        for b, right_value in enumerate(right):
            if int(right_value) & 1:
                result[a | b] ^= 1
    return result


def submasks(mask: int) -> Iterator[int]:
    """Yield every bitwise submask, including zero."""

    current = mask
    while current:
        yield current
        current = (current - 1) & mask
    yield 0


def simplify(blocks: Iterable[Block]) -> list[Block]:
    """Apply parity cancellation and the published greedy cube merging."""

    current = list(blocks)
    while True:
        current = [block for block, count in Counter(current).items() if count & 1]
        used: set[int] = set()
        result: list[Block] = []
        merged = False
        for left, (base_left, mask_left) in enumerate(current):
            if left in used:
                continue
            for right in range(left + 1, len(current)):
                if right in used:
                    continue
                base_right, mask_right = current[right]
                difference = base_left ^ base_right
                if (
                    mask_left == mask_right
                    and difference
                    and difference & (difference - 1) == 0
                    and mask_left & difference == 0
                ):
                    result.append((base_left & base_right, mask_left | difference))
                    used.update((left, right))
                    merged = True
                    break
            if left not in used:
                result.append(current[left])
                used.add(left)
        current = result
        if not merged:
            return current


def block_or_convolution(left: Sequence[Block], right: Sequence[Block]) -> list[Block]:
    """Exact parity OR-convolution of two XOR-sums of masked blocks."""

    result: list[Block] = []
    for base_left, mask_left in left:
        for base_right, mask_right in right:
            shared = mask_left & mask_right
            left_only = mask_left & ~shared
            right_only = mask_right & ~shared
            for left_bits in submasks(left_only):
                for right_bits in submasks(right_only):
                    result.append(
                        (base_left | left_bits | base_right | right_bits, shared)
                    )
    return simplify(result)


def block_increment(blocks: Sequence[Block]) -> list[Block]:
    """Map the represented finite set X to {x+1:x in X}."""

    result: list[Block] = []
    for base, mask in blocks:
        footprint = base | mask
        first_zero = (~footprint) & (footprint + 1)
        colliding = mask & (first_zero - 1)
        safe = mask & ~(first_zero - 1)
        result.extend(((base | bits) + 1, safe) for bits in submasks(colliding))
    return simplify(result)


def expand_blocks(blocks: Sequence[Block]) -> set[int]:
    """Expand an XOR-sum of blocks to its represented finite support set."""

    counts = Counter(base | bits for base, mask in blocks for bits in submasks(mask))
    return {value for value, count in counts.items() if count & 1}


def next_support(previous: Sequence[Block], before_previous: Sequence[Block]) -> list[Block]:
    """Advance the exact support recurrence by one row."""

    product = block_or_convolution(previous, before_previous)
    return block_increment(simplify([*product, *previous, *before_previous]))


def support_rows(target_m: int) -> Iterator[tuple[int, list[Block]]]:
    """Yield every successive compressed support through ``target_m``."""

    if target_m < 1:
        raise ValueError("target_m must be positive")
    before_previous = [(0, 0)]
    yield 1, before_previous
    if target_m == 1:
        return
    previous = [(1, 0)]
    yield 2, previous
    for m in range(3, target_m + 1):
        current = next_support(previous, before_previous)
        yield m, current
        before_previous, previous = previous, current


def support_blocks(target_m: int) -> list[Block]:
    """Construct ``S_target_m`` by the published sequential recurrence."""

    return next(blocks for m, blocks in support_rows(target_m) if m == target_m)


def evaluate_blocks(blocks: Sequence[Block], n: int) -> int:
    """Evaluate the Lucas parity represented by blocks at integer ``n``."""

    return sum((base & n) == base and (mask & n) == 0 for base, mask in blocks) & 1


def center_bit_via_blocks(n: int) -> int:
    """Compute c(n), including the construction cost of S_(n+1)."""

    if n < 0:
        raise ValueError("n must be nonnegative")
    return evaluate_blocks(support_blocks(n + 1), n)


@dataclass(frozen=True)
class AuditRow:
    m: int
    blocks: int
    expanded_support: int
    maximum_support: int
    maximum_mask_weight: int
    elapsed_seconds: float


def audit_rows(target_m: int, expand_limit: int = 30) -> list[AuditRow]:
    """Profile the actual supplied representation along the growing row index."""

    records: list[AuditRow] = []
    start = perf_counter()
    for m, blocks in support_rows(target_m):
        expanded = expand_blocks(blocks) if m <= expand_limit else set()
        records.append(
            AuditRow(
                m=m,
                blocks=len(blocks),
                expanded_support=len(expanded) if expanded else -1,
                maximum_support=max(expanded) if expanded else -1,
                maximum_mask_weight=max((mask.bit_count() for _, mask in blocks), default=0),
                elapsed_seconds=perf_counter() - start,
            )
        )
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-m", type=int, default=24)
    parser.add_argument("--check-centers", type=int, default=20)
    args = parser.parse_args()
    if args.max_m < 1 or args.check_centers < 0:
        parser.error("max-m must be positive and check-centers nonnegative")

    expected = center_column(args.check_centers)
    actual = bytes(center_bit_via_blocks(n) for n in range(args.check_centers))
    if actual != expected:
        mismatch = next(n for n, pair in enumerate(zip(actual, expected)) if pair[0] != pair[1])
        raise AssertionError(f"center mismatch at n={mismatch}")

    print(f"center oracle check: PASS through n={args.check_centers - 1}")
    print("m blocks support_size max_support max_mask_weight cumulative_seconds")
    for row in audit_rows(args.max_m):
        print(
            f"{row.m:2d} {row.blocks:6d} {row.expanded_support:12d} "
            f"{row.maximum_support:11d} {row.maximum_mask_weight:15d} "
            f"{row.elapsed_seconds:.6f}"
        )


if __name__ == "__main__":
    main()

"""Probe a fixed-state binary-digit shortcut for the Rule 30 center column.

For a binary sequence a(n), its 2-kernel contains every residual sequence

    (a(2**e * k + r))_{k >= 0},  e >= 0, 0 <= r < 2**e.

A fixed finite 2-kernel would give a direct finite-state query on the binary
digits of n.  This is one concrete version of the residual mechanism proposed
after the Rule 150 superposition and dyadic-cancellation arms closed.

Pre-registered disconfirmation:

* If all 2**12 residuals at depth 12 have distinct 64-bit prefixes, an exact
  representation needs at least 4096 distinct residual states.  This kills a
  small fixed-state explanation; it does not prove that the full kernel is
  infinite.
* If the GF(2) rank of depth-9 residual prefixes reaches 512, a fixed linear
  representation needs dimension at least 512.  This kills a small bounded-rank
  transfer operator; it does not rule out dimension growing with n.

Thue--Morse is included as a positive control: its 2-kernel should saturate at
two residual sequences and rank two.

Bernoulli(1/2) is the negative control, and it is the one that says what a
saturated count is worth.  Shallit and Breitbart, "Automaticity I", JCSS 53
(1996), section 11, Theorem 27, prove that this count -- the k-automaticity
A^k_s(n) of a sequence -- is O(n / log n) for every sequence over a finite
alphabet and Omega(n / log n) for ALMOST ALL of them.  Saturation is therefore
the generic behaviour, so a saturated Rule 30 count separates the centre column
from nothing unless it is read against a matched null.
"""

from __future__ import annotations

import argparse
import random
import statistics
from collections.abc import Callable

from center_column import center_column


KNOWN_PREFIX = b"11011100110001011001001110101110"


def naive_center_column(steps: int) -> bytes:
    width = 2 * steps + 3
    center = steps + 1
    row = [0] * width
    row[center] = 1
    output = bytearray(steps)
    for time in range(steps):
        output[time] = row[center]
        row = [
            0,
            *(row[index - 1] ^ (row[index] | row[index + 1]) for index in range(1, width - 1)),
            0,
        ]
    return bytes(output)


def thue_morse(length: int) -> bytes:
    return bytes(index.bit_count() & 1 for index in range(length))


def bernoulli(seed: int) -> Callable[[int], bytes]:
    def make(length: int) -> bytes:
        bits = random.Random(seed).getrandbits(length)
        return bytes((bits >> index) & 1 for index in range(length))

    return make


def residual_prefix(sequence: bytes, depth: int, residue: int, length: int) -> bytes:
    stride = 1 << depth
    return bytes(sequence[residue + stride * index] for index in range(length))


def pack_bits(bits: bytes) -> int:
    word = 0
    for index, bit in enumerate(bits):
        word |= bit << index
    return word


def gf2_rank(words: list[int]) -> int:
    basis: dict[int, int] = {}
    for word in words:
        while word:
            pivot = word.bit_length() - 1
            if pivot in basis:
                word ^= basis[pivot]
            else:
                basis[pivot] = word
                break
    return len(basis)


def probe(
    name: str,
    make_sequence: Callable[[int], bytes],
    max_depth: int,
    identity_prefix: int,
    rank_prefix: int,
) -> list[tuple[int, int, int, int, int, int]]:
    total_length = identity_prefix << max_depth
    sequence = make_sequence(total_length)
    if name == "rule30":
        observed = bytes(ord("1") if bit else ord("0") for bit in sequence[: len(KNOWN_PREFIX)])
        assert observed == KNOWN_PREFIX, "Rule 30 ground-truth prefix mismatch"
        assert sequence[:256] == naive_center_column(256), "bit-parallel/naive mismatch"

    cumulative: set[bytes] = set()
    rows = []
    for depth in range(max_depth + 1):
        count = 1 << depth
        available = total_length // count
        identity_length = min(identity_prefix, available)
        rank_length = min(rank_prefix, available)
        identity_residuals = [
            residual_prefix(sequence, depth, residue, identity_length)
            for residue in range(count)
        ]
        cumulative.update(identity_residuals)
        rank_words = [
            pack_bits(residual_prefix(sequence, depth, residue, rank_length))
            for residue in range(count)
        ]
        rows.append(
            (
                depth,
                count,
                identity_length,
                len(set(identity_residuals)),
                len(cumulative),
                gf2_rank(rank_words),
            )
        )
    return rows


def print_report(
    name: str,
    rows: list[tuple[int, int, int, int, int, int]],
) -> None:
    print(f"## {name}")
    print("depth residuals prefix distinct cumulative gf2_rank")
    for depth, count, prefix, distinct, cumulative, rank in rows:
        print(f"{depth:5d} {count:9d} {prefix:6d} {distinct:8d} {cumulative:10d} {rank:8d}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-depth", type=int, default=12)
    parser.add_argument("--identity-prefix", type=int, default=64)
    parser.add_argument("--rank-prefix", type=int, default=1024)
    parser.add_argument("--null-seeds", type=int, default=8)
    args = parser.parse_args()
    if args.max_depth < 0 or args.identity_prefix < 1 or args.rank_prefix < 1:
        parser.error("depth must be non-negative and prefix lengths must be positive")
    if args.null_seeds < 0 or args.null_seeds == 1:
        parser.error("--null-seeds must be 0 or at least 2, since it reports a sample sd")

    rule30 = probe(
        "rule30",
        center_column,
        args.max_depth,
        args.identity_prefix,
        args.rank_prefix,
    )
    control = probe(
        "thue-morse",
        thue_morse,
        args.max_depth,
        args.identity_prefix,
        args.rank_prefix,
    )
    print_report("rule30", rule30)
    print()
    print_report("thue-morse control", control)
    if not args.null_seeds:
        return

    nulls = [
        probe(
            f"bernoulli-{seed}",
            bernoulli(seed),
            args.max_depth,
            args.identity_prefix,
            args.rank_prefix,
        )
        for seed in range(args.null_seeds)
    ]
    print()
    print(f"## bernoulli(1/2) negative control, {args.null_seeds} seeds")
    print("depth  r30_cum null_cum_mean sd  r30_rank null_rank_mean sd  separates")
    for index, row in enumerate(rule30):
        cum = [null[index][4] for null in nulls]
        rank = [null[index][5] for null in nulls]
        cum_mean, cum_sd = statistics.fmean(cum), statistics.stdev(cum)
        rank_mean, rank_sd = statistics.fmean(rank), statistics.stdev(rank)
        apart = (abs(row[4] - cum_mean) > 3 * cum_sd if cum_sd else row[4] != cum_mean) or (
            abs(row[5] - rank_mean) > 3 * rank_sd if rank_sd else row[5] != rank_mean
        )
        print(
            f"{row[0]:5d} {row[4]:8d} {cum_mean:13.1f} {cum_sd:4.1f}"
            f" {row[5]:9d} {rank_mean:14.1f} {rank_sd:4.1f}  {'YES' if apart else 'no'}"
        )
    print(
        "A saturated count is the generic case (Shallit and Breitbart 1996, Thm 27.4),"
        " so a depth only carries evidence about Rule 30 where this column reads YES."
    )


if __name__ == "__main__":
    main()

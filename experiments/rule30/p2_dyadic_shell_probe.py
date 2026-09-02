"""Exact dyadic-shell discrepancy diagnostics for the Rule 30 center trace.

For signed center bits ``x_t = 2*c_t-1``, define

    M_k = max_{0 <= u <= 2**k} |sum(x_t, 2**k <= t < 2**k+u)|.

The accompanying results note proves that P2 is equivalent to
``M_k / 2**k -> 0``.  This program only measures finite ``M_k`` values.  It
does not extrapolate them or treat a fitted exponent as a proof.

The optional band cache is the uint32 format produced by the deep Rule 30
generator.  By convention bit 15 is the center column.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from center_column import center_column


@dataclass(frozen=True)
class ShellRecord:
    k: int
    length: int
    shell_sum: int
    shell_max_abs: int
    integrated_prefix_energy: int
    prefix_at_start: int
    prefix_at_end: int
    high_bit_correlation: int

    @property
    def normalized_max(self) -> float:
        return self.shell_max_abs / self.length

    @property
    def normalized_integrated_energy(self) -> float:
        return self.integrated_prefix_energy / self.length**3


def signed(bits: Sequence[int]) -> list[int]:
    return [2 * int(bit) - 1 for bit in bits]


def integrated_prefix_energy(values: Sequence[int]) -> int:
    """Return the sum of squared signed prefix sums, including the endpoint."""

    running = 0
    energy = 0
    for value in values:
        running += int(value)
        energy += running * running
    return energy


def prefix_moments(values: Sequence[int]) -> tuple[int, int, int, int]:
    """Return ``(length, total, prefix area, prefix-square energy)``."""

    running = 0
    area = 0
    energy = 0
    for value in values:
        running += int(value)
        area += running
        energy += running * running
    return len(values), running, area, energy


def concatenate_prefix_moments(
    left: tuple[int, int, int, int],
    right: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    """Compose prefix moments exactly under word concatenation."""

    left_length, left_total, left_area, left_energy = left
    right_length, right_total, right_area, right_energy = right
    return (
        left_length + right_length,
        left_total + right_total,
        left_area + right_length * left_total + right_area,
        left_energy
        + right_length * left_total * left_total
        + 2 * left_total * right_area
        + right_energy,
    )


def ordinary_shift_correlations(values: Sequence[int], max_shift: int) -> list[int]:
    """Return ordinary (non-XOR) correlations for shifts zero through a cap."""

    if max_shift < 0:
        raise ValueError("max_shift must be nonnegative")
    length = len(values)
    return [
        sum(
            int(values[index]) * int(values[index + shift])
            for index in range(length - shift)
        )
        if shift < length
        else 0
        for shift in range(max_shift + 1)
    ]


def van_der_corput_certificate(values: Sequence[int], horizon: int) -> tuple[int, int]:
    """Return the numerator and denominator of the exact finite vdC bound.

    The returned pair ``(p,q)`` certifies

        (sum values)**2 <= p / q.

    Correlations retain their signs; replacing them by absolute values gives
    the familiar looser asymptotic criterion used in the results note.
    """

    if horizon < 1:
        raise ValueError("horizon must be positive")
    length = len(values)
    correlations = ordinary_shift_correlations(values, horizon - 1)
    square_sum = horizon * length + 2 * sum(
        (horizon - shift) * correlations[shift]
        for shift in range(1, horizon)
    )
    return (length + horizon - 1) * square_sum, horizon * horizon


def shell_record(bits: Sequence[int], k: int) -> ShellRecord:
    """Return the exact record for shell ``[2**k, 2**(k+1))``.

    ``high_bit_correlation`` is the unnormalized signed correlation between
    that shell and the prefix of equal length.  It tests the most direct
    high-bit coupling ``t <-> t+2**k``; it is diagnostic only.
    """

    length = 1 << k
    if len(bits) < 2 * length:
        raise ValueError(f"need at least {2 * length} bits for shell {k}")

    values = signed(bits)
    prefix_at_start = sum(values[:length])
    running = 0
    maximum = 0
    prefix_energy = 0
    correlation = 0
    for offset in range(length):
        value = values[length + offset]
        running += value
        maximum = max(maximum, abs(running))
        prefix_energy += running * running
        correlation += values[offset] * value

    return ShellRecord(
        k=k,
        length=length,
        shell_sum=running,
        shell_max_abs=maximum,
        integrated_prefix_energy=prefix_energy,
        prefix_at_start=prefix_at_start,
        prefix_at_end=prefix_at_start + running,
        high_bit_correlation=correlation,
    )


def records(bits: Sequence[int], min_k: int, max_k: int) -> list[ShellRecord]:
    if min_k < 0 or max_k < min_k:
        raise ValueError("require 0 <= min_k <= max_k")
    return [shell_record(bits, k) for k in range(min_k, max_k + 1)]


def read_band_cache(path: Path, count: int, center_bit: int = 15) -> bytes:
    """Read ``count`` center bits without depending on NumPy or native endian."""

    if count < 0:
        raise ValueError("count must be nonnegative")
    needed = 4 * count
    with path.open("rb") as handle:
        raw = handle.read(needed)
    if len(raw) != needed:
        raise ValueError(f"cache has fewer than {count} rows")
    return bytes(
        (int.from_bytes(raw[offset : offset + 4], "little") >> center_bit) & 1
        for offset in range(0, needed, 4)
    )


def print_table(found: Sequence[ShellRecord]) -> None:
    print(
        "k length shell_sum shell_max_abs prefix_energy prefix_start prefix_end "
        "high_bit_corr max/length energy/length^3 corr/length"
    )
    for row in found:
        print(
            f"{row.k:2d} {row.length:8d} {row.shell_sum:9d} "
            f"{row.shell_max_abs:13d} {row.integrated_prefix_energy:13d} "
            f"{row.prefix_at_start:12d} "
            f"{row.prefix_at_end:10d} {row.high_bit_correlation:13d} "
            f"{row.normalized_max:.9g} "
            f"{row.normalized_integrated_energy:.9g} "
            f"{row.high_bit_correlation / row.length:+.9g}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-k", type=int, default=4)
    parser.add_argument("--max-k", type=int, default=18)
    parser.add_argument("--band-cache", type=Path)
    parser.add_argument("--center-bit", type=int, default=15)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.min_k < 0 or args.max_k < args.min_k:
        parser.error("require 0 <= min-k <= max-k")
    count = 1 << (args.max_k + 1)
    if args.band_cache is None:
        bits = center_column(count)
    else:
        bits = read_band_cache(args.band_cache, count, args.center_bit)

    found = records(bits, args.min_k, args.max_k)
    if args.json:
        print(
            json.dumps(
                [
                    asdict(row)
                    | {
                        "normalized_max": row.normalized_max,
                        "normalized_integrated_energy": row.normalized_integrated_energy,
                    }
                    for row in found
                ],
                indent=2,
            )
        )
    else:
        print_table(found)


if __name__ == "__main__":
    main()

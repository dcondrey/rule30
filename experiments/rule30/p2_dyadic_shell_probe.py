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
    prefix_at_start: int
    prefix_at_end: int
    high_bit_correlation: int

    @property
    def normalized_max(self) -> float:
        return self.shell_max_abs / self.length


def signed(bits: Sequence[int]) -> list[int]:
    return [2 * int(bit) - 1 for bit in bits]


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
    correlation = 0
    for offset in range(length):
        value = values[length + offset]
        running += value
        maximum = max(maximum, abs(running))
        correlation += values[offset] * value

    return ShellRecord(
        k=k,
        length=length,
        shell_sum=running,
        shell_max_abs=maximum,
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
        "k length shell_sum shell_max_abs prefix_start prefix_end "
        "high_bit_corr max/length corr/length"
    )
    for row in found:
        print(
            f"{row.k:2d} {row.length:8d} {row.shell_sum:9d} "
            f"{row.shell_max_abs:13d} {row.prefix_at_start:12d} "
            f"{row.prefix_at_end:10d} {row.high_bit_correlation:13d} "
            f"{row.normalized_max:.9g} "
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
                [asdict(row) | {"normalized_max": row.normalized_max} for row in found],
                indent=2,
            )
        )
    else:
        print_table(found)


if __name__ == "__main__":
    main()

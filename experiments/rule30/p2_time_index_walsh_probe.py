"""Walsh diagnostics for the actual time-index functions of the Rule 30 seed.

For a dyadic shell define the k-variable Boolean function

    f_k(r) = c(2**k + r),  0 <= r < 2**k,

where the bits of ``r`` are the variables.  This differs from the archived
arbitrary-initial-row Walsh calculation: every value here lies on the one
designated lone-seed orbit.  The zero Walsh coefficient is the shell's signed
discrepancy.  The maximum coefficient controls every restriction obtained by
fixing high time bits, hence every binary-prefix decomposition of the shell.

All transforms use exact Python integers.  Finite spectral flatness is a
diagnostic, not an asymptotic P2 result.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from center_column import center_column
from p2_dyadic_shell_probe import read_band_cache


@dataclass(frozen=True)
class WalshRecord:
    k: int
    length: int
    dc: int
    max_abs_walsh: int
    max_walsh_index: int
    max_shell_prefix: int
    max_aligned_restriction: int
    max_abs_bit_derivative_correlation: int
    max_abs_xor_autocorrelation_nonzero: int
    l1_xor_autocorrelation: int
    anf_degree: int
    anf_terms: int

    @property
    def random_scale_ratio(self) -> float:
        """Maximum Walsh magnitude divided by ``sqrt(k*2**k)``."""

        return self.max_abs_walsh / math.sqrt(self.k * self.length)


def signs(bits: Sequence[int]) -> list[int]:
    return [1 - 2 * int(bit) for bit in bits]


def walsh_transform(values: Sequence[int]) -> list[int]:
    """Unnormalized Walsh-Hadamard transform in XOR character order."""

    if not values or len(values) & (len(values) - 1):
        raise ValueError("Walsh input length must be a positive power of two")
    transformed = list(values)
    half = 1
    while half < len(transformed):
        for start in range(0, len(transformed), 2 * half):
            for offset in range(half):
                left = transformed[start + offset]
                right = transformed[start + half + offset]
                transformed[start + offset] = left + right
                transformed[start + half + offset] = left - right
        half *= 2
    return transformed


def maximum_aligned_restriction(values: Sequence[int]) -> int:
    """Maximum absolute sum over nonempty aligned dyadic subblocks."""

    current = list(values)
    maximum = max(abs(value) for value in current)
    while len(current) > 1:
        current = [current[index] + current[index + 1] for index in range(0, len(current), 2)]
        maximum = max(maximum, *(abs(value) for value in current))
    return maximum


def bit_derivative_correlations(values: Sequence[int]) -> list[int]:
    """Return ``sum_r z(r) z(r XOR 2**j)`` for every time-index bit ``j``."""

    length = len(values)
    if not values or length & (length - 1):
        raise ValueError("derivative input length must be a positive power of two")
    return [
        sum(values[index] * values[index ^ (1 << bit)] for index in range(length))
        for bit in range(length.bit_length() - 1)
    ]


def xor_autocorrelations(values: Sequence[int]) -> list[int]:
    """Return every XOR autocorrelation using Walsh convolution exactly."""

    spectrum = walsh_transform(values)
    length = len(spectrum)
    numerators = walsh_transform([value * value for value in spectrum])
    if any(value % length for value in numerators):
        raise AssertionError("Walsh autocorrelation numerator is not divisible")
    return [value // length for value in numerators]


def anf_profile(values: Sequence[int]) -> tuple[int, int]:
    """Return ``(degree, term count)`` of a Boolean truth table."""

    if not values or len(values) & (len(values) - 1):
        raise ValueError("ANF input length must be a positive power of two")
    coefficients = [int(value) & 1 for value in values]
    variables = len(coefficients).bit_length() - 1
    for bit in range(variables):
        mask = 1 << bit
        for index in range(len(coefficients)):
            if index & mask:
                coefficients[index] ^= coefficients[index ^ mask]
    support = [index for index, value in enumerate(coefficients) if value]
    return max((index.bit_count() for index in support), default=-1), len(support)


def record(bits: Sequence[int], k: int) -> WalshRecord:
    length = 1 << k
    if len(bits) < 2 * length:
        raise ValueError(f"need at least {2 * length} center bits")
    shell = signs(bits[length : 2 * length])
    spectrum = walsh_transform(shell)
    maximum = max(abs(value) for value in spectrum)
    maximum_index = next(index for index, value in enumerate(spectrum) if abs(value) == maximum)
    running = 0
    prefix_maximum = 0
    for value in shell:
        running += value
        prefix_maximum = max(prefix_maximum, abs(running))
    correlations = bit_derivative_correlations(shell)
    all_correlations = xor_autocorrelations(shell)
    degree, terms = anf_profile(bits[length : 2 * length])
    if all_correlations[0] != length:
        raise AssertionError("zero-shift autocorrelation mismatch")
    return WalshRecord(
        k=k,
        length=length,
        dc=spectrum[0],
        max_abs_walsh=maximum,
        max_walsh_index=maximum_index,
        max_shell_prefix=prefix_maximum,
        max_aligned_restriction=maximum_aligned_restriction(shell),
        max_abs_bit_derivative_correlation=max(map(abs, correlations)),
        max_abs_xor_autocorrelation_nonzero=max(map(abs, all_correlations[1:])),
        l1_xor_autocorrelation=sum(map(abs, all_correlations)),
        anf_degree=degree,
        anf_terms=terms,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-k", type=int, default=6)
    parser.add_argument("--max-k", type=int, default=18)
    parser.add_argument("--band-cache", type=Path)
    parser.add_argument("--center-bit", type=int, default=15)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.min_k < 1 or args.max_k < args.min_k:
        parser.error("require 1 <= min-k <= max-k")

    count = 1 << (args.max_k + 1)
    bits = (
        center_column(count)
        if args.band_cache is None
        else read_band_cache(args.band_cache, count, args.center_bit)
    )
    found = [record(bits, k) for k in range(args.min_k, args.max_k + 1)]
    if args.json:
        print(
            json.dumps(
                [asdict(row) | {"random_scale_ratio": row.random_scale_ratio} for row in found],
                indent=2,
            )
        )
        return

    print(
        "k length dc max_walsh walsh_index prefix_max aligned_max "
        "bit_derivative_max xor_corr_max xor_corr_l1 anf_degree anf_terms "
        "max/sqrt(kN)"
    )
    for row in found:
        print(
            f"{row.k:2d} {row.length:8d} {row.dc:7d} {row.max_abs_walsh:10d} "
            f"{row.max_walsh_index:11d} {row.max_shell_prefix:10d} "
            f"{row.max_aligned_restriction:11d} "
            f"{row.max_abs_bit_derivative_correlation:18d} "
            f"{row.max_abs_xor_autocorrelation_nonzero:12d} "
            f"{row.l1_xor_autocorrelation:11d} "
            f"{row.anf_degree:10d} {row.anf_terms:9d} "
            f"{row.random_scale_ratio:.6f}"
        )


if __name__ == "__main__":
    main()

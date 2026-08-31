"""Probe Rule 30 through a lossless ensemble of representations and compressors.

The transforms are fixed and exactly reversible.  They expose space, time,
reflection, rotation, diagonal, Morton, derivative, and dyadic-scale views of
the same spacetime square.  zlib, bzip2, and LZMA then act as deliberately
different pattern detectors.  A second compression pass is measured as a
control, not assumed to create information.

This is a diagnostic only: producing every representation still costs the
area of the spacetime window.  A useful result must persist as the horizon
grows and eventually yield a directly composable state representation.
"""

from __future__ import annotations

import argparse
import bz2
import lzma
import zlib
from collections.abc import Callable, Sequence
from dataclasses import dataclass

from spacetime_grammar_probe import (
    RULE_90,
    active_cone_complement,
    eca_grid,
    eca_zero_grid,
    fit_exponent,
    random_triangle_grid,
)
from support_state_probe import RULE_22, RULE_30


COMPRESSORS: dict[str, tuple[Callable[[bytes], bytes], Callable[[bytes], bytes]]] = {
    "zlib": (lambda data: zlib.compress(data, 9), zlib.decompress),
    "bz2": (lambda data: bz2.compress(data, 9), bz2.decompress),
    "lzma": (lambda data: lzma.compress(data, preset=6), lzma.decompress),
}
MODEL_TAG_BYTES = 2


def pack_bits(bits: Sequence[int]) -> bytes:
    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("only binary sequences can be packed")
    packed = bytearray((len(bits) + 7) // 8)
    for index, bit in enumerate(bits):
        packed[index // 8] |= bit << (index % 8)
    return bytes(packed)


def unpack_bits(data: bytes, length: int) -> list[int]:
    return [(data[index // 8] >> (index % 8)) & 1 for index in range(length)]


def coordinate_order(name: str, side: int) -> list[tuple[int, int]]:
    if name == "row":
        return [(row, column) for row in range(side) for column in range(side)]
    if name == "mirror_lr":
        return [(row, side - 1 - column) for row in range(side) for column in range(side)]
    if name == "mirror_ud":
        return [(side - 1 - row, column) for row in range(side) for column in range(side)]
    if name == "rotate_180":
        return [
            (side - 1 - row, side - 1 - column)
            for row in range(side)
            for column in range(side)
        ]
    if name == "transpose":
        return [(column, row) for row in range(side) for column in range(side)]
    if name == "rotate_90":
        return [
            (side - 1 - column, row)
            for row in range(side)
            for column in range(side)
        ]
    if name == "rotate_270":
        return [
            (column, side - 1 - row)
            for row in range(side)
            for column in range(side)
        ]
    if name == "anti_transpose":
        return [
            (side - 1 - column, side - 1 - row)
            for row in range(side)
            for column in range(side)
        ]
    if name == "diagonal":
        return [
            (row, diagonal - row)
            for diagonal in range(2 * side - 1)
            for row in range(max(0, diagonal - side + 1), min(side, diagonal + 1))
        ]
    if name == "morton":
        coordinates: list[tuple[int, int]] = []
        bits = side.bit_length() - 1
        for code in range(side * side):
            row = column = 0
            for bit in range(bits):
                column |= ((code >> (2 * bit)) & 1) << bit
                row |= ((code >> (2 * bit + 1)) & 1) << bit
            coordinates.append((row, column))
        return coordinates
    raise ValueError(f"unknown coordinate encoding: {name}")


COORDINATE_ENCODINGS = (
    "row", "mirror_lr", "mirror_ud", "rotate_180", "transpose",
    "rotate_90", "rotate_270", "anti_transpose", "diagonal", "morton",
)
DERIVATIVE_ENCODINGS = (
    "row_xor", "column_xor", "mirror_lr_channels", "mirror_ud_channels",
    "transpose_channels", "dyadic_residual",
)
ENCODINGS = COORDINATE_ENCODINGS + DERIVATIVE_ENCODINGS


def _dyadic_residual_encode(bits: Sequence[int], side: int) -> list[int]:
    current = list(bits)
    width = side
    layers: list[list[int]] = []
    while width > 1:
        anchors: list[int] = []
        details: list[int] = []
        for row in range(0, width, 2):
            for column in range(0, width, 2):
                offset = row * width + column
                anchor = current[offset]
                anchors.append(anchor)
                details.extend(
                    (
                        anchor ^ current[offset + 1],
                        anchor ^ current[offset + width],
                        anchor ^ current[offset + width + 1],
                    )
                )
        layers.append(details)
        current = anchors
        width //= 2
    return current + [bit for layer in reversed(layers) for bit in layer]


def _dyadic_residual_decode(encoded: Sequence[int], side: int) -> list[int]:
    current = [encoded[0]]
    cursor = 1
    width = 1
    while width < side:
        expanded_width = width * 2
        expanded = [0] * (expanded_width * expanded_width)
        for row in range(width):
            for column in range(width):
                anchor = current[row * width + column]
                first, second, third = encoded[cursor : cursor + 3]
                cursor += 3
                offset = (2 * row) * expanded_width + 2 * column
                expanded[offset] = anchor
                expanded[offset + 1] = anchor ^ first
                expanded[offset + expanded_width] = anchor ^ second
                expanded[offset + expanded_width + 1] = anchor ^ third
        current = expanded
        width = expanded_width
    if cursor != len(encoded):
        raise ValueError("dyadic residual stream has the wrong length")
    return current


def encode_sequence(bits: Sequence[int], side: int, name: str) -> list[int]:
    if len(bits) != side * side or side < 1 or side & (side - 1):
        raise ValueError("encodings require a power-of-two square binary grid")
    if name in COORDINATE_ENCODINGS:
        return [bits[row * side + column] for row, column in coordinate_order(name, side)]
    if name == "row_xor":
        return [
            bits[row * side + column]
            ^ (bits[(row - 1) * side + column] if row else 0)
            for row in range(side)
            for column in range(side)
        ]
    if name == "column_xor":
        return [
            bits[row * side + column]
            ^ (bits[row * side + column - 1] if column else 0)
            for row in range(side)
            for column in range(side)
        ]
    if name == "mirror_lr_channels":
        left = [bits[row * side + column] for row in range(side) for column in range(side // 2)]
        residual = [
            bits[row * side + column] ^ bits[row * side + side - 1 - column]
            for row in range(side)
            for column in range(side // 2)
        ]
        return left + residual
    if name == "mirror_ud_channels":
        top = list(bits[: side * side // 2])
        residual = [
            bits[row * side + column] ^ bits[(side - 1 - row) * side + column]
            for row in range(side // 2)
            for column in range(side)
        ]
        return top + residual
    if name == "transpose_channels":
        diagonal = [bits[index * side + index] for index in range(side)]
        upper = [bits[row * side + column] for row in range(side) for column in range(row + 1, side)]
        residual = [
            bits[row * side + column] ^ bits[column * side + row]
            for row in range(side)
            for column in range(row + 1, side)
        ]
        return diagonal + upper + residual
    if name == "dyadic_residual":
        return _dyadic_residual_encode(bits, side)
    raise ValueError(f"unknown encoding: {name}")


def decode_sequence(encoded: Sequence[int], side: int, name: str) -> list[int]:
    if len(encoded) != side * side:
        raise ValueError("encoded sequence has the wrong length")
    if name in COORDINATE_ENCODINGS:
        result = [0] * len(encoded)
        for bit, (row, column) in zip(encoded, coordinate_order(name, side)):
            result[row * side + column] = bit
        return result
    if name == "row_xor":
        result = [0] * len(encoded)
        for row in range(side):
            for column in range(side):
                index = row * side + column
                result[index] = encoded[index] ^ (result[index - side] if row else 0)
        return result
    if name == "column_xor":
        result = [0] * len(encoded)
        for row in range(side):
            for column in range(side):
                index = row * side + column
                result[index] = encoded[index] ^ (result[index - 1] if column else 0)
        return result
    if name == "mirror_lr_channels":
        result = [0] * len(encoded)
        half = len(encoded) // 2
        cursor = 0
        for row in range(side):
            for column in range(side // 2):
                left = encoded[cursor]
                result[row * side + column] = left
                result[row * side + side - 1 - column] = left ^ encoded[half + cursor]
                cursor += 1
        return result
    if name == "mirror_ud_channels":
        result = [0] * len(encoded)
        half = len(encoded) // 2
        for index in range(half):
            row, column = divmod(index, side)
            top = encoded[index]
            result[index] = top
            result[(side - 1 - row) * side + column] = top ^ encoded[half + index]
        return result
    if name == "transpose_channels":
        result = [0] * len(encoded)
        cursor = side
        residual_cursor = side + side * (side - 1) // 2
        for index in range(side):
            result[index * side + index] = encoded[index]
        for row in range(side):
            for column in range(row + 1, side):
                upper = encoded[cursor]
                result[row * side + column] = upper
                result[column * side + row] = upper ^ encoded[residual_cursor]
                cursor += 1
                residual_cursor += 1
        return result
    if name == "dyadic_residual":
        return _dyadic_residual_decode(encoded, side)
    raise ValueError(f"unknown encoding: {name}")


@dataclass(frozen=True)
class Measurement:
    source: str
    horizon: int
    encoding: str
    compressor: str
    size: int

    @property
    def pipeline(self) -> str:
        return f"{self.encoding}+{self.compressor}"


def compress_grid(bits: Sequence[int], side: int, encoding: str, compressor: str) -> bytes:
    sequence = encode_sequence(bits, side, encoding)
    assert decode_sequence(sequence, side, encoding) == list(bits)
    packed = pack_bits(sequence)
    compressed = COMPRESSORS[compressor][0](packed)
    assert COMPRESSORS[compressor][1](compressed) == packed
    return compressed


def parse_sizes(raw_sizes: Sequence[int]) -> list[int]:
    sizes = sorted(set(raw_sizes))
    if len(sizes) < 2 or any(size < 2 or size & (size - 1) for size in sizes):
        raise ValueError("provide at least two distinct power-of-two horizons")
    return sizes


def report(sizes: Sequence[int]) -> None:
    sources = (
        ("rule90", lambda horizon: eca_grid(RULE_90, horizon)),
        ("rule22", lambda horizon: eca_grid(RULE_22, horizon)),
        ("rule30", lambda horizon: eca_grid(RULE_30, horizon)),
        ("random", random_triangle_grid),
        ("rule30_zeros", lambda horizon: eca_zero_grid(RULE_30, horizon)),
        (
            "random_zeros",
            lambda horizon: active_cone_complement(*random_triangle_grid(horizon), horizon),
        ),
    )
    measurements: list[Measurement] = []
    largest_data: dict[str, tuple[list[int], int]] = {}
    print("source horizon raw_bytes best_bytes best_pipeline")
    for source, make_grid in sources:
        for horizon in sizes:
            bits, side = make_grid(horizon)
            largest_data[source] = (bits, side)
            local: list[Measurement] = []
            for encoding in ENCODINGS:
                for compressor in COMPRESSORS:
                    size = len(compress_grid(bits, side, encoding, compressor)) + MODEL_TAG_BYTES
                    local.append(Measurement(source, horizon, encoding, compressor, size))
            measurements.extend(local)
            best = min(local, key=lambda item: (item.size, item.pipeline))
            print(f"{source:7s} {horizon:7d} {len(bits) // 8:9d} {best.size:10d} {best.pipeline}")

    print("\nsource best_envelope_exponent")
    for source, _ in sources:
        points = [
            (horizon, min(item.size for item in measurements if item.source == source and item.horizon == horizon))
            for horizon in sizes
        ]
        print(f"{source:7s} {fit_exponent(points):22.6f}")

    print("\nrule30_encoding best_compressor largest_bytes size_exponent")
    for encoding in ENCODINGS:
        candidates = [item for item in measurements if item.source == "rule30" and item.encoding == encoding]
        by_horizon = []
        for horizon in sizes:
            best = min((item for item in candidates if item.horizon == horizon), key=lambda item: item.size)
            by_horizon.append((horizon, best.size))
        largest = min(
            (item for item in candidates if item.horizon == sizes[-1]),
            key=lambda item: item.size,
        )
        print(f"{encoding:20s} {largest.compressor:15s} {largest.size:13d} {fit_exponent(by_horizon):13.6f}")

    print("\nsource best_single best_chain chain_gain chain_pipeline")
    for source, _ in sources:
        bits, side = largest_data[source]
        singles: list[tuple[int, str, bytes]] = []
        chains: list[tuple[int, str]] = []
        for encoding in ENCODINGS:
            packed = pack_bits(encode_sequence(bits, side, encoding))
            for first_name, (first_compress, first_decompress) in COMPRESSORS.items():
                first = first_compress(packed)
                assert first_decompress(first) == packed
                singles.append((len(first) + MODEL_TAG_BYTES, f"{encoding}+{first_name}", first))
                for second_name, (second_compress, second_decompress) in COMPRESSORS.items():
                    second = second_compress(first)
                    assert first_decompress(second_decompress(second)) == packed
                    chains.append(
                        (len(second) + MODEL_TAG_BYTES, f"{encoding}+{first_name}+{second_name}")
                    )
        best_single = min(singles, key=lambda item: (item[0], item[1]))
        best_chain = min(chains, key=lambda item: (item[0], item[1]))
        print(
            f"{source:7s} {best_single[0]:11d} {best_chain[0]:10d} "
            f"{best_single[0] - best_chain[0]:10d} {best_chain[1]}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", nargs="+", type=int, default=[32, 64, 128, 256, 512])
    args = parser.parse_args()
    try:
        sizes = parse_sizes(args.sizes)
    except ValueError as error:
        parser.error(str(error))
    report(sizes)


if __name__ == "__main__":
    main()

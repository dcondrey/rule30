"""Search for an exact hierarchical tile grammar in Rule 30 spacetime.

This is deliberately orthogonal to closed forms for the center sequence.  A
power-of-two spacetime window is partitioned recursively into quadrants.  At
each scale, equal tiles receive the same canonical ID, producing an exact
quadtree DAG with no hash-collision assumptions.

If the number of reusable tile types stays bounded or polylogarithmic as the
horizon doubles, the DAG suggests a finite substitution algebra from which a
jump-ahead algorithm might be derived.  If it scales like the area, this route
is behaving like incompressible data and should be closed.  The DAG is only a
diagnostic: building it still evaluates the full window and is not itself a
shortcut.

Rule 90 is the exact self-similar positive control.  A deterministic random
triangle is the incompressible control.  Rule 22 tests a nonlinear symmetric
system, and Rule 30 is the target.
"""

from __future__ import annotations

import argparse
import math
import struct
import zlib
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from support_state_probe import RULE_22, RULE_30, eca_rows


RULE_90 = 90

DIHEDRAL_TRANSFORMS = (
    "identity", "mirror_lr", "mirror_ud", "rotate_180",
    "transpose", "rotate_90", "rotate_270", "anti_transpose",
)


@dataclass(frozen=True)
class TileGrammar:
    side: int
    root: int
    # definitions[level][node_id] = (top_left, top_right, bottom_left, bottom_right)
    definitions: tuple[dict[int, tuple[int, int, int, int]], ...]
    occurrences: tuple[dict[int, int], ...]

    @property
    def levels(self) -> int:
        return self.side.bit_length() - 1

    @property
    def type_counts(self) -> tuple[int, ...]:
        return (2, *(len(level) for level in self.definitions[1:]))

    @property
    def dag_nodes(self) -> int:
        return 2 + sum(len(level) for level in self.definitions[1:])

    def bit_at(self, row: int, column: int) -> int:
        if not (0 <= row < self.side and 0 <= column < self.side):
            raise IndexError("tile coordinate outside grammar root")
        node = self.root
        for level in range(self.levels, 0, -1):
            half = 1 << (level - 1)
            bottom = row >= half
            right = column >= half
            quadrant = (2 if bottom else 0) + (1 if right else 0)
            node = self.definitions[level][node][quadrant]
            if bottom:
                row -= half
            if right:
                column -= half
        return node

    def render_tile(self, level: int, node: int) -> list[list[int]]:
        if not (0 <= level <= self.levels):
            raise ValueError("tile level outside grammar")
        memo: dict[tuple[int, int], list[list[int]]] = {}

        def render(current_level: int, current_node: int) -> list[list[int]]:
            key = (current_level, current_node)
            if key in memo:
                return memo[key]
            if current_level == 0:
                result = [[current_node]]
            else:
                children = self.definitions[current_level][current_node]
                quadrants = [render(current_level - 1, child) for child in children]
                half = 1 << (current_level - 1)
                result = [
                    quadrants[0][row] + quadrants[1][row]
                    for row in range(half)
                ] + [
                    quadrants[2][row] + quadrants[3][row]
                    for row in range(half)
                ]
            memo[key] = result
            return result

        return render(level, node)


@dataclass(frozen=True)
class DirectionalReuse:
    horizontal_equal: int
    horizontal_pairs: int
    vertical_equal: int
    vertical_pairs: int
    horizontal_strips: int
    horizontal_unique: int
    horizontal_periodic: int
    vertical_strips: int
    vertical_unique: int
    vertical_periodic: int


@dataclass(frozen=True)
class DirectionalWords:
    horizontal_observations: int
    horizontal_types: int
    horizontal_reflection_types: int
    vertical_observations: int
    vertical_types: int
    vertical_reflection_types: int


@dataclass(frozen=True)
class GreedyBoundarySignature:
    tile_types: int
    information_lower_bound: int
    selected_bits: tuple[int, ...]
    unresolved_groups: int
    largest_unresolved_group: int


def build_tile_grammar(bits: Sequence[int], side: int) -> TileGrammar:
    if side < 1 or side & (side - 1):
        raise ValueError("side must be a positive power of two")
    if len(bits) != side * side or any(bit not in (0, 1) for bit in bits):
        raise ValueError("bits must be a square binary grid")
    levels = side.bit_length() - 1
    definitions: list[dict[int, tuple[int, int, int, int]]] = [{} for _ in range(levels + 1)]
    occurrences: list[dict[int, int]] = [{} for _ in range(levels + 1)]
    occurrences[0] = {0: len(bits) - sum(bits), 1: sum(bits)}
    current = list(bits)
    width = side
    for level in range(1, levels + 1):
        unique: dict[tuple[int, int, int, int], int] = {}
        reverse: dict[int, tuple[int, int, int, int]] = {}
        counts: dict[int, int] = {}
        next_grid: list[int] = []
        for row in range(0, width, 2):
            top = row * width
            bottom = (row + 1) * width
            for column in range(0, width, 2):
                key = (
                    current[top + column],
                    current[top + column + 1],
                    current[bottom + column],
                    current[bottom + column + 1],
                )
                identifier = unique.get(key)
                if identifier is None:
                    identifier = len(unique)
                    unique[key] = identifier
                    reverse[identifier] = key
                counts[identifier] = counts.get(identifier, 0) + 1
                next_grid.append(identifier)
        definitions[level] = reverse
        occurrences[level] = counts
        current = next_grid
        width //= 2
    return TileGrammar(side, current[0], tuple(definitions), tuple(occurrences))


def splitmix64(value: int) -> int:
    value = (value + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
    value = ((value ^ (value >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
    value = ((value ^ (value >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
    return value ^ (value >> 31)


def eca_grid(rule: int, horizon: int) -> tuple[list[int], int]:
    """Square containing `horizon` rows and the full width-2*horizon cone."""
    side = 2 * horizon
    rows = eca_rows(rule, horizon - 1)
    center = horizon
    grid = [0] * (side * side)
    for time, packed in enumerate(rows):
        offset = time * side
        for column in range(side):
            position = column - horizon
            grid[offset + column] = (packed >> (center + position)) & 1
    return grid, side


def active_cone_complement(bits: Sequence[int], side: int, horizon: int) -> tuple[list[int], int]:
    """Flip cells inside the causal triangle while preserving the exterior mask."""
    if side != 2 * horizon or len(bits) != side * side:
        raise ValueError("expected the standard width-2*horizon spacetime square")
    complemented = list(bits)
    center = horizon
    for time in range(horizon):
        offset = time * side
        for column in range(center - time, center + time + 1):
            complemented[offset + column] ^= 1
    return complemented, side


def eca_zero_grid(rule: int, horizon: int) -> tuple[list[int], int]:
    bits, side = eca_grid(rule, horizon)
    return active_cone_complement(bits, side, horizon)


def random_triangle_grid(horizon: int) -> tuple[list[int], int]:
    side = 2 * horizon
    grid = [0] * (side * side)
    for time in range(horizon):
        offset = time * side
        for column in range(side):
            position = column - horizon
            if abs(position) <= time:
                key = ((time & 0xFFFFFFFF) << 32) ^ (position & 0xFFFFFFFF)
                grid[offset + column] = splitmix64(key) & 1
    grid[horizon] = 1
    return grid, side


def fit_exponent(points: Sequence[tuple[int, int]]) -> float:
    xs = [math.log(horizon) for horizon, _ in points]
    ys = [math.log(nodes) for _, nodes in points]
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    return sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / sum(
        (x - mean_x) ** 2 for x in xs
    )


def edge_vocabulary(bits: Sequence[int], side: int, scale: int) -> tuple[int, int, int, int]:
    """Return edge words, perimeter signatures, tile types, ambiguous signatures."""
    if scale < 1 or scale > side or scale & (scale - 1) or side % scale:
        raise ValueError("scale must be an aligned power-of-two tile size")
    edges: set[int] = set()
    signatures: dict[tuple[int, int, int, int], int] = {}
    tile_types: set[int] = set()
    ambiguous: set[tuple[int, int, int, int]] = set()
    for top in range(0, side, scale):
        for left in range(0, side, scale):
            top_edge = bottom_edge = left_edge = right_edge = tile_word = 0
            for row in range(scale):
                row_offset = (top + row) * side + left
                for column in range(scale):
                    bit = bits[row_offset + column]
                    tile_word |= bit << (row * scale + column)
                    if row == 0:
                        top_edge |= bit << column
                    if row == scale - 1:
                        bottom_edge |= bit << column
                    if column == 0:
                        left_edge |= bit << row
                    if column == scale - 1:
                        right_edge |= bit << row
            signature = (top_edge, right_edge, bottom_edge, left_edge)
            edges.update(signature)
            tile_types.add(tile_word)
            previous = signatures.setdefault(signature, tile_word)
            if previous != tile_word:
                ambiguous.add(signature)
    return len(edges), len(signatures), len(tile_types), len(ambiguous)


def _perimeter_bits(word: int, side: int) -> tuple[int, ...]:
    coordinates = (
        [(0, column) for column in range(side)]
        + [(row, side - 1) for row in range(1, side)]
        + [(side - 1, column) for column in range(side - 2, -1, -1)]
        + [(row, 0) for row in range(side - 2, 0, -1)]
    )
    return tuple((word >> (row * side + column)) & 1 for row, column in coordinates)


def greedy_boundary_signature(
    bits: Sequence[int], side: int, scale: int
) -> GreedyBoundarySignature:
    """Greedily select perimeter positions that distinguish observed tile types.

    This gives an upper bound for a sampled boundary signature, not a proof of
    minimality or a rule for unseen tiles.
    """
    words = sorted({word for row in aligned_tile_words(bits, side, scale) for word in row})
    vectors = [_perimeter_bits(word, scale) for word in words]
    groups: list[list[int]] = [list(range(len(words)))]
    available = set(range(max(1, 4 * scale - 4)))
    selected: list[int] = []
    while any(len(group) > 1 for group in groups):
        best_position = -1
        best_score = 0
        for position in sorted(available):
            score = 0
            for group in groups:
                ones = sum(vectors[index][position] for index in group)
                score += ones * (len(group) - ones)
            if score > best_score:
                best_position = position
                best_score = score
        if best_position < 0:
            break
        selected.append(best_position)
        available.remove(best_position)
        refined: list[list[int]] = []
        for group in groups:
            zeros = [index for index in group if not vectors[index][best_position]]
            ones = [index for index in group if vectors[index][best_position]]
            if zeros:
                refined.append(zeros)
            if ones:
                refined.append(ones)
        groups = refined
    unresolved = [group for group in groups if len(group) > 1]
    return GreedyBoundarySignature(
        len(words),
        math.ceil(math.log2(max(1, len(words)))),
        tuple(selected),
        len(unresolved),
        max(map(len, unresolved), default=1),
    )


def aligned_tile_words(bits: Sequence[int], side: int, scale: int) -> list[list[int]]:
    """Encode each aligned scale-by-scale tile as an exact integer."""
    if len(bits) != side * side:
        raise ValueError("bits must be a square grid")
    if scale < 1 or scale > side or scale & (scale - 1) or side % scale:
        raise ValueError("scale must be an aligned power-of-two tile size")
    result: list[list[int]] = []
    for top in range(0, side, scale):
        tile_row: list[int] = []
        for left in range(0, side, scale):
            word = 0
            for row in range(scale):
                offset = (top + row) * side + left
                for column in range(scale):
                    word |= bits[offset + column] << (row * scale + column)
            tile_row.append(word)
        result.append(tile_row)
    return result


def transform_tile_word(word: int, side: int, transform: str) -> int:
    """Apply one square dihedral transform to a row-major tile word."""
    if side < 1 or transform not in DIHEDRAL_TRANSFORMS:
        raise ValueError("invalid tile side or transform")
    transformed = 0
    for row in range(side):
        for column in range(side):
            if not (word >> (row * side + column)) & 1:
                continue
            if transform == "identity":
                target_row, target_column = row, column
            elif transform == "mirror_lr":
                target_row, target_column = row, side - 1 - column
            elif transform == "mirror_ud":
                target_row, target_column = side - 1 - row, column
            elif transform == "rotate_180":
                target_row, target_column = side - 1 - row, side - 1 - column
            elif transform == "transpose":
                target_row, target_column = column, row
            elif transform == "rotate_90":
                target_row, target_column = column, side - 1 - row
            elif transform == "rotate_270":
                target_row, target_column = side - 1 - column, row
            else:
                target_row, target_column = side - 1 - column, side - 1 - row
            transformed |= 1 << (target_row * side + target_column)
    return transformed


def symmetry_quotient(bits: Sequence[int], side: int, scale: int) -> tuple[int, int, int, int]:
    """Return raw, left/right-quotiented, D4-quotiented, and mirror-fixed type counts."""
    words = {word for row in aligned_tile_words(bits, side, scale) for word in row}
    left_right = {
        min(word, transform_tile_word(word, scale, "mirror_lr")) for word in words
    }
    dihedral = {
        min(transform_tile_word(word, scale, transform) for transform in DIHEDRAL_TRANSFORMS)
        for word in words
    }
    mirror_fixed = sum(
        word == transform_tile_word(word, scale, "mirror_lr") for word in words
    )
    return len(words), len(left_right), len(dihedral), mirror_fixed


def _trim_zeros(values: Sequence[int]) -> tuple[int, ...]:
    first = 0
    last = len(values)
    while first < last and values[first] == 0:
        first += 1
    while last > first and values[last - 1] == 0:
        last -= 1
    return tuple(values[first:last])


def _has_exact_repeat(values: Sequence[int]) -> bool:
    """Whether a sequence contains at least two copies of one exact period."""
    if len(values) < 2:
        return False
    prefix = [0] * len(values)
    for index in range(1, len(values)):
        candidate = prefix[index - 1]
        while candidate and values[index] != values[candidate]:
            candidate = prefix[candidate - 1]
        if values[index] == values[candidate]:
            candidate += 1
        prefix[index] = candidate
    period = len(values) - prefix[-1]
    return period <= len(values) // 2


def directional_tile_reuse(bits: Sequence[int], side: int, scale: int) -> DirectionalReuse:
    """Separate exact horizontal (space) from vertical (time) tile recurrence."""
    tiles = aligned_tile_words(bits, side, scale)
    width = len(tiles)
    horizontal_equal = horizontal_pairs = 0
    vertical_equal = vertical_pairs = 0
    for row in range(width):
        for column in range(width - 1):
            left, right = tiles[row][column : column + 2]
            if left or right:
                horizontal_pairs += 1
                horizontal_equal += left == right
    for row in range(width - 1):
        for column in range(width):
            top, bottom = tiles[row][column], tiles[row + 1][column]
            if top or bottom:
                vertical_pairs += 1
                vertical_equal += top == bottom

    horizontal = [_trim_zeros(row) for row in tiles]
    vertical = [
        _trim_zeros([tiles[row][column] for row in range(width)])
        for column in range(width)
    ]
    horizontal = [strip for strip in horizontal if strip]
    vertical = [strip for strip in vertical if strip]
    return DirectionalReuse(
        horizontal_equal, horizontal_pairs, vertical_equal, vertical_pairs,
        len(horizontal), len(set(horizontal)), sum(map(_has_exact_repeat, horizontal)),
        len(vertical), len(set(vertical)), sum(map(_has_exact_repeat, vertical)),
    )


def _reverse_word(word: int, length: int) -> int:
    reversed_word = 0
    for _ in range(length):
        reversed_word = (reversed_word << 1) | (word & 1)
        word >>= 1
    return reversed_word


def directional_word_vocabulary(bits: Sequence[int], side: int, length: int) -> DirectionalWords:
    """Count all nonzero horizontal/vertical words, including unaligned starts."""
    if len(bits) != side * side or length < 1 or length > side:
        raise ValueError("invalid square grid or word length")
    mask = (1 << length) - 1
    horizontal: set[int] = set()
    vertical: set[int] = set()
    horizontal_observations = vertical_observations = 0
    for row in range(side):
        offset = row * side
        word = sum(bits[offset + column] << column for column in range(length))
        for start in range(side - length + 1):
            if word:
                horizontal_observations += 1
                horizontal.add(word)
            if start + length < side:
                word = (word >> 1) | (bits[offset + start + length] << (length - 1))
                word &= mask
    for column in range(side):
        word = sum(bits[row * side + column] << row for row in range(length))
        for start in range(side - length + 1):
            if word:
                vertical_observations += 1
                vertical.add(word)
            if start + length < side:
                word = (word >> 1) | (bits[(start + length) * side + column] << (length - 1))
                word &= mask
    horizontal_reflections = {
        min(word, _reverse_word(word, length)) for word in horizontal
    }
    vertical_reflections = {
        min(word, _reverse_word(word, length)) for word in vertical
    }
    return DirectionalWords(
        horizontal_observations,
        len(horizontal),
        len(horizontal_reflections),
        vertical_observations,
        len(vertical),
        len(vertical_reflections),
    )


def png_chunk(kind: bytes, payload: bytes) -> bytes:
    return (
        struct.pack(">I", len(payload))
        + kind
        + payload
        + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
    )


def write_grayscale_png(path: Path, width: int, height: int, pixels: bytearray) -> None:
    rows = b"".join(
        b"\x00" + bytes(pixels[row * width : (row + 1) * width])
        for row in range(height)
    )
    payload = (
        b"\x89PNG\r\n\x1a\n"
        + png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0))
        + png_chunk(b"IDAT", zlib.compress(rows, level=9))
        + png_chunk(b"IEND", b"")
    )
    path.write_bytes(payload)


def write_atlas(path: Path, grammar: TileGrammar, scales: Sequence[int], top_k: int = 8) -> None:
    tile_pixels = 128
    gutter = 8
    width = gutter + top_k * (tile_pixels + gutter)
    height = gutter + len(scales) * (tile_pixels + gutter)
    pixels = bytearray([255]) * (width * height)
    print("\natlas_row scale rank node occurrences")
    for atlas_row, scale in enumerate(scales):
        if scale > grammar.side or scale & (scale - 1):
            raise ValueError("atlas scales must be powers of two within the grammar")
        level = scale.bit_length() - 1
        frequent = sorted(
            grammar.occurrences[level].items(),
            key=lambda item: (-item[1], item[0]),
        )[:top_k]
        factor = max(1, tile_pixels // scale)
        rendered_size = scale * factor
        y_origin = gutter + atlas_row * (tile_pixels + gutter)
        for rank, (node, count) in enumerate(frequent, start=1):
            print(f"{atlas_row:9d} {scale:5d} {rank:4d} {node:4d} {count:11d}")
            x_origin = gutter + (rank - 1) * (tile_pixels + gutter)
            tile = grammar.render_tile(level, node)
            for row, values in enumerate(tile):
                for column, bit in enumerate(values):
                    color = 0 if bit else 255
                    for dy in range(factor):
                        start = (y_origin + row * factor + dy) * width + x_origin + column * factor
                        pixels[start : start + factor] = bytes([color]) * factor
            # Light gray frame makes empty/white tiles visible.
            for x in range(x_origin, x_origin + rendered_size):
                pixels[(y_origin + rendered_size - 1) * width + x] = min(
                    pixels[(y_origin + rendered_size - 1) * width + x], 192
                )
            for y in range(y_origin, y_origin + rendered_size):
                pixels[y * width + x_origin + rendered_size - 1] = min(
                    pixels[y * width + x_origin + rendered_size - 1], 192
                )
    write_grayscale_png(path, width, height, pixels)


def parse_sizes(raw_sizes: Sequence[int]) -> list[int]:
    sizes = sorted(set(raw_sizes))
    if len(sizes) < 2 or any(size < 2 or size & (size - 1) for size in sizes):
        raise ValueError("provide at least two distinct power-of-two horizons")
    return sizes


def report(sizes: Sequence[int], atlas_path: Path | None = None) -> None:
    sources: tuple[tuple[str, Callable[[int], tuple[list[int], int]]], ...] = (
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
    measurements: dict[str, list[tuple[int, int]]] = {name: [] for name, _ in sources}
    largest: dict[str, TileGrammar] = {}
    largest_bits: dict[str, list[int]] = {}
    print("source horizon raw_bits dag_nodes compression")
    for name, make_grid in sources:
        for horizon in sizes:
            bits, side = make_grid(horizon)
            grammar = build_tile_grammar(bits, side)
            for index, bit in enumerate(bits):
                assert grammar.bit_at(index // side, index % side) == bit
            measurements[name].append((horizon, grammar.dag_nodes))
            largest[name] = grammar
            largest_bits[name] = bits
            print(
                f"{name:7s} {horizon:7d} {len(bits):8d} {grammar.dag_nodes:9d} "
                f"{len(bits) / grammar.dag_nodes:11.3f}"
            )

    print("\nsource dag_node_exponent")
    for name, points in measurements.items():
        print(f"{name:7s} {fit_exponent(points):17.6f}")

    print("\nscale tile_count " + " ".join(name for name, _ in sources))
    side = largest["rule30"].side
    for level in range(largest["rule30"].levels + 1):
        scale = 1 << level
        tile_count = (side // scale) ** 2
        counts = [largest[name].type_counts[level] for name, _ in sources]
        print(
            f"{scale:5d} {tile_count:10d} "
            + " ".join(f"{count:12d}" for count in counts)
        )

    print("\nsource scale edge_words perimeter_signatures tile_types ambiguous_perimeters")
    for name, _ in sources:
        for scale in (4, 8, 16, 32, 64):
            if scale > side:
                continue
            edge_words, signatures, tile_types, ambiguous = edge_vocabulary(
                largest_bits[name], side, scale
            )
            print(
                f"{name:7s} {scale:5d} {edge_words:10d} {signatures:20d} "
                f"{tile_types:10d} {ambiguous:20d}"
            )

    print("\nsource scale raw_types mirror_types d4_types mirror_fixed")
    for name, _ in sources:
        for scale in (4, 8, 16, 32, 64):
            if scale > side:
                continue
            raw, mirrored, dihedral, fixed = symmetry_quotient(largest_bits[name], side, scale)
            print(f"{name:7s} {scale:5d} {raw:9d} {mirrored:12d} {dihedral:8d} {fixed:12d}")

    print("\nsource scale tile_types info_lower_bound selected_perimeter_bits unresolved_groups max_group")
    for name, _ in sources:
        for scale in (4, 8, 16, 32, 64):
            if scale > side:
                continue
            signature = greedy_boundary_signature(largest_bits[name], side, scale)
            print(
                f"{name:13s} {scale:5d} {signature.tile_types:10d} "
                f"{signature.information_lower_bound:16d} {len(signature.selected_bits):23d} "
                f"{signature.unresolved_groups:17d} {signature.largest_unresolved_group:9d}"
            )

    print(
        "\nsource scale horizontal_equal/pairs vertical_equal/pairs "
        "horizontal_unique/strips/periodic vertical_unique/strips/periodic"
    )
    for name, _ in sources:
        for scale in (4, 8, 16, 32, 64):
            if scale > side:
                continue
            reuse = directional_tile_reuse(largest_bits[name], side, scale)
            print(
                f"{name:7s} {scale:5d} "
                f"{reuse.horizontal_equal:6d}/{reuse.horizontal_pairs:<6d} "
                f"{reuse.vertical_equal:6d}/{reuse.vertical_pairs:<6d} "
                f"{reuse.horizontal_unique:6d}/{reuse.horizontal_strips:<6d}/"
                f"{reuse.horizontal_periodic:<6d} "
                f"{reuse.vertical_unique:6d}/{reuse.vertical_strips:<6d}/"
                f"{reuse.vertical_periodic:<6d}"
            )

    print(
        "\nsource length horizontal_types/observations/reflection_types "
        "vertical_types/observations/reflection_types"
    )
    for name, _ in sources:
        for length in (4, 8, 16, 32, 64):
            if length > side:
                continue
            words = directional_word_vocabulary(largest_bits[name], side, length)
            print(
                f"{name:7s} {length:6d} "
                f"{words.horizontal_types:8d}/{words.horizontal_observations:<8d}/"
                f"{words.horizontal_reflection_types:<8d} "
                f"{words.vertical_types:8d}/{words.vertical_observations:<8d}/"
                f"{words.vertical_reflection_types:<8d}"
            )

    if atlas_path is not None:
        atlas_scales = [scale for scale in (4, 8, 16, 32, 64) if scale <= side]
        write_atlas(atlas_path, largest["rule30"], atlas_scales)
        print(f"atlas={atlas_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", nargs="+", type=int, default=[32, 64, 128, 256, 512])
    parser.add_argument("--atlas", type=Path)
    args = parser.parse_args()
    try:
        sizes = parse_sizes(args.sizes)
    except ValueError as error:
        parser.error(str(error))
    report(sizes, args.atlas)


if __name__ == "__main__":
    main()

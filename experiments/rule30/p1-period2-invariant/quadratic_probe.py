#!/usr/bin/env python3
"""Triangular inverse-Gray correlations and a fixed-summary closure probe."""

from __future__ import annotations

import argparse
from itertools import combinations_with_replacement

from bilateral_hardcore import forced_rho, hard_core
from carry_transducer import gray_inverse, gray_macro, seed_state


def parity(value: int) -> int:
    return value.bit_count() & 1


def index_mask(width: int, residue: int) -> int:
    return sum(1 << index for index in range(residue, width, 2))


def gray_correlation_direct(x: int, y: int, width: int, residue: int | None) -> int:
    product = gray_inverse(x) & gray_inverse(y)
    if residue is not None:
        product &= index_mask(width, residue)
    return parity(product)


def count_residue_through(endpoint: int, residue: int) -> int:
    if residue == 0:
        return (endpoint + 2) // 2
    return (endpoint + 1) // 2


def gray_correlation_triangular(
    x: int, y: int, width: int, residue: int | None
) -> int:
    """Evaluate x^T P^T E P y directly from its triangular kernel."""
    answer = 0
    for i in range(width):
        if not ((x >> i) & 1):
            continue
        for j in range(width):
            if not ((y >> j) & 1):
                continue
            endpoint = min(i, j)
            count = endpoint + 1 if residue is None else count_residue_through(
                endpoint, residue
            )
            answer ^= count & 1
    return answer


def matrix(width: int, residue: int | None) -> list[int]:
    rows = []
    for i in range(width):
        row = 0
        for j in range(width):
            endpoint = min(i, j)
            count = endpoint + 1 if residue is None else count_residue_through(
                endpoint, residue
            )
            row |= (count & 1) << j
        rows.append(row)
    return rows


def gf2_rank(rows: list[int]) -> int:
    work = rows[:]
    rank = 0
    while work:
        pivot = max(work)
        if not pivot:
            break
        rank += 1
        bit = 1 << (pivot.bit_length() - 1)
        work = [row ^ pivot if row & bit else row for row in work if row != pivot]
    return rank


def exhaustive_identity(max_width: int) -> list[tuple[int, int, int, int]]:
    results = []
    for width in range(1, max_width + 1):
        checked = 0
        for x in range(1 << width):
            for y in range(1 << width):
                for residue in (None, 0, 1):
                    direct = gray_correlation_direct(x, y, width, residue)
                    triangular = gray_correlation_triangular(x, y, width, residue)
                    if direct != triangular:
                        raise AssertionError((width, x, y, residue))
                checked += 1
        ranks = tuple(gf2_rank(matrix(width, residue)) for residue in (None, 0, 1))
        results.append((width, checked, *ranks))
        print(
            f"width={width:2d}: {checked:6d} pairs PASS; "
            f"rank(full,even,odd)={ranks}"
        )
    return results


WORD_NAMES = ("A", "V", "C", "S")


def macro_words(state: tuple[int, int, int]) -> dict[str, int]:
    _, A, B = state
    V = 1 | (B << 1)
    C = gray_inverse(A | V)
    S = A << 1
    return {"A": A, "V": V, "C": C, "S": S}


def quadratic_summary(state: tuple[int, int, int]) -> tuple[int, ...]:
    """Registered fixed family: split parities and all split Gray pairings."""
    T, _, _ = state
    words = macro_words(state)
    width = T + 2
    values: list[int] = [T & 15]
    for name in WORD_NAMES:
        word = words[name]
        values.extend(
            (
                parity(word & index_mask(width, 0)),
                parity(word & index_mask(width, 1)),
                word & 1,
                (word >> max(0, T - 1)) & 1,
            )
        )
    for left, right in combinations_with_replacement(WORD_NAMES, 2):
        for residue in (0, 1):
            values.append(
                gray_correlation_direct(words[left], words[right], width, residue)
            )
    return tuple(values)


def closure_collision(
    max_seed_length: int, max_follow: int
) -> tuple[object, ...] | None:
    """Find an equal-T collision on legal hard-core finite-seed paths."""
    seen: dict[tuple[int, int, tuple[int, ...]], tuple[object, ...]] = {}
    for length in range(1, max_seed_length + 1):
        for seed in range(1 << length):
            if not hard_core(seed):
                continue
            state = seed_state(seed, length)
            previous = (seed >> (length - 1)) & 1
            for follow in range(max_follow + 1):
                rho = forced_rho(state)
                pin, successor = gray_macro(state)
                valid_hard_core = not (previous == rho == 1)
                signature = (
                    rho,
                    pin,
                    valid_hard_core,
                    quadratic_summary(successor),
                )
                # The previous rho bit is part of the hard-core automaton and
                # must be retained; omitting it would create a trivial control
                # collision unrelated to the quadratic state.
                key = state[0], previous, quadratic_summary(state)
                origin = length, seed, follow, state
                old = seen.get(key)
                if old is not None and old[0] != signature:
                    return key, old, (signature, origin)
                seen.setdefault(key, (signature, origin))
                if not valid_hard_core or not pin:
                    break
                previous = rho
                state = successor
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-width", type=int, default=8)
    parser.add_argument("--max-seed", type=int, default=16)
    parser.add_argument("--max-follow", type=int, default=32)
    args = parser.parse_args()
    exhaustive_identity(args.max_width)
    collision = closure_collision(args.max_seed, args.max_follow)
    if collision is None:
        print("no quadratic-summary closure collision in registered range")
    else:
        key, old, new = collision
        old_signature, old_origin = old
        new_signature, new_origin = new
        differing = [
            index
            for index, (left, right) in enumerate(
                zip(old_signature[3], new_signature[3])
            )
            if left != right
        ]
        print(f"quadratic-summary closure collision at T={key[0]}, previous-rho={key[1]}")
        print(f"  first origin={old_origin}")
        print(f"  second origin={new_origin}")
        print(
            "  common current (forced-rho,pin,hard-core-valid)="
            f"{old_signature[:3]}"
        )
        print(f"  differing successor-summary indices={differing}")


if __name__ == "__main__":
    main()

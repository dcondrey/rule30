#!/usr/bin/env python3
"""Exact controls for the moving endpoint-flip cocycle.

The inverse-cut coordinate at time ``t`` reads endpoint coordinates
``floor(t/2)..t``.  Consequently changing endpoint coordinate ``k`` can
change cut coordinates only in ``k..2k+1``.  This checker applies that window
to the order-preserving operation that flips hard-core endpoint symbols from
1 to 2 one at a time.
"""

from __future__ import annotations

import argparse
from itertools import product

from dyadic_periodicity_analyzer import inverse_cone_diagonal
from rank_zero_separator import hard_core, hard_core_prefixes


Vector = tuple[int, ...]


def dependency_window(time: int) -> range:
    return range(time // 2, time + 1)


def influence_interval(coordinate: int, length: int) -> range:
    return range(coordinate, min(length, 2 * coordinate + 2))


def change(endpoint: Vector, coordinate: int, value: int) -> Vector:
    return endpoint[:coordinate] + (value,) + endpoint[coordinate + 1 :]


def arbitrary_flip_controls(max_length: int) -> tuple[int, int]:
    """Check compact influence on the full four-symbol endpoint alphabet."""

    words = 0
    flips = 0
    for length in range(1, max_length + 1):
        for endpoint in product(range(4), repeat=length):
            cut = inverse_cone_diagonal(endpoint)
            words += 1
            for coordinate in range(length):
                for value in range(4):
                    if value == endpoint[coordinate]:
                        continue
                    following = inverse_cone_diagonal(
                        change(endpoint, coordinate, value)
                    )
                    allowed = set(influence_interval(coordinate, length))
                    differences = {
                        index
                        for index, pair in enumerate(zip(cut, following))
                        if pair[0] != pair[1]
                    }
                    assert differences <= allowed
                    # Triangular bijectivity makes the first influenced cut
                    # coordinate change for every genuine endpoint change.
                    assert coordinate in differences
                    flips += 1
    return words, flips


def hard_core_cocycle_controls(max_length: int) -> tuple[int, int]:
    """Flip hard-core 1s left-to-right and check every exact update window."""

    words = 0
    updates = 0
    for length in range(1, max_length + 1):
        for endpoint in hard_core_prefixes(length):
            current_endpoint = endpoint
            current_cut = inverse_cone_diagonal(current_endpoint)
            for coordinate, value in enumerate(endpoint):
                if value != 1:
                    continue
                following_endpoint = change(current_endpoint, coordinate, 2)
                assert hard_core(following_endpoint)
                following_cut = inverse_cone_diagonal(following_endpoint)
                allowed = set(influence_interval(coordinate, length))
                differences = {
                    index
                    for index, pair in enumerate(zip(current_cut, following_cut))
                    if pair[0] != pair[1]
                }
                assert differences <= allowed
                assert coordinate in differences
                current_endpoint = following_endpoint
                current_cut = following_cut
                updates += 1
            assert current_endpoint == (2,) * length
            words += 1
    return words, updates


def all_two_window_controls(max_length: int) -> int:
    """Check the nonzero-window covering consequence on hard-core words."""

    checked = 0
    for length in range(1, max_length + 1):
        baseline = inverse_cone_diagonal((2,) * length)
        assert all(value in (1, 2) for value in baseline)
        for endpoint in hard_core_prefixes(length):
            cut = inverse_cone_diagonal(endpoint)
            for time in range(length):
                window = dependency_window(time)
                if all(endpoint[index] == 2 for index in window):
                    assert cut[time] == baseline[time]
                    assert cut[time] != 0
                checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-arbitrary-length", type=int, default=7)
    parser.add_argument("--max-hard-core-length", type=int, default=16)
    args = parser.parse_args()
    if args.max_arbitrary_length < 1 or args.max_hard_core_length < 1:
        parser.error("length bounds must be positive")

    words, flips = arbitrary_flip_controls(args.max_arbitrary_length)
    print(
        f"arbitrary endpoint compact-influence controls: "
        f"{words} words, {flips} flips PASS"
    )
    words, updates = hard_core_cocycle_controls(args.max_hard_core_length)
    print(
        f"hard-core left-to-right flip cocycle: "
        f"{words} words, {updates} updates PASS"
    )
    windows = all_two_window_controls(args.max_hard_core_length)
    print(f"all-two nonzero-window covering controls: {windows} cells PASS")


if __name__ == "__main__":
    main()

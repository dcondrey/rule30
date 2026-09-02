#!/usr/bin/env python3
"""Solver-free controls for high-bit elimination in the binary wedge.

For ``G_n = P^n o I``, fix the first ``n`` endpoint symbols in ``{1,2}``.
Requiring every newly exposed output of ``G_n`` to have high bit one
determines each subsequent binary endpoint symbol uniquely.  The remaining
output coordinate is the equality/defect bit ``E=1+H+L``.

The local affine argument is uniform in ``n``.  The finite enumerations below
are regression controls, not a proof of the remaining constant-defect claim.
"""

from __future__ import annotations

import argparse
from itertools import product

from dyadic_periodicity_analyzer import inverse_terminal_cone
from rank_zero_separator import peel_power


Vector = tuple[int, ...]
Permutation = tuple[int, int, int, int]


def wedge(endpoint: Vector, depth: int) -> Vector:
    if not 0 <= depth <= len(endpoint):
        raise ValueError("invalid Peel depth")
    return peel_power(inverse_terminal_cone(endpoint), depth)


def affine_coordinates(permutation: Permutation) -> tuple[int, int, int]:
    """Decode ``(h,l)->(h+a,l+b*h+g)`` and reject non-D8 maps."""

    alpha = permutation[0] >> 1
    gamma = permutation[0] & 1
    beta = (permutation[2] & 1) ^ gamma

    def apply(state: int) -> int:
        high, low = state >> 1, state & 1
        return 2 * (high ^ alpha) + (low ^ (beta & high) ^ gamma)

    if tuple(map(apply, range(4))) != permutation:
        raise ValueError(f"not an affine D8 permutation: {permutation}")
    return alpha, beta, gamma


def newest_permutation(prefix: Vector, depth: int) -> Permutation:
    """Map the final endpoint symbol to the newest ``G_depth`` cell."""

    if depth > len(prefix):
        raise ValueError("the prefix must expose an output after appending")
    return tuple(wedge(prefix + (state,), depth)[-1] for state in range(4))  # type: ignore[return-value]


def force_high_one(source: Vector, count: int) -> tuple[Vector, Vector]:
    """Append ``count`` unique binary symbols making all wedge highs one."""

    depth = len(source)
    endpoint = source
    for _ in range(count):
        choices = tuple(
            state
            for state in (1, 2)
            if wedge(endpoint + (state,), depth)[-1] >> 1 == 1
        )
        assert len(choices) == 1
        endpoint += choices
    output = wedge(endpoint, depth)
    assert len(output) == count and all(state >> 1 for state in output)
    defect = tuple(1 ^ (state >> 1) ^ (state & 1) for state in output)
    return endpoint[depth:], defect


def affine_controls(max_prefix: int) -> int:
    checked = 0
    found: set[Permutation] = set()
    for length in range(max_prefix + 1):
        for prefix in product(range(4), repeat=length):
            for depth in range(length + 1):
                permutation = newest_permutation(prefix, depth)
                alpha, _beta, _gamma = affine_coordinates(permutation)
                found.add(permutation)
                choices = tuple(
                    state
                    for state in (1, 2)
                    if permutation[state] >> 1 == 1
                )
                assert choices == (2 - alpha,)
                checked += 1
    assert len(found) == 8
    return checked


def elimination_controls(max_source: int) -> int:
    checked = 0
    for length in range(1, max_source + 1):
        for source in product((1, 2), repeat=length):
            suffix, defect = force_high_one(source, length + 2)
            assert len(suffix) == len(defect) == length + 2
            endpoint = source + suffix
            output = wedge(endpoint, length)
            assert all(state in (2, 3) for state in output)
            assert tuple(state & 1 for state in output) == defect
            for tail in (2, 3):
                target_defect = tail & 1
                target = (tail,) * (length + 2)
                constant_defect = (target_defect,) * (length + 2)
                assert (output == target) == (defect == constant_defect)
            checked += 1
    return checked


def sharp_counterexample_control() -> tuple[str, str]:
    source = tuple(map(int, "111122211212112"))
    suffix, defect = force_high_one(source, len(source) + 2)
    assert suffix == tuple(map(int, "12211111122111211"))
    assert defect == (1,) * 16 + (0,)
    # The first 16 outputs are state 3, then the defect flips to state 2.
    assert wedge(source + suffix, len(source)) == (3,) * 16 + (2,)
    return "".join(map(str, suffix)), "".join(map(str, defect))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-prefix", type=int, default=5)
    parser.add_argument("--max-source", type=int, default=7)
    args = parser.parse_args()
    if args.max_prefix < 0 or args.max_source < 1:
        parser.error("invalid control bound")

    affine = affine_controls(args.max_prefix)
    eliminated = elimination_controls(args.max_source)
    suffix, defect = sharp_counterexample_control()
    print(f"newest-cell affine D8 controls: {affine} cases PASS")
    print(f"binary high-elimination controls: {eliminated} sources PASS")
    print(f"n=15 sharp suffix={suffix} defect={defect} PASS")


if __name__ == "__main__":
    main()

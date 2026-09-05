#!/usr/bin/env python3
"""Exact scale-block and affine-boundary controls for constant cut tails.

For an endpoint ``e`` the cut coordinate ``I(e)_t`` depends only on endpoint
coordinates ``floor(t/2)..t``.  Therefore, if a cut is constant ``c`` on a
tail and ``W=e[n:2n]``, the block ``e[2n:4n]`` is a deterministic function
``R_c(W)`` independent of ``e[:n]``.  A constant-tail hard-core endpoint
would give hard-core blocks ``W`` and ``R_c(W)`` at every sufficiently large
scale.

This script exhausts that finite-word obstruction through a requested scale.
It also checks that every newest-endpoint/newest-cut permutation is one of
the eight affine maps

    (h,l) -> (h + alpha, l + beta*h + gamma)

over F_2.  The affine coordinates turn a constant high cut bit into the
simple forced endpoint bit ``h=1+alpha``.

The bounded scale census is evidence, not an induction over the word length.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import product

from dyadic_periodicity_analyzer import (
    BOUNDARY,
    cone_local,
    inverse_cone_diagonal,
)
from rank_zero_separator import hard_core_prefixes


Vector = tuple[int, ...]
Permutation = tuple[int, int, int, int]


def newest_cut_permutation(endpoint_prefix: Vector) -> Permutation:
    """Map a newly appended endpoint state to the newly exposed cut state."""

    return tuple(
        inverse_cone_diagonal(endpoint_prefix + (value,))[-1]
        for value in range(4)
    )  # type: ignore[return-value]


@dataclass(frozen=True, slots=True)
class Affine:
    """The map ``(h,l)->(h+alpha,l+beta*h+gamma)`` over F_2."""

    alpha: int
    beta: int
    gamma: int

    def apply(self, state: int) -> int:
        high, low = state >> 1, state & 1
        return 2 * (high ^ self.alpha) + (
            low ^ (self.beta & high) ^ self.gamma
        )

    def permutation(self) -> Permutation:
        return tuple(self.apply(state) for state in range(4))  # type: ignore[return-value]

    def after(self, before: "Affine") -> "Affine":
        """Return ``self o before``."""

        return Affine(
            self.alpha ^ before.alpha,
            self.beta ^ before.beta,
            self.gamma ^ before.gamma ^ (self.beta & before.alpha),
        )


def affine_coordinates(permutation: Permutation) -> Affine:
    alpha = permutation[0] >> 1
    gamma = permutation[0] & 1
    beta = (permutation[2] & 1) ^ gamma
    answer = Affine(alpha, beta, gamma)
    if answer.permutation() != permutation:
        raise ValueError(f"permutation is not in the eight-map affine group: {permutation}")
    return answer


def local_affine_controls() -> None:
    affine_maps = {Affine(a, b, g) for a in range(2) for b in range(2) for g in range(2)}
    assert len({item.permutation() for item in affine_maps}) == 8

    local = []
    for left in range(4):
        permutation = tuple(cone_local(left, right) for right in range(4))
        affine = affine_coordinates(permutation)  # type: ignore[arg-type]
        activity = int(left != 0)
        assert affine == Affine(activity, 1 ^ (left & 1), activity)
        local.append(affine)

    # Check the explicit cocycle law against literal permutation composition.
    for after in affine_maps:
        for before in affine_maps:
            literal = tuple(
                after.apply(before.apply(state)) for state in range(4)
            )
            assert after.after(before).permutation() == literal


def affine_prefix_controls(max_length: int) -> int:
    """Check all eight boundary maps and constant-high endpoint forcing."""

    checked = 0
    found: set[Permutation] = set()
    for length in range(max_length + 1):
        frontier: list[Vector] = [()]
        for _ in range(length):
            frontier = [word + (value,) for word in frontier for value in range(4)]
        for prefix in frontier:
            permutation = newest_cut_permutation(prefix)
            found.add(permutation)
            affine = affine_coordinates(permutation)
            for low_output, output in ((0, 2), (1, 3)):
                forced = permutation.index(output)
                if forced in (1, 2):
                    # Endpoint state 1 has high bit 0; state 2 has high bit 1.
                    assert forced == 2 - affine.alpha
                    input_high = 1 ^ affine.alpha
                    input_low = affine.alpha
                    assert low_output == (
                        input_low
                        ^ (affine.beta & input_high)
                        ^ affine.gamma
                    )
                checked += 1
    assert len(found) == 8
    return checked


def scale_extension_with_padding(
    word: Vector, tail: int, padding: Vector
) -> Vector:
    """Compute ``R_tail(word)`` using an explicit inert left padding."""

    if tail not in (2, 3):
        raise ValueError("the first-infinite-tail modes are exactly 2 and 3")
    length = len(word)
    if len(padding) != length:
        raise ValueError("padding and word must have the same length")
    # Coordinates before ``length`` are outside every dependency window used
    # below.  Padding only makes the absolute indices agree with the
    # definition W=e[n:2n].
    endpoint = list(padding) + list(word)
    for _ in range(2 * length):
        candidates = tuple(
            value
            for value in range(4)
            if inverse_cone_diagonal(tuple(endpoint) + (value,))[-1] == tail
        )
        # Triangular bijectivity makes the newest endpoint/newest cut map a
        # permutation, hence the forced symbol is unique.
        assert len(candidates) == 1
        endpoint.append(candidates[0])
    return tuple(endpoint[2 * length :])


def scale_extension(word: Vector, tail: int) -> Vector:
    """Compute the exact block ``R_tail(word)`` of twice the input length."""

    if not word:
        return ()

    # Keep only the newest dependency diagonal.  If ``edge[t]`` is the
    # order-t cone state whose dependency interval ends at the current last
    # endpoint symbol, then appending q gives
    #
    #   next[0] = B(q),
    #   next[1] = phi(e_last, next[0]),
    #   next[t] = phi(edge[t-2], next[t-1]).
    #
    # The last entry is the newly exposed cut coordinate.  This is the same
    # triangular recurrence as ``inverse_cone_diagonal``, but it makes an
    # entire forced scale block quadratic rather than cubic in |word|.
    # The n inert symbols place W at absolute coordinates n,...,2n-1.
    # Their values are irrelevant to the forced block, but the absolute cone
    # orders are not; the zero padding is therefore retained in the edge.
    endpoint = []
    edge: Vector = ()
    for value in (0,) * len(word) + word:
        edge = append_dependency_edge(edge, endpoint[-1] if endpoint else None, value)
        endpoint.append(value)

    extension = []
    for _ in range(2 * len(word)):
        candidates = []
        for value in range(4):
            following = append_dependency_edge(edge, endpoint[-1], value)
            if following[-1] == tail:
                candidates.append((value, following))
        assert len(candidates) == 1
        value, edge = candidates[0]
        endpoint.append(value)
        extension.append(value)
    return tuple(extension)


def append_dependency_edge(
    edge: Vector, previous_endpoint: int | None, value: int
) -> Vector:
    """Append one endpoint symbol to the exact newest dependency diagonal."""

    following = [BOUNDARY[value]]
    if not edge:
        assert previous_endpoint is None
        return tuple(following)
    assert previous_endpoint is not None and len(edge) >= 1
    following.append(cone_local(previous_endpoint, following[0]))
    for order in range(2, len(edge) + 1):
        following.append(cone_local(edge[order - 2], following[-1]))
    return tuple(following)


def fast_scale_controls(max_length: int = 6) -> int:
    """Cross-check the diagonal constructor against the literal cone."""

    checked = 0
    for length in range(1, max_length + 1):
        for word in product(range(4), repeat=length):
            edge: Vector = ()
            endpoint: list[int] = []
            for value in word:
                edge = append_dependency_edge(
                    edge, endpoint[-1] if endpoint else None, value
                )
                endpoint.append(value)
                assert edge[-1] == inverse_cone_diagonal(tuple(endpoint))[-1]
                checked += 1
            for tail in (2, 3):
                assert scale_extension(word, tail) == scale_extension_with_padding(
                    word, tail, (0,) * length
                )
                checked += 1
    return checked


def padding_independence_controls(max_length: int = 3) -> int:
    """Exhaustively confirm that coordinates before ``n`` do not affect R."""

    checked = 0
    for length in range(1, max_length + 1):
        for word in product(range(4), repeat=length):
            for tail in (2, 3):
                expected = scale_extension(word, tail)
                for padding in product(range(4), repeat=length):
                    assert (
                        scale_extension_with_padding(word, tail, padding)
                        == expected
                    )
                    checked += 1
    return checked


def hard_core_extension_length(word: Vector, extension: Vector) -> int:
    previous = word[-1]
    for index, value in enumerate(extension):
        if value not in (1, 2) or previous == value == 1:
            return index
        previous = value
    return len(extension)


EXPECTED_MAXIMA = {
    2: (0, 1, 1, 2, 1, 2, 4, 3, 2, 4, 4, 5, 5, 7, 7, 10, 10, 9, 7, 10, 12, 10),
    3: (1, 1, 4, 2, 2, 2, 4, 3, 8, 6, 4, 5, 5, 5, 6, 6, 5, 9, 8, 8, 8, 9),
}

EXPECTED_CHARGE_EXCESSES = {
    2: (0, -1, -1, 0, -2, -2, 0, -2, -3, -2, -3, -2, -3, -2, -3, 0, 1, -1, -5, -5, -2, -5),
    3: (0, 0, 3, 0, -1, -2, 0, -2, 2, 0, -2, -2, -3, -4, -5, -3, -5, -3, -4, -4, -6, -6),
}


def scale_census(
    length: int, tail: int
) -> tuple[int, Vector, Vector, int, Vector, int, Vector]:
    maximum = -1
    witness: Vector = ()
    witness_extension: Vector = ()
    maximum_charge_excess = -10**9
    charge_witness: Vector = ()
    maximum_repaired_excess = -10**9
    repaired_witness: Vector = ()
    for word in hard_core_prefixes(length):
        extension = scale_extension(word, tail)
        survival = hard_core_extension_length(word, extension)
        if survival > maximum:
            maximum = survival
            witness = word
            witness_extension = extension
        charge_excess = survival - word.count(2)
        if charge_excess > maximum_charge_excess:
            maximum_charge_excess = charge_excess
            charge_witness = word
        repaired_budget = word.count(2) + (
            int(any(left == right == 2 for left, right in zip(word, word[1:])))
            if tail == 2
            else 3
        )
        repaired_excess = survival - repaired_budget
        if repaired_excess > maximum_repaired_excess:
            maximum_repaired_excess = repaired_excess
            repaired_witness = word
    assert maximum < 2 * length
    return (
        maximum,
        witness,
        witness_extension,
        maximum_charge_excess,
        charge_witness,
        maximum_repaired_excess,
        repaired_witness,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-scale", type=int, default=12)
    parser.add_argument("--affine-prefix", type=int, default=6)
    args = parser.parse_args()
    if args.max_scale < 1 or args.affine_prefix < 0:
        parser.error("bounds must be nonnegative and max scale must be positive")

    local_affine_controls()
    checked = affine_prefix_controls(args.affine_prefix)
    print(f"eight-map affine boundary group: {checked} prefix/output cases PASS")
    padding_checks = padding_independence_controls()
    print(f"scale-block padding independence: {padding_checks} cases PASS")
    fast_checks = fast_scale_controls()
    print(f"incremental dependency diagonal: {fast_checks} cases PASS")

    for length in range(1, args.max_scale + 1):
        fields = []
        for tail in (2, 3):
            (
                maximum,
                word,
                extension,
                charge_excess,
                charge_word,
                repaired_excess,
                repaired_word,
            ) = scale_census(length, tail)
            if length <= len(EXPECTED_MAXIMA[tail]):
                assert maximum == EXPECTED_MAXIMA[tail][length - 1]
                assert (
                    charge_excess
                    == EXPECTED_CHARGE_EXCESSES[tail][length - 1]
                )
            # The original tail-2 #2 budget is deliberately *not* asserted:
            # its first counterexample is the registered length-17 word
            # 12212121212121212.  The one-contact repair and the tail-3
            # three-credit budget remain finite-census conjectures.
            assert repaired_excess <= 0
            failure = extension[maximum : maximum + 2]
            fields.append(
                f"tail={tail} max-extension={maximum:2d}/{2*length:2d} "
                f"max(extension-#2)={charge_excess:2d} "
                f"max(repaired-excess)={repaired_excess:2d} "
                f"W={''.join(map(str, word))} "
                f"fail={''.join(map(str, failure))} "
                f"charge-W={''.join(map(str, charge_word))} "
                f"repaired-W={''.join(map(str, repaired_word))}"
            )
        print(f"scale={length:2d} " + " | ".join(fields))


if __name__ == "__main__":
    main()

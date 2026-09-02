#!/usr/bin/env python3
"""Exact reflected-half overlay and carry-quotient audit."""

from __future__ import annotations

from itertools import combinations, product

from carry_transducer import input_transform


FEATURES = ("L", "R", "X", "A", "O")
SYMMETRIC = ("X", "A", "O")


def bits(state: int) -> tuple[int, int]:
    """Decode the folded state ``2*L+R``."""

    return state >> 1, state & 1


def rule30(left: int, center: int, right: int) -> int:
    return left ^ (center | right)


def folded_step(inward: int, center: int, outward: int) -> int:
    """Update one reflected pair at positive distance from the center."""

    li, ri = bits(inward)
    lc, rc = bits(center)
    lo, ro = bits(outward)
    left_next = rule30(lo, lc, li)
    right_next = rule30(ri, rc, ro)
    return 2 * left_next + right_next


def feature(state: int, name: str) -> int:
    left, right = bits(state)
    return {
        "L": left,
        "R": right,
        "X": left ^ right,
        "A": left & right,
        "O": left | right,
    }[name]


def projection(state: int, names: tuple[str, ...]) -> tuple[int, ...]:
    return tuple(feature(state, name) for name in names)


def closure_collision(
    names: tuple[str, ...],
) -> tuple[tuple[int, int, int], tuple[int, int, int]] | None:
    """Return two projected-equal neighborhoods with different outputs."""

    seen: dict[
        tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]],
        tuple[tuple[int, ...], tuple[int, int, int]],
    ] = {}
    for neighborhood in product(range(4), repeat=3):
        key = tuple(projection(state, names) for state in neighborhood)
        output = projection(folded_step(*neighborhood), names)
        previous = seen.get(key)
        if previous is not None and previous[0] != output:
            return previous[1], neighborhood
        seen.setdefault(key, (output, neighborhood))
    return None


def literal_fold_control() -> int:
    """Cross-check the folded formula by updating the two literal sides."""

    checked = 0
    for inward, center, outward in product(range(4), repeat=3):
        li, ri = bits(inward)
        lc, rc = bits(center)
        lo, ro = bits(outward)
        expected = 2 * rule30(lo, lc, li) + rule30(ri, rc, ro)
        assert folded_step(inward, center, outward) == expected
        checked += 1
    return checked


def alternating_boundary_control() -> tuple[int, int]:
    """Check the exact `0->1` XOR pin and `1->0` OR pin."""

    zero_to_one = 0
    one_to_zero = 0
    for state in range(4):
        left, right = bits(state)
        if rule30(left, 0, right) == 1:
            assert feature(state, "X") == 1
            zero_to_one += 1
        if rule30(left, 1, right) == 0:
            assert left == 1
            assert feature(state, "O") == 1
            one_to_zero += 1
    assert zero_to_one == 2 and one_to_zero == 2
    return zero_to_one, one_to_zero


def all_feature_subsets(names: tuple[str, ...]):
    for size in range(1, len(names) + 1):
        yield from combinations(names, size)


def carry_quotient_control() -> tuple[int, int]:
    """Verify that carry inputs use `(L,L OR R)` and need orientation."""

    by_ordered_or: dict[tuple[int, int], tuple[int, int, int, int]] = {}
    for state in range(4):
        key = projection(state, ("L", "O"))
        action = input_transform(state)
        previous = by_ordered_or.setdefault(key, action)
        assert previous == action
    assert len(by_ordered_or) == 3
    assert input_transform(2) == input_transform(3)

    # The two mismatch orientations have identical reflection-symmetric
    # overlays, but they induce different carry actions.
    assert projection(1, SYMMETRIC) == projection(2, SYMMETRIC)
    assert input_transform(1) != input_transform(2)
    return len(by_ordered_or), len(set(map(input_transform, range(4))))


def main() -> None:
    checked = literal_fold_control()
    print(f"literal four-state fold: {checked}/64 neighborhoods PASS")

    zero_to_one, one_to_zero = alternating_boundary_control()
    print(
        "alternating boundary pins: "
        f"0->1 XOR cases={zero_to_one}, 1->0 OR cases={one_to_zero} PASS"
    )

    for names in all_feature_subsets(SYMMETRIC):
        collision = closure_collision(names)
        assert collision is not None
        left, right = collision
        print(
            f"symmetric projection={''.join(names)} NOT-CLOSED "
            f"collision={left}/{right}"
        )

    closed = []
    for names in all_feature_subsets(FEATURES):
        if closure_collision(names) is None:
            closed.append(names)
    minimal = [
        names
        for names in closed
        if not any(set(other) < set(names) for other in closed)
    ]
    assert set(minimal) == {("L",), ("R",)}
    print(
        "bulk folded-factor minimal closed projections: "
        + ", ".join("".join(names) for names in minimal)
        + " PASS"
    )

    quotient, actions = carry_quotient_control()
    print(
        "ordered OR-latch carry quotient: "
        f"classes={quotient}, distinct-actions={actions}, 2~3 PASS"
    )
    print(
        "symmetric mismatch orientations 01/10: same XAO, "
        "different carry action PASS"
    )


if __name__ == "__main__":
    main()


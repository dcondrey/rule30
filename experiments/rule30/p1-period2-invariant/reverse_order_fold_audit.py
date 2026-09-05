#!/usr/bin/env python3
"""Exact audit of the reverse-order (antidiagonal) Rule 30 fold."""

from __future__ import annotations

from itertools import combinations, product


FEATURES = ("A", "B", "X", "N", "O")
SYMMETRIC = ("X", "N", "O")


def rule30(left: int, center: int, right: int) -> int:
    return left ^ (center | right)


def bits(state: int) -> tuple[int, int]:
    """Decode `state=2*A+B`."""

    return state >> 1, state & 1


def reverse_fold_step(
    minus_two: int, minus_one: int, center: int, plus_one: int
) -> int:
    """Update the reverse fold at an interior index `i`.

    The arguments are `Q_t(i-2),...,Q_t(i+1)`.  The `A` coordinate is the
    ordinary left half read center-to-edge.  The `B` coordinate is the right
    half read edge-to-center and therefore follows the right characteristic.
    """

    a_minus_one, _ = bits(minus_one)
    a_center, b_center = bits(center)
    a_plus_one, _ = bits(plus_one)
    _, b_minus_two = bits(minus_two)
    _, b_minus_one = bits(minus_one)
    a_next = rule30(a_plus_one, a_center, a_minus_one)
    b_next = rule30(b_center, b_minus_one, b_minus_two)
    return 2 * a_next + b_next


def feature(state: int, name: str) -> int:
    a, b = bits(state)
    return {
        "A": a,
        "B": b,
        "X": a ^ b,
        "N": a & b,
        "O": a | b,
    }[name]


def projection(state: int, names: tuple[str, ...]) -> tuple[int, ...]:
    return tuple(feature(state, name) for name in names)


def feature_subsets(names: tuple[str, ...]):
    for size in range(1, len(names) + 1):
        yield from combinations(names, size)


def closure_collision(
    names: tuple[str, ...],
) -> tuple[tuple[int, int, int, int], tuple[int, int, int, int]] | None:
    seen: dict[
        tuple[tuple[int, ...], ...],
        tuple[tuple[int, ...], tuple[int, int, int, int]],
    ] = {}
    for neighborhood in product(range(4), repeat=4):
        key = tuple(projection(state, names) for state in neighborhood)
        output = projection(reverse_fold_step(*neighborhood), names)
        previous = seen.get(key)
        if previous is not None and previous[0] != output:
            return previous[1], neighborhood
        seen.setdefault(key, (output, neighborhood))
    return None


def literal_interior_control() -> int:
    checked = 0
    for neighborhood in product(range(4), repeat=4):
        minus_two, minus_one, center, plus_one = neighborhood
        a_minus_one, _ = bits(minus_one)
        a_center, b_center = bits(center)
        a_plus_one, _ = bits(plus_one)
        _, b_minus_two = bits(minus_two)
        _, b_minus_one = bits(minus_one)
        expected = 2 * rule30(
            a_plus_one, a_center, a_minus_one
        ) + rule30(b_center, b_minus_one, b_minus_two)
        assert reverse_fold_step(*neighborhood) == expected
        checked += 1
    return checked


def evolve_single_seed(steps: int) -> list[dict[int, int]]:
    rows = [{0: 1}]
    for _ in range(steps):
        old = rows[-1]
        left = min(old) - 1
        right = max(old) + 1
        following = {
            position: rule30(
                old.get(position - 1, 0),
                old.get(position, 0),
                old.get(position + 1, 0),
            )
            for position in range(left, right + 1)
        }
        rows.append(following)
    return rows


def endpoint_and_formula_controls(max_time: int = 16) -> tuple[int, str]:
    rows = evolve_single_seed(max_time)
    checked = 0
    centers = []
    for time, row in enumerate(rows):
        center = row[0]
        centers.append(str(center))
        states = tuple(
            2 * row[-index] + row[time - index]
            for index in range(time + 1)
        )
        assert bits(states[0]) == (center, 1)
        assert bits(states[-1]) == (1, center)
        checked += 2

        following = rows[time + 1] if time < max_time else None
        if following is None:
            continue
        for index in range(2, time):
            old_stencil = (
                states[index - 2],
                states[index - 1],
                states[index],
                states[index + 1],
            )
            expected = 2 * following[-index] + following[time + 1 - index]
            assert reverse_fold_step(*old_stencil) == expected
            checked += 1
    return checked, "".join(centers)


def main() -> None:
    checked = literal_interior_control()
    print(f"reverse-fold interior table: {checked}/256 neighborhoods PASS")

    spacetime_checked, centers = endpoint_and_formula_controls()
    print(
        "single-seed reverse-fold endpoints and spacetime formula: "
        f"{spacetime_checked} checks PASS"
    )
    print(f"single-seed center prefix through t=16: {centers}")
    print("endpoint law: Q_t(0)=(c_t,1), Q_t(t)=(1,c_t) PASS")

    for names in feature_subsets(SYMMETRIC):
        collision = closure_collision(names)
        assert collision is not None
        print(
            f"symmetric projection={''.join(names)} NOT-CLOSED "
            f"collision={collision[0]}/{collision[1]}"
        )

    closed = [
        names
        for names in feature_subsets(FEATURES)
        if closure_collision(names) is None
    ]
    minimal = [
        names
        for names in closed
        if not any(set(other) < set(names) for other in closed)
    ]
    assert set(minimal) == {("A",), ("B",)}
    print(
        "reverse-fold minimal closed bulk projections: "
        + ", ".join("".join(names) for names in minimal)
        + " PASS"
    )
    print(
        "interpretation: B is the binary one-sided right-characteristic "
        "shear; it is not the four-state inverse-terminal queue"
    )


if __name__ == "__main__":
    main()

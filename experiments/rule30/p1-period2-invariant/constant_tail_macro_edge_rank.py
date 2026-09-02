#!/usr/bin/env python3
"""Solver-free falsifiers for the frozen retreat--pull macro edge rank."""

from __future__ import annotations

from constant_tail_queue import (
    NORMALIZED_FORBIDDEN,
    Vector,
    normalize_queue,
    queue_step,
)


LEFT = 8
RIGHT = 9

# Integer normalization of the exact rational discovery model.  Every
# unlisted edge has weight zero.
REGISTERED_WEIGHTS = {
    (LEFT, 2): 54,
    (3, 0): 59,
    (3, 1): 55,
    (3, 2): 50,
    (1, 1): -5,
    (1, 2): -9,
    (0, 0): -3,
    (0, 1): -10,
    (0, 2): -14,
}


def weight(left: int, right: int) -> int:
    return REGISTERED_WEIGHTS.get((left, right), 0)


def edge_rank(queue: Vector) -> int:
    padded = (LEFT,) + queue + (RIGHT,)
    return sum(weight(left, right) for left, right in zip(padded, padded[1:]))


def invariant_queue(queue: Vector, tail: int) -> bool:
    if not queue or queue[0] != tail or queue[-1] not in (1, 2):
        return False
    return all(
        queue[index : index + len(forbidden)] != forbidden
        for forbidden in NORMALIZED_FORBIDDEN
        for index in range(len(queue) - len(forbidden) + 1)
    )


def successor(queue: Vector, tail: int) -> Vector:
    following = queue_step(queue, tail)
    assert following is not None
    return normalize_queue(following.queue, tail)


def update_type(source: Vector, target: Vector) -> str:
    if target[-1] == 2:
        return "A"
    if source[-1] == 2 and source != (2,):
        return "C"
    return "B"


def nonnegative_family_control() -> int:
    """Prove a uniform negative family, not merely one bounded witness."""

    checked = 0
    for repetitions in range(5, 65):
        tail2 = tuple(map(int, "211" + "01" * repetitions))
        tail3 = tuple(map(int, "30" + "10" * repetitions + "1"))
        assert invariant_queue(tail2, 2)
        assert invariant_queue(tail3, 3)
        assert edge_rank(tail2) == 49 - 10 * repetitions
        assert edge_rank(tail3) == 59 - 10 * (repetitions + 1)
        assert edge_rank(tail2) < 0 and edge_rank(tail3) < 0
        checked += 2
    return checked


def literal_falsifiers() -> tuple[tuple[str, int, int, int], ...]:
    """Verify the first stored counterexample to each frozen inequality."""

    answers = []
    nonnegative = {
        2: "2110101010101",
        3: "3010101010101",
    }
    for tail, text in nonnegative.items():
        queue = tuple(map(int, text))
        assert invariant_queue(queue, tail)
        value = edge_rank(queue)
        assert value == -1
        answers.append(("MR1", tail, value, 0))

    monotonicity = {
        2: "2111101010101",
        3: "3010101010101",
    }
    expected_targets = {
        2: "21212100121121",
        3: "32112100121121",
    }
    for tail, text in monotonicity.items():
        queue = tuple(map(int, text))
        target = successor(queue, tail)
        assert update_type(queue, target) == "B"
        assert "".join(map(str, target)) == expected_targets[tail]
        before, after = edge_rank(queue), edge_rank(target)
        assert (before, after) == (-1, 0)
        answers.append(("MR2", tail, before - after, 0))

    contraction = {
        2: "21101012111111",
        3: "31111111021101",
    }
    expected_middle = {
        2: "212100101010102",
        3: "301010100212102",
    }
    expected_targets = {
        2: "2110001211210021",
        3: "3211210002110021",
    }
    expected_ranks = {2: (-5, -7), 3: (-4, -6)}
    for tail, text in contraction.items():
        queue = tuple(map(int, text))
        middle = successor(queue, tail)
        target = successor(middle, tail)
        assert update_type(queue, middle) == "A"
        assert update_type(middle, target) == "C"
        assert "".join(map(str, middle)) == expected_middle[tail]
        assert "".join(map(str, target)) == expected_targets[tail]
        before, after = edge_rank(queue), edge_rank(target)
        assert (before, after) == expected_ranks[tail]
        assert before - after == 2 < 3
        answers.append(("MR3", tail, before - after, 3))
    return tuple(answers)


def main() -> None:
    family = nonnegative_family_control()
    print(
        "registered MR1 negative families: "
        f"{family} literal instances, repetitions 5..64 PASS"
    )
    for claim, tail, actual, required in literal_falsifiers():
        print(
            f"{claim} tail={tail}: actual margin={actual}, "
            f"required margin={required} -- FALSIFIED"
        )
    print(
        "CONCLUSION: all three frozen macro-edge-rank claims are false; "
        "period two remains open"
    )


if __name__ == "__main__":
    main()

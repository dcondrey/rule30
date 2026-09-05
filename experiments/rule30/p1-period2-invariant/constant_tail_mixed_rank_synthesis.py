#!/usr/bin/env python3
"""Synthesize bounded-factor ranks for the mixed retreat conjecture.

This is an exploratory falsifier for a particularly economical proof form.
For a padded normalized queue, assign one rational weight to every factor of
fixed width.  The induced additive rank must be nonnegative, bounded above by
``#1 + #zero-runs``, and satisfy

    rank(source) >= rank(successor) + [successor appends 2].

Satisfiability on a bounded corpus is not a proof.  Unsatisfiability is an
exact obstruction to that factor width on the stated corpus.
"""

from __future__ import annotations

import argparse
import z3

from constant_tail_mixed_run_budget import mixed_budget
from constant_tail_origin_prefix_hall import feature_starts
from constant_tail_queue import Vector, normalize_queue, queue_step
from constant_tail_retreat_budget import invariant_queues


LEFT = 8
RIGHT = 9


def factors(queue: Vector, width: int) -> tuple[tuple[int, ...], ...]:
    padded = (LEFT,) * (width - 1) + queue + (RIGHT,) * (width - 1)
    return tuple(
        padded[index : index + width]
        for index in range(len(padded) - width + 1)
    )


def expression(
    queue: Vector,
    width: int,
    weights: dict[tuple[int, ...], z3.ArithRef],
) -> z3.ArithRef:
    terms = []
    for factor in factors(queue, width):
        if factor not in weights:
            weights[factor] = z3.Real("w_" + "_".join(map(str, factor)))
        terms.append(weights[factor])
    return z3.Sum(*terms)


def solve(width: int, max_length: int) -> tuple[str, int, int]:
    weights: dict[tuple[int, ...], z3.ArithRef] = {}

    solver = z3.Solver()
    queues = 0
    transitions = 0
    seen: set[Vector] = set()
    for length in range(1, max_length + 1):
        for tail in (2, 3):
            for queue in invariant_queues(length, tail):
                if queue in seen:
                    continue
                seen.add(queue)
                queues += 1
                rank = expression(queue, width, weights)
                solver.add(rank >= 0, rank <= mixed_budget(queue))
                following = queue_step(queue, tail)
                if following is None:
                    continue
                successor = normalize_queue(following.queue, tail)
                successor_rank = expression(successor, width, weights)
                solver.add(
                    successor_rank >= 0,
                    successor_rank <= mixed_budget(successor),
                    rank >= successor_rank + int(successor[-1] == 2),
                )
                transitions += 1

    status = solver.check()
    if status == z3.sat:
        model = solver.model()
        nonzero = sorted(
            (
                factor,
                model.eval(weight, model_completion=True),
            )
            for factor, weight in weights.items()
            if model.eval(weight, model_completion=True).numerator_as_long()
            != 0
        )
        print(f"width={width} SAT nonzero-weights={len(nonzero)}")
        for factor, value in nonzero:
            print("  " + "".join(map(str, factor)) + f": {value}")
    else:
        print(f"width={width} {status}")
    return str(status), queues, transitions


def marked_word(queue: Vector, marks: list[bool]) -> Vector:
    """Combine a normalized queue symbol and one ancestry bit."""

    assert len(queue) == len(marks)
    return tuple(symbol + 4 * int(mark) for symbol, mark in zip(queue, marks))


def solve_marked(width: int, max_length: int) -> tuple[str, int, int]:
    """Search for a rank proving every origin-cutoff Hall inequality."""

    weights: dict[tuple[int, ...], z3.ArithRef] = {}
    solver = z3.Solver()
    cases = 0
    transitions = 0
    for length in range(1, max_length + 1):
        for tail in (2, 3):
            for initial in invariant_queues(length, tail):
                starts = feature_starts(initial)
                for cutoff in range(length):
                    queue = initial
                    marks = [index <= cutoff for index in range(length)]
                    rank = expression(marked_word(queue, marks), width, weights)
                    solver.add(
                        rank >= 0,
                        rank <= sum(start <= cutoff for start in starts),
                    )
                    cases += 1
                    for _step in range(4 * max_length + 8):
                        following = queue_step(queue, tail)
                        if following is None:
                            break
                        inherited = normalize_queue(following.queue[:-1], tail)
                        differences = tuple(
                            index
                            for index in range(1, len(queue))
                            if inherited[index] != queue[index]
                        )
                        if differences:
                            pivot = differences[-1]
                        else:
                            assert queue == (2,)
                            pivot = 0
                        successor = normalize_queue(following.queue, tail)
                        successor_marks = marks + [marks[pivot]]
                        successor_rank = expression(
                            marked_word(successor, successor_marks),
                            width,
                            weights,
                        )
                        marked_retreat = successor[-1] == 2 and marks[pivot]
                        solver.add(
                            successor_rank >= 0,
                            rank >= successor_rank + int(marked_retreat),
                        )
                        transitions += 1
                        queue = successor
                        marks = successor_marks
                        rank = successor_rank
                    else:
                        raise AssertionError("marked synthesis orbit cap reached")

    status = solver.check()
    if status == z3.sat:
        model = solver.model()
        nonzero = sorted(
            (
                factor,
                model.eval(weight, model_completion=True),
            )
            for factor, weight in weights.items()
            if model.eval(weight, model_completion=True).numerator_as_long()
            != 0
        )
        print(f"marked width={width} SAT nonzero-weights={len(nonzero)}")
        for factor, value in nonzero:
            print("  " + ",".join(map(str, factor)) + f": {value}")
    else:
        print(f"marked width={width} {status}")
    return str(status), cases, transitions


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first-width", type=int, default=1)
    parser.add_argument("--last-width", type=int, default=4)
    parser.add_argument("--max-length", type=int, default=10)
    parser.add_argument("--marked", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.first_width <= args.last_width or args.max_length < 1:
        parser.error("invalid width interval or maximum length")

    for width in range(args.first_width, args.last_width + 1):
        if args.marked:
            status, queues, transitions = solve_marked(
                width, args.max_length
            )
        else:
            status, queues, transitions = solve(width, args.max_length)
        print(
            f"width={width} corpus queues={queues} transitions={transitions} "
            f"status={status}",
            flush=True,
        )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Audit transition closure of ordered zero-prefix D8 defect words.

This is the solver-free experiment frozen in
``PREREGISTRATION-HOLONOMY-DEFECT-CLOSURE.md``.  It distinguishes a useful
ordered observable from a genuine dynamical state: an ordinal rank can be
placed on the former only after enough hidden queue data has been retained
to make its legal update well defined.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from constant_tail_scale import (
    Affine,
    Vector,
    affine_coordinates,
    append_dependency_edge,
    hard_core_extension_length,
)
from dyadic_periodicity_analyzer import BOUNDARY
from rank_zero_separator import hard_core_prefixes


AffineCode = tuple[int, int, int]
Queue = tuple[int, ...]


def code(affine: Affine) -> AffineCode:
    return affine.alpha, affine.beta, affine.gamma


def inverse(affine: Affine) -> Affine:
    """Return the inverse in the eight-map affine realization of D8."""

    answer = Affine(
        affine.alpha,
        affine.beta,
        affine.gamma ^ (affine.alpha & affine.beta),
    )
    assert answer.after(affine) == Affine(0, 0, 0)
    assert affine.after(answer) == Affine(0, 0, 0)
    return answer


def defect(left: Affine, right: Affine) -> Affine:
    """Return ``left^(-1) o right``."""

    return inverse(left).after(right)


def newest_affine(edge: Vector, previous: int) -> Affine:
    permutation = tuple(
        append_dependency_edge(edge, previous, value)[-1]
        for value in range(4)
    )
    return affine_coordinates(permutation)  # type: ignore[arg-type]


@dataclass(frozen=True, slots=True)
class RowState:
    affine: Affine
    previous: int
    forced: int
    queue: Queue


def scenario_rows(
    word: Vector, zero_prefix: int, tail: int
) -> tuple[RowState, ...]:
    """Return exact row states for one member of the zero-prefix chain."""

    length = len(word)
    source = (0,) * zero_prefix + word[zero_prefix:]
    endpoint: list[int] = []
    edge: Vector = ()
    for value in (0,) * length + source:
        edge = append_dependency_edge(
            edge, endpoint[-1] if endpoint else None, value
        )
        endpoint.append(value)

    rows = []
    # One extra row is retained so every audited transition has a successor.
    for _ in range(2 * length + 1):
        affine = newest_affine(edge, endpoint[-1])
        forced = affine.permutation().index(tail)
        rows.append(
            RowState(
                affine=affine,
                previous=endpoint[-1],
                forced=forced,
                queue=tuple(reversed(edge)),
            )
        )
        edge = append_dependency_edge(edge, endpoint[-1], forced)
        endpoint.append(forced)
    return tuple(rows)


def reconstruct_from_defects(
    defects: tuple[Affine, ...], rightmost: Affine
) -> tuple[Affine, ...]:
    """Reconstruct phases leftward from their ordered defects and anchor."""

    phases = [rightmost]
    for item in reversed(defects):
        # delta=A_k^-1 o A_(k+1), hence A_k=A_(k+1) o delta^-1.
        phases.append(phases[-1].after(inverse(item)))
    phases.reverse()
    return tuple(phases)


@dataclass(frozen=True, slots=True)
class Witness:
    word: Vector
    tail: int
    row: int
    successor: tuple[AffineCode, ...]

    def render(self) -> str:
        return (
            f"tail={self.tail} W={''.join(map(str, self.word))} "
            f"row={self.row} successor={self.successor}"
        )


@dataclass(slots=True)
class LayerAudit:
    name: str
    seen: dict[object, Witness]
    collisions: int = 0
    first_collision: tuple[object, Witness, Witness] | None = None

    def observe(self, key: object, witness: Witness) -> None:
        previous = self.seen.get(key)
        if previous is None:
            self.seen[key] = witness
        elif previous.successor != witness.successor:
            self.collisions += 1
            if self.first_collision is None:
                self.first_collision = key, previous, witness


@dataclass(slots=True)
class Census:
    words: int = 0
    transitions: int = 0
    diagonal_support_failures: int = 0
    first_support_failure: str | None = None


def audit_word(
    word: Vector,
    tail: int,
    layers: tuple[LayerAudit, ...],
    census: Census,
) -> None:
    scenarios = tuple(
        scenario_rows(word, zero_prefix, tail)
        for zero_prefix in range(len(word) + 1)
    )
    original_extension = tuple(row.forced for row in scenarios[0])
    survival = hard_core_extension_length(word, original_extension)
    required = survival if tail == 2 else max(0, survival - 1)
    census.words += 1

    for row in range(min(required, len(word))):
        current = tuple(scenarios[k][row] for k in range(row, len(word) + 1))
        following = tuple(
            scenarios[k][row + 1] for k in range(row + 1, len(word) + 1)
        )
        phases = tuple(item.affine for item in current)
        defects = tuple(
            defect(left, right) for left, right in zip(phases, phases[1:])
        )
        assert reconstruct_from_defects(defects, phases[-1]) == phases
        successor = tuple(
            code(defect(left.affine, right.affine))
            for left, right in zip(following, following[1:])
        )
        witness = Witness(word, tail, row, successor)

        # Tail 2 is an additive quotient and could equivalently be read from
        # the group defects.  Tail 3 is the nonhomomorphic evaluation A(0),
        # so compare adjacent phase coordinates literally rather than
        # projecting ``A_k^-1 o A_(k+1)``.
        projected_support = any(
            (left.alpha, left.beta) != (right.alpha, right.beta)
            if tail == 2
            else (left.alpha, left.gamma) != (right.alpha, right.gamma)
            for left, right in zip(phases, phases[1:])
        )
        if not projected_support:
            census.diagonal_support_failures += 1
            if census.first_support_failure is None:
                census.first_support_failure = witness.render()

        defect_codes = tuple(map(code, defects))
        anchored = (code(phases[-1]), defect_codes)
        boundary = anchored + (tuple(item.previous for item in current),)
        two_ended = anchored + (
            tuple((item.queue[0], item.queue[-1]) for item in current),
        )
        queues = tuple(item.queue for item in current)
        keys = (
            (tail, defect_codes),
            (tail, anchored),
            (tail, boundary),
            (tail, two_ended),
            (tail, queues),
        )
        for layer, key in zip(layers, keys):
            layer.observe(key, witness)
        census.transitions += 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first-length", type=int, default=1)
    parser.add_argument("--max-length", type=int, default=12)
    args = parser.parse_args()
    if not 1 <= args.first_length <= args.max_length:
        parser.error("length bounds must satisfy 1 <= first <= max")

    layers = tuple(
        LayerAudit(name, {})
        for name in (
            "defects",
            "anchored",
            "boundary",
            "two-ended-1",
            "queues",
        )
    )
    census = Census()
    for length in range(args.first_length, args.max_length + 1):
        before = census.transitions
        for word in hard_core_prefixes(length):
            for tail in (2, 3):
                audit_word(word, tail, layers, census)
        print(
            f"length={length:2d} transitions={census.transitions-before:6d} "
            f"support-failures={census.diagonal_support_failures}"
        )

    print(
        f"TOTAL words={census.words} transitions={census.transitions} "
        f"diagonal-support-failures={census.diagonal_support_failures}"
    )
    print(
        "first support failure: "
        f"{census.first_support_failure or 'none'}"
    )
    for layer in layers:
        print(
            f"layer={layer.name} keys={len(layer.seen)} "
            f"transition-collisions={layer.collisions}"
        )
        if layer.first_collision is None:
            print("  first collision: none")
        else:
            key, left, right = layer.first_collision
            print(f"  shared key: {key}")
            print(f"  first collision A: {left.render()}")
            print(f"  first collision B: {right.render()}")

    # Full queues are literal complete states; their update must be closed.
    assert layers[-1].collisions == 0


if __name__ == "__main__":
    main()

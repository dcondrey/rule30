#!/usr/bin/env python3
"""Search the preregistered local selectors for scale-derivative pivots."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import product

from constant_tail_derivative_rank import binary_rank, derivative_coordinate_rows
from constant_tail_ordered_matching import correction_count, forced_trace
from constant_tail_scale import Vector, hard_core_extension_length
from rank_zero_separator import hard_core_prefixes


LABELS = ("a", "b", "a^b")


@dataclass(frozen=True, slots=True)
class Case:
    word: Vector
    tail: int
    correction: int
    forced: Vector
    alpha_rows: tuple[int, ...]
    beta_rows: tuple[int, ...]

    @property
    def survival(self) -> int:
        return len(self.forced)


def make_case(word: Vector, tail: int) -> Case:
    extension, trace = forced_trace(word, tail)
    survival = hard_core_extension_length(word, extension)
    rows, _ = derivative_coordinate_rows(word, tail, survival)
    alpha = tuple(rows["alpha"])
    beta = tuple(rows["beta"])

    # Recheck the unrestricted two-row prefix invariant on every dataset case.
    for prefix in range(survival + 1):
        stacked = [
            row
            for step in range(prefix)
            for row in (alpha[step], beta[step])
        ]
        assert binary_rank(stacked) >= max(
            0, prefix - correction_count(word, tail)
        )
    return Case(
        word=word,
        tail=tail,
        correction=correction_count(word, tail),
        forced=tuple(step.forced for step in trace[:survival]),
        alpha_rows=alpha,
        beta_rows=beta,
    )


def dataset(first_length: int, last_length: int) -> list[Case]:
    answer = []
    for length in range(first_length, last_length + 1):
        for word in hard_core_prefixes(length):
            for tail in (2, 3):
                answer.append(make_case(word, tail))
        print(f"built cases through length={length}")
    return answer


def context_index(case: Case, step: int, family: str) -> int:
    tail_index = case.tail - 2
    forced_index = case.forced[step] - 1
    assert tail_index in (0, 1) and forced_index in (0, 1)
    if family == "symbol":
        return tail_index * 2 + forced_index
    if family == "symbol-parity":
        return tail_index * 4 + forced_index * 2 + (step & 1)
    raise ValueError(family)


def selected_row(case: Case, step: int, choice: int) -> int:
    alpha = case.alpha_rows[step]
    beta = case.beta_rows[step]
    if choice == 0:
        return alpha
    if choice == 1:
        return beta
    if choice == 2:
        return alpha ^ beta
    raise ValueError(choice)


def case_survives(case: Case, selector: tuple[int, ...], family: str) -> bool:
    basis: dict[int, int] = {}
    selected: list[int] = []
    for step in range(case.survival):
        choice = selector[context_index(case, step, family)]
        row = selected_row(case, step, choice)
        selected.append(row)
        vector = row
        while vector:
            pivot = vector.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = vector
                break
            vector ^= basis[pivot]
        rank = len(basis)
        assert rank == binary_rank(selected)
        if rank < max(0, step + 1 - case.correction):
            return False
    return True


def selector_text(selector: tuple[int, ...], family: str) -> str:
    fields = []
    for tail in (2, 3):
        for forced in (1, 2):
            parities = (0,) if family == "symbol" else (0, 1)
            for parity in parities:
                if family == "symbol":
                    index = (tail - 2) * 2 + forced - 1
                    key = f"c{tail}q{forced}"
                else:
                    index = (tail - 2) * 4 + (forced - 1) * 2 + parity
                    key = f"c{tail}q{forced}p{parity}"
                fields.append(f"{key}:{LABELS[selector[index]]}")
    return " ".join(fields)


def search_family(
    family: str, training: list[Case], validation: list[Case]
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    keys = 4 if family == "symbol" else 8
    training_survivors = []
    for selector in product(range(3), repeat=keys):
        if all(case_survives(case, selector, family) for case in training):
            training_survivors.append(selector)
    validation_survivors = [
        selector
        for selector in training_survivors
        if all(case_survives(case, selector, family) for case in validation)
    ]
    return training_survivors, validation_survivors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--training-max", type=int, default=12)
    parser.add_argument("--validation-max", type=int, default=16)
    args = parser.parse_args()
    if not (1 <= args.training_max < args.validation_max):
        parser.error("require 1 <= training-max < validation-max")

    training = dataset(1, args.training_max)
    validation = dataset(args.training_max + 1, args.validation_max)
    validation.extend(
        (
            make_case(tuple(map(int, "12212121212121212")), 2),
            make_case((1, 2, 1), 3),
        )
    )
    print(
        f"training-cases={len(training)} validation-cases={len(validation)}"
    )

    for family in ("symbol", "symbol-parity"):
        training_survivors, validation_survivors = search_family(
            family, training, validation
        )
        print(
            f"family={family} candidates={3 ** (4 if family == 'symbol' else 8)} "
            f"training-survivors={len(training_survivors)} "
            f"validation-survivors={len(validation_survivors)}"
        )
        display = validation_survivors[:20]
        for selector in display:
            print(f"  survivor {selector_text(selector, family)}")
        if len(validation_survivors) > len(display):
            print(
                f"  ... {len(validation_survivors)-len(display)} additional "
                "validation survivors omitted"
            )
        if training_survivors and not validation_survivors:
            print(
                "  first training-only "
                + selector_text(training_survivors[0], family)
            )


if __name__ == "__main__":
    main()

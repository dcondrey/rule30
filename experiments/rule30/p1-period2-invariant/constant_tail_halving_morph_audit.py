#!/usr/bin/env python3
"""Exact counterexample to a parent-only deterministic-halving morph.

The displayed finite family kills a universal factorization claim.  It is not
evidence for the all-length halving recurrence, which remains open.
"""

from __future__ import annotations

from constant_tail_scale import (
    Vector,
    hard_core_extension_length,
    scale_extension,
)


def render(word: Vector) -> str:
    return "".join(map(str, word))


def main() -> None:
    parents = tuple(
        tuple(map(int, word))
        for word in (
            "121222122",
            "122222122",
            "212222122",
            "221222122",
            "222222122",
        )
    )
    tail = 3
    length = 9
    cut = length // 2
    charge = (length + 1) // 2 + 1

    right_halves = {word[cut:] for word in parents}
    parent_extensions = {scale_extension(word, tail) for word in parents}
    parent_survivals = {
        hard_core_extension_length(word, scale_extension(word, tail))
        for word in parents
    }
    assert right_halves == {tuple(map(int, "22122"))}
    assert len(parent_extensions) == 1
    assert parent_survivals == {8}

    child_records = []
    for word in parents:
        child = word[:cut]
        extension = scale_extension(child, 2)
        survival = hard_core_extension_length(child, extension)
        assert survival == 2
        assert 8 == charge + survival
        child_records.append(
            (
                render(child),
                render(extension),
                extension[survival],
            )
        )

    child_extensions = {record[1] for record in child_records}
    child_defects = {record[2] for record in child_records}
    assert len(child_extensions) == 2
    assert child_defects == {0, 3}

    parent_extension = next(iter(parent_extensions))
    print(
        f"parent collision: n={length} tail={tail} "
        f"right={render(next(iter(right_halves)))} "
        f"extension={render(parent_extension)} survival=8 charge={charge}"
    )
    for child, extension, defect in child_records:
        print(
            f"  child={child} tail=2 extension={extension} "
            f"survival=2 first-defect={defect}"
        )
    print(
        "same parent continuation -> two child traces and defects {0,3}: "
        "parent-only morph KILLED"
    )


if __name__ == "__main__":
    main()

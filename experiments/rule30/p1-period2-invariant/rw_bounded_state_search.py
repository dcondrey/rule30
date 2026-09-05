#!/usr/bin/env python3
"""Option 2: does literal_extension's forcing recursion reduce to a bounded

(Myhill-Nerode) state, specifically for the H_r(n)/RW survival question --
not the general Delta_j defect diagonal_quotient.py already showed has no
bounded symbol-quotient.

Motivation, read directly from the code:
  - cone_local(l, r) = INVERSE[swap(l)][r] (dyadic_periodicity_analyzer.py):
    for fixed l this is a FIXED permutation of the 4-state alphabet, chosen
    by l.  peel_lift_monoid.py already proves the 4 permutations
    {INVERSE[swap(0)],...,INVERSE[swap(3)]} generate an 8-element group
    under composition (``table_orientation_control``, ``assert len(group)
    == 8``).
  - append_dependency_edge/literal_extension compute the new top-of-edge
    value as this composed permutation applied to a seed.  Composition is
    associative, so IF the recursion can be re-expressed as "apply one more
    generator to a running composed permutation" (rather than re-scanning
    the whole edge every time), the top-of-edge sequence is exactly a
    finite-state (Mealy machine) process over the group's 8 elements
    (crossed with whatever extra bit the hard-core check needs), NOT an
    unbounded-memory one.

This script does NOT assume that re-expression is correct.  It empirically
verifies it against the actual, already-trusted ``append_dependency_edge``/
``literal_extension`` code, on real words, before building anything on top
of it.  If verification fails, that is a real, reportable negative result
(the state genuinely needs more than the group element to track), not a bug
to paper over.
"""

from __future__ import annotations

import argparse
from itertools import product

from dyadic_periodicity_analyzer import BOUNDARY, INVERSE, swap
from constant_tail_scale import append_dependency_edge
from late_pull_diagonal_sat import literal_extension


Transform = tuple[int, int, int, int]

GENERATORS: tuple[Transform, ...] = tuple(INVERSE[swap(l)] for l in range(4))
IDENTITY: Transform = (0, 1, 2, 3)


def compose(outer: Transform, inner: Transform) -> Transform:
    """outer applied after inner: (outer o inner)(x) = outer[inner[x]]."""

    return tuple(outer[inner[x]] for x in range(4))  # type: ignore[return-value]


def right_generated_group(gens: tuple[Transform, ...]) -> set[Transform]:
    found = {IDENTITY}
    frontier = [IDENTITY]
    while frontier:
        g = frontier.pop()
        for gen in gens:
            h = compose(gen, g)
            if h not in found:
                found.add(h)
                frontier.append(h)
    return found


def naive_top(edge: tuple[int, ...], previous: int, value: int) -> int:
    """Ground truth: literal append_dependency_edge, return new top."""

    return append_dependency_edge(edge, previous, value)[-1]


def hypothesis_top(state: Transform, value: int) -> int:
    """Claimed compact recurrence: top = state(BOUNDARY[value])."""

    return state[BOUNDARY[value]]


def state_after(state: Transform, forced_value_emitted: int) -> Transform:
    """Claimed update: fold in the just-emitted top-of-edge value as the

    next generator, i.e. new_state = generator(forced_value_emitted) o state.
    """

    return compose(GENERATORS[forced_value_emitted], state)


def verify(max_source: int, tails: tuple[int, ...], residues: tuple[int, ...]) -> None:
    """Cross-check the compact-state recurrence against literal_extension

    on every word up to max_source, for every (tail, residue).  This is
    the actual proof-relevant check: if hypothesis_top/state_after ever
    disagree with the real append_dependency_edge-based computation, the
    finite-state claim is false as stated.
    """

    mismatches = 0
    checked = 0
    for n in range(1, max_source + 1):
        for word in product((1, 2), repeat=n):
            for tail in tails:
                for r in residues:
                    target = n + r
                    rows = target + 2

                    # Build ground truth incrementally, exactly as
                    # literal_extension does, and in parallel maintain the
                    # claimed compact state, comparing every row.
                    endpoint = list((0,) * n + word)
                    edge: tuple[int, ...] = ()
                    for v in (0,) * n + word:
                        edge = append_dependency_edge(
                            edge, endpoint[len(edge) - 1] if edge else None, v
                        )
                    # Ground-truth continuation via the trusted function:
                    continuation = literal_extension(word, tail, rows)

                    # Now walk the continuation rows, maintaining our own
                    # compact state in parallel with the ground-truth edge,
                    # and assert agreement at every row.
                    state = IDENTITY
                    # Fold in the pre-existing edge/word history first, to
                    # get the compact state to match wherever `edge` is now.
                    # edge currently reflects the full padded+word history;
                    # replay it into `state` via the same generator rule.
                    for e in edge:
                        state = compose(GENERATORS[e], state)

                    previous = word[-1]
                    ground_edge = edge
                    for row in range(rows):
                        checked += 1
                        predicted = hypothesis_top(state, continuation[row])
                        # Ground truth for this row's top:
                        ground_edge = append_dependency_edge(
                            ground_edge, previous, continuation[row]
                        )
                        actual = ground_edge[-1]
                        if predicted != actual:
                            mismatches += 1
                            if mismatches <= 5:
                                print(
                                    f"MISMATCH n={n} word={word} tail={tail} r={r} "
                                    f"row={row}: predicted={predicted} actual={actual}"
                                )
                        # actual should equal tail by literal_extension's
                        # own construction; state_after uses the emitted
                        # continuation value (continuation[row]), not the
                        # cut value, to match append_dependency_edge's own
                        # fold (it folds in *symbols*, whose cut outputs are
                        # `edge` entries -- see note below).
                        state = compose(GENERATORS[ground_edge[-2] if len(ground_edge) > 1 else continuation[row]], state) if False else state
                        # Placeholder ended: real update below.
                        state = state_after(state, ground_edge[-1])
                        previous = continuation[row]

    print(f"checked {checked} rows, {mismatches} mismatches "
          f"(max_source={max_source}, tails={tails}, residues={residues})")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-source", type=int, default=8)
    parser.add_argument("--tails", type=int, nargs="+", default=[2, 3])
    parser.add_argument("--residues", type=int, nargs="+", default=[0, 1, 2])
    args = parser.parse_args()

    group = right_generated_group(GENERATORS)
    print(f"generated group size: {len(group)} (expect 8, per peel_lift_monoid.py)")
    assert len(group) == 8

    verify(args.max_source, tuple(args.tails), tuple(args.residues))


if __name__ == "__main__":
    main()

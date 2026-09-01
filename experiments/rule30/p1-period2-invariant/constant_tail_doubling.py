#!/usr/bin/env python3
"""Audit period-doubling events in exact constant-tail lasso orbits.

The input corpus is finite, but every individual orbit step is the exact
canonical endpoint-shift map.  The purpose is to test whether a proposed
finite cycle profile closes across doublings before attempting a uniform
proof with that profile.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from itertools import product
from pathlib import Path

from constant_tail_shift import Lasso, endpoint_shift, lift_lasso
from dyadic_periodicity_analyzer import (
    IDENTITY,
    compose,
    inverse_cone_diagonal,
    least_period,
    transformation_cycles,
)
from peel_lift_monoid import LIFT_GENERATORS, LIFT_MONOID
from rank_zero_separator import hard_core_prefixes


Vector = tuple[int, ...]
Transform = tuple[int, int, int, int]


def canonical_rotation(word: Vector) -> Vector:
    return min(word[index:] + word[:index] for index in range(len(word)))


def return_transform(word: Vector) -> Transform:
    transform = IDENTITY
    for symbol in word:
        transform = compose(LIFT_GENERATORS[symbol], transform)
    return transform


def cycle_profile(word: Vector) -> tuple[object, ...]:
    word = canonical_rotation(word)
    half = len(word) // 2
    half_disagreements = (
        sum(word[index] != word[index + half] for index in range(half))
        if half
        else 0
    )
    bit_defect = (
        sum((word[index] ^ word[index + half]).bit_count() for index in range(half))
        if half
        else 0
    )
    return (
        len(word),
        tuple(word.count(symbol) for symbol in range(4)),
        return_transform(word),
        half_disagreements,
        bit_defect,
    )


def doubling_monoid_lemma() -> tuple[Transform, ...]:
    """Return the lift-monoid elements that can double a driver period.

    Every such element has exactly one cyclic component, of length two.
    This finite monoid fact proves that the doubled output cycle of a fixed
    driver word is unique up to rotation at *every* driver period.
    """

    doubling = tuple(
        sorted(
            transform
            for transform in LIFT_MONOID
            if any(len(cycle) == 2 for cycle in transformation_cycles(transform))
        )
    )
    assert doubling == (
        (1, 2, 3, 2),
        (2, 0, 0, 0),
        (3, 2, 3, 2),
    )
    assert all(
        tuple(map(len, transformation_cycles(transform))) == (2,)
        for transform in doubling
    )
    return doubling


def orbit_record(endpoint: Vector, tail: int) -> dict[str, object]:
    cut = Lasso.canonical(inverse_cone_diagonal(endpoint), (tail,))
    seen: set[Lasso] = set()
    trace = []
    doublings = []
    step = 0
    while cut not in seen:
        seen.add(cut)
        following = endpoint_shift(cut)
        trace.append((cut.preperiod, cut.period))
        if following is None:
            return {
                "survival": step + 1,
                "trace": trace,
                "doublings": doublings,
                "cycle": False,
            }
        if following.period > cut.period:
            assert following.period == 2 * cut.period
            doublings.append(
                {
                    "step": step + 1,
                    "before_preperiod": cut.preperiod,
                    "after_preperiod": following.preperiod,
                    "before_cycle": "".join(map(str, cut.cycle)),
                    "after_cycle": "".join(map(str, following.cycle)),
                    "before_profile": cycle_profile(cut.cycle),
                    "after_profile": cycle_profile(following.cycle),
                }
            )
        cut = following
        step += 1
    return {
        "survival": None,
        "trace": trace,
        "doublings": doublings,
        "cycle": True,
    }


def load_ga_records(directory: Path) -> list[tuple[Vector, int, str]]:
    answer = []
    for name in ("ga_tail2_results.json", "ga_tail3_results.json"):
        path = directory / name
        if not path.exists():
            continue
        for record in json.loads(path.read_text()):
            answer.append(
                (
                    tuple(map(int, record["endpoint_prefix"])),
                    int(record["tail"]),
                    f"{name}:T={record['cutoff']}",
                )
            )
    return answer


def build_corpus(max_exhaustive_cutoff: int, ga_directory: Path):
    corpus: list[tuple[Vector, int, str]] = []
    for cutoff in range(1, max_exhaustive_cutoff + 1):
        for endpoint in hard_core_prefixes(cutoff):
            for tail in (2, 3):
                corpus.append((endpoint, tail, f"exact:T={cutoff}"))
    corpus.extend(load_ga_records(ga_directory))
    return corpus


def universal_cycle_audit(max_period: int) -> dict[str, object]:
    """Audit the profile on *all* primitive dyadic driver cycles.

    This is deliberately independent of endpoint cutoffs.  For every
    primitive word ``w`` of dyadic length at most ``max_period`` and every
    possible state entering its periodic tail, lift the pure periodic driver
    exactly.  A collision proves that ``cycle_profile`` is not an inductive
    state descriptor, even if no collision occurred in the hard-core corpus.

    The exact cycle word is also tracked up to rotation.  Its observed
    determinism is not needed as a finite-data conjecture: whenever a lift
    doubles, the return transformation is one of the three lift-monoid
    elements with a unique two-cycle.  The two points of that cycle merely
    rotate the lifted word by one driver period.
    """

    if max_period < 1 or max_period & (max_period - 1):
        raise ValueError("universal maximum period must be a positive power of two")
    # 4^16 inputs is already too large for this exhaustive guardrail.  The
    # option is intentionally bounded; it is a falsifier for the profile, not
    # an asserted induction over dyadic periods.
    if max_period > 8:
        raise ValueError("universal exhaustive audit is capped at period 8")

    profile_transitions: dict[
        tuple[object, ...], set[tuple[object, ...]]
    ] = defaultdict(set)
    exact_transitions: dict[Vector, set[Vector]] = defaultdict(set)
    profile_witnesses: dict[
        tuple[tuple[object, ...], tuple[object, ...]], tuple[Vector, Vector, int]
    ] = {}
    rows = []
    total_words = 0
    total_lifts = 0
    total_doublings = 0

    period = 1
    while period <= max_period:
        words = 0
        lifts = 0
        doublings = 0
        for word in product(range(4), repeat=period):
            if least_period(word) != period:
                continue
            words += 1
            total_words += 1
            driver = Lasso.canonical((), word)
            for initial in range(4):
                following = lift_lasso(driver, initial)
                lifts += 1
                total_lifts += 1
                if following.period != 2 * period:
                    continue
                doublings += 1
                total_doublings += 1
                before_word = canonical_rotation(driver.cycle)
                after_word = canonical_rotation(following.cycle)
                before_profile = cycle_profile(before_word)
                after_profile = cycle_profile(after_word)
                exact_transitions[before_word].add(after_word)
                profile_transitions[before_profile].add(after_profile)
                profile_witnesses.setdefault(
                    (before_profile, after_profile),
                    (before_word, after_word, initial),
                )
        rows.append(
            {
                "period": period,
                "primitive_words": words,
                "lifts": lifts,
                "doublings": doublings,
            }
        )
        period *= 2

    profile_collisions = []
    for before, afters in profile_transitions.items():
        if len(afters) <= 1:
            continue
        profile_collisions.append(
            {
                "before_profile": before,
                "outputs": [
                    {
                        "after_profile": after,
                        "before_cycle": "".join(
                            map(str, profile_witnesses[(before, after)][0])
                        ),
                        "after_cycle": "".join(
                            map(str, profile_witnesses[(before, after)][1])
                        ),
                        "initial": profile_witnesses[(before, after)][2],
                    }
                    for after in sorted(afters, key=str)
                ],
            }
        )

    exact_collisions = {
        "".join(map(str, before)): ["".join(map(str, after)) for after in afters]
        for before, afters in exact_transitions.items()
        if len(afters) > 1
    }
    return {
        "max_period": max_period,
        "period_rows": rows,
        "primitive_words": total_words,
        "lifts": total_lifts,
        "doublings": total_doublings,
        "profile_nodes": len(profile_transitions),
        "profile_edges": sum(map(len, profile_transitions.values())),
        "profile_collision_nodes": len(profile_collisions),
        "profile_collisions": profile_collisions,
        "exact_cycle_nodes": len(exact_transitions),
        "exact_cycle_edges": sum(map(len, exact_transitions.values())),
        "exact_cycle_collision_nodes": len(exact_collisions),
        "exact_cycle_collisions": exact_collisions,
    }


def periodic_cycle_successors(word: Vector) -> set[Vector]:
    """All lifted tail cycles over every periodic-entry state.

    Changing the phase of a periodic driver only changes the time origin of
    each bi-infinite periodic lift, hence only rotates its canonical cycle.
    It is therefore enough to use one driver phase and all four entry states.
    """

    answer = set()
    driver = Lasso.canonical((), word)
    for initial in range(4):
        lifted = lift_lasso(driver, initial)
        answer.add(canonical_rotation(lifted.cycle))
    return answer


def abstract_tail_branch_audit(max_steps: int) -> dict[str, object]:
    """Follow the prefix-independent cycle orbit until it first branches.

    An eventually constant lasso has an arbitrary finite prefix.  Once a
    periodic driver is reached, that prefix can select any state entering the
    periodic tail.  This audit therefore follows every one of the four entry
    states (driver phase is immaterial up to cycle rotation).  A branching
    witness rules out treating the tail
    cycle as a deterministic state independent of the lasso prefix.
    """

    records = []
    for tail in (2, 3):
        word = (tail,)
        changes = [
            {
                "step": 0,
                "period": 1,
                "cycle": str(tail),
                "return_transform": return_transform(word),
            }
        ]
        branch = None
        for step in range(max_steps + 1):
            successors = periodic_cycle_successors(word)
            if len(successors) > 1:
                branch = {
                    "step": step,
                    "period": len(word),
                    "driver_cycle": "".join(map(str, word)),
                    "return_transform": return_transform(word),
                    "successor_cycles": [
                        "".join(map(str, value)) for value in sorted(successors)
                    ],
                }
                break
            following = next(iter(successors))
            if len(following) != len(word):
                changes.append(
                    {
                        "step": step + 1,
                        "period": len(following),
                        "cycle": "".join(map(str, following)),
                        "return_transform": return_transform(following),
                    }
                )
            word = following
        records.append(
            {
                "tail": tail,
                "period_changes": changes,
                "first_branch": branch,
            }
        )
    if max_steps >= 26603:
        expected_changes = {
            2: ((0, 1), (2, 2), (4, 4), (15, 8), (200, 16)),
            3: ((0, 1), (1, 2), (4, 4), (14, 8), (200, 16)),
        }
        for record in records:
            branch = record["first_branch"]
            assert branch is not None
            assert (branch["step"], branch["period"]) == (26603, 16)
            assert len(branch["successor_cycles"]) == 2
            changes = tuple(
                (item["step"], item["period"])
                for item in record["period_changes"]
            )
            assert changes == expected_changes[record["tail"]]
    return {"max_steps": max_steps, "tails": records}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-exhaustive-cutoff", type=int, default=14)
    parser.add_argument(
        "--ga-directory",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "openevolve-p1-rank-zero",
    )
    parser.add_argument(
        "--universal-max-period",
        type=int,
        default=8,
        help="exhaust every primitive dyadic driver cycle through this period",
    )
    parser.add_argument(
        "--abstract-branch-steps",
        type=int,
        default=27000,
        help="follow the two constant tail-cycle orbits to this many shifts",
    )
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    if args.max_exhaustive_cutoff < 1:
        parser.error("cutoff must be positive")

    corpus = build_corpus(args.max_exhaustive_cutoff, args.ga_directory)
    transitions: dict[tuple[object, ...], set[tuple[object, ...]]] = defaultdict(set)
    witnesses: dict[tuple[tuple[object, ...], tuple[object, ...]], str] = {}
    maximum_period = 1
    maximum_doublings = 0
    cycles = 0
    detailed = []
    for endpoint, tail, label in corpus:
        result = orbit_record(endpoint, tail)
        cycles += int(result["cycle"])
        maximum_doublings = max(maximum_doublings, len(result["doublings"]))
        maximum_period = max(
            maximum_period,
            *(period for _, period in result["trace"]),
        )
        for event in result["doublings"]:
            before = tuple(event["before_profile"])
            after = tuple(event["after_profile"])
            transitions[before].add(after)
            witnesses.setdefault((before, after), label)
        if label.startswith("ga_") or ":T=96" in label:
            detailed.append(
                {
                    "label": label,
                    "tail": tail,
                    "survival": result["survival"],
                    "period_trace": [period for _, period in result["trace"]],
                    "doublings": result["doublings"],
                }
            )

    collisions = {
        str(profile): [str(value) for value in sorted(values, key=str)]
        for profile, values in transitions.items()
        if len(values) > 1
    }
    if args.abstract_branch_steps < 0:
        parser.error("abstract branch steps must be nonnegative")

    doubling_transforms = doubling_monoid_lemma()
    universal = universal_cycle_audit(args.universal_max_period)
    abstract_branches = abstract_tail_branch_audit(args.abstract_branch_steps)
    summary = {
        "corpus_size": len(corpus),
        "maximum_period": maximum_period,
        "maximum_doublings": maximum_doublings,
        "lasso_cycles": cycles,
        "doubling_profile_nodes": len(transitions),
        "doubling_profile_edges": sum(map(len, transitions.values())),
        "nondeterministic_profile_nodes": len(collisions),
        "profile_collisions": collisions,
        "ga_records": detailed,
        "doubling_monoid_transforms": doubling_transforms,
        "universal_cycle_audit": universal,
        "abstract_tail_branch_audit": abstract_branches,
    }
    print(f"exact lasso orbits audited: {len(corpus)}")
    print(f"maximum period: {maximum_period}")
    print(f"maximum doubling count: {maximum_doublings}")
    print(f"hard-core lasso cycles found: {cycles}")
    print(
        "cycle-profile graph: "
        f"{len(transitions)} nodes, {sum(map(len, transitions.values()))} edges, "
        f"{len(collisions)} nondeterministic nodes"
    )
    print(
        "universal doubling audit: "
        f"{universal['primitive_words']} primitive words, "
        f"{universal['doublings']} doubling lifts, "
        f"{universal['profile_collision_nodes']} profile collisions, "
        f"{universal['exact_cycle_collision_nodes']} exact-cycle collisions"
    )
    print(
        "unique two-cycle doubling transforms: "
        f"{len(doubling_transforms)} monoid elements PASS"
    )
    for record in abstract_branches["tails"]:
        branch = record["first_branch"]
        if branch is None:
            print(
                f"tail {record['tail']} abstract cycle: no branch through "
                f"{args.abstract_branch_steps} shifts"
            )
        else:
            print(
                f"tail {record['tail']} abstract cycle: first branch at shift "
                f"{branch['step']}, period {branch['period']}, "
                f"{len(branch['successor_cycles'])} successors"
            )
    if args.json is not None:
        args.json.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
        print(f"wrote {args.json}")


if __name__ == "__main__":
    main()

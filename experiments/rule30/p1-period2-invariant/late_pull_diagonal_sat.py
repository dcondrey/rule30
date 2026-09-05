#!/usr/bin/env python3
"""Exact CNF falsifier for the three-row late-pull diagonal target.

For each source length n, tail c, and residue r in {0,1,2}, the formula is
SAT iff a binary source word has a hard-core forced continuation through row
n+r+1 and makes endpoint transition 1 -> 2 at row n+r.  Finite UNSAT
instances are not an all-length proof.
"""

from __future__ import annotations

import argparse
import itertools
import time
from dataclasses import dataclass
from typing import Iterable

from pysat.solvers import Solver

from constant_tail_scale import Vector, append_dependency_edge
from dyadic_periodicity_analyzer import BOUNDARY, cone_local
from mortality_sat import Encoder


BitPair = tuple[int, int]


def phase_defect(state: int) -> tuple[int, int]:
    """Return (high,equality), with equality zero exactly on states 1/2."""

    high, low = state >> 1, state & 1
    return high, 1 ^ high ^ low


def phase_defect_controls() -> int:
    checked = 0
    for left in range(4):
        for right in range(4):
            left_high, left_defect = phase_defect(left)
            right_high, right_defect = phase_defect(right)
            expected = (
                right_high
                ^ 1
                ^ left_defect
                ^ (left_defect & left_high),
                right_defect
                ^ (right_high & (left_high ^ left_defect)),
            )
            assert phase_defect(cone_local(left, right)) == expected
            checked += 1
    for state in range(4):
        high, defect = phase_defect(state)
        assert phase_defect(BOUNDARY[state]) == (1 ^ high, defect)
        checked += 1
    assert {state for state in range(4) if phase_defect(state)[1] == 0} == {
        1,
        2,
    }
    return checked


@dataclass(slots=True)
class Instance:
    n: int
    tail: int
    residue: int
    encoder: Encoder
    source_bits: tuple[BitPair, ...]
    endpoint_high: tuple[int, ...]


def cone_gate(
    encoder: Encoder, left: BitPair, right: BitPair, role: str
) -> BitPair:
    """Tseitin-encode the exact four-state map cone_local(left,right)."""

    left_high, left_low = left
    right_high, right_low = right
    activity = encoder.or_gate(left_high, left_low, f"{role}.activity")
    high = encoder.xor_gate(right_high, activity, f"{role}.high")
    # low' = right_low XOR ((NOT left_low) AND right_high) XOR activity.
    # Encode the conjunction as NOT(left_low OR NOT right_high).
    complement = encoder.or_gate(
        left_low, -right_high, f"{role}.low-complement"
    )
    partial = encoder.xor_gate(
        right_low, -complement, f"{role}.low-partial"
    )
    low = encoder.xor_gate(partial, activity, f"{role}.low")
    return high, low


def append_edge(
    encoder: Encoder,
    edge: tuple[BitPair, ...],
    previous: BitPair | None,
    value: BitPair,
    role: str,
) -> tuple[BitPair, ...]:
    following: list[BitPair] = [(-value[0], -value[1])]
    if not edge:
        assert previous is None
        return tuple(following)
    assert previous is not None
    following.append(
        cone_gate(encoder, previous, following[0], f"{role}.order.1")
    )
    for order in range(2, len(edge) + 1):
        following.append(
            cone_gate(
                encoder,
                edge[order - 2],
                following[-1],
                f"{role}.order.{order}",
            )
        )
    return tuple(following)


def constrain_tail(encoder: Encoder, state: BitPair, tail: int) -> None:
    high, low = state
    encoder.add(high)
    encoder.add(low if tail == 3 else -low)


def build_instance(
    n: int,
    tail: int,
    residue: int,
    *,
    binary_source: bool = True,
    hard_core_source: bool = False,
    hard_core_continuation: bool = True,
    tail_window: int | None = None,
    relaxed_source_positions: frozenset[int] = frozenset(),
) -> Instance:
    if n < 1 or tail not in (2, 3) or residue not in (0, 1, 2):
        raise ValueError("require n>=1, tail in {2,3}, residue in {0,1,2}")
    encoder = Encoder()
    source: list[BitPair] = []
    if not binary_source and relaxed_source_positions:
        raise ValueError("source relaxation positions require binary_source=True")
    if any(index < 0 or index >= n for index in relaxed_source_positions):
        raise ValueError("source relaxation position is out of range")
    for index in range(n):
        if binary_source and index not in relaxed_source_positions:
            high = encoder.new(f"source.{index}.high")
            source.append((high, -high))
        else:
            source.append(
                (
                    encoder.new(f"source.{index}.high"),
                    encoder.new(f"source.{index}.low"),
                )
            )
    if hard_core_source:
        if not binary_source or relaxed_source_positions:
            raise ValueError("hard-core source option requires a fully binary source")
        for left, right in zip(source, source[1:]):
            encoder.add(left[0], right[0])

    edge: tuple[BitPair, ...] = ()
    endpoint: list[BitPair] = []
    for index, value in enumerate(
        [(encoder.zero, encoder.zero)] * n + source
    ):
        edge = append_edge(
            encoder,
            edge,
            endpoint[-1] if endpoint else None,
            value,
            f"initial.{index}",
        )
        endpoint.append(value)

    target = n + residue
    extension_high: list[int] = []
    for row in range(target + 2):
        high = encoder.new(f"extension.{row}.high")
        value = (high, -high)
        previous = endpoint[-1]
        if hard_core_continuation:
            # On the binary alphabet, state 1 means high=0.  Therefore this
            # clause is exactly the exclusion of consecutive state 1.
            encoder.add(previous[0], high)
        edge = append_edge(
            encoder, edge, previous, value, f"extension.{row}"
        )
        if tail_window is None or row >= target + 2 - tail_window:
            constrain_tail(encoder, edge[-1], tail)
        endpoint.append(value)
        extension_high.append(high)

    # Pull at target: previous state 1 (high zero), current state 2 (high one).
    encoder.add(-extension_high[target - 1])
    encoder.add(extension_high[target])
    return Instance(
        n,
        tail,
        residue,
        encoder,
        tuple(source),
        tuple(extension_high),
    )


def solve(
    instance: Instance, *, proof: bool = False
) -> tuple[bool, list[int] | None, list[str], dict[str, int | float]]:
    started = time.perf_counter()
    with Solver(
        name="glucose4" if proof else "cadical195",
        bootstrap_with=instance.encoder.clauses,
        with_proof=proof,
    ) as solver:
        sat = solver.solve()
        model = solver.get_model() if sat else None
        proof_lines = (solver.get_proof() or []) if proof else []
        stats: dict[str, int | float] = dict(solver.accum_stats())
    stats["seconds"] = time.perf_counter() - started
    return sat, model, proof_lines, stats


def decode_source(instance: Instance, model: Iterable[int]) -> Vector:
    positive = {literal for literal in model if literal > 0}

    def bit(literal: int) -> int:
        return int(literal > 0 and literal in positive or literal < 0 and -literal not in positive)

    return tuple(2 * bit(high) + bit(low) for high, low in instance.source_bits)


def decode_extension(instance: Instance, model: Iterable[int]) -> Vector:
    positive = {literal for literal in model if literal > 0}
    return tuple(2 if variable in positive else 1 for variable in instance.endpoint_high)


def replay_cut(word: Vector, extension: Vector) -> Vector:
    edge: Vector = ()
    endpoint: list[int] = []
    for value in (0,) * len(word) + word:
        edge = append_dependency_edge(
            edge, endpoint[-1] if endpoint else None, value
        )
        endpoint.append(value)
    cut = []
    for value in extension:
        edge = append_dependency_edge(edge, endpoint[-1], value)
        endpoint.append(value)
        cut.append(edge[-1])
    return tuple(cut)


def literal_extension(word: Vector, tail: int, rows: int) -> Vector:
    endpoint: list[int] = []
    edge: Vector = ()
    for value in (0,) * len(word) + word:
        edge = append_dependency_edge(
            edge, endpoint[-1] if endpoint else None, value
        )
        endpoint.append(value)
    extension = []
    for _ in range(rows):
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


def literal_witness(
    word: Vector, tail: int, residue: int, *, hard_core: bool = True
) -> bool:
    n = len(word)
    target = n + residue
    extension = literal_extension(word, tail, target + 2)
    previous = word[-1]
    for row, forced in enumerate(extension[: target + 2]):
        if hard_core and (
            forced not in (1, 2) or previous == forced == 1
        ):
            return False
        if row == target and previous == 1 and forced == 2:
            return True
        previous = forced
    return False


def validation(max_n: int = 7) -> int:
    checked = 0
    for n in range(1, max_n + 1):
        words = tuple(itertools.product((1, 2), repeat=n))
        for tail in (2, 3):
            for residue in (0, 1, 2):
                direct = any(literal_witness(word, tail, residue) for word in words)
                instance = build_instance(n, tail, residue)
                sat, model, _proof, _stats = solve(instance)
                assert sat == direct
                if sat:
                    assert model is not None
                    assert literal_witness(
                        decode_source(instance, model), tail, residue
                    )
                checked += 1
    return checked


def controls() -> tuple[str, str]:
    arbitrary = build_instance(2, 3, 0, binary_source=False)
    sat, model, _proof, _stats = solve(arbitrary)
    assert sat and model is not None
    arbitrary_word = decode_source(arbitrary, model)
    assert literal_witness(arbitrary_word, 3, 0)

    no_hard_core = None
    for n in range(1, 9):
        for tail in (2, 3):
            for residue in (0, 1, 2):
                candidate = build_instance(
                    n, tail, residue, hard_core_continuation=False
                )
                sat, model, _proof, _stats = solve(candidate)
                if sat:
                    assert model is not None
                    word = decode_source(candidate, model)
                    assert literal_witness(
                        word, tail, residue, hard_core=False
                    )
                    no_hard_core = (
                        f"n={n},tail={tail},r={residue},W="
                        f"{''.join(map(str, word))}"
                    )
                    break
            if no_hard_core:
                break
        if no_hard_core:
            break
    assert no_hard_core is not None
    return "".join(map(str, arbitrary_word)), no_hard_core


def proof_width(lines: list[str]) -> int:
    maximum = 0
    for line in lines:
        fields = line.split()
        if not fields or fields[0] == "d":
            continue
        maximum = max(maximum, sum(field != "0" for field in fields))
    return maximum


def window_audit(n: int) -> tuple[list[str], str]:
    fields = []
    for tail in (2, 3):
        for residue in (0, 1, 2):
            total = n + residue + 2
            minimum = None
            for window in range(1, total + 1):
                instance = build_instance(
                    n,
                    tail,
                    residue,
                    hard_core_source=True,
                    tail_window=window,
                )
                sat, _model, _proof, _stats = solve(instance)
                if not sat:
                    minimum = window
                    break
            assert minimum is not None
            fields.append(f"c{tail}r{residue}={minimum}/{total}")

    # Exact certificate that a six-symbol constant-cut suffix, even with a
    # hard-core source and continuation, does not locally exclude the pull.
    instance = build_instance(
        12,
        2,
        0,
        hard_core_source=True,
        tail_window=6,
    )
    sat, model, _proof, _stats = solve(instance)
    assert sat and model is not None
    word = decode_source(instance, model)
    extension = decode_extension(instance, model)
    cut = replay_cut(word, extension)
    assert all(left != 1 or right != 1 for left, right in zip(word, word[1:]))
    assert all(
        left != 1 or right != 1
        for left, right in zip((word[-1],) + extension, extension)
    )
    assert extension[11:14] in ((1, 2, 1), (1, 2, 2))
    assert cut[-6:] == (2,) * 6 and cut != (2,) * len(cut)
    witness = (
        f"W={''.join(map(str, word))} "
        f"extension={''.join(map(str, extension))} "
        f"cut={''.join(map(str, cut))}"
    )
    return fields, witness


def source_defect_audit(max_n: int) -> None:
    for n in range(2, max_n + 1):
        fields = []
        for tail in (2, 3):
            for residue in (0, 1, 2):
                relaxed = []
                for position in range(n):
                    instance = build_instance(
                        n,
                        tail,
                        residue,
                        relaxed_source_positions=frozenset((position,)),
                    )
                    sat, model, _proof, _stats = solve(instance)
                    if sat:
                        assert model is not None
                        word = decode_source(instance, model)
                        assert word[position] in (0, 3)
                        assert literal_witness(word, tail, residue)
                        relaxed.append(position)
                arbitrary = build_instance(n, tail, residue, binary_source=False)
                sat, model, _proof, _stats = solve(arbitrary)
                if sat:
                    assert model is not None
                    assert literal_witness(
                        decode_source(arbitrary, model), tail, residue
                    )
                fields.append(
                    f"c{tail}r{residue}=single{relaxed}/all{int(sat)}"
                )
        print(f"source-defect n={n}: " + " ".join(fields), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=40)
    parser.add_argument("--max-validate", type=int, default=7)
    parser.add_argument("--proof-through", type=int, default=12)
    parser.add_argument("--window-audit-n", type=int, default=12)
    parser.add_argument("--source-defect-through", type=int, default=0)
    args = parser.parse_args()
    if (
        args.max_n < 1
        or args.max_validate < 0
        or args.proof_through < 0
        or args.window_audit_n < 0
        or args.source_defect_through < 0
    ):
        parser.error("invalid bounds")

    checked = validation(args.max_validate)
    coordinates = phase_defect_controls()
    print(
        f"phase/equality local identities: {coordinates} cases PASS; "
        f"CNF/literal validation: {checked} formulas PASS",
        flush=True,
    )
    arbitrary, no_hard_core = controls()
    print(
        "controls SAT: arbitrary-source W="
        f"{arbitrary}; no-hard-core {no_hard_core} PASS",
        flush=True,
    )
    if args.window_audit_n:
        windows, witness = window_audit(args.window_audit_n)
        print(
            f"tail-suffix windows n={args.window_audit_n}: "
            + " ".join(windows),
            flush=True,
        )
        print(f"six-symbol local-window counterexample: {witness} PASS", flush=True)
    if args.source_defect_through:
        source_defect_audit(args.source_defect_through)

    failures = 0
    for n in range(1, args.max_n + 1):
        fields = []
        for tail in (2, 3):
            for residue in (0, 1, 2):
                instance = build_instance(n, tail, residue)
                want_proof = n <= args.proof_through
                sat, model, proof, stats = solve(instance, proof=want_proof)
                if sat:
                    failures += 1
                    assert model is not None
                    word = decode_source(instance, model)
                    assert literal_witness(word, tail, residue)
                    outcome = f"SAT:{''.join(map(str, word))}"
                else:
                    outcome = "UNSAT"
                fields.append(
                    f"c{tail}r{residue}={outcome} "
                    f"v{instance.encoder.top}/q{len(instance.encoder.clauses)} "
                    f"x{int(stats.get('conflicts', 0))} "
                    f"p{len(proof)}/w{proof_width(proof)} "
                    f"t{stats['seconds']:.3f}"
                )
        print(f"n={n:2d} " + " | ".join(fields), flush=True)
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

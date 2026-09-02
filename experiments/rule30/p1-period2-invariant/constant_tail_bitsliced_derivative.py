#!/usr/bin/env python3
"""Bit-sliced held-out validation of the fixed scale-derivative selector."""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

from constant_tail_derivative_rank import binary_rank
from constant_tail_ordered_matching import correction_count, forced_trace
from constant_tail_scale import Vector, hard_core_extension_length
from rank_zero_separator import hard_core_prefixes


BitState = tuple[int, int]
BitAffine = tuple[int, int, int]


def bit_state(value: int, mask: int) -> BitState:
    return (mask if value >> 1 else 0, mask if value & 1 else 0)


def cone_local_bits(left: BitState, right: BitState, mask: int) -> BitState:
    left_high, left_low = left
    right_high, right_low = right
    activity = left_high | left_low
    return (
        right_high ^ activity,
        right_low ^ ((mask ^ left_low) & right_high) ^ activity,
    )


def append_edge_bits(
    edge: tuple[BitState, ...],
    previous: BitState | None,
    value: BitState,
    mask: int,
) -> tuple[BitState, ...]:
    following = [(value[0] ^ mask, value[1] ^ mask)]
    if not edge:
        assert previous is None
        return tuple(following)
    assert previous is not None
    following.append(cone_local_bits(previous, following[0], mask))
    for order in range(2, len(edge) + 1):
        following.append(
            cone_local_bits(edge[order - 2], following[-1], mask)
        )
    return tuple(following)


def newest_affine_bits(
    edge: tuple[BitState, ...], previous: BitState, mask: int
) -> BitAffine:
    """Compose the newest-cut permutation in the D8 affine coordinates."""

    alpha, beta, gamma = mask, 0, mask  # BOUNDARY = (1,0,1)
    for left in (previous,) + edge[:-1]:
        activity = left[0] | left[1]
        local_alpha = activity
        local_beta = mask ^ left[1]
        old_alpha = alpha
        alpha = local_alpha ^ alpha
        beta = local_beta ^ beta
        gamma = activity ^ gamma ^ (local_beta & old_alpha)
    return alpha, beta, gamma


def forced_value_bits(
    affine: BitAffine, tail: int, mask: int
) -> BitState:
    alpha, beta, gamma = affine
    high = mask ^ alpha
    low = (mask if tail & 1 else 0) ^ (beta & high) ^ gamma
    return high, low


def scenario_word_states(word: Vector) -> tuple[list[BitState], list[int], int]:
    sources = [index for index, value in enumerate(word) if value == 2]
    scenarios = len(sources) + 1
    mask = (1 << scenarios) - 1
    source_scenario = {source: column + 1 for column, source in enumerate(sources)}
    states = []
    for index, value in enumerate(word):
        if value == 1:
            states.append((0, mask))
        else:
            changed = 1 << source_scenario[index]
            states.append((mask ^ changed, changed))
    return states, sources, mask


def bitsliced_trace(
    word: Vector, tail: int
) -> tuple[tuple[BitState, ...], tuple[BitAffine, ...], list[int], int]:
    word_states, sources, mask = scenario_word_states(word)
    extension, affines = bitsliced_trace_states(
        word_states, len(word), tail, mask
    )
    return extension, affines, sources, mask


def bitsliced_trace_states(
    word_states: list[BitState], length: int, tail: int, mask: int
) -> tuple[tuple[BitState, ...], tuple[BitAffine, ...]]:
    """Run arbitrary bit-sliced source scenarios of one common length."""

    if len(word_states) != length:
        raise ValueError("word-state list and source length disagree")
    endpoint: list[BitState] = []
    edge: tuple[BitState, ...] = ()
    zero = (0, 0)
    for value in [zero] * length + word_states:
        edge = append_edge_bits(
            edge, endpoint[-1] if endpoint else None, value, mask
        )
        endpoint.append(value)

    extension: list[BitState] = []
    affines: list[BitAffine] = []
    for _ in range(2 * length):
        affine = newest_affine_bits(edge, endpoint[-1], mask)
        value = forced_value_bits(affine, tail, mask)
        affines.append(affine)
        edge = append_edge_bits(edge, endpoint[-1], value, mask)
        endpoint.append(value)
        extension.append(value)
    return tuple(extension), tuple(affines)


def scenario_state(state: BitState, scenario: int) -> int:
    return 2 * ((state[0] >> scenario) & 1) + ((state[1] >> scenario) & 1)


def scenario_affine(affine: BitAffine, scenario: int) -> tuple[int, int, int]:
    return tuple((coordinate >> scenario) & 1 for coordinate in affine)  # type: ignore[return-value]


def derivative_row(coordinate: int, sources: int, mask: int) -> int:
    original = coordinate & 1
    scenarios = coordinate >> 1
    if original:
        scenarios ^= (1 << sources) - 1
    assert scenarios >> sources == 0
    assert mask == (1 << (sources + 1)) - 1
    return scenarios


def slow_controls(max_length: int) -> int:
    checked = 0
    for length in range(1, max_length + 1):
        for word in hard_core_prefixes(length):
            for tail in (2, 3):
                extension, affines, sources, _ = bitsliced_trace(word, tail)
                scenarios = [word]
                for source in sources:
                    scenarios.append(word[:source] + (1,) + word[source + 1 :])
                for scenario, source_word in enumerate(scenarios):
                    slow_extension, slow_steps = forced_trace(source_word, tail)
                    for step in range(2 * length):
                        assert scenario_state(extension[step], scenario) == slow_extension[step]
                        assert scenario_affine(affines[step], scenario) == (
                            slow_steps[step].affine.alpha,
                            slow_steps[step].affine.beta,
                            slow_steps[step].affine.gamma,
                        )
                        checked += 1
    return checked


@dataclass(slots=True)
class Census:
    cases: int = 0
    prefixes: int = 0
    failures: int = 0
    minimum_slack: int = 10**9
    first_failure: str | None = None
    paired_failures: int = 0
    paired_minimum_slack: int = 10**9
    paired_first_failure: str | None = None


def audit_word(word: Vector, tail: int, census: Census) -> tuple[int, int, int]:
    extension_bits, affines, sources, mask = bitsliced_trace(word, tail)
    original_extension = tuple(scenario_state(state, 0) for state in extension_bits)
    survival = hard_core_extension_length(word, original_extension)
    correction = correction_count(word, tail)
    alpha_rows = [
        derivative_row(affine[0], len(sources), mask)
        for affine in affines[:survival]
    ]
    beta_rows = [
        derivative_row(affine[1], len(sources), mask)
        for affine in affines[:survival]
    ]

    selected: list[int] = []
    basis: dict[int, int] = {}
    paired: list[int] = []
    paired_basis: dict[int, int] = {}
    minimum = 10**9
    paired_minimum = 10**9
    for step in range(survival):
        forced = original_extension[step]
        assert forced in (1, 2)
        row = alpha_rows[step] if tail == 3 or forced == 1 else beta_rows[step]
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
        for paired_row in (alpha_rows[step], beta_rows[step]):
            paired.append(paired_row)
            vector = paired_row
            while vector:
                pivot = vector.bit_length() - 1
                if pivot not in paired_basis:
                    paired_basis[pivot] = vector
                    break
                vector ^= paired_basis[pivot]
        paired_rank = len(paired_basis)
        assert paired_rank == binary_rank(paired)
        target = max(0, step + 1 - correction)
        slack = rank - target
        paired_slack = paired_rank - target
        minimum = min(minimum, slack)
        paired_minimum = min(paired_minimum, paired_slack)
        census.prefixes += 1
        if slack < 0:
            census.failures += 1
            if census.first_failure is None:
                census.first_failure = (
                    f"tail={tail} W={''.join(map(str, word))} "
                    f"prefix={step+1} s={survival} K={correction} "
                    f"#2={len(sources)} rank={rank} target={target}"
                )
        if paired_slack < 0:
            census.paired_failures += 1
            if census.paired_first_failure is None:
                census.paired_first_failure = (
                    f"tail={tail} W={''.join(map(str, word))} "
                    f"prefix={step+1} s={survival} K={correction} "
                    f"#2={len(sources)} paired-rank={paired_rank} "
                    f"target={target}"
                )
    if survival == 0:
        minimum = 0
        paired_minimum = 0
    census.cases += 1
    census.minimum_slack = min(census.minimum_slack, minimum)
    census.paired_minimum_slack = min(
        census.paired_minimum_slack, paired_minimum
    )
    return survival, minimum, paired_minimum


def random_hard_core(length: int, generator: random.Random) -> Vector:
    word = []
    for _ in range(length):
        if word and word[-1] == 1:
            word.append(2)
        else:
            word.append(generator.choice((1, 2)))
    return tuple(word)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--control-length", type=int, default=7)
    parser.add_argument("--exhaustive-first", type=int, default=17)
    parser.add_argument("--exhaustive-last", type=int, default=22)
    parser.add_argument("--random-per-length", type=int, default=1000)
    args = parser.parse_args()
    if not (0 <= args.control_length and 1 <= args.exhaustive_first <= args.exhaustive_last):
        parser.error("invalid length bounds")

    controls = slow_controls(args.control_length)
    print(f"slow/bit-sliced trajectory controls: {controls} steps PASS")

    census = Census()
    for length in range(args.exhaustive_first, args.exhaustive_last + 1):
        before_cases = census.cases
        before_prefixes = census.prefixes
        before_failures = census.failures
        before_paired_failures = census.paired_failures
        for word in hard_core_prefixes(length):
            for tail in (2, 3):
                audit_word(word, tail, census)
        print(
            f"exhaustive length={length:2d} cases={census.cases-before_cases:6d} "
            f"prefixes={census.prefixes-before_prefixes:6d} "
            f"failures={census.failures-before_failures:4d} "
            f"paired-failures="
            f"{census.paired_failures-before_paired_failures:4d} "
            f"global-min-slack={census.minimum_slack} "
            f"paired-global-min-slack={census.paired_minimum_slack}"
        )

    repair = tuple(map(int, "12212121212121212"))
    survival, slack, paired_slack = audit_word(repair, 2, census)
    print(
        f"repair witness survival={survival} minimum-slack={slack} "
        f"paired-minimum-slack={paired_slack}"
    )

    selector_counterexample = tuple(map(int, "121212222222221212122"))
    survival, slack, paired_slack = audit_word(
        selector_counterexample, 2, census
    )
    print(
        f"selector counterexample survival={survival} minimum-slack={slack} "
        f"paired-minimum-slack={paired_slack}"
    )

    generator = random.Random(30030)
    for length in (24, 32, 48, 64):
        before_failures = census.failures
        before_paired_failures = census.paired_failures
        minimum = 10**9
        paired_minimum = 10**9
        for _ in range(args.random_per_length):
            word = random_hard_core(length, generator)
            for tail in (2, 3):
                _, slack, paired_slack = audit_word(word, tail, census)
                minimum = min(minimum, slack)
                paired_minimum = min(paired_minimum, paired_slack)
        print(
            f"random length={length:2d} cases={2*args.random_per_length:5d} "
            f"failures={census.failures-before_failures:4d} "
            f"paired-failures="
            f"{census.paired_failures-before_paired_failures:4d} "
            f"min-slack={minimum} paired-min-slack={paired_minimum}"
        )

    print(
        f"TOTAL cases={census.cases} prefixes={census.prefixes} "
        f"failures={census.failures} min-slack={census.minimum_slack} "
        f"paired-failures={census.paired_failures} "
        f"paired-min-slack={census.paired_minimum_slack}"
    )
    print(f"first failure: {census.first_failure or 'none'}")
    print(
        f"paired first failure: {census.paired_first_failure or 'none'}"
    )


if __name__ == "__main__":
    main()

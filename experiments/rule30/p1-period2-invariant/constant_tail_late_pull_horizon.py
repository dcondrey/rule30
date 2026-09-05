#!/usr/bin/env python3
"""Bounded falsifier for the late-pull horizon (LPH).

LPH says that a length-n hard-core scale word has no nonfinal forced endpoint
transition 1 -> 2 at a row j >= n.  It is strictly weaker than pull-row alpha
support and uses no zero-prefix scenarios.  A finite pass is not a proof.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
from dataclasses import dataclass
from pathlib import Path

from constant_tail_bitsliced_derivative import (
    BitState,
    bitsliced_trace_states,
)
from constant_tail_scale import Vector, scale_extension
from rank_zero_separator import hard_core_prefixes


EXPERIMENTS = Path(__file__).resolve().parents[2]
GA_FILES = (
    EXPERIMENTS / "openevolve-p1-rank-zero" / "ga_tail2_results.json",
    EXPERIMENTS / "openevolve-p1-rank-zero" / "ga_tail3_results.json",
)


@dataclass(slots=True)
class Census:
    words: int = 0
    surviving_pulls: int = 0
    nonfinal_pulls: int = 0
    late_surviving_pulls: int = 0
    late_nonfinal_pulls: int = 0
    maximum_pull_row: int = -1
    minimum_slack: int = 10**9
    maximum_word: str | None = None
    first_late: str | None = None


def pack_words(words: list[Vector]) -> tuple[list[BitState], int]:
    if not words:
        return [], 0
    length = len(words[0])
    if any(len(word) != length for word in words):
        raise ValueError("packed words must have one common length")
    high = [0] * length
    low = [0] * length
    for scenario, word in enumerate(words):
        bit = 1 << scenario
        for index, value in enumerate(word):
            if value >> 1:
                high[index] |= bit
            if value & 1:
                low[index] |= bit
    return list(zip(high, low)), (1 << len(words)) - 1


def audit_batch(words: list[Vector], tail: int, census: Census) -> None:
    if not words:
        return
    length = len(words[0])
    states, mask = pack_words(words)
    extension, _affines = bitsliced_trace_states(states, length, tail, mask)

    active = mask
    active_after: list[int] = []
    for row, (high, low) in enumerate(extension):
        previous = states[-1] if row == 0 else extension[row - 1]
        previous_one = (mask ^ previous[0]) & previous[1]
        forced_one = (mask ^ high) & low
        forced_two = high & (mask ^ low)
        legal = (forced_one | forced_two) & (mask ^ (previous_one & forced_one))
        active &= legal
        active_after.append(active)

    for row, (high, low) in enumerate(extension[:-1]):
        previous = states[-1] if row == 0 else extension[row - 1]
        previous_one = (mask ^ previous[0]) & previous[1]
        forced_two = high & (mask ^ low)
        pulls = active_after[row] & previous_one & forced_two
        nonfinal = pulls & active_after[row + 1]
        pull_count = pulls.bit_count()
        nonfinal_count = nonfinal.bit_count()
        census.surviving_pulls += pull_count
        census.nonfinal_pulls += nonfinal_count
        if pulls:
            slack = length - 1 - row
            census.minimum_slack = min(census.minimum_slack, slack)
            if row > census.maximum_pull_row:
                scenario = (pulls & -pulls).bit_length() - 1
                census.maximum_pull_row = row
                census.maximum_word = "".join(map(str, words[scenario]))
        if row >= length:
            census.late_surviving_pulls += pull_count
            census.late_nonfinal_pulls += nonfinal_count
            if pulls and census.first_late is None:
                scenario = (pulls & -pulls).bit_length() - 1
                census.first_late = (
                    f"tail={tail} n={length} row={row} "
                    f"nonfinal={bool(nonfinal & (1 << scenario))} "
                    f"W={''.join(map(str, words[scenario]))}"
                )
    census.words += len(words)


def literal_controls(max_length: int = 7) -> int:
    checked = 0
    for length in range(1, max_length + 1):
        words = list(hard_core_prefixes(length))
        for tail in (2, 3):
            packed = Census()
            audit_batch(words, tail, packed)
            literal = Census()
            for word in words:
                extension = scale_extension(word, tail)
                survival = 0
                previous = word[-1]
                pulls: list[int] = []
                for row, forced in enumerate(extension):
                    legal = forced in (1, 2) and not (previous == forced == 1)
                    if not legal:
                        break
                    survival += 1
                    if previous == 1 and forced == 2:
                        pulls.append(row)
                    previous = forced
                literal.words += 1
                literal.surviving_pulls += len(pulls)
                literal.nonfinal_pulls += sum(row + 1 < survival for row in pulls)
                literal.late_surviving_pulls += sum(row >= length for row in pulls)
                literal.late_nonfinal_pulls += sum(
                    row >= length and row + 1 < survival for row in pulls
                )
                if pulls and pulls[-1] > literal.maximum_pull_row:
                    literal.maximum_pull_row = pulls[-1]
                    literal.minimum_slack = length - 1 - pulls[-1]
                    literal.maximum_word = "".join(map(str, word))
                checked += len(extension)
            assert (
                packed.words,
                packed.surviving_pulls,
                packed.nonfinal_pulls,
                packed.late_surviving_pulls,
                packed.late_nonfinal_pulls,
                packed.maximum_pull_row,
            ) == (
                literal.words,
                literal.surviving_pulls,
                literal.nonfinal_pulls,
                literal.late_surviving_pulls,
                literal.late_nonfinal_pulls,
                literal.maximum_pull_row,
            )
    return checked


def random_hard_core(length: int, generator: random.Random) -> Vector:
    word: list[int] = []
    for _ in range(length):
        word.append(
            2 if word and word[-1] == 1 else generator.choice((1, 2))
        )
    return tuple(word)


def ga_scale_words() -> list[tuple[Vector, int, int]]:
    answer = []
    for path in GA_FILES:
        for record in json.loads(path.read_text()):
            cutoff = int(record["cutoff"])
            if cutoff % 2:
                continue
            endpoint = tuple(map(int, record["endpoint_prefix"]))
            assert len(endpoint) == cutoff
            half = cutoff // 2
            answer.append((endpoint[half:], int(record["tail"]), cutoff))
    return answer


def render(label: str, census: Census) -> str:
    slack = census.minimum_slack if census.maximum_pull_row >= 0 else "-"
    return (
        f"{label} words={census.words} pulls={census.surviving_pulls} "
        f"nonfinal-pulls={census.nonfinal_pulls} "
        f"late-pulls={census.late_surviving_pulls} "
        f"late-nonfinal={census.late_nonfinal_pulls} "
        f"max-row={census.maximum_pull_row} min-slack={slack} "
        f"max-word={census.maximum_word or '-'}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exact-max-length", type=int, default=23)
    parser.add_argument("--random-per-length", type=int, default=20_000)
    parser.add_argument("--all-binary-max-length", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=30041)
    args = parser.parse_args()
    if (
        args.exact_max_length < 1
        or args.all_binary_max_length < 0
        or args.random_per_length < 0
        or args.batch_size < 1
    ):
        parser.error("invalid audit bound")

    controls = literal_controls()
    print(f"packed/literal controls: {controls} forced rows PASS", flush=True)

    exact = Census()
    for length in range(1, args.exact_max_length + 1):
        words = list(hard_core_prefixes(length))
        for start in range(0, len(words), args.batch_size):
            batch = words[start : start + args.batch_size]
            for tail in (2, 3):
                audit_batch(batch, tail, exact)
        print(render(f"exact-through-{length}", exact), flush=True)

    ga = Census()
    for word, tail, cutoff in ga_scale_words():
        audit_batch([word], tail, ga)
        print(render(f"GA-cutoff-{cutoff}-tail-{tail}", ga), flush=True)

    binary = Census()
    for length in range(1, args.all_binary_max_length + 1):
        words = list(itertools.product((1, 2), repeat=length))
        for start in range(0, len(words), args.batch_size):
            batch = words[start : start + args.batch_size]
            for tail in (2, 3):
                audit_batch(batch, tail, binary)
        print(render(f"all-binary-through-{length}", binary), flush=True)

    generator = random.Random(args.seed)
    random_census = Census()
    for length in (24, 32, 48, 64, 96, 128):
        remaining = args.random_per_length
        while remaining:
            size = min(args.batch_size, remaining)
            words = [random_hard_core(length, generator) for _ in range(size)]
            for tail in (2, 3):
                audit_batch(words, tail, random_census)
            remaining -= size
        print(render(f"random-through-{length}", random_census), flush=True)

    total_late = (
        exact.late_nonfinal_pulls
        + ga.late_nonfinal_pulls
        + binary.late_nonfinal_pulls
        + random_census.late_nonfinal_pulls
    )
    print(render("EXACT", exact))
    print(render("GA", ga))
    print(render("ALL-BINARY", binary))
    print(render("RANDOM", random_census))
    print(
        "first late pull: "
        f"{exact.first_late or ga.first_late or binary.first_late or random_census.first_late or 'none'}"
    )
    if total_late:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

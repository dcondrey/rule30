#!/usr/bin/env python3
"""Search fixed finite quotients suggested by the failed additive rankings.

Summaries retain endpoint words and local-pattern counts modulo a fixed m.
They scan the whole frontier with fixed memory and therefore do not form a
depth ladder.  A quotient is rejected by an exact pair of raw states having
the same summary and different failure/next-summary outcomes, or by exceeding
the preregistered 256-state ceiling.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from ranking_search import (  # noqa: E402
    State,
    forced_macro,
    frontier_word,
    seed_state,
)


def count_codes(word: tuple[int, ...], locality: int, modulus: int) -> tuple[int, ...]:
    counts = [0] * (4**locality)
    for start in range(len(word) - locality + 1):
        code = 0
        for symbol in word[start : start + locality]:
            code = 4 * code + symbol
        counts[code] = (counts[code] + 1) % modulus
    return tuple(counts)


def summary(
    state: State, locality: int, modulus: int, endpoint_width: int
) -> tuple[int, ...]:
    word = frontier_word(0, state)
    width = min(endpoint_width, len(word))
    prefix = word[:width]
    suffix = word[-width:] if width else ()
    return (
        len(word) % modulus,
        width,
        *prefix,
        *suffix,
        *count_codes(word, locality, modulus),
    )


@dataclass(frozen=True)
class Origin:
    seed_length: int
    seed: int
    follow: int
    state: State


def raw_states(max_seed: int, max_follow: int) -> list[Origin]:
    result: list[Origin] = []
    seen: set[State] = set()
    for length in range(1, max_seed + 1):
        for seed in range(1 << length):
            state = seed_state(seed, length)
            for follow in range(max_follow + 1):
                if state not in seen:
                    seen.add(state)
                    result.append(Origin(length, seed, follow, state))
                nxt = forced_macro(0, state)
                if nxt is None:
                    break
                state = nxt
    return result


def origin_label(origin: Origin) -> str:
    return (
        f"k={origin.seed_length},seed="
        f"{origin.seed:0{origin.seed_length}b},follow={origin.follow},"
        f"state={origin.state}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-seed", type=int, default=12)
    parser.add_argument("--max-follow", type=int, default=64)
    args = parser.parse_args()
    origins = raw_states(args.max_seed, args.max_follow)
    print(f"distinct exact finite-seed frontier states: {len(origins)}")

    for locality in range(1, 5):
        for modulus in (2, 3, 4):
            for endpoint_width in (0, 1, 2):
                groups: dict[tuple[int, ...], tuple[tuple[object, ...], Origin]] = {}
                collision = None
                for origin in origins:
                    key = summary(origin.state, locality, modulus, endpoint_width)
                    nxt = forced_macro(0, origin.state)
                    outcome: tuple[object, ...]
                    if nxt is None:
                        outcome = ("FAIL",)
                    else:
                        outcome = (
                            "NEXT",
                            summary(nxt, locality, modulus, endpoint_width),
                        )
                    old = groups.get(key)
                    if old is not None and old[0] != outcome:
                        collision = old[1], origin, old[0], outcome
                        break
                    groups[key] = outcome, origin
                label = f"L={locality},m={modulus},e={endpoint_width}"
                if collision is not None:
                    first, second, out1, out2 = collision
                    print(
                        f"{label}: COLLISION at {len(groups)} summaries; "
                        f"{origin_label(first)} versus {origin_label(second)}; "
                        f"outcomes={out1[0]}/{out2[0]}"
                    )
                elif len(groups) > 256:
                    print(f"{label}: KILL state ceiling, {len(groups)} > 256")
                else:
                    print(
                        f"{label}: SURVIVES sample with {len(groups)} states "
                        "(requires uniform soundness proof)"
                    )


if __name__ == "__main__":
    main()

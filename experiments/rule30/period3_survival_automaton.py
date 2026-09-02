#!/usr/bin/env python3
"""Exact horizon automaton for the period-three active-core schedules.

An ``H``-step cascade of the three-symbol transducer has one carry bit at each
layer.  Reading one initial core symbol updates those ``H`` bits
deterministically.  After the word ends, the phase-dependent boundary symbols
are flushed through the remaining layers and the pin parities are checked.

The resulting DFA recognizes exactly the finite cores surviving ``H`` steps.
Its shortest accepted-word length is an exact lower bound on the initial core
needed for that horizon.  A finite sequence of such bounds is not mortality.
"""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
from itertools import product

from period3_active_core import quotient_driven_step
from period3_fiber_probe import PERIOD_WORDS

QuotientCore = tuple[int, ...]


def propagate_symbol(
    state: int,
    symbol: int,
    horizon: int,
    start_layer: int = 0,
) -> int:
    """Feed one quotient symbol through a suffix of the carry cascade."""

    if not 0 <= symbol < 3:
        raise ValueError("quotient symbol must lie in [0,2]")
    if not 0 <= start_layer <= horizon:
        raise ValueError("invalid start layer")
    for layer in range(start_layer, horizon):
        carry = (state >> layer) & 1
        emitted = 2 if carry else int(symbol == 2)
        updated = carry ^ int(symbol != 0)
        if updated != carry:
            state ^= 1 << layer
        symbol = emitted
    return state


def state_after_word(core: QuotientCore, horizon: int) -> int:
    """Return the cascade carry vector after reading one complete core."""

    if horizon < 0:
        raise ValueError("horizon must be nonnegative")
    state = 0
    for symbol in core:
        state = propagate_symbol(state, symbol, horizon)
    return state


def accepting_state(
    state: int,
    period: tuple[int, ...],
    phase: int,
    horizon: int,
) -> bool:
    """Flush all boundaries and decide the exact horizon pin schedule."""

    for layer in range(horizon):
        center = period[(phase + layer) % len(period)]
        following = period[(phase + layer + 1) % len(period)]
        parity = (state >> layer) & 1
        if center == 1 and parity != (1 ^ following):
            return False
        boundary = 2 if parity else center
        state = propagate_symbol(state, boundary, horizon, layer + 1)
    return True


def direct_survives(
    core: QuotientCore,
    period: tuple[int, ...],
    phase: int,
    horizon: int,
) -> bool:
    """Reference evaluator using literal successive quotient words."""

    current = core
    for elapsed in range(horizon):
        following = quotient_driven_step(current, period, phase + elapsed)
        if following is None:
            return False
        current = following
    return True


@dataclass(frozen=True)
class ShortestSurvivor:
    horizon: int
    length: int | None
    word: QuotientCore | None
    discovered_states: int


def shortest_survivor(
    period: tuple[int, ...], phase: int, horizon: int
) -> ShortestSurvivor:
    """Breadth-first search the carry DFA for a shortest surviving core."""

    if horizon < 0:
        raise ValueError("horizon must be nonnegative")
    start = 0
    if accepting_state(start, period, phase, horizon):
        return ShortestSurvivor(horizon, 0, (), 1)

    queue = deque([start])
    distance = {start: 0}
    previous: dict[int, tuple[int, int]] = {}
    while queue:
        state = queue.popleft()
        for symbol in (1, 2, 0):
            following = propagate_symbol(state, symbol, horizon)
            if following in distance:
                continue
            distance[following] = distance[state] + 1
            previous[following] = state, symbol
            if accepting_state(following, period, phase, horizon):
                word = []
                cursor = following
                while cursor != start:
                    cursor, used = previous[cursor]
                    word.append(used)
                return ShortestSurvivor(
                    horizon,
                    distance[following],
                    tuple(reversed(word)),
                    len(distance),
                )
            queue.append(following)
    return ShortestSurvivor(horizon, None, None, len(distance))


def exhaustive_control(max_horizon: int = 8, max_length: int = 5) -> None:
    """Compare the DFA and literal word dynamics on a finite complete grid."""

    for period in PERIOD_WORDS:
        for phase in range(len(period)):
            for horizon in range(max_horizon + 1):
                for length in range(max_length + 1):
                    for core in product(range(3), repeat=length):
                        via_dfa = accepting_state(
                            state_after_word(core, horizon),
                            period,
                            phase,
                            horizon,
                        )
                        assert via_dfa == direct_survives(
                            core, period, phase, horizon
                        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-horizon", type=int, default=24)
    parser.add_argument("--control-horizon", type=int, default=7)
    parser.add_argument("--control-length", type=int, default=4)
    args = parser.parse_args()
    if min(args.max_horizon, args.control_horizon, args.control_length) < 0:
        parser.error("bounds must be nonnegative")

    exhaustive_control(args.control_horizon, args.control_length)
    print("period-three survival carry automaton: direct control PASS")
    for period in PERIOD_WORDS[::-1]:
        print(f"trace={''.join(map(str, period))}")
        print("phase horizon min_length discovered_states witness")
        for phase in range(len(period)):
            for horizon in range(1, args.max_horizon + 1):
                result = shortest_survivor(period, phase, horizon)
                witness = (
                    "NONE"
                    if result.word is None
                    else "".join(map(str, result.word)) or "EMPTY"
                )
                print(
                    f"{phase:5d} {horizon:7d} {str(result.length):>10s} "
                    f"{result.discovered_states:17d} {witness}"
                )


if __name__ == "__main__":
    main()


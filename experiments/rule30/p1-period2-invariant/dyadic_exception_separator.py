#!/usr/bin/env python3
"""Exact checks for the dyadic exceptional-family separator.

The proof-level statement checked locally here is the one-cell descent used in
``RESULTS-DYADIC-EXCEPTION-SEPARATOR.md``.  The finite graph census is only a
regression check; the descent itself is uniform in the cascade width.
"""

from __future__ import annotations

import argparse
from itertools import product

from dyadic_periodicity_analyzer import (
    FORWARD,
    INVERSE,
    cascade_step,
    cone_local,
    inverse_cone_diagonal,
    least_period,
    swap,
)


def alternating_descent_table() -> tuple[tuple[int, int, int, int], ...]:
    """Return ``(previous output, output, last symbol, prefix output)`` rows.

    On an alternating output tail, the last internal cascade symbol at time
    ``t`` is ``swap(output[t-1]) = output[t]``.  Inverting the final carry
    action therefore determines the output of the width-one-shorter cascade.
    """

    rows = []
    for previous, current in ((1, 2), (2, 1)):
        last_symbol = swap(previous)
        assert last_symbol == current
        prefix_output = INVERSE[last_symbol][current]
        assert FORWARD[last_symbol][prefix_output] == current
        assert prefix_output == swap(current)
        rows.append((previous, current, last_symbol, prefix_output))
    return tuple(rows)


def output_orbit(word: int, width: int) -> tuple[int, tuple[int, ...]]:
    """Return preperiod and the primitive eventual output block."""

    seen: dict[int, int] = {}
    outputs: list[int] = []
    state = word
    while state not in seen:
        seen[state] = len(outputs)
        state, emitted = cascade_step(state, width)
        outputs.append(emitted)
    preperiod = seen[state]
    cycle = tuple(outputs[preperiod:])
    period = least_period(cycle)
    return preperiod, cycle[:period]


def cascade_outputs(word: int, width: int, steps: int) -> tuple[int, ...]:
    outputs = []
    state = word
    for _ in range(steps):
        state, emitted = cascade_step(state, width)
        outputs.append(emitted)
    return tuple(outputs)


def peel_identity_control(max_width: int = 5, steps: int = 24) -> int:
    """Cross-check the output-only width-peel identity on all small states."""

    checked = 0
    for width in range(1, max_width + 1):
        prefix_mask = (1 << (2 * (width - 1))) - 1
        for word in range(1 << (2 * width)):
            outputs = cascade_outputs(word, width, steps)
            prefix = cascade_outputs(word & prefix_mask, width - 1, steps)
            for time in range(1, steps):
                assert (
                    cone_local(outputs[time - 1], outputs[time])
                    == prefix[time]
                )
                checked += 1
    return checked


def finite_graph_control(max_width: int) -> int:
    """Check every finite cascade state through ``max_width``.

    This is deliberately stronger than checking only core-generated states,
    but remains a bounded control and is not the proof of the theorem.
    """

    checked = 0
    forbidden = {(1, 2), (2, 1)}
    for width in range(1, max_width + 1):
        for word in range(1 << (2 * width)):
            _, block = output_orbit(word, width)
            assert block not in forbidden
            checked += 1
    return checked


def hard_core_prefixes(length: int):
    for prefix in product((1, 2), repeat=length):
        if all(
            left != right or left != 1
            for left, right in zip(prefix, prefix[1:])
        ):
            yield prefix


def exceptional_family_control(max_prefix: int) -> int:
    """Check the exact eventually-2 endpoint dependency bound.

    If an endpoint is all state 2 after a prefix of length ``N``, its inverse
    terminal cut is alternating from coordinate ``2N`` onward.  The all-width
    statement follows from the dependency interval proved in the predecessor
    dyadic audit; these instances guard the alignment and phase.
    """

    checked = 0
    for length in range(max_prefix + 1):
        for prefix in hard_core_prefixes(length):
            endpoint = prefix + (2,) * (length + 24)
            cut = inverse_cone_diagonal(endpoint)
            assert all(
                cut[index] == 1 + index % 2
                for index in range(2 * length, len(cut))
            )
            checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-width", type=int, default=8)
    parser.add_argument("--max-prefix", type=int, default=8)
    args = parser.parse_args()
    if args.max_width < 1 or args.max_prefix < 0:
        parser.error("width must be positive and prefix must be nonnegative")

    rows = alternating_descent_table()
    assert rows == ((1, 2, 2, 1), (2, 1, 1, 2))
    print(f"alternating one-cell descent table: {rows} PASS")

    peel_checks = peel_identity_control()
    print(f"output-only Peel identity: {peel_checks} cells PASS")

    graph_checks = finite_graph_control(args.max_width)
    print(
        "finite cascade output cycles: "
        f"{graph_checks} states through width {args.max_width} PASS"
    )

    family_checks = exceptional_family_control(args.max_prefix)
    print(
        "eventually-2 endpoint / eventually-12 cut alignment: "
        f"{family_checks} hard-core prefixes PASS"
    )


if __name__ == "__main__":
    main()

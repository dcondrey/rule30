#!/usr/bin/env python3
"""Prove simultaneous colex descent before and after queue normalization.

The normalized inverse-lift quotient is ``B=(0,1,2,1)``.  The reflected
OR-latch/carry quotient is ``F=(0,1,2,2)``.  Their joint values recover the
raw four-state scan symbol.  This checker exhausts finite synchronous
products and therefore covers legal queue words of every length.
"""

from __future__ import annotations

from collections import deque

from constant_tail_colex_descent import legal_decoder, latest_comparison
from constant_tail_language_cocycle import SFT_TRANSITIONS
from constant_tail_queue import (
    diagonal_from_endpoint,
    normalize_queue,
    queue_step,
)
from peel_lift_monoid import LIFT_GENERATORS


BACKWARD_QUOTIENT = (0, 1, 2, 1)
FORWARD_QUOTIENT = (0, 1, 2, 2)


def endpoint_from_diagonal(diagonal: tuple[int, ...]) -> tuple[int, ...]:
    """Invert the triangular endpoint-to-diagonal bijection."""

    endpoint: tuple[int, ...] = ()
    for target in diagonal:
        candidates = tuple(
            endpoint + (state,)
            for state in range(4)
            if diagonal_from_endpoint(endpoint + (state,))[-1] == target
        )
        assert len(candidates) == 1
        endpoint = candidates[0]
    return endpoint


def product_control(
    tail: int,
    output_map: tuple[int, ...],
    rank: dict[int, int],
) -> tuple[int, frozenset[tuple[int, int, int, str]]]:
    """Exhaust the SFT/scan/comparison product for one output map."""

    start_context = 3 if tail == 2 else 0
    start = (tail, start_context, 3, "equal", False)
    reachable = {start}
    frontier = deque((start,))
    finals: set[tuple[int, int, int, str]] = set()

    while frontier:
        scan, context, last, comparison, has_suffix = frontier.popleft()
        if (
            has_suffix
            and context != 4
            and last in (1, 2)
            and legal_decoder(last, scan)
        ):
            final = (scan, context, last, comparison)
            finals.add(final)
            assert comparison == "less"

        for source in range(3):
            next_scan = LIFT_GENERATORS[scan][source]
            output = output_map[next_scan]
            following = (
                next_scan,
                SFT_TRANSITIONS[context][source],
                source,
                latest_comparison(comparison, output, source, rank),
                True,
            )
            if following not in reachable:
                reachable.add(following)
                frontier.append(following)

    assert finals
    return len(reachable), frozenset(finals)


def main() -> None:
    ternary_orders = {
        "0<2<1": {0: 0, 2: 1, 1: 2},
        "2<0<1": {2: 0, 0: 1, 1: 2},
    }
    expected = {
        "backward": {
            "0<2<1": {2: 31, 3: 30},
            "2<0<1": {2: 35, 3: 34},
        },
        "forward": {
            "0<2<1": {2: 34, 3: 32},
            "2<0<1": {2: 36, 3: 34},
        },
    }
    for name, quotient in (
        ("backward", BACKWARD_QUOTIENT),
        ("forward", FORWARD_QUOTIENT),
    ):
        for order, rank in ternary_orders.items():
            for tail in (2, 3):
                states, finals = product_control(tail, quotient, rank)
                assert states == expected[name][order][tail]
                assert {comparison for *_rest, comparison in finals} == {
                    "less"
                }
                print(
                    f"quotient={name} order={order} tail={tail} "
                    f"states={states} finals={len(finals)} DESCENT PASS"
                )

    raw_orders = {
        "0<2<3<1": {0: 0, 2: 1, 3: 2, 1: 3},
        "2<0<3<1": {2: 0, 0: 1, 3: 2, 1: 3},
    }
    raw_expected = {
        "0<2<3<1": {2: 31, 3: 30},
        "2<0<3<1": {2: 33, 3: 32},
    }
    identity = (0, 1, 2, 3)
    for order, rank in raw_orders.items():
        for tail in (2, 3):
            states, finals = product_control(tail, identity, rank)
            assert states == raw_expected[order][tail]
            assert {comparison for *_rest, comparison in finals} == {
                "less"
            }
            print(
                f"quotient=raw order={order} tail={tail} "
                f"states={states} finals={len(finals)} DESCENT PASS"
            )

    joint = tuple(
        (BACKWARD_QUOTIENT[state], FORWARD_QUOTIENT[state])
        for state in range(4)
    )
    assert len(set(joint)) == 4
    assert [state for state in range(4) if joint[state][0] != joint[state][1]] == [3]
    print(f"joint quotient={joint} injective; sole disagreement state=3 PASS")

    # State 3 is not the only mechanism by which normalization can increase
    # the number of symbol-1 cells.  A state-1 scan propagates across an
    # arbitrarily long zero block.  This uniform family prevents the joint
    # quotient from being misread as a finite branching budget.
    for zeros in range(1, 65):
        queue = (2, 1) + (0,) * zeros + (1,)
        scan = []
        state = 2
        for symbol in queue[1:]:
            state = LIFT_GENERATORS[state][symbol]
            scan.append(state)
        assert tuple(scan) == (1,) * (zeros + 1) + (2,)
        assert 3 not in scan
        following = queue_step(queue, 2)
        assert following is not None
        normalized = normalize_queue(following.queue, 2)
        assert normalized[1:-1] == tuple(scan)
        assert normalized[-1] == 1
    print("state-1 zero-block fanout family: lengths 1..64 PASS (uniform table proof)")

    # The family is admissible for the stronger arbitrary-queue mortality
    # language, but it is not itself the reversed diagonal of a hard-core
    # endpoint.  The three cases below prove this uniformly: for m>=3 the
    # desired diagonal always begins 1000 and hence its endpoint begins 2120.
    assert endpoint_from_diagonal((1, 0, 1, 2)) == (2, 1, 3, 1)
    assert endpoint_from_diagonal((1, 0, 0, 1, 2)) == (2, 1, 2, 1, 3)
    assert endpoint_from_diagonal((1, 0, 0, 0)) == (2, 1, 2, 0)
    for zeros in range(1, 65):
        queue = (2, 1) + (0,) * zeros + (1,)
        endpoint = endpoint_from_diagonal(tuple(reversed(queue)))
        assert not all(
            state in (1, 2)
            and not (index and endpoint[index - 1] == state == 1)
            for index, state in enumerate(endpoint)
        )
    print(
        "fanout family is abstract-queue only: m=1 -> 2131, "
        "m=2 -> 21213, m>=3 starts 2120 PASS"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Prove strict colex descent of every legal normalized queue scan.

The proof exhausts a finite synchronous product, so it covers words of all
lengths.  It does not assert queue mortality: the legal update appends one
new boundary symbol after the strictly smaller old-coordinate scan.
"""

from __future__ import annotations

from collections import deque

from constant_tail_language_cocycle import SFT_TRANSITIONS
from constant_tail_queue import LIFT_GENERATORS, SYMBOL_QUOTIENT


Comparison = str
ProductState = tuple[int, int, int, Comparison, bool]
RANKS = {
    "0<2<1": {0: 0, 2: 1, 1: 2},
    "2<0<1": {2: 0, 0: 1, 1: 2},
}


def legal_decoder(last: int, final_scan_state: int) -> bool:
    """Return whether the hard-core boundary decoder accepts."""

    return (last == 1 and final_scan_state in (0, 2)) or (
        last == 2 and final_scan_state == 2
    )


def latest_comparison(
    previous: Comparison,
    output: int,
    source: int,
    rank: dict[int, int],
) -> Comparison:
    """Update the comparison at the newest/rightmost coordinate."""

    if output == source:
        return previous
    return "less" if rank[output] < rank[source] else "greater"


def product_control(
    tail: int, rank: dict[int, int]
) -> tuple[int, frozenset[tuple[int, int, int, str]]]:
    """Exhaust the SFT/scan/colex product for one fixed tail."""

    if tail not in (2, 3):
        raise ValueError("tail must be 2 or 3")

    # Tail 2 is part of the normalized SFT word and initializes the context
    # at ``last 2``.  The leading tail-3 symbol is only a scan initializer,
    # exactly as in the queue normalization theorem.
    start_context = 3 if tail == 2 else 0
    start: ProductState = (tail, start_context, 3, "equal", False)
    reachable = {start}
    frontier = deque((start,))
    legal_finals: set[tuple[int, int, int, str]] = set()

    while frontier:
        scan, context, last, comparison, has_suffix = frontier.popleft()

        if (
            has_suffix
            and context != 4
            and last in (1, 2)
            and legal_decoder(last, scan)
        ):
            final = (scan, context, last, comparison)
            legal_finals.add(final)
            assert comparison == "less"

        for source in range(3):
            following_scan = LIFT_GENERATORS[scan][source]
            output = SYMBOL_QUOTIENT[following_scan]
            following: ProductState = (
                following_scan,
                SFT_TRANSITIONS[context][source],
                source,
                latest_comparison(comparison, output, source, rank),
                True,
            )
            if following not in reachable:
                reachable.add(following)
                frontier.append(following)

    assert legal_finals
    return len(reachable), frozenset(legal_finals)


def main() -> None:
    expected_states = {
        "0<2<1": {2: 31, 3: 30},
        "2<0<1": {2: 35, 3: 34},
    }
    for order, rank in RANKS.items():
        for tail in (2, 3):
            states, finals = product_control(tail, rank)
            assert states == expected_states[order][tail]
            assert {comparison for *_prefix, comparison in finals} == {
                "less"
            }
            print(
                f"order={order} tail={tail} "
                f"reachable-product-states={states} "
                f"legal-final-states={len(finals)} "
                "strict-colex-descent PASS"
            )


if __name__ == "__main__":
    main()

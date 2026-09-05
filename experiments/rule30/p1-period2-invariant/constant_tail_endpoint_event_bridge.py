#!/usr/bin/env python3
"""Exact endpoint/event bridge and a literal-witness counterexample.

For a nonsingleton endpoint-derived reversed diagonal, successful queue
events are just the three allowed transitions of the hard-core endpoint:

    A <=> 2 -> 1,   B <=> 2 -> 2,   C <=> 1 -> 2.

The identities are uniform consequences of the boundary permutation.  The
finite sweeps below are regression controls, not their proof.  The stored
all-2 endpoint shows that a pull can occur even when the *initial* endpoint
contains no ``12`` factor, so pull ancestry cannot be charged to literal
initial endpoint pairs.
"""

from __future__ import annotations

import argparse

from constant_tail_hard_core_pull_depth import diagonal, endpoint_diagonals
from constant_tail_pull_coordinate_depth import update_type
from constant_tail_queue import normalize_queue, queue_step
from dyadic_periodicity_analyzer import BOUNDARY


Vector = tuple[int, ...]
PAIR_EVENT = {(2, 1): "A", (2, 2): "B", (1, 2): "C"}
NO_INITIAL_12_ENDPOINT = (2,) * 8


def event_trace(endpoint: Vector, cap: int = 100) -> tuple[str, Vector]:
    """Return the successful event word and appended endpoint symbols."""

    cut = diagonal(endpoint)
    tail = cut[-1]
    if tail not in (2, 3):
        return "", ()
    queue = normalize_queue(tuple(reversed(cut)), tail)
    previous_endpoint = endpoint[-1]
    events: list[str] = []
    extension: list[int] = []
    for _time in range(cap):
        following = queue_step(queue, tail)
        if following is None:
            return "".join(events), tuple(extension)
        successor = normalize_queue(following.queue, tail)
        kind = update_type(queue, successor)
        assert (previous_endpoint, following.endpoint) in PAIR_EVENT
        expected = PAIR_EVENT[previous_endpoint, following.endpoint]
        # The singleton queue (2,) is the one boundary-credit exception in
        # the pull-ray convention: update_type deliberately calls it B, not
        # C.  Every nonsingleton update obeys the literal dictionary.
        if queue == (2,):
            assert expected == "C" and kind == "B"
        else:
            assert kind == expected
        # The last queue cell is the normalized raw boundary state B(e).
        # On hard-core symbols B interchanges 1 and 2.
        assert queue[-1] == BOUNDARY[previous_endpoint]
        assert successor[-1] == BOUNDARY[following.endpoint]
        events.append(kind)
        extension.append(following.endpoint)
        queue = successor
        previous_endpoint = following.endpoint
    raise AssertionError("endpoint-derived queue reached the explicit cap")


def literal_witness_counterexample() -> tuple[str, str, str]:
    """A pull whose initial hard-core endpoint contains no ``12`` pair."""

    endpoint = NO_INITIAL_12_ENDPOINT
    assert all(endpoint[index : index + 2] != (1, 2) for index in range(7))
    cut = diagonal(endpoint)
    assert cut == tuple(map(int, "12121212"))
    queue = normalize_queue(tuple(reversed(cut)), cut[-1])
    assert queue == tuple(map(int, "21212121"))
    events, extension = event_trace(endpoint)
    assert events == "AC"
    assert extension == (1, 2)
    return (
        "".join(map(str, endpoint)),
        "".join(map(str, cut)),
        events,
    )


def exhaustive_controls(max_length: int) -> tuple[int, int]:
    endpoints = 0
    updates = 0
    for length in range(1, max_length + 1):
        for endpoint, cut in endpoint_diagonals(length):
            endpoints += 1
            if cut[-1] not in (2, 3):
                continue
            events, extension = event_trace(endpoint)
            assert len(events) == len(extension)
            updates += len(events)
    return endpoints, updates


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--control-length", type=int, default=15)
    args = parser.parse_args()
    if args.control_length < 1:
        parser.error("control length must be positive")

    endpoint, cut, events = literal_witness_counterexample()
    print(
        f"literal initial-12 witness FALSE: endpoint={endpoint} "
        f"D={cut} events={events} (C is a pull) PASS",
        flush=True,
    )
    endpoints, updates = exhaustive_controls(args.control_length)
    print(
        f"endpoint/event bridge through length={args.control_length}: "
        f"endpoints={endpoints} successful-updates={updates} PASS"
    )


if __name__ == "__main__":
    main()

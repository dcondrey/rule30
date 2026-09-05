#!/usr/bin/env python3
"""Second-generation edge-state representation: bytes instead of tuples
of ints. Motivation: dict keys built from a length-n tuple-of-Python-int
are expensive to hash (per-element hash-combine) and carry per-tuple
object overhead; a `bytes` object of the same length hashes with a
single C-level pass and costs ~33 bytes of overhead total instead of
~(56 + 8*n) for a tuple. This matters once state counts reach the
hundreds of thousands to millions (n>=24 in fastdk_benchmark.py).

Equivalence to fastdk_fastedge.append_edge_fast (itself already verified
bit-identical to the original constant_tail_scale.append_dependency_edge)
is checked exhaustively up to length 9 in `equivalence_check`, matching
the same discipline as fastdk_fastedge.py.
"""
from __future__ import annotations

from dyadic_periodicity_analyzer import cone_local, BOUNDARY

CONE = tuple(tuple(cone_local(l, r) for r in range(4)) for l in range(4))
BND = tuple(BOUNDARY)


def append_edge_bytes(edge: bytes, previous_endpoint, value: int) -> bytes:
    """Same recurrence as append_edge_fast, operating on/returning bytes.

    following[0] = BOUNDARY[value]
    following[k] = cone_local(edge[k-1], following[k-1]), k = 1..len(edge)
    """
    b0 = BND[value]
    if not edge:
        assert previous_endpoint is None
        return bytes((b0,))
    assert previous_endpoint is not None
    following = bytearray(len(edge) + 1)
    following[0] = b0
    prev_following = CONE[previous_endpoint][b0]
    following[1] = prev_following
    cone = CONE
    for order in range(1, len(edge)):
        prev_following = cone[edge[order - 1]][prev_following]
        following[order + 1] = prev_following
    return bytes(following)


def equivalence_check(max_len: int = 9) -> int:
    from itertools import product as iproduct
    from fastdk_fastedge import append_edge_fast

    checked = 0
    for length in range(0, max_len + 1):
        for word in iproduct(range(4), repeat=length):
            edge_tuple: tuple = ()
            edge_bytes = b""
            endpoint = None
            for value in word:
                edge_tuple = append_edge_fast(edge_tuple, endpoint, value)
                edge_bytes = append_edge_bytes(edge_bytes, endpoint, value)
                assert tuple(edge_bytes) == edge_tuple, (word, edge_tuple, edge_bytes)
                endpoint = value
                checked += 1
    return checked


if __name__ == "__main__":
    import sys

    max_len = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    n = equivalence_check(max_len)
    print(f"equivalence_check PASS: {n} incremental steps checked up to length {max_len}")

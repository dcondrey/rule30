#!/usr/bin/env python3
"""Optimized, allocation-lean reimplementation of
constant_tail_scale.append_dependency_edge using a precomputed 4x4
cone_local lookup table instead of the swap/INVERSE function-call chain.
Equivalence to the original is asserted by direct random+exhaustive
comparison in `equivalence_check`, not assumed.
"""
from __future__ import annotations

from dyadic_periodicity_analyzer import cone_local, BOUNDARY

# CONE[l][r] == cone_local(l, r); BND[v] == BOUNDARY[v]
CONE = tuple(tuple(cone_local(l, r) for r in range(4)) for l in range(4))
BND = tuple(BOUNDARY)


def append_edge_fast(edge: tuple[int, ...], previous_endpoint, value: int) -> tuple[int, ...]:
    cone = CONE
    b0 = BND[value]
    if not edge:
        assert previous_endpoint is None
        return (b0,)
    assert previous_endpoint is not None
    # following[k] = cone_local(edge[k-1], following[k-1]), k=1..len(edge);
    # following[0] = BOUNDARY[value]. Matches append_dependency_edge exactly.
    following = [b0]
    prev_following = cone[previous_endpoint][b0]
    following.append(prev_following)
    for order in range(1, len(edge)):
        prev_following = cone[edge[order - 1]][prev_following]
        following.append(prev_following)
    return tuple(following)


def equivalence_check(max_len: int = 9) -> int:
    from itertools import product as iproduct
    from constant_tail_scale import append_dependency_edge

    checked = 0
    for length in range(0, max_len + 1):
        for word in iproduct(range(4), repeat=length):
            edge = ()
            edge_fast = ()
            endpoint = None
            for value in word:
                edge = append_dependency_edge(edge, endpoint, value)
                edge_fast = append_edge_fast(edge_fast, endpoint, value)
                assert edge == edge_fast, (word, edge, edge_fast)
                endpoint = value
                checked += 1
    return checked


if __name__ == "__main__":
    import sys

    max_len = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    n = equivalence_check(max_len)
    print(f"equivalence_check PASS: {n} incremental steps checked up to length {max_len}")

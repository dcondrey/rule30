#!/usr/bin/env python3
"""Prototype: does deduping on the dependency-edge state collapse the
2^n source-word enumeration in literal_extension's construction?

For a given n, walk the trie of source words {1,2}^n one symbol at a
time, building the append_dependency_edge state exactly as
late_pull_diagonal_sat.literal_extension does (after the n zero-padding
steps), and group prefixes by their resulting edge tuple. If many
different prefixes converge to the same edge tuple, we can carry a
single representative forward instead of 2^k branches at prefix length k.

This is a diagnostic only -- prints, for each prefix length, the number
of live branches (words) vs number of DISTINCT edge states.
"""
from __future__ import annotations

from itertools import product

from constant_tail_scale import append_dependency_edge


def edge_after_zero_padding(n: int):
    edge = ()
    endpoint = []
    for _ in range(n):
        edge = append_dependency_edge(edge, endpoint[-1] if endpoint else None, 0)
        endpoint.append(0)
    return edge, endpoint[-1]


def dedup_trace(n: int, verbose: bool = True):
    zero_edge, zero_endpoint = edge_after_zero_padding(n)
    # states: dict edge_tuple -> count of words reaching it (endpoint value
    # is edge[-1] itself is not literally the endpoint symbol; track
    # endpoint separately since cone_local needs it, but edge[-1] IS the
    # newest diagonal entry -- check against append_dependency_edge usage:
    # in literal_extension, endpoint.append(value) tracks raw symbol,
    # separate from edge. Need both.)
    # state key = (edge_tuple, endpoint_symbol)
    states = {(zero_edge, zero_endpoint): 1}
    counts_per_length = []
    for step in range(n):
        new_states: dict = {}
        for (edge, endpoint_sym), cnt in states.items():
            for value in (1, 2):
                new_edge = append_dependency_edge(edge, endpoint_sym, value)
                key = (new_edge, value)
                new_states[key] = new_states.get(key, 0) + cnt
        states = new_states
        total_words = sum(states.values())
        counts_per_length.append((step + 1, len(states), total_words))
        if verbose:
            print(f"  prefix_len={step+1:3d} distinct_edge_states={len(states):8d} total_words={total_words:10d}")
    return states, counts_per_length


def main():
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    print(f"n={n}")
    states, trace = dedup_trace(n)
    print(f"final: distinct_edge_states={len(states)} total_words={sum(states.values())} (expect 2**{n}={2**n})")


if __name__ == "__main__":
    main()

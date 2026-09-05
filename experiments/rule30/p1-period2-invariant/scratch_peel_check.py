#!/usr/bin/env python3
"""Throwaway check: anchored (not 'anywhere') shift test."""
from constant_tail_scale import append_dependency_edge
from rank_zero_separator import hard_core_prefixes

def edge_after(word):
    endpoint = []
    edge = ()
    for value in (0,) * len(word) + tuple(word):
        edge = append_dependency_edge(edge, endpoint[-1] if endpoint else None, value)
        endpoint.append(value)
    return edge

def check(n):
    words = hard_core_prefixes(n)
    total = 0
    prefix_tail_hits = 0
    suffix_prefix_hits = 0
    for w in words:
        if n < 2:
            continue
        w_drop_first = w[1:]
        w_drop_last = w[:-1]
        e_full = edge_after(w)
        e_pf = edge_after(w_drop_first)
        e_sf = edge_after(w_drop_last)
        total += 1
        # anchored: does e_pf equal the exact trailing segment of e_full?
        if e_full[len(e_full)-len(e_pf):] == e_pf:
            prefix_tail_hits += 1
        # anchored: does e_sf equal the exact leading segment of e_full (causal-prefix hope)?
        if e_full[:len(e_sf)] == e_sf:
            suffix_prefix_hits += 1
    return total, prefix_tail_hits, suffix_prefix_hits

for n in range(2, 13):
    total, pt, sp = check(n)
    print(f"n={n:2d} hard-core-words={total:5d} anchored-trailing-match(drop-first)={pt:5d} anchored-leading-match(drop-last)={sp:5d}")

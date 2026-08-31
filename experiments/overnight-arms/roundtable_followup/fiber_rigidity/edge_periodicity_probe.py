"""Measure the width of the exactly-periodic spatial buffer near the right
edge of the lone-seed diagram, for Rule 30 and Rule 90.

This is the spatial analogue of Rowland's *temporal* diagonal periodicity
(RESULTS-diagonal-periodicity.md): instead of asking "is the value at fixed
offset j from the edge eventually periodic in t", we ask "at fixed time t, how
wide is the region near the edge that is exactly periodic in x, right now".

Bit-packed exact simulation, O(T) cells per rule, T up to a few thousand is
instant.
"""
from __future__ import annotations

import sys

RULE_30 = 30
RULE_90 = 90


def evolve_lone_seed(rule: int, steps: int) -> list[int]:
    """Return rows 0..steps of the lone-seed diagram as lists of 0/1, each
    row row[i] trimmed to its exact causal support [-steps, steps] (fixed
    width across all rows, seed at index `steps`)."""
    width = 2 * steps + 1
    mask = (1 << width) - 1
    center = steps
    row = 1 << center
    rows = [row]
    for _ in range(steps):
        left = (row << 1) & mask
        mid = row
        right = row >> 1
        nxt = 0
        for nb in range(8):
            if not ((rule >> nb) & 1):
                continue
            term = mask
            for src, flag in ((left, 4), (mid, 2), (right, 1)):
                term &= src if nb & flag else (~src & mask)
            nxt |= term
        row = nxt & mask
        rows.append(row)
    out = []
    for r in rows:
        out.append([(r >> i) & 1 for i in range(width)])
    return out  # out[t][center+x] = s(t,x)


def max_periodic_suffix_width(cells: list[int], edge_index: int, direction: int,
                               opposite_edge: int,
                               max_period: int = 512) -> tuple[int, int]:
    """cells is the full row (list of 0/1), but only the true causal support
    [left_edge, right_edge] is real signal -- everything outside is padding
    forced to zero by the finite light cone and must be excluded, or any
    period trivially "fits" the padding. edge_index is the index of the edge
    cell (rightmost live cell if direction=-1 scanning leftward, or leftmost
    live cell if direction=+1 scanning rightward); opposite_edge bounds the
    scan so it never reads padding. Returns (best_width, best_period): the
    largest L such that the L cells from the edge inward, still inside the
    true support, are *exactly* periodic with some period <= max_period."""
    if direction == -1:
        span = cells[opposite_edge: edge_index + 1][::-1]  # edge first, going inward
    else:
        span = cells[edge_index: opposite_edge + 1]
    n = len(span)
    best_width, best_period = 0, 0
    for p in range(1, max_period + 1):
        if p > n:
            break
        # width = largest L (multiple check) such that span[i] == span[i-p] for all p<=i<L
        L = p
        for i in range(p, n):
            if span[i] != span[i - p]:
                break
            L = i + 1
        if L < 4 * p:
            continue  # fewer than 4 repeats is not evidence of periodicity
        if L > best_width:
            best_width, best_period = L, p
    return best_width, best_period


def find_edges(row: list[int]) -> tuple[int, int]:
    ones = [i for i, v in enumerate(row) if v]
    if not ones:
        return -1, -1
    return ones[0], ones[-1]


def main() -> None:
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 2048
    ts = [16, 32, 64, 128, 256, 512, 1024, 2048]
    ts = [t for t in ts if t <= steps]
    for rule in (RULE_30, RULE_90):
        print(f"rule {rule}")
        rows = evolve_lone_seed(rule, steps)
        for t in ts:
            row = rows[t]
            left_edge, right_edge = find_edges(row)
            w_right, p_right = max_periodic_suffix_width(row, right_edge, -1, left_edge)
            w_left, p_left = max_periodic_suffix_width(row, left_edge, +1, right_edge)
            print(f"  t={t:5d}  right_buffer_width={w_right:5d} (period {p_right})"
                  f"   left_buffer_width={w_left:5d} (period {p_left})"
                  f"   support_width={right_edge-left_edge+1}")
        print()


if __name__ == "__main__":
    main()

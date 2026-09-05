#!/usr/bin/env python3
"""Fast (sub-exponential in practice) computation of D_k(n), max survival
row, and gamma(n), by deduping on the dependency-edge state that
literal_extension builds internally, instead of brute-force enumerating
all 2^n source words in {1,2}^n.

Key fact used (verified empirically and by construction): the forced
continuation of a source word W, as computed by
late_pull_diagonal_sat.literal_extension, depends on W ONLY through the
pair (edge, endpoint_symbol) that append_dependency_edge has built after
consuming the n zero-padding symbols and then W itself. Two different
words that arrive at an identical (edge, endpoint_symbol) pair after
their n symbols are indistinguishable to every later step: same forced
continuation, same survival depth, same continuation prefixes at every
k. So instead of enumerating all 2^n words and running literal_extension
2^n times, we walk the length-n symbol trie ONE symbol at a time,
grouping (collapsing) branches that reach the same (edge, endpoint)
state, and only then run the forced continuation once per SURVIVING
DISTINCT state.

This changes the source-enumeration cost from O(2^n) to
O(sum_i |distinct states at prefix length i|), which the diagnostic
script fastdk_prototype.py showed grows with an empirical ratio well
below 2 (measured ~1.34-1.6 per extra symbol in the n=16..22 range,
decreasing as n grows), letting us reach much larger n in the same
wall-clock budget.

Correctness is established by exact agreement with the brute-force
continuation_image_analysis.d_k_table at n=8,10,12,14,16 (see
fastdk_crosscheck.py / RESULTS-KSTAR-GAMMA-EXTENDED.md), not by
argument alone.
"""
from __future__ import annotations

from fastdk_fastedge import append_edge_fast as append_dependency_edge


def fib(k: int) -> int:
    a, b = 1, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def _edge_after_zero_padding(n: int):
    edge = ()
    endpoint_sym = None
    for _ in range(n):
        edge = append_dependency_edge(edge, endpoint_sym, 0)
        endpoint_sym = 0
    return edge, endpoint_sym


def distinct_final_states(n: int, *, verbose: bool = False):
    """Walk the {1,2}^n symbol trie, deduping on (edge, endpoint symbol).

    Returns dict {(edge_tuple, endpoint_symbol): count_of_words}.
    """
    zero_edge, zero_endpoint = _edge_after_zero_padding(n)
    states = {(zero_edge, zero_endpoint): 1}
    for step in range(n):
        new_states: dict = {}
        for (edge, endpoint_sym), cnt in states.items():
            for value in (1, 2):
                new_edge = append_dependency_edge(edge, endpoint_sym, value)
                key = (new_edge, value)
                new_states[key] = new_states.get(key, 0) + cnt
        states = new_states
        if verbose:
            print(
                f"  prefix_len={step + 1:3d} distinct_states={len(states):9d} "
                f"total_words={sum(states.values()):12d}",
                flush=True,
            )
    return states


def forced_continuation_from_state(edge, endpoint_sym: int, tail: int, rows: int):
    """Mirror late_pull_diagonal_sat.literal_extension's forced-extension
    loop exactly, but starting from an already-built (edge, endpoint)
    state instead of building it from a literal word. Returns the
    continuation tuple (length <= rows; shorter if a defect/dead-end is
    hit -- mirrors what continuation_image_analysis treats as fail_at)."""
    extension = []
    for _ in range(rows):
        candidates = []
        for value in range(4):
            following = append_dependency_edge(edge, endpoint_sym, value)
            if following[-1] == tail:
                candidates.append((value, following))
        assert len(candidates) == 1, (
            f"expected exactly one forced candidate, got {len(candidates)}"
        )
        value, edge = candidates[0]
        endpoint_sym = value
        extension.append(value)
    return tuple(extension)


def survived_prefix(cont, prev_last_symbol: int):
    """Given a raw forced continuation (values in 0..3, since 0/3 are
    'defect' states in this alphabet) and the last real symbol before it,
    return the length of the hard-core-surviving prefix (fail_at logic
    matching continuation_image_analysis.full_continuations)."""
    prev = prev_last_symbol
    for i, v in enumerate(cont):
        if v not in (1, 2) or (prev == 1 and v == 1):
            return i
        prev = v
    return len(cont)


def d_k_table_fast(n: int, tail: int, residue: int, kmax: int | None = None, *, verbose: bool = False):
    """Fast analogue of continuation_image_analysis.d_k_table.

    Returns (table, kmax, max_survival_row) where table is a list of
    (k, fib(k+1), D_k) tuples, matching the brute-force function's
    output format exactly (images dict omitted -- not needed downstream
    and would reintroduce O(2^n) memory)."""
    target = n + residue
    rows = target + 2
    kmax = kmax or rows

    states = distinct_final_states(n, verbose=verbose)

    # images[k] = set of distinct continuation prefixes of length k among
    # words alive through at least k steps.
    prefix_sets = [set() for _ in range(kmax + 1)]  # index by k, 0 unused
    max_survival = 0
    # We don't have the literal last symbol of W directly from (edge,
    # endpoint) alone... but endpoint_sym IS exactly the last real symbol
    # appended (see distinct_final_states: key=(new_edge, value), value
    # is literally the last source symbol). So prev_last_symbol ==
    # endpoint_sym is exactly right, matching full_continuations' use of
    # w[-1] as `prev`.
    for (edge, endpoint_sym), _cnt in states.items():
        cont = forced_continuation_from_state(edge, endpoint_sym, tail, rows)
        survived = survived_prefix(cont, endpoint_sym)
        max_survival = max(max_survival, survived)
        for k in range(1, min(survived, kmax) + 1):
            prefix_sets[k].add(cont[:k])

    table = []
    for k in range(1, kmax + 1):
        table.append((k, fib(k + 1), len(prefix_sets[k])))
    return table, rows, max_survival


def main():
    import sys

    n = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    tail = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    residue = int(sys.argv[3]) if len(sys.argv) > 3 else 0

    table, rows, max_survival = d_k_table_fast(n, tail, residue, verbose=True)
    print(f"n={n} c={tail} r={residue} rows={rows}")
    print(" k   Fib(k+1)   D_k   surjective?")
    for k, f, d in table:
        print(f"{k:3d}   {f:8d}   {d:5d}   {'yes' if d == f else 'no'}")
    k_star = next((k for k, f, d in table if d < f), None)
    gamma = rows - max_survival
    print(f"\nk_star = {k_star}")
    print(f"max_survival_row = {max_survival} (rows=n+r+2={rows})")
    print(f"gamma(n) = (n+r+2) - max_survival_row = {gamma}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Bytes-backed variant of fastdk_core.d_k_table_fast -- same algorithm
(dedup on (edge, endpoint) state), swapping the edge representation from
tuple-of-int to bytes for lower memory and faster hashing at large state
counts. See fastdk_fastedge_bytes.py for the edge-op equivalence proof.

Correctness gate: fastdk_crosscheck_bytes.py must show exact agreement
with fastdk_core.d_k_table_fast (already itself cross-checked against
brute force through n=18) before this is trusted at n beyond that.
"""
from __future__ import annotations

from fastdk_fastedge_bytes import append_edge_bytes as append_dependency_edge


def fib(k: int) -> int:
    a, b = 1, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def _edge_after_zero_padding(n: int):
    edge = b""
    endpoint_sym = None
    for _ in range(n):
        edge = append_dependency_edge(edge, endpoint_sym, 0)
        endpoint_sym = 0
    return edge, endpoint_sym


def distinct_final_states(n: int, *, verbose: bool = False):
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


def forced_continuation_from_state(edge: bytes, endpoint_sym: int, tail: int, rows: int):
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
    prev = prev_last_symbol
    for i, v in enumerate(cont):
        if v not in (1, 2) or (prev == 1 and v == 1):
            return i
        prev = v
    return len(cont)


def d_k_table_fast(n: int, tail: int, residue: int, kmax: int | None = None, *, verbose: bool = False):
    target = n + residue
    rows = target + 2
    kmax = kmax or rows

    states = distinct_final_states(n, verbose=verbose)

    prefix_sets = [set() for _ in range(kmax + 1)]
    max_survival = 0
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
    import time

    n = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    tail = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    residue = int(sys.argv[3]) if len(sys.argv) > 3 else 0

    t0 = time.perf_counter()
    table, rows, max_survival = d_k_table_fast(n, tail, residue, verbose=True)
    dt = time.perf_counter() - t0
    k_star = next((k for k, f, d in table if d < f), None)
    gamma = rows - max_survival
    print(f"n={n} c={tail} r={residue} time={dt:.2f}s k_star={k_star} max_survival={max_survival} rows={rows} gamma={gamma}")


if __name__ == "__main__":
    main()

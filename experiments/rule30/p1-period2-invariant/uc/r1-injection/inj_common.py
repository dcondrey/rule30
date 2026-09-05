#!/usr/bin/env python3
"""Shared helpers for the triangular-injection lens (uc/r1-injection, round 2).

Everything runs on the validated kernel ``psi_kernel.Endpoint``.  Conventions
follow uc/BRIEF.md section 2: cells are four-state, H = T>>1, Lo = T&1,
E = 1 + H + Lo (mod 2).  The quotient letter of a cell is
    0 -> 'A'  (a=1, b=1)      2 -> 'B'  (a=0, b=1)      1, 3 -> 'C'  (a=0, b=0).

Run from the kernel directory:
    cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-injection/<script>
"""

from __future__ import annotations

import sys
from itertools import product

sys.path.insert(0, ".")
from psi_kernel import Endpoint  # noqa: E402

LETTER = {0: "A", 2: "B", 1: "C", 3: "C"}


def endpoint_of(word) -> Endpoint:
    st = Endpoint()
    for s in word:
        st.append(s)
    return st


def window_cells(st: Endpoint, u: int, n: int) -> list[int]:
    """Cells of column u-1 on depths d in [-u, n-1]; st holds e_0..e_{u-1}."""
    cells = [st.column[u]] + [st.column[k] for k in range(u - 1, 0, -1)] + [
        st.diagonal[k] for k in range(u)
    ]
    return cells[: n + u]


def state_of(word) -> str:
    """Three-letter quotient of column n-1 on [-n, n-1] for a source of length n."""
    n = len(word)
    st = endpoint_of(word)
    return "".join(LETTER[t] for t in window_cells(st, n, n))


def forced_step(st: Endpoint, prev: int, n: int, c: int):
    """(symbol, hit, hardcore_ok, next_state); the H-forced binary symbol always exists."""
    for s in (1, 2):
        col, dia = st.peek(s)
        if dia[n] >> 1 == 1:
            nxt = Endpoint()
            nxt.column, nxt.diagonal, nxt.length = col + [s], dia, st.length + 1
            return s, dia[n] == c, not (prev == 1 and s == 1), nxt
    raise AssertionError("no binary symbol forces the high bit")


def rw_depth(word, c: int, max_len: int | None = None) -> int:
    """Number of consecutive RW hits (E hit and hard-core) of the forced orbit."""
    n = len(word)
    if max_len is None:
        max_len = n + 2
    st = endpoint_of(word)
    prev = word[-1]
    depth = 0
    for _ in range(max_len):
        s, hit, hc, st = forced_step(st, prev, n, c)
        if not (hit and hc):
            break
        depth += 1
        prev = s
    return depth


def rw_depth_and_word(word, c: int, max_len: int | None = None):
    n = len(word)
    if max_len is None:
        max_len = n + 2
    st = endpoint_of(word)
    prev = word[-1]
    depth = 0
    forced = []
    for _ in range(max_len):
        s, hit, hc, st = forced_step(st, prev, n, c)
        forced.append(s)
        if not (hit and hc):
            break
        depth += 1
        prev = s
    return depth, tuple(forced)


def all_depths(n: int, c: int) -> dict[tuple[int, ...], int]:
    """RW depth of every binary source of length n (complete, not sampled)."""
    return {w: rw_depth(w, c) for w in product((1, 2), repeat=n)}


def counts_from_depths(depths: dict, n: int) -> list[int]:
    hist = [0] * (n + 3)
    for d in depths.values():
        hist[d] += 1
    vals = [0] * (n + 3)
    acc = 0
    for k in range(n + 2, -1, -1):
        acc += hist[k]
        vals[k] = acc
    return vals


def validate_against_rw_margin(max_n: int = 9) -> str:
    """Gate: N_k from all_depths equals the recorded rw_counts_pruned values."""
    known = {
        (8, 2): [256, 87, 44, 9, 0, 0, 0, 0, 0, 0, 0],
        (8, 3): [256, 97, 49, 17, 7, 4, 3, 0, 0, 0, 0],
        (9, 2): [512, 162, 57, 17, 4, 0, 0, 0, 0, 0, 0, 0],
        (9, 3): [512, 214, 112, 53, 23, 6, 6, 6, 6, 0, 0, 0],
    }
    for (n, c), ref in known.items():
        if n > max_n:
            continue
        got = counts_from_depths(all_depths(n, c), n)
        assert got == ref, (n, c, got, ref)
    return "inj_common gate: N_k at n=8,9 match rw_counts_pruned_n8-17.log"


if __name__ == "__main__":
    print(validate_against_rw_margin())

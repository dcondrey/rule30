#!/usr/bin/env python3
"""Forced orbit M* on columns: census of hit runs, distinct columns, frozen rows.

Run from the kernel directory:
    cd .../p1-period2-invariant && uv run python uc/r1-potential/orbit_census.py

Coordinates are those of BRIEF.md section 2.  Column ``u`` holds cells
``T[u][d]`` for ``d in [-u-1, u]``; the window relevant to the next column is
``d in [-u-1, n-1]`` (the endpoint symbol plus the states above depth ``n``).
The Moore transducer reads column ``u-1``'s quotient letters
``(a, b) = ([T == 0], [Lo(T) == 0])`` from ``d = -u`` upward with state
``(h, F) = (H, E)``, ``step(h, F, a, b) = (h ^ 1 ^ a, F ^ (h & b))``.

The forced map ``M*``: ``e_u in {1, 2}`` is chosen so that ``H(T[u][n]) = 1``;
a hit at ``u`` means ``T[u][n] = c`` and the hard-core check passes
(``e_u = 1`` after ``e_{u-1} = 1`` is forbidden, junction included).

Everything the script prints is verified against ``psi_kernel.Endpoint`` for
small ``n`` before the census runs.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from itertools import product

sys.path.insert(0, ".")
from psi_kernel import Endpoint  # noqa: E402


def cell(h: int, f: int) -> int:
    return 2 * h + (1 ^ h ^ f)


def hf(t: int) -> tuple[int, int]:
    h = t >> 1
    return h, 1 ^ h ^ (t & 1)


def letter(t: int) -> tuple[int, int]:
    return (1 if t == 0 else 0), (1 if (t & 1) == 0 else 0)


class Column:
    """Column ``u`` restricted to depths ``[-u-1, n]``.

    ``states[i]`` is ``T[u][-u + i]`` for ``i in 0 .. u + n`` (depth ``-u``
    at ``i = 0`` up to depth ``n`` at ``i = u + n``); ``e`` is ``e_u``.
    """

    __slots__ = ("u", "n", "e", "states")

    def __init__(self, u: int, n: int, e: int, states: list[int]) -> None:
        self.u = u
        self.n = n
        self.e = e
        self.states = states

    def letters(self) -> list[tuple[int, int]]:
        """Quotient letters at depths ``-u-1 .. n-1`` (the next column's input)."""
        return [letter(self.e)] + [letter(t) for t in self.states[:-1]]

    def key(self) -> tuple:
        return (self.e, tuple(self.states[:-1]))


def transduce(prev: Column, e: int) -> Column:
    """Column ``u+1`` from column ``u`` and the endpoint symbol ``e = e_{u+1}``."""
    h, f = hf(e ^ 3)
    out = [cell(h, f)]
    for a, b in prev.letters():
        h, f = h ^ 1 ^ a, f ^ (h & b)
        out.append(cell(h, f))
    return Column(prev.u + 1, prev.n, e, out)


def forced_step(prev: Column) -> tuple[int, Column]:
    """Return ``(e_{u+1}, column u+1)`` with ``H(T[u+1][n]) = 1``."""
    trial = transduce(prev, 1)
    if trial.states[-1] >> 1 == 1:
        return 1, trial
    other = transduce(prev, 2)
    assert other.states[-1] >> 1 == 1, "high-bit forcing failed"
    return 2, other


def build_from_prefix(source: tuple[int, ...], n: int) -> Column:
    """Build column ``n-1`` on depths ``[-n, n]`` by full triangle recursion.

    Uses the exact rule ``T[u][d] = phi(T[u-1][d-1], T[u][d-1])`` with the
    virtual left parent ``3`` at the wedge edge, i.e. the same transducer
    with no truncation, so column ``u`` is produced on all its depths.
    """
    prev_states: list[int] = []
    prev_e = 0
    for u, e in enumerate(source):
        h, f = hf(e ^ 3)
        out = [cell(h, f)]
        if u > 0:
            lets = [letter(prev_e)] + [letter(t) for t in prev_states]
            for a, b in lets:
                h, f = h ^ 1 ^ a, f ^ (h & b)
                out.append(cell(h, f))
        prev_states, prev_e = out, e
    # column n-1 has depths -n .. n-1 (2n cells) in prev_states; the window
    # up to depth n needs one more cell, which does not exist in column n-1.
    # The forced step reads only depths -n .. n-1, so store exactly those.
    return Column(len(source) - 1, n, prev_e, prev_states + [None])  # type: ignore


def forced_orbit(source: tuple[int, ...], target: int, max_steps: int):
    """Yield ``(u, e_u, hit, column)`` along the forced orbit from column n-1.

    Stops after the first non-hit or hard-core failure (that column is still
    yielded, with ``hit = False``).
    """
    n = len(source)
    col = build_from_prefix(source, n)
    # states[:-1] are depths -n .. n-1, exactly what transduce() reads.
    prev_e = source[-1]
    for step in range(max_steps):
        e, nxt = forced_step(col)
        hit = nxt.states[-1] == target and not (e == 1 and prev_e == 1)
        yield nxt.u, e, hit, nxt
        if not hit:
            return
        col, prev_e = nxt, e


def verify(max_n: int) -> str:
    """Gate the transducer orbit against psi_kernel.Endpoint."""
    checked = 0
    for n in range(2, max_n + 1):
        for source in product((1, 2), repeat=n):
            ref = Endpoint()
            for s in source:
                ref.append(s)
            prev = source[-1]
            for target in (2, 3):
                ref2 = ref.clone()
                prev2 = prev
                orbit = forced_orbit(source, target, n + 3)
                for u, e, hit, col in orbit:
                    # reference forced symbol
                    chosen = None
                    for sym in (1, 2):
                        _, diag = ref2.peek(sym)
                        if diag[n] >> 1 == 1:
                            assert chosen is None
                            chosen = sym
                    assert chosen == e, (source, target, u, chosen, e)
                    ref2.append(e)
                    # full window comparison: depths -u .. n
                    expect = [ref2.column[k] for k in range(u, 0, -1)] + [
                        ref2.diagonal[k] for k in range(0, n + 1)
                    ]
                    assert col.states == expect, (source, target, u)
                    ref_hit = ref2.diagonal[n] == target and not (e == 1 and prev2 == 1)
                    assert ref_hit == hit
                    prev2 = e
                    checked += 1
    return f"verified {checked} forced columns against psi_kernel.Endpoint"


def census(n: int, target: int, log) -> None:
    max_steps = n + 3
    run_len: Counter = Counter()
    distinct: list[set] = [set() for _ in range(max_steps + 1)]
    survivors = [0] * (max_steps + 1)
    longest: tuple[int, tuple] = (-1, ())
    for source in product((1, 2), repeat=n):
        k = 0
        for u, e, hit, col in forced_orbit(source, target, max_steps):
            if not hit:
                break
            k += 1
            survivors[k] += 1
            distinct[k].add(col.key())
        run_len[k] += 1
        if k > longest[0]:
            longest = (k, source)
    survivors[0] = 2 ** n
    distinct0 = 2 ** n
    print(f"n={n} c={target} deepest={longest[0]} need={n+2} witness={''.join(map(str, longest[1]))}", file=log)
    print("  k  N_k  D_k(distinct next-input windows)  N_k/N_{k-1}  D_k/N_k", file=log)
    for k in range(0, max_steps + 1):
        nk = survivors[k]
        if nk == 0:
            break
        dk = distinct0 if k == 0 else len(distinct[k])
        ratio = nk / survivors[k - 1] if k > 0 else 1.0
        print(f"  {k:2d} {nk:7d} {dk:7d}   {ratio:.3f}   {dk/nk:.3f}", file=log)


def frozen_rows(target: int, rows: int, cols: int, log) -> None:
    """Rows above an infinite hit row, computed bottom-up with G(l, y)."""

    def G(l: int, y: int) -> int:
        hy, ey = hf(y)
        hr = hy ^ 1 ^ (1 if l == 0 else 0)
        er = ey ^ (hr & (1 if (l & 1) == 0 else 0))
        return cell(hr, er)

    print(f"frozen rows above hit row c={target}, left boundary all four values", file=log)
    row = [target] * cols
    for depth in range(1, rows + 1):
        outs = []
        for lb in range(4):
            r = [lb]
            for y in row[1:]:
                r.append(G(r[-1], y))
            outs.append(r)
        # eventual period of each
        desc = []
        for lb, r in enumerate(outs):
            tail = r[cols // 2 :]
            per = next((p for p in range(1, len(tail)) if all(tail[i] == tail[i + p] for i in range(len(tail) - p))), None)
            desc.append(f"lb{lb}:{''.join(map(str, r[:24]))} per={per}")
        print(f"  row n-{depth}: " + " | ".join(desc), file=log)
        # continue with a canonical boundary (lb = the value produced from 1)
        row = outs[1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify-n", type=int, default=8)
    ap.add_argument("--min-n", type=int, default=6)
    ap.add_argument("--max-n", type=int, default=14)
    ap.add_argument("--log", default="uc/r1-potential/orbit_census.log")
    args = ap.parse_args()
    with open(args.log, "w") as log:
        msg = verify(args.verify_n)
        print(msg)
        print(msg, file=log)
        frozen_rows(2, 12, 64, log)
        frozen_rows(3, 12, 64, log)
        for n in range(args.min_n, args.max_n + 1):
            for target in (2, 3):
                census(n, target, log)
                log.flush()
    print(f"log written to {args.log}")


if __name__ == "__main__":
    main()

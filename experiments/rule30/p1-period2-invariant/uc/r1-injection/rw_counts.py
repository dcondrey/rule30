#!/usr/bin/env python3
"""Survivor counts N_k for the rotated wedge under three constraint modes.

For every binary source W in {1,2}^n the forced orbit is run for n+2 columns
(u = n .. 2n+1).  At column u the symbol e_u is the unique binary symbol with
H(T[u][n]) = 1 (kernel: ``Endpoint.peek``); two flags are recorded:

    E_k  = [T[u][n] == c]                      (the E constraint, u = n+k-1)
    HC_k = [not (e_{u-1} == 1 and e_u == 1)]   (hard-core across the junction)

Modes: 'E' keeps sources with E_1..E_k; 'HC' keeps sources with HC_1..HC_k
along the forced orbit (no E constraint); 'RW' keeps both.  N_k(mode) is the
count.  The RW mode reproduces ``rw_margin.py``'s deepest run as
max{k : N_k(RW) > 0}, which is printed as a gate.

Reported per (n, c, mode): N_k, the ratio R_k = N_k / 2^(n-k), and the
least-squares slope of log2 N_k against k over the k with N_k >= 8.

Usage: uv run python uc/r1-injection/rw_counts.py --min 3 --max 14
"""

from __future__ import annotations

import argparse
import math
import sys
from itertools import product

sys.path.insert(0, ".")
from psi_kernel import Endpoint  # noqa: E402


def forced_flags(source: tuple[int, ...], target: int) -> tuple[list[int], list[int], list[int]]:
    """Return (E flags, HC flags, forced symbols) for n+2 forced columns."""
    depth = len(source)
    state = Endpoint()
    for symbol in source:
        state.append(symbol)
    previous = source[-1]
    e_flags: list[int] = []
    hc_flags: list[int] = []
    forced: list[int] = []
    for _ in range(depth + 2):
        chosen = None
        for symbol in (1, 2):
            column, diagonal = state.peek(symbol)
            if diagonal[depth] >> 1 == 1:
                assert chosen is None
                chosen = (symbol, diagonal[depth], column, diagonal)
        assert chosen is not None
        symbol, cell, column, diagonal = chosen
        e_flags.append(1 if cell == target else 0)
        hc_flags.append(0 if (previous == 1 and symbol == 1) else 1)
        forced.append(symbol)
        nxt = Endpoint()
        nxt.column = column + [symbol]
        nxt.diagonal = diagonal
        nxt.length = state.length + 1
        state = nxt
        previous = symbol
    return e_flags, hc_flags, forced


def counts(n: int, target: int) -> dict[str, list[int]]:
    kmax = n + 2
    out = {"E": [0] * (kmax + 1), "HC": [0] * (kmax + 1), "RW": [0] * (kmax + 1)}
    for source in product((1, 2), repeat=n):
        e_flags, hc_flags, _ = forced_flags(source, target)
        alive = {"E": True, "HC": True, "RW": True}
        for mode in out:
            out[mode][0] += 1
        for k in range(1, kmax + 1):
            e, h = e_flags[k - 1], hc_flags[k - 1]
            alive["E"] = alive["E"] and bool(e)
            alive["HC"] = alive["HC"] and bool(h)
            alive["RW"] = alive["RW"] and bool(e) and bool(h)
            for mode in out:
                if alive[mode]:
                    out[mode][k] += 1
    return out


def slope(values: list[int], floor: int = 8) -> float | None:
    pts = [(k, math.log2(v)) for k, v in enumerate(values) if v >= floor]
    if len(pts) < 3:
        return None
    m = len(pts)
    sx = sum(k for k, _ in pts)
    sy = sum(y for _, y in pts)
    sxx = sum(k * k for k, _ in pts)
    sxy = sum(k * y for k, y in pts)
    den = m * sxx - sx * sx
    if den == 0:
        return None
    return (m * sxy - sx * sy) / den


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min", type=int, default=3)
    parser.add_argument("--max", type=int, default=14)
    args = parser.parse_args()

    print("mode  n  c  deepest  maxR(k)  argmaxk  slope(bits/col)   N_k ...")
    for n in range(args.min, args.max + 1):
        for target in (2, 3):
            table = counts(n, target)
            for mode in ("RW", "E", "HC"):
                vals = table[mode]
                deepest = max(k for k, v in enumerate(vals) if v > 0)
                ratios = [v / 2 ** (n - k) for k, v in enumerate(vals)]
                kstar = max(range(len(ratios)), key=lambda k: ratios[k])
                s = slope(vals)
                stxt = f"{s:8.3f}" if s is not None else "     n/a"
                print(
                    f"{mode:<4} {n:>2}  {target}  {deepest:>7}  {ratios[kstar]:7.2f}  "
                    f"{kstar:>7}  {stxt}   {vals}"
                )
        sys.stdout.flush()


if __name__ == "__main__":
    main()

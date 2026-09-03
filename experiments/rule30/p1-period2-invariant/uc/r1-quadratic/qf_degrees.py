#!/usr/bin/env python3
"""Algebraic degrees of the (RW) constraint system in three coordinate systems.

(a) full diagonal coordinates: 2n bits (H(D_u), E(D_u)), all L constraints
    E(e_u) = 0 of the diagonal form;
(b) reduced diagonal coordinates: after the n triangular constraints
    E(e_u) = 0, u < n, are solved for E(D_u), the free bits x_u = H(D_u);
    the remaining constraints E(e_u), u >= n, as functions of x in F2^n;
(c) source coordinates: bits H(e_u), u < n, of the binary source W;
    the same diagonal-form constraints E(e_u), u >= n;
(d) the forced-orbit hits hit_j = E(T[n+j][n]) of the orbit form, in source
    bits and in reduced diagonal bits.

Run:  cd <work dir> && uv run python uc/r1-quadratic/qf_degrees.py
"""

from __future__ import annotations

import argparse
import time
from itertools import product

from qf_common import (
    E,
    anf_degree,
    cell,
    endpoint_of,
    forced_orbit,
    region,
    source_diagonal,
)


def diag_from_bits(bits: int, n: int) -> tuple[int, ...]:
    """bit 2u = H(D_u), bit 2u+1 = E(D_u)."""
    return tuple(cell((bits >> (2 * u)) & 1, (bits >> (2 * u + 1)) & 1) for u in range(n))


def reduced_diag(x: int, n: int, c: int) -> tuple[int, ...]:
    """Solve the triangular constraints: x_u = H(D_u), E(D_u) forced."""
    diag: list[int] = []
    for u in range(n):
        h = (x >> u) & 1
        choice = None
        for f in (0, 1):
            trial = tuple(diag) + (cell(h, f),)
            cols = region(trial, c, u + 1)
            if E(cols[u][-u - 1]) == 0:
                assert choice is None, "triangular constraint not a half-split"
                choice = f
        assert choice is not None
        diag.append(cell(h, choice))
    return tuple(diag)


def source_from_bits(w: int, n: int) -> tuple[int, ...]:
    return tuple(2 if (w >> u) & 1 else 1 for u in range(n))


def part_a(n: int, c: int) -> list[int]:
    L = 2 * n + 2
    size = 1 << (2 * n)
    table = [[0] * size for _ in range(L)]
    for bits in range(size):
        g = endpoint_of(region(diag_from_bits(bits, n), c, L))
        for u in range(L):
            table[u][bits] = E(g[u])
    return [anf_degree(table[u]) for u in range(L)]


def part_b(n: int, c: int) -> tuple[list[int], list[tuple[int, ...]]]:
    L = 2 * n + 2
    size = 1 << n
    table = [[0] * size for _ in range(n + 2)]
    diags = []
    for x in range(size):
        diag = reduced_diag(x, n, c)
        diags.append(diag)
        g = endpoint_of(region(diag, c, L))
        for j in range(n + 2):
            assert all(E(g[u]) == 0 for u in range(n))
            table[j][x] = E(g[n + j])
    return [anf_degree(table[j]) for j in range(n + 2)], diags


def part_c(n: int, c: int) -> list[int]:
    L = 2 * n + 2
    size = 1 << n
    table = [[0] * size for _ in range(n + 2)]
    for w in range(size):
        src = source_from_bits(w, n)
        g = endpoint_of(region(source_diagonal(src), c, L))
        assert g[:n] == src
        for j in range(n + 2):
            table[j][w] = E(g[n + j])
    return [anf_degree(table[j]) for j in range(n + 2)]


def part_d(n: int, c: int, diags: list[tuple[int, ...]]) -> tuple[list[int], list[int]]:
    size = 1 << n
    tab_src = [[0] * size for _ in range(n + 2)]
    tab_x = [[0] * size for _ in range(n + 2)]
    for w in range(size):
        src = source_from_bits(w, n)
        _, hits, _ = forced_orbit(src, n + 2)
        for j in range(n + 2):
            tab_src[j][w] = hits[j] ^ E(c)
    for x in range(size):
        L = 2 * n + 2
        g = endpoint_of(region(diags[x], c, L))
        src = g[:n]
        _, hits, _ = forced_orbit(src, n + 2)
        for j in range(n + 2):
            tab_x[j][x] = hits[j] ^ E(c)
    return (
        [anf_degree(tab_src[j]) for j in range(n + 2)],
        [anf_degree(tab_x[j]) for j in range(n + 2)],
    )


def part_e(n: int, c: int, diags: list[tuple[int, ...]]) -> tuple[list[int], list[int]]:
    """Degrees of the bijection x <-> W (both directions)."""
    size = 1 << n
    L = 2 * n + 2
    w_of_x = [[0] * size for _ in range(n)]
    x_of_w = [[0] * size for _ in range(n)]
    for x in range(size):
        g = endpoint_of(region(diags[x], c, L))
        for u in range(n):
            w_of_x[u][x] = g[u] >> 1
    for w in range(size):
        src = source_from_bits(w, n)
        diag = source_diagonal(src)
        for u in range(n):
            x_of_w[u][w] = diag[u] >> 1
    return [anf_degree(w_of_x[u]) for u in range(n)], [anf_degree(x_of_w[u]) for u in range(n)]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-a", type=int, default=7)
    ap.add_argument("--max-n", type=int, default=12)
    args = ap.parse_args()

    print("(a) full diagonal coordinates, 2n bits; degrees of E(e_u), u = 0..2n+1")
    for n in range(2, args.max_a + 1):
        for c in (2, 3):
            t0 = time.time()
            degs = part_a(n, c)
            print(f"  n={n} c={c} deg E(e_u): {degs}   [{time.time()-t0:.1f}s]")

    print("(b) reduced diagonal bits x (n bits): degrees of E(e_{n+j}), j = 0..n+1")
    print("(c) source bits (n bits): degrees of the same diagonal-form E(e_{n+j})")
    print("(d) forced-orbit hits: degrees in source bits / in reduced diagonal bits")
    print("(e) bijection degrees: W(x) per coordinate / x(W) per coordinate")
    for n in range(2, args.max_n + 1):
        for c in (2, 3):
            t0 = time.time()
            db, diags = part_b(n, c)
            dc = part_c(n, c)
            dd_src, dd_x = part_d(n, c, diags)
            de_w, de_x = part_e(n, c, diags)
            print(f"  n={n} c={c}")
            print(f"    (b) diag-form E(e_n+j) in x:      {db}")
            print(f"    (c) diag-form E(e_n+j) in W:      {dc}")
            print(f"    (d) orbit hits in W:              {dd_src}")
            print(f"    (d) orbit hits in x:              {dd_x}")
            print(f"    (e) deg W_u(x): {de_w}   deg x_u(W): {de_x}   [{time.time()-t0:.1f}s]")


if __name__ == "__main__":
    main()

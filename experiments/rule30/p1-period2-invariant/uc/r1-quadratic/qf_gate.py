#!/usr/bin/env python3
"""Gate for qf_common against psi_kernel: decoupling, Phi, diagonal form.

Run:  cd <work dir> && uv run python uc/r1-quadratic/qf_gate.py
"""

from __future__ import annotations

from itertools import product

from qf_common import (
    E,
    check_decoupling,
    endpoint_of,
    forced_orbit,
    forward_columns,
    phi_form,
    region,
    source_diagonal,
)


def gate_phi(max_n: int) -> int:
    checked = 0
    for n in range(1, max_n + 1):
        for src in product((1, 2), repeat=n):
            symbols, hits, cells = forced_orbit(src, n + 2)
            word = tuple(src) + tuple(symbols)
            cols = forward_columns(word)
            for j in range(n + 2):
                u = n + j
                # column u-1, window d in [-u, n-1]
                val = phi_form(cols[u - 1], -u, n, n)
                assert val == hits[j], (src, j, val, hits[j])
                checked += 1
    return checked


def gate_diagonal(max_n: int) -> tuple[int, int]:
    words_checked = 0
    cells_checked = 0
    for n in range(1, max_n + 1):
        L = 2 * n + 2
        for c in (2, 3):
            seen = set()
            for diag in product(range(4), repeat=n):
                cols = region(diag, c, L)
                g = endpoint_of(cols)
                assert g not in seen
                seen.add(g)
                fcols = forward_columns(g)
                for u in range(L):
                    top = u if u < n else n
                    for d in range(-u - 1, top + 1):
                        assert fcols[u][d] == cols[u][d], (n, c, diag, u, d)
                        cells_checked += 1
                    if u >= n:
                        assert fcols[u][n] == c
                assert source_diagonal(g[:n]) == diag
                words_checked += 1
            assert len(seen) == 4 ** n
    return words_checked, cells_checked


def gate_agreement(max_n: int) -> int:
    """On binary survivors the diagonal form and the forced orbit agree."""
    agreed = 0
    for n in range(1, max_n + 1):
        L = 2 * n + 2
        for c in (2, 3):
            for src in product((1, 2), repeat=n):
                symbols, hits, cells = forced_orbit(src, n + 2)
                diag = source_diagonal(src)
                cols = region(diag, c, L)
                g = endpoint_of(cols)
                assert g[:n] == src
                # the first j+1 hits equal E(c) iff the diagonal-form symbols
                # e_n..e_{n+j} are binary and equal the forced symbols
                for j in range(n + 2):
                    surv = all(h == E(c) for h in hits[: j + 1])
                    if surv:
                        assert g[n + j] == symbols[j], (src, c, j)
                        assert E(g[n + j]) == 0
                    else:
                        break
                agreed += 1
    return agreed


def main() -> None:
    print(f"decoupling of phi and psi: {check_decoupling()} argument pairs PASS")
    print(f"Phi (even/zero form) equals E(T[u][n]) on forced orbits: {gate_phi(8)} checks PASS")
    w, cc = gate_diagonal(5)
    print(f"diagonal form: {w} words, {cc} cells agree with forward kernel; 4^n distinct PASS")
    print(f"diagonal form vs forced orbit on survivors: {gate_agreement(8)} sources PASS")


if __name__ == "__main__":
    main()

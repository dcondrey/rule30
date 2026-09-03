#!/usr/bin/env python3
"""Shared helpers for the quadratic-form lens on (RW).

Everything here is derived from the four-state rule ``phi = CONE[l][r]`` of
``psi_kernel.py``; nothing is trusted without a gate against that kernel.

Coordinates.  A cell ``T`` in ``{0,1,2,3}`` has ``H = T >> 1``,
``Lo = T & 1``, ``E = 1 + H + Lo mod 2``.  The pair ``(h, F) = (H, E)`` is the
Moore state; ``T = 2h + ((1 + h + F) & 1)``.  Quotient letters of a cell are
``a = [T == 0]`` and ``b = [Lo == 0]``.

Backward rule.  ``psi(l, s)`` is the unique ``r`` with ``phi(l, r) = s``:

    H(r) = H(s) + 1 + a(l)
    E(r) = E(s) + b(l) H(s) + b(l) + a(l)

Diagonal form.  Given ``D in {0..3}^n`` and ``c in {2,3}``, the triangle with
``T[u][u] = D_u`` (``u < n``), ``T[u][n] = c`` (``u >= n``) and
``T[u][d] = psi(T[u-1][d], T[u][d+1])`` (virtual left parent ``3`` when
column ``u-1`` has no cell at depth ``d``) is the unique word ``g`` of length
``L`` with ``P^n(I(g)) = c^(L-n)`` and that diagonal.  ``e_u = T[u][-u-1]``.
"""

from __future__ import annotations

import os
import sys

WORK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if WORK not in sys.path:
    sys.path.insert(0, WORK)

from psi_kernel import CONE, Endpoint  # noqa: E402


def H(t: int) -> int:
    return t >> 1


def Lo(t: int) -> int:
    return t & 1


def E(t: int) -> int:
    return (1 + (t >> 1) + (t & 1)) & 1


def cell(h: int, f: int) -> int:
    return 2 * h + ((1 + h + f) & 1)


def a_letter(t: int) -> int:
    return 1 if t == 0 else 0


def b_letter(t: int) -> int:
    return 1 - (t & 1)


def phi(left: int, right: int) -> int:
    return CONE[left][right]


def _build_psi() -> tuple[tuple[int, ...], ...]:
    table = []
    for left in range(4):
        row = [None] * 4
        for right in range(4):
            s = CONE[left][right]
            assert row[s] is None, "phi not injective in right argument"
            row[s] = right
        table.append(tuple(row))
    return tuple(table)


PSI = _build_psi()


def psi(left: int, above: int) -> int:
    return PSI[left][above]


def check_decoupling() -> int:
    """Exhaustive check of the (H, E) decoupling of phi and of psi."""
    checked = 0
    for left in range(4):
        for right in range(4):
            s = phi(left, right)
            assert H(s) == (H(right) + 1 + a_letter(left)) & 1
            assert E(s) == (E(right) + H(right) * b_letter(left)) & 1
            r = psi(left, s)
            assert r == right
            assert H(r) == (H(s) + 1 + a_letter(left)) & 1
            assert E(r) == (
                E(s) + b_letter(left) * H(s) + b_letter(left) + a_letter(left)
            ) & 1
            checked += 1
    return checked


def region(diag: tuple[int, ...], c: int, length: int) -> list[dict[int, int]]:
    """Columns ``T[u]`` (dict depth -> cell) of the diagonal-form triangle.

    ``diag`` has length ``n``; columns ``u < n`` are topped by ``diag[u]`` at
    depth ``u``, columns ``u >= n`` by ``c`` at depth ``n``.  Returns
    ``length`` columns.
    """
    n = len(diag)
    cols: list[dict[int, int]] = []
    for u in range(length):
        top = u if u < n else n
        col: dict[int, int] = {top: diag[u] if u < n else c}
        prev = cols[u - 1] if u >= 1 else None
        for d in range(top - 1, -u - 2, -1):
            left = prev[d] if (prev is not None and d in prev) else 3
            col[d] = psi(left, col[d + 1])
        cols.append(col)
    return cols


def endpoint_of(cols: list[dict[int, int]]) -> tuple[int, ...]:
    return tuple(cols[u][-u - 1] for u in range(len(cols)))


def forward_columns(word: tuple[int, ...]) -> list[dict[int, int]]:
    """Columns ``T[u][d]`` for ``d in [-u-1, u]`` from the forward kernel."""
    ep = Endpoint()
    cols = []
    for u, s in enumerate(word):
        ep.append(s)
        col = {}
        for i, t in enumerate(ep.column):
            col[-i] = t
        for k, t in enumerate(ep.diagonal):
            col[k] = t
        cols.append(col)
    return cols


def source_diagonal(word: tuple[int, ...]) -> tuple[int, ...]:
    """``(T[0][0], ..., T[n-1][n-1])`` of a word of length ``n``."""
    cols = forward_columns(word)
    return tuple(cols[u][u] for u in range(len(word)))


def forced_orbit(source: tuple[int, ...], count: int) -> tuple[list[int], list[int], list[int]]:
    """Forced binary continuation of ``source`` for ``count`` steps.

    Returns ``(symbols, hits, cells)`` where ``hits[j] = E(T[n+j][n])`` and
    ``cells[j] = T[n+j][n]``.
    """
    n = len(source)
    ep = Endpoint()
    for s in source:
        ep.append(s)
    symbols, hits, cells = [], [], []
    for _ in range(count):
        chosen = None
        for s in (1, 2):
            _, cand = ep.peek(s)
            if cand[n] >> 1 == 1:
                assert chosen is None
                chosen = (s, cand[n])
        assert chosen is not None
        s, t = chosen
        ep.append(s)
        symbols.append(s)
        hits.append(E(t))
        cells.append(t)
    return symbols, hits, cells


def phi_form(col: dict[int, int], lo: int, hi: int, n: int) -> int:
    """Phi over the window ``d in [lo, hi)`` of a column, in the form

        Phi = sum_d (1 + n - d) b_d  +  sum_d a_d (1 + #even cells below d)

    which equals the BRIEF's primed form (see the erratum there).
    """
    total = 0
    evens_below = 0
    for d in range(lo, hi):
        t = col[d]
        b = b_letter(t)
        a = a_letter(t)
        total ^= ((1 + n - d) & 1) & b
        total ^= a & ((1 + evens_below) & 1)
        evens_below += b
    return total


def moebius(values: list[int]) -> list[int]:
    coeff = values[:]
    step = 1
    while step < len(coeff):
        for block in range(0, len(coeff), step * 2):
            for i in range(block, block + step):
                coeff[i + step] ^= coeff[i]
        step *= 2
    return coeff


def anf_degree(values: list[int]) -> int:
    anf = moebius(values)
    return max((bin(m).count("1") for m in range(len(anf)) if anf[m]), default=-1)


def anf_monomials(values: list[int]) -> list[int]:
    anf = moebius(values)
    return [m for m in range(len(anf)) if anf[m]]

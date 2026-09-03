#!/usr/bin/env python3
"""Incremental O(L) endpoint-append kernel for the binary-wedge defect word.

The reference pipeline in ``binary_wedge_high_elimination.py`` recomputes
``peel_power(inverse_terminal_cone(endpoint), depth)`` from scratch for every
appended symbol, which costs ``O(L^2)`` per append and ``O(n^3)`` per binary
source.  This module keeps two columns of state and updates both in ``O(L)``.

Derivation, stated so the code can be checked against it rather than trusted:

``inverse_terminal_cone`` runs ``unfeed(p, 3, layer)`` for ``layer`` from
``L-1`` down to ``0``.  One such pass is exactly

```text
    p'[i] = p[i]                        i < layer
    p'[layer] = BOUNDARY[p[layer]]
    p'[i] = cone_local(p[i-1], p[i])    i > layer
```

because ``unfeed`` advances its symbol from the *old* array, and
``cone_local(l, r) = INVERSE[swap(l)][r]``.  Writing ``B[k][i]`` for the value
at position ``i`` after the pass at ``layer = k``, positions below the pass
index are untouched, so ``B[k+1][j] = endpoint[j]`` for ``j <= k`` and

```text
    B[k][k] = BOUNDARY[endpoint[k]]
    B[k][i] = cone_local(B[k+1][i-1], B[k+1][i])     i > k
```

with ``B[k+1][k]`` read as ``endpoint[k]``.  Hence ``B`` is triangular: column
``i`` depends only on ``endpoint[:i+1]``, so appending a symbol leaves every
earlier column fixed and only adds one new column, computable from the stored
previous column in ``O(L)``.  ``inverse_terminal_cone(endpoint)[i] = B[0][i]``.

The wedge at fixed depth is prefix-stable for the same reason, so the
anti-diagonal ``v[k] = wedge(endpoint, k)[-1]`` updates by

```text
    a[0] = B[0][L]
    a[k+1] = cone_local(v[k], a[k])
```

Every claim above is checked against the reference implementation by
``validate()``; nothing here is used before that gate passes.
"""

from __future__ import annotations

import argparse
from itertools import product


State = int
Vector = tuple[int, ...]


def _swap(state: State) -> State:
    return 2 * (state & 1) + (state >> 1)


def _carry_action(symbol: State, state: State) -> State:
    a, b = symbol >> 1, symbol & 1
    c, d = state >> 1, state & 1
    return 2 * (c ^ (a | b)) + (d ^ (c | a))


FORWARD = tuple(
    tuple(_carry_action(symbol, state) for state in range(4)) for symbol in range(4)
)


def _invert(transform: tuple[int, ...]) -> tuple[int, ...]:
    inverse = [0] * 4
    for state, following in enumerate(transform):
        inverse[following] = state
    return tuple(inverse)


INVERSE = tuple(map(_invert, FORWARD))
BOUNDARY = INVERSE[3]

# CONE[l][r] = cone_local(l, r) = INVERSE[swap(l)][r]
CONE = tuple(tuple(INVERSE[_swap(left)][right] for right in range(4)) for left in range(4))


class Endpoint:
    """Endpoint prefix carrying the two columns needed to append in O(L)."""

    __slots__ = ("column", "diagonal", "length")

    def __init__(self) -> None:
        self.column: list[int] = []
        self.diagonal: list[int] = []
        self.length = 0

    def clone(self) -> "Endpoint":
        copy = Endpoint()
        copy.column = self.column[:]
        copy.diagonal = self.diagonal[:]
        copy.length = self.length
        return copy

    def peek(self, symbol: State) -> tuple[list[int], list[int]]:
        """Return the new column and anti-diagonal appending ``symbol`` gives."""
        length = self.length
        column = self.column
        new_column = [0] * (length + 1)
        new_column[length] = BOUNDARY[symbol]
        for index in range(length - 1, -1, -1):
            new_column[index] = CONE[column[index + 1]][new_column[index + 1]]
        diagonal = self.diagonal
        new_diagonal = [0] * (length + 1)
        new_diagonal[0] = new_column[0]
        for index in range(length):
            new_diagonal[index + 1] = CONE[diagonal[index]][new_diagonal[index]]
        return new_column, new_diagonal

    def append(self, symbol: State) -> None:
        new_column, new_diagonal = self.peek(symbol)
        self.column = new_column + [symbol]
        self.diagonal = new_diagonal
        self.length += 1

    def wedge_last(self, depth: int) -> State:
        """``wedge(endpoint, depth)[-1]``; requires ``depth < length``."""
        return self.diagonal[depth]


def psi(source: Vector) -> tuple[Vector, Vector]:
    """Return ``(Q_n(W), Psi_n(W))`` for a binary source ``W`` in ``{1,2}^n``.

    ``Q_n`` is the unique binary continuation of length ``n+2`` forcing every
    newly exposed depth-``n`` output to have high bit one; ``Psi_n`` is the
    resulting defect word ``1 + H + L``, which under the forced high bit is
    just the low bit.
    """
    depth = len(source)
    endpoint = Endpoint()
    for symbol in source:
        endpoint.append(symbol)
    continuation: list[int] = []
    defect: list[int] = []
    for _ in range(depth + 2):
        chosen = None
        for symbol in (1, 2):
            _, candidate = endpoint.peek(symbol)
            if candidate[depth] >> 1 == 1:
                assert chosen is None, "high-bit forcing is not unique"
                chosen = (symbol, candidate[depth])
        assert chosen is not None, "no binary symbol forces the high bit"
        symbol, cell = chosen
        endpoint.append(symbol)
        continuation.append(symbol)
        defect.append(cell & 1)
    return tuple(continuation), tuple(defect)


def validate(max_source: int = 8) -> str:
    """Gate this kernel against the reference pipeline. Raises on mismatch."""
    from binary_wedge_high_elimination import force_high_one, wedge

    checked = 0
    for length in range(1, max_source + 1):
        for source in product((1, 2), repeat=length):
            reference = force_high_one(source, length + 2)
            mine = psi(source)
            assert mine == reference, (source, mine, reference)
            checked += 1

    # Full anti-diagonal agreement on arbitrary four-state endpoints, which
    # exercises the column recurrence outside the binary/hard-core domain.
    diagonals = 0
    for length in range(1, 8):
        for endpoint in product(range(4), repeat=length):
            state = Endpoint()
            for symbol in endpoint:
                state.append(symbol)
            expected = tuple(wedge(endpoint, depth)[-1] for depth in range(length))
            assert tuple(state.diagonal) == expected, (endpoint, state.diagonal, expected)
            diagonals += 1

    # The recorded n=15 falsifier of the sharp bound.
    source = tuple(map(int, "111122211212112"))
    continuation, defect = psi(source)
    assert continuation == tuple(map(int, "12211111122111211")), continuation
    assert defect == (1,) * 16 + (0,), defect
    return (
        f"psi kernel: {checked} binary sources and {diagonals} four-state endpoints "
        f"agree with the reference; n=15 falsifier reproduced"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-source", type=int, default=8)
    args = parser.parse_args()
    print(validate(args.max_source))


if __name__ == "__main__":
    main()

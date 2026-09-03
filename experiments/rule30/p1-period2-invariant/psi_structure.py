#!/usr/bin/env python3
"""Structure probe for the binary-wedge defect word ``Psi``.

Two independent things are measured here, both against exact enumeration.

**1. Local identities in ``(H, E)`` coordinates.**  Writing ``E = 1+H+L`` and
``phi(L, R) = cone_local(L, R)``, the claim is that the four-state peel rule
collapses to two *decoupled* parity accumulations:

```text
    H(phi(L, R)) = H(R) + 1 + [L == 0]
    E(phi(L, R)) = E(R) + [H(R) == 1] * [Lo(L) == 0]
```

where ``Lo`` is the low bit.  If true, then along a fixed endpoint column ``u``
of the peel triangle, ``H`` and ``E`` are prefix parities of indicator sums
over the *previous* column, which is the "ordered ancestry of the E defect"
the proof-state capsule names as the likely proof object.  ``identities()``
checks all 16 argument pairs, so the check is exhaustive, not sampled.

**2. The resolution the census actually demands.**  ``(PSI)`` says the defect
word ``Psi_n(W)`` of length ``n+2`` is nonconstant, equivalently that
``Delta_j = Psi_j + Psi_{j+1}`` contains a ``1``.  The recorded ``n=15``
falsifier of the sharper bound has ``Psi = 1^16 0``, so its first ``1`` in
``Delta`` sits at the last available index ``j = n``.  ``census()`` reports,
for each ``n``, the largest first-``1`` index over all binary sources.  Any
candidate lemma that cannot separate ``Delta = 0^{n+1}`` from
``Delta = 0^n 1`` is not a proof of ``(PSI)``; this fixes that margin as a
measured number rather than an impression from one witness.
"""

from __future__ import annotations

import argparse
from itertools import product

from psi_kernel import CONE, Endpoint, psi


def high(state: int) -> int:
    return state >> 1


def low(state: int) -> int:
    return state & 1


def defect(state: int) -> int:
    return 1 ^ high(state) ^ low(state)


def identities() -> str:
    """Exhaustively check the two ``(H, E)`` accumulation laws."""
    for left in range(4):
        for right in range(4):
            out = CONE[left][right]
            assert high(out) == high(right) ^ 1 ^ (left == 0), (left, right)
            assert defect(out) == defect(right) ^ (high(right) & (low(left) ^ 1)), (
                left,
                right,
            )
    return "H and E accumulation laws: 16/16 argument pairs PASS"


def column_laws(max_endpoint: int) -> str:
    """Check the prefix-parity form of the laws down a whole peel column.

    For endpoint index ``u`` and depth ``d``, with ``col_u(d) = T[u][d]``:

    ```text
        H(T[u][d]) = H(T[u][0]) + d + #{d' < d : T[u-1][d'] == 0}
        E(T[u][d]) = E(T[u][0]) + #{d' < d : H(T[u][d']) & ~Lo(T[u-1][d'])}
    ```
    """
    checked = 0
    for length in range(2, max_endpoint + 1):
        for endpoint in product(range(4), repeat=length):
            columns = []
            state = Endpoint()
            for symbol in endpoint:
                state.append(symbol)
                columns.append(list(state.diagonal))
            for u in range(1, length):
                previous, current = columns[u - 1], columns[u]
                zeros = 0
                flips = 0
                for d in range(len(previous)):
                    assert high(current[d]) == high(current[0]) ^ (d & 1) ^ zeros, (
                        endpoint,
                        u,
                        d,
                    )
                    assert defect(current[d]) == defect(current[0]) ^ flips, (
                        endpoint,
                        u,
                        d,
                    )
                    flips ^= high(current[d]) & (low(previous[d]) ^ 1)
                    zeros ^= previous[d] == 0
                checked += 1
    return f"column prefix-parity laws: {checked} columns PASS"


def census(max_source: int) -> list[tuple[int, int, int, str]]:
    """Per ``n``: the largest first-``1`` index in ``Delta``, and a witness."""
    rows = []
    for length in range(1, max_source + 1):
        best = -1
        witness = ""
        constant = 0
        for source in product((1, 2), repeat=length):
            _, word = psi(source)
            first = next(
                (j for j in range(len(word) - 1) if word[j] != word[j + 1]),
                None,
            )
            if first is None:
                constant += 1
                first = len(word) - 1
            if first > best:
                best = first
                witness = "".join(map(str, source))
        rows.append((length, best, constant, witness))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-endpoint", type=int, default=6)
    parser.add_argument("--max-source", type=int, default=14)
    args = parser.parse_args()

    print(identities())
    print(column_laws(args.max_endpoint))
    print()
    print("n  maxfirst  limit  constant  witness")
    for length, best, constant, witness in census(args.max_source):
        print(f"{length:<3}{best:<10}{length:<7}{constant:<10}{witness}")


if __name__ == "__main__":
    main()

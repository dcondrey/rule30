#!/usr/bin/env python3
"""Is the forced continuation an autonomous map on peel columns?

Background.  ``psi_structure.py`` establishes exhaustively that the four-state
peel rule ``phi`` decouples in ``(H, E)`` coordinates:

```text
    H(phi(L, R)) = H(R) + 1 + [L == 0]
    E(phi(L, R)) = E(R) + H(R) * (1 + Lo(L))
```

Down a fixed endpoint column ``u`` these integrate to prefix parities over the
*previous* column ``u-1``.  Imposing the binary wedge's high-bit forcing
``H(T[u][n]) = 1`` removes the free constant from the ``H`` integral and
leaves a closed form with no free parameter at all:

```text
    H(T[u][d]) = 1 + ((n - d) mod 2) + #{d' in [d, n) : T[u-1][d'] == 0}   (H)
```

so the whole ``H`` profile of column ``u`` is a function of where column
``u-1`` takes the value ``0``.  The ``E`` integral keeps one free constant,
``E(T[u][0])``:

```text
    E(T[u][d]) = E(T[u][0]) + #{d' < d : H(T[u][d']) & ~Lo(T[u-1][d'])}    (E)
```

This module tests the three consequences that matter, all by exact
enumeration against the validated kernel:

1. ``(H)`` and ``(E)`` hold on every forced continuation column.
2. Whether ``E(T[u][0])`` is itself a function of column ``u-1``, i.e.
   whether ``col_{u-1} -> col_u`` is a deterministic autonomous map.  If it
   is, the forced continuation is an orbit of one map and ``(PSI)`` is a
   read-out statement about that orbit rather than a statement about
   ``2^n`` independent sources.
3. The extremal family: the sources whose ``Delta`` first turns ``1`` at the
   last available index, which the census shows is attained.
"""

from __future__ import annotations

import argparse
from itertools import product

from psi_kernel import Endpoint, psi


def high(state: int) -> int:
    return state >> 1


def low(state: int) -> int:
    return state & 1


def defect(state: int) -> int:
    return 1 ^ (state >> 1) ^ (state & 1)


def forced_columns(source: tuple[int, ...]) -> list[list[int]]:
    """Columns ``T[u][0..n]`` for ``u = n-1 .. 2n+1`` along the forced run.

    Index ``0`` of the returned list is the last source column, which is the
    first column deep enough to read depth ``n``; the remaining ``n+2``
    entries are the forced continuation columns.
    """
    depth = len(source)
    endpoint = Endpoint()
    for symbol in source:
        endpoint.append(symbol)
    columns = [list(endpoint.diagonal)]
    for _ in range(depth + 2):
        chosen = None
        for symbol in (1, 2):
            _, candidate = endpoint.peek(symbol)
            if candidate[depth] >> 1 == 1:
                assert chosen is None
                chosen = symbol
        assert chosen is not None
        endpoint.append(chosen)
        columns.append(list(endpoint.diagonal))
    return columns


def check_integrals(max_source: int) -> str:
    """Verify ``(H)`` and ``(E)`` on every forced continuation column."""
    checked = 0
    for length in range(1, max_source + 1):
        for source in product((1, 2), repeat=length):
            columns = forced_columns(source)
            for index in range(1, len(columns)):
                previous, current = columns[index - 1], columns[index]
                # (H): closed form, no free parameter.
                for d in range(length + 1):
                    zeros = sum(previous[k] == 0 for k in range(d, length)) & 1
                    expected = 1 ^ ((length - d) & 1) ^ zeros
                    assert high(current[d]) == expected, (source, index, d)
                # (E): one free constant, taken from depth 0.
                flips = 0
                for d in range(length + 1):
                    assert defect(current[d]) == defect(current[0]) ^ flips, (
                        source,
                        index,
                        d,
                    )
                    if d < len(previous):
                        flips ^= high(current[d]) & (low(previous[d]) ^ 1)
                checked += 1
    return f"forced-column integrals (H) and (E): {checked} columns PASS"


def autonomy(max_source: int) -> tuple[int, int, list[str], list[str]]:
    """Does ``col_{u-1}[0..n]`` determine ``col_u[0..n]`` on forced runs?

    Collects every observed ``(previous, current)`` pair and reports whether
    any ``previous`` maps to two different ``current`` values.
    """
    table: dict[tuple[int, ...], tuple[int, ...]] = {}
    seed_table: dict[tuple[int, ...], int] = {}
    conflicts: list[str] = []
    seed_conflicts: list[str] = []
    pairs = 0
    for length in range(1, max_source + 1):
        for source in product((1, 2), repeat=length):
            columns = forced_columns(source)
            for index in range(2, len(columns)):
                # Key on n as well: columns of different n are different states.
                key = (length,) + tuple(columns[index - 1][: length + 1])
                value = tuple(columns[index][: length + 1])
                pairs += 1
                seen = table.get(key)
                if seen is None:
                    table[key] = value
                elif seen != value and len(conflicts) < 3:
                    conflicts.append(f"n={length} {key[1:]} -> {seen} and {value}")
                # The only unresolved bit is the seed defect E(T[u][0]).
                seed = defect(columns[index][0])
                prior = seed_table.get(key)
                if prior is None:
                    seed_table[key] = seed
                elif prior != seed and len(seed_conflicts) < 3:
                    seed_conflicts.append(f"n={length} {key[1:]} -> seed {prior} and {seed}")
    return pairs, len(table), conflicts, seed_conflicts


def extremal(length: int) -> tuple[int, list[str]]:
    """Sources whose ``Delta`` first turns ``1`` at the largest index."""
    best = -1
    witnesses: list[str] = []
    for source in product((1, 2), repeat=length):
        _, word = psi(source)
        first = next(
            (j for j in range(len(word) - 1) if word[j] != word[j + 1]), len(word) - 1
        )
        if first > best:
            best, witnesses = first, []
        if first == best:
            witnesses.append("".join(map(str, source)))
    return best, witnesses


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-source", type=int, default=10)
    parser.add_argument("--extremal", type=int, nargs="*", default=[15])
    args = parser.parse_args()

    print(check_integrals(args.max_source))
    pairs, distinct, conflicts, seed_conflicts = autonomy(args.max_source)
    verdict = "DETERMINISTIC" if not conflicts else "NOT a function"
    print(f"column map: {pairs} transitions, {distinct} distinct sources, {verdict}")
    for line in conflicts:
        print(f"  conflict {line}")
    seed_verdict = "DETERMINED" if not seed_conflicts else "NOT determined"
    print(f"seed defect E(T[u][0]) from column u-1: {seed_verdict}")
    for line in seed_conflicts:
        print(f"  conflict {line}")
    for length in args.extremal:
        best, witnesses = extremal(length)
        print(f"\nn={length} extremal first-1 index {best} ({len(witnesses)} sources)")
        for witness in witnesses:
            print(f"  {witness}")


if __name__ == "__main__":
    main()

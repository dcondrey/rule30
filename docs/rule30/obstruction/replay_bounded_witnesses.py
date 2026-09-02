#!/usr/bin/env python3
"""Replay the finite alpha-support and endpoint-residual certificates.

This file contains no search.  It checks two fixed certificates used by
BOUNDED-CERTIFICATE-OBSTRUCTIONS.md:

* ``alpha`` checks the minimal diagonal-token counterexample and a fixed
  distance-27 alpha-support witness;
* ``residual`` constructs the exact finite-horizon Myhill--Nerode partition
  for the binary output of the endpoint morph F=T P I.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENT = ROOT / "experiments/rule30/p1-period2-invariant"
sys.path.insert(0, str(EXPERIMENT))

from constant_tail_pull_row_projected_support import scenario_extension  # noqa: E402
from constant_tail_right_zero_prefix_selector import (  # noqa: E402
    SELECTED_COORDINATES,
)
from constant_tail_zero_prefix_bitsliced import (  # noqa: E402
    adjacent_scenarios_differ,
)
from dyadic_periodicity_analyzer import (  # noqa: E402
    cone_local,
    inverse_cone_diagonal,
    terminal_cone,
)


DIAGONAL_WORD = tuple(map(int, "122221"))
LONG_WORD = tuple(
    map(
        int,
        "122122122212222212221222121222212222122222122212"
        "222122222122222122212221212212122212122212221221",
    )
)
EXPECTED_LONG_ALPHA_SUPPORT = (
    27,
    28,
    29,
    31,
    34,
    35,
    36,
    37,
    38,
    39,
    42,
    43,
    44,
    45,
    46,
    48,
    53,
    54,
    56,
    57,
    58,
    59,
    61,
    62,
    65,
    67,
    68,
    69,
    70,
    74,
    75,
    76,
    77,
    79,
    82,
    83,
    84,
    86,
    88,
    92,
)


def support(word: tuple[int, ...], tail: int, row: int, coordinate: int) -> tuple[int, ...]:
    _extension, affines, _survival = scenario_extension(word, tail)
    return tuple(
        token
        for token in range(len(word))
        if adjacent_scenarios_differ(affines[row][coordinate], token)
    )


def replay_alpha() -> None:
    extension, _affines, survival = scenario_extension(DIAGONAL_WORD, 3)
    assert survival == 2
    assert DIAGONAL_WORD[-1] == 1 and extension[0] == 2
    alpha = support(DIAGONAL_WORD, 3, 0, 0)
    projected = tuple(
        token
        for token in range(len(DIAGONAL_WORD))
        if any(
            token in support(DIAGONAL_WORD, 3, 0, coordinate)
            for coordinate in SELECTED_COORDINATES[3]
        )
    )
    assert alpha == (2, 4)
    assert projected == (2, 4, 5)
    assert 0 not in alpha

    extension, _affines, survival = scenario_extension(LONG_WORD, 2)
    assert len(LONG_WORD) == 96
    assert survival == 2
    assert extension[:3] == (2, 1, 0)
    alpha = support(LONG_WORD, 2, 0, 0)
    assert alpha == EXPECTED_LONG_ALPHA_SUPPORT
    assert alpha[0] == 27

    print(
        "diagonal-token witness: W=122221 tail=3 row=0 "
        "alpha-support=(2,4) projected-support=(2,4,5) PASS"
    )
    print(
        "long-range witness: n=96 tail=2 row=0 survival=2 "
        f"first-alpha-token={alpha[0]} displacement={alpha[0]} PASS"
    )
    print("W=" + "".join(map(str, LONG_WORD)))


def peel(word: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(cone_local(left, right) for left, right in zip(word, word[1:]))


def endpoint_morph(word: tuple[int, ...]) -> tuple[int, ...]:
    """The finite endpoint morph F=T(P(I(word)))."""

    return terminal_cone(peel(inverse_cone_diagonal(word)))


def output_bit(word: tuple[int, ...]) -> int:
    """Binary legality projection of the newest output symbol."""

    return int(endpoint_morph(word)[-1] in (1, 2))


def residual_partition(horizon: int) -> tuple[list[int], str]:
    """Return exact backward residual counts and a canonical digest.

    All words at the terminal horizon have the same continuation class.
    At each earlier prefix p, its signature records, for both next symbols,
    the emitted bit and the continuation class of that child.  Equality of
    signatures is exactly finite-horizon right congruence.
    """

    if horizon < 2:
        raise ValueError("horizon must be at least two")
    words = {
        length: list(itertools.product((1, 2), repeat=length))
        for length in range(1, horizon + 1)
    }
    classes: dict[tuple[int, ...], int] = {
        word: 0 for word in words[horizon]
    }
    counts_descending: list[int] = []
    records: list[str] = []
    for length in range(horizon - 1, 0, -1):
        signatures = {
            prefix: tuple(
                (output_bit(prefix + (symbol,)), classes[prefix + (symbol,)])
                for symbol in (1, 2)
            )
            for prefix in words[length]
        }
        identifiers = {
            signature: index
            for index, signature in enumerate(sorted(set(signatures.values())))
        }
        for prefix in words[length]:
            classes[prefix] = identifiers[signatures[prefix]]
            records.append(
                f"{length}:{''.join(map(str, prefix))}:"
                f"{classes[prefix]}:{signatures[prefix]}"
            )
        counts_descending.append(len(identifiers))
    digest = hashlib.sha256("\n".join(sorted(records)).encode()).hexdigest()
    return list(reversed(counts_descending)), digest


def replay_residual() -> None:
    counts, digest = residual_partition(14)
    expected = [2, 3, 4, 6, 10, 16, 27, 46, 77, 133]
    assert counts[:10] == expected
    print("endpoint-morph finite residual counts, horizon=14:")
    print("depth 1..10:", ",".join(map(str, counts[:10])))
    print(f"canonical-partition-sha256={digest}")
    print("133-state finite-horizon lower bound PASS")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", choices=("alpha", "residual", "all"))
    args = parser.parse_args()
    if args.certificate in ("alpha", "all"):
        replay_alpha()
    if args.certificate in ("residual", "all"):
        replay_residual()


if __name__ == "__main__":
    main()

"""Exact finite-window search for additive conservation laws of an ECA.

For a density ``rho`` on m-bit words and a current ``J`` on (m+1)-bit
words, impose the local continuity equation on every (m+2)-bit word x:

    rho(F(x)[0:m]) - rho(x[1:m+1])
      = J(x[0:m+1]) - J(x[1:m+2]).

This is an integer linear system.  Constants and spatial coboundary densities
are always trivial solutions.  For Rule 30 the rank modulo two reaches the
largest value compatible with those solutions through the requested windows;
because modular rank cannot exceed rational rank, that is an exact certificate
that no additional real/rational additive density exists at those windows.

This probes only additive local conservation laws.  Absence at finite windows
is not a P2 theorem and says nothing about non-additive or unbounded states.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ConservationRecord:
    rule: int
    window: int
    equations: int
    unknowns: int
    rank_mod2: int
    maximum_rank_with_trivial_solutions: int
    mod2_density_projection_dimension: int
    trivial_density_dimension: int
    only_trivial_rational_densities_certified: bool


def local(rule: int, left: int, center: int, right: int) -> int:
    return (rule >> (4 * left + 2 * center + right)) & 1


def word_bits(word: int, width: int) -> list[int]:
    return [(word >> (width - 1 - index)) & 1 for index in range(width)]


def encode(bits: list[int]) -> int:
    answer = 0
    for bit in bits:
        answer = 2 * answer + bit
    return answer


def equation_rows_mod2(rule: int, window: int) -> tuple[list[int], list[int]]:
    """Return full continuity rows and their current-only submatrix rows."""

    density_count = 1 << window
    full_rows = []
    current_rows = []
    for word in range(1 << (window + 2)):
        bits = word_bits(word, window + 2)
        future = [
            local(rule, bits[index], bits[index + 1], bits[index + 2])
            for index in range(window)
        ]
        future_density = encode(future)
        present_density = encode(bits[1:-1])
        left_current = encode(bits[:-1])
        right_current = encode(bits[1:])

        # Minus and plus coincide modulo two.  XOR also correctly cancels a
        # column if the same unknown occurs twice in one equation.
        density_part = (1 << future_density) ^ (1 << present_density)
        current_part = (1 << left_current) ^ (1 << right_current)
        full_rows.append(density_part ^ (current_part << density_count))
        current_rows.append(current_part)
    return full_rows, current_rows


def gf2_rank(rows: list[int]) -> int:
    basis: dict[int, int] = {}
    for original in rows:
        row = original
        while row:
            pivot = row.bit_length() - 1
            if pivot in basis:
                row ^= basis[pivot]
            else:
                basis[pivot] = row
                break
    return len(basis)


def conservation_record(rule: int, window: int) -> ConservationRecord:
    if window < 1:
        raise ValueError("window must be positive")
    density_count = 1 << window
    current_count = 1 << (window + 1)
    full_rows, current_rows = equation_rows_mod2(rule, window)
    full_rank = gf2_rank(full_rows)
    current_rank = gf2_rank(current_rows)

    # Projection of ker([A B]) onto rho has dimension
    # n_rho - rank([A B]) + rank(B), over any field.
    projection_dimension = density_count - full_rank + current_rank
    trivial_dimension = 1 << (window - 1)
    maximum_rank = density_count + current_count - trivial_dimension - 1
    certified = full_rank == maximum_rank
    return ConservationRecord(
        rule=rule,
        window=window,
        equations=1 << (window + 2),
        unknowns=density_count + current_count,
        rank_mod2=full_rank,
        maximum_rank_with_trivial_solutions=maximum_rank,
        mod2_density_projection_dimension=projection_dimension,
        trivial_density_dimension=trivial_dimension,
        only_trivial_rational_densities_certified=certified,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rules", type=int, nargs="+", default=[184, 30])
    parser.add_argument("--max-window", type=int, default=12)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.max_window < 1:
        parser.error("max-window must be positive")

    found = {
        str(rule): [
            conservation_record(rule, window)
            for window in range(1, args.max_window + 1)
        ]
        for rule in args.rules
    }
    if args.json:
        print(
            json.dumps(
                {
                    rule: [asdict(row) for row in records]
                    for rule, records in found.items()
                },
                indent=2,
            )
        )
        return

    print(
        "rule window equations unknowns rank max_rank density_dim "
        "trivial_dim certified"
    )
    for rule in args.rules:
        for row in found[str(rule)]:
            print(
                f"{row.rule:4d} {row.window:6d} {row.equations:9d} "
                f"{row.unknowns:8d} {row.rank_mod2:5d} "
                f"{row.maximum_rank_with_trivial_solutions:8d} "
                f"{row.mod2_density_projection_dimension:11d} "
                f"{row.trivial_density_dimension:11d} "
                f"{str(row.only_trivial_rational_densities_certified):>9s}"
            )


if __name__ == "__main__":
    main()

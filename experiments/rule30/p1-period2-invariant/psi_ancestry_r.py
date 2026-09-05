#!/usr/bin/env python3
"""Setup S1' for PREREGISTRATION-RW-FORCED-TERMINAL-DEFECT.md.

Generalizes ``psi_kernel.psi`` from continuation length ``n+2`` (r=0) to
``n+2+r`` for ``r in {1, 2}``: same H=1-forcing recursion, longer horizon.
At r=0 this is the identical code path as ``psi_kernel.psi`` (control #2
in the prereg's section 5: r=0 output here must match the existing table
in RESULTS-PSI-ANCESTRY-LAW.md section 6 exactly).

Reports, per (n, r), the count of binary sources W in {1,2}^n whose
Psi_{n,r}(W) (defect word of length n+2+r) is constant. Per the prereg,
any nonzero count at n>=7 needs an immediate hard-core+12a-terminal check
(S2), not deferral.
"""

from __future__ import annotations

import argparse
from itertools import product

from psi_kernel import Endpoint, psi as psi_r0


def psi_r(source: tuple[int, ...], r: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    depth = len(source)
    endpoint = Endpoint()
    for symbol in source:
        endpoint.append(symbol)
    continuation: list[int] = []
    defect: list[int] = []
    for _ in range(depth + 2 + r):
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


def check_r0_matches_reference(max_source: int) -> None:
    for length in range(1, max_source + 1):
        for source in product((1, 2), repeat=length):
            assert psi_r(source, 0) == psi_r0(source), (
                "r=0 code path diverges from psi_kernel.psi",
                source,
            )


def census(max_source: int, r: int) -> list[tuple[int, int, str]]:
    rows = []
    for length in range(1, max_source + 1):
        constant = 0
        witness = ""
        for source in product((1, 2), repeat=length):
            _, word = psi_r(source, r)
            is_constant = all(bit == word[0] for bit in word)
            if is_constant:
                constant += 1
                witness = "".join(map(str, source))
        rows.append((length, constant, witness))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-source", type=int, default=17)
    parser.add_argument("--check-r0", type=int, default=9)
    args = parser.parse_args()

    check_r0_matches_reference(args.check_r0)
    print(f"r=0 control: matches psi_kernel.psi exactly through n={args.check_r0}")

    for r in (1, 2):
        print(f"\n--- r={r} (continuation length n+{2 + r}) ---")
        print("n   constant   witness")
        for length, constant, witness in census(args.max_source, r):
            flag = "  <-- n>=7, nonzero: check S2 immediately" if (constant and length >= 7) else ""
            print(f"{length:<3} {constant:<10} {witness}{flag}")


if __name__ == "__main__":
    main()

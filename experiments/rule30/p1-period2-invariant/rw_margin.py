#!/usr/bin/env python3
"""Margin census for the rotated wedge (RW), the DLP-equivalent target.

`RESULTS-PSI-ANCESTRY-LAW.md` section 10 fires the capsule's section 7 switch
criterion: `Delta` has full algebraic degree, so the complete-state recursion
for `(BWH+)` fans out and the program falls back to DLP/RW.  This module
measures RW the way `psi_structure.py` measured `(PSI)`, so the two targets can
be compared on the same axis.

`(RW)` (`RESULTS-DLP-ROTATED-WEDGE.md` section 2): there are no `n >= 1`,
`r in {0,1,2}`, `c in {2,3}` and binary `f` of length `2n+r+2` with

1. `f[n:]` hard-core, including its junction with `f[n-1]`;
2. `P^n(I(f)) = c^(n+r+2)`;
3. `f[-3:-1] = 12`.

Two facts make this cheap where the raw word count `2^(2n+r+2)` is not.
Condition 2 constrains one new output cell per appended symbol from index `n`
onward, and the incremental kernel exposes that cell as `diagonal[n]`; and
condition 1 forbids `11`.  So the continuation is searched as a tree that is
pruned at every level, and the free part is only the `2^n` prefix.

Reported per `(n, r, c)`: the deepest prefix of `c^(n+r+2)` any admissible `f`
achieves, and the slack to the `n+r+2` a counterexample would need.  Slack 0 is
a counterexample to `(RW)` and would refute DLP; the point of the census is the
size of the slack, since `(BWH+)`'s was measured at 1.
"""

from __future__ import annotations

import argparse
from itertools import product

from psi_kernel import Endpoint


def deepest(length: int, pad: int, target: int) -> tuple[int, str]:
    """Deepest run of ``target`` cells reachable, and a witness word."""
    need = length + pad + 2
    best = 0
    witness = ""

    def walk(state: Endpoint, previous: int, word: list[int], depth: int) -> None:
        nonlocal best, witness
        if depth > best:
            # Condition 3 only bites at full depth; report the run regardless,
            # but never count a short word as a counterexample.
            best = depth
            witness = "".join(map(str, word))
        if depth == need:
            return
        for symbol in (1, 2):
            if previous == 1 and symbol == 1:
                continue  # hard-core, including the f[n-1] junction
            column, diagonal = state.peek(symbol)
            if diagonal[length] != target:
                continue
            nxt = Endpoint()
            nxt.column = column + [symbol]
            nxt.diagonal = diagonal
            nxt.length = state.length + 1
            walk(nxt, symbol, word + [symbol], depth + 1)

    for source in product((1, 2), repeat=length):
        state = Endpoint()
        for symbol in source:
            state.append(symbol)
        walk(state, source[-1], list(source), 0)
    return best, witness


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-source", type=int, default=3)
    parser.add_argument("--max-source", type=int, default=14)
    args = parser.parse_args()

    print(" n  r  c   deepest   need   slack   witness")
    for length in range(args.min_source, args.max_source + 1):
        for pad in (0, 1, 2):
            for target in (2, 3):
                need = length + pad + 2
                best, witness = deepest(length, pad, target)
                mark = "  <- RW COUNTEREXAMPLE" if best == need else ""
                print(
                    f"{length:<3}{pad:<3}{target:<4}{best:<10}{need:<7}"
                    f"{need - best:<8}{witness[:44]}{mark}"
                )


if __name__ == "__main__":
    main()

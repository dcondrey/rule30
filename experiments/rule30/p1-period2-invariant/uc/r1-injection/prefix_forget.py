#!/usr/bin/env python3
"""What does the column-(n-1) quotient state forget about the first j source symbols?

For n in a range and j in (2, 3, 4): for every suffix s in {1,2}^(n-j), the
prefixes P in {1,2}^j are partitioned by the state sigma(P s)
(inj_common.state_of).  The partition type is recorded (blocks as sets of
prefix strings) together with the first symbol of s.  Printed per (n, j): the
number of distinct partition types and the most frequent types with counts.
A single dominant type of the form {all P not ending in 11} + singletons (or
similar) is the structure behind the recurring 6-of-8 and 4-of-4 fibres seen in
plateau_fibres_n21-33.log and prefix_fibre_witness_n18c2k3.log.

Usage: cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-injection/prefix_forget.py --min 6 --max 14
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from itertools import product

sys.path.insert(0, "uc/r1-injection")
from inj_common import state_of  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min", type=int, default=6)
    ap.add_argument("--max", type=int, default=14)
    a = ap.parse_args()
    for n in range(a.min, a.max + 1):
        cache = {}
        for w in product((1, 2), repeat=n):
            cache[w] = state_of(w)
        for j in (2, 3, 4):
            types = Counter()
            by_first = {1: Counter(), 2: Counter()}
            for s in product((1, 2), repeat=n - j):
                blocks = {}
                for p in product((1, 2), repeat=j):
                    blocks.setdefault(cache[p + s], []).append("".join(map(str, p)))
                typ = tuple(sorted(tuple(sorted(b)) for b in blocks.values()))
                types[typ] += 1
                by_first[s[0]][typ] += 1
            print(f"n={n} j={j}: {len(types)} partition types over {2 ** (n - j)} suffixes; top 4:")
            for typ, cnt in types.most_common(4):
                sizes = sorted((len(b) for b in typ), reverse=True)
                print(f"    x{cnt:<5} sizes={sizes}  (s[0]=1: {by_first[1][typ]}, s[0]=2: {by_first[2][typ]})  blocks={['|'.join(b) for b in typ if len(b) > 1]}")
        sys.stdout.flush()


if __name__ == "__main__":
    main()

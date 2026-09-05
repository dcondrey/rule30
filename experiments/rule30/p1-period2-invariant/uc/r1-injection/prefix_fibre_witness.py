#!/usr/bin/env python3
"""Exact counterexamples for the prefix-injection lemma (prefix_fibre.py).

For (n, c, k) given on the command line, list every prefix P of length n-k
whose fibre {W in S_k : W[:n-k] = P} has size >= --at-least, with the members
and their forced continuations; re-verify each member's RW depth with
inj_common.rw_depth_and_word.

Usage: cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-injection/prefix_fibre_witness.py --n 18 --c 2 --k 3 --at-least 5
"""

from __future__ import annotations

import argparse
import sys

sys.path.insert(0, "uc/r1-injection")
from inj_common import all_depths, rw_depth_and_word  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--c", type=int, required=True)
    ap.add_argument("--k", type=int, required=True)
    ap.add_argument("--at-least", type=int, default=5)
    a = ap.parse_args()
    n, c, k = a.n, a.c, a.k
    depths = all_depths(n, c)
    fib: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    for w, d in depths.items():
        if d >= k:
            fib.setdefault(w[: n - k], []).append(w)
    big = {p: ws for p, ws in fib.items() if len(ws) >= a.at_least}
    print(f"n={n} c={c} k={k}: N_k={sum(1 for d in depths.values() if d >= k)}, prefixes with fibre >= {a.at_least}: {len(big)}")
    for p, ws in sorted(big.items()):
        print(f"  prefix {''.join(map(str, p))} (length {n - k}) fibre {len(ws)} of {2 ** k} completions:")
        for w in sorted(ws):
            d, forced = rw_depth_and_word(w, c)
            print(f"     W={''.join(map(str, w))}  suffix={''.join(map(str, w[n - k:]))}  depth={d}  forced={''.join(map(str, forced))}")


if __name__ == "__main__":
    main()

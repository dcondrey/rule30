#!/usr/bin/env python3
"""Does a prefix (or suffix) of the source inject the RW survivor set?

For each n, c and k, S_k = {W in {1,2}^n : E_1..E_k and HC_1..HC_k hold}
(RW mode of rw_counts.py).  Two candidate injections are tested:

  prefix:  W -> W[:j]   smallest j with max fibre size 1 on S_k  ("j_pre")
  suffix:  W -> W[n-j:] smallest j with max fibre size 1 on S_k  ("j_suf")

and the max fibre size of the natural candidates W -> W[:n-k] and
W -> W[k:] is printed ("fib_pre", "fib_suf").  If the k-th constraint
determined one new source bit triangularly from the end, j_pre would equal
n - k and fib_pre would be 1; ratios above 1 measure the defect.

Also printed: the influence matrix I[k][j] = Pr_W[E_k(W) != E_k(W xor bit j)]
over all W, for the E flags of the forced orbit (no survivor conditioning),
to see whether any source bit enters any constraint linearly (I = 1).

Usage: uv run python uc/r1-injection/rw_injection_probe.py --min 6 --max 13
"""

from __future__ import annotations

import argparse
import sys
from itertools import product

sys.path.insert(0, ".")
sys.path.insert(0, "uc/r1-injection")
from rw_counts import forced_flags  # noqa: E402


def survivors(n: int, target: int) -> tuple[list[list[tuple[int, ...]]], dict]:
    """S_k for k = 0..n+2 (RW mode) and the raw E flags per source."""
    kmax = n + 2
    sets: list[list[tuple[int, ...]]] = [[] for _ in range(kmax + 1)]
    eflags: dict[tuple[int, ...], list[int]] = {}
    for source in product((1, 2), repeat=n):
        e, h, _ = forced_flags(source, target)
        eflags[source] = e
        sets[0].append(source)
        for k in range(1, kmax + 1):
            if all(e[i] and h[i] for i in range(k)):
                sets[k].append(source)
            else:
                break
    return sets, eflags


def max_fibre(words: list[tuple[int, ...]], key) -> int:
    fibres: dict = {}
    for w in words:
        fibres[key(w)] = fibres.get(key(w), 0) + 1
    return max(fibres.values()) if fibres else 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min", type=int, default=6)
    parser.add_argument("--max", type=int, default=13)
    parser.add_argument("--influence", action="store_true")
    args = parser.parse_args()

    print(" n c  k   N_k  j_pre  j_suf  fib_pre(n-k)  fib_suf(k)")
    for n in range(args.min, args.max + 1):
        for target in (2, 3):
            sets, eflags = survivors(n, target)
            for k in range(0, n + 3):
                words = sets[k]
                if not words:
                    break
                j_pre = next(j for j in range(n + 1) if max_fibre(words, lambda w: w[:j]) == 1)
                j_suf = next(j for j in range(n + 1) if max_fibre(words, lambda w: w[n - j:]) == 1)
                cut = max(n - k, 0)
                fib_pre = max_fibre(words, lambda w: w[:cut])
                fib_suf = max_fibre(words, lambda w: w[min(k, n):])
                print(
                    f"{n:>2} {target}  {k:>2} {len(words):>5}  {j_pre:>5}  {j_suf:>5}  "
                    f"{fib_pre:>12}  {fib_suf:>10}"
                )
            if args.influence:
                print(f"influence I[k][j] for n={n} c={target} (rows k=1..n+2, cols j=0..n-1):")
                for k in range(1, n + 3):
                    row = []
                    for j in range(n):
                        diff = 0
                        for w, e in eflags.items():
                            w2 = list(w)
                            w2[j] = 3 - w2[j]
                            if e[k - 1] != eflags[tuple(w2)][k - 1]:
                                diff += 1
                        row.append(diff / len(eflags))
                    print(f"  k={k:>2}: " + " ".join(f"{x:4.2f}" for x in row))
        sys.stdout.flush()


if __name__ == "__main__":
    main()

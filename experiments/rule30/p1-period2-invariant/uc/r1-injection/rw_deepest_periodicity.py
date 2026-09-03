#!/usr/bin/env python3
"""How close are the deepest RW survivors' forced words to periodic templates?

For each (n, c) collect every source whose admissible run attains the
deepest value D(n, c) (rw_counts_pruned.py), take the forced continuation
Q (length D), and report the Hamming distance from Q to the nearest of the
templates 2^D, (12)^*, (21)^*, (122)^*, (212)^*, (221)^* truncated to
length D, together with the number of distinct forced words and the number
of distinct source suffixes of length 8 among the deepest sources.

Usage: uv run python uc/r1-injection/rw_deepest_periodicity.py --min 8 --max 17
"""

from __future__ import annotations

import argparse
import sys
from itertools import product

sys.path.insert(0, ".")
sys.path.insert(0, "uc/r1-injection")
from rw_counts import forced_flags  # noqa: E402


def run_depth(source: tuple[int, ...], target: int) -> tuple[int, tuple[int, ...]]:
    e, h, forced = forced_flags(source, target)
    depth = 0
    for k in range(len(e)):
        if e[k] and h[k]:
            depth += 1
        else:
            break
    return depth, tuple(forced[:depth])


def template(pattern: tuple[int, ...], length: int) -> tuple[int, ...]:
    return tuple(pattern[i % len(pattern)] for i in range(length))


TEMPLATES = {
    "2^*": (2,),
    "(12)^*": (1, 2),
    "(21)^*": (2, 1),
    "(122)^*": (1, 2, 2),
    "(212)^*": (2, 1, 2),
    "(221)^*": (2, 2, 1),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min", type=int, default=8)
    parser.add_argument("--max", type=int, default=17)
    args = parser.parse_args()
    print(" n c  D  #deepest  #forced_words  #suffix8  nearest template (distance)")
    for n in range(args.min, args.max + 1):
        for target in (2, 3):
            best = -1
            words: dict[tuple[int, ...], int] = {}
            suffixes: set = set()
            for source in product((1, 2), repeat=n):
                depth, forced = run_depth(source, target)
                if depth > best:
                    best, words, suffixes = depth, {}, set()
                if depth == best:
                    words[forced] = words.get(forced, 0) + 1
                    suffixes.add(source[-8:])
            report = []
            for forced in words:
                dist = min(
                    (sum(x != y for x, y in zip(forced, template(pat, best))), name)
                    for name, pat in TEMPLATES.items()
                )
                report.append(f"{''.join(map(str, forced))}~{dist[1]}({dist[0]})x{words[forced]}")
            print(
                f"{n:>2} {target}  {best:>2}  {sum(words.values()):>8}  {len(words):>13}  "
                f"{len(suffixes):>8}  " + "  ".join(report)
            )
            sys.stdout.flush()


if __name__ == "__main__":
    main()

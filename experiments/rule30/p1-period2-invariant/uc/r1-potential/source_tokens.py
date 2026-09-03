#!/usr/bin/env python3
"""Is the hit-run length bounded by a token count of the source W?

For each (n, c) and every W in {1,2}^n, compute k(W) (consecutive hits from
column n, hard-core enforced) and tabulate max k against simple statistics of
W: number of 1s, 2s, factors 11/12/21/22, longest 2-run, longest 1-run, and
the same statistics restricted to the suffix W[n/2:].  For each statistic s
report max over W of k(W) - s(W) per n: a candidate token injection needs this
bounded in n.  Also prints k for the extreme words 1^n and 2^n.

    cd .../p1-period2-invariant && uv run python uc/r1-potential/source_tokens.py
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from itertools import product

sys.path.insert(0, "uc/r1-potential")
sys.path.insert(0, ".")
from orbit_census import forced_orbit  # noqa: E402


def run_length(source: tuple[int, ...], target: int) -> tuple[int, list[int]]:
    k = 0
    endpoints = []
    for u, e, hit, col in forced_orbit(source, target, len(source) + 3):
        if not hit:
            break
        k += 1
        endpoints.append(e)
    return k, endpoints


def wstats(w: tuple[int, ...]) -> dict[str, int]:
    s = "".join(map(str, w))
    n = len(w)
    half = s[n // 2 :]
    def longest(t: str, ch: str) -> int:
        best = cur = 0
        for x in t:
            cur = cur + 1 if x == ch else 0
            best = max(best, cur)
        return best
    out = {
        "ones": s.count("1"),
        "twos": s.count("2"),
        "f11": sum(1 for i in range(n - 1) if s[i : i + 2] == "11"),
        "f12": sum(1 for i in range(n - 1) if s[i : i + 2] == "12"),
        "f21": sum(1 for i in range(n - 1) if s[i : i + 2] == "21"),
        "f22": sum(1 for i in range(n - 1) if s[i : i + 2] == "22"),
        "run2": longest(s, "2"),
        "run1": longest(s, "1"),
        "ones_suffix_half": half.count("1"),
        "twos_suffix_half": half.count("2"),
        "f12_suffix_half": sum(1 for i in range(len(half) - 1) if half[i : i + 2] == "12"),
        "f21_suffix_half": sum(1 for i in range(len(half) - 1) if half[i : i + 2] == "21"),
    }
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-n", type=int, default=6)
    ap.add_argument("--max-n", type=int, default=15)
    ap.add_argument("--log", default="uc/r1-potential/source_tokens.log")
    args = ap.parse_args()
    with open(args.log, "w") as log:
        keys = None
        gaps: dict[tuple[int, int], dict[str, tuple[int, str]]] = {}
        for n in range(args.min_n, args.max_n + 1):
            for target in (2, 3):
                worst: dict[str, tuple[int, str]] = {}
                maxk_by: dict[str, dict[int, int]] = defaultdict(lambda: defaultdict(int))
                ext = {}
                for source in product((1, 2), repeat=n):
                    k, eps = run_length(source, target)
                    st = wstats(source)
                    if keys is None:
                        keys = sorted(st)
                    for key, val in st.items():
                        maxk_by[key][val] = max(maxk_by[key][val], k)
                        g = k - val
                        if key not in worst or g > worst[key][0]:
                            worst[key] = (g, "".join(map(str, source)) + f" k={k} e={''.join(map(str, eps))}")
                    if source == (1,) * n or source == (2,) * n:
                        ext["".join(map(str, source))] = (k, "".join(map(str, eps)))
                gaps[(n, target)] = worst
                print(f"n={n} c={target}  k(1^n)={ext['1'*n]}  k(2^n)={ext['2'*n]}", file=log)
                for key in ("ones", "twos", "f12", "f21", "run2"):
                    row = " ".join(f"{v}:{maxk_by[key][v]}" for v in sorted(maxk_by[key]))
                    print(f"   max k by {key:>5s}: {row}", file=log)
        print("\n== max over W of k(W) - s(W), per (n, c) and statistic s; witness ==", file=log)
        for key in keys:
            print(f"[{key}]", file=log)
            for (n, target), worst in sorted(gaps.items()):
                g, wit = worst[key]
                print(f"   n={n:2d} c={target}: {g:+d}   {wit}", file=log)
    print(f"log written to {args.log}")


if __name__ == "__main__":
    main()

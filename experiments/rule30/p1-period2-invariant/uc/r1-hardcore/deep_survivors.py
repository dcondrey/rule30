#!/usr/bin/env python3
"""Anatomy of the deepest survivors on the actual-right prefix set R13.

For each (n, c): every W in R13_n is run through the forced continuation with
three kill rules recorded separately along the SAME path:

    E      : E(T[u][n]) = E(c)                           (the RW target cell)
    LANG   : the bit word W.Q stays in R13 (superset of R, exact to length 13)
    HC     : the symbol word has no 11 (junction included)

Reported: deepest run under E alone, under E+HC, under E+LANG (the lemma's
count), the prefixes attaining the E+LANG maximum with their forced symbol
word and defect word, the longest common suffix of those prefixes (a suffix
cylinder would reproduce the BWH+ clustering), and, among prefixes whose
E-only run is at least 0.5 n, where the first language violation occurs.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-hardcore")
from psi_kernel import CONE  # noqa: E402
from rw_restricted_margin import FORBIDDEN, allowed, bit_of  # noqa: E402


def forced_path(prefix: tuple[int, ...], steps: int) -> tuple[list[int], list[int]]:
    n = len(prefix)
    col: list[int] = []
    for u, e in enumerate(prefix):
        new = [0] * (2 * u + 2)
        new[0] = e
        new[1] = e ^ 3
        for i in range(2, 2 * u + 2):
            new[i] = CONE[col[i - 2]][new[i - 1]]
        col = new
    syms, defs = [], []
    for j in range(steps):
        u = n + j
        zeros = col.count(0)
        e = 2 if (n + u + zeros) & 1 else 1
        new = [0] * (n + u + 2)
        new[0] = e
        new[1] = e ^ 3
        for i in range(2, n + u + 2):
            new[i] = CONE[col[i - 2]][new[i - 1]]
        cell = new[n + u + 1]
        syms.append(e)
        defs.append(1 ^ (cell >> 1) ^ (cell & 1))
        col = new[: n + u + 1]
    return syms, defs


def words(language: str, n: int):
    forbidden = FORBIDDEN[language]
    stack = [("", ())]
    while stack:
        bits, syms = stack.pop()
        if len(syms) == n:
            yield bits, syms
            continue
        for e in (1, 2):
            nb = bits + bit_of(e)
            if not allowed(nb, forbidden):
                continue
            stack.append((nb, syms + (e,)))


def common_suffix(strs: list[str]) -> str:
    if not strs:
        return ""
    s = strs[0]
    k = 0
    while k < len(s) and all(t.endswith(s[len(s) - k - 1:]) for t in strs):
        k += 1
    return s[len(s) - k:]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--language", default="R13")
    ap.add_argument("--min-n", type=int, default=28)
    ap.add_argument("--max-n", type=int, default=36)
    args = ap.parse_args()
    forbidden = FORBIDDEN[args.language]
    for n in range(args.min_n, args.max_n + 1):
        for c in (2, 3):
            target = 0 if c == 2 else 1
            steps = n + 2
            best_e = best_ehc = best_el = best_e5 = 0
            attain: list[tuple[str, str, str]] = []
            deep_e: list[tuple[str, str, str, int, int]] = []
            first_lang_fail: Counter = Counter()
            long_e = 0
            for bits, syms in words(args.language, n):
                q, d = forced_path(syms, steps)
                k_e = steps
                for j in range(steps):
                    if d[j] != target:
                        k_e = j
                        break
                prev = syms[-1]
                k_hc = steps
                for j, s in enumerate(q):
                    if prev == 1 and s == 1:
                        k_hc = j
                        break
                    prev = s
                word = bits
                k_l = steps
                for j, s in enumerate(q):
                    word += bit_of(s)
                    if not allowed(word, forbidden):
                        k_l = j
                        break
                word = bits
                k_5 = steps
                for j, s in enumerate(q):
                    word += bit_of(s)
                    if not allowed(word, FORBIDDEN["R5"]):
                        k_5 = j
                        break
                k_ehc = min(k_e, k_hc)
                k_el = min(k_e, k_l)
                best_e5 = max(best_e5, min(k_e, k_5))
                if k_e >= 0.4 * n:
                    deep_e.append((bits, "".join(map(str, q[:k_e + 1])), "".join(map(str, d[:k_e + 1])), k_hc, k_l))
                best_e = max(best_e, k_e)
                best_ehc = max(best_ehc, k_ehc)
                if k_el > best_el:
                    best_el = k_el
                    attain = []
                if k_el == best_el:
                    attain.append((bits, "".join(map(str, q[:k_el + 1])), "".join(map(str, d[:k_el + 1]))))
                if k_e >= n / 2:
                    long_e += 1
                    first_lang_fail[min(k_l, k_e)] += 1
            suffix = common_suffix([a[0] for a in attain])
            print(f"=== n={n} c={c} |R13_n|={sum(1 for _ in words(args.language, n))} need={n+2}")
            print(f"deepest: E-only {best_e}  E+HC {best_ehc}  E+R5 {best_e5}  E+LANG {best_el}   attained by {len(attain)} prefixes, "
                  f"longest common suffix of attainers: '{suffix}' (len {len(suffix)})")
            for bits, q, d in attain[:12]:
                print(f"   W={bits}  Q={q}  Psi={d}")
            print(f"prefixes with E-only run >= n/2: {long_e}; first kill index (LANG or E) histogram: "
                  f"{sorted(first_lang_fail.items())}")
            print(f"E-only survivors with run >= 0.4n ({len(deep_e)}): W, Q (through first E fail), Psi, first 11 index, first LANG fail index")
            for bits, q, d, k_hc, k_l in deep_e[:40]:
                print(f"   W={bits} Q={q} Psi={d} hc_fail={k_hc} lang_fail={k_l}")
            sys.stdout.flush()


if __name__ == "__main__":
    main()

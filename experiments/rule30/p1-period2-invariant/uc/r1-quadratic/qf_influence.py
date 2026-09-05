#!/usr/bin/env python3
"""Two probes for an injection-type counting lemma.

(1) Influence matrix.  For each level k (hit at column n+k-1) and each source
    bit j, the fraction of level-(k-1) survivors W for which flipping bit j
    (a) keeps W' a level-(k-1) survivor and (b) flips the level-k outcome
    (hit XOR hard-core kill).  An injection lemma of the triangular kind
    needs, for every k, a bit j with fraction 1 on the survivors.  Also
    reports the fraction of survivors that have SOME bit j with (a) and (b).

(2) Fake counterexamples.  Letter words of column n-1 (not necessarily
    reachable) whose region has n+2 consecutive hits with hard-core forced
    symbols; for n = 5, 6 lists how many also end in 12a, and whether any is
    reachable from a binary source.

Run:  cd <work dir> && uv run python uc/r1-quadratic/qf_influence.py
"""

from __future__ import annotations

import argparse
import time
from itertools import product

from qf_common import E, forced_orbit, forward_columns
from qf_letterspace import region_hits


def survival(src: tuple[int, ...], n: int, c: int) -> int:
    symbols, hits, _ = forced_orbit(src, n + 2)
    eps = E(c)
    prev = src[-1]
    k = 0
    for j in range(n + 2):
        if hits[j] != eps:
            break
        if prev == 1 and symbols[j] == 1:
            break
        prev = symbols[j]
        k += 1
    return k


def influence(n: int, c: int) -> None:
    surv = {}
    for src in product((1, 2), repeat=n):
        surv[src] = survival(src, n, c)
    print(f"n={n} c={c}  influence of source bit j on level-k outcome among level-(k-1) survivors")
    header = "   k   N_(k-1)  " + " ".join(f"j={j:<2}" for j in range(n)) + "   any-bit"
    print(header)
    for k in range(1, n + 3):
        base = [s for s, v in surv.items() if v >= k - 1]
        if not base:
            break
        counts = [0] * n
        anyc = 0
        for s in base:
            found = False
            for j in range(n):
                t = list(s)
                t[j] = 3 - t[j]
                t = tuple(t)
                if surv[t] >= k - 1 and ((surv[s] >= k) != (surv[t] >= k)):
                    counts[j] += 1
                    found = True
            if found:
                anyc += 1
        row = f"  {k:>2}  {len(base):>7}  " + " ".join(f"{counts[j]/len(base):4.2f}" for j in range(n)) + f"   {anyc/len(base):4.2f}"
        print(row)


def fake_counterexamples(n: int, c: int) -> None:
    m = 2 * n
    reach = set()
    for src in product((1, 2), repeat=n):
        col = forward_columns(src)[n - 1]
        reach.add(tuple({0: 0, 2: 2, 1: 1, 3: 1}[col[d]] for d in range(-n, n)))
    total = 0
    with_12a = 0
    reachable = 0
    examples = []
    for word in product((0, 1, 2), repeat=m):
        # skip words that are not of the form a <= b (all words over {0,1,2} are valid letters)
        hits, symbols = region_hits(list(word), n, c)
        if not all(hits):
            continue
        prev = word[0] ^ 3
        ok = True
        for s in symbols:
            if prev == 1 and s == 1:
                ok = False
                break
            prev = s
        if not ok:
            continue
        total += 1
        ends = symbols[-3] == 1 and symbols[-2] == 2
        if ends:
            with_12a += 1
        if word in reach:
            reachable += 1
        if len(examples) < 3:
            examples.append((word, symbols, ends))
    print(f"n={n} c={c}: letter words with all {n+2} hits and hard-core forced symbols: {total}; "
          f"with 12a ending: {with_12a}; reachable from a binary source: {reachable}")
    for word, symbols, ends in examples:
        print(f"   column n-1 (d=-n..n-1) = {''.join(map(str, word))}  forced e_n..e_{2*n+1} = {''.join(map(str, symbols))}  12a={ends}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--influence-n", type=int, nargs="*", default=[10, 12, 14])
    ap.add_argument("--fake-n", type=int, nargs="*", default=[5, 6])
    args = ap.parse_args()
    for n in args.influence_n:
        for c in (2, 3):
            t0 = time.time()
            influence(n, c)
            print(f"   [{time.time()-t0:.1f}s]")
    for n in args.fake_n:
        for c in (2, 3):
            t0 = time.time()
            fake_counterexamples(n, c)
            print(f"   [{time.time()-t0:.1f}s]")


if __name__ == "__main__":
    main()

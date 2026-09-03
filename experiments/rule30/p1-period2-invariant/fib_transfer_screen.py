#!/usr/bin/env python3
"""L10-FIB-TRANSFER, done properly.

Question: is the language of forced-symbol blocks that occur along RW-admissible
runs a proper sub-language of the hard-core language, with growth rate below
the golden ratio?

Three languages are compared, block counts pooled over n = 10..17 and both c:

  H-only : forced continuation under the H-constraint alone (no hit, no
           hard-core); this is the BWH+ continuation Q_n(W)
  hit    : H-forced and every column a hit (E matches), hard-core NOT required
  RW     : H-forced, hit, and hard-core (the RW survivors)

For each m, B_X(m) = number of distinct m-blocks of forced symbols occurring in
language X, against 2^m (binary) and Fib(m+2) (hard-core).  Blocks are taken
strictly inside the forced part; the junction with the prefix is excluded.

The earlier run (backlog_screen_r1.py section I) used only survivors with at
least four hits at n <= 13 and was sample-limited.  Here every survivor at
every depth contributes its whole forced word, and the H-only and hit-only
languages give the two controls that say what hard-core removes and what the
hit constraint removes.
"""

from __future__ import annotations

from itertools import product

from psi_kernel import Endpoint


def fib(k):
    a, b = 1, 1
    for _ in range(k):
        a, b = b, a + b
    return a


def forced_words(n, c, need_hit, need_hc, max_len):
    """Yield the forced word from every W, stopped at the first violated condition."""
    for W in product((1, 2), repeat=n):
        st = Endpoint()
        for s in W:
            st.append(s)
        prev = W[-1]
        word = []
        for _ in range(max_len):
            chosen = None
            for s in (1, 2):
                col, dia = st.peek(s)
                if dia[n] >> 1 == 1:
                    chosen = (s, col, dia)
                    break
            if chosen is None:
                break
            s, col, dia = chosen
            if need_hit and dia[n] != c:
                break
            if need_hc and prev == 1 and s == 1:
                break
            word.append(s)
            nxt = Endpoint()
            nxt.column, nxt.diagonal, nxt.length = col + [s], dia, st.length + 1
            st, prev = nxt, s
        yield tuple(word)


def blocks(words, mmax):
    seen = {m: {} for m in range(2, mmax + 1)}
    for w in words:
        s = "".join(map(str, w))
        for m in seen:
            for i in range(len(s) - m + 1):
                blk = s[i : i + m]
                seen[m][blk] = seen[m].get(blk, 0) + 1
    return seen


def main():
    mmax = 10
    langs = {"H-only": (False, False), "hit": (True, False), "RW": (True, True)}
    tables = {}
    for name, (hit, hc) in langs.items():
        agg = {m: {} for m in range(2, mmax + 1)}
        for n in range(10, 18):
            for c in (2, 3):
                for m, d in blocks(forced_words(n, c, hit, hc, n + 2), mmax).items():
                    for k, v in d.items():
                        agg[m][k] = agg[m].get(k, 0) + v
        tables[name] = agg
    print("pooled over n=10..17, both c; blocks strictly inside the forced word")
    print(" m   2^m  Fib(m+2)   B_H-only   B_hit    B_RW    RW/Fib   longest-run occurrences RW")
    for m in range(2, mmax + 1):
        bh = len(tables["H-only"][m])
        bt = len(tables["hit"][m])
        br = len(tables["RW"][m])
        occ = sum(tables["RW"][m].values())
        print(f"{m:2}  {2**m:4}  {fib(m+2):8}   {bh:8}   {bt:6}   {br:5}   {br/fib(m+2):.3f}   {occ}")
    print()
    print("hard-core blocks ABSENT from RW forced words, by m:")
    for m in range(4, 9):
        hc = ["".join(map(str, w)) for w in product((1, 2), repeat=m) if "11" not in "".join(map(str, w))]
        absent = [w for w in hc if w not in tables["RW"][m]]
        present_hit_only = [w for w in absent if w in tables["hit"][m]]
        print(f"  m={m}: {len(absent)}/{len(hc)} absent: {absent}")
        print(f"        of these, present in the hit-only language (so hard-core is not what removes them): {present_hit_only}")
    print()
    print("growth-rate estimates B(m)/B(m-1) for RW (meaningful only while counts are not sample-limited):")
    for m in range(3, mmax + 1):
        a, b = len(tables["RW"][m - 1]), len(tables["RW"][m])
        print(f"  m={m}: {b/a:.3f}" if a else f"  m={m}: n/a")
    print("  hard-core reference ratio -> phi = 1.618; binary -> 2")


if __name__ == "__main__":
    main()

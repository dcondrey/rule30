#!/usr/bin/env python3
"""Extract and display the closest RW near-misses in the diagonal (four-state) bookkeeping.

Skeptic lens, second pass.  `fourstate_nearmiss.py` (same directory) counted, for
every binary prefix W, the number v of violations along the EXACT four-state
forced path (every T[u][n] = c; a violation is a non-binary forced symbol or a
hard-core `11` between binary symbols) over the n+2 continuation columns, and
found v = 1 with the 12a ending at n = 21, c = 3 (10 prefixes), v = 2 with 12a at
n = 22, c = 3 (2 prefixes) and v = 3 with 12a at n = 27, c = 2 (24 prefixes).
Its companion `fourstate_witness.py` was a pure-Python scan of all 2^n prefixes
and never finished (its log is empty).  This script recomputes the same
bit-sliced census with the masks kept, decodes the prefixes, and then
re-derives each forced path independently with `psi_kernel.Endpoint`, so every
displayed near-miss is checked on the reference kernel.

For each near-miss the display gives: the prefix W, the four-state forced word
Q (length n+2), the positions and kinds of the violations, the ending
(e_{2n-1}, e_{2n}) which must be (1, 2) for the 12a pull, the number of
distinct forced-process states among the prefixes (quotient of column n-1),
and, at every violation column, the window statistics of the previous column
(|Z| zeros, |W2| twos, m = window length) entering the H-forcing and Phi.

Run:  cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-skeptic/nearmiss_extract.py
"""

from __future__ import annotations

import argparse
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
KERNEL_DIR = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, KERNEL_DIR)
sys.path.insert(0, HERE)

from psi_kernel import Endpoint  # noqa: E402
from quotient_multiplicity import quotient_column  # noqa: E402
from rw_bitsliced import (  # noqa: E402
    bit_patterns,
    build_column,
    const_array,
    decode_word,
    forced_high,
    popcount,
    set_bits,
)


def fourstate_masks(n: int, sources, c: int, K: int, nwords: int, vmax: int):
    """Masks of prefixes with exactly v violations (v <= vmax) over K four-state forced columns,
    together with the 12a-ending mask (r = 0)."""
    prev = None
    for u in range(n):
        prev = build_column(prev, u, min(u, n - 1), sources[u], nwords)
    Ec_arr = const_array(nwords, c & 1)
    ex = [const_array(nwords, 1)] + [const_array(nwords, 0) for _ in range(vmax)]
    Hprev = sources[n - 1]
    prev_nonbinary = const_array(nwords, 0)
    Hforced = []
    for j in range(K):
        u = n + j
        Hu = forced_high(prev, u, n, nwords)
        col = build_column(prev, u, n, Hu, nwords)
        Fn = col.F[col.idx(n)]
        nonbinary = Fn ^ Ec_arr
        col.F ^= nonbinary[None, :]
        hc_kill = (~Hu) & (~Hprev) & (~nonbinary) & (~prev_nonbinary)
        bad = nonbinary | hc_kill
        new = [ex[0] & ~bad]
        for v in range(1, vmax + 1):
            new.append((ex[v] & ~bad) | (ex[v - 1] & bad))
        ex = new
        Hforced.append(Hu)
        prev = col
        Hprev = Hu
        prev_nonbinary = nonbinary
    end = (~Hforced[n - 1]) & Hforced[n]
    return ex, end


def fourstate_path(word: str, c: int, K: int) -> list[int]:
    n = len(word)
    ep = Endpoint()
    for ch in word:
        ep.append(int(ch))
    forced = []
    for _ in range(K):
        chosen = [s for s in range(4) if ep.peek(s)[1][n] == c]
        assert len(chosen) == 1, chosen
        forced.append(chosen[0])
        ep.append(chosen[0])
    return forced


def window_stats(word: str, forced: list[int], j: int) -> tuple[int, int, int]:
    """(|Z|, |W2|, m) of column u-1 = n+j-1 on depths [-u, n-1], u = n+j."""
    n = len(word)
    ep = Endpoint()
    for ch in word:
        ep.append(int(ch))
    for s in forced[:j]:
        ep.append(s)
    u = n + j
    # psi_kernel: column[k] = T[u-1][-k] for k = 0..u-1, column[u] = e_{u-1} (depth -u);
    # diagonal[i] = T[u-1][i] for i = 0..u-1.
    cells = [ep.column[-d] for d in range(-u, 0)] + [ep.diagonal[i] for i in range(0, n)]
    z = sum(1 for x in cells if x == 0)
    w2 = sum(1 for x in cells if x == 2)
    return z, w2, len(cells)


def violations(word: str, forced: list[int]) -> list[tuple[int, str]]:
    out = []
    prev = int(word[-1])
    for j, s in enumerate(forced):
        if s in (0, 3):
            out.append((j, f"non-binary {s}"))
        elif s == 1 and prev == 1:
            out.append((j, "hard-core 11"))
        prev = s
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cases", type=str, default="21,3,1;22,3,2;27,2,3", help="n,c,vmax triples separated by ;")
    ap.add_argument("--block", type=int, default=22)
    ap.add_argument("--require-12a", action="store_true", default=True)
    args = ap.parse_args()
    for case in args.cases.split(";"):
        n, c, vmax = (int(x) for x in case.split(","))
        K = n + 2
        B = min(args.block, n)
        nwords = (1 << B) >> 6
        pats = bit_patterns(B)
        t0 = time.time()
        found: dict[int, list[str]] = {v: [] for v in range(vmax + 1)}
        found_12a: dict[int, list[str]] = {v: [] for v in range(vmax + 1)}
        for outer in range(1 << (n - B)):
            sources = [const_array(nwords, (outer >> (n - B - 1 - t)) & 1) for t in range(n - B)] + pats
            ex, end = fourstate_masks(n, sources, c, K, nwords, vmax)
            for v in range(vmax + 1):
                for i in set_bits(ex[v]):
                    found[v].append(decode_word(sources, int(i)))
                for i in set_bits(ex[v] & end):
                    found_12a[v].append(decode_word(sources, int(i)))
        dt = time.time() - t0
        print(f"=== n={n} c={c}: prefixes with exactly v violations over {K} four-state forced columns "
              f"[{dt:.1f}s]")
        for v in range(vmax + 1):
            print(f"    v={v}: {len(found[v])} prefixes, {len(found_12a[v])} with the 12a ending")
        target = found_12a[vmax]
        if not target:
            print("    (no prefix at v = vmax with the 12a ending)")
            continue
        states = {}
        for w in target:
            states.setdefault(quotient_column(w), []).append(w)
        print(f"    v={vmax} with 12a: {len(states)} distinct forced-process state(s); fibers {[len(v) for v in states.values()]}")
        for q, members in states.items():
            w = members[0]
            forced = fourstate_path(w, c, K)
            viol = violations(w, forced)
            assert len(viol) == vmax, (w, viol)
            fw = "".join(map(str, forced))
            ending = (forced[n - 1], forced[n])
            assert ending == (1, 2), ending
            print(f"    state with fiber {len(members)}:")
            print(f"      W  = {w}")
            print(f"      Q  = {fw}   (four-state forced word, length {K})")
            print(f"      ending (e_2n-1, e_2n) = {ending}  [12a pull satisfied]")
            for j, kind in viol:
                z, w2, m = window_stats(w, forced, j)
                print(f"      violation at continuation column {j} (u = {n + j}): {kind}; "
                      f"previous-column window m={m} |Z|={z} |W2|={w2}")
            # binary-bookkeeping run of the same prefix, for comparison
            ep = Endpoint()
            for ch in w:
                ep.append(int(ch))
            prev = int(w[-1])
            run = None
            for j in range(K):
                chosen = [s for s in (1, 2) if ep.peek(s)[1][n] >> 1 == 1]
                s = chosen[0]
                cell = ep.peek(s)[1][n]
                if cell != c or (s == 1 and prev == 1):
                    run = j
                    break
                ep.append(s)
                prev = s
            print(f"      binary-bookkeeping admissible run of this prefix: {run if run is not None else K} of {K}")
            print(f"      members: {' '.join(members)}")
        sys.stdout.flush()


if __name__ == "__main__":
    main()

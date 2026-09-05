#!/usr/bin/env python3
"""Are column collisions local?  Structure of the fibres of W -> full column.

state_language.py measured |C_u| ~ 1.765^u: the source-to-column map has
exponentially large fibres.  A PROOF of |C_u| <= C beta^u, beta < 2, needs a
mechanism producing exponentially many collisions.  The cleanest possible
mechanism is a local invisible rewriting: a bounded pattern P in the source
that can be replaced by P' without changing the full column.  Then |C_u| is
at most the number of sources modulo the rewriting, an SFT-type count with
entropy < 1.

This script tests locality directly.  For u = umin..umax it builds the
fibres (BFS over distinct states, multiplicities as source lists), and for
every pair of fibre-mates records the difference set.  A pair is PRIMITIVE
if the two (u-1)-prefixes have different columns (the collision is created
at this level, not inherited).  Reported per u:

  * number of primitive pairs, and the histogram of their difference SPAN
    (last differing position - first differing position + 1);
  * the histogram of the distance from the end (u-1) to the last differing
    position;
  * the distinct (window of W, window of W') substitutions for spans <= 6,
    with counts, i.e. the candidate rewriting rules.

If every primitive pair has bounded span and bounded distance from the end,
a local invisible rewriting exists and beta < 2 becomes provable by an SFT
count.  If spans grow with u, collisions are global and no local proof
exists.

Run:  cd <kernel dir> && uv run python uc/r1-entropy/fibre_structure.py --umin 6 --umax 15
"""
from __future__ import annotations

import argparse
import os
import sys
from collections import Counter, defaultdict
from itertools import combinations

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from psi_kernel import Endpoint  # noqa: E402


def build_levels(umax: int):
    """levels[u] = dict state_key -> list of sources (tuples) of length u."""
    levels = {}
    cur = {}
    root = Endpoint()
    for s in (1, 2):
        st = root.clone()
        st.append(s)
        cur.setdefault((tuple(st.column), tuple(st.diagonal)), []).append((s,))
    levels[1] = cur
    for u in range(2, umax + 1):
        nxt = {}
        for k, srcs in cur.items():
            st = Endpoint()
            st.column, st.diagonal, st.length = list(k[0]), list(k[1]), u - 1
            for s in (1, 2):
                col, dia = st.peek(s)
                key = (tuple(col + [s]), tuple(dia))
                lst = nxt.setdefault(key, [])
                for w in srcs:
                    lst.append(w + (s,))
        levels[u] = nxt
        cur = nxt
    return levels


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--umin", type=int, default=6)
    ap.add_argument("--umax", type=int, default=15)
    ap.add_argument("--max-pairs", type=int, default=200000)
    ap.add_argument("--log", type=str, default="uc/r1-entropy/fibre_structure.log")
    args = ap.parse_args()
    levels = build_levels(args.umax)
    with open(args.log, "w") as log:
        print("# fibre structure of W -> full column at level u-1 (prefix length u)", file=log)
        for u in range(args.umin, args.umax + 1):
            fib = levels[u]
            prev = levels[u - 1]
            # map each (u-1)-prefix to its state key
            prev_key = {}
            for k, srcs in prev.items():
                for w in srcs:
                    prev_key[w] = k
            span_hist = Counter()
            end_hist = Counter()
            first_hist = Counter()
            rules = Counter()
            n_pairs = 0
            n_prim = 0
            fibre_sizes = Counter(len(v) for v in fib.values())
            for k, srcs in fib.items():
                if len(srcs) < 2:
                    continue
                for w, w2 in combinations(srcs, 2):
                    n_pairs += 1
                    if n_pairs > args.max_pairs:
                        break
                    if prev_key[w[:-1]] == prev_key[w2[:-1]]:
                        continue  # inherited collision
                    n_prim += 1
                    diff = [i for i in range(u) if w[i] != w2[i]]
                    first, last = diff[0], diff[-1]
                    span = last - first + 1
                    span_hist[span] += 1
                    end_hist[u - 1 - last] += 1
                    first_hist[first] += 1
                    if span <= 6:
                        a = "".join(map(str, w[first:last + 1]))
                        b = "".join(map(str, w2[first:last + 1]))
                        rules[(min(a, b), max(a, b), u - 1 - last)] += 1
            print(f"\n# u={u}: |C_u|={len(fib)}, fibre-size histogram {dict(sorted(fibre_sizes.items()))}", file=log)
            print(f"  pairs examined {n_pairs}, primitive {n_prim}", file=log)
            print(f"  primitive span histogram: {dict(sorted(span_hist.items()))}", file=log)
            print(f"  primitive distance-from-end of last diff: {dict(sorted(end_hist.items()))}", file=log)
            print(f"  primitive first-diff position: {dict(sorted(first_hist.items()))}", file=log)
            top = sorted(rules.items(), key=lambda kv: -kv[1])[:12]
            print(f"  top substitution rules (P, P', dist-from-end) among span<=6: {top}", file=log)
            log.flush()
    with open(args.log) as f:
        sys.stdout.write(f.read())


if __name__ == "__main__":
    main()

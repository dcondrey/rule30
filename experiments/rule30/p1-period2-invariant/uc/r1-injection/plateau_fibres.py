#!/usr/bin/env python3
"""Anatomy of the deep RW survivors at n = 21..33: states, fibres, free prefixes.

Input: the witness lists stored by uc/r1-skeptic/rw_bitsliced.py (census_*.json,
field "witnesses": level -> list of source words, deepest levels only).  For each
(n, c) and each stored level k this script

  1. re-runs the forced RW orbit (inj_common.rw_depth) on every witness and
     checks depth >= k (gate on the skeptic's data);
  2. groups the witnesses by their column-(n-1) quotient state
     (inj_common.state_of) and reports the number of distinct states and the
     fibre sizes;
  3. for each state: the longest common suffix s of its members, the free
     prefix length j = n - |s|, the number of members versus 2^j, and whether
     the member prefixes (encoded 1 -> 1, 2 -> 0 as GF(2) vectors) form an
     affine subspace (closed under x + y + z); if so its dimension; if not,
     the dimension of the affine hull and the fraction of the hull occupied;
  4. the fibre-run product: log2(fibre) + run - n for the deepest state.

Usage: cd experiments/rule30/p1-period2-invariant && uv run python uc/r1-injection/plateau_fibres.py
"""

from __future__ import annotations

import json
import math
import sys
from itertools import combinations

sys.path.insert(0, "uc/r1-injection")
from inj_common import rw_depth, state_of  # noqa: E402

SKEPTIC = "uc/r1-skeptic/"


def common_suffix(words: list[str]) -> str:
    s = words[0]
    for w in words[1:]:
        i = 0
        while i < len(s) and i < len(w) and s[-1 - i] == w[-1 - i]:
            i += 1
        s = s[len(s) - i:]
        if not s:
            break
    return s


def bits(prefix: str) -> int:
    v = 0
    for ch in prefix:
        v = (v << 1) | (1 if ch == "1" else 0)
    return v


def affine_hull_dim(vecs: list[int]) -> int:
    base = vecs[0]
    rows = [v ^ base for v in vecs[1:]]
    # GF(2) rank by elimination
    rank = 0
    pivots = []
    for r in rows:
        for p in pivots:
            r = min(r, r ^ p)
        if r:
            pivots.append(r)
            rank += 1
    return rank


def is_affine(vecs: list[int]) -> bool:
    S = set(vecs)
    if len(S) <= 2:
        return True
    base = vecs[0]
    for x, y in combinations(vecs[1:], 2):
        if (x ^ y ^ base) not in S:
            return False
    return True


def main() -> None:
    files = ("census_n21_30.json", "census_n31.json", "census_n32.json", "census_n33.json")
    tail_worst = (-99.0, None)
    for name in files:
        with open(SKEPTIC + name) as fh:
            data = json.load(fh)
        for _, rec in data.items():
            n, c = rec["n"], rec["c"]
            wit = rec.get("witnesses", {})
            for k_str in sorted(wit, key=int):
                k = int(k_str)
                words = wit[k_str]
                srcs = [tuple(int(ch) for ch in w) for w in words]
                depths = [rw_depth(w, c) for w in srcs]
                bad = sum(1 for d in depths if d < k)
                groups: dict[str, list[str]] = {}
                for w, src in zip(words, srcs):
                    groups.setdefault(state_of(src), []).append(w)
                sizes = sorted((len(g) for g in groups.values()), reverse=True)
                print(f"n={n} c={c} k={k}: {len(words)} witnesses, gate failures={bad}, states={len(groups)}, fibres={sizes[:8]}{'...' if len(sizes) > 8 else ''}")
                for state, members in sorted(groups.items(), key=lambda kv: -len(kv[1]))[:3]:
                    s = common_suffix(members)
                    j = n - len(s)
                    pre = [m[:j] for m in members]
                    vecs = [bits(p) for p in pre]
                    aff = is_affine(vecs)
                    hull = affine_hull_dim(vecs) if len(vecs) > 1 else 0
                    run = rw_depth(tuple(int(ch) for ch in members[0]), c, max_len=n + 2)
                    hc = sum(1 for p in pre if "11" not in p)
                    tail = math.log2(len(members)) + run - n
                    if tail > tail_worst[0]:
                        tail_worst = (tail, (n, c, k))
                    print(
                        f"    state fibre={len(members):>4} run={run:>2} suffix={s} (|s|={len(s)}) free j={j} "
                        f"members/2^j={len(members)}/{2**j} affine={aff} hull_dim={hull} hardcore_prefixes={hc} "
                        f"log2F+run-n={tail:.2f}"
                    )
                    if len(members) <= 40 and j <= 10:
                        print("       prefixes: " + " ".join(sorted(pre)))
    print(f"max over deepest states of log2(fibre) + run - n = {tail_worst[0]:.2f} at {tail_worst[1]}")


if __name__ == "__main__":
    main()

"""Reconstruct and print the minimum tree-like derivation at tiny n.

This is what revealed the backward-elimination family: the optimum derives NO
intermediate unit clause, it eliminates ancestor variables one at a time.

Run:
    /Volumes/A/researchpapers/.venv/bin/python p3_optimal_witness.py
"""

from __future__ import annotations

import heapq
import logging

import p3_core as P


def optimal(rule: int, n: int, cap: int):
    inst = P.Instance(rule, n)
    target = inst.target()
    dist, par, pq = {}, {}, []
    for c in inst.axioms:
        if c not in dist:
            dist[c] = 0
            par[c] = None
            heapq.heappush(pq, (0, sorted(c), c))
    done, by = set(), {}
    while pq:
        d, _, c = heapq.heappop(pq)
        if d > dist.get(c, 1 << 60) or c in done:
            continue
        done.add(c)
        if c == target:
            break
        for l in c:
            for o in by.get(-l, ()):
                nd = d + dist[o] + 1
                if nd > cap:
                    continue
                r = frozenset((c - {l}) | (o - {-l}))
                if any(-m in r for m in r):
                    continue
                if nd < dist.get(r, 1 << 60):
                    dist[r] = nd
                    par[r] = (c, o, l)
                    heapq.heappush(pq, (nd, sorted(r), r))
        for l in c:
            by.setdefault(l, []).append(c)
    inv = {v: k for k, v in inst.var.items()}

    def show(c):
        return "{" + ",".join(
            f"{'' if l > 0 else '~'}{inv[abs(l)]}" for l in sorted(c, key=abs)
        ) + "}"

    seen = []

    def walk(c):
        if par.get(c) is None:
            return
        a, b, l = par[c]
        walk(a)
        walk(b)
        seen.append((a, b, l, c))

    walk(target)
    bwd, _ = P.derive_backward(rule, n)
    logging.info(
        "rule %d n=%d  min_tree=%d  steps=%d  backward family=%d",
        rule, n, dist[target], len(seen), bwd.length,
    )
    for a, b, l, c in seen:
        logging.info("    %s + %s on %s => %s", show(a), show(b), inv[abs(l)], show(c))
    return dist[target]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    for n in (2, 3):
        optimal(30, n, 20)

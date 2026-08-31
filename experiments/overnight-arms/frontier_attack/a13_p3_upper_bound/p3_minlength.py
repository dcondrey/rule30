"""Exact MINIMUM tree-like resolution derivation length of the centre unit,
at the tiny n where it is computable, by Dijkstra over the clause space.

cost(axiom) = 0;  cost(resolvent(a,b)) = cost(a) + cost(b) + 1.

What this is: the shortest derivation of c_n that any tree-like search could
find.  Since min_DAG <= min_tree, a value BELOW the constructed baseline would
be a genuine shorter derivation; a value EQUAL to it says the baseline is
already tree-optimal at that n.  This buys nothing asymptotic (obstruction H):
n terms buy a statement about n, ever.

Run:
    /Volumes/A/researchpapers/.venv/bin/python p3_minlength.py --out minlen.json
"""

from __future__ import annotations

import argparse
import heapq
import json
import logging
import time

import p3_core as P


def min_tree_length(rule: int, n: int, cap: int, node_cap: int, time_cap: float = 1e18):
    """Dijkstra to the target unit.  Returns (cost or None, settled, seconds)."""
    inst = P.Instance(rule, n)
    target = inst.target()
    t0 = time.time()
    dist: dict[frozenset[int], int] = {}
    pq = []
    for c in inst.axioms:
        if c not in dist:
            dist[c] = 0
            heapq.heappush(pq, (0, sorted(c), c))
    done: set[frozenset[int]] = set()
    by_lit: dict[int, list[frozenset[int]]] = {}
    while pq:
        d, _, c = heapq.heappop(pq)
        if d > dist.get(c, 1 << 60):
            continue
        if c in done:
            continue
        done.add(c)
        if c == target:
            return d, len(done), time.time() - t0
        if len(done) > node_cap or time.time() - t0 > time_cap:
            return None, len(done), time.time() - t0
        for l in c:
            for other in by_lit.get(-l, ()):
                nd = d + dist[other] + 1
                if nd > cap:
                    continue
                r = frozenset((c - {l}) | (other - {-l}))
                if any(-m in r for m in r):
                    continue
                if nd < dist.get(r, 1 << 60):
                    dist[r] = nd
                    heapq.heappush(pq, (nd, sorted(r), r))
        for l in c:
            by_lit.setdefault(l, []).append(c)
    return None, len(done), time.time() - t0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ns", type=int, nargs="+", default=[2, 3, 4, 5, 6])
    ap.add_argument("--node-cap", type=int, default=400000)
    ap.add_argument("--time-cap", type=float, default=1200.0,
                    help="seconds per band before the wall is recorded")
    ap.add_argument("--out", default="minlen.json")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    out = []
    for rule in (30, 90):
        for n in a.ns:
            base, _ = P.derive_full(rule, n)
            sl, _ = P.derive_sliced(rule, n)
            bwd, _ = P.derive_backward(rule, n)
            # decisive question: is ANYTHING strictly shorter than the backward
            # elimination chain?  Cap one below it; exhausting the search then
            # proves the chain is TREE-optimal at this n (min_DAG <= min_tree,
            # so this is not a lower bound on resolution length in general).
            cap = bwd.length - 1
            cost, settled, sec = min_tree_length(
                rule, n, cap, a.node_cap, a.time_cap
            )
            rec = {
                "rule": rule, "n": n, "baseline": base.length, "sliced": sl.length,
                "backward": bwd.length, "cap": cap,
                "min_tree_below_cap": cost, "settled": settled, "sec": round(sec, 1),
            }
            out.append(rec)
            logging.info(
                "rule %d n=%-2d baseline=%-5d sliced=%-5d backward=%-5d  "
                "search<=%d: %-28s settled=%-8d %.1fs",
                rule, n, base.length, sl.length, bwd.length, cap,
                f"FOUND shorter, length {cost}" if cost is not None
                else ("EXHAUSTED: none shorter"
                      if settled <= a.node_cap and sec <= a.time_cap
                      else "WALL (cap reached)"),
                settled, sec,
            )
            with open(a.out, "w") as f:
                json.dump(out, f, indent=1)
            if cost is None and (settled > a.node_cap or sec > a.time_cap):
                logging.info(
                    "   WALL at n=%d (rule %d): settled %d clauses in %.0f s "
                    "(node cap %d, time cap %.0f s)",
                    n, rule, settled, sec, a.node_cap, a.time_cap,
                )
                break
    with open(a.out, "w") as f:
        json.dump(out, f, indent=1)
    logging.info("wrote %s", a.out)


if __name__ == "__main__":
    main()

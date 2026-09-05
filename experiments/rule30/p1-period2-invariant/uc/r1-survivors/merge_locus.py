#!/usr/bin/env python3
"""Where in the column do state merges happen?

For u = 3..U, over all 2^(u+1) binary sources:
  b-merges: sources with identical full col_u but distinct col_{u-1}.  For
    every such pair (within a fibre, all pairs) record the set of depths d
    where col_{u-1} differs, as the distance from the bottom of col_{u-1}:
    dist = (u-1) - d  (0 = the diagonal cell T[u-1][u-1]).
  q-merges: sources with identical quotient(col_u) but distinct full col_u.
    Record the differing depths (all are 1<->3 swaps) as dist = u - d.
Prints, per u, the number of merged pairs, the histogram of the SHALLOWEST
differing cell's distance from the bottom (max over the pair's differing
depths of dist), and the maximum such distance.  If merges are confined to
the bottom O(1) cells the histogram is concentrated at small dist and the
max is bounded in u; if the loss is spread over the column it grows.
"""
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from itertools import combinations

sys.path.insert(0, "/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant")
from psi_kernel import CONE, BOUNDARY  # noqa: E402

LET = bytes([2, 0, 1, 0])


def main() -> None:
    U = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    for u in range(3, U + 1):
        by_full: dict[bytes, list[bytes]] = defaultdict(list)   # col_u -> list of col_{u-1}
        by_quot: dict[bytes, set[bytes]] = defaultdict(set)     # quot(col_u) -> set of col_u

        def rec(k: int, prev: list[int] | None) -> None:
            for e in (1, 2):
                col = [0] * (2 * k + 2)
                col[0] = e
                col[1] = BOUNDARY[e]
                for d in range(-k + 1, k + 1):
                    col[d + k + 1] = CONE[prev[d + k - 1]][col[d + k]]
                if k == u:
                    b = bytes(col)
                    by_full[b].append(bytes(prev))
                    by_quot[bytes(LET[c] for c in col)].add(b)
                else:
                    rec(k + 1, col)
        rec(0, None)

        # b-merges
        bhist = Counter()
        bpairs = 0
        bmax = -1
        cellhist = Counter()
        for colu, prevs in by_full.items():
            distinct = sorted(set(prevs))
            for p, q in combinations(distinct, 2):
                # p, q are col_{u-1} at depths -u..u-1, index d+u
                diffs = [i for i in range(len(p)) if p[i] != q[i]]
                dists = [(u - 1) - (i - u) for i in diffs]  # (u-1) - d
                shallow = max(dists)
                bhist[shallow] += 1
                bpairs += 1
                bmax = max(bmax, shallow)
                for dd in dists:
                    cellhist[dd] += 1
        # q-merges
        qhist = Counter()
        qpairs = 0
        qmax = -1
        qcell = Counter()
        for quot, fulls in by_quot.items():
            for p, q in combinations(sorted(fulls), 2):
                diffs = [i for i in range(len(p)) if p[i] != q[i]]
                dists = [u - (i - u - 1) for i in diffs]  # u - d
                shallow = max(dists)
                qhist[shallow] += 1
                qpairs += 1
                qmax = max(qmax, shallow)
                for dd in dists:
                    qcell[dd] += 1
        def fmt(h: Counter) -> str:
            return " ".join(f"{k}:{h[k]}" for k in sorted(h))
        print(f"u={u:2d}  b-merged pairs {bpairs:6d}  max shallowest-diff dist {bmax:3d}   hist(shallowest dist from bottom of col_(u-1)): {fmt(bhist)}")
        print(f"       b-merge differing cells by dist: {fmt(cellhist)}")
        print(f"u={u:2d}  q-merged pairs {qpairs:6d}  max shallowest-diff dist {qmax:3d}   hist(shallowest dist from bottom of col_u): {fmt(qhist)}")
        print(f"       q-merge differing cells by dist: {fmt(qcell)}")


if __name__ == "__main__":
    main()

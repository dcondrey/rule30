"""Independent re-derivation of every cross-reference and algebraic premise the
novel-framework triage rests on.  Written because TRIAGE-novel-frameworks.md
originally carried three claims it had not itself checked.

V1  Rule 30 is not additive over GF(2); Rule 90 is.  (A1's premise.)
V2  The lone-seed orbit is aperiodic for a trivial reason: support width is
    2t+1, strictly increasing, so no two rows coincide.  (A1's "non-torsion
    gives nothing new".)
V3  ARM8's ROBDD table re-derived from scratch: the minimal exact bond
    dimension across a VERTICAL (variable-order) cut of F_h is the
    Myhill-Nerode residual count, i.e. ROBDD width.  Reproduces ARM8's
    right-to-left max widths 2, 7, 24, 92 and reachable node counts
    7, 28, 105, 405 at h = 2, 4, 6, 8.
V4  The HORIZONTAL (temporal) cut named in the tensor-network proposal is
    degenerate for a single-bit output: the bond is at most 2.

Run: uv run python experiments/overnight-arms/novel_frameworks/verify_crossrefs.py
"""

from __future__ import annotations

import json

import numpy as np


def _step(bits, rule):
    n = len(bits)
    if rule == 30:
        return tuple(bits[(i - 1) % n] ^ (bits[i] | bits[(i + 1) % n]) for i in range(n))
    return tuple(bits[(i - 1) % n] ^ bits[(i + 1) % n] for i in range(n))


def v1_additivity(n=8):
    out = {}
    for rule in (30, 90):
        viol = tot = 0
        for a in range(1 << n):
            x = tuple((a >> i) & 1 for i in range(n))
            fx = _step(x, rule)
            for b in range(1 << n):
                y = tuple((b >> i) & 1 for i in range(n))
                xy = tuple(u ^ v for u, v in zip(x, y))
                tot += 1
                if _step(xy, rule) != tuple(u ^ v for u, v in zip(fx, _step(y, rule))):
                    viol += 1
        out[str(rule)] = {"violations": viol, "pairs": tot}
    return out


def v2_orbit(T=200):
    row, sizes = 1, []
    for _ in range(T):
        sizes.append(row.bit_length())
        row = (row << 2) ^ ((row << 1) | row)
    return {"T": T, "widths_head": sizes[:6], "width_last": sizes[-1],
            "strictly_increasing": all(sizes[i] < sizes[i + 1]
                                       for i in range(len(sizes) - 1)),
            "matches_2t_plus_1": sizes == [2 * t + 1 for t in range(T)]}


def _truth_table(h):
    """F_h : {0,1}^{2h+1} -> {0,1}; bit j of the index is cell x = j-h at t=0."""
    n = 2 * h + 1
    idx = np.arange(1 << n, dtype=np.int64)
    rows = [((idx >> j) & 1).astype(np.uint8) for j in range(n)]
    for _ in range(h):
        rows = [rows[j - 1] ^ (rows[j] | rows[j + 1]) for j in range(1, len(rows) - 1)]
    assert len(rows) == 1
    return rows[0], n


def _reorder(tt, n, order):
    idx = np.arange(1 << n, dtype=np.int64)
    new = np.zeros_like(idx)
    for pos, j in enumerate(order):
        new |= ((idx >> j) & 1) << (n - 1 - pos)
    perm = np.empty(1 << n, dtype=np.int64)
    perm[new] = idx
    return tt[perm]


def v3_robdd(hs=(2, 4, 6, 8)):
    """ROBDD node count per level: distinct residuals after fixing the first k
    order-variables that are non-constant AND depend on the next variable
    (a reduced diagram skips the rest)."""
    out = []
    for h in hs:
        tt, n = _truth_table(h)
        t = _reorder(tt, n, list(range(n - 1, -1, -1)))  # right-to-left
        levels = []
        for k in range(n):
            keep = 0
            for b in np.unique(t.reshape(1 << k, -1), axis=0):
                if b.min() == b.max():
                    continue
                lo, hi = b[:len(b) // 2], b[len(b) // 2:]
                if not np.array_equal(lo, hi):
                    keep += 1
            levels.append(keep)
        out.append({"horizon": h, "max_width": max(levels),
                    "reachable_nodes": sum(levels), "levels": levels})
    return out


def v4_temporal_cut(hs=(2, 4, 6)):
    return {str(h): int(len(np.unique(_truth_table(h)[0]))) for h in hs}


def main():
    res = {"V1_additivity": v1_additivity(),
           "V2_orbit_support": v2_orbit(),
           "V3_robdd_vs_ARM8": v3_robdd(),
           "V4_temporal_cut_bond": v4_temporal_cut()}
    arm8 = {2: (2, 7), 4: (7, 28), 6: (24, 105), 8: (92, 405)}
    ok = all((r["max_width"], r["reachable_nodes"]) == arm8[r["horizon"]]
             for r in res["V3_robdd_vs_ARM8"])
    res["V3_matches_ARM8_table"] = ok
    assert res["V1_additivity"]["90"]["violations"] == 0
    assert res["V1_additivity"]["30"]["violations"] > 0
    assert res["V2_orbit_support"]["matches_2t_plus_1"]
    assert ok, "ARM8 cross-reference NOT reproduced"
    assert set(res["V4_temporal_cut_bond"].values()) == {2}
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()

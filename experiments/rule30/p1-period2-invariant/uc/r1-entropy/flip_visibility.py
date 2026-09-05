#!/usr/bin/env python3
"""Single-symbol flip visibility: the coalescence mechanism behind |C_u| ~ 1.765^u.

By the light cone, T[u][d] depends on e_j only for d >= u-1-2j, so flipping
e_j changes column u only in its top 2j+2 cells, and only while the
difference stays letter-visible (phi reads its left argument through the
3-letter quotient, and reads b = [Lo == 0] only where the right argument has
H = 1).  If the difference becomes invisible the two prefixes have the same
full column for ever after.

Measured here for j = 0..4 and u = j+2..umax:

    f_j(u) = #{W in {1,2}^u : column(W) == column(W with e_j flipped)} / 2^u

and the survival g_j(u) = 1 - f_j(u), with successive ratios, to see whether
the e_j-defect dies geometrically in u.  Also the fraction of W where ALL of
e_0..e_{j} are individually invisible (a lower bound on log2 fibre >= j+1 is
NOT implied; this is the mechanism check only).

Run:  cd <kernel dir> && uv run python uc/r1-entropy/flip_visibility.py --umax 20
"""
from __future__ import annotations

import argparse
import os
import sys
from itertools import product

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from psi_kernel import Endpoint  # noqa: E402


def columns_of_all(u: int) -> dict:
    """W -> state key, by DFS over the prefix tree (O(2^u u))."""
    out = {}
    def rec(st: Endpoint, w: tuple):
        if len(w) == u:
            out[w] = (tuple(st.column), tuple(st.diagonal))
            return
        for s in (1, 2):
            nxt = st.clone()
            nxt.append(s)
            rec(nxt, w + (s,))
    rec(Endpoint(), ())
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--umax", type=int, default=20)
    ap.add_argument("--jmax", type=int, default=4)
    ap.add_argument("--log", type=str, default="uc/r1-entropy/flip_visibility.log")
    args = ap.parse_args()
    with open(args.log, "w") as log:
        print("# g_j(u) = fraction of W in {1,2}^u whose e_j flip changes the full column u-1 (defect still visible)", file=log)
        print("# columns: u, then for j=0..jmax: g_j(u) and ratio g_j(u)/g_j(u-1); last: fraction with e_0..e_jmax all invisible", file=log)
        prev = {}
        hdr = "  u " + " ".join(f"   g_{j}(u)  ratio " for j in range(args.jmax + 1)) + "   all-invis"
        print(hdr, file=log)
        for u in range(args.jmax + 2, args.umax + 1):
            cols = columns_of_all(u)
            total = 2 ** u
            line = f"{u:3d} "
            all_inv = 0
            vis_counts = []
            for j in range(args.jmax + 1):
                vis = 0
                for w, key in cols.items():
                    w2 = w[:j] + (3 - w[j],) + w[j + 1:]
                    if cols[w2] != key:
                        vis += 1
                vis_counts.append(vis)
                g = vis / total
                r = g / prev[j] if j in prev and prev[j] > 0 else float("nan")
                line += f" {g:8.4f} {r:6.3f} "
                prev[j] = g
            for w, key in cols.items():
                ok = True
                for j in range(args.jmax + 1):
                    w2 = w[:j] + (3 - w[j],) + w[j + 1:]
                    if cols[w2] != key:
                        ok = False
                        break
                if ok:
                    all_inv += 1
            line += f"   {all_inv/total:8.4f}"
            print(line, file=log)
            log.flush()
    with open(args.log) as f:
        sys.stdout.write(f.read())


if __name__ == "__main__":
    main()

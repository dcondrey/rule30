"""Feed the constructed configuration's letter word into the REAL ladder engine.

`ladder_copy.py` is a byte-identical copy of `experiments/rule30/ladder/ladder.py`.
We drive its own `step_window` with the letter word (col_{R-1}(t), col_R(t))
read off the constructed configuration.

Exhaustiveness note.  `step_window` performs a wedge/edge check only while
`cnt < P.saturate = R + 2k + 1`.  Checking the first `saturate + margin`
letters therefore decides *every* safety constraint the ladder imposes, not a
sample of them.  The Buchi (centre eventually w-periodic) and Diff_q
acceptance conditions are separate and are settled by construction / measured
below.
"""

from __future__ import annotations

import argparse
import json

import numpy as np

import ladder_copy as L
from realize import build, diff_q_events, min_eventual_period


def run(rule: int, k: int, word: tuple[int, ...], T: int, rmax: int,
        q: int | None, margin: int):
    xlo, xhi = -k - 2, rmax + 2
    b = build(rule, k, word, T, xlo, xhi)
    cols, T0 = b["cols"], b["T0"]
    rows = []
    for R in range(1, rmax + 1):
        P = L.Params(rule=rule, right_depth=R, left_depth=k,
                     period_word=word, diff_q=q)
        sat = P.saturate
        nlet = sat + margin
        window = ()
        cnt = 0
        rej = None
        cmis = m1mis = 0
        for t in range(nlet):
            letter = (int(cols[R - 1][t]) << 1) | int(cols[R][t])
            hit = L.step_window(window, cnt, letter, P)
            if hit is None:
                rej = t
                break
            window, c_val, m1_val = hit
            # column x is read at letter time cnt with delay max(0, R-1-x)
            tc = cnt - max(0, R - 1)
            if c_val is not None and 0 <= tc <= T and int(cols[0][tc]) != c_val:
                cmis += 1
            tm = cnt - max(0, R)
            if m1_val is not None and 0 <= tm <= T and int(cols[-1][tm]) != m1_val:
                m1mis += 1
            cnt += 1
        # Boundary extendability at the modelled boundary column R, using EACH
        # RULE'S OWN condition (rung-1 Lemma 1 / Lemma 1').  Rule 90's is
        # vacuous -- col_{R+1}(t) = col_R(t+1) XOR col_{R-1}(t) always solves --
        # so applying rule 30's pin to rule 90 would destroy the control rather
        # than test it.
        pin_ante = pin_bad = 0
        if rule == 30:
            for t in range(T):
                if cols[R][t]:
                    pin_ante += 1
                    if int(cols[R - 1][t]) != 1 - int(cols[R][t + 1]):
                        pin_bad += 1
        rows.append({"R": R, "saturate": sat, "letters_fed": nlet,
                     "rejected_at": rej, "centre_mismatches": cmis,
                     "col_m1_mismatches": m1mis,
                     "pin_antecedents": pin_ante, "pin_violations": pin_bad})
    return b, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule", type=int, default=30)
    ap.add_argument("-k", type=int, default=2)
    ap.add_argument("-w", default="01")
    ap.add_argument("-T", type=int, default=20000)
    ap.add_argument("--rmax", type=int, default=12)
    ap.add_argument("-q", type=int, default=1)
    ap.add_argument("--margin", type=int, default=8)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    word = tuple(int(c) for c in a.w)
    b, rows = run(a.rule, a.k, word, a.T, a.rmax, a.q, a.margin)

    print(f"rule {a.rule}, k={a.k}, w={a.w}, q={a.q}, T={a.T}")
    print(" R  saturate  fed  rejected_at  centre_mism  col-1_mism  "
          "pin_antecedents  pin_violations")
    allok = True
    for r in rows:
        allok &= (r["rejected_at"] is None and r["centre_mismatches"] == 0
                  and r["col_m1_mismatches"] == 0 and r["pin_violations"] == 0)
        print(f"{r['R']:2d}  {r['saturate']:8d}  {r['letters_fed']:3d}  "
              f"{str(r['rejected_at']):>11}  {r['centre_mismatches']:11d}  "
              f"{r['col_m1_mismatches']:10d}  {r['pin_antecedents']:15d}  "
              f"{r['pin_violations']:14d}")
    print(f"ALL PASS: {allok}")

    m1 = b["cols"][-1]
    drop = b["T0"] + 4
    mp = min_eventual_period(m1, 512, drop)
    print(f"col_-1 smallest eventual period <= 512 on t in [{drop},{a.T}]: {mp}")
    print(f"Diff_q events, q=1..16: "
          f"{[diff_q_events(m1, q, drop) for q in range(1, 17)]}")
    if a.json:
        with open(a.json, "w") as f:
            json.dump({"rows": rows, "all_pass": bool(allok),
                       "col_m1_min_period_le_512": mp,
                       "rule": a.rule, "k": a.k, "w": a.w, "T": a.T}, f,
                      indent=1, default=str)


if __name__ == "__main__":
    main()

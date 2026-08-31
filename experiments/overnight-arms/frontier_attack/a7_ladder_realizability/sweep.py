"""Sweep the realizability construction over rule, left depth k, and tail word.

For each (rule, k, w) it builds the configuration, drives the real
`ladder_copy.step_window` at R = 1..rmax, and records:

  * ladder rejection (safety) -- exhaustive, since checks stop at `saturate`;
  * agreement of the ladder's derived col_0 / col_{-1} with the configuration;
  * Lemma-1 boundary-pin violations at column R (must be 0: the object has a
    genuine col_{R+1});
  * the smallest eventual period of col_{-1} up to `qmax` on the horizon, and
    the Diff_1 event count.
"""

from __future__ import annotations

import argparse
import json
from itertools import product

from ladder_check import run
from realize import diff_q_events, min_eventual_period


def necklaces(pmax: int):
    """Primitive binary necklaces of length <= pmax, lexicographic rep."""
    seen = []
    for p in range(1, pmax + 1):
        reps = set()
        for bits in product((0, 1), repeat=p):
            if p > 1 and any(p % d == 0 and bits == (bits[:d] * (p // d))
                             for d in range(1, p)):
                continue
            rot = min(tuple(bits[i:] + bits[:i]) for i in range(p))
            reps.add(rot)
        seen += ["".join(map(str, r)) for r in sorted(reps)]
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rules", default="30,90")
    ap.add_argument("--kmax", type=int, default=8)
    ap.add_argument("--pmax", type=int, default=6)
    ap.add_argument("--rmax", type=int, default=16)
    ap.add_argument("-T", type=int, default=4000)
    ap.add_argument("--qmax", type=int, default=256)
    ap.add_argument("--json", default="out_sweep.json")
    a = ap.parse_args()

    words = necklaces(a.pmax)
    rules = [int(x) for x in a.rules.split(",")]
    out = []
    nfail = 0
    print(f"words ({len(words)}): {' '.join(words)}")
    print("rule   k  w        Rmax  reject  cmis  m1mis  pinviol  "
          "minper(col-1)  diff1")
    for rule in rules:
        for k in range(1, a.kmax + 1):
            for w in words:
                word = tuple(int(c) for c in w)
                b, rows = run(rule, k, word, a.T, a.rmax, 1, 8)
                rej = [r["R"] for r in rows if r["rejected_at"] is not None]
                cmis = sum(r["centre_mismatches"] for r in rows)
                m1mis = sum(r["col_m1_mismatches"] for r in rows)
                pv = sum(r["pin_violations"] for r in rows)
                m1 = b["cols"][-1]
                drop = b["T0"] + 4
                mp = min_eventual_period(m1, a.qmax, drop)
                d1 = diff_q_events(m1, 1, drop)
                ok = not rej and cmis == 0 and m1mis == 0 and pv == 0
                nfail += (not ok)
                out.append({"rule": rule, "k": k, "w": w, "rmax": a.rmax,
                            "rejected_R": rej, "centre_mismatches": cmis,
                            "col_m1_mismatches": m1mis, "pin_violations": pv,
                            "col_m1_min_eventual_period": mp,
                            "diff1_events": d1, "ok": ok})
                print(f"{rule:4d} {k:3d}  {w:8s} {a.rmax:4d}  "
                      f"{str(rej):>6}  {cmis:4d}  {m1mis:5d}  {pv:7d}  "
                      f"{str(mp):>13}  {d1:6d}")
    print(f"\ncases: {len(out)}   failures: {nfail}")
    with open(a.json, "w") as f:
        json.dump({"cases": out, "failures": nfail, "T": a.T,
                   "rmax": a.rmax, "qmax": a.qmax}, f, indent=1, default=str)


if __name__ == "__main__":
    main()

"""Left-extension sweep: does a ladder witness at left depth k survive depth k+1?

For each left depth k, sample accepting mode-(ii) lassos and run the forced
leftward extension past the ladder's own x_min, checking the lone-seed wedge
(col_x(t) = 0 for t < |x|, col_x(|x|) = 1) at every deeper column.

Rule 90 filter: the identical sweep is run on the rule-90 ladder with its own
true eventually-zero centre word (w = 0), whose language provably CONTAINS a
genuine realizable word (the true rule-90 lone-seed word, which the control in
extend_probe.py confirms survives to depth 24).  If rule 90's sampled witnesses
die at exactly the same place as rule 30's, the measurement is about random
lassos in an over-approximation, not about Rule 30.
"""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter

import extend_probe as EP

Params = EP.Params


def sweep(rule: int, word: str, q: int, R: int, ks, n: int, D: int, seed: int,
          max_states: int = 3_000_000):
    rows = []
    for k in ks:
        rng = random.Random(seed + 1000 * k)
        P = Params(rule=rule, right_depth=R, left_depth=k,
                   period_word=tuple(int(c) for c in word), diff_q=q)
        try:
            lassos = EP.sample_lassos(P, n, rng, max_states)
        except AssertionError as e:
            rows.append({"rule": rule, "w": word, "k": k, "error": str(e)})
            continue
        T = R + 2 * D + 80
        depths, reasons, cyc = [], [], []
        for wt in lassos:
            wd = EP.lasso_word(wt["prefix"], wt["cycle"], T)
            d, det = EP.left_reach(wd, R, rule, D)
            depths.append(d)
            reasons.append(det.get("stopped"))
            cyc.append(len(wt["cycle"]))
        rows.append({
            "rule": rule, "w": word, "q": q, "R": R, "k": k,
            "x_min": P.x_min,
            "n_sampled": len(lassos),
            "depth_hist": sorted(Counter(depths).items()),
            "max_depth_reached": max(depths) if depths else None,
            "min_depth_reached": min(depths) if depths else None,
            "reasons": sorted(Counter(reasons).items(), key=lambda z: str(z[0])),
            "cycle_len_hist": sorted(Counter(cyc).items()),
        })
        print(json.dumps(rows[-1]), flush=True)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-R", type=int, default=2)
    ap.add_argument("--kmax", type=int, default=5)
    ap.add_argument("-n", type=int, default=60)
    ap.add_argument("-D", type=int, default=24)
    ap.add_argument("--seed", type=int, default=20260905)
    ap.add_argument("--max-states", type=int, default=3_000_000)
    args = ap.parse_args()
    ks = list(range(1, args.kmax + 1))
    out = {
        "args": vars(args),
        "rule30_p2": sweep(30, "01", 1, args.R, ks, args.n, args.D,
                           args.seed, args.max_states),
        "rule90_control_p1": sweep(90, "0", 1, args.R, ks, args.n, args.D,
                                   args.seed, args.max_states),
        "rule30_p1_calib": sweep(30, "1", 1, args.R, ks, args.n, args.D,
                                 args.seed, args.max_states),
    }
    with open(f"left_sweep_R{args.R}.json", "w") as f:
        json.dump(out, f, indent=1)
    print("written", f"left_sweep_R{args.R}.json")


if __name__ == "__main__":
    main()

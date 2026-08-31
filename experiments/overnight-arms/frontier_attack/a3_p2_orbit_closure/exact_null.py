"""The EXACT reference scale: uniform-Bernoulli probability of each fixed-point patch.

Uniform Bernoulli(1/2) on {0,1}^Z is invariant for Rule 30 (Rule 30 is surjective
on Z; Taati arXiv:1505.06464 sec 2.4).  Under that measure the (2W+1) x H band
patch is determined by the initial row on the cone [-W-H+1, W+H-1], of width
n = 2W + 2H - 1, and every such row has probability 2^-n.  So

    q(W,H) = #{rows of width n producing the patch} / 2^n

is EXACT -- no seeds, no simulation, no burn-in.  This replaces a simulated
ensemble null: iterating Rule 30 on a finite cycle does NOT preserve uniform
Bernoulli (the cyclic map is not surjective), so a long cyclic orbit degenerates
onto an attractor and its patch statistics are not the invariant-measure ones.

Reference scale reported: H*(W,T) = the largest H with T * q(W,H) >= 1, i.e. the
patch height one expects to see in T rows of a uniform-Bernoulli-typical Rule 30
orbit.  The lone-seed diagram's measured heights are compared against it.

The ensemble null is a scale, not evidence: by obstruction B (PATH.md 7.3) an
ensemble statement cannot decide anything about the single lone-seed orbit.

Run:  uv run python exact_null.py [--maxbits 24]
"""

from __future__ import annotations

import argparse
import json
import math
import os

import numpy as np

from band_census import HERE, family_targets


def q_exact(rule: str, w: int, h: int, name: str) -> tuple[int, int]:
    """(number of cone rows producing the patch, 2^n)."""
    n = 2 * w + 2 * h - 1
    bw = 2 * w + 1
    target_row = family_targets(w)[name]
    cur = np.arange(1 << n, dtype=np.uint64)
    mask = np.uint64((1 << n) - 1)
    ok = np.ones(1 << n, dtype=bool)
    for _ in range(h):
        seg = (cur >> np.uint64(h - 1)) & np.uint64((1 << bw) - 1)
        ok &= seg == np.uint64(target_row)
        if rule == "30":
            cur = ((cur << np.uint64(1)) ^ (cur | (cur >> np.uint64(1)))) & mask
        else:
            cur = ((cur << np.uint64(1)) ^ (cur >> np.uint64(1))) & mask
    return int(ok.sum()), 1 << n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--maxbits", type=int, default=24)
    ap.add_argument("--steps", type=int, default=2_000_000)
    args = ap.parse_args()

    out: dict = {"maxbits": args.maxbits, "steps": args.steps, "rule30": {}}
    with open(os.path.join(HERE, "band_census_rule30.json")) as fh:
        bc = json.load(fh)

    for name in ("all_zeros", "checker_A", "checker_B"):
        for w in range(0, 9):
            qs = {}
            hstar = 0
            for h in range(1, 40):
                n = 2 * w + 2 * h - 1
                if n > args.maxbits:
                    break
                c, tot = q_exact("30", w, h, name)
                qs[str(h)] = {"count": c, "of": tot,
                              "q": c / tot,
                              "expected_in_T": args.steps * c / tot}
                if c and args.steps * c / tot >= 1.0:
                    hstar = h
                if c == 0:
                    break
            meas = bc["families"][name][str(w)]["by_horizon"][str(args.steps)][
                "max_height"
            ]
            # The enumeration is capped at n = 2W + 2H - 1 <= maxbits, which
            # truncates H*.  q(W,H+1)/q(W,H) is EXACTLY constant over the whole
            # enumerated range (1/4 for all_zeros, 1/2 for the checkerboards),
            # so extend by that ratio and report H* from the closed form.
            hs = sorted(int(k) for k in qs if qs[k]["q"] > 0)
            ratio = None
            if len(hs) >= 3:
                rs = {round(qs[str(b)]["q"] / qs[str(a)]["q"], 9)
                      for a, b in zip(hs[1:], hs[2:])}
                ratio = rs.pop() if len(rs) == 1 else None
            if ratio:
                hl = hs[-1]
                exp_last = args.steps * qs[str(hl)]["q"]
                hstar_cf = hl + math.floor(math.log(exp_last, 1 / ratio)) \
                    if exp_last >= 1 else hstar
            else:
                hstar_cf = hstar
            out["rule30"][f"{name}_W{w}"] = {
                "q_table": qs,
                "q_ratio_exact": ratio,
                "H_star_enumerated_capped": hstar,
                "H_star_uniform_bernoulli": int(hstar_cf),
                "measured_lone_seed": meas,
                "measured_minus_Hstar": meas - int(hstar_cf),
            }
            print(f"{name:10s} W={w}: q ratio {ratio}, "
                  f"H*(uniform Bernoulli, T={args.steps}) = {int(hstar_cf)},"
                  f"  lone seed = {meas},  diff = {meas - int(hstar_cf)}")

    # decay rate of q in H at fixed W (the per-row cost of holding the patch)
    rates = {}
    for name in ("all_zeros", "checker_A", "checker_B"):
        for w in (0, 1, 2, 3):
            qs = out["rule30"][f"{name}_W{w}"]["q_table"]
            hs = sorted(int(k) for k in qs)
            r = []
            for a, b in zip(hs, hs[1:]):
                if qs[str(a)]["q"] > 0 and qs[str(b)]["q"] > 0:
                    r.append(round(qs[str(b)]["q"] / qs[str(a)]["q"], 5))
            rates[f"{name}_W{w}"] = r
    out["q_ratio_per_extra_row"] = rates
    print("\nq(W,H+1)/q(W,H), the per-row cost of holding the patch:")
    for k, v in rates.items():
        print(f"  {k}: {v}")

    path = os.path.join(HERE, "exact_null.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote", path)


if __name__ == "__main__":
    main()

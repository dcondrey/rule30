"""R4: the one regime every earlier bank replicated rather than extended.

`build_bank` draws random configurations of width 3..16 and unions of two
pieces of width <= 8.  The three "fresh" banks in `inspect_finds.py` use the
SAME generator with different seeds, so they are bigger, not wider.  A width-2
or width-3 artefact that only shows up on long dense rows, or on unions of
many clumps, would survive all of them.

This script closes that gap for every candidate that reached the end of the
triage.  Two new regimes, neither present in any bank:

  W1  DENSE WIDE.  50 uniform random configurations at each of widths
      200, 800 and 2000, checking that `(*)` still admits a well-defined `f`
      jointly with everything seen before.
  W2  MANY CLUMPS.  50 configurations built from 4 to 6 random clumps
      separated by `w+2` zeros.  This re-exercises the homomorphism lemma at
      arity 4-6 rather than the arity 2 the search bank used.

It also reports, for each surviving candidate, the numbers rather than the
booleans: the step-0 `disagreeAB` profile across `W`, labelled by `flatness()`
below, and whether the image submonoid is commutative.

PROVENANCE, stated so the write-up cannot overclaim: R0-R3 in
`inspect_finds.py` were written BEFORE any candidate had been triaged.  This
file (R4) was written AFTER 72 column-sensitive-looking candidates appeared at
`T3, w = 2`, as a targeted attempt to break them.  It is post-hoc and it killed
0 of 2,555.  A post-hoc filter that fails to kill is stronger evidence for the
survivors than a planned one; calling it pre-registered would be both false and
weaker.
"""

from __future__ import annotations

import argparse
import json
import random
import sys

HERE = ("/Volumes/A/researchpapers/13-rule30/experiments/overnight-arms/"
        "frontier_attack/a15_nonabelian_invariant")
sys.path.insert(0, HERE)

from monoids import nonzero_windows, registry  # noqa: E402
from search import pad, phi_value  # noqa: E402
from substrate import random_finite_config, step  # noqa: E402


def wide_pairs(rule, w, rng):
    pairs = []
    for width in (200, 800, 2000):
        for _ in range(50):
            s = random_finite_config(rng, width)
            pairs.append((s, step(s, rule)))
    for _ in range(50):
        s = []
        for i in range(rng.randint(4, 6)):
            if i:
                s += [0] * (w + 2)
            s += random_finite_config(rng, rng.randint(3, 10))
        pairs.append((s, step(s, rule)))
    return [(nonzero_windows(pad(a, w), w), nonzero_windows(pad(b, w), w))
            for a, b in pairs]


def survives(phi, mon, pairs):
    f = {}
    for ws_s, ws_t in pairs:
        a = phi_value(ws_s, phi, mon.mul, mon.n)
        b = phi_value(ws_t, phi, mon.mul, mon.n)
        if f.get(a, b) != b:
            return False, None
        f[a] = b
    return True, f


def flatness(d):
    """Label the step-0 profile WITHOUT claiming a decay law it does not have.

    "zero"            -- 0 at every W: column-blind outright.
    "vanishes_by_W64" -- nonzero only at W = 32, exactly 0 at 64/128/256.  In
                         this arm those nonzeros are one or two rows out of
                         201; that is a couple of rows, NOT a measured 1/W
                         curve, and must not be described as one.
    "FLAT"            -- W=256 value at least half the W=32 value: genuinely
                         column-sensitive, the positive-control shape.
    "intermediate"    -- anything else.
    """
    if not d:
        return "n/a"
    ks = sorted(int(k) for k in d)
    lo, hi = d[str(ks[0])], d[str(ks[-1])]
    if all(v == 0 for v in d.values()):
        return "zero"
    if all(d[str(k)] == 0 for k in ks if k >= 64):
        return "vanishes_by_W64"
    if hi >= 0.5 * lo:
        return "FLAT"
    return "intermediate"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--triage", nargs="*",
                    default=[f"{HERE}/finds_triage.json"])
    ap.add_argument("--out", default=f"{HERE}/stress_wide.json")
    args = ap.parse_args()

    reg = registry()
    # DEDUPE.  results.jsonl and results_strict.jsonl re-run the SAME sampled
    # cells with the same seed and budget, so the first file's 40 stored finds
    # are literally the first 40 of the second file's full list.  Loading both
    # without deduping double-counts every sampled cell.
    cand, seen, dupes = [], set(), 0
    for path in args.triage:
        for e in json.load(open(path)):
            if not e.get("R1_fresh_bank"):
                continue
            key = (e["rule"], e["monoid"], e["w"], tuple(e["phi"]))
            if key in seen:
                dupes += 1
                continue
            seen.add(key)
            cand.append(e)
    print(json.dumps({"candidates_entering_R4": len(cand),
                      "duplicates_dropped": dupes}), flush=True)

    cache = {}
    groups = {}
    for e in cand:
        key = (e["rule"], e["monoid"], e["w"])
        groups.setdefault(key, []).append(e)

    out = []
    for (rule, mname, w), es in sorted(groups.items()):
        mon = reg[mname]
        if (rule, w) not in cache:
            cache[(rule, w)] = wide_pairs(rule, w, random.Random(31337))
        pairs = cache[(rule, w)]
        kept = []
        for e in es:
            ok, f = survives(tuple(e["phi"]), mon, pairs)
            e["R4_wide_ok"] = ok
            if ok:
                e["R4_f"] = {str(k): v for k, v in sorted(f.items())}
                e["R2_flatness"] = flatness(e.get("R2_step0_disagreeAB"))
                kept.append(e)
            out.append(e)
        flat = sum(1 for e in kept if e["R2_flatness"] == "FLAT")
        dec = sum(1 for e in kept if e["R2_flatness"] == "vanishes_by_W64")
        zer = sum(1 for e in kept if e["R2_flatness"] == "zero")
        comm = sum(1 for e in kept if e.get("T4_commutative_image"))
        nonid = sum(1 for e in kept
                    if any(int(k) != v for k, v in e["R4_f"].items()))
        print(json.dumps({
            "rule": rule, "monoid": mname, "w": w,
            "entering": len(es), "R4_wide_survivors": len(kept),
            "R4_killed": len(es) - len(kept),
            "step0_FLAT": flat, "step0_vanishes_by_W64": dec,
            "step0_zero": zer,
            "commutative_image": comm,
            "f_not_identity": nonid,
            "max_orbit_bits": max((e.get("R3_orbit_bits", 0) for e in kept),
                                  default=None)}), flush=True)
    json.dump(out, open(args.out, "w"), indent=1)
    tot = sum(1 for e in out if e.get("R4_wide_ok"))
    print(json.dumps({"TOTAL_entering_R4": len(cand),
                      "TOTAL_surviving_R4": tot}), flush=True)


if __name__ == "__main__":
    main()

"""Summarise the search, and test the sharp prediction the null hypothesis makes.

THE PREDICTION (derived here, and falsifiable).  Let `G` be a GROUP of order
`g`.  For any `h: {0,1}^{w-1} -> G` the "coboundary"

    phi(v) = h(v_0..v_{w-2}) * h(v_1..v_{w-1})^{-1}

telescopes along the row, because the right factor of window `x` and the left
factor of window `x+1` are the SAME word: the product collapses to
`h(0^{w-1}) * h(0^{w-1})^{-1} = e` on every finite-support configuration.  So
every coboundary is a conserved transfer invariant with `Phi == e`, i.e. a
T1-constant one.  The map `h -> phi` has kernel exactly the constants, so there
are `g^(2^(w-1) - 1)` of them.  Note this construction needs inverses and so is
stated for groups only; the non-group monoids `T2`, `T3`, `FlipFlop3` are
reported as measured.

Therefore, if there is NOTHING beyond the coboundaries:

    survivors(rule, G, w)  ==  g ** (2**(w-1) - 1)      and all are T1-constant.

Any excess is a genuine find; any shortfall is a bug.  For `G = Z2` and `Z3`
this number is exactly a14's finite-support dimension `2^(w-1) - 1` re-derived
in a completely different way (product form, no linear algebra, no de Bruijn
graph), so agreement is an independent cross-validation between the two arms.
For `Z4`, `Z5`, `Z6`, `Z2xZ2` and `S3` it is NEW: a14 section 6 lists composite
`Z/m` and primes past 3 as outside its bound.
"""

from __future__ import annotations

import json
import sys

HERE = ("/Volumes/A/researchpapers/13-rule30/experiments/overnight-arms/"
        "frontier_attack/a15_nonabelian_invariant")
sys.path.insert(0, HERE)
from monoids import registry  # noqa: E402


def load(path):
    return [json.loads(l) for l in open(path)]


def main():
    reg = registry()
    rows = load(f"{HERE}/results.jsonl")
    ctrl = load(f"{HERE}/control_battery.jsonl")

    print("=" * 100)
    print("MAIN SEARCH -- Rule 30 and the Rule 90 filter")
    print("=" * 100)
    hdr = (f"{'rule':>4} {'monoid':>10} {'w':>2} {'mode':>10} {'candidates':>12} "
           f"{'surv':>8} {'verif':>7} {'T1':>7} {'T3':>7} {'FIND':>5} {'STRICT':>6} "
           f"{'predicted':>10} {'match':>8} {'E[coboundary hits]':>18}")
    print(hdr)
    total_find = 0
    mismatches = []
    powerless = 0
    for r in rows:
        mon = reg[r["monoid"]]
        pred = match = ""
        power = ""
        if mon.is_group:
            # Rule 30's prediction is the coboundary count.  Rule 90 additionally
            # admits every phi valued in G[2] = {g : g^2 = e} (each cell feeds
            # exactly two successor cells, so those cancel in pairs and Phi(F(s))
            # is identically e -- a COLLAPSING invariant, f the constant map).
            # rule90_extras.py verifies both the count identity and the collapse.
            g2 = sum(1 for a in range(mon.n) if mon.mul[a * mon.n + a] == 0)
            p = mon.n ** (2 ** (r["w"] - 1) - 1) * (g2 if r["rule"] == 90 else 1)
            if r["mode"] == "exhaustive":
                pred = str(p)
                match = "OK" if p == r["survivors"] else "MISMATCH"
                if match == "MISMATCH":
                    mismatches.append((r["rule"], mon.name, r["w"],
                                       r["survivors"], p))
            else:
                # POWER CALIBRATION: expected number of the KNOWN-trivial
                # coboundaries a uniform sample of this size would land on.
                # Much below 1 means the cell cannot detect even what is there,
                # so its zero is uninformative and is reported as such.
                e = r["candidates"] * p / mon.n ** ((1 << r["w"]) - 1)
                power = f"{e:.3g}"
                if e < 1:
                    powerless += 1
        total_find += r["nontrivial"]
        print(f"{r['rule']:>4} {r['monoid']:>10} {r['w']:>2} {r['mode']:>10} "
              f"{r['candidates']:>12} {r['survivors']:>8} {r['verified_survivors']:>7} "
              f"{r['T1_constant']:>7} {r['T3_end_reader']:>7} "
              f"{r['nontrivial']:>5} {r['nontrivial_strict']:>6} {pred:>10} "
              f"{match:>8} {power:>18}")

    print()
    print("CONTROLS -- 204 identity, 170 shift (saturation); 184 number-conserving")
    print(f"{'rule':>4} {'monoid':>10} {'w':>2} {'candidates':>10} {'surv':>8} "
          f"{'verif':>8} {'FIND':>6} {'noncomm_find':>13}")
    ctrl_find = {}
    for r in ctrl:
        nc = r["nontrivial"] - r["T4_commutative_image"] if r["nontrivial"] else 0
        ctrl_find.setdefault(r["rule"], 0)
        ctrl_find[r["rule"]] += r["nontrivial"]
        print(f"{r['rule']:>4} {r['monoid']:>10} {r['w']:>2} {r['candidates']:>10} "
              f"{r['survivors']:>8} {r['verified_survivors']:>8} {r['nontrivial']:>6} "
              f"{max(nc, 0):>13}")

    print()
    print("-" * 100)
    sat = [r for r in ctrl if r["rule"] in (204, 170)]
    sat_ok = all(r["survivors"] == r["candidates"] for r in sat)
    r184 = [r for r in ctrl if r["rule"] == 184]
    r184_proper = any(r["survivors"] < r["candidates"] for r in r184)
    r184_finds = sum(r["nontrivial"] for r in r184)
    r184_noncomm = sum(max(r["nontrivial"] - r["T4_commutative_image"], 0)
                       for r in r184 if not reg[r["monoid"]].is_commutative)
    print(f"saturation controls (204,170) return every candidate : {sat_ok}")
    print(f"rule 184 returns a PROPER subset                     : {r184_proper}")
    print(f"rule 184 nontrivial invariants found                 : {r184_finds}")
    print(f"  of which with a NON-COMMUTATIVE image (>=)         : {r184_noncomm}")
    print(f"coboundary-count prediction mismatches               : {len(mismatches)}"
          f"  {mismatches}")
    for rule in (30, 90):
        rr = [r for r in rows if r["rule"] == rule]
        grp = [r for r in rr if reg[r["monoid"]].is_group]
        print(f"rule {rule}: strictly-nontrivial candidates, GROUP cells      : "
              f"{sum(r['nontrivial_strict'] for r in grp)}"
              f"   (over {sum(r['candidates'] for r in grp):,} candidates)")
        print(f"rule {rule}: strictly-nontrivial candidates, NON-GROUP cells  : "
              f"{sum(r['nontrivial_strict'] for r in rr if r not in grp)}"
              f"   -> all triaged in inspect_finds.py")
    print(f"RULE 30 / RULE 90 ladder survivors (pre-triage)      : {total_find}")
    print(f"sampled group cells with E[coboundary hits] < 1      : {powerless}"
          f"   (their zeros carry NO information and are not claimed)")
    r30 = {(r['monoid'], r['w']): r for r in rows if r['rule'] == 30}
    r90 = {(r['monoid'], r['w']): r for r in rows if r['rule'] == 90}
    same = sum(1 for k in r30 if k in r90
               and r30[k]["survivors"] == r90[k]["survivors"])
    print(f"(monoid,w) cells where Rule 30 and Rule 90 agree     : {same}/{len(r30)}")
    print(f"total candidates tested                              : "
          f"{sum(r['candidates'] for r in rows):,} (main) + "
          f"{sum(r['candidates'] for r in ctrl):,} (controls)")


if __name__ == "__main__":
    main()

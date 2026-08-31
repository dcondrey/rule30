"""Identify the survivors STRUCTURALLY, not merely by count.

The null hypothesis predicts `|G|^(2^(w-1) - 1)` survivors for a group `G`.
A matching count is suggestive; set equality is decisive.  This script builds
the coboundary set explicitly,

    phi_h(v) = h(v_0..v_{w-2}) * h(v_1..v_{w-1})^{-1},   h: {0,1}^{w-1} -> G,

verifies by direct simulation that each `phi_h` really does give `Phi == e` on
finite-support configurations (the telescoping argument, checked rather than
trusted), and then asserts

    { survivors of the search }  ==  { coboundaries }

as SETS, for both Rule 30 and Rule 90.  If the two sets are equal, the search's
zero is not "nothing was found": it is "exactly the rule-independent trivial
space was found, and nothing else".
"""

from __future__ import annotations

import itertools
import json
import random
import sys

HERE = ("/Volumes/A/researchpapers/13-rule30/experiments/overnight-arms/"
        "frontier_attack/a15_nonabelian_invariant")
sys.path.insert(0, HERE)

from monoids import nonzero_windows, registry  # noqa: E402
from search import (build_bank, build_interior_probes, build_orbit,  # noqa: E402
                    pad, phi_value, test_candidate)
from substrate import random_finite_config  # noqa: E402


def inverses(mon):
    inv = [None] * mon.n
    for a in range(mon.n):
        for b in range(mon.n):
            if mon.mul[a * mon.n + b] == 0:
                inv[a] = b
                break
    assert all(x is not None for x in inv), f"{mon.name} is not a group"
    return inv


def coboundaries(mon, w):
    inv = inverses(mon)
    n, mul = mon.n, mon.mul
    out = set()
    for h in itertools.product(range(n), repeat=1 << (w - 1)):
        phi = [0] * (1 << w)
        for v in range(1 << w):
            left = v >> 1
            right = v & ((1 << (w - 1)) - 1)
            phi[v] = mul[h[left] * n + inv[h[right]]]
        assert phi[0] == 0
        out.add(tuple(phi))
    return out


def survivors(mon, w, rule):
    rng = random.Random(20260830)
    bank = build_bank(rule, w, rng)
    orbit = build_orbit(rule, w)
    probes = build_interior_probes(rule, w, rng)
    out = set()
    for tail in itertools.product(range(mon.n), repeat=(1 << w) - 1):
        phi = (0,) + tail
        ok, _ = test_candidate(phi, mon, bank, orbit, probes)
        if ok:
            out.add(phi)
    return out


def main():
    reg = registry()
    rng = random.Random(77)
    report = []
    for mname, w in (("Z2", 3), ("Z2", 4), ("Z3", 3), ("Z4", 3),
                     ("Z2xZ2", 3), ("Z5", 3), ("Z6", 3), ("S3", 2), ("S3", 3)):
        mon = reg[mname]
        cb = coboundaries(mon, w)
        # the telescoping claim, checked by direct simulation
        bad = 0
        for phi in list(cb)[:60]:
            for _ in range(25):
                s = random_finite_config(rng, rng.randint(1, 18))
                if phi_value(nonzero_windows(pad(s, w), w), phi,
                             mon.mul, mon.n) != 0:
                    bad += 1
        rec = {"monoid": mname, "w": w, "|G|": mon.n,
               "predicted": mon.n ** (2 ** (w - 1) - 1),
               "coboundaries_built": len(cb),
               "telescoping_failures": bad}
        for rule in (30, 90):
            sv = survivors(mon, w, rule)
            rec[f"survivors_rule{rule}"] = len(sv)
            rec[f"set_equal_rule{rule}"] = (sv == cb)
        report.append(rec)
        print(json.dumps(rec), flush=True)

    ok = all(r["telescoping_failures"] == 0 and r["set_equal_rule30"]
             and r["set_equal_rule90"] and r["coboundaries_built"] == r["predicted"]
             for r in report)
    print(json.dumps({"all_cells_identify_exactly_the_coboundary_space": ok,
                      "cells": len(report)}), flush=True)
    with open(f"{HERE}/coboundary_check.json", "w") as fh:
        json.dump(report, fh, indent=1)


if __name__ == "__main__":
    main()

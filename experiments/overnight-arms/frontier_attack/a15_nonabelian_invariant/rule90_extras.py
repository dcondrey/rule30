"""What Rule 90 has that Rule 30 does not, and why it is not a Rule 30 route.

`coboundary_check.py` found, for every group cell tested:

    survivors(Rule 30)  ==  the coboundary set, exactly
    survivors(Rule 90)  >=  the coboundary set, strictly larger whenever `G`
                            has an element of order 2

with the observed ratio equal to `|G[2]|`, `G[2] = {g : g^2 = e}`
(Z2:2, Z3:1, Z4:2, Z2xZ2:4, Z5:1, Z6:2, S3:4).

MECHANISM.  Rule 90 is `s(t+1,x) = s(t,x-1) XOR s(t,x+1)`: every cell of a row
contributes to exactly TWO cells of the successor.  A `phi` whose values all
square to the identity therefore has each contribution cancel in pairs, and
`Phi(F(s)) = e` for every `s` -- a valid transfer invariant with `f` the
CONSTANT map to `e`.  These are degenerate: `f` collapses the whole monoid to
one point in a single step, so the invariant is eventually constant along
every orbit (`T2`), carries 0 bits, and exists only because Rule 90 is
additive over `GF(2)`.

This script checks both halves of that claim:
  (i)  the count identity `|survivors_90| = |coboundaries| * |G[2]|`;
  (ii) every Rule 90 survivor outside the coboundary set has a CONSTANT `f`.

Consequence for PATH.md section 0: the Rule 90 filter here is a live control
that could have failed and did not.  Rule 30's set is the rule-independent
trivial core and nothing more; Rule 90's strict excess is an artefact of its
GF(2)-linearity, which Rule 30 does not have, so it transfers nothing.
"""

from __future__ import annotations

import itertools
import json
import random
import sys

HERE = ("/Volumes/A/researchpapers/13-rule30/experiments/overnight-arms/"
        "frontier_attack/a15_nonabelian_invariant")
sys.path.insert(0, HERE)

from coboundary_check import coboundaries  # noqa: E402
from monoids import registry  # noqa: E402
from search import (build_bank, build_interior_probes, build_orbit,  # noqa: E402
                    test_candidate)


def main():
    reg = registry()
    out = []
    for mname, w in (("Z2", 3), ("Z3", 3), ("Z4", 3), ("Z2xZ2", 3),
                     ("Z5", 3), ("Z6", 3), ("S3", 2), ("S3", 3)):
        mon = reg[mname]
        g2 = [a for a in range(mon.n) if mon.mul[a * mon.n + a] == 0]
        cb = coboundaries(mon, w)
        rng = random.Random(20260830)
        bank = build_bank(90, w, rng)
        orbit = build_orbit(90, w)
        probes = build_interior_probes(90, w, rng)
        surv, extras, collapsing = 0, 0, 0
        for tail in itertools.product(range(mon.n), repeat=(1 << w) - 1):
            phi = (0,) + tail
            ok, rec = test_candidate(phi, mon, bank, orbit, probes)
            if not ok:
                continue
            surv += 1
            if phi not in cb:
                extras += 1
                collapsing += int(len(set(rec["f"].values())) == 1)
        rec = {"monoid": mname, "w": w, "|G|": mon.n, "|G[2]|": len(g2),
               "coboundaries": len(cb), "survivors_rule90": surv,
               "ratio": surv / len(cb),
               "count_identity_holds": surv == len(cb) * len(g2),
               "extras": extras,
               "extras_with_constant_f": collapsing,
               "all_extras_collapse": extras == collapsing}
        out.append(rec)
        print(json.dumps(rec), flush=True)
    print(json.dumps({
        "count_identity_all_cells": all(r["count_identity_holds"] for r in out),
        "every_extra_has_constant_f": all(r["all_extras_collapse"] for r in out),
        "cells": len(out)}), flush=True)
    with open(f"{HERE}/rule90_extras.json", "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()

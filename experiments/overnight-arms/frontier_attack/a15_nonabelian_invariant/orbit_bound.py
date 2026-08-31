"""The width-independent kill: the ORBIT-PHASE BOUND, and its verification.

PROPOSITION (derived, not assumed).  Let `Phi` be any transfer invariant in
the searched class -- any finite monoid `M`, any width `w`, any
`phi: {0,1}^w -> M` with `phi(0^w) = e` -- so that `Phi(F(s)) = f(Phi(s))` for
some `f: M -> M`.  Write `m_0 = Phi(row_0)` for the lone seed.  Then

    Phi(row_t) = f^t(m_0)   for every t.

`f^t(m_0)` is a trajectory of a map of a set of size `|M|` into itself, hence
eventually periodic with preperiod + period <= |M|.  Consequences:

  (a) `Phi(row_t)` is computable in `O(|M|)` work WITHOUT simulating Rule 30.
      It is a function of `t` and the phase alone.
  (b) The invariant's TOTAL information about the whole orbit
      `row_0, row_1, row_2, ...` is at most `log2 |M|` bits: 1 bit for
      `|M| = 2`, 2.585 bits for `|M| = 6`, 4.755 bits for `|M| = 27`.
  (c) The single equation the invariant supplies at row `t` is
          L * phi(window at column 0) * R  =  f^t(m_0),
      with `L` and `R` ordered products over the `~2t` other cells of the row.
      Solving it for column 0 requires `L` and `R`, i.e. requires the rest of
      the row already.  This is the exact-constraint analogue of a14 section
      2.1's support-growth asymmetry, and it is sharper: the total budget is
      named (`<= log2|M|` bits) rather than bounded asymptotically.

The bound is INDEPENDENT of `w` and of `|M|`'s value beyond the logarithm, so
it closes every width past the searched frontier and every monoid, and it is
the arm's verdict.  The exhaustive search is confirmation that there was
nothing to find inside the frontier, never the reason the arm died.

NO CONTRADICTION WITH STEP 0, and this is the seam the reader must see.  Step
0 measures a WINDOWED readout `Phi_W` on a width-`W` window about the centre;
`L` and `R` there are products over unconstrained cells, so `Phi_W` moves when
column 0 moves -- it is not column-blind, and the class passes the PATH.md 0.1
gate.  The searched object is the FULL-ROW product, whose value conservation
pins to `f^t(m_0)`.  Sensitivity of the windowed readout is a necessary
condition that the class satisfies; the orbit-phase bound is the separate,
sufficient reason the full-row object decides nothing.

WHAT THIS SCRIPT VERIFIES
  1. The combinatorial core, EXHAUSTIVELY: for |M| = 6, every one of the
     6^6 = 46656 maps `f: M -> M` and every start, preperiod + period <= 6.
  2. The premise chain on a rule where invariants ACTUALLY EXIST (184): find
     its nontrivial transfer invariants by the same pipeline, then confirm on
     long orbits that `Phi(row_t)` is eventually periodic within the bound and
     measure the realised information content in bits.
  3. The same measurement for Rule 30's surviving invariants.
"""

from __future__ import annotations

import itertools
import json
import math
import sys

HERE = ("/Volumes/A/researchpapers/13-rule30/experiments/overnight-arms/"
        "frontier_attack/a15_nonabelian_invariant")
sys.path.insert(0, HERE)

from monoids import nonzero_windows, registry  # noqa: E402
from search import (build_bank, build_interior_probes, build_orbit, pad,  # noqa: E402
                    phi_value, test_candidate)
from substrate import random_finite_config, step  # noqa: E402

import random  # noqa: E402


def check_core(n):
    """Every map of an n-set to itself: preperiod + period <= n, exhaustively."""
    worst = 0
    for f in itertools.product(range(n), repeat=n):
        for start in range(n):
            seen, x, t = {}, start, 0
            while x not in seen:
                seen[x] = t
                x = f[x]
                t += 1
            worst = max(worst, t)  # preperiod + period
    assert worst <= n, (n, worst)
    return worst


def orbit_profile(phi, mon, rule, seed_bits, w, steps=400):
    vals, bits = [], list(seed_bits)
    for _ in range(steps):
        vals.append(phi_value(nonzero_windows(pad(bits, w), w), phi,
                              mon.mul, mon.n))
        bits = step(bits, rule)
    seen, pre, per = {}, None, None
    for t, v in enumerate(vals):
        if v in seen:
            pre, per = seen[v], t - seen[v]
            break
        seen[v] = t
    distinct = len(set(vals))
    return {"preperiod_plus_period": (pre + per) if pre is not None else None,
            "distinct_values": distinct,
            "information_bits": round(math.log2(distinct), 4),
            "bound_log2_M": round(math.log2(mon.n), 4),
            "head": vals[:20]}


def main():
    out = {}
    print("1. COMBINATORIAL CORE, exhaustive over all maps of an n-set")
    core = {}
    for n in (2, 3, 4, 5, 6):
        core[n] = check_core(n)
        print(f"   n={n}: {n**n:6d} maps, worst preperiod+period = {core[n]} <= {n}  OK")
    out["core"] = core

    reg = registry()
    rng = random.Random(4242)

    print("\n2. PREMISE CHAIN on rule 184, where invariants DO exist")
    rows = []
    for mname, w in (("S3", 2), ("S3", 3), ("Z3", 2)):
        mon = reg[mname]
        bank = build_bank(184, w, random.Random(20260830))
        orbit = build_orbit(184, w)
        probes = build_interior_probes(184, w, random.Random(20260830))
        k = (1 << w) - 1
        found = []
        for tail in itertools.product(range(mon.n), repeat=k):
            phi = (0,) + tail
            ok, rec = test_candidate(phi, mon, bank, orbit, probes)
            if ok and rec["nontrivial"]:
                found.append(phi)
        seeds = [random_finite_config(rng, 11) for _ in range(6)]
        prof = [orbit_profile(p, mon, 184, s, w)
                for p in found[:6] for s in seeds[:2]]
        bad = [p for p in prof if p["preperiod_plus_period"] is None
               or p["preperiod_plus_period"] > mon.n]
        rec = {"monoid": mname, "w": w, "nontrivial_found": len(found),
               "orbits_profiled": len(prof),
               "violations_of_bound": len(bad),
               "max_preperiod_plus_period": max(
                   (p["preperiod_plus_period"] for p in prof), default=None),
               "max_information_bits": max(
                   (p["information_bits"] for p in prof), default=None),
               "bound_log2_M": round(math.log2(mon.n), 4)}
        rows.append(rec)
        print(f"   {mname} w={w}: {len(found):4d} nontrivial invariants; "
              f"{len(prof)} orbits x 400 steps; bound violations = {len(bad)}; "
              f"max preperiod+period = {rec['max_preperiod_plus_period']} "
              f"<= |M| = {mon.n}; max info = "
              f"{rec['max_information_bits']} <= {rec['bound_log2_M']} bits")
    out["rule184"] = rows

    print("\n3. RULE 30's surviving invariants, same measurement")
    r30 = []
    for mname, w in (("Z3", 3), ("S3", 3), ("Z6", 3)):
        mon = reg[mname]
        bank = build_bank(30, w, random.Random(20260830))
        orbit = build_orbit(30, w)
        probes = build_interior_probes(30, w, random.Random(20260830))
        k = (1 << w) - 1
        surv = []
        for tail in itertools.product(range(mon.n), repeat=k):
            phi = (0,) + tail
            ok, _ = test_candidate(phi, mon, bank, orbit, probes)
            if ok:
                surv.append(phi)
        seeds = [random_finite_config(rng, 11) for _ in range(4)]
        prof = [orbit_profile(p, mon, 30, s, w) for p in surv[:8] for s in seeds[:2]]
        info = max((p["information_bits"] for p in prof), default=None)
        rec = {"monoid": mname, "w": w, "survivors": len(surv),
               "orbits_profiled": len(prof), "max_information_bits": info,
               "all_constant": all(p["distinct_values"] == 1 for p in prof)}
        r30.append(rec)
        print(f"   {mname} w={w}: {len(surv):5d} survivors; {len(prof)} orbits; "
              f"max info = {info} bits; every profiled orbit constant = "
              f"{rec['all_constant']}")
    out["rule30"] = r30

    with open(f"{HERE}/orbit_bound.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print("\nwrote orbit_bound.json")


if __name__ == "__main__":
    main()

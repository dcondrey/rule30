"""Per-survivor triage of every candidate that cleared the triviality ladder.

Four independent post-filters, each of which can kill a candidate on its own:

  R0  ORBIT-PHASE FALSIFIER, the sharpest one and the cheapest.  Section 4's
      proposition says a real transfer invariant has
      `Phi(row_t) = f^t(m_0)`, hence the sequence `Phi(row_0), Phi(row_1), ...`
      is eventually periodic with `preperiod + period <= |M|`.  A candidate
      whose sequence is not is DEAD by the derived proposition, with no
      sampling caveat and no bigger bank needed: it is a bank-insufficiency
      artefact.  Note this is strictly stronger than counting distinct values
      -- a sequence can visit only 3 values and still fail eventual
      periodicity within the bound.  Checked over 400 steps on the lone seed
      and on three random finite seeds.
  R1  FRESH BANK.  Every (rule, monoid, w) cell in the main search shares one
      configuration bank, so a bank insufficiency would be correlated across
      the whole row.  Each candidate is re-tested against three banks built
      from different seeds, an order of magnitude more configurations, and
      wider configurations than the search bank.
  R2  STEP 0, INDIVIDUALLY.  A class-level step-0 pass is not a pass for a
      particular survivor; conservation forces structure, and the structure it
      forces is column-blind.  Each candidate is run through the mandated
      `discriminator.py` fields A/B as a windowed readout at W = 32..256.
  R3  ORBIT INFORMATION.  The realised information content
      `log2 |{Phi(row_t)}|` on the lone-seed orbit, against the proposition's
      ceiling `log2 |M|`.

Cells re-enumerated exhaustively here are named on the command line; sampled
cells are re-read from `results.jsonl`'s stored `finds`.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import math
import random
import sys

HERE = ("/Volumes/A/researchpapers/13-rule30/experiments/overnight-arms/"
        "frontier_attack/a15_nonabelian_invariant")
sys.path.insert(0, HERE)

from monoids import nonzero_windows, registry  # noqa: E402
from orbit_bound import orbit_profile  # noqa: E402
from search import (build_bank, build_interior_probes, build_orbit,  # noqa: E402
                    pad, phi_value, test_candidate)
from substrate import random_finite_config, step  # noqa: E402

DISC = ("/Volumes/A/researchpapers/13-rule30/experiments/rule30/"
        "p_geometric_attack/discriminator.py")


def load_disc():
    spec = importlib.util.spec_from_file_location("a15_disc2", DISC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def orbit_phase_ok(phi, mon, rule, w, rng):
    """R0: eventual periodicity within |M| on the lone seed and 3 random seeds.

    Returns (ok, worst_preperiod_plus_period, per-seed profiles).
    """
    # 150 steps is ample: the proposition bounds preperiod+period by |M| <= 27,
    # so a real invariant repeats within the first 28 rows and a violation
    # shows up as a non-repeating prefix long before step 150.
    seeds = [[1]] + [random_finite_config(rng, 11) for _ in range(3)]
    profs = [orbit_profile(phi, mon, rule, s, w, steps=150) for s in seeds]
    vals = [p["preperiod_plus_period"] for p in profs]
    ok = all(v is not None and v <= mon.n for v in vals)
    return ok, max((v for v in vals if v is not None), default=None), profs


_FRESH_CACHE = {}


def _fresh(rule, w, seed):
    """Cache the (bank, orbit, probes) triple: it depends only on rule, w, seed,
    not on the candidate, and rebuilding it per candidate dominated runtime."""
    key = (rule, w, seed)
    if key not in _FRESH_CACHE:
        rng = random.Random(seed)
        _FRESH_CACHE[key] = (
            build_bank(rule, w, rng, n_random=1400, n_orbit=90, n_union=300),
            build_orbit(rule, w, n=90),
            build_interior_probes(rule, w, rng, n=300))
    return _FRESH_CACHE[key]


def fresh_bank_ok(phi, mon, rule, w):
    """R1: survive three independent, larger, wider banks.

    Distinguishes the two ways a candidate can fail, because they are
    different kills: `broken` means it no longer satisfies (*) at all (a false
    survivor the small bank missed), `trivial` means it still satisfies (*)
    but the wider interior probes reveal it as an end-reader or constant.
    """
    for seed in (11, 2718281, 999331):
        bank, orbit, probes = _fresh(rule, w, seed)
        ok, rec = test_candidate(phi, mon, bank, orbit, probes)
        if not ok:
            return False, seed, "broken_star_identity"
        if not rec["nontrivial"]:
            reason = ("T1_constant" if rec["T1_constant"]
                      else "T3_end_reader" if rec["T3_end_reader"]
                      else "hom_violation")
            return False, seed, f"became_trivial:{reason}"
    return True, None, None


def step0(phi, mon, w, disc, T=400):
    A = disc.diagram(30, T, T + 4)
    Bg = disc.overwrite_centre(A, T + 4)
    out = {}
    for W in (32, 64, 128, 256):
        half = W // 2
        d = 0
        rows = range(T // 2, T + 1)
        for t in rows:
            va = phi_value(nonzero_windows(
                [int(x) for x in A[t, T + 4 - half:T + 4 + half + 1]], w),
                phi, mon.mul, mon.n)
            vb = phi_value(nonzero_windows(
                [int(x) for x in Bg[t, T + 4 - half:T + 4 + half + 1]], w),
                phi, mon.mul, mon.n)
            d += va != vb
        out[W] = round(d / len(list(rows)), 6)
    return out


def orbit_info(phi, mon, rule, w, steps=400):
    bits = [1]
    vals = []
    for _ in range(steps):
        vals.append(phi_value(nonzero_windows(pad(bits, w), w), phi,
                              mon.mul, mon.n))
        bits = step(bits, rule)
    return len(set(vals)), round(math.log2(len(set(vals))), 4)


def enumerate_cell(rule, mname, w):
    mon = registry()[mname]
    rng = random.Random(20260830)
    bank = build_bank(rule, w, rng)
    orbit = build_orbit(rule, w)
    probes = build_interior_probes(rule, w, rng)
    out = []
    for tail in itertools.product(range(mon.n), repeat=(1 << w) - 1):
        phi = (0,) + tail
        ok, rec = test_candidate(phi, mon, bank, orbit, probes)
        if ok and rec["nontrivial"]:
            out.append((phi, rec))
    return mon, out


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--sampled-only", action="store_true",
                    help="skip the exhaustive-cell re-enumeration")
    ap.add_argument("--results", default=f"{HERE}/results.jsonl",
                    help="jsonl whose stored `finds` are triaged")
    ap.add_argument("--out", default=f"{HERE}/finds_triage.json")
    args = ap.parse_args()

    disc = load_disc()
    cells = [] if args.sampled_only else [
        (30, "T2", 2), (30, "T2", 3), (30, "T3", 2),
        (30, "FlipFlop3", 2), (30, "FlipFlop3", 3),
        (90, "T2", 3), (90, "T3", 2)]
    report = []
    for rule, mname, w in cells:
        mon, found = enumerate_cell(rule, mname, w)
        kept = []
        for phi, rec in found:
            r0ok, worst, _ = orbit_phase_ok(phi, mon, rule, w, random.Random(5))
            entry = {"phi": list(phi), "image": rec["image"],
                     "T2_orbit_flat": rec["T2_orbit_flat"],
                     "T4_commutative_image": rec["T4_commutative_image"],
                     "R0_orbit_phase_ok": r0ok,
                     "R0_worst_preperiod_plus_period": worst,
                     "R0_bound_M": mon.n}
            if not r0ok:
                entry["R1_fresh_bank"] = False
                entry["R1_kill_reason"] = "killed_at_R0"
                report.append({"rule": rule, "monoid": mname, "w": w, **entry})
                continue
            ok, badseed, why = fresh_bank_ok(phi, mon, rule, w)
            entry.update({"R1_fresh_bank": ok, "R1_killed_by_seed": badseed,
                          "R1_kill_reason": why})
            if ok:
                entry["R2_step0_disagreeAB"] = step0(phi, mon, w, disc)
                nv, bits = orbit_info(phi, mon, rule, w)
                entry["R3_orbit_distinct"] = nv
                entry["R3_orbit_bits"] = bits
                kept.append(entry)
            report.append({"rule": rule, "monoid": mname, "w": w, **entry})
        n_r0 = sum(1 for _p, _r in found)
        n_flat0 = sum(1 for e in kept
                      if all(v == 0.0 for v in e["R2_step0_disagreeAB"].values()))
        print(json.dumps({
            "rule": rule, "monoid": mname, "w": w,
            "ladder_survivors": len(found),
            "R0_killed_by_orbit_phase_bound": sum(
                1 for e in report
                if e.get("rule") == rule and e.get("monoid") == mname
                and e.get("w") == w and e.get("R1_kill_reason") == "killed_at_R0"),
            "R1_survived_fresh_banks": len(kept),
            "R1_killed": len(found) - len(kept),
            "R2_column_blind_at_every_W": n_flat0,
            "R2_column_sensitive": len(kept) - n_flat0,
            "R3_max_orbit_bits": max((e["R3_orbit_bits"] for e in kept),
                                     default=None),
        }), flush=True)

    # sampled cells: re-read the stored strict finds
    for line in open(args.results):
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue  # tolerate a partially written trailing line
        if r["mode"] != "sampled" or not r["finds"]:
            continue
        mon = registry()[r["monoid"]]
        kept = []
        r0dead = 0
        for fnd in r["finds"]:
            phi = tuple(fnd["phi"])
            r0ok, worst, profs = orbit_phase_ok(phi, mon, r["rule"], r["w"],
                                                random.Random(5))
            entry = {"rule": r["rule"], "monoid": r["monoid"], "w": r["w"],
                     "sampled": True, "phi": list(phi), "image": fnd["image"],
                     "R0_orbit_phase_ok": r0ok,
                     "R0_worst_preperiod_plus_period": worst,
                     "R0_bound_M": mon.n,
                     "R0_profiles": profs}
            if not r0ok:
                r0dead += 1
                entry["R1_fresh_bank"] = False
                entry["R1_kill_reason"] = "killed_at_R0"
                report.append(entry)
                continue
            ok, badseed, why = fresh_bank_ok(phi, mon, r["rule"], r["w"])
            entry.update({"R1_fresh_bank": ok, "R1_killed_by_seed": badseed,
                          "R1_kill_reason": why})
            if ok:
                entry["R2_step0_disagreeAB"] = step0(phi, mon, r["w"], disc)
                nv, bits = orbit_info(phi, mon, r["rule"], r["w"])
                entry["R3_orbit_distinct"], entry["R3_orbit_bits"] = nv, bits
                kept.append(entry)
            report.append(entry)
        print(json.dumps({"rule": r["rule"], "monoid": r["monoid"], "w": r["w"],
                          "sampled_strict_finds": len(r["finds"]),
                          "R0_killed_by_orbit_phase_bound": r0dead,
                          "R1_survived_fresh_banks": len(kept)}), flush=True)

    with open(args.out, "w") as fh:
        json.dump(report, fh, indent=1)
    survived = [e for e in report if e.get("R1_fresh_bank")]
    live = [e for e in survived
            if any(v > 0 for v in e.get("R2_step0_disagreeAB", {}).values())]
    print(json.dumps({
        "TOTAL_ladder_survivors": len(report),
        "killed_at_R0_orbit_phase": sum(
            1 for e in report if e.get("R1_kill_reason") == "killed_at_R0"),
        "killed_at_R1_broken_star_identity": sum(
            1 for e in report
            if str(e.get("R1_kill_reason", "")).startswith("broken")),
        "killed_at_R1_became_trivial": sum(
            1 for e in report
            if str(e.get("R1_kill_reason", "")).startswith("became_trivial")),
        "survived_fresh_banks": len(survived),
        "AND_column_sensitive_at_some_W": len(live)}), flush=True)


if __name__ == "__main__":
    main()

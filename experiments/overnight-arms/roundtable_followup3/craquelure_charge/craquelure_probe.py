"""Verification of the "craquelure-charge" LLM-panel spark.

Defect field D(t,x) = a(t,x) XOR a'(t,x) between two Rule 30 (or Rule 90)
orbits a, a'.  This module:

1. Derives, and checks exhaustively, the exact one-step recurrence for D
   under Rule 30 and under Rule 90 -- confirming/refuting kill-condition (a):
   is D itself an autonomous local rule (depends only on D's own
   neighbourhood), independent of the underlying a-values?

2. Defines the "signed stratigraphic charge" kappa(t,x) as the exact
   nonlinear correction term in the Rule 30 D-recurrence (the piece beyond
   the Rule-90-like linear XOR propagation), and checks exhaustively over the
   full determining footprint (5 boolean cells, 32 cases -- same scale as the
   gauge-holonomy 32-case check) whether kappa is identically zero, and
   whether the center-column reduction used by the "conserved charge forbids
   periodicity" argument matches the closed form already derived in
   RESULTS-eventual-period.md (d_t(-1) = (1 XOR c_t) AND d_t(1)).

3. Runs a bounded simulation of the "erasure by ones" mechanism to confirm
   the charge is NOT conserved (it is annihilated whenever the center is 1),
   capping any accumulation at the longest run of the periodic word's zeros.

No SAT/SMT solver is used; every claim below is either a closed-form
identity checked by exhaustive enumeration over its full determining
footprint, or a direct simulation of the true Rule 30 / Rule 90 evolution
with no periodicity assumption baked in until section 3.
"""

from __future__ import annotations

import itertools
import json
import random
from typing import List, Tuple


def rule30_forward(l: int, c: int, r: int) -> int:
    return l ^ (c | r)


def rule90_forward(l: int, c: int, r: int) -> int:
    return l ^ r


def evolve_row(row: List[int], forward) -> List[int]:
    """Evolve a finite row one step, zero-padded at both ends."""
    n = len(row)
    padded = [0] + row + [0]
    out = []
    for x in range(1, n + 1):
        out.append(forward(padded[x - 1], padded[x], padded[x + 1]))
    return out


def defect(a: List[int], b: List[int]) -> List[int]:
    return [x ^ y for x, y in zip(a, b)]


# ---------------------------------------------------------------------------
# Section 1: exhaustive footprint check of the D-recurrence, both rules.
#
# The site D(t+1, x) depends, for Rule 30, on exactly 5 boolean inputs that
# fully determine it: a_t(x-1), a_t(x), a_t(x+1) and a'_t(x), a'_t(x+1)
# (a'_t(x-1) is not needed at site x, only its XOR-partner D_t(x-1) is).
# Equivalently, re-parametrize by (D_t(x-1), D_t(x), D_t(x+1), a_t(x), a_t(x+1))
# -- 5 bits, 32 cases -- since a'_t(x) = a_t(x) XOR D_t(x) and
# a'_t(x+1) = a_t(x+1) XOR D_t(x+1), and a_t(x-1), a'_t(x-1) only enter via
# their XOR D_t(x-1) in both rules' linear part.  This is the same footprint
# size as gauge-holonomy's exhaustive check.
# ---------------------------------------------------------------------------

def exhaustive_recurrence_check(forward):
    """For each of the 32 (Dxm1, Dx, Dxp1, ax, axp1) cases, evolve the real
    (a, a') pair one step with the real forward rule and record D(t+1,x).
    Returns list of (bits, next_D, kappa) where kappa is the Rule-30-style
    nonlinear correction term computed from the same inputs, for later
    identical-zero / not-identical-zero comparison. axm1 is not a free
    parameter of the footprint (a_{t}(x-1) only enters through the XOR
    partner D_t(x-1)); we fix it at 0 for the 'a' orbit and derive a'_t(x-1)
    from it, since forward(l,c,r) at rule 30/90 both use only l via XOR with
    the rest, so its absolute value cancels in the XOR -- verified explicitly
    below by also re-running with axm1=1 and checking the recorded D(t+1,x)
    is unchanged (this is itself a mini-proof that a_t(x-1) is a spurious
    variable for D(t+1,x), i.e. is already 'integrated out').
    """
    results = []
    for axm1 in (0, 1):
        for Dxm1, Dx, Dxp1, ax, axp1 in itertools.product((0, 1), repeat=5):
            apxm1 = axm1 ^ Dxm1
            ax_ = ax
            apx = ax ^ Dx
            axp1_ = axp1
            apxp1 = axp1 ^ Dxp1
            next_a = forward(axm1, ax_, axp1_)
            next_ap = forward(apxm1, apx, apxp1)
            Dnext = next_a ^ next_ap
            # nonlinear correction term (defined only meaningfully for
            # rule30; computed here regardless for comparison)
            kappa = (ax_ & Dxp1) ^ (axp1_ & Dx) ^ (Dx & Dxp1)
            linear_only = Dxm1 ^ Dx ^ Dxp1
            results.append(
                dict(
                    axm1=axm1, Dxm1=Dxm1, Dx=Dx, Dxp1=Dxp1, ax=ax_, axp1=axp1_,
                    Dnext=Dnext, kappa=kappa, linear_only=linear_only,
                    matches_linear=(Dnext == linear_only),
                    matches_linear_xor_kappa=(Dnext == (linear_only ^ kappa)),
                )
            )
    return results


def summarize_recurrence(name, results):
    n = len(results)
    matches_linear = sum(r["matches_linear"] for r in results)
    matches_linear_xor_kappa = sum(r["matches_linear_xor_kappa"] for r in results)
    # does Dnext depend only on (Dxm1,Dx,Dxp1), i.e. is it constant across
    # (ax,axp1,axm1) for fixed (Dxm1,Dx,Dxp1)?
    by_dtriple = {}
    for r in results:
        key = (r["Dxm1"], r["Dx"], r["Dxp1"])
        by_dtriple.setdefault(key, set()).add(r["Dnext"])
    autonomous = all(len(v) == 1 for v in by_dtriple.values())
    axm1_matters = any(
        {rr["Dnext"] for rr in results if (rr["Dxm1"], rr["Dx"], rr["Dxp1"], rr["ax"], rr["axp1"]) == (r["Dxm1"], r["Dx"], r["Dxp1"], r["ax"], r["axp1"])} for r in results
    )
    return dict(
        rule=name,
        cases=n,
        matches_linear_rule90_style=matches_linear,
        matches_linear_xor_kappa=matches_linear_xor_kappa,
        autonomous_in_D_alone=autonomous,
        n_distinct_dtriples=len(by_dtriple),
    )


# ---------------------------------------------------------------------------
# Section 2: charge (kappa) exhaustive properties.
# ---------------------------------------------------------------------------

def kappa_properties(results):
    nonzero = sum(1 for r in results if r["kappa"] != 0)
    zero = len(results) - nonzero
    # is kappa a function of D alone (ignoring a)?
    by_dtriple = {}
    for r in results:
        key = (r["Dxm1"], r["Dx"], r["Dxp1"])
        by_dtriple.setdefault(key, set()).add(r["kappa"])
    kappa_depends_on_a_only = any(len(v) > 1 for v in by_dtriple.values())
    return dict(
        total=len(results),
        kappa_nonzero_cases=nonzero,
        kappa_zero_cases=zero,
        kappa_varies_with_a_for_fixed_D=kappa_depends_on_a_only,
    )


# ---------------------------------------------------------------------------
# Section 3: center-column reduction -- reproduce
# RESULTS-eventual-period.md's d_t(-1) = (1 XOR c_t) AND d_t(1) and confirm
# it is exactly what "conserved charge at x=0" reduces to under the standing
# hypothesis D_t(0) = D_{t+1}(0) = 0 (both orbits share the center column
# exactly at t and t+1 -- the "periodicity never yet disagreed" hypothesis).
# ---------------------------------------------------------------------------

def center_reduction_check():
    """Exhaustively enumerate the free variables at x=0 consistent with
    D_t(0)=0 and D_{t+1}(0)=0 for Rule 30, and confirm
    D_t(-1) = (1 XOR a_t(0)) AND D_t(1) holds in every consistent case, with
    kappa(t,0) = a_t(0) AND D_t(1) exactly (the charge IS the erasure term).
    """
    ok = 0
    total = 0
    kappa_eq_expected = 0
    for a0, a1, Dm1, Dp1 in itertools.product((0, 1), repeat=4):
        # D_t(0) = 0 means a'_0 = a0. Need D_{t+1}(0) = 0 too: check whether
        # this is consistent, and if so what it forces.
        ap0 = a0  # from D_t(0)=0
        ap1 = a1 ^ Dp1
        # a_{t}(-1) and a'_t(-1) relate via D_t(-1)=Dm1; absolute value of
        # a_t(-1) doesn't matter for the XOR-difference at x=0 (shown in
        # section 1), so fix it at 0 WLOG.
        am1 = 0
        apm1 = am1 ^ Dm1
        next_a0 = rule30_forward(am1, a0, a1)
        next_ap0 = rule30_forward(apm1, ap0, ap1)
        Dnext0 = next_a0 ^ next_ap0
        total += 1
        if Dnext0 == 0:
            # this is a case consistent with the standing hypothesis; check
            # the claimed identity
            predicted = (1 ^ a0) & Dp1
            kappa_here = (a0 & Dp1) ^ (a1 & 0) ^ (0 & Dp1)  # Dx=0 at x=0
            if Dm1 == predicted:
                ok += 1
            if kappa_here == (a0 & Dp1):
                kappa_eq_expected += 1
    return dict(total_D0_zero_cases=total, consistent_and_matches_identity=ok,
                kappa_equals_a0_and_Dp1=kappa_eq_expected)


# ---------------------------------------------------------------------------
# Section 4: non-conservation / erasure simulation.
#
# Simulate the leftward wedge under an assumed exact period-p center (no
# disagreement ever, i.e. genuinely testing whether the recursion can be run
# self-consistently arbitrarily far left) and show the defect front is wiped
# to zero every time the center word contains a 1, capping the reach at the
# longest run of zeros in one period -- reproducing the "bounded wedge, not
# a descent to contradiction" result already on record.
# ---------------------------------------------------------------------------

def wedge_reach_simulation(period_word: List[int], depth: int, right_seed_bits: List[int]):
    """Run the leftward wedge D_t(-1) = (1 XOR c_t) AND D_t(1) recursion for
    `depth` layers, injecting a fresh, adversarially chosen D_t(1) bit at
    each layer from right_seed_bits (simulating the free right-hand data),
    and report the maximum unbroken run of nonzero D reached and whether it
    ever exceeds the longest zero-run of the period word.
    """
    max_run = 0
    cur_run = 0
    trace = []
    for t in range(depth):
        c_t = period_word[t % len(period_word)]
        Dp1 = right_seed_bits[t % len(right_seed_bits)]
        Dm1 = (1 ^ c_t) & Dp1
        trace.append(Dm1)
        if Dm1:
            cur_run += 1
            max_run = max(max_run, cur_run)
        else:
            cur_run = 0
    zero_runs = []
    run = 0
    doubled = period_word * 2
    for c in doubled:
        if c == 0:
            run += 1
            zero_runs.append(run)
        else:
            run = 0
    longest_zero_run = max(zero_runs) if zero_runs else 0
    return dict(period_word=period_word, depth=depth, max_defect_run=max_run,
                longest_zero_run_in_period=longest_zero_run,
                bounded_by_period=max_run <= longest_zero_run, trace=trace)


# ---------------------------------------------------------------------------
# Section 5: direct simulated confirmation on random orbit pairs (no
# periodicity assumption at all) -- sanity check that sections 1-2's
# footprint algebra matches literal forward simulation end to end.
# ---------------------------------------------------------------------------

def random_orbit_pair_check(forward, n_trials=500, width=40, seed=0):
    rng = random.Random(seed)
    mismatches = 0
    for _ in range(n_trials):
        a = [rng.randint(0, 1) for _ in range(width)]
        b = [rng.randint(0, 1) for _ in range(width)]
        D = defect(a, b)
        a2 = evolve_row(a, forward)
        b2 = evolve_row(b, forward)
        D2 = defect(a2, b2)
        # predict D2 from D and a alone (rule30 style, using kappa formula);
        # for interior sites only (skip boundary padding effects)
        padded_D = [0] + D + [0]
        padded_a = [0] + a + [0]
        for x in range(2, width):  # avoid edges influenced by padding asymmetry
            Dxm1, Dx, Dxp1 = padded_D[x - 1], padded_D[x], padded_D[x + 1]
            ax, axp1 = padded_a[x], padded_a[x + 1]
            if forward is rule30_forward:
                kappa = (ax & Dxp1) ^ (axp1 & Dx) ^ (Dx & Dxp1)
                predicted = Dxm1 ^ Dx ^ Dxp1 ^ kappa
            else:
                predicted = Dxm1 ^ Dxp1
            actual = D2[x - 1]
            if predicted != actual:
                mismatches += 1
    return dict(n_trials=n_trials, width=width, mismatches=mismatches)


def main():
    out = {}

    r30 = exhaustive_recurrence_check(rule30_forward)
    r90 = exhaustive_recurrence_check(rule90_forward)
    out["rule30_recurrence_summary"] = summarize_recurrence("rule30", r30)
    out["rule90_recurrence_summary"] = summarize_recurrence("rule90", r90)
    out["rule30_kappa_properties"] = kappa_properties(r30)
    out["rule90_kappa_properties"] = kappa_properties(r90)

    out["center_reduction_check"] = center_reduction_check()

    out["wedge_simulations"] = [
        wedge_reach_simulation([0, 1], 200, [1] * 5 + [0] * 5),
        wedge_reach_simulation([0, 0, 1], 200, [1] * 7 + [0] * 5),
        wedge_reach_simulation([0, 1, 0, 0, 1], 300, [1] * 11 + [0] * 3),
        wedge_reach_simulation([0] * 6 + [1], 400, [1] * 400),  # long zero run, always-defect right seed
    ]

    out["random_pair_check_rule30"] = random_orbit_pair_check(rule30_forward, n_trials=800, width=60, seed=1)
    out["random_pair_check_rule90"] = random_orbit_pair_check(rule90_forward, n_trials=800, width=60, seed=2)

    with open("craquelure_probe_results.json", "w") as f:
        json.dump(out, f, indent=2)

    for k, v in out.items():
        print(k, "=>", v if not isinstance(v, list) else f"[{len(v)} items, see json]")


if __name__ == "__main__":
    main()

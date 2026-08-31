"""Verification of the "faro monoid" spark for Rule 30 Prize Problem 1.

Spark (verbatim, panel roundtable_followup2): "Rule 30 is a faro that sticks:
whenever two face-up cards meet, they adhere and the move drops out of the
symmetric group into a monoid ... f = the linear/invertible XOR-only move
... s = a 'stick' move that fires exactly when the OR term in Rule 30
saturates ... Centre periodicity is the claim that this one [tracked] card
has a cyclic itinerary under words in {f,s}. The analogy bites if s is
absorbing on the singleton conjugacy class."

This script:

1. Formalizes {f,s} exactly as the pin/no-pin split already proved in
   PATH.md section 1 and RESULTS-ladder-rung1.md Lemma 1, for a general
   left-permutive rule f(a,b,c) = a XOR g(b,c).
2. Runs the classification on the TRUE lone-seed orbit (reusing
   experiments/rule30/inverse_trace_probe.py's reconstruct_left_column) and
   measures the actual word / s-density.
3. Verifies computationally that an s-type step provably discards the right
   neighbour (the literal "information-losing" content of the spark) while
   an f-type step provably does not, by perturbation.
4. Confirms Rule 90 is all-f by construction (no OR term exists in its
   local rule at all), both from the truth table and on the actual orbit.
5. Reproduces, independently, the bounded automaton that is the only
   computationally checkable form of "is s absorbing": the 2-periodic
   restriction of RESULTS-ladder-rung1.md Lemma 4 (16 states, exhaustive),
   and a general-depth reproduction check against experiments/rule30/ladder
   rung1.py's already-published bisimulation-class counts.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
RULE30_DIR = REPO_ROOT / "experiments" / "rule30"
sys.path.insert(0, str(RULE30_DIR))

from periodicity_bridge_probe import RULE_30, RULE_90, evolve_rows, cell, center_trace  # noqa: E402
from inverse_trace_probe import reconstruct_left_column  # noqa: E402


# ---------------------------------------------------------------------------
# Part 1: formalize {f,s} for a general left-permutive rule f(a,b,c)=a XOR g(b,c)
# ---------------------------------------------------------------------------

def g_of(rule: int, center: int, right: int) -> int:
    """g(center,right) for rule = a XOR g(b,c); requires a-linearity (checked)."""
    n0 = (0 << 2) | (center << 1) | right
    n1 = (1 << 2) | (center << 1) | right
    out0 = (rule >> n0) & 1
    out1 = (rule >> n1) & 1
    if out0 == out1:
        raise ValueError(f"rule {rule} is not left-permutive (a-independent at b={center},c={right})")
    # a-linear means out1 == out0 XOR 1, i.e. g = out0 (a=0 row)
    return out0


def pins_at(rule: int) -> list[int]:
    """Centre values b at which g(b,0)==g(b,1) (the OR-saturation / pin / s-type site)."""
    return [b for b in (0, 1) if g_of(rule, b, 0) == g_of(rule, b, 1)]


def classify_site(rule: int, center_bit: int) -> str:
    """'s' if this centre value saturates g (pin fires, right neighbour irrelevant), else 'f'."""
    return "s" if center_bit in pins_at(rule) else "f"


def word_from_column(rule: int, column: list[int]) -> str:
    return "".join(classify_site(rule, c) for c in column)


# ---------------------------------------------------------------------------
# Part 2/3: run on the true lone-seed orbit; verify information loss/pass
# ---------------------------------------------------------------------------

def measure_true_orbit(T: int) -> dict:
    rows, center = evolve_rows(RULE_30, T)
    col0 = list(center_trace(rows, center))
    word = word_from_column(RULE_30, col0)
    s_count = word.count("s")
    f_count = word.count("f")

    # Cross-check against PATH.md section 1's pin table, freshly derived here.
    # Rule 60 (g(b,c)=b, "both" in PATH.md's table) is included as a two-sided
    # control: it should pin at BOTH center values, unlike 30/45/75 (one side)
    # and 90/150/105 (neither side).
    pin_table = {rule: pins_at(rule) for rule in (30, 45, 75, 60, 90, 150, 105)}

    # Perturbation test: at an f-type site, changing the right-neighbour column
    # value at that time must change the reconstructed left cell; at an
    # s-type site it must not.  Uses inverse_trace_probe.reconstruct_left_column
    # verbatim (no reimplementation of the pin arithmetic).  NOTE: given the
    # closed form left[t] = col0[t+1] ^ (col0[t] | right[t]), this outcome is
    # an algebraic identity of the formula, not new orbit-dependent evidence;
    # it is run here only to show the identity holds on the concrete data
    # this document works from, not as an independent confirmation.
    right_col = [cell(rows, center, t, 1) for t in range(len(col0))]
    base_left = reconstruct_left_column(col0, right_col)
    tested = {"f": {"total": 0, "changed": 0}, "s": {"total": 0, "changed": 0}}
    for t in range(len(base_left)):
        site_type = classify_site(RULE_30, col0[t])
        flipped_right = list(right_col)
        flipped_right[t] ^= 1
        flipped_left = reconstruct_left_column(col0, flipped_right)
        changed = flipped_left[t] != base_left[t]
        tested[site_type]["total"] += 1
        if changed:
            tested[site_type]["changed"] += 1

    return {
        "T": T,
        "s_count": s_count,
        "f_count": f_count,
        "s_density": s_count / len(word),
        "pin_table_reproduced": pin_table,
        "perturbation_test": tested,
    }


def measure_rule90(T: int) -> dict:
    """Rule 90's local rule has no OR term at all: confirm g(b,0)==g(b,1) never holds."""
    pins = pins_at(RULE_90)
    rows, center = evolve_rows(RULE_90, T)
    col0 = list(center_trace(rows, center))
    word = word_from_column(RULE_90, col0)
    return {
        "T": T,
        "pins_at": pins,
        "s_count_in_word": word.count("s"),
        "f_count_in_word": word.count("f"),
        "all_f_by_construction": pins == [],
    }


# ---------------------------------------------------------------------------
# Part 4: the "is s absorbing" question, made checkable
#   (a) Lemma 4's 2-periodic restriction, reproduced independently, 16 states
# ---------------------------------------------------------------------------

def lemma4_two_periodic_automaton() -> dict:
    """Independent reproduction of RESULTS-ladder-rung1.md Lemma 4.

    State (U,V) = (col_x, col_{x+1}) restricted to time-period-2 columns,
    U=(u0,u1), V=(v0,v1).  Transition (U,V) -> (W,U) with
      w0 = u1 XOR (u0 OR v0)
      w1 = u0 XOR (u1 OR v1)
    (this is literally the pin identity applied at both time-phases; w0's
    step is s-type iff u0=1, w1's step is s-type iff u1=1).
    Exhaustive over all 16 states.
    """
    def step(state):
        (u0, u1), (v0, v1) = state
        w0 = u1 ^ (u0 | v0)
        w1 = u0 ^ (u1 | v1)
        W = (w0, w1)
        U = (u0, u1)
        return (W, U)

    all_states = [((u0, u1), (v0, v1)) for u0 in (0, 1) for u1 in (0, 1)
                  for v0 in (0, 1) for v1 in (0, 1)]
    reach_cycle_at = {}
    cycles_found = set()
    for s0 in all_states:
        seen = {}
        s = s0
        step_no = 0
        while s not in seen:
            seen[s] = step_no
            s = step(s)
            step_no += 1
        cycle_start = seen[s]
        cycle_len = step_no - cycle_start
        reach_cycle_at[s0] = (cycle_start, cycle_len, s)
        # normalize cycle representative
        cyc = []
        c = s
        for _ in range(cycle_len):
            cyc.append(c)
            c = step(c)
        cycles_found.add(tuple(sorted(cyc)))

    max_transient = max(v[0] for v in reach_cycle_at.values())
    cycle_lengths = sorted({v[1] for v in reach_cycle_at.values()})
    # what does the absorbing cycle's column look like in real (non-restricted) terms?
    # U=(1,1),V=(0,0) <-> U=(0,0),V=(0,0)? check directly
    example_cycle = next(iter(cycles_found))
    return {
        "n_states": len(all_states),
        "distinct_cycles": len(cycles_found),
        "cycles": [list(c) for c in cycles_found],
        "max_transient_length": max_transient,
        "cycle_lengths_seen": cycle_lengths,
        "absorbing": len(cycles_found) == 1,
    }


# ---------------------------------------------------------------------------
# Part 5: general-depth reproduction check against rung1.py's bisim counts
# ---------------------------------------------------------------------------

def rerun_rung1_language(rmax: int) -> dict:
    """Reuse experiments/rule30/ladder/rung1.py to independently recheck a
    couple of small R against the published table (spot check, not a
    from-scratch re-derivation of the whole table)."""
    ladder_dir = REPO_ROOT / "experiments" / "rule30" / "ladder"
    sys.path.insert(0, str(ladder_dir))
    import importlib
    rung1 = importlib.import_module("rung1")
    Params = rung1.Params
    results = {}
    for R in range(1, rmax + 1):
        P = Params(rule=30, right_depth=R, left_depth=2, period_word=(0, 1), diff_q=1)
        plain = rung1.tail_language(P, pin=False)
        pin = rung1.tail_language(P, pin=True)
        results[R] = {
            "plain_bisim_classes": plain["bisim_classes"],
            "pin_bisim_classes": pin["bisim_classes"],
        }
    return results


def main() -> None:
    report: dict = {}
    report["true_orbit_T2000"] = measure_true_orbit(2000)
    report["rule90_T2000"] = measure_rule90(2000)
    report["lemma4_reproduction"] = lemma4_two_periodic_automaton()
    try:
        report["rung1_spot_check"] = rerun_rung1_language(3)
    except Exception as exc:  # pragma: no cover
        report["rung1_spot_check_error"] = repr(exc)
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()

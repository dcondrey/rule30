"""Plaquette-defect kappa(x,t) probe for the "gauge holonomy" spark.

Precise definitions (worked out per the task, not assumed from the spark
text, which left "reconstruct-left-then-evolve vs evolve-then-reconstruct-left"
undefined):

Rule 30's forward update and its left-permutive inverse are the SAME
algebraic identity read in two directions:

    forward:  s(t+1,x)   = s(t,x-1) XOR (s(t,x)   OR s(t,x+1))
    inverse:  s(t,x-1)   = s(t+1,x) XOR (s(t,x)   OR s(t,x+1))

(this is exactly reconstruct_left_column in inverse_trace_probe.py, reused
read-only below as ref_reconstruct_left).

A "plaquette" is the diamond {(t,x-1),(t,x),(t,x+1),(t+1,x)}.  To get a
genuine 2-path comparison we need a SECOND plaquette sharing an edge, so we
target the cell (t+1,x-1) by two routes:

  Path A "reconstruct-then-evolve": from the diamond at column x, use the
    inverse identity to get s(t,x-1) from {s(t,x-1... )} -- i.e. treat
    s(t,x-1) as already known (it's just read off the diagram) and instead
    EVOLVE the triple (s(t,x-2), s(t,x-1), s(t,x)) forward one step:
        s(t+1,x-1) = s(t,x-2) XOR (s(t,x-1) OR s(t,x))

  Path B "evolve-then-reconstruct": evolve the diamond at column x forward
    to get s(t+1,x) (already known / re-derived), then apply the INVERSE
    identity one time-step later, at column x, using {s(t+2,x), s(t+1,x),
    s(t+1,x+1)} to solve for s(t+1,x-1):
        s(t+1,x-1) = s(t+2,x) XOR (s(t+1,x) OR s(t+1,x+1))

kappa(x,t) := PathA(x,t) XOR PathB(x,t)

Both paths are literally the forward-rule identity applied to (possibly
different) already-known cells of the SAME true spacetime diagram.  Because
the identity is an algebraic rearrangement of one single update rule, kappa
must vanish identically on any array of cells that is internally consistent
with Rule 30 forward evolution, for ANY left-permutive rule -- this is
checked below as a one-line algebraic proof, then confirmed empirically on
the true lone-seed diagram and cross-checked against Rule 90.

Then a periodic-continuation version is built: replace the "known" cells that
lie PAST what direct simulation from the lone seed actually supports (i.e.
inject an assumed period-p continuation of the center column into one of the
two paths only) and see whether kappa becomes a nontrivial, nonzero
indicator -- and if so, whether it's anything other than the pre-existing
local consistency check (row 55 in PATH.md's ladder) in gauge-theory dress.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO_ROOT / "experiments" / "rule30"))

from inverse_trace_probe import (  # noqa: E402
    evolve_once_packed,
    reconstruct_left_column,
)
from periodicity_bridge_probe import RULE_30, RULE_90  # noqa: E402


def simulate(rule: int, half_width: int, steps: int):
    """Simulate a lone-seed diagram; returns rows[t][x] for x in [-half_width,half_width]."""
    width = 2 * (half_width + steps) + 5
    mask = (1 << width) - 1
    center_bit = half_width + steps + 2
    row = 1 << center_bit
    rows = []
    for _t in range(steps + 1):
        cells = {}
        for x in range(-half_width, half_width + 1):
            cells[x] = (row >> (center_bit + x)) & 1
        rows.append(cells)
        row = evolve_once_packed(rule, row, mask)
    return rows


def forward_cell(rule: int, left: int, mid: int, right: int) -> int:
    """Apply the 1-cell forward ECA rule to a 3-bit neighborhood."""
    idx = (left << 2) | (mid << 1) | right
    return (rule >> idx) & 1


def inverse_cell_rule30(future_mid: int, mid: int, right: int) -> int:
    """s(t,x-1) = s(t+1,x) XOR (s(t,x) OR s(t,x+1)) -- Rule 30's left inverse."""
    return future_mid ^ (mid | right)


def inverse_cell_rule90(future_mid: int, mid: int, right: int) -> int:
    """Rule 90 affine inverse: forward is s(t+1,x)=s(t,x-1) XOR s(t,x+1)
    (Rule 90 does not depend on the centre cell at all), so
    s(t,x-1) = s(t+1,x) XOR s(t,x+1); ``mid`` is accepted only to keep the
    call signature identical to the Rule 30 inverse and is unused."""
    del mid
    return future_mid ^ right


def kappa_true_diagram(rule: int, rows, x: int, t: int) -> int:
    """kappa on the TRUE simulated diagram, no periodicity assumption at all."""
    s = lambda tt, xx: rows[tt][xx]  # noqa: E731
    forward = forward_cell if rule == RULE_30 else None

    # Path A: reconstruct-then-evolve == evolve the triple at (t, x-2..x)
    pathA = forward_cell(rule, s(t, x - 2), s(t, x - 1), s(t, x))
    # Path B: evolve-then-reconstruct == inverse identity one step later at column x
    inv = inverse_cell_rule30 if rule == RULE_30 else inverse_cell_rule90
    pathB = inv(s(t + 2, x), s(t + 1, x), s(t + 1, x + 1))
    return pathA ^ pathB, pathA, pathB


def algebraic_identity_check():
    """Prove kappa==0 for ANY left-permutive rule's forward/inverse pair by
    brute-force enumeration over all bit assignments consistent with one
    forward step -- i.e. without ever touching a periodicity assumption."""
    results = {}
    for name, rule, inv in (
        ("rule30", RULE_30, inverse_cell_rule30),
        ("rule90", RULE_90, inverse_cell_rule90),
    ):
        bad = []
        # Enumerate all cells that appear in the two-plaquette footprint:
        # s(t,x-2), s(t,x-1), s(t,x), s(t,x+1), s(t,x+2) are free; every other
        # cell used below (s(t+1,x-1), s(t+1,x), s(t+1,x+1), s(t+2,x)) is
        # DERIVED by forward evolution from these -- that is what "internally
        # consistent with the forward rule" means.  There is no free variable
        # left over: 5 free bits, 32 cases, each checked exactly once.
        for a in (0, 1):  # s(t,x-2)
            for b in (0, 1):  # s(t,x-1)
                for c in (0, 1):  # s(t,x)
                    for d in (0, 1):  # s(t,x+1)
                        for e in (0, 1):  # s(t,x+2)
                            s_t1_xm1 = forward_cell(rule, a, b, c)  # s(t+1,x-1) == pathA
                            s_t1_x = forward_cell(rule, b, c, d)  # s(t+1,x)
                            s_t1_xp1 = forward_cell(rule, c, d, e)  # s(t+1,x+1)
                            s_t2_x = forward_cell(rule, s_t1_xm1, s_t1_x, s_t1_xp1)
                            pathA = s_t1_xm1
                            pathB = inv(s_t2_x, s_t1_x, s_t1_xp1)
                            k = pathA ^ pathB
                            if k != 0:
                                bad.append((a, b, c, d, e, k))
        results[name] = {"total_cases": 32, "nonzero_cases": len(bad), "examples": bad[:5]}
    return results


def measured_true_diagram_check(half_width=60, steps=400, samples=2000):
    rows_30 = simulate(RULE_30, half_width, steps)
    rows_90 = simulate(RULE_90, half_width, steps)
    out = {}
    for name, rows, rule in (("rule30", rows_30, RULE_30), ("rule90", rows_90, RULE_90)):
        nonzero = 0
        total = 0
        import random

        rnd = random.Random(0)
        for _ in range(samples):
            t = rnd.randint(0, steps - 3)
            x = rnd.randint(-half_width + 3, half_width - 3)
            k, _, _ = kappa_true_diagram(rule, rows, x, t)
            total += 1
            if k != 0:
                nonzero += 1
        out[name] = {"total": total, "nonzero": nonzero}
    return out


def periodic_injection_check(period_word, steps=200, half_width=40):
    """Inject an assumed period-p centre trace into Path B's future values
    (the (t+2,x) and (t+1,x) inputs), while Path A still uses the TRUE
    simulated diagram, and see whether kappa becomes nonzero and, if so,
    whether that nonzero-ness is anything but a local mismatch between the
    assumed and the true value at exactly the injected cell."""
    p = len(period_word)
    rows = simulate(RULE_30, half_width, steps)

    def assumed_center(t):
        return period_word[t % p]

    mismatches_at_injection = 0
    kappa_nonzero = 0
    kappa_nonzero_without_local_mismatch = 0
    total = 0
    for t in range(0, steps - 3):
        for x in range(-half_width + 3, half_width - 3):
            true_pathA = forward_cell(RULE_30, rows[t][x - 2], rows[t][x - 1], rows[t][x])
            # Path B uses assumed periodic value ONLY where x == 0 (the centre
            # column injection point); everywhere else it uses the true value.
            s_t1_x = rows[t + 1][x] if x != 0 else assumed_center(t + 1)
            s_t2_x = rows[t + 2][x] if x != 0 else assumed_center(t + 2)
            s_t1_xp1 = rows[t + 1][x + 1] if (x + 1) != 0 else assumed_center(t + 1)
            pathB = inverse_cell_rule30(s_t2_x, s_t1_x, s_t1_xp1)
            k = true_pathA ^ pathB
            total += 1
            if x == 0 or x == -1:
                local_true = rows[t + 1][0] if x == 0 else None
            if k != 0:
                kappa_nonzero += 1
                local_mismatch = (x == 0 and assumed_center(t + 1) != rows[t + 1][0]) or (
                    x == 0 and assumed_center(t + 2) != rows[t + 2][0]
                ) or ((x + 1) == 0 and assumed_center(t + 1) != rows[t + 1][0])
                if not local_mismatch:
                    kappa_nonzero_without_local_mismatch += 1
    return {
        "period": period_word,
        "total": total,
        "kappa_nonzero": kappa_nonzero,
        "kappa_nonzero_without_local_mismatch": kappa_nonzero_without_local_mismatch,
    }


def main():
    report = {}
    report["algebraic_identity_check"] = algebraic_identity_check()
    report["measured_true_diagram"] = measured_true_diagram_check()
    report["periodic_injection_p2_00"] = periodic_injection_check([0, 0])
    report["periodic_injection_p2_01"] = periodic_injection_check([0, 1])
    print(json.dumps(report, indent=2))
    out_path = Path(__file__).parent / "kappa_probe_results.json"
    out_path.write_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

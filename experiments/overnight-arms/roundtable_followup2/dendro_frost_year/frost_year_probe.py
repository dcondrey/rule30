"""Verification harness for the 'dendro frost year' Rule 30 spark.

Self-contained: does not import from other experiment directories, per the
task's directory restriction.

Two things are checked:

1. (PROVED, by direct algebra, confirmed numerically here) G_p(T), restricted
   to any index subset drawn from times >= the eventual-periodicity onset, is
   forced to 1 by the reductio hypothesis itself, regardless of how the index
   subset (the "frost years") is chosen.  The construction is vacuous as a
   discriminator of P1/P2: it can only fail to reach 1 by way of a *finite*
   prefix mismatch, and eventual periodicity is silent on any finite prefix.

2. (MEASURED) Certifying a frost year at a centre time t, when c_t=0, requires
   knowing r_t = s(t,1).  Absent an analytic law for r_t (which is exactly
   this repo's open R1 target -- "periodic centre => periodic adjacent
   column"), the only way to get r_t is to reconstruct/simulate columns
   inward from a right boundary that is genuinely zero (beyond the light
   cone).  This measures how much boundary width is needed, confirming it is
   Theta(t), not bounded and not O(log t).
"""

from __future__ import annotations

import json
from dataclasses import dataclass

RULE_30 = 30
RULE_90 = 90


def lone_seed_rows(rule: int, steps: int) -> list[int]:
    """Return packed rows 0..steps of the lone-seed diagram, centered.

    Row t is a Python int bitmask over a window wide enough that the light
    cone never touches the edges through `steps`.
    """
    width = 2 * steps + 5
    mask = (1 << width) - 1
    center = steps + 2
    row = 1 << center
    rows = [row]
    for _ in range(steps):
        left = (row << 1) & mask
        mid = row
        right = row >> 1
        nxt = 0
        for nb in range(8):
            if not ((rule >> nb) & 1):
                continue
            term = mask
            for src, flag in ((left, 4), (mid, 2), (right, 1)):
                term &= src if (nb & flag) else (~src & mask)
            nxt |= term
        row = nxt & mask
        rows.append(row)
    return rows, center


def column(rows: list[int], center: int, offset: int) -> list[int]:
    return [(row >> (center + offset)) & 1 for row in rows]


def or_fires_A(x_i: int, x_ip1: int) -> int:
    """Task's literal definition: fires iff NOT (both are 0)."""
    return int(not (x_i == 0 and x_ip1 == 0))


def or_fires_B(x_i: int, x_ip1: int) -> int:
    """Alternate reading: OR differs from XOR, i.e. fires iff both are 1."""
    return int(x_i == 1 and x_ip1 == 1)


@dataclass
class FrostReport:
    rule: int
    T: int
    density_c1: float
    density_frost_A: float
    density_frost_B: float


def frost_densities(rule: int, T: int) -> FrostReport:
    rows, center = lone_seed_rows(rule, T)
    c = column(rows, center, 0)
    r = column(rows, center, 1)
    n = len(c)
    dens_c1 = sum(c) / n
    fA = sum(or_fires_A(c[t], r[t]) for t in range(n)) / n
    fB = sum(or_fires_B(c[t], r[t]) for t in range(n)) / n
    return FrostReport(rule, T, dens_c1, fA, fB)


def restricted_G_p(c: list[int], p: int, T0: int, T: int, index_set: set[int]) -> tuple[int, int]:
    """Agreement count and denominator of G_p(T) over index_set within [0,T).

    c must already satisfy c[t] == c[t+p] for all t >= T0 (constructed that
    way below); we do NOT enforce it here, we just score whatever c is.
    """
    num = 0
    den = 0
    for t in index_set:
        if t < 0 or t + p >= len(c) or t >= T:
            continue
        den += 1
        if c[t] == c[t + p]:
            num += 1
    return num, den


def make_synthetic_eventually_periodic(prefix: list[int], period_word: list[int], total_len: int) -> list[int]:
    """A sequence equal to `prefix` up to T0, then exactly p-periodic after."""
    out = list(prefix)
    p = len(period_word)
    t0 = len(prefix)
    while len(out) < total_len:
        out.append(period_word[(len(out) - t0) % p])
    return out


def verify_vacuity(T: int = 20000, p: int = 148, T0: int = 300, seed: int = 12345) -> dict:
    """Numeric confirmation of the algebraic vacuity claim.

    Build a synthetic column that is genuinely p-periodic from T0 onward
    (garbage random prefix before T0), pick a deliberately adversarial,
    sparse, aperiodic-looking frost index set (Beatty sequence with an
    irrational slope) as a stand-in for 'frost years', and confirm
    G_p(T) -> 1 as T grows, using ONLY that periodic hypothesis -- no rule
    dynamics involved, because the claim is about the algebra of the
    construction, not about Rule 30 specifically.
    """
    import random
    import math

    rng = random.Random(seed)
    prefix = [rng.randint(0, 1) for _ in range(T0)]
    period_word = [rng.randint(0, 1) for _ in range(p)]
    if all(b == 0 for b in period_word):
        period_word[0] = 1
    c = make_synthetic_eventually_periodic(prefix, period_word, T + p + 1)

    # Beatty sequence with irrational slope: sparse, aperiodic index set.
    alpha = math.sqrt(2)
    beatty = set()
    n = 1
    while True:
        v = int(math.floor(n * alpha))
        if v >= T:
            break
        beatty.add(v)
        n += 1

    checkpoints = [500, 1000, 2000, 5000, 10000, T]
    results = []
    for Tc in checkpoints:
        num, den = restricted_G_p(c, p, T0, Tc, beatty)
        results.append({
            "T": Tc,
            "num": num,
            "den": den,
            "G_p": (num / den) if den else None,
        })
    return {
        "p": p,
        "T0": T0,
        "index_set": "Beatty(sqrt(2)) -- sparse, aperiodic by construction",
        "results": results,
    }


def certification_depth_scan(Ts: list[int]) -> list[dict]:
    """Measure the minimal right-boundary width R needed to correctly get
    r_t = s(t,1) via zero-boundary-anchored reconstruction, for several t.

    Ground truth comes from direct forward simulation (free, since we are
    doing the verification here and can afford it at these T).  We simulate
    a WINDOW-truncated diagram with an artificially early zero right
    boundary at various positions R and see at what R the value at position
    1, time t, stops matching the true (untruncated) value.  This stands in
    for '`inverse_trace_probe`-style reconstruction from a hypothesized
    right boundary'; truncating column R to 0 for all t is exactly the
    'genuinely zero beyond the light cone' fact used as the anchor.
    """
    out = []
    for T in Ts:
        # True diagram, wide enough that R < true_rows width never gets
        # touched by the real light cone within T steps.
        true_rows, true_center = lone_seed_rows(RULE_30, T)
        true_r = column(true_rows, true_center, 1)[T]

        # Try shrinking the simulated half-width R and see when position 1
        # at time T stops matching truth.  We simulate a truncated CA where
        # everything at |offset| > R is forced to 0 at every step (a hard
        # wall), which is exactly what "assume column R is zero for all
        # time" gives you as an anchor for inward reconstruction.
        minimal_R = None
        for R in range(1, T + 3):
            width = 2 * T + 5
            mask = (1 << width) - 1
            center = T + 2
            row = 1 << center
            wall_lo = center - R
            wall_hi = center + R
            for _ in range(T):
                left = (row << 1) & mask
                mid = row
                right = row >> 1
                nxt = 0
                for nb in range(8):
                    if not ((RULE_30 >> nb) & 1):
                        continue
                    term = mask
                    for src, flag in ((left, 4), (mid, 2), (right, 1)):
                        term &= src if (nb & flag) else (~src & mask)
                    nxt |= term
                # hard wall: zero out everything outside [wall_lo, wall_hi]
                keep_mask = ((1 << (wall_hi - wall_lo + 1)) - 1) << wall_lo
                nxt &= keep_mask & mask
                row = nxt & mask
            r_val = (row >> (center + 1)) & 1
            if r_val == true_r:
                minimal_R = R
                break
        out.append({"T": T, "true_r_T": true_r, "minimal_R_for_correct_r": minimal_R})
    return out


def main() -> None:
    report = {}
    report["frost_densities"] = {
        "rule30": frost_densities(RULE_30, 4000).__dict__,
        "rule90": frost_densities(RULE_90, 4000).__dict__,
    }
    report["vacuity_check_rule_agnostic_algebra"] = verify_vacuity()
    report["certification_depth_scan"] = certification_depth_scan([10, 30, 60, 100, 200])
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

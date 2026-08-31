"""Independent verification of the T_w 'periodic-trace return transducer'
proposal (GPT-5.6 / DeepSeek, roundtable) and the screen-out that killed it
(Grok, later turn).

Rule 30: s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1)).
Lone seed: s(0,0)=1, else 0.

This module tests, computationally, each load-bearing claim in both the
proposal and the screen-out, rather than trusting either model's prose.
"""
from __future__ import annotations

import json
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Ground truth: exact lone-seed diagram, symmetric array, rule 30.
# ---------------------------------------------------------------------------

def lone_seed_diagram(T: int, half_width: int) -> list[list[int]]:
    """Return rows[0..T], each a list indexed x = -half_width..+half_width
    (so rows[t][half_width + x] = s(t, x)).  Pads with 0 outside the array;
    half_width must exceed T so the true light cone never touches the edge.
    """
    assert half_width > T, "half_width must exceed T so edges never contaminate the light cone"
    n = 2 * half_width + 1
    row = [0] * n
    row[half_width] = 1  # x = 0
    rows = [row[:]]
    for t in range(T):
        new = [0] * n
        for i in range(n):
            left = row[i - 1] if i - 1 >= 0 else 0
            mid = row[i]
            right = row[i + 1] if i + 1 < n else 0
            new[i] = left ^ (mid | right)
        rows.append(new)
        row = new
    return rows


def right_ray(rows: list[list[int]], half_width: int, t: int, width: int) -> list[int]:
    """u_{t,i} for i = 0..width-1, i.e. s(t, 0..width-1)."""
    return rows[t][half_width: half_width + width]


# ---------------------------------------------------------------------------
# PART 1/2: literal reading of the proposal.
#
# The proposal's own recurrence: u_{t,-1} = a_{t+1} XOR (a_t OR u_{t,1}),
# "iterated" to reconstruct col_{-1}, col_{-2}, ... and define an exact
# p-step ray map T_w: rho_t -> rho_{t+p}.
#
# Two distinct, both-plausible formalizations of "T_w" are tested, because
# the prose is not precise enough to pin down only one:
#
#  Reading B (driven-boundary forward CA): column 0 is forced to the
#  hypothesised periodic word; columns i>=1 evolve by the ordinary forward
#  rule using only rho_t (columns i-1,i,i+1, all >=0 for i>=1).  This is a
#  genuine, well-defined, LOCAL (bounded-radius) map -- no reconstruction of
#  the left half-plane is even needed to advance the ray forward, because a_t
#  is *given* directly at every t under the hypothesis, not derived.
#
#  Reading C (literal leftward reconstruction via reconstruct_left_column):
#  use the inverse recurrence to actually build col_{-1}, col_{-2}, ... as
#  FULL finite time series, cascading left, and measure how much of the
#  right ray's TIME extent (not space extent) each additional level of left
#  depth consumes -- since "one future centre value is consumed" per level
#  (this repo's own documented identity, RESULTS-ladder-rung1.md section 0.5
#  and inverse_trace_probe.reconstruct_left_column).
# ---------------------------------------------------------------------------


def periodic_word(p: int, phase: int = 0) -> list[int]:
    """A canonical nonconstant period-p word.  p=1 -> [0]; p=2 -> [0,1]."""
    if p == 1:
        return [0]
    if p == 2:
        return [0, 1]
    raise ValueError("only p=1,2 requested by the task")


def reading_B_driven_forward(w: list[int], seed_row0: list[int], T: int, width: int) -> list[list[int]]:
    """Simulate the driven-boundary system: D_t[0] is forced to w[t % p];
    D_t[i] for i>=1 evolves by the ordinary forward rule using D_{t-1} at
    i-1,i,i+1 (all indices >=0, since i>=1 means i-1>=0).  D_0 is the true
    lone-seed row restricted to x>=0.  Returns D_t for t=0..T, each of length
    `width` (cells beyond `width` are not tracked; width must exceed T so the
    forward light cone from the driven boundary and from D_0's tail never
    reaches the tracked window from outside).
    """
    p = len(w)
    D = [seed_row0[:width]]
    cur = D[0][:]
    for t in range(T):
        nxt = [0] * width
        nxt[0] = w[(t + 1) % p]
        for i in range(1, width - 1):
            nxt[i] = cur[i - 1] ^ (cur[i] | cur[i + 1])
        # last cell: right neighbor unknown -> leave undefined, drop it.
        D.append(nxt)
        cur = nxt
    return D


def one_forward_step(w: list[int], t: int, cur: list[int]) -> list[int]:
    """Advance rho_t -> rho_{t+1} under reading B's driven-boundary rule."""
    p = len(w)
    width = len(cur)
    nxt = [0] * width
    nxt[0] = w[(t + 1) % p]
    for i in range(1, width - 1):
        nxt[i] = cur[i - 1] ^ (cur[i] | cur[i + 1])
    return nxt


def reach_of_T_w_step(w: list[int], rho_t: list[int], t: int, i_target: int, p_steps: int) -> int:
    """THE key measurement: does D_{t+p_steps}[i_target], computed by
    iterating the local forward rule p_steps times starting from rho_t
    itself (not the seed row), depend on rho_t beyond some bounded window?

    Method: perturb rho_t at position j (flip the bit) for increasing j,
    recompute p_steps forward, and find the largest j that still changes the
    target cell -- i.e. the true dependency radius, measured directly by
    perturbation, not assumed from the rule's locality.
    """
    def advance(row: list[int]) -> list[int]:
        cur = row[:]
        tt = t
        for _ in range(p_steps):
            cur = one_forward_step(w, tt, cur)
            tt += 1
        return cur

    base_val = advance(rho_t)[i_target]
    max_dep = -1
    for j in range(len(rho_t)):
        if j == 0:
            continue  # column 0 is pinned externally regardless of rho_t; perturbing it is meaningless
        pert = rho_t[:]
        pert[j] ^= 1
        if len(pert) - 1 < i_target + p_steps + 2:
            continue
        val = advance(pert)[i_target]
        if val != base_val:
            max_dep = j
    return max_dep


def reading_C_leftward_time_cost(rows, half_width, p: int, T: int, target_depth: int, base_t: int) -> dict:
    """Literal leftward reconstruction: use the inverse recurrence
    col_{x-1}(t) = col_x(t+1) XOR (col_x(t) OR col_{x+1}(t))
    with col_0 REPLACED by the hypothesised periodic word (not its true
    value), and col_1, col_2, ... equal to the TRUE right-ray data (this is
    the only way to get real numbers into the recursion; the proposal is
    silent on where columns >=1 come from except 'the right ray').

    Measures: to produce col_{-m}(base_t) for m = 1..target_depth, how many
    *additional future time samples* of column 1 must be supplied, i.e. how
    far in TIME (not space) into the right ray's own history the
    reconstruction must reach, as a function of requested left depth m.
    This is the quantity the repo already tracks as the O(log t)/pin
    propagation wall (PATH.md obstruction A).
    """
    w = periodic_word(p)
    length = T + target_depth + 5

    def a(t: int) -> int:
        return w[t % p]

    # column 1's true time series (ground truth from the seed diagram)
    col1_true = [rows[t][half_width + 1] for t in range(length)]

    # col_{-1} as a time series: needs a(t), a(t+1), col1_true(t)
    def build_left_series(depth: int) -> list[int]:
        """Return col_{-depth} as a time series of maximal available length,
        cascading the reconstruction `depth` times starting from a(=col0,
        hypothesised) and col1_true (ground truth)."""
        cur_center = [a(t) for t in range(length)]
        cur_right = col1_true[:]
        for level in range(depth):
            L = min(len(cur_center), len(cur_right)) - 1
            new_col = [cur_center[t + 1] ^ (cur_center[t] | cur_right[t]) for t in range(L)]
            cur_right = cur_center
            cur_center = new_col
        return cur_center

    results = {}
    for m in range(1, target_depth + 1):
        series = build_left_series(m)
        max_t_available = len(series) - 1
        results[m] = {
            "series_length": len(series),
            "max_t_reachable": max_t_available,
            "time_samples_of_col1_consumed": length - len(series),
        }
    return results


# ---------------------------------------------------------------------------
# PART 4: does the driven trajectory's spatial tail actually go periodic?
# ---------------------------------------------------------------------------

def spatial_tail_is_eventually_periodic(row: list[int], max_period: int = 40, tail_frac: float = 0.5) -> dict:
    n = len(row)
    tail = row[int(n * (1 - tail_frac)):]
    best = None
    for per in range(1, max_period + 1):
        if len(tail) < 4 * per:
            continue
        ok = all(tail[i] == tail[i - per] for i in range(per, len(tail)))
        if ok:
            best = per
            break
    return {"tail_len": len(tail), "eventually_periodic": best is not None, "period_found": best}


def run_all():
    T = 300
    half_width = T + 120
    print("Building true lone-seed diagram to T =", T, "...")
    rows = lone_seed_diagram(T + 60, half_width)  # extra depth for reading_C time budget
    # row 0 restricted to x>=0 is exactly [1,0,0,0,...]; pad with 0s out to any
    # width the driven simulation needs (true value there is 0 regardless).
    MAX_DRIVE_WIDTH = 2000
    seed_row0 = [1] + [0] * (MAX_DRIVE_WIDTH - 1)

    out = {}

    # --- Part 1/2: reach of reading B (driven forward map), bounded or not ---
    # Build rho_t at many t values by running the driven system once, then
    # perturb-test the actual dependency radius at each t independently.
    reach_results = {}
    for p in (1, 2):
        w = periodic_word(p)
        width = 100
        D = reading_B_driven_forward(w, seed_row0, T, width)
        reach_by_t = {}
        for t0 in (0, 5, 10, 20, 40, 80, 120, 160, 200):
            if t0 >= len(D):
                continue
            r = reach_of_T_w_step(w, D[t0], t0, i_target=8, p_steps=p)
            reach_by_t[t0] = r
        reach_results[f"p={p}"] = reach_by_t
    out["reading_B_reach_by_t"] = reach_results

    # --- Part 2: reading C, time-cost of going left, per depth ---
    time_cost_results = {}
    for p in (1, 2):
        res = reading_C_leftward_time_cost(rows, half_width, p, T=100, target_depth=15, base_t=50)
        time_cost_results[f"p={p}"] = res
    out["reading_C_time_cost_per_depth"] = time_cost_results

    # --- Part 4: run T_w (reading B) forward, check spatial tail periodicity ---
    tail_results = {}
    for p in (1, 2):
        w = periodic_word(p)
        width = 1600
        Tdrive = 1400
        D = reading_B_driven_forward(w, seed_row0, Tdrive, width)
        final_row = D[Tdrive][:width - Tdrive - 5]  # keep only cells inside the light cone from t=0 data + drive
        tail_results[f"p={p}"] = spatial_tail_is_eventually_periodic(final_row, max_period=40, tail_frac=0.6)
        tail_results[f"p={p}"]["sample_tail_bits"] = "".join(str(b) for b in final_row[-60:])

    # control: rule 90 analog for sanity (additive rule; column 0 pinned is vacuous per Lemma 1')
    def rule90_driven(w, seed_row0, T, width):
        p = len(w)
        D = [seed_row0[:width]]
        cur = D[0][:]
        for t in range(T):
            nxt = [0] * width
            nxt[0] = w[(t + 1) % p]
            for i in range(1, width - 1):
                nxt[i] = cur[i - 1] ^ cur[i + 1]
            D.append(nxt)
            cur = nxt
        return D

    # rule 90 lone seed
    def lone_seed_90(T, half_width):
        n = 2 * half_width + 1
        row = [0] * n
        row[half_width] = 1
        rows90 = [row[:]]
        for t in range(T):
            new = [0] * n
            for i in range(n):
                left = row[i - 1] if i - 1 >= 0 else 0
                right = row[i + 1] if i + 1 < n else 0
                new[i] = left ^ right
            rows90.append(new)
            row = new
        return rows90

    seed90_row0 = [1] + [0] * (MAX_DRIVE_WIDTH - 1)
    for p in (1, 2):
        w = periodic_word(p)
        width = 1600
        Tdrive = 1400
        D90 = rule90_driven(w, seed90_row0, Tdrive, width)
        final_row90 = D90[Tdrive][:width - Tdrive - 5]
        tail_results[f"rule90_control_p={p}"] = spatial_tail_is_eventually_periodic(final_row90, max_period=40, tail_frac=0.6)
        tail_results[f"rule90_control_p={p}"]["sample_tail_bits"] = "".join(str(b) for b in final_row90[-60:])

    out["tail_periodicity"] = tail_results

    with open("results.json", "w") as f:
        json.dump(out, f, indent=2)

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    run_all()

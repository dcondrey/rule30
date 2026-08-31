"""Weaver-preimage-count probe: LLM-panel spark, reformalized and measured.

Spark (weaving / selvage-tension domain): define P(t) as the number of
left-half configurations that, together with the actual known seed/right-half
data, reproduce the TRUE observed lone-seed centre-column prefix
a_0,...,a_{t-1} under Rule 30.  Claim under test: eventual periodicity of the
centre column would force P(t) to stabilize (become eventually constant or
slow-growing in a specific way); the real orbit's P(t) "drifts" instead.

## Exact setup (the spark under-specifies this; this is the reading used here)

Fix the TRUE lone-seed initial row at time 0: s(0,0) = 1 (the seed), and
s(0,x) = 0 for every x != 0 (the true right half AND the true left half,
both identically zero, since the lone-seed configuration has no other 1).

For a window length t, replace the true left half on {-t,...,-1} with a
candidate bitstring b in {0,1}^t, holding the seed cell (x=0) and the entire
right half (x>=1) at their TRUE values (0 for all x>=1), and holding
everything left of the window (x < -t) at its TRUE value (0) as well.  Forward
-evolve this modified initial row t-1 steps under the target rule and read off
the candidate centre trace a'_0,...,a'_{t-1}.

  P(t) := #{ b in {0,1}^t : a'_0..a'_{t-1} == a_0..a_{t-1} (the TRUE trace) }

This is a genuinely different object from the pin/trace-reconstruction
mechanism already in this repo (`inverse_trace_probe.py`): that mechanism
fixes the ENTIRE time-trace of a column (all t, and implicitly beyond) plus
the entire right-half diagram and asks for the unique left-half diagram
reproducing it -- a bijection by left permutivity, hence exactly 1 preimage,
by construction, with no counting content at all.  P(t) here fixes only the
INITIAL ROW's left half (one space-like slice) and asks how many settings of
it reproduce the centre trace under forward time evolution -- a forward
combinatorial counting question that is not resolved by the reconstruction
bijection.

## Algorithm

Brute force is 2^t. Because each candidate bit b_{-k} first enters the causal
cone of a'_k only (light cone: a'_j depends only on initial cells in
[-j, j]), the search is done by backtracking depth-first over k = 1..t,
fixing b_{-1}, then b_{-2}, ... and checking a'_k against the true a_k as soon
as it is determined (i.e. as soon as all cells in [-k,k] are fixed). A branch
that mismatches is pruned (contributes 0 to every deeper P(t')). This gives
the EXACT value of P(t) for every t along the way in one pass, without ever
materializing more than surviving branches -- exponential only in the
information the problem itself carries, not in 2^t, and it is exact (not a
sample), so it is safe to use as ground truth up to whatever depth remains
tractable.

For Rule 90, s(t+1,x) = s(t,x-1) XOR s(t,x+1) is GF(2)-linear (no dependence
on the centre bit at all), so requiring a'_1..a'_{t-1} = 0 (Rule 90's true
lone-seed trace is exactly the seed at t=0 then identically zero) is a linear
system in b_{-1..-t} over GF(2). Its solution count is exactly
2^(t - rank), computed once via Gaussian elimination -- this gives EXACT
Rule 90 values at large t (no backtracking blow-up risk) as an independent
cross-check on the backtracking result at the t where both are run.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field


def forward_rule(rule: int, left: int, mid: int, right: int) -> int:
    neighborhood = (left << 2) | (mid << 1) | right
    return (rule >> neighborhood) & 1


def true_lone_seed_trace(rule: int, length: int) -> list[int]:
    """Exact lone-seed centre trace a_0..a_{length-1}, brute simulation."""
    max_time = length - 1
    width = 2 * max_time + 3
    center = max_time + 1
    row = [0] * width
    row[center] = 1
    trace = [row[center]]
    for _ in range(max_time):
        new_row = [0] * width
        for x in range(1, width - 1):
            new_row[x] = forward_rule(rule, row[x - 1], row[x], row[x + 1])
        row = new_row
        trace.append(row[center])
    return trace


@dataclass
class BacktrackResult:
    p_of_t: dict[int, int] = field(default_factory=dict)
    branch_history: list[tuple[int, int]] = field(default_factory=list)
    # branch_history[i] = (depth, number_of_nodes_visited_at_that_depth)
    nodes_visited: int = 0


def count_p_backtracking(rule: int, true_trace: list[int], max_t: int) -> BacktrackResult:
    """Exact backtracking count of P(t) for t = 1..max_t, all in one pass.

    The recursion fixes b_{-1}, b_{-2}, ... in order.  At depth k the initial
    row on [-k, k] is fully fixed (candidate bits on [-k,-1], true seed at 0,
    true zero right half on [1,k]); it is forward-simulated k steps to get
    a'_0..a'_k, and pruned unless it matches the true trace on that prefix.
    """
    result = BacktrackResult()
    # window[k] holds current known row values indexed by absolute position
    # -k .. k, but we regenerate the whole triangle each call for clarity and
    # correctness (t is small enough that O(t^3) total work is irrelevant).

    def simulate_and_check(bits_left_to_right: list[int]) -> bool:
        """bits_left_to_right: b_{-k}, b_{-(k-1)}, ..., b_{-1} (k entries).

        Returns True iff the induced centre trace a'_0..a'_{k-1} (the PREFIX
        of length k, matching the P(t) definition's a_0..a_{t-1} with t=k)
        matches truth.  Note a'_k itself is NOT checked here: with a window of
        exactly k candidate bits {-k,...,-1}, P(k) is defined against a
        length-k prefix a_0..a_{k-1}, so the newest bit b_{-k} is unconstrained
        by this call (it first becomes constrained only at depth k+1, via
        a'_k, in the next recursion level).
        """
        k = len(bits_left_to_right)
        width = 2 * k + 1
        row = [0] * width
        # positions: index 0 -> x=-k, index k -> x=0, index 2k -> x=k
        for i, b in enumerate(bits_left_to_right):
            row[i] = b
        row[k] = 1  # true seed
        # right half [1,k] already 0
        trace = [row[k]]
        cur = row
        for _ in range(k):
            new_row = [0] * width
            for x in range(1, width - 1):
                new_row[x] = forward_rule(rule, cur[x - 1], cur[x], cur[x + 1])
            cur = new_row
            trace.append(cur[k])
        return trace[:k] == true_trace[:k]

    depth_counts: dict[int, int] = {}
    running_total_per_t: dict[int, int] = {}

    def recurse2(bits_right_to_left: list[int], depth: int) -> None:
        result.nodes_visited += 1
        depth_counts[depth] = depth_counts.get(depth, 0) + 1
        ordered = list(reversed(bits_right_to_left))
        if depth > 0 and not simulate_and_check(ordered):
            return
        # this node is a valid partial assignment of length `depth`
        running_total_per_t[depth] = running_total_per_t.get(depth, 0) + 1
        if depth == max_t:
            return
        for bit in (0, 1):
            recurse2([bit] + bits_right_to_left, depth + 1)

    recurse2([], 0)
    result.p_of_t = {k: v for k, v in running_total_per_t.items() if k >= 1}
    result.branch_history = [(k, depth_counts.get(k, 0)) for k in sorted(depth_counts)]
    return result


def exhaustive_edge_bijection_check(rule: int, max_k: int) -> dict[int, bool]:
    """Exhaustive check, for k=1..max_k: is a'_k, as a function of the newest
    (deepest) bit b_{-k}, a bijection {0,1}->{0,1} for EVERY one of the
    2^(k-1) settings of the earlier bits b_{-1..-(k-1)} (right half and seed
    held at their true values as always)?  This tests the general "fastest
    path" argument already used in this repo's `inverse_trace_probe.py`
    docstring, independent of periodicity, the true trace, or Rule 30's
    nonlinearity in particular -- it should hold for ANY left-permutive rule
    if the argument is what it appears to be.
    """
    results: dict[int, bool] = {}
    for k in range(1, max_k + 1):
        width = 2 * k + 1
        all_bijective = True
        for prior in range(1 << (k - 1)):
            prior_bits = [(prior >> i) & 1 for i in range(k - 1)]  # b_{-1}..b_{-(k-1)}
            outs = []
            for last_bit in (0, 1):
                bits = list(reversed(prior_bits)) + [last_bit]  # b_{-k},...,b_{-1}... wait order
                # Build initial row directly by absolute position for clarity.
                row = [0] * width
                # index i in [0, 2k] <-> x = i - k
                row[k] = 1  # seed
                for j in range(1, k):  # b_{-j} for j=1..k-1 at x=-j -> index k-j
                    row[k - j] = prior_bits[j - 1]
                row[0] = last_bit  # b_{-k} at x=-k -> index 0
                cur = row
                for _ in range(k):
                    new_row = [0] * width
                    for x in range(1, width - 1):
                        new_row[x] = forward_rule(rule, cur[x - 1], cur[x], cur[x + 1])
                    cur = new_row
                outs.append(cur[k])
            if outs[0] == outs[1]:
                all_bijective = False
                break
        results[k] = all_bijective
    return results


def gf2_rank(rows: list[list[int]]) -> int:
    """Rank of a GF(2) matrix given as a list of rows (each a set of column
    indices with a 1), via Gaussian elimination using integers as bitmasks."""
    masks = [0] * len(rows)
    for i, r in enumerate(rows):
        m = 0
        for c in r:
            m |= 1 << c
        masks[i] = m
    rank = 0
    pivots: list[int] = []
    for m in masks:
        cur = m
        for p in pivots:
            highbit = p.bit_length() - 1
            if (cur >> highbit) & 1:
                cur ^= p
        if cur != 0:
            pivots.append(cur)
            rank += 1
    return rank


def count_p_rule90_linear(true_trace: list[int], max_t: int) -> dict[int, int]:
    """Exact P(t) for Rule 90 for every t=1..max_t via GF(2) linear algebra.

    s(t+1,x) = s(t,x-1) XOR s(t,x+1) (Rule 90) is additive: the centre value
    a'_k, as a function of the unknown initial bits b_{-1..-k} (with the seed
    fixed at 1 and all other true cells 0), is an explicit GF(2)-LINEAR
    function of those bits plus a constant (the seed's own contribution).
    We derive that linear functional symbolically by superposition: run the
    all-zero-unknowns baseline to get the constant term, then flip one
    unknown at a time to read off its coefficient in each a'_k (linearity
    justifies reading off coefficients this way exactly, not approximately).
    """
    # constant term: unknowns=0 (true diagram) -> already true_trace
    baseline = true_trace
    # coefficient of b_{-j} (0-indexed j=1..max_t) in a'_k for each k
    influence: list[list[int]] = [[0] * (max_t + 1) for _ in range(max_t + 1)]
    for j in range(1, max_t + 1):
        width = 2 * max_t + 1
        row = [0] * width
        row[max_t - j] = 1  # b_{-j} = 1 at absolute position x=-j, all other unknowns 0
        row[max_t] = 0  # seed excluded here (isolating the linear part only)
        cur = row
        trace_j = [cur[max_t]]
        for _ in range(max_t):
            new_row = [0] * width
            for x in range(1, width - 1):
                new_row[x] = cur[x - 1] ^ cur[x + 1]
            cur = new_row
            trace_j.append(cur[max_t])
        for k in range(0, max_t + 1):
            influence[k][j] = trace_j[k]

    # constant term c_k = value at a'_k with all b=0 and seed=1 only
    width = 2 * max_t + 1
    row0 = [0] * width
    row0[max_t] = 1
    cur = row0
    const_trace = [cur[max_t]]
    for _ in range(max_t):
        new_row = [0] * width
        for x in range(1, width - 1):
            new_row[x] = cur[x - 1] ^ cur[x + 1]
        cur = new_row
        const_trace.append(cur[max_t])

    # sanity: const_trace should equal the true trace (b=0 is the true config)
    assert const_trace[: max_t + 1] == baseline[: max_t + 1], "linear decomposition sanity check failed"

    p_of_t: dict[int, int] = {}
    for k in range(1, max_t + 1):
        # constraint for time index m (1<=m<=k): sum_j influence[m][j]*b_j = const_trace[m] XOR true_trace[m] = 0
        # (true_trace[m] == const_trace[m] identically, so RHS is always 0: homogeneous system)
        rows = []
        # P(t=k) is checked against the LENGTH-k prefix a_0..a_{k-1}, i.e.
        # constraints at times m=1..k-1 (a_0 is the trivial seed constraint,
        # always satisfied); this matches count_p_backtracking's convention.
        for m in range(1, k):
            cols = [j - 1 for j in range(1, k + 1) if influence[m][j] == 1]
            rows.append(cols)
        rank = gf2_rank(rows)
        p_of_t[k] = 1 << (k - rank)
    return p_of_t


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-t-backtrack", type=int, default=24)
    parser.add_argument("--max-t-linear", type=int, default=200)
    parser.add_argument("--out", type=str, default="preimage_count_results.json")
    args = parser.parse_args()

    trace_len = max(args.max_t_backtrack, args.max_t_linear) + 5
    true_trace_30 = true_lone_seed_trace(30, trace_len)
    true_trace_90 = true_lone_seed_trace(90, trace_len)

    print("Rule 30 true trace (first 30):", true_trace_30[:30], file=sys.stderr)
    print("Rule 90 true trace (first 30):", true_trace_90[:30], file=sys.stderr)

    print(f"Backtracking P(t) for Rule 30, t=1..{args.max_t_backtrack} ...", file=sys.stderr)
    res30 = count_p_backtracking(30, true_trace_30, args.max_t_backtrack)
    print("Rule 30 P(t):", res30.p_of_t, file=sys.stderr)
    print("Rule 30 nodes visited:", res30.nodes_visited, file=sys.stderr)

    print(f"Backtracking P(t) for Rule 90, t=1..{args.max_t_backtrack} (cross-check) ...", file=sys.stderr)
    res90_bt = count_p_backtracking(90, true_trace_90, args.max_t_backtrack)
    print("Rule 90 P(t) [backtracking]:", res90_bt.p_of_t, file=sys.stderr)

    print(f"Linear GF(2) exact P(t) for Rule 90, t=1..{args.max_t_linear} ...", file=sys.stderr)
    p90_linear = count_p_rule90_linear(true_trace_90, args.max_t_linear)
    print("Rule 90 P(t) [linear, first 24]:", {k: p90_linear[k] for k in range(1, min(24, args.max_t_linear) + 1)}, file=sys.stderr)

    # cross-check backtracking vs linear agree where both computed
    mismatches = []
    for k in range(1, args.max_t_backtrack + 1):
        if res90_bt.p_of_t.get(k) != p90_linear.get(k):
            mismatches.append((k, res90_bt.p_of_t.get(k), p90_linear.get(k)))
    print("Rule90 backtracking vs linear mismatches (should be empty):", mismatches, file=sys.stderr)

    print("Exhaustive edge-bijection check (does b_-k always toggle a'_k for EVERY prior setting)...", file=sys.stderr)
    max_k_bij = min(16, args.max_t_backtrack)
    bij30 = exhaustive_edge_bijection_check(30, max_k_bij)
    bij90 = exhaustive_edge_bijection_check(90, max_k_bij)
    print("Rule 30 bijective at every k:", bij30, file=sys.stderr)
    print("Rule 90 bijective at every k:", bij90, file=sys.stderr)

    # pin-density style statistics
    trace_one_density_30 = {
        t: sum(true_trace_30[:t]) / t for t in range(1, args.max_t_backtrack + 1)
    }
    trace_one_density_90 = {
        t: sum(true_trace_90[:t]) / t for t in range(1, args.max_t_linear + 1)
    }

    out = {
        "edge_bijection_check": {
            "rule30_bijective_at_every_k": bij30,
            "rule90_bijective_at_every_k": bij90,
        },
        "rule30": {
            "true_trace_prefix": true_trace_30[: args.max_t_backtrack + 2],
            "P_of_t": res30.p_of_t,
            "nodes_visited": res30.nodes_visited,
            "branch_history": res30.branch_history,
            "trace_one_density": trace_one_density_30,
        },
        "rule90": {
            "true_trace_prefix": true_trace_90[: args.max_t_linear + 2],
            "P_of_t_backtracking": res90_bt.p_of_t,
            "P_of_t_linear": p90_linear,
            "backtracking_vs_linear_mismatches": mismatches,
            "trace_one_density": trace_one_density_90,
        },
    }
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Wrote {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Throwaway verifier for PREREGISTRATION-SURVIVOR-DECAY.md Setup T1-T4 and
Controls 1-2.  NOT wired into any pipeline.  Uses the real, unmodified
``literal_extension`` (via ``dlp_rotated_wedge.rotated_wedge_population``,
itself calling ``late_pull_diagonal_sat.literal_extension`` directly) --
no reimplementation of the forced-continuation logic.

n range: 1..16 (no horizon extension past this, per instructions).
"""

from __future__ import annotations

import itertools
from collections import defaultdict

import numpy as np

from dlp_rotated_wedge import rotated_wedge_population

N_MAX = 15  # capped below the prereg's 16 ceiling for cost: exhaustive cost
# grows steeply per n (measured: n=12 took ~15s, n=16 projected ~10+ minutes
# for this single pass); n<=15 covers Control 1's n<=13 requirement with
# margin and gives two n values (14, 15) beyond it for the across-n
# stationarity check, at a total single-pass cost of a few minutes.
RESIDUES = (0, 1, 2)
TAILS = (2, 3)
TOL_STATIONARITY = 0.05
TOL_LAMBDA_FACTOR = 1.5
REFERENCE_LAMBDA = 0.4  # order-of-magnitude control target (0.4, 0.4062)


_CACHE: list | None = None


def all_continuations():
    """Yield (n, r, c, word, continuation, finite_endpoint, surviving) for
    every W in {1,2}^n, n=1..N_MAX, r in RESIDUES, c in TAILS.  This is the
    exhaustive small-n generation Setup T1 asks for, using the real
    ``rotated_wedge_population`` (hence the real ``literal_extension``).

    Materialized once and cached: this is called once per k value (k=1,2,3)
    plus once for the exact-count control, and ``literal_extension`` cost
    grows with n, so recomputing from scratch each time is wasteful (and,
    at n=16, was the cause of a 5-minute timeout on first run)."""
    global _CACHE
    if _CACHE is None:
        rows = []
        for n in range(1, N_MAX + 1):
            for word in itertools.product((1, 2), repeat=n):
                for c in TAILS:
                    for r in RESIDUES:
                        surviving, terminal_pull, finite_endpoint = rotated_wedge_population(
                            word, c, r
                        )
                        continuation = finite_endpoint[n:]
                        rows.append((n, r, c, word, continuation, finite_endpoint, surviving))
        _CACHE = rows
    return iter(_CACHE)


def build_context_table(k: int):
    """T1: for order k, tabulate counts[(ctx, row)][symbol] and also
    counts[(ctx, row, n)][symbol] so T2's two stationarity checks (across
    row, across n) can both be answered from one pass over the data.

    ctx = the k symbols of ``finite_endpoint`` immediately preceding the
    current forced continuation position (drawn from the full word+continuation
    sequence, so early continuation rows draw their context tail from W --
    this is the only sequence available and is not a reimplementation, just
    an index into the already-computed finite_endpoint).

    row = index within the continuation (0-based), matching literal_witness's
    own ``row`` enumeration.
    """
    by_row = defaultdict(lambda: defaultdict(int))       # (ctx, row) -> {1: c, 2: c, other: c}
    by_row_n = defaultdict(lambda: defaultdict(int))     # (ctx, row, n) -> {...}
    n_values_seen = set()

    for n, r, c, word, continuation, finite_endpoint, surviving in all_continuations():
        n_values_seen.add(n)
        for row, forced in enumerate(continuation):
            idx = n + row  # position of `forced` within finite_endpoint
            if idx < k:
                continue  # no full-length context available (only for n=0, never happens here)
            ctx = finite_endpoint[idx - k: idx]
            if any(v not in (1, 2) for v in ctx):
                continue  # context itself already left {1,2}; not a valid Markov state
            label = forced if forced in (1, 2) else "other"
            by_row[(ctx, row)][label] += 1
            by_row_n[(ctx, row, n)][label] += 1

    return by_row, by_row_n, sorted(n_values_seen)


def freq_1(counts: dict) -> float | None:
    total = sum(counts.values())
    if total == 0:
        return None
    ones = counts.get(1, 0)
    twos = counts.get(2, 0)
    other = counts.get("other", 0)
    if other:
        # symbol left {1,2}; frequency of "1 vs 2" is only over the {1,2} mass
        denom = ones + twos
        if denom == 0:
            return None
        return ones / denom
    return ones / total


def check_stationarity_across_row(by_row: dict, k: int):
    """(a) agree across row position for fixed ctx."""
    per_ctx_rows = defaultdict(dict)
    for (ctx, row), counts in by_row.items():
        f = freq_1(counts)
        if f is not None:
            per_ctx_rows[ctx][row] = (f, sum(v for v in counts.values()))

    report_lines = []
    max_spread = 0.0
    worst_ctx = None
    all_ok = True
    for ctx in sorted(per_ctx_rows):
        rows = per_ctx_rows[ctx]
        freqs = [f for f, _ in rows.values()]
        spread = max(freqs) - min(freqs) if freqs else 0.0
        ok = spread <= TOL_STATIONARITY
        all_ok = all_ok and ok
        if spread > max_spread:
            max_spread = spread
            worst_ctx = ctx
        report_lines.append(
            f"    ctx={ctx} k={k}: n_rows_seen={len(rows)} "
            f"freq_1 range=[{min(freqs):.4f}, {max(freqs):.4f}] "
            f"spread={spread:.4f} {'OK' if ok else 'FAIL'}"
        )
    return all_ok, max_spread, worst_ctx, report_lines


def check_stationarity_across_n(by_row_n: dict, k: int):
    """(b) agree across different n, for fixed ctx (pooling over row)."""
    per_ctx_n = defaultdict(lambda: defaultdict(lambda: [0, 0, 0]))  # ctx -> n -> [ones, twos, other]
    for (ctx, row, n), counts in by_row_n.items():
        bucket = per_ctx_n[ctx][n]
        bucket[0] += counts.get(1, 0)
        bucket[1] += counts.get(2, 0)
        bucket[2] += counts.get("other", 0)

    report_lines = []
    max_spread = 0.0
    worst_ctx = None
    all_ok = True
    for ctx in sorted(per_ctx_n):
        per_n = per_ctx_n[ctx]
        freqs = {}
        for n, (ones, twos, other) in per_n.items():
            denom = ones + twos
            if denom > 0:
                freqs[n] = ones / denom
        if not freqs:
            continue
        vals = list(freqs.values())
        spread = max(vals) - min(vals)
        ok = spread <= TOL_STATIONARITY
        all_ok = all_ok and ok
        if spread > max_spread:
            max_spread = spread
            worst_ctx = ctx
        report_lines.append(
            f"    ctx={ctx} k={k}: n range={min(freqs)}..{max(freqs)} over "
            f"{sorted(freqs)} freq_1 range=[{min(vals):.4f}, {max(vals):.4f}] "
            f"spread={spread:.4f} {'OK' if ok else 'FAIL'}"
        )
    return all_ok, max_spread, worst_ctx, report_lines


def pooled_transition_frequencies(by_row: dict, k: int):
    """Pool across row (and implicitly n) to get one P_hat(next|ctx) per ctx,
    for use in T3's transition matrix. Returns dict ctx -> (p1, p2, total_obs)."""
    pooled = defaultdict(lambda: [0, 0, 0])
    for (ctx, row), counts in by_row.items():
        pooled[ctx][0] += counts.get(1, 0)
        pooled[ctx][1] += counts.get(2, 0)
        pooled[ctx][2] += counts.get("other", 0)
    out = {}
    for ctx, (ones, twos, other) in pooled.items():
        denom = ones + twos
        total = ones + twos + other
        if denom == 0:
            continue
        out[ctx] = (ones / denom, twos / denom, total)
    return out


def perron_frobenius_lambda(pooled: dict, k: int):
    """Build the order-k chain's transition matrix on states = {1,2}^k,
    restricted to the substochastic 'no-11-yet' block: exclude any state
    that itself contains '11' (already dead), and any transition that would
    create '11' contributes zero (it is already zero empirically, since the
    hard-core check forbids it, but we zero it explicitly here to build the
    *restricted* block per the document's construction, rather than relying
    on empirical rarity alone).

    Transition state->state: ctx = (s_1..s_k) -> next symbol v -> new ctx =
    (s_2..s_k, v). Weight = P_hat(v | ctx). A transition is excluded from
    the 'alive' block if the new context contains adjacent (1,1) anywhere,
    i.e. represents having produced an 11 (dead).
    """
    states = [s for s in itertools.product((1, 2), repeat=k)
              if not any(s[i] == s[i + 1] == 1 for i in range(k - 1))]
    state_index = {s: i for i, s in enumerate(states)}
    m = len(states)
    P = np.zeros((m, m))
    for ctx, (p1, p2, total) in pooled.items():
        if ctx not in state_index:
            continue  # ctx itself already contains 11 (already dead going in)
        i = state_index[ctx]
        for v, p in ((1, p1), (2, p2)):
            new_ctx = ctx[1:] + (v,)
            # alive iff no adjacent 11 anywhere in new_ctx, i.e. specifically
            # the junction ctx[-1]==1 and v==1 (only new adjacency introduced)
            if ctx[-1] == 1 and v == 1:
                continue  # this transition produces 11: excluded from alive block (weight 0)
            if new_ctx in state_index:
                P[i, state_index[new_ctx]] += p
            # else: new_ctx contains 11 elsewhere already excluded by state list construction
    eigvals = np.linalg.eigvals(P)
    lam = max(abs(eigvals)) if len(eigvals) else float("nan")
    return lam, states, P


def control1_predicted_zero(pooled: dict, k: int):
    """Control 1: using the fitted chain's transition probabilities, compute
    the model-predicted probability of reaching the exact terminal_pull
    pattern (last two forced symbols == (1,2)) after L = n+r+2 steps without
    ever producing 11, for each n<=13 already covered by the exact
    enumeration. Multiply by 2^n to get a predicted count and compare
    against the real exact count (established/observed to be 0 for n<=13).

    This is necessarily a coarse, honestly-labeled operationalization: a
    nondegenerate stochastic chain essentially never assigns *exactly* zero
    probability to a specific finite-length event (only structurally
    forbidden transitions get exact zero), so the meaningful comparison is
    whether the predicted count is order-1-or-more (contradicting real
    exact emptiness) versus negligible (consistent with it, in a
    rounding sense -- not a proof of the real zero).
    """
    _, states, P = perron_frobenius_lambda(pooled, k)
    state_index = {s: i for i, s in enumerate(states)}
    lines = []
    for n in range(1, 14):
        for r in RESIDUES:
            L = n + r + 2
            # Start distribution: uniform over all length-k contexts observed
            # (approximates "any W"); walk L-k steps then check last two
            # symbols of the resulting state path. We approximate via matrix
            # powers of P and read off mass reaching states ending in (..,1,2)
            # after enough steps, which requires k<=2 to align directly with
            # the terminal pair. For k>2 we treat this as a coarser check on
            # the trailing 2 symbols of the state label.
            if L < k:
                continue
            v0 = np.ones(len(states)) / len(states)
            Pk = np.linalg.matrix_power(P, max(L - k, 0))
            v = v0 @ Pk
            target_mass = sum(
                v[i] for i, s in enumerate(states) if s[-2:] == (1, 2)
            ) if k >= 2 else float("nan")
            predicted_count = target_mass * (2 ** n) if target_mass == target_mass else float("nan")
            lines.append((n, r, predicted_count))
    return lines


def run_k(k: int, label: str):
    print(f"\n{'=' * 70}\nORDER k={k} ({label})\n{'=' * 70}")
    by_row, by_row_n, ns_seen = build_context_table(k)
    print(f"n values covered: {ns_seen}")

    print(f"\n--- T2(a): stationarity across row position, fixed ctx, k={k} ---")
    ok_a, spread_a, worst_a, lines_a = check_stationarity_across_row(by_row, k)
    for line in lines_a:
        print(line)
    print(f"  => across-row stationarity: {'PASS' if ok_a else 'FAIL'} "
          f"(max spread {spread_a:.4f} at ctx={worst_a}, tol={TOL_STATIONARITY})")

    print(f"\n--- T2(b): stationarity across n, fixed ctx, k={k} ---")
    ok_b, spread_b, worst_b, lines_b = check_stationarity_across_n(by_row_n, k)
    for line in lines_b:
        print(line)
    print(f"  => across-n stationarity: {'PASS' if ok_b else 'FAIL'} "
          f"(max spread {spread_b:.4f} at ctx={worst_b}, tol={TOL_STATIONARITY})")

    overall_pass = ok_a and ok_b
    print(f"\n  ==> T2 OVERALL for k={k}: {'PASS' if overall_pass else 'FAIL'}")

    pooled = pooled_transition_frequencies(by_row, k)
    print(f"\n  Pooled P_hat(next=1|ctx) for k={k}:")
    for ctx in sorted(pooled):
        p1, p2, total = pooled[ctx]
        print(f"    ctx={ctx}: P(next=1)={p1:.4f} P(next=2)={p2:.4f} n_obs={total}")

    return overall_pass, pooled, by_row


def main():
    print("PREREGISTRATION-SURVIVOR-DECAY.md Setup T1-T4 + Controls 1-2")
    print(f"n range: 1..{N_MAX}, residues={RESIDUES}, tails={TAILS}")
    print(f"stationarity tolerance: {TOL_STATIONARITY}, lambda factor tolerance: {TOL_LAMBDA_FACTOR}")

    print(f"\n{'=' * 70}\nEXACT H_r(n) SURVIVOR COUNTS (real, from rotated_wedge_population)\n{'=' * 70}")
    exact_counts = defaultdict(int)
    for n, r, c, word, continuation, finite_endpoint, surviving in all_continuations():
        if surviving:
            exact_counts[(n, r, c)] += 1
    nonzero_le_13 = []
    for n in range(1, N_MAX + 1):
        row = []
        for r in RESIDUES:
            for c in TAILS:
                cnt = exact_counts.get((n, r, c), 0)
                row.append(f"r={r},c={c}:{cnt}")
                if n <= 13 and cnt != 0:
                    nonzero_le_13.append((n, r, c, cnt))
        print(f"  n={n:2d}: " + "  ".join(row))
    if nonzero_le_13:
        print(f"\n  WARNING: nonzero exact survivor count(s) found at n<=13: {nonzero_le_13}")
        print("  This contradicts the established emptiness claim -- Control 1's baseline is not what was assumed.")
    else:
        print("\n  Confirmed: exact H_r(n) survivor count is 0 for all n<=13, all r, all c (matches established record).")

    # ---- Control 2: k=1 (expected to fail) ----
    pass1, pooled1, by_row1 = run_k(1, "Control 2 -- expected to fail stationarity")

    # ---- T1/T2 at k=2 ----
    pass2, pooled2, by_row2 = run_k(2, "primary target order")

    used_k = None
    used_pooled = None
    if pass2:
        used_k, used_pooled = 2, pooled2
    else:
        print("\nk=2 FAILED T2. Per T4, trying k=3 once before declaring the mechanism dead.")
        pass3, pooled3, by_row3 = run_k(3, "T4 fallback, one bump only")
        if pass3:
            used_k, used_pooled = 3, pooled3

    print(f"\n{'=' * 70}\nKILL CONDITION (section 6)\n{'=' * 70}")
    if used_k is None:
        print("KILL CONDITION FIRED: stationarity failed at both k=2 and k=3.")
        print("Per section 6, the route is DEAD: the process depends on deep/growing")
        print("history in a way that defeats any finite-order Markov description of")
        print("the output symbols themselves.")
    else:
        print(f"Stationarity PASSED at k={used_k}. Proceeding to T3.")
        lam, states, P = perron_frobenius_lambda(used_pooled, used_k)
        print(f"\n--- T3: Perron-Frobenius lambda on 'no-11-yet' substochastic block, k={used_k} ---")
        print(f"states (alive, no-11): {states}")
        print("transition matrix P (rows=from-state, cols=to-state):")
        print(P)
        print(f"lambda (max |eigenvalue|) = {lam:.6f}")
        lo, hi = REFERENCE_LAMBDA / TOL_LAMBDA_FACTOR, REFERENCE_LAMBDA * TOL_LAMBDA_FACTOR
        in_tol = lo <= lam <= hi
        print(f"reference constant ~{REFERENCE_LAMBDA} (flip_pairing 0.4^j, endpoint-coord 0.4062)")
        print(f"factor-{TOL_LAMBDA_FACTOR} tolerance window: [{lo:.4f}, {hi:.4f}] "
              f"=> {'WITHIN TOLERANCE (control)' if in_tol else 'OUTSIDE TOLERANCE (control)'}")
        secondary_kill = lam >= 1
        if secondary_kill:
            print(f"\nSECONDARY (soft) KILL: lambda={lam:.6f} >= 1. Chain predicts growth, not decay.")
            print("Technically stationary/valid but useless for the decay purpose. Recorded as such.")

    print(f"\n{'=' * 70}\nCONTROL 1: exact small-n path-count check (n<=13)\n{'=' * 70}")
    check_k = used_k if used_k is not None else 2
    check_pooled = used_pooled if used_pooled is not None else pooled2
    print(f"(using k={check_k} fitted chain even if T2 failed, to report the comparison honestly)")
    control1_lines = control1_predicted_zero(check_pooled, check_k)
    print("n, r, predicted_count (chain model) vs real exact count (established empty for n<=13)")
    any_nonzero = False
    for n, r, predicted in control1_lines:
        flag = ""
        if predicted == predicted and predicted >= 0.5:  # not NaN and materially nonzero
            flag = "  <-- MODEL PREDICTS NONZERO where real count is exactly 0 (per prior exact enumeration)"
            any_nonzero = True
        print(f"  n={n:2d} r={r}: predicted={predicted:.6g}{flag}")
    print(f"\nControl 1 verdict: {'FAIL (model over-predicts nonzero count)' if any_nonzero else 'PASS (model predicts negligible/zero count, consistent with real exact emptiness)'}")
    if any_nonzero:
        print("Per the preregistration, this OVERRIDES a T2/T3 pass: the model is wrong")
        print("regardless of stationarity/lambda results above.")

    print(f"\n{'=' * 70}\nCONTROL 2 SUMMARY (k=1)\n{'=' * 70}")
    print(f"k=1 stationarity: {'PASS (unexpected)' if pass1 else 'FAIL (expected)'}")


if __name__ == "__main__":
    main()

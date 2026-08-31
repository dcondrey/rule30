"""Decouple window width W from prefix length t and re-verify the closed form.

`preimage_count_probe.py` always uses the "aligned" case W = t (window
{-t,...,-1} matched against prefix a_0..a_{t-1}), which a skeptical reader
could dismiss as trivial-by-dimension-matching: t free bits against t-1 real
constraints, so of course only one bit of freedom is left over.

This script checks the general claim implied by the same theorem
(`preimage_count_probe.exhaustive_edge_bijection_check`): for ANY window
width W >= t-1, holding bits at {-1,...,-(t-1)} each uniquely forced by
a_1..a_{t-1} in turn (the edge-bijection theorem, one bit per constraint) and
every bit at {-t,...,-W} free (outside the light cone of a_0..a_{t-1}
entirely), the exact closed form is

    P(W, t) = 2 ** (W - t + 1)

independent of the rule (checked for Rule 30 and Rule 90) and independent of
whether the target trace is periodic (Rule 90's true trace) or not (Rule
30's).  Brute force (2^W enumeration) is used here since W is kept small
(<=12); this is a direct, non-recursive cross-check of the backtracking
result in `preimage_count_probe.py`, run over a grid of (W, t) pairs so the
"aligned" case is not the only one tested.
"""

from __future__ import annotations

from itertools import product

from preimage_count_probe import forward_rule, true_lone_seed_trace


def brute_p(rule: int, true_trace: list[int], W: int, t: int) -> int:
    """Exact P(W, t): window {-W,...,-1}, matched against a_0..a_{t-1}."""
    width = 2 * W + 1
    center = W
    count = 0
    for bits in product((0, 1), repeat=W):
        row = [0] * width
        for j in range(1, W + 1):
            row[center - j] = bits[j - 1]  # b_{-j}
        row[center] = 1  # true seed
        cur = row
        trace = [cur[center]]
        for _ in range(t - 1):
            new_row = [0] * width
            for x in range(1, width - 1):
                new_row[x] = forward_rule(rule, cur[x - 1], cur[x], cur[x + 1])
            cur = new_row
            trace.append(cur[center])
        if trace == true_trace[:t]:
            count += 1
    return count


def main() -> None:
    max_len = 25
    true_trace_30 = true_lone_seed_trace(30, max_len)
    true_trace_90 = true_lone_seed_trace(90, max_len)

    grid = [
        (3, 3), (5, 3), (6, 3),
        (4, 4), (6, 4), (8, 4),
        (6, 6), (8, 6), (10, 6),
        (10, 10), (12, 10),
    ]
    print(f"{'W':>3} {'t':>3} {'predicted 2^(W-t+1)':>20} {'rule30':>8} {'rule90':>8}  match?")
    all_match = True
    for W, t in grid:
        p30 = brute_p(30, true_trace_30, W, t)
        p90 = brute_p(90, true_trace_90, W, t)
        pred = 2 ** (W - t + 1)
        ok = (p30 == pred) and (p90 == pred)
        all_match &= ok
        print(f"{W:>3} {t:>3} {pred:>20} {p30:>8} {p90:>8}  {'OK' if ok else 'MISMATCH'}")
    print()
    print("ALL MATCH" if all_match else "SOME MISMATCH -- theorem falsified, do not report as proved")


if __name__ == "__main__":
    main()

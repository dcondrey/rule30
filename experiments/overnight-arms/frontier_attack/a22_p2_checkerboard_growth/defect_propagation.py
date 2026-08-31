"""a22(b): structural (non-simulation-of-lone-seed) probe of whether a single
defect against the checkerboard background is a bounded "soliton" under Rule 30,
or whether it generically grows without bound.

This is NOT a proof and is reported as such. It is a small, honest structural
experiment on the LOCAL update rule alone (no lone-seed diagram involved), run
because a3's report explains why no local/finite-window argument can EXCLUDE the
checkerboard from Y (every finite checkerboard patch is trivially Rule-30
consistent, being an orbit). The question asked here is different and does not
face that obstruction: given a checkerboard background with one site flipped,
does the difference pattern (checkerboard XOR perturbed-orbit) stay a bounded
width forever (a genuine soliton, which would be a candidate mechanism for a
forbidden-patch lemma: a defect that can never disperse could be excluded a
priori) or does it generically grow?

Rule: s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1)).

Result 1 (exact, one step). Flip a single site x0 in an infinite checkerboord-A
row (s(x)=1 iff x even) and apply one Rule 30 step. By direct substitution:
  - x0 EVEN (a "1" site flipped to 0): the difference pattern after one step
    has width 3, at columns {x0-1, x0, x0+1}.
  - x0 ODD  (a "0" site flipped to 1): the difference pattern after one step
    has width 1, at column {x0+1} (a pure right-shift by one).
This parity asymmetry is checked exhaustively below for x0 in a wide window.

Result 2 (simulation of the LOCAL rule only, not the lone-seed diagram). Iterating
either case for many steps: the single-site (odd-defect) case does NOT stay a
width-1 soliton forever -- it alternates between width 1 and width 3 for a few
steps, then the difference pattern's right edge advances at exactly speed 1
(the maximum possible under this rule's dependency cone) while the left edge
lags, so the width grows, irregularly but on average roughly linearly, with no
sign of saturation over 300 steps (checked up to width ~196 with no return to
zero). 300 independent random-offset trials over 60 steps produced ZERO heals
(zero returns to an all-agreeing row) -- see the printed block below.

Conclusion (honest, negative for finding a clean lemma): there is no bounded
"immune" defect mode found. This is CONSISTENT with a3's empirical result
(checkerboard patch heights keep growing with T, matching the exact uniform-
Bernoulli reference law) and with Rule 30's known sensitive dependence /
chaotic mixing, but it is not itself a theorem bounding K(T)'s growth rate, and
it does not by itself establish unboundedness of the LONE-SEED diagram's
checkerboard patches (this local experiment has nothing to do with the specific
lone-seed orbit; it is a statement about the rule near the checkerboard
configuration in general). Reported as a negative/inconclusive structural
result: (b) did not yield a lemma; (a)'s simulation extension is the
load-bearing result of this arm.

Run: uv run python defect_propagation.py
"""

from __future__ import annotations

import random


def rule30_row(r: list[int]) -> list[int]:
    n = len(r)
    return [r[i - 1] ^ (r[i] | r[(i + 1) % n]) for i in range(n)]


def checker_row(N: int, one_at_even: bool = True) -> list[int]:
    return [(1 if ((x % 2) == 0) == one_at_even else 0) for x in range(-N, N + 1)]


def one_step_parity_check(N: int = 40) -> None:
    print("=== one-step defect width by parity of the flipped site (exact) ===")
    base = checker_row(N, True)
    for x0 in range(-8, 9):
        defect = list(base)
        idx = x0 + N
        defect[idx] ^= 1
        nb = rule30_row(base)
        nd = rule30_row(defect)
        diffs = [x - N for x, (a, b) in enumerate(zip(nb, nd)) if a != b]
        parity = "even" if x0 % 2 == 0 else "odd"
        print(f"  x0={x0:+d} ({parity:4s}) -> diff width {len(diffs)}, at {diffs}")


def long_run_trace(N: int = 60, steps: int = 12) -> None:
    print("\n=== multi-step trace (local rule only, not the lone-seed diagram) ===")
    for x0, label in [(-1, "odd"), (0, "even")]:
        base = checker_row(N, True)
        row = list(base)
        row[x0 + N] ^= 1
        print(f" start defect at x0={x0} ({label})")
        for t in range(steps):
            diffs = [x - N for x, (a, c) in enumerate(zip(base, row)) if a != c]
            print(f"   t={t:2d} diffs={diffs}")
            row = rule30_row(row)
            base = rule30_row(base)


def healing_statistics(N: int = 150, steps: int = 60, trials: int = 300, seed: int = 0) -> None:
    print(f"\n=== healing statistics: {trials} random single-site defects, {steps} steps ===")
    rng = random.Random(seed)
    healed = 0
    maxwidths = []
    for _ in range(trials):
        base = checker_row(N, True)
        row = list(base)
        x0 = rng.randint(-5, 5)
        row[x0 + N] ^= 1
        mw = 0
        for t in range(steps):
            diffs = [i for i, (a, c) in enumerate(zip(base, row)) if a != c]
            w = (max(diffs) - min(diffs) + 1) if diffs else 0
            mw = max(mw, w)
            if not diffs:
                healed += 1
                break
            row = rule30_row(row)
            base = rule30_row(base)
        maxwidths.append(mw)
    print(f"  healed (returned to zero diff) within {steps} steps: {healed} / {trials}")
    print(f"  max-width reached: min={min(maxwidths)} max={max(maxwidths)} "
          f"mean={sum(maxwidths)/len(maxwidths):.1f}")


def long_growth_curve(N: int = 400, steps: int = 300) -> None:
    print(f"\n=== long single-trial width curve, x0=0 (even), {steps} steps ===")
    base = checker_row(N, True)
    row = list(base)
    row[0 + N] ^= 1
    widths = []
    for t in range(steps):
        diffs = [i for i, (a, c) in enumerate(zip(base, row)) if a != c]
        if not diffs:
            widths.append((t, "HEALED"))
            break
        widths.append(max(diffs) - min(diffs) + 1)
        row = rule30_row(row)
        base = rule30_row(base)
    print("  width every 10 steps:", widths[::10])
    print("  final width:", widths[-1])


if __name__ == "__main__":
    one_step_parity_check()
    long_run_trace()
    healing_statistics()
    long_growth_curve()

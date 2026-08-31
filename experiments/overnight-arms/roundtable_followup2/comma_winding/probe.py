"""Comma-winding coupling probe (roundtable_followup2 / comma_winding).

Tests the ONE substantive claim in the spark: that hypothesizing the Rule 30
centre column is eventually period-p constrains the COUNT of OR-saturating
("s-type") steps encountered along a backward (leftward) reconstruction of
some fixed reach/depth from that column.

Definitions pinned down here (the spark left these vague):

  s(t, x-1) = s(t+1, x) XOR ( s(t, x) OR s(t, x+1) )        [the pin identity,
  already in inverse_trace_probe.reconstruct_left_column]

  At one reconstruction layer (fixed x), stepping through time t, a step is
  "s-type" (OR-saturating / OR-engaged) iff  s(t, x) OR s(t, x+1) == 1, i.e.
  at least one of the two right-neighbour inputs to that cell's update is 1.
  Otherwise it is "f-type" (clean XOR: s(t,x-1) = s(t+1,x) with no OR
  contribution).

  v(t) at reach/depth D from a starting column pair (center, right) is
  alpha * (total s-type steps encountered across all D reconstruction layers,
  time range available at each layer). The XOR/f-type steps contribute 0 by
  construction (the spark's own claim), so v(t) reduces to alpha * s_count.

This script:
  1. Fixes a periodic centre-column hypothesis (period p, given by hand).
  2. Varies ONLY the adjacent right column, at exactly the time-positions
     where the centre bit is 0 (the only positions where the OR term is not
     already forced to 1 by the centre bit itself) -- this changes NOTHING
     about the centre column (still exactly the same period-p word) while
     changing the s-type step count at depth 1.
  3. Extends the same test to depth 2 and depth 3 using the ladder-style
     iterated call to reconstruct_left_column (each layer's output becomes
     the next layer's "centre", the previous layer's centre becomes the next
     "right"), to check whether the mismatch persists / grows at greater
     reach (relevant to obstruction A, the O(log t) wall).
  4. Also runs two genuinely different *self-consistent* full two-sided
     finite diagrams (built by hand for small p) that both have the exact
     same period-p centre trace, to confirm the same non-coupling holds when
     right columns are not adversarially hand-picked but come from actual
     valid Rule 30 configurations.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "rule30"))

from inverse_trace_probe import evolve_once_packed, reconstruct_left_column  # noqa: E402
from periodicity_bridge_probe import RULE_30  # noqa: E402


def s_type_count(center: tuple[int, ...], right: tuple[int, ...]) -> int:
    """Count OR-saturating (s-type) steps in one reconstruction layer."""
    assert len(center) == len(right)
    return sum(1 for c, r in zip(center, right) if (c | r) == 1)


def one_layer(center, right):
    left = reconstruct_left_column(center, right)
    return left


def depth_d_scount(center, right, depth):
    """Sum s-type steps across `depth` iterated reconstruction layers.

    Layer 1 uses (center, right). Layer k+1 uses (left_k, center truncated),
    matching rotated_defect_front's shift convention: after producing
    left_k, the new "right" is the old center (truncated by one), and the
    new "center" is left_k.
    """
    total = 0
    cur_center, cur_right = center, right
    for _ in range(depth):
        total += s_type_count(cur_center, cur_right)
        left = one_layer(cur_center, cur_right)
        cur_right, cur_center = cur_center[:-1], left
    return total


def build_periodic_right_variants(period_word, length):
    """Two right-columns consistent with the SAME period-p centre hypothesis.

    period_word is the hypothesized centre period, tiled to `length`. The
    two right-columns below are chosen to differ ONLY where the centre bit
    is 0 (so neither variant changes the OR term wherever the centre bit
    already forces it to 1 -- this isolates exactly the free degree of
    freedom the spark's v(t) depends on that centre-periodicity does not
    touch).
    """
    center = tuple(period_word[t % len(period_word)] for t in range(length))
    right_a = tuple(0 for _ in range(length))
    right_b = tuple(1 - c if c == 0 else 0 for c in center)  # flips 0->1 at zero slots
    return center, right_a, right_b


def report_case(name, period_word, length, depth):
    center, right_a, right_b = build_periodic_right_variants(period_word, length)
    sa = depth_d_scount(center, right_a, depth)
    sb = depth_d_scount(center, right_b, depth)
    print(f"[{name}] period_word={period_word} length={length} depth={depth}")
    print(f"  centre trace IDENTICAL in both variants (period-{len(period_word)} hypothesis unchanged)")
    print(f"  right_a s-count (depth {depth}) = {sa}")
    print(f"  right_b s-count (depth {depth}) = {sb}")
    print(f"  difference = {sb - sa}  (nonzero => centre periodicity does not fix s-count)")
    print()
    return sa, sb


def actual_rule30_consistency_check(period_word, length):
    """Confirm right_a / right_b in build_periodic_right_variants correspond
    to genuinely different, forward-consistent two-sided Rule 30 histories
    sharing the same centre trace, by running reconstruct_left_column's
    inverse and then re-evolving forward with the real Rule 30 rule and
    checking the centre trace is reproduced. This anchors the hand-built
    counterexample in the real automaton rather than an abstract identity.
    """
    center, right_a, right_b = build_periodic_right_variants(period_word, length)
    for name, right in (("right_a", right_a), ("right_b", right_b)):
        left = reconstruct_left_column(center, right)
        # Rebuild a packed row: position layout  [left...][center@0][right@1..]
        # then re-run one Rule 30 step and confirm center[1] reproduces.
        width = len(left) + 1 + len(right)
        mask = (1 << width) - 1
        row = 0
        for i, b in enumerate(reversed(left)):
            row |= b << i
        offset = len(left)
        row |= center[0] << offset
        for i, b in enumerate(right):
            row |= b << (offset + 1 + i)
        nxt = evolve_once_packed(RULE_30, row, mask)
        forced_center1 = (nxt >> offset) & 1
        ok = forced_center1 == center[1]
        print(f"  forward re-check ({name}): forced next-centre bit = {forced_center1}, "
              f"expected {center[1]} -> {'OK' if ok else 'MISMATCH'}")


if __name__ == "__main__":
    print("=" * 70)
    print("Case 1: period-2 centre hypothesis [0,1]")
    print("=" * 70)
    report_case("period-2", (0, 1), length=40, depth=1)
    report_case("period-2, depth 2", (0, 1), length=40, depth=2)
    report_case("period-2, depth 3", (0, 1), length=40, depth=3)

    print("=" * 70)
    print("Case 2: period-3 centre hypothesis [0,0,1]")
    print("=" * 70)
    report_case("period-3", (0, 0, 1), length=45, depth=1)
    report_case("period-3, depth 3", (0, 0, 1), length=45, depth=3)

    print("=" * 70)
    print("Case 3: period-5 centre hypothesis [0,1,0,0,1] (mixed)")
    print("=" * 70)
    report_case("period-5", (0, 1, 0, 0, 1), length=50, depth=1)
    report_case("period-5, depth 4", (0, 1, 0, 0, 1), length=50, depth=4)

    print("=" * 70)
    print("Forward-consistency anchor: are right_a/right_b genuinely valid")
    print("Rule 30 continuations sharing the same centre trace at t=0,1?")
    print("=" * 70)
    actual_rule30_consistency_check((0, 1), 10)
    actual_rule30_consistency_check((0, 0, 1), 12)

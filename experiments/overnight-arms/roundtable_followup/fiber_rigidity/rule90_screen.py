"""Rule 90 screen for the fibre-rigidity proposal.

Rule 90: f(a,b,c) = a XOR c.  Left-permutive, so the same triangular inverse
scheme as Rule 30 applies, but the inverse relation is purely linear:

    col_x(t+1) = col_{x-1}(t) XOR col_{x+1}(t)
    =>  col_{x-1}(t) = col_x(t+1) XOR col_{x+1}(t)

Unlike Rule 30's `col_{x-1}(t) = col_x(t+1) XOR (col_x(t) OR col_{x+1}(t))`,
there is no OR term and hence no state (`col_x(t)=1`) that can *saturate* and
erase an incoming defect.  A one-bit discrepancy in the right column XORs
straight through, unattenuated, forever.  This is the algebraic reason the
panel gives for why the interface-rigidity lemma should fail for Rule 90; this
script checks it by direct construction rather than trusting the assertion.
"""
from __future__ import annotations


def reconstruct_left_column_90(center_column, right_column):
    if len(center_column) != len(right_column):
        raise ValueError("columns must have equal length")
    return tuple(
        center_column[t + 1] ^ right_column[t]
        for t in range(len(center_column) - 1)
    )


def rotated_defect_front_90(period_word, perturbation_time, left_steps):
    length = perturbation_time + left_steps + len(period_word) + 2
    common_center = tuple(period_word[t % len(period_word)] for t in range(length))
    baseline_right = (0,) * length
    changed_right = tuple(int(t == perturbation_time) for t in range(length))
    baseline_center = common_center
    changed_center = common_center
    front = []
    for _ in range(left_steps):
        baseline_left = reconstruct_left_column_90(baseline_center, baseline_right)
        changed_left = reconstruct_left_column_90(changed_center, changed_right)
        first = next(
            (t for t, (a, b) in enumerate(zip(baseline_left, changed_left)) if a != b),
            None,
        )
        front.append(first)
        baseline_right, baseline_center = baseline_center[:-1], baseline_left
        changed_right, changed_center = changed_center[:-1], changed_left
    return tuple(front)


def main() -> None:
    # p=1 word=(0,), the actual Rule 90 lone-seed asymptotic trace (zero for t>0).
    print("rule 90, p=1 word=(0,), perturbation at t=64, 40 leftward steps:")
    print(rotated_defect_front_90((0,), 64, 40))
    print()
    # p=1 word=(1,), the constant-one control (never occurs for lone seed, but
    # exercises whether Rule 90 ever erases at all).
    print("rule 90, p=1 word=(1,), perturbation at t=64, 40 leftward steps:")
    print(rotated_defect_front_90((1,), 64, 40))
    print()
    print("rule 90, p=2 word=(0,1), perturbation at t=64 and t=65, 40 leftward steps:")
    print(rotated_defect_front_90((0, 1), 64, 40))
    print(rotated_defect_front_90((0, 1), 65, 40))


if __name__ == "__main__":
    main()

"""Test whether the cheapest formalization of the spark's "type" invariant
(each cell's value as a Boolean function of a single formal seed variable s,
i.e. an element of the free Boolean algebra on one generator, GF(2)[s]/(s^2=s))
carries any information beyond the ordinary bit value.

Method: run TWO bit-parallel Rule 30 (or Rule 90) simulations side by side,
one starting from the true lone seed (s := 1), one from an all-zero row
(s := 0).  A cell's "type", as a Boolean function of s, is fully determined
(since a 1-variable Boolean function is determined by its two values) by the
pair (value-at-s=0, value-at-s=1).  This is exactly the free Boolean algebra
on one generator: it has exactly 4 elements {0, 1, s, not-s}, corresponding
to pairs (0,0), (1,1), (0,1), (1,0) respectively.

Claim to check: the s=0 branch is identically 0 forever (the all-zero
configuration is a fixed point of both rules), which collapses the reachable
type-pairs from 4 down to 2: {(0,0), (0,1)} = {"0", "s"} only.  That means
type == bit, exactly, with no residual freedom.
"""
import sys


def step_rule30(row: int) -> int:
    return (row << 1) ^ (row | (row >> 1))


def step_rule90(row: int) -> int:
    return (row << 1) ^ (row >> 1)


def run(step_fn, steps: int, seed_bit: int):
    off = steps + 2
    row = seed_bit << off
    out = bytearray(steps)
    for t in range(steps):
        out[t] = (row >> off) & 1
        row = step_fn(row)
    return bytes(out)


def check(rule_name: str, step_fn, steps: int):
    zero_branch = run(step_fn, steps, 0)
    one_branch = run(step_fn, steps, 1)
    assert all(b == 0 for b in zero_branch), (
        f"{rule_name}: s=0 branch is NOT identically zero -- "
        f"the type/bit collapse argument does not apply"
    )
    # type pair at each t is (zero_branch[t], one_branch[t]) = (0, bit[t])
    # reachable pairs:
    pairs = sorted(set(zip(zero_branch, one_branch)))
    n_ones = sum(one_branch)
    print(f"{rule_name}: steps={steps}")
    print(f"  s=0 branch identically zero: {all(b==0 for b in zero_branch)}")
    print(f"  distinct (val@s=0, val@s=1) type-pairs realized: {pairs}")
    print(f"  bit-1 count in true (s=1) orbit: {n_ones}/{steps}")
    print(f"  => type is a bijective relabeling of bit: {len(pairs) <= 2}")
    return pairs


if __name__ == "__main__":
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    print("=" * 60)
    check("Rule 30", step_rule30, steps)
    print("=" * 60)
    check("Rule 90", step_rule90, steps)

"""Shared substrate for the R1 zero-set attack (this directory only). Stdlib only.

Scope: PATH.md route R1 -- the OR-latch pin (section 1-2) and its stated
obligation "c eventually periodic => r|_{c=0} eventually periodic" (★).  This
file provides:

  1. A read-only cross-check against the repo's ground-truth generator
     (experiments/rule30/center_column.py) and the overnight-arms common
     substrate, exactly as the a21/a7 arms did.
  2. A *driven quarter-plane* simulator: columns x=1..W evolve under the
     standard local rule, with column x=0 supplied externally at each time
     step (not evolved from column -1), and column x=W+1 supplied externally
     too (the "free boundary").  This is exactly the object in a21's Theorem S
     proof ("the quarter plane x>=1 is driven forward by the column x=0") and
     in PATH.md section 3, generalised to an explicit, adjustable right
     boundary so both a periodic-boundary and a random-boundary experiment can
     reuse the same stepper.

Conventions match experiments/overnight-arms/common/rule30.py:
    rule 30:  s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1))
    rule 90:  s(t+1,x) = s(t,x-1) XOR s(t,x+1)

Bit layout for the driven strip: an integer V with W bits, bit i (0-indexed)
holding s(t, i+1) for i = 0..W-1 (so bit 0 is column x=1, bit W-1 is column
x=W).  Left neighbour of bit i is s(t,i) = bit (i-1) of V for i>=1, and the
externally supplied c_t for i=0.  Right neighbour of bit i is s(t,i+2) = bit
(i+1) of V for i<=W-2, and the externally supplied boundary bit for i=W-1.
"""

from __future__ import annotations

import importlib.util
import sys

_COMMON = "/Volumes/A/researchpapers/13-rule30/experiments/overnight-arms/common/rule30.py"
_REPO_CENTER = "/Volumes/A/researchpapers/13-rule30/experiments/rule30/center_column.py"


def _load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


COMMON = _load(_COMMON, "r1za_common_rule30")


def step_driven(v: int, w: int, c_bit: int, boundary_bit: int, rule: int) -> int:
    """One step of the driven quarter-plane, columns 1..w, rule in {30, 90}.

    c_bit is the externally supplied value of column 0 at the CURRENT step
    (i.e. the left neighbour fed into column 1's update).  boundary_bit is the
    externally supplied value of column w+1 at the current step (the right
    neighbour fed into column w's update).  Returns the new w-bit state.
    """
    mask = (1 << w) - 1
    left = ((v << 1) | c_bit) & mask
    right = ((v >> 1) | (boundary_bit << (w - 1))) & mask
    if rule == 30:
        return (left ^ (v | right)) & mask
    if rule == 90:
        return (left ^ right) & mask
    raise ValueError(f"unsupported rule {rule}")


def bit(v: int, i: int) -> int:
    """s(t, i+1) i.e. column i+1 (0-indexed bit)."""
    return (v >> i) & 1


def _naive_two_sided_grid(seed: dict[int, int], n: int, rule: int) -> list[dict[int, int]]:
    """Independent dict-based simulator, both rules, for cross-validation."""
    grid = [dict(seed)]
    cur = {x: v for x, v in seed.items() if v}
    for _ in range(n - 1):
        if cur:
            lo, hi = min(cur) - 1, max(cur) + 1
        else:
            lo, hi = 0, 0
        nxt = {}
        for x in range(lo, hi + 1):
            l = cur.get(x - 1, 0)
            c = cur.get(x, 0)
            r = cur.get(x + 1, 0)
            v = (l ^ (c | r)) if rule == 30 else (l ^ r)
            if v:
                nxt[x] = 1
        grid.append(nxt)
        cur = nxt
    return grid


def selftest() -> None:
    import random

    # 1. Ground truth: lone-seed centre column, rule 30, vs repo generator via common.
    n = 4096
    repo_bits = list(_load(_REPO_CENTER, "r1za_repo_center").center_column(n))[:n]
    assert COMMON.center_column_bits(n) == repo_bits, (
        "type mismatch or real divergence -- center_column() returns bytes, "
        "must list()-wrap before comparing to a list[int]"
    )

    # 2. Driven quarter-plane reproduces a genuine two-sided lone-seed diagram
    #    when c_t and the boundary are both taken FROM that same true diagram
    #    (not externally imposed) -- i.e. the driven stepper is not a new rule,
    #    it is the real rule restricted to a strip, fed its own true edges.
    rng = random.Random(20260904)
    for rule in (30, 90):
        for _ in range(150):
            w = rng.randint(1, 12)
            width_seed = rng.randint(1, 10)
            bits = [rng.randint(0, 1) for _ in range(width_seed)]
            if not any(bits):
                bits[0] = 1
            seed = {-j: b for j, b in enumerate(bits) if b}
            T = 30
            grid = _naive_two_sided_grid(seed, T + 1, rule)
            v = 0
            for x in range(1, w + 1):
                if grid[0].get(x, 0):
                    v |= 1 << (x - 1)
            for t in range(T):
                c_bit = grid[t].get(0, 0)
                boundary_bit = grid[t].get(w + 1, 0)
                v = step_driven(v, w, c_bit, boundary_bit, rule)
                for x in range(1, w + 1):
                    expect = grid[t + 1].get(x, 0)
                    got = bit(v, x - 1)
                    assert got == expect, (rule, w, bits, t, x, got, expect)

    # 3. Rule 90 additivity sanity check on the driven stepper: XOR of two runs
    #    equals the run started from the XOR'd initial state and XOR'd drives
    #    (linearity), which rule 30 must NOT satisfy (OR is nonlinear).
    for _ in range(40):
        w = rng.randint(2, 10)
        v1 = rng.randint(0, (1 << w) - 1)
        v2 = rng.randint(0, (1 << w) - 1)
        c1, c2 = rng.randint(0, 1), rng.randint(0, 1)
        b1, b2 = rng.randint(0, 1), rng.randint(0, 1)
        n1 = step_driven(v1, w, c1, b1, 90)
        n2 = step_driven(v2, w, c2, b2, 90)
        nx = step_driven(v1 ^ v2, w, c1 ^ c2, b1 ^ b2, 90)
        assert (n1 ^ n2) == nx, "rule 90 driven stepper is not linear -- bug"
        n1_30 = step_driven(v1, w, c1, b1, 30)
        n2_30 = step_driven(v2, w, c2, b2, 30)
        nx_30 = step_driven(v1 ^ v2, w, c1 ^ c2, b1 ^ b2, 30)
        if (n1_30 ^ n2_30) == nx_30 and (v1, c1, b1) != (v2, c2, b2):
            # not a bug by itself (can coincide by chance); just don't assert
            # linearity for rule 30, it is expected to fail generically.
            pass

    print("substrate selftest OK: ground truth match, driven-stepper == true diagram on a strip, "
          "rule 90 driven-stepper linear, rule 30 driven-stepper (checked elsewhere) not.")


if __name__ == "__main__":
    selftest()
    sys.exit(0)

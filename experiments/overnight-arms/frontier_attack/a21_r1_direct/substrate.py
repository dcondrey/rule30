"""Shared substrate for arm a21 (R1 direct attack).  Stdlib only.

Conventions match `experiments/overnight-arms/common/rule30.py`:

    rule 30:  s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1))
    rule 90:  s(t+1,x) = s(t,x-1) XOR s(t,x+1)

Frame trick, generalised to an arbitrary initial row.  Fix an offset K and put

    b_t(i) = s(t, i - t - K)

so that the light cone never runs off the bottom of the word.  Then

    rule 30:  b_{t+1} = (b_t << 2) XOR ((b_t << 1) OR b_t)
    rule 90:  b_{t+1} = (b_t << 2) XOR b_t

and  s(t,x) = bit (x + t + K) of b_t.

Everything here is cross-validated against the repo substrate before use.
"""

from __future__ import annotations

import importlib.util
import sys

_COMMON = "/Volumes/A/researchpapers/13-rule30/experiments/overnight-arms/common/rule30.py"


def _load_common():
    spec = importlib.util.spec_from_file_location("a21_common_rule30", _COMMON)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


COMMON = _load_common()


def step(row: int, rule: int) -> int:
    if rule == 30:
        return (row << 2) ^ ((row << 1) | row)
    if rule == 90:
        return (row << 2) ^ row
    raise ValueError(f"unsupported rule {rule}")


def cell(row: int, t: int, x: int, K: int) -> int:
    i = x + t + K
    return (row >> i) & 1 if i >= 0 else 0


def left_supported_row(bits: list[int], K: int) -> int:
    """Initial row with s(0,-j) = bits[j] for j = 0..len(bits)-1, 0 elsewhere.

    Requires K >= len(bits) - 1 so every set cell lands at a nonnegative index.
    """
    assert K >= len(bits) - 1
    r = 0
    for j, b in enumerate(bits):
        if b:
            r |= 1 << (K - j)
    return r


def diagram(row0: int, K: int, T: int, rule: int) -> list[int]:
    """Rows b_0..b_T in the shifted frame."""
    out = [row0]
    r = row0
    for _ in range(T):
        r = step(r, rule)
        out.append(r)
    return out


def selftest() -> None:
    # 1. lone seed centre column vs the repo ground truth (through common).
    n = 2048
    K = 4
    row0 = left_supported_row([1], K)
    rows = diagram(row0, K, n, 30)
    mine = [cell(rows[t], t, 0, K) for t in range(n)]
    assert mine == COMMON.center_column_bits(n), "centre column mismatch vs common"

    # 2. arbitrary finite seeds vs the naive dict simulator in common, both rules.
    import random

    rng = random.Random(20260830)
    for _ in range(200):
        w = rng.randint(1, 12)
        bits = [rng.randint(0, 1) for _ in range(w)]
        if not any(bits):
            bits[0] = 1
        K = w + 2
        row0 = left_supported_row(bits, K)
        T = 40
        rows = diagram(row0, K, T, 30)
        seed = {-j: b for j, b in enumerate(bits) if b}
        grid = COMMON.simulate_seed(seed, T + 1)
        for t in range(T + 1):
            for x in range(-w - t - 2, t + 3):
                assert cell(rows[t], t, x, K) == grid[t].get(x, 0), (bits, t, x)

    # 3. rule 90 against an independent naive simulator written here.
    for _ in range(100):
        w = rng.randint(1, 12)
        bits = [rng.randint(0, 1) for _ in range(w)]
        if not any(bits):
            bits[0] = 1
        K = w + 2
        row0 = left_supported_row(bits, K)
        T = 40
        rows = diagram(row0, K, T, 90)
        cur = {-j: b for j, b in enumerate(bits) if b}
        for t in range(T + 1):
            for x in range(-w - t - 2, t + 3):
                assert cell(rows[t], t, x, K) == cur.get(x, 0), (bits, t, x, "r90")
            lo, hi = (min(cur) - 1, max(cur) + 1) if cur else (0, 0)
            cur = {
                x: v
                for x in range(lo, hi + 1)
                if (v := cur.get(x - 1, 0) ^ cur.get(x + 1, 0))
            }

    print("substrate selftest OK: centre column, rule 30 grid, rule 90 grid")


if __name__ == "__main__":
    selftest()
    sys.exit(0)

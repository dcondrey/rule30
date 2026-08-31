"""Shared Rule 30 substrate for the overnight arms. Stdlib only.

Convention (matches the repo pin in experiments/rule30/center_column.py):
position increases rightward; s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1)).

Internal frame: b_t(i) = s(t, i - t), stored as a Python int with cell at bit i,
so rows stay nonnegative as the light cone grows left. Update in that frame:
b_{t+1} = (b_t << 2) XOR ((b_t << 1) OR b_t). Center cell s(t,0) = bit t of b_t.

Validation is EXACT COMPUTATION against the repo ground-truth generator
(read-only import) and an independent naive grid simulator. Run:
    uv run python experiments/overnight-arms/common/rule30.py
"""

from __future__ import annotations


def step_frame(row: int) -> int:
    """One Rule 30 step in the shifted frame b_t(i) = s(t, i - t)."""
    return (row << 2) ^ ((row << 1) | row)


def center_column_bits(n: int) -> list[int]:
    """First n bits of the one-seed center column, s(0,0)..s(n-1,0)."""
    row = 1  # b_0: single 1 at bit 0
    out = []
    for t in range(n):
        out.append((row >> t) & 1)
        row = step_frame(row)
    return out


def rows_frame(n: int) -> list[int]:
    """b_0..b_{n-1} in the shifted frame (cell x of row t is bit x + t)."""
    row = 1
    out = []
    for _ in range(n):
        out.append(row)
        row = step_frame(row)
    return out


def cell(row_frame: int, t: int, x: int) -> int:
    """s(t, x) from the shifted-frame row b_t."""
    i = x + t
    return (row_frame >> i) & 1 if i >= 0 else 0


def simulate_seed(seed: dict[int, int], n: int) -> list[dict[int, int]]:
    """Naive simulator for an arbitrary finite seed {x: bit}. Independent of the
    frame trick on purpose: used as the cross-check implementation."""
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
            v = l ^ (c | r)
            if v:
                nxt[x] = 1
        grid.append(nxt)
        cur = nxt
    return grid


def _selftest() -> None:
    import importlib.util
    import sys

    n = 4096
    mine = center_column_bits(n)

    # Cross-check 1: independent naive simulator, first 512 steps.
    grid = simulate_seed({0: 1}, 512)
    naive = [grid[t].get(0, 0) for t in range(512)]
    assert mine[:512] == naive, "frame-trick generator disagrees with naive simulator"

    # Cross-check 2: repo ground truth (READ-ONLY import), full n.
    spec = importlib.util.spec_from_file_location(
        "repo_center_column",
        "/Volumes/A/researchpapers/13-rule30/experiments/rule30/center_column.py",
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    truth = list(mod.center_column(n))
    assert mine == truth[:n], "disagrees with repo ground truth A051023 generator"

    import logging

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logging.info(
        "OK: %d center bits match repo ground truth; 512 match naive simulator", n
    )
    logging.info("prefix: %s", "".join(map(str, mine[:32])))
    sys.exit(0)


if __name__ == "__main__":
    _selftest()

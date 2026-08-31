"""Bit-list Rule 30 / Rule 90 stepping, validated against the shared substrate.

The search needs configurations as padded bit LISTS (to slide windows over),
not as the packed ints of `common/rule30.py`.  This module provides that and
proves the two agree.

Convention pinned by `common/rule30.py`:  s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1)).
Rule 90:                                  s(t+1,x) = s(t,x-1) XOR s(t,x+1).
"""

from __future__ import annotations

import importlib.util
import random
import sys

REPO = "/Volumes/A/researchpapers/13-rule30"
COMMON = f"{REPO}/experiments/overnight-arms/common/rule30.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def eca_table(rule):
    """Wolfram numbering: bit (4l + 2m + r) of `rule` gives the new cell."""
    assert 0 <= rule < 256 and (rule & 1) == 0, "rule must fix the 0 background"
    return [(rule >> k) & 1 for k in range(8)]


def step(bits, rule=30):
    """One step with a growing quiescent background: two extra cells per side."""
    tab = eca_table(rule)
    b = [0, 0] + list(bits) + [0, 0]
    out = [0] * len(b)
    for x in range(1, len(b) - 1):
        out[x] = tab[(b[x - 1] << 2) | (b[x] << 1) | b[x + 1]]
    return out


def lone_seed_rows(n, rule=30):
    """Rows 0..n-1 from a single 1, each a bit list; centre index is tracked."""
    bits = [1]
    centre = 0
    rows = [(list(bits), centre)]
    for _ in range(n - 1):
        bits = step(bits, rule)
        centre += 2
        rows.append((list(bits), centre))
    return rows


def random_finite_config(rng, width):
    """A random finite-support configuration, guaranteed non-empty."""
    b = [rng.randint(0, 1) for _ in range(width)]
    if not any(b):
        b[rng.randrange(width)] = 1
    return b


def _selftest():
    import logging

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    common = _load(COMMON, "a15_common_rule30")

    n = 600
    rows = lone_seed_rows(n, 30)
    mine = [rows[t][0][rows[t][1]] for t in range(n)]
    truth = common.center_column_bits(n)
    assert mine == truth, "bit-list stepper disagrees with common/rule30.py"

    # arbitrary finite seeds, against common.simulate_seed
    rng = random.Random(20260830)
    for _ in range(20):
        w = rng.randint(1, 12)
        seed = random_finite_config(rng, w)
        gridsz = 40
        g = common.simulate_seed({i: v for i, v in enumerate(seed)}, gridsz)
        bits, off = list(seed), 0
        for t in range(gridsz):
            got = {i - off for i, v in enumerate(bits) if v}
            want = {x for x, v in g[t].items() if v}
            assert got == want, (t, seed, sorted(got), sorted(want))
            bits = step(bits, 30)
            off += 2

    # Rule 90 lone-seed centre column is 0 for all t >= 1 (the section-0 filter)
    r90 = lone_seed_rows(200, 90)
    assert all(r90[t][0][r90[t][1]] == 0 for t in range(1, 200))

    # generic-table stepper agrees with the two hand-written rules it replaced
    for _ in range(50):
        s = random_finite_config(rng, rng.randint(1, 14))
        b = [0, 0] + s + [0, 0]
        for rule, fn in ((30, lambda l, m, r: l ^ (m | r)),
                         (90, lambda l, m, r: l ^ r)):
            want = [0] * len(b)
            for x in range(1, len(b) - 1):
                want[x] = fn(b[x - 1], b[x], b[x + 1])
            assert step(s, rule) == want, rule
    # control rules used by the search harness
    assert step([1, 0, 1], 204) == [0, 0, 1, 0, 1, 0, 0], "204 must be identity"
    assert step([1, 0, 0], 170) == [0, 1, 0, 0, 0, 0, 0], "170 must shift left"
    for _ in range(50):  # 184 is number-conserving
        s = random_finite_config(rng, rng.randint(1, 14))
        assert sum(step(s, 184)) == sum(s), "184 must conserve particle number"

    logging.info("OK: %d centre bits match common/rule30.py; 20 random seeds match "
                 "simulate_seed for 40 steps; Rule 90 centre column is 0 after t=0", n)
    sys.exit(0)


if __name__ == "__main__":
    _selftest()

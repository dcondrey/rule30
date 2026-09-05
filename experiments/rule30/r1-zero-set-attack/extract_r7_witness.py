"""Extract an explicit R7 mode-(ii) witness at p=2 (read-only use of the
existing ladder code) and dump its (l, c, r) bit sequences plus a direct
check of whether column 2 is UNIQUELY forced at every step (the property the
p1-period2-invariant census's `literal_extension` guarantees by construction:
`assert len(candidates) == 1`) or only PARTIALLY forced, with genuine
freedom left over (what obstruction F / "the free boundary" predicts).

Imports experiments/rule30/ladder/{ladder,rung1}.py READ-ONLY via
importlib (no sys.path mutation of the real modules, no edits).  This
mirrors how a21/a7's own arms cross-imported experiments/overnight-arms/common.
"""

from __future__ import annotations

import importlib.util
import json
import sys

_LADDER_DIR = "/Volumes/A/researchpapers/13-rule30/experiments/rule30/ladder"


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # rung1.py does `from ladder import ...`
    spec.loader.exec_module(mod)
    return mod


ladder = _load("ladder", f"{_LADDER_DIR}/ladder.py")
rung1 = _load("rung1", f"{_LADDER_DIR}/rung1.py")


def extract(R: int, k: int, word: tuple[int, ...], q: int, pin: bool, reps: int = 6):
    P = ladder.Params(rule=30, right_depth=R, left_depth=k, period_word=word, diff_q=q)
    res = rung1.decide_pin(P, pin)
    assert res["verdict"] == "NONEMPTY", res
    wit = res["witness"]
    okv, note = ladder.verify_witness(wit["prefix"], wit["cycle"], P)
    assert okv, note

    letters = list(wit["prefix"]) + list(wit["cycle"]) * reps
    T = len(letters)
    cols = {R: [ab & 1 for ab in letters], R - 1: [ab >> 1 for ab in letters]}
    inv = ladder.INV[30]
    x = R - 2
    while x >= P.x_min:
        up = cols[x + 1]
        upr = cols[x + 2]
        cols[x] = [inv(up[i + 1], up[i], upr[i]) for i in range(len(up) - 1)]
        x -= 1
    return P, res, wit, note, cols, letters


def report(R: int, k: int, word: tuple[int, ...], q: int, pin: bool):
    P, res, wit, note, cols, letters = extract(R, k, word, q, pin)
    print(f"\n=== R={R} k={k} w={''.join(map(str,word))} q={q} pin={pin} ===")
    print(f"states={res['states']} witness_verified_note={note}")
    print(f"prefix={wit['prefix']}")
    print(f"cycle={wit['cycle']} (len {len(wit['cycle'])})")

    c = cols[0]
    r = cols.get(1)
    l = cols[-1]
    n_show = min(len(c), len(wit["prefix"]) + 3 * len(wit["cycle"]))
    print(f"c (col 0) [{n_show}]: {''.join(map(str, c[:n_show]))}")
    if r is not None:
        print(f"r (col 1) [{n_show}]: {''.join(map(str, r[:n_show]))}")
    print(f"l (col -1)[{n_show}]: {''.join(map(str, l[:n_show]))}")

    if r is not None:
        # column 2 forcing analysis: at r_t=0, s(t,2) = r_{t+1} XOR c_t is FORCED.
        # at r_t=1, s(t,2) is UNCONSTRAINED by the one-step forward rule at x=1.
        forced = []
        free_count = 0
        forced_count = 0
        tail_start = len(wit["prefix"])  # only look at the recurring part
        for t in range(tail_start, len(r) - 1):
            if r[t] == 0:
                forced.append(r[t + 1] ^ c[t])
                forced_count += 1
            else:
                forced.append(None)
                free_count += 1
        print(f"column-2 forcing over the cyclic tail: "
              f"{forced_count} forced cells, {free_count} FREE cells "
              f"(r_t=1) out of {forced_count+free_count}")
        # Now check: does the pin's OWN extendability condition on column 2
        # (s(t,2)=1 => r_t = NOT s(t+1,2)) have a UNIQUE consistent completion
        # of the free cells, or does real freedom survive?  Try both values at
        # every free cell and see how many full assignments over one cycle are
        # internally pin-consistent.
        free_positions = [i for i, v in enumerate(forced) if v is None]
        print(f"free positions in one look at the tail: {len(free_positions)} "
              f"(first few: {free_positions[:10]})")
    return P, res, wit, cols


if __name__ == "__main__":
    # Rung 1's own smallest documented pin-NONEMPTY case, table row R=1.
    report(R=1, k=2, word=(0, 1), q=1, pin=True)
    # And R=2 for comparison (letters are (col_1, col_2) directly).
    report(R=2, k=2, word=(0, 1), q=1, pin=True)

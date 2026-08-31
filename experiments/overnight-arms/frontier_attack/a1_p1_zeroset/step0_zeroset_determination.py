"""STEP 0 for route R1 (PATH.md section 4): is the zero-set obligation decidable
from the centre column alone?

R1 asks: does `c` eventually periodic force `r` eventually periodic on
`Z = {t : c_t = 0}`?  Its stated kill condition is "if the zero-set obligation is
not decidable from `c` alone, R1 dies".

Register row 38 records that the finite rows `{0}` and `{0,1}` have the SAME centre
trace at every checked step.  This script asks the question row 38 did not: on the
zero-set of that shared trace, do the two diagrams have the SAME right column?

It also sweeps every finite seed inside a window, groups seeds by centre trace,
and measures, for every colliding pair, whether the right columns differ on the
zero set and whether the difference is finite (a transient) or persists.

Rule 90 control included (section 0 filter).

Simulation is cross-validated against experiments/overnight-arms/common/rule30.py
(`simulate_seed`, an independent naive dict simulator) at every run.

Run: uv run python step0_zeroset_determination.py
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import logging
import pathlib
import sys

log = logging.getLogger("step0")

REPO = pathlib.Path("/Volumes/A/researchpapers/13-rule30")
HERE = pathlib.Path(__file__).resolve().parent


def _load_common():
    spec = importlib.util.spec_from_file_location(
        "oa_rule30", REPO / "experiments/overnight-arms/common/rule30.py"
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


COMMON = _load_common()


# ---------------------------------------------------------------- simulation
def step30(row: int) -> int:
    """b_{t+1} = (b<<2) ^ ((b<<1) | b) in the frame b_t(i) = s(t, i-t)."""
    return (row << 2) ^ ((row << 1) | row)


def step90(row: int) -> int:
    return (row << 2) ^ row


STEP = {"30": step30, "90": step90}


def columns(seed_bits: int, n: int, rule: str = "30", xs: tuple[int, ...] = (0, 1)):
    """Return {x: [s(t,x) for t < n]} for a seed supported in x >= 0.

    seed_bits has bit x set iff s(0,x) = 1.
    """
    step = STEP[rule]
    row = seed_bits
    out = {x: [] for x in xs}
    for t in range(n):
        for x in xs:
            i = x + t
            out[x].append((row >> i) & 1 if i >= 0 else 0)
        row = step(row)
    return out


def _crosscheck() -> None:
    """Validate `columns` against the shared naive dict simulator."""
    n = 200
    for bits in (0b1, 0b11, 0b101, 0b1011):
        seed = {x: 1 for x in range(bits.bit_length()) if (bits >> x) & 1}
        grid = COMMON.simulate_seed(seed, n)
        mine = columns(bits, n, "30", xs=(-1, 0, 1, 2))
        for x in (-1, 0, 1, 2):
            ref = [grid[t].get(x, 0) for t in range(n)]
            assert mine[x] == ref, f"mismatch seed={bin(bits)} x={x}"
    log.info("cross-check OK: `columns` matches common/rule30.simulate_seed "
             "for 4 seeds x 4 columns x 200 steps")


# ------------------------------------------------------------------- step 0a
def compare_pair(a: int, b: int, n: int, rule: str = "30") -> dict:
    ca = columns(a, n, rule)
    cb = columns(b, n, rule)
    c_a, r_a = ca[0], ca[1]
    c_b, r_b = cb[0], cb[1]
    trace_eq_upto = n
    for t in range(n):
        if c_a[t] != c_b[t]:
            trace_eq_upto = t
            break
    horizon = trace_eq_upto  # only compare where the traces agree
    zero_set = [t for t in range(horizon) if c_a[t] == 0]
    diffs = [t for t in zero_set if r_a[t] != r_b[t]]
    # where do the two diagrams differ at all, and how far right?
    return {
        "rule": rule,
        "seed_a": bin(a),
        "seed_b": bin(b),
        "n": n,
        "centre_traces_agree_up_to": horizon,
        "zero_set_size": len(zero_set),
        "r_differences_on_zero_set": len(diffs),
        "first_r_difference": diffs[0] if diffs else None,
        "last_r_difference": diffs[-1] if diffs else None,
        "r_differs_anywhere": sum(1 for t in range(horizon) if r_a[t] != r_b[t]),
    }


def defect_front(a: int, b: int, n: int, rule: str = "30") -> list[int | None]:
    """Leftmost column where the two diagrams differ, per time step (None = equal)."""
    step = STEP[rule]
    ra, rb = a, b
    front = []
    for t in range(n):
        d = ra ^ rb
        if d == 0:
            front.append(None)
        else:
            lsb = (d & -d).bit_length() - 1  # smallest differing bit index i = x + t
            front.append(lsb - t)
        ra, rb = step(ra), step(rb)
    return front


# ------------------------------------------------------------------- step 0b
def sweep(w: int, n: int, rule: str = "30") -> dict:
    """All seeds supported in [0,w) with bit 0 set (translation-normalised at the
    centre column), grouped by centre trace over n steps."""
    groups: dict[tuple[int, ...], list[int]] = {}
    rcol: dict[int, tuple[int, ...]] = {}
    for rest in itertools.product((0, 1), repeat=w - 1):
        bits = 1 | sum(v << (i + 1) for i, v in enumerate(rest))
        col = columns(bits, n, rule)
        groups.setdefault(tuple(col[0]), []).append(bits)
        rcol[bits] = tuple(col[1])
    collisions = {k: v for k, v in groups.items() if len(v) > 1}
    reports = []
    n_pairs_r_differs_on_Z = 0
    n_pairs_r_differs_on_Z_after_t2 = 0
    for trace, seeds in collisions.items():
        zero_set = [t for t in range(n) if trace[t] == 0]
        rs: dict[tuple[int, ...], list[int]] = {}
        for s in seeds:
            rs.setdefault(tuple(rcol[s][t] for t in zero_set), []).append(s)
        dis = [t for t in zero_set if len({rcol[s][t] for s in seeds}) > 1]
        # pairwise accounting (the quantity the deliverable reports)
        for i in range(len(seeds)):
            for j in range(i + 1, len(seeds)):
                a, b = seeds[i], seeds[j]
                d = [t for t in zero_set if rcol[a][t] != rcol[b][t]]
                if d:
                    n_pairs_r_differs_on_Z += 1
                    if any(t >= 2 for t in d):
                        n_pairs_r_differs_on_Z_after_t2 += 1
        reports.append(
            {
                "seeds": [bin(s) for s in seeds],
                "n_seeds": len(seeds),
                "distinct_r_on_zero_set": len(rs),
                "zero_set_size": len(zero_set),
                "last_r_disagreement": max(dis) if dis else None,
            }
        )
    n_colliding_pairs = sum(
        len(v) * (len(v) - 1) // 2 for v in collisions.values()
    )
    return {
        "rule": rule,
        "window": w,
        "n": n,
        "n_seeds": 2 ** (w - 1),
        "n_trace_classes": len(groups),
        "n_collision_classes": len(collisions),
        "n_colliding_pairs": n_colliding_pairs,
        "n_pairs_r_differs_on_zero_set": n_pairs_r_differs_on_Z,
        "n_pairs_r_differs_on_zero_set_at_some_t_ge_2": n_pairs_r_differs_on_Z_after_t2,
        "classes": reports if w <= 8 else "omitted (large)",
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
    _crosscheck()
    out: dict = {}

    N = 4000
    log.info("")
    log.info("=== 0a. register row 38's pair: {0} vs {0,1}, rule 30 ===")
    pair = compare_pair(0b1, 0b11, N, "30")
    log.info(json.dumps(pair, indent=2))
    out["row38_pair_rule30"] = pair

    fr = defect_front(0b1, 0b11, 60, "30")
    log.info("defect front (leftmost differing column) t=0..59: %s", fr)
    out["row38_defect_front_60"] = fr
    fr_long = defect_front(0b1, 0b11, N, "30")
    reached_le1 = [t for t, x in enumerate(fr_long) if x is not None and x <= 1]
    out["times_defect_front_reaches_column_le_1"] = {
        "count": len(reached_le1),
        "max_t": max(reached_le1) if reached_le1 else None,
    }
    log.info(
        "front at column <= 1 at %d of %d times, last t = %s",
        len(reached_le1), N, max(reached_le1) if reached_le1 else None,
    )

    log.info("")
    log.info("=== 0a'. rule 90 on the same pair: VACUOUS, not a control ===")
    log.info("(rule 90's two seeds' centre traces diverge at t=1, so the zero set")
    log.info(" of the shared trace is empty and nothing is tested.  The real rule 90")
    log.info(" control is the rule-90 branch of the sweep in 0b.)")
    pair90 = compare_pair(0b1, 0b11, N, "90")
    log.info(json.dumps(pair90, indent=2))
    out["row38_pair_rule90"] = pair90

    log.info("")
    log.info("=== 0b. exhaustive seed sweep, centre-trace collision classes ===")
    for rule in ("30", "90"):
        for w in (8, 12, 16, 20):
            s = sweep(w, 400, rule)
            log.info(
                "rule %s w=%2d: %6d seeds -> %6d trace classes, %5d collision classes, "
                "%6d colliding pairs; pairs with r differing on Z: %d "
                "(at some t>=2: %d)",
                rule, w, s["n_seeds"], s["n_trace_classes"],
                s["n_collision_classes"], s["n_colliding_pairs"],
                s["n_pairs_r_differs_on_zero_set"],
                s["n_pairs_r_differs_on_zero_set_at_some_t_ge_2"],
            )
            if isinstance(s["classes"], list):
                for c in s["classes"]:
                    log.info(
                        "    class %s: %d distinct r|Z (|Z|=%d), last disagreement t=%s",
                        c["seeds"], c["distinct_r_on_zero_set"], c["zero_set_size"],
                        c["last_r_disagreement"],
                    )
            out[f"sweep_rule{rule}_w{w}"] = s

    (HERE / "step0_output.json").write_text(json.dumps(out, indent=2))
    log.info("")
    log.info("wrote step0_output.json")


if __name__ == "__main__":
    main()

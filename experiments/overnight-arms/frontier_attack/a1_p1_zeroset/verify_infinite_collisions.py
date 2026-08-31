"""Verify step 0's verdict directly: among finite-seed pairs whose centre traces
NEVER separate within the horizon, does `r` ever differ on the zero set?

step0c's histogram lumped "no zero-set defect" together for pairs that reach the
cap and pairs that break early.  This script separates them, which is the claim
step 0's verdict rests on:

    A(a,b) = first t with c_t(a) != c_t(b), capped at CAP.
    "surviving pair"  <=>  A = CAP.
    Question: does any surviving pair have r_t(a) != r_t(b) for some t < CAP with
    c_t = 0?

Run: uv run python verify_infinite_collisions.py
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import logging
import pathlib
import sys

log = logging.getLogger("verify")
REPO = pathlib.Path("/Volumes/A/researchpapers/13-rule30")
HERE = pathlib.Path(__file__).resolve().parent


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, REPO / rel)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


COMMON = _load("oa_rule30", "experiments/overnight-arms/common/rule30.py")


def stepper(rule: str):
    if rule == "30":
        return lambda row: (row << 2) ^ ((row << 1) | row)
    return lambda row: (row << 2) ^ row


def scan(a: int, b: int, rule: str, cap: int) -> dict:
    step = stepper(rule)
    ra, rb = a, b
    zdef, odef, far = [], [], []
    for t in range(cap):
        ca, cb = (ra >> t) & 1, (rb >> t) & 1
        if ca != cb:
            return {"A": t, "reached_cap": False,
                    "zero_set_r_defects": zdef, "one_phase_r_defects": len(odef)}
        rda = (ra >> (t + 1)) & 1
        rdb = (rb >> (t + 1)) & 1
        if rda != rdb:
            (zdef if ca == 0 else odef).append(t)
        # rightmost extent of the whole-configuration difference, for context
        d = ra ^ rb
        if d:
            far.append(d.bit_length() - 1 - t)
        ra, rb = step(ra), step(rb)
    return {"A": cap, "reached_cap": True, "zero_set_r_defects": zdef,
            "one_phase_r_defects": len(odef),
            "rightmost_diff_column_last": far[-1] if far else None,
            "leftmost_of_rightmost": min(far) if far else None}


def run(w: int, rule: str, cap: int) -> dict:
    step = stepper(rule)
    groups: dict[tuple, list[int]] = {}
    P = 24
    for rest in itertools.product((0, 1), repeat=w - 1):
        bits = 1 | sum(v << (i + 1) for i, v in enumerate(rest))
        row, pref = bits, []
        for t in range(P):
            pref.append((row >> t) & 1)
            row = step(row)
        groups.setdefault(tuple(pref), []).append(bits)

    surviving = 0
    surviving_with_zero_defect = 0
    surviving_with_one_phase_defect = 0
    broke = 0
    examples = []
    for seeds in groups.values():
        if len(seeds) < 2:
            continue
        for a, b in itertools.combinations(seeds, 2):
            res = scan(a, b, rule, cap)
            if not res["reached_cap"]:
                broke += 1
                continue
            surviving += 1
            if res["zero_set_r_defects"]:
                surviving_with_zero_defect += 1
                if len(examples) < 10:
                    examples.append({"a": bin(a), "b": bin(b),
                                     "first_zero_defect":
                                         res["zero_set_r_defects"][0]})
            if res["one_phase_r_defects"]:
                surviving_with_one_phase_defect += 1
    return {
        "rule": rule,
        "window": w,
        "cap": cap,
        "pairs_broken_before_cap": broke,
        "surviving_pairs": surviving,
        "surviving_pairs_with_a_ZERO_SET_r_defect": surviving_with_zero_defect,
        "surviving_pairs_with_a_one_phase_r_defect":
            surviving_with_one_phase_defect,
        "examples": examples,
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
    grid = COMMON.simulate_seed({0: 1}, 100)
    assert grid[1] == {-1: 1, 0: 1, 1: 1}
    log.info("cross-check OK against common/rule30.simulate_seed")
    out = {}
    for rule in ("30", "90"):
        for w in (10, 12, 14):
            res = run(w, rule, 4000)
            log.info(
                "rule %s w=%2d cap=4000: %d surviving pairs (centre traces never "
                "separate), of which %d have a zero-set r defect and %d have a "
                "one-phase r defect; %d pairs broke before the cap",
                rule, w, res["surviving_pairs"],
                res["surviving_pairs_with_a_ZERO_SET_r_defect"],
                res["surviving_pairs_with_a_one_phase_r_defect"],
                res["pairs_broken_before_cap"],
            )
            out[f"rule{rule}_w{w}"] = res
    (HERE / "verify_infinite_collisions_output.json").write_text(
        json.dumps(out, indent=2))
    log.info("wrote verify_infinite_collisions_output.json")


if __name__ == "__main__":
    main()

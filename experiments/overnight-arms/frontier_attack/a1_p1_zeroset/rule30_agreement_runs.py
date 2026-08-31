"""Does centre-column agreement ever coexist with right-column disagreement ON
THE ZERO SET?  (The only place R1's kill condition could fire from data in this
tree.)

Register row 37 (`RESULTS-periodicity-bridge.md` section 2) records finite runs
where the lone-seed centre column agrees with its own time shift while both
adjacent columns carry a defect: an 18-step run at `p=148, t=1855` and a 24-step
run at `p=110, t=13219`.  Row 37 did not record the PHASE of those adjacent
defects.  That phase is exactly what R1 turns on:

  * a column-1 defect at a time with `c_t = 1` is absorbed by the OR-latch pin
    (`d_t(-1) = (1 XOR c_t) AND d_t(1)`, so it never reaches column -1);
  * a column-1 defect at a time with `c_t = 0` is a finite instance of
    "same centre trace, different `r` on the zero set" -- the shape of R1's
    stated kill.

This script:
  1. reproduces row 37's runs (stroboscopic pairing `t <-> t+p` on the lone-seed
     orbit, i.e. row 31's pairing `y` vs `F^p(y)`);
  2. classifies every column-1 defect inside every long agreement run by centre
     phase;
  3. re-verifies the defect identity `D(t,-1) = (1 XOR c_t) AND D(t,1)` at every
     eligible time, as a regression against the repo statement;
  4. runs the Rule 90 control, where the agreement run is INFINITE.

Run: uv run python rule30_agreement_runs.py
"""

from __future__ import annotations

import importlib.util
import json
import logging
import pathlib
import re
import sys

log = logging.getLogger("runs")
REPO = pathlib.Path("/Volumes/A/researchpapers/13-rule30")
HERE = pathlib.Path(__file__).resolve().parent


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, REPO / rel)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


COMMON = _load("oa_rule30", "experiments/overnight-arms/common/rule30.py")


def columns(n: int, rule: str = "30") -> dict[int, list[int]]:
    row = 1
    out: dict[int, list[int]] = {-1: [], 0: [], 1: []}
    for t in range(n):
        for x in (-1, 0, 1):
            i = x + t
            out[x].append((row >> i) & 1 if i >= 0 else 0)
        row = (row << 2) ^ ((row << 1) | row) if rule == "30" else (row << 2) ^ row
    return out


def _bits(word: list[int]) -> str:
    return "".join(map(str, word))


def analyse(rule: str, T: int, max_p: int, min_run: int) -> dict:
    cols = columns(T, rule)
    c, r, l = cols[0], cols[1], cols[-1]
    cs, rs, ls = _bits(c), _bits(r), _bits(l)

    best = {"len": 0}
    long_runs = []
    identity_violations = 0
    identity_checks = 0
    runs_with_zero_phase_defect = 0
    runs_without_zero_phase_defect = 0

    for p in range(1, max_p + 1):
        n = T - p
        agree = "".join("1" if cs[t] == cs[t + p] else "0" for t in range(n))
        for m in re.finditer(r"1+", agree):
            a, b = m.start(), m.end()  # centre agrees for t in [a, b)
            L = b - a
            if L > best["len"]:
                best = {"len": L, "p": p, "t0": a}
            # defect identity holds at t with D(t,0)=D(t+1,0)=0, i.e. t,t+1 in run
            for t in range(a, b - 1):
                identity_checks += 1
                d_l = int(ls[t] != ls[t + p])
                d_r = int(rs[t] != rs[t + p])
                if d_l != ((1 - int(cs[t])) & d_r):
                    identity_violations += 1
            if L >= min_run:
                zero_phase_def = [
                    t for t in range(a, b) if cs[t] == "0" and rs[t] != rs[t + p]
                ]
                one_phase_def = [
                    t for t in range(a, b) if cs[t] == "1" and rs[t] != rs[t + p]
                ]
                zero_times = sum(1 for t in range(a, b) if cs[t] == "0")
                if zero_phase_def:
                    runs_with_zero_phase_defect += 1
                else:
                    runs_without_zero_phase_defect += 1
                long_runs.append(
                    {
                        "p": p,
                        "t0": a,
                        "len": L,
                        "zero_phase_times": zero_times,
                        "zero_phase_r_defects": len(zero_phase_def),
                        "one_phase_r_defects": len(one_phase_def),
                        "first_zero_phase_defect": (
                            zero_phase_def[0] if zero_phase_def else None
                        ),
                    }
                )
    return {
        "rule": rule,
        "T": T,
        "max_p": max_p,
        "min_run": min_run,
        "longest_agreement_run": best,
        "defect_identity_checks": identity_checks,
        "defect_identity_violations": identity_violations,
        "n_long_runs": len(long_runs),
        "long_runs_with_a_zero_phase_r_defect": runs_with_zero_phase_defect,
        "long_runs_with_NO_zero_phase_r_defect": runs_without_zero_phase_defect,
        "long_runs": long_runs[:40],
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
    out: dict = {}

    # cross-check against the shared naive simulator
    grid = COMMON.simulate_seed({0: 1}, 200)
    mine = columns(200, "30")
    for x in (-1, 0, 1):
        assert mine[x] == [grid[t].get(x, 0) for t in range(200)], f"col {x}"
    log.info("cross-check OK: columns match common/rule30.simulate_seed, 200 steps")

    log.info("")
    log.info("=== rule 30, T=4096, p<=256 (row 37's first regime) ===")
    a = analyse("30", 4096, 256, 12)
    log.info(json.dumps({k: v for k, v in a.items() if k != "long_runs"}, indent=2))
    log.info("longest runs found: %s", json.dumps(
        sorted(a["long_runs"], key=lambda d: -d["len"])[:6]))
    out["rule30_T4096_p256"] = a

    log.info("")
    log.info("=== rule 30, T=16384, p<=512 (row 37's second regime) ===")
    b = analyse("30", 16384, 512, 16)
    log.info(json.dumps({k: v for k, v in b.items() if k != "long_runs"}, indent=2))
    log.info("longest runs found: %s", json.dumps(
        sorted(b["long_runs"], key=lambda d: -d["len"])[:6]))
    out["rule30_T16384_p512"] = b

    log.info("")
    log.info("=== rule 90 control, T=4096, p<=8 ===")
    d = analyse("90", 4096, 8, 12)
    log.info(json.dumps({k: v for k, v in d.items() if k != "long_runs"}, indent=2))
    log.info("first 3 long runs: %s", json.dumps(d["long_runs"][:3], indent=2))
    out["rule90_T4096_p8"] = d

    (HERE / "agreement_runs_output.json").write_text(json.dumps(out, indent=2))
    log.info("")
    log.info("wrote agreement_runs_output.json")


if __name__ == "__main__":
    main()

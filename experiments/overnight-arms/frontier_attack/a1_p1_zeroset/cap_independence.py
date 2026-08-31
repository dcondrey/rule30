"""Is the surviving-pair family of section 1 a horizon artifact?

`verify_infinite_collisions.py` calls a pair "surviving" when its centre traces
do not separate before the cap.  If the count `2^{w-1} - 1` were an artifact of
the cap, it would move when the cap moves.  This script fixes `w = 12` and varies
the cap over 400 / 4,000 / 40,000, staging the deep pass over only the pairs that
already survived the shallow one.

Run: uv run python cap_independence.py
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import logging
import pathlib
import sys

log = logging.getLogger("cap")
HERE = pathlib.Path(__file__).resolve().parent


def _load(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


V = _load("verify", HERE / "verify_infinite_collisions.py")


def step30(row: int) -> int:
    return (row << 2) ^ ((row << 1) | row)


def survivors(w: int, cap: int) -> list[tuple[int, int]]:
    groups: dict[tuple, list[int]] = {}
    for rest in itertools.product((0, 1), repeat=w - 1):
        bits = 1 | sum(v << (i + 1) for i, v in enumerate(rest))
        row, pref = bits, []
        for t in range(24):
            pref.append((row >> t) & 1)
            row = step30(row)
        groups.setdefault(tuple(pref), []).append(bits)
    out = []
    for seeds in groups.values():
        for a, b in itertools.combinations(seeds, 2):
            res = V.scan(a, b, "30", cap)
            if res["reached_cap"]:
                out.append((a, b))
    return out


def deepen(pairs: list[tuple[int, int]], cap: int) -> dict:
    kept, zdef, odef = [], 0, 0
    for a, b in pairs:
        res = V.scan(a, b, "30", cap)
        if res["reached_cap"]:
            kept.append((a, b))
            if res["zero_set_r_defects"]:
                zdef += 1
            if res["one_phase_r_defects"]:
                odef += 1
    return {"cap": cap, "surviving": len(kept),
            "with_zero_set_r_defect": zdef, "with_one_phase_r_defect": odef,
            "pairs": kept}


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
    out = {}
    w = 12
    base = survivors(w, 400)
    log.info("w=%d cap=   400: %d surviving pairs", w, len(base))
    out["400"] = {"cap": 400, "surviving": len(base)}
    prev = base
    for cap in (4000, 40000):
        d = deepen(prev, cap)
        log.info("w=%d cap=%6d: %d surviving pairs, %d with a zero-set r defect, "
                 "%d with a one-phase r defect", w, cap, d["surviving"],
                 d["with_zero_set_r_defect"], d["with_one_phase_r_defect"])
        prev = d["pairs"]
        out[str(cap)] = {k: v for k, v in d.items() if k != "pairs"}
    counts = {out[k]["surviving"] for k in out}
    out["cap_independent"] = len(counts) == 1
    out["count"] = sorted(counts)
    log.info("cap-independent across 400 / 4,000 / 40,000: %s (counts %s; "
             "2^%d - 1 = %d)", out["cap_independent"], sorted(counts), w - 1,
             2 ** (w - 1) - 1)
    (HERE / "cap_independence_output.json").write_text(json.dumps(out, indent=2))
    log.info("wrote cap_independence_output.json")


if __name__ == "__main__":
    main()

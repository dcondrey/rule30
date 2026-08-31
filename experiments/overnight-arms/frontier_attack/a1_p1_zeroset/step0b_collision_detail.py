"""Detail on the step-0 finding: finite seed pairs with the SAME centre trace and
DIFFERENT right column on the zero set.

step0_zeroset_determination.py found, over T = 400 steps:
    rule 30, w=16: 18 such pairs out of 32,842 colliding pairs
    rule 30, w=20: 558 such pairs out of 539,078
    rule 30, w<=12: none
    rule 90, every w: no centre-trace collisions at all

This script extracts those pairs, then asks the question that decides how much
they are worth:

  * do the two centre traces still agree at T = 4,000 and T = 40,000, or was the
    collision an artifact of the 400-step window?
  * how far out do the zero-set disagreements in `r` reach?
  * does the column -1 defect identity `D(t,-1) = (1 XOR c_t) AND D(t,1)` hold
    (it must; this is a regression check on the pairing);
  * is the resulting column -1 disagreement also on the zero set?

Run: uv run python step0b_collision_detail.py
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import logging
import pathlib
import sys

log = logging.getLogger("detail")
REPO = pathlib.Path("/Volumes/A/researchpapers/13-rule30")
HERE = pathlib.Path(__file__).resolve().parent


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, REPO / rel)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


COMMON = _load("oa_rule30", "experiments/overnight-arms/common/rule30.py")


def step30(row: int) -> int:
    return (row << 2) ^ ((row << 1) | row)


def agree_upto(a: int, b: int, n: int) -> int:
    """First t < n with c_t differing, else n.  Early-exit, cheap."""
    ra, rb = a, b
    for t in range(n):
        if ((ra >> t) & 1) != ((rb >> t) & 1):
            return t
        ra, rb = step30(ra), step30(rb)
    return n


def cols_fast(bits: int, n: int, xs=(-1, 0, 1)) -> dict[int, list[int]]:
    row = bits
    out = {x: [] for x in xs}
    for t in range(n):
        for x in xs:
            i = x + t
            out[x].append((row >> i) & 1 if i >= 0 else 0)
        row = step30(row)
    return out


def find_pairs(w: int, n: int) -> list[tuple[int, int]]:
    groups: dict[tuple[int, ...], list[int]] = {}
    rcol: dict[int, tuple[int, ...]] = {}
    ccol: dict[int, tuple[int, ...]] = {}
    for rest in itertools.product((0, 1), repeat=w - 1):
        b = 1 | sum(v << (i + 1) for i, v in enumerate(rest))
        c = cols_fast(b, n, (0, 1))
        groups.setdefault(tuple(c[0]), []).append(b)
        rcol[b] = tuple(c[1])
        ccol[b] = tuple(c[0])
    hits = []
    for trace, seeds in groups.items():
        if len(seeds) < 2:
            continue
        Z = [t for t in range(n) if trace[t] == 0]
        for a, b in itertools.combinations(seeds, 2):
            if any(rcol[a][t] != rcol[b][t] for t in Z):
                hits.append((a, b))
    return hits


def examine(a: int, b: int, n: int) -> dict:
    ca, cb = cols_fast(a, n), cols_fast(b, n)
    agree_upto = n
    for t in range(n):
        if ca[0][t] != cb[0][t]:
            agree_upto = t
            break
    H = agree_upto
    Z = [t for t in range(H) if ca[0][t] == 0]
    dr = [t for t in Z if ca[1][t] != cb[1][t]]
    dl = [t for t in Z if ca[-1][t] != cb[-1][t]]
    # identity regression: at every t < H-1 (so D(t,0)=D(t+1,0)=0)
    viol = 0
    for t in range(H - 1):
        d_l = int(ca[-1][t] != cb[-1][t])
        d_r = int(ca[1][t] != cb[1][t])
        if d_l != ((1 - ca[0][t]) & d_r):
            viol += 1
    return {
        "seed_a": bin(a),
        "seed_b": bin(b),
        "n_checked": n,
        "centre_traces_agree_up_to": H,
        "centre_agreement_is_full_window": H == n,
        "zero_set_size": len(Z),
        "r_zero_set_disagreements": len(dr),
        "first_r_zero_set_disagreement": dr[0] if dr else None,
        "last_r_zero_set_disagreement": dr[-1] if dr else None,
        "l_zero_set_disagreements": len(dl),
        "defect_identity_violations": viol,
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
    out: dict = {}

    grid = COMMON.simulate_seed({0: 1, 3: 1}, 150)
    m = cols_fast(0b1001, 150)
    for x in (-1, 0, 1):
        assert m[x] == [grid[t].get(x, 0) for t in range(150)], f"col {x}"
    log.info("cross-check OK against common/rule30.simulate_seed")

    for w in (16, 20):
        pairs = find_pairs(w, 400)
        log.info("")
        log.info("=== w=%d: %d pairs with same centre trace (400 steps) and "
                 "r differing on the zero set ===", w, len(pairs))
        recs = []
        DEEP = 40000
        for a, b in pairs:
            rec400 = examine(a, b, 400)
            deep = agree_upto(a, b, DEEP)
            rec = {
                "at_400": rec400,
                "agree_upto_at_deep": deep,
                "deep_horizon": DEEP,
                "survives_deep": deep == DEEP,
            }
            if deep == DEEP:
                full = examine(a, b, DEEP)
                rec["deep_examine"] = full
            recs.append(rec)
            log.info(
                "  %s vs %s: agree to %d/400; centre traces first differ at "
                "t=%s (horizon %d); r|Z disagreements in [0,400): %d, "
                "last at t=%s; defect-identity violations: %d",
                rec400["seed_a"], rec400["seed_b"],
                rec400["centre_traces_agree_up_to"],
                deep if deep < DEEP else "never",
                DEEP,
                rec400["r_zero_set_disagreements"],
                rec400["last_r_zero_set_disagreement"],
                rec400["defect_identity_violations"],
            )
        out[f"w{w}"] = recs
        n_survive = sum(1 for r in recs if r["survives_deep"])
        log.info("  ---> %d of %d pairs still have equal centre traces at "
                 "T = %d", n_survive, len(recs), DEEP)
        out[f"w{w}_n_survive_deep"] = n_survive
        out[f"w{w}_n_pairs"] = len(recs)

    (HERE / "collision_detail_output.json").write_text(json.dumps(out, indent=2))
    log.info("")
    log.info("wrote collision_detail_output.json")


if __name__ == "__main__":
    main()

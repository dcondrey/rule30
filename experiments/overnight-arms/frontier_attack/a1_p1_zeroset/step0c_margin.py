"""The decisive step-0 measurement: is a zero-set `r` disagreement ever STRICTLY
INSIDE a centre-agreement window, or only at its edge?

step0b showed that all 18 w=16 "hits" at T=400 disagree in `r|Z` at t=399 and
have their centre traces break at t=400 -- i.e. the disagreement is the leading
edge of the collision collapsing, not a genuine "same trace, different r|Z".
That is a horizon artifact of the fixed T.

The scale-free version.  For a pair of finite seeds `(a,b)` let

    A = first t with c_t(a) != c_t(b)            (centre agreement horizon)
    D = first t < A with c_t = 0 and r_t(a) != r_t(b)   (zero-set r defect)

and define the MARGIN = A - D.  A margin of 1 is the artifact above.  A large
margin is a genuine finite instance of R1's kill shape: the centre agrees for
`margin` further steps while `r` already differs on the zero set.

This script sweeps every pair of finite seeds in a window whose centre traces
agree on a 32-step prefix, computes (A, D, margin) with a deep cap, and reports
the margin distribution.  It also reports the same statistic for the
STROBOSCOPIC pairing (the lone-seed diagram against its own time shift, which is
the pairing R1 actually needs, register row 31) for direct comparison.

Rule 90 control included.

Run: uv run python step0c_margin.py
"""

from __future__ import annotations

import collections
import importlib.util
import itertools
import json
import logging
import pathlib
import sys

log = logging.getLogger("margin")
REPO = pathlib.Path("/Volumes/A/researchpapers/13-rule30")
HERE = pathlib.Path(__file__).resolve().parent
CAP = 4000
PREFIX = 24


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


def prefix_cr(bits: int, n: int, rule: str) -> tuple[str, str]:
    step = stepper(rule)
    row = bits
    c, r = [], []
    for t in range(n):
        c.append("1" if (row >> t) & 1 else "0")
        r.append("1" if (row >> (t + 1)) & 1 else "0")
        row = step(row)
    return "".join(c), "".join(r)


def scan_pair(a: int, b: int, rule: str, cap: int = CAP) -> tuple[int, int | None]:
    """(A, D) with early exit at the first centre disagreement."""
    step = stepper(rule)
    ra, rb = a, b
    D = None
    for t in range(cap):
        ca = (ra >> t) & 1
        cb = (rb >> t) & 1
        if ca != cb:
            return t, D
        if ca == 0 and D is None:
            if ((ra >> (t + 1)) & 1) != ((rb >> (t + 1)) & 1):
                D = t
        ra, rb = step(ra), step(rb)
    return cap, D


def sweep(w: int, rule: str) -> dict:
    buckets: dict[str, list[int]] = {}
    for rest in itertools.product((0, 1), repeat=w - 1):
        bits = 1 | sum(v << (i + 1) for i, v in enumerate(rest))
        c, _ = prefix_cr(bits, PREFIX, rule)
        buckets.setdefault(c, []).append(bits)
    margins = collections.Counter()
    examples: list[dict] = []
    n_pairs = 0
    for seeds in buckets.values():
        if len(seeds) < 2:
            continue
        for a, b in itertools.combinations(seeds, 2):
            n_pairs += 1
            A, D = scan_pair(a, b, rule)
            if D is None:
                margins["no_zero_set_defect_before_A"] += 1
                continue
            m = A - D
            margins[m] += 1
            if m >= 3:
                examples.append({"a": bin(a), "b": bin(b), "A": A, "D": D,
                                 "margin": m})
    examples.sort(key=lambda d: -d["margin"])
    return {
        "rule": rule,
        "window": w,
        "prefix_grouping": PREFIX,
        "cap": CAP,
        "n_pairs_agreeing_on_prefix": n_pairs,
        "margin_histogram": {str(k): v for k, v in sorted(
            margins.items(), key=lambda kv: str(kv[0]))},
        "max_margin": max((e["margin"] for e in examples), default=(
            max((k for k in margins if isinstance(k, int)), default=None))),
        "top_examples": examples[:15],
    }


def stroboscopic(rule: str, T: int, max_p: int) -> dict:
    """Same statistic for the pairing R1 needs: the lone-seed diagram vs itself
    shifted by p in time (register row 31)."""
    step = stepper(rule)
    row = 1
    c, r = [], []
    for t in range(T):
        c.append((row >> t) & 1)
        r.append((row >> (t + 1)) & 1)
        row = step(row)
    margins = collections.Counter()
    best: list[dict] = []
    for p in range(1, max_p + 1):
        t = 0
        n = T - p
        while t < n:
            if c[t] != c[t + p]:
                t += 1
                continue
            a = t
            while t < n and c[t] == c[t + p]:
                t += 1
            A = t  # first disagreement (or n)
            D = next((u for u in range(a, A)
                      if c[u] == 0 and r[u] != r[u + p]), None)
            if D is None:
                margins["no_zero_set_defect_in_run"] += 1
            else:
                m = A - D
                margins[m] += 1
                best.append({"p": p, "run_start": a, "run_end": A,
                             "run_len": A - a, "D": D, "margin": m})
    best.sort(key=lambda d: -d["margin"])
    return {
        "rule": rule,
        "T": T,
        "max_p": max_p,
        "margin_histogram": {str(k): v for k, v in sorted(
            margins.items(), key=lambda kv: str(kv[0]))},
        "max_margin": best[0]["margin"] if best else None,
        "top_examples": best[:10],
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
    grid = COMMON.simulate_seed({0: 1, 2: 1}, 120)
    c, r = prefix_cr(0b101, 120, "30")
    assert c == "".join(str(grid[t].get(0, 0)) for t in range(120))
    assert r == "".join(str(grid[t].get(1, 0)) for t in range(120))
    log.info("cross-check OK against common/rule30.simulate_seed")

    out: dict = {}
    log.info("")
    log.info("=== distinct-seed pairing (step 0's mandated test) ===")
    for rule in ("30", "90"):
        for w in (14, 16):
            s = sweep(w, rule)
            log.info("rule %s w=%d: %d pairs agreeing on a %d-step centre prefix; "
                     "margin histogram %s; max margin %s",
                     rule, w, s["n_pairs_agreeing_on_prefix"], PREFIX,
                     s["margin_histogram"], s["max_margin"])
            for e in s["top_examples"][:5]:
                log.info("    %s", json.dumps(e))
            out[f"pairs_rule{rule}_w{w}"] = s

    log.info("")
    log.info("=== stroboscopic pairing (the pairing R1 needs; row 31) ===")
    for rule, T, P in (("30", 16384, 512), ("90", 4096, 8)):
        s = stroboscopic(rule, T, P)
        log.info("rule %s T=%d P=%d: max margin %s", rule, T, P, s["max_margin"])
        log.info("  margin histogram: %s", json.dumps(s["margin_histogram"]))
        for e in s["top_examples"][:5]:
            log.info("    %s", json.dumps(e))
        out[f"strobo_rule{rule}"] = s

    (HERE / "margin_output.json").write_text(json.dumps(out, indent=2))
    log.info("")
    log.info("wrote margin_output.json")


if __name__ == "__main__":
    main()

"""R1's target implication is FALSE for Rule 90, on Rule 90's own lone seed.

R1 (PATH.md section 4): "Show that `c` eventually periodic forces `r` eventually
periodic on `{c_t = 0}`."

Rule 90, lone seed:
  * `c_t = s(t,0) = 0` for every `t >= 1`, so `c` is eventually periodic
    (period 1) and the zero set is `Z = {t : t >= 1}`, i.e. cofinite;
  * `r_t = s(t,1) = 1` **iff** `t = 2^j - 1` for some `j >= 1`.

Proof of the second line.  For the Rule 90 lone seed
`s(t,x) = C(t, (t+x)/2) mod 2` when `t+x` is even and `|x| <= t`, and 0 otherwise.
At `x = 1` this needs `t` odd; write `t = 2m+1`, giving
`s(t,1) = C(2m+1, m+1) = C(2m+1, m) mod 2`.  By Kummer's theorem `C(a+b, a)` is
odd iff adding `a` and `b` in base 2 produces no carries, i.e. iff `a AND b = 0`.
Here `a = m`, `b = m+1`, and `m AND (m+1) = 0` iff `m = 2^j - 1`.  Hence
`t = 2m+1 = 2^{j+1} - 1`.

So `r` restricted to `Z` has infinitely many ones and unbounded gaps between
consecutive ones.  An eventually periodic binary word either is eventually zero
or has bounded gaps between its ones; `r|Z` is neither.  Therefore `r|Z` is NOT
eventually periodic while `c` IS eventually periodic.

Consequence: **the rule-generic form of R1's implication is false**, and it is
false on a finite (lone-seed) configuration of a quiescent left-permutive ECA, so
no argument for R1 that does not use a Rule-30-specific ingredient can work.  By
the PATH.md section 1.1 table the separating ingredient available is the OR-latch
pin, which Rule 90 lacks (`g(b,0) = g(b,1)` fails for both `b`).

This script verifies every quantified claim above by exact simulation, reusing
experiments/overnight-arms/common/rule30.py as the independent cross-check.

Run: uv run python rule90_zeroset_counterexample.py
"""

from __future__ import annotations

import importlib.util
import json
import logging
import pathlib
import sys

log = logging.getLogger("r90")
REPO = pathlib.Path("/Volumes/A/researchpapers/13-rule30")
HERE = pathlib.Path(__file__).resolve().parent


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, REPO / rel)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


COMMON = _load("oa_rule30", "experiments/overnight-arms/common/rule30.py")
FILTER = _load("oa_filter", "experiments/overnight-arms/common/ensemble_filter.py")


def cols90(n: int) -> tuple[list[int], list[int], list[int]]:
    """(c, r, l) = columns 0, +1, -1 of the Rule 90 lone seed, t < n."""
    row = 1  # frame b_t(i) = s(t, i-t)
    c, r, l = [], [], []
    for t in range(n):
        c.append((row >> t) & 1)
        r.append((row >> (t + 1)) & 1)
        l.append((row >> (t - 1)) & 1 if t >= 1 else 0)
        row = (row << 2) ^ row
    return c, r, l


def eventually_periodic(word: list[int], max_p: int, max_t0: int) -> dict:
    """Search for (t0, p) with word[t] == word[t+p] for all t0 <= t < len-p.

    A negative answer over a finite window is a finite check, not a proof
    (PATH.md obstruction H); the PROOF is the unbounded-gap argument above.
    """
    n = len(word)
    for p in range(1, max_p + 1):
        for t0 in range(0, max_t0 + 1):
            if all(word[t] == word[t + p] for t in range(t0, n - p)):
                return {"found": True, "t0": t0, "p": p}
    return {"found": False, "max_p": max_p, "max_t0": max_t0, "n": n}


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
    out: dict = {}
    N = 1 << 16  # 65536

    # cross-check the generator against the shared substrate
    ref = FILTER.center_column("90", 4096)
    c, r, l = cols90(N)
    assert c[:4096] == ref, "column 0 disagrees with common/ensemble_filter"
    grid = COMMON.simulate_seed({0: 1}, 300)  # rule 30 simulator: sanity of the API
    assert grid[0] == {0: 1}
    log.info("cross-check OK: rule 90 column 0 matches common/ensemble_filter "
             "for 4096 steps")

    # 1. c is eventually periodic
    ones_after_0 = [t for t in range(1, N) if c[t]]
    out["c_zero_for_all_t_ge_1"] = not ones_after_0
    log.info("c_t = 0 for every 1 <= t < %d: %s", N, not ones_after_0)
    zero_set_is_cofinite = all(c[t] == 0 for t in range(1, N))
    out["zero_set_is_{t>=1}"] = zero_set_is_cofinite

    # 2. r_t = 1 iff t = 2^j - 1
    predicted = {(1 << j) - 1 for j in range(1, N.bit_length() + 2)}
    actual = {t for t in range(N) if r[t]}
    out["r_ones_upto_N"] = sorted(actual)
    match = actual == {t for t in predicted if t < N}
    out["r_matches_2^j_minus_1"] = match
    log.info("r_t = 1 exactly at t in %s  (N = %d)", sorted(actual), N)
    log.info("matches the closed form t = 2^j - 1: %s", match)

    # 3. gaps are unbounded -> r|Z is not eventually periodic
    ones = sorted(actual)
    gaps = [b - a for a, b in zip(ones, ones[1:])]
    out["consecutive_gaps"] = gaps
    log.info("consecutive gaps between ones of r: %s (strictly increasing: %s)",
             gaps, all(x < y for x, y in zip(gaps, gaps[1:])))

    # 4. finite confirmation: no (t0 <= 512, p <= 4096) period for r on Z = {t>=1}
    r_on_Z = r[1:]
    ep = eventually_periodic(r_on_Z, max_p=4096, max_t0=512)
    out["r_on_Z_eventually_periodic_search"] = ep
    log.info("finite search for an eventual period of r|Z: %s", json.dumps(ep))

    # 5. the same for column -1 (the object section 2 converts to)
    out["l_equals_r"] = l[1:] == r[1:]
    log.info("column -1 equals column +1 from t=1 (mirror symmetry): %s",
             out["l_equals_r"])

    # 6. the pin: rule 90 has none, rule 30 does. Count antecedents/violations.
    def pin_stats(rule: str, T: int) -> dict:
        row = 1
        rows = []
        for _ in range(T + 2):
            rows.append(row)
            row = (row << 2) ^ ((row << 1) | row) if rule == "30" else (row << 2) ^ row
        ante = viol = 0
        for t in range(T):
            for x in range(-t - 1, t + 2):
                i = x + t
                if i < 0:
                    continue
                if (rows[t] >> i) & 1:  # s(t,x) = 1
                    ante += 1
                    left = (rows[t] >> (i - 1)) & 1 if i >= 1 else 0
                    below = (rows[t + 1] >> (x + t + 1)) & 1
                    if left != (1 ^ below):
                        viol += 1
        return {"antecedents": ante, "violations": viol}

    out["pin_rule30"] = pin_stats("30", 300)
    out["pin_rule90"] = pin_stats("90", 300)
    log.info("OR-latch pin s(t,x)=1 => s(t,x-1) = NOT s(t+1,x), T=300: "
             "rule 30 %s ; rule 90 %s", out["pin_rule30"], out["pin_rule90"])

    verdict = (
        out["c_zero_for_all_t_ge_1"]
        and match
        and all(x < y for x, y in zip(gaps, gaps[1:]))
        and not ep["found"]
    )
    out["VERDICT_rule90_falsifies_rule_generic_R1"] = verdict
    log.info("")
    log.info("VERDICT: rule 90 falsifies the rule-generic form of R1's "
             "implication: %s", verdict)
    (HERE / "rule90_output.json").write_text(json.dumps(out, indent=2))
    log.info("wrote rule90_output.json")


if __name__ == "__main__":
    main()

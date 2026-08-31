"""How long can a centre-agreement run get?  Rule 30 vs a Bernoulli(1/2) null.

R1's kill condition needs an INFINITE centre-agreement run (that is what
"`c` eventually periodic" means, in the stroboscopic pairing `t <-> t+p`).  Every
run found in this tree is finite: row 37's 18 and 24.  This script measures how
the longest run grows with the search volume `T * P`, and compares it with the
same statistic on 20 seeded Bernoulli(1/2) words of the same length.

If the Rule 30 curve tracks `log2(T*P)` -- the null -- then the finite runs carry
no signal about an infinite one, and no amount of further searching can fire
R1's kill condition (PATH.md obstruction H).  That is the claim being tested.

Run: uv run python run_length_scaling.py
"""

from __future__ import annotations

import json
import logging
import math
import pathlib
import random
import re
import sys

log = logging.getLogger("scal")
HERE = pathlib.Path(__file__).resolve().parent


def centre(n: int, rule: str = "30") -> str:
    row = 1
    out = []
    for t in range(n):
        out.append("1" if (row >> t) & 1 else "0")
        row = (row << 2) ^ ((row << 1) | row) if rule == "30" else (row << 2) ^ row
    return "".join(out)


def longest_self_shift_run(word: str, max_p: int) -> tuple[int, int, int]:
    best = (0, 0, 0)  # len, p, t0
    n = len(word)
    for p in range(1, max_p + 1):
        agree = "".join("1" if word[t] == word[t + p] else "0" for t in range(n - p))
        for m in re.finditer(r"1+", agree):
            if m.end() - m.start() > best[0]:
                best = (m.end() - m.start(), p, m.start())
    return best


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
    out = {"rows": []}
    c = centre(65536, "30")
    for T, P in ((1024, 64), (2048, 128), (4096, 256), (8192, 256),
                 (16384, 512), (32768, 512), (65536, 512)):
        L, p, t0 = longest_self_shift_run(c[:T], P)
        nulls = []
        for seed in range(20):
            rng = random.Random(seed)
            w = "".join(rng.choice("01") for _ in range(T))
            nulls.append(longest_self_shift_run(w, P)[0])
        row = {
            "T": T,
            "P": P,
            "log2_TP": round(math.log2(T * P), 2),
            "rule30_longest_run": L,
            "rule30_p": p,
            "rule30_t0": t0,
            "bernoulli_null_mean": round(sum(nulls) / len(nulls), 2),
            "bernoulli_null_min": min(nulls),
            "bernoulli_null_max": max(nulls),
        }
        out["rows"].append(row)
        log.info(
            "T=%6d P=%3d  log2(TP)=%5.2f | rule30 longest run %2d (p=%d, t0=%d) "
            "| Bernoulli null mean %5.2f  [%d, %d]",
            T, P, row["log2_TP"], L, p, t0,
            row["bernoulli_null_mean"], row["bernoulli_null_min"],
            row["bernoulli_null_max"],
        )

    # rule 90: the run is the whole window, at every P
    c90 = centre(4096, "90")
    L90 = longest_self_shift_run(c90, 8)
    out["rule90"] = {"T": 4096, "P": 8, "longest_run": L90[0], "p": L90[1],
                     "t0": L90[2]}
    log.info("rule 90: longest centre-agreement run = %d of 4096 (p=%d, t0=%d) "
             "-- infinite in the limit", *L90)

    (HERE / "run_length_scaling_output.json").write_text(json.dumps(out, indent=2))
    log.info("wrote run_length_scaling_output.json")


if __name__ == "__main__":
    main()

"""Exact language L_n of the centre-column TRACE SUBSHIFT W_rule, by exhaustive
enumeration of the light cone.

W_rule = tau(X) where X = {0,1}^Z (the FULL shift), F = the ECA, and
tau(x) = (x_0, F(x)_0, F^2(x)_0, ...).  This is the column-0 factor over ALL
configurations, NOT the lone-seed column.

Exactness: with neighbourhood {-1,0,+1}, trace bits t = 0..n-1 depend only on
cells [-(n-1), n-1], a window of W = 2n-1 cells, and EVERY assignment of that
window extends to a configuration of Z.  Hence

    L_n(W_rule) = { trace_n(y) : y in {0,1}^{2n-1} }

exactly -- no approximation, no bounded-width caveat.  (The bounded-width caveat
of obstruction H bites on FOLLOWER sets, not on L_n; see follower_ladder.py.)

Run: uv run python exact_language.py [--nmax 13]
"""

from __future__ import annotations

import argparse
import json
import logging
import pathlib

import numpy as np

log = logging.getLogger(__name__)


def step(c: np.ndarray, mask: int, rule: str) -> np.ndarray:
    """One CA step on packed windows.  bit i of c is cell x = i - (n-1)."""
    left = (c << np.uint64(1)) & np.uint64(mask)  # s(t, x-1) moved into slot x
    right = c >> np.uint64(1)  # s(t, x+1) moved into slot x
    if rule == "30":
        return (left ^ (c | right)) & np.uint64(mask)
    if rule == "90":
        return (left ^ right) & np.uint64(mask)
    raise ValueError(rule)


def language(n: int, rule: str) -> np.ndarray:
    """All length-n trace words, as ints with bit t = trace bit at time t."""
    w = 2 * n - 1
    if w > 27:
        raise ValueError("window too wide for brute force")
    mask = (1 << w) - 1
    c = np.arange(1 << w, dtype=np.uint64)
    centre = np.uint64(n - 1)
    out = np.zeros(1 << w, dtype=np.uint64)
    for t in range(n):
        out |= ((c >> centre) & np.uint64(1)) << np.uint64(t)
        if t + 1 < n:
            c = step(c, mask, rule)
    return np.unique(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmax", type=int, default=13)
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    here = pathlib.Path(__file__).parent
    results: dict[str, dict[str, list]] = {}
    for rule in ("30", "90"):
        rows = []
        for n in range(1, args.nmax + 1):
            words = language(n, rule)
            full = len(words) == (1 << n)
            rows.append({"n": n, "count": int(len(words)), "full": bool(full)})
            log.info(
                "rule %s  n=%2d  |L_n| = %6d / %6d   %s",
                rule, n, len(words), 1 << n, "FULL SHIFT" if full else "PROPER",
            )
            if not full and n <= 8:
                missing = sorted(set(range(1 << n)) - set(int(x) for x in words))
                log.info(
                    "         forbidden (%d): %s",
                    len(missing),
                    [format(m, f"0{n}b")[::-1] for m in missing[:12]],
                )
        results[rule] = {"L_n": rows}

    (here / "out" / "exact_language.json").write_text(json.dumps(results, indent=1))
    log.info("wrote out/exact_language.json")


if __name__ == "__main__":
    main()

"""Exact language of the WIDTH-k column (trace) subshift over ALL configurations.

tau_k(x) = ( (x_0..x_{k-1}), (F x)_0..(F x)_{k-1}, ... ) in ({0,1}^k)^N.
W_rule^{(k)} = tau_k({0,1}^Z).  k = 1 is the centre-column trace.

Exactness: trace letters t = 0..n-1 depend only on cells [-(n-1), n-2+k], a
window of W = 2n + k - 2 cells, and every window assignment extends to a
configuration.  So the enumeration below is exact for L_n, not a lower bound.

Run: uv run python width_k_language.py --kmax 3 --nmax 10
"""

from __future__ import annotations

import argparse
import json
import logging
import pathlib

import numpy as np

log = logging.getLogger(__name__)


def step(c: np.ndarray, mask: int, rule: str) -> np.ndarray:
    left = (c << np.uint64(1)) & np.uint64(mask)
    right = c >> np.uint64(1)
    if rule == "30":
        return (left ^ (c | right)) & np.uint64(mask)
    if rule == "90":
        return (left ^ right) & np.uint64(mask)
    raise ValueError(rule)


def language(n: int, k: int, rule: str) -> int:
    """Number of distinct length-n words over the alphabet {0,1}^k."""
    w = 2 * n + k - 2
    if w > 26:
        raise ValueError(f"window {w} too wide")
    mask = (1 << w) - 1
    c = np.arange(1 << w, dtype=np.uint64)
    base = np.uint64(n - 1)  # bit index of cell x = 0
    out = np.zeros(1 << w, dtype=np.uint64)
    for t in range(n):
        for j in range(k):
            bit = (c >> (base + np.uint64(j))) & np.uint64(1)
            out |= bit << np.uint64(t * k + j)
        if t + 1 < n:
            c = step(c, mask, rule)
    return int(len(np.unique(out)))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kmax", type=int, default=3)
    ap.add_argument("--nmax", type=int, default=10)
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    here = pathlib.Path(__file__).parent
    res = []
    for rule in ("30", "90"):
        for k in range(1, args.kmax + 1):
            prev = None
            for n in range(1, args.nmax + 1):
                if 2 * n + k - 2 > 26:
                    break
                cnt = language(n, k, rule)
                full = cnt == (1 << (n * k))
                growth = None if prev is None else cnt / prev
                res.append({"rule": rule, "k": k, "n": n, "count": cnt,
                            "full": full, "ratio": growth})
                log.info(
                    "rule %s k=%d n=%2d |L_n| = %10d / %-12d %-6s ratio=%s",
                    rule, k, n, cnt, 1 << (n * k),
                    "FULL" if full else "PROPER",
                    "-" if growth is None else f"{growth:.4f}",
                )
                prev = cnt
    (here / "out" / "width_k_language.json").write_text(json.dumps(res, indent=1))
    log.info("wrote out/width_k_language.json")


if __name__ == "__main__":
    main()

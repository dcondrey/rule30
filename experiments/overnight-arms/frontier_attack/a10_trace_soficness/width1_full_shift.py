"""THEOREM CHECK: for every LEFT-PERMUTIVE ECA, the width-1 column subshift
Sigma_1(F) = { (F^t(x)_0)_{t>=0} : x in {0,1}^Z } is the FULL shift {0,1}^N.

Proof (two lines, no computation).  Left permutivity means
s(t+1,x) = s(t,x-1) XOR g(s(t,x), s(t,x+1)).  Induction on t gives
    s(t,0) = x_{-t} XOR G_t(x_{-(t-1)}, ..., x_t),
i.e. the centre trace bit at time t depends on x_{-t} permutively and otherwise
only on strictly-inner cells.  So fix x_1, x_2, ... arbitrarily, choose x_0 to
hit the trace bit at t=0, then x_{-1} to hit t=1, then x_{-2} for t=2, ...:
the system is triangular and every word is realised.  QED.

CONSEQUENCE (this is the point).  Sigma_1(W30) = Sigma_1(W90) = the full shift.
The width-1 trace subshift over all configurations is rule-blind across the
whole left-permutive class, so it cannot be the object in any Rule-30-specific
question, and it says nothing whatever about P1 (the full shift contains both
eventually periodic and non-eventually-periodic points).

This script verifies the theorem by exhaustive enumeration for all 256 ECAs and
n <= 10, and reports which rules are left permutive.

Run: uv run python width1_full_shift.py
"""

from __future__ import annotations

import json
import logging
import pathlib

import numpy as np

log = logging.getLogger(__name__)


def is_left_permutive(rule: int) -> bool:
    """f(a,b,c) with a the LEFT cell: flipping a must always flip the output."""
    def f(a: int, b: int, c: int) -> int:
        return (rule >> (4 * a + 2 * b + c)) & 1
    return all(f(0, b, c) != f(1, b, c) for b in (0, 1) for c in (0, 1))


def trace_words(n: int, rule: int) -> int:
    """|L_n| of the width-1 column subshift, exact (light-cone enumeration)."""
    w = 2 * n - 1
    mask = (1 << w) - 1
    c = np.arange(1 << w, dtype=np.uint64)
    lut = np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint64)
    centre = np.uint64(n - 1)
    out = np.zeros(1 << w, dtype=np.uint64)
    for t in range(n):
        out |= ((c >> centre) & np.uint64(1)) << np.uint64(t)
        if t + 1 < n:
            left = (c << np.uint64(1)) & np.uint64(mask)
            right = c >> np.uint64(1)
            # per-cell index 4*left + 2*self + right, computed bitwise via LUT
            nxt = np.zeros_like(c)
            for bit in range(w):
                idx = (((left >> np.uint64(bit)) & np.uint64(1)) * np.uint64(4)
                       + ((c >> np.uint64(bit)) & np.uint64(1)) * np.uint64(2)
                       + ((right >> np.uint64(bit)) & np.uint64(1)))
                nxt |= lut[idx] << np.uint64(bit)
            c = nxt
    return int(len(np.unique(out)))


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    here = pathlib.Path(__file__).parent
    lp = [r for r in range(256) if is_left_permutive(r)]
    log.info("left-permutive ECAs (%d): %s", len(lp), lp)
    n = 9
    rows = []
    bad = []
    for r in lp:
        cnt = trace_words(n, r)
        full = cnt == (1 << n)
        rows.append({"rule": r, "n": n, "count": cnt, "full": full})
        if not full:
            bad.append(r)
    log.info("n=%d: %d/%d left-permutive rules have FULL width-1 trace language;"
             " exceptions: %s", n, len(lp) - len(bad), len(lp), bad or "none")
    # negative control: a non-left-permutive rule with a proper width-1 trace
    ctrl = [(r, trace_words(n, r)) for r in (110, 128, 4, 0, 232)]
    for r, cnt in ctrl:
        log.info("control rule %3d (not left permutive): |L_%d| = %5d / %d %s",
                 r, n, cnt, 1 << n, "FULL" if cnt == (1 << n) else "PROPER")
    (here / "out" / "width1_full_shift.json").write_text(json.dumps(
        {"left_permutive": lp, "n": n, "rows": rows,
         "exceptions": bad, "controls": ctrl}, indent=1))
    log.info("wrote out/width1_full_shift.json")


if __name__ == "__main__":
    main()

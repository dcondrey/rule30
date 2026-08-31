"""ergodic arm: decisive full-support uniqueness test (PREREG-ergodic.md).

sp.solve enumerates components and may miss some, which is too weak for a
classification claim. Instead: add the Rabinowitsch element
    z * prod_w q_w (1 - q_w) - 1 = 0
to the invariance ideal. Its variety is exactly the invariance solutions with
EVERY transition probability strictly in (0,1) (full support). A Groebner basis
of that saturated ideal decides uniqueness outright:
    GB = {q_w - 1/2, ...}  => uniform Bernoulli is the unique full-support solution
    GB = {1}               => NO full-support solution exists at all
    anything else          => a non-uniform full-support solution exists (K1 fires)

Run: uv run --with sympy python experiments/overnight-arms/ergodic/markov_saturate.py [m] [L]
"""

from __future__ import annotations

import itertools
import json
import logging
import pathlib
import sys
import time

import sympy as sp

from markov_main import MarkovM, invariance_eqs

log = logging.getLogger(__name__)
OUT = pathlib.Path("/Volumes/A/researchpapers/13-rule30/runs/overnight/ergodic/saturate.json")


def run(m: int, L: int) -> dict:
    mu = MarkovM(m)
    qs = [mu.q[w] for w in sorted(mu.q)]
    z = sp.Symbol("z")
    log.info("m=%d L=%d: building invariance equations", m, L)
    polys = []
    for e in invariance_eqs(mu, L):
        num, _ = sp.fraction(sp.together(e))
        num = sp.expand(num)
        if num != 0:
            polys.append(num)
    sat = z * sp.prod([q * (1 - q) for q in qs]) - 1
    log.info("m=%d L=%d: %d equations + saturation, computing Groebner basis", m, L, len(polys))
    t0 = time.monotonic()
    gb = sp.groebner(polys + [sat], *(qs + [z]), order="lex")
    dt = time.monotonic() - t0
    basis = [str(g) for g in gb.exprs]
    trivial = list(gb.exprs) == [sp.Integer(1)]
    uniform_only = all(
        any(sp.simplify(g.subs({q: sp.Rational(1, 2) for q in qs})) == 0 for _ in [0])
        for g in gb.exprs
    ) and not trivial
    res = {
        "m": m, "L": L, "n_eqs": len(polys), "seconds": round(dt, 1),
        "gb_size": len(basis), "gb": basis[:40],
        "empty_variety": trivial, "uniform_satisfies_gb": uniform_only,
    }
    log.info("m=%d L=%d: done in %.1fs, |GB|=%d, empty=%s", m, L, dt, len(basis), trivial)
    for g in basis[:20]:
        log.info("   %s", g)
    return res


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    L = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    res = run(m, L)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    prev = json.loads(OUT.read_text()) if OUT.exists() else []
    prev = [r for r in prev if (r["m"], r["L"]) != (m, L)] + [res]
    OUT.write_text(json.dumps(prev, indent=1))


if __name__ == "__main__":
    main()

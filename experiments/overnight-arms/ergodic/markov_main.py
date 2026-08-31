"""ergodic arm, main run (PREREG-ergodic.md).

Memory-2 (and attempted memory-3) jointly (shift, Rule 30)-invariant Markov
measures, exact arithmetic. Strategy: SOLVE on shallow blocks, then VERIFY every
surviving solution on deep blocks by substitution (cheap).

Parameterization: q_w = P(next=1 | previous m symbols = w), 2^m unknowns.
Stationary distribution on m-blocks obtained exactly via linsolve.
Writes runs/overnight/ergodic/main.json.

Run: uv run --with sympy python experiments/overnight-arms/ergodic/markov_main.py
"""

from __future__ import annotations

import itertools
import json
import logging
import pathlib

import sympy as sp

log = logging.getLogger(__name__)
OUT = pathlib.Path("/Volumes/A/researchpapers/13-rule30/runs/overnight/ergodic/main.json")


def rule30(l: int, c: int, r: int) -> int:
    return l ^ (c | r)


class MarkovM:
    """Memory-m stationary Markov measure with symbolic transition params."""

    def __init__(self, m: int):
        self.m = m
        self.q = {
            w: sp.Symbol("q" + "".join(map(str, w)), real=True)
            for w in itertools.product((0, 1), repeat=m)
        }
        self.pi = self._stationary()

    def _trans_prob(self, w, z):
        return self.q[w] if z else 1 - self.q[w]

    def _stationary(self):
        states = list(itertools.product((0, 1), repeat=self.m))
        n = len(states)
        pvars = sp.symbols(f"pi0:{n}", real=True)
        eqs = []
        for j, s in enumerate(states):
            # inflow: states u with u[1:] + (z,) == s
            expr = -pvars[j]
            for i, u in enumerate(states):
                if u[1:] == s[:-1]:
                    expr += pvars[i] * self._trans_prob(u, s[-1])
            eqs.append(expr)
        eqs.append(sum(pvars) - 1)
        sol = sp.solve(eqs[1:], pvars, dict=True)
        assert sol, "no stationary solution"
        return {s: sp.together(sol[0][pvars[j]]) for j, s in enumerate(states)}

    def prob(self, word):
        m = self.m
        if len(word) < m:
            # marginal of the m-block distribution
            total = 0
            for pad in itertools.product((0, 1), repeat=m - len(word)):
                total += self.pi[tuple(word) + pad]
            return total
        p = self.pi[tuple(word[:m])]
        for i in range(len(word) - m):
            p *= self._trans_prob(tuple(word[i : i + m]), word[i + m])
        return p


def invariance_eqs(mu, max_len: int, min_len: int = 1):
    eqs = []
    for k in range(min_len, max_len + 1):
        for w in itertools.product((0, 1), repeat=k):
            total = 0
            for u in itertools.product((0, 1), repeat=k + 2):
                if all(rule30(u[i], u[i + 1], u[i + 2]) == w[i] for i in range(k)):
                    total += mu.prob(u)
            eqs.append(total - mu.prob(w))
    return eqs


def solve_memory(m: int, solve_len: int, verify_len: int) -> dict:
    mu = MarkovM(m)
    qvars = [mu.q[w] for w in sorted(mu.q)]
    log.info("m=%d: building solve equations |w|<=%d ...", m, solve_len)
    eqs = invariance_eqs(mu, solve_len)
    polys = []
    for e in eqs:
        e = sp.together(e)
        num, _den = sp.fraction(e)
        num = sp.expand(num)
        if num != 0:
            polys.append(num)
    log.info("m=%d: solving %d polynomial equations in %d unknowns", m, len(polys), len(qvars))
    sols = sp.solve(polys, qvars, dict=True)
    log.info("m=%d: raw solutions: %d", m, len(sols))
    out = []
    for s in sols:
        entry = {str(k): str(v) for k, v in s.items()}
        # verify deep blocks by substitution; skip solutions with free symbols
        subs = {mu.q[w]: s.get(mu.q[w], mu.q[w]) for w in mu.q}
        free = any(getattr(v, "free_symbols", set()) for v in subs.values())
        if not free:
            deep = invariance_eqs_sub(mu, subs, verify_len, solve_len + 1)
            entry["verified_to"] = verify_len if deep else "FAILED-DEEP"
        else:
            entry["verified_to"] = "has-free-symbols; verify manually"
        out.append(entry)
        log.info("m=%d sol %s -> %s", m, entry, entry["verified_to"])
    return {"m": m, "solve_len": solve_len, "verify_len": verify_len, "solutions": out}


def invariance_eqs_sub(mu, subs, max_len: int, min_len: int) -> bool:
    """True iff all invariance equations hold after substitution."""
    for k in range(min_len, max_len + 1):
        for w in itertools.product((0, 1), repeat=k):
            total = 0
            for u in itertools.product((0, 1), repeat=k + 2):
                if all(rule30(u[i], u[i + 1], u[i + 2]) == w[i] for i in range(k)):
                    total += mu.prob(u)
            diff = sp.simplify(sp.together(total - mu.prob(w)).subs(subs))
            if sp.simplify(diff) != 0:
                return False
    return True


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    results = []
    results.append(solve_memory(2, solve_len=6, verify_len=9))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=1))
    results.append(solve_memory(3, solve_len=6, verify_len=8))
    OUT.write_text(json.dumps(results, indent=1))
    log.info("done")


if __name__ == "__main__":
    main()

"""ergodic arm, cheapest disconfirming test (PREREG-ergodic.md).

Exact invariance of Bernoulli(p) and memory-1 Markov measures under Rule 30
pushforward, blocks |w| <= 5, sympy exact arithmetic.
Gates: uniform Bernoulli(1/2) MUST pass (classical, surjectivity); identity rule
must accept every measure; Rule 90 must accept p = 1/2. Question: any other
exact solutions?

Run: uv run --with sympy python experiments/overnight-arms/ergodic/markov_probe.py
"""

from __future__ import annotations

import itertools
import logging

import sympy as sp

log = logging.getLogger(__name__)


def rule30(l: int, c: int, r: int) -> int:
    return l ^ (c | r)


def rule90(l: int, c: int, r: int) -> int:
    return l ^ r


def identity_rule(l: int, c: int, r: int) -> int:
    return c


def bernoulli_prob(word: tuple[int, ...], p):
    return sp.prod([p if x else 1 - p for x in word])


def markov_prob(word: tuple[int, ...], a, b):
    # a = P(1|0), b = P(0|1); stationary pi = (b, a)/(a+b)
    pi0, pi1 = b / (a + b), a / (a + b)
    prob = pi1 if word[0] else pi0
    trans = {(0, 1): a, (0, 0): 1 - a, (1, 0): b, (1, 1): 1 - b}
    for x, y in zip(word, word[1:]):
        prob *= trans[(x, y)]
    return prob


def pushforward_eqs(rule, mu, max_len: int):
    """Polynomial equations (F mu)[w] - mu[w] = 0 for |w| <= max_len."""
    eqs = []
    for k in range(1, max_len + 1):
        for w in itertools.product((0, 1), repeat=k):
            total = 0
            for u in itertools.product((0, 1), repeat=k + 2):
                if all(rule(u[i], u[i + 1], u[i + 2]) == w[i] for i in range(k)):
                    total += mu(u)
            eqs.append(sp.simplify(total - mu(w)))
    return [e for e in eqs if e != 0]


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    p = sp.Symbol("p", real=True)
    a, b = sp.symbols("a b", real=True)

    for name, rule in (("identity", identity_rule), ("rule90", rule90), ("rule30", rule30)):
        eqs = pushforward_eqs(rule, lambda w: bernoulli_prob(w, p), 5)
        sols = sp.solve(eqs, p, dict=True) if eqs else "ALL p (no constraints)"
        log.info("%s / Bernoulli(p), |w|<=5: eqs=%d sols=%s", name, len(eqs) if eqs else 0, sols)

    # Memory-1 Markov under rule 30, blocks <= 4 (cheap); a,b in (0,1] boundary handled after.
    eqs = pushforward_eqs(rule30, lambda w: markov_prob(w, a, b), 4)
    polys = [sp.factor(sp.together(e)) for e in eqs]
    sols = sp.solve(polys, (a, b), dict=True)
    log.info("rule30 / Markov(a,b), |w|<=4: eqs=%d", len(polys))
    for s in sols:
        log.info("  sol: %s", s)


if __name__ == "__main__":
    main()

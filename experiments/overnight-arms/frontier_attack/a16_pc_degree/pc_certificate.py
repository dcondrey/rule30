"""Explicit PC refutation of S_n(rule) at degree = max axiom degree, machine-checked.

Constructs a concrete derivation and then re-verifies EVERY line with an
independent checker: each line is either an axiom, or `x * f` for an earlier
line `f` and a variable `x`, or `f + g` for two earlier lines.  The final line
must be the constant 1, and no line may exceed the claimed degree.

The construction is the uniform lemma:

    Along the topological order of D_n, suppose the unit lines U_p = p + b_p are
    already derived for the in-cone parents of a cell (b_p the true value).
    Start from the cell axiom A = s + ANF(parents).  While A carries a monomial
    m of degree >= 2, pick u in m and multiply U_u by the remaining variables of
    m one at a time, giving m + b_u * (m \\ {u}); add it to A.  This strictly
    reduces the multidegree, and every intermediate line has degree <= deg(m).
    When only degree-<=1 monomials remain, add U_p for each parent p that still
    occurs.  What is left is s + const, and the const is b_s by soundness.
    Finally add the negation unit to U_{(n,0)} to obtain 1.

    uv run python pc_certificate.py --ns 4 8 16 32 64 96 128 --out certificate.json
"""

from __future__ import annotations

import argparse
import json
import logging
import time

from pc_core import ONE, System, padd, pdeg, peval, pmulvar

AX, MUL, ADD = "axiom", "mul", "add"


class Derivation:
    """A PC derivation, recorded step by step so it can be replayed and checked."""

    def __init__(self, axioms: set) -> None:
        self.axiom_set = axioms
        self.lines: list = []       # list of Poly
        self.just: list = []        # (kind, args)
        self._seen: dict = {}

    def axiom(self, p) -> int:
        assert p in self.axiom_set, "claimed axiom is not in the axiom set"
        self.lines.append(p)
        self.just.append((AX, ()))
        return len(self.lines) - 1

    def mul(self, i: int, x: int) -> int:
        self.lines.append(pmulvar(self.lines[i], x))
        self.just.append((MUL, (i, x)))
        return len(self.lines) - 1

    def add(self, i: int, j: int) -> int:
        self.lines.append(padd(self.lines[i], self.lines[j]))
        self.just.append((ADD, (i, j)))
        return len(self.lines) - 1

    # -- independent checker ------------------------------------------------
    def check(self, target, max_degree: int) -> tuple[int, int]:
        """Replay from scratch. Returns (n_lines, observed max degree)."""
        replay: list = []
        obs = -1
        for k, (p, (kind, args)) in enumerate(zip(self.lines, self.just)):
            if kind == AX:
                assert p in self.axiom_set, f"line {k}: not an axiom"
                q = p
            elif kind == MUL:
                i, x = args
                assert 0 <= i < k, f"line {k}: forward reference"
                q = pmulvar(replay[i], x)
            elif kind == ADD:
                i, j = args
                assert 0 <= i < k and 0 <= j < k, f"line {k}: forward reference"
                q = padd(replay[i], replay[j])
            else:
                raise AssertionError(kind)
            assert q == p, f"line {k}: recorded polynomial does not match its rule"
            d = pdeg(q)
            assert d <= max_degree, f"line {k}: degree {d} > {max_degree}"
            obs = max(obs, d)
            replay.append(q)
        assert replay[-1] == target, "final line is not the target"
        return len(replay), obs


def refute(sysm: System) -> Derivation:
    D = Derivation(set(sysm.all_axioms()))
    units: dict[int, int] = {}  # var id -> line index of (var + true value)

    # seed
    units[sysm.idx[(0, 0)]] = D.axiom(sysm.seed_axiom)

    for cell, ax in sysm.cell_axioms:
        v = sysm.idx[cell]
        cur = D.axiom(ax)
        # eliminate every monomial of degree >= 2 (all involve parents only)
        while True:
            hi = [m for m in D.lines[cur] if len(m) >= 2]
            if not hi:
                break
            m = max(hi, key=lambda mm: (len(mm), sorted(mm)))
            u = min(m)
            rest = sorted(m - {u})
            t = units[u]
            for x in rest:
                t = D.mul(t, x)          # U_u * prod(rest) = m + b_u*(m\{u})
            cur = D.add(cur, t)
        # eliminate remaining degree-1 monomials other than the cell's own var
        while True:
            lo = [m for m in D.lines[cur] if len(m) == 1 and next(iter(m)) != v]
            if not lo:
                break
            p = next(iter(lo[0]))
            cur = D.add(cur, units[p])
        units[v] = cur

    target_line = units[sysm.idx[(sysm.n, 0)]]
    neg = D.axiom(sysm.neg_axiom)
    D.add(target_line, neg)
    return D


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ns", type=int, nargs="+", default=[4, 8, 16, 32, 64])
    ap.add_argument("--rules", type=int, nargs="+", default=[30, 90, 160, 128])
    ap.add_argument("--out", default="certificate.json")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    log = logging.getLogger("cert")
    out = []
    for rule in args.rules:
        log.info("")
        log.info("rule %d   explicit PC refutation, EVERY line independently re-checked", rule)
        log.info("%6s %7s %9s %9s %8s %9s", "n", "vars", "lines", "maxdeg", "secs", "lines/n^2")
        for n in args.ns:
            s = System(n, rule)
            md = s.max_axiom_degree()
            t0 = time.time()
            D = refute(s)
            nl, obs = D.check(ONE, md)
            dt = time.time() - t0
            # extra soundness check: every line vanishes under the true assignment
            # EXCEPT those depending on the negation unit (only the last add).
            a = s.assignment()
            bad = [k for k in range(nl - 2) if peval(D.lines[k], a) != 0]
            assert not bad, f"unsound line(s) {bad[:5]}"
            out.append(
                {"rule": rule, "n": n, "nvars": s.nvars, "lines": nl,
                 "max_degree": obs, "claimed_degree": md, "secs": round(dt, 2)}
            )
            log.info("%6d %7d %9d %9d %8.2f %9.4f", n, s.nvars, nl, obs, dt, nl / (n * n))
    with open(args.out, "w") as f:
        json.dump(out, f, indent=1)
    log.info("")
    log.info("wrote %s", args.out)


if __name__ == "__main__":
    main()

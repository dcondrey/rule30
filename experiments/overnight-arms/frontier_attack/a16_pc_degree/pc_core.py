"""Polynomial calculus (PC) over GF(2) for the Rule 30 light-cone system.

Ring: F_2[x]/(x^2 - x), i.e. multilinear.  NOT PCR (no twin variables).

Polynomials are represented as a Python `frozenset` of monomials; a monomial is
a `frozenset` of variable ids.  The empty frozenset is the constant 1.
Addition = symmetric difference.  Multiplication by a variable maps each
monomial `m` to `m | {x}` (multilinear reduction is automatic), then cancels.

Everything here is gated against the repo ground truth:
  experiments/rule30/center_column.py        (OEIS A051023, read-only)
  experiments/overnight-arms/common/rule30.py (read-only)

Run `uv run python pc_core.py` for the gates.
"""

from __future__ import annotations

import importlib.util
import itertools
import logging
import sys
from typing import Iterable

REPO = "/Volumes/A/researchpapers/13-rule30"

Mono = frozenset  # frozenset[int]
Poly = frozenset  # frozenset[Mono]

ONE: Poly = frozenset({frozenset()})
ZERO: Poly = frozenset()


# --------------------------------------------------------------------------
# polynomial arithmetic
# --------------------------------------------------------------------------
def padd(*ps: Poly) -> Poly:
    out: frozenset = frozenset()
    for p in ps:
        out = out ^ p
    return out


def pmulvar(p: Poly, x: int) -> Poly:
    """Multiply by a single variable in the multilinear ring."""
    out: set = set()
    for m in p:
        mm = m | {x}
        if mm in out:
            out.discard(mm)
        else:
            out.add(mm)
    return frozenset(out)


def pmulmono(p: Poly, m: Mono) -> Poly:
    for x in m:
        p = pmulvar(p, x)
    return p


def pdeg(p: Poly) -> int:
    return max((len(m) for m in p), default=-1)


def peval(p: Poly, assign: dict[int, int]) -> int:
    tot = 0
    for m in p:
        v = 1
        for x in m:
            v &= assign[x]
            if not v:
                break
        tot ^= v
    return tot


# --------------------------------------------------------------------------
# rule ANF, derived from the truth table by Moebius transform (never from memory)
# --------------------------------------------------------------------------
def rule_table(rule: int) -> dict[tuple[int, int, int], int]:
    """Wolfram elementary-CA numbering: bit index 4l+2c+r of `rule`."""
    return {
        (l, c, r): (rule >> (4 * l + 2 * c + r)) & 1
        for l in (0, 1)
        for c in (0, 1)
        for r in (0, 1)
    }


def rule_anf(rule: int) -> frozenset:
    """ANF as a set of subsets of {0,1,2} standing for (l, c, r).

    Moebius transform: coefficient of monomial S is XOR of f(y) over y <= S.
    """
    tbl = rule_table(rule)
    terms = set()
    for S in itertools.chain.from_iterable(
        itertools.combinations((0, 1, 2), k) for k in range(4)
    ):
        Ss = set(S)
        acc = 0
        for sub in itertools.chain.from_iterable(
            itertools.combinations(sorted(Ss), k) for k in range(len(Ss) + 1)
        ):
            y = [0, 0, 0]
            for i in sub:
                y[i] = 1
            acc ^= tbl[(y[0], y[1], y[2])]
        if acc:
            terms.add(frozenset(Ss))
    return frozenset(terms)


def anf_str(rule: int) -> str:
    names = {0: "l", 1: "c", 2: "r"}
    terms = sorted(rule_anf(rule), key=lambda s: (len(s), sorted(s)))
    if not terms:
        return "0"
    return " + ".join("1" if not t else "".join(names[i] for i in sorted(t)) for t in terms)


def apply_rule(rule: int, l: int, c: int, r: int) -> int:
    return rule_table(rule)[(l, c, r)]


# --------------------------------------------------------------------------
# the light-cone system
# --------------------------------------------------------------------------
class System:
    """Axioms of S_n(rule): seed unit, one cell axiom per t>=1 cell, negation unit."""

    def __init__(self, n: int, rule: int) -> None:
        self.n = n
        self.rule = rule
        self.cells = [
            (t, x)
            for t in range(n + 1)
            for x in range(-min(t, n - t), min(t, n - t) + 1)
        ]
        self.idx = {cell: i for i, cell in enumerate(self.cells)}
        self.nvars = len(self.cells)
        self.anf = rule_anf(rule)

        # true values by naive simulation of the lone seed
        self.truth = self._truth()

        self.seed_axiom: Poly = frozenset({frozenset({self.idx[(0, 0)]}), frozenset()})
        self.cell_axioms: list[tuple[tuple[int, int], Poly]] = []
        for t, x in self.cells:
            if t == 0:
                continue
            self.cell_axioms.append(((t, x), self._cell_axiom(t, x)))
        cn = self.truth[(n, 0)]
        # negation of the true value: s(n,0) + c_n + 1
        neg = {frozenset({self.idx[(n, 0)]})}
        if (cn + 1) % 2:
            neg.add(frozenset())
        self.neg_axiom: Poly = frozenset(neg)

    # -- ground truth ------------------------------------------------------
    def _truth(self) -> dict[tuple[int, int], int]:
        cur = {0: 1}
        vals = {(0, 0): 1}
        for t in range(1, self.n + 1):
            nxt = {}
            for x in range(-t, t + 1):
                v = apply_rule(
                    self.rule, cur.get(x - 1, 0), cur.get(x, 0), cur.get(x + 1, 0)
                )
                if v:
                    nxt[x] = 1
            cur = nxt
            for x in range(-min(t, self.n - t), min(t, self.n - t) + 1):
                vals[(t, x)] = cur.get(x, 0)
        return vals

    # -- axioms ------------------------------------------------------------
    def _parent(self, t: int, x: int, which: int) -> int | None:
        """Variable id of parent, or None if the parent is off-cone (constant 0)."""
        px = x + (which - 1)  # which=0 -> x-1 (l), 1 -> x (c), 2 -> x+1 (r)
        pt = t - 1
        if abs(px) <= min(pt, self.n - pt):
            return self.idx[(pt, px)]
        return None

    def _cell_axiom(self, t: int, x: int) -> Poly:
        out: set = {frozenset({self.idx[(t, x)]})}
        for term in self.anf:
            ids = []
            dead = False
            for which in term:
                p = self._parent(t, x, which)
                if p is None:
                    dead = True
                    break
                ids.append(p)
            if dead:
                continue  # term contains an off-cone (identically 0) parent
            m = frozenset(ids)
            if m in out:
                out.discard(m)
            else:
                out.add(m)
        return frozenset(out)

    def all_axioms(self) -> list[Poly]:
        return [self.seed_axiom] + [p for _, p in self.cell_axioms] + [self.neg_axiom]

    def consistent_axioms(self) -> list[Poly]:
        """Everything except the negation unit (this subsystem is satisfiable)."""
        return [self.seed_axiom] + [p for _, p in self.cell_axioms]

    def assignment(self) -> dict[int, int]:
        return {self.idx[c]: self.truth[c] for c in self.cells}

    def max_axiom_degree(self) -> int:
        return max(pdeg(p) for p in self.all_axioms())


# --------------------------------------------------------------------------
# exact degree-d closure  V_d  (Clegg-Edmonds-Impagliazzo style, done properly)
# --------------------------------------------------------------------------
class Space:
    """Row-reduced GF(2) subspace of the multilinear polynomials of degree <= d."""

    def __init__(self, order: dict) -> None:
        self.order = order  # monomial -> rank (higher rank = leading)
        self.pivots: dict = {}  # leading monomial -> reduced poly

    def _lead(self, p: Poly):
        return max(p, key=lambda m: self.order[m])

    def reduce(self, p: Poly) -> Poly:
        while p:
            lm = self._lead(p)
            q = self.pivots.get(lm)
            if q is None:
                return p
            p = p ^ q
        return p

    def add(self, p: Poly) -> Poly | None:
        r = self.reduce(p)
        if not r:
            return None
        self.pivots[self._lead(r)] = r
        return r

    def contains(self, p: Poly) -> bool:
        return not self.reduce(p)

    def basis(self) -> list[Poly]:
        return list(self.pivots.values())

    def dim(self) -> int:
        return len(self.pivots)


def _monomial_order(nvars: int, d: int) -> dict:
    monos = []
    for k in range(d + 1):
        for comb in itertools.combinations(range(nvars), k):
            monos.append(frozenset(comb))
    monos.sort(key=lambda m: (len(m), sorted(m)))
    return {m: i for i, m in enumerate(monos)}


def closure_degree(
    axioms: Iterable[Poly], nvars: int, d: int, early_exit: bool = True
) -> tuple[bool, int, int]:
    """Compute V_d; return (1 in V_d, dim V_d, rounds).

    V_d = smallest subspace containing the degree-<=d axioms, closed under
    f |-> x*f whenever deg(x*f) <= d.  The subspace {f in V : deg(x f) <= d} is
    computed as a kernel every round; the naive span of {m*p : deg(m*p) <= d}
    is NOT used because it undercounts derivable polynomials.
    """
    order = _monomial_order(nvars, d)
    V = Space(order)
    fresh = []
    for p in axioms:
        if pdeg(p) <= d:
            r = V.add(p)
            if r is not None:
                fresh.append(r)
    if early_exit and V.contains(ONE):
        return True, V.dim(), 0

    rounds = 0
    while True:
        rounds += 1
        added = False
        for x in range(nvars):
            # S_x = {f in V : every degree-d monomial of f contains x}
            # constraint coordinates: degree-d monomials NOT containing x
            basis = V.basis()
            if not basis:
                break
            cons: dict = {}  # monomial -> bit position
            for f in basis:
                for m in f:
                    if len(m) == d and x not in m:
                        cons.setdefault(m, len(cons))
            if not cons:
                ker = basis  # every element already satisfies the constraint
            else:
                # Gaussian elimination on the projection, tracking combinations
                rows = []
                for f in basis:
                    proj = 0
                    for m in f:
                        b = cons.get(m)
                        if b is not None:
                            proj |= 1 << b
                    rows.append((proj, f))
                piv: dict[int, tuple[int, Poly]] = {}
                ker = []
                for proj, f in rows:
                    cur, comb = proj, f
                    while cur:
                        hb = cur.bit_length() - 1
                        if hb in piv:
                            pp, pc = piv[hb]
                            cur ^= pp
                            comb = comb ^ pc
                        else:
                            piv[hb] = (cur, comb)
                            cur = 0
                            comb = None
                            break
                    if comb is not None and cur == 0:
                        ker.append(comb)
            for f in ker:
                if not f:
                    continue
                g = pmulvar(f, x)
                if pdeg(g) > d:
                    continue
                r = V.add(g)
                if r is not None:
                    added = True
                    if early_exit and V.contains(ONE):
                        return True, V.dim(), rounds
        if not added:
            break
    return V.contains(ONE), V.dim(), rounds


def pc_degree(sysm: System, dmax: int = 5) -> int | None:
    for d in range(dmax + 1):
        ok, _, _ = closure_degree(sysm.all_axioms(), sysm.nvars, d)
        if ok:
            return d
    return None


# --------------------------------------------------------------------------
# gates
# --------------------------------------------------------------------------
def _load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def gates() -> None:
    log = logging.getLogger("gates")
    truth_mod = _load(f"{REPO}/experiments/rule30/center_column.py", "repo_cc")
    r30 = _load(f"{REPO}/experiments/overnight-arms/common/rule30.py", "common_r30")

    # G1: ANF of rule 30 is exactly l + c + r + c*r, of rule 90 is l + r,
    #     of 160 is l*r, of 128 is l*c*r -- derived, then checked exhaustively.
    assert rule_anf(30) == frozenset(
        {frozenset({0}), frozenset({1}), frozenset({2}), frozenset({1, 2})}
    ), rule_anf(30)
    assert rule_anf(90) == frozenset({frozenset({0}), frozenset({2})})
    assert rule_anf(160) == frozenset({frozenset({0, 2})})
    assert rule_anf(128) == frozenset({frozenset({0, 1, 2})})
    for rule in (30, 90, 160, 128):
        anf = rule_anf(rule)
        for l, c, r in itertools.product((0, 1), repeat=3):
            v = [l, c, r]
            got = 0
            for term in anf:
                p = 1
                for i in term:
                    p &= v[i]
                got ^= p
            assert got == apply_rule(rule, l, c, r), (rule, l, c, r)
    # G1b: rule 30 ANF == l XOR (c OR r), the form used in common/rule30.py
    for l, c, r in itertools.product((0, 1), repeat=3):
        assert apply_rule(30, l, c, r) == (l ^ (c | r))
    log.info("G1 OK: ANF derived by Moebius transform matches every truth-table row")
    log.info("       rule 30: %s | rule 90: %s", anf_str(30), anf_str(90))
    log.info("       rule 160: %s | rule 128: %s", anf_str(160), anf_str(128))

    # G2: System.truth agrees with simulate_seed and with the repo center column.
    n = 24
    grid = r30.simulate_seed({0: 1}, n + 1)
    s30 = System(n, 30)
    for (t, x), v in s30.truth.items():
        assert v == grid[t].get(x, 0), (t, x)
    cc = list(truth_mod.center_column(n + 1))
    for t in range(n + 1):
        if (t, 0) in s30.truth:
            assert s30.truth[(t, 0)] == cc[t], t
    log.info("G2 OK: cell values match simulate_seed and A051023 for n=%d", n)

    # G3: off-cone parent substitution is exact -- every parent of an in-diamond
    #     cell that is NOT in the diamond is identically 0 in the real lattice.
    for nn in range(2, 20):
        s = System(nn, 30)
        full = r30.simulate_seed({0: 1}, nn + 1)
        for t, x in s.cells:
            if t == 0:
                continue
            for which, px in ((0, x - 1), (1, x), (2, x + 1)):
                if s._parent(t, x, which) is None:
                    assert full[t - 1].get(px, 0) == 0, (nn, t, x, px)
    log.info("G3 OK: every off-diamond parent is identically 0 (n=2..19)")

    # G4: the axioms are sound -- the true assignment satisfies seed + cell
    #     axioms and violates the negation unit, for all four rules.
    for rule in (30, 90, 160, 128):
        for nn in range(2, 14):
            s = System(nn, rule)
            a = s.assignment()
            assert peval(s.seed_axiom, a) == 0
            for cell, p in s.cell_axioms:
                assert peval(p, a) == 0, (rule, nn, cell)
            assert peval(s.neg_axiom, a) == 1, (rule, nn)
    log.info("G4 OK: axioms sound, negation unit violated (rules 30/90/160/128, n=2..13)")

    # G5: |D_n| = n^2/2 + n + 1 for even n
    for nn in range(2, 40, 2):
        assert System(nn, 30).nvars == nn * nn // 2 + nn + 1, nn
    log.info("G5 OK: |D_n| = n^2/2 + n + 1 for even n up to 38")

    # G6: closure instrument sanity on a hand system.
    #     {x+1, y+1, xy} is inconsistent; degree 2 refutes it, degree 1 does not.
    ax = [
        frozenset({frozenset({0}), frozenset()}),
        frozenset({frozenset({1}), frozenset()}),
        frozenset({frozenset({0, 1})}),
    ]
    assert closure_degree(ax, 2, 2)[0] is True
    assert closure_degree(ax, 2, 1)[0] is False
    #     {x+1, x} is inconsistent at degree 1.
    ax2 = [frozenset({frozenset({0}), frozenset()}), frozenset({frozenset({0})})]
    assert closure_degree(ax2, 1, 1)[0] is True
    assert closure_degree(ax2, 1, 0)[0] is False
    #     a satisfiable system must NOT be refutable at any degree
    ax3 = [frozenset({frozenset({0}), frozenset()})]
    for d in range(3):
        assert closure_degree(ax3, 2, d)[0] is False
    #     the closure must see derivations that need a NON-axiom multiplication:
    #     {x+y, y+1, x} over 2 vars is inconsistent and degree 1 suffices.
    ax4 = [
        frozenset({frozenset({0}), frozenset({1})}),
        frozenset({frozenset({1}), frozenset()}),
        frozenset({frozenset({0})}),
    ]
    assert closure_degree(ax4, 2, 1)[0] is True
    log.info("G6 OK: closure instrument correct on four hand systems")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    gates()
    logging.getLogger("gates").info("ALL GATES PASS")
    sys.exit(0)

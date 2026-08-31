"""R9 / arm A13 (UPPER bound): light-cone CNF, a machine-checked resolution
checker, and three candidate derivation families for the centre unit c_n.

Everything here is mechanical.  No asymptotic claim is made in this file; it
only builds derivations, verifies EVERY resolution step, and counts them.

Encoding (identical convention to experiments/rule30/proof-complexity/
mus_probe.py and to the sibling arm a4_p3_resolution/derivation_upper_bound.py,
so the numbers compose):

  variables: one per cell of D_n = {(t,x) : |x| <= min(t, n-t)}, the backward
             diamond of (n,0) intersected with the forward light cone of the
             lone seed.
  axioms:    unit {s(0,0)} for the seed; for every cell with t >= 1 the full
             truth-table clause set over its IN-DIAMOND parents.  Parents
             outside the diamond lie outside the forward light cone, so they
             are identically 0 and are substituted as constants (this is exact,
             not an assumption; it is checked in gate_encoding()).
  target:    the unit clause asserting the true value of s(n,0).

Ground truth: experiments/rule30/center_column.py (OEIS A051023 gated) and
experiments/overnight-arms/common/rule30.py, both imported read-only.

Run the gates:
    /Volumes/A/researchpapers/.venv/bin/python p3_core.py
"""

from __future__ import annotations

import importlib.util
import logging

REPO = "/Volumes/A/researchpapers/13-rule30"

# rule -> (indices of (left, centre, right) actually read, transition function)
RULES = {
    30: ((0, 1, 2), lambda a, b, c: a ^ (b | c)),
    90: ((0, 2), lambda a, b, c: a ^ c),
}


# --------------------------------------------------------------------------
# geometry, simulation, encoding
# --------------------------------------------------------------------------
def simulate(rule: int, n: int) -> dict[tuple[int, int], int]:
    """Full light-cone truth values s(t,x) for t <= n, |x| <= t."""
    _, f = RULES[rule]
    cells = {(0, 0): 1}
    row = {0: 1}
    for t in range(1, n + 1):
        new = {}
        for x in range(-t, t + 1):
            v = f(row.get(x - 1, 0), row.get(x, 0), row.get(x + 1, 0))
            new[x] = v
            cells[(t, x)] = v
        row = new
    return cells


def diamond(n: int) -> list[tuple[int, int]]:
    return [
        (t, x)
        for t in range(n + 1)
        for x in range(-min(t, n - t), min(t, n - t) + 1)
    ]


class Instance:
    """The light-cone CNF for one (rule, n)."""

    def __init__(self, rule: int, n: int) -> None:
        self.rule = rule
        self.n = n
        self.reads, self.f = RULES[rule]
        self.truth = simulate(rule, n)
        self.cone = diamond(n)
        self.var = {c: i + 1 for i, c in enumerate(self.cone)}
        self.axioms: list[frozenset[int]] = [frozenset({self.var[(0, 0)]})]
        # per-cell axiom block: cell -> list of axiom indices
        self.cell_axioms: dict[tuple[int, int], list[int]] = {}
        for (t, x) in self.cone:
            if t == 0:
                continue
            idx = self.read_parents(t, x)
            block = []
            for m in range(1 << len(idx)):
                asn = [0, 0, 0]
                for j, i in enumerate(idx):
                    asn[i] = (m >> j) & 1
                out = self.f(*asn)
                pv = self.parent_vars(t, x)
                lits = [-pv[i] if asn[i] else pv[i] for i in idx]
                lits.append(self.var[(t, x)] if out else -self.var[(t, x)])
                block.append(len(self.axioms))
                self.axioms.append(frozenset(lits))
            self.cell_axioms[(t, x)] = block

    def parent_vars(self, t: int, x: int) -> list[int | None]:
        ps = [(t - 1, x - 1), (t - 1, x), (t - 1, x + 1)]
        return [self.var.get(p) for p in ps]

    def read_parents(self, t: int, x: int) -> list[int]:
        """Indices in {0,1,2} of parents this rule reads AND that are variables."""
        pv = self.parent_vars(t, x)
        return [i for i in self.reads if pv[i] is not None]

    def lit(self, cell: tuple[int, int]) -> int:
        """The literal that is TRUE under the (unique) real assignment."""
        v = self.var[cell]
        return v if self.truth[cell] else -v

    def target(self) -> frozenset[int]:
        return frozenset({self.lit((self.n, 0))})


# --------------------------------------------------------------------------
# resolution proof object + checker
# --------------------------------------------------------------------------
class Proof:
    """A resolution derivation.  Length = number of resolution STEPS."""

    def __init__(self, inst: Instance) -> None:
        self.inst = inst
        self.clauses: list[frozenset[int]] = list(inst.axioms)
        self.n_axioms = len(self.clauses)
        self.steps: list[tuple[int, int, int]] = []  # (i, j, pivot)
        self.index: dict[frozenset[int], int] = {}
        for i, c in enumerate(self.clauses):
            self.index.setdefault(c, i)

    def resolve(self, i: int, j: int, pivot: int) -> int:
        c1, c2 = self.clauses[i], self.clauses[j]
        if pivot in c2 and -pivot in c1:
            i, j = j, i
            c1, c2 = c2, c1
        assert pivot in c1 and -pivot in c2, "bad pivot orientation"
        res = frozenset((c1 - {pivot}) | (c2 - {-pivot}))
        assert not any(-l in res for l in res), "tautological resolvent"
        self.clauses.append(res)
        self.steps.append((i, j, pivot))
        k = len(self.clauses) - 1
        self.index.setdefault(res, k)
        return k

    @property
    def length(self) -> int:
        return len(self.steps)

    def check(self, final: frozenset[int]) -> None:
        """Re-verify every step from scratch and that `final` is derived."""
        cl = list(self.inst.axioms)
        assert self.clauses[: len(cl)] == cl, "axiom prefix corrupted"
        for (i, j, p) in self.steps:
            assert 0 <= i < len(cl) and 0 <= j < len(cl), "forward reference"
            c1, c2 = cl[i], cl[j]
            assert p in c1 and -p in c2, "not a legal resolution step"
            res = frozenset((c1 - {p}) | (c2 - {-p}))
            assert not any(-l in res for l in res), "tautological resolvent"
            cl.append(res)
        assert cl == self.clauses, "replay mismatch"
        assert final in cl, "target clause not derived"


# --------------------------------------------------------------------------
# helper: specialise a cell's axiom block to a chosen antecedent subset
# --------------------------------------------------------------------------
def firing_clause(pf: Proof, t: int, x: int, keep: list[int]) -> int:
    """Index of the clause  {~lit(p) : p in keep} u {lit(t,x)}.

    `keep` must be a subset of the cell's read, in-diamond parent indices whose
    true values already determine the child.  If it is a proper subset, the
    clause is DERIVED from the axiom block by resolving the dropped parent
    variables away, and those resolution steps are counted.
    """
    inst = pf.inst
    idx = inst.read_parents(t, x)
    pv = inst.parent_vars(t, x)
    drop = [i for i in idx if i not in keep]
    want = frozenset(
        [-pv[i] if inst.truth[(t - 1, x - 1 + i)] else pv[i] for i in keep]
        + [inst.lit((t, x))]
    )
    if not drop:
        return pf.index[want]
    if want in pf.index:
        return pf.index[want]
    # eliminate dropped variables one at a time from the sub-block of axioms
    # that agree with the true values on `keep`.
    live = []
    for a in inst.cell_axioms[(t, x)]:
        c = pf.clauses[a]
        ok = all(
            (-pv[i] if inst.truth[(t - 1, x - 1 + i)] else pv[i]) in c for i in keep
        )
        if ok:
            live.append(a)
    for i in drop:
        v = pv[i]
        nxt = []
        pos = [a for a in live if v in pf.clauses[a]]
        neg = [a for a in live if -v in pf.clauses[a]]
        for a in pos:
            for b in neg:
                r = frozenset((pf.clauses[a] - {v}) | (pf.clauses[b] - {-v}))
                if any(-l in r for l in r):
                    continue
                nxt.append(pf.resolve(a, b, v))
        live = nxt
    hit = [a for a in live if pf.clauses[a] == want]
    assert hit, "specialisation failed to produce the wanted clause"
    return hit[0]


# --------------------------------------------------------------------------
# candidate derivation families
# --------------------------------------------------------------------------
def derive_full(rule: int, n: int) -> tuple[Proof, dict]:
    """FAMILY 0 (baseline): row simulation.  Derive the unit of every diamond
    cell in topological order, using all read parents."""
    inst = Instance(rule, n)
    pf = Proof(inst)
    unit = {(0, 0): 0}
    for (t, x) in inst.cone:
        if t == 0:
            continue
        idx = inst.read_parents(t, x)
        cur = firing_clause(pf, t, x, idx)
        for i in idx:
            p = (t - 1, x - 1 + i)
            cur = pf.resolve(cur, unit[p], -inst.lit(p))
        unit[(t, x)] = cur
    return pf, {"cells_derived": len(unit)}


def required_parents(inst: Instance, t: int, x: int, policy: str) -> list[int]:
    """Smallest antecedent set that already determines s(t,x), given the true
    values.  For rule 30 the OR latch lets one parent be dropped whenever the
    OR evaluates to 1."""
    idx = inst.read_parents(t, x)
    if inst.rule == 90:
        return idx
    val = lambda i: inst.truth[(t - 1, x - 1 + i)]  # noqa: E731
    keep = [i for i in idx if i == 0]  # left parent is always needed (XOR)
    m_in, r_in = 1 in idx, 2 in idx
    m = val(1) if m_in else 0
    r = val(2) if r_in else 0
    if m == 1 and (policy in ("centre", "greedy")):
        keep += [1] if m_in else []
    elif r == 1 and (policy in ("right", "greedy", "centre")):
        keep += [2] if r_in else []
    elif m == 1:
        keep += [1] if m_in else []
    else:
        keep += [i for i in (1, 2) if i in idx]
    return sorted(keep)


def backward_slice(rule: int, n: int, policy: str = "greedy") -> set:
    """Cells whose unit clause the sliced derivation actually derives."""
    inst = Instance(rule, n)
    need = {(n, 0)}
    for t in range(n, 0, -1):
        layer = [c for c in need if c[0] == t]
        for (tt, x) in layer:
            for i in required_parents(inst, tt, x, policy):
                need.add((tt - 1, x - 1 + i))
    return need


def derive_sliced(rule: int, n: int, policy: str = "greedy") -> tuple[Proof, dict]:
    """FAMILY 1: keep the row-simulation shape but derive only the units in the
    backward slice, and use the smallest sufficient antecedent set per cell."""
    inst = Instance(rule, n)
    need = backward_slice(rule, n, policy)
    pf = Proof(inst)
    unit = {(0, 0): 0}
    for (t, x) in inst.cone:
        if t == 0 or (t, x) not in need:
            continue
        keep = required_parents(inst, t, x, policy)
        cur = firing_clause(pf, t, x, keep)
        for i in keep:
            p = (t - 1, x - 1 + i)
            cur = pf.resolve(cur, unit[p], -inst.lit(p))
        unit[(t, x)] = cur
    return pf, {"cells_derived": len(unit), "slice": len(need)}


def derive_backward(rule: int, n: int, sliced: bool = False) -> tuple[Proof, dict]:
    """FAMILY 3/4: backward elimination (input-resolution chain).

    Found by the exact minimum-tree-length search at n=2,3 (p3_minlength.py):
    derive NO intermediate unit at all.  Start from the target cell's firing
    clause and resolve each ancestor variable away against that ancestor's own
    firing clause, deepest first, ending on a clause over the seed alone.
    Exactly one elimination step per ancestor cell (plus one specialisation
    step per cell whose antecedent set is cut, when sliced=True).
    """
    inst = Instance(rule, n)
    pf = Proof(inst)
    policy = "greedy"

    def keep_of(t: int, x: int) -> list[int]:
        return (
            required_parents(inst, t, x, policy)
            if sliced
            else inst.read_parents(t, x)
        )

    tgt_cell = (n, 0)
    cur = firing_clause(pf, n, 0, keep_of(n, 0))
    eliminated = 0
    while True:
        cells = [
            inst.cone[abs(l) - 1]
            for l in pf.clauses[cur]
            if inst.cone[abs(l) - 1] != tgt_cell
        ]
        cells = [c for c in cells if c != (0, 0)]
        if not cells:
            break
        t, x = max(cells)
        sub = firing_clause(pf, t, x, keep_of(t, x))
        cur = pf.resolve(cur, sub, -inst.lit((t, x)))
        eliminated += 1
    if inst.var[(0, 0)] in {abs(l) for l in pf.clauses[cur]}:
        cur = pf.resolve(cur, 0, -inst.lit((0, 0)))
        eliminated += 1
    assert pf.clauses[cur] == inst.target(), "backward chain did not reach the unit"
    return pf, {"eliminated": eliminated, "sliced": sliced}


def derive_kstep(rule: int, n: int, k: int) -> tuple[Proof, dict]:
    """FAMILY 2 (the block-doubling story, actually built): derive units only on
    rows that are multiples of k.  For each such target the k-step "composed
    rule" clause over its row-(t-k) ancestors is DERIVED from the one-step
    axioms by resolving every intermediate cell variable away, and every one of
    those steps is counted."""
    inst = Instance(rule, n)
    pf = Proof(inst)
    unit = {(0, 0): 0}
    rows = list(range(0, n + 1, k))
    if rows[-1] != n:
        rows.append(n)
    for ri in range(1, len(rows)):
        t1, t0 = rows[ri], rows[ri - 1]
        d = t1 - t0
        for x in range(-min(t1, n - t1), min(t1, n - t1) + 1):
            # backward cone of (t1,x) down to row t0, restricted to the diamond
            cur = _compose(pf, t1, x, t0, d)
            # resolve away every row-t0 ancestor literal using its unit
            for p in sorted(_ancestors(inst, t1, x, t0)):
                if -inst.lit(p) in pf.clauses[cur]:
                    cur = pf.resolve(cur, unit[p], -inst.lit(p))
            unit[(t1, x)] = cur
            assert pf.clauses[cur] == frozenset({inst.lit((t1, x))}), "not a unit"
    return pf, {"cells_derived": len(unit), "k": k}


def _ancestors(inst: Instance, t: int, x: int, t0: int) -> set:
    cur = {(t, x)}
    while cur and max(c[0] for c in cur) > t0:
        nxt = set()
        for (a, b) in cur:
            if a == t0:
                nxt.add((a, b))
                continue
            # a cell with no in-diamond read parents has a UNIT axiom: its value
            # is already fixed by the off-cone zeros, so it is not an ancestor
            # of the composed clause.
            for i in inst.read_parents(a, b):
                nxt.add((a - 1, b - 1 + i))
        cur = nxt
    return {c for c in cur if c[0] == t0}


def _compose(pf: Proof, t: int, x: int, t0: int, d: int) -> int:
    """Derive {~lit(a) : a in row-t0 ancestors} u {lit(t,x)} from the one-step
    axioms by eliminating all intermediate cell variables."""
    inst = pf.inst
    idx = inst.read_parents(t, x)
    cur = firing_clause(pf, t, x, idx)
    # eliminate intermediates layer by layer, deepest first
    for tt in range(t - 1, t0, -1):
        while True:
            elim = [
                v
                for l in pf.clauses[cur]
                for v in [abs(l)]
                if inst.cone[v - 1][0] == tt
            ]
            if not elim:
                break
            v = elim[0]
            cell = inst.cone[v - 1]
            sub = firing_clause(pf, cell[0], cell[1], inst.read_parents(*cell))
            cur = pf.resolve(cur, sub, -inst.lit(cell))
    return cur


# --------------------------------------------------------------------------
# gates
# --------------------------------------------------------------------------
def _load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def gate_ground_truth(n: int = 512) -> list[int]:
    """Centre column from the OEIS-gated repo generator, cross-checked against
    the overnight-arms substrate and against this file's own simulate()."""
    gt = _load(f"{REPO}/experiments/rule30/center_column.py", "gt")
    sub = _load(f"{REPO}/experiments/overnight-arms/common/rule30.py", "sub")
    a = list(gt.center_column(n))
    b = sub.center_column_bits(n)
    assert a == b, "repo ground truth disagrees with overnight-arms substrate"
    cells = simulate(30, n)
    c = [cells[(t, 0)] for t in range(n)]
    assert a == c, "p3_core.simulate disagrees with repo ground truth"
    return a


def gate_encoding(rule: int, n: int) -> None:
    """The CNF has the true diagram as a model, and the off-diamond-parent
    substitution is exact."""
    inst = Instance(rule, n)
    assign = {inst.var[c]: inst.truth[c] for c in inst.cone}
    for cl in inst.axioms:
        assert any(
            (assign[abs(l)] == 1) if l > 0 else (assign[abs(l)] == 0) for l in cl
        ), "true diagram falsifies an axiom"
    for (t, x) in inst.cone:
        if t == 0:
            continue
        for i, p in enumerate([(t - 1, x - 1), (t - 1, x), (t - 1, x + 1)]):
            if p not in inst.var and i in inst.reads:
                assert abs(p[1]) > p[0] or p[0] < 0, "dropped an in-cone parent"
                assert inst.truth.get(p, 0) == 0, "dropped a nonzero parent"


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    col = gate_ground_truth(512)
    logging.info("GATE ok: centre column matches repo ground truth to n=512")
    logging.info("prefix: %s", "".join(map(str, col[:40])))
    for rule in (30, 90):
        for n in (4, 8, 16, 32):
            gate_encoding(rule, n)
    logging.info("GATE ok: encoding sound and off-cone substitution exact")
    for rule in (30, 90):
        for n in (4, 8, 16):
            pf, meta = derive_full(rule, n)
            pf.check(Instance(rule, n).target())
            logging.info(
                "rule %d n=%-3d baseline steps=%-6d %s", rule, n, pf.length, meta
            )

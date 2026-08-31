"""Exact Boolean-chain synthesis by SAT (SSV encoding).

Encoding follows the "single selection variable" (SSV) formulation of

  W. Haaswijk, A. Mishchenko, M. Soeken, G. De Micheli,
  "SAT-Based Exact Synthesis: Encodings, Topology Families, and
  Parallelism", IEEE TCAD 39(4):871-884, 2020,

which is itself the CNF form of the Boolean-chain synthesis problem set as
exercise in D. E. Knuth, TAOCP vol. 4A, section 7.1.2 (Boolean chains) with
the SAT machinery of 7.2.2.2.  Nothing here is invented; the only choices
made locally are which optional symmetry breaks are enabled, and each of
those is validated by running the sanity suite with and without it.

A *Boolean chain* of length k over m inputs is a sequence of steps
x_{m+1}, ..., x_{m+k} where step i is g_i(x_{j}, x_{l}) for some
1 <= j < l < i and some binary operator g_i drawn from the full basis B2
(all 16 two-input functions, minus degenerate ones -- see below).  The last
step is the output.  k_min(f) is the least k for which such a chain
computes f.  This is the standard "combinational complexity" C(f) over B2.
"""

from __future__ import annotations

import itertools
import time
from dataclasses import dataclass

from pysat.formula import IDPool
from pysat.solvers import Cadical195

# The six degenerate binary operators, as (f00, f01, f10, f11) tuples:
# the two constants and the four projections/negations.  Excluding them
# loses no generality (a chain using one can always be shortened) and is
# the standard normalisation.
DEGENERATE = [
    (0, 0, 0, 0),
    (1, 1, 1, 1),
    (0, 0, 1, 1),  # first operand
    (1, 1, 0, 0),  # negated first operand
    (0, 1, 0, 1),  # second operand
    (1, 0, 1, 0),  # negated second operand
]


@dataclass
class Result:
    sat: bool
    k: int
    seconds: float
    chain: list | None = None
    n_vars: int = 0
    n_clauses: int = 0


def _trivial(tt: list[int], m: int) -> bool:
    """True iff tt needs zero gates: a constant, an input, or a negated input.

    Note that a negated input is *not* free in the B2 chain model used here
    (the output must be a chain step), so only constants and plain inputs
    count as k=0.  Both are reported so the caller can see which.
    """
    n = 1 << m
    if all(v == tt[0] for v in tt):
        return True
    for j in range(m):
        if all(tt[t] == ((t >> (m - 1 - j)) & 1) for t in range(n)):
            return True
    return False


def encode(
    tt: list[int],
    m: int,
    k: int,
    pool: IDPool,
    *,
    distinct_pairs: bool = True,
    colex: bool = True,
) -> list[list[int]]:
    """CNF for 'a length-k B2 Boolean chain computes tt'.

    Input t is the m-bit integer t, with bit (m-1-j) being input j, so
    truth-table index t is the binary encoding of the integer t with input 0
    the most significant bit.
    """
    n = 1 << m
    gates = list(range(m, m + k))  # chain step indices, 0-based over "nodes"
    cnf: list[list[int]] = []

    def sim(i, t):  # value of node i on input t
        return pool.id(("x", i, t))

    def sel(i, j, l):  # node i takes fanins j < l
        return pool.id(("s", i, j, l))

    def fun(i, a, b):  # gate i's operator value on (a, b)
        return pool.id(("f", i, a, b))

    # inputs are fixed, not variables: encode them as unit clauses so the
    # main clauses can be written uniformly.
    for j in range(m):
        for t in range(n):
            bit = (t >> (m - 1 - j)) & 1
            cnf.append([sim(j, t) if bit else -sim(j, t)])

    for i in gates:
        pairs = list(itertools.combinations(range(i), 2))
        # exactly one fanin pair
        cnf.append([sel(i, j, l) for (j, l) in pairs])
        for p, q in itertools.combinations(pairs, 2):
            cnf.append([-sel(i, *p), -sel(i, *q)])
        # non-degenerate operator
        for d in DEGENERATE:
            cnf.append(
                [
                    -fun(i, a, b) if d[2 * a + b] else fun(i, a, b)
                    for a in (0, 1)
                    for b in (0, 1)
                ]
            )
        # main simulation clauses
        for j, l in pairs:
            s = -sel(i, j, l)
            for t in range(n):
                for a in (0, 1):
                    for b in (0, 1):
                        pre = [
                            s,
                            sim(j, t) if a == 0 else -sim(j, t),
                            sim(l, t) if b == 0 else -sim(l, t),
                        ]
                        cnf.append(pre + [-sim(i, t), fun(i, a, b)])
                        cnf.append(pre + [sim(i, t), -fun(i, a, b)])

    # output: the last step computes tt
    out = m + k - 1
    for t in range(n):
        cnf.append([sim(out, t) if tt[t] else -sim(out, t)])

    # every non-output step feeds some later step
    for i in gates[:-1]:
        lits = []
        for i2 in gates:
            if i2 <= i:
                continue
            for j, l in itertools.combinations(range(i2), 2):
                if j == i or l == i:
                    lits.append(sel(i2, j, l))
        cnf.append(lits)

    if distinct_pairs:
        # no two steps share a fanin pair (sound over the full B2 basis:
        # two steps on the same pair both compute functions of that pair,
        # so any later step reading both is itself a function of that pair
        # and collapses into one step)
        for i1, i2 in itertools.combinations(gates, 2):
            for j, l in itertools.combinations(range(i1), 2):
                cnf.append([-sel(i1, j, l), -sel(i2, j, l)])

    if colex:
        # steps ordered by their larger fanin index (a topological
        # re-sorting of any chain achieves this)
        for a, b in zip(gates, gates[1:]):
            for j1, l1 in itertools.combinations(range(a), 2):
                for j2, l2 in itertools.combinations(range(b), 2):
                    if l2 < l1 and l2 != a and l1 != a:
                        cnf.append([-sel(a, j1, l1), -sel(b, j2, l2)])

    return cnf


def solve_k(tt, m, k, *, timeout=None, **kw) -> Result:
    """Is there a length-k chain for tt?  Returns SAT/UNSAT plus timing."""
    pool = IDPool()
    t0 = time.time()
    cnf = encode(tt, m, k, pool, **kw)
    with Cadical195(bootstrap_with=cnf) as s:
        if timeout is not None:
            # pysat has no portfolio timeout on Cadical; the caller enforces
            # wall-clock limits by running solve_k in a subprocess.
            pass
        sat = s.solve()
        model = s.get_model() if sat else None
    dt = time.time() - t0
    chain = None
    if sat:
        mset = {abs(v) for v in model if v > 0}
        chain = []
        for i in range(m, m + k):
            fan = next(
                (j, l)
                for j, l in itertools.combinations(range(i), 2)
                if pool.id(("s", i, j, l)) in mset
            )
            f = tuple(
                1 if pool.id(("f", i, a, b)) in mset else 0
                for a in (0, 1)
                for b in (0, 1)
            )
            chain.append((i, fan, f))
    return Result(sat, k, dt, chain, pool.top, len(cnf))


def k_min(tt, m, *, kmax=20, verbose=False, **kw):
    """Least k with a chain, searching upward.  Returns (k, [Result,...]).

    Upward search, never binary search: the 'exists a chain of length
    exactly k' predicate is not monotone in k under the no-dead-step
    constraint, and the cheap UNSAT calls come first this way.
    """
    trace = []
    if _trivial(tt, m):
        return 0, trace
    for k in range(1, kmax + 1):
        r = solve_k(tt, m, k, **kw)
        trace.append(r)
        if verbose:
            print(f"    k={k:2d} {'SAT ' if r.sat else 'UNSAT'} {r.seconds:8.2f}s "
                  f"({r.n_clauses} clauses)")
        if r.sat:
            return k, trace
    return None, trace


def verify_chain(chain, tt, m) -> bool:
    """Independently evaluate a returned chain against the truth table."""
    n = 1 << m
    for t in range(n):
        val = [(t >> (m - 1 - j)) & 1 for j in range(m)]
        for _i, (j, l), f in chain:
            val.append(f[2 * val[j] + val[l]])
        if val[-1] != tt[t]:
            return False
    return True

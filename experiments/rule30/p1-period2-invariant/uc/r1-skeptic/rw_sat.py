#!/usr/bin/env python3
"""CNF encoding of the rotated wedge (RW) at one (n, r, c), solved with CaDiCaL.

The triangle is encoded in (h, F) coordinates with the decoupled rule of BRIEF
section 2:  a = NOT h_L AND F_L,  b = h_L XOR F_L,  h' = h XOR 1 XOR a,
F' = F XOR (h AND b), where (h_L, F_L) is the left parent (column u-1, depth d)
and (h, F) the cell below (column u, depth d).  Symbol variables s_u = H(e_u).
Constraints: T[u][n] = c for u in [n, 2n+r+1]; hard-core (s_{u-1} OR s_u) for
u >= n; 12a ending s_{2n+r-1} = 0, s_{2n+r} = 1.

`--check` validates the encoding against the census: for n in a small range it
finds by SAT the deepest k such that a run of k target cells is satisfiable
(without the 12a ending) and compares with rw_bitsliced.full_census.

`--scan` times the full RW instance for growing n to see whether SAT can reach
n beyond the bit-sliced exhaustive census.

Run:  cd experiments/rule30/p1-period2-invariant && uv run --with python-sat python uc/r1-skeptic/rw_sat.py --check
"""

from __future__ import annotations

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
KERNEL_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, KERNEL_DIR)

from pysat.solvers import Cadical153  # noqa: E402


class CNF:
    def __init__(self):
        self.nv = 0
        self.clauses = []

    def var(self) -> int:
        self.nv += 1
        return self.nv

    def const(self, value: bool) -> int:
        v = self.var()
        self.clauses.append([v] if value else [-v])
        return v

    def and2(self, x: int, y: int) -> int:
        z = self.var()
        self.clauses += [[-z, x], [-z, y], [z, -x, -y]]
        return z

    def xor2(self, x: int, y: int) -> int:
        z = self.var()
        self.clauses += [[-z, x, y], [-z, -x, -y], [z, -x, y], [z, x, -y]]
        return z


def encode(n: int, r: int, c: int, run: int | None = None, ending: bool = True) -> tuple[CNF, list[int], dict]:
    """RW instance; `run` overrides the number of constrained columns (default n+r+2)."""
    L = 2 * n + r + 2
    need = n + r + 2 if run is None else run
    cnf = CNF()
    s = [cnf.var() for _ in range(L)]
    cells: dict[tuple[int, int], tuple[int, int]] = {}
    zero = cnf.const(False)
    for u in range(L):
        top = min(u, n)
        # wedge edge and boundary cell
        cells[(u, -u - 1)] = (s[u], zero)
        nots = cnf.xor2(s[u], cnf.const(True))
        cells[(u, -u)] = (nots, zero)
        for d in range(-u, top):
            hL, FL = cells[(u - 1, d)]
            h, F = cells[(u, d)]
            a = cnf.and2(cnf.xor2(hL, cnf.const(True)), FL)  # NOT hL AND FL
            b = cnf.xor2(hL, FL)
            hn = cnf.xor2(cnf.xor2(h, a), cnf.const(True))  # h XOR a XOR 1
            Fn = cnf.xor2(F, cnf.and2(h, b))
            cells[(u, d + 1)] = (hn, Fn)
    Ec = c & 1
    for u in range(n, n + need):
        h, F = cells[(u, n)]
        cnf.clauses.append([h])
        cnf.clauses.append([F] if Ec else [-F])
        cnf.clauses.append([s[u - 1], s[u]])  # hard-core across the junction
    if ending:
        cnf.clauses.append([-s[L - 3]])
        cnf.clauses.append([s[L - 2]])
    return cnf, s, cells


def solve(cnf: CNF, timeout: float | None = None):
    with Cadical153(bootstrap_with=cnf.clauses) as slv:
        t0 = time.time()
        ok = slv.solve()
        return ok, time.time() - t0, (slv.get_model() if ok else None)


def check(min_n: int, max_n: int) -> None:
    from rw_bitsliced import full_census

    for n in range(min_n, max_n + 1):
        for c in (2, 3):
            N, *_ = full_census(n, c, 22, n + 4)
            deepest = max(k for k in range(len(N)) if N[k] > 0)
            # SAT: k = deepest must be SAT, k = deepest + 1 UNSAT (no ending)
            cnf, s, _ = encode(n, 2, c, run=deepest, ending=False)
            ok1, t1, model = solve(cnf)
            cnf2, _, _ = encode(n, 2, c, run=deepest + 1, ending=False)
            ok2, t2, _ = solve(cnf2)
            word = "".join("2" if model[v - 1] > 0 else "1" for v in s[:n]) if ok1 else ""
            print(f"n={n:<3} c={c} census deepest={deepest:<3} SAT(k=deepest)={ok1} SAT(k=deepest+1)={ok2}  times {t1:.2f}s {t2:.2f}s  witness prefix={word}")
            assert ok1 and not ok2
            sys.stdout.flush()


def scan(min_n: int, max_n: int, timeout: float) -> None:
    print(" n  r  c   vars    clauses   result   seconds")
    for n in range(min_n, max_n + 1):
        for c in (2, 3):
            for r in (0,):
                cnf, s, _ = encode(n, r, c)
                t0 = time.time()
                with Cadical153(bootstrap_with=cnf.clauses) as slv:
                    ok = slv.solve()
                    dt = time.time() - t0
                    model = slv.get_model() if ok else None
                res = "SAT  <- RW COUNTEREXAMPLE" if ok else "UNSAT"
                word = "".join("2" if model[v - 1] > 0 else "1" for v in s) if ok else ""
                print(f"{n:<3}{r:<3}{c:<4}{cnf.nv:<8}{len(cnf.clauses):<10}{res:<8} {dt:8.2f}  {word}")
                sys.stdout.flush()
                if dt > timeout:
                    print(f"stopping: {dt:.1f}s exceeds the per-instance budget {timeout}s")
                    return


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--min-n", type=int, default=8)
    ap.add_argument("--max-n", type=int, default=14)
    ap.add_argument("--timeout", type=float, default=900.0)
    args = ap.parse_args()
    if args.check:
        check(args.min_n, args.max_n)
    if args.scan:
        scan(args.min_n, args.max_n, args.timeout)


if __name__ == "__main__":
    main()

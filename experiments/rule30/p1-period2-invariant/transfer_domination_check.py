#!/usr/bin/env python3
"""Test whether the empirical 1-step transition counts over the H_r(n)
forcing recursion's survivor set are entrywise dominated by

    M = [[0, 1/4], [1/4, 1/4]]     (rows/cols indexed by state 1, state 2)

or by any uniform scalar multiple of it.

Motivation: rw_population_h.py's survival_curve found alive_after decaying
at a fitted geometric rate ~0.40 per row. M's leading eigenvalue is
(1+sqrt(5))/8 ~ 0.4045, matching that fit closely. If the *entrywise*
transition counts (not just the aggregate decay rate) are dominated by M,
that is a concrete, checkable induction-lemma candidate: it would say the
per-step survival mechanism is never more forgiving than the null model, at
every row and every n tested, not just on average.

Method: for each (n, c, r) and each row k of literal_extension's forced
continuation, look at every source word W still alive through row k-1
(prev symbol in {1,2}, no "11" so far). Classify the forced symbol at row k
as staying alive (in {1,2}, no new "11") landing in state 1 or 2, or dying
(state not in {1,2}, or a new "11"). Build the empirical count matrix
C[s][s'] = #{alive words with prev=s and next=s'} for s,s' in {1,2}, plus
the death counts, and check C[s][s'] <= M[s][s'] * N[s] at every row.
"""
from __future__ import annotations

from itertools import product

from late_pull_diagonal_sat import literal_extension

M = {(1, 1): 0.0, (1, 2): 0.25, (2, 1): 0.25, (2, 2): 0.25}


def row_transitions(n: int, tail: int, residue: int):
    """Yield, for each row k, the empirical (N[1], N[2], C[s][s'] dict)."""
    target = n + residue
    rows = target + 2
    words = list(product((1, 2), repeat=n))
    continuations = [literal_extension(w, tail, rows) for w in words]

    alive = list(range(len(words)))  # indices of still-alive words
    prev_symbol = [w[-1] for w in words]

    for k in range(rows):
        N = {1: 0, 2: 0}
        C = {(1, 1): 0, (1, 2): 0, (2, 1): 0, (2, 2): 0}
        next_alive = []
        for i in alive:
            s = prev_symbol[i]
            N[s] += 1
            nxt = continuations[i][k]
            if nxt in (1, 2) and not (s == 1 and nxt == 1):
                C[(s, nxt)] += 1
                prev_symbol[i] = nxt
                next_alive.append(i)
        yield k, N, C
        alive = next_alive
        if not alive:
            break


def check(n_values, tails, residues):
    violations = []
    checked_rows = 0
    for n in n_values:
        for tail in tails:
            for residue in residues:
                for k, N, C in row_transitions(n, tail, residue):
                    checked_rows += 1
                    for s in (1, 2):
                        for s2 in (1, 2):
                            bound = M[(s, s2)] * N[s]
                            actual = C[(s, s2)]
                            if actual > bound + 1e-9:
                                violations.append(
                                    (n, tail, residue, k, s, s2, actual, N[s], bound)
                                )
    return checked_rows, violations


def main():
    n_values = range(4, 15)
    tails = (2, 3)
    residues = (0, 1, 2)
    print(f"checking n={list(n_values)}, tails={tails}, residues={residues}", flush=True)
    checked_rows, violations = check(n_values, tails, residues)
    print(f"rows checked (n,tail,residue,row) tuples: {checked_rows}", flush=True)
    if not violations:
        print("NO VIOLATIONS: every (n,tail,residue,row,s,s') entry satisfies "
              "C[s][s'] <= M[s][s'] * N[s]. Domination by M holds on this range.",
              flush=True)
    else:
        print(f"{len(violations)} VIOLATIONS found. First 20:", flush=True)
        for v in violations[:20]:
            n, tail, residue, k, s, s2, actual, Ns, bound = v
            print(
                f"  n={n} c={tail} r={residue} row={k}: "
                f"C[{s}][{s2}]={actual} > M*N = {bound:.3f} (N[{s}]={Ns})",
                flush=True,
            )


if __name__ == "__main__":
    main()

# Retreat--pull macro edge rank: exact falsification

Date: 2026-09-01

Status: **ALL THREE FROZEN CLAIMS ARE FALSE.  THE MACROSTEP REMAINS THE
RIGHT TEMPORAL UNIT, BUT THE REGISTERED WIDTH-TWO POTENTIAL DOES NOT PROVE
MORTALITY.  PERIOD TWO REMAINS OPEN.**

## 1. What was tested

`PREREGISTRATION-MACRO-EDGE-RANK.md` froze an integer edge potential `V`
after discovery on all invariant queues through length 12.  Unlike the
earlier per-update ranks, it asked only for:

```text
(MR1) V(R)>=0,
(MR2) V does not increase on a B update,
(MR3) V drops by at least 3 across a surviving AC macro.
```

The `AC` unit is exact: a retreat successor ends in raw suffix `302`, and if
it survives, the next update is the pull `102 -> 0021`.  Consequently these
three inequalities really would have bounded the number of retreats.

## 2. Exact counterexamples

The first held-out analysis killed every registered claim.

Nonnegativity fails at length 13 in both tail modes:

```text
V(2110101010101) = -1,
V(3010101010101) = -1.                              (1)
```

This is not a finite-cutoff accident.  For every `k>=5`, the invariant queue
families

```text
R_2(k)=211(01)^k,       V(R_2(k))=49-10k,
R_3(k)=30(10)^k1,      V(R_3(k))=59-10(k+1)          (2)
```

have negative rank.  The allowed `10/01` cycle has negative weight, so the
potential is unbounded below on the invariant language.

`B` monotonicity also fails literally:

```text
2111101010101 -> 21212100121121,     -1 -> 0,
3010101010101 -> 32112100121121,     -1 -> 0.         (3)
```

Finally, the required `AC` drop is three, while these macros drop only two:

```text
21101012111111
  -A-> 212100101010102
  -C-> 2110001211210021,             -5 -> -7;

31111111021101
  -A-> 301010100212102
  -C-> 3211210002110021,             -4 -> -6.        (4)
```

Every word in (1)--(4) is checked against the exact invariant SFT, and every
arrow is recomputed by the raw four-state queue scan.  Thus each displayed
word is a solver-free certificate.

## 3. Structural lesson

Bundling `A` with its forced `C` successor is still a valid improvement over
demanding descent on the pull separately.  What fails is a translation-
invariant scalar sum of the frozen adjacent-edge weights.  The negative
alternating cycle in (2) shows why a discovery corpus ending at length 12
could admit the candidate while the unbounded regular language could not.

An exact weighted-product synthesis was then formulated directly over words
of arbitrary length.  It couples:

- the five-state invariant suffix automaton;
- one raw scan for `B`;
- two raw scans for `AC`; and
- Bellman lower-bound variables certifying all accepted paths at once.

Even after allowing separate potentials for tails 2 and 3, the rational
systems are unsatisfiable for factor widths one through five.  This is an
unbounded-word computation at each stated factor width, not a queue-length
census.  It is evidence against another small local repair, but no
coefficient-independent claim for arbitrary width is made here.

A concurrently developed stronger analyzer,
`constant_tail_pull_potential.py`, dispenses with macro bundling: it asks for
a factor potential bounded below on the complete invariant SFT, nonincreasing
on every successful update, and dropping on every pull.  Its finite products
also cover words of every length.  Widths one through five are unsatisfiable
(`3,12,35,88,210` factor variables respectively); width six did not finish
quickly enough to classify and is not reported as either satisfiable or
unsatisfiable.  This is a bounded-*memory* obstruction, not a bounded-time
experiment.

The missing bottom-feature crossing lemma is therefore still the live
target.  A successful rank must retain ordered ancestry or an unbounded
stack; a fixed adjacent-edge scalar loses precisely that information.

## 4. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_macro_edge_rank.py

PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/constant_tail_pull_potential.py \
  --last-width 5
```

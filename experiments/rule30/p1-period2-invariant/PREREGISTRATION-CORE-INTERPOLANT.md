# Preregistration: active-core diagonal interpolant

Date: 2026-09-01

Status: **PREREGISTERED BEFORE THE SEARCH DESCRIBED BELOW.**

## 1. Target

The target is the uniform active-core statement

```text
C(m,m+1) is UNSAT for every m >= 1,
```

where `C(m,H)` is the exact local carry CNF defined in
`core_mortality_sat.py`.  This statement would prove the remaining
period-two rung after the already-established bilateral reduction.  It would
not prove arbitrary-period Prize Problem 1, P2, or P3.

## 2. Candidate certificate class

Search for a parameterized family of Boolean consequences on a diagonal cut
of the carry triangle.  An admissible family must have all of the following
properties:

1. every clause or ANF relation has a symbolic position parameter rather than
   a fixed tested width;
2. the family is valid at the deep boundary and is preserved when one input
   symbol and one time row are added;
3. the terminal pin clauses together with the no-`11` clauses contradict the
   family after `m+1` rows; and
4. every preservation and contradiction step reduces to a bounded Boolean
   identity that an independent exhaustive checker can verify.

Relations may carry an unbounded ordered index or a well-founded interval
rank.  A fixed-radius additive score, a fixed finite summary, or a separate
certificate for each width is outside this class because earlier exact
obstructions already kill those templates.

The first probe will mine prime implicates/backbones and low-degree ANF
consequences of small diagonal CNFs after projecting to geometrically aligned
cuts.  Its only purpose is to conjecture a translation-stable schema.  A
schema counts as a result only after it is stated and proved for arbitrary
width.

## 3. Success criterion

Success requires a written induction quantifying over every `m`, plus a
checker for each bounded local identity used by that induction.  Finite SAT,
UNSAT, interpolation, proof traces, ranks, or pattern agreement do not count
as the theorem.

A useful partial result may instead be recorded if it is an exact all-width
identity, or if a smallest counterexample rigorously eliminates the whole
preregistered certificate class.

## 4. Controls

Any implementation must retain and check:

- agreement of `C(m,H)` with direct enumeration through `m=7`;
- the SAT control obtained by dropping no-`11`, namely `C(6,7)`;
- terminal symbol `3`, zero deep carry in every row, endpoint pin inequality,
  and the exact carry equations;
- the long finite Rule 30 trap that first fails at time 185, if a proposed
  consequence is translated back to seed dynamics; and
- Rule 90 `{-1,1}` whenever an argument is claimed to use more than the
  Rule-30 OR identities.

## 5. Resource limits

The exploratory projection search is limited to core widths at most 12,
horizons at most 13, projected clauses of width at most 6, and ANF degree at
most 4.  One run may use at most 30 CPU minutes and 8 GiB of memory.  Larger
finite diagonal sweeps are prohibited unless a concrete symbolic schema has
already been extracted and the larger instance tests a specified induction
step.

## 6. Kill conditions

Abandon a proposed schema immediately if:

- a direct truth-table check falsifies one of its local identities;
- the family needs a number of exceptional clauses or state bits growing
  with the tested width without a proved ordered induction;
- its clauses cease to be translation-stable at the next tested width;
- it is only a low-radius additive invariant (the existing Farkas
  certificates apply); or
- it proves only the finite instances from which it was mined.

If the low-width probe produces no stable schema, record that as a negative
search result only; do not infer that no parameterized proof exists.

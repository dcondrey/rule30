# P3 circuit attack: assessment of the three proposed arms

The ANF degree
theorem was accepted as given and **not** re-verified: `deg f_t = 2t-1`
for `t >= 3` with unique top monomial `M_t`, PROVED unconditionally in
`docs/rule30/overnight/RESULTS-anf.md`.  Zero compute was spent on it.

## Verdict up front

**No `P3_PROOF_DRAFT.md` is written.  All three arms fail, two of them for a
reason that no amount of compute can fix.**  The blocking issue is a category
mismatch between the measures proposed and what Problem 3 asks.  One real
corollary of the degree theorem survives and is recorded below; it is not
Problem 3 and must never be reported as progress on it.

## The category error (kills arms 2 and 3 as specified)

Prize Problem 3 asks for the cost of computing the nth center cell **of the
lone-seed orbit**, on a Turing machine receiving `n` in digit form
(`PREREGISTRATION.md`).  The input is a *fixed* sequence; the only variable
is `n`.

Circuit size, decision-tree depth, sensitivity, block sensitivity and
certificate complexity are all measures of a **function of variable inputs**.
Evaluated "along the single-seed line" the input is a single fixed point, the
function is a constant, and every one of these measures is 0.  There is no
theorem to prove there.  Arms 2 and 3 as written ("SLP length to evaluate
`C(t)` along the single-seed line", "sensitivity along the single-seed
evaluation path") are asking for the complexity of a constant.

This is exactly the gap already recorded for route R9 in `PATH.md`, and it is
why R9 was framed around **proof complexity**: derivation length keeps the
input fixed and still has a nontrivial lower-bound question.  Non-uniform
circuit measures do not have that property.

## Arm 1 (AC0/Smolensky): hypothesis is false as stated

**Counterexample, immediate:** `AND_n` has F2-degree exactly `n` (its ANF is
the single monomial `x_1 x_2 ... x_n`, maximal degree) and is computed by a
depth-2 AC0 circuit with **one gate**.  High exact F2-degree therefore does
not imply any AC0 size lower bound.

The Razborov-Smolensky method needs the target to be inapproximable by
low-degree polynomials over F_p (approximate degree / correlation with
low-degree polynomials), which is a strictly stronger and quite different
property from exact degree.  `deg f_t = 2t-1` says nothing about the
approximate degree of `f_t`, so the proposed derivation has no valid step.

A second, independent objection: `f_t` has `n = 2t+1` variables, so a claimed
`2^Omega(t)` bound is `2^Omega(n)` - the trivial regime, where almost every
Boolean function already lives by counting.  Even if such a bound held it
would distinguish nothing about Rule 30 and would say nothing about the
prize, which is a statement about time as a function of `n`, not circuit size
on `Theta(t)` variables.

## Arm 3's specific numeric claim is empirically false

The claim to be derived was `s(f_t) >= t`.  Measured directly (exact
evolution, all `2t+1` single-cell flips of the seed row):

| t | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|
| s(f_t) at lone seed | 2 | 4 | 4 | **4** | 5 | 8 | **7** | 8 | **8** | 12 |
| max s over 200 random inputs | 6 | 7 | 9 | 10 | 11 | 12 | 13 | 14 | 13 | 14 |

`s(f_t) >= t` fails at t = 6 (4 < 6), t = 9 (7 < 9), t = 11 (8 < 11).  The
hypothesis is refuted, and the lone-seed sensitivity is visibly *below* the
random-input maximum, i.e. the single seed is not a sensitivity-maximizing
input.

## What actually follows from the degree theorem (recorded, modest)

For any Boolean function, F2-degree lower-bounds decision-tree depth:
`deg_2(f) <= D(f)`.  With the theorem:

> **Corollary.**  `D(f_t) >= 2t-1`.  Any algorithm computing the center cell
> at time `t` from an **arbitrary** initial row of the `2t+1`-cell light cone
> must query at least `2t-1` of those cells in the worst case.

True, unconditional, and a legitimate one-line consequence worth a sentence
in a write-up.  Its scope must be stated in the same sentence: it concerns
the *variable-input* problem, it is about queries not time, and it is not
Problem 3, which fixes the input to the lone seed.  Reported alone without
that scope it would read as prize progress, which it is not.

## What would be a sound version of this program

Keep the input fixed and change the measure to one that still has content
there.  That is the R9 framing: encode the light cone as CNF and lower-bound
**derivation length** in resolution / polynomial calculus / bounded-depth
Frege for deriving `c_n`.  The prior-art position for that is already in
`PATH.md` R9 (Cavagnetto 2011 and Kapytka arXiv:2604.01041 are the only
proof-complexity-meets-CA work, both on inversion, never prediction), along
with the honest transfer obstruction: grid-Tseitin bounds attack unsatisfiable
parity instances, whereas this system is satisfiable with a unique solution.
The degree theorem may well feed a polynomial-calculus **degree** lower bound
there, which is the one connection between these two lines that is not a
category error - and PC degree bounds are a standard route to PC size bounds.
That is the arm worth building; it was not built in this round.

## Files

* This document.  No code was written for arms 1 and 2, because the
  refutations are analytic and running searches would have produced numbers
  in support of a false hypothesis.
* Sensitivity measurement is a five-line exact evolution, reproduced inline
  in the command recorded in the log.

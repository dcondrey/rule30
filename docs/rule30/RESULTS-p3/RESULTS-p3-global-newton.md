# Global Newton iteration: an exact correction law and failed fast schedules

Date: 2026-09-13. **No sublinear Rule 30 algorithm is obtained.** This is a
new constructive test of solving the entire space-time system by repeated
linearization, motivated by Newton/Hensel iteration and tangent propagation
in nonlinear dynamics. It does not infer computational hardness from chaos.

The useful exact result is a residual formula: after a complete Newton solve,
the remaining defects are precisely products of adjacent corrections. This
gives an independently checkable correctness certificate and identifies why
ordinary precision doubling is unavailable. Four specified logarithmic
iteration schedules are refuted on the actual singleton trajectory.

Code: [p3_global_newton.py](../../experiments/rule30/p3_global_newton.py).
Bounded artifact: [p3-global-newton.json](../../experiments/rule30/p3-global-newton.json).
All preprocessing and operand sizes remain charged under the
[P3 query model](P3-SCOPE-AUDIT.md).

## 1. The proposed solve, with its actual nonlinear term

Use addition in F_2. For a row x, Rule 30 is

\[
 F(x)_i=x_{i-1}+x_i+x_{i+1}+x_ix_{i+1}.
\]

Let a_t be a proposed space-time diagram with the correct initial row. Its
Boolean derivative is the linear row map

\[
 (J(a_t)e)_i=e_{i-1}+(1+a_{t,i+1})e_i+(1+a_{t,i})e_{i+1}.
\]

A global Newton step solves the triangular linear system

\[
 v_0=u_0,\qquad v_{t+1}=F(a_t)+J(a_t)(v_t+a_t).
\]

Equivalently, each new row satisfies

\[
 v_{t+1,i}=v_{t,i-1}+(1+a_{t,i+1})v_{t,i}
              +(1+a_{t,i})v_{t,i+1}+a_{t,i}a_{t,i+1}. \tag{1}
\]

This is a valid exact algorithm for one Newton step: the coefficients are
known from a, and (1) is linear in v. It is not a solution by assertion; the
verifier implements this solve both as packed rows and as scalar
truth-table derivatives. No unknown true row is used to perform the solve.

Initialize a^(0)_0 to the singleton and a^(0)_t=0 for t>0, and repeat (1).
The resulting sequence of approximations is fully specified from n alone.

## 2. Exact residual certificate

For any row a and correction e, direct expansion gives

\[
 F(a+e)=F(a)+J(a)e+(e_i e_{i+1})_i.
\]

Writing delta_t=v_t+a_t in a completed Newton step yields

\[
 v_{t+1,i}+F(v_t)_i=\delta_{t,i}\delta_{t,i+1}. \tag{2}
\]

Thus the new diagram is an exact trajectory if these products vanish at
every relevant cell. Checking (2) uses only the supplied approximation and
its new iterate. More generally, to certify its center bit at time n, it
suffices to check the initial singleton and zero residual on the complete
backward cone of that query. The conclusion follows by induction from the
base row. This certificate can be large; it is not free query advice.

If the reference agrees with the true trajectory through time m, (1) agrees
through time m+1. Induction therefore proves a^(k) exact through at least
time k, for every k. Running n iterations is a uniform, terminating exact
query algorithm, but it is computationally worse than direct simulation in
the materialized implementation.

## 3. Why the usual Newton doubling argument fails, at every length

Ordinary power-series multiplication adds orders of vanishing. The product
in (2) is at the **same time index**: it is coefficientwise multiplication
in time. Two errors first appearing at time m can have a nonzero product at
that same time. There is no valid inference from two order-m errors to an
order-2m residual.

Here is an exact counterexample family, without an asymptotic extrapolation.
For any m>=1, start from a true diagram and change exactly two adjacent
cells i,i+1 of its row m in the reference a, leaving all other rows true.
Its Newton iterate v agrees with the true diagram through row m. At that
row delta has precisely those two ones, so (2) has exactly one nonzero
residual, at (m,i). It follows that v_(m+1) differs from the true row at
exactly i. A Newton step improves the first wrong time from m to m+1,
which is strictly less than 2m for every m>=2.

An equivalent error equation makes the remaining propagation explicit. If
e_t=a_t+u_t and d_t=v_t+u_t, then

\[
 d_0=0,\qquad d_{t+1}=J(a_t)d_t+(e_{t,i}e_{t,i+1})_i.
\]

The source of the new error is the adjacent-pair product of the old error;
its propagation is linear but depends on the full reference a. This
identity supplies no sparsity or fast-solve bound by itself.

This refutes uniform temporal precision doubling for arbitrary references.
It does not establish the iteration count for the special references
generated from a^(0), or rule out a different preconditioner or lift. A
2-adic lift of Boolean equations would also need a correct solution modulo
2 to begin ordinary Hensel lifting; supplying that solution would supply
the Rule 30 answer being sought.

## 4. Exact singleton counterexamples to four query algorithms

The bounded experiment tests the concrete candidate: return the center of
a^(k) with k=A ceil(log2(n+1)), for A=1,2,3,4. The initial approximation and
iteration are exactly those in section 1. Each candidate is incorrect:

| A | n | Newton iterations | Predicted bit | True bit |
|---:|---:|---:|---:|---:|
| 1 | 6 | 3 | 1 | 0 |
| 2 | 21 | 10 | 1 | 0 |
| 3 | 40 | 18 | 1 | 0 |
| 4 | 50 | 24 | 1 | 0 |

Each n is the first failure of that schedule in the checked range. The
artifact retains every first-error diagnostic through 32 rounds on horizon
128; it is not a large prefix-generation experiment. For example, the first
incorrect full-row times at rounds 0 through 4 are 1,2,3,6,7. Early apparent
doubling therefore already fails on the actual iterates. The corresponding
first incorrect center times are 1,2,4,6,8.

These witnesses do **not** refute every constant A, an O(log n) iteration
bound with unspecified constants, or sublinear iteration count in general.
They refute four complete, specified algorithms. No fitted growth exponent
is used as a theorem.

## 5. Construction cost and the unresolved acceleration

The current implementation materializes 2n+5 cells at each of n time steps.
One round visits n(2n+5) scalar cells, or Theta(n^2) work. Packing the rows
changes constants; its wide bit operations remain charged. Therefore even
a proved logarithmic number of these rounds would not give a sublinear
query algorithm.

The prospective acceleration has two distinct missing ingredients: a
provably small iteration schedule for the center, and a way to solve the
time-dependent linear systems (1), or certify their center residual,
without materializing the cone. The algebra establishes neither. For a
truly additive cellular automaton the quadratic remainder is zero and one
Newton step solves the whole diagram; fast powering of that fixed linear
operator can then be a real shortcut. For Rule 30 the coefficients in (1)
depend on the evolving approximation and retain the nonlinear difficulty.

## 6. Validation

The verifier checks all 64 local reference/new-state assignments for (2),
4,096 packed residual rows, and 25 Newton iterates against an independent
scalar truth-table implementation on horizon 24. It checks eight instances
of the all-length adjacent-error construction, accepts an exact causal-cone
certificate, and rejects two deliberately corrupted certificates. The
universal statements above follow from their displayed algebra and
inductions; the finite checks validate the implementations and witnesses.

```
uv run --offline --no-project python experiments/rule30/p3_global_newton.py
```

No paid compute, GPU work, long-prefix regeneration, or extension of an old
compression census was used. Problem 3 remains open.

# RESULTS — arm "automaticity": reduction ladder between P1 and non-2-automaticity

STATUS: REDUCED — a ladder of statements S(0) <= S(1) <= S(2) <= ... is established, with
S(0) EXACTLY equivalent to Wolfram P1 and the conjunction of all S(n) exactly equivalent to
non-2-automaticity of the center column. A finite GF(2) rank computation certifies only a
bounded-height S(n,d), not an all-height rung S(n). Certificates were independently reproduced.
**Correction integrated 2026-09-15:** the generic Lemma L below was already refuted in
`frontier_attack/a20_bridy_verification/bridy_verification.md`. It is not an open obligation.
See [the scope audit](../AUDIT-automaticity-route-scope.md) for that source and the surviving
possibility of an independently proved, sequence-specific conditional bound.

All four leads passed adversarial verification with verdict "holds" — the only workflow this
session in which nothing broke.

## The ladder

Let F(x) = sum_{t>=0} a(t) x^t in F_2[[x]] for the single-seed center column a = A051023.
Over F_2, F(x)^(2^i) = F(x^(2^i)).

DEFINITION. F admits an Ore relation of order n and height d if there are polynomials
P_{-1}, P_0, ..., P_n in F_2[x] of degree <= d, not all zero, with
    (*)   P_{-1}(x) + sum_{i=0}^{n} P_i(x) * F(x^(2^i)) = 0   in F_2[[x]].
S(n) := "F admits no Ore relation of order n at any height". S(n,d) bounds the height too.

- S(0) <=> P1 exactly. Order 0 is P_{-1} + P_0 F = 0, so F is rational over F_2(x); a power
  series over a finite field is rational iff its coefficient sequence is eventually periodic.
- Conjunction of all S(n) <=> F transcendental over F_2(x) <=> (Christol 1980;
  Christol-Kamae-Mendes France-Rauzy 1980) a is not 2-automatic.
- Non-automatic => not eventually periodic, so the ladder interpolates strictly between P1 and
  the stronger target, giving a graded sequence of intermediate statements rather than one
  all-or-nothing goal.
- Finite refutability (one-sided, monotone in N): truncating (*) to coefficients of
  x^0..x^(N-1) gives an F_2-linear system; an exact relation satisfies EVERY truncation, so a
  single N with trivial nullspace proves S(n,d).

The ladder is strict, not a chain of equivalent restatements: Thue-Morse is not eventually
periodic yet satisfies x + (1+x)^2 T(x) + (1+x)^3 T(x^2) = 0, an unconditional witness that
S(0) does not imply S(1).

## The genuinely new rung

NOT-S(1) says: there exist a width d and fixed subsets J0, J1 of {0..d} with
    sum_{j in J0} a(m-j)  XOR  sum_{j in J1, m-j even} a((m-j)/2)  =  0   for all m > d,
a bounded-width F_2-linear relation tying a window of the column near m to a window near m/2.
S(1) asserts no such relation exists. It is strictly stronger than P1, strictly weaker than
non-automaticity, and no prior statement of it for A051023 was found.

## Certificates (INDEPENDENTLY REPRODUCED HERE)

The agent reported: no Ore relation for A051023 at order <= 12 and heights to 570, order 0 to
height 3999, order 1 to height 2665, at N = 32000, all nullity 0; solver calibrated by
recovering relations for Thue-Morse (1,3), Rule 90 columns 0 and 5, Rule 60, Rule 150, and the
regular paperfolding sequence, all at order <= 2 and height <= 6.

Re-implemented here from scratch (experiments/overnight-arms/automaticity/ore_check.py, own
matrix construction and own GF(2) elimination), with a ground-truth prefix assertion:

| target | (n,d) | nullity | reading |
|---|---|---|---|
| Thue-Morse | (1,2) | 0 | no relation — solver is tight, not permissive |
| Thue-Morse | (1,3) | 1 | RELATION FOUND, matches the known witness |
| Rule 90 center | (0,0) | 1 | caught instantly |
| Rule 90 center | (1,5) | 12 | caught |
| Rule 30 center | (0,50), (0,200), (0,800) | 0 | S(0,d) certified |
| Rule 30 center | (1,20), (1,60), (1,120) | 0 | S(1,d) certified |
| Rule 30 center | (2,20), (2,40) | 0 | S(2,d) certified |
| Rule 30 center | (3,20) | 0 | S(3,d) certified |

The Rule 90 control behaves exactly as it must: the identical code catches Rule 90 at order 0
height 0 while leaving Rule 30 standing. This arm therefore PASSES the Rule 90 filter, unlike
every ensemble-level approach examined this session — and it passes for a structural reason,
not by luck: Rule 90 is F_2-linear, so by Rowland-Yassawi its columns are 2-automatic and
must be caught at some finite order.

## What the order-0 certificates do and do not mean

Honest reading, since this is the easiest thing to over-claim. An order-0 nullity-0 certificate
at height d rules out eventual periodicity for every (preperiod q, period p) with
max(p, q+p-1) <= d. That is a real unconditional partial result on P1 — but it is equivalent to
a direct finite periodicity check on the prefix, so the mathematics is elementary and is not
new. The new content of this arm is the LADDER: the order >= 1 rungs, which are not finite
periodicity checks and have no elementary restatement.

## Two proved negatives worth keeping

1. "Nonlinear rule, therefore transcendental" can NEVER work. Rule 30's only nonlinearity is
   the coefficientwise product c*r, a Hadamard product, and by Sharif-Woodcock (J. London Math.
   Soc., 1988) algebraic power series over F_2 are closed under Hadamard product. So the
   algebraic class absorbs exactly the nonlinearity Rule 30 has. What must fail instead is
   uniformity of degree/height under iteration, and that is precisely where a proof has to live.
2. Rowland-Yassawi does not transfer. It characterizes p-automatic sequences as columns of
   LINEAR CA; if A051023 were automatic it would merely also be a column of some linear CA,
   which contradicts nothing about Rule 30.
3. (From the kernel-witness lead, also verified.) The tempting handle "no residual of A051023 is
   eventually constant, therefore the 2-kernel is infinite" is FALSE. Thue-Morse is an explicit
   counterexample: finite 2-kernel, no eventually constant residual.

## Historical proposed obligation — Lemma L (refuted)

The following proposal is retained as history, not a live target. Both its order and height
bounds are false in general; see the correction above. The exponential generic bound does
not prove that a special bound for the Rule 30 center is impossible.

The ladder converts non-automaticity into infinitely many finite computations, but the
conversion rate is unproved. Needed:

    LEMMA L. If a is 2-automatic with k states, then F admits an Ore relation of order
    <= poly(log k) and height <= poly(k).

Only the exponential bound order <= m, height <= m*2^(2m) is proved, where m is the GF(2)
dimension of the span of the 2-kernel. Because that conversion is exponential, the certificates
above do NOT dominate ARM6's rank-512 measurement, and no claim is made that they do. With
Lemma L, finite rank computations at feasible heights would begin to exclude automatic
sequences with genuinely large state counts.

## Companion obstruction (separate lead, also verified "holds")

Theorem O: for every N, the sequence agreeing with a on [0,N) and 0 thereafter is eventually
periodic, hence 2-automatic, with 2-kernel size <= 2N+1. So no property of any finite prefix
can imply non-automaticity or non-periodicity: ARM6's >= 8191 distinct residuals are exactly a
lower bound on a complexity function and can never be more. Quantitative form: with
A^ker(N) := min{|K_2(b)| : b 2-automatic, b agrees with a on [0,N)}, non-automaticity is
equivalent to sup_N A^ker(N) = infinity, and A^ker was pinned within a factor 1.08 at N = 2^16.
This converts "finite data cannot settle it" into an exchange rate: N terms buy a kernel lower
bound of about N/8 and nothing more, ever.

Note the two results are complementary and consistent: Theorem O says no finite prefix computed
from a alone settles the question, while the ladder's rungs are finite computations that settle
BOUNDED-COMPLEXITY cases — each S(n,d) excludes a bounded family, never the whole class.

## Reproduction

- uv run python experiments/overnight-arms/automaticity/ore_check.py
- uv run python experiments/overnight-arms/common/ensemble_filter.py  (Rule 90 control)

## Spending

Local CPU only. Modal $0.

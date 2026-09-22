# Audit of START-HERE and the PATH row table

Date: 2026-09-15. **P1, P2 and P3 remain open.**

The main overlooked distinction is between a failed representation and a
failed mathematical strategy. Some entry-point summaries reject more than
their source proofs establish. There are also smaller, quantitative targets
inside the surviving routes. This audit records those differences; it does
not reopen Collatz/Anashin or treat finite randomness as a seed theorem.

## 1. The contraction screen exceeds its cited theorem

`START-HERE.md` and `CROSS-ARCHIVE-2026-09-07.md` said a decreasing rank,
potential or bounded annotation was refuted unless it escaped the free-monoid
obstruction. But the cited
[injectivity proof](../../experiments/rule30/p1-period2-invariant/RESULTS-SYNTACTIC-MONOID-INJECTIVITY-PROOF.md#6-scope-honestly)
explicitly excludes only lossless summaries of an interior block's complete
successor trace. Its section 6 leaves lossy target-specific summaries and
whole-queue summaries untouched.

An injective representation need not admit finite lossless compression.
That fact says nothing by itself about whether a target predicate can be
certified by less information. Nor does reversibility prohibit guarded
termination: the bijection `n -> n-1` on the integers leaves the positive
integers in finitely many steps, certified by the rank `n` while its guard
holds. This is a logical control, not a Rule 30 ranking construction.

The appropriate next requirement is to specify the predicate the summary
must certify and prove preservation of that predicate. Reconstructing the
whole successor queue is required only if the proposed argument needs it.
The existing exact local-potential and queue-window counterexamples retain
their stated force. The screens in both entry documents have been narrowed.

## 2. Overwriting a column can leave the mathematical domain

`PATH.md` sections 0.1 and 7.3 used an `O(1/W)` response to overwriting the
center as a universal disqualification of bulk statistics. The valid
conclusion concerns the statistic alone on arbitrary arrays. An overwritten
diagram generally violates Rule 30, so this operation does not supply two
counterexamples within the domain of a theorem about valid seed orbits.

For a simple control, consider the fixed shift rule `s(t+1,x)=s(t,x+1)`
on the two initial rows `0^Z` and `(01)^Z`. Bulk density distinguishes their
center densities, respectively zero and one half. A nontrivial overwrite
of just their center changes bulk averages by `O(1/W)`, but breaks the shift rule. Thus
column insensitivity alone is not a no-go theorem for deductions that use
the evolution law. This does not provide the missing Rule 30 deduction.

Quantitative rates also matter: a discrepancy of order `1/W` can retain
information erased by taking an unscaled limit. A candidate still needs an
exact identity or inequality connecting its statistic to the designated
center. The previously tested geometric statistics supplied no such link;
their failed experiments stand. PATH and START-HERE now state this scope.

## 3. Row 46 retains an already-refuted obligation

The primary row table and overnight automaticity report still called the
generic polynomial Ore-height / polylogarithmic Ore-order bound “Lemma L,”
an open next step. The archive's `a20_bridy_verification` had already refuted
both bounds. Later PATH prose knew part of this, but the main row did not.

There is a second, independent scope error: the subsequent `a22` report
calls automaticity the negation of P1 and rejects a seed-specific conditional
bound as circular. Automatic nonperiodic sequences exist. Assuming
automaticity in a contradiction proof is legitimate. What is missing is an
independently proved Rule-30-specific bound, not permission to use that
logical form. See [the detailed correction](AUDIT-automaticity-route-scope.md),
which credits the existing refutation and corrects its monomial state count.

This repairs the research map; it supplies neither nonautomaticity nor a
shortcut for the singleton query.

## 4. P1: keep the origin and quantify the required mismatch

The [R1 scope audit](RESULTS-r1-periodic-realization-scope.md) gives exact
small periodic tori for a purportedly unconstructed right-hand realization.
Existence of such a realization does not identify the seed's right history;
the tori are not left-finite. It also refutes the literal all-eventually-
periodic PIN-Pi target by the boundary word `110^infinity`.

A quantitative corollary of the existing driven-left-half-plane proof is
more useful. If its boundary starts at `c_0=1` and is eventually periodic
with period dividing `P`, then, for every sufficiently late `T`, column
`-1` has a period-`P` mismatch in `[T,2T+P-1]`. In a glued Rule 30 diagram
such a mismatch must occur at a zero phase and also be a right-neighbor
mismatch. The proof propagates a hypothetical long agreement backward
until it contradicts the exact leftmost seed edge.

Thus a compatible right history must have at least logarithmically many
such mismatches. An origin-specific upper bound `o(log N)` at one fixed
period multiple would already contradict it, even if there were infinitely
many mismatches. No such upper bound is proved. This is a quantitative
replacement obligation, not a claim that P1 has become logically easier.

## 5. P2: fewer lags and a one-sided bound suffice

The [sparse-difference report](RESULTS-p2-sparse-difference-correlations.md)
specializes the existing correlation argument to dyadic translations.
For center signs `z_t=1-2c_t` and ordinary correlations `C_N(h)`, it suffices
to prove

```
limsup_N C_N(2^a-2^b)/N <= 0,     for each fixed a>b>=0.
```

There are only `O(log^2 X)` such lags below `X`. Limits of the correlations
need not exist. This condition would prove P2 and also P1. The finite
inequality and implications are proved; the singleton estimates are not.

The differences are essential: the biased periodic word
`(110100010000)^infinity` has zero correlation at every power-of-two lag.
It refutes a tempting dyadic-only shortcut. No artificial control in this
audit is claimed to be a Rule 30 seed trace.

## 6. Work justified by the audit

For P1, work on the origin-preserving mismatch obligation or a guarded
target-specific certificate, stating exactly what information it retains.
For P2, the sparse ordinary-lag condition is a smaller sufficient analytic
target, but still needs a seed mechanism. For P3, this audit identifies no
new query algorithm or general lower bound.

No larger simulation, universal-constant fit, or generic Collatz conjugacy
would resolve the missing steps identified here.

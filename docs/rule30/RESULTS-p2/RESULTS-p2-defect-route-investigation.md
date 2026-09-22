# Investigation of defect geometry and exact scale reduction

Date: 2026-09-10. **No proof or disproof of P1, P2, or P3 was obtained.**

The objective was to turn the exact defect decomposition into an actual
sublinear bound on the lone-seed center discrepancy. Two routes were pursued:
weighted defect-count inequalities, and exact coarse dynamics retaining the
nonlinear source feedback. Both yielded precise constraints on the method;
neither yielded the required asymptotic estimate.

## 1. Weighting the defect certificate does not preserve its useful bound

The [flux report](RESULTS-defect-mask-flux.md) derives the exact local law

\[
3(y-q)+5qr+4p(1-q)r
=2(p\lor q\lor r)+J(p,q)-J(q,r),
\quad J(p,q)=p-q-4pq.
\]

Spatial summation recovers the previous cumulative defect-count theorem.
Mask weighting exposes an additional spatial current. Its uniform
absolute-value bound accumulates at order

\[
T^{\log_2(1+\sqrt5)}\approx T^{1.69424}
\]

on dyadic Rule 150 backward masks. This order is attained by independently
chosen finite rows; no such lower bound is asserted on the coupled seed orbit.
Most decisively, reducing the certificate modulo two removes its positive
terms and gives exactly the original Rule 30 polynomial. The certificate
therefore contributes no additional parity relation to the Duhamel identity.

Actual seed current diagnostics through T=8192 show finite cancellation
relative to the absolute bound. They prove no asymptotic current estimate,
and the integer current is not itself the center discrepancy.

## 2. Evaluating the nonlinear feedback at two steps

The [pair-factor report](RESULTS-dyadic-pair-factor-obstruction.md) proves

\[
(F_{30}^{2}x)_i=x_{i-2}\oplus
[(1\oplus x_{i-1}\oplus x_i)(x_{i+1}\lor x_{i+2})].
\]

This yields an exact four-state evolution on adjacent spatial pairs.
Every one of the 13 proper nonconstant partitions of those four states
fails to determine its next projected state. This exhausts all binary
projections and all three-symbol projections, not just selected summaries
such as pair parity or the `11` indicator.

The universal witnesses are also realized at the seed's center. All 13
have input times at most 64 and output times at most 66. Hence no
time-independent radius-one recurrence on such projected pairs describes
the seed from its start. The result does not exclude an eventual recurrence
after an unknown cutoff or a larger neighborhood on the seed.

The matching Rule 90 and Rule 150 tests each admit three nontrivial binary
projections: either coordinate and their XOR. Thus the test identifies an
exact difference from the linear controls while respecting their known
dyadic decompositions.

## 3. Larger blocks: certificates through size eight

The [supercell certificates](RESULTS-supercell-congruence-certificates.md)
extend the universal classification to every block size n=1,...,8 and every
output alphabet. Any projection that merges two states while preserving
the exact n-step block evolution is forced to merge all states.

Four explicit unary maps derived from Rule 30 suffice. For each size, the
certificate sends every distinct state pair to a terminal pair, then proves
that identifying that pair identifies every state. Replay checks 43,435
pair cases across all eight sizes and 502 spanning merges. This supplies
a complete finite proof without enumerating every possible partition.

An attempted extension to arbitrary n did not close. In particular, a
simple full-cycle argument for one of the maps fails on explicit small
cycle decompositions. No all-size conclusion is drawn.

## 4. Prior work and the remaining target

Exact block coarse-graining is an established framework, not a newly
introduced proof strategy. [Song and Grochow](https://www.cs.toronto.edu/~jgrochow/songGrochowCA.pdf)
describe larger finite searches and the unresolved arbitrary-block-size
question. [Dzwinel and Magiera](https://doi.org/10.1016/j.jocs.2015.07.001)
report Rule 30 among the surviving non-coarse-grainable cases at block size
seven. The present records emphasize explicit certificates and the scope
of their actual-seed applications; no literature-priority claim is made.

The outstanding requirement is still a theorem on the designated seed,
such as

\[
\left|\sum_{t=1}^T(-1)^{\theta(t)+R_t}\right|=o(T).
\]

The [ordered-energy report](RESULTS-p2-ordered-energy-audit.md) gives an
alternative sufficient target: accumulated contrast of adjacent temporal
block sums at growing scales. That formulation permits inequalities without
an autonomous compressed state. The present nonclosure results do not
exclude it, but no seed-specific accumulated-contrast estimate was obtained.

None of these finite representation obstructions establishes P3: failure
of a specified compression family does not prove a lower bound against all
algorithms. They also do not decide whether the center eventually becomes
periodic, so P1 remains outside the proved conclusions.

## 5. Reproducible evidence

- [Weighted-current verifier](../../experiments/rule30/defect_mask_flux_audit.py)
  and [results](../../experiments/rule30/defect-mask-flux-audit.json): eight
  local patterns, 8,190 mask extremizers, 16,384 kernel rows, and finite seed
  diagnostics through 8,192.
- [Pair-factor verifier](../../experiments/rule30/dyadic_pair_factor_audit.py)
  and [certificates](../../experiments/rule30/dyadic-pair-factor-audit.json):
  32 local assignments, all pair partitions for three rules, 569 complete
  seed rows checked by two implementations, and all 13 seed collisions.
- [Supercell verifier](../../experiments/rule30/supercell_congruence_certificate.py)
  and [certificates](../../experiments/rule30/supercell-congruence-certificates.json):
  exact non-compression through block size eight, for every output alphabet.

The local identities, current signs, kernel recurrences, pair classification,
and seed witnesses received independent checks. No stochastic independence
assumption or extrapolation of a finite density measurement enters any
proved statement.

## 6. Quarter-wave potential and current

The [quarter-wave report](RESULTS-quarter-wave-current-target.md) derives
an integer identity for the actual seed:

\[
A(T)-T/2=P_T+\sum_{t<T}(K_t-1/2),\qquad
P_T=\sum_{m\ge0}(x_{4m+1}^T-x_{4m+3}^T).
\]

The identity and finite diagnostics through time 131,072 have been checked.
No sublinear bound on either term is proved. The report isolates a distinct
partial target, a uniform sublinear bound on the spatial imbalance P_T,
and gives periodic controls showing why spatial phase and the initial
condition cannot be discarded. A finite spatial cutoff bounds the potential
automatically but introduces an unknown boundary column. Neither this
identity nor that cutoff removes the unresolved cancellation estimate.

## 7. Spatial variance and finite approximation claims

The [finite-gap, MPS, and variance report](RESULTS-finite-gap-mps-and-variance.md)
proves the exact spatial-window identity E_(2L)=4E_L-2Q_L-D_L. It gives
strict normalized energy loss at every doubling on a nonzero finite positive
row. Explicit coherent rows nevertheless retain limiting variance 1/16 at
sublinear window lengths. The outstanding theorem is uniform accumulated
loss on the designated seed, not mere strictness at finite scales.

The same report gives an all-k de Bruijn counterexample to inferring infinite
mixing from a fitted finite-block spectral gap, an exact Rule 30 invariant
bond-two measure with nondecaying correlations, and a fair-noise Boolean
surrogate whose stationary center density is 1/3. These refute the stated
general implications, not P1, P2, or P3 for the lone seed.

The [seed loss search](RESULTS-seed-loss-certificate-search.md) adds an
all-time-in-the-enumerated-range census of 35,509 row/scale cases and the
exact counterexample delta_(20,4)=17/84 to a uniform one-quarter loss.
The [coherence report](RESULTS-quarter-wave-coherence-barrier.md) proves
an all-length finite-support loss floor and an inverse persistence lemma;
the floor is insufficient on sublinear scales.

The [sparse-coherence report](RESULTS-quarter-wave-sparse-coherence.md)
retains actual initial zeros in an inverse search. A closed 16-depth,
64-period subsystem proves that origins with at most two ones can attain
maximal positive P at times n=1 modulo 4 only for n=1,5,9. This excludes
exact maximality in that class; it does not bound ordinary non-maximal
imbalance by o(n).

The [atom-propagation report](RESULTS-quarter-wave-atom-propagation.md)
proves an all-k obstruction to propagating finite-width spectral absence
on arbitrary rows: every fixed width can hide a quarter eigenfactor that
a later Rule 30 coordinate reveals. It supplies explicit periodic controls
and an all-length argument using the existing ANF theorem and a
phase-indexed circulation. The seed limiting-measure criterion remains
valid and unproved.

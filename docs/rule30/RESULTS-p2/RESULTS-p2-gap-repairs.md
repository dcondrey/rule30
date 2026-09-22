# P2: repairs to the research gaps

Date: 2026-09-11. **The scale and matching formulations are repaired. The
singleton cancellation theorem remains open.** The work below also proves
why a specific attempt to supply the missing seed information is insufficient.
It does not turn a conditional implication or finite observation into a
solution of P2.

## 1. Remove the unnecessary scale restriction

The primary target in the [dependency map](PRIZE-PROBLEM-DEPENDENCIES.md)
now allows any dyadic block length L_k=o(N_k) whose normalized energy tends
to zero. The old square-root cutoff and fixed-window recurrence remain
optional sufficient conditions.

The [full-scale analysis](RESULTS-p2-flexible-scale-audit.md) proves that,
for maximum shell prefix discrepancy M_k and N_k=2^k,

\[
F_k=\min_{0\le j\le k}\left(V_{k,j}+4^{j-k}\right),\qquad
\frac12\left(\frac{M_k}{N_k}\right)^2
\le F_k\le5\frac{M_k}{N_k}.
\]

Thus F_k->0 is equivalent to P2. This diagnostic retains all scales and
automatically penalizes blocks comparable to the whole shell. It does not
require a guessed rate of convergence. A proved construction shows that
**every predetermined sublinear schedule** misses some balanced artificial
sequence; simply replacing sqrt(N) with a larger prescribed cutoff would
leave that logical restriction in place.

The actual data contain cancellation that the optional sign test misses.
At k=28,j=26 the four sums are

\[
(-5906,-304,11572,-6458).
\]

Their sign-diversity weight is zero, but merging them removes more than
99.85% of their normalized energy. Across all 378 available four-block
profiles, the new analysis includes 209 beyond the old domain. For k=28,
allowing all scales improves the finite upper bound on M/N from 0.00786135
to 0.00293268. The measured value is 8303/268435456. Neither finite number
is an asymptotic estimate.

Even an optimized sign-diversity product, with arbitrary skips and varying
losses, is only sufficient: an explicit nearly balanced run family has
M/N->0 while that product tends to 1/2, with energy nonzero at every level.
Exact energy remains the primary diagnostic.

## 2. Repair the matching quantifiers and identify duplicate routes

The [matching report](RESULTS-p2-matching-energy-bridge.md) proves the direct
conversions

\[
U_{L-1}/N\le\sqrt{V_L},\qquad
V_L\le U_R/N+2R/L.
\]

Therefore flexible sublinear matching and flexible coarse energy are
equivalent certificate families. The kinetic projection, echo pairing,
and queue accumulator provide different tools for one cancellation problem;
they are not three established seed mechanisms.

More specifically, define the positive deficit of an interval I as its
positive count minus the negative count in its radius-R expansion. The
exact unmatched positive count is the maximum **sum** of such deficits
over collections with disjoint expansions; likewise for negatives.
Bounding just the largest deficit by o(N) is insufficient. Repeated
`++++----` blocks at R=1 have bounded largest individual deficits but
linear total unmatched count.

The repaired sufficient single-interval target is

\[
R_k=o(N_k),\quad R_k\ge1,\qquad
D_+(R_k)+D_-(R_k)=o(R_k),
\]

where D_+ and D_- are the nonnegative largest one-sided deficits. The proof
uses the packing factor `1+floor((N-1)/(2R+1))`. This estimate, or a bound
on the full collection deficiency, must be obtained from the actual seed.
No such estimate has been proved. Choosing the radius from the unknown
discrepancy would only use an existing equivalence.

## 3. Test the proposed seed information instead of assuming it suffices

The [seed-geometry theorem](RESULTS-p2-seed-geometry-audit.md) supplies an
all-length obstruction. Starting from the actual seed row x^a, for
`a>=h+T+d`, only the T interior positions `-h-1,...,-h-T` need to be
changed to prescribe any T subsequent center bits after relative time h.
The alternative autonomous evolution preserves:

- The actual center history through relative time h.
- The entire actual right half at the observation cut h.
- Both exact d-deep moving edge strips forever, including the mandatory
  left-edge nonlinear defect when d>=2.
- The exact expanding support endpoints.

With sublinear h and d, T can be a fixed positive fraction of the nominal
age at the cut. Thus these data permit macroscopic signed discrepancy.
The competitors are not singleton evolutions; the theorem shows exactly
which remembered data fail to distinguish them. It neither disproves P2
nor excludes an induction that retains additional constraints from time zero.

There is an exact origin test. Every nonzero finite Rule 30 row expands
both extreme occupied positions by one at every step, and Rule 30 is
injective on finite rows. Hence a row with endpoints [-n,n] has n finite
predecessor steps if and only if it is the singleton row x^n. Full finite
ancestry excludes the competing rows; recent history alone does not.
More explicitly, if d_fin(y) is the maximum finite ancestry depth, then
`n-d_fin(y)` is invariant under Rule 30 and vanishes precisely on the
singleton orbit. This characterizes origin without providing a cancellation
estimate. The four explicit competitors have invariant values 60, 62, 122,
and 120, so the distinction can be checked directly.

## 4. What is now required of the next proof

The remaining task is to extract a quantitative consequence of singleton
origin that controls exact temporal energy or total matching deficiency.
A proposed invariant must distinguish the actual row from the explicit
competitors above. Merely retaining seed edges, measuring another local
statistic, or relabeling the discrepancy does not supply that consequence.

The spatial potential/current identity remains available as another
algebraic starting point. Its terms may cancel jointly; separate sublinear
bounds are sufficient rather than necessary. Neither the local-window
obstructions nor the new cut-data obstruction excludes all nonlocal or
origin-preserving arguments.

These results remove unsupported restrictions and prove a stronger
obstruction to one proposed mechanism. They do not establish an asymptotic
breakthrough for P2, and they do not establish that the remaining theorem
has become easier.

## 5. Verification

Each linked report includes its proof, runnable checker, and exact output.

- Flexible scales: 278 exhaustive short words, six artificial controls,
  all 378 stored-seed profiles, 169 previous-profile rechecks, and three
  independent byte-count checks of large-scale profiles.
- Matching: 2,046 exhaustive words, 20,480 graph/Hall comparisons, and
  74,188 matching-to-energy checks. Independent subset enumeration also
  checked 8,192 one-sided Hall cases through length eight.
- Seed geometry: 1,134 exhaustive prescribed-tail constructions and
  139,752 scalar-replayed edge comparisons, plus four larger explicit
  witnesses. An independent review reran these checks and verified the
  all-length proof. Finite inversion was checked against 1,024 independently
  generated scalar cases and seed ages 0 through 128; a separate census
  verified the ancestry counts on 2,730 centered rows.

The large center-bit payload was reused, not independently regenerated.
Finite checks support the implementations and displayed witnesses. The
all-length conclusions rest on the stated algebraic proofs.

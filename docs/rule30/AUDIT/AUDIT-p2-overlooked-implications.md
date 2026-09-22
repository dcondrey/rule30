# Audit of the recent P2 research

Date: 2026-09-11. Three independent reviews covered the contrast argument,
matching argument, and scientific transfer strategy. No error was found in
the central projection, sign-diversity, matching-optimality, or expiration
identities. The audit found an omitted converse, an underused freedom of
scale, and one small reporting error. None supplies a seed-specific
asymptotic estimate or a solution of P2.

Follow-up: the [gap repairs](RESULTS-p2-gap-repairs.md) implement the full
scale criterion, prove the exact matching/energy bridge and interval-family
deficiency formula, and test the proposed seed-boundary information with
an all-length competing-row construction. The central seed estimate is
still unproved.

**1. Optimized matching is quantitatively equivalent to discrepancy.**

Let z be any nonempty finite sign word, using positions 1,...,N. Set
`S(u)=sum_(t<=u) z_t` and `M=max_(0<=u<=N)|S(u)|`. Let p_i and m_i be the
positions of the i-th positive and i-th negative signs. Pair equal ranks
up to the smaller of the two counts. The exact identities are

\[
p_i=2i-S(p_i),\qquad m_i=2i+S(m_i),
\qquad m_i-p_i=S(p_i)+S(m_i).
\]

At a positive endpoint, `-M+1<=S(p_i)<=M`; at a negative endpoint,
`-M<=S(m_i)<=M-1`. Therefore every pair has separation at most 2M-1.
Exactly `|S(N)|` signs remain unmatched.

Writing U_R for the minimum unmatched count at distance limit R gives

\[
\boxed{U_{2M-1}=|S(N)|,\qquad
M\leq\min_{R\geq0}(U_R+R)\leq2M-1+|S(N)|\leq3M-1.}
\]

The lower bound uses the existing pairing-prefix inequality. The equality
uses the rank pairing above and the unavoidable unmatched total imbalance.
Consequently

\[
\mathrm{P2}\iff\exists R_k=o(N_k)\text{ with }U_{R_k}=o(N_k).
\]

Thus allowing the radius to vary freely gives another exact reformulation
of P2, even up to a universal constant factor in the optimized finite cost.
A radius or matching bound derived independently from the seed could still
be useful, but defining R from M assumes the bound we are seeking.

The distance estimate is sharp. The balanced word
`+^M (-+)^(M-1) -^M` has maximum prefix M. At radius 2M-2 its first M
positive signs have only M-1 eligible negative neighbors; perfect matching
is impossible. Radius 2M-1 suffices by the rank construction.

For the measured k=20 shell, the earlier 1476 unmatched signs remain
unavoidable at R=1024. Rank pairing has maximum separation 2321 and leaves
only the total imbalance, 152 signs. This does not contradict optimality
at fixed R. It shows why the radius is a substantive part of the theorem
being sought, not an incidental implementation choice.

**2. Cancellation need not occur by the square-root scale.**

The recent probes restricted block lengths to at most sqrt(N), or set the
matching radius approximately to sqrt(N). Both are stronger requirements
than P2. This is a more substantial restriction than merely allowing a
longer but fixed wait between contractions.

For an explicit artificial sequence, on every shell N=2^k, k>=4, alternate
runs of H=2^floor(3k/4) plus signs and H minus signs. Each shell has total
sum zero and maximum prefix H. Therefore `M/N=H/N->0`, and assembling
these shells yields density one-half. This example is **not Rule 30**.

Every aligned block of length at most sqrt(N) lies inside one run, so
`V_j=1` for j<=floor(k/2). No contrast occurs in any merge whose parent
block still lies within a run. In particular the four-block diversity
criterion vanishes throughout its previously prescribed domain.

At R=2^floor(k/2), each opposite-sign pair must cross a run boundary.
At most R disjoint pairs can cross one boundary, since their left endpoints
must occupy the preceding R positions. There are N/H-1 boundaries, giving

\[
U_R\geq N-2R(N/H-1)=(1-o(1))N.
\]

When H>=2R, this bound is attained by pairing the R signs on each side of
every boundary at distance R. Thus almost every sign can remain unmatched
at the square-root radius despite the density conclusion being true.

| k | N | H | R | Exact U_R |
|---:|---:|---:|---:|---:|
| 8 | 256 | 64 | 16 | 160 |
| 12 | 4096 | 512 | 64 | 3200 |
| 16 | 65536 | 4096 | 256 | 57856 |

The [earlier ordered-energy result](RESULTS-p2-ordered-energy-audit.md)
already permits any cutoff j_k with `k-j_k->infinity` and `V_(k,j_k)->0`.
The audit correction is to preserve that flexibility in research priorities.
The square-root targets remain valid sufficient conditions for the seed;
these examples neither disprove them on Rule 30 nor make them logically
invalid. Their failure would not justify abandoning the broader routes.

**3. The return scan was stronger than its explanation claimed.**

The [biological experiment report](RESULTS-p2-five-science-explorations.md)
previously attributed possible nonoptimality of its residual lower bound
to checking only consecutive visits to each local state. That explanation
was incorrect and has been corrected.

If a state is visited at t_0<t_1<...<t_m, the signed average on [t_0,t_m)
is the length-weighted average of those on [t_i,t_(i+1)). Its absolute
value cannot exceed the largest absolute consecutive-return average.
Therefore the scan already optimizes over every actual equal-state return
interval in the finite observation horizon. Its reported numbers stand.

This does not establish the optimal bound from every observed transition
constraint: combining constraints in other ways can yield additional
obstructions. Nor does a finite return calculation give an all-time density
bound. The correction strengthens the scope of the finite scan modestly.

**4. Several scientific connections expose the same missing quantity.**

The kinetic projection, echo matching, and queue accumulator are useful
representations, but they do not constitute three independently established
seed mechanisms. Their new analytic identities hold for arbitrary sign
words. The specific seed enters mainly through finite measurements and
counterexamples. No transfer has yet derived the necessary cancellation
from the singleton initial condition.

The practical consequence is to require a proposed next step to explain
that causal link, retain flexible scales, and distinguish a new seed bound
from another equivalence. A sign-diversity certificate is optional, not an
indispensable theorem. It can miss complete cancellation, as the prior
example `(2,2,2,-6)` already shows.

The local failures also remain narrowly scoped: they do not rule out
nonlocal potentials, growing windows, later onsets beyond the ones tested,
or residuals that cancel on average. A matching upper bound must control
collections of deficient neighborhoods, not just the largest single deficit.

**Verification and evidence limits.**

[Audit controls](../../experiments/rule30/p2_research_audit.py) and
[output](../../experiments/rule30/p2-research-audit.json) check all 8190
nonempty sign words through length 12 for the rank-pair bound and unmatched
equality, 32 instances of the sharp family, and the three slow-cancellation
shells above. Run:

```sh
uv run python experiments/rule30/p2_research_audit.py
```

The matching reviewer also independently recounted the earlier million-bit
interval certificate from the stored bytes; all counts agreed. This uses
the same payload, not an independent CA regeneration. The previous
verifier evaluates all 169 stored local witnesses and independently resums
six complete profiles; it does not independently establish that every
stored witness is a global maximizer. The symbolic results do not depend
on that empirical maximum claim. All audit controls passed.

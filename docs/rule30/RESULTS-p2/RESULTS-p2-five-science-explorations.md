# Exploring five scientific transfers to P2

Date: 2026-09-10. **P2 remains open.** This follow-up develops each direction
in the [research memo](RESEARCH-p2-cross-science-transfer.md), with exact
reductions, actual-seed obstruction witnesses, and finite diagnostics.
The scientific papers motivate the questions; none proves a Rule 30 result.

Follow-up, 2026-09-11: the [gap repairs](RESULTS-p2-gap-repairs.md) remove
the scale restriction below, identify equivalent cancellation routes, and
prove why exact seed edges plus recent history cannot supply the missing
origin constraint. The matching queue below has since been proved optimal.

The strongest actionable outcomes are a sharper description of the
multi-scale contrast target, a seed-specific obstruction to simple local
accumulators, and an explicit cancellation algorithm. The fluid and
materials investigations identify hypotheses we should avoid importing.

**1. Kinetic theory: what delayed observability means here.**

Hypocoercivity couples components untouched by instantaneous dissipation
to components that are damped. Modified energies make that coupling
quantitative under specified operator assumptions.
[Dolbeault–Mouhot–Schmeiser, section 1.3](https://arxiv.org/html/1005.1495).

For our temporal shell, fix j and write `u_a=b_(k,j,a)`. Partition this
vector into groups of `m=2^ell` consecutive entries. Let P be the orthogonal
projection that replaces all entries of each group by their group mean.
Then the exact identity is

\[
\boxed{\|(I-P)u\|^2=E_{k,j}-2^{-\ell}E_{k,j+\ell}
 =\sum_{s=0}^{\ell-1}2^{-s-1}D_{k,j+s}.}
\]

Proof: in one group, subtracting its mean leaves squared norm
`sum u_a^2-(sum u_a)^2/m`. Sum over groups and telescope the existing
one-merge identity. Equivalently, the group contribution equals
`m^(-1) sum_(a<b)(u_a-u_b)^2`.

Thus P2-C is precisely a restriction on concentration near the subspace
of groupwise equal block sums:

\[
\|(I-P)u\|^2\geq\eta\|u\|^2-CN.
\]

The observation operator I-P has eigenvalues zero and one. Its kernel has
dimension `(N/2^j)/2^ell`. There is no small positive spectral gap waiting
to be extracted on the full vector space: a whole subspace is invisible.
The missing result must constrain which vectors the seed produces. In
particular, ruling out an exactly invisible vector does not quantitatively
exclude vectors arbitrarily close to that subspace.

**Finite test.** Using every complete shell `k=1,...,28`, with the specified
domain `j+ell<=floor(k/2)`, the minimum relative observed loss is:

| ell | Number of admissible scale pairs | Minimum loss / E | Attained at (k,j) |
|---:|---:|---:|---:|
| 1 | 196 | 0 | (2,0) |
| 2 | 169 | 5/8 | (6,0) |
| 4 | 121 | 3711/4040 | (12,2) |

These exact minima were extracted after the measurement. The preselected
grid `ell in {1,2,4}`, `eta in {1/4,1/2,3/4}` also records the smallest
nonnegative C needed on this finite domain. In particular, ell=2, eta=1/2,
C=0 passes all 169 pairs. No all-scale conclusion follows.

There is a consequential diagnostic trap: with ell=2, eta=1/2, C=1,
**none** of those 169 cases has `eta E-CN>0`. Nonnegativity of the loss
already proves every one of those finite inequalities. A numerical pass
with this remainder would provide no evidence of forced contrast at all.
The C=0 comparison is informative about the tested relative losses;
neither comparison controls future shells.

**Next proof attempt:** find a causal seed constraint that bounds the
projection Pu when its energy dominates N. A proposed augmented state must
retain enough information to justify its transition; the earlier
[mean-only nonclosure](RESULTS-p2-temporal-mean-nonclosure.md) still applies.
This remains the most direct transfer to the intended inequality.

**2. Biological regulation: test whether a local accumulator can exist.**

Integral feedback in chemotaxis accumulates output error in an internal
state, enabling adaptation under the model's assumptions.
[Yi–Huang–Simon–Doyle](https://pmc.ncbi.nlm.nih.gov/articles/PMC18287/).

We tested the concrete template

\[
z_t=B(w_{t+1},(t+1)\bmod p)-B(w_t,t\bmod p)+r_t,
\]

where `w_t=x^t[-r,...,r]` is a centered spatial window. B can be *any*
real-valued function of that window and phase; it is not restricted to
polynomials, linear combinations, or a fitted model.

If `(w_s,s mod p)=(w_t,t mod p)`, telescoping forces

\[
\sum_{v=s}^{t-1}z_v=\sum_{v=s}^{t-1}r_v,
\qquad
\|r\|_\infty\geq\frac{|\sum_{v=s}^{t-1}z_v|}{t-s}.
\]

This gives rigorous obstructions from finite seed computations. It does
not require that the local window evolution be a closed dynamical system.

| Radius | Phase modulus p | Equal-window times | Signed sum between them | Forced residual bound |
|---:|---:|---:|---:|---:|
| 6 | 1 | 6535, 6537 | -2 | at least 1 |
| 6 | 8 | 6989, 6997 | 6 | at least 3/4 |
| 8 | 8 | 8010, 8106 | -20 | at least 5/24 |
| 10 | 1 | 1177, 1407 | 22 | at least 11/115 |

In the first row the identical 13-cell window has integer code 1365 when
cell -6 is bit zero. The two center signs are both -1. Consequently a
phase-free accumulator seeing only those 13 cells cannot even achieve
the uniform residual improvement `|r_t|<1`. The same witness applies to
every smaller centered window. The final row rules out an exact,
residual-free phase-free accumulator through radius 10. The third row
also rules out exact accumulators through radius 8 with phase moduli
1, 2, 4, or 8.

The search checked radii 0,1,2,3,4,6,8,10,12 and phase moduli 1,2,4,8,
both from time zero and from time 4096 through 8192. It found 61 certified
witnesses among 72 combinations. It examines consecutive visits to each
state. This suffices to maximize the absolute return average over every
actual equal-state return interval in the tested horizon: a longer return
interval decomposes into consecutive returns, and its signed average is
their length-weighted average. The resulting bound need not be the strongest
bound obtainable by combining all observed transition constraints. Missing
witnesses do not establish a potential. The late-window checks rule out
those templates starting at 4096, not every possible eventual onset.

Audit correction, 2026-09-11: the earlier explanation incorrectly attributed
possible nonoptimality to scanning only consecutive visits. The recorded
witnesses and numbers are unchanged.

**What survives:** the proposed compensating *spatial sum* Q in the
[current identity](RESULTS-quarter-wave-current-target.md) is not a bounded
center-window observable and is not ruled out. Growing spatial windows,
history states, and signed residual cancellation also remain available.
A family of increasingly accurate approximate potentials is not excluded
by positive bounds at a few fixed radii.

**Next proof attempt:** search nonlocal phase-weighted observables for
`K-1/2=Delta Q+r`, retaining the boundary terms, and bound P+Q together.
Another useful architecture appears in the pairing experiment below: a
finite queue is an explicit accumulator, with unmatched expirations as
its precisely identified residual.

**3. Quantum echoes: construct cancellation, and check whether it is new.**

Digital dynamical decoupling uses structured sign changes to suppress
errors. The borrowed idea is a cancellation architecture, not a claim
that the Rule 30 word is an externally controlled Walsh sequence.
[Hayes–Khodjasteh–Viola–Biercuk](https://arxiv.org/html/1109.6002).

We implemented a causal-in-time matching algorithm. Scan the shell signs,
retaining unmatched indices in a queue. Expire an index when it is farther
than R from the current position. An incoming opposite sign pairs with the
oldest retained index; otherwise enqueue it. The queue always contains
only one sign. No optimality of this matching is asserted or needed.

Every pair has opposite signs and separation at most R. If U indices are
unmatched at the end, including expired indices, then `M<=U+R`. Complete
pairs in any prefix cancel, and at most R left endpoints can belong to
pairs crossing its endpoint. This controls all prefixes, not just a shell's
total discrepancy.

The finite algorithm used `R=2^floor(k/2)` and four times that radius on
shells k=4,...,18. Selected records for the smaller radius are:

| k | N | R | U | Certified M upper bound U+R | Actual M |
|---:|---:|---:|---:|---:|---:|
| 8 | 256 | 16 | 8 | 24 | 12 |
| 12 | 4096 | 64 | 56 | 120 | 65 |
| 16 | 65536 | 256 | 356 | 612 | 367 |
| 18 | 262144 | 512 | 104 | 616 | 330 |

The indices constitute an explicit finite certificate. There is no proved
asymptotic bound on U for this algorithm.

**Connection back to biology.** Let Q_t be the signed sum in the queue
immediately before processing the next sign, and e_t the signed sum of
tokens expired during that step. Pairing removes a net zero, so

\[
Q_{t+1}-Q_t=z_t-e_t.
\]

The queue has at most R+1 tokens, making it a bounded accumulator. The
unproved cancellation is isolated in the expiration sequence. Counting
absolute expirations recovers a sufficient unmatched-token bound; bounding
their signed sum could be weaker. This identity alone does not control
either quantity on the seed.

**A reduction that prevents double-counting progress.** If instead we pair
opposite signs arbitrarily *within each aligned L-block*, then

\[
U=\sum_a|b_a|\leq\sqrt{(N/L)E_j}=N\sqrt{V_j},\qquad R\leq L-1.
\]

Thus this particular echo construction yields exactly the already known
energy-prefix bound. It is not an independent analytic breakthrough.
The queue may pair across block boundaries, but needs a new seed-specific
expiration estimate to add anything substantive.

**Next proof attempt:** derive a Rule 30 restriction on long-lived unmatched
tokens or on the signed expiration current. A bounded-memory matcher is
an explicit test object for such a restriction; it is not a shortcut for
proving the restriction.

**4. Fluid mechanics: coherence can persist without defeating P2.**

Enhanced dissipation studies how transport and diffusion combine, and how
coherent modes obstruct relaxation. The relevant fluid theorem operates
on the mean-zero subspace; it does not select an initially unknown mean.
[Constantin–Kiselev–Ryzhik–Zlatoš](https://sites.math.duke.edu/~kiselev/relaxation.pdf).

We measured `delta_(k,j)=D_(k,j)/(2E_(k,j))` below j=floor(k/2). Apart from
the known k=2 zero-loss case, every tested loss for k=3,...,28 is at least
3/10, attained at (7,1). For k=28 the smallest is
`33471477/67238768`, approximately 0.4978. Consequently this finite domain
contains no long run of losses below 1/4. This does not bound the duration
of coherent episodes at untested scales.

There is also a useful all-scale counterexample to making *short* coherence
lifetimes a necessary condition. This is an artificial sign sequence,
**not Rule 30**. On shell k>=4, set `m=floor(sqrt(k))` and repeat runs
of `2^m` plus signs followed by `2^m` minus signs until the shell is filled.
Then

\[
M_k=2^m=o(2^k),\quad V_{k,j}=1\ (0\leq j\leq m),
\quad D_{k,j}=0\ (0\leq j<m).
\]

Every shell has total sum zero, and its maximum excursion is sublinear,
so the assembled sequence satisfies the density-one-half conclusion.
Yet for any fixed ell, eta>0, and finite C, take j=m-ell for sufficiently
large k. The condition j+ell<=k/2 holds, whereas P2-C would require
`1<=1-eta+C2^(-j)`, which eventually fails. This proves strictness of the
fixed-window contraction target, not its failure for Rule 30.

**Next proof attempt:** tolerate coherence whose lifetime grows with scale,
provided enough contrast occurs before blocks approach shell length.
If a fixed-ell certificate resists proof, this example gives a precise
reason to try accumulated loss without a fixed waiting-time bound.

**5. Materials science: measure the right fluctuation, with a biased control.**

Hyperuniformity concerns unusually suppressed large-window number
fluctuations. It does not prescribe the number density itself.
[Torquato–Stillinger](https://arxiv.org/abs/cond-mat/0311532).

For every overlapping L-window contained in the k=20 shell, we computed
the exact first and second moments of its signed sum b. The table reports
centered variance divided by L; exact rational values are in the artifact.

| L | Var(b)/L | Variance of number of ones / L |
|---:|---:|---:|
| 16 | 0.999094 | 0.249773 |
| 64 | 1.002666 | 0.250667 |
| 256 | 0.986317 | 0.246579 |
| 1024 | 0.978930 | 0.244733 |
| 4096 | 1.054469 | 0.263617 |

These finite measurements show approximately volume-order fluctuations
over this range. They supply no observed suppression toward zero of
variance/L and no asymptotic classification. Independent fair signs would
have signed-sum variance L, but that is only a comparison scale, not a
model assumed for Rule 30. The overlapping samples are not independent.

**Exact biased Rule 30 control.** The spatially period-12 rows

```
100111110000
111100001001
000010011111
```

form a three-step cycle under Rule 30. Their coordinate-zero trace is
`110110...`, of density 2/3. Average the number of ones in a length-L window
over its three temporal starting phases. The variance is exactly zero
when 3 divides L and 2/9 otherwise. It is bounded, hence strongly
suppressed relative to L, despite the wrong density. This is a valid
Rule 30 spacetime diagram, but **not the lone-seed orbit**.

For the signed block means in our target,
`V=Var(block mean)+(shell signed mean)^2`. Centering at the measured mean
would remove the second term. The periodic control shows why even a strong
fluctuation theorem must be accompanied by a mechanism selecting one-half.

**Next proof attempt:** seek only the uncentered second-moment decay needed
by P2 at a sub-shell scale. Do not impose hyperuniformity as an extra goal,
and preserve the DC component in every spectral or variance calculation.

**Evidence, reproduction, and limits.**

- [Exploration code](../../experiments/rule30/p2_cross_science_explore.py)
  and [exact output](../../experiments/rule30/p2-cross-science-explore.json).
- [Independent verifier](../../experiments/rule30/verify_p2_cross_science.py)
  and [verification output](../../experiments/rule30/p2-cross-science-independent.json).
- The stored Wolfram billion-bit payload was read through time
  536870911. Its alignment and bit order were uniquely located using a
  generated 64-bit prefix, then checked against 8192 generated bits.
  The entire large prefix was **not** independently regenerated as a CA.
  File SHA-256:
  `15858d84f4902cc61d9d99bff1ce32047ba17fea0422dc421df34cfad4229612`.
- All 12 earlier shell records agree exactly. Direct byte population counts
  independently verify 66 energies in shells k=20,24,28 without recursive
  merging. Full shell energies and contrasts use signed 64-bit arithmetic;
  the bound `E_j<=N2^j<=2^56` prevents overflow on the tested domain.
- The local-return witnesses were independently replayed with fixed
  coordinates, after expanding-coordinate generation and 65 scalar-row
  checks. All 61 witnesses pass. These finite identities genuinely exclude
  their specified accumulator templates.
- Universal matching checks cover every sign word of lengths 1 through 9
  at four radius choices: 4088 checks. Independent controls include
  constant and alternating words. Projection checks cover 625 integer
  vectors; the periodic control checks all 36 Rule 30 gates and 100 lengths.
  The verifier also checks 13 artificial square-wave shells and 1024
  instances of the equivalence between aligned matching and the energy bound.

Run from the repository root:

```sh
uv run python experiments/rule30/p2_cross_science_explore.py
uv run python experiments/rule30/verify_p2_cross_science.py
```

The research priority remains the seed-specific temporal contrast bound.
The accumulator and pairing constructions now have explicit obstruction
tests and residuals to target. No finite profile, external mixing theorem,
or count of these reductions establishes an asymptotic advance for P2.

Follow-up: [weighted sign diversity and exact matching obstructions](RESULTS-p2-cancellation-mechanisms.md)
proves a concrete sufficient contrast certificate, establishes queue
optimality, and directly counts an unavoidable matching deficit in seed data.

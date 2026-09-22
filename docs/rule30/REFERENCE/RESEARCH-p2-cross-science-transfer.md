# P2: mechanisms to borrow from other sciences

Research date: 2026-09-10. This is a literature-informed research proposal,
not a proof of cancellation for Rule 30. The connections and priorities
below are our proposed transfers; the cited authors do not claim results
about the Rule 30 lone seed. No new seed computation was performed.

The target remains the actual orbit `x^t=F^t(delta_0)`, with
`z_t=1-2x_0^t` and `sum_(t<T) z_t=o(T)`. Definitions of shell energy E,
normalized energy V, contrast D, and the sufficient inequality P2-C are in
[the dependency map](PRIZE-PROBLEM-DEPENDENCIES.md).

The most useful connections concern mechanisms that enforce cancellation,
not visual resemblance to randomness. Three deserve a concrete proof search:
delayed dissipation from kinetic theory, integral regulation from biology,
and structured sign reversal from quantum control. Fluid mixing and
materials science supply useful diagnostics and warnings about centering.

**1. Kinetic theory: hypocoercivity and delayed dissipation.**

In kinetic equations, collisions can dissipate some components while leaving
others untouched. Transport couples the undamped components to dissipative
ones. Dolbeault, Mouhot, and Schmeiser construct a modified energy with a
cross term and prove decay under microscopic and macroscopic coercivity
and auxiliary operator bounds. Thus an instantaneous dissipation kernel
does not by itself prevent decay. Their theorem concerns specified linear
operators on a Hilbert space, not arbitrary nonlinear dynamics.
[Primary paper, section 1.3](https://arxiv.org/html/1005.1495).

For our block sums, a pair `(u,v)` splits into its mean `(u+v)/2` and
contrast `(u-v)/2`. A zero D says that the current contrast is blind to
some nonzero energy. The proposed transfer is to ask what Rule 30 forces
that invisible energy to do over several merges. This is the precise role
of the desired inequality

\[
\sum_{s=0}^{\ell-1}2^{-s-1}D_{k,j+s}
\geq \eta E_{k,j}-CN.
\]

This is analogous to an observability estimate: enough accumulated output
must detect substantial stored energy. It is not already a consequence of
the analogy.

Concrete search: retain block sums together with causal boundary data and
signed information discarded by a merge. Seek either the displayed bound
or an augmented energy comparable to V whose change exposes this contrast.
The [mean nonclosure result](RESULTS-p2-temporal-mean-nonclosure.md) explains
why the extra state needs justification. A finite matrix derived from a
truncated state is useful only after proving that the state retains the
relevant dependencies.

First falsification test: characterize the common kernel of all contrast
observations in the proposed merge window. Constant vectors of child sums
belong to it. Therefore there is no coercive estimate on all possible
vectors without a remainder or a restriction. The actual work is to show
that seed-realizable vectors cannot carry arbitrarily large energy in,
or sufficiently near, this kernel. Excluding exact zero contrast alone
does not establish a quantitative lower bound.

An additional limitation matters: the kinetic theorem studies relaxation
around the equilibrium selected by conserved mass. It does not determine
that mass. We must not silently subtract the unknown temporal mean of
Rule 30 and then call decay of the centered field a proof of P2.

**2. Systems biology: integral feedback and perfect adaptation.**

Yi, Huang, Simon, and Doyle identify integral feedback in a model of
bacterial chemotaxis: an internal variable accumulates output error,
allowing the regulated output to return to its set point under the model's
conditions. This is a mechanism for fixing an average without requiring
independent fluctuations.
[Primary paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC18287/).

The transferable algebra is simple. If an independently defined state
observable B satisfies

\[
z_t=B(x^{t+1})-B(x^t)+r_t,
\]

then

\[
\sum_{t<T}z_t=B(x^T)-B(x^0)+\sum_{t<T}r_t.
\]

A sublinear endpoint and sublinear residual establish P2 pathwise. Here
an identity is only the first obligation: B must be derived from the CA
state, and its growth and residual need independent bounds. Defining B
as the accumulated center discrepancy merely restates the target.

Our [existing current identity](RESULTS-quarter-wave-current-target.md)
already implements part of this structure:

\[
x_0^t-\tfrac12=P(x^{t+1})-P(x^t)+K(x^t)-\tfrac12.
\]

The new search suggested by biology is a *second compensating observable*
Q, satisfying

\[
K(x^t)-\tfrac12=Q(x^{t+1})-Q(x^t)+r_t.
\]

Then it is the growth of P+Q that matters; separate bounds on P and Q are
unnecessary. One can search phase-weighted local pattern sums, retaining
all support-edge terms. Exact identity candidates can be checked by
expanding the Boolean update over the integers. A proposed identity that
holds only on the seed still needs an all-time seed justification.

A useful relaxed certificate is a family indexed by h. For each fixed h,
prove a decomposition with endpoint `o(T)` and `|r_t|<=epsilon_h` for all
seed times, where `epsilon_h -> 0`. Divide the telescoping identity by T,
take limsup in T at fixed h, and then let h grow. This is a sufficient
certificate template, not a newly established estimate.

Briat, Gupta, and Khammash's antithetic controller supplies a further
design idea: differences of two internal species can eliminate a shared
reaction term. Its stochastic adaptation conclusions have ergodicity and
stability requirements; they cannot be transferred to this specified
deterministic orbit. Borrow the cancellation architecture only.
[Primary paper](https://doi.org/10.1016/j.cels.2016.01.004).

**3. Quantum control and NMR: echo cancellation.**

Walsh dynamical decoupling uses designed sign-switching sequences to
suppress environmental errors. Hayes, Khodjasteh, Viola, and Biercuk
relate digital sequence structure to cancellation performance.
[Primary paper](https://arxiv.org/html/1109.6002).

The potential transfer is a geometric pairing of opposite center signs,
rather than a claim that all Walsh coefficients are small. For P2, we need
cancellation of the unmodulated sum; an externally imposed modulation
that cancels it would change the problem.

Here is a concrete deterministic certificate. On each shell of N signs,
construct disjoint pairs of positions with opposite signs, leaving at most
U unmatched positions, with every pair separated by at most R positions.
Then the maximum absolute shell prefix sum satisfies

\[
M\leq U+R.
\]

Proof: complete pairs inside a prefix cancel. A pair crossing the prefix
boundary has its left endpoint within R positions of that boundary, so
there are at most R such pairs. Unmatched positions contribute at most U.
Thus `U_k+R_k=o(2^k)` would prove P2, including excursions inside shells.

This certificate does not require a fixed lag or adjacent pairing. The
research task is to construct the pairing from the seed's causal structure
and prove the two bounds. Pairing arbitrary observed opposite bits after
looking at the full word provides no such bounds. A proposal based on
complementing configurations must explicitly check Rule 30's update and
the seed boundary; bit complementation is not an automatic symmetry.

**4. Fluid mechanics: stirring, enhanced dissipation, and coherent modes.**

Constantin, Kiselev, Ryzhik, and Zlatos characterize relaxation-enhancing
incompressible flows using the absence of nonconstant sufficiently regular
eigenfunctions. Their analysis separates transport from diffusion and
identifies coherent structures that obstruct rapid decay.
[Primary paper, Theorems 1.2 and 1.4](https://sites.math.duke.edu/~kiselev/relaxation.pdf).

The transferable question is whether biased temporal block sums can remain
coherent across many scales. Instead of merely recording typical losses,
look for extended runs of small relative loss and retain the causal data
that support them. A proof would need to limit their duration or total
energy on the seed.

The decisive limitation is visible in the fluid equations: with periodic
or no-flux boundaries, stirring and diffusion preserve the scalar's mean.
They homogenize it to that mean, not to a prescribed value. The paper
explicitly restricts its decay analysis to mean-zero functions. For Rule
30, choosing the mean to be zero in sign convention would assume P2.
Also, a merge index is not physical CA time; an evolution relating them
must be derived rather than inferred from a cascade analogy.

This direction is useful as an obstruction search supporting item 1. It
does not supply an independent reason for density one-half.

**5. Materials science: hyperuniformity and number fluctuations.**

Torquato and Stillinger study number variance in observation windows and
suppression of long-wavelength density fluctuations in point patterns,
including disordered ones. Order need not mean periodicity.
[Primary paper](https://doi.org/10.1103/PhysRevE.68.041113).

For our aligned blocks of length L, put `m_a=b_a/L`, and let Q=N/L.
The exact finite-sample decomposition is

\[
V=\frac1Q\sum_a m_a^2
 =\frac1Q\sum_a(m_a-\bar m)^2+\bar m^2,
\qquad \bar m=\frac1N\sum_{t=N}^{2N-1}z_t.
\]

Consequently small variance *around the measured mean* leaves the squared
bias completely uncontrolled. This distinguishes the materials diagnostic
from our second moment around the prescribed target zero. Hyperuniformity
also concerns a stronger fluctuation suppression than P2 requires, and
by itself does not select density one-half.

Useful transfer: retain both pieces in every block-fluctuation diagnostic.
If fitting removes the DC component, it has removed part of the theorem
we need. Measurements across translated windows must also not silently
replace a statement about this one orbit by an ensemble assertion.

**A related route screened out: deterministic homogenization.**

Kelly and Melbourne prove diffusion limits for classes of deterministic
fast-slow systems, with suitable dynamical hypotheses. Their forcing is
assumed centered under the fast flow. This explains how deterministic
motion can produce stochastic limits, but does not establish the missing
centering or typicality of our seed.
[Authors' paper summary](https://math-ianmelbourne.github.io/papers/fastslow2.html).
It is not the first theorem to try importing for P2.

**Recommended order of proof work.**

1. Pursue a seed-specific delayed-observability certificate for temporal
   contrast, with explicit treatment of its common kernel and near-kernel.
2. Search a compensating current observable using the integral-feedback
   architecture; require a growth bound as well as an algebraic identity.
3. Search for causal opposite-sign pairings with sublinear unmatched count
   and displacement. This is a distinct sufficient route if the scale
   contraction target is unnecessarily rigid.

These are priorities based on structural fit, not estimated probabilities
of solving P2. None of the outside results presently closes the seed gap.

Follow-up: [five concrete explorations](RESULTS-p2-five-science-explorations.md)
develop the transfers, test the contrast target, construct pairings, and
give actual-seed obstructions to bounded-window accumulator identities.

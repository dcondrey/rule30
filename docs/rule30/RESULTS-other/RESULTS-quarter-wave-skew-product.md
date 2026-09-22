# Spatial phase, spectral resonance, and the Rule 30 quarter-wave target

The spatial skew product can be constructed exactly. Its phase matrix has
four unit-modulus eigenvalues, and its invariant measures automatically have
uniform phase marginals. Neither fact forces the quarter-wave potential to
cancel. The relevant quantity is a correlation between cell value and phase.

This report gives explicit counterexamples to the proposed implications,
an exact operator formulation, and a sufficient spectral criterion. The
criterion is not proved for the lone seed. No P1, P2, or P3 solution follows.

## 1. What the cited physics does and does not establish

The references concern genuine physical systems, but three author
attributions require correction:

| Identifier | Actual paper and authors |
| --- | --- |
| gr-qc/0504114 | *Constraint damping in the Z4 formulation and harmonic gauge*, Gundlach, Martin-Garcia, Calabrese, Hinder [^1] |
| 1106.2254 | *Conformal and covariant formulation of the Z4 system with constraint-violation damping*, Alic, Bona-Casas, Bona, Rezzolla, Palenzuela [^2] |
| PMID 25083656 / 1404.1072 | *Time-Reversal-Invariant Z4 Fractional Josephson Effect*, Zhang and Kane [^3] |
| 1507.08881 | *Z4 Parafermions & the 8pi-periodic Josephson effect in interacting Rashba nanowires*, Pedder, Meng, Tiwari, Schmidt [^4] |

The related damping paper involving Bernuzzi and Hilditch is by Weyhausen,
Bernuzzi, and Hilditch, arXiv:1107.5539 [^5].

In numerical relativity, Z4 introduces a four-vector constraint field Z_mu;
the label is not the cyclic group Z/4Z. Gundlach et al. analyze damping after
adding specified terms to specified differential equations. Their exception
for spatially constant modes is not a theorem that an arbitrary four-phase
system has a rank-one undamped subspace. The result also does not justify
adding damping to Rule 30 while claiming to preserve its seed trajectory.

The Josephson papers concern interacting quantum systems with superconducting
phase, protected degeneracies, and particular symmetry assumptions. Those
structures are not supplied by labeling four spatial residue classes. An
expanding light cone alone defines neither the Hamiltonian family nor the
index needed to transfer a spectral-flow theorem. A proposed discrete index
would need its own definition, conservation proof, and implication for the
observable P. None is currently provided.

These observations limit the proposed applications, not the validity of the
physics results in their stated settings.

## 2. The proposed protected zero mode fails on the seed

The real multilinear extension of the Boolean Rule 30 gate is

\[
f(p,q,r)=p+q+r-qr-2pq-2pr+2pqr.
\]

Its derivative at the zero configuration is the real Rule 150 operator

\[
(Lx)_j=x_{j-1}+x_j+x_{j+1},\qquad \lambda(k)=1+2\cos k.
\]

At k=pi/2 its eigenvalue is 1; zero refers to L-I. This linearization has
no damping gap: its multiplier at k=0 is 3. A Boolean derivative over GF(2)
is a different object and carries no automatic real spectral-decay estimate.

The actual half-line weight is
w_j=sin(pi j/2) for j>0 and zero otherwise. It satisfies

\[
(L-I)^*w=\delta_0,
\]

so it has a boundary source. The exact current identity gives

\[
P_{t+1}-P_t=c_t-K_t.
\]

For the actual seed, P_0=0, c_0=1, K_0=0, and P_1=1. Zero initial P
therefore does not protect P from excitation. The seed's full Fourier
transform is initially 1 at every frequency, so zero half-line P also does
not mean that the full quarter-wave Fourier mode is absent.

There is an explicit later excitation with no center boundary contribution:

\[
P_{21}=0,\quad c_{21}=0,\quad K_{21}=3,\quad P_{22}=-3.
\]

Even the full-line sine component, which has no linear boundary source,
changes from 0 at times zero and one to -1 at time two. Nonlinear evolution
does not preserve its zero projection. A spectral decomposition of a frozen
linearization cannot discard this forcing.

## 3. The exact spatial skew product

Let X={0,1}^Z, let sigma be the left shift, (sigma x)_j=x_(j+1), and let
F be Rule 30. On X times Z/4Z define two commuting actions:

\[
S(x,a)=(\sigma x,a+1),\qquad A(x,a)=(Fx,a).
\]

Spatial displacement advances spatial phase. Time evolution at fixed
physical coordinates does not advance that phase. Using (Fx,a+1) instead
would attach a temporal phase and would not represent P_t without an
additional coordinate transformation.

The phase transition matrix, with source phases indexing rows, is

\[
C=\begin{pmatrix}
0&1&0&0\\0&0&1&0\\0&0&0&1\\1&0&0&0
\end{pmatrix}.
\]

Its eigenvalues are 1,i,-1,-i. All have modulus one. Its unique stationary
phase distribution is uniform, but powers of C cycle; there is no damping
of the other three phase modes.

The exact Koopman operator on joint observables is

\[
(U_S f)(x,a)=f(\sigma x,a+1).
\]

Writing f(x,a)=sum_(k=0)^3 f_k(x)i^(ka) gives

\[
U_S[f_k(x)i^{ka}]=i^k f_k(\sigma x)i^{ka}.
\]

This is a four-sector decomposition with an entire space of configuration
observables in each sector. It is not a four-dimensional model of Rule 30.
The quarter-wave observable is

\[
g(x,a)=(\mathbf1_{a=1}-\mathbf1_{a=3})x_0
       =\operatorname{Im}(i^a x_0).
\]

The phase matrix alone cannot determine its evolution. Even the four
phase-conditioned one-cell means do not close under F: the fair Bernoulli
measure and the equal mixture of the all-zero and all-one rows both have
one-cell mean 1/2 at every phase. Their next one-cell means are respectively
1/2 and 0. Higher-block information is indispensable.

## 4. Exact counterexamples to phase balance and unique-ergodicity claims

Any S-invariant probability nu has uniform phase marginal. Invariance gives
nu(a=j)=nu(a=j-1), and the four masses sum to one. This includes every
invariant measure supported on a periodic S-orbit.

Nevertheless, take x=(0100)^Z with x_1=1 and initial phase zero. The four
points S^j(x,0), 0<=j<4, form a single periodic orbit. Its uniform measure
is the unique invariant probability on that orbit, visits every phase
equally, and satisfies

\[
\int g\,d\nu=1/4.
\]

Thus unique ergodicity restricted to one joint orbit closure is insufficient.
Unique ergodicity on an entire product K times Z/4Z would be a stronger
hypothesis: because mu times the uniform phase measure is invariant whenever
mu is sigma-invariant, uniqueness on the entire product would force a
product measure. The four-orbit example does not refute that stronger
condition, which is not established on an appropriate seed-generated space.

Even simultaneous spatial and temporal invariance is insufficient. The
exact twelve-cell Rule 30 cycle

```text
100111110000 -> 111100001001 -> 000010011111 -> 100111110000
```

has quarter-wave charge -1 in each row. Average over its three temporal
phases and twelve simultaneous spatial shifts/phase increments. The resulting
measure is invariant under both S and A, has uniform phase marginal, and
has integral g=-1/12. This is a periodic control, not the lone seed.

## 5. Measures that actually represent the growing seed rows

Let x^t=F^t(delta_0). Since x_i^t=0 for i>t, define for t>=1

\[
\nu_t=\frac1t\sum_{j=1}^t
       \delta_{(\sigma^j x^t,\,j\bmod4)},\qquad
\frac{P_t}{t}=\int g\,d\nu_t.
\]

The difference S_*nu_t-nu_t consists of the endpoint at j=t+1 minus
the endpoint at j=1, divided by t. Thus its action on a bounded test
function has magnitude at most 2||f||_infinity/t. Every weak accumulation
measure nu is S-invariant and has uniform phase marginal.

Compactness and continuity of g give the exact criterion

\[
P_t=o(t)\quad\Longleftrightarrow\quad
\int g\,d\nu=0\text{ for every accumulation measure of }\nu_t.
\]

The required equality is
nu(x_0=1,a=1)=nu(x_0=1,a=3), not merely nu(a=1)=nu(a=3).
This is an exact reformulation, not a proof that the equality holds.

One must also retain the order of limits. Each fixed finite-support row has
only the zero configuration's point mass as a spatially invariant probability
on its spatial orbit closure. This says nothing uniform about row x^t
sampled in a window of length t. Taking an infinite spatial window first
would discard the growing active region under investigation.

Likewise, nu_(t+1) differs from A_*nu_t by O(1/t) on bounded test functions,
but individual accumulation measures need not be A-invariant. They may be
permuted by A. Temporal Cesaro averaging adds A-invariance but weakens the
pointwise-in-t question and still admits the preceding periodic control.

## 6. A sufficient spectral criterion without full mixing

Let mu be a weak accumulation measure of the unmarked spatial measures

\[
\mu_t=\frac1t\sum_{j=1}^t\delta_{\sigma^j x^t}.
\]

It is sigma-invariant. Write h(x)=x_0 and let sigma_(h,mu) be the spectral
measure of h for the unitary shift operator U_sigma on L2(mu). In particular,
an atom at z corresponds to h's squared projection onto that eigenvalue's
eigenspace. No assertion of existence of a unique limiting mu is needed.

**Sufficient condition.** If every such mu satisfies

\[
\boxed{\sigma_{h,\mu}(\{i,-i\})=0,}
\]

then P_t=o(t), and hence max_(s<=T)|P_s|=o(T).

Proof: take an accumulation measure nu of the marked measures and let mu
be its base projection. Put I=int i^a h(x) dnu. Invariance under S gives,
for every positive integer L,

\[
I=\int i^a\left[\frac1L\sum_{j=0}^{L-1}i^j h(\sigma^j x)\right]d\nu.
\]

Cauchy-Schwarz implies

\[
|I|^2\le\left\|\frac1L\sum_{j=0}^{L-1}i^j U_\sigma^j h\right\|_{L^2(\mu)}^2
\longrightarrow \sigma_{h,\mu}(\{-i\}).
\]

The limit follows directly from the spectral representation: the squared
geometric average tends to zero at every z except z=-i, where it equals
one, and is bounded by one. Since h is real, the atoms at i and -i have
equal mass. Under the stated hypothesis I=0, so int g dnu=Im(I)=0. The
accumulation-measure criterion proves the assertion.

This supplies a precise necessary obstruction to nonzero subsequential
phase bias: if that bias has magnitude epsilon, some corresponding base
measure has coordinate spectral mass at -i at least epsilon squared.
Conversely, the existence of a spectral atom need not give a nonzero
imaginary correlation in the actual marked measure. The sufficient condition
is not claimed necessary.

This concerns **spatial** spectra of limiting growing-row distributions.
It is different from the earlier **temporal** Thue-Morse/residual spectra.
Absolutely continuous spectrum, positive entropy, or full unique ergodicity
is not required by this criterion. The absence of the two specified atoms
has not been proved for any required family of seed accumulation measures.

## 7. A finite-block form of the missing estimate

For a length L define a local complex quarter-wave sum and its mean square:

\[
B_{L,j}^{(t)}=\sum_{r=0}^{L-1}i^r x_{j+r}^t,\qquad
V_{t,L}=\frac1{tL^2}\sum_{j=1}^t|B_{L,j}^{(t)}|^2.
\]

Comparing the global quarter-wave sum with the average of its L translates
changes only endpoints. Cauchy-Schwarz then gives the deterministic bound

\[
\boxed{\frac{|P_t|}{t}\le\sqrt{V_{t,L}}+\frac{L-1}{t}.}
\]

Thus a proved seed-specific estimate V_(t,L(t))->0 at lengths L(t)=o(t)
would suffice. It controls both quarter-wave quadratures and may be stronger
than necessary for the sine component P. The inequality alone supplies no
decay of V. It is an explicit certificate target retaining correlations
within spatial blocks, rather than an assumed four-state Markov closure.

The [finite-origin construction](RESULTS-quarter-wave-origin-obstruction.md)
also shows why a proof cannot discard the left initial data: arbitrary
left-supported initial rows can generate maximal quarter-wave bias and
quadratic injections into either scalar or two-quadrature energy. Those
counterexamples do not reject an inequality on the designated seed.

## 8. Verification and unresolved status

The [exact verifier](../../experiments/rule30/quarter_wave_skew_audit.py) and
[JSON record](../../experiments/rule30/quarter-wave-skew-audit.json) check the
phase eigenvectors, the biased uniquely ergodic four-cycle, the jointly
invariant three-by-twelve example, one-cell moment nonclosure, actual seed
mode excitations, 512 endpoint identities for cylinder measures, and 640
spatial block-energy inequalities through time 128. Symbolic arguments above
supply the all-size statements.

The spectral criterion and finite-block bound remain conditional. They do
not establish the spatial milestone, and even that milestone would leave
the centered-current cancellation required for P2 unproved. P1 and P3 are
also not resolved by these constructions.

For the subsequent exact doubling identity for V, and counterexamples to
inferring infinite mixing from a finite transfer gap or bounded MPS
truncation, see the [variance and approximation audit](RESULTS-finite-gap-mps-and-variance.md).
Its contraction formula retains the spatial boundary term. The required
uniform accumulated contraction on the actual seed remains open.

## Sources

[^1]: Gundlach, Martin-Garcia, Calabrese, Hinder. [Constraint damping in the Z4 formulation and harmonic gauge](https://arxiv.org/pdf/gr-qc/0504114), 2005.
[^2]: Alic, Bona-Casas, Bona, Rezzolla, Palenzuela. [Conformal and covariant formulation of the Z4 system with constraint-violation damping](https://arxiv.org/abs/1106.2254), 2011/2012.
[^3]: Zhang, Kane. [Time-Reversal-Invariant Z4 Fractional Josephson Effect](https://arxiv.org/abs/1404.1072), 2014; [PMID 25083656](https://pubmed.ncbi.nlm.nih.gov/25083656/).
[^4]: Pedder, Meng, Tiwari, Schmidt. [Z4 Parafermions & the 8pi-periodic Josephson effect in interacting Rashba nanowires](https://arxiv.org/abs/1507.08881), 2015/2016.
[^5]: Weyhausen, Bernuzzi, Hilditch. [Constraint damping for the Z4c formulation of general relativity](https://arxiv.org/abs/1107.5539), 2011/2012.

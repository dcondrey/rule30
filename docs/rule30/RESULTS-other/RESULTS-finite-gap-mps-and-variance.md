# Finite transfer gaps, tensor truncation, and exact spatial variance loss

The proposed finite-matrix and tensor-network implications are false without
additional hypotheses. Exact counterexamples below separate a fitted
finite-memory model from an infinite process, a finite tensor representation
from mixing, and fair right input from fair center output. None is a
counterexample to the Rule 30 lone-seed conjectures.

The usable part of the proposal is the spatial quarter-wave mean square.
An exact doubling identity, including the boundary loss, is proved below.
It gives strict decrease on every nonzero finite positive row, but that
decrease is not uniform on growing rows. The missing seed-specific estimate
remains unproved.

## 1. A finite gap can coexist with an exactly periodic underlying process

For every k>=1, choose a binary de Bruijn cycle of order k+1, of length
M=2^(k+1), and choose its starting phase uniformly. This defines a stationary
periodic process. Each block of length k+1 occurs exactly once in the cycle;
every shorter block therefore has its fair Bernoulli frequency.

Existence at every k follows by taking an Euler tour of the directed graph
whose vertices are k-bit words and whose edges append one bit while deleting
the first. Each vertex has indegree and outdegree two, and appending any
desired k-bit word reaches that vertex. The graph is strongly connected and
Eulerian. Its edges are the distinct (k+1)-bit words.

Construct the spatial transition matrix T_k from the observed conditional
probabilities of the next bit given the previous k. Every k-block is followed
once by zero and once by one, hence

\[
T_k(w,\operatorname{suffix}_k(wb))=1/2,\qquad b\in\{0,1\}.
\]

After k independent transitions in this fitted chain all original bits
have been replaced, so

\[
\boxed{T_k^k=2^{-k}\mathbf1\mathbf1^T.}
\]

The matrix is primitive. Its eigenvalues consist of a simple 1 and zeros,
so its modulus spectral gap is 1. Its k-step Dobrushin coefficient is zero:
every row of T_k^k is the same probability vector.

The underlying process nevertheless repeats exactly after M positions.
Its mean is 1/2 and

\[
\operatorname{Cov}(X_0,X_{mM})=1/4\quad(m\ge1).
\]

It has zero entropy rate and is not mixing. Its exact (k+1)-block transition
is a deterministic permutation cycle, whose modulus spectral gap is zero.
The inferred k-block transition probabilities are correct as one-step
conditional probabilities; iterating them assumes a Markov property that
the actual process does not have at order k.

For example, the cycle `00010111` contains every three-bit block once.
The fitted two-block matrix has T_2^2 equal to the matrix with all entries
1/4, while the process retains covariance 1/4 at lag eight. Its coordinate
spectral measure even has an atom of mass 1/32 at each of the quarter-turn
frequencies, despite that fitted gap of 1.

The process in this construction depends on k. There is no claim that one
nonmixing process has fair block frequencies at every finite length.

Perron-Frobenius and finite-chain convergence theorems concern the matrix
to which they are applied [^1]. A finite certificate can establish an
infinite-system result when it proves an exact representation or a uniform
contraction bound for the actual conditional laws, including the omitted
boundary conditions and approximation errors. A positive gap for a fitted
finite block matrix alone supplies neither requirement.

## 2. Exact finite bond dimension does not imply mixing

Let a_j=j modulo 2. Both a and its complement are fixed configurations of
Rule 30: the local neighborhoods 010 and 101 return their middle bits.
The measure

\[
\mu=\tfrac12\delta_a+\tfrac12\delta_{1-a}
\]

is invariant under both Rule 30 and spatial translation. It has fair
single-site marginals and covariance

\[
\operatorname{Cov}_\mu(x_i,x_j)=\frac{(-1)^{i-j}}4.
\]

Thus it has nondecaying spatial memory. In each individual realization,
the center column is constant, of density zero or one.

All its finite-dimensional distributions have an exact nonnegative
bond-dimension-two representation. With row boundary vector l=(1/2,1/2),
column vector r=(1,1)^T, and matrices

\[
A_0=\begin{pmatrix}0&1\\0&0\end{pmatrix},\qquad
A_1=\begin{pmatrix}0&0\\1&0\end{pmatrix},
\]

the probability of w_1...w_N is l A_(w_1)...A_(w_N) r. It equals 1/2 on
each of the two alternating words and zero otherwise. No truncation is
needed. In the normalized square-root representation, each nontrivial
bipartition has two Schmidt weights 1/2, entropy log 2, and zero discarded
weight at bond dimension two. The transfer matrix A_0+A_1 has eigenvalues
1 and -1, retaining the alternating memory exactly.

Finite bond dimension, bounded entropy, exact invariance, zero truncation
error, and fair marginals therefore do not establish a memoryless bath or
an individual orbit's time-average density. Standard MPS machinery does
not identify these distinct properties [^2].

For the actual deterministic seed, the probability distribution at each
time is simply delta_(F^t delta_0). This is a product distribution with
bond dimension one and zero bipartite entropy at every time. Its center
time-average remains the unresolved question. An ensemble, a time average,
and a single evolving configuration must not be conflated.

### What a truncation error actually controls

For a raw probability matrix, the sum of squared singular values is its
squared Frobenius norm, not generally one. For example, an equal mixture
of the deterministic words 0^N and 1^N has two nonzero singular values 1/2
across any nontrivial cut; their squared sum is 1/2.

If a probability vector has d entries and a truncation has squared
Euclidean error epsilon, then, provided the approximation is already a
normalized nonnegative distribution,

\[
\operatorname{TV}(P,Q)\le\tfrac12\sqrt{d\epsilon}.
\]

Raw SVD truncation guarantees neither positivity nor normalization. In a
normalized square-root-amplitude representation, orthogonal Schmidt
truncation and renormalization instead give TV(P,Q)<=sqrt(epsilon).
An epsilon of 10^-8 then bounds single-truncation TV by 10^-4, not 10^-8.
Moreover, deterministic evolution is linear in probabilities P, generally
not in their square roots.

Let exact evolution be p_(t+1)=K_t p_t, and let valid approximate
distributions satisfy delta_t=TV(q_(t+1),K_t q_t). Nonexpansiveness of
Markov pushforward in total variation gives

\[
\operatorname{TV}(p_T,q_T)\le\operatorname{TV}(p_0,q_0)+\sum_{t<T}\delta_t.
\]

A small fixed error per step does not furnish a uniform infinite-time
guarantee. Improving this estimate needs a separate contraction or stability
theorem about the actual evolution, not the observed bond dimension.

## 3. Fair right noise still does not force fair center output

The Boolean OR requires a bit r_t in {0,1}. A centered variable eta_t in
{-1/2,1/2} must first be converted to r_t=eta_t+1/2.

Even granting independent fair right bits, take l_t identically one in
the proposed surrogate recurrence

\[
c_{t+1}=l_t\oplus(c_t\lor r_t).
\]

The transition matrix for c, with states 0,1, is

\[
\begin{pmatrix}1/2&1/2\\1&0\end{pmatrix}.
\]

It is irreducible and aperiodic, has eigenvalues 1 and -1/2, and has
stationary probability P(c=1)=1/3. It mixes, but its limiting density is
not 1/2. Taking l identically zero instead makes state one absorbing.
These are counterexamples to the proposed stochastic implication, not
claims about the actual seed's left input.

The exact integer decomposition exposes the missing term:

\[
c_{t+1}-\tfrac12
=c_t(\tfrac12-l_t)
 +(1-c_t)(1-2l_t)(r_t-\tfrac12).
\]

If r_t were conditionally fair given a causal filtration containing l_t
and c_t, the last term would be a bounded martingale difference. Its time
average would vanish almost surely under that stochastic model, while
half-density would still require

\[
\frac1T\sum_{t<T}c_t(1-2l_t)\longrightarrow0.
\]

Conditional fairness itself has not been established for an appropriate
seed-derived process. Finite spatial correlation length does not imply
temporal independence: the static random field x_i^t=xi_i with independent
fair xi_i has zero spatial correlations and perfect temporal memory.

Finally, density 1/2 does not by itself imply nonperiodicity; the sequence
010101... is balanced and periodic. An argument for P2 cannot automatically
be relabeled an argument for P1.

## 4. An exact recursive variance bound with its boundary term

Fix a time t>=1 and its positive row x_1,...,x_t, extended by zero past t.
Suppress t in notation and define, using ordinary complex arithmetic,

\[
B_{L,j}=\sum_{r=0}^{L-1}i^r x_{j+r},\quad
E_L=\sum_{j\ge1}|B_{L,j}|^2,\quad V_L=\frac{E_L}{tL^2}.
\]

Retain both a boundary energy and a contrast energy:

\[
Q_L=\sum_{j=1}^{L}|B_{L,j}|^2,\qquad
D_L=\sum_{j\ge1}|B_{L,j}-i^L B_{L,j+L}|^2.
\]

Then

\[
\boxed{E_{2L}=4E_L-2Q_L-D_L,}
\]

\[
\boxed{V_{2L}=V_L-\frac{2Q_L+D_L}{4tL^2}
             =V_L(1-\delta_L),\qquad
\delta_L=\frac{2Q_L+D_L}{4E_L}.}
\]

Proof: B_(2L,j)=B_(L,j)+i^L B_(L,j+L). The parallelogram identity gives
E_(2L)+D_L=2E_L+2 sum_(j>=1)|B_(L,j+L)|^2. The shifted sum is E_L-Q_L,
which proves the formula. Dropping Q_L would discard the boundary term.

If the positive row is nonzero, then E_L and E_(2L) are positive: their
window beginning at the last nonzero cell has squared modulus one. Also
D_L>0. Otherwise B_(L,j)=i^L B_(L,j+L) for every j, and iteration into
the zero tail would force every window sum to vanish. Therefore

\[
\boxed{0<\delta_L<1}
\]

for every L on every nonzero finite positive row. In particular, this
strict decrease holds on every actual seed row at t>=1, because x_t^t=1.
The identity and strictness use no stochastic assumptions.

## 5. Strict decrease is not the required uniform decrease

Consider positive rows with x_j=1 exactly when j=1 modulo 4. If L is a
multiple of four, every full window has modulus L/4, and truncated windows
have modulus at most L/4. Hence, for 4<=L<=t,

\[
\frac{t-L+1}{16t}\le V_L\le\frac1{16}.
\]

Consequently V_(t,L(t))->1/16 whenever 4 divides L(t) and L(t)=o(t).
Nevertheless V strictly decreases at each doubling for every individual
finite row. For 2L<=t, the same bounds give

\[
0<\delta_L\le\frac{2L-1}{t}.
\]

Thus the loss may vanish as the scale becomes small relative to row length.
These rows are also terminal rows of the explicit
[finite-origin extremizer family](RESULTS-quarter-wave-origin-obstruction.md),
with a different initial row for each t. They are not asserted to occur
on the lone-seed orbit.

The useful sufficient condition must control accumulated loss. Set L_j=2^j.
For the actual seed,

\[
V_{t,L_J}=V_{t,1}\prod_{j<J}(1-\delta_{t,L_j}),\qquad V_{t,1}\le1.
\]

It would suffice to prove a choice J=J(t) with L_J/t->0 and
sum_(j<J) delta_(t,L_j)->infinity. Then V_(t,L_J)<=exp(-sum delta)->0,
and the previously proved bound

\[
\frac{|P_t|}{t}\le\sqrt{V_{t,L_J}}+\frac{L_J-1}{t}
\]

would yield P_t=o(t). This accumulated-loss condition is sufficient, not
necessary: a single factor tending to zero can also suppress the product.
No such seed-specific accumulated-loss theorem is proved here.

## 6. Computation and the remaining proof obligation

The [transfer-gap verifier](../../experiments/rule30/finite_transfer_gap_counterexample.py)
and [certificate](../../experiments/rule30/finite-transfer-gap-counterexample.json)
check explicit de Bruijn examples for k=1,...,8, including exact transition
path counts, periodic covariance, and nonzero quarter-turn spectral atoms
for those examples. The all-k nonmixing statement follows from the Euler-tour
construction, not from extrapolating the finite list.

The [variance-loss verifier](../../experiments/rule30/quarter_wave_variance_loss.py)
and [record](../../experiments/rule30/quarter-wave-variance-loss.json) check
2,550 finite-row/scale cases against independent scalar sums. They also
record exact profiles on ten actual seed rows, at dyadic times 256 through
131,072, and check the coherent-row counterexamples. A separate scalar
review checked 7,602 row/scale cases. Integer arithmetic is used for all
energies, contrasts, and relative losses. The finite profiles establish no
asymptotic claim.

The MPS counterexample and stochastic transition matrix are exact analytic
constructions, independent of these finite profiles. Their probabilities
through word length eight, all eight cases of the stochastic decomposition,
and the stationary 1/3 law were also checked with exact rational arithmetic.

There is no proved requirement to abandon exact counting, bijections, or
deterministic geometry as entire classes of methods. Particular failed
boundary involutions rule out those constructions, not every combinatorial
argument. A computer-assisted proof remains possible, but it must certify
an inequality or representation valid for the designated infinite sequence.

The exact variance recursion is now available. The missing theorem is
uniform accumulated loss on the actual seed before the averaging window
becomes comparable to the row. Establishing that would prove only the
spatial quarter-wave milestone; the accumulated-current estimate needed
for P2 and a separate argument for P1 would still remain.

The [actual-seed certificate search](RESULTS-seed-loss-certificate-search.md)
continues this target. It checks every time through 8,192 at dyadic scales
4<=L<=sqrt(t), and gives the exact seed witness delta_(20,4)=17/84 against
a proposed uniform quarter loss. The
[coherence analysis](RESULTS-quarter-wave-coherence-barrier.md) proves an
explicit finite-support loss floor, an inverse persistence estimate, and
a local eight-step history bound near maximal window energy. Those
inequalities do not establish the required seed accumulated loss.

## Sources

[^1]: Levin and Peres, with contributions by Wilmer. [Markov Chains and Mixing Times, second edition](https://pages.uoregon.edu/dlevin/MARKOV/mcmt2e.pdf), particularly Chapters 4 and 12. The finite-matrix scope is distinct from assuming a finite-memory model for an unspecified process.
[^2]: Schollwock. [The density-matrix renormalization group in the age of matrix product states](https://arxiv.org/abs/1008.3477), 2010/2011. The exact counterexamples and error inequalities in this report specify which representation and norm are being used.

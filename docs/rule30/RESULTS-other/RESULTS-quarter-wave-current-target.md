# Quarter-wave current: exact identity and the next independent target

This report concerns Rule 30 from the lone seed. It proves an integer
potential/current identity and records finite diagnostics. It does not prove
an asymptotic estimate, P1, P2, or P3.

## 1. An exact identity over the integers

For a finite-support row x, define

\[
P(x)=\sum_{m\ge0}(x_{4m+1}-x_{4m+3}),\qquad
q_i(x)=2x_i(x_{i+1}\lor x_{i+2})+x_{i+1}x_{i+2},
\]

\[
K(x)=\sum_{m\ge0}(q_{4m}(x)-q_{4m+2}(x)).
\]

All these sums and differences are ordinary integers, not GF(2).
The local charges q_i belong to {0,1,2,3}. Then

\[
\boxed{x_0=P(Fx)-P(x)+K(x).}
\]

To prove it, write N_i=x_ix_{i+1} and
H_i=x_i(1-x_{i+1})x_{i+2}. Rule 30 has the integer expansion

\[
(Fx)_i=x_{i-1}+x_i+x_{i+1}-N_i-2N_{i-1}-2H_{i-1}.
\]

Let w_i=sin(pi i/2) for i>0 and w_i=0 otherwise. The weights are
0,1,0,-1,0,1,... and satisfy w_{j-1}+w_{j+1}=1_{j=0}.
Multiply the expansion by w_i and sum. The linear contribution to
P(Fx)-P(x) is x_0. The nonlinear contribution is minus K(x), since
q_i=2(N_i+H_i)+N_{i+1}. This proves the identity.

For the seed, put P_t=P(x^t), K_t=K(x^t), and
A(T)=sum_{0<=t<T} x_0^t. Since P_0=0, telescoping gives

\[
\boxed{A(T)-\frac T2=P_T+\sum_{t<T}(K_t-\tfrac12).}
\]

Separate sublinear bounds on the two terms are sufficient for P2. They are
not known to be necessary: the identity permits cancellation between the
terms. Once P_T=o(T) is established, the remaining current estimate is
equivalent to P2. Small measured current discrepancy is consequently not
independent evidence for a density theorem.

## 2. A finite cutoff exposes the boundary term

For L=4m, truncate both sums to 0<=j<m, obtaining P_L and K_L. The
truncated weights satisfy w_{j-1}+w_{j+1}=1_{j=0}-1_{j=L}, hence

\[
\boxed{x_0-x_L=P_L(Fx)-P_L(x)+K_L(x).}
\]

Here |P_L(x)|<=L/4. Starting from the seed gives

\[
A(T)-\frac T2=P_L(x^T)
 +\sum_{t<T}(K_L(x^t)+x_L^t-\tfrac12).
\]

One may choose L=L(T)=o(T), divisible by four, and make the endpoint
negligible without proving a spatial theorem. But the extra boundary
column x_L remains unknown. Omitting it would invalidate the argument.
The cutoff transfers the unresolved estimate to a boundary-plus-current
observable; it does not establish cancellation.

## 3. What the seed computation actually establishes

The [verifier](../../experiments/rule30/quarter_wave_current_audit.py) checks
the full identity on 6,138 finite-row/placement cases and every seed step
up to time 131,072. A scalar set-based evolution independently checks the
packed-bit evolution through time 128. The finite cutoff also received an
independent check on 18,414 row/placement/cutoff cases, for L=4,8,12.

The [recorded output](../../experiments/rule30/quarter-wave-current-audit.json)
includes maxima over all prefixes, not just endpoint values:

| T | P_T | Maximum potential magnitude through T |
| ---: | ---: | ---: |
| 4,096 | 2 | 80 |
| 16,384 | -71 | 178 |
| 65,536 | -54 | 345 |
| 131,072 | 122 | 498 |

At T=131,072, 2A(T)-T=-138 and 2 sum_{t<T} K_t-T=-382;
indeed -138=2(122)-382. Here A(T) counts times 0,...,T-1,
which differs from the times 1,...,T convention of some earlier probes.

These are finite integer computations. They establish neither a growth
exponent nor a stochastic model for P_t or K_t.

## 4. Why spatial phase and the initial condition matter

The support bound x_i^t=0 for i>t gives the elementary estimate

\[
|P_t|\le \left\lfloor\frac{t+3}{4}\right\rfloor.
\]

Replacing the actual seed by arbitrary rows, even rows with arbitrarily
many predecessors, cannot improve this bound uniformly. On a four-cell
ring, the exact cycle is

```text
0010 -> 0111 -> 0100 -> 1110 -> 1000 -> 1101 -> 0001 -> 1011 -> 0010.
```

The periodic row (0100)^Z saturates P_L=L/4. It has a periodic predecessor
at every depth. Zero-padded copies reproduce arbitrarily long portions of
this row after any fixed number of steps, by finite propagation speed.
These are other initial states, not counterexamples on the lone seed.

Time invariance alone does not remove the obstruction. The twelve-cell
cycle

```text
100111110000 -> 111100001001 -> 000010011111 -> 100111110000
```

has P_12=-1 in all three rows. Its uniform time-orbit measure has a
nonzero phase imbalance. Averaging additionally over every spatial shift
would erase the phase imbalance by construction.

Thus a block-frequency model for this observable must retain the starting
position modulo four. For phase-indexed block frequencies p^a(w), the
extension equations have the form

\[
p^a(w)=\sum_b p^a(wb)=\sum_b p^{a-1}(bw),\qquad a\pmod4,
\]

with endpoint corrections when using finite-window counts. Ordinary
shift-invariant block frequencies average away the distinction between
positions 1 and 3 modulo four. They cannot certify the designated row's
quarter-wave cancellation.

## 5. A concrete next milestone and a certificate standard

The first independent target is a seed-specific spatial theorem:

\[
\boxed{M_P(T):=\max_{0\le t\le T}|P_t|=o(T).}
\]

This uniform-prefix formulation is equivalent to P_t=o(t); it makes the
required control between sampled dyadic endpoints
explicit. This is a distinct partial theorem, not a restatement of the
center's density.

A sufficient certificate format is a family of inequalities

\[
|P_t|\le \varepsilon_h t+C_h\quad\text{for every seed time }t,
\qquad \varepsilon_h\longrightarrow0,
\]

where C_h is independent of t. At fixed h, retain spatial phases and
enough boundary/history information to derive a local inequality that
sums or inducts over the entire cone from the pinned seed. Increasing h
may enlarge that information. A first smaller success would be a proved
coefficient strictly below the trivial 1/4.

Finite-cone LP or SAT calculations may help discover such an inequality,
but solving a deterministic cone at one height is just computing that
height. A proof must supply a reusable induction or telescoping certificate
valid for arbitrary height, including all boundary terms. Rational
arithmetic can verify a proposed finite certificate; floating-point
optimization or success at finitely many heights cannot establish the
uniform claim.

If a candidate inequality fails, its witness should identify the missing
phase or history information. Failure of a chosen certificate family is
only an obstruction to that family. A disproof of P2 would instead require
an actual-seed construction giving infinitely many T with
|A(T)-T/2|>=epsilon T for some fixed epsilon>0.

Even a successful spatial theorem leaves the centered-current estimate
unproved. There is currently no demonstrated mechanism closing that second
step. The purpose of the first milestone is to obtain a verifiable partial
theorem before treating this identity as a route to the full density result.

## 6. Subsequent tests of the proposed induction and spectral bridge

The [finite-origin obstruction](RESULTS-quarter-wave-origin-obstruction.md)
constructs all-length initial-row families with maximal phase imbalance and
quadratic one-step injections into scalar or two-quadrature energy. Any fixed
bounded local additive correction is too small to repair a universal drift
bound proportional to initial mass. These are other initial rows; the result
does not disprove the seed-specific target or a global initial-mass estimate.

The [spatial skew-product audit](RESULTS-quarter-wave-skew-product.md)
constructs the exact phase operator and corrects the proposed zero-mode and
unique-ergodicity implications. Uniform phase marginals do not enforce
cell/phase decorrelation. Absence of coordinate spectral atoms at spatial
frequencies +/-1/4 in every base accumulation measure is a proved sufficient
condition for P_t=o(t), but that spectral condition remains unproved on the
seed. These tests do not close either step of the P2 argument.

The [actual-seed current collisions](RESULTS-quarter-wave-current-collision.md)
exclude every exact correction `K_t-rho=h(W_(t+1))-lambda*h(W_t)`
using only the centered radius-five window, even with arbitrary complex
constants and an arbitrary function h. A period-four clock also fails at
radius two. These finite witnesses do not exclude larger or growing
windows, histories, later-onset identities, or residual cancellation.
The [bilateral frequency identity](RESULTS-bilateral-frequency-current.md)
bounds its potential uniformly at fixed nonreal unit frequencies, but
leaves the nonlinear current and the zero-frequency density target open.

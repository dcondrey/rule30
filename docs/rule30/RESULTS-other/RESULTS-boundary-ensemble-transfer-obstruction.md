# Exact boundary control and the obstruction to transferring it to the seed

Date: 2026-09-10. **No solution or counterexample to P1, P2, or P3.**

The proposed left-boundary involution does exist, at every length, and fair
left-boundary bits produce an exactly independent fair center tail. The
missing inference is not an estimate of how well this ensemble mixes. Even
perfect ensemble randomness does not determine the autonomous seed's trace.
This report makes that obstruction quantitative and gives a deterministic
counterpart using prescribed constant tails.

The triangular inverse theorem is standard left permutivity, already recorded
in [the inverse-trace report](RESULTS-inverse-trace.md). Its finite-prefix
consequences also appear in [the eventual-period report](RESULTS-eventual-period.md).
The nearby-configuration-to-seed error and Rule 90 control were already
identified in [the Fradkin audit](REFUTATION-fradkin-rule30-resolved.md).
The contribution here is an explicit law, conditioning distance, and
time/window tradeoff for the proposed ensemble, with reproducible checks.
No novelty claim is made for left permutivity or the general transfer warning.

## 1. Exact coding with a fixed initial right half

Let F be Rule 30, let e be the lone seed, and write c_t=(F^t e)_0. Fix the
entire initial right half x_i=e_i for i>=0, while allowing a_n=x_-n, n>=1,
to vary. A cell at -n cannot affect the center before time n. At time n
its unique fastest path uses the left parent of the rule at every step.
The other two parents at each gate lie outside that cell's influence cone.
Since f(p,q,r)=p XOR (q OR r),

```
z_n = a_n XOR G_n(a_1,...,a_(n-1)),    n>=1.
```

Thus the first n initial-left bits biject to the first n center bits after
time zero. Two inputs first differing at depth n have center traces first
differing at time n. These consistent finite bijections give a bijection Phi
between infinite left halves and arbitrary traces with z_0=1. Both Phi and
its inverse preserve common-prefix length; equivalently, they are isometries
for the ultrametric 2^(-first disagreement index).

This is a coding between two spaces, not a claimed dynamical conjugacy to a
shift: the fixed-right initial slice is not asserted to be F-invariant.

## 2. Perfect randomness can approach the seed locally

For L>=0, fix a_1=...=a_L=0, and choose a_(L+1),a_(L+2),... independently
and fairly. The preceding triangular bijections imply the exact trace law

```
mu_L = delta_(c_0,...,c_L) tensor Bernoulli(1/2)^N.
```

For every finite tail length n, each of the 2^n possible center tails has
probability exactly 2^-n. This proves joint independence, not just fair
one-bit marginals. With probability one the temporal trace has density 1/2
and every finite word has its fair limiting frequency; a fixed initial
prefix does not change these limits.

Nevertheless the initial ensembles converge weakly to delta_e: every fixed
finite spatial window is eventually pinned exactly to e. Correspondingly,
mu_L converges weakly to the point mass at the actual seed trace, because
every fixed temporal prefix is eventually pinned to that trace.

This does not prove unequal iterated limits for Rule 30: the reverse-order
time-density limit is precisely the unknown quantity in P2. It proves that
the ensemble calculation alone does not justify exchanging these limits.

## 3. Deterministic completions with incompatible limiting densities

For q in {0,1}, prescribe the complete trace

```
c^(L,q)_t = c_t for t<=L, and q for t>L.
```

Section 1 gives a unique initial completion x^(L,q) with this trace and the
fixed nonnegative half. Its first L negative cells are zero, since its
center prefix agrees with the seed. Hence

```
x^(L,q) = e on [-L,infinity),
x^(L,q) -> e locally as L -> infinity,
density(c^(L,0)) = 0,
density(c^(L,1)) = 1.
```

These are arbitrary-left completions, not autonomous evolutions from the
lone seed; they are not counterexamples to P1 or P2. They show directly that
finite local seed agreement and local convergence cannot determine temporal
density. Eventually periodic traces are a countable dense set in trace
space; their initial-left preimages are also countable dense. Therefore no
finite initial neighborhood of the seed excludes eventually periodic center
completions. A proof must use more than such a neighborhood.

## 4. The proposed driven-boundary involution works exactly

Now use the finite window [-L,R], with L,R>=1. The initial row is the seed.
For positive times prescribe the endpoint values; interior cells obey the
usual rule. Freeze the right endpoint to its actual autonomous seed tape.
Let b_s=x_-L^(s), s>=1, be the freely chosen left tape.

If two tapes first differ at s, their centers first differ at L+s. The same
unique fastest-path argument gives

```
z_(L+s) = b_s XOR H_s(b_1,...,b_(s-1)).
```

For every n the induced map F_n from b_1,...,b_n to
z_(L+1),...,z_(L+n) is a bijection. If C complements every output bit,

```
I_n = F_n^(-1) o C o F_n
```

is a fixed-point-free involution. The I_n are prefix-compatible, so define
an infinite-tape involution. It preserves t=0 and complements the entire
controllable center tail. No linear response approximation is used.

The first changed boundary bit is necessarily b_1. Thus the involution
changes the externally prescribed tape at positive time; it cannot preserve
the unique tape induced by the autonomous lone seed. Its backward diagonal
stops at the driven boundary, rather than forcing an initial-row change.
This distinguishes the driven construction from Section 1.

Fair independent b_s again give exactly mu_L. The autonomous right tape
ensures that the fixed center prefix is c_0,...,c_L even when R<L.

## 5. Exact price of autonomous compatibility

Let b* be the left tape of the autonomous seed, and consider n free left
boundary bits. By bijectivity exactly one n-bit tape gives the corresponding
seed center block z*. Under the uniform boundary ensemble,

```
P(B_1...B_n = b*_1...b*_n) = 2^-n,
Law(Z | B=b*) = delta_z*,
TV(delta_z*, Uniform({0,1}^n)) = 1 - 2^-n,
KL(delta_z* || Uniform({0,1}^n)) = n log 2.
```

Here Z and the conditioning are finite n-bit blocks. Later bits remain
random. Conditioning on the complete infinite tape is a probability-zero
event and is not justified by elementary finite conditional probabilities.

The autonomous initial-half construction has the same formulas when n counts
the free exterior bits a_(L+1),...,a_(L+n), all set to zero for the seed.

## 6. An exact observation-time/window tradeoff

Observe the first T center bits, at times 0,...,T-1. Set

```
m = min(T,L+1),       n = T-m,
S_c(m) = sum_(t<m) (1-2c_t),
D_T = (1/T) sum_(t<T) (1-2z_t).
```

Under mu_L there are m fixed bits and n independent fair bits. Therefore

```
E[D_T] = S_c(m)/T,
Var(D_T) = n/T^2,
TV(mu_L restricted to [0,T), delta_(c_0,...,c_(T-1))) = 1-2^-n.
```

The total variation identity follows because the actual seed word is one
of 2^n equiprobable possible tail completions. For n>0, Hoeffding's inequality
also yields

```
P(|D_T - S_c(m)/T| >= eps) <= 2 exp(-eps^2 T^2/(2n)).
```

If L=o(T), the ensemble is balanced in mean square by the trivial bound
|S_c(m)|<=m. But then most observed bits lie beyond the seed agreement
prefix. If L>=T-1, the full observation is exactly the seed and n=0: there
is no random tail, and the mean is precisely the unknown seed discrepancy.
If n grows, total variation from the seed observation tends to one.

This rules out a transfer based solely on local agreement or total variation
closeness of long traces. It does not rule out additional seed-specific
estimates for the particular time-average observable.

## 7. Why this cannot by itself prove P1, P2, or P3

Every coding, involution, and ensemble law above uses only left permutivity.
They hold for Rule 90, whose lone-seed trace is exactly 1,0,0,...: odd times
are zero by parity, and at time 2s>0 the center is binomial(2s,s) modulo two,
which vanishes since binomial(2s,s)=2 binomial(2s-1,s-1).

Thus the same exact random-ensemble conclusions coexist with eventual
periodicity, density zero, and a constant answer for every positive-index
center query. These structural hypotheses cannot imply the desired prize
conclusions for a fixed seed. This is a counterexample to their sufficiency,
not a counterexample to any Rule 30 prize problem.

For Rule 30 P1 the minimal same-orbit target remains

```
for every T>=0 and p>=1, some n>=0 satisfies
(F^(T+n)e)_0 != (F^(T+p+n)e)_0.
```

Excluding collisions for every nonzero finite row would be stronger than
needed. The existing inverse reconstruction identifies its first spatial
mismatch at exactly the first temporal mismatch; it is not automatically
a shorter proof or a computational shortcut. A new argument must control
these seed-specific mismatches uniformly, or supply another exact seed
obstruction. The phase-refill law does not currently supply that control.

## 8. Verification

Run from the repository directory:

```sh
uv run python experiments/rule30/boundary_ensemble_audit.py
```

The dependency-free check uses a direct truth-table finite-support evaluator
and a separately implemented finite driven strip. It verifies:

* 144 window/horizon cases, for Rules 30 and 90, L,R=1,2,3 and n=1,...,8;
* 9,180 enumerated boundary histories and complement-involution checks;
* 64,548 earliest-difference checks and 144 exact first/second moment cases;
* 16 prescribed-tail reconstructions through time 48, independently replayed
  using the truth-table evaluator;
* the exact nonlinear damage identity on all 64 local assignments, including
  16 failures of the proposed linear formula;
* the exact stationary density 1/3 of the proposed fair-right-noise model
  when the left input is constantly one.

All passed. The infinite-length claims are proved in Sections 1-7; the finite
checks validate implementations and indexing rather than extrapolating a
prize conclusion. Existing unrelated working files were not changed.

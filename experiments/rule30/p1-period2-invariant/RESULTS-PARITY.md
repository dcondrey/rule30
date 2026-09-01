# Period-two nonlinear pin-parity continuation

Date: 2026-08-31

Status: **OPEN.  No period-two theorem was proved.**  The fixed-order
Hasse/mixed-moment certificate in `PREREGISTRATION-PARITY.md` was falsified.
The useful positive result is an exact inverse-Gray-code normal form for the
already-recorded two-sweep frontier map.  The negative result is both an
all-orders algebraic obstruction to truncated Hasse closure and an exact
same-length collision between genuinely reachable finite-seed frontiers.

## 1. Exact Gray-code normal form

At an even macro boundary, let

```text
A(z) = sum_(j>=1) A_j z^(j-1),
B(z) = sum_(j>=1) B_j z^(j-1).
```

The boundary values are `A_0=0` and `B_0=1`.  Define `I` on a finite Boolean
word by reverse cumulative XOR,

```text
I(X)_j = XOR_(k>=j) X_k.
```

If a word is stored as a nonnegative integer with `X_j` in bit `j-1`, then

```text
I(x) = x XOR (x >> 1) XOR (x >> 2) XOR ...,
```

the inverse of the usual binary Gray-code map `g(x)=x XOR (x>>1)`.

The exact surviving macrostep in `RESULTS.md` is therefore

```text
O = A OR (1 + z B),       C = I(O),
P = C OR z A,             D = I(P),
pin passes iff D_1=1,
(A,B) maps to (D,C).
```

Equivalently, as a map on finite nonnegative integers,

```text
C = I(A | (1 | (B << 1))),
D = I(C | (A << 1)),
M(A,B) = (D,C),           survive iff D is odd.
```

This removes the inert deep-zero margin and the explicit frontier length.
It retains exactly the finite rho-seed initial set and Rule 30's two ORs; it
is not an arbitrary half-plane witness or a generic left-permutive argument.
`verify_moment_negative.py` checks it against the two right-to-left recurrences
on all 34,952 legal even-boundary frontiers through `T=8`.

## 2. Why fixed Hasse order cannot close

Let `H_k(X)` be the `k`th Hasse derivative of `X` at `z=1`:

```text
H_k(X) = sum_n binom(n,k) X_n mod 2.
```

Reverse cumulative XOR satisfies

```text
(1+z) I(X) = z X + H_0(X).
```

Taking the coefficient of `(z+1)^(k+1)` gives the exact hierarchy

```text
H_k(I(X)) = H_k(X) XOR H_(k+1)(X).                 (1)
```

Thus order `K` asks for order `K+1` after one sweep.  This is not merely a
formal warning.  For every `K>=0`, put

```text
E_K = z(1+z)^(K+1),
X   = 1,
X'  = 1 + E_K.
```

Then `X` and `X'` have the same `H_0,...,H_K`, and both have constant
coefficient one.  Both are legal first OR-words: take `B=0` and respectively
`A=X` or `A=X'`.  But linearity and (1) give

```text
I(E_K) = z^2(1+z)^K,
H_K(I(X)) != H_K(I(X')).
```

So no truncation at any fixed Hasse order determines its own image even on
finite words with the correct Rule-30 boundary bit.  The standalone verifier
checks the construction for every `K=0..64`; the displayed polynomial
identity proves it for all `K`.

Adding a fixed list of correlations might conceivably repair a particular
truncation, so the registered search also used a deliberately stronger state.
At each order `K<=8` it included the moments of every squarefree monomial of
degree at most three in

```text
A, V=1+zB, C=I(A OR V), S=zA,
```

plus two bits at each endpoint and the active height modulo 16.  Every one of
these nine registered rich summaries has an exact reachable closure
collision.  At `K=8`, the first collision in the preregistered lexicographic
enumeration is between `(T,A,B)=(4,3,2)`, reached from length-one seed zero
after one forced macrostep, and `(20,174763,174762)`, reached from length-nine
seed 504 after one step.  Both pass the current pin, but their successor
summaries differ.

The length modulus is not the cause.  The earliest equal-`T` collision found
at rich order eight is

```text
rho seed (length, integer, follow) = (13,1196,3)
(T,A,B) = (32,358962517,181753173)

rho seed (length, integer, follow) = (13,1344,3)
(T,A,B) = (32,357913957,178957013).
```

Seed integers are read least-significant bit first by the exact rho recurrence.
The two 131-component registered features agree exactly.  Both current pins
are one, while successor components 26 and 62 differ.  The standalone script
reconstructs both states from their rho seeds before checking the collision;
the decimal states are not trusted inputs.

This fires the preregistered kill condition.  Raising `K` would only move the
dependency in (1), and retaining the entire hierarchy is the raw word in a
different basis.  Fixed-order Hasse/mixed-moment **closure** should be retired.
The result does not rule out a different non-closed rank that happens to be
computable from a fixed statistic, or a certificate using correlations of
unbounded degree; neither was proved impossible.

## 3. Controls

The full existing control script was rerun after the moment search:

- the radius-two `F^2` formula passed all 32 neighborhoods;
- the two-orbit defect recurrence passed all 64 assignments;
- the alternating strobe pattern passed its complete truth table;
- Rule 30 `{-8,-1,6}` alternated through `t=14` and failed at `t=15`;
- Rule 90 `{-1,1}` had zero center through `t=128` and was not excluded;
- all 131,071 nonzero rows in `[-8,8]` were checked through 64 steps, with
  maximum alternating horizon 14 and witness `{-8,-1,6}`;
- the maximum constant-zero and constant-one horizons were again 8 and 9.

The last two constant results are bounded validation of existing theorems,
not new claims.  The load-bearing map here contains Rule 30's coefficientwise
OR twice.  Rule 90 replaces those unions by XOR and retains its known finite
period-two collision, so no permutivity-only exclusion has entered.

## 4. Commands and development checks

Final reproducible commands, from `/Volumes/A/researchpapers/13-rule30`:

```bash
ps aux | grep claude
lsof -a -p 72158 -d cwd
git status --short --branch

PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/moment_search.py \
  --max-seed 16 --max-follow 128 --max-order 8 --endpoint-width 2

PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/verify_moment_negative.py

PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/derive_and_controls.py
```

Results:

```text
moment search: 32,043 distinct exact finite-seed states;
               closure collisions at every base/rich K=0..8;
               rich K=8 equal-length collision verified
standalone:    589,824 Hasse identity checks PASS
               34,952 Gray macro checks PASS
               K=0..64 obstruction instances PASS
               reconstructed equal-length collision PASS
controls:      all exact/local/global controls PASS
```

Additional exact diagnostic scripts, run as Python standard-input commands,
checked: seed-state/survival tables through seed length 16; the longest seed-16
orbit; absence of self-loops and of strongly connected components in the
*sampled* rich-`K=8` quotient graph; equal-length closure collisions; and
same-summary/different-pin collisions for the weaker base summary.  These
diagnostics are falsification only and support no universal claim.

Two development assertions caught boundary mistakes before the final run.
The first Gray checker incorrectly included odd `T`, which is an intermediate
phase rather than a complete macro boundary.  The first standalone seed
reconstructor used `T mod 2` instead of the correct `(T-1) mod 2` boundary.
Both were corrected; the final standalone checks above pass.  No timeout,
memory limit, paid call, GPU, Modal job, SAT grid, or writing agent was used.

## 5. Consequence and next theorem

The alternating case, the period-two same-orbit theorem, and Prize Problem 1
all remain open.  This continuation advances the formulation, not the theorem:
the growing frontier is now a length-free integer map made from inverse Gray
code and two coefficientwise ORs, while an exact algebraic obstruction retires
the tempting fixed-moment quotient.

The single best next theorem target is:

> **Finite-seed Gray-OR mortality.**  Every pair `(A,B)` arising from a finite
> rho seed has an iterate under `M` whose first component `D` is even.

Equivalently, prove that an orbit of the displayed Gray-OR map whose first
component stays odd forever cannot originate in the finite rho-seed language;
it must encode an infinite spatial tail.  A useful certificate must exploit
that seed language without storing the whole word or merely raising moment
order.

The construction is period-two-specific: one zero phase creates the forced
first sweep with boundary `1+zB`, and one pinned phase creates the second sweep
and the single oddness test.  A general period has a phase-word-dependent
chain of sweeps and free inputs.  No period-uniform generalization follows,
and proving this target would still be only the `p=2` rung of Prize Problem 1.

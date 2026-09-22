# Pursuing unbounded sublinear growth at frequency one third

Date: 2026-09-16. **The sufficient criterion is valid; neither required
asymptotic estimate is proved for the singleton.** This follow-up separates
the weaker target from inheritance of the Thue-Morse exponent, gives an
exact two-counter formulation and a phase-sensitive upper criterion, and
rejects several shortcuts with exact controls.

## 1. The target is a spread between three integer counts

Use the actual singleton center `c_t`, signs `s_t=1-2*c_t`, and
`omega=exp(-2*pi*i/3)`. Write

```text
S(N) = sum_(0<=t<N) s_t*omega^t,
A_r(m) = sum_(0<=j<m) c_(3j+r),       r=0,1,2,
X_m = A_2(m)-A_0(m),
Y_m = A_2(m)-A_1(m),
Delta_m = max_r A_r(m)-min_r A_r(m).
```

Since `1+omega+omega^2=0`, direct grouping gives

```text
S(3m) = 2*(X_m+Y_m*omega),
|S(3m)|^2 = 4*(X_m^2-X_m*Y_m+Y_m^2)
          = 2*sum_(r<s) (A_r(m)-A_s(m))^2,
Delta_m = max(|X_m|,|Y_m|,|X_m-Y_m|),
sqrt(3)*Delta_m <= |S(3m)| <= 2*Delta_m.                 (1)
```

The norm bounds follow by placing the smallest count at zero, the largest
at `d=Delta_m`, and the middle one at `u in [0,d]`:
`|S|^2=2*(d^2+u^2+(d-u)^2)` lies between `3d^2` and `4d^2`.
The one- or two-term remainder between `3m` and the next prefix has
magnitude at most `sqrt(3)`. Thus the all-prefix target is precisely

```text
Delta_m is unbounded,             Delta_m=o(m).           (2)
```

This asks for agreement between the three residue classes, with an
unbounded absolute fluctuation. It does not require that their common
asymptotic density exist or equal one half.

There is a useful weaker combination of quantifiers. If an eventually
periodic trace existed, the earlier
[rational-frequency lemma](RESULTS-third-frequency-scale-target.md)
would give `S(N)=N*ell+O(1)` for **all** N. Consequently it suffices to prove

```text
S(N_k)/N_k -> 0 along any sequence N_k -> infinity,
and |S(N)| is unbounded over all N.                     (3)
```

The first assertion forces `ell=0`, contradicting the second. The lower
bound need not occur at the same times as the upper estimate. In
particular, upper control at `4^k` can be combined with lower witnesses
at arbitrary times. Neither assertion in (3) is established here.

## 2. What would force escape, and what does not

At each aligned triple, `(X,Y)` gains

```text
(c_(3m+2)-c_(3m), c_(3m+2)-c_(3m+1)).
```

There are seven possible steps: zero and six directions of an Eisenstein
lattice. Zero occurs exactly for triples `000` and `111`. Confinement of
this walk would not give a closed finite-state generator for its steps.

Two exact controls show the missing implication:

- Replace each symbol of any binary sequence by `000` or `111`.
  Then `S(3m)=0` and `|S(N)|<=1` for every N. The underlying sequence
  may be aperiodic, balanced, and have arbitrarily long constant runs.
- Concatenate blocks `011100` and `100011` according to an arbitrary
  binary sequence. Each six-block has zero total charge, while both
  of its aligned triples have nonzero charge. All prefix sums remain
  bounded (for example by 6), and an aperiodic choice sequence gives an
  aperiodic output. Thus even a nonzero step at every aligned triple
  does not prove escape.

For an explicit aperiodic choice sequence one can use
`1^1 0^1 1^2 0^2 1^3 0^3 ...`: both symbols keep appearing and run lengths
are unbounded, precluding eventual periodicity. Its density is one half.
These are logical controls, not claimed Rule 30 seed trajectories.

One concrete sufficient seed property is recurrence of arbitrarily large
powers of a nonconstant three-bit word. Every such word u has signed
third-frequency charge of magnitude 2. A center block within Hamming
distance e of `u^m` therefore has charge at least `2m-2e`, because a bit
flip changes its charge by magnitude 2. If the block starts at a,

```text
max(|S(a)|,|S(a+3m)|) >= m-e.                            (4)
```

Thus blocks with `m-e -> infinity` would establish the lower half of
(3); `e <= (1-delta)*m` for a fixed delta>0 is sufficient. Block starts
need not share a phase modulo three. This is a specific recurrence
hypothesis, weaker than full normality, but it is not proved for the
singleton. The archive's nonconstant-tail and adjacent-column results
do not supply it.

Finally, **nonvanishing at `4^k` is automatic** and is not a lower-bound
theorem. For every binary sign sequence, reduction modulo two gives
`S(4^k)=1` in `Z[omega]/2Z[omega]`: signs are all 1 modulo two and
`4^k=1 mod3`. Thus `S(4^k)` can never be zero, even for a constant trace
whose Fourier sums are bounded.

## 3. A phase-sensitive sufficient upper estimate

For a finite sign word of length N define its zero-extended real
correlations

```text
C_N(h) = sum_(t=0)^(N-1-h) s_t*s_(t+h),    h>=0,
C_N(-h)=C_N(h),                           C_N(h)=0 if |h|>=N.
```

In particular `C_N(0)=N`. Define the filtered correlations

```text
K_N(h) = 3*C_N(h)-C_N(h-1)-C_N(h+1)
         -(C_N(h-2)+C_N(h+2))/2,
B_N = 3*N-2*C_N(1)-C_N(2).                              (5)
```

These K are temporal correlation combinations; they are distinct from
the spatial nonlinear current and the earlier four-adic residual defects.
For `m>=1`, put `a_j=4^j-1`, `0<=j<m`. Then

```text
9*m^2*|S(N)|^2
 <= (N+4^(m-1)+1)
      *[m*B_N + 2*sum_(0<=i<j<m) K_N(4^j-4^i)],
0 <= B_N <= 4*N.                                       (6)
```

**Proof.** Extend `z_t=s_t*omega^t` by zero and sum its translates at
the `3m` positions `{a_j+r: 0<=j<m, 0<=r<3}`. The resulting Y has
support in an interval of length `N+4^(m-1)+1`, and its total is `3m*S(N)`.
Cauchy-Schwarz bounds this total by that support length times
`sum_t |Y_t|^2`. Within a translation triple the latter expands to B_N.
Between two triples, their base difference is divisible by three;
the real phase factors are 1 for equal offsets and -1/2 for unequal
offsets, giving exactly K_N in (5). This proves the first line.

To bound B_N, view it as the squared norm of the zero-extended triple
sum `s_t+omega*s_(t+1)+omega^2*s_(t+2)`. Every full binary triple has
squared charge 0 or 4. For N>=2 the four boundary windows contribute
at most 8 in total, and there are N-2 interior windows, giving `B_N<=4N`.
For N=1 its value is 3. Nonnegativity follows from the same squared norm.

A sufficient, presently unproved, seed hypothesis is: for an unbounded
set of positive integers m,

```text
limsup_(N->infinity) (1/N)*sum_(i<j<m) K_N(4^j-4^i) <= 0. (7)
```

Indeed, fix m in (6) and take N to infinity. The squared normalized
Fourier sum has limsup at most `4/(9m)`. Then let m tend to infinity
through the admitted set. This proves `S(N)=o(N)` without any density
claim or uniform rate in m. The order of limits is essential.

The filter coefficients in (5) sum to zero. This removes a constant
correlation baseline rather than requiring its disappearance. For
example the periodic word `(111000000)^infinity` satisfies (7) for every
m divisible by three. Modulo nine the anchors cycle through 0,3,6;
their translation triples cover every residue equally, and the whole
nine-term Fourier sum is zero. More explicitly, its cyclic K_0 numerator
is 16 and the off-diagonal numerator is `-8m`. Its density is one third,
and its Fourier sums are bounded. Thus (7) supplies neither P2 nor the
unboundedness needed in (3).

The stronger pointwise hypothesis `limsup K_N(h)/N<=0` for every
`h=4^a-4^b` also implies (7), but demands more than upper control alone.
For any hypothetical nonconstant period p, two powers of four coincide
modulo p. Their difference h is period-compatible, and the limiting
filtered correlation is `3-2*R(1)-R(2)>0`, since `R(1)<1` for a
nonconstant periodic binary word and `R(2)<=1`. Thus this pointwise
hypothesis already excludes every nonconstant eventual period. Together
with the existing constant-tail exclusions it would itself prove P1.
It should not be presented as a cheap substitute for the upper bound.

## 4. The earlier inherited-exponent certificate has a narrower scope

The [residual-margin audit](RESULTS-third-frequency-residual-margin-audit.md)
uses only the already stored values of `F_k=S(4^k)` and their exact defects
`D_k=F_(k+1)-3F_k`. It proves that the strict absolute-tail margin for a
nonzero limit of `F_k/3^k` fails at every starting scale h=0,...,7.
At h=8,9 the recorded tails do not refute the margin; the unknown future
prevents a positive certificate.

The same data refute monotone growth: the exact energy falls from
7231 to 1963. In the identity

```text
|F_(k+1)|^2 = 9*|F_k|^2
             +6*Re(F_k*conjugate(D_k))+|D_k|^2,
```

the radial cross term is negative at nine of the ten recorded scales.
Neither its sign nor the energy is extrapolated beyond those scales.
The weaker target (3) requires no inherited exponent, monotonicity,
or nonzero scaled limit, and remains open.

## 5. Evidence and next proof obligations

Independent exact checkers accompany the three parts:

- [Walk/count checker](../../experiments/rule30/third_frequency_walk_audit.py)
  and [record](../../experiments/rule30/third-frequency-walk-audit.json):
  residue-count identities, norm bounds, charge controls, and robust block
  witnesses on finite words.
- [Correlation checker](../../experiments/rule30/third_frequency_correlation_audit.py)
  and [record](../../experiments/rule30/third-frequency-correlation-audit.json):
  the complete translation identity, inequality, diagonal bound, and
  periodic controls in exact arithmetic.
- [Residual-margin checker](../../experiments/rule30/third_frequency_residual_margin_audit.py)
  and [record](../../experiments/rule30/third-frequency-residual-margin-audit.json):
  rational certificates against the earlier margins and exact energy
  terms, reading the existing JSON rather than extending the seed run.

The analytic lemmas are general statements, and the controls delimit
their logical strength. The seed-specific work still required is an
upper estimate such as (7), plus an escape theorem such as (4) or another
argument proving unbounded residue-count spread. No such singleton
estimate is claimed by this pursuit.

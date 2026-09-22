# Actual-seed collisions obstruct small local current corrections

Date: 2026-09-16. **Exact finite counterexamples on the lone-seed orbit.**
The quarter-wave current cannot be absorbed by the small boundary potentials
specified below. This does not exclude growing or nonlocal potentials, and
does not prove or disprove P1, P2, or P3.

## 1. The correction being tested

Use the ordinary integer current from the
[quarter-wave identity](RESULTS-quarter-wave-current-target.md):

```
q_i(x) = 2*x_i*(x_(i+1) OR x_(i+2)) + x_(i+1)*x_(i+2),
K(x) = sum_(m>=0) (q_(4m)(x)-q_(4m+2)(x)),
c_t = P_(t+1)-P_t+K_t.
```

Write `W_r(t)=x^t[-r,...,r]`, with increasing spatial index from left
to right. A time-independent boundary correction would require

```
K_t-rho = h(W_r(t+1))-lambda*h(W_r(t)).                 (1)
```

Here `h` is an arbitrary complex-valued function on the finite window
state space, and `lambda,rho` are arbitrary complex constants. In
particular, lambda=1 and rho=1/2 would absorb the centered current into
a temporal difference. Every such h is bounded, but the argument uses
no bound on its magnitude and no polynomial ansatz for h.

## 2. Two exact collisions

Scalar Rule 30 evolution from the singleton gives:

| Radius | Time | Window before | Window after | K_t |
|---:|---:|---|---|---:|
| 5 | 20 | `11000001111` | `00100011000` | -1 |
| 5 | 31 | `11000001111` | `00100011000` | 1 |
| 2 | 29 | `00101` | `11101` | -1 |
| 2 | 41 | `00101` | `11101` | -4 |

**Consequently, no h, lambda, rho satisfy (1) at all seed times, for
any radius r<=5.** The two right sides at times 20 and 31 must agree,
whereas the two left sides differ. Restricting both identical windows
to a smaller radius preserves this contradiction. The argument excludes
every lambda, including every proposed unit-modulus temporal multiplier.

Adding a period-four clock does not repair the radius-two case. Both
times 29 and 41 have phase one modulo four, and both next times have
phase two. Thus no four functions h_a can satisfy

```
K_t-rho = h_((t+1) mod4)(W_r(t+1))
          -lambda*h_(t mod4)(W_r(t))                  (2)
```

at all seed times when r<=2. Even allowing lambda and rho to depend
on the clock phase leaves this particular contradiction unchanged.

For an approximate equality with additive residual epsilon_t, identical
right sides force `epsilon_s-epsilon_t=K_s-K_t`. Hence the maximum
residual magnitude at the first pair is at least 1, and at the
clock-preserving pair at least 3/2. These are finite lower bounds,
not lower bounds on an asymptotic average residual.

## 3. Why an unqualified torus test misses the issue

On a spatial ring of length L divisible by four, define P_L and K_L
using the same phase weights and cyclic cells. The
[cutoff identity](RESULTS-quarter-wave-current-target.md) becomes

```
0 = P_L(Fx)-P_L(x)+K_L(x),
```

because x_L=x_0. Thus the bulk ring current is already the temporal
coboundary `K_L=P_L-P_L o F`. Its sum on every temporal cycle is zero.
Removing this current with the correction -P_L simply erases the
observable; it does not yield a center-column estimate. A meaningful
correction must retain the center or boundary contribution and control
the corrected potential. The collisions above test an explicit such
boundary correction on the actual seed, rather than substituting a
different periodic origin.

## 4. Scope and independent verification

The witnesses exclude precisely the displayed window classes and
time ranges containing the witness pairs. They leave open a larger or
growing window, additional history or ancestry, a later-onset identity,
and a sum of local correction terms over the growing half-row. They
also leave open a nonzero residual that cancels on average. None of
these possibilities is supplied with a successful correction here.

The [independent verifier](../../experiments/rule30/quarter_wave_current_collision_audit.py)
checks only the two specified witnesses, without an extended search.
A literal eight-entry Rule 30 truth table generates all rows through
time 42 and agrees with a separate packed integer evolution on all
43 rows. The current is calculated directly both from q_i and from
the weighted multilinear defect

```
D_j = x_j*x_(j+1)+2*x_(j-1)*x_j+2*x_(j-1)*x_(j+1)
      -2*x_(j-1)*x_j*x_(j+1),
K(x) = sum_(j>=1) sin(pi*j/2)*D_j.
```

These two formulas agree on all 43 rows; the independent potential
identity is also checked on all 42 transitions. The
[JSON record](../../experiments/rule30/quarter-wave-current-collision-audit.json)
contains the exact witness rows, currents, potentials, counts, and
verifier hash.

```sh
uv run --offline --no-project python experiments/rule30/quarter_wave_current_collision_audit.py
```

Pass `--output PATH` to additionally write the JSON record.

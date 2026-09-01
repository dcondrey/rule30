# Rule 30 fact and obstruction index

Updated: 2026-09-01

This is a compact lookup table.  Cite the linked result document—not this
index—when publishing.

## Notation and standing controls

```text
F(x)(i) = x(i-1) XOR (x(i) OR x(i+1))
Tr_0(x)_t = F^t(x)(0)
c_t=s(t,0), r_t=s(t,1), l_t=s(t,-1)
```

Position increases rightward.  The regular/striped side is the left side and
the chaotic side is the right side.

Standing controls:

| Object | Required behavior |
|---|---|
| Rule 90 finite row `{-1,1}` | Center is zero forever; any generic P1 exclusion must fail here |
| Rule 30 row `{-8,-1,6}` | Matches `0101...` through time 14, fails at 15 |
| Radius-eight finite rows | 131,071 nonzero rows; maximum alternating inclusive horizon 14 |
| Constant controls | Radius-eight maximum zero/one horizons 8/9; validation only |

## Exact identities

### Local Rule 30 forms

Over `GF(2)`:

```text
F(l,c,r) = l + c + r + c*r.
l_t = c_(t+1) XOR (c_t OR r_t).
```

The OR-latch pin is

```text
s(t,x)=1 => s(t,x-1)=NOT s(t+1,x).
```

It is the principal Rule 30/Rule 90 separator.  Sources: `PATH.md` sections
1–2 and `RESULTS-eventual-period.md`.

### Same-orbit defect

For `D_t(i)=F^(t+2)(y)(i) XOR F^t(y)(i)` and `s_t=F^t(y)`:

```text
D_(t+1)(i) = D_t(i-1) XOR D_t(i) XOR D_t(i+1)
              XOR s_t(i)*D_t(i+1) XOR s_t(i+1)*D_t(i)
              XOR D_t(i)*D_t(i+1).
```

If the two center traces agree, then

```text
D_t(-1) = (1 XOR s_t(0))*D_t(1).
```

Checked on all 64 assignments.  Sources: `RESULTS-eventual-period.md` and the
period-two `RESULTS.md`.

### Exact `F^2` rule

For `(a,b,c,d,e)=y(i-2..i+2)`:

```text
F^2(y)(i) = a XOR d XOR b*d XOR c*d XOR e
             XOR b*e XOR c*e XOR d*e XOR b*d*e XOR c*d*e.
```

The initial defect adds `c`.  Checked on all 32 neighborhoods.  Source:
`experiments/rule30/p1-period2-invariant/RESULTS.md`.

### Alternating center constraint

At each even strobe of a `0101...` trace:

```text
(a_n(-2),a_n(-1),a_n(0),a_n(1)) in {1001,0100}.
```

The opposite phase reduces to this one by applying `F` once.

### Gray–OR macro

For finite frontier words `(A,B)` and inverse Gray code
`I(X)=X XOR (X>>1) XOR ...`:

```text
C = I(A OR (1 OR (B << 1)))
D = I(C OR (A << 1))
survive iff D is odd
(A,B) maps to (D,C).
```

Equivalent boundary-gap form, with `g(X)=X XOR (X>>1)`:

```text
g(C)=A OR (1+zB)
g(D)=C OR zA.
```

Sources: period-two `RESULTS-PARITY.md` and `RESULTS-RUNLENGTH.md`.

### Four-state carry transducer

Read `q=(a,b)` deep-to-shallow with carry `(c,d)`:

```text
c' = c XOR (a OR b)
d' = d XOR (c OR a)
emit (d',c').
```

The four input actions generate the transitive dihedral permutation group of
order eight.  Therefore no input word synchronizes carries and there is no
proper contracting ideal.  Source: period-two `RESULTS-CARRY.md`.

### Odd-row toggle

For `z_t=x_t XOR (t mod 2)`, the rule alternates between

```text
phase 0: 1 XOR left XOR (center OR right)
phase 1: left XOR (center AND right).
```

The two phases compose to exactly `F^2`.  A finite row becomes cofinite on odd
phases, so this does not reduce to the finite-support constant-trace theorem.

### Bilateral hard-core corollary

For an actual `0101...` diagram, put `rho_k=s(2k,1)` and `q_t=s(t,2)`:

```text
rho_(k+1) = (NOT rho_k) AND (NOT q_(2k)) AND (NOT q_(2k+1)).
```

Hence rho contains no `11`.  This is a two-step corollary of the existing pin
cascade, not a separately credited theorem.  Rule 90 fails it.

## Proved exclusions and reductions

| Fact | Scope | Source |
|---|---|---|
| Zero-tail classification | No nonzero finite row has identically zero center trace | `RESULTS-zero-tail.md` |
| All-one fiber | Constant-one trace forces an infinite checkerboard left half | `RESULTS-eventual-period.md`, `RESULTS-inverse-trace.md` |
| Same-orbit reduction | Eventual period `p` reduces to `Tr_0(y)=Tr_0(F^p(y))` for a nonzero finite orbit row | `RESULTS-eventual-period.md` |
| Alternating-fiber survivor map | Past the support knee, rho is forced and each pin is a parity check | `RESULTS-alt-trace-fiber.md` |
| Bounded left-depth certificates | Alternating trace excluded for left depth through 24 only | `RESULTS-alt-trace-fiber.md` |
| Width-two trace theorem | An eventually periodic adjacent width-two trace is excluded in the recorded class | `RESULTS-periodicity-bridge.md` and cited Kopra result |
| Front degree | In every surviving Gray–OR macro, the active front advances exactly one | period-two `RESULTS.md` |

## Exact negative certificates from the period-two attempt

| Candidate class | Exact obstruction | Source/verifier |
|---|---|---|
| Fixed-local additive energies, locality 1–4 | Farkas multisets with endpoint cancellation and nonnegative local gain | `RESULTS.md`, `verify_negative_certificate.py` |
| Finite modular/local quotients | Same-summary, different-future collisions | `RESULTS.md`, `quotient_search.py` |
| Fixed Hasse/mixed moments | `H_k(I(X))=H_k(X) XOR H_(k+1)(X)` plus all-order witness and reachable collisions | `RESULTS-PARITY.md`, `verify_moment_negative.py` |
| Carry contraction/action quotient | D8 permutation group; same action, different successor action/pin | `RESULTS-CARRY.md`, `carry_transducer.py` |
| Bounded RLE summaries | Equal-length summary collision with opposite next pins | `RESULTS-RUNLENGTH.md`, `runlength_search.py` |
| Signed imbalance/contact counts | Two-step summary oscillation and 36-transition Farkas multiset | `RESULTS-DIVERGENCE.md`, `verify_divergence_negative.py` |
| Hard-core plus D8 action | Length-1 and length-3 zero seeds share summary but have different successors | `RESULTS-BILATERAL.md`, `bilateral_hardcore.py` |

These certificates retire the stated classes only.  They do not prove that no
finite-state or nonlinear invariant exists.

## Recurring global obstructions

| ID | Exact warning | Canonical source |
|---|---|---|
| A | `O(log t)` propagation cannot meet a `Theta(t)` target | `PATH.md` 7.3A |
| B | Generic left-permutive reasoning is refuted by Rule 90 | `PATH.md` 7.3B |
| C | Density-continuous 2D statistics are blind to one overwritten column | `PATH.md` 7.3C |
| D | A composition law must be derived and checked, not named | `PATH.md` 7.3D |
| E | Almost-everywhere/ensemble results miss the lone seed | `PATH.md` 7.3E |
| F | Fixed-depth strips move freedom to their outer boundary | `PATH.md` 7.3F |
| G | Arbitrary-input complexity is not fixed-input query complexity | `PATH.md` 7.3G |
| H | Bounded data cannot establish an infinite conclusion | `PATH.md` 7.3H |
| I | Fixed-input satisfiable proof systems hit a small derivation ceiling | `FINDINGS.md` 5b |

## Current open theorem targets

1. **P1, period two:** no-`11` rho plus eventually-zero full forced-left
   reconstruction implies rho eventually periodic.
2. **P1, general R1:** eventual periodicity of `c` forces eventual periodicity
   of `r` on the zero set, using Rule 30's OR in a way Rule 90 lacks.
3. **P2:** a seed-specific orbit-closure/generic-point theorem, not another
   ensemble statistic.
4. **P3:** an unconditional work lower bound for the fixed index-to-bit
   problem, with a model that escapes obstructions D/G/I.

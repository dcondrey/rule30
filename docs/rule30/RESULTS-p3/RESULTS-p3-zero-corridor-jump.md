# Exact H jumps across a chronological zero corridor

Date: 2026-09-13. **A guarded bulk identity is proved, with an explicit
four-step residual and actual-core counterexamples. No faster general
singleton query is obtained.** This continues beyond the already proved
[four-element affine block monoid](RESULTS-p3-aggregate-affine-blocks.md):
the issue here is when its driving histories permit a spatial jump.

Write `x_j(t)=bit_j(H^t(x))`, where

\[
H(x)=(x\gg2)\mathbin{\mathrm{XOR}}((x\gg1)\mathbin{\mathrm{OR}}x),
\quad x_j(t+1)=x_{j+2}(t)+(x_{j+1}(t)\lor x_j(t)).
\]

Additions below are in `F_2`. A zero corridor at column `j+1` means that
this bit is zero at **every specified chronological time**, not merely
at its endpoints or in the initial row.

## 1. Two exact local jump laws

If `x_(j+1)(t)=x_(j+1)(t+1)=0`, then

\[
x_j(t+2)=x_j(t)+x_{j+4}(t).\tag{1}
\]

Proof: the zero column's update forces
`x_(j+2)(t)=x_(j+3)(t)`. Consequently the difference of the two successive
drivers of `x_j` is exactly `x_(j+4)(t)`. This uses both driving columns
and their consistency under H.

Four zero-driver times do not justify blindly doubling (1). The exact
formula, assuming `x_(j+1)(t+i)=0` for `i=0,1,2,3`, is

\[
\boxed{x_j(t+4)=x_j(t)+x_{j+8}(t)
             +x_{j+4}(t)(1+x_{j+6}(t)).}\tag{2}
\]

Here is an algebraic derivation of the residual. Suppress the initial time
and name the successive columns
`z,p,q,r,s,u,v,w,y` at positions `j` through `j+8`. The zero conditions
give `q=r` at the first three times and `u=qs` at the first two. Hence
`q'=q+s` and `s'=s+v` at the needed times. Comparing the update of u with
`u'=q's'` gives

\[
w=s+v(1+q)(1+s),\qquad w(1+v)=s(1+v).
\]

Applying (1) at times t and t+2 gives
`z(t+4)+z(t)=s(t+2)+s(t)=v(t+1)+v(t)`.
The update of v makes the last expression `y+w(1+v)`, proving (2).
The complete five- and nine-bit local truth domains independently verify
(1) and (2); no higher initial input bit can enter these target cones.

## 2. Failure occurs on an actual singleton core

The core family used by the [exact center representation](RESULTS-p3-query-cone-rewrite.md)
includes

```text
C^5(0)=891,
891 --H--> 801 --H--> 889 --H--> 803 --H--> 891.
```

Every state in this cycle has bit two equal to zero. Take `j=1` in (2).
After four steps its bit one is 1, whereas the prediction without the
residual is

```text
bit1(891) XOR bit9(891) = 1 XOR 1 = 0.
```

The missing term is `bit5(891) AND NOT bit7(891)=1`.
This rejects the proposed doubling rule even when its single zero-driver
corridor persists forever. The witness is a value of an actual initial
C-headed query core; the claim being refuted is a row identity at the
specified column.

There can be no finite upper bound on a corridor's length based only on
the finite width above it. Already the smaller actual core has

```text
C^2(0)=12,       12 --H--> 13 --H--> 12.
```

Its width is four and bit one stays zero forever. These are exact closed
cycles, not finite observations extrapolated to arbitrary time.

Even the two-step law needs its chronological guard. Input9 starts with
bit one zero, but H(9)=15 has that bit one. The unguarded two-step formula
predicts1 while H^2(9)=12 has bit zero equal to0.

## 3. An all-length zero-staircase jump

There is a sufficient condition that really closes repeated jumps. Fix
`M>=1`. Assume the following complete triangular collection of zero facts:

\[
x_{j+1+4a}(t+2b+e)=0,
\quad a,b\ge0,\quad a+b\le M-1,\quad e\in\{0,1\}.\tag{3}
\]

Then

\[
x_j(t+2M)=\bigoplus_{a=0}^{M}
 \left(\binom Ma\bmod2\right)x_{j+4a}(t).\tag{4}
\]

Proof: put `y_b(a)=x_(j+4a)(t+2b)`. Every applicable cell of the triangular
region satisfies `y_(b+1)(a)=y_b(a)+y_b(a+1)` by (1). Its M-step update
is therefore `(I+E)^M`, where E shifts a by one. Expanding this commuting
operator proves (4) over the exact finite dependency triangle.

In particular, if `M=2^(s-1)` for `s>=1`, Frobenius gives the two-term jump

\[
\boxed{x_j(t+2^s)=x_j(t)+x_{j+2^{s+1}}(t).}\tag{5}
\]

The Frobenius operation here acts on an already proved linear recurrence
inside the guarded region. It is not being substituted for decimation
of the original nonlinear sequence.

## 4. What a fast use of the identity would have to construct

An explicit certificate of (3) contains `M(M+1)` zero cells. Reading that
certificate is already quadratic in the jump length, before charging the
cost of obtaining its values. The supplied bounded checker constructs
the required H rows and checks each guard; it is a verifier, not a fast
query implementation.

A short all-length guard certificate can exist in special cases. For the
12/13 cycle, the two verified cycle edges prove that column1 is always
zero, and all columns at least4 remain zero. This certifies (3) at `j=0`
for every M without expanding the triangle. No such compact certificate
has been constructed for the general singleton core. The 891 cycle fails
the larger staircase condition even though its one original zero-driver
column persists.

Thus (4)-(5) give a precise bulk operation when the staircase is certified.
They supply neither a cheap method to establish its guards from an arbitrary
binary query index nor a construction of all required initial-row values.
The [existing local-evaluation barrier](RESULTS-p3-local-evaluation-barrier.md)
does not automatically extend to a proof system granted (4) as an additional
rule. The explicit guard count above is a separate construction charge.
The exact new residual (2) identifies what a single-corridor simplification
loses; it does not claim that every other aggregate must retain those bits
explicitly.

## 5. Reproducible exact checks

- [Verifier](../../experiments/rule30/p3_zero_corridor_jump.py).
- [Artifact](../../experiments/rule30/p3-zero-corridor-jump.json).

The verifier checks all 32 five-bit inputs and all 512 nine-bit inputs.
Exactly eight and 32 respectively satisfy their chronological corridor
conditions, and every one satisfies its stated identity. It verifies both
closed actual-core cycles, the residual, the missing-guard counterexample,
and twelve directed staircase controls at jump lengths two through16.
The saved run passed in approximately 0.0004 seconds. No old kernel,
singleton prefix, or frontier census was regenerated.

```sh
uv run --offline --no-project python experiments/rule30/p3_zero_corridor_jump.py
```

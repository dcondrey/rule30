# Exact guarded norm pruning and a whole-block phase obstruction

Date: 2026-09-14. **An all-length guarded identity erases every uncertain
low prefix and gives closed formulas for both marked output bits.** An
alternating word of length `w` above the prefix suffices, with its
construction and linear verification costs retained. The full surviving
tail action is identified exactly as a power of an original binary
generator; that remaining power is not treated as free.

Separately, an exact counterexample rejects deleting the left half of
the actual dyadic norm. Both relevant center readouts change at the
single fixed case N=8, and four exact cycle edges prove that the error
never coalesces. No other norm size is tested. The positive guarded
theorem does not validate this failed omission or complete P3.

**Actual-query applicability is now settled for the whole observer.**
The [fixed-edge proof](RESULTS-p3-actual-alternating-guard.md) shows that
this positive-width alternating guard holds on the actual family only
at center times4 and6. It fails at every other positive-width full
observer, so it cannot supply the proposed asymptotic whole-query
shortcut. The supplied-input theorem remains valid; partial-block
applications and different guards are outside that classification.

## 1. The proposed deletion and its chronology

Use original binary coordinates and ordinary composition, with the
rightmost map applied first:

\[
A(x)=x\mathbin{\mathrm{XOR}}((x\ll1)\mathbin{\mathrm{OR}}(x\ll2)),
\quad B=\tau_0 A,\quad
\alpha_j=A^j\tau_0A^{-j},\quad P_N=\alpha_0\cdots\alpha_{N-1}.
\]

The exact identities are

\[
P_N=B^N A^{-N},\qquad
P_{2m}=P_m\operatorname{Ad}_{A}^{m}(P_m).
\]

Since A fixes zero, the right factor evaluated at zero is

\[
\operatorname{Ad}_{A}^{m}(P_m)(0)=A^m B^m(0).
\]

Thus omitting the whole left factor P_m replaces the actual B^(2m)(0)
by A^m B^m(0). The omission is a modified evaluation; it is not asserted
to be a second singleton trajectory.

The [actual B-query theorem](RESULTS-p3-actual-b-query.md) gives the two
marked observations at exponent N:

\[
c_{2N-2}=\operatorname{bit}_0 H^{N-2}(B^N(0)),\qquad
c_{2N-3}=\operatorname{bit}_1 H^{N-3}(B^N(0)),
\quad H(x)=(x\gg2)\mathbin{\mathrm{XOR}}((x\gg1)\mathbin{\mathrm{OR}}x).
\]

## 2. One exact actual counterexample

For N=8 and m=4, use the established states B^4(0)=100 and
B^8(0)=25712. The latter is also recorded in the
[exact collection artifact](../../experiments/rule30/p3-dyadic-norm-collection.json).
The proposed replacement is

\[
z=A^4(100)=25636,\qquad x=B^8(0)=25712.
\]

The complete integer evaluations are:

| H steps | Actual x | Replacement z | XOR difference |
|---:|---:|---:|---:|
| 0 | 25712 | 25636 | 84 |
| 1 | 28516 | 28479 | 91 |
| 2 | 25647 | 25712 | 95 |
| 3 | 28468 | 28516 | 80 |
| 4 | 25715 | 25647 | 92 |
| 5 | 28519 | 28468 | 83 |
| 6 | 25646 | 25715 | 93 |

At step five the actual high bit of the low digit is1, while the
replacement gives0. This changes c13. At step six the actual low bit is0,
while the replacement gives1. This changes c14. These are the actual
marked indices of the N=8 query, not merely some changed output bits.

## 3. The error never coalesces

The table gives H²(z)=x. The actual state enters the following complete
four-cycle after three steps:

```
28468 -> 25715 -> 28519 -> 25646 -> 28468.
```

The four states are distinct and every edge is checked exactly. Therefore
the cycle has period four. For every t>=2,
H^t(z)=H^(t-2)(x); for t>=5 both values lie on the cycle, two phases apart.
Their XOR difference consequently alternates83,93 forever. Their earlier
differences are all nonzero as well. Thus no later erasure can restore
this particular deleted block.

This differs from the separately certified
[single-correction pruning](RESULTS-p3-balanced-defect-normal-form.md),
where one omission really does coalesce before the marked observation.
The present counterexample rules out unconditional whole-left-block
deletion. It does not rule out a different decomposition, a correction
retained with the smaller expression, or a separately proved chronological
erasure guard. It proves neither a P3 algorithm nor an unrestricted lower
bound.

## 4. A uniform prefix-erasure certificate

Fix `w>=1` and one arbitrary common higher tail `z` in `Z_2`. Let
the original inputs range over **every** lower prefix,

```text
x_u=2^w z+u,        0<=u<2^w.
```

Assume precisely this finite initial guard:

```text
bit_(w+r)(x_u)=1+(r mod2),       0<=r<w.                 (1)
```

The addition in bit formulas is XOR. Thus the common bits at
positions `w,...,2w-1` are `1,0,1,0,...`; no higher tail bits are
restricted. Then the complete all-input identity is

```text
H^w(2^w z+u)=H^w(2^w z),       0<=u<2^w.              (2)
```

Moreover the common marked value has the exact formula

```text
bit_0 H^w(x_u)=bit_(2w)(x_u)+(w mod2).                 (3)
```

**Proof retaining every chronological guard.** The alternating
reference pattern flips all its bits under H. At time `t`, its bit
at position `w-t` is therefore one. For `0<=t<w`, each actual input
agrees with this reference on the finite interval

```text
[w-t, 2w-1-2t].                                       (4)
```

Initially this is exactly (1). In an induction step before the last
time, the first two bits of (4) are `1,0`. The next bit immediately
below the interval is forced to one, since
`0 XOR(1 OR unknown)=1`. Every other bit in the next interval uses
only the old interval. This proves (4), including all the required
chronological ones, directly from the finite initial guard.

Independently, suppose all inputs agree at every position at least
`b` at a given time and their common bit `b` is one. Their next
images agree at all positions at least `b-1`: the new bit there is
the common bit `b+1` XOR one, regardless of its old value. H uses
only current and higher bits, so already-common higher coordinates
remain common. Apply this fact at `b=w-t` for `t=0,...,w-1`, using
(4). After `w` steps every position is common, proving (2). The
last step needs the one at position one; it does **not** require
the next higher bit to be zero.

For (3), first give the extra bit at position `2w` its alternating
value `1+(w mod2)`. The same reference induction now extends to
time `w` at position zero, whose value is one. For any input,
`bit_0 H^w(x)` is the XOR of `bit_(2w)(x)` and a function of the
lower `2w` bits: induction follows from H's highest-input XOR term,
which is absent from the other two input cones. Changing just this
last cone bit therefore toggles the output. This proves (3) for
both values, with the entire higher tail still unrestricted.

Checking (1) reads exactly `w` supplied bits; (3) reads one more.
The [certificate implementation](../../experiments/rule30/p3_prefix_synchronization.py)
does no trajectory expansion and enumerates no lower prefixes.
It uses `O(w)` scalar bit operations, plus charged input/index access,
to certify (2) and return (3). Constructing these supplied higher bits
from an arbitrary norm expression remains part of the query cost.
Computing the full common output of (2) is also not made free.
The [artifact](../../experiments/rule30/p3-prefix-synchronization.json)
retains local induction controls, directed complete-output checks,
and rejection of corrupted guards.

### The complete surviving tail action and both marked bits

There is a stronger complete-map formula behind (2). Define

```text
beta_w=sum_(r=0,...,w-1) (1+(r mod2))*2^(w+r),
x=a+beta_w+2^(2w)z,       0<=a<2^w.
```

Here `z` denotes the tail beyond position `2w`, rather than the
earlier tail beginning at position `w`. Use the original binary
generators with recursions

```text
A=(A,C),      B=(A,C)swap,      C=(B,C)swap.
```

With ordinary composition as elsewhere in this report,

```text
H^w(x)=(CB)^(w/2)(z)                    if w is even,
H^w(x)=(CB)^((w-1)/2) C(z)              if w is odd.    (4a)
```

Thus the letters act in execution order `B,C,...` or `C,B,C,...`,
respectively. Equivalently the complete output is

```text
H^w(x)=B^w(z)    if bit_0(z)=w mod2,
H^w(x)=C^w(z)    otherwise.                            (4b)
```

**Exact guard-preserving induction.** The two-bit section of A is
`A,B,C,C` on low two-bit digits `0,1,2,3`, respectively. At `w=1`
the input's low digit is `2+a`, with `a` zero or one, so
`H(x)=C(z)` for both lower prefixes. Suppose the result is known
for width `w` and start with a guard of length `L=w+1`.
One H update produces the length-`w` guard: its lowest bit is
forced to one by the old initial `1,0`, while the remaining
alternating part flips. No new initial prefix is chosen.

The new tail beyond position `2w` is
`D^(2w)H(x)=H(D^(2w)x)`, where `D(x)=x>>1` and H commutes
with D. The last two old guard bits form digit `c=1` for even L
and `c=2` for odd L, so this tail equals `H(c+4z)`, namely B(z)
or C(z). Therefore the complete tail maps satisfy
`F_L=F_(L-1) B` for even L and `F_L=F_(L-1) C` for odd L,
with `F_1=C`. This proves (4a) for all widths and all tails.
Both B and C flip the root bit and their entire actions coincide
on odd inputs. Replacing the appropriate alternating letters along
the actual root-parity sequence proves (4b), including its guard.

Both marked readouts now have closed formulas. Put
`a=bit_0(z)`, `b=bit_1(z)`, `q=w mod2`, and
`r=floor(w/2) mod2`. Then

```text
bit_0 H^w(x)=a+q,
bit_1 H^w(x)=b+q+r*(1+a+q).                            (4c)
```

Indeed B acts modulo four as addition by one, while C sends the
low digit to three minus that digit. Substitute these actions in
the two branches of (4b); both yield (4c).

The implemented `marked_low_digit` reads the same `w` guard bits
and the two supplied bits at positions `2w,2w+1`. After guard
verification, its Boolean arithmetic is constant size; it performs
no generator-power updates. Input/index arithmetic and construction
of the supplied guard remain charged. The separate
`compile_tail_action` returns the exact B/C power descriptor (4b)
and retains its evaluation cost for any further output bits. Thus
the theorem gives an explicit evaluator for that low/high observer
type. However, the separate
[actual-guard classification](RESULTS-p3-actual-alternating-guard.md)
proves that this guard is absent from the entire actual observer except
at the two small times4 and6. For that use, the missing step was not
merely cheap guard verification: the required predicate is false.
No classification of shorter partial blocks is asserted here.

This is a sufficient erasure-time bound, not an exact minimum-time
test for all contexts. Correlated resets can erase two uncertain
bits at once. If inputs agree from position `j+2` upward and their
common bits `j+2,j+3,j+4` are `0,1,0`, their second H images agree
at every position at least `j`. To prove this, name the old bits
at `j+1,j` by `a,b`. After one step they are `1+a,a OR b`, whose
OR is always one; the common bit at `j+2` has become one. Thus
the next lower bit is zero, and the next upper bit is also reset.
For example,

```text
H^2(8+u+32z) is independent of u,     0<=u<4, z in Z_2.
H^2(8+u)=12.
```

A procedure that waits for each successive coordinate to have a
common-one reset would miss this simultaneous synchronization.
Neither criterion discards a failed chronological guard, and neither
proves that the complete actual norm admits such a guarded pruning.

## 5. Source-block deletion does not halve the remaining time

Even a valid deletion needs a separate construction-cost analysis.
Let `K=N-m`, `e` be zero or one, `t=N-2-e>=0`, and
`n=2N-2-e`. The candidate obtained by deleting the first `m` norm
factors is `A^m B^K(0)`. Its marked observation has the exact form

```text
bit_e H^t(A^m B^K(0))
  =bit_n A^(n-K)(A^K(1) XOR beta_K),
beta_K=1+2*(K mod2).                                   (5)
```

Here `A^K(1)` is the actual singleton row at time `K`, in the
original moving coordinates. Its first two bits are `beta_K`;
XOR with that value deletes just those bits. Formula (5) is therefore
the original final-time-`n` center observation, with a precisely
modified intermediate row and `n-K` further updates.

To check the orientation, put `D(x)=x>>1`. H commutes with D and
`H=D^2 A`, hence `H^t=D^(2t) A^t`. This does not assume that A
commutes with D. The established singleton boundary identity is
`A^K(1)=beta_K+4B^K(0)`, with disjoint low bits. A commutes with
multiplication by four. Consequently the left side of (5) equals

```text
bit_(2t+e+2) A^(t+m)(4B^K(0)),
```

and `2t+e+2=n`, `t+m=n-K` prove the claim. The endpoint cases
`m=0` and `K=0` are included. Building the intermediate state at
time K can be shorter, but the remaining evolution increases to
`n-K`; deleting the block alone has not produced a time-halving
algorithm. This is an exact cost interpretation, not a lower bound
against another compressed evaluation of the remaining map.

## 6. Exact verifier and scope

The [verifier](../../experiments/rule30/p3_actual_norm_block_pruning.py)
reads the saved actual B8 state, evaluates the four A steps of the new
candidate with both raw binary Mealy and Boolean formulas, checks the
two marked observations, and verifies the four cycle edges with a
separate scalar H implementation. The
[artifact](../../experiments/rule30/p3-actual-norm-block-pruning.json)
records the exact values and source hashes.

No growing norm scan, singleton prefix regeneration, frontier census,
group closure, GPU computation, or paid computation is performed.

```
uv run --offline --no-project python experiments/rule30/p3_actual_norm_block_pruning.py
```

# Peel-lift monoid and dyadic propagation

Date: 2026-09-01

Status: **A PERIODICITY-LIFTING LEMMA AND AN EXACT REGULAR-LANGUAGE
CLASSIFICATION OF EVERY PERIOD-DOUBLING BLOCK ARE PROVED.  THEY PROPAGATE
AND SHARPLY CONSTRAIN DYADIC PERIODICITY THROUGH EVERY ENDPOINT SHIFT, BUT
THEY DO NOT YET FORCE THE HARD-CORE ENDPOINT TO BE EVENTUALLY CONSTANT.  THE
PERIOD-TWO THEOREM AND PRIZE PROBLEM 1 REMAIN OPEN.**

The exact checker is `peel_lift_monoid.py`.

## 1. Inverting one Peel row

Write

```text
P(y)_t = phi(y_t,y_(t+1)).
```

For every fixed left state `l`, the map `r -> phi(l,r)` is a permutation.
Hence, for an output symbol `q`, there is a unique map `g_q` satisfying

```text
y_(t+1) = g_q(y_t)  iff  phi(y_t,y_(t+1)) = q.
```

In image-tuple notation the four maps are

```text
g_0=(0,3,2,3)  g_1=(1,2,3,2)
g_2=(3,1,1,1)  g_3=(2,0,0,0).
```

Their transformation monoid has exactly 13 elements:

```text
(0,0,0,0) (0,1,2,3) (0,2,2,2) (0,3,2,3)
(1,1,1,1) (1,2,3,2) (1,3,3,3)
(2,0,0,0) (2,2,2,2) (2,3,2,3)
(3,1,1,1) (3,2,3,2) (3,3,3,3).
```

Direct closure under all four generators verifies the list.  Every cyclic
component of every listed transformation has length one or two.

## 2. Periodicity-lifting lemma

**Lemma.** If `P(y)` is ultimately periodic with a period dividing `p`, then
`y` is ultimately periodic with a period dividing `2p`.

**Proof.** After the output enters its `p`-periodic tail, one block of `p`
output symbols advances `y_t` by a fixed composition of the maps `g_q`.
That composition belongs to the displayed 13-element monoid.  Its orbit on
the four possible states eventually enters a cycle of length one or two.
Therefore the lifted row eventually repeats after `p` or `2p` steps.  QED.

In particular, a lift of an ultimately dyadic-periodic Peel image is itself
ultimately dyadic-periodic.  No odd factor can be introduced by peeling
backward.

## 3. Exact language of period-doubling blocks

Only three elements of the displayed monoid have a two-cycle:

```text
(1,2,3,2), (2,0,0,0), (3,2,3,2).
```

The input words producing those elements have an exact regular-language
description.  A nonempty Peel-output block `q` admits a cyclic lift of twice
its block period if and only if

```text
q belongs to {0,1}* and has odd weight in symbol 1,
or
q belongs to {0,3}* and has odd weight in symbol 3.        (1)
```

Thus any occurrence of state `2`, or any mixture of states `1` and `3`,
prevents a period-doubling cyclic lift.  The condition is much stronger than
odd total activity: every nonzero symbol in the driver block must have one
common type.

**Proof.**  Let the complete 13-state monoid automaton read an output word by
right composition and accept exactly when its return transformation has a
two-cycle.  In parallel, use the finite automaton whose states record:

```text
only zeroes so far;
alphabet {0,1} plus parity of the number of 1s;
alphabet {0,3} plus parity of the number of 3s;
dead after a 2 or a mixture of 1 and 3.
```

Accept the two odd-parity states.  The synchronous product has 13 reachable
state pairs.  On every one, the two acceptance predicates agree, and every
outgoing symbol is checked.  Finite product exhaustion therefore proves
language equivalence for words of every length.  The checker performs this
complete product traversal in `period_doubling_language_control`; it is not a
finite maximum-length test.  QED.

The drivers `00000111` and `00001101` in the recorded `8 -> 16` profile
collision both satisfy (1): they use only `0,1` and contain three `1`s.  The
classification explains that collision's common ability to double without
claiming that their lifted cycles or entry states are identical.

## 4. Strict doublings are isolated

The language classification has a stronger dynamical consequence.

**Lemma (no consecutive strict doublings).**  If a period-`p` Peel-output
block has a cyclic lift of primitive period `2p`, that lifted block cannot in
turn have a cyclic lift of primitive period `4p`.

**Proof.**  For a `{0,1}` driver of odd `1` parity, the unique return
two-cycle is `{2,3}`.  Generator `g_0` fixes both states and `g_1` swaps them.
The entire doubled lift therefore uses only `2,3`, and it contains both: one
turn around the driver takes either two-cycle state to the other.  For a
`{0,3}` driver of odd `3` parity, the same argument uses the two-cycle
`{0,2}`; `g_0` fixes its states and `g_3` swaps them.  That doubled lift uses
and contains both `0,2`.

In either case the lifted block contains state `2`.  Section 3 proves that
every block containing `2` is outside the strict-doubling language.  QED.

Consequently, if successive cuts in a rotated-Peel tower have dyadic minimal
periods `2^k`, the exponent can increase at most once in any two consecutive
endpoint shifts.  Starting at exponent `k`, after `j` shifts the period
therefore divides

```text
2^(k+ceil(j/2)).
```

This improves the one-doubling-per-shift bound but is still not uniform in
`j`.  In particular, it does not prove the dyadic lock.

## 5. The complementary `D8` orientation

There is an exact reason the 13-element monoid here and the eight affine
boundary states elsewhere both arise.  Curry the same table in the opposite
direction:

```text
h_r(q) = g_q(r).
```

For fixed `r`, let `L_r(u)=phi(r,u)`.  Directly from the defining inverse
relation,

```text
h_r = L_r^(-1).
```

The four `h_r` are

```text
h_0=(0,1,3,2)  h_1=(3,2,1,0)
h_2=(2,3,1,0)  h_3=(3,2,1,0),
```

and they generate the eight-element dihedral permutation group `D8`.  Thus:

- fixing the Peel output gives the 13-element, generally noninvertible lift
  monoid and controls temporal period growth;
- fixing the queue input gives inverse local permutations and controls the
  queue scan, affine boundary phase, and frontier-cover monodromy.

More explicitly, let `D=(d_0,...,d_(m-1))` be the newest dependency diagonal
of an endpoint prefix, let `p` be its final endpoint state, and let `A` map a
new endpoint state to the newly exposed cut state.  Reversing the local
triangle gives the exact word identity

```text
A^(-1) = B^(-1) o h_p o h_(d_0) o ... o h_(d_(m-2)).
```

The old final diagonal cell `d_(m-1)` initializes the desired tail and is not
read by the reverse scan.  The checker confirms this identity against the
literal triangle on all 5,461 endpoint prefixes through length six; the
proof is the displayed composition of the local inverse identities.

This identifies the ordered zero-prefix affine differences as `D8` holonomy
defects.  Their order must be retained: multiplying the defects down to one
endpoint product permits the cancellations already observed in the failed
derivative probes.

## 6. Combination with the rotated identity

Put

```text
x^j = I(sigma^j e).
```

The proved rotated identity is

```text
P(x^(j+1)) = sigma^2 x^j.
```

If `x^0=I(e)` is ultimately periodic with period `2^k`, the lemma inductively
shows that every endpoint-tail cut `x^j` is ultimately dyadic-periodic, with
a period dividing `2^(k+j)`.

This is the missing rigorous bridge between a dyadic initial cut and all
successive endpoint tails.  It does **not** give a uniform period bound in
`j`, so it does not imply that `e` is eventually periodic.

## 7. Exact controlled-lift reformulation

Let

```text
a_j = x^j_0 = B(e_j).
```

For a hard-core endpoint, `a_j` belongs to `{1,2}` and the word `a` contains
no factor `22` (because `B` interchanges endpoint states `1` and `2`).  The
entire two-dimensional inverse-cut array is then determined by

```text
x^(j+1)_0     = a_(j+1),
x^j_1         = phi(B(a_j),a_(j+1)),
x^(j+1)_(t+1) = g_(x^j_(t+2))(x^(j+1)_t).            (1)
```

The middle line is essential boundary data; the rotated Peel equation alone
does not characterize inverse-terminal cones.  On admissible hard-core
pairs it reduces to

```text
(a_j,a_(j+1)) = (1,1) or (2,1)  ->  x^j_1=2,
(a_j,a_(j+1)) = (1,2)           ->  x^j_1=0.
```

The desired dyadic lock is now the following precise statement:

> Every infinite solution of (1) for which `x^0` is ultimately
> dyadic-periodic and `a` is a `{1,2}` word without `22` is eventually the
> fixed solution `a_j=1`, `x^j=(12)^omega`.

This statement would imply that the endpoint is eventually `2^omega`; the
already proved reachability separator would then finish the nonconstant
period-two exclusion.

The reverse-period trees for periods `2,4,8,16` verify bounded instances of
this lock.  Sections 3-4 now say that every strict doubling in a hypothetical
unbounded tower must be driven by one of the two parity-pure languages in
(1), and that two such events cannot be consecutive.  The remaining uniform
question is whether the hard-core boundary data and lasso entry state can
support infinitely many separated events.  Merely keeping the exact periodic
cycle is insufficient: the recorded branch at endpoint shift 26,603 proves
that the finite lasso prefix can select different fixed entry states for the
same return word.

## 8. Relation to the `(z+1)`-adic proposal

The sound dyadic operator is `Delta=1+S`, where `S` is temporal shift.  On an
`N=2^k` cycle,

```text
Delta^N = 1 + S^N = 0.
```

At the half scale `h=N/2`, `D_h=1+S^h` maps an `N`-periodic word to an
`h`-periodic defect, and `D_h x=0` exactly when `x` already has period
dividing `h`.  Coordinatewise multiplication obeys the exact difference
rule

```text
D_h(f*g) = f*D_h(g) + g*D_h(f) + D_h(f)*D_h(g).
```

This is the appropriate filtered difference algebra for the OR gate.  OR is
not the cyclic-convolution product in the coefficient presentation of
`F_2[z]/(z^N-1)`.

## 9. Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/peel_lift_monoid.py
```

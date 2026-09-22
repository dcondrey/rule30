# Neighboring scales have an exact forced-continuation identity

Date: 2026-09-15.

**An all-length continuation identity and explicit realization of the
two-row live-state embedding are proved below.** The result connects
overlapping source words at neighboring scales. It supplies no mortality
bound, rotated-wedge separator, period-two exclusion, or solution of P1.

The [checker](../../experiments/rule30/p1_continuation_scale_shift_audit.py)
and [saved audit](../../experiments/rule30/p1-continuation-scale-shift-audit.json)
contain bounded implementation controls. The universal quantifiers come
from the symbolic arguments, not those controls.

## 1. Force the complete cut symbol

Use the four-state endpoint alphabet `A={0,1,2,3}`, inverse-terminal map
`I`, left shift `sigma`, and local Peel map

```text
P(x)_i = phi(x_i,x_(i+1)),       G_n = P^n o I.
```

For a nonempty source `W in A^n` and `c in {2,3}`, define `Q_c(W)` to be
the unique infinite four-state word such that

```text
G_n(W Q_c(W)) = c^infinity.                              (1)
```

Existence and uniqueness hold for every source, without a binary or
hard-core assumption. When a new endpoint symbol is appended, the newest
cell of `G_n` is a permutation of that symbol: it is a composition of the
boundary permutation and fixed-left rows of `phi`. This is the same
all-length triangular argument used in the
[high-bit elimination report](../../experiments/rule30/p1-period2-invariant/RESULTS-BINARY-WEDGE-HIGH-ELIMINATION.md).
Exactly one of the four endpoint symbols attains the specified output
`c`. Inductively choosing it gives compatible prefixes of every length
and hence the unique infinite word in (1).

This `Q_c` forces **both bits** of every output cell and permits appended
symbols `0` and `3`. It is not the binary high-bit-only continuation
`Q_n(W)` used to define `Psi`. No equality of those two continuation maps
is being assumed after their constraints diverge.

The padded implementation computes (1) exactly, since the iterated
rotated identity gives

```text
G_n(f) = sigma^(2n) I(0^n f).                            (2)
```

## 2. Delete one source symbol and append two forced symbols

Write `Q=Q_c(W)` and define a word of length `n+1` by

```text
S_c(W) = W[1:] Q[:2].                                    (3)
```

Then, for every nonempty four-state source,

```text
Q_c(S_c(W)) = Q_c(W)[2:].                                (4)
```

**Proof.** The
[rotated inverse-cone identity](../../experiments/rule30/p1-period2-invariant/RESULTS-ROTATED-PEEL-IDENTITY.md)
holds for every one-sided four-state endpoint:

```text
P I(sigma f) = sigma^2 I(f).
```

Also `P sigma = sigma P` directly from the local definition of `P`.
Apply both identities to `f=WQ`:

```text
G_(n+1)(sigma f)
  = P^n P I(sigma f)
  = P^n sigma^2 I(f)
  = sigma^2 G_n(f)
  = c^infinity.
```

The first `n+1` symbols of `sigma f` are exactly `S_c(W)`; the remainder
is `Q[2:]`. Uniqueness in (1) proves (4). Every infinite-word equality
here is an equality of finite coordinates under prefix-causal maps.

More generally, the compatible source at scale `n+k` is the block
`f[k:n+2k]`, and its forced continuation is `Q[2k:]`. This follows by
iterating (4), or by applying the rotated identity `k` times. Thus
neighboring scales cannot be chosen independently along one forced
trajectory.

## 3. Equality of the complete live states

Let `E(A)` denote the newest dependency edge after reading a finite
endpoint word `A`, indexed by depth from zero. Its recurrence is the one
implemented in
[constant_tail_scale.py](../../experiments/rule30/p1-period2-invariant/constant_tail_scale.py):

```text
new[0] = B(q),
new[1] = phi(previous_endpoint, new[0]),
new[d] = phi(old[d-2], new[d-1])            (d>=2).
```

The live state is `E(A)[:-1]`: the last entry is the current cut cell,
which the next append does not read. For every `W in A^n`, `n>=1`, and
every pair `q_0,q_1 in A`,

```text
E(0^n W q_0 q_1)[:-1]
  = E(0^(n+1) W[1:] q_0 q_1)[:-1].                       (5)
```

No forcing assumption on the appended pair is needed in (5).

**Dependency proof.** The edge entry at endpoint position `i` and depth
`d` depends only on input positions

```text
[i-ceil(d/2), i].                                        (6)
```

The claims for `d=0,1` follow from the first two recurrence lines. For
`d>=2`, the left argument has last endpoint `i-1` and depth `d-2`, so its
earliest possible input is
`i-1-ceil((d-2)/2)=i-ceil(d/2)`. The right argument has depth `d-1` and
no earlier dependency. Induction proves the dependency upper bound (6).
No claim that every listed coordinate is essential is required.

The words on the two sides of (5) have length `2n+2` and differ only at
absolute input coordinate `n`: the first symbol of `W` is replaced by
`0`. Their live edge entries have `i=2n+1` and `0<=d<=2n`. By (6), all
their inputs have index at least `n+1`. The changed coordinate is outside
every live dependency interval, proving (5).

Dropping the final cell is essential. For example,
`E(0100)=(3,2,1,1)` and `E(0000)=(3,2,1,2)`: their live states agree,
but their complete edges do not. The checker retains this negative control.

Starting from the live state associated with `0^nW`, append the first
two forced symbols of `Q_c(W)`. Equation (5) identifies the resulting
live state with the initial live state for the explicit source `S_c(W)`
at level `n+1`. This establishes at all lengths the realizability
previously recorded as finite evidence in
[fembed_RESULTS.md, section A](../../experiments/rule30/p2-needle-attack/fembed_RESULTS.md).
That report explicitly distinguished the already proved survival shift
from the then-unproved realizability assertion. Its stored representative
word need not equal (3), because distinct source words can represent one
live state. No injectivity or preservation of survivor counts is asserted.

This source transformation deletes a symbol before appending two. It
does not assert that a source at scale `n+1` extends the source at scale
`n`; consequently it does not contradict the append-only obstruction in
[the Gamma proof attempt, section 2](../../experiments/rule30/p1-period2-invariant/RESULTS-GAMMA-PROOF-ATTEMPT.md).

## 4. Binary and hard-core scope; no mortality deduction

If `W` is binary, `S_c(W)` is binary exactly when the first two symbols
of `Q_c(W)` belong to `{1,2}`. Define `h_c(W)` to be the length of the
initial binary continuation, with value infinity if it never fails.
Then whenever `h_c(W)>=2`,

```text
h_c(S_c(W)) = h_c(W)-2.                                 (7)
```

The same formula holds for the hard-core continuation horizon that also
forbids `11`, including the junction with the last source symbol. If its
first two appended symbols are legal, the new junction is exactly the
old continuation junction after those two symbols. When the source
itself is hard-core, (3) preserves that source restriction as well.

For the stronger actual-endpoint language avoiding both `11` and
`22222`, the new complete source remains in that language whenever
`W Q[:2]` is in it, because (3) takes a suffix. This is compatible with
the narrower scale-word domain established in
[the guarded seam report, section 1](../../experiments/rule30/p1-period2-invariant/RESULTS-RW-GUARDED-SEAM-DESCENT.md).
It does not assert actual-right realizability or actual-orbit ancestry
for arbitrary words satisfying those forbidden-factor tests.

For a finite horizon, (7) gives

```text
h_c(S_c(W)) + 2(n+1) = h_c(W) + 2n.                      (8)
```

This quantity is the absolute first-failure position in the moving
scale coordinates. It is not a computable finite ranking function
supplied by this theorem: using its finiteness would already assume
mortality. In particular, (7) is equally consistent with infinite
survival at every scale. It gives the known lower bound on maximal
survival, not the upper bound needed for a wedge horizon theorem.

The useful new audit result is the uniform realization and explicit
compatibility map, not a separator proof. A future argument would need
to exclude an infinite compatible trajectory using additional structure;
merely renaming the continuation horizon as a potential does not do so.

## 5. Reproduction and bounded controls

```sh
uv run --no-project python \
  experiments/rule30/p1_continuation_scale_shift_audit.py
```

The checker reconstructs `phi` independently from Boolean coordinates,
checks all sixteen local entries and four boundary symbols, and compares
independent scalar-coordinate edge reconstruction against the maintained
append implementation on all 5,460 four-state words of lengths one
through six. It also checks:

- (5) on all 21,824 four-state source/appended-pair cases through source
  length five;
- (4) on all 1,020 binary source/tail cases through length eight, with
  twelve forced symbols before the shift and ten afterward;
- (4) on 168 arbitrary four-state source/tail cases through length three;
- both complete constant-cut equalities with the independent scalar
  wedge reconstruction, and the horizon recurrence whenever a first
  failure is observed within the bounded continuation.

Unfailed finite prefixes are not treated as infinite survivors. The
artifact records the exact finite horizon-check counts and source
hashes. These checks validate implementation and indexing; the
all-length proofs are in sections 1–3.

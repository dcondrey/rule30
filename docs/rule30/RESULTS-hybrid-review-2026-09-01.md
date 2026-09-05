# Hybrid review of the Rule 30 attempt archive

Date: 2026-09-01

Status: **TWO NEW UNIFORM P1 LEMMAS; NO PRIZE PROBLEM SOLVED.**

## Scope

This review cross-checked the compact index, fact index, ranked route register,
frontier-attack findings, and the complete current period-two resumption sheet.
The purpose was not to rename retired ideas, but to find places where the
output of one exact technique supplies a missing hypothesis of another.

## 1. Strongest surviving hybrid: dyadic cascade + reachability + acceptance

The dyadic-period audit stopped because accepted cuts include the infinite
family eventually equal to `(12)^omega`. The audit compared period spectra
but did not use the fact that a relevant cut must lie in the orbit of
`0^omega` under a finite generator word.

Adding that missing reachability condition repairs the exception. A uniform
width descent proves that no generated zero-ray cut is eventually alternating;
hence every accepted cut arising from an endpoint eventually equal to
`2^omega` is unreachable. The proof and independent checks are in
`experiments/rule30/p1-period2-invariant/RESULTS-DYADIC-EXCEPTION-SEPARATOR.md`.

The same calculation exposes a stronger output-only condition. With

```text
(Peel x)_t = phi(x_(t-1),x_t)
            = tau_(swap(x_(t-1)))^(-1)(x_t),
```

peeling one core symbol is exactly one application of `Peel`, apart from a
finite prefix. A cut produced by an `m`-symbol core is therefore eventually
killed by `Peel^m`. This is stronger than saying that the cut has dyadic
eventual period.

The noteworthy coincidence is literal, not analogical: `phi` is also the
local rule in the inverse-terminal diagonal recurrence. The period-two target
can now be attacked as a collision between two triangles built from the same
four-state table:

> For every hard-core endpoint `e`, if `x=inverse_terminal(e)`, prove that no
> finite iterate `Peel^m(x)` is eventually zero.

This retains the unbounded ordered object required by all previous negative
certificates, uses finite-left support through `Peel`-nilpotence, and uses
Rule 30's OR through the hard-core endpoint condition. It is the best new
proof target found in this review.

## 2. How to combine the remaining positive fragments

### 2.1 Use the inverse-cone recurrence as a rotated-triangle invariant

The inverse-terminal recurrence and `Peel` use the same `phi`. A viable next
lemma should be a rotated-square, braid, or boundary identity comparing:

```text
endpoint e  --inverse terminal phi-triangle-->  cut x
cut x       --iterated Peel phi-triangle----->  peeled cuts.
```

This is not another fixed summary. It keeps every boundary symbol and asks
for a uniform relation between two orientations of the complete triangle.
The immediate falsifier is an exact hard-core endpoint whose inverse cut is
eventually `Peel`-nilpotent.

The proposed rotated identity was subsequently derived exactly.  With `I(e)`
the inverse-terminal cut, `sigma` the one-sided shift, and zero-indexed Peel
`P`,

```text
P(I(sigma e)) = sigma^2 I(e).
```

It implies exact linear drift of positive finite Peel rank under endpoint
shift.  A last-support argument using `phi(s,0)=3` for `s!=0` handles rank
zero.  Therefore every hard-core endpoint whose inverse cut has finite Peel
rank is aperiodic.  The remaining collision target is the aperiodic endpoint
case.  Proof and checks are in the period-two
`RESULTS-ROTATED-PEEL-IDENTITY.md`.

### 2.2 Pull Craig separators back through `Peel`, not through translation

The small-cut CNFs have cubic separators, while translation-stable local
clauses fail at the next width. The defect/restart cocycle explains why:
translation changes the restart phase and omits the growing driver. A better
interpolant experiment is to ask whether a separator `I_m` pulls back under
the exact local peel,

```text
I_m(x) = I_(m-1)(Peel x) plus a boundary/restart term,
```

with the boundary term taken from the exact restart partition. This blends
the cubic interpolants, corner peel, and restart cocycle without assuming a
fixed spatial motif. Minimum clauses or isolated cubic fits alone should not
be extended again.

### 2.3 Revisit the two weak tail balances only with global compatibility

The inequalities

```text
2 wt(L) >= wt(rho),
2 (wt(L)+wt(rho)) >= n
```

remain compatible with the recorded finite evidence and together would force
positive reconstructed-left density. Radius-seven discharging failed because
locally legal factors from different frontiers can be spliced into negative
cycles. The exact `Peel` ancestry supplies the missing global compatibility:
legal label blocks should be conditioned on belonging to one finite
`Peel`-preimage tree, not merely on appearing somewhere. Any renewed balance
proof must use that ancestry or an equivalent noncrossing matching; another
fixed-radius de Bruijn potential repeats the certified failure.

### 2.4 Add actual-right restrictions only after the hard-core split

The exact right-side constraints `no 11`, `no 00000`, and the further
forbidden factor `101001` were previously used as a flat finite-factor filter;
that recognizer is incomplete. They can still help after the new split:
mine or prove which non-eventually-`2` hard-core endpoints with dyadic inverse
cuts survive the exact right light-cone presentation. The proof object must be
the genuine right cone or a proved symbolic presentation of it, not a longer
ad hoc forbidden-word list.

## 3. What does not become viable by mixing

- The D8 action, bounded run summaries, fixed Hasse moments, and local additive
  energies remain excluded by exact closure or Farkas certificates. Appending
  one of them to `Peel` does not restore the information they discarded.
- The dyadic-period theorem alone is still insufficient. The new lemma removes
  its known period-two counterfamily only after reachability is imposed; the
  non-eventually-`2` hard-core case remains open.
- P2 ensemble ergodicity cannot be transferred to the lone seed by any P1
  boundary statistic currently in the archive. The measure-zero orbit gap is
  unchanged, and checkerboard-patch growth remains evidence rather than
  membership in the orbit closure.
- P3 proof-complexity, arbitrary-input ANF, and finite circuit results remain
  separated from the fixed index-to-bit lower bound. The new `Peel`
  formulation could expose an evaluation shortcut and is therefore useful as
  a P3 falsifier, but it supplies no lower bound.

## 4. Recommended order of work

1. Use the proved rotated-triangle identity to rule out an aperiodic
   hard-core endpoint with finite Peel rank.
2. Synthesize `Peel`-recursive cubic interpolants with
   the exact restart branch as an explicit boundary state.
3. In parallel only conceptually, test whether the two weak balances admit a
   global matching on one `Peel`-preimage tree.
4. Use the exact right cone to attack only survivors of those tests.

The key change is to organize the proof around finite `Peel` ancestry rather
than around bounded summaries of a growing frontier. That is the one synthesis
in this review not already covered by a retained negative certificate.

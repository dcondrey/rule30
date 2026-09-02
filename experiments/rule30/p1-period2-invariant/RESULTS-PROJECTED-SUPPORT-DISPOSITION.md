# Projected diagonal support: algebra and irreducible lemma

Date: 2026-09-01

Status: **THE PROJECTED-SUPPORT ROUTE IS REDUCED TO ONE FULL-QUEUE
CONTRAPOSITIVE.  ITS LOCAL AFFINE CONTENT IS COMPLETELY EXPLICIT, WHILE
ENDPOINT TELESCOPES, BOUNDED DEFECT STATES, AND LOCAL EDGE MONOTONICITY ARE
KILLED.  THE CONTRAPOSITIVE REMAINS OPEN.**

## 1. Exact target and consequence

For the zero-prefix scenarios

```text
W^(k)=0^k W[k:n]
```

let `A_(j,k)=(alpha,beta,gamma)` be the newest endpoint-to-cut affine map at
forced row `j`.  The sufficient diagonal-support statements are:

```text
tail 2: some k>=j changes (alpha,beta),
tail 3: some k>=j changes (alpha,gamma)
        on every nonfinal legal row.                  (1)
```

Applying (1) only at the final tail-2 row or final nonfinal tail-3 row gives

```text
s_2(W)<=n,
s_3(W)<=n+1,
```

and therefore the rank-zero separator.  No matching theorem is needed.

## 2. Complete local affine meaning

For

```text
A(h,l)=(h+alpha,l+beta*h+gamma),
```

forcing cut state `2` or `3` gives a hard-core endpoint exactly under the
following table:

```text
tail 2 legal iff gamma = alpha OR beta,
tail 3 legal iff gamma = NOT(alpha OR beta).          (2)
```

Whenever legal, the forced endpoint state is

```text
2-alpha.                                              (3)
```

Thus `alpha` is the endpoint bit that distinguishes states `1` and `2`; the
other selected coordinate is precisely what allows the omitted affine bit to
be recovered from legality.

The two projections have different algebraic roles:

- `(alpha,beta)` is an additive quotient of the `D8` composition law;
- `(alpha,gamma)` is the literal state `A(0)` and is not a group quotient.

`constant_tail_projected_support_algebra.py` verifies (2)-(3), all 64 affine
products in the first quotient, and all eight evaluations in the second.

## 3. Why an endpoint telescope is insufficient

If every adjacent projection in (1) were equal, the two endpoint scenarios
would of course agree.  The converse is false because ordered changes can
cancel.  The smallest retained example is

```text
W=121, tail=3, row=0, survival=4,
```

whose `(alpha,gamma)` values along zero-prefix scenarios `k=0,1,2,3` are

```text
(0,1), (1,0), (1,0), (0,1).                          (4)
```

The first and last values agree even though internal support is present.
Therefore comparing only scenario `k=j` with the all-zero scenario loses the
ordered defect word used by (1).

## 4. Why the defect word is an observable, not a state

The complete ordered `D8` defect word plus its rightmost affine anchor
reconstructs every current `A_(j,k)`.  Nevertheless it does not determine the
next defect word.  Exact reachable collisions persist after adding every
scenario's previous endpoint, and a preregistered two-ended depth-one repair
fails at length 13.  Only the complete reversed dependency queues are closed.

Likewise:

- every binary `2x2` projected edge pattern occurs, excluding a local Monge
  or total-monotonicity proof;
- the decisive projected token can jump by an unbounded distance, excluding
  a fixed-radius propagation table; and
- strict dual colex descent applies to inherited coordinates of one queue,
  but its newly appended boundary can reset the comparison and fan out
  through arbitrarily long zero runs.

These are exact structural obstructions, not reasons to distrust (1).

## 5. Irreducible contrapositive

The route's remaining all-length lemma is now:

> Start from the complete family of reversed dependency queues for scenarios
> `k=j,...,n`.  If every adjacent tail-2 `(alpha,beta)` projection is equal,
> then row `j` is not tail-2 legal.  If every adjacent tail-3
> `(alpha,gamma)` projection is equal, rows `j,j+1` cannot both be tail-3
> legal.

The proof must use the full queue recurrence, an exact unbounded ancestry
quotient, or a leading-term argument equivalent to it.  No bounded defect
annotation or endpoint product is a closed enough state.

The registered exhaustive and random corpora contain no counterexample, but
they do not prove the contrapositive.  Further width sweeps are not an
admissible next step under the six-route evidence gate.

## 6. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_projected_support_algebra.py
```

For the closure collisions and held-out support audits, use the commands in
`RESULTS-HOLONOMY-DEFECT-CLOSURE.md` and
`RESULTS-PROJECTED-DIAGONAL-HALVING.md`.

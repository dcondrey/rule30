# Nonfinal alpha support: exact holdout and proof disposition

Date: 2026-09-02

Status: **THE FROZEN FINITE HOLDOUT HAS ZERO FAILURES, BUT THE CANDIDATE IS
NOT A PROOF REDUCTION.  AT THE FIRST EMPTY-DIAGONAL ROW IT IS EXACTLY THE
DESIRED SCALE-SURVIVAL BOUND IN DIFFERENT WORDS.  IT IS RETIRED AS A PRIMARY
ROUTE.  PERIOD TWO REMAINS OPEN.**

## 1. Candidate and exact consequence

For a binary hard-core word `W` of length `n`, let `alpha_(j,k)` be the
high-translation coordinate of the constant-tail boundary permutation in
the zero-prefix scenario

```text
W^(k)=0^k W[k:n],       0<=k<=n.
```

The frozen candidate was:

> If the original scenario survives through row `j+1`, some `k` with
> `j<=k<n` satisfies
> `alpha_(j,k) != alpha_(j,k+1)`.

Taking `j=n` makes the witness interval empty.  Therefore the statement at
that single row says precisely

```text
the continuation cannot survive through row n+1,
equivalently s_c(W) <= n+1.                         (1)
```

Conversely, (1) makes every instance with `j>=n` vacuous on the premise.
Thus the part of nonfinal alpha support that closes the scale separator is
not an independently simpler lemma: it is the desired scale bound itself.
The alpha vocabulary supplies useful diagnostics for rows `j<n`, but it
does not explain (1).

This is stricter route triage than the original preregistration.  The
candidate remains true on every completed finite test, but it must not be
reported as progress toward an all-length proof merely because its
empty-interval consequence is immediate.

## 2. Frozen held-out result

Before testing, discovery used every hard-core word through length 17.  The
held-out exact range was every hard-core word at lengths 18 through 23, for
both constant tails.  It produced

```text
word/tail cases:             370,944
nonfinal rows audited:       102,014
alpha-support failures:            0.
```

The completed deterministic random rows used 2,000 words per tail at each
of lengths 24, 32, 48, 64, and 96:

```text
length                 24    32    48    64    96
word/tail cases      4000  4000  4000  4000  4000
nonfinal rows        1101  1154  1114  1196  1156
failures                0     0     0     0     0
```

The preregistered length-128 random row was interrupted before completion
when the route-disposition observation above made further sampling
low-value.  It is not included in the totals.  The completed held-out corpus
therefore contains 390,944 word/tail cases and 107,735 nonfinal rows, with
zero failures.  These are finite facts only.

The hard-core source restriction is load-bearing.  With arbitrary binary
sources, tail `2`, `W=2112`, survival two, and row zero give no alpha support;
the source contains `11`.

## 3. What remains live

The strictly smaller sufficient statement remains the three-row late-pull
diagonal `(DLP)`:

```text
no surviving pull occurs at j in {n,n+1,n+2}.
```

Unlike nonfinal alpha support, DLP asks only for the endpoint event needed
by the uniform scale-placement theorem.  Its best current algebraic form is
the rotated finite wedge in `RESULTS-DLP-ROTATED-WEDGE.md`.  A proof must use
the binary source boundary and the complete constant-cut history; a fixed
terminal window and a single backward source-defect path are both already
falsified.

The other genuinely weaker live route is endpoint-derived pull ancestry:
all pull roots are proved to lie in the final three initial queue
coordinates, and it is enough to prove any finite depth bound depending on
the initial length.  Neither route is closed by the present experiment.

## 4. Reproduction

The exact held-out checker is:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/constant_tail_nonfinal_alpha_support.py \
  --first-length 18 --last-length 23 --random-per-length 2000
```

The complete default command includes the unfinished length-128 random row;
the exact lengths 18--23 and the five completed random rows above are the
recorded result.

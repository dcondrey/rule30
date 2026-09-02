# Actual-right terminal frontiers and D8-conditioned distances

Date: 2026-09-01

Status: **A UNIFORM ACTUAL-RIGHT TERMINAL INVERSE SYSTEM IS PROVED, AND THE
CONDITIONED FINITE DISTANCES SEPARATE SHARPLY FROM THE ABSTRACT HARD-CORE
TARGET.  HOWEVER, RANK DESCENT CAN ADD AN ARTIFICIAL FINITE ENDPOINT PREFIX,
SO WHOLE-PREFIX ACTUAL-RIGHT CONDITIONING IS NOT BY ITSELF A PERIOD-TWO
REDUCTION.  PERIOD TWO AND P1 REMAIN OPEN.**

The preregistration is `PREREGISTRATION-ACTUAL-RIGHT-FRONTIER.md`; the exact
checker is `constant_tail_actual_frontier.py`.

## 1. Condition the existing terminal set

At horizon `h`, the abstract frontier graph accepts

```text
A_h={I(e): e in {1,2}^(h+1), e avoids 11}.
```

Endpoint state `1` encodes rho bit `1`, while state `2` encodes rho bit `0`.
Let `R_n` be the complete length-`n` trace language at column one of a Rule 30
right half-plane whose center boundary is `0101...`.  Define

```text
A_h^right={I(e): e avoids 11 and bits(e) is in R_(h+1)}.       (1)
```

Membership in `R_n` is decided by the full minimal right light cone with
`2n-1` free initial cells.  It is not approximated by a list of forbidden
factors.

## 2. Uniform projection theorem

Let `pi_h` delete the last frontier coordinate.  Then for every `h>=1`,

```text
pi_h(A_h^right)=A_(h-1)^right.                       (2)
```

The inclusion from left to right is causality and prefix compatibility of
the inverse cone.  For the reverse inclusion, take a length-`h` right-cone
witness.  Its initial cells occupy positions `1,...,2h-1`.  Append any two
new initial cells, for example zeros.  The first `h` even-time column-one
samples are unchanged, and the enlarged cone supplies one further sample.
Every actual alternating-center trace already avoids `11`, so the resulting
endpoint extension remains hard-core.  The inverse-terminal map is prefix
compatible, proving (2).

Thus the conditioned terminal sets form a genuine inverse subsystem of the
frontier graphs.  The checker confirms (2) through horizon 12, but the proof
does not depend on that bound.

For a fully actual-right infinite endpoint, the same compactness argument as
in the hard-core frontier theorem gives the exact orbit-separation target

```text
O_c intersect I(R_infinity)=empty,  c in {2,3}.       (3)
```

Here `O_c={T_u(c^omega):u finite}` and `R_infinity` denotes complete infinite
right traces under the alternating center boundary.  Distance to
`A_h^right` diverges exactly when (3) holds.

## 3. Critical scope correction

Equation (3) is a valid theorem about fully actual-right endpoints, but it is
not yet the endpoint delivered by rank descent.  Starting with the genuine
endpoint `e`, lowering finite Peel rank `m` replaces it by `2^m e`.  At the
first infinite shifted cut, the remaining endpoint is either a shift of `e`
or has a finite artificial prefix of state `2`s before a tail of `e`.

Consequently the period-two application supplies an **eventually**
actual-right endpoint, not necessarily an element of `R_infinity` from
coordinate zero.  Since an arbitrary finite hard-core prefix can precede an
actual-right tail, filtering finite terminal prefixes without retaining the
prefix length loses this distinction.  Whole-prefix conditioning is
therefore too strong to close the rank-zero separator.

The already-recorded scale statement avoids this mistake: choose the scale
beyond the artificial prefix, so `W R_c(W)` is an actual-right factor.  A
future frontier product must similarly couple the permitted prefix length to
the finite source/Peel ancestry; it cannot simply replace `A_h` by
`A_h^right`.

This correction is the most important conclusion of the experiment.

## 4. Exact finite language and distance audit

The actual endpoint counts are:

```text
h:                 1   2   3   4   5   6   7   8   9  10  11  12
hard |A_h|:         3   5   8  13  21  34  55  89 144 233 377 610
actual |A_h^right|: 3   5   8  12  17  25  36  50  68  91 119 156
```

The first three columns coincide; the first deleted endpoint is the
length-five forbidden trace `00000`.  The complete actual language through
endpoint length 13 has counts

```text
2,3,5,8,12,17,25,36,50,68,91,119,156.
```

This is a finite sequence, not a recurrence claim.

Let `m_h^any` be the arbitrary-queue minimum and `m_h^SFT` the minimum after
also imposing the invariant queue factors `20,22,011`.  Conditioning the
terminal set gives:

```text
h:                    1  2  3  4  5  6  7  8  9 10 11 12

hard any, tail 2:     1  3  5  5  5 10 10 10 10 16 16 18
actual any, tail 2:   1  3  5  5  5 10 10 10 10 16 18 23
actual SFT, tail 2:   1  3  5  5  5 10 10 10 10 17 19 23

hard any, tail 3:     2  3  5  5  5 10 10 10 12 12 15 16
actual any, tail 3:   2  3  5  5  5 10 10 10 12 15 17 17
actual SFT, tail 3:   2  3  5  5  5 10 10 10 14 15 17 17
```

The largest displayed arbitrary-queue gap is at horizon 12, tail 2:

```text
hard minimum   = 18,
actual minimum = 23.
```

Every displayed actual endpoint has a SAT-extracted finite right initial row
that is replayed independently by the bit-parallel Rule 30 kernel.  Every
queue is replayed by the literal growing queue cocycle.

## 5. D8 phase costs

Augment a frontier path by the exact affine `D8` product on its newest fiber.
If the projected successor frontier ends in state `t`, the new fiber action
is `K_t`; the checker asserts after every edge that the accumulated action
maps the source tail to the literal newest frontier coordinate.

All eight phase elements reach both terminal families by horizon seven, so
actual-right conditioning does **not** produce a persistent missing phase.
It does change phase-conditioned shortest lengths.  At horizon ten the
minima, ordered by affine coordinates `(alpha,beta,gamma)`, are:

```text
tail 2 phase:   000 001 010 011 100 101 110 111
hard:            17  17  17  18  18  17  16  19
actual:          23  19  17  18  18  24  16  19

tail 3 phase:   000 001 010 011 100 101 110 111
hard:            16  18  18  12  20  14  17  16
actual:          18  21  21  20  22  15  17  21
```

This is a real phase-dependent selection effect, not a uniform thinning of
the terminal set.  It is nevertheless finite evidence.  Because every phase
survives, the preregistered missing-phase route is killed; only a weighted or
ancestry-coupled monodromy argument remains possible.

## 6. New finite forbidden factors

As a secondary SAT audit, the complete right language has the following new
minimal forbidden words beyond the previously recorded length-11 list:

```text
length 12: 010010000101, 010100010001, 100100010000
length 13: 0001000010001, 1001000010001
```

These are exact finite-cone UNSAT results in this experiment, but no DRUP
artifacts were retained.  They should therefore remain SAT-audited factors,
not be promoted to a solver-independent theorem or used as a substitute for
the complete right-cone language.

## 7. Consequence and next target

The experiment establishes three things:

1. actual-right terminal frontiers form a uniform inverse subsystem;
2. genuine right realizability materially raises finite frontier and `D8`
   phase distances; and
3. applying that subsystem directly after rank descent is logically too
   strong because of the artificial finite endpoint prefix.

The proof-relevant synthesis is therefore:

> Retain the source word/Peel ancestry and condition only the endpoint block
> beyond its induced artificial-prefix bound, or work in the existing scale
> formulation where the block is chosen beyond both prefixes.

The repaired scale charges

```text
s_2(W) <= #2(W)+indicator(22 occurs in W),
s_3(W) <= #2(W)+3
```

remain the cleanest falsifiable all-length target.  The exact D8 phase should
be carried as boundary state in an ordered matching proof, not used as a
standalone phase exclusion.

## 8. Reproduction

From `13-rule30/`:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/constant_tail_actual_frontier.py \
  --max-horizon 12 --monodromy-horizon 0

PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/constant_tail_actual_frontier.py \
  --max-horizon 10 --monodromy-horizon 10
```

The first command performs the complete conditioned distance, invariant-SFT,
projection, SAT/direct-language, right-seed replay, and queue replay audit.
The second adds the augmented `D8` phase search through the preregistered
bound.

For a quick smoke test, reduce both horizons to `4` and add
`--direct-control-length 5`.

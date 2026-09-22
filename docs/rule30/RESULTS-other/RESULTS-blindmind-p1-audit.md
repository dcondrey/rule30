# BlindMind trial on the fixed-original P1 counting problem

**Status: no uniform counting theorem and no period-two exclusion obtained.**
BlindMind generated six proposals in two bounded rounds. None supplied a
valid construction or proof mechanism. One counting direction extracted
from its first proposal remains a precise, unproved hypothesis. An exact
counterexample refutes a natural one-step version of that direction.

This investigation concerns all legal finite **auxiliary** reconstruction
frontiers. None of the words below is asserted to occur at the singleton
Rule 30 seed's frontier. P2 and arbitrary periods are outside its scope.

## 1. What was actually run

The project at `/Volumes/A/blindmind` was used through its actual
`EvolutionEngine`: parent selection, crossover/mutation prompts, novelty
prefilter, structured critic, and SQLite lineage storage. The stock
`headless_evolve_rule30.py` was not run: its task includes P2/P3 and old
complexity/thermodynamic proposals, rather than this exact P1 question.
It also contains an incorrect Rule 90 formula. Its existing model outputs
were inspected as proposals, not imported as mathematical evidence.

The focused bridge is
[`run.py`](../../experiments/rule30/blindmind-p1/run.py), with
[`brief.md`](../../experiments/rule30/blindmind-p1/brief.md) and the
independent first-round audit in
[`feedback.md`](../../experiments/rule30/blindmind-p1/feedback.md).
The second round received that audit, including exact counterexamples.

The fixed limit was four initial proposals and two refinements, each with
a separate critique: twelve serialized model calls total. Calls used
BlindMind's existing `claude-haiku-4-5-20251001` Claude CLI provider through
the authenticated subscription, with no API-key provider or fallback,
model tools, automatic retries, GPU work, or seed regeneration. Per-call
and per-round wall limits were 240 and 1,200 seconds. The bridge omits the
stock repeated-batch retry loop. These limits were local execution choices,
not additional user approval requirements.

All prompts, schemas, structured results, raw responses, round records,
source hashes, and the private concept database are retained under
[`run01/`](../../experiments/rule30/blindmind-p1/run01/). The original
BlindMind source and shared database were not edited. Its source working
tree remained clean. The private database's `critic_retained` flag is a
model scoring decision; every recorded candidate has
`mathematically_validated=false`.

## 2. Independent verdicts on all six proposals

| Proposal | Decisive problem | Verdict |
|---|---|---|
| Repeat Feasibility Lattice Bound | Deterministic futures do not furnish independent choices of repeat positions. An upper bound on feasible pattern count cannot supply a lower bound of `2^D`. The overlap factor is undefined. | Proof rejected; a different lower-count hypothesis can be extracted. |
| Temporal-Spatial Forced-Bit Accumulation Debt | Recounts the same original bits at successive times. Conditional forcing cannot change when the complete original class is unchanged. Its new empirical verification claims were not supplied by the repository data. | Proposed information charge invalid. |
| Forward Multiplicity Budget | At a fixed successful state there is exactly one next scalar. Its denominator `log2(number of possible next scalars)` is zero. | Explicit undefined-budget witness below. |
| Cumulative Guard Irreversibility via Temporal Binding of Spatial Paths | Binding is not defined by a finite rule; an exponent is literally unfinished; no identity supplies its asserted linear charge. | No executable mathematical mechanism. |
| Episode-Guard Depth Partitioning | Reset ancestry is undefined, repeats are confused with phase switches, and a claimed first-image partition is false on the supplied example. The remaining weighted inequality assumes its needed cumulative charge. | Rejected after refinement. |
| Local injectivity demands at repeat junctions | Its junction set `F_i` equals `C_r(alpha)` by definition. The only explicit cardinality inequality is an identity, with no dependence on `D`. | Tautology; no repeat bound. |

These verdicts are independent of BlindMind's critic. Its critiques also
contain errors. In particular, a constant class over a **finite** plateau
does not refute a cumulative bound that allows earlier credit; a phase
switch never creates new original ancestors; and different tapes may have
different signatures even if their original classes are equal.

One practical failure of critic retention is especially clear: the
Forward Multiplicity Budget received score `3.5` and was retained. Its
structured `fatal_flaws` list is empty even though prose resembling a
flaw list appears inside its rationale. Its division by zero is an exact
mathematical defect. Model scoring and schema acceptance cannot replace
the checks below.

## 3. A different counting direction, explicitly unproved

Keep the original length `r` fixed. Let `C=C_r(alpha)` be the complete set
of original legal length-`r` words passing every chronological guard and
emitting `alpha`, and put `G=|C|` and `D=D(alpha)`.

The original target is the **upper** bound

```
G * 2^D <= 2^(2r-1).
```

The first BlindMind proposal suggested bounding repeats by the amount of
original multiplicity. After removing its invalid possible-futures
argument, a precise separate question is:

> **L, global lower multiplicity conjecture.** For every `r>=1` and every
> finite tape `alpha` with `C_r(alpha)` nonempty, does `G>=2^D` hold?

This is an analyst's repaired formulation, not a result proved or even
correctly formulated by BlindMind. It does not follow from the original
upper-bound conjecture. Nor is it a per-repeat growth statement:
`C_r(alpha s)` is always a subset of `C_r(alpha)`.

If L were proved, `2^D<=G<=2^(2r-1)` would give `D<=2r-1`, and the existing
repeat lower bound would give the same conditional mortality estimate

```
N <= 4^r (r+2) - r - 1.
```

More generally, a proved lower bound `G>=2^(epsilon D)/c` with universal
`epsilon,c>0` would give
`D<=(2r-1+log2(c))/epsilon`. This is only a conditional implication, not
an advance on the missing uniform theorem.

A distinct, more literal repair of the original proposal is:

> **S, synchronized continuation conjecture.** If `|alpha|=r` and
> `C_r(alpha gamma)` is nonempty, set
> `E=D(alpha gamma)-D(alpha)`. Does
> `2^E <= 2 |C_r(alpha)|` hold?

The already proved synchronization theorem makes
`C_r(alpha gamma)=C_r(alpha)` in this setting. S would imply
`E<=2r`, hence `D(alpha gamma)<=3r-1`, also sufficient for mortality.
L would imply S with constant one, but S does not assert the full global
lower bound. Neither is proved.

### Finite observations for the new questions

The test enumerated original lengths 1 through 7, retaining every guard
and stopping each trajectory at its first failure. This revisited small
originals to distinguish **new lower-bound hypotheses**, not to extend
the old upper-bound census. It checked 10,922 original words and 21,576
attempted updates with both the local scan and frozen `cert33.direct_step`.
There are only 74 nonempty `(r,alpha)` classes in this test; the longest
successful tape has ten symbols. All trajectories died before the fixed
128-step safety cap. No indefinite continuation is inferred.

| Original `r` | Maximum `2^D/G` over nonempty classes |
|---:|---:|
| 1 | 1 |
| 2 | 1/2 |
| 3 | 1 |
| 4 | 1/6 |
| 5 | 2/3 |
| 6 | 2/9 |
| 7 | 4/15 |

L and S both passed this finite test. L also passed arithmetic checks on
477 existing nonempty BDD records; no BDD computation was regenerated.
Their smallest `G/2^D` is `1229823/4096`, at `r=22` and tape
`00011111111111000`, with `G=4919292` and `D=14`. These records mostly
have tape length below original length, and provide little evidence about
the synchronized, unbounded-future regime.

## 4. Exact refutation of a first-image shortcut

For an original `w` producing a nonempty successful tape, let

```
F(Z(w)) = {v : v is legal of the ORIGINAL length r, Z(v)=Z(w)},
M(Z(w)) = |F(Z(w))|.
```

Then `F(Z(w))` is a valid subset of `C_r(alpha)`: the same first image
includes the same appended scalar, and all later updates coincide.
This statement uses original first-step predecessors and preserves all
guards. It makes no assertion about arbitrary later predecessors.

The existing exact inverse-fiber formula makes `M` easy to compute. For
an actual image `x` of length `R>=3`, preceding scalar `q`, and crossing
counts as defined in
[`RESULTS-repeat-budget-phase-reset.md`](RESULTS-repeat-budget-phase-reset.md),

```
M(x) = 2^(1+q+N_up) * 3^N_down.
```

**Counterexample.** The original word `2000001` emits the full successful
tape `0001101011`, whose four repeats give `2^D=16`. Its first image is
`21313103`. That image has exactly these six original predecessors:

```
2000001  2000020  2000021  2100001  2100020  2100021
```

Consequently `2^D<=2M(Z(w))` is false: `16>12`. This refutes even the
factor-two first-image shortcut for the particular original, not L.

The **complete** tape class has 60 original ancestors, partitioned by
first image as follows:

| First image | Number of original predecessors |
|---|---:|
| `21313103` | 6 |
| `21322103` | 18 |
| `21303103` | 36 |

Each entire listed fiber lies in the same chronological tape class. The
verifier retains all 60 words, the six-word fiber, and every state of the
displayed original's ten successful updates plus its final failed guard.
Enumeration and the inverse product formula agree on all three counts.

Thus a construction beginning with this original cannot obtain the
proposed repeat-indexed multiplicity from its own first-image fiber alone.
Moving to a different first-image fiber would require a separately proved
operation preserving the later history. The refined BlindMind response
did not supply that operation. Its concrete prediction of six fibers of
size at most ten is also false: there are three, of sizes 6, 18, and 36.

## 5. Exact controls for the remaining proposals

For the five established tapes
`101,1011,10111,101110,1011100`, the verifier independently reconstructs
the same complete class of 36 originals. Their repeat counts are
`0,1,2,2,3`. Under the fixed original-bit reading order

```
b_(r-1), a_(r-1), ..., b_1, a_1, b_0,
```

every original's entire conditional forced-position mask is identical
across all five classes. `Q=sum f=204` throughout. There are **zero** newly
forced positions at each extension. Thus no construction that charges new
forced original bits on these extensions can be justified by these
unchanged sets. This does not refute deferred credit or the open mean
forcing inequality.

For the Forward Multiplicity Budget, take original `3` and tape `1`.
The unique successful original has endpoint `32`, whose unique next
scalar is `0`. The proposed next-scalar set has cardinality one, so
`B=log2(1)=0`, while `Q=G=1`. Its ratio `Q/(G B)` is undefined. In fact
this defect holds at every successful fixed endpoint, because `Z` is
deterministic.

For the final proposal, its literal definition is

```
F_i = {w in C_r(alpha) : w successfully emits alpha_i at junction i}.
```

Every member of `C_r(alpha)` already meets that condition. Hence
`F_i=C_r(alpha)` for every junction, and its displayed maximum of
`log2(|F_i|)` is identically `log2(G)`, regardless of the number of repeats.
For the 60-word example the four repeat-junction sizes are exactly
`60,60,60,60`. Reinterpreting `F_i` as all ancestors of a shorter prefix
would change the definition and still supply no proven cumulative bound.

## 6. Reproduction and limits

Run the maintained solver-free verifier from the Rule 30 repository root:

```
uv run --no-project python experiments/rule30/blindmind_p1_audit.py
```

It writes
[`exact-audit.json`](../../experiments/rule30/blindmind-p1/exact-audit.json),
including full witnesses, finite-test limits, source hashes, and explicit
false status flags for uniform proof and period-two exclusion. The final
run completed in under one second. It calls neither BlindMind nor any
network service. Rerunning the model rounds is unnecessary; their original
inputs and outputs are retained, and the runner refuses duplicate rounds.

The useful outcome of this trial is a precisely separated lower-count
question and a refuted shortcut, with exact witnesses. It produced no
history-preserving transformation, no uniform bound on cumulative repeats,
and no new period exclusion. The main P1 obstruction remains open.

Follow-up: the [direct proof attempt](RESULTS-lower-multiplicity-proof-attempt.md)
proves an explicit two-update rewrite between original first-image fibers.
It also gives a complete 162-member class with seven repeats but maximum
coordinate-cube dimension five, refuting an independent-bit construction
of the lower bound. The unrestricted lower bound remains open.

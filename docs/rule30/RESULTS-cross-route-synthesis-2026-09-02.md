# Cross-route synthesis after the ancestry counterexamples

Date: 2026-09-02

Status: **NO PRIZE PROBLEM IS SOLVED.  THE PERIOD-TWO REDUCTION IS EXACT, BUT
ITS FINAL UNBOUNDED SEPARATION LEMMA REMAINS OPEN.**

## 1. Scope and accounting

This review covers the ranked routes in `PATH.md`, frontier rows 73--90, the
later route rows, and all 58 result reports in the period-two directory.  The
archive also contains 51 preregistration reports.  These numbers must
not be added and called a number of independent approaches: many entries are
controls, equivalent formulations, refinements, or falsifications of one
proof family.

The honest problem status is:

| Target | Exact progress | Missing theorem |
|---|---|---|
| P1 | Eventually-zero and eventually-one center tails are excluded.  A nonconstant period-two trace is reduced to an exact finite-word/orbit separation. | Prove that every relevant finite queue is mortal, equivalently that the frontier/source and hard-core terminal inverse limits are disjoint.  Other nonconstant periods remain after that. |
| P2 | Bernoulli facts, right-edge periodicity, patch censuses, and weak counting bounds are rigorous. | A seed-specific orbit-closure/genericity or discrepancy theorem. |
| P3 | Exact ANF degree, bounded circuits, proof-system ceilings, and a deterministic work instrument are rigorous. | A lower bound for the fixed lone-seed bit sequence in a precisely stated computation model. |

Finite searches remain falsifiers and structural probes.  No horizon reported
in this archive proves an asymptotic prize claim.

## 2. Corrected period-two state

The exact reduction chain still stands:

```text
eventual period two
  -> same-orbit comparison
  -> alternating phase
  -> Gray/OR hard-core endpoint
  -> inverse-terminal cut of finite Peel rank
  -> rank zero with eventual tail 2 or 3
  -> reversed dependency queue/frontier orbit separation.
```

The queue transition, the rotated Peel identity, the `D8` affine action, the
13-element Peel-lift monoid, the frontier graph, and the hard-core terminal
language are exact.  The following stronger-looking claims are now known to
be false for unrestricted normalized queues:

- a fixed feature/raw-reserve budget for pull ancestry;
- the coordinate-depth estimate `r >= 2h-1` for arbitrary queues;
- a generic odd-period-versus-dyadic-period mismatch;
- scalar or bounded-window contraction of the queue/frontier state.

The counterfamily

```text
R_m = 3001 0^m 2
```

stores pull depth in dyadic congruence classes.  In the tested range, depth
two occurs at `m = 6 (mod 8)`, depth three at `m = 382 or 390 (mod 512)`, and
depth four at `m = 390 (mod 2048)`.  This is finite evidence, not a closed
formula, but it decisively identifies the missing state variable: scale and
binary phase, not local symbol count.

The same counterfamily does **not** arise directly from a hard-core endpoint.
An abstract witness begins its reversed diagonal with `200`; the exact
endpoint construction forces `203`.  More generally, the following all-length
theorem survives:

> For an endpoint-derived initial queue of length `N`, every appended node,
> and hence every pull root, descends from one of the last three initial
> coordinates `{N-3,N-2,N-1}`.

The restricted estimate `r >= 2h-1` has no finite counterexample in the
recorded exhaustive and random corpora, but it is not proved.  Root
localization alone does not imply it.

### 2.1 Endpoint events and the needed strength of a depth bound

For every nonsingleton endpoint-derived queue, the event letters are exactly
the three hard-core endpoint transitions

```text
A <=> 2 -> 1,    B <=> 2 -> 2,    C <=> 1 -> 2.
```

The singleton `(2,)` is the isolated boundary-credit exception.  In
particular, a pull `C` creates a *future* `12`; it need not consume one in the
initial endpoint.  The exact endpoint `22222222` has no `12`, yet its queue
has event word `AC` and therefore a pull.  Literal initial-endpoint pair
charging is false.

More importantly, `(HCD)` is unnecessarily sharp.  For a fixed initial
length `N`, any proved finite bound `h<=f(N)` on one pull ancestry chain is
enough: the parent-forest theorem turns infinitely many pulls into unbounded
depth.  This opens a weaker cross-route target—inject chain pulls into the
`N` ordered zero-prefix tokens, possibly decorated by one of the eight `D8`
phases.  Either `h<=N` or `h<=8N` suffices.  The injection is not proved.
The later pull-row alpha reduction below is weaker still and supersedes this
injection as the first proof target.

There is also an exact dichotomy behind this weakening.  If an immortal
relevant queue has only finitely many `C` events, it eventually has no `A`
events (every surviving `A` is immediately followed by `C`) and therefore
has event tail `B^omega`; its endpoint is eventually `2^omega`, already
excluded by the reachable dyadic exceptional-family theorem.  Otherwise it
has infinitely many pulls, and the parent forest forces unbounded depth on
one chain.  Thus a finite chain bound closes the entire remaining branch.

### 2.2 Pull-row alpha support

Combining the endpoint/event dictionary with the projected zero-prefix
scenarios removes most of the remaining certificate.  It is enough to prove:

> At every nonfinal pull row `j`, some zero-prefix token `k` with `j<=k<n`
> changes the single affine coordinate `alpha`.

If a relevant endpoint is not eventually `2`, it has infinitely many pull
rows.  For an absolute pull `m=3n+r`, where `n=floor(m/3)`, the scale block
`e[n:2n]` sees it at row `j=n+r>=n`; the displayed token interval is empty.
No matching, pull-depth bound, or second affine coordinate is required.

This coordinate has an exact interpretation.  For raw reversed dependency
queue `R` and previous endpoint `p`,

```text
alpha = 1 XOR [p != 0] XOR parity{i>=1:R_i != 0}.
```

On a hard-core row this is just the activity parity of `R[1:]`, and the
forced endpoint high bit is `1 XOR alpha`.  Hence a pull is a temporal
`alpha:1 -> 0` transition.  The remaining theorem is a discrete parity-flux
statement across the ordered scenario strip.

PAS has zero failures on 392,830 word/tail cases through length 23, including
31,595 nonfinal pull rows.  The frozen held-out lengths 19--23 contribute
357,414 cases and 28,954 pull rows.  These counts are finite evidence only.
The diagonal token `k=j` already fails at length six.  Alpha first-witness
displacement reaches at least twelve: `W=12122212212122222`, tail `2`, row
`1` has alpha support `{13,16}`.  The earlier value nine measured the
two-coordinate projected witness, not alpha, so a bounded-radius proof is
not supported.

### 2.3 Three-row late-pull diagonal

The scale arithmetic weakens PAS once more.  It is sufficient to prove that
a length-`n` scale block has no nonfinal pull at rows `n,n+1,n+2`.  Every
sufficiently late absolute pull is `m=3n+r` and lands in exactly this window.
This removes all alpha variables and all early-row support obligations.

No late pull occurs in the complete hard-core corpus through length 23,
eight aligned GA adversaries, 240,000 long random word/tail cases, or all
binary source words through length 20.  The six exact tail/residue CNF
families are UNSAT through `n=20`, but generic conflicts and proof width grow
and reveal no induction.  Moreover, a hard-core length-12 certificate
supports the target pull while its final six cut symbols are already
constant; the full earlier cut history is load-bearing.  The three rows are
candidate event positions, not a literal `3 x 3` patch theorem.  This is now
the smallest sufficient conjecture, not a period-two proof.  See
`RESULTS-LATE-PULL-DIAGONAL.md`.

## 3. Correlations that recur across nominally different routes

### 3.1 Scale is the missing coordinate

The zero-run fan-out, the dyadic pull resonances, Peel doubling, half-word
recurrences, and the `O(log t)` penetration of the regular boundary are
different faces of one phenomenon: information is retained in a hierarchy of
binary spatial scales.  Local counts erase exactly the phase that decides a
later exceptional event.

This suggests a state containing:

```text
(ordered gap vector, binary-scale filtration, absolute D8 phase).
```

The useful theorem would not say this state shrinks every row.  It would say
that every additional pull depth forces a strict refinement of a nested
dyadic cylinder associated with an ordinary finite gap.  Infinite pull depth
would then require infinitely many compatible binary digits inside a finite
source word.  The necessary open step is proving that refinements are nested;
the observed residue classes alone do not prove it.

### 3.2 Source restrictions repeatedly rescue false generic statements

Three independent episodes have the same shape:

| False broad claim | Exact source condition | Surviving result |
|---|---|---|
| All accepted cuts have an odd period factor | Reachability from the zero ray | The eventually alternating exception is unreachable. |
| Pull depth is bounded by an abstract coordinate budget | Hard-core endpoint forces diagonal prefix `203` | Every pull root is localized to the final three source coordinates. |
| A finite list of right factors describes the terminal cone | Full actual-right inverse subsystem | Frontier distance increases, with exact inverse compatibility. |

Therefore future conjectures should construct states from the genuine
endpoint/source map at the outset.  Filtering arbitrary words afterward is
too weak and repeatedly produces false theorems.

### 3.3 All viable period-two targets are the same separation

The following are equivalent faces of the remaining constant-tail problem:

- mortality of every endpoint-derived tail-2/tail-3 queue;
- divergence of the shortest accepted word in the language cocycle;
- divergence of source-to-terminal distance in the frontier graph;
- emptiness of the finite-generator orbit intersection with the infinite
  hard-core terminal set;
- absence of finite-Peel-rank inverse cuts for aperiodic hard-core endpoints.

Changing among these coordinates is useful only when it exposes a new
monotone object.  It is not five independent routes.

### 3.4 Expansion of formulas is compatible with contraction of witnesses

The DFA for height `h` has size `4^(h+1)+1`, Boolean ideals absorb new pin
constraints, and frontier dimension increases with height.  Thus the dynamic
cocycle intuition is correct but its proposed rank contraction is not:
formula complexity expands.  The viable contraction target is instead a
minimum witness quantity, such as source length, frontier distance, or the
number of unresolved scale cylinders.

Craig separators should therefore be pulled through the exact Peel identity
with an explicit restart/boundary state.  Searching again for a fixed clause,
fixed energy, or fixed automaton rank repeats a recorded failure.

### 3.5 P1 and P2 share a lone-source problem

In P1, generic period-spectrum assertions became useful only after zero-ray
reachability was imposed.  P2 has the analogous gap: invariant-measure and
almost-everywhere theorems do not locate the lone seed in the relevant basin.
The next P2 theorem should classify the lone-seed orbit closure or establish a
seed-specific discrepancy recurrence.  More ensemble statistics cannot bridge
that logical gap.

The observed growth of checkerboard patches also warns that unique ergodicity
may be the wrong target.  The prior question is whether arbitrarily large
checkerboard patches occur; finite occurrence rates do not settle it.

### 3.6 P1 structure does not automatically imply P3 hardness

An infinite Cartier kernel, a growing frontier, high arbitrary-input ANF
degree, or nonperiodicity could exclude particular finite-state evaluator
classes.  None gives a lower bound for computing the fixed sequence in the
general model required by P3.  Conversely, the exact queue/Peel machinery may
discover an evaluation shortcut and is valuable as a P3 falsifier.  Claims of
pseudorandomness, circuit hardness, or proof hardness require a separate
bridge.

## 4. Ranked mashups

### A. Pull-row alpha parity flux

This is now the smallest sufficient target.  Assume the ordered alpha
finite-difference row vanishes for every token `k>=j`.  Using the complete
scenario queues and the activity-parity formula, prove that the original
endpoint cannot make a nonfinal `1 -> 2` transition.  Equivalently, derive a
discrete triangular Stokes/noncrossing law transporting the temporal alpha
loss to spatial alpha support.

The active source alphabet `{1,2}` is essential: arbitrary four-state source
word `01`, tail `2`, is already a counterexample.  Endpoint telescoping and a
fixed diagonal radius are also false.  A valid proof must keep ordered
interior ancestry until the final parity projection.

### B. Ordered scale tokens + endpoint pull ancestry

This is the strongest new ancestry route.  The previous proposal asked for a
fresh hard-core `12` pair and thereby aimed at `2h<=r+1`.  That quantitative
target is stronger than mortality needs, and literal endpoint pairs are
already false witnesses.  Instead, attach each pull on one ancestry chain to
an ordered zero-prefix token in the initial inverse-cone strip.  Prove either:

1. tokens are never reused, giving `h<=N`;
2. a token can be reused only at a new absolute `D8` phase, giving `h<=8N`;
   or
3. successive uses impose properly nested dyadic residue cylinders whose
   modulus strictly increases but whose support remains in the finite source
   strip.

The missing step is the common coordinate map from a `C` edge on the
ballistic pull ray to an adjacent projected zero-prefix change.  The complete
dependency diagonal must remain available when defining the map; bounded
defect states are already killed.  A repeated token/phase pair or a
nonnested exact endpoint-derived residue is a kill certificate.

### C. Projected diagonal support + the same scale filtration

The projected diagonal-support lemma has broader finite coverage and gives
the desired tail bounds directly.  Its adjacent affine differences must be
tracked with an absolute `D8` anchor; bare defect words are not closed.  A
binary gap filtration may supply the well-founded order that scalar support
counts lacked.  This is the primary proof route; ancestry depth is an
independent sufficient route and a source of counterexamples.

### D. Peel-recursive separators + moving restart state

Pull the small exact Craig interpolants back through

```text
P(I(sigma e)) = sigma^2 I(e)
```

while carrying the restart phase explicitly.  Seek a recurrence for minimum
source length rather than bounded formula size.  This combines exact algebra
with the dynamic-cocycle idea without assuming a static local invariant.

### E. Artificial-prefix bound + actual-right frontier distance

The actual-right terminal subsystem raises finite distances, but rank descent
may prepend an artificial block of `2`s.  Prove that a generator word of
length `d` can contaminate only the first `f(d)` terminal coordinates; beyond
that point the terminal must be actual-right.  Endpoint root localization is
the plausible boundary alignment.  A distance lower bound exceeding `d`
would then close the orbit intersection.

## 5. Work order and kill discipline

1. Prove or falsify pull-row alpha support from the exact activity-parity
   formula and complete ordered scenario queues; do not extend the finite
   horizon.
2. If PAS fails, return to the endpoint-derived token/phase or
   noncrossing/residue-nesting lemma; do not test arbitrary normalized queues.
3. In parallel at the level of mathematics, strengthen projected diagonal
   support using a gap/scale filtration with the absolute `D8` phase.
4. If both fail, synthesize Peel-recursive separators whose objective is
   minimum source length.
5. Apply actual-right constraints only after bounding the artificial prefix.

The period-two proof is complete only when one of these yields an all-length
theorem and an independently checkable derivation.  A larger census, another
plateau, or absence of a genetic counterexample does not change that status.

## 6. Progress calibration

The ancestry counterexamples lower the period-two estimate because they
invalidate a proposed quantitative bridge, even though the exact reduction
and endpoint localization remain.  The following percentages measure
research-program completion, not the probability that a conjecture is true:

```text
P1 overall                 [###-----------------------] 12%
P1 period-two foundations [#########################-] 96%
P1 period-two exclusion   [###################-------] 72%
P1 arbitrary periods      [##------------------------]  8%
P2                         [##------------------------]  8%
P3                         [##------------------------]  6%
```

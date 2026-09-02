# Rule 30: compact research index

Updated: 2026-09-01

Purpose: resume this project with the fewest tokens consistent with not
repeating work.  This file routes to authoritative sources; it is not itself a
source for publication claims.

## Current status

| Problem | Status | Best live edge |
|---|---|---|
| P1: center-column nonperiodicity | **OPEN** | R1's OR-specific zero-set obligation; within it, the period-two same-orbit rung |
| P2: limiting density `1/2` | **OPEN** | R8/orbit-closure route remains conditional; ensemble ergodicity does not reach the lone seed |
| P3: computational effort | **OPEN** | A genuine fixed-sequence work lower bound remains unproved; proof-complexity and finite circuit probes are bounded only |

Proved prize-adjacent results exclude eventually constant centers only:

- zero center tail: `RESULTS-zero-tail.md`;
- one center tail: `RESULTS-eventual-period.md` and
  `RESULTS-inverse-trace.md`.

No document proves a nonconstant-period exclusion, density convergence for the
lone seed, or a computational lower bound.

## Where every attempt is indexed

For cross-examination by proof obligation, state representation, information
retained, evidence level, and failure mechanism, start with
`EXPERIMENT-ATLAS.md`.  It overlays the historical registers without moving
or renumbering their sources.

The register is split for historical reasons:

| Coverage | Canonical source |
|---|---|
| Ranked routes R1–R9 and internal rows 1–72 | `PATH.md` sections 4 and 7 |
| Frontier attack rows 73–90 | `experiments/overnight-arms/frontier_attack/FINDINGS.md` sections 1–7 |
| Later rows 91–93 | `PATH.md` section 7.1 |
| Period-two same-orbit continuation after row 90 | `experiments/rule30/p1-period2-invariant/README.md` |
| Cross-technique synthesis and new dyadic separator | `RESULTS-hybrid-review-2026-09-01.md` |
| External literature/claim audit | `PATH.md` section 8 and the two `REFUTATION-*` files |

There is a historical row-number collision: `PATH.md` row 76 is the S-adic /
Morse–Hedlund subword attempt, while `FINDINGS.md` row 76 is the alternating
survivor-invariant attempt.  Always cite the file plus row number.

`overnight/CONTEXT-DIGEST.md` is a useful 2026-08-30 snapshot but predates rows
73–93 and the period-two continuation.  Do not use it as the current index.

## Minimal routing by problem

### P1

Read:

1. `RESULTS-eventual-period.md` for the same-orbit reduction and constant cases.
2. `PATH.md` R1 plus sections 9.3–9.5 for the zero-set obligation.
3. `RESULTS-alt-trace-fiber.md` for the alternating-fiber normal form.
4. `experiments/rule30/p1-period2-invariant/README.md` for the current exact
   period-two map, certificates, and next theorem.

Do not rerun: larger finite-period SAT grids, fixed-depth ladders, generic
left-permutive arguments, bounded adjacent-column prediction, support-width
descent, periodic-mask contraction, or local additive rankings.

### P2

Read `PATH.md` R8 and section 9.3, then
`RESULTS-orbit-closure-diagnostic.md` and
`RESULTS-checkerboard-growth-extended.md`.  Uniform Bernoulli invariance and
almost-everywhere density `1/2` are known but miss the lone seed by obstruction
E.  Checkerboard-patch growth is quantitative finite evidence, not a proof of
orbit-closure membership.

### P3

Read `PATH.md` R9, obstructions D/G/I, and rows 91–93.  The deterministic fuel
instrument is validated but no evolutionary search ran.  Exact succinct-index
circuit synthesis gives bounded results only.  Do not infer a work lower bound
from arbitrary-input ANF degree, one derivation system, proof size, or a fitted
runtime exponent at small `n`.

## Current P1 period-two frontier

Target for every nonzero finite configuration `y`:

```text
Tr_0(y) != Tr_0(F^2(y)).
```

Constant traces are already excluded.  The remaining phase is `0101...`
(the opposite phase maps to it after one Rule 30 step).

The strongest exact coordinates now are

```text
C = I(A OR (1 OR (B << 1))),
D = I(C OR (A << 1)),
pin = D & 1,
(A,B) -> (D,C),
```

where `I` is inverse Gray code.  For a genuinely realizable right half,
`rho_k=s(2k,1)` has no adjacent ones.  Neither fact has yet yielded mortality.

Best next theorem:

> **Projected diagonal-support lemma.**  For
> `W^(k)=0^k W[k:]`, let `A_(j,k)` be the exact newest affine boundary map at
> forced scale step `j`.  Every tail-2 survival row has some `k>=j` where the
> adjacent `(alpha,beta)` projections differ.  Every nonfinal tail-3 survival
> row has some `k>=j` where the adjacent `(alpha,gamma)` projections differ.

At the last required row, `j<=k<=|W|-1`, so the lemma gives
`s_2(W)<=|W|` and `s_3(W)<=|W|+1`, proving both constant-tail separators and
closing the nonconstant period-two rung.  It has zero failures on the full
hard-core corpus through `|W|=23` but is unproved.  An independent sufficient
target is the one-credit half-word recurrence in
`RESULTS-PROJECTED-DIAGONAL-HALVING.md`.  Pointwise derivatives, fixed-radius
edge rules, endpoint-only telescopes, and literal half-block embeddings are
already falsified.

The adjacent affine differences can be written as ordered `D8` holonomy
defects, but this does not make them a closed state.  Defects plus an
absolute anchor reconstruct every current affine phase and still have
different next-row defect words; previous endpoints also fail, and a
preregistered annotation retaining both queue ends fails at length 13.
Only the complete reversed dependency queues currently close.  Any ordinal
version of diagonal support must therefore rank interior queue ancestry, not
the bare defect word.  See `RESULTS-HOLONOMY-DEFECT-CLOSURE.md`.

An alternate exact bridge now removes the sole known overlap in the dyadic
period-spectrum route.  Every reachable zero-ray cut is ultimately
dyadic-periodic, but a uniform width descent proves that none is eventually
`1212...`; therefore no hard-core endpoint eventually equal to `222...` can
be an immortal finite-core endpoint.  The remaining generic statement is:
every non-eventually-`2` hard-core endpoint has an inverse-terminal cut that is
not ultimately dyadic-periodic.  See the period-two
`RESULTS-DYADIC-EXCEPTION-SEPARATOR.md`.

The two `phi` triangles now have an exact commuting law,
`P(I(sigma e))=sigma^2 I(e)`.  Together with preservation of the last
nonzero cell under `P`, it proves that every finite-rank collision must have
an aperiodic hard-core endpoint; in the positive-rank branch the successive
tail ranks are exactly `m,m+1,...`.  See
`RESULTS-ROTATED-PEEL-IDENTITY.md` in the period-two directory.

The inverse Peel lifts also form an exact 13-element transformation monoid.
All cycles have length one or two, and a block can cause the doubling only
when it uses `{0,1}` with odd `1` parity or `{0,3}` with odd `3` parity.
The doubled child necessarily contains state `2`, so strict doublings cannot
occur in consecutive endpoint shifts.  Currying the other input of the same
table recovers the queue/affine `D8` action.  These all-word theorems sharply
identify the exceptional events and the noncancelling phase data, but do not
by themselves exclude aperiodic hard-core endpoints.  See
`RESULTS-PEEL-LIFT-MONOID.md`.

The finite-rank branch is now reduced further.  Prepending endpoint state `2`
descends every positive rank to rank zero, and the first infinite shifted cut
then has constant tail `2` or `3`.  Reversing its complete newest dependency
diagonal gives the exact growing queue

```text
S_0=c,  S_i=g_(S_(i-1))(R_i),
R'=S . B(next endpoint).
```

The final scan state exactly decides the next hard-core endpoint.  Proving
mortality for every finite queue beginning in `c` and ending in `{1,2}` would
therefore prove the period-two rung.  Nonleading input symbols have the exact
quotient `3 -> 1`; every normalized successor then avoids `20`, `22`, and
`011`.  The resulting invariant ternary queue is exhaustively mortal through
length 15, but the all-length induction remains open.  See the period-two
`RESULTS-CONSTANT-TAIL-QUEUE.md`.

The associated survival formulas obey the exact regular-language cocycle
`L_(h+1)=L_0 intersect Q_c^(-1)(L_h)`.  Their minimized DFA size expands as
`4^(h+1)+1` through horizon seven, so strict formula-rank contraction is
false in this representation.  The live target is to prove that the shortest
word in `L_h` tends to infinity; its checked values jump through lengths
`1/2,3,5,10` with plateaus.  See
`RESULTS-CONSTANT-TAIL-LANGUAGE-COCYCLE.md`.

There is now a uniform graph realization of that shortest-word metric.  A
height-`h+1` vertical frontier updates under input `a` by
`w_0=a, w_j=g_(v_j)(w_(j-1))`.  The source is `(c,...,c)` and the terminal set
is exactly the `F_(h+3)` inverse-cone diagonals of hard-core endpoint words of
length `h+1`.  Bare distance measures arbitrary normalized queues; product
with the three-factor suffix DFA measures the invariant language.  Their
divergence is equivalent and is the remaining constant-tail queue-mortality
theorem.  Both distances are exact through horizon 12.  See
`RESULTS-CONSTANT-TAIL-FRONTIER-GRAPH.md`.
Deleting the last frontier coordinate commutes with all graph edges and
terminal sets.  The inverse-limit form is the exact orbit separation
`{T_u(c^omega):u finite} intersect I(HC_omega)=empty` for `c=2,3`; this
disjointness, not further horizon enumeration, is the live proof obligation.
Height extension is a four-sheeted permutation cover whose fiber actions
generate `D8`; a proof must control accumulated monodromy rather than expect
the new coordinate to contract.

Fully actual-right terminal frontiers form a proved inverse subsystem of this
graph and materially increase finite distances: at horizon 12, the tail-2
minimum rises from `18` to `23`.  All eight `D8` phases still occur, although
their costs separate.  This does not directly strengthen the rank-zero
theorem because rank descent can prepend a finite artificial block of state
`2`; its endpoint is only eventually actual-right.  Actual-right information
must therefore be applied beyond that prefix, as in the scale block above, or
coupled to a proved source-ancestry prefix bound.  See the period-two
`RESULTS-ACTUAL-RIGHT-FRONTIER.md`.

## Do-not-repeat obstruction screen

Reject a proposal immediately unless it explains why these do not apply:

| ID | Obstruction |
|---|---|
| A | Trace/boundary propagation reaches `O(log t)` depth while the target is `Theta(t)` away |
| B | The argument also excludes Rule 90's known periodic center |
| C | A 2D/density statistic changes only `O(1/W)` when column zero is overwritten |
| D | The proposed shortcut names but does not derive its exact composition/seam law |
| E | An ensemble or almost-everywhere theorem does not cover the lone-seed orbit |
| F | A fixed-depth strip leaves a new free outer boundary |
| G | Arbitrary-input complexity says nothing about evaluating one fixed input |
| H | Finite data cannot prove an infinite statement |
| I | Satisfiable fixed-input proof systems hit a small `Theta(n^2)` derivation ceiling rather than a lower bound |

Full hypotheses and affected rows are in `PATH.md` section 7.3 and
`FINDINGS.md` section 5b.

## Publication routing

- The zero-tail theorem has manuscript, Lean/SMT artifacts, figures, and a
  hostile audit under `docs/rule30/paper/`.  Its novelty still depends on
  checking the original Jen premise noted in `paper/PUBLICATION-NOTES.md`.
- Period-two work currently supports a methods/negative-results appendix, not
  a P1 claim.  Cite its raw `RESULTS-*` files and solver-free verifiers.
- P2/P3 reports are bounded or conditional and must retain those qualifiers.
- External prize-resolution claims by Fradkin and Topal are refuted in the
  corresponding `REFUTATION-*` files; cite the full audits, not this summary.

## Resumption discipline

1. Inspect process and Git state.
2. Choose one live theorem, not a topic survey.
3. Cross-examine the proposal in `EXPERIMENT-ATLAS.md` before treating it as
   new; identify its complete state, seam law, discarded information, and
   exact prior obstruction escaped.
4. Read only the sources routed above plus the exact predecessor result.
5. State how the proposal uses Rule 30's OR, the single orbit, and finite
   support.
6. Preregister the certificate class, controls, bounds, and kill conditions.
7. Prefer a finite human-checkable certificate; treat enumerations only as
   falsifiers.
8. Update this index only after exact controls and an independent verifier pass.

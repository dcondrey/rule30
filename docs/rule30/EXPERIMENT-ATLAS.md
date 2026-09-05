# Rule 30 experiment atlas and cross-examination ledger

Updated: 2026-09-03

Status: **ORGANIZATIONAL SYNTHESIS; NO PRIZE PROBLEM SOLVED.**

This is the single entry point for comparing experiments.  It does not
replace their result reports and must not be cited as proof.  Its purpose is
to make it difficult to confuse a finite observation with a uniform theorem,
to recognize when two techniques are the same state transition in different
coordinates, and to expose combinations whose hypotheses really fit.

## 1. Coverage and sources of truth

The archive has two historical registers and one active continuation:

| Coverage | Authoritative register |
|---|---|
| Ranked routes and attempt rows 1--72, 76, and 91--93 | [`PATH.md`](PATH.md), section 7 |
| Frontier rows 73--90 | [`FINDINGS.md`](../../experiments/overnight-arms/frontier_attack/FINDINGS.md), sections 1--7 |
| Active period-two continuation | [`p1-period2-invariant/README.md`](../../experiments/rule30/p1-period2-invariant/README.md) and the result matrix below |
| Exact reusable facts and obstructions | [`FACT-INDEX.md`](FACT-INDEX.md) |
| Current compact status | [`START-HERE.md`](START-HERE.md) |

There is a historical row-number collision at row 76.  Always identify a row
as `PATH:76` or `FINDINGS:76`.

The registers include proposals that were not run, killed mechanisms,
limitation theorems, infrastructure, and bounded measurements.  Those are not
missing experiments: their negative status is part of the record.

## 2. Evidence levels

Use these levels when comparing results:

| Level | Meaning | Can close an infinite prize statement? |
|---|---|---|
| `U` | Uniform proof or exact identity with all quantifiers discharged | Yes, if its conclusion is the required statement |
| `R` | Uniform equivalence or reduction to a named remaining lemma | Only after that lemma is proved |
| `C` | Independently checked finite certificate, UNSAT proof, or exhaustive bounded census | No, unless a separate uniform reduction makes the bound complete |
| `M` | Measurement, fitted law, heuristic search, or adversarial witness | No |
| `K` | Exact counterexample or structural obstruction killing the stated mechanism | It closes only that mechanism class |
| `I` | Infrastructure or a validated evaluator | No |

A single experiment can have two levels: for example, the frontier graph is a
uniform reduction (`R`) and its distances through horizon 12 are finite
certificates (`C`).

## 3. Cross-examination fields

Every experiment should be read through the following fields.  If a field is
absent from a report, treat it as an unresolved audit question.

| Field | Question |
|---|---|
| Target | Which exact quantified statement would the experiment advance? |
| Domain | Lone seed, every finite row, arbitrary hard-core word, actual Rule 30 right cone, or an ensemble? |
| State | What complete object is advanced: spacetime cone, frontier, cut, queue, formula, automaton, or scalar statistic? |
| Seam law | What exact rule composes two pieces or advances one scale? |
| Finite-support use | Where is eventual zero, a support edge, or source reachability imposed? |
| Actual-right use | Is the right half genuinely Rule 30-realizable or only filtered by finitely many forbidden words? |
| Information retained | Does the state retain symbol order, boundary phase, source ancestry, and the growing dependency diagonal? |
| Uniformity | Which part is proved for all widths/horizons, and which part is merely enumerated? |
| Controls | Does it survive Rule 30 truth-table checks and fail on the Rule 90 periodic-center control where appropriate? |
| Result | Proved fact, reduction, finite evidence, or exact failure? |
| Reusable output | What lemma, verifier, witness corpus, or obstruction can another technique consume? |

This schema is the practical meaning of “cross-examine.”  Two experiments can
be blended only when the output domain of one satisfies the input hypotheses
of the other.

## 4. Archive-wide mechanism map

This table groups the complete registers by mechanism.  The row registers
remain the exhaustive item-by-item list.

| Mechanism family | Representative rows/reports | Strongest result | Reusable content | Governing obstruction |
|---|---|---|---|---|
| OR-latch and constant trace fibers | `PATH:1--5,25--27` | Zero and one center tails excluded (`U`) | Rule-30-specific pin; prefix-OR classification | Nonconstant phases break the zero latch |
| Inverse trace and same-orbit collision | `PATH:28--41` | Eventual period reduces to `Tr(y)=Tr(F^p y)`; alternating fiber exact (`R`) | Forced-left reconstruction, period-two target, hard controls | Free right boundary; no bounded-delay adjacent trace |
| Fixed-period automata/SAT | `PATH:7,31--32,41`; ladder reports | Many exact bounded exclusions (`C`) | Witnesses and minimal cores | State/free-boundary growth; finite depth is not uniformity |
| Local statistics and finite quotients | period-two additive, parity, carry, runlength, divergence reports | Stated ranking/quotient classes killed (`K`) | Farkas certificates, closure collisions, `D8` action | Ordered frontier information is discarded |
| Boundary/right-cone regularity | `PATH:4,33--35`; bilateral/right-filter reports | `rho` avoids `11` and `00000` for an actual alternating right cone (`U`) | Actual-right SAT filter and forbidden factors | Boundary information reaches only logarithmic depth unless coupled to the active cone |
| Dyadic/automatic/spectral coordinates | `PATH:14--24,34,43,45--46,74,88`; dyadic Peel reports | Several exact identities; most shortcut claims killed | Dyadic cascade spectrum and exact lift monoid | A basis change is not a composition law; periods alone overlap |
| Symbolic formulas, ideals, and proof systems | dynamic ideal, mortality SAT, interpolant, Bezout, cofactor, `PATH:9,81,85,87` | Exact finite certificates and some uniform branch identities | Survivor indicators, restart cocycle, Craig cuts | Translation changes the boundary state; satisfiable fixed-input proofs remain small |
| Peel/cut/queue/frontier geometry | rotated Peel through frontier-graph reports | Full period-two finite-rank branch reduced to orbit separation (`R`) | Shared `phi` triangle, rank descent, inverse system | Aperiodic endpoint/source-orbit disjointness remains |
| Primitive period-three active core | `RESULTS-period3-fiber.md`; `RESULTS-period3-active-core.md` | Exact ternary quotient, finite carry signature, and all-length nonincrease of an 11-factor lexicographic vector (`U/R`) | Zero-tail dual and equality-subgraph weighted-graph proof | Equality transitions remain; a strict final rank component is open |
| P2 measures and orbit closure | `PATH:8,11,44--47,61,78--80`; checkerboard reports | Ensemble facts and bounded patch growth | Markov classifications, checkerboard fixed point | Almost-everywhere statements miss the lone seed |
| P2 finite trace statistics | `PATH:76,89`; subword and dyadic-shell reports | Large finite periodicity exclusion and no detected bias (`C/M`) | Bit-exact long prefixes, factor counts, shell discrepancy | Any finite prefix leaves the asymptotic limit open |
| P2 seed-specific dyadic analysis | `RESULTS-p2-p3-cross-review-2026-09-03.md`; `RESULTS-p2-time-index-walsh.md` | P2 iff dyadic-shell maximal discrepancy is sublinear; sufficient Walsh and averaged xor-correlation bounds (`U/R`) | Canonical all-scale target and exact Fourier identities | Quantitative correlation decay for this fixed orbit remains unproved |
| P2 local conservation laws | `RESULTS-additive-conservation-probe.md` | Only trivial rational additive densities through width 12 (`C/K`) | Exact rank certificate and Rule 184 positive control | Finite width does not exclude nonlocal or unbounded-width laws |
| P3 algebraic/circuit/proof complexity | `PATH:9,12--24,43,48,63--66,81,85,87,91--93` | ANF theorem, exact small circuits, validated fuel (`U/C/I`) | Honest cost instrument and bounded controls | Arbitrary-input complexity is not fixed `n -> c_n` work |
| P3 exact dyadic query algorithms | `RESULTS-hashlife-center.md` | Exact 1D Hashlife query; Rule 90 control polylogarithmic, measured Rule 30 calls superlinear (`U/M/K`) | A concrete shortcut architecture and exact cost counter | One failed architecture cannot prove a lower bound |
| Geometric, physical, and information analogies | `PATH:6,55--62,73,83,86` | Proposed routes killed or shown column-blind (`K`) | Sensitivity screens for future proposals | Single-column blindness, wrong category, or Rule 90 control |
| Adaptive/ML search | `PATH:19,21--24,30,40,90--92`; OpenEvolve reports | Exact falsifiers and evaluator lessons | Width-18 plateau edge; adversarial cut corpus | Finite fitness rewards phase residues and overfitting |

## 5. Active period-two dependency graph

The token-compressed and more current form of this graph is
`experiments/rule30/p1-period2-invariant/PROOF-STATE-CAPSULE.md`.  It also
records the binary-wedge high-bit elimination.  The essential scope
distinction is that endpoint-derived orbit separation is exact, whereas
arbitrary-queue mortality and the binary-wedge horizon are stronger
sufficient statements.

The live P1 work is one chain of reductions, not thirty independent bets:

```text
eventual period two
  -> same-orbit collision
  -> alternating trace phase
  -> Gray/OR frontier and hard-core endpoint
  -> inverse-terminal cut I(e)
  -> finite Peel rank versus a hard-core endpoint
  -> rank zero
  -> first infinite cut has tail 2^omega or 3^omega
  -> reversed-diagonal queue
  -> frontier source-to-terminal distance divergence
  -> O_2 intersect I(HC) = O_3 intersect I(HC) = empty.       OPEN
```

The arrows through the constant-tail reduction are uniform.  The final
disjointness is not proved.  P1, P2, P3, and the nonconstant period-two
exclusion therefore remain open.

## 6. Period-two result matrix

### 6.1 Coordinates and killed bounded summaries

| Report | Level | Complete retained object | Result to carry forward | Do not infer |
|---|---:|---|---|---|
| `RESULTS.md` | `U/K` | Exact `F^2` defect and full frontier | Same-orbit equations; local additive rankings falsified | No period-two theorem |
| `RESULTS-PARITY.md` | `U/K` | Gray/OR words | Exact inverse-Gray macro; fixed Hasse closure false | A low-order moment invariant |
| `RESULTS-CARRY.md` | `U/K` | Four-state carry plus ordered input | Carry actions generate `D8`; no synchronizing contraction | A proper contracting carry quotient |
| `RESULTS-RUNLENGTH.md` | `U/K` | Full lossless RLE/boundary gaps | Exact coordinate remains usable; bounded summaries fail | That run-length coordinates themselves are dead |
| `RESULTS-BILATERAL.md` | `U/K` | Actual column-one endpoint plus carry | Hard-core `no 11`; smallest phase/action summary not closed | That finite forbidden factors equal right realizability |
| `RESULTS-DIVERGENCE.md` | `U/K` | Ordered operator tiles | Toggle identity; signed/local charges falsified | Wave energy, contact mass, or imbalance monotonicity |
| `RESULTS-BELLMAN-RADIUS2.md` | `K` | Radius-two proposed energy | Solver-independent rational contradiction | A repair by merely changing the optimizer |
| `RESULTS-TAIL-DENSITY.md` | `K/R` | Full reconstructed tail | Coefficient-seven bound false; two weaker balances remain | Density from a finite radius potential |

All paths in this subsection that collapse the ordered growing boundary to a
fixed-size statistic have failed.  Full RLE is not lossy, but its bounded
digit summaries are.

### 6.2 Finite mortality encodings and symbolic algebra

| Report | Level | Exact object | Reusable positive output | Limit/failure |
|---|---:|---|---|---|
| `RESULTS-MORTALITY-SAT.md` | `C/U` | Variable-seed CNF | Exact mortality formulas and inverse-Gray correlations | Width remains a parameter |
| `RESULTS-CORE-MORTALITY-SAT.md` | `C/R` | Arbitrary active core | Diagonal target; UNSAT through core length 34 | No induction in core length |
| `RESULTS-DYNAMIC-BOOLEAN-IDEAL.md` | `C` | Full survivor ideal | Counts agree with projected SAT through `n=12` | Unit-ideal time not uniform |
| `RESULTS-PLATEAU-BEZOUT.md` | `C` | Plateau variety | Exact unit certificates | No uniform support/degree bound |
| `RESULTS-INTERVAL-ANNIHILATOR.md` | `U/R` | Survivor indicator on a matched interval | Shift conjugacy for matched branch | Unmatched restart states appear |
| `RESULTS-DEFECT-RESTART-COCYCLE.md` | `U/R` | Frontier, prior endpoint, survivor indicator | Exact advance/restart/extension split | Principal rank can plateau |
| `RESULTS-COFACTOR-AUTOMATON.md` | `K/U` | Ordered cofactors | Stabilizer recurrence | Cofactor alone is not closed |
| `RESULTS-PIVOT-EMISSION.md` | `K/U` | Symbolic emissions | Exact ANF; time-ordered pivot claim killed | Leading monomials do not force mortality |
| `RESULTS-CORE-DISCHARGE.md` | `U/K` | Reverse carry cascade | Fixed-horizon cascade lemma | Radius-seven local discharge has negative cycles |
| `RESULTS-CORE-INTERPOLANT.md` | `R/C` | Reachable cuts versus terminal cuts | Exact word-metric/Craig partition | Registered bounded clauses do not scale |
| `RESULTS-CORE-RESOLUTION-INTERPOLANTS.md` | `C/K` | Checked DRUP cores and interpolants | Small cubic separators | Translation-stable motif fails at next cut |
| `RESULTS-COUPLED-MODE-TRAP.md` | `K` | Proposed boundary/defect/right product | Exact audit of three clocks | No common scheduler; product is not closed |
| `RESULTS-JOINT-MORTALITY.md` | `C/K` | Left finite core plus genuine right cone | Long exact adversarial row | Constant-eight claim false; prefix is not periodicity |

These are multiple views of survivor emptiness.  Their compatible pieces are
the complete cut, survivor indicator, and restart state—not a translated
local clause by itself.

### 6.3 Peel, reachability, and the constant-tail frontier

| Report | Level | Uniform contribution | Exact remaining gap |
|---|---:|---|---|
| `RESULTS-DYADIC-PERIODICITY.md` | `U/K` | Reachable zero-ray cuts have dyadic eventual periods | Raw period-spectrum separation is false |
| `RESULTS-DYADIC-EXCEPTION-SEPARATOR.md` | `U` | Reachable cuts cannot be eventually alternating; removes the eventually-`2` endpoint family | Other hard-core endpoints |
| `RESULTS-PEEL-LIFT-MONOID.md` | `U/R` | Dyadic periodicity propagates through endpoint shifts | Periodicity does not pin the endpoint |
| `RESULTS-ENDPOINT-PEEL.md` | `U/K` | Exact aligned Peel tableau and moving-endpoint identities | Registered one-seed/two-follow induction is false |
| `RESULTS-ROTATED-PEEL-IDENTITY.md` | `U/R` | `P(I(sigma e))=sigma^2 I(e)` and exact rank drift | Aperiodic endpoints |
| `RESULTS-RANK-ZERO-REDUCTION.md` | `U/R` | Every positive finite rank descends to rank zero | Rank-zero separator |
| `RESULTS-ENDPOINT-FLIP-COCYCLE.md` | `U/R` | Flip `k` can affect only `[k,2k+1]` and affects coordinate `k` nontrivially | Ordered overlaps can move outward |
| `RESULTS-EVENTUAL-CONSTANT-TAIL.md` | `U/R/C` | First infinite cut tail is `2^omega` or `3^omega`; scale and affine reductions | All-length separator |
| `RESULTS-CONSTANT-TAIL-QUEUE.md` | `U/R/C` | Exact queue update, ternary quotient, invariant SFT | Mortality for every finite queue |
| `RESULTS-CONSTANT-TAIL-LANGUAGE-COCYCLE.md` | `U/K/R` | Exact regular inverse-image update | DFA rank expands; shortest accepted length divergence open |
| `RESULTS-CONSTANT-TAIL-FRONTIER-GRAPH.md` | `U/R/C` | Uniform inverse graph system, Fibonacci terminal set, `D8` cover | Source-orbit/terminal-set disjointness |
| `RESULTS-ACTUAL-RIGHT-FRONTIER.md` | `U/C/K` | Fully actual-right terminal sets form an inverse subsystem and raise finite distances | Rank descent permits an artificial finite endpoint prefix, so raw conditioning is too strong |
| `RESULTS-RIGHT-FILTERED-MORTALITY.md` | `U/K/C` | Actual right trace avoids `11` and `00000` | Finite-factor relaxation is incomplete |
| `RESULTS-PULL-COORDINATE-DEPTH.md` | `U/K` | Temporal ancestry is exact; unrestricted root-coordinate charge is false at `3001 0^382 2` | Long zero runs store dyadic phase |
| `RESULTS-HARD-CORE-PULL-DEPTH.md` | `U/R/C` | Every endpoint-derived pull root lies in the last three initial coordinates | Bound the depth of those localized roots |
| `RESULTS-ENDPOINT-EVENT-BRIDGE.md` | `U/K/R` | `A/B/C` are endpoint transitions `21/22/12` off the singleton boundary case; an all-`2` initial endpoint still produces a pull | Charge pull chains to internal ordered zero-prefix tokens, not literal initial endpoint pairs |
| `RESULTS-PULL-ROW-ALPHA-SUPPORT.md` | `U/R/C/K` | On a hard-core row, `alpha` is raw queue activity parity; it is enough to support only nonfinal pull rows in this one coordinate | Prove the ordered parity-flux contrapositive; `k=j`, fixed-radius, and arbitrary four-state source versions are false |
| `RESULTS-LATE-PULL-DIAGONAL.md` | `R/C/K` | Only rows `n,n+1,n+2` must exclude nonfinal pulls; all binary sources pass through length 20 | Exact CNFs grow; six terminal cut symbols are insufficient, and one relaxed source defect generally cannot carry the backward obstruction |

The constant-tail queue is stronger than the seed-derived statement because
its middle word is arbitrary.  The actual-right scale separator is weaker and
closer to the original application.  A proof may legitimately target the
weaker actual-right intersection; it need not prove mortality for every
abstract queue.

### 6.4 Adaptive searches

| Experiment | Level | What it contributed | Binding caution |
|---|---:|---|---|
| OpenEvolve cocycle rank | `M/K` | Exact plateau dataset and width-18 falsifier; no two-component separator in the recorded nonmodular grammar | Modular residues create perfect finite rankings by wraparound |
| OpenEvolve/GA rank-zero | `M/C` | Replays exact optimum at cutoff 23 and supplies difficult witnesses through cutoff 96 | Failure to cross `2T+2` is not evidence for the bound |

Future adaptive search should generate proof templates whose branch
conditions can be checked symbolically.  It should not optimize another
unproved numerical rank over larger cutoffs.

## 7. Correlations that survive cross-examination

### 7.1 One four-state kernel appears in four orientations

The carry transducer, inverse-terminal triangle, Peel map, queue scan, and
frontier lift all curry or rotate the same local four-state table `phi`.
The carry input actions, frontier fiber actions, and affine boundary actions
all recover the same eight-element `D8` group.

The complementary curry is now exact as well.  Fixing a Peel-output symbol
gives a 13-element transformation monoid with only one- and two-cycles;
fixing the queue-input symbol gives the inverse local permutations and closes
to `D8`.  The former proves the exact parity-pure period-doubling language
and forbids consecutive strict doublings, while the latter transports the
ordered affine phase without contraction.

This is explanatory and restrictive:

- vertical extension transports one new coordinate reversibly;
- raw formula/DFA rank expands because information is not being forgotten;
- carry synchronization and scalar contraction cannot be the proof; and
- the boundary `D8` phase should be normalized, stratified, or explicitly
  accumulated, never silently discarded.

This correlation joins reports that previously looked like separate carry,
scale, and graph experiments.

### 7.2 The live target has several exactly equivalent faces

The following are not independent conjectures in the constant-tail branch:

```text
finite queue mortality
<=> shortest surviving queue length tends to infinity
<=> frontier source-to-terminal distance tends to infinity
<=> O_c intersect I(HC_omega) is empty, c in {2,3}
<=> no finite-Peel-rank inverse cut lies over an infinite hard-core endpoint.
```

A counterexample or lemma in any one coordinate must be translated before
launching a new search in another.  Re-running all four is duplicate work.

### 7.3 Dyadic structure helps only after source reachability is imposed

Two superficially similar dyadic facts must remain separate:

- fixed sheared/right-boundary columns are dyadic-periodic but are only
  `O(log t)` deep at center time `t`; this route is closed; and
- a fixed finite queue word drives an ultimately dyadic cut in the zero-ray
  orbit; this acts on the exact live source orbit.

Raw spectra overlap the accepted endpoint family.  Combining dyadicity with
zero-ray reachability produced the genuine exceptional-family separator.
That successful hybrid is the model for future combinations: add a missing
hypothesis, not another analogy.

### 7.4 Fibonacci is a target-language count, not a growth law

The proved Fibonacci quantity is

```text
|A_h| = number of length-(h+1) hard-core endpoints = F_(h+3).
```

The accepting-state count in one minimized DFA is a neighboring Fibonacci
sequence for representation-specific reasons.  Neither count implies a
golden-ratio geometry, Fibonacci polynomial degree, or divergence of graph
distance.  The one-lift endpoint-delay counterfamily shows that a single edge
can postpone the first decoded defect arbitrarily far.  Counting terminal
states or Zeckendorf-coding them is therefore only a coordinate change until
a source-ancestry monotonicity law is supplied.

### 7.5 Exact right realizability carries information absent from local SFTs

At scale 27, the finite forbidden-factor relaxation permits continuation
lengths 7 and 9, while exact right-light-cone membership lowers the observed
maxima to 5 in both tail modes.  This is the largest measured gain from adding
a hypothesis that the abstract queue discarded.

The exact frontier product has now been run.  Fully actual-right terminal
sets form a proved inverse subsystem.  By horizon 12 their count is `156`
instead of the hard-core `610`; the tail-2 arbitrary-queue minimum rises from
`18` to `23`.  Exact `D8` phase minima also separate.

Cross-examination exposes a load-bearing qualification.  Rank descent can
prepend finitely many artificial state-2 endpoint symbols, so its endpoint is
only eventually actual-right.  Filtering the whole terminal prefix is too
strong and cannot by itself prove period two.  Actual-right information must
be applied beyond the artificial prefix, as in the scale-block reduction, or
coupled to a proved prefix bound carried by the source ancestry.  See
`RESULTS-ACTUAL-RIGHT-FRONTIER.md`.

### 7.6 Local algebraic separators need the moving boundary clock

Small Craig interpolants are real, but their translation-stable motif fails.
The defect/restart cocycle and endpoint-flip intervals identify the missing
data: translating a cut changes the restart phase and the active boundary.
The compatible synthesis is a Peel pullback with explicit restart state,
not another spatially repeated cubic clause.

### 7.7 The scale charge and endpoint-flip interval are complementary

The scale census leaves a sharply falsifiable charging target:

```text
s_2(W) <= #2(W) + indicator(22 occurs in W),
s_3(W) <= #2(W) + 3.
```

Endpoint coordinate `k` rewrites only cut interval `[k,2k+1]`.  These facts
originally suggested a pointwise ordered matching proof.  That certificate is
now killed at length 21: six source positions can be simultaneously invisible
to every survival row.  The numerical inequalities remain valid through
length 22, but any proof must use cumulative order (as in section 7.8), not
independent endpoint sensitivity.

### 7.8 Zero-prefix telescoping supersedes pointwise scale matching

The proposed independent endpoint-intervention matching and all of its
derivative-rank compressions fail at length 21.  Cumulative left-to-right
interventions remove the cancellation, and the still simpler chain

```text
W, 0W[1:], 00W[2:], ..., 0^|W|
```

supports a deterministic earliest-change greedy matching.  It has no failure
through length 22 in 242,783 cases.  Tail 2 matches every survival row; tail 3
matches every nonfinal survival row.  The resulting coarse bounds
`s_2(W)<=|W|` and `s_3(W)<=|W|+1` already prove the scale separator if the
greedy statement is established uniformly.  See
`RESULTS-SCALE-TELESCOPING.md` and its preregistrations.

Writing adjacent affine changes as `D8` holonomy defects does not close the
row update.  Equal defect words with the same absolute phase already have
different successors at length eight; all previous endpoints still collide
at length nine.  A preregistered repair retaining the first and last symbol
of every scenario queue passes held-out lengths 11--12 and fails at length
13.  Complete interior dependency queues are the smallest state class here
with proved closure.  This kills a direct Higman/ordinal rank on bounded
defect annotations but leaves projected diagonal support itself intact.  See
`RESULTS-HOLONOMY-DEFECT-CLOSURE.md`.

### 7.9 Equality-subgraph synthesis is now proof-bearing in period three

The primitive `011` zero-tail dual supplies the archive's first successful
all-length use of the adaptive-ranking workflow.  An exact weighted graph
proves that the number of `010` factors never increases across two
consecutive zero-tail steps; restricting to its equality edges and repeating
the argument yields an eleven-component lexicographically nonincreasing
factor vector.  Equality remains possible in every component, so period
three is still open.

The method can be mutated into the period-two attack only after a fixed exact
path graph or composition law for `(Q_n,Psi_n)` is derived.  The period-two
frontier currently carries a growing dependency diagonal, and the existing
closure collisions prove that projecting it prematurely to local factors
would be unsound.  The valid transfer is the equality-subgraph workflow, not
the period-three trigram invariant itself.

## 8. Overlooked opportunities, ranked

### A. Actual-right frontier product — completed and scope-corrected

The product, projection proof, distances through horizon 12, and monodromy
audit through horizon 10 are complete.  It gives a real finite separation,
but the direct period-two inference fails because rank descent may leave an
artificial finite endpoint prefix.

Retained output: the exact conditioned inverse subsystem, independently
replayed right-cone witnesses, and phase-cost table.

Correct successor: condition only after a prefix bound proved from the source
word/Peel ancestry, or use the scale formulation beyond both finite prefixes.

### B. Monodromy-stratified distance — finite phase exclusion killed

The exact augmented BFS finds all eight phases reaching both hard-core and
actual-right targets by horizon seven.  Therefore no persistent missing
phase exists in this representation.  Actual-right conditioning does raise
individual phase costs—by as much as eight symbols at horizon ten—but that is
finite evidence, not a phase invariant.

Why it is new: earlier ranks discarded the phase; the graph theorem now gives
the exact three-bit multiplication law and source ancestry needed to retain
it.

Retained possibility: carry `D8` as boundary state inside an ordered
scale/ancestry proof.  Do not launch a standalone phase-exclusion search.

### C. Peel-recursive Craig separators

Pull the checked small-cut interpolants back through `Peel` and include the
restart/boundary state from the exact defect cocycle.  Search for

```text
J_h(x,b) = J_(h-1)(P(x),b') plus a checked boundary clause.
```

Why it is new: the failed search required spatial translation invariance;
this search follows the proved rotated dynamics.

Kill condition: the smallest next-width separator cannot be expressed from
the pulled-back predecessor plus any bounded explicit restart state in the
preregistered grammar.

### D. Ordered scale matching

Attempt the injection suggested in section 7.7, using the interval ancestry
and affine boundary phase.  First recover the empirical `#2 + contact` bound
from a machine-checkable matching on all words through the existing census;
then isolate a local exchange rule that is independent of word length.

Kill condition: an exact word for which every allowed ancestry matching needs
more than the stated credit, even though the numerical inequality survives.

### E. Proof-template evolution

Use the GA/OpenEvolve witnesses only as adversarial tests for one of A--D.
Evolve branch-complete rewrites, matchings, or interpolant recurrences and
verify their identities for symbolic inputs.  Exclude `%` and any feature
whose range is not proved.

This is lower priority than A--D because search does not supply the missing
quantifiers by itself.

## 9. Combinations that remain invalid

- Width three does not solve width one: a periodic center does not force an
  adjacent periodic column, and finite-delay reconstruction is falsified.
- Sheared-column dyadic periodicity does not constrain the moving physical
  center diagonal without a proved bridge.
- Walsh/Fourier spectra of the arbitrary-input Rule 30 gate or finite-time
  center map do not imply P2.  This is distinct from the time-index function
  `r -> c_(2^k+r)`: a uniform maximal-Walsh bound for that seed-specific
  function does imply P2 by the proved dyadic-block decomposition.
- Computational irreducibility does not imply Martin-Lof randomness or a
  relation to Chaitin's `Omega`.
- A nonlinear “harmonic cascade” has no energy or bandwidth contradiction in
  this discrete finite-support problem.  The exact replacement is the
  four-state `phi` cocycle.
- Finite-width boundary cycles are pigeonhole facts about a different closed
  system, not evidence that the infinite zero-background orbit consumes
  randomness from its boundary.
- ANF degree, proof size for one encoding, and arbitrary-input circuit
  complexity do not give the fixed-sequence work lower bound in P3.
- Ensemble ergodicity, cryptographic tests, and no detected bias do not imply
  P2 for the lone seed.

## 10. Recommended next sequence

For P2, the prize-aligned next theorem is a uniform power saving for the
time-index xor correlations on every dyadic shell.  Equivalently, prove enough
Walsh decay to make `k W_k / 2^k -> 0`.  Use the exact two-orbit defect
recurrence to retain source ancestry; do not return to ensemble ergodicity,
generic Boolean-gate spectra, or larger finite bias tables.  For P3, only a
new exact center-observational quotient is presently credible; ordinary
Hashlife and arbitrary-input complexity have already failed to bridge to the
fixed sequence.

For the active P1 period-two effort:

1. Prove or falsify pull-row alpha support using the exact activity-parity
   formula.  This one-coordinate pull-only statement is sufficient and is
   strictly weaker than projected diagonal support.  Do not extend its
   complete length-23 census; derive the ordered parity-flux contrapositive.
2. Prove or falsify projected diagonal support using the ordered
   zero-prefix/Peel filtration.  Tail 2 needs only the additive quotient
   `(alpha,beta)`; tail 3 needs the terminal state `(alpha,gamma)=A(0)`.  A
   second route is the one-credit half-word recurrence.  Do not return to
   pointwise derivative rank, fixed-radius edge rules, endpoint-only
   telescopes, or literal half-block embedding; all are exactly falsified.
3. Replace the falsified unrestricted coordinate-interval bound.  The family
   `3001 0^m 2` violates `r>=2h-1` at `m=382` and shows that right-hand zero
   gaps carry dyadic phase.  Either retain a scale/gap vector in the ancestry
   charge, or prove the bound only for queues that are reversed inverse
   diagonals of hard-core endpoints.  The sharp half-density inequality is
   unnecessary: injection of one chain into `N` ordered zero-prefix tokens,
   or `8N` token/`D8`-phase pairs, already gives the finite depth bound needed
   for mortality.  A source-ancestry bound is still needed to couple frontier
   path length to the artificial endpoint-prefix length.
4. In parallel conceptually, test Peel-recursive interpolants against the
   existing checked cores, with the restart state explicit.
5. Use all stored SAT, GA, OpenEvolve, and actual-right frontier witnesses as
   an external corpus for any proposed uniform rule.
6. Do not extend the conditioned distance or phase tables without a new
   uniform recurrence candidate.

Success means a uniform lemma with an independently checkable proof.  A new
distance table, larger cutoff, fitted recurrence, or perfect finite fitness
score is only a falsification instrument.

## 11. Template for every new experiment

```text
Title:
Date and commit:
Target theorem and exact quantifiers:
Domain (lone seed / finite row / hard-core / actual right / ensemble):
Complete state and seam/update law:
Where finite support enters:
Information intentionally discarded:
Uniform claim being tested:
Finite bounds, if any:
Positive controls:
Negative controls (including Rule 90 when relevant):
Preregistered success and kill conditions:
Result level (U/R/C/M/K/I):
Exact result:
Reusable artifact:
Which prior obstruction it escapes:
Which prior result consumes it next:
Explicit non-claims:
Reproduction command:
```

This template should be filled before a new broad search.  It is acceptable
for the result to be `K`; a precise killed mechanism is durable progress.

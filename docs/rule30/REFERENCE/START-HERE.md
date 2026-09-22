# Rule 30: compact research index

Updated: 2026-09-03 (review 2026-09-11: 27 new experiments in progress; see EXPERIMENT-ATLAS.md for latest)

Purpose: resume this project with the fewest tokens consistent with not
repeating work.  This file routes to authoritative sources; it is not itself a
source for publication claims.

## Current status

| Problem | Status | Best live edge |
|---|---|---|
| P1: center-column nonperiodicity | **OPEN** | R1's OR-specific zero-set obligation; within it, the period-two same-orbit rung |
| P2: limiting density `1/2` | **OPEN** | P2 is exactly subcubic integrated discrepancy energy on dyadic shells; the needed all-scale seed-specific bound is unproved |
| P3: computational effort | **OPEN** | Exact itinerary observers, controlled affine scans and supplied-object shortcuts are proved in their stated scopes; actual control construction and every general singleton-query lower bound remain open |

Proved prize-adjacent results exclude eventually constant centers only:

- zero center tail: `RESULTS-zero-tail.md`;
- one center tail: `RESULTS-eventual-period.md` and
  `RESULTS-inverse-trace.md`.

No document proves an unrestricted nonconstant-period exclusion, density convergence for the
lone seed, or a computational lower bound.

The [2026-09-15 entry-point audit](AUDIT-entrypoint-overlooked-2026-09-15.md)
corrects overbroad contraction and column-blindness screens, integrates row
46's already-refuted generic obligation, and records quantitative P1
mismatch and sparse P2 correlation targets. Their missing seed estimates
remain open.

The [P1 mismatch follow-up](RESULTS-r1-mismatch-followup.md) proves an
explicit tradeoff between right-neighbour mismatches and centre-equation
errors for independently driven halves, checks the logarithmic scale
against Rule 90, and records a small `0001` boundary certificate. It also
repairs the old pin-lock sampler's two-word coverage bug. No mismatch
upper bound or nonconstant-period exclusion is obtained.

The [periodic-cylinder deadline corollary](RESULTS-r1-cylinder-deadlines.md)
does give uniform alternating-trace exclusions for two specified
right-prefix families: with left support bounded by depth `d`, failure
occurs by `d+7` or `d+10`, with exact sharp deadlines computed from the
forced periodic left tail. This holds for every right continuation.
Entry of the singleton orbit into either prefix family remains unproved;
the unrestricted period-two problem stays open.

The [fundamental-frequency audit](RESULTS-fundamental-frequency-search.md)
distinguishes the exact spatial weight of wavelength four from temporal oscillation.
It classifies the bounded one-sided linear extraction weights and records
a fixed-candidate temporal search with held-out blocks; no persistent
temporal frequency or asymptotic spectral claim is established.
Its [bilateral continuation](RESULTS-bilateral-frequency-current.md) gives
an exact bounded-endpoint current identity and an optimal localization
frequency, while the [1/3 scale target](RESULTS-third-frequency-scale-target.md)
identifies an intermediate-growth criterion sufficient for P1. Neither
supplies the required singleton growth or cancellation estimate.

New 2026-09-07: the left light-cone frame is written as an exact recurrence
whose OR is *absorbing*, giving a glide form `s(t+g,x-g)=s(t,x)` of the left
region's periodicity, and the Rule 90 control fails it. The underlying
phenomenon and its depth table are NKS p. 871, reproduced here to the unit
(first period 32 at `j = 87,867`). It corrects obstruction A on the left side.
It does **not** open a route: the conditional argument in the first draft is
retracted and Kopra 2023 Thm 3.5 stays in the chain. See
`RESULTS-ordered-wedge-glide.md` sections 5 and 6, and
`CROSS-ARCHIVE-2026-09-07.md`.
[Ordered-ancestry obstruction paper](obstruction/BOUNDED-CERTIFICATE-OBSTRUCTIONS.md) collects the exact bounded-certificate failures and their scope corrections.

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
| Corrected all-route synthesis after ancestry counterexamples | `RESULTS-cross-route-synthesis-2026-09-02.md` |
| P2/P3 archive review and prize-aligned reductions | `RESULTS-p2-p3-cross-review-2026-09-03.md` |
| External literature/claim audit | `PATH.md` section 8, `REFUTATION-*`, and `CLAIM-AUDIT-*` |

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

For an ordinary continuation that does not need the full historical route
table, start instead with
`experiments/rule30/p1-period2-invariant/PROOF-STATE-CAPSULE.md`.  It records
the exact implication DAG, distinguishes equivalent targets from stronger
sufficient ones, and routes to only the five result reports needed at the
current frontier.

Do not rerun: larger finite-period SAT grids, fixed-depth ladders, generic
left-permutive arguments, bounded adjacent-column prediction, support-width
descent, periodic-mask contraction, or local additive rankings.
Also closed, do not rerun: the Collatz / 2-adic shift conjugacy of the
triangular core map, which exists, is automatic, and reaches no prize target
(`AUDIT-collatz-2adic-bridge.md`); bounded-degree `F2` certificates over raw
seed bits for the alternation systems, Nullstellensatz or polynomial calculus
(`experiments/rule30/p1-period2-invariant/RESULTS-PT2-PC-DEGREE.md`); and
guarded-seam lemmas from any finite history, whose uniform-in-`n` form is
equivalent to a bounded run and strictly stronger than `RW`
(`experiments/rule30/p1-period2-invariant/RESULTS-SEAM-HISTORY-GUARDS.md`).

### P2

Read `RESULTS-p2-p3-cross-review-2026-09-03.md` and
`RESULTS-p2-time-index-walsh.md` first.  For the signed center trace, P2 is
exactly equivalent both to sublinear maximal discrepancy on every dyadic shell
and to the subcubic integrated prefix energy `I_k=o(2^(3k))`.  The latter has
an exact associative composition using only length, total discrepancy, prefix
area, and energy.  A van der Corput theorem also proves P2 if every fixed
ordinary time-shift defect has density `1/2`, giving the precise quantitative
upgrade required from the temporal-period work.

The updated [coarse-energy result](RESULTS-p2-coarse-energy-and-or-pairing.md)
proves subquadratic dyadic-tree energy **equivalent** to P2. Time-index Walsh
decay or an `l1` XOR-autocorrelation power saving remain stronger sufficient
conditions. A [sparser ordinary-shift condition](RESULTS-p2-sparse-difference-correlations.md)
uses only lags `2^a-2^b` and nonpositive limiting upper correlations; its seed
estimate is unproved. All statements concern
the lone seed directly.  Measurements through the exact `2^25`-row cache are
strongly consistent with square-root cancellation, but no uniform bound is
proved.

Then read `PATH.md` R8 and section 9.3,
`RESULTS-orbit-closure-diagnostic.md`, and
`RESULTS-checkerboard-growth-extended.md` for the older measure route.  Uniform
Bernoulli invariance and almost-everywhere density `1/2` miss the lone seed by
obstruction E.  The orbit-closure target is likely stronger than P2, and
checkerboard-patch growth is finite evidence only.  The literal local additive
conservation-law route has also been eliminated over the rationals through
width 12; see `RESULTS-additive-conservation-probe.md`.

### P3

Start with [the scope audit](P3-SCOPE-AUDIT.md) and
[the current investigation](RESULTS-p3-implicit-boundary-investigation.md).
The all-index singleton observer is now explicit in itinerary B/C coordinates.
Read [two affine scans](RESULTS-p3-two-affine-scans.md),
[the two-time high observer](RESULTS-p3-two-time-rise-reset.md), and
[guarded rise chains](RESULTS-p3-rise-chain-transparency.md) for the current
constructive route. These exact identities keep both origins and ordered
controls. They have not produced an o(n) query algorithm.

The next obligation is to construct the required actual control histories
from binary n and prove a sublinear total-work recurrence. Supplied repetition
grammars and fixed-width large-time powering have exact shortcuts, but their
construction is charged. The actual time-0/time-4 collision refutes the
rise-only summary for a second two-time block; the full alternating pruning guard has only the
two classified small actual cases. Keep these controls when proposing a
new summary. A finite benchmark, arbitrary-input sensitivity, faithful group
representation obstruction, or parallel depth is not a general lower bound.

The [session limits supplement](RESULTS-p3-session-limits-supplement.md)
preserves final reasoning and withdrawn suggestions. The machine-readable
session inventory and synchronization receipt are under
`research/p3-session-sync/`. Catalog entries separate source-reviewed proofs,
fresh bounded replays, old saved evidence and unformalized correspondences.
No new P3 Lean kernel theorem is claimed. The official-wording issue remains
separate from exclusion of o(n) and the stronger eventual Omega(n) statement.

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

Best clean theorem target:

> **Binary-wedge horizon.**  A length-`n` binary source forcing a constant
> inverse cut `c in {2,3}` leaves the binary endpoint alphabet within its
> first `n+2` appended symbols for `n>=7`; equivalently `M_c(n)<=n+1` in that range.

By the rotated-Peel identity, this excludes every binary word `f` of length
`2n+2` satisfying `P^n(I(f))=c^(n+2)`, hence implies the three-row late-pull
diagonal and closes the nonconstant period-two rung.  It is stronger than
DLP but discards the hard-core and terminal-pull predicates.  The exact
bound has zero failures for `7<=n<=29`, exhaustively over all `2^n` sources at
each length (lengths 5 and 6 violate the unrestricted version), and over that
range the slack `max_c M_c(n) - n` declines at `-0.129` per unit `n`, so the
bound is not asymptotically tight and does not need a sharp argument.  Read the
next census row for the slope, not for a falsifier: the fitted slope has risen
at every extension (`0.842` at `n<=27`, `0.871` at `n<=29`) and the margin under
the `0.95` that would suffice is now `0.079`. The preregistered sharper version
`M_c(n)<=n` is false at `M_3(15)=16`; that falsifier saturates the sufficient
bound and dies on the next symbol.  See the period-two
`RESULTS-BINARY-WEDGE-HORIZON.md`.

The high-bit constraint is no longer part of the open search.  Affine `D8`
triangularity uniquely forces the binary continuation once the source is
fixed.  The remaining theorem is the one-bit statement that the resulting
defect word is not constant; see
`RESULTS-BINARY-WEDGE-HIGH-ELIMINATION.md`.

The smallest sufficient fallback remains:

> **Three-row late-pull diagonal.**  A length-`n` constant-tail scale block
> has no nonfinal endpoint pull `1 -> 2` at rows `n,n+1,n+2`.

This is strictly weaker than every support or survival conjecture below.  If
an absolute pull is at `m=3n+r`, `n=floor(m/3)`, the block `e[n:2n]` sees it
at relative row `n+r`; hence these three rows suffice.  The claim uses no
alpha variables.  It has no failure in the full hard-core corpus through
length 23, eight aligned GA adversaries, 240,000 long random word/tail cases,
or all binary words through length 20.  Its exact diagonal CNFs are UNSAT
through `n=20`, but generic proof width/conflicts grow and no induction is
known.  A hard-core `n=12` certificate realizes the pull with a six-symbol
constant cut suffix, so the three candidate rows do not reduce to a literal
`3 x 3` local check.  See `RESULTS-LATE-PULL-DIAGONAL.md`.

In a separate assumption-core audit, 88/90 DLP formulas through `n=15` are
already UNSAT after every continuation no-`11` clause is removed.  The only
exceptions are `(n,c,r)=(5,3,1),(6,2,1)`, each killed by a singleton clause.
This is finite evidence that the contradiction lies at the binary source
boundary, not in actual-right forbidden factors.  See
`RESULTS-DLP-HARD-CORE-CORE.md`.

The stronger alpha route is:

> **Pull-row alpha support.**  At every nonfinal forced endpoint transition
> `1 -> 2`, some zero-prefix token `k` at or to the right of row `j` changes
> the single affine coordinate `alpha`.

An immortal relevant endpoint either becomes eventually `2` (already
excluded) or has infinitely many such pull rows.  For an absolute pull
`m=3n+r`, the scale block `e[n:2n]` sees row `j=n+r>=n`, making the required
token interval empty; thus this lemma closes the period-two rung.  On
hard-core rows `alpha` is exactly the parity
of nonzero cells in the raw reversed dependency queue after its leading
tail.  The claim has zero failures in 392,830 word/tail cases and 31,595 pull
rows through length 23, but is unproved.  The diagonal-token strengthening
fails at length six, so a bounded-radius proof is unavailable.  See
`RESULTS-PULL-ROW-ALPHA-SUPPORT.md`.

The stronger fallback theorem is:

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

The pull alphabet now has a direct endpoint meaning: away from the singleton
boundary credit, `A/B/C` are exactly future hard-core transitions
`21/22/12`.  This kills a literal initial-`12` witness—`22222222` has no such
pair but its queue performs `AC`—and clarifies the next hybrid.  The sharp
coordinate-depth estimate is unnecessary; any finite depth bound in the
initial length closes mortality.  The current ancestry target is therefore
to inject one pull chain into the ordered zero-prefix tokens, possibly with
an eight-state `D8` phase decoration.  See the period-two
`RESULTS-ENDPOINT-EVENT-BRIDGE.md`.

## Do-not-repeat obstruction screen

Reject a proposal immediately unless it explains why these do not apply:

| ID | Obstruction |
|---|---|
| A | Trace/boundary propagation reaches `O(log t)` depth while the target is `Theta(t)` away. **Right boundary only.** On the left the depth reached with period `<= P` is `3, 8, 29, 400, 87867, >2.1e9` for `P = 2..64` (NKS p. 871) — super-exponential in `log P`, not linear. Both still need unbounded period at depth `Theta(t)`; only the rate differs (`RESULTS-ordered-wedge-glide.md` 3) |
| B | The argument also excludes Rule 90's known periodic center |
| C | A limiting bulk statistic alone cannot distinguish arbitrary arrays differing on one column. This does not exclude a Rule-30-specific identity or quantitative bound linking that statistic to the center; the overwritten array need not be a valid orbit |
| D | The proposed shortcut names but does not derive its exact composition/seam law |
| E | An ensemble or almost-everywhere theorem does not cover the lone-seed orbit |
| F | A fixed-depth strip leaves a new free outer boundary |
| G | Arbitrary-input complexity says nothing about evaluating one fixed input |
| H | Finite data cannot prove an infinite statement |
| I | Satisfiable fixed-input proof systems hit a small `Theta(n^2)` derivation ceiling rather than a lower bound |

Full hypotheses and affected rows are in `PATH.md` section 7.3 and
`FINDINGS.md` section 5b.

Two standing screens, both cheap and both paid for:

- **Bounded summaries.** The queue scan's injectivity excludes bounded
  summaries that must reproduce its whole successor trace. It does not
  exclude lossy summaries sufficient for a particular target, ranks on the
  whole queue, or contraction under additional guards. Check the exact
  certificate class against the source theorem; see
  `CROSS-ARCHIVE-2026-09-07.md` section 1 and the injectivity proof's section 6.
- **Which branch of the OR.** "Uses Rule 30's OR" is not enough: the saturating
  branch and the open branch behave oppositely, and in the left light-cone
  frame the OR is what *creates* order. See `CROSS-ARCHIVE-2026-09-07.md` 3.1.

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

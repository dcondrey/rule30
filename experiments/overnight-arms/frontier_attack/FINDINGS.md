# Frontier attack, 19 arms, 2026-08-30

Nineteen parallel arms: 14 against the four surviving frontiers (§1), plus 5
deliberately outlandish arms (§1b) picked to be either genuinely novel or a
fast, clean kill. **No prize problem moved.** One theorem proved (about a
method, not about Rule 30), one filter correction (§1b, a15), six corrections
to committed repo material, and eight arms killed at their own stated gates.

Nothing in this directory has been written into `docs/`. The register delta in
§3 is proposed, not applied.

*Status update, 2026-08-31.* The section-8 work this file previously described
as a live uncommitted diff (an external literature survey on P1/P2/P3 prior art
and transfer barriers, appended after section 7) is now committed, as `f2664cb`,
together with sections 7, 9, 10 and 11. Anyone applying §3's delta rebases onto
`main` rather than onto a working tree. §3 itself is still unapplied.

Verification column: **P** = the parent session reproduced the load-bearing
claim independently, from primary data or its own code. **A** = agent-reported,
files present and gates re-run, claim not independently re-derived.

## 1. Verdicts

| arm | target | verdict | V |
|---|---|---|---|
| a1 | R1 zero-set obligation (row 1) | NEGATIVE-NAMES-MISSING-LEMMA | P |
| a2 | stroboscopic descent (row 31) | NEGATIVE-NAMES-MISSING-LEMMA | P |
| a3 | orbit closure `Y` (row 8) | NEGATIVE, route refuted | P |
| a4 | P3 resolution lower bound (row 9) | NEGATIVE, metric mis-specified | P |
| a5 | alternating-trace fiber (row 41) | NEGATIVE, row stays OPEN | A |
| a6 | Ore ladder uniformity (row 46) | NEGATIVE, sub-route closed | P |
| a7 | ladder realizability | **LIMITATION THEOREM PROVED** | P |
| a8 | preimage-tree descent (new) | KILLED at step 0 | P |
| a9 | P2 density bounds (new) | NEGATIVE, rediscovery caught | P |
| a10 | trace soficness (new) | NEGATIVE, brief's object degenerate | P |
| a11 | Jen 1986 premise | PROCEEDING-WITHOUT-SOURCE | P |
| a12 | Rowland-Yassawi obstruction map | NEGATIVE, open problem named | A |
| a13 | P3 derivation upper bound | NEGATIVE, constant factor only | P |
| a14 | conserved window functions (row 53) | KILLED at step 0 | A |

## 1b. The five outlandish arms

| arm | target | verdict | V |
|---|---|---|---|
| a15 | nonabelian conserved invariant | NEGATIVE, orbit-phase bound (<=1.585 bits) | P |
| a16 | Polynomial Calculus degree (P3) | NEGATIVE, degree is O(1), not asymptotic | P |
| a17 | 2-adic valuation / Newton polygon (P1) | KILLED, no closed functional equation exists | P |
| a18 | cryptanalytic bias detection | NO BIAS FOUND, Bonferroni-corrected | P |
| a19 | ML-guided conjecture mining | REFUTED at depth 20000, pin rediscovered | P |
| a20 | Bridy citation check (row 46) | Lemma L FALSE, sharper bound found in source | P |
| a21 | R1 direct attempt (OR-nonlinearity) | NEW-OBSTRUCTION-NAMED, row 1 stays OPEN | A |

## 1d. Two follow-up arms

**a20 corrects row 46's citation and closes the ladder question, quantitatively.**
Lemma L (this document's a17 flag) is FALSE, both halves, refuted by Bridy's
own worked example (arXiv:1604.08241v2 = Alg. Number Th. 11 (2017) 685-712,
p.8, Ex. 2.14: `y=x^n` gives Ore height exactly `n`, growing exponentially in
state count) rather than by the secondary non-improvability sentence a17 had
leaned on — verified independently, both quantitative claims exact:
`N(7)=16,137 <= 32,000 < N(8)=40,970` and `N(20)=922,746,902 <= 10^9 <
N(21)=2,025,848,855`. Bonus: a6's witness family `G_n` is Bridy's own
Example 2.15, published 2016, not a novel construction. Row 46 stays OPEN
(a6's `m*2^(2m)` derivation is untouched, just not tight); the real content is
a quantified finiteness wall: excluding every `k`-state 2-automatic sequence
by this route needs `N(k) = (k+2)(k*2^(k+1)+1)` terms, reaching only `k=7`
states at the register's own `N=32000` and `k=20` at Wolfram's 10^9-bit check.
Corrects both a17 and this session's own dispatch: Bridy's `m` (automaticity
state count) and a6's `m` (kernel-span dimension) are different variables,
`m_span <= k <= 2^m_span`, so the comparison must be re-expressed in one of
them before it means anything.

**a21 attempts R1's localized lemma directly and finds a genuinely new
obstruction rather than a fourth automaton/SAT search.** Confirmed the three
convergent statements (a1 Lemma Z, a2's missing lemma, a7's `Diff_q` gap) are
one claim, with a real nuance a7's isn't literally the same implication (needs
one polarity excluded on a relaxed object, not identical). Proved four new
results on left-supported rows (`s(0,x)=0` for `x>=1`, which includes the lone
seed): Theorem U (exact uniformity of `s(t,0..k)` for `k<=t`), Theorem S
(bounded-window Bayes error stabilizes exactly at `t=2m+1`), Theorem W (that
stabilized error is strictly positive at every window width `m`, so bounded-
window closure fails unconditionally, not by failed search), and exact error
values `eps_30(1)=1/4` down to `0.17331` at `m=16` against `eps_90(m)=1/2`
exactly at every `m` (Rule 90's recent window carries zero information about
`r_t`; Rule 30's carries up to 83%, never all of it). Cross-checked
independently by the parent session with a simpler, non-Bayes-optimal
predictor and a different sampling protocol: same qualitative shape (well
below 1/2, consistent with a19's separately-found 0.75 accuracy figure), but
the exact 1/4 was not reproduced by the simpler check — expected, given the
different protocol, not a contradiction.
The named missing piece, precisely: a proof that `eps(m)>0` (proved on the
ENSEMBLE of left-supported rows) is realised on the lone-seed orbit's actual
trace specifically, not just across the ensemble. That is obstruction E
(measure-zero single-orbit gap) reached from a new direction, now with a named
quantity attached instead of a vague statement. Flagged explicitly, twice:
whether `eps_30(m) -> 0` as `m -> infinity` is NOT a route to P1 even if
answered, since exactness never arrives at any finite `m` regardless.

## 1c. What the outlandish batch actually found

None of the five moved a prize problem. Two are worth more than a flat kill.

**a15 corrects the standing filter's scope, and closes the gap it opens.**
PATH.md 0.1's column-blindness gate ("moves by `O(1/W)` or less") is stated for
normalised, real-valued functionals. It does not bind an EXACT discrete
invariant. Verified independently: a14's own `phi_w2_block11`, read mod 2
rather than as a density, stays flat under a column-0 overwrite where its
normalised twin decays. a15 found 1,988 real, verified, non-abelian conserved
invariants for Rule 30 that survive the gate as literally stated — then closed
them anyway with a general, width-independent argument: any monoid-valued
quantity computed by iterating a fixed map is a trajectory in a finite set, so
preperiod+period `<= |M|` by pigeonhole. Total information such an invariant
carries about the WHOLE infinite orbit is `<= log2|M|`, under 1.6 bits for
every monoid tested. This generalises a14's width-12 empirical bound to a
proof, for the non-abelian case, independent of width. Register action: PATH.md
0.1 should read "moves by `O(1/W)` or less **as a normalised functional**";
an exact invariant needs the orbit-phase argument instead.

**a19's one live number.** The empirically Bayes-optimal predictor of `r_t` on
the zero-set `{c_t=0}` from left-window history alone scores at chance
(0.4993). Every above-chance signal comes from one CA step of centre-column
history: the naive predictor `s(t,1) := NOT c_{t-1}` scores 0.7493 out of range,
matching logistic regression to many digits. Reproduced independently at
0.7503 on a nearby window. This is a correlation baseline, not structure; a19
states explicitly it does not touch a1's Lemma Z or a2's missing lemma, both
conditional on a periodic centre trace this orbit doesn't have.

**a16 is the sharpest negative: it found the first proof-complexity quantity
that separates Rule 30 from Rule 90, then proved the separation is a syntactic
artifact.** PC-refutation degree is exactly 2 for Rule 30 and 1 for Rule 90,
constant in `n`, both proved unconditionally and confirmed independently (ANF
degrees re-derived by a separate Mobius-transform implementation; certificate
script re-run, max-degree column flat at every `n = 4..64`). But Rule 160 (same
ANF degree, trivial column) ties Rule 30, and Rule 128 (higher ANF degree,
trivial column) beats it — the gap is `deg(ANF)`, readable off the rule number
before simulating anything. Under a4/a13's CNF encoding the ordering flips.
Rule 90 filter: **failed**, and a16 says so rather than arguing around it.

**a17 and a18 are clean, honest negatives.** a17: no closed functional
equation exists for the centre-column generating function, so Newton-polygon
machinery has nothing to act on — verified the load-bearing Hadamard-vs-series-
product distinction independently. It also corrected the parent session's
brief: eventual periodicity of a 2-adic integer's digit expansion DOES imply
rationality (verified with `-3/7`'s expansion from `(110)^inf`), the reverse
of what was asserted going in. a18: no bias survives Bonferroni correction over
100,838 tests; the one apparent 5.42-sigma hit was traced to a degenerate
lattice-valued null and dismissed by the agent itself, with the pre-audit
REJECT line left visible in raw output for inspection.

## 1e. Load-bearing sub-results the verdict table compresses away

Six results that carry the weight of their arm's verdict but do not appear in
§1's one-line entries. Each is what makes the corresponding NEGATIVE a closure
rather than a shrug, so a reader who stops at the table gets a weaker record
than the arms actually earned.

**a15-1. The survivor set is not "small", it is *exactly* the coboundary space,
by set equality.** `coboundary_check.py` does not compare counts. It builds the
coboundary set explicitly, checks the telescoping claim by direct simulation
(60 coboundaries x 25 random configurations per cell), and asserts set equality
against the search's survivors. Nine group cells, zero telescoping failures,
set-equal in all nine: `Z2 w=3` (8), `Z2 w=4` (128), `Z3 w=3` (27), `Z4 w=3`
(64), `Z2xZ2 w=3` (64), `Z5 w=3` (125), `Z6 w=3` (216), `S3 w=2` (6), `S3 w=3`
(216). So the zero is "exactly the rule-independent trivial space turned up and
nothing else", not "nothing turned up" — the same shape a14 reached for its own
class, by a disjoint route (ordered products and direct simulation; no linear
algebra, no de Bruijn graph, no continuity equation). `Z4`, `Z5`, `Z6`,
`Z2xZ2` and `S3` are new: a14 section 6 puts composite `Z/m` and primes past 3
outside its bound.

**a15-2. Rule 90's 567 invariants are column-sensitive, and that is the filter
working, not a separation.** All 567 sit at `0.522388`, the positive-control
value exactly, flat in `W`. The rule in the pair whose invariants *can* see
column 0 is the rule whose centre column is trivially eventually periodic; even
there they carry `<= 1.585` bits about the orbit and are eventually constant
along it. Reporting the formal Rule 30 / Rule 90 difference as a separation
would be the trap `PATH.md` 7.3 C records against rows 57-59. The excess
survivors are wholly degenerate: all 1,146 extras across the eight cells have
`f` the constant map, and `|surv_90| = |cb| * |G[2]|` holds in every cell.

**a15-3. Sampled cells have no power, and their zeros are not counted as
coverage.** The candidate space is `|M|^(2^w - 1)`. At `w >= 4` for `|M| >= 4`
a 300,000-candidate uniform sample covers a vanishing fraction, and `verify.py`
reports `E[coboundary hits] = budget * g^(2^(w-1)-1) / g^(2^w-1)` per sampled
group cell. Where that is below 1 the cell cannot detect even the trivial space
known to be present, so its zero is discarded rather than banked: `Z6, w=4`
returned 0 survivors from 300,000 samples at `E[coboundary hits] = 0.18`,
consistent with zero and uninformative. Sampled non-group cells (`T2`, `T3`,
`FlipFlop3`) have no coboundary formula, hence no calibration, hence
uninformative zeros too. No budget fixes this; the exhaustive frontier is the
entire empirical bound. The asymmetry is stated and is real: a sampled cell's
zero is uninformative but a sampled cell's *find* is a find, and the 206
verified `T3, w=3` invariants came out of a sampled cell.

**a16. Obstruction G: FAILED, and recorded as a failure rather than an
evasion.** a4 and a13 both ran this check and passed, because derivation length
grows in `n`. a16 ran it and failed the non-constancy half. The literal G
collapse does not occur — P3's seed is a unit axiom of `S_n`, not an argument,
so there is no input distribution and `d_PC` is 2 rather than 0. But the check
a13 actually executes asks whether the quantity is a nontrivial non-constant
function of `n`, and `d_PC` is 2 at every `n >= 2` (4 under the CNF encoding).
A constant carries no information about `n`. Evading G is supposed to buy a
nontrivial question about `n`; here it buys a constant, one step removed from
rows 63-66, whose measures were identically zero where this one is identically
two. The arm ends with no missing lemma in either direction: the upper bound is
proved outright and a lower bound above 2 is impossible, not merely unproved.

**a18-1. Each of the four tests is shown able to fire, and they are not
redundant.** `lfsr32` breaks test 1 deterministically (`L = 32` at
`n = 262,144` against `131,072` for rule30, a factor of 4,096; `J = 20` against
a null of `65,541 +- 176`) yet passes tests 3 and 4 cleanly. `bern51` breaks
test 3 as registered. `copy1000` breaks tests 2 and 4 (`abs z = 20.74` at
exactly lag 1,000, adjusted `p = 1.6e-90`) yet passes tests 1 and 3. Each test
catches something the others miss, which is what makes four of them jointly
finding nothing stronger than any one of them finding nothing. The `rule90`
control fires on everything but degenerately, being an all-zero string, and is
marked as establishing far less than the other three.

**a18-2. Three pre-registration deviations, all self-reported, `PREREG.md`
unedited.** D1: the registered `lag1000` control was mis-specified and is
provably null — `y_t XOR y_{t+1000} = r_{t-1000} XOR r_{t+1000}` is uniform, so
the construction destroys the correlation it was meant to plant; it is kept in
every table as an instructive failure and `copy1000` was added as the corrected
control. D2: the registered test-2 lag grid has no `Delta = 1000`, so
`copy1000`'s test-2 miss is a gap in the grid, not absent power —
`test2b_power_check.py` shows `z = 42.8` for `copy1000` against `0.47` for
rule30 at `Delta = 1000`, and is reported **outside** the `N = 100,838` ledger
because it was chosen after seeing test 2's output; folding it in would be the
multiple-comparison abuse the pre-registration exists to prevent. D3: test 1's
delivered ledger is `{G, J}` x 9 prefixes, not the registered `{J, Hbar, D}` x
6 prefixes; both are 18 by coincidence, not by design.

**a19. The symbolic-regression negative is exact, and is worth more than any
accuracy number in the arm.** The GF(2) stage solves by Gaussian elimination
for a polynomial over the feature bits with monomials of degree `<= d`
reproducing TRAIN *exactly*; an inconsistent system is a proof of nonexistence,
not a poor fit, and every claimed fit is re-verified against TRAIN by
assertion. Rule 30, targets A and B, every framing tested (`col-history
K<=12`, `left-window W<=8`): **no exact fit exists at degree 1, 2 or 3.** The
positive control recovers the Rule 30 local rule itself at degree 2, and Rule
90 fits at degree 1 everywhere, as it must, being additive. This fires H4's
pre-registered kill condition and carries no depth caveat inside the training
range, unlike every accuracy figure in the arm.

## 2. Corrections to committed material

These are defects in files already in the tree. Each is stated with what
replaces it.

**2.1 `RESULTS-ladder-rung1.md` Lemma 4 is false as written.** It claims "All
16 states reach, within at most 3 steps, the single 2-cycle". Exhaustive
enumeration of the map `(U,V) |-> (W,U)`, `W = (u1 XOR (u0 OR v0), u0 XOR (u1 OR v1))`
gives **two** cycles: the stated 2-cycle `((1,1),(0,0)) <-> ((0,0),(1,1))`, and
the fixed point `((0,0),(0,0))`. The repair holds, since the extra cycle is
all-zero columns and rows 25/26 exclude it, but the wording must change from
"the single 2-cycle" to "the single 2-cycle, plus the all-zero fixed point,
which rows 25/26 exclude." *(P)*

**2.2 `PATH.md` R9's stated obstruction is wrong.** R9 says Tseitin transfer is
blocked because "this instance is satisfiable with a unique solution". Deriving
`{c_n}` from `F_n` and refuting `F_n and {not c_n}` differ by one resolution
step in both directions, and the stored probe's instance is UNSAT by design.
Satisfiability is not the operative obstruction. *(P)*

**2.3 `PATH.md` R9's target metric is unreachable, not merely unproved.** Every
resolution step of a light-cone derivation of `c_n` was machine-checked:
`floor(3n^2/2)` steps for Rule 30, `2*floor(n^2/2)` for Rule 90, `n = 4..128`,
`steps/n^2 = 1.5000` at every band. Since `|F_n| = Theta(n^2)`, derivation length
is `Theta(|F_n|)`, so a superlinear-in-formula-size bound is impossible on this
route. *(P)*

**2.4 `PATH.md` R8's claim "Rule 30 is outside all of them" is false.** Tal
arXiv:2604.10124v7 Theorem 3.2 has left permutativity alone as its structural
hypothesis, which Rule 30 satisfies. What blocks it is obstruction E (it needs
an ergodic invariant measure supplied in advance and concludes a.e.), not
structure. Also: "Pivato's survey names the nonlinear case as an open gap" is
UNVERIFIED; the retrieved sections contain no numbered Question. Do not cite
one. *(A)*

**2.5 `PATH.md` 8.6's Jen 1986 dichotomy is weaker than stated.** It says
clause (ii) is load-bearing in both directions. That holds only under an
existential reading. Read universally — and Jen's own 1990 Prop. 3 uses the
identical phrase universally — excluding Rule 30 yields only "some finite IC
has no constant column", far weaker than row 25 in both quantifier and locus,
so row 25 stays novel either way. The inclusion horn is separately dead: rows
25 + 26 plus shift-invariance exclude any eventually constant column at any
index. Residual is priority exposure only. *(A, with clause (ii) itself P)*

Also: clause (ii) **was obtained**, contrary to 8.6's "unread". Springer's
article page returns the abstract through a text proxy even though the direct
fetch 303s and Semantic Scholar has it elided. Full text remains unobtained;
the retrieval route table is in `a11_jen1986/`. *(P)*

**2.6 `PATH.md` 0.1's column-blindness gate is scoped too broadly.** It reads
"moves by `O(1/W)` or less" with no qualifier. That binds normalised,
real-valued functionals only. An exact discrete invariant (e.g. a window
functional read mod 2, or a monoid-valued transfer quantity) is not caught by
it and can stay flat under a column-0 overwrite while still being unable to
decide P1/P2. Verified independently (a14's own `phi_w2_block11`, read mod 2,
does not decay where its normalised twin does). The correct gate for exact
invariants is a15's orbit-phase bound: any quantity computed as `f^t(m_0)` for
`f: M -> M` carries `<= log2|M|` bits about the whole orbit, independent of
window width. Suggested wording: append "**as a normalised functional; an
exact discrete invariant instead needs the orbit-phase bound (see a15,
`experiments/overnight-arms/frontier_attack/a15_nonabelian_invariant/`)**."
*(P)*

## 3. Proposed register delta

New rows, numbering continuing from 72:

| # | attempt | P | status | reason |
|---|---|---|---|---|
| 73 | Preimage-tree / backward-dynamics descent | 1 | **KILLED** | Column-blind at step 0; premise was a boundary confusion (row 60's branching is on `Z_N`, the orbit is finite-support on `Z` where the rule is injective); and the object is the pin restated. |
| 74 | Ore ladder uniformity by induction on rungs | 1 | **KILLED** | Theorem N: `G_n = sum_j x^(2^(nj))` has Ore order exactly `n` at height 1, so the ladder is strict at every level and no generic `S(n) => S(n+1)` exists. Row 46 stays OPEN; only the induction sub-route dies. |
| 75 | Stroboscopic descent for `p=2` | 1 | **OPEN**, no descent | Support grows exactly 2 per side under `F^2`, so no width-shaped quantity can decrease. Reduces to Lemma Z / row 1. |
| 76 | Row 41 `d`-uniform survivor invariant | 1 | **OPEN**, one bridge removed | Time-reindexing gives a parameter-free recurrence, but the natural truncation is vacuous by a light-cone argument, and pin parity is not shallow-local. |
| 77 | Ladder realizability / half-plane slip | 1 | **PROVED (limitation)** | The slip extends to a full half-plane: `plain_{R,k}(w)` nonempty for every `R`, `k`, `w`. The ladder can never return EMPTY in mode (i). Retires R7 mode (i) entirely. |
| 78 | P2 nontrivial density bounds | 2 | **KILLED** | Row 25's gap bound is linear in `t` (support radius is exactly `T`, the worst case), giving only `log2 T`; row 47 Theorem A already held that. |
| 79 | Orbit-closure patch census | 2 | **REFUTED (conditional)** | Checkerboard is a Rule 30 temporal fixed point (not Rule 90's); if it is in `Y`, R8's target fails. Proved for Rule 90 via Kummer; for Rule 30 conditional on unbounded patch growth, measured to `K=6` at `T=2e6`. |
| 80 | Rowland-Yassawi nonlinear analog | 2 | **NEGATIVE**, problem named | Arrow 1 of the R-Y chain is the only one consuming linearity, and solving it delivers only a simplex, since the nondegeneracy results need an aperiodic seed. |
| 81 | Resolution lower bound for `c_n` | 3 | **KILLED** | Metric mis-specified; see 2.2 and 2.3. |
| 82 | Trace subshift soficness | 1,2 | **NEGATIVE** | `Sigma_1` is the full shift for every left-permutive ECA, so the width-1 object fails the section 0 filter by construction. Reduced to `Sigma_2`; `>= 492` follower sets, a lower bound only. Implies nothing about P1 either way. |
| 83 | Conserved non-additive window functions | 1,2 | **KILLED** | Column-blind width-independently; exhaustive absence to `w=12` over `Z`, `Z/2`, `Z/3` as a byproduct; Rule 90 gives identical answers. |
| 84 | Jen 1986 provenance | infra | INFRA | Clause (ii) obtained, full text not. Mathematical dependency on the 1986 paper audited to zero across the tree. |
| 85 | Sub-quadratic derivation family for `c_n` | 3 | **KILLED** | R9's inverted kill did not fire. Best family is `n^2/2 + n` (rule 30) and `n^2/4 + n` (rule 90), exact for every even `n` in 2..200, and tree-optimal at `n=2,3` (rule 30) and `n=2,3,4` (rule 90); rule 30's `n=4` band walls at the 1500 s cap. `min_DAG <= min_tree`, so no shorter DAG derivation is excluded. That is 2.95x / 3.88x under the baseline but still `Theta(n^2)`. Block doubling was built and measured 3.9x-15x *worse*, refuting the rows 19-24 dyadic story by measurement. |
| 86 | Nonabelian conserved transfer invariant | 1,2 | **KILLED**, filter corrected | 1,988 real invariants found (survive the literal `O(1/W)` gate), then closed generally: any monoid-valued transfer quantity is a finite trajectory, `<= log2\|M\|` bits about the whole orbit. See correction 2.6. Rule 90's non-group invariants are the only column-sensitive ones in the family, and belong to the trivially-periodic rule. |
| 87 | Polynomial Calculus degree for `c_n` | 3 | **KILLED** | Degree is exactly 2 for Rule 30, 1 for Rule 90, both constant in `n`, both proved unconditionally. Separates the rules, but the gap is `deg(ANF)` read off the rule table (Rule 160 ties, Rule 128 beats Rule 30 despite a trivial column); ordering flips under the CNF encoding. Fails the Rule 90 filter honestly. |
| 88 | 2-adic Newton-polygon / valuation argument | 1 | **KILLED** | No closed functional equation exists for the centre-column generating function (the pin's nonlinear term is a Hadamard product, not a ring operation on `F(x)`); Newton-polygon machinery has no object. Corrects the parent brief: eventually-periodic 2-adic digits DO imply rationality, so P1 restates as "the centre-column 2-adic integer is irrational" — true, and empty. |
| 89 | Cryptanalytic bias detection on the lone-seed trace | none/empirical | **NO BIAS FOUND** | BM linear complexity profile, correlation attack, NIST SP 800-22, autocorrelation at all lags to `2^21`, Bonferroni-corrected over 100,838 tests: smallest adjusted p = 0.627. One apparent 5.42-sigma hit traced to a degenerate lattice-valued null and dismissed by the agent itself. Validation, not discovery — Wolfram and Len et al. already report this. |
| 90 | ML-guided conjecture mining | 1 | **REFUTED at depth 20000** | 30 candidates surviving the pre-registered threshold all break within 38 steps of the training boundary. Only extraction surviving exact out-of-range checking is the OR-latch pin (known). Best baseline: `NOT c_{t-1}` predicts `r_t` on the zero-set at 0.7493 out-of-range, matching logistic regression to many digits — a correlation number, not structure; does not touch a1's Lemma Z or a2's missing lemma. |

## 4. The one result that changes the ranking

**No proof of R1 can be rule-generic.** Rule 90's lone-seed centre column is
zero for all `t >= 1`, so its zero set is everything, and `r_t = 1` exactly when
`t = 2^j - 1` (Kummer). Gaps double forever, so `r` on the zero set is not
eventually periodic and R1's kill condition fires verbatim on the filter rule.
Verified to `T = 65536`: sixteen ones, all of the form `2^j - 1`, none missing.

R1 remains the best route and is not killed — the implication may still be true
for Rule 30 — but any argument reaching it through general left-permutive
reasoning is now refuted. Whatever proves R1 must consume the OR nonlinearity
directly.

Sharpening for section 4: decidability of `r` on the zero set and the truth of
R1's implication are logically independent in both directions, since Rule 90 has
the first and fails the second. R1's stated kill condition is therefore a weaker
trigger than its wording suggests.

## 5. Convergence

Three arms with disjoint encodings landed on the same obligation. a2's named
missing lemma (`s(t,1)` constant on the zero set of a 2-periodic trace), a7's
sharpened gap (`Diff_q` i.o. iff `col_1(t)=1` infinitely often where `col_0(t)=0`),
and a1's Lemma Z are the same statement, which is register row 1. That is
evidence the register's ranking is right, not that the route is close.

## 5b. A new obstruction for section 7.3: satisfiable-and-small

**I. The satisfiable-and-small ceiling.** Every P3 proof-complexity route in
this tree fixes the input to the lone seed, which makes the light-cone CNF
`F_n` SATISFIABLE with a UNIQUE solution and only `Theta(n^2)` clauses over an
input written in `Theta(log n)` bits. Three independent proof systems hit that
ceiling and nothing else: resolution derivation length is `Theta(|F_n|)` by
direct construction (a4, a13 — best family `n^2/2+n` for Rule 30, `n^2/4+n`
for Rule 90, both `Theta(n^2)`, both proved by exhaustive machine-checked
derivation, not estimate); Polynomial Calculus refutation degree is exactly 2
for Rule 30 and 1 for Rule 90, CONSTANT in `n` (a16, proved both directions).
Every one of the standard hardness techniques cited across a4/a13/a16
(Ben-Sasson-Wigderson, Dantchev-Riis, Hastad-Risse, Impagliazzo-Pudlak-Sgall,
Alekhnovich-Razborov's design method) is stated for REFUTATION of an
UNSATISFIABLE instance; none of the three arms located a satisfiable-instance
derivation-length lower-bound technique in the literature, and a4 reports that
search as negative rather than merely unattempted.
First recorded here 2026-08-30, from the convergence of a4, a13 and a16.
Predicts, and is the reason not to spend further compute on: Sum-of-Squares,
cutting planes, or any other proof system applied the same way — each would
need to certify hardness of a formula that a competing construction in the
same family already derives in `Theta(n^2)` steps at constant degree, so
either the new system also collapses to the `Theta(n^2)` ceiling (informative
only as a fourth confirmation) or it would first have to explain why its
measure escapes a bound the other three could not, which none of the three
found a route to.
Kills or bounds: rows 9, 81, 85 (this document's numbering), 87. Explicitly
does NOT bound: any P3 route that varies the input (obstruction G's territory,
the opposite failure mode) or any route abandoning derivation length for a
genuinely different complexity notion not yet tried against this ceiling.

## 6. Errors in the parent session's briefs

Recorded so they are not repeated.

1. **a10's object was degenerate.** The width-1 trace subshift over all
   configurations is the full shift for every left-permutive ECA (verified: all
   256 length-8 words realized by rules 30, 45, 60, 75, 90, 105, 150; rule 110
   gives 179, rule 22 gives 161). Rule 30 and Rule 90 agree, so it fails the
   section 0 filter by construction.
2. **"Gillman-Kopra" does not exist.** The author is R. H. Gilman, one L, ETDS
   1987. Passed through from memory without checking, which is the failure mode
   8.6 records for the fabricated Grassberger citation.
3. **Proposition 3 was attributed to Jen 1986.** It is Jen 1990.
4. **a1's step-0 kill was mis-aimed.** Row 38's pair disagrees only at `c_t = 1`,
   where the pin absorbs it, so it could not have fired the kill condition.
5. **a17's brief asserted the wrong direction on 2-adic rationality.** It warned
   the agent that eventually-periodic 2-adic digits do NOT imply rationality,
   "unlike the real case." That is backwards; they do (verified independently:
   `(110)^inf` reconstructs to exactly `-3/7`, whose digit expansion recomputes
   to `1,1,0` repeating). The agent caught and corrected it rather than
   propagating it.

## 7. Second wave, 2026-08-30: seven `a22_*` arms against the named open avenues

Seven parallel arms, one per the seven avenues named open after the first
sweep (R1's lone-orbit gap, R8's checkerboard growth, row 46's
specific-sequence question, row 41's alternative strategy, row 82's
soficness push, R7's mode (ii), and a Tier-3 literature check on succinct
circuit complexity of `n -> c_n`). **No prize problem moved, no proof, no
new kill-grade obstruction.** Every arm reached a stated, independently
spot-checked endpoint. Verification column as in §1: **P** = parent
reproduced the load-bearing number independently; **A** = agent-reported,
re-run/spot-checked but not independently re-derived from scratch.

| arm | target | verdict | V |
|---|---|---|---|
| a22_r1_lone_orbit | R1, lone-seed orbit vs ensemble `eps_30(m)` (row 1 / obstruction E) | NEGATIVE, estimator artifact explained | P |
| a22_p2_checkerboard_growth | R8, checkerboard patch growth (row 8 / row 79) | INCONCLUSIVE, consistent with a3 | P |
| a22_row46_specific_uniformity | row 46, A051023-specific Ore-height route | CLEAN DEAD END | A |
| a22_row41_alt_strategy | row 41, alternating-fiber alternative strategy | NEGATIVE, no new exclusion; one unproved reframing (Lemma S') | A |
| a22_row82_soficness_push | row 82 / a10, `Sigma_2` soficness push | NO TRACTION | A |
| a22_r7_mode2 | R7 mode (ii), the untested inclusion mode | NO TRACTION, replicates a7 at smaller scale | A |
| a22_p3_succinct_index | Tier-3, succinct circuit complexity of `n -> c_n` | GENUINELY OPEN, no prior work transfers | A |

**a22_r1_lone_orbit is the one arm worth reading in full.** It built a
held-out majority-vote predictor of `r_t` from width-`m` windows of the
*actual* lone-seed centre trace (`T=1,000,000`, TRAIN/TEST split at
`T/2`, cross-checked against `common.rule30.center_column_bits`) and
compared its test error against a21's ensemble `eps_30(m)` values, with a
block-level one-sample t-test (30 contiguous test blocks, since the trace
is one autocorrelated sequence, not i.i.d. draws) and a matched i.i.d.
control (1,000,000 independent left-supported rows, one `(window, r_t)`
sample per row per `m`) to separate orbit structure from estimator bias.
Verified independently from `orbit_eps_output.txt`, then re-verified with
two follow-up checks after the parent session flagged the first pass's
Bonferroni wording as self-contradictory (`GAP_CLOSEOUT.md`, same
directory). One cell (m=12, all-t) initially read as a surviving,
unexplained anomaly (`p=0.0021` against `alpha/22=0.00227`, with its
matched control at K=1,000,000 showing no deviation, `p=0.57`); a
follow-up i.i.d.-ensemble-only rerun at K=2,000,000 (same seed) made the
apparent anomaly far more extreme (`p=1.5e-8`), but a second rerun at the
same K with an **independent RNG seed** returned to no deviation
(`p=0.55`). Two of three realizations show nothing; the pattern is ordinary
sampling variability at m=12's bin-count regime (4096 bins), not a
reproducible effect, and the m=12 anomaly is retracted. m=14 and m=16, by
contrast, show the same large deviation in every realization tested
(both seeds, both restrictions, and in the ensemble control with no orbit
involved at all) and carry the sparse-bin overfitting signature named
originally (train_err far below `eps_30(m)`, test_err far above it; `2^16`
bins against ~500,000-1,000,000 draws). Separately, the zero-set
restriction's use of the same (unconditional) `eps_30(m)` as its
reference — flagged as an unchecked assumption — is now verified correct:
`c_t` is exactly independent of `(gamma, r_t)` in the i.i.d. ensemble (by
the standard left-permutivity fresh-bit argument, confirmed empirically to
5 significant figures and by a matched zero-set control tracking the
unrestricted one at every `m`). A structurally independent re-derivation
of `eps_30(m)` itself (array-based, not a3/a21's bitmask-packing method)
exact-matches every value `m=1..16` to 12 significant figures — closing a
real hole in a21's own pipeline, whose cross-check against direct
enumeration silently no-ops for `m>=11`, meaning `eps_30(12/14/16)` had
never actually been independently verified before this check.
**Conclusion, now on firmer footing: at every window width where the
comparison is trustworthy, the lone-seed orbit's window-conditional error
is statistically indistinguishable from the ensemble value; no cell —
including the one originally flagged as an outlier — survives a proper
replication check as real signal.** Does not resolve obstruction E — the
open question (does `eps_30(m)>0`, proved on the ensemble, hold on the
lone orbit specifically) stays open — but is the first direct empirical
probe of it, and finds no evidence against the ensemble value transferring.
`T` is capped near `10^6` by the `O(T^2)` simulator (P3-irreducibility
biting directly on the probe itself); pushing further needs either more
compute or a genuinely different (non-simulation) technique.

**a22_p2_checkerboard_growth extended a3's horizon 2x (`T=2e6 -> 4e6`,
`WMAX` 8->15) and ran a structural defect-propagation probe.** Diagonal
patch height `K`: `all_zeros` 4->5, `checker_A` 6->6 (flat, same
witness `t=196745`, no new occurrence), `checker_B` 5->6. One doubling
cannot distinguish "still growing, flat this step" from "bounded" — a3's
own series already had comparable flat stretches before jumping, and this
arm's numbers stay inside the same small-integer deviation band from the
exact Bernoulli reference (`height - H*` in `[-2,+2]` for checker_A) that
a3 reported. Separately, a direct experiment on the Rule 30 local update
near an infinite checkerboard found single-site defects never heal (0/300
trials healed within 60 steps) and grow with no sign of saturation (one
long trial: width 1 at t=0 to 196 at t=300, roughly linear, well under
light-cone speed). This rules out the simplest rescue mechanism (a bounded
defect "soliton" that could seed a forbidden-patch exclusion lemma) but
says nothing about the lone-seed diagram specifically. **Net: consistent
with, not a rescue of, a3/row 79's conditional REFUTED verdict for R8.**
One important correction, caught by the agent and not the dispatch brief:
growing `K` with the horizon is evidence the checkerboard *is* in `Y`
(patches recur at arbitrarily large `t`), which is what refutes R8's
sufficient target — the opposite of what this arm's dispatch prompt
assumed. a3's own document already states this correctly; only the
relaying prompt had it backwards, and no committed material was affected.

**a22_row46_specific_uniformity: clean dead end, two independent
obstructions, neither computational.** (1) Any sequence-specific Ore
bound `H(k)` for A051023, however tight, is still `k`-indexed, and
"finite-dimensional 2-kernel span" is one of the standard *definitions*
of automaticity — so bounding order without bounding `k` is circular
against P1 itself; a20's own exclusion table (32,000 terms excludes only
`k<=7`; Wolfram's `10^9`-bit check excludes only `k<=20`) shows tightening
the constant only moves those numbers, never terminates the ladder. (2)
Index mismatch: the OR-latch pin is additive-in-`t`, cross-column; the ANF
degree law `deg f_t = 2t-1` is about seed-bit dependence at fixed `t`;
Bridy's mechanism needs degree growth under `x -> x^{2^i}`, multiplicative-
in-`t`, single-sequence. Neither Rule-30 fact has the index structure
Bridy's machinery needs. Row 46 stays OPEN; this arm adds no new
obligation and names `docs/rule30/ARM6-binary-kernel.md`'s
kernel-element-distinctness route (already open, `k`-free) as the correct
next thread for anyone continuing specific-sequence work.

**a22_row41_alt_strategy: negative, but with one live, unproved
reframing.** Verified independently (`bilinear_decomp_check.py`, 8,792
checks at kseed=10, 0 mismatches, re-run by the parent): the survivor
quantity decomposes as `parity(o) = parity(u) XOR parity(v) XOR
corr(u,v)`, where `corr(u,v) = XOR_m (u[m] AND v[m])` carries all the
Rule-30-specific content (`parity(u)`, `parity(v)` alone are Rule-90-blind,
per a5 §6). A naive generating-function rescue of a5's killed truncation
strategy is a known dead end (Hadamard-product, not ring-operation,
structure). The one new object is **Lemma S'**: reframe a5's killed
Lemma S (bounded raw-window determinism) as bounded-*register*
determinism maintained online, which a5's tail-sensitivity witnesses do
not automatically refute (a streaming register can fold in a tail bit's
contribution at emission time rather than needing a later window) —
**stated, not proved**, and the concrete obstacle it must clear is named
(`corr` is recomputed fresh over the whole window at every `T`, not
append-only). Row 41 stays OPEN.

**a22_row82_soficness_push: no traction.** Confirmed a10's object is
still genuinely open (`Sigma_2(W30)` soficness undetermined, `>=492`
follower sets stands as a lower bound only). Attempted a10's own named
next step (extend the exact language census to `N=16` to test the
strongest `|y|=3` pumped candidate at `j=4`); the run did not complete in
budget and was killed with zero output. The structural route (an
inductive separation argument via the OR-latch pin's rightward-
extendability recursion) was scoped but not attempted — real open math,
not producible in this budget. Nothing in a10 modified or re-verified.

**a22_r7_mode2: no traction, replicates a7 at smaller scale.** a7's own
rung-1 sweep already tested mode (ii)'s underlying question for `p=2`
(the `col_{-1}` eventual-periodicity check on ladder witnesses) far more
thoroughly than this arm's budget allowed (T up to 50,000 vs. this arm's
T=4,000 after an O(T^2) `build()` stalled at T=400,000 and was killed).
The cheap replacement run found no eventual period `<=256` for `col_{-1}`
at any tested depth `k in {1,2,4,8,16}` — flat, matching a7's own finding,
adding no new evidence either for or against inclusion. Genuinely
extending this needs an `O(T log T)` or vectorized `build()`, out of
scope here.

**a22_p3_succinct_index: genuinely open, no computation run (by design,
literature-only scope).** Citation check for the succinct/positional
circuit complexity of `n -> c_n` (`n` as genuine binary input, distinct
from every P3 arm in this tree, which fixed the input to the lone seed
and varied only the label `t`, obstruction G's territory). No exact prior
work found. The closest hit, verified directly from its arXiv abstract
page — **Eppstein, "The Complexity of Iterated Reversible Computation,"
arXiv:2112.11607, TheoretiCS vol. 2 (2023) article 10** — proves the
general succinct-iteration question (`f^(n)(x)` from binary `n`) is
FP^PSPACE-complete, but only for `f` a *bijection*; Rule 30 is
non-injective (up to 4 preimages, per PATH.md 8.4), so it falls outside
the hypothesis entirely. `docs/rule30/PATH.md` 8.7's "structurally dead"
verdict for circuit lower bounds on the centre column is about
*non-uniform* complexity of a fixed sequence (one hardwired circuit per
`n`), a different object from the *uniform* succinct-index question asked
here — the register does not currently draw that distinction anywhere.
Trivial upper bound noted (not run): the `O(n^2)` row-simulation gives a
`P`-uniform, `O(n^{1+o(1)})`-size circuit family for `n -> c_n` via
standard TM-to-circuit simulation. No first probe was executed, per this
arm's literature-only scope.

## 8. Fence

All agent writes stayed inside their own subdirectories. Disclosed exceptions,
all of the kind register row 70 records: `__pycache__` `.pyc` files regenerated
by mandated read-only imports under `common/`, `p_geometric_attack/` and
`proof-complexity/`. No source file was modified, nothing was committed.

One genuine out-of-fence write: a nested research subagent wrote
`~/.claude/agent-memory/researcher/rule30_trace_prior_art.md`. It is the
researcher persona's own memory store rather than repo state. Its header claims
all entries were read from PDFs on disk, which is false for the thesis entries;
do not trust that header.

One false claim to note: a11 reported updating memory files that were never
written.

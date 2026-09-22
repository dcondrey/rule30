# Audit: wryan2986/rule30-lab, "all-one-tail exclusion" claim

**Verdict: the narrow claim holds and is correctly proved, but its novelty is
marginal, and the repo itself does not claim otherwise.** The theorem is an
almost-immediate corollary of Erica Jen's 1986/1990 "at most one temporal
column can be eventually periodic" result — the same fact Wolfram's own 2019
prize announcement cites — plus two lines of Rule-30-specific Boolean
algebra. `docs/research_status.md:194` attributes the contradiction to
"Kopra's Corollary 3.7 (equivalently the applicable Jen result)" and files
the whole thing under `partial-proof`, defined in
`docs/experiment_protocol.md:9` as "a rigorous argument proving less than the
full target." The repo asserts no novelty for this step; this audit finds
none beyond the short bootstrap itself. The repo's million-bit
center-column reproduction is independently verified byte-for-byte against
this repo's own trusted generator. No overclaim was found in the specific
partial-proof record; the repo's broader README/status language is
unusually careful about not claiming more.

Assessed 2026-09-13. Repository fetched via `git clone --depth 1
https://github.com/wryan2986/rule30-lab.git`, HEAD commit at clone time by
`wryan2986 <152133950+wryan2986@users.noreply.github.com>`, dated
2026-08-02.

## What "all-one-tail exclusion" actually is

The name does appear verbatim (`README.md:13`, "the explicitly scoped
all-one-tail exclusion is currently classified as a `partial-proof`";
`docs/adversarial_review.md:193`, "the partial all-one-tail theorem"), but it
undersells the theorem it names: the actual proof excludes an eventually
all-**zero** center tail as well as all-one, and the repo's own proof file
correctly calls it **period-one exclusion**, filed under
`docs/research_status.md`'s "Partial mathematical results" section as
`partial-proof`. The proof is in
`proofs/informal/problem1_period_one_exclusion.md`, cross-checked against
`docs/theory_literature_review.md` lines 105-220, and the two Boolean-algebra
deductions are additionally machine-checked in
`proofs/lean/Rule30.lean` (theorems `true_center_true_next_forces_left_false`,
`consecutive_true_values_force_adjacent_left_false`,
`true_tail_forces_adjacent_left_false_tail`,
`false_left_tail_true_right_persists`; no `sorry`, no axioms).

**Exact claim.** For Rule 30 started from any nonzero finite-support initial
configuration (in particular the single-black-cell seed), the fixed center
column cannot be *eventually constant* — neither eventually all-1 nor
eventually all-0 — for any finite onset time. Equivalently: the center
column cannot have eventual period 1.

**Method: elementary local Boolean algebra plus one external published
theorem cited as a black box, not exhaustive search.**

1. If `c(t)=1` for all `t>=T`, the Rule 30 identity at the center,
   `c(t+1) = left(t) XOR (c(t) OR right(t))`, forces `1 = left(t) XOR 1`, so
   `left(t)=0` for all `t>=T`. The adjacent width-two trace on `[-1,0]`
   becomes the constant pair `(0,1)` from `T` onward.
2. If `c(t)=0` for all `t>=T`, applying the Rule 30 identity one cell to the
   right gives `right(t+1) = right(t) OR right2(t)`, a monotone-nondecreasing
   Boolean recurrence, hence eventually constant. The adjacent trace on
   `[0,1]` becomes eventually `(0,0)` or `(0,1)`.
3. Both outcomes make some fixed adjacent width-two trace eventually
   periodic. This is asserted to contradict **Kopra's Corollary 3.7**
   (Johan Kopra, "Rapid Left Expansivity, a Commonality between Wolfram's
   Rule 30 and Powers of p/q," *Theoretical Computer Science* 946 (2023),
   113668), which the repo paraphrases as: if a binary ECA is left permutive
   and left spreading (local rule maps `001->1`) and the initial
   configuration is nonzero and eventually zero to the left, then no
   adjacent width-two trace is eventually periodic. Rule 30 satisfies both
   hypotheses (`f(a,b,c)=a XOR (b OR c)` is bijective in `a`; `f(0,0,1)=1`).

No exhaustive search, SAT/SMT solver, or statistical argument is involved in
the proof itself; those techniques appear elsewhere in the repo for
*regression checks* on adjacent finite claims (see below), which the repo
correctly labels as evidence, not proof.

## Verifying the load-bearing external citation

The one place this claim could break is misapplication of Kopra's theorem —
exactly the failure mode this repo's own
`AUDIT-adjacent-research-targets.md` (item 6) already flags for a different
paper: "Kopra's rapidly left expansive framework includes Rule 30 and
fractional multiplication automata, but also Rule 90. The latter has an
eventually periodic singleton center trace." Rule 90 (`f(a,b,c)=a XOR c`) is
also left permutive and also left spreading (`f(0,0,1)=1`), and its
single-cell-seed center column is `1,0,0,0,...` (odd only when `C(2t,t)` is
odd, i.e. `t=0`, by Kummer's theorem) — eventually constant zero. If Kopra's
Corollary 3.7 covered width-1 traces, Rule 90 would refute it outright, and
by extension would refute the wryan2986 repo's use of the corollary as a
contradiction source.

Checked directly against Kopra's arXiv preprint (2202.13809, the preprint
form of the TCS paper, same theorem under the number 3.5 there): the theorem
is stated for adjacent traces of **width `w`**, not width 1, and the paper
explicitly discusses Rule 90 as the reason the class cannot be strengthened
to a width-1 guarantee — Rule 90 "produces a single eventually periodic
column starting from the configuration with a single 1 at the origin," at
width 1, which the corollary never claims to cover. Rule 30 and Rule 90 are
both in scope of the width-2 non-periodicity theorem and both genuinely
satisfy it; the wryan2986 argument's citation is accurate, and the repo's
own bootstrap step (width-1 eventual constancy implies an adjacent width-2
trace is eventually periodic) is exactly the step that turns a known width-2
theorem into a width-1 corollary. (One notation note: the researcher
subagent that read Kopra's arXiv preprint reported the initial-condition
hypothesis as `N(Sigma)`, where the repo and `theory_literature_review.md`
write `L_0(Sigma_2)`; both denote configurations that are nonzero and
eventually zero to the left, and the single-cell seed lies in either, but the
two names were not independently reconciled against the same document
revision here.) Independent literature check (Jen,
"Aperiodicity in One-Dimensional Cellular Automata," *Physica D* 45 (1990),
Proposition 3, and Kopra's PhD thesis Theorem 3.1.12 / 2023 paper's own
open-problem list) found no prior published statement of this specific
period-one exclusion for Rule 30's center column; Jen's and Kopra's
published results state only "at most one width-2 trace can be periodic" and
list the single-column question as open. So this is small but genuinely new:
a two-line bootstrap from a cited 2023 (resp. 1986/1990) width-2 theorem to
an unpublished width-1 corollary, not a restatement of settled prior art and
not an exhaustive-search overclaim.

Wolfram's own 2019 announcement (fetched directly) states only the
two-column (Jen 1986) fact — "no two columns can both become periodic" — and
explicitly says "there's no known way to extend the argument to a single
column," with no separate acknowledgment that period-1 is excluded.

**How thin the gap actually is.** Jen's theorem, as Wolfram phrases it, is
about *any* pair of columns, not specifically an adjacent width-two trace:
"no two columns can both become periodic." Given that phrasing, the whole
wryan2986 argument collapses to two lines, with no need for Kopra's 2023
paper, width-two traces, or adjacency at all:

1. If the center is eventually all-1, the Rule 30 identity forces the
   left-neighbor column to be eventually all-0. Both are eventually periodic
   (period 1) columns — contradicting "no two columns can both become
   periodic."
2. If the center is eventually all-0, the right-neighbor column obeys the
   monotone recurrence `right(t+1) = right(t) OR right2(t)` and is therefore
   eventually constant. Center and right-neighbor are again two eventually
   periodic columns — same contradiction.

This is exactly the repo's argument; Kopra's Corollary 3.7 is a modern,
width-generalized restatement of the same 1986/1990 fact and is not
load-bearing here. The repo's own citation already says as much
(`docs/research_status.md:194`: "contradicting Kopra's Corollary 3.7
(equivalently the applicable Jen result)").

**Classification: closer to (b) than (a).** The claim is correct and the two
elementary deductions are genuine (independently checked in Lean without
axioms), but the step from "no two columns both eventually periodic" to
"the center cannot itself be eventually period-1" is a short, almost
mechanical corollary of a nearly 40-year-old theorem that Wolfram's own prize
announcement already cites. No source found here (Jen 1990, Kopra 2023 or
his PhD thesis, Wolfram's page) states this specific corollary in print, so
it is not a restatement of an already-published result, but the distance
from the cited theorem to this corollary is small enough that the repo is
right not to claim more than `partial-proof`, and this audit does not
consider it a substantial new result. It is explicitly *not*
general-purpose: the repo's own scope note is exact — "this deduction does
not generalize automatically to a period-`p` center with `p>=2`. For a zero
center tail the right-neighbor update becomes a monotone OR recurrence; a
nonconstant periodic center reintroduces the XOR term and destroys that
monotonicity." That caveat is correct: the argument does not extend to
period 2, because a period-2 center is not eventually constant and the
OR-monotonicity trick used in the `c(t)=0` case only fires when `c(t)` is
constant.

## Adjacent finite-search claims: correctly scoped, not the load-bearing part

The bulk of `docs/research_status.md`'s "Finite exhaustive results" section
(complete-tail campaigns, period-defect campaigns, two-adic diagonal
quotient checks, DFAO/recurrence/affine-model fits) is exhaustive search over
small finite boxes, and every one of these entries is phrased with an
explicit "this excludes only this finite [class/quotient/width], not a
statement about all [widths/periods/prefixes]" qualifier in the same
sentence or the sentence immediately following. This matches this repo's own
convention of never letting a finite check masquerade as an infinite
statement. None of these finite results is used as a premise in the
period-one theorem; the theorem is closed under the three-step Boolean
argument plus the one external citation, independent of any bounded search.

## Million-bit center-column reproduction: independently reproduced here

`docs/research_status.md` claims: for `c_0..c_999999`, Python and C++ AVX2
independently produced a 1,000,000-byte file with SHA-256
`6fc1e4e2abfb382255b94955467f259be88c1044d09ec361c5039970985a1669`,
500,768 ones, 499,232 zeros, `D(1,000,000)=1,536`, and checkpoint values
`D(100)=4`, `D(1,000)=-38`, `D(10,000)=64`, `D(100,000)=196`.

Computed here against this repo's own generator
(`/Volumes/A/researchpapers/13-rule30/experiments/rule30/center_column.py`):

```
n=100     ones=52     zeros=48     D=4
n=1000    ones=481    zeros=519    D=-38
n=10000   ones=5032   zeros=4968   D=64
n=100000  ones=50098  zeros=49902  D=196
n=1000000 ones=500768 zeros=499232 D=1536
sha256(byte-per-bit, one byte per cell) =
  6fc1e4e2abfb382255b94955467f259be88c1044d09ec361c5039970985a1669
```

Every checkpoint and the SHA-256 hash match exactly. This is a full,
independent, byte-level reproduction of the claimed dataset using a
generator this repo already trusts (OEIS A051023 ground truth,
`experiments/rule30/center_column.py`), not a resampling or an approximate
check.

## Relation to dcondrey/rule30 and Patto1155/rule30-foundry

Both were cloned for comparison. `dcondrey/rule30` (three files: README,
experiments/README, `.bestpractices.json`) is a stub, not yet a comparable
multi-backend effort; it shows no structural overlap with wryan2986/rule30-lab
beyond the shared subject and the P1/P2/P3 naming convention that traces back
to Wolfram's own announcement.

`Patto1155/rule30-foundry` is structurally the closer analog: independently
targets Rule 30 with a large experiment/data/tools tree, its own claim ledger
(`docs/CLAIM_LEDGER.md`), agent-loop tooling, and dozens of named finite
experiments (coarse-graining, autocorrelation, block frequency, DFAO search,
linear complexity, and similar). **Git history shows a different author**:
every commit is by `Patto1155 <paddymellon3000@gmail.com>`, not David
Condrey — the task framing that this is one of "David Condrey's related
projects" is not supported by the clone's own commit log; it may be a
different person's independent project, a collaborator, or an account the
task's framing conflated, but the repository content itself does not attest
authorship by David Condrey. Given the observed clone, that also holds for
`wryan2986/rule30-lab`, single-author `wryan2986`.

Beyond shared subject matter, the P1/P2/P3-named, multi-backend,
claim-ledger structure recurring across `rule30-lab`,
`Patto1155/rule30-foundry`, and this repo's own `13-rule30/` tree is common
for this kind of project once Wolfram's own problem statements and the
existing convention of "finite check != infinite proof" are taken as given;
it is not by itself evidence that any one repo was derived from another, and
no textual, commit-history, or file-naming match beyond the shared domain
vocabulary was found between wryan2986/rule30-lab and either
dcondrey/rule30 or Patto1155/rule30-foundry.

## Summary table

| Claim | Verdict |
|---|---|
| Period-one exclusion for Rule 30 center column | correct; closer to (b) than (a) — a short, almost mechanical corollary of Jen's 1986/1990 "no two columns both periodic" theorem, which Wolfram's own announcement already cites; not found stated in print in this exact corollary form, but the repo claims only `partial-proof` and attributes it to Jen/Kopra, not to itself |
| Method | elementary Boolean deduction (Lean-checked, no axioms) + correctly cited, correctly applied external theorem (Jen 1986-90, restated by Kopra 2023 Cor. 3.7); no exhaustive search in the proof itself |
| Scope discipline | correct: repo explicitly limits the result to period 1, states the period->=2 obstruction, and does not claim Problem 1 |
| Million-bit reproduction | independently reproduced here, exact byte-for-byte SHA-256 and checkpoint match |
| Finite exhaustive-search sections | correctly scoped as finite-only in the same breath, not used as a premise in the theorem |
| Overlap with dcondrey/rule30 | none beyond shared subject; dcondrey/rule30 is a stub |
| Overlap with Patto1155/rule30-foundry | structurally similar (P1/P2/P3, multi-experiment, claim-ledger pattern), commit history shows a different author than David Condrey; no evidence of derivation either way |

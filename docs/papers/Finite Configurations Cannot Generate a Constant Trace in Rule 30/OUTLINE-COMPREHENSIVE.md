# Comprehensive paper: architecture and build plan

Date: 2026-09-05.  This is the plan for the "single paper with everything,
including the failed experiments" the user asked for.  It is a build plan, not
the paper.  Nothing here is committed or published.

## The honest framing (read first)

The corpus is one proven publishable theorem, two mechanized limitation
results, one unproven structural lead, and 94 killed attack routes across
170 result documents.  A paper that dumps all 170 is a lab archive, not a
paper, and would bury the real results.  A paper that hides the failures throws
away the one thing the field genuinely lacks.

The resolution, and the spine of this plan: **the failures are the
contribution, once organized.**  Nobody has published a map of what fails on
Rule 30's center-column problem and why.  We have that map — nine obstruction
classes, each with an exact kill reason, unified by a single fact (Rule 30's OR
nonlinearity is the only thing separating it from Rule 90, and every failed
route either used a property Rule 90 shares or hit one of nine walls).  Turned
into a *register*, the 94 failures become a citable methods contribution.

So the paper leads with what is proven, states honestly what is not, and makes
the negative results rigorous rather than exhaustive-verbatim.

**Title (working):** *Structure and Obstructions in the Rule 30
Eventual-Periodicity Problem.*
**One-line positioning:** we settle eventual period one for all finite
configurations, delimit the period-two problem with a mechanized ladder and an
exhaustive forced-continuation census, and give the first structured register
of the attacks that fail, unified by the Rule 90 filter.

**Calibration, stated in the abstract and never violated:** Wolfram Problems 1,
2, 3 remain open.  Nothing here claims otherwise.  The period-two structural
finding is a conjecture supported by exhaustive small-n data, labeled as such
everywhere.

---

## Structure

### Part I — The eventual-period-one theorem (PROVEN; already written)

Lift `zero-tail-note.tex` almost verbatim.  This is the paper's anchor: a
complete, refereed-quality settlement of eventual period one for every nonzero
finite configuration, strictly broader than the lone seed.

* Theorem (zero-trace fiber), Theorem (all-one fiber), the two sharp horizons,
  the no-eventually-constant-column corollary.  Sources: `zero-tail-note.tex`,
  `RESULTS-zero-tail.md`, `RESULTS-right-cone.md`, `RESULTS-eventual-period.md`.
* The Rule 90 contrast is introduced here for the first time and becomes the
  organizing thread of the whole paper: the OR latch is what makes it work, and
  its absence is why Rule 90's center column *is* eventually periodic.
* ~7 pp.  Already exists; integration cost is low.

### Part II — The period-two problem: reduction, census, and a structural lead

The heart of the new material.  Honestly split into proven / measured /
conjectured.

1. **The reduction chain (PROVEN implications).**  `PT2 <= RW <=> DLP => SEP`,
   every arrow a proved uniform implication; only the terminal separator (SEP)
   is open.  So `gamma(n) >= 1 for all n` would imply the first per-period
   exclusion theorem for this column.  Source: `PROOF-STATE-CAPSULE.md` traced
   to its proof files.
2. **The forced-continuation census (MEASURED, exhaustive).**  `|H_r(n)| = 0`
   exhaustively to `n=24`, RW UNSAT by SAT to `n=28`, `gamma(n)` to `n=30`.
   `gamma` fluctuates in `[7,14]`, no trend (the even-n "climb" was an artifact,
   retracted).  Sources: `RESULTS-KSTAR-GAMMA-EXTENDED.md`, `BACKLOG.md` §12.
3. **The structural lead (CONJECTURE + EVIDENCE).**  Near extinction the census
   collapses onto `O(1)` extremal forcing states sharing a long suffix and one
   killer symbol; within a class the whole live state is identical.  Robust to
   the hard-core restriction (clean periodic extremals there).  The suffix
   lemma and the OR-collapse `FORWARD[2]==FORWARD[3]` are proved.  Labeled a
   conjecture, verified exhaustively to `n<=18/21`.  Source:
   `RESULTS-TERMINAL-CLASS-ARCHAEOLOGY.md`.
4. **Why the cheap routes cannot close it (PROVEN negative).**  First-moment /
   transfer-matrix / spectral bounds fail: the hard-core spectral radius is
   exactly `phi = 1.618 > 1`, the bound is tight below `k_star` and off 300x at
   extinction.  Source: `MEMO-SPECTRAL-BOUND-CANNOT-CLOSE.md`,
   `MEMO-PHI-OVER-4-FIRST-MOMENT.md`.
* ~9 pp.

### Part III — The R7 periodicity ladder and its limits (PROVEN limitation theorems)

The mechanized side, all honest limitation results.

1. Encoding: columns as omega-words, inverse transduction, Buchi periodicity.
   Calibration passes; the Rule 90 soundness control is built in.  Source:
   `RESULTS-ladder-rung0.md`.
2. Limitation theorems: verdict uniform in right depth `R` (rung 0), the pin is
   depth in disguise (rung 1 Cor. 2/3), constant in left depth `k` (this
   session; bisim classes exactly 15/20/32 over a 3,068x range), `Q` closed by
   `N_base`.  All three levers proved inert.  Sources: `RESULTS-ladder-rung1.md`,
   `RESULTS-R7-WITNESS-EXTENSION.md` §6.
3. The witness-extension test is an invalid instrument, proved by a Rule 90
   control (a genuine witness exists and is missed 4x).  Obstruction F (free
   boundary) and its left-hand analog.  Source: `RESULTS-R7-WITNESS-EXTENSION.md`.
* ~6 pp.

### Part IV — The register of obstructions (THE failed experiments, organized)

This is where "all our failed experiments" live, as science.  The novel
contribution.

1. **The Rule 90 filter** as the organizing principle: any argument that also
   applies to Rule 90 proves nothing, because Rule 90's center column is
   eventually periodic.  The one thing Rule 30 has that Rule 90 lacks is the OR
   nonlinearity (the pin).  Every proven result above routes through it; every
   failure below either ignored it or hit another wall.
2. **The nine obstruction classes A-I**, each: statement, the routes it killed,
   the kill-reason class (population / depth / boundary / measure / composition
   / single-column / arbitrary-input), and Rule 90 status.  Source:
   `PATH.md` §7.3, `FACT-INDEX.md`.
   * A. The `O(log t)` propagation wall (three independent representations).
     **Amended 2026-09-07:** the *rate* is a right light-cone fact.  With period
     `<= P` the left cone reaches depth `3,8,29,400,87867,>2.1e9` for
     `P = 2..64` (NKS p. 871), super-exponential in `log P`.  Same verdict,
     wrong rate on the left.  Source: `RESULTS-ordered-wedge-glide.md` 3.
   * B. The Rule 90 filter itself.
   * C. Single-column blindness (entropy/complexity boundary routes).
   * D. The missing composition law (P3 shortcuts).
   * E. The measure-zero single-orbit gap (P2 density routes).
   * F. The free boundary of a fixed-depth strip (the ladder).
   * G. Arbitrary-input measures vs a single fixed point (P3 complexity).
   * H. Finite certificates are lower bounds on a complexity function, never
     more (why no census closes an all-length theorem).
   * I. The light-cone CNF with `n` pinned (P3 circuit routes).
3. **The attempt register**, a compact table: 94 routes indexed to their
   obstruction, one line each with the kill reason.  Source: `PATH.md` §7.1
   rows 1-93 plus the period-2 prereg/memo kills.
3b. **The two light-cone frames** (`Remark rem:wedge`, added 2026-09-07).  Not a
   route and not a kill.  The ordered left region is prior art (NKS p. 871) and
   the remark says so; what it contributes is the recurrence pair that makes the
   asymmetry mechanical, the glide form of the left region's periodicity, the
   Rule 90 split, and the correction to A's rate.  It earns its place because it
   is the sharpest instance of the paper's unifying fact — the OR makes Rule 30
   two-phased, not merely hard — and because it carries a cautionary example of
   obstruction H that the paper is otherwise short of: a period-16 plateau that
   looks like a theorem until `j = 87,867`.
4. **The five prior sightings of the structural lead**, dropped each for a
   population-shaped reason — the methodological point that the population was
   never where the answer was.  Source: `RESULTS-TERMINAL-CLASS-ARCHAEOLOGY.md`.
* ~8-14 pp depending on the exhaustiveness dial (below).

### Part V — Scope, the unifying fact, and open problems

1. Honest scope: P1/P2/P3 open; what each proven result does and does not reach;
   the published state of the art (Kopra width-2, Jen, Rowland) and exactly how
   these results sit against it.
2. The unifying fact: the OR nonlinearity is the whole game.  A one-paragraph
   statement of why every route that avoids it is on the wrong side of the
   Rule 90 filter.
3. Concrete open leads, stated so they can be picked up: the extremal-state
   family across `n` (the untried comparison); the Rule 90 carry-kernel census
   control; the SEP separator.
* ~3 pp.

### Reproducibility

The full computational apparatus: the proven-result validators (already in the
note), the census/ladder/needle scripts, seeds, and the exact-agreement
cross-checks.  The Lean partial formalization of Part I.  ~2 pp.

---

## Two dials for the user to set

1. **Exhaustiveness of the register (Part IV.3).**
   * *Curated* (default): the 9 obstruction classes in prose + a one-line-per-
     route table of the ~93 PATH rows.  ~35 pp total.  Reads as a paper.
   * *Exhaustive*: every one of the 94 routes gets a short paragraph with its
     measurement.  ~55 pp.  Reads as a technical report / monograph.

2. **One file or main + compendium.**
   * *Single file* (default): everything in one document, register as Part IV.
   * *Main + compendium*: a tight ~20 pp main paper (Parts I-III, V) plus a
     separately-paginated "Compendium of failed attacks" (Part IV, exhaustive).
     Keeps the main paper citable and clean, preserves every failure.  This is
     the research-mode-preferred shape (validation visually separate from
     contribution) but is arguably two documents, not "single."

My recommendation: **single file, curated register** for a first complete
draft, because it is a real paper that a reviewer will read end to end, and the
register can be expanded to exhaustive later without restructuring.  The
existing proven note becomes Part I at near-zero cost, which de-risks the
largest block.

## DECIDED 2026-09-05 (three artifacts)

The user chose paper + supplement + Zenodo:

1. **Main paper** `rule30-obstructions.tex`: Parts I-V with the **curated**
   9-class register as Part IV.  The obstruction map is the contribution and
   stays in the paper.
2. **Supplement** `rule30-supplement.tex`: the **exhaustive** per-route register
   (94 routes, one paragraph each) plus detailed measurement tables.  Cited
   from the main paper.  This is the home for "all failed experiments" in full.
3. **Zenodo archive**: the computational corpus (scripts, logs, seeds, the 170
   result docs), a DOI cited in the reproducibility section.  Manifest prepared
   locally (`ZENODO-MANIFEST.md`); the deposit itself needs the user's account
   and explicit go-ahead, so it is not created autonomously.
4. **Wolfram Notebook Archive**: a WL companion notebook for the NKS audience.
   `rule30-companion.wls` is STAGED but UNRUN — the Wolfram Engine is not
   installed in this environment (`wolframscript` absent), so nothing in it is
   verified.  It covers the canonical `CellularAutomaton` visuals only; the
   census/needle WL port is a marked TODO to be written against a live kernel
   and cross-checked against the Python output.  Enabling: user installs the
   free Wolfram Engine and activates it with their Wolfram ID (interactive,
   theirs to do).  Venues: paper -> arXiv (math.DS/nlin.CG), corpus -> Zenodo,
   WL companion -> Notebook Archive.  None published without explicit go-ahead.

## What exists vs what must be written

* Part I: **exists** (`zero-tail-note.tex`), lift and renumber.
* Part II.1-2: exists as prose across capsule + gamma doc, needs assembly into
  theorem/measurement form.
* Part II.3-4: exists (`RESULTS-TERMINAL-CLASS-ARCHAEOLOGY.md`, the two memos),
  needs conversion to a labeled conjecture with an evidence table.
* Part III: exists (rung0/rung1/witness-extension), needs compression.
* Part IV: the register table exists in `PATH.md` §7.1/§7.3; needs transcription
  and per-row kill-reason classification (tonight's PATH-read agent did most of
  this).
* Part V: new prose, short.

## Risks to manage while drafting

* Do not let the register's 94 negatives drown Part I's proven theorem.  The
  abstract and intro must make the reader know within a page what is proven.
* Every "measured" number carries its `n`-range and what it does not control
  for.  The `n=28,c=2` gamma spike stays quarantined.
* The structural lead is a conjecture.  It never appears as a result.
* Rule 90 status is stated for every claim, proven and failed alike.
* No verbatim dumping: each failed route is a sentence with a reason, not a
  transcript.

## Build order (on greenlight)

1. [DONE 2026-09-05] `rule30-obstructions.tex` skeleton built and COMPILES
   (6 pp, exit 0, 0 unresolved refs). Contains: full preamble, comprehensive
   abstract, introduction, all five parts as real sections, Part I theorem
   statements, Part II reduction/census/lead/spectral as stated
   propositions+conjecture, Part III's three-lever + witness theorems stated,
   Part IV's nine obstruction classes A-I in prose, Part V scope prose, bib.
   Every substantive block carries a `% DRAFT:` marker naming its source doc.
2. [NEXT] Merge Part I proofs verbatim from `zero-tail-note.tex` (Lemma 1,
   Thm 2/3, Cor 4/5, Thm 6/7, Cor 8) + its two figures.
3. [NEXT] Draft Part IV register table: transcribe the 93 PATH sec-7.1 rows,
   one line each (route | problem | obstruction | kill reason), from the
   PATH-read agent's classification. This sets the paper's length.
4. Expand Parts II, III prose from the result docs (statements are already in).
5. Expand Part V; finalize intro/abstract once the body scope is fixed.
6. `rule30-supplement.tex`: exhaustive per-route compendium (94 paragraphs).
7. `ZENODO-MANIFEST.md`: archive file list + citation stub (deposit needs the
   user's account; not autonomous).

## Files created this session

* `OUTLINE-COMPREHENSIVE.md` (this file).
* `rule30-obstructions.tex` + `rule30-obstructions.pdf` (compiling skeleton).
* One-sentence edit to `zero-tail-note.tex` section 5 (see LEDGER).

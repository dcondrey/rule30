# Claim-level coverage: a screen, two failed detectors, and six extracted records

Date: 2026-09-16. `research_catalog.audit` reports coverage **file-level** and
says so in its own interpretation string: a file with one record counts as
covered however many claims it holds. This is the first pass at the question
below that, which sections of an already-covered file are held by no record.

Instrument: [screen_claim_coverage.py](../../screen_claim_coverage.py),
artifact [claim-coverage-screen.json](../../claim-coverage-screen.json).
The artifact is the regeneration at the end of the pass, over a catalog of
1,905 records: the six extracted below are in it and the record holding this
screen's own failed detectors is not. Its ranking is therefore already
post-extraction, and the two true positives sit at 253rd and 254th with five
records each. The screening ranks in section 2 are the pre-extraction ones
the reading audit started from, and the artifact no longer shows them.

**This is a screen over 493 covered files, of which three were read. It is not
a completeness certificate and the archive should not cite it as one.**

## 1. Two detectors were built and both failed

Recorded honestly because a failed detector that stays unrecorded gets rebuilt.

**A, claim markers.** A regex for `Theorem`, `Lemma`, `Claim`, `Conjecture`,
`VERIFIED`, `REFUTED`, `Status:`, `Verdict:` and the rest of this archive's own
vocabulary. Over 5,046 indexed sections, a marker appears in **37.4%** of the
1,522 sections that did receive a record and **36.4%** of the 3,524 that did
not. A discrimination of 0.010 is no discrimination at all: the marker says
nothing about whether a section was extracted.

**B, orphan measured figures.** Distinctive figures in a section that appear in
no catalog record, which is the shape of the one previously known gap. The
base rates are again close, 16.2% of recorded sections against 11.2% of
unrecorded ones, and worse, the ranking it produces is topped by per-row data
tables and witness bitstring listings. A record is correctly not expected to
hold a table cell by cell, so the instrument ranks precisely the sections that
should not be extracted.

**C, density.** Substantive sections per record, per file. Not a claim
detector either, and it does not pretend to be one: it says only where the
catalog is thinnest per unit of document. This is the ranking that shipped,
and its validation is the reading audit below rather than any statistic.

## 2. What reading the top of the ranking actually found

| screening rank | file | verdict | records |
|---|---|---|---|
| 2 / 492 | `RESULTS-p3-implicit-boundary-investigation.md` | **false positive** | 0 |
| 11 / 492 | `RESULTS-orbit-closure-diagnostic.md` | true positive | 4 |
| 123 / 492 | `RESULTS-p3-balanced-defect-normal-form.md` | true positive | 2 |

**Rank 2 is a false positive, and a persistent one.** That file is a synthesis
index over roughly 35 linked `RESULTS-p3-*.md` reports. Ten of its twelve
strongest claims are already held by records anchored at those reports, which
is correct practice: a claim belongs to its origin, not to the digest that
restates it. It keeps its single record, it will keep ranking near the top, and
the ranking cannot tell a thin file from an index. This verdict is recorded in
the script's `AUDITED` ledger so the next reader does not spend the pass again.

**Rank 11 is the clean case.** `RESULTS-orbit-closure-diagnostic.md` held one
Rule 90 lemma at line 64 while the entire diagnostic the document exists to
report was uncovered. Four records now hold it:
`r30-ocd-slopes-inside-iid-range`, `r30-ocd-criteria-do-not-fire`,
`r30-ocd-rule90-pipeline-control`, and `r30-ocd-preregistration-deviations`.

The last of those is a defect report rather than a result, and it qualifies
every statistic in that document: the run deviates from its own frozen
protocol in three ways, none recorded as an amendment. The pre-registration
sets `T >= 2,000,000` and the run used 1,100,000. The pre-registration
guarantees every window at least 8 depths; counted from the per-depth tables
the depths are 10, 10, 10, 9 and 5 for `W = 2^12` through `2^20`, so the
guarantee fails at the largest window, where the deepest start is
`t0 = 51,424`, 4.7% into the column. And the frozen reproduction block still
reads `--steps 2000000` while the run line reads `--steps 1100000`, so the
documented command does not reproduce the reported run. This is consequential
rather than cosmetic: the one large-window seed-max exceedance and the
deepest-window drift test both land in the cell the depth shortfall weakens.

*Amended 2026-09-16, same day.* The deviation was closed by running the
registered protocol at `T = 2,000,000` rather than by amending the frozen
pre-registration; the columns were already cached, so the correction cost 7
seconds. Depths per window are now 10, 10, 10, 10 and 9, so the `>= 8`
guarantee holds everywhere, and the frozen reproduction command is now the one
that produced the tables. The verdict is unchanged, CONSISTENT WITH unique
ergodicity, on 2 of 25 seed-max exceedances rather than 3: the exceedance that
disappeared is `(L = 8, W = 2^20)`, the weakened cell itself, where Rule 30's
statistic is identical in both runs and the null's seed maximum rose from
2.441e-04 to 2.613e-04 once each null seed took its sup over 9 depths instead
of 5. `r30-ocd-preregistration-deviations` is retained as the record of what
the screen found and now carries the correction.

**Rank 123 is the finding that matters most, and the ranking did not produce
it.** `RESULTS-p3-balanced-defect-normal-form.md` already carried three
records. It was reached by following a link out of the rank-2 index. Two
quantitative claims were held by no record: the cost accounting that is the
document's entire point, `L_d = (7*4^d - 4)/3` literal word length against a
normal form evaluating one guard in `O(d)` Boolean work and a zero-input marked
query at `O(log(d+2)+log(k+2))` bit work; and the exact witness
`[F_3,F_1](A^8(1)) = 102465` against `102849`, refuting adjacent cancellation
for nonadjacent conjugate pairs. Now `r30-p3-balanced-defect-normal-form-cost`
and `r30-p3-balanced-defect-nonadjacent-witness`.

## 3. The conclusion, which is about method

Coverage debt in this archive has now been found twice, and both times by the
same route: **a figure or claim restated in a second document, traced back to
an origin that held no record.** That is how
`r30-p3-fused-section-blocks-fixed-family-control` surfaced, and it is how the
balanced-defect gap surfaced here. Neither was found by a metric. The density
ranking earned its keep once, at rank 11, and produced a false positive at
rank 2.

So the ranking is a place to start reading, not an instrument that finds gaps.
The instrument that finds gaps is a reader following a restatement home.

## 4. What is not established

Three files of 493 were read. Nothing here says the other 490 are covered, and
nothing here bounds how much debt remains; the honest statement is that the
screen has been built, calibrated, and used once. The two failed detectors are
recorded as failures rather than deleted, and the three audited files carry
their verdicts in the script so the ranking is resumable.

`EXTRACTION_STATUS.md` already says claim-level completeness within a file was
never independently verified. That is still true. This narrows it by three
files and supplies the tooling, nothing more.

## 5. Reproduction

```sh
uv run python screen_claim_coverage.py --output claim-coverage-screen.json
```

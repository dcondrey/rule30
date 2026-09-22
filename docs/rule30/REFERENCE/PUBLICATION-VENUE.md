# Where to publish the attempt register

Checked 2026-08-31. Retrieval was done by an agent reading primary sources;
identifiers are recorded so every claim can be checked. Items marked
*not primary-verified* were reported from secondary sources or domain knowledge
and must be confirmed before they are relied on.

## Recommendation, revised

An **arXiv survey / state-of-the-problem paper** is the primary venue, with the
register as a permanent versioned URL beside it, a Zenodo DOI as archival
supplement only, a post to the existing Wolfram Community contest thread, and a
submission to the prize site's own bibliography channel.

**This revises the recommendation given earlier the same day**, which was to
publish the repo with a Zenodo DOI as the front door. That was wrong on the
evidence below: depositing a standalone register with a DOI has no precedent in
mathematics, and the Rule 30 Zenodo namespace is currently occupied by
unreviewed claimed solutions. Zenodo-alone would not confer standing and would
inherit an association we do not want.

## 1. The prizes are all three open and unclaimed

Verified from the site. **`rule30prize.com` 301-redirects to `rule30prize.org`;
the `.org` is canonical** and should be what we cite. The site is a landing page
plus `/bibliography/`; `/rules/` and `/sitemap.xml` both 404.

No prize claimed, none withdrawn. The only status language is *"For each of the
Problems, submissions will be accepted until a satisfactory Solution has been
achieved."* $10,000 each from the Wolfram Foundation, $30,000 total.

**Adjudication is by an unnamed committee.** *"The Prize Committee will oversee
the review and validation of candidate correct solutions"*, decisions *"final
and binding"*. No member is named on the site or in the October 2019
announcement.

**Submission** is a Wolfram Cloud form
(`wolframcloud.com/obj/forms/rule-30-prize/submit-solution`). The solution must
be a *"technical research paper, suitable for publication"*; no anonymous
submissions; submitter keeps ownership and grants a non-exclusive royalty-free
right to publish.

**There is no stated policy on partial or negative results.** String tests on
the landing page return nothing for "partial", "negative" or "bound", and the
2019 announcement offers no mechanism for recognising progress short of a
complete solution. **This is silence, not exclusion. Do not read it either way.**

Consequence: the register **cannot be submitted as a prize entry**. The rules
require a solution paper.

## 2. No public attempt log exists, for Rule 30 or comparably

We would be **creating a format, not joining one**. That is verified rather than
assumed: multiple independent surfaces come back empty (HAL 1 unrelated hit,
Zenodo 2, no Wolfram Summer School project on the centre column, Hacker News
announcements only). Strength: strong for Rule 30 specifically; weaker as a
general claim about CA theory, where only keyword searches were run.

Two adjacent conventions worth inheriting from rather than inventing against:

**Polymath** states the norm explicitly, at
`polymathprojects.org/general-polymath-rules`: *"Often, progress on a
mathematical problem proceeds by first eliminating some ostensibly plausible
approaches; the reason for the failure of the approach is often instructive."*
An ideal contribution includes *"negative insights"*. But Polymath's dead-end
record is a **byproduct of a live collaboration**, scattered across blog threads
and wiki pages, never extracted into a standalone citable object. Gowers'
"complete with false starts, dead ends" description is *not primary-verified*.

**erdosproblems.com (Bloom, 2023-)** is the best structural model: ~1,217
problems, ~46% solved, each with a verbatim statement, bibliography, progress
notes and an Open/Solved flag; cited in the literature as e.g. "T. F. Bloom,
Erdős Problem #650" with a URL. Two differences that matter for us: it is **a
website cited by URL, not a DOI deposit**, and it records *progress*, not
systematically *typed exclusions of failed approaches*. Details *not
primary-verified* (the homepage 403s to automated fetch).

## 3. No survey of the prize problems exists

| surface | query | result |
|---|---|---|
| arXiv API | `abs:"rule 30"` | **11 total**, full list read; no survey, review or bibliography |
| OpenAlex | `title.search:"rule 30"` | 83 results, list read; dominated by US legal procedure (FRCP Rule 30) and CA cryptography; no survey |
| rule30prize.org | `/bibliography/` | the only curated Rule 30 bibliography that exists, and it **stops at 2019** |

Strength: **strong.** Two independent indexes, full result lists read rather
than sampled. Blind spot: arXiv's `abs:` is metadata-only, so a survey in a book
chapter or non-indexed venue would be invisible.

**This is the gap, and it is the strongest hook we have.** The prize site's
bibliography page carries a standing invitation, *"Send us suggestions for
additional publications of Rule 30"*, and has been frozen for seven years. That
is the one documented channel by which non-solution work can be acknowledged by
the prize apparatus.

## 4. Zenodo is the wrong front door

No named example was found of a structured negative-results or attempt register
deposited as a standalone citable artifact with a DOI **in mathematics or
theoretical computer science**. Zenodo's own guidance accepts negative results,
and Zenodo is well established for TCS/SE **artifacts** (0.0% to 16.0% of
research-artifact hosting between 2017 and 2022; FSE 2021 and ICSE 2021-2023
recommend it) -- but "artifact" there means code and data accompanying a paper.

Where the practice does exist it is outside mathematics: ReScience C and the ML
Reproducibility Challenge; the Journal of Negative Results in ecology and
evolutionary biology; JASNH in psychology. All four *not primary-verified*.

**The decisive point is namespace contamination.** As of 2026 the most visible
Rule 30 Zenodo deposits are unreviewed claimed resolutions (see §5). A careful
negative-results register deposited there lands adjacent to them.

## 5. Claimed 2026 resolutions, none reviewed, none awarded

Added to `PATH.md` §8.1 the same day. **None is a prize award and none is peer
reviewed**, but they are now the most visible Rule 30 material on Zenodo.

- **Fradkin 2026**, "Rule 30 Resolved: Synchronization, Uniform Cylinder
  Frequencies, and Unconditional Convergence from First Principles", **five**
  Zenodo versions (10.5281/zenodo.18838072, .18838239, .18865858, .19148341,
  .19187115). OpenAlex: `is_accepted: false, is_published: false`.
- **"Transcendence of the Center Column Generating Function of Rule 30 and the
  Resolution of the Prize Problems"** (2026). Adjacent to row 47 and
  `RESULTS-followup-rationality-obstruction.md`, so this is the one to read first.
- **"Structural Reductions for Wolfram's Rule 30 Prize Problems"** (2026),
  matching the Ikram OSF nodes already in the register.

Neither Fradkin nor the transcendence paper has been read in this repo. They are
listed as claimants to be assessed, **not as refuted**.

## 6. Wolfram Community: thin but alive, and external links are normal

Site-restricted search surfaces exactly **two** Rule 30 threads.

- ["Wolfram's Rule 30 contest"](https://community.wolfram.com/groups/-/m/t/1802242),
  started by Todd Rowland (Wolfram staff), **7 years old, 22.6K views, 14
  replies**, last active **7 months ago**.
- [Nersissian's "Rule 30 exact binomial-Lucas lifting"](https://community.wolfram.com/groups/-/m/t/3647733),
  carrying a Wolfram Staff Pick and Featured badge.

So roughly two dozen substantive contributions across seven years: a low-traffic
thread, not an active area. **But linking out is settled practice, not
inference:** the contest thread already links to writings.stephenwolfram.com,
rule30prize.org, brunni.de, LinkedIn, and attached notebooks. The staff-pick
badge shows substantive external research gets promoted rather than tolerated.

## Prerequisites before anything is published

1. **Reconcile the split register.** `PATH.md` §7.1 holds rows 1-72 plus an
   out-of-band row 76; rows 73-90 live in
   `experiments/overnight-arms/frontier_attack/FINDINGS.md` §3, and the two
   streams collide at row 76. Acceptable as a working note, not in a published
   artifact where the first thing a reader does is look up a row number.
2. **Rename `eps_30`**, which collides with a different `eps(m)` defined for
   Rule 30 in arXiv:2604.00165 (2026), and rename the fuel instrument, whose
   name inverts wasmtime's meaning (see `LITCHECK-fuel-instrument.md`). Both are
   cheap now and expensive after a DOI pins them.
3. **Read the two unassessed 2026 claimants** in §5. Publishing a
   state-of-the-problem survey without having read the papers claiming to have
   solved the problem is not defensible, whatever their review status.

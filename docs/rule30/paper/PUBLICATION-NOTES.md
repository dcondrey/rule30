# Publication notes: Rule 30 zero-tail theorem

## Defensible claim

> We prove a Rule-30-specific zero-trace fiber theorem for finite
> configurations, settling the eventually-constant case of Kopra's width-one
> finite-configuration eventual-periodicity problem, and obtain a sharp
> finite-radius escape-time law.

**Scope widened 2026-08-30 from constant-zero to eventually-constant.**
`zero-tail-note.tex` now carries Corollary 5: no column of the orbit of a
nonzero finite configuration is eventually constant.  The proof is three lines
from Corollary 4 (the zero-tail theorem, formerly numbered 3) plus the latch
identity at the origin, and needs nothing outside the manuscript.  The
constant-one side is now stated in full rather than gestured at: Theorem 3 gives
the all-one fiber, a single checkerboard left half independent of the right
half, Theorem 7 its sharp horizon `q-1` for `q` the least even integer past `w`
with `2^w` extremizers, and Corollary 8 the combined law, longest constant central prefix `w+1` with `2^w` extremizers for even `w`
and `2^w-1` for odd `w`.  All of this was already proved in
`../RESULTS-eventual-period.md`; the note had been carrying only the zero half,
so it under-claimed against the repo's own settled results.  Independently
re-verified in `../../../experiments/rule30/constant_trace_audit.py`, which
matches Theorem 7's extremizer set exactly for `w <= 7`.  This supersedes the two routes already in the repo,
both of which remain correct: `../PATH.md` section 2 derives the constant-one
case in one line but through Jen 1990 Prop. 3 / Kopra Thm. 3.5, an external
dependency, and `../RESULTS-eventual-period.md` proves it independently via the
all-one checkerboard fiber.  The wording rule below is unchanged and now binds
harder: the eventually-constant case is still a strict subcase of the thesis
form, so say "settles the eventually-constant case of Kopra's width-one
finite-configuration question (2019 thesis, after Thm 3.1.12)", never "settles
Problem 3.10".

**The novelty half of this claim is corpus-bounded.**  "Settling" asserts the
subcase was open, and that assertion rests on the sources listed under *Novelty
audit* below.  Jen, *J. Stat. Phys.* **43** (1986) 219-242 is **unread**, and
its abstract clause (ii), on nearest-neighbor rules whose finite initial
conditions generate a constant temporal sequence, is the one passage in the
located literature that could touch T1 in either direction.  Until it is read,
the honest form of the claim is "not found in the corpus searched", not
"novel".

Do not describe the manuscript as a proof of Rule 30 center-column
nonperiodicity. Nonconstant eventual periods remain open.  A separate exact
cycle in `../RESULTS-eventual-period.md` found no proof of that remaining case;
its finite SMT exclusions must not be promoted to an asymptotic claim.

## Independent review status

A read-only hostile proof audit independently rederived triangular
uniqueness, every `C_m` boundary case, the complete fiber classification, the
eventual-zero corollary, and the exact radius bound/count. It found no critical
or major mathematical issue; the remaining scope is stated explicitly below.

Those revisions have been applied:

- the odd-radius extra zero at depth `w+1` is explicit;
- triangular uniqueness is a causal-boundary induction;
- the arbitrary-period/right-tail statement is labelled a sufficient
  strengthening rather than an equivalent obligation;
- the unretained depth-22 scratch claim was removed;
- the finite-set oracle now rejects rules with nonquiescent zero.

This is an internal independent review, not journal peer review.

## Novelty audit

**Status: primary sources read, 2026-08-28.**  The earlier version of this
section said "no prior source was located", which is a search result rather
than a reading.  The two load-bearing passages have now been fetched and read
in the original; the verbatim text is below.  One source remains unread and is
named at the end.

### Kopra's open problem exists in two forms, and only the broad one is ours

Thesis (Kopra, *Cellular Automata with Complicated Dynamics*, TUCS
Dissertations 249, Turku 2019), immediately after Theorem 3.1.12, verbatim:

> Theorem 3.1.12 (Jen [28]).  If `x` in `Sigma_2^Z` is a finite configuration
> not equal to `0^Z`, then `Tr_{W30,[0,1]}(x)` (the trace of width 2), is not
> eventually periodic.  ... **It still seems to be an open problem whether
> `Tr_{W30}(x)` (the trace of width 1) can be eventually periodic for some
> finite `x != 0^Z`.**

Journal/arXiv (arXiv:2202.13809v1, Problem 4.8; renumbered Problem 3.10 in TCS
946 (2023) 113668 after two corollaries were inserted), verbatim:

> We conclude by noting that perhaps the most famous question [16] concerning
> Rule 30 remains unsolved.  It concerns the trace of width 1 of a single, very
> simple configuration, but it is probably equally difficult for all
> configurations of `N(Sigma_2)`.  Note that the case of trace of width 2 is
> covered by Theorem 3.5.  The answer "no" is expected.
>
> **Problem 4.8.**  Let `x = ...0001000...` in `Sigma_2^Z` be the configuration
> containing a single 1 at the origin.  Is `Tr_{W30,0}(x)` eventually periodic?

**Consequence for positioning.**  Cite the *thesis* form, not Problem 4.8/3.10.
The thesis form quantifies over all finite nonzero `x`, which is our
configuration class; Problem 4.8 is the lone seed only.  A constant column is
eventually periodic, so T1 together with Corollary 5 settles a strict subcase of
the thesis form: same width, same configuration class, strictly narrower
property.  Neither settles Problem 4.8.  Say "settles the eventually-constant case of Kopra's width-one
finite-configuration question (2019 thesis, after Thm 3.1.12)", never "settles
Problem 3.10".

Kopra's own Rule 90 obstruction should be quoted in the note, since our
Rule-90 counterexample is the same observation: Rule 90 from a lone seed does
produce a single eventually periodic column, so no argument that only uses
rapid left expansivity can work.

### Why Kopra's Theorem 3.5 does not subsume T1

Theorem 3.5 gives width-two nonperiodicity for rapidly left expansive CA; Rule
30 is `(1,1)` left permutive, hence `w = 2`.  Two adjacent columns determine
everything to their left, but a lone zero column at 0 does not determine column
`-1`, and the pair (zero at 0, aperiodic at 1) is an aperiodic width-two trace
fully consistent with Theorem 3.5.  The gap is exactly one column wide, and
that is the entire content of T1.

### Closest prior art, and the exact gap

Jen 1990, Proposition 3 (read from LANL preprint LA-UR-90-761,
<https://www.osti.gov/servlets/purl/7230855>), verbatim:

> Let `R` be a rule injective in its `(i+1)`-th component with `{100} -> 1` (or
> injective in its `(i-1)`-th component with `{001} -> 1`).  Then with arbitrary
> finite initial conditions, there can exist at most one periodic temporal
> sequence.

Applies to rules 30, 86, 90, 150, 154, 210; her "periodic" means eventually
periodic.  **The gap:** Jen leaves exactly one exceptional column open, and a
zero column is precisely where that exception sits.  She characterizes the
exception where it exists (Proposition 2 for Rule 90, Proposition 5 for Rule
18, each naming the all-zero center column from a symmetric initial condition)
and gives no such exclusion for Rule 30.  T1 closes that hole for Rule 30.

Attribution: Wolfram's prize page credits **Jen 1986** ("Erica Jen showed in
1986 that no two columns can both become periodic"); Kopra credits **Jen 1990,
Proposition 3**.  Cite both.

### The one source still unread

**Jen, "Global properties of cellular automata", J. Stat. Phys. 43 (1986)
219-242.**  Still not read in the original.  Springer paywalled (303
to `idp.springer.com`); OSTI holds the bibliographic record `biblio/5674011` but
`servlets/purl/5674011` is 404, so unlike her 1990 paper there is **no LA-UR
preprint**; no arXiv, no scholar.archive.org (`sim_journal-of-statistical-
physics_1986*` does not exist), no CORE, no zbMATH review (the `api.zbmath.org`
record Zbl 0638.68043 carries only a truncated publisher abstract, which must
not be quoted), MathSciNet paywalled and its archive.org scan lending-restricted.

**What Theorem 4 gives, from the only source that cites it by number.**  Rowland
2006 cites it twice, and his ref [1] is confirmed as this paper (bibliography
p.17 reads: [1] Erica Jen, "Global Properties of Cellular Automata",
*Journal of Statistical Physics*, **43** (1986) 219-242).  Verbatim, p.6:

> A result of Jen [1, Theorem 4] guarantees the eventual periodicity of columns
> in any range `[-d, 0]` cellular automaton with a rightful initial condition.

and, applying it to Rule 30 itself, p.13:

> A consequence of Jen's Theorem 4 [1] is that each left diagonal of rule 30 is
> eventually periodic with period length a power of 2.

The second quote is the discriminator, because it is Rowland instantiating
Theorem 4 at Rule 30 and reporting what comes out.  What comes out is
**diagonals**, not columns.  The reason is his `[-d,0]` normalization (p.5): "By
composing with an appropriate horizontal shift, any k-color, finite range rule
can be put into this form ... The advantage of these 'shifted' rules is that the
columns (rather than the diagonals) are periodic."  Rule 30 is range `[-1,1]`;
the shift that puts it in `[-d,0]` form sends Theorem 4's columns to Rule 30's
diagonals.  That is exactly the A094605 / Rowland Lemma 2 territory already
recorded as prior art in `../RESULTS-diagonal-periodicity.md`, and it does not
touch a center-column statement.

*Verified locally:* all three quotes read out of the Rowland PDF on disk, not
from a summary.

**The residual exposure is abstract clause (ii), not Theorem 4.**  The OSTI
abstract promises conditions characterizing nearest-neighbor rules whose
arbitrary finite initial conditions "(ii) generate at least one constant
temporal sequence".  No retrieved source restates clause (ii) or names the
numbered result carrying it, and nearest-neighbor is Rule 30's class, so the
clause is load-bearing in both directions.

## RESOLVED 2026-08-30: full text obtained and read

The paper was obtained (`~/Downloads/Global_properties_of_cellular_automata.pdf`,
10 pp. scan of JSP 43:219-242) and read in full by the parent session.  The
speculation below this heading is superseded; the earlier dichotomy claim
"there is no third reading in which clause (ii) is irrelevant" was **wrong**,
and the third reading is the one that obtains.

**Clause (ii) is Section 5, Theorem 7a (p. 236).**  Verbatim: "A rule R with
`a_0 = 0`, `a_1 = a_4 = 1` will generate from arbitrary finite initial
conditions at least one constant nonzero temporal sequence iff one of the
following conditions holds", with four conditions (i)-(iv).  The zero case is
not proved separately; p. 236 states only "Symmetric results hold for the case
of constant zero temporal sequences."  Jen's "constant" is the *eventual*
notion (p. 235: exists finite `T` with `x_i^t = C` for all `t >= T`), matching
T1's.

**Rule 30 is in scope and fails every condition.**  Coefficients
`a = [0,1,1,1,1,0,0,0]` (`a_0..a_7`), so the hypothesis `a_0=0, a_1=a_4=1`
holds.  Machine-checked against the four conditions: (i) needs `a_6=a_7=1`;
(ii) needs `a_6=1`; (iii) needs `a_7=1`; (iv) needs `a_5=1`.  All false.

**The quantifier decides it, and T1 survives.**  Theorem 7a characterizes rules
for which *arbitrary* (i.e. all) finite initial conditions generate at least one
constant column *somewhere*.  Rule 30's failure yields only the negation:
*there exists* a finite initial condition with no constant column.  T1 is
universal over nonzero finite configurations and fixes the locus.  T1 is
therefore **strictly stronger and not derivable from Jen 1986**.  Novelty is
retained, and the note now positions against Theorem 7a explicitly rather than
claiming absence of prior art.

**The three circulating attributions are resolved**, all to different results in
this one paper: "at most one periodic column" is Theorems 2a/2b (rule list
30, 86, 90, 150, 154, 210, p. 231) generalized as Theorem 3; Rowland's
"Theorem 4" is diagonal-sequence periodicity (p. 232); clause (ii) is Theorem 7a.
That is why the citations looked inconsistent.

**Voorhees 1988** (CMP 117:431-439, `~/Downloads/`) was checked at the same time
for overlap with T1.  None: its scope is *binomially determined nearest-neighbor
**additive*** CA over `Z_p` (Sec. II), Rule 30 appears zero times in the full
text, and it solves the one-step predecessor problem rather than a constraint
over all future time.  It is now cited as a contrast: inversion results in this
area are additive-only, and it records that the general predecessor problem is
NP-complete.

**Circulation gate: MET.**  The precondition below is discharged; no email to
Rowland is required for this purpose.  Both papers are cited in the note's
introduction and bibliography.

---

*Superseded speculation follows, retained for provenance.*

*Routes to the text, in order of cost.*  (1) Ask Eric Rowland; he cites Theorem
4 by number and can answer the clause-(ii) question without seeing the note.
(2) Public-library interlibrary loan, which fills a 1986 *J. Stat. Phys.*
article routinely and free at systems such as NYPL ("Interlibrary Loan Services
are free for NYPL cardholders", scans capped at 50 pages or 10%).  (3) Springer
purchase; the article page redirects to `idp.springer.com` and shows no price
numeral and no rental option unauthenticated.  (4) Gravner & Griffeath, "Robust
periodic solutions and evolution from seeds in one-dimensional edge cellular
automata", *Theoret. Comput. Sci.* (2012), the most on-point of the 49 works
Semantic Scholar lists as citing `10.1007/BF01010579`, CAPTCHA-walled on
ScienceDirect with no arXiv version.

Erica Jen cannot be asked; she died 12 November 2023.  Do not spend further
effort on OSTI: `purl/5674011` is a confirmed 404 and no LA-UR report exists for
this paper, unlike her 1990 one.

#### The further-work section claims nothing

Section 5 of the manuscript states the latch split
`c_t=1 => l_t = 1 XOR c_{t+1}`, `c_t=0 => l_t = c_{t+1} XOR r_t`, and the
consequent localization of the remaining obligation to column `1` on the trace's
zero set.  **None of this is presented as new, and it must not be.**  It is the
repo's own stated second exact target (`../RESULTS-eventual-period.md:52-55`),
and the identity is already implemented in
`../../../experiments/rule30/inverse_trace_probe.py:135-160`.  It appears in the
paper as a signpost for a reader, not as a contribution.  See `../PATH.md`
section 0.5, which is authoritative on what that material does and does not
contribute.

The identity itself was re-verified before it entered the manuscript: 200
random finite configurations, 24,000 steps, zero violations of any of the three
forms.

## Independent claims sweep

arXiv full-text sweep on `all:"rule 30"`, 100 most recent, plus nlin.CG and
math.DS listings 2019-2026: no claim about a constant, zero, or eventually
periodic center column.  No Rule 30 prize has been claimed.  rule30prize.org's
bibliography stops at 2019 and lists neither Jen 1990 nor Kopra.

### T2 verified independently

The sharp horizon theorem was re-derived by brute force outside the manuscript's
own machinery: for `w = 1..7`, exhaustive enumeration of all nonzero `x` with
`supp(x) subset [-w,w]` and `x_0 = 0` reproduces both
`max H = 2 ceil(w/2)` and the extremizer count `2^w - 1` exactly.  Note for
readers of these notes: `S_w` has `2^{2w} - 1` members, and the `2^w - 1`
extremizers are indexed by the nonzero right word `(R_1,...,R_w)` with the left
half forced.  An earlier summary here described `S_w` loosely as a "radius-w
window", which made the two counts look inconsistent; they are not.

### Original audit, retained

No prior source was located for either

```text
Tr_0^(-1)(0^infinity) intersect finite-support = {0}
```

or

```text
H_max(w) = 2 ceil(w/2), with 2^w-1 extremizers.
```

Closest sources:

- Jen 1990, Proposition 3: at most one periodic temporal sequence; one
  exceptional column remains possible.
- Kopra 2019, Theorem 3.1.12 and following paragraph: width-two
  nonperiodicity, followed by the explicit open width-one finite-configuration
  question.
- Kopra 2023, Theorem 3.5 and Problem 3.10: width-two exclusion and the
  lone-seed width-one problem, with Rule 90 as the control.
- Rowland 2006, Proposition 1 and Lemma 1: one-sided inverse-history
  uniqueness and leading-discrepancy propagation, but no zero-trace fiber.
- Trace-subshift work studies the image of the trace map, not the inverse
  fiber of `0^infinity`; pre-expansivity is stronger and uses all asymptotic
  pairs and generally a finite observation window.

Safe novelty wording is “no prior source located” or “apparently new partial
theorem.” Before asserting priority, send the theorem statement and closest-
prior-art paragraph to Johan Kopra and Eric Rowland for a terminology and
reference check.

## Suggested venue path

Facts below verified against publisher and arXiv primary sources 2026-08-28.

1. Private circulation to two cellular-automata experts.  Author metadata is
   already confirmed, so this is unblocked.
2. Preprint, but only after deciding the licence question in the note below.
3. Best focused-note fit: *Complex Systems*.
4. Specialist alternative: *Journal of Cellular Automata*.
5. AUTOMATA workshop for early feedback, next available edition.

*Theoretical Computer Science* would be more plausible if the result were
extended to a general trace-fiber/observability theorem beyond Rule 30.

### Venue facts

**Complex Systems** (`complex-systems.com/contribute/`; the host fails TLS
verification on direct fetch).  No publication charges: "For the added benefit
of authors, there are no publication charges for *Complex Systems*."  LaTeX and
Mathematica templates provided.  Submission by Wolfram Cloud webform or email to
`info@complex-systems.com`.  Submissions must "Include the names, addresses and
telephone numbers of suggested referees", so the private-circulation contacts
double as the referee suggestions.  No stated page limit, no short-communication
category, and no AI-disclosure policy appear on the author-facing pages; that is
verified absence there, not a positive statement that none exists.  Current issue
Vol. 35 No. 2 (2026) runs four articles of roughly twenty pages each, so a
four-page note is atypical for the venue even though nothing forbids it.

**Journal of Cellular Automata** (Old City Publishing).  Active but slow and
lagging in indexing: DBLP stops at Vol. 16 (2021), the publisher's own contents
page reaches Vol. 18 (2024), and the 2026 call for papers sells Vol. 19.
Editor-in-Chief Andrew Adamatzky, `andrew.adamatzky@uwe.ac.uk`; submission is a
PDF emailed to an editor.  No page charges.  **Copyright transfers to the
publisher on acceptance**, which is the one fact that constrains ordering
against a preprint.

**AUTOMATA.**  The 2026 edition (AUTOMATA & ACRI, Ghent, 6-10 July 2026) has
already taken place and no 2027 edition is announced.  When one opens, the
right track is the exploratory-paper category, up to eight pages, "quick
reporting of recent discoveries and partial results", Springer LNCS format via
EasyChair.  Full papers are capped at twelve pages and go to LNCS proceedings.

**arXiv.**  Endorsement is required: "arXiv requires that users be endorsed
before submitting their first paper to arXiv or a new category."  Automatic
endorsement requires both a claimed co-authored arXiv paper and an institutional
email address; a company domain satisfies neither, so a first submission to
math.DS or nlin.CG needs a human endorser, solicited from the abstract page of a
recent paper in that category.  The endorsers worth asking are the same people
worth asking for a proof read, so consolidate the two requests.  Licence choice
is "irrevocable" per version, so it must be settled before the first upload and
against the target journal's copyright terms.

**arXiv generative-AI policy**, verbatim from `info.arxiv.org/help/moderation/`:

> continue to require authors to report in their work any significant use of
> sophisticated tools, such as instruments and software; we now include in
> particular text-to-text generative AI among those that should be reported
> consistent with subject standards for methodology.

> generative AI language tools should not be listed as an author

Disclosure therefore goes in the methodology or acknowledgments, and the named
author carries full responsibility for the contents.

### Contacts

- Eric Rowland, Associate Professor, Department of Mathematics, Hofstra
  University.  `ericrowland.github.io`; his email is deliberately obscured on
  the site's contact page, so use that page.  He cites Jen 1986 Theorem 4 by
  number, which makes him the single best person to ask about clause (ii).
- Jarkko Kari, Professor of Mathematics, University of Turku, `jkari@utu.fi`.
- Ville Salo, Associate Professor of Mathematics, University of Turku,
  `vosalo@utu.fi`.
- Johan Kopra: no current institutional page (`utu.fi/en/people/johan-kopra`
  returns 403 while colleagues' pages on the same host resolve, and DBLP shows
  no output after 2023).  Publication-time address `jtjkop@utu.fi`, possibly
  stale.

**Erica Jen died on 12 November 2023**, aged 71 (Santa Fe Institute memoriam,
`santafe.edu/news-center/news/in-memoriam-erica-jen`, verified directly).  She
cannot be asked about her own 1986 paper.  Cite the work.

## Reproducibility package

- `zero-tail-note.tex`: standalone six-page theorem note in five sections,
  with two generated space-time figures and verified author metadata.  The
  hand-drawn inverse-transducer schematic was cut; its worked example is now
  one sentence in the introduction.
- `figures/`: generated TikZ fragments for both figures, together with
  `../../../experiments/rule30/figures.py`, which computes every drawn cell
  from the rule and self-checks each figure's claimed property before emitting.
- `zero-tail-note.bib`: expanded source bibliography retained for a longer
  version; the note itself uses a compact inline bibliography.
- `../../../experiments/rule30/zero_tail_probe.py`: exact transducer,
  certificates, and independent finite oracle.
- `../../../experiments/rule30/constant_trace_audit.py`: adversarial audit of
  every numbered claim in the note, importing nothing from this repository.
- `../../../experiments/rule30/zero_tail_smt_certificate.py`: optional Z3
  checks for the finite Boolean schemas used in the proof.
- `../../../experiments/rule30/Rule30ZeroTail.lean`: axiom-free, kernel-checked
  partial formalization of the proof's inductive core.
- corresponding unit tests in `../../../experiments/rule30/`.

The Z3 artifact checks local schemas only. The unbounded proof is the explicit
mathematical induction in the manuscript; this is not called a full
proof-assistant formalization.

The Lean artifact proves left permutivity, arbitrary-depth triangular
sensitivity, the prefix-OR closed form under a first-right-one hypothesis, all
local invariant identities, and the infinite-tail contradiction conditional
on the classification disjunction. It does not yet derive that disjunction
from a zero trace; describe it as a partial formalization only.

## Before external circulation

- **AI-disclosure statement is still missing from the manuscript.**  The arXiv
  policy quoted above requires significant use of text-to-text generative AI to
  be reported in methodology or acknowledgments.  `zero-tail-note.tex` has no
  such statement.  Left unwritten deliberately: the wording asserts what the
  named author's own contribution was, which is his to state, not to be drafted
  for him.
- ~~Replace “Anonymous working draft” with the actual author list and
  affiliations.~~  **DONE 2026-08-28.**  `zero-tail-note.tex:26-28` and the
  `pdfauthor` field carry David Lee Condrey, WritersLogic, Inc.,
  `david@writerslogic.com`, and the compiled PDF shows them on page 1.
- Decide authorship and acknowledgments based on the human contribution and
  intended venue's AI-disclosure policy.
- Obtain at least one human expert proof review.
- Recheck current venue formatting and disclosure requirements.
- Do not submit or contact anyone without the user's explicit authorization.

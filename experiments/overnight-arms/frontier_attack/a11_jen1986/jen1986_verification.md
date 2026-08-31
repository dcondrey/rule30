PROCEEDING-WITHOUT-SOURCE

# Jen 1986 provenance and scope note

Scope of this file: it is the record that lets `docs/rule30/PATH.md` row 72
(the zero-tail note packaging row 25) proceed to circulation **without** the
full text of Jen 1986, by (a) showing the mathematical dependency on that paper
is zero, (b) stating the residual novelty exposure precisely rather than hiding
it, (c) rescoping the novelty claim to sources that were actually read, and
(d) closing the retrieval question so no future session reopens it.

Written 2026-08-30. Author: researcher agent, session `ed534796`.
Write fence honoured: nothing outside this directory was modified.

---

## 0. What changed today, and what did not

**Did not change.** The full text of Jen, "Global properties of cellular
automata", *J. Stat. Phys.* **43** (1986) 219-242, DOI `10.1007/BF01010579`,
is still unobtained. No numbered result from that paper can be quoted. That
was already settled in `docs/rule30/PATH.md` §8.6 and
`docs/rule30/paper/PUBLICATION-NOTES.md` ("The one source still unread"), and
this session did not overturn it. **Standing instruction: do not retry.** The
route table in §5 is the full record of what has been tried.

**Did change — one provenance upgrade, worth recording.** The abstract, and
therefore clause (ii), is now sourced from **the publisher's own article page**
rather than from the OSTI bibliographic record or the zbMATH stub. Route:

```
https://r.jina.ai/https://link.springer.com/article/10.1007/BF01010579
```

Direct `link.springer.com` fetch 303s to `idp.springer.com`; the `r.jina.ai`
text proxy returns the Springer landing page in full, including the complete
abstract, the "About this article" block, and the paper's own 19-item
reference list. It does **not** defeat the paywall: no body text, no section
headings, no theorem statements, no page images. This upgrades §8.6's status
for the abstract only — from "OSTI rendering of an abstract" to "publisher's
rendering of an abstract" — and changes nothing about the body.

The zbMATH stub (Zbl 0638.68043) is not quoted anywhere below, per the
standing prohibition. Nothing below is inferred from a paper that cites Jen
1986.

---

## 1. Clause (ii), verbatim, with provenance

Quoted verbatim from the Springer article page for `10.1007/BF01010579`,
accessed 2026-08-30 via the proxy route above. This is the publisher of record
for the article.

> Cellular automata are discrete mathematical systems that generate diverse,
> often complicated, behavior using simple deterministic rules. Analysis of the
> local structure of these rules makes possible a description of the global
> properties of the associated automata. A class of cellular automata that
> generate infinitely many aperiodic temporal sequences is defined, as is the
> set of rules for which inverses exist. Necessary and sufficient conditions
> are derived characterizing the classes of "nearest-neighbor" rules for which
> arbitrary finite initial conditions (i) evolve to a homogeneous state;
> (ii) generate at least one constant temporal sequence.

Clause (ii) in isolation, as the register quotes it:

> ... for which arbitrary finite initial conditions ... (ii) generate at least
> one constant temporal sequence.

Also recovered from the same page (new, and not previously in the repo):

- **Received 07 August 1985; issue date April 1986; volume 43, pages 219-242.**
- The paper's own reference list has **19 entries**, all 1966-1985, and
  includes `[5] E. Jen, J. Stat. Phys. 43:243 (1986)` — the companion paper in
  the same volume. Nothing in the list is a source that would restate clause
  (ii) for us.
- **No section headings, theorem numbers or page-level content are exposed.**
  The page's own headings are Abstract / Access this article / Subscribe and
  save / Buy Now / Similar content / References / Author information / About
  this article / Cite this article / Key words. The "Key words" block renders
  empty. So the numbered result carrying clause (ii) remains **UNKNOWN**, as
  does whether Rule 30 appears in any classification table.

UNVERIFIED, and it matters: the abstract's "(i)" and "(ii)" are the *abstract's*
enumeration. There is no evidence that the paper labels the corresponding
results as Theorem/Proposition (i) and (ii), and no evidence about their
relation to the "Theorem 4" that Rowland cites.

---

## 2. The mathematical dependency on Jen 1986 is ZERO

Claim: no proof step in the row-25 tree, or in row 26 which travels with it,
discharges into Jen 1986. Every citation of Jen 1986 in this repo is either
prior-art positioning or a novelty-audit hedge. The classification below was
made by reading the documents, not by grep (no shell in this session); the
coverage limit is stated at the end of this section.

| Site | What is cited | Depends on 1986? |
|---|---|---|
| `RESULTS-zero-tail.md` "The theorem" + "Proof" §§1-3 | **Nothing.** Triangular uniqueness (left permutivity + causal boundary), the `C_m` invariant classes, and the finite-support contradiction are self-contained and cite no external result at any step. | **NO** |
| `RESULTS-zero-tail.md` "Consequence for the lone seed" | Nothing external; uses only "a finite nonzero row has ones at `A-1` and `B+1` in its successor". | **NO** |
| `RESULTS-zero-tail.md` all-one paragraph (row 26 content) | Nothing external; direct inverse classification forcing `L_k = 1` iff `k` positive even. | **NO** |
| `RESULTS-zero-tail.md` "Exact bounded constraint certificate" (T2) | Nothing external. | **NO** |
| `RESULTS-zero-tail.md` "Literature and novelty audit" | Jen 1990 Prop 3; Kopra 2023; Kopra 2019 Thm 3.1.12; Rowland 2006 Prop 1/Lemma 1. Jen 1986 not cited here at all. | **NO** |
| `PUBLICATION-NOTES.md` "Defensible claim" / "Novelty audit" | Jen 1986 named as the **unread** source whose clause (ii) could touch T1. Used only to qualify the novelty claim. | **novelty only** |
| `PUBLICATION-NOTES.md` "What Theorem 4 gives" | Rowland 2006 pp. 6 and 13 quoting Jen 1986 Thm 4; used to *discharge* Thm 4 as a diagonal statement under the `[-d,0]` normalization. | **novelty only** |
| `PATH.md` §2, constant-one one-liner | "contradicts Jen 1990 Prop. 3 / Kopra Thm 3.5". | **NO — 1990/Kopra** |
| `PATH.md` R7 mode (ii) | "hands the contradiction to Kopra Thm 3.5 / Jen Prop 3". | **NO — 1990/Kopra** |
| `PATH.md` §8.1 register rows | Jen 1986 as a register entry; Rowland's left-diagonal periodicity "via Jen 1986 Thm 4". | **prior art only** |
| `PATH.md` §8.4 | "Jen 1990 Prop. 3 or Kopra Thm 3.5 in Lean/Coq — NONE." | **NO** |
| `PATH.md` §8.6 | The caution itself. | **novelty only** |
| `RESULTS-eventual-period.md` "Direct all-one fiber" (row 26's own source) | **Nothing.** Proof is self-contained and the file says so explicitly: "This removes the earlier dependence on the width-two theorem for the constant-one case." | **NO** |
| `RESULTS-eventual-period.md` "Exact remaining obligation" | "Jen's Proposition 3 and Kopra's width-two theorem give a second exact target" — 1990. | **NO — 1990/Kopra** |
| `RESULTS-inverse-trace.md` constant-one subcase | "contrary to Kopra's width-two theorem". Superseded anyway by the citation-free proof above. | **NO — Kopra** |
| `RESULTS-diagonal-periodicity.md` | Jen 1986 Thm 4 appears **only** inside a verbatim Rowland quote and in the bibliography, where the file itself records "Not fetched". The file's stated citation for both claims (A) power-of-two periods and (B) preperiod zero is **Rowland 2006 Lemma 2**, quoted verbatim and proved for arbitrary rows. Rowland's Lemma 2 *strengthens* Jen Thm 4 (eventual periodicity → immediate), so the repo depends on the strengthening, not on Jen. | **NO — Rowland** |
| `paper/README.md` (row 72's other source) | No Jen citation of any kind; build, figure-check and artifact instructions only. | **NO** |
| `Rule30ZeroTail.lean` (per `PUBLICATION-NOTES.md` description) | Axiom-free, kernel-checked; formalizes permutivity, triangular sensitivity, the prefix-OR closed form, the local invariants, the infinite-tail contradiction. An axiom-free Lean artifact cannot import an unread 1986 lemma. | **NO** |

**Every load-bearing citation in the tree discharges into a source that was
actually read in the original.** Concretely, the only two external theorems the
tree ever leans on are:

- **Jen 1990, Proposition 3**, read from LANL preprint LA-UR-90-761 at
  `https://www.osti.gov/servlets/purl/7230855`, re-read page-by-page in this
  session (§3 below); and
- **Kopra 2023**, TCS 946 (2023) 113668, **Theorem 3.5** with **Corollary 3.7**
  (which the journal version explicitly labels "(Jen, [7], Proposition 3)", i.e.
  Kopra himself recovers Jen's result inside his own framework), plus **Kopra
  2019 thesis Theorem 3.1.12** and the open-problem paragraph after it.

Note the structural consequence: **Corollary 3.7 means the field already has a
modern, independently proved, fully readable substitute for whatever Jen proved
about two columns.** Even if Jen 1986 were the true origin of the width-two
result, nothing in this repo needs to cite it to *use* that result.

**Loud finding, as required: there is none. No load-bearing step anywhere in
the row-25/26/72 tree depends on Jen 1986, alone or otherwise.**

*Coverage.* The audit is **complete over the tree**, not a sample. `PATH.md`
§7.1 names every source document for rows 25, 26 and 72, and all of them were
read this session, in full: `RESULTS-zero-tail.md` (rows 25, 26),
`RESULTS-eventual-period.md` and `RESULTS-inverse-trace.md` (row 26),
`paper/PUBLICATION-NOTES.md` and `paper/README.md` (row 72). Also read in full:
`RESULTS-diagonal-periodicity.md`, because `PATH.md` §8.1 describes Rowland's
left-diagonal result as holding "via Jen 1986 Thm 4" and that was the one place
in `docs/` where a genuine 1986 dependency could plausibly have been hiding. It
is not there: the file cites Rowland 2006 Lemma 2 for both of its claims and
records Jen 1986 as "Not fetched" in its own bibliography. `PATH.md` itself was
read at §§0-2, 7.1-7.3, 8.0-8.7.

*Residual coverage limit.* Not read this session: `RESULTS-right-cone.md`,
`RESULTS-ladder-rung0/1.md`, `RESULTS-alt-trace-fiber.md`,
`RESULTS-periodicity-bridge.md`, `RESULTS-orbit-closure-diagnostic.md`,
`RESULTS-proof-complexity-probe.md`, the `overnight/` and `ARM*` documents.
None of these is a source for rows 25, 26 or 72, so none can affect this
verdict; whether any of them cites Jen 1986 elsewhere is **UNVERIFIED**.

---

## 3. Jen 1990, Proposition 3 — verbatim, with page numbers

Re-read this session directly from the scanned LANL preprint
**LA-UR-90-761 / DE90 008947**, "Aperiodicity in One-Dimensional Cellular
Automata", Erica Jen, Theoretical Division MS-B258, LANL, submitted to
*Proceedings of AIP US-Soviet Conference on Chaos*. Published as *Physica D*
**45**(1-3):3-18 (1990), DOI `10.1016/0167-2789(90)90169-P`. Access path:
`https://www.osti.gov/servlets/purl/7230855`, PDF read as page images (the text
layer is CCITT-fax and does not extract).

**Page numbers below are the preprint's own printed page numbers**, not journal
pagination. Journal pagination was not obtained; do not convert.

### Proposition 3 (preprint p. 6)

> **Proposition 3:** Let `R` be a rule injective in its `(i + 1)`-th component
> with `{100} -> 1` (or injective in its `(i - 1)`-th component with
> `{001} -> 1`). Then with arbitrary finite initial conditions, there can exist
> at most one periodic temporal condition.

("temporal condition" is the preprint's wording; Figure 2's caption says
"temporal sequence".)

**Exact hypotheses**, assembled from the preprint's own definitions:

1. *Rule class.* `R` is an elementary (nearest-neighbour, binary, radius-1) CA
   rule, injective in its `(i+1)`-th component, with the propagation condition
   `{100} -> 1`; or the mirror form, injective in `(i-1)` with `{001} -> 1`.
   "Injective in the `(i+k)`-th component" is defined on p. 4: the rule table
   is a one-to-one map between `x_{i+k}` and `f(x_{i-1} x_i x_{i+1})` when the
   other two components are held fixed.
2. *Initial conditions.* "arbitrary finite initial conditions" — the paper's
   Definition (p. 3): a configuration `{x_i^0}` with `x_i^0 = 0` for `i < M`
   and `i > N`, and `x_M^0 = x_N^0 = 1`. So the quantifier is **universal over
   all nonzero finitely supported configurations**, and the zero configuration
   is excluded by definition.
3. *"Periodic".* Definition (p. 3): "The temporal sequence `W_i` is periodic of
   period `0 < p < infinity` with transience `0 < T < infinity` if
   `x_i^{t+p} = x_i^t` for `t > T`." So **periodic means eventually periodic**,
   transience allowed.
4. *Conclusion.* At most one site index `i` has an eventually periodic column.

**Applicability, stated by Jen (p. 7), verbatim:**

> The conditions of the above theorem hold for elementary automata Rules 30,
> 86, 90, 150, 154, 210.

**Figure 2 caption (figure page, Rule 30 diagram), verbatim:**

> Figure 2. Evolution of Rule 30 defined by
> `{000, 101, 110, 111} -> 0`, `{001, 010, 011, 100} -> 1`.
> Proposition 3 establishes that, with arbitrary finite initial conditions, at
> most one temporal sequence can be periodic.

### Supporting material read in the same pass

**The Lemma Proposition 3 rests on (preprint p. 6), verbatim:**

> Lemma: Let `W_i` and `W_j`, `i < j`, be two temporal sequences periodic of
> periods `p_i, p_j`, respectively. Then for `i < k < j`, the temporal sequence
> `W_k` is periodic of period `p | lcm(p_i, p_j)` (where `x|y` indicates that
> `x` divides `y` evenly), and of transience bounded by `T < infinity`, where
> `T` is a constant independent of `k`.

**Attribution sentence immediately preceding Proposition 3 (p. 6), verbatim:**

> On the basis of the above lemma, the following proposition [8] asserts that
> (propagating) automaton rules belonging to Class A and B generate at most one
> aperiodic temporal sequence.

Three things about that sentence, all load-bearing for §4:

- `[8]` is Jen 1986. (Confirmed in the repo's prior audit by recovering the
  1990 reference list from the scispace rendering; the reference list is absent
  from the OSTI scan, and this session did not re-verify it. **UNVERIFIED here,
  verified previously.**)
- It says **"at most one aperiodic"**, which contradicts Proposition 3's own
  "at most one periodic" one line below and Figure 2's "at most one temporal
  sequence can be periodic". Read as a typographical error in the preprint for
  "periodic". Flagged, not relied upon.
- It confirms that **Jen 1986 contains a rule classification with named
  "Class A" and "Class B"**, and that Proposition 3 is Jen's own 1990
  restatement of a 1986 result about those classes. This is the only direct
  evidence anywhere about the 1986 paper's internal structure, and it is
  consistent with the abstract's phrase "the classes of 'nearest-neighbor'
  rules".

**Rule 30's membership, established inside the 1990 preprint (p. 5), verbatim:**

> Rule 30, for example, defined by
> `{000, 101, 110, 111} -> 0`, `{001, 010, 011, 100} -> 1`,
> is injective in the `(i - 1)`-th component, but does not satisfy the
> definition of linearity.

**The exceptions Jen names explicitly, and does not name for Rule 30.**

Proposition 2 (p. 5), Rule 90:

> Proposition 2: With the exception of the trivial case, every temporal sequence
> generated by Rule 90 with arbitrary finite initial conditions on an infinite
> lattice is aperiodic. The trivial case is the temporal sequence of all 0's
> generated by Rule 90 from an initial condition that is spatially symmetric, of
> odd length, with the central component being 0.

Proposition 5 (p. 10), Rule 18:

> Proposition 5: With the exception of the trivial case, every temporal sequence
> generated by Rule 18 with arbitrary finite initial conditions on an infinite
> lattice is aperiodic. The trivial case is the temporal sequence of all 0's
> generated by Rule 18 from an initial condition that is spatially symmetric,
> with all 0-blocks of odd length, and the central component being 0.

Proposition 3, covering Rule 30, carries **no exception clause and no trivial
case**. It permits one periodic column without saying anything about whether
one exists or what it looks like. **That permitted-but-uncharacterized column
is exactly the hole row 25 closes for the constant-zero case, and row 26 for
the constant-one case.** This is the repo's existing reading and this session's
page-by-page read of the preprint confirms it verbatim.

---

## 4. The residual risk, stated precisely

### 4.1 The register's stated dichotomy is not sound as written

`PATH.md` row 72 and `PUBLICATION-NOTES.md` both assert that clause (ii) is
load-bearing in both directions and that "There is no third reading in which
clause (ii) is irrelevant." **That is too strong.** It turns on a quantifier
that the abstract does not disambiguate, and on one reading the exclusion horn
does not bite.

Clause (ii) characterizes "the classes of 'nearest-neighbor' rules for which
arbitrary finite initial conditions ... generate at least one constant temporal
sequence." Two readings of "arbitrary finite initial conditions":

- **Universal reading.** Class (ii) `= { R : for EVERY nonzero finite IC, at
  least one column is constant }`.
  Then "Rule 30 is excluded" means only: **there exists one finite IC with no
  constant column anywhere**. That is weaker than T1 in both quantifier (one IC
  vs all ICs) and locus (some column vs the centre column). It does **not**
  reproduce T1, and T1 would remain novel.
- **Existential reading.** Class (ii) `= { R : for SOME finite IC, at least one
  column is constant }`.
  Then "Rule 30 is excluded" means: no finite IC yields any constant column
  anywhere. By shift-invariance (§4.3) that **does** imply T1, and T1 would not
  be novel.

So the exclusion horn only makes row 25 non-novel under the existential
reading. **A third reading exists: clause (ii) can be simply irrelevant to
novelty.**

### 4.2 Which reading the evidence favours — universal

Three arguments, all from text that was read in the original. None is
conclusive; label the conclusion **INFERRED, not documented**.

*A note on method, because argument 2 sits close to a prohibited move.* The
standing rule is: do not infer clause (ii)'s **content** from papers that cite
Jen 1986. Nothing below does. Argument 2 uses Jen's **own** 1990 text, read in
the original, and uses it only as evidence about **grammar** — what the phrase
"arbitrary finite initial conditions" means in this author's usage — not about
what the 1986 result says. No third party's restatement of Jen is used
anywhere in this section. If that distinction is rejected, the quantifier
analysis reduces to arguments 1 and 3, which are internal to the abstract's own
sentence and to Jen 1990's contrasting exception wording, and the conclusion of
§4.1 (that a third reading exists at all) does not depend on any of the three.

1. **Parallel grammar with clause (i).** The same sentence governs both clauses
   with one occurrence of "arbitrary finite initial conditions". Clause (i),
   "evolve to a homogeneous state", is a meaningful necessary-and-sufficient
   rule class only under the universal reading (it is nilpotence on finite
   configurations). Under the existential reading clause (i) is close to
   vacuous. A single shared subject phrase carries a single quantifier.
2. **Jen's own usage of the identical phrase.** Proposition 3 (1990, p. 6)
   reads "with arbitrary finite initial conditions, there can exist at most one
   periodic temporal condition", and Figure 2's caption repeats it. That
   statement is unambiguously **universal over all nonzero finite ICs** — it is
   a theorem about every finite IC, not about the existence of one. Same
   author, same phrase, same object. This is the strongest of the three.
3. **Jen's own exception clauses are existential and are worded differently.**
   Propositions 2 and 5 do not use "arbitrary finite initial conditions" to
   express the exception; they say "the trivial case is the temporal sequence
   ... generated ... from an initial condition that is spatially symmetric ...".
   When Jen means "there exists a special IC", she names the IC.

Under the universal reading, note further that **Rule 90 would itself fail to
be in class (ii)**: its all-zero centre column requires a spatially symmetric
odd-length IC with central 0, so most finite ICs give no constant column. Class
(ii) would then be a small class (Rule 0, the identity, and similar), which is
consistent with it being a clean necessary-and-sufficient local criterion, and
inconsistent with it being a statement that could quietly contain Rule 30.

### 4.3 The inclusion horn is dead on the repo's own audited results

If clause (ii)'s characterization *included* Rule 30 under either reading, Rule
30 would have some nonzero finite IC with some constant column. The repo's
results exclude that outright:

- Row 25 (`RESULTS-zero-tail.md`): no nonzero finitely supported configuration
  has an identically zero centre trace, and the lone-seed corollary extends it
  to *eventually* zero via `F^T(delta_0)` being finite and nonzero.
- Row 26 (same file, all-one paragraph): the all-one trace forces
  `L_k = 1` iff `k` positive even, an infinite left half, so no finite row has
  constant-one trace.
- **Shift-generality.** Rule 30 commutes with the shift and finite support is
  shift-invariant, so applying row 25 to `sigma^n x` (also nonzero and finitely
  supported) excludes an identically/eventually zero column at **every** index
  `n`, not only at the centre. Same for row 26. Hence: **no nonzero finite
  Rule 30 configuration has any eventually constant column at any index.**
  This is INFERRED from the theorem as stated in `RESULTS-zero-tail.md`; the
  document states the theorem for the centre trace and does not spell out the
  shift argument. If a reviewer wants the general form, state it explicitly in
  the manuscript — it is one sentence and no new mathematics.

So the inclusion horn only fires if row 25 or row 26 is **wrong**, in which
case clause (ii) is not the problem. It has therefore been demoted from a live
exposure to a consistency check that the repo's own hostile audit already
passed.

### 4.4 What actually still blocks, named exactly

**The residual is a PRIORITY exposure, not a correctness one, and it is
accepted by decision.** Clause (ii) as the register frames it no longer blocks:
the dichotomy is refuted (§4.1), the inclusion horn is dead on the repo's own
results (§4.3), and the mathematical dependency is zero (§2). What remains is
that the body of the paper was never read, so a priority claim cannot be made
unconditionally — hence the rescoped wording in §6, which claims novelty
relative to named read sources only. **The single action that would retire the
residual is asking Eric Rowland**, who cites Jen 1986 Theorem 4 by number and
can answer the clause-(ii) question without being shown the note. Interlibrary
loan is the fallback. Neither is an agent action.

The one thing that would make row 25 non-novel is a lemma in the body of Jen
1986 that is **stronger than its abstract advertises**, of the shape:

> For rules in Class X (Class A / Class B, in the 1986 terminology that Jen
> 1990 p. 6 quotes), which includes Rule 30, no finite initial condition
> generates a constant temporal sequence.

Such a lemma would be T1 (and, with the constant-one half, row 26 too). A
weaker but still damaging shape is a lemma characterizing *which* column is the
Proposition-3 exception for each rule in the class — if it says the Rule 30
exception cannot be a constant column, that is again T1.

Nothing retrieved by this repo or this session restates any such lemma. Against
its existence, four pieces of evidence, all of which are **inference from
silence and must be labelled as such**:

1. Jen 1990 names the all-zero centre column explicitly where it exists
   (Prop. 2, Rule 90; Prop. 5, Rule 18) and gives no such statement for Rule 30
   in Prop. 3 — in her own restatement of the 1986 result, four years later.
2. Wolfram's 2019 prize page credits Jen 1986 by name for the two-column result
   while posing the single-column question as open.
3. Kopra states the width-one finite-configuration question open in 2019
   (thesis, after Thm 3.1.12) and again in 2023 (Problem 3.10, "The answer 'no'
   is expected"), having read Jen closely enough to write Corollary 3.7
   recovering her Proposition 3.
4. Rowland 2006 cites Jen 1986 by theorem number ("Theorem 4") and instantiates
   it at Rule 30, and what comes out is **diagonals**, not columns.

Three parties who read the 1986 paper behave as though it does not settle a
Rule 30 constant column. That is not a quotation and must never be written as
one.

### 4.5 Separately: Theorem 4 is discharged, and stays discharged

`PUBLICATION-NOTES.md`'s Theorem-4 analysis is unaffected by anything found
today and remains the correct reading: Rowland's `[-d,0]` normalization (his
p. 5) sends Theorem 4's "columns" to Rule 30's diagonals, and his p. 13
instantiation confirms it — "each left diagonal of rule 30 is eventually
periodic with period length a power of 2". That is A094605 / Rowland Lemma 2
territory, already recorded as prior art in `RESULTS-diagonal-periodicity.md`.
Theorem 4 is not a threat to row 25. Note also that clause (ii) speaks of
"nearest-neighbor" rules, which is Rule 30's native `[-1,1]` form, so **do not
import Rowland's `[-d,0]` normalization into clause (ii)**; whether Jen applies
it there is UNVERIFIED.

---

## 5. Retrieval record — closed, do not retry

| Route | Outcome |
|---|---|
| `doi.org/10.1007/BF01010579` | Resolves to Springer; paywalled |
| `link.springer.com/article/10.1007/BF01010579` direct | 303 to `idp.springer.com` (auth); no price numeral, no rental option shown unauthenticated |
| `r.jina.ai/https://link.springer.com/article/10.1007/BF01010579` | **PARTIAL SUCCESS.** Abstract, receipt date, pagination, 19-item reference list. No body, no headings, no theorem numbers. **This is the only route that returns anything new; it is already exhausted.** |
| OSTI `biblio/5674011` | Bibliographic record only |
| OSTI `servlets/purl/5674011` | **404.** Unlike Jen 1990, there is no LA-UR preprint for this paper |
| Semantic Scholar Graph API, `DOI:10.1007/BF01010579` | Record exists (`paperId bad9e4d1...`, CorpusId 121967511); `isOpenAccess: false`, `openAccessPdf.status: "CLOSED"`, `url: ""`, `abstract: null` (publisher-elided). **No full text** |
| fatcat / scholar.archive.org API (`api.fatcat.wiki`) | **Host unreachable**, `ECONNREFUSED 207.241.225.9:443` |
| archive.org `sim_journal-of-statistical-physics_1986*` | Item does not exist |
| HathiTrust full-text search (`babel.hathitrust.org/cgi/ls`) | **403 Forbidden** |
| arXiv / CORE / preprint archives | Predates arXiv; nothing found |
| zbMATH Zbl 0638.68043 | Truncated publisher abstract only, no independent review. **Must not be quoted** |
| MathSciNet | Paywalled; archive.org scan lending-restricted |
| Ask the author | **Impossible.** Erica Jen died 12 November 2023 (Santa Fe Institute memoriam, verified) |

**Routes never attempted, deliberately, and the only ones left:** (1) ask Eric
Rowland, who cites Theorem 4 by number and can answer the clause-(ii) question
without seeing the note; (2) public-library interlibrary loan (NYPL fills 1986
*J. Stat. Phys.* articles free for cardholders, scans capped at 50 pages or
10%); (3) Springer single-article purchase. All three require a human and are
outside an agent session. **No further automated retrieval is authorized.**

---

## 6. The rescoped novelty claim

Replace the unconditional novelty language wherever it appears with a claim
that is relative to sources actually read. Suggested wording, to be dropped
into `PUBLICATION-NOTES.md` "Defensible claim" by whoever owns that file (this
session's fence forbids editing it):

> We prove a Rule-30-specific zero-trace fiber theorem for finite
> configurations, settling the constant-zero case of Kopra's width-one
> finite-configuration eventual-periodicity question (Kopra, TUCS Diss. 249,
> 2019, stated immediately after Theorem 3.1.12), and obtain a sharp
> finite-radius escape-time law.
>
> *Novelty scope.* The theorem is new relative to the sources we read in the
> original: Jen 1990 (Physica D 45:3-18) Propositions 2, 3 and 5; Kopra 2019
> Theorem 3.1.12 and the open problem following it; Kopra 2023 (TCS 946
> 113668) Theorem 3.5, Corollary 3.7 and Problem 3.10; and Rowland 2006
> (Complex Systems 16:239-258), including his use of Jen 1986 Theorem 4, which
> under his `[-d,0]` normalization is a statement about Rule 30's diagonals.
> Jen 1986 (J. Stat. Phys. 43:219-242) we could not obtain; its abstract
> advertises a characterization of nearest-neighbour rules whose arbitrary
> finite initial conditions "generate at least one constant temporal
> sequence", and we do not know which numbered result carries it or whether
> Rule 30 falls inside or outside it. Our result does not depend on that paper
> mathematically; the exposure is to priority only.

**Attribution, unchanged and to be kept:** cite **both** Jen 1986 and Jen 1990.
Wolfram's 2019 prize page credits Jen 1986 for the two-column result; Kopra
credits Jen 1990 Proposition 3 (and his Corollary 3.7 is labelled "(Jen, [7],
Proposition 3)"). Citing a paper one has not read is normal practice *when the
citation is attributional rather than load-bearing*, which is exactly the case
here; do not quote from it, and do not attribute a specific theorem statement
to it beyond what Rowland attributes to its Theorem 4.

**Two wording rules that survive from `PUBLICATION-NOTES.md` and must not be
relaxed:** say "settles the constant-zero case of Kopra's width-one
finite-configuration question (2019 thesis, after Thm 3.1.12)", never "settles
Problem 3.10"; and do not describe the manuscript as a proof of Rule 30
centre-column nonperiodicity — nonconstant eventual periods remain open.

---

## 7. Answers to the five questions as originally posed

1. **Clause (ii) verbatim** — obtained, §1, from the publisher's own article
   page. "Necessary and sufficient conditions are derived characterizing the
   classes of 'nearest-neighbor' rules for which arbitrary finite initial
   conditions (i) evolve to a homogeneous state; (ii) generate at least one
   constant temporal sequence."
2. **Include or exclude Rule 30** — **UNRESOLVED.** No passage settles it; no
   body text was obtained. The abstract names no rule numbers. Evidence about
   the 1986 paper's structure amounts to one sentence in Jen 1990 p. 6 telling
   us it has classes named A and B.
3. **Proposition 3** — obtained verbatim with page number, §3, but it is
   **Jen 1990**, Physica D 45, preprint p. 6, not Jen 1986. The task framing
   attached it to the 1986 citation; that attribution is wrong. Jen 1990 p. 6
   describes Prop. 3 as resting on a result of `[8]` = Jen 1986, so it is Jen's
   own restatement, but the numbered 1986 result is unknown.
4. **Verdict on row 25** — see the first line of this file and §4. The
   mathematical dependency is zero; the register's two-way dichotomy is refuted
   (a third reading exists and the evidence favours it); the inclusion horn is
   dead on the repo's own results; the residual is a possible body lemma
   stronger than the abstract, which is a **priority** exposure only and is
   named as such in the rescoped claim.
5. **Read against the manuscript, not a paraphrase** — done.
   `RESULTS-zero-tail.md`, `paper/PUBLICATION-NOTES.md`, `paper/README.md`,
   `RESULTS-eventual-period.md`, `RESULTS-inverse-trace.md` and
   `RESULTS-diagonal-periodicity.md` were read in full, plus `PATH.md`
   §§0-2, 7.1-7.3, 8.0-8.7.

## 8. What remains UNVERIFIED

- The numbered result in Jen 1986 carrying abstract clause (ii). Unknown.
- Whether Rule 30 is inside or outside that characterization. Unknown.
- Whether "arbitrary finite initial conditions" in clause (ii) is universal or
  existential. INFERRED universal (§4.2), not documented.
- Whether Jen 1986 contains a body lemma stronger than its abstract that would
  imply T1. Unknown; four independent silences argue against (§4.4).
- What "Class A" and "Class B" are in the 1986 taxonomy, and whether Rule 30 is
  in them. Only their existence is attested, by Jen 1990 p. 6.
- Whether Jen 1986 applies a `[-d,0]` normalization in the clause-(ii) result.
  Unknown; the abstract says "nearest-neighbor", which is the native form.
- That `[8]` in Jen 1990 is Jen 1986: verified in the repo's prior audit from
  the scispace rendering of the reference list, **not re-verified this
  session** (the reference list is absent from the OSTI scan).
- The shift-general form of rows 25/26 (§4.3) is INFERRED from shift-invariance
  and is not written out in `RESULTS-zero-tail.md`.
- The Jen-citation sweep in §2 is complete over every source document `PATH.md`
  §7.1 names for rows 25, 26 and 72, plus `RESULTS-diagonal-periodicity.md`.
  Whether Jen 1986 is cited in the `RESULTS-*.md`, `overnight/` or `ARM*` files
  outside that tree is UNVERIFIED; it cannot affect this verdict.

# R9 / Arm A4: NEGATIVE, and the route's target metric is mis-specified. No lower bound about Rule 30 is proved here — not even `Omega(n)` asymptotically. A machine-checked resolution derivation of `c_n` of exactly `floor(3n^2/2)` steps is exhibited, so derivation length is `Theta(|F_n|)` and no lower bound over this encoding can exceed it: the best conceivable outcome of the whole route is "resolution derives `c_n` in time linear in the axioms it must read", which is the shortcut-friendly verdict, not an irreducibility one. The only sound bridge from the stored GMUS probe to derivation length is proved here as a lemma; it is system-independent (it holds for Extended Frege, so it is not measuring proof power), and it fails the Rule 90 filter — the lemma is stated and proved without reference to which rule, and on verified numbers it returns "at least 16 steps at `n=8`, at least 20 at `n=10`" for a centre column that is identically 0 after `t=0` and computable in `O(1)`.

Status: this document contains no lower-bound theorem about Rule 30.  It
contains one small unconditional lemma (the leaf-counting bound), two exact
machine-checked measurements, and a technique-by-technique account of why the
canonical proof-complexity toolbox does not reach the R9 target.  Every
missing step is named as a missing step.  No proof artifact is produced and
nothing here contains `sorry`.

Everything in section 5 that would look like a bound is capped by section 3
and disqualified by section 6, in that order.  Read those two before quoting
anything.

---

## 0. What was run

| artifact | what it establishes |
|---|---|
| `derivation_upper_bound.py`, `upper_bound.json`, `upper_bound.log` | Exact, **every-step-machine-checked** resolution derivation of the centre unit `c_n` from the light-cone CNF: `floor(3n^2/2)` steps for rule 30, `2 floor(n^2/2)` for rule 90, at `n = 4..128`.  Also the derivation/refutation equivalence at an additive cost of exactly 1 step. |
| `min_gmus.py`, `smus30.json`, `smus90.json` | `mu(n)`, the size of the **smallest** sufficient cell set (SMUS, implicit hitting set), computed exactly at small `n`.  This is the quantity the only sound bridge needs; the stored probe measured a deletion-**minimal** set, which is a different number.  Rule 30 reached `n = 8`; `n = 10` was launched with a 1200 s budget and did not complete its first band — **wall recorded, no number**. |
| `ensemble_filter.log` | Output of the repo's codified Rule 90 filter, `experiments/overnight-arms/common/ensemble_filter.py`, run as the section 5.3(b) check. |
| `leaf_bound_check.py`, `leaf_bound.log` | Mechanical check of the two side conditions of the leaf-counting lemma, and the combined lower-bound / upper-bound window table. |
| `PREREG-min-gmus.md` | Pre-registration of the `mu(n)` experiment, frozen before the first run, with kill conditions K1-K3. |

Ground truth for rule 30 is cross-checked against
`experiments/overnight-arms/common/rule30.py` (read-only import) at every band.
The CNF encoding is character-for-character the semantics of
`experiments/rule30/proof-complexity/mus_probe.py` (read-only reference), so
the numbers here compose with the stored probe.

## 1. Step 0: the satisfiability framing in PATH.md R9 is not the operative obstruction

`PATH.md` R9 states the transfer obstruction as: "Tseitin is unsatisfiable by a
global parity argument, while this instance is satisfiable with a unique
solution."  That is true of `F_n` alone but does not survive contact with the
target statement, and building on it would be an error a reviewer catches
immediately.

Let `F_n` be the light-cone CNF and `c_n` the true centre literal.  Then

* a resolution derivation of the unit `{c_n}` from `F_n` of length `L` yields a
  refutation of `F_n /\ {~c_n}` of length `L + 1` (one final resolution against
  the wrong-value unit), and
* a refutation of `F_n /\ {~c_n}` of length `L'` yields a derivation of `{c_n}`
  from `F_n` of length at most `L'` (standard restriction argument: delete the
  unit `~c_n` from the refutation and propagate, every clause gains at most the
  literal `c_n`).

The first direction is machine-checked in `derivation_upper_bound.py` (the
final resolvent is asserted to be the empty clause at every `n`).  The stored
probe's own pre-registration says the same thing from the other side: "The
formula must be UNSAT at every `n` before measurement."  The object under study
therefore **is** an unsatisfiable CNF, up to one step.  Satisfiability of `F_n`
is not what blocks the Tseitin transfer.

What blocks it is stated in section 4: the Tseitin bounds are driven by
*expansion plus `F_2`-linear global parity*, and this instance has neither.  Its
unique solution is produced by unit propagation in `Theta(n^2)` steps, which is
the exact opposite of an expander obstruction.

## 2. The machine-checked upper bound (verified quantified claim)

`derivation_upper_bound.py` constructs, for each `n`, the unit-propagation
resolution derivation of `c_n` cell by cell in topological order, and then
verifies **every individual resolution step** against its two premises and
pivot before reporting anything.  Output (`upper_bound.log`):

```text
rule 30  (every resolution step machine-checked)
     n      cells     axioms      steps  steps/n^2  steps/|F|
     4         13         59         24     1.5000     0.4068
     5         18         91         37     1.4800     0.4066
     6         25        135         54     1.5000     0.4000
     7         32        183         73     1.4898     0.3989
     8         41        243         96     1.5000     0.3951
     9         50        307        121     1.4938     0.3941
    10         61        383        150     1.5000     0.3916
    16        145        995        384     1.5000     0.3859
    32        545       4035       1536     1.5000     0.3807
    64       2113      16259       6144     1.5000     0.3779
    96       4705      36675      13824     1.5000     0.3769
   128       8321      65283      24576     1.5000     0.3765

rule 90  (every resolution step machine-checked)
     n      cells     axioms      steps  steps/n^2  steps/|F|
     4         13         34         16     1.0000     0.4706
     5         18         50         24     0.9600     0.4800
     8         41        130         64     1.0000     0.4923
     9         50        162         80     0.9877     0.4938
   ...
   128       8321      32770      16384     1.0000     0.5000
```

Exact closed forms.  These are **asserted inside the script** at every band, not
read off the table:

* variables (diamond cells) `= floor(n^2/2) + n + 1`, both rules.
* rule 30: derivation length `= floor(3n^2/2)`;
  `|F_n| = 4n^2 - 2n + 3 - 2(n mod 2)` clauses.
* rule 90: derivation length `= 2 floor(n^2/2)`;
  `|F_n| = 4 floor(n^2/2) + 2` clauses.

The derivation is unit, tree-like and regular, so it lives in the weakest
fragment of resolution.  `PATH.md` R9's assertion that "row simulation gives
`O(n^2)`-size resolution derivations" is now a checked construction with an
exact constant rather than an assertion.

## 3. The window argument: this is what actually closes the route

Three facts, all now exact:

1. `|F_n| = Theta(n^2)`.
2. Derivation length `= floor(3n^2/2) = Theta(|F_n|)` (section 2).
3. Therefore a lower bound of `omega(|F_n|)` is **impossible**, and any lower
   bound at all is capped at `floor(3n^2/2)`.

So the R9 objective, "superlinear in `n`", is the only reading with content, and
the cap is what closes it: the best conceivable outcome of the entire route is
`Theta(n^2) = Theta(|F_n|)`.  (Measured margins at the bands where both ends are
known are `UB/LB = 3.00, 3.38, 3.00` for rule 30 at `n = 4, 6, 8`; those are data
points, not the argument.  The argument is the cap.)

The deeper problem is what `length = Theta(|F|)` *means*.  A proof that is
linear in the size of its axiom set is a proof that does nothing but read its
input.  "Irreducibility" in any proof-complexity sense would have to be
`length = superpoly(|F|)`: the system cannot beat brute simulation.  Here the
system matches brute simulation exactly, which is the shortcut-friendly
verdict, not the hard one.

**This is the kill.**  The formalization is not merely hard to lower-bound; a
successful lower bound in it would not say what R9 wants it to say.

## 4. Per-technique transfer analysis

The discriminating question for each entry: *does the technique bound the
derivation of a unit clause from this CNF, or only the refutation of an
unsatisfiable instance of a particular structural kind?*  Section 1 removes
"unsatisfiable" as a distinction, so the question sharpens to: *does the
structural precondition hold here?*

Every citation below was checked against the primary source this session (ECCC
or arXiv full text where available, publisher abstract otherwise); items that
could not be verified are marked as such and are not relied on.

### 4.1 Ben-Sasson-Wigderson size-width.  **Does not transfer.  Two independent reasons.**

Eli Ben-Sasson, Avi Wigderson, "Short Proofs are Narrow — Resolution Made
Simple", STOC 1999 pp. 517-526 (doi 10.1145/301250.301392); J. ACM 48(2):149-169,
2001 (doi 10.1145/375827.375835); ECCC TR99-022.

* **Refutation only.**  The paper defines `w(F |- A)` for an arbitrary clause
  `A` (Sec 2.3, Lemma 3.1), but Theorems 3.1, 3.2 and Corollaries 3.1, 3.2 are
  stated **only for `|- 0`**, and their proofs use "a restriction of a
  refutation is a refutation", which does not transfer to deriving a general
  clause.  The width-lower-bound strategy of Sec 5 is unsatisfiability-bound by
  definition: Def 5.1 requires "A be an unsatisfiable set of boolean functions",
  Def 5.2 begins "For F a non-satisfiable CNF".  There is no BW version for
  general derivations.  By section 1 above we can convert to a refutation, so
  this reason alone is repairable — the next one is not.
* **Exponential-or-trivial, so it cannot produce the target.**  Cor 3.2 reads
  `S(F) = exp(Omega((w(F |- 0) - w(F))^2 / n))` with `n` the variable count.
  The paper itself says, verbatim immediately after Cor 3.2: *"If `w(F) ~
  #Variables`, corollaries 3.1, 3.2 are useless for obtaining lower bounds."*
  To extract a merely polynomial `S >= n^{1.5}` one needs a width bound of
  `Theta(sqrt(n log n))`, and that band has no known instantiation; Bonet and
  Galesi exhibit a family with polynomial size and width `Omega(sqrt n)`, where
  Cor 3.2 yields only `exp(Omega(1))` (Bonet, Galesi, "Optimality of size-width
  tradeoffs for resolution", Comput. Complex. 10(4):261-276, 2001, doi
  10.1007/s000370100000).  Here `|F_n|` has `Theta(n^2)` variables and the
  derivation exists at length `3n^2/2`, so the true size is *polynomial*; BW is
  in exactly the regime it declares useless.

### 4.2 Dantchev-Riis.  **Structural precondition absent; and the bound is `2^Omega(sqrt(variables))`.**

The FOCS 2001 paper is S. Dantchev, S. Riis, **"'Planar' tautologies hard for
resolution"**, FOCS 2001 pp. 220-229, doi 10.1109/SFCS.2001.959896.  (`PATH.md`
R9 cites "Dantchev-Riis FOCS 2001 `2^Omega(n)` resolution"; that is this paper.
Their weak-pigeonhole tree-resolution paper is a different, earlier work.)
Abstract, verbatim: *"We prove exponential lower bounds on the resolution proofs
of some tautologies, based on rectangular grid graphs... a `2^Omega(n)` lower
bound for any resolution proof of the mutilated chessboard problem on a
`2n x 2n` chessboard as well as for the Tseitin tautology... based on the
`n x n` rectangular grid graph."*

* The instances are **unsatisfiable**: Tseitin with odd total charge is
  unsatisfiable by the handshake lemma, as is the mutilated chessboard.
* **Parameterization, easy to misread:** `n` is the grid *side*, so the
  `n x n` grid has `Theta(n^2)` edge variables and the bound is
  `2^Omega(sqrt(N))` in the variable count `N`.  Our formula also has
  `Theta(n^2)` variables, so a literal transfer would claim
  `2^Omega(n)` — flatly contradicted by the `3n^2/2` derivation of section 2.
  The transfer therefore cannot hold, and the question is only which hypothesis
  fails.
* **Which hypothesis fails.**  It is *not* satisfiability (section 1).  It is
  the `F_2`-linear global-charge structure: Tseitin's hardness comes from a
  parity invariant that no local reasoning can see.  Our instance has a *unique*
  solution reachable by unit propagation in `Theta(n^2)` steps; there is no
  parity invariant to hide, and no clause of `F_n` is ever "globally" needed in
  the Tseitin sense.
* **Flagged unverified:** the paper's *proof mechanism* could not be retrieved
  (Leicester copy 404, Durham repository 403).  This document therefore does
  **not** assert "expansion plus parity" as the mechanism.  Note that the `n x n`
  grid is a poor expander (`Theta(n) = Theta(sqrt N)` edge expansion), which is
  precisely why plain BW expansion does not yield this result.

### 4.3 Hastad 2021 and Hastad-Risse 2022.  **Same unsatisfiable Tseitin instances; bounded-depth Frege, not resolution derivation.**

Johan Hastad, "On Small-Depth Frege Proofs for Tseitin for Grids", FOCS 2017 pp.
97-108 (doi 10.1109/FOCS.2017.18); **J. ACM 68(1) Article 1, 2021** (doi
10.1145/3425606); ECCC TR17-142.  Published abstract, verbatim: *"We prove a
lower bound on the size of a small depth Frege refutation of the Tseitin
contradiction on the grid."*  The ECCC text is explicit that the instance is a
contradiction: *"the formula says that the edges adjacent to a node sum to one
modulo two.  For any odd sized graph this is a contradiction."*  Quantitatively
`exp(Omega(n^{1/58(d+1)}))` in ECCC; Hastad-Risse quote the published figure as
`n^{1/59d}` (discrepancy flagged, not resolved here).

Johan Hastad, Kilian Risse, "On bounded depth proofs for Tseitin formulas on the
grid; revisited", FOCS 2022 pp. 1138-1149 (doi 10.1109/FOCS54457.2022.00110);
SIAM J. Comput. 54 (2025) S22-288 (doi 10.1137/22M153851X); arXiv:2209.05839.
Improves the depth-`d` bound to `exp(Omega~(n/(log M)^{O(d)}))`-shape via a
multi-switching lemma.

Both bound **refutations** of the same unsatisfiable odd-charge Tseitin
formulas.  The satisfiability objection is again repairable by section 1; the
`F_2`-linear-invariant objection of 4.2 is not, and applies verbatim.  These are
also depth-`d` Frege bounds, a different system from the resolution derivation
R9 targets.

### 4.4 Pebbling.  **Category error for size: pebbling formulas have LINEAR-size refutations, and the results are about space.**

* Pebbling contradictions are **linear-size** in resolution.  Ben-Sasson and
  Wigderson themselves state it (ECCC TR99-022 Def 7.1 and Lemma 7.1):
  `Peb(G)` is "a non-satisfiable 4-CNF over `2|V|` variables, with `O(|V|)`
  clauses", and `S(Peb_G) = O(|V|)` with `w(Peb_G |- 0) <= 6`.  Invoking
  pebbling for a *size* lower bound is therefore backwards: the canonical
  pebbling formulas are the standard example of *short* refutations.
* The genuine pebbling results are **space** and **size/space trade-off**
  results.  Eli Ben-Sasson, Jakob Nordstrom, "Short Proofs May Be Spacious: An
  Optimal Separation of Space and Length in Resolution", FOCS 2008 pp. 709-718
  (doi 10.1109/FOCS.2008.42): 6-CNF families with refutations of length `O(n)`
  that require space `Omega(n / log n)`.  Jakob Nordstrom, "Pebble Games, Proof
  Complexity, and Time-Space Trade-offs", LMCS 9(3):15, 2013 (doi
  10.2168/LMCS-9(3:15)2013), whose abstract is explicit: *"with a focus on proof
  space lower bounds and trade-offs between proof size and proof space."*  The
  foundational resolution-space papers are Esteban-Toran (Inform. and Comput.
  171(1):84-97, 2001, doi 10.1006/inco.2001.2921) and
  Alekhnovich-Ben-Sasson-Razborov-Wigderson (SIAM J. Comput. 31(4):1184-1211,
  2002, doi 10.1137/S0097539700366735) — *not* Ben-Sasson-Wigderson, which
  contributes only the tree-like separation `S_D(Peb_G) = 2^Omega(P(G))`.
* **Unsatisfiability is built into the construction** (source axioms assert
  pebbles at the sources, target axioms deny them at the target), so pebbling
  formulas are not a satisfiable-instance technique either.
* The honest pivot this leaves: **space, not size, is the measure with content
  in a pebbling-like regime.**  The section-2 derivation is `Theta(n^2)` in
  length; its *space* (the peak number of simultaneously live clauses) is a
  separate and unmeasured quantity.  A space lower bound would still not be the
  R9 target, which is stated as a length bound, and this document does not
  pursue it.

### 4.5 Polynomial calculus size-degree.  **Same exponential-or-trivial shape; refutations only; and the degree theorem it would be fed is inert.**

Russell Impagliazzo, Pavel Pudlak, Jiri Sgall, "Lower Bounds for the Polynomial
Calculus and the Groebner Basis Algorithm", Comput. Complex. 8(2):127-144, 1999
(doi 10.1007/s000370050024); ECCC TR97-042.  Cor 5.3, verbatim: *"For any set of
inconsistent constant degree polynomials, if `d` is the minimum degree of a
polynomial calculus refutation, and `M` is the minimal number of non-zero
monomials in such a refutation, then `M >= 2^{Omega(d^2/n)}`."*

* The published exponent is `d^2/n`, not `(d - d_0)^2/n` — Cor 5.3 hypothesizes
  constant initial degree, which absorbs `d_0`.
* "inconsistent" = **unsatisfiable**, and `M` counts monomials in a
  **refutation**.
* Same exponential-or-trivial shape as BW, and BW says so (intro: *"identical
  functional relations as those we obtain for width vs. size, appear in
  [CEI96]"*).  With `n = Theta(n^2)` variables here and a polynomial-size proof
  known to exist, this is again the useless regime.
* `P3_ASSESSMENT.md` suggests the ANF degree theorem `deg f_t = 2t-1` might feed
  a PC degree bound.  **That step is a second missing lemma, not an available
  one.**  `deg f_t` is the `F_2`-degree of the arbitrary-input centre function
  on `2t+1` variables — `PATH.md` row 43 records its own write-up calling it
  "provably inert" for P3 — whereas Cor 5.3's `d` is the minimum PC *refutation*
  degree of the fixed lone-seed instance.  No implication between the two is
  known to this document, and none is assumed.

### 4.6 Is there any technique for superlinear derivation length from a satisfiable CNF?  **None located.**

* The one framework that explicitly extends resolution hardness measures to
  satisfiable clause-sets is Olaf Beyersdorff, Oliver Kullmann, "Unified
  Characterisations of Resolution Hardness Measures", SAT 2014, LNCS 8561 pp.
  170-187 (doi 10.1007/978-3-319-09284-3_13); arXiv:1310.7627.  Verbatim, Sec
  1.4: *"These measures do not just apply to unsatisfiable clause-sets, but are
  extended to satisfiable clause-sets, taking a worst-case approach over all
  unsatisfiable sub-instances obtained by applying partial assignments
  (instantiations), or, equivalently, the maximal complexity to derive any
  (prime) implicate."*  **The measures they treat are depth, hardness,
  symmetric and asymmetric width, and three space measures.  Derivation length
  is not among them**, and the extension mechanism is reduction to an
  unsatisfiable instantiation — the same route as section 1, with the same
  `O(n^2)` ceiling waiting at the end of it.
* The superlinear-but-subexponential *refutation*-size regime does exist and is
  achieved, but for regular resolution on unsatisfiable instances: Atserias,
  Bonacina, de Rezende, Lauria, Nordstrom, Razborov, "Clique Is Hard on Average
  for Regular Resolution", J. ACM 68(4):23, 2021 (doi 10.1145/3449352; STOC
  2018; arXiv:2012.09476), giving `n^{Omega(k)}` for `k << n^{1/4}`.
* Buss-Pudlak, "How to Lie Without Being (Easily) Convicted and the Length of
  Proofs in Propositional Calculus", CSL 1994, LNCS 933 pp. 151-162 (doi
  10.1007/BFb0022253), is a **Frege**-length paper, not a satisfiable-derivation
  paper.  (Content secondary-sourced; flagged.)
* **Reported honestly as a negative retrieval, not a proof of absence:** no
  technique for superlinear lower bounds on the derivation length of a unit
  clause from a satisfiable CNF was located.  `PATH.md` R9's phrasing — "an
  implicational/pebbling-like regime where superlinear resolution bounds barely
  exist" — is corroborated, and 4.4 sharpens it: in the pebbling regime the
  known refutations are *linear*.

### 4.7 The proof-complexity-meets-CA prior art.  **Verified; both are about inversion and both route through UNSAT.**

* arXiv:2604.01041 **exists** (verified against the arXiv API and OpenAlex, not
  taken from the register on trust): Maryia Kapytka, "Lower Bounds on Inverse
  Cellular Automata via Proof Complexity", arXiv:2604.01041v1, 2026-04-01,
  math.LO / cs.DM / cs.LO.  Abstract, verbatim in part: *"Deciding injectivity
  in this setting is co-NP-complete by a theorem of Durand.  We give a simpler
  proof of this theorem by a direct reduction from UNSAT... we prove lower
  bounds on their size.  The proof uses known lower bounds for bounded-depth
  Frege systems together with the Paris-Wilkie translation."*  Injectivity, not
  prediction; and the reduction is *from UNSAT*, so it inherits every
  unsatisfiability precondition above.
* Stefano Cavagnetto, "Propositional Proof Complexity and Cellular Automata", in
  *Cellular Automata — Simplicity Behind Complexity*, ed. A. Salcido,
  IntechOpen, 11 April 2011, doi 10.5772/16030 — a **book chapter**, and the
  work Kapytka's abstract cites as "cf. Cavagnetto".  `PATH.md` R9's assessment
  that this is the whole of the prior art, and that neither touches prediction,
  is confirmed.

### 4.8 Summary table

| technique | bounds derivation of a unit clause from a satisfiable CNF? | why it does not reach the R9 target here |
|---|---|---|
| Ben-Sasson-Wigderson size-width | No — refutation only (Thms 3.1/3.2, Defs 5.1/5.2) | Exponential-or-trivial; the paper's own "useless" regime, and a polynomial-size proof exists |
| Dantchev-Riis FOCS 2001 | No — unsatisfiable grid Tseitin / mutilated chessboard | Needs an `F_2` global-charge invariant; this instance has a unique unit-propagated solution.  Bound is `2^Omega(sqrt(vars))` and is contradicted here by the `3n^2/2` construction |
| Hastad JACM 2021, Hastad-Risse FOCS 2022 | No — refutations of odd-charge Tseitin | Same invariant missing; also bounded-depth Frege, not resolution derivation |
| Pebbling | No — pebbling contradictions are unsatisfiable **and have `O(|V|)`-size refutations** | Category error for size; the real results are space and size/space trade-offs |
| PC size-degree (IPS Cor 5.3) | No — "inconsistent" polynomials, refutation monomials | Exponential-or-trivial, `2^{Omega(d^2/n)}`; and ANF-degree -> PC-refutation-degree is an unproved second lemma |
| Beyersdorff-Kullmann satisfiable-clause-set measures | Extends to satisfiable clause-sets, **but length is not one of the measures** | Reduces to an unsatisfiable instantiation; no length measure offered |

## 5. The one sound bridge, proved, and why it does not rescue the route

### 5.1 Leaf-counting lemma (unconditional; proved and checked here)

Let `mu(n)` be the size of the **smallest** set `G` of rule-bearing cells of the
diamond `D_n` such that enforcing the rule exactly on `G` (all other cells free)
together with the seed unit implies `c_n`.

> **Lemma.**  Every resolution derivation of `{c_n}` from `F_n` has length at
> least `mu(n) - 1`.

*Proof.*  Let `S` be the set of axiom clauses appearing as leaves, and `G(S)`
the cells they touch.  (i) Distinct cells own disjoint axiom clauses, so
`|S| >= |G(S)|`; this is mechanically checked for every `n` in the table by
`leaf_bound_check.py`.  (ii) `S` is contained in the full clause set of `G(S)`,
so that clause set also implies `c_n`, i.e. `G(S)` is sufficient and
`|G(S)| >= mu(n)`.  (iii) A DAG with binary inferences, `L` distinct leaves and
one root has `I` internal nodes with edges `2I` and nodes `L + I`; connectivity
forces `2I >= L + I - 1`, so `I >= L - 1`.  Chaining: length `>= |S| - 1 >=
mu(n) - 1`.  QED

This is the only step in the whole arm that legitimately connects the stored
GMUS probe's subject matter to derivation length, and it connects it to
`mu(n)`, **not** to the deletion-minimal number the probe measured.

### 5.2 `mu(n)` measured exactly (K1 did not fire)

`min_gmus.py` computes `mu(n)` by implicit hitting-set SMUS.  Pre-registered in
`PREREG-min-gmus.md` before the first run.

```text
rule 30   n=4 ground=12 mu=9 (0.0s)   n=6 ground=24 mu=17 (0.1s)
          n=8 ground=40 mu=33 (17.1s, 997 hitting-set iterations)
          n=10 ground=60 -- did not complete its first band inside 1200 s.  WALL.
rule 90   n=4 mu=7   n=6 mu=9   n=8 mu=17   n=10 mu=21   n=12 mu=25
```

**Rule 90 control passes exactly.**  `mu_90(n)` equals the analytic odd-binomial
(Sierpinski) set size at *every* computed band — 7, 9, 17, 21, 25 against the
analytic 7, 9, 17, 21, 25 recomputed from
`experiments/rule30/proof-complexity/mus_probe.py:rule90_odd_set`.  The stored
probe asserts (from linearity, and it is an assertion there, not a proof) that
the rule 90 GMUS is *unique*, hence minimal = minimum; this run verifies that
identification as a **minimum** for `n <= 12`, which the stored deletion-based
ladder could not do.

For rule 30, `mu(8) = 33` coincides with the stored probe's `mus_min = 33` at
`n = 8`: at that band the deletion-minimal set happened to be minimum.  The
inverted outcome K1 did **not** fire at the computable bands.  Note that the
computable bands are `n <= 8`; `mu(n)` is `Sigma_2^p`-hard and the wall arrived
immediately after.

Combined window (`leaf_bound.log`):

```text
rule 30      n     cells     axioms   LB=mu-1   UB=steps   UB/LB
             4        13         59         8         24    3.00
             6        25        135        16         54    3.38
             8        41        243        32         96    3.00
rule 90      4        13         34         6         16    2.67
             6        25         74         8         36    4.50
             8        41        130        16         64    4.00
            10        61        202        20        100    5.00
```

### 5.3 Why this is not the R9 result, four independent reasons

**(a) It is finite data, and for Rule 30 no asymptotic bound of any kind
follows — not even `Omega(n)`.**  `mu(n)` is computed exactly at `n = 4, 6, 8`
for rule 30 and nowhere else; `n = 10` hit the wall.  What is proved for Rule 30
is therefore: *any resolution derivation of `c_8` from `F_8` has at least 32
steps.*  That is the whole of it.  `mu(n) = omega(n)` is unproved, and no
asymptotic rate is claimed.  This is `PATH.md` obstruction H exactly: finite data
cannot establish an infinite statement.  Computing `mu(n)` is `Sigma_2^p`-hard.

**(b) It fails the Rule 90 filter, in the strongest possible form (K2 fired).**
The repo's codified filter is `experiments/overnight-arms/common/ensemble_filter.py`;
run here (`ensemble_filter.log`), it reports:

```text
rule 90: ones in first 20000 = 1 (density 0.0001); nonzero t>0: none
   prefix: 1000000000000000000000000000000000000000
rule 30: ones in first 20000 = 10120 (density 0.5060); nonzero t>0: 10119
```

The filter's check is: does the argument apply verbatim to Rule 90, where the
lone-seed centre column is `1, 0, 0, 0, ...` — eventually constant, density 0,
and computable in `O(1)` time for every `n`?  For the leaf-counting lemma the
answer is yes, and worse than yes:

* **The lemma applies verbatim.**  Its statement and proof (5.1) mention no rule
  at all; they use only the diamond's clause-to-cell injectivity, which is
  checked for rule 90 at every band in `leaf_bound.log`.  That is what the filter
  asks, and the answer is yes.
* **On verified numbers**, for rule 90 the lemma proves: any resolution
  derivation of `c_8` has `>= 16` steps, and of `c_10` has `>= 20` steps — for a
  bit that is identically 0 and computable in constant time for every `n`.

**Symmetry of scope, stated deliberately: neither rule gets an asymptotic bound
here.**  The stored probe asserts (from linearity; it is an assertion there, not
a proof, and this document does not re-prove it) that the rule 90 GMUS is
*unique*, which would give `mu_90(n) = Theta(n^{log2 3}) = Theta(n^{1.585})` and
hence a genuinely superlinear bound for the control.  **That is an inherited
unproved premise and is not used as a step anywhere.**  What is verified here is
`mu_90(n)` as the *minimum* for `n <= 12` only; the analytic odd-binomial count
by itself is merely a sufficient set, i.e. an *upper* bound on `mu_90`, and K2
does not need it.

The finite-`n` form is already decisive about the metric.  It is not a paradox —
resolution derivation length from a `Theta(n^2)`-clause encoding is not
algorithmic cost — but **R9's target, "a lower bound on derivation length", is
met on the control, by axiom counting alone, for a problem with no computational
content whatsoever.**  The target metric is therefore not a proxy for
computational effort, and the arm's objective as stated is mis-specified.  The
lemma is insensitive to the OR nonlinearity; it sees only how many axioms must be
mentioned.

**(c) It is system-independent, so it is not a proof-complexity bound.**  The
argument uses nothing about resolution beyond two properties: *each inference has
at most two premises*, and *each input axiom used occupies its own line*.  (State
the precondition, because a system with unbounded-arity rules breaks the DAG
count.)  Resolution, polynomial calculus, bounded-depth Frege and **Extended
Frege** all have both properties, so the bound holds verbatim in all of them.  A
bound that Extended Frege cannot beat is not measuring proof power; it is the
proof-complexity analogue of "the algorithm must read its input".  It cannot
distinguish an irreducible problem from a trivial one.

**(d) It is capped by section 3.**  Even in the best case it yields
`Theta(n^2)`, and the exhibited derivation is `floor(3n^2/2)`.  The outcome of
the whole programme, fully successful, is "resolution derivation length for this
CNF is `Theta(n^2)`", i.e. `Theta(|F_n|)`, i.e. **optimal**, i.e. the opposite of
irreducible.

## 6. Why no bound over this encoding can address Problem 3

Prize Problem 3 asks for the computational effort of computing `c_n` given `n`,
on a Turing machine receiving `n` **in digit form** (`PREREGISTRATION.md`), i.e.
an input of `Theta(log n)` bits.  The naive algorithm costs `Theta(n^2)`, which
is exponential in the input length, and the open question is whether anything
beats it.

The light-cone CNF `F_n` has `Theta(n^2)` clauses.  **Writing the formula down
already costs as much as running the naive algorithm.**  The encoding presents
`n` in unary.  Consequently:

* Any derivation-length lower bound over `F_n` is at most `floor(3n^2/2)` (section 3),
  i.e. at most the naive cost.  It can never separate anything.
* A formalization with content for P3 would need a **succinct** encoding of the
  statement "`c_n = 1`" of size `poly(log n)`, and a superpolynomial
  derivation-length lower bound over it.  Over succinct encodings, systems with
  extension simulate fast algorithms, so such a bound would imply circuit lower
  bounds.  This is `PATH.md` R9's own standing gap, and it is the reason it must
  be quoted in the same sentence as any result here: **a proof-complexity bound
  over the light-cone CNF does not resolve Wolfram's Turing-machine formulation
  of Problem 3, and the specific reason is that the encoding is unary in `n`.**

## 7. Obstruction G check, shown rather than asserted

`PATH.md` 7.3 obstruction G: P3 fixes the input to the lone seed and varies only
`n`; circuit size, decision-tree depth, sensitivity, certificate complexity and
algebraic immunity are measures of a function of *variable* inputs and are
identically zero on one fixed point.  Row 9 is "the framing built to evade it".

**Does derivation length actually evade G?  Yes, and here is the check.**

* The quantity is defined per fixed `n` on one fixed formula `F_n`.  There is no
  input distribution and no variable input; the seed is a unit *axiom* of `F_n`,
  not an argument.
* The degenerate collapse that kills the circuit measures is: on a single fixed
  point the function is a constant and the measure is `0`.  The analogous test
  here is whether the derivation-length quantity is `0` (or constant) for all
  `n`.  It is not: `leaf_bound.log` gives `>= 8` at `n = 4` and `>= 32` at
  `n = 8`, and the exhibited derivations are `24` and `96`.  Both bounds grow.
* `F_n` has exactly one satisfying assignment, produced by unit propagation, and
  the derivation in section 2 *is* that propagation; the quantity is nonzero
  because it counts inference steps on a fixed instance, not variation of an
  output under input perturbation.

So G is genuinely evaded.  **The honest counterweight, in the same breath:** the
unique solution is computable in `O(n^2)`, so the quantity that evades G is
bounded above by the naive simulation cost, which is exactly the trap of
section 6.  Evading G buys a nontrivial question; it does not buy a question
about Problem 3.

**And note where it lands.**  What derivation length evades G *into* is
obstruction B: the quantity is rule-blind (5.3(b)), so escaping the
arbitrary-input trap costs exactly the rule discrimination the route needed.  The
two obstructions are not independent here; they are the two ends of one squeeze.

## 8. What is actually missing, named as open problems

Neither of these is assumed anywhere above.  They are stated as the named gaps
that would be required, in the sense `PATH.md` obstruction D demands.

* **Open problem A (the minimum-MUS conjecture).**  Prove `mu(n) = omega(n)` for
  Rule 30's light-cone CNF, where `mu(n)` is the smallest sufficient cell set.
  Measured exactly only for `n <= 8` here.  Even if proved, it is disqualified
  by 5.3(b), (c) and (d); it is listed because it is the only sound bridge and a
  reader should know its status is "open and insufficient", not "assumed".
* **Open problem B (the succinct-encoding lower bound).**  Exhibit an encoding
  of "`c_n = 1`" of size `poly(log n)` and prove a superpolynomial
  derivation-length lower bound over it in resolution or polynomial calculus.
  This is what a genuine formalization of P3 as proof complexity requires.  No
  technique in section 4 approaches it, and over systems with extension it
  implies circuit lower bounds.

No step of this document has the form "under an appropriate lifting /
composition / uniformity lemma".  Where such a step would have been needed, the
lemma is named above as an open problem and the corresponding claim is not made.

## 9. What a reader must not over-read

* **The 76-82% diamond fill and the fitted exponent 1.932 from
  `RESULTS-proof-complexity-probe.md` are a precondition (axiom necessity in the
  deletion-minimal sense), not a lower bound and not evidence of one**; a formula
  can require every axiom and still have a linear derivation, and section 2
  exhibits precisely such a derivation for this formula.  They appear nowhere in
  this document as a bound.
* `mu(8) = 33` is a lower bound of 32 steps at `n = 8` **only**.  It is not an
  asymptotic statement.  **No asymptotic derivation-length lower bound for Rule
  30 is proved anywhere in this document, not even `Omega(n)`.**
* The leaf-counting lemma is a real unconditional lemma and a shallow one.  It
  must never be reported as a proof-complexity lower bound for Rule 30, because
  it holds for Extended Frege and for Rule 90 alike.
* The Rule 90 material in 5.3(b) is **not** a claim that Rule 90 is hard.  It is
  the demonstration that the metric is empty: the same lemma delivers a lower
  bound for a centre column that is constant 0.  Quoting it as a hardness result
  about Rule 90 would invert its purpose.
* The `Theta(n^{1.585})` figure for `mu_90` is the **stored document's analytic
  count of the odd-binomial set**, quoted.  By itself that set is only
  *sufficient*, i.e. an upper bound on `mu_90(n)`; turning it into a lower bound
  needs the stored uniqueness assertion, which is inherited and not re-proved
  here.  `mu_90(n)` is verified as the minimum only for `n <= 12`.  No asymptotic
  derivation-length lower bound is proved here for **either** rule.
* `PATH.md` R9's stated obstruction ("Tseitin is unsatisfiable... while this
  instance is satisfiable") is corrected in section 1: satisfiability is not the
  operative obstruction, since derivation and refutation here differ by one step.
  The operative obstructions are the absent `F_2` global invariant (4.2) and the
  exponential-or-trivial shape of every size-from-width/degree relation (4.1,
  4.5).
* Nothing here bears on P1 or P2.
* Nothing here bears on Wolfram's Problem 3 in its Turing-machine formulation,
  for the reason given in section 6.

## Reproduction

```sh
cd experiments/overnight-arms/frontier_attack/a4_p3_resolution
uv run python derivation_upper_bound.py --ns 4 5 6 7 8 9 10 16 32 64 96 128 \
    --out upper_bound.json
uv run python min_gmus.py --rule 30 --ns 4 6 8 --budget 240 --out smus30.json
uv run python min_gmus.py --rule 90 --ns 4 6 8 10 12 --budget 600 --out smus90.json
uv run python leaf_bound_check.py
uv run python ../../common/ensemble_filter.py
# rule 30 n=10: `min_gmus.py --rule 30 --ns 10 --budget 1200` did not complete
# its first band.  Reported as a wall, not as a number.
```

Modal: $0.  Paid model-provider calls: $0.

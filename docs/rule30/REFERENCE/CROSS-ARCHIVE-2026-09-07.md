# What the whole archive has in common, and what that rules in

Date: 2026-09-07.  Companion to `EXPERIMENT-ATLAS.md`, which compares
experiments item by item; this reads the register for a single cause, and then
asks what technique classes the cause leaves open.

Nothing here is a theorem.  Sections 1 and 2 are re-readings of results already
in the archive; section 3 names methodological priors that are load-bearing and
may be wrong; section 4 is the literature transfer; section 5 is the ranked
work with kill conditions.

## 1. One cause under roughly fifteen kills

Take the killed mechanisms from `FACT-INDEX.md` ("exact negative certificates")
and `EXPERIMENT-ATLAS.md` 6.1--6.3: fixed-local additive energies; finite
modular and local quotients; fixed Hasse and mixed moments; carry contraction
and the carry action quotient; bounded RLE summaries; signed imbalance and
contact counts; hard-core plus `D8` action; the queue end-window phase no-go;
the syntactic monoid quotient; paired divergence invariants; the Lyapunov
potential search; holonomy defect closure; the cofactor automaton; time-ordered
pivot emission; pointwise derivative, rank, and bounded-jump certificates.

Fifteen experiments, fifteen separate falsifiers, one mechanism.  Each proposes
a **bounded summary of a growing ordered object** and each dies to a collision:
two states with equal summary and different futures.

*Credit where it is due:* this is not a new observation.
`p1-period2-invariant/PROOF-STATE-CAPSULE.md` section 5 already closes its own
kill table with "All these failures have the same cause: a growing ordered
dependency diagonal stores phase in long gaps.  A bounded annotation loses it;
a complete state transports it reversibly and grows."  What is added here is
three things: that the cause is now a **theorem** rather than a pattern, that
it sorts the *whole* register and not only the period-two sublist, and that its
useful half is positive rather than cautionary.

The theorem:

> `RESULTS-SYNTACTIC-MONOID-INJECTIVITY-PROOF.md`: the right congruence induced
> by the queue block scan is the identity, so the block monoid is **free** on
> three generators.  No lossless bounded summary exists at any radius.

The proof is two finite checks: every symbol acts as a **permutation** of the
four scan states, and distinct symbols act differently somewhere.  Permutations
do not forget.  `EXPERIMENT-ATLAS.md` 7.1 records the same fact from the other
side — "raw formula/DFA rank expands because information is not being
forgotten" — and draws a caution from it. The consequence is limited to
reconstructing that scan's full output:

> **Standing screen (lossless bounded summaries; corrected 2026-09-15).**
> A bounded summary cannot reproduce the complete intermediate queue trace
> for every block and entering state. The cited proof explicitly leaves
> lossy target-specific summaries and whole-queue summaries untouched
> (section 6). Injectivity alone does not forbid a decreasing rank or a
> guarded termination argument. Reject a proposed certificate only when its
> required information and hypotheses match a proved excluded class.

The inverse is the usable half.  Injectivity is not only an obstruction; it is
a supply of **exact size**.  A map that forgets nothing has images as large as
its domains, which is a counting hypothesis, not a monotonicity one.  Every
route that has produced a uniform (`U`) result in this archive — the zero-tail
classification, the rotated Peel identity, the rank-zero reduction, the
injectivity proof itself, the rung-2 realizability corollary — is an identity
or a counting statement.  Every route that has produced only `K` is a
contraction.  That split is exact across the register and is the single most
predictive feature in it.

## 2. The second correlation: the archive works only in the disordered region

Routes R1--R9 and rows 1--93 all take as their object the centre column, an
adjacent column, a same-orbit defect, or a queue derived from one of those.
Every one lives at or near `x = 0`.

`RESULTS-ordered-wedge-glide.md` (this session) measures the other region: an
exact left light-cone recurrence whose OR is absorbing, a glide form
`s(t+g,x-g) = s(t,x)` of its periodicity, and a rule 90 control that destroys
both.  The archive had never taken that region as an object; the archive's one
frame-change document, `RESULTS-diagonal-periodicity.md`, examines the right
cone and closes R4 on what it finds there.

Two qualifications, both important, and the second is the more instructive.

**The phenomenon is prior art.**  NKS p. 871 already records the left-edge
period doubling and its depths `3, 8, 29, 400, 87867, >2.1e9`.  What is new
here is the recurrence, the glide form, the rule 90 split, and an independent
reproduction of that table to the unit.  The blind spot was real but it was a
blind spot about *our own* reading of the literature as much as about the
diagram.

**The first draft turned a horizon into a law.**  It scanned to `j = 65,536`,
found period 16 throughout, and proposed "period 16 for every `j`" as a proof
target.  The plateau ends at `87,867`.  The value that would have caught it was
published, and this repository already cited the same page two lines away in
`PATH.md:269`.  So section 1's screen has a sibling worth stating with it:

> **Standing screen (horizon).**  Before a scan's flat region becomes a
> conjecture, find the published or predicted scale of the next event and check
> whether the scan reached it.  Obstruction H is usually invoked against
> certificates; it bites hardest against *plateaus*, which look like theorems
> and cost nothing to state.

## 3. Priors that are load-bearing and may be wrong

**3.1 "Use Rule 30's OR" reads the OR as the source of hardness.**  In the left
light-cone frame the recurrence is
`L_j[t] = L_{j-2}[t-1] XOR (L_{j-1}[t-1] OR L_j[t-1])`, the OR is **absorbing**,
and it is precisely what makes the period grow so slowly there — one doubling
between depth 400 and depth 87,867 — while the right frame's XOR-carried parity
doubles every `2.4` steps of depth and passes 4096 by `j = 64`.
The OR is the source of order on one side and of hardness on the other.  The
screen should ask which branch of the OR a proposal consumes — the saturating
branch or the open one — not merely whether it mentions the gate.

The cost of not asking it precisely enough is on the record.  The one-column
reach lemma of `NEXT-DIRECTIONS-post-rung2.md` section 1 was **retracted on
2026-09-07**: its proof saturated the OR in
`col_{-1}(t+1) = col_{-2}(t) XOR (col_{-1}(t) OR c(t))` by checking
`col_{-1}(t)` and never checking `c(t)`, which saturates it equally and is part
of the centre column.  The centre in fact forces `col_{-k}(t)` along any run of
`k` ones, so the reach is `O(log t)`, not 1.  The lemma had been re-verified
the same day — but only its *identities* were re-run, not its *argument*, and
its own corroborating measurement encoded the same wrong criterion.  That is
the sharpest instance in this archive of a general hazard: a measurement built
from a claim cannot test the claim.

> **Standing screen (self-corroboration).**  If a check was written from the
> same statement it is checking, it can only confirm.  A negative result whose
> criterion is the claim's own definition is not evidence.  Get the criterion
> from the rule, or from an enumeration that does not know the claim.

**3.2 Obstruction A is stated rule-wide and is a right-boundary fact.**
`FACT-INDEX.md` gives it as "`O(log t)` propagation cannot meet a `Theta(t)`
target".  The right frame reaches depth `~2.4 log2 P` with period `P`; the left
frame reaches `3, 8, 29, 400, 87867, >2.1e9` for `P = 2..64`, super-exponential
in `log P`.  A's quantitative claim is false on the left.  Its *verdict*
survives — both still demand unbounded period at depth `Theta(t)` — so the
correction is to A's rate, not a new obstruction.  An earlier version of this
memo proposed a screen "J" asserting the ordered region's slope is independent
of the glide length; that was a finite-horizon artifact and is withdrawn.  See
`RESULTS-ordered-wedge-glide.md` sections 3 and 6.

**3.3 The archive generalises away from the lone seed while complaining that
others do.**  Obstruction E rejects ensemble results for missing the lone-seed
orbit.  Meanwhile the live P1 chain runs through the same-orbit reduction to
"every nonzero finite row", and then to the constant-tail queue, which
`EXPERIMENT-ATLAS.md` 6.3 concedes "is stronger than the seed-derived statement
because its middle word is arbitrary".  Strengthening is not free: it discards
the finite-support hypothesis whose absence obstruction E is about.  The wedge
is a lone-seed-specific object; the interface position `0.252 t` is a property
of *this* orbit and of no ensemble.

**3.4 "Prefer a finite human-checkable certificate" against obstruction H.**
`START-HERE.md` step 7 and obstruction H pull opposite ways, and the register
shows which won: dozens of `C` results at lengths 20--23 and no `U` result on
any open problem.  A finite verification of a numerical *bound* has no route to
an induction.  A finite verification of a *symmetry* does, because a symmetry
states what to induct on.  That is the only methodological difference between
the wedge measurement and, say, the zero-prefix greedy lemma verified to length
23, and it is why the former is worth a proof attempt.

**3.5 The prize names the centre column; that is not a reason to work there.**
Sections 1 and 2 are the same bias seen twice: the archive attacks the object
named in the question, in the frame the question is phrased in, with devices
that try to make something decrease.  All three choices are optional.

## 4. How other rules were settled, and what actually transfers

| Rule | How it was settled | Transfers to Rule 30? |
|---|---|---|
| 90, 150, 60 | Linear algebra over `GF(2)`; Lucas/Kummer closed forms | No — obstruction B, and the archive's controls already turn on exactly this |
| 184 | A conserved particle number, then ballistic particles | Half.  `RESULTS-additive-conservation-probe.md` kills the conservation half through width 12; the *particle* half was never tried |
| 110 | Cook's universality, by gliders on a periodic background | Method transfers: background subtraction, then classify collisions |
| **18** | **Eloranta & Nummelin 1992, JSP: the kink performs a random walk with independent increments and independent delay times** | **This is the nearest precedent and it is absent from the archive** |

Rule 18 is the relevant case because it is chaotic and non-additive, like Rule
30, and it nevertheless carries a rigorous limit theorem.  The method is: fix a
background, define the defect as the failure of the background symmetry, prove
the defect's motion is a random walk.  Eloranta's follow-up ("The dynamics of
defect ensembles in one-dimensional cellular automata", JSP) extends it to
ensembles under a stated diffusivity condition.

A keyword census of `docs/` and `experiments/` returns zero files mentioning
Eloranta, Nummelin, kink, glider, or sublattice.  Rule 18 appears three times
and only as an aside; Rule 184 only as a positive control; "particle" twice, in
the conservation probe.  The defect-dynamics literature is a blind spot, not a
rejected route.

*Citation status: retrieved from the publication records (Springer JSP, Aalto
research portal), not read in the primary.  Anything load-bearing must be
checked against the papers before it enters a results doc, per
`paper/CITATION-AUDIT.md`.*

Use Eloranta as a **method pointer**, not a template, and do not write that
Rule 30 has a Rule 18 kink.  The method needs an *invariant* background, and
Rule 30's ordered region is not one: Rule 18's background is shift-periodic in
space and invariant, whereas the left region here is glide-periodic in
spacetime, aperiodic in space, and — by NKS p. 871 — not invariant at large
depth, since the period doubles at `87,867` and again around `2.1e9`.  A
plateau that later doubles is a transient phase, not a vacuum.  The neighbouring
literature to read first is Grassberger on deterministic diffusion in Rule 18
and Lind's conjectures, and that is one paragraph of reading, not an arm.

`PATH.md:285` remains right that a fluctuation-class measurement for the
`0.252` boundary would be a standalone paper.  It is a different paper from
P1 and from the period-two thread, and it should not be started before the two
items in section 5.

## 5. Ranked next work

**A. The synthetic width-two check.**  The only item that can give the
retracted composition argument any content.  Take the five `T = 24` on-cycle
witnesses of `RESULTS-ladder-rung2-periodic-realizability.md` — ready-made
width-two periodic Rule 30 diagrams — and ask whether their ordered regions
carry spatial period `16p`.  If they do, the composition proves nothing and the
matter is closed; if they do not, there is a real obstruction to a width-two
periodic diagram having an ordered region at all, and that is worth the next
step.  *Kill:* either answer settles it, which is why it goes first.

**B. The left-frame doubling law.**  Which depths first carry period `2^k`, and
why.  NKS sketches the mechanism (a doubling when a diagonal becomes a white
stripe and the one to its left has an odd number of ones per block); the
left-frame recurrence with its absorbing OR is where to make it exact.  This is
a genuine open question about the tame cone and a plausible theorem.  It is not
P1, and by obstruction A's corrected form it does not cross the interface.
*Kill:* the depths do not follow any law expressible from the recurrence's
local data.

Do **not** start a defect-ensemble arm, a space `omega`-automaton, or `T = 26`
before A and B.  In particular the interface fluctuation-class measurement,
though real and publishable, needs the ordered region's status settled first,
and it is a different paper.

**C. Standing, not a project.**  Apply the two screens — contraction
(section 1) and horizon (section 2) — before running anything, and prefer
identity/counting engines.  Do not open a sixteenth bounded-summary search, and
do not promote a plateau to a conjecture without checking the scale of the next
event.

Also standing: `T = 26` does not need running to protect the rung-2 modulus 420,
and `RESULTS-C3-LOCALIZATION-NO-GO.md` is closed as a `K` and should not be
reopened.

## 6. What this does not claim

P1, P2 and P3 remain open and nothing here narrows any of them.  The glide form
and the spatial aperiodicity are measurements on finite windows; obstruction H
applies, and section 2 records what happened the one time this memo forgot it.
The ordered region is prior art (NKS p. 871) and no novelty is claimed for it.
The width-two hypothesis is not weakened and Kopra 2023 Thm 3.5 stays in the
chain.  The literature transfer in section 4 is a method analogy whose
citations are retrieved from publication records rather than read in the
primary; no result of Eloranta, Nummelin, Grassberger, Lind or Cook is used
here as a premise.

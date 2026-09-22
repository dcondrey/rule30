# Audit: Pasquali, "The Quantized Cage," §76.7 on the Rule 30 Prize Problems

**Verdict: AUDIT, not refutation.** The paper does not claim what the framing
question here expected it to claim. It is unusually candid: Theorem 76.43
proves only that any algorithm computing `c0(n)` must access at least `2n+1`
seed bits, and the paper's own text immediately says "the algorithmic
(circuit-complexity) version remains open." That is honest, and correctly
distinguishes an information-theoretic access bound from Prize Problem 3
itself. Two things nonetheless need saying: the proof of Theorem 76.43, as
written, contains an invalid general inference step, exposed directly by a
Rule 90 control; and even a fully valid version of the theorem would still be
compatible with every possible answer to Problem 3, so it cannot count as
partial progress on the problem no matter how it is repaired.

Assessed 2026-09-13. Carlos Pasquali, *The Quantized Cage: Unified Physics
from One Algebraic Identity*, Zenodo, DOI 10.5281/zenodo.22270217 (v10,
2026-09-03), concept DOI 10.5281/zenodo.18482656. Not on arXiv, not peer
reviewed. 3,558 pages; retrieved in full (`the_quantized_cage.pdf`, 27.8 MB,
and `executive_summary.pdf`, 486 KB) via Zenodo's `/api/records/.../content`
endpoint with an explicit `Range: bytes=0-<size-1>` header — the plain GET
returns HTTP 504 for both files regardless of size (486 KB also failed),
so this session's failure was not the file-size cap noted in
`REFUTATION-fradkin-rule30-resolved.md`; the range request worked around it
and both PDFs are byte-complete (`pdftotext`, 3,558 pages). The Rule 30
material is §76.7, "The three Wolfram Rule 30 Prize Problems in the cage,"
pp. 2694-2703, containing Thm. 76.39 (Problem 1), Conj. 76.40, Thm./Cor.
76.41-76.42 (Problem 2), Thm. 76.43-76.45 (Problem 3), read in full.

## 1. What the paper actually claims, stated precisely

The section opens with a "Novelty Map" table (p. 2694) that is explicit about
status for each problem:

- **Problem 1** (periodicity): "Conditional theorem (Thm. 76.39): proved
  modulo the assumption that the cage lift is irreducible on `H_CA^(0)`."
- **Problem 2** (density 1/2): "Conditional on the Cage Rule-30 Ergodicity
  Hypothesis (Conj. 76.40)."
- **Problem 3** (complexity): "Any algorithm computing `c0(n)` must have
  access to the `2n+1` seed bits of the cage light cone, giving the
  unconditional information-theoretic lower bound `Ω(n)` (Thm. 76.43). The
  algorithmic version remains open: it requires ruling out succinct circuits
  via a diagonalization argument we do not have."

The Zenodo landing-page description compresses this into: "The third is
unconditional, with an `Ω(n)` lower bound from the algebraic light cone... The
second is not settled by the ergodic route... That statement needs a second
and strictly stronger hypothesis, which is stated separately as the
assumption it is." Read against the body text, "unconditional" modifies the
proof technique (no unproven conjecture required, unlike Problems 1 and 2),
not the problem. **The paper does not claim Prize Problem 3 is resolved.**
Theorem 76.39's own proof is withdrawn by its author in the same breath it is
stated — three numbered steps are listed as not carrying, ending "The
statement is therefore conditional... and should be read as a reduction... not
as a proof of non-periodicity" (p. 2695) — and Theorem 76.41(ii)/(iii) states
the P2 gap in exactly the form this repository's own `REFUTATION-*` files
independently derived against other claimants: the single-cell seed has
`µ`-measure zero, the exceptional null set is nonempty (spatially periodic
seeds are given as members, with rational densities), and closing it needs "a
second and strictly stronger hypothesis," named as Conjecture 76.42 rather
than smuggled through. This is the inverse of the Fradkin paper's failure mode
(`REFUTATION-fradkin-rule30-resolved.md` §"The false step"): Fradkin asserted
the seed-specific theorem and hid the substitution of a nearby ensemble;
Pasquali names the substitution and declines to assert the theorem. No
refutation is available at the level the target claim actually operates.

## 2. The load-bearing step of the Problem 3 argument

Theorem 76.43 (p. 2696-2697):

> Any algorithm `A` that computes `c0(n)` from an initial seed `s` must access
> at least `2n+1` bits of the seed.

Proof structure: (a) the window `[-n,n]` **suffices** — two seeds agreeing on
it produce the same `c0(n)`, by the light-cone containment of Thm. 76.1
(standard, correct: Rule 30 has radius 1, so `t` steps reach exactly `t` cells
each side). (b) the window **cannot be shortened at either end** — Cor. 76.44
computes the influence of the left endpoint as exactly 1 (it enters by XOR, so
flipping it flips `c0(n)` for *every* other-bit setting) and the influence of
the right endpoint as exactly `2^-n` (flipping it flips `c0(n)` only when a
specific chain of `n` intervening cells are all 0, which happens for a `2^-n`
fraction of the remaining seeds). Both influences are proved nonzero, exactly
and cleanly, by induction (part i) and a triangular-bijection count over the
conditioning cells (part ii) — this arithmetic is correct and independently
checkable. (c) the paper then concludes: "Any window omitting an endpoint
therefore fails to determine `c0(n)`... and `A` must have access to its `2n+1`
bits."

Step (c) is the gap. What (b) establishes is that `c0(n)`, as a Boolean
function of `2n+1` variables, is a genuine junta on the full window — no
proper *fixed* sub-window determines it for every seed. What (c) asserts is a
claim about *adaptive query complexity*: that any algorithm, which may choose
which bits to read based on bits already read, must still read all `2n+1` in
the worst case. These are different statements, and the second does not
follow from the first. A function can depend on every one of its `n`
variables — none droppable, each with nonzero influence — while its exact
adaptive decision-tree depth is far below `n`; the standard example is an
address/multiplexer function, where an adaptive tree reads the address bits
and then only the one data bit they select, even though every data bit is
individually relevant. Relevance of a variable (there exists some setting of
the others under which flipping it changes the output) licenses "some
input requires reading it"; it does not license "every input requires reading
it," which is what a `2n+1`-deep worst-case tree needs. The paper's own
"unconditional" framing rests on exactly this unproved step.

## 3. Rule 90 control, computed directly

Both refutation precedents in this repository use Rule 90 as the standard
control for Rule-30 arguments: linear over `F2`, left-permutive, and with
known-trivial center-column behavior. It is the right control here for a
different reason than in the Fradkin case — not because Rule 90 falsifies
the *conclusion*, but because it falsifies the *inference pattern* in step
(c), using the paper's own stated edge classification. §76.7's marginal
"Prediction" box (p. 2699-2700) explicitly places Rule 90 in the same edge
class as Rule 30: "rules 150 and 90 have `g = c⊕r` and `g = r`... `q = 1` and
both edges are unconditional" — i.e., by the paper's own influence
calculation, Rule 90's light-cone endpoints are exactly as non-droppable as
Rule 30's (influence 1 at both ends, for all depths). If step (c)'s inference
("edges non-droppable ⟹ full window must be accessed by any algorithm") were
valid, it would force `D(f) = 2n+1` for Rule 90's center column too.

Computed exactly (script below; brute-force minimum-depth adaptive decision
tree over the full `2^(2n+1)`-row truth table of `c0(n)`, both rules,
`n = 1..4`):

```
=== Rule 30 ===
  n=1: window size 2n+1=3, exact min worst-case decision-tree depth D(f)=3
  n=2: window size 2n+1=5, exact min worst-case decision-tree depth D(f)=5
  n=3: window size 2n+1=7, exact min worst-case decision-tree depth D(f)=7
  n=4: window size 2n+1=9, exact min worst-case decision-tree depth D(f)=9
=== Rule 90 ===
  n=1: window size 2n+1=3, exact min worst-case decision-tree depth D(f)=2
  n=2: window size 2n+1=5, exact min worst-case decision-tree depth D(f)=2
  n=3: window size 2n+1=7, exact min worst-case decision-tree depth D(f)=4
  n=4: window size 2n+1=9, exact min worst-case decision-tree depth D(f)=2
```

Rule 90's true query complexity is `2^popcount(n)` (both endpoints are the
only always-relevant bits when `n` is a power of two; the middle collapses
because Rule 90's center cell is `c0(n) = XOR` over `{r : C(n,r) odd}` of
`s_{-n+2r}`, and by Kummer's theorem only `2^popcount(n)` of the `2n+1`
positions carry a nonzero coefficient — the rest are not merely
low-influence, they are exactly zero-influence and a decision tree can skip
them unconditionally). Both endpoints are members of that odd-coefficient set
for every `n` tested (matching "both edges unconditional"), yet the interior
collapses far below `2n+1` the moment `n` is not itself a power of two with
all-one binary weight. The paper's step-(c) inference, applied uniformly as
its own Prediction box invites, would misclassify Rule 90 as requiring a
full-width `2n+1` query — false by a factor of up to `2n+1` over `2`. Rule 30
itself checks out at `D(f) = 2n+1` for `n = 1..4` (consistent with, though not
a proof of, the paper's conclusion for Rule 30 specifically) — the defect is
in the general argument, not in whether Rule 30 happens to be evasive.

Reproduction: `dt_complexity.py` in the scratch directory for this session
(brute-force memoized minimum decision-tree search over the exact truth
table; not committed to the repository, as it is a one-off check rather than
a reusable probe — regenerate from the recursion described above if needed).

## 4. Why the theorem, even repaired, would still not touch Problem 3

Independent of the step-(c) gap: Wolfram's third prize problem asks whether
`c0(n)` admits an algorithm faster than the direct `O(n^2)` simulation — i.e.,
whether the *time* complexity is sub-quadratic. An `Ω(n)` bound on the number
of seed bits an algorithm must *read* bounds neither the time complexity nor
the qualitative question the prize asks. Reading `n` bits costs `O(n)` time
at minimum, and nothing stops an `O(n)`-time algorithm from existing that
reads exactly those `n` bits and does `O(1)` work per bit — such an algorithm
would answer Problem 3 affirmatively (yes, a sub-quadratic algorithm exists)
while satisfying Theorem 76.43 with equality. The theorem, fully repaired and
fully proved, would be consistent with every possible resolution of Problem
3: a matching `O(n)` algorithm, an `Ω(n^2)` lower bound proving naive
simulation optimal, or anything between. It is this repository's recurring
finding under a new name: a true statement about the problem's *input*
requirement is not a statement about its *output-computation cost*, and
proving the former — even correctly — makes zero progress on the latter. The
paper's own restatement of Problem 3 in its Novelty Map ("Does computing the
nth cell... require at least `O(n)` computational effort?") is itself a much
weaker question than the one Wolfram posed (whether `Θ(n^2)` can be beaten);
answering the weaker question, honestly labeled as such, is what Theorem
76.43 does, and the paper's explicit disclaimer ("the algorithmic version
remains open... connects to the P vs NC question") shows its author already
knows this. That disclaimer is the reason this is an audit and not a
refutation: there is no overclaim in the primary text to refute.

## 5. What holds up

- Thm. 76.1's light-cone containment (radius-1 propagation ⟹ `t`-step
  dependency confined to `[-t,t]`) is standard and correct.
- Cor. 76.44's influence computations (left endpoint 1, right endpoint
  `2^-n`, by induction and a triangular-bijection argument over the
  conditioning chain) are exact and were independently reproduced above as a
  side effect of building the truth tables.
- Thm. 76.41 and Conj. 76.42 on Problem 2 correctly isolate the
  measure-zero gap and do not attempt to paper over it — a materially more
  careful treatment of the same obstruction than `REFUTATION-fradkin-rule30-resolved.md`
  found elsewhere in this literature.
- Cor. 76.45 (Rule 110's left edge goes silent beyond depth two) is a
  genuine, checkable asymmetry between Rule 30 and Rule 110 and is not
  assessed further here; it is not load-bearing for Problem 3.

## 6. Verdict

**AUDIT.** No refutable overclaim exists at the level of "Prize Problem 3 is
resolved" — the paper does not make that claim and is explicit about the gap
between its information-theoretic bound and the algorithmic question. Two
defects are real and worth recording: (1) Theorem 76.43's proof takes an
invalid step from "the light-cone window cannot be shrunk at either end" to
"any algorithm must query the full window," an inference pattern that the
paper's own edge classification, applied to Rule 90, produces a demonstrably
false conclusion for; and (2) even a fully repaired version of the theorem
would remain irrelevant to Problem 3 as posed, since an `Ω(n)` read
requirement is compatible with every possible answer to whether an `O(n^2)`
simulation can be beaten. Problem 3 remains open, exactly as this repository's
other audits of it have found, and this source adds no progress toward or
against a resolution.

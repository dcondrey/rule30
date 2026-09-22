# Citation and novelty audit

Audit date: 2026-09-02. The manuscript's retained attributions were checked
against the full primary texts, not secondary summaries. Priority beyond the
sources listed here has not been exhaustively established, so the paper makes
no global first-publication claim.

| Source | Resolution and claim check | Manuscript use |
|---|---|---|
| Jen, *Global Properties of Cellular Automata* (1986), DOI [`10.1007/BF01010579`](https://doi.org/10.1007/BF01010579) | DOI resolves. Full text checked. Theorems 2a and 2b list Rule 30 among rules for which a finite initial condition can produce at most one eventually periodic temporal sequence; Theorem 3 is the nonbinary generalization. Theorem 7a gives necessary and sufficient mechanisms for an eventually constant nonzero temporal sequence under its nearest-neighbor hypotheses. | Supports the one-exception background and marks Theorem 7a as prior art close to the all-one exclusion. The paper does not claim novelty for the bare all-one nonexistence statement. |
| Jen, *Aperiodicity in One-Dimensional Cellular Automata* (1990), DOI [`10.1016/0167-2789(90)90169-P`](https://doi.org/10.1016/0167-2789(90)90169-P) | DOI resolves. Full text checked from the LANL preprint LA-UR-90-761. Proposition 3 states the one-periodic-temporal-sequence bound for the relevant one-sided injective rules and explicitly lists Rule 30. | Independent later source for the same one-exception theorem. |
| Kopra, *Cellular Automata with Complicated Dynamics* (2019), [`URN:ISBN:978-952-12-3891-8`](https://urn.fi/URN:ISBN:978-952-12-3891-8) | Repository record and full PDF resolve in a browser; the host returns HTTP 403 to an unauthenticated command-line probe. Theorem 3.1.12 gives width-two nonperiodicity for every nonzero finite Rule 30 configuration. The following paragraph says the width-one question remains open for such configurations. | Source for the broader finite-configuration formulation against which the paper settles period one. |
| Kopra, *Rapid Left Expansivity, a Commonality Between Wolfram's Rule 30 and Powers of p/q* (2023), DOI [`10.1016/j.tcs.2022.12.018`](https://doi.org/10.1016/j.tcs.2022.12.018) | DOI and open full text resolve. Theorem 3.5 is the general rapidly-left-expansive width theorem; Corollary 3.7 gives the width-two conclusion for left-permutive, left-spreading elementary CA. Problem 3.10 is the lone-seed width-one Rule 30 problem. | Supports the precise width-two/width-one boundary. |
| Rowland, *Local Nested Structure in Rule 30* (2006), DOI [`10.25088/ComplexSystems.16.3.239`](https://doi.org/10.25088/ComplexSystems.16.3.239) | DOI and author-hosted full PDF resolve. Proposition 1 proves uniqueness of an infinite rightful history for a rightful row under a right-bijective rule; the paper explains the reflected left-bijective Rule 30 setting. It does not classify constant trace fibers or give the finite-radius horizon law. | Cited only for the related one-sided unique-history construction, not as the proof of this paper's triangular lemma. |
| Voorhees, *Predecessor States for Certain Cellular Automata Evolutions* (1988), DOI [`10.1007/BF01223374`](https://doi.org/10.1007/BF01223374) | DOI and full text resolve. The paper solves predecessor equations for binomially determined nearest-neighbor additive CA over `Z_p` on finite or half-infinite sequences, using an operator analogous to backward integration; its introduction records the general predecessor problem as NP-complete. The previously cited suffix `376` belongs to an unrelated article and was incorrect. | Used as a contrast with an all-future trace inversion for nonadditive Rule 30. |
| Wolfram, [*Announcing the Rule 30 Prizes*](https://writings.stephenwolfram.com/2019/10/announcing-the-rule-30-prizes/) (2019) | Page resolves. Problem 1 asks whether the center column from a single black seed ever becomes periodic. | Defines Prize Problem 1; the manuscript explicitly states that it is not solved here and that the note is not a prize submission. |
| Wolfram, *A New Kind of Science* (2002), p. 871 (notes to p. 27) | **Checked against the book, 2026-09-07.** Records that the diagonal `n` cells in from the left edge is eventually periodic, with first occurrences of period `2,4,8,16,32,64` at depths `3, 8, 29, 400, 87,867` and `2,107,985,255 or more`, and that the repetition/randomness boundary moves left at `~0.252` cells/step. The archive independently reproduces the first five depths to the unit (`experiments/rule30/ordered-wedge/`, two asserting tests). Note p. 949 gives a *different* constant, `0.2428`, for the left edge of a difference pattern; the two must not be pooled. | Remark `rem:wedge` cites it as prior art for the phenomenon itself, not as corroboration. The remark claims novelty only for the recurrence pair, the glide form, and the Rule 90 split. |

## Novelty boundary retained in the paper

The four named research sources do not contain either right-half-by-right-half
constant-fiber classification or either sharp finite-radius horizon and exact
extremizer count. The manuscript limits its novelty wording to those results.
It does not claim that Jen's results are weaker in every logical formulation,
and it does not claim exhaustive priority over the wider literature.

## Items not independently verified

None. A global priority claim was deliberately not made because this audit was
source-targeted rather than exhaustive.

## Novelty note for Remark `rem:wedge`

The ordered left region, its period doubling, and the depths at which it doubles
are **prior art**: `NKS` p. 871. The remark says so and claims novelty only for
the left-frame recurrence, the glide form of that periodicity, and the Rule 90
split. Even for those the searched scope was this repository plus one web
search, which is not a literature audit; nearest published neighbour for the
opposite cone is Rowland (2006).

A first draft of the remark asserted that the left-frame period is 16 for every
`j`, from a scan reaching `j = 65,536`. That is false — the plateau ends at
`j = 87,867`, the value `NKS` p. 871 supplies — and the claim never entered a
built PDF that left this machine. It is recorded here because the failure is
the citable kind: the refuting number was already in a source the repository
had cited on an adjacent line.

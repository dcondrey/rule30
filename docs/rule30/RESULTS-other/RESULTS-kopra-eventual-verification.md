# Kopra's eventual width-two theorem: dependency verified

Date: 2026-09-09. Evidence: `U/R`, verification of a published theorem and
its application; no new Rule 30 theorem.

**The dependency in RESULTS-four-convergent-statements §5 checks out.
S1 is equivalent to P1, including eventual periods at p>=2.**

| Finding | Evidence |
|---|---|
| The journal theorem excludes eventual periodicity | `U`, Theorem 3.5, p. 5 |
| Width two applies to Rule 30 | `U`, Corollary 3.7, p. 6; local rule in Example 2.3 |
| The configuration need only be nonzero and zero sufficiently far left | `U`, Definition 2.4, p. 3 |
| S1 implies P1 with the repository's pin biconditional | `R`, explicit application below |

## 1. Primary-source check

Johan Kopra, *Rapid left expansivity, a commonality between Wolfram's
Rule 30 and powers of p/q*, TCS **946** (2023), 113668,
[DOI](https://doi.org/10.1016/j.tcs.2022.12.018).
The [journal PDF in Turku's repository](https://www.utupub.fi/bitstream/handle/10024/174540/1-s2.0-S0304397522007502-main.pdf?isAllowed=y&sequence=1)
and its [current repository endpoint](https://www.utupub.fi/server/api/core/bitstreams/eeb04919-9fa7-443b-998f-032fab664a41/content)
identify the journal version. The indexed primary text of pages 3, 5 and 6
was read directly. Direct PDF download returned HTTP 403; no local PDF or
download hash is claimed. The [arXiv v1 PDF](https://arxiv.org/pdf/2202.13809)
was also read; its title and page numbering differ.

Theorem 3.5 says: for a rapidly left expansive CA of width `w`, every
width-`w` trace of each `x in L_0(Sigma)` fails eventual periodicity.
Definition 2.4 makes `L_0` the **nonzero** configurations vanishing below
some spatial index; their right tails are unrestricted. Corollary 3.7
specializes to width two for left-permutive, left-spreading elementary CA.
Rule 30 meets these hypotheses: `a XOR (b OR c)` is permutive in `a`,
and `f(001)=1` moves the left edge left. The proof starts with an arbitrary
preperiod and propagates periodicity using Lemma 3.2. It is not restricted
to traces periodic from time zero. Corollary 3.7 credits Jen's Proposition 3;
this check does not establish a historical strengthening over Jen.

## 2. Application to S1

Use the notation and proved pin biconditional of
[the four-statement audit](RESULTS-four-convergent-statements.md) §0.
Assume S1 and assume the lone-seed centre is eventually `p`-periodic.
Then `rho` is eventually periodic. If the centre has zeros in its periodic
tail, a temporal shift of `p*q`, where `q` is a sample period of `rho`,
preserves both the centre phase and the sampled neighbour. The pin therefore
makes column `-1` eventually periodic too. Equivalently, use the already
proved biconditional directly. Synchronize the two column periods by their
least common multiple and the onsets by their maximum: the pair is an
eventually periodic width-two trace of the nonzero lone seed. The verified
corollary excludes it. Thus S1 implies P1. P1 implies S1 vacuously.

The existing p=1 exclusions, PATH rows 25/26, remain independent ways to
handle constant tails. Neither the new verification nor its stronger
left-finite hypothesis proves S4: S4 assumes only one periodic column, and
no periodicity of its neighbour has been established there.

## 3. Scope and corrections to inherited wording

The finisher needs **left-finiteness**, not finite support on both sides.
This still excludes its use on the a7 construction with infinite support
to the left and on the spatially periodic tori. The distinction matters
for arbitrary-right-tail statements, but supplies no missing implication.

The conditional warning about degradation to non-eventual periodicity is
discharged by the primary source. It should not be read as a newly verified
claim that Jen's original result was weaker; that would require a separate
reading of Jen. P1, P2, P3, S4 and the q=420 residual remain open.

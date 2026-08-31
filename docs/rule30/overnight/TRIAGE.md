# Literature-novelty triage table (overnight run, 2026-08-30)

Method: one researcher agent per technique (10 agents, schema-constrained), each required to
verify citations by actual search, name the precise gap, and state the proof-relevance path to
P1 (non-periodicity), P2 (limiting density), P3 (computational effort). Full rows with all
citations: `runs/overnight/triage-rows.json`. Verdict vocabulary: novel-open /
known-adjacent-with-stated-open-edge / closed.

| # | Technique | Verdict | Closest prior work | Open edge or reason closed |
|---|---|---|---|---|
| 1 | Persistent homology / TDA on the (x,t) cloud | **closed** | Gameiro, Kalies, Mischaikow, Phys. Rev. E 70:035203 (2004); Tozzi preprint (2025, not peer-reviewed) | Gap is unoccupied but structurally doomed: time-filtered H1 bars biject with enclosed white triangles (NKS-era bookkeeping); center-column periodicity constrains no spatial neighborhood (cols 0,1 cannot both be periodic, Jen 1990 Prop 3 / Kopra); salvage collapses into off-limits column-band territory. |
| 2 | Quantum circuit / entanglement across center cut | **closed** | Gutschow, Uphoff, Werner, Zimboras, J. Math. Phys. 51:015203 (2010); Iaconis, PRX Quantum 2:010329 (2021) | Single-seed basis-state input through a permutation circuit has center-cut entropy identically 0; nontrivial quantities are ensemble averages that cannot see one orbit; no transfer to P3 lower bounds. Only reachable open item (exact MPO operator-entanglement asymptotics) has no path to P1/P2/P3. |
| 3 | p-adic / van der Put analysis (time direction) | **known-adjacent-with-stated-open-edge** | Anashin, p-Adic Numbers Ultrametric Anal. Appl. 4(2) (2012); Grigorchuk, Savchuk, J. Aust. Math. Soc. (2020) | 1-Lipschitz/van der Put machinery on the TIME direction of a nonlinear CA is unoccupied; Anashin's automata-finiteness criterion gives a concrete finite-state test whose failure modes are informative. Conditional reduction: finite-state R-hat would imply 2-automaticity (which ARM6 evidence disfavors). |
| 4 | Latent-space geometry -> exact conserved window functions | **known-adjacent-with-stated-open-edge** | Gilpin, Phys. Rev. E 100:032402 (2019); Burtsev, NeurIPS MATH-AI workshop (2024); additive conserved-quantity theory (Hattori-Takesue line) | Additive/linear conserved quantities are settled theory; the open edge is EXACT non-additive, group/monoid-valued, or tilted-direction conserved window functions for Rule 30, searchable exhaustively/SAT at small windows. ML part is only a candidate generator; exact search is the content. |
| 5 | Hydrodynamic / coarse-grained PDE limit | **closed** | Gutowitz, Victor, Knight, Physica D 28:18-48 (1987); Wolfram, Rev. Mod. Phys. 55:601 (1983) | Coarse-grained density is a spatial-average object; P2 is a temporal statement about one measure-zero orbit; local structure theory is the adjacent prior art and its refinements cannot in principle produce the single-column limit. |
| 6 | Non-standard analysis / hyperfinite rows | **closed** | Nelson, Bull. AMS 83:1165 (1977); Kamae, Israel J. Math. 42:284 (1982) | Transfer/overspill/Loeb machinery is conservative: it yields P2 only after the standard lemma it needs (equidistribution of the specific orbit) is already available; no Rule-30-specific leverage; schematic derivations apply verbatim to Rule 90 where the conclusion fails. |
| 7 | Homotopy type theory / loop-space framing | **closed** | Arsiwalla, Gorard, Elshatlawy, Complex Systems 31(3) (2022); Kraus, von Raumer, LICS 2019 | All types involved are hSets; the loop-space statement 0-truncates to the plain first-order eventual-periodicity sentence; higher structure in the multiway line comes from nondeterministic branching absent here. Adds nothing over set-level formalization. |
| 8 | Axiomatic / definability / automaticity of the grid | **known-adjacent-with-stated-open-edge** | Rowland, Yassawi, Adv. Appl. Math. 63:68-89 (2015); Marcovici, Stoll, Tahay, AUTOMATA 2018 | Target "A051023 is not 2-automatic" (equiv. Christol transcendence; equiv. non-FO-definability in (N,+,V_2)) is unposed in the literature; columns of LINEAR CA are exactly p-automatic (Rowland-Yassawi), Rule 30 nonlinear case open. Repo ARM6 already measured the finite evidence (>=8191 residuals, rank 512); the open edge is residuals provably distinct at arbitrary depth, a proof problem, not an overnight computation. |
| 9 | Boolean-function ANF/Walsh analysis of iterated center bit | **known-adjacent-with-stated-open-edge** | Meier, Staffelbach, EUROCRYPT '91 LNCS 547:186-199; Koc, Apohan, IEE Proc. Comput. Digit. Tech. 144(5):279-284 (1997) | No published theorem gives deg, ANF size, or max Walsh coefficient of the t-iterated center-bit function f_t on 2t+1 variables for general t; no inductive lemma controls ANF growth under the overlapping-window composition. Candidate law deg f_t = t+1 must be reconciled with ARM4's measured "ANF degree exactly 2t-1" (different object; obligation recorded in PREREG-anf.md). Model-restricted P3 relevance. |
| 10 | Ergodic theory / invariant-measure rigidity for P2 | **known-adjacent-with-stated-open-edge** | Host, Maass, Martinez, DCDS 9(6):1423-1446 (2003); Pivato, DCDS 12(4):723-736 (2005) | Rigidity theorems cover ALGEBRAIC/bipermutative rules; Rule 30 is left-permutive, non-right-closing, non-algebraic: no theorem or counterexample on its jointly (shift,F)-invariant measures exists (gap G1). Exact finite search over Markov measures is unoccupied and decidable. Repo Arm 2 (PREREGISTRATION.md) noted only Hedlund-invariance of uniform Bernoulli and never ran as discovery; the edge is uniqueness/rigidity, not invariance. |

Verdict counts: 5 closed, 5 known-adjacent-with-stated-open-edge, 0 novel-open.
Closed rows killed without sentiment; none is promoted regardless of unoccupied-territory appeal.

## Ranking of open rows (novelty x proof-relevance x feasibility)

1. **anf** (row 9): fully exact overnight computation (bit-sliced truth tables to t~13-14),
   two live formal targets (degree law + Walsh decay), P3-model-restricted relevance,
   a reconciliation obligation against ARM4 that doubles as the cheapest disconfirming test.
2. **ergodic** (row 10): exact rational-arithmetic classification of jointly invariant Markov
   measures (memory <= 3) is a finite theorem either way; direct P2 relevance via the
   equidistribution route; kill condition can genuinely fire (a non-uniform solution).
3. **latent-conserved** (row 4): exhaustive/SAT search for exact non-additive conserved window
   functions; promoted if an above arm kills early. Not pre-registered yet.
4. **padic** (row 3): Anashin finite-state test on the time-direction van der Put series;
   backup to the backup; heavy compute for a mostly-negative expected outcome.
5. **axiomatic** (row 8): highest value, but its open edge is a proof problem (arbitrary-depth
   residual distinctness) with no overnight-computable component that ARM6 has not already done.

Arms pre-registered tonight: **anf** (PREREG-anf.md), **ergodic** (PREREG-ergodic.md).

# Formalization ledger for Rule 30 reductions

Date: 2026-09-13.

This ledger separates finite certificates from the logical reductions that make those certificates matter. The computational artifacts may be exact within their finite domains, but the implication chain from those domains to the prize rungs must be stated as finite logical theorems and, where practical, checked in Lean.

## Reduction edges that should be formalized before more computation is trusted

| Edge | Current role | Formal theorem shape | Why it matters |
|---|---|---|---|
| `mortality -> pt2` | Turns auxiliary frontier mortality into nonconstant period-two exclusion. | From an assumed period-two center trace construct, by alternating-trace reconstruction, a legal finite Z-frontier history surviving all chronological guards. | If this implication fails, capacity and repeat-budget mortality certificates do not discharge the period-two rung. |
| `sep -> pt2` | Turns the endpoint-derived separator into period-two exclusion. | Rank descent and first-infinite-shift reduction leave exactly the two endpoint separator obligations, with reachability and ordered frontier retained. | A separator in the wrong coordinate system or with weakened endpoint shifts would not prove the target. |
| `rw -> sep` | Turns all-length RW/DLP exclusion into the endpoint separator. | RW is DLP with the hard-core junction and terminal `12a` predicate preserved, and DLP exclusion implies `O_c ∩ I(HC_ω)=∅` for `c∈{2,3}`. | Dropping either retained predicate recreates the known false relaxations. |
| `bwh -> rw` | Uses the binary wedge horizon as a sufficient relaxation for DLP. | A DLP witness of length `n>=7` forces at least `n+2` binary continuation symbols, while the finite small cases keep their own guards. | The repaired BWH+ target only matters if the guard-preserving reduction is exact. |
| `capacity -> mortality` | Turns fixed-capacity repeat bounds into auxiliary mortality. | Every original has finite `Q_2`; a repeat bound at its capacity and the survival inequality force finite lifetime. | Capacity certificates are only a partial ladder unless this bridge is formal. **Kernel-checked 2026-09-21** in `experiments/rule30/formalize-the-reduction-chain/Rule30SurvivalBridge.lean` (`mortality_of_capacity_budget`, for every capacity function at once, with the survival inequality proved there as `survival`). The abstract pigeonhole lemma `capacity_bounds_length` of `experiments/rule30/Rule30P1Reduction.lean` is not this bridge: the `K` of `bounded_capacity_language.py` is the threshold at which inverse path counts saturate, not a bound on how often a state recurs. |
| `budget -> mortality` | Identifies per-length repeat budgets with mortality. | The repeat inequality proves sufficiency; finite mortality over finitely many words at a fixed length gives a finite maximum repeat count. | Prevents confusing sharp repeat conjectures with the weaker budget actually needed. **Kernel-checked 2026-09-21**, both directions at every length, in `experiments/rule30/formalize-the-reduction-chain/Rule30SurvivalBridge.lean` (`budgetAt_iff_mortalAt`, `budget_iff_mortality`). |
| `energy -> p2` | Equates ordered-energy decay with density one-half. | The exact dyadic shell comparison is bidirectional for the singleton orbit with boundary terms retained. | Numerical decay searches need this bridge checked separately from measurements. **Kernel-checked 2026-09-21** for every Boolean sequence, together with the `shell_max` and `ordered_energy` forms, in `experiments/rule30/formalize-the-reduction-chain/Rule30P2Bridge.lean`; the seed-specific decay stays open. |

## Closure-certificate shape for open rungs

For each open rung, the preferred question is: what finite closed object would imply the all-length statement?

- Capacity-18 index 15: close a compressed joint-column automaton for `213(13)^a1213(13)^b03`, starting from the 125 depth-12 survivor classes, with ordered seam transport and chronological guard histories retained. A two-million-state cap at depth 16 is not a certificate.
- Capacity-18 indices 8, 23, 34: same joint-column closure shape, with the last known closed depths and survivor counts recorded in `RESULTS-capacity18-joint-mortality.md`.
- RW/DLP: build a finite separator automaton or closed transducer section whose states retain reachability, the hard-core junction, and terminal `12a`; a rewrite search without a closed invariant is the slow path.
- SEP: build a closed endpoint-derived orbit/separator certificate in the actual ordered frontier coordinates, then prove the reduction to period two separately.
- Repeat budgets: build a finite guarded composition quotient or potential automaton whose closure yields a repeat charge for every source, rather than hand-finding rewrites.

Until a reduction edge has a Lean theorem or an equivalent small audited formal proof, mark it as source-reviewed and unformalized, not as a verified implication.

## P3 session components and outstanding formal obligations (2026-09-14)

No new P3 Lean kernel-checked theorem is claimed. Exact finite local tables,
independent bounded replays, and source-reviewed all-length inductions have
separate evidence records. A successful catalog build checks none of those
mathematical inductions. Existing P1/P2 Lean evidence and assumptions remain
as previously recorded.

| Component | Current scope | Remaining formal/cost obligation |
|---|---|---|
| Phi conjugacy and actual B/C center observer | Source-reviewed all-index correspondence; c0=c1=1 retained | Formalize the 2-adic coding, branch transport and exact singleton indices together |
| Controlled affine scans and two-time high readout | Exact B/C formulas, including distinct fictitious origins | Formalize complete word induction; preserve the actual midpoint control |
| Single-rise pause and chain language | Interior temporal transparency under every supplied chronological guard | Formalize guarded composition; build actual predecessor certificates from binary n |
| Fixed-width period powering / supplied-repeat grammar | Exact shortcuts in their specified domains | Charge width-dependent construction, exponent arithmetic, memory and actual input generation |
| General P3 | Open | Prove a correct uniform o(n) algorithm, or a lower bound covering all allowed algorithms; no representation-specific inference substitutes |

Sources: [current P3 report](RESULTS-p3-implicit-boundary-investigation.md),
[two-time observer](RESULTS-p3-two-time-rise-reset.md),
[rise-chain report](RESULTS-p3-rise-chain-transparency.md), and
[P3 scope audit](P3-SCOPE-AUDIT.md). New all-index claim families remain
blocked in the orchestrator until an exact evaluator is reviewed; this
integration does not mark SQLite jobs verified.

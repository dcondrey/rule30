# Overnight Tasks 3–6: verified results and remaining obligations

Date: 2026-09-09. Based on commit `76f3dc4`.

**All four requested investigations have run. There are uniform family
exclusions, a precise obstruction to two proposed abstractions, explicit
C3 state lower-bound witnesses, and repaired checker defects. P1 is not
proved.** The terminal-period theorem, S4 and C3 remain open.

| Task | Result | Full report |
|---|---|---|
| 3: gap-set automaton | Widths 20 and 24 close at 3,209 and 15,424 states. All 74,532 base transitions independently replayed. Uniformly excludes cyclic `(4,2^m)` for m>=1 and `(3,1^m)` for m>=0. | [Gap-set automaton](RESULTS-gap-set-automaton.md) |
| 3: stronger combined model | 155 newly proof-checked exclusions plus 36 rechecked prior certificates yield 177 distinct forbidden words. Their product with the strip still admits `(2,4^m)` for every m>=3. This is a limitation of the model, not a realization. | Same report, §§3–4 |
| 4: zero-cost strip transfer | The direct prefix and free-carry suffix relaxations are sound but total. Neither can prove mortality. The lost terminal condition/carry history is identified explicitly. | [Alt-strip transfer](RESULTS-alt-strip-transfer.md) |
| 5: C3 sequential structure | Exact minimal eight-state comparator on paired dependency diagonals. Source-order raw-edge computation requires 13,207 states at n=22, with explicit distinguishable prefixes. Source generation, legal H and any unbounded-state theorem remain unresolved. | [C3 sequential structure](RESULTS-c3-sequential-structure.md) |
| 6: seam audit | Two false-extinction paths in `gap3_probe.explore` repaired. Named algebraic seams pass; exact terminal image coverage and a uniform image-count recurrence certificate added. Earlier saved Task 1 results survive. | [Load-bearing seam audit](RESULTS-load-bearing-seam-audit.md) |
| External dependency | Kopra's journal theorem explicitly excludes eventual width-two periodicity for nonzero left-finite configurations. S1 iff P1 stands. | [Kopra verification](RESULTS-kopra-eventual-verification.md) |

The audit also corrects the inherited Task 2 report: the q=1 witness does
not disprove an existential q=420-multiple certificate, and the asserted
two-way universe separation lacked the required maps. These implications
remain unproved. The incorrect S3 polarity is corrected to not-S3. Original
text is retained, with superseding notes appended to that report and PATH §11.

Validation includes all 61,696 width-24 and 12,836 width-20 strip edges,
all 74,956 product edges, DRUP checking of 191 certificate instances,
SAT-witness replay, exact packing/provenance checks, 2,730 full zero-cost
macro checks, and the C3 scalar/kernel controls. The existing ladder,
rung-1, rung-2 and image-DFA test suites pass: **34 tests**. New experiment
scripts pass Ruff. The twelve frozen family-seam source hashes are unchanged.

The Task 3 reports distinguish complete finite-graph checks from the bounded
catalogue of cone attempts. Task 5 distinguishes finite lower bounds from
an all-length obstruction. Task 6 lists its coverage rather than claiming a
repository-wide proof audit. No Christol/transcendence or uniform-measure
argument is adopted, and concurrent P2 work is outside this change.

# Extremal forcing STATES do not form a family across n (clean negative)

Date: 2026-09-05. Directory `experiments/rule30/p2-needle-attack/`, files
`estate_*`. Preregistered in `estate_PREREG.md` (frozen before any run).
Scripts: `estate_family_census.py` (census -> `estate_census.json`),
`estate_family_analysis.py` (family + null tests). Read-only imports from
`../p1-period2-invariant/`; nothing outside this directory was written.

## Verdict

**NO FAMILY under any relation in the preregistered space.** The O(1) extremal
forcing STATES (the live dependency-edge vectors `edge[:-1]` of the max-survival
words) carry no cross-n family across the tested relations: prefix/suffix
alignment and prefix/suffix containment of the live-state vector, the `2^k`
cocycle signature, source-word longest-common-suffix, and alpha-support
geometry; at strides 1, 2, 4; in both arms (all-W and hard-core-W); both tails.
All three preregistered questions hit their KILL conditions; none reached its
strong outcome. Residual alignment NOT covered (flagged, not claimed excluded):
a survival-aligned or killing-row-aligned comparison — a future session that
wants one should not read this file as having ruled it out.

The needle is therefore a **per-n certificate, not a proof route via the
state-family door.** The endpoint-restart cocycle template is **not** brought
into range: its prerequisite is a fixed / eventually-periodic family, and that
family is absent at the STATE level — confirming and extending
`RESULTS-FIBER-EXTREMAL-FAMILY.md`'s negative, which found the same for the
continuation and source STRINGS. This is a real result: the door is closed, and
that is worth knowing.

## 0. What was measured, and that it is a new object

The forcing `literal_extension(W,c,rows)` carries the dependency edge; after the
padded source `(0)^n·W` the edge has length `2n`. The recurrence never reads its
last cell, so `edge[-1]` is the exposed cut (output) and the LIVE state is
`edge[:-1]`; `W[-1]=BOUNDARY[edge[0]]` is recoverable, so `edge[:-1]` is the
complete state that determines the entire future.

Edge orientation (verified empirically, `estate` check): **index 0 is shallow,
driven by the NEWEST source symbols; high index is deep and accumulates the
whole history; `edge[-1]` is the cut.** Varying the first (oldest) source symbol
changes only the top edge cell; varying the last (newest) changes every cell.
So common-suffix words agree on a low-index PREFIX and differ at the deep/output
end — which fixes prefix vs suffix alignment in the tests below.

This is the STATE object. It is distinct from the two completed string
analyses (`RESULTS-FIBER-EXTREMAL-FAMILY.md`: extremal continuation strings and
source residual strings). Nobody had compared the edge STATE vectors across n.

## 1. Controls (all pass)

1. **Inlined edge vs `append_dependency_edge`**: 4000 random trials, 0 mismatch.
2. **Reproduces `RESULTS-TERMINAL-CLASS-ARCHAEOLOGY.md` §2.1 EXACTLY**, all-W,
   n=14..19, every field (max_survival, gamma, pooled fiber, class count, class
   sizes):

   | n | c | max_surv | gamma | pooled fiber | classes | class sizes | §2.1 |
   |---|---|---|---|---|---|---|---|
   | 14 | 2 | 10 | 6 | 4 | 1 | 4 | match |
   | 14 | 3 | 8 | 8 | 8 | 3 | 4,2,2 | match |
   | 15 | 2 | 9 | 8 | 10 | 3 | 4,4,2 | match |
   | 15 | 3 | 8 | 9 | 9 | 3 | 4,3,2 | match |
   | 16 | 2 | 10 | 8 | 3 | 1 | 3 | match |
   | 16 | 3 | 10 | 8 | 18 | 2 | 10,8 | match |
   | 17 | 2 | 11 | 8 | 10 | 1 | 10 | match |
   | 17 | 3 | 10 | 9 | 6 | 1 | 6 | match |
   | 18 | 2 | 12 | 8 | 16 | 2 | 8,8 | match |
   | 18 | 3 | 11 | 9 | 12 | 1 | 12 | match |
   | 19 | 2 | 11 | 10 | 8 | 2 | 4,4 | match (§2.1 "8 words, 2 classes") |
   | 19 | 3 | 13 | 8 | 6 | 1 | 6 | match |

3. **Cross-check vs `literal_extension` directly**: for EVERY extremal word,
   the incrementally-carried full edge, the survival, and the continuation
   equal `late_pull_diagonal_sat.literal_extension(W,c,n+4)` recomputed. 100%
   agreement (the `xcheck` column in the run log equals the extremal count in
   every one of the 44 cells).
4. **§10 hard-core fibers reproduced**: n16c2, n17c2, n18c3 hard-core arm all
   give pooled fiber 2, 1 class.
5. **alpha identities**: eq(3) `1^[p!=0]^parity{i<|E|-1:E_i!=0}` and eq(4) via
   the reversed edge agree on every forced row; and `forced_symbol>>1 ==
   1^alpha` on every row of every extremal state (asserted, no failure).
6. **gamma>=1 (validation, not a finding)**: `survival < n+2` for every one of
   the ~1.0M+ enumerated live states across n=10..20; re-confirms the settled
   finite result on independent code.

Enumeration was exhaustive to n=20 (all-W: 2^20 words dedup to 131,873 live
states in 23 s/cell; hard-core: F(n+2) words). No sampling except the null
population (seed 0). Nothing was too slow to run exhaustively.

## 2. Test (i): shared structure across consecutive n — KILL fired

For each consecutive pair and each (arm, tail, alignment): `A_a` = best
agreement (max matching run) between an extremal state at n and one at n+1;
null `A_b` = 95th percentile of extremal(n)-vs-typical(n+1) agreement (up to
1500 sampled non-extremal reachable states). Family required `A_a >= A_b+2` on
>= 70% of pairs in some (arm, alignment).

Result: best fraction over all (arm, c, alignment) = **0.20** (stride 1), 0.22
(stride 2), 0.29 (stride 4) — all far below 0.70. The extremal-extremal
agreement sits BELOW the null p95 on the large majority of pairs (negative
separation). Two isolated positive spikes exist (n18->19 c2 and n14->15 c3,
prefix, sep +17) but do not persist to neighboring n, do not recur in the other
arm/tail, and vanish under suffix alignment — coincidental long shallow prefixes,
exactly what the null is built to expose.

**The null itself is the finding here**: the prefix-alignment null p95 is 7-17
cells. A typical reachable state shares 7-17 low-index cells with an extremal
state as a matter of course, because the shallow (newest-symbol) end is
low-entropy and generically shared. Low-index agreement is generic forgetting,
so extremal states are not special in it. Under suffix (deep-end) alignment the
null is TIGHT — p95 only 2-4 cells — so it is the discriminating arm, with
headroom for a real signal to appear; yet extremal-extremal agreement there is
also only 0-4 cells, no separation. So even in the one arm where the null cannot
be accused of being permissive, no signal appears. No family.

## 3. Test (ii): fixed operation n -> n+1/n+2 — KILL fired

The edge grows 2 cells per unit n. Preregistered operations:
- `o1` state(n) is a low-index PREFIX of state(n+1): **0-1 of 10** pairs per
  cell (and 0/N at strides 2, 4). The one hit is a single isolated c=3 pair.
- `o2` state(n) is a high-index SUFFIX of state(n+1): **0/10** everywhere.
- `o3` cocycle `2^k·core` signature (`RESULTS-ENDPOINT-RESTART-COCYCLE.md`
  family `2^k 12 v`): the extremal SOURCE words begin with `1`, not a run of
  `2`s. Leading-2 run length is 0 in 38 of 39 extremal words (one lone `lead2=1`
  at n10 c3 hard-core). The `2^k`-prefix family does not describe them.
- source-word longest-common-suffix across consecutive n is small (0-4) with the
  same two isolated spikes (12, 13) as test (i); no conserved core.

No operation in the preregistered list — nor any stride — relates the extremal
states. This is consistent with the source-string negatives already in
`RESULTS-FIBER-EXTREMAL-FAMILY.md` and now confirmed at the state level.

## 4. Test (iii): alpha SUPPORT pattern in n — KILL fired

The alpha PARITY sequence along the surviving run is a bijective re-encoding of
the continuation string (`forced_high = 1^alpha`), so its variation carries no
information beyond the continuation strings already shown structureless — not
re-reported as new.

The genuinely new object, the alpha SUPPORT `{i : E_i != 0}` (nonzero cells of
the live state) at the killing row, is **dense and unstructured**: `|support|`
is 17-38 (near the full state length 2n+survival-1), the support begins
`[0,1,2,3,4,...]` (the shallow end is essentially all nonzero), and the pattern
of the few zero cells reshuffles with n with no stable offset from either index
0 or the cut end. This is the same "reshuffles with n" outcome the missing-block
sets gave in `RESULTS-FIBER-EXTREMAL-FAMILY.md` §2.

Secondary observation (reinforces an existing obstruction, not a new finding):
the density of the support means the parity flux PAS must be argued over a dense,
non-local set — matching `RESULTS-PULL-ROW-ALPHA-SUPPORT.md`'s own remarks that
"the witness displacement is not locally bounded" and "alpha changes can cancel
in pairs." The state view adds no local structure to exploit there.

## 5. What DID reproduce: within-cell forgetting (archaeology §2.2)

When two extremal live states share the same continuation (9 such classes across
all cells), they differ in a SMALL number of cells: max 4, and the differences
sit at the deep/output (high-index) end (distance-from-top 0-5, usually 0-2),
e.g. n13c2 and n19c3 differ in exactly ONE cell, the top one. This reproduces
§2.2 and independently confirms the edge orientation. One exception
(n11 c3 hard-core: two co-continuation states differ at mid indices 10-11, not
the top) is noted honestly; it does not change the picture.

So the phenomenon §2.2 named is real and robust — the forcing forgets down to
the last cell or two WITHIN a fixed n. But that forgetting is precisely why
there is no ACROSS-n family: the states that survive longest are not a
propagating structure, they are wherever the generic forgetting happens to hold
on longest at each n, and that location is not conserved.

## 6. Consequence for the cocycle proof template (honesty ceiling)

Held to the ceiling fixed in the prereg. Even setting aside the negative, the
template (`RESULTS-ENDPOINT-RESTART-COCYCLE.md`) closes its case because it has
an autonomous finite quotient of BOUNDED dimension (the L=5, period-32
traversal). Here the live-state dimension grows as 2n, and the data show:
- no fixed / periodic extremal family (tests i, ii, all strides);
- a DENSE, reshuffling kill-support (test iii), i.e. no bounded-window kill rule
  is visible — the exact thing the template would need.

So the template is **not in range** via this door. A bounded-window kill rule is
not merely underived; the state-level data are evidence against its existence in
this regime, alongside the standing closure collisions (bounded summaries
collide at lengths 8, 9, 13) and Obstruction D.

## 7. Bottom line

- The extremal forcing states are O(1) per (n,c) (1-5; confirmed), collapse
  cleanly within a fixed n (forgetting, §2.2 reproduced), and are exactly
  cross-checked against `literal_extension`.
- Across n they carry no family: not by shared prefix/suffix of the edge, not by
  any fixed operation or cocycle prepend, not by alpha-support geometry, at any
  stride, in either arm. The apparent agreements are generic forgetting, and the
  null model separates them from structure.
- Net: this closes the "compare the states across n" question the archaeology
  left open (§8.1, §11). The answer is negative. The p=2 needle remains a
  per-n exhaustive certificate; the cocycle template does not reach it here.
- Next action (a recommendation, not a claim): with the state-family route closed, the
  cheapest remaining calibration on this thread is the Rule 90 carry-kernel
  control (archaeology §8.3). Any theorem here must route through the OR collapse
  `FORWARD[2]==FORWARD[3]` (only 3 distinct left-actions), which is vacuous under
  Rule 90's XOR; the prediction is that Rule 90 gives no hard-core advantage and
  no gamma>=1. This negative removes the structural route that would have made
  that control moot, so it is now the next thing to run.

Reproduce:
```
/Volumes/A/researchpapers/.venv/bin/python3 estate_family_census.py     # -> estate_census.json
/Volumes/A/researchpapers/.venv/bin/python3 estate_family_analysis.py   # tests + null
```

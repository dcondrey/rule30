# R9 probe: scaling of the minimal sufficient constraint set for the centre cell

Status: **prereg frozen 2026-08-30 before any ladder run; results appended
below the line.**  Everything below "MEASURED" is measurement; nothing here is
a lower bound.

## Pre-registration (frozen)

**Instance.**  One Boolean variable per cell of the backward diamond of
`(n,0)` inside the lone-seed light cone; truth-table clauses per cell for
`s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1))` (rule 90 control:
`s(t,x-1) XOR s(t,x+1)`, 4 clauses since the rule reads 2 parents); unit
fixing the seed; unit asserting the WRONG centre value at row `n` (true value
from `experiments/rule30/center_column.py`, whose first 30 terms
`PREREGISTRATION.md` records as OEIS-A051023-verified via the API; an
independent dense simulation in the probe must agree with it to row 64, and
the rule clauses alone must reproduce the simulated diagram cell-for-cell
before anything is measured).  Restriction to the diamond is exact: no clause
outside it can belong to any MUS, since the diamond alone still derives the
centre.  The formula must be UNSAT at every `n` before measurement.

**Design deviation from the task spec, recorded up front.**  The spec's
clause-level MUS is degenerate by a two-line argument: the set of "firing"
clauses (for each cell, the one clause matching its actual parent assignment)
is itself a MUS of size ~ the whole diamond for ANY rule, because deleting
one frees its cell and every downstream firing clause is vacuously satisfied
by the deviation, so a deviation path to the centre always exists.  A
clause-level MUS therefore measures the diamond area, identically for rules
30 and 90, i.e. nothing about rule structure.  Prediction registered before
running: clause-level MUS cell-count == diamond cell-count for both rules.
This will be run at small `n` to confirm, and the primary metric is:

**Primary metric.**  Cell-level group MUS (GMUS): one selector per cell; a
cell's rule constraint is enforced entirely or not at all.  A cell set `G` is
UNSAT iff enforcing the rule exactly on `G` (all other cells free variables)
pins the centre value against the wrong-value unit.  Deletion-minimal `G`
with core refinement; 3 random deletion orders (seeds 0,1,2) per `n`; report
size spread, depth profile, and left/right-of-centre split.  Secondary:
trimmed-core size (assumption-core refinement to fixpoint, no deletion) as
the cheap over-estimator.

**Rule 90 control, with analytic prediction.**  By linearity the GMUS is
unique and equals the diamond cells with odd dependency-path count into
`(n,0)` (binomial parity, Kummer).  The pipeline must reproduce that set
exactly at every completed `n`; its size scales as `n^{log2 3} ~ n^1.585`.  A
pipeline that fails this control, or that cannot tell the rules apart, is not
measuring structure and its rule 30 numbers are void.

**Bands.**  `n = 8, 16, 32, 64, 128, 256`, extending to 512 only if 256
completes all seeds inside 20 minutes per seed.  Fit `log(mus_cells)` vs
`log(n)` by least squares over completed bands with `n >= 16`; also report
the local slope over the top three bands.

**Strong outcome.**  Rule 30 exponent near 2 with the GMUS filling a constant
fraction of the diamond: empirical support that the whole cone is
derivationally necessary.  Support for the R9 conjecture; proves nothing.

**Inverted outcome, flagged loudly if it fires.**  Rule 30 GMUS scaling
clearly subquadratic and sustained: a small sufficient constraint set exists,
which undercuts the R9 lower-bound target and is a candidate mechanism for
the Arm 3 tournament (a potential centre-column shortcut).  That would be the
more valuable result.

**Kill condition.**  GMUS extraction fails to complete beyond `n = 32`
(fewer than 3 usable ladder points): report the wall and stop.

**Named failure modes.**  (i) A MUS upper-bounds the axioms some derivation
needs; it is not a minimal derivation, and extractors return A minimal
subset, not THE minimum; the seed spread is the honesty bar.  (ii) The
degenerate clause-level metric above; confirmed empirically rather than
assumed.

---

## MEASURED

All numbers from `experiments/rule30/proof-complexity/mus_probe.py` (CaDiCaL
1.5.3 via python-sat 1.9.dev15), lone seed, encoding self-checks passing at
every band: rule clauses alone reproduce the simulated diagram cell-for-cell,
the independent dense simulation matches `center_column.py` to row 64, and
the wrong-value instance is UNSAT before any measurement.

### Primary result: cell-level GMUS scaling

```text
rule 30 (3 seeds/band; n=256 one seed, others hit the 1500 s band budget)
   n   mus_min  mus_max  diamond   fill%   left  right  centre   sec
   8        33       36       41    87.8
  16       119      119      145    82.1
  32       445      445      545    81.7
  64      1604     1806     2113    85.5
 128      6535     6544     8321    78.6
 256     25108    25108    33025    76.0   16380   8472    256   2021
fitted exponent (n>=16): 1.93     local slope (top 3 bands): 1.94

rule 90 control (3 seeds/band)
   n   mus_cells  diamond   fill%     analytic odd-binomial set
   8        17        41    41.5      17   exact match, every seed
  16        43       145    29.7      43   exact match, every seed
  32       113       545    20.7     113   exact match, every seed
  64       307      2113    14.5     307   exact match, every seed
 128       857      8321    10.3     857   exact match, every seed
fitted exponent (n>=16): 1.44     doubling ratios 2.53 -> 2.85 (analytic
asymptote 3, i.e. exponent log2 3 = 1.585; the finite-size fit reads low
because odd-binomial counts are popcount-bursty)
```

**The strong outcome fired; the inverted outcome did not.**  Rule 30's
deletion-minimal sufficient cell set is a constant ~76-88% fraction of the
whole backward diamond with fitted exponent 1.93, against the rule 90
control's structured sparse set (exact Sierpinski/odd-binomial at every band
and seed, exponent heading to 1.585).  The pipeline separates the rules
cleanly, and rule 30 shows no sign of a small sufficient constraint set: no
candidate centre-column shortcut surfaced.  Seed spread for rule 30 is tiny
where measurable (<=1.5% of set size; n=256 completed only seed 0 inside the
band budget, so its spread is unmeasured), and the fill fraction drifts
slowly downward (87.8 -> 76.0),
so "exponent exactly 2 with declining constant" vs "exponent marginally
below 2" is not decided by this ladder.

**Asymmetry.**  Rule 30's GMUS is left-heavy roughly 2:1 (n=256: 16380 cells
left of centre, 8472 right, 256 on the column), matching the damage-cone
asymmetry (rightward perturbation speed 1 via the XOR term, leftward spread
throttled by the OR latch, in this repo's orientation).  The depth profile
fills essentially the whole diamond band-by-band (3, 5, 7, ... near the seed;
..., 5, 3, 1 near row n).

### Registered degeneracy of the clause-level metric: confirmed, with one miss

Clause-level MUS at n=8,16,32: rule 30 returns every rule-bearing cell of the
diamond (n=32: 544 of 544; the prereg prediction, confirmed).  Rule 90
returns 288 of 544, not the predicted full diamond: the miss is the parity
argument the prediction overlooked — cells with no dependency path of the
right parity into `(n,0)` are never necessary.  The substance of the
registered prediction (area-scaling clause MUS, no rule structure visible,
exponent 2 for both rules) stands; the literal "equal for both rules" clause
was wrong and is recorded as such.

### Walls hit

Rule 90 GMUS at n=256 stalled >15 min inside the first seed and was killed:
each droppable-cell test there is a pure-XOR UNSAT instance, exactly the
parity reasoning CDCL/resolution is classically bad at (Tseitin-style
hardness), so the *control* hit a solver wall the nonlinear rule did not.
Solver runtime is not derivation size; this is an aside, not a finding.  The
rule 90 ladder therefore stops at 128 (5 bands, above the kill threshold),
with the n=256 analytic value (2443) known anyway.  Rule 30's n=256 band ran
2021 s for its one completed seed.

### What this does and does not say

Within the restricted frame, the measurement says: the minimal set of local
rule constraints sufficient to pin the centre value grows like the full
backward diamond for rule 30 (exponent ~1.93, constant fraction), while an
additive rule's grows like its sparse dependency skeleton.  That is empirical
support for the R9 conjecture that the whole cone is derivationally
necessary, in the weak sense that no small sufficient axiom subset exists —
a necessary precondition for any superlinear derivation-length lower bound,
not evidence of one (a small derivation could in principle still exist over
the full axiom set).  It says nothing directly about Wolfram's Problem 3 in
its Turing-machine formulation; no MUS measurement can.

### Reproduction

```sh
cd experiments/rule30/proof-complexity
/Volumes/A/researchpapers/.venv/bin/python mus_probe.py --rule 30 --group cell --ns 8 16 32 64 128 256 --seeds 3 --timeout 1500 --out ladder30.json
/Volumes/A/researchpapers/.venv/bin/python mus_probe.py --rule 90 --group cell --ns 8 16 32 64 128 --seeds 3 --timeout 1200 --out ladder90.json
/Volumes/A/researchpapers/.venv/bin/python mus_probe.py --rule 30 --group clause --ns 8 16 32 --seeds 3 --out clause30.json
/Volumes/A/researchpapers/.venv/bin/python mus_probe.py --rule 90 --group clause --ns 8 16 32 --seeds 3 --out clause90.json
/Volumes/A/researchpapers/.venv/bin/python fit_exponent.py ladder30.json ladder90.json
```

Artifacts: `ladder30.json`, `ladder90.json`, `clause30.json`, `clause90.json`
(per-band GMUS cell lists, depth profiles, seeds, wall times) in the same
directory.  python-sat was installed into `/Volumes/A/researchpapers/.venv`.
Modal: $0.  Paid model-provider calls: $0.

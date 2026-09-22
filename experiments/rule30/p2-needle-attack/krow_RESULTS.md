# Killing-row alignment: the archaeology §12 residual is closed, negative

Date: 2026-09-06. Preregistered in `krow_PREREG.md` (frozen before any run).
Scripts: `krow_analysis.py` (analysis), `krow_ne_census.py` (exhaustive
near-extremal null), `krow_hc_extend.py` (hard-core arm n=21..30).
Reads `estate_census.json` from the 2026-09-05 run; recomputes every row state
by re-forcing, so only the state list is inherited.

## Verdict

**NO FAMILY at any survival-anchored row.** The residual alignment that
`RESULTS-TERMINAL-CLASS-ARCHAEOLOGY.md` §12 and `estate_RESULTS.md` flagged as
untested — survival-row / killing-row alignment — was run and behaves exactly
like the row-0 alignment already reported: best cross-`n` separation fraction
**0.60**, against a family threshold of 0.70, and this holds under all three
null models built. The archaeology §12 residual is now resolved and the
"a later session must not read the negative as excluding that alignment" caveat
can be retired.

**The alignment does produce elevated agreement, and both sources of it are
generic covariates, not extremality.** This is the substantive content of the
run and the reason it is not just another table of small numbers:

* Under the preregistered null, kill anchors beat the row-0 control by up to
  **+0.60** — which looks like the convergence the alignment was designed to
  find. It is not. Two independent controls, each matching a different
  covariate, each kill a different half of the effect, and **no cell survives
  both**.
* The **suffix**-alignment signal is forced-row depth. It dies against a
  row-matched null (0.60 -> 0.20).
* The **prefix**-alignment signal is survival length. It dies against a
  near-extremal null (0.60 -> 0.13).

## 0. What the residual was, and that it is a new object

`estate_RESULTS.md` compared extremal forcing STATES across `n` at **one row
anchor: row 0**, the live state immediately after the padded source. It varied
the index-axis origin (prefix = shallow/newest, suffix = deep/cut), the relation,
the stride, the arm and the tail — never the row.

This run varies the row anchor: `K0` = the killing row (`t = survival`),
`K1` = `t = survival-1`, `K2` = `t = survival-2`, and `R0` = row 0 as the
control. The hypothesis the residual encodes is convergence — that the forcing
runs a transient and the extremal states approach a common configuration at the
moment of death — which is the reverse of the row-0 hypothesis, not a
restatement of it. States at different `n` have different survival lengths
(max_survival 4-13 over the corpus, non-monotone), so a row-0 comparison holds
them at different distances from their own kill events.

## 1. Controls (all pass)

1. **Prereg control 1: `R0` reproduces `estate_RESULTS.md` §2 exactly.** On the
   same `n` range (`--legacy-ns`, n=10..20) the best fraction by stride is
   **0.20 / 0.22 / 0.29** for strides 1/2/4, matching the published values, and
   the per-pair separations agree cell by cell (e.g. all/c=2/prefix:
   `-8 -7 -3 -4 -8 -2 -7 +0 +17 -4`, identical). On the extended range the same
   cells read 0.13/0.22/0.25 because the denominators change; the control is
   stated on the legacy range for that reason.
2. **Controls 2, 3, 5:** 106 extremal records re-forced from their row-0 live
   states; every one reproduces the stored survival and continuation, the stored
   `full_edge[:-1]` equals the stored `live_state`, and `|S(t)| = 2n+t-1` holds
   at every anchor. Zero exceptions.
3. **Control 4:** forcing found exactly one legal symbol at every row of every
   state, extremal and typical alike (a second hit or none raises).
4. **gamma >= 1 (validation, not a finding):** `survival < n+2` asserted on
   every enumerated live state including the new n=21..30 hard-core cells.

## 2. Q1 — family at a survival-anchored row: KILL FIRED

Best separation fraction over all (stride, arm, tail, anchor, alignment),
threshold 0.70:

| null model | best fraction | where |
|---|---|---|
| preregistered (typical at its own killing row) | 0.60 | stride 1, hardcore, c=3, `K0`, suffix |
| row-matched (typical forced to the same absolute row) | 0.60 | stride 1, hardcore, c=3, `K0`, prefix |
| near-extremal (longest-surviving non-extremal states) | 0.55 | stride 1, hardcore, c=3, `K0`, suffix |

No cell reaches 0.70 under any null. Q3 (fixed operation `o1`/`o2` at the
anchor) also killed: best 0.20 on the extended range, 0.14 on the legacy range.

## 3. The two controls, and why each was necessary

The preregistered null compares an extremal state at its killing row against
typical states at THEIR killing rows. Those two things differ in two ways that
have nothing to do with being extremal, and each needed its own control.

### 3.1 Row-matched null — kills the suffix signal

A typical state dies after 0-2 forced rows; an extremal state dies after 8-13.
Under the preregistered null the two sides have been forced a very different
number of times. Since the state vector grows at the deep end by one cell per
row, suffix (cut-end) alignment compares exactly the cells the forcing has just
generated, so "both have been forced ~10 times" alone produces agreement.

The row-matched null forces typical states to the SAME absolute row as the
extremal state they are compared against (forcing is defined past the hard-core
death, so this is well posed). The suffix signal collapses:

```text
stride 1, all, c=3, K1, suffix:   0.60 -> 0.20
stride 1, all, c=3, K0, suffix:   0.60 -> 0.20
stride 2, hardcore, c=3, K0, suffix: 0.56 -> 0.11
stride 4, all, c=3, K1/K2, suffix:   0.43 -> 0.00
```

### 3.2 Near-extremal null — kills the prefix signal

The row-matched null has its own defect in the other alignment: a typical state
forced past its own death has left the hard-core language (either an emitted
symbol outside `{1,2}`, or a `1` after a `1`), so its shallow (newest) cells are
non-hard-core by construction, while an extremal state's are hard-core by the
definition of survival. Prefix alignment therefore separates
"survived" from "did not", not "extremal" from "not extremal" — and indeed
`hardcore c=3 K0 prefix` scores 0.60/0.43/0.58 against the row-matched null.

Looking at the states directly shows the mechanism. The shallow ends of the
extremal states at the killing row are stereotyped low-complexity strings —
`2031` repeated, or `12` repeated:

```text
n=13 surv=5  203120312031120312000321112030
n=16 surv=6  203120312031112300323030312323
n=19 surv=8  121212121212321123000312030312
n=20 surv=8  121212121203232120032120030300
```

This is the periodic continuation before a phase slip that
`RESULTS-TERMINAL-CLASS-ARCHAEOLOGY.md` §11 already describes (relayed there
from `RESULTS-PULL-ROW-ALPHA-SUPPORT.md`). It is a property of any state that
survives long, not of the longest-surviving one. Reproducing it here is
**validation of a known structure, not a finding.**

The near-extremal null tests exactly that: the longest-surviving NON-extremal
states, anchored at their own killing rows. The prefix signal collapses:

```text
stride 1, hardcore, c=3, K0, prefix:  row-matched 0.60 -> near-extremal 0.13
stride 2, hardcore, c=3, K0, prefix:  row-matched 0.43 -> near-extremal 0.07
stride 4, hardcore, c=3, K0, prefix:  row-matched 0.58 -> near-extremal 0.17
```

The near-extremal fractions are identical to the preregistered-null fractions,
i.e. the extremal states are no more like each other than the near-extremal
states are.

### 3.3 Two deviations from the prereg, both declared

1. **The preregistered near-extremal band is unusable.** `krow_PREREG.md` §2
   implies a band `[max_survival-2, max_survival-1]`. Built EXHAUSTIVELY (not
   sampled) that band holds 0-45 states per cell — a p95 over one state is not a
   null. Substituted: the `TOPK=400` longest-surviving non-extremal states per
   cell (`krow_ne_census.py`). Each cell's actual pool survival range is stored
   as `pool_survivals` so the reader can see how near the pool really is; it is
   typically `[m-1 .. m-6]`.
2. **The hard-core arm was extended to n=21..30** (`krow_hc_extend.py`). At
   n<=20 the hard-core arm has only 50-3,013 live states, so even exhaustively
   there are too few long survivors to build the near-extremal null — and the
   hard-core arm is precisely where the prefix signal survived the row-matched
   null. The hard-core word count is `F(n+2)`, so the extension is cheap, and it
   brings the near-extremal pools to 400-750 states. Without it the decisive
   control could not have been run where it mattered.

Both deviations move in the direction of MORE power for the null, i.e. they make
it easier for the signal to survive, not harder. It did not survive.

## 4. Honest residue

* **The large separations are exact state equalities, and they are explained.**
  On the extended range the hard-core `c=3` `K0` row shows spikes at
  `n=23->24`, `26->27`, `28->29` (separations up to +66) in BOTH alignments,
  surviving both nulls. They are not coincidental shared prefixes: at those
  pairs `lcp = lcs = ` the full state length (58, 64, 69), i.e. the killing-row
  states are IDENTICAL. The mechanism is generic, not a family:

  - The 2-row forcing image of a live state at `n` is a realizable live state
    at `n+1`, with survival exactly `s-2`. Measured over EVERY live state with
    survival `>= 2`, hard-core arm, both tails, `n=10..20`: **100%**, no
    exceptions. The `n -> n+2` version (force 4 rows) is likewise 100%.

    Those two sentences were originally written from an interactive check with
    no script behind them. They are now reproduced by `fembed_lemma.py`
    (prereg `fembed_PREREG.md`, results `fembed_RESULTS.md`): 50,146 instances
    across 50 cells, 0 exceptions, with the range extended to the `all` arm and
    to hard-core `n=26`. It holds throughout. That run additionally found the
    map is NOT injective (up to 7 preimages), covers a flat ~7-10% of the next
    level, and gives a bound tight in only 7 of 50 cells.

    Two corrections to the paragraph below, both from that run. First, the
    tightness/spike correspondence is EXACT in both directions over `n=10..29`,
    not just at the three pairs named: the tight `n` are `c=2: 18, 21, 23` and
    `c=3: 10, 23, 26, 28`, and no non-tight pair in either tail separates by
    `>= +20`. `n=18` and `n=21` were missed here only because §4 looked at the
    extended range alone. Second, that run recomputes `max_survival(n,c)` by a
    different code path and matches `krow_hc_extend.json` on all 34 overlapping
    hard-core cells, so this file's `m(n)` column is independently reproduced.
  - Hence `m(n+1) >= m(n) - 2` always, and the spike pairs are exactly the `n`
    at which that generic bound is TIGHT (`m(n+1) = m(n)-2`). When it is tight,
    the extremal state at `n+1` is forced to be the 2-row image of the extremal
    state at `n`, so the two coincide exactly.
  - This is a property of the forcing map, not of extremality: it holds for all
    states, so it supports the no-family verdict rather than weakening it.

  An earlier draft of this file called these spikes "coincidental long shared
  prefixes, not structure", carrying over the reading `estate_RESULTS.md` §2
  applied to the isolated n18->19 and n14->15 spikes. On the extended range
  that reading is wrong: the states are equal, for the reason above. The
  earlier spikes at `n<=20` were not re-examined under this lens and may have
  the same cause.

* Twelve of 192 cells still have a near-extremal pool below 30 states and are
  excluded from that null (reported in the run output). They are all in the
  small-`n` hard-core arm.
* The near-extremal pool is "top 400 by survival", not literally
  `max_survival - 1`. Where a cell's pool reaches down to `m-6`, the control is
  weaker than its name suggests. This is why the pool range is stored per cell.

## 5. Consequence

The state-family door is now closed under every alignment that has been
proposed for it: prefix, suffix, containment, the `2^k` cocycle signature,
alpha-support geometry (all `estate_RESULTS.md`), and now killing-row and
survival-row anchoring at three depths. `RESULTS-TERMINAL-CLASS-ARCHAEOLOGY.md`
§12's residual is resolved.

This does not change the net verdict already recorded there: the p=2 needle is a
per-`n` certificate, the endpoint-restart cocycle template is not in range via
this door, and the honest paper result on this thread is a structured negative.
The present run removes the last flagged reason to think an alignment might yet
rescue it.

Independent of the family question, §3.1 and §3.2 are reusable: any future
comparison of extremal states across `n` must control for forced-row count and
for survival length, or it will measure them instead. Both controls are in
`krow_analysis.py` and cost nothing to reuse.

## 6. Reproduction

```bash
cd experiments/rule30/p2-needle-attack
PYTHONDONTWRITEBYTECODE=1 python3 krow_ne_census.py     # exhaustive NE null
PYTHONDONTWRITEBYTECODE=1 python3 krow_hc_extend.py     # hard-core n=21..30
PYTHONDONTWRITEBYTECODE=1 python3 krow_analysis.py      # the analysis
PYTHONDONTWRITEBYTECODE=1 python3 krow_analysis.py --legacy-ns   # control 1
```

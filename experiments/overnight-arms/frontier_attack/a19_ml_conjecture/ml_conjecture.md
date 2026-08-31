# CANDIDATE REFUTED AT DEPTH 20000 — all 30 candidates admitted by the pre-registered threshold break within 38 steps of the training boundary (first break `t = 20000` in-range, `t = 200000` out-of-range); the only extraction that survives exact checking is the OR-latch pin, so CANDIDATE CONFIRMED, KNOWN — no novelty

Arm a19, 2026-08-30.  Register row 53's ML half, which was never run.
Pre-registration: `PREREG.md`, written before the full run and after a
reduced-depth smoke test that is disclosed there.

**Prize movement: none.  P1, P2, P3 all unmoved.**

---

## 0. The discipline this arm follows, stated before any number

An ML model that predicts `c_{t+1}`, or a local window, well **is not a
mathematical result and is not reported as one here.**  This arm has exactly one
legitimate output: a precise, finite, checkable candidate statement, handed to an
exact check on a depth range disjoint from the training range.

**Obstruction H (`PATH.md` 7.3 H) is the central risk and it is unavoidable.**
Every model here is trained and evaluated inside one bounded depth range, and is
therefore incapable, by construction, of establishing an infinite statement.
`RESULTS-automaticity.md` Theorem O gives the exchange rate in the neighbouring
representation: any sequence agreeing with `a` on `[0,N)` and zero thereafter is
eventually periodic, so "`N` terms buy a kernel lower bound of about `N/8` and
nothing more, ever."  The same applies in spirit here.  **The exact check below
has exactly one power: it can refute a candidate.  It can never confirm one.**
Where a candidate survives, the only honest report is "not refuted at this
depth", and any stronger claim must come from a separate non-empirical argument.

The depth split, quoted with every number below:

```
TRAIN t in [0, 20000)          table extraction / GF(2) solve / model fit
DEV   t in [20000, 50000)      in-range holdout, ADJACENT to train
TEST  t in [200000, 500000)    OUT OF RANGE, disjoint, 10x-25x deeper
```

All three ranges are one exact integer simulation of the lone-seed diagram
(`substrate.py`, validated against the repo's A051023 generator and against an
independent naive simulator; the truncation lemma that makes it linear-ish is
stated and regression-tested there).  No sampling, no approximation, anywhere.

---

## 1. Verdict

| | outcome |
|---|---|
| **Only candidate that survives the exact out-of-range check** | the **OR-latch pin**, `c_t = 1 => c_{t+1} = NOT s(t,-1)`.  **CONFIRMED, ALREADY KNOWN** — it is `PATH.md` section 1, and `PATH.md` section 0.5 records that it was in this repo's code and proofs before `PATH.md` was written (`inverse_trace_probe.py:135-160`; `RESULTS-eventual-period.md:88-100`; regression-pinned in `test_inverse_trace_probe.py:115-117`).  **No novelty is claimed.** |
| **Every other candidate** | **REFUTED, all 30 of them.**  The pre-registered threshold admits 30 of 56 Rule 30 framings as candidates (`threshold.py`, section 1.1).  **Every one breaks in the *adjacent in-range* holdout, between `t = 20000` and `t = 20038`** — that is, within 38 steps of the training boundary — and again out of range between `t = 200000` and `t = 200040`.  An exact break witness (pattern, prediction, truth, training support) is in section 4.1. |
| **The R1-relevant framing (target B)** | **NOTHING.**  The threshold admits exactly two target-B framings; both are refuted (`W=12` at `t = 20005`/`200007`, `W=8`+`K=8` at `t = 20006`/`200005`).  The other seven are rejected on coverage.  Predicting `r_t = s(t,1)` on the zero-set `{c_t = 0}` **from the left window** sits at chance out of range at every width — `0.4986`, `0.5014`, `0.5029`, `0.5048` for `W = 12,16,20,24` — and the *empirically Bayes-optimal* predictor over the whole `W = 16` left window scores `0.4993`.  Clause (b), with the numbers. |
| **Symbolic (GF(2)) regression** | **EXACT NEGATIVE.**  No GF(2) polynomial of degree `<= 3` over any tested feature set reproduces even the *training* range, for any target-A or target-B framing.  The single exception is the positive control — the Rule 30 local rule itself, `c_{t+1} = s(t,-1) XOR (c_t OR s(t,1))`, degree 2 — which the solver recovers exactly. |
| **Rule 90 filter** | Pipeline **passes**: every Rule 90 framing is table-consistent on TRAIN with accuracy `1.0000` and coverage `1.000` at every depth, and a degree-1 GF(2) fit exists.  The pipeline detects real structure when it exists.  It does **not** report anything similar for Rule 30. |

### 1.1 The pre-registered threshold, applied mechanically

`PREREG.md` declares, before the run, that a framing yields a **candidate worth
extracting** iff (1) its exact table is consistent on TRAIN *or* its unanimous
sub-table covers `>= 20%` of TEST, (2) TEST coverage `>= 0.05`, and (3) it fails
the universality check.  `threshold.py` applies that to every Rule 30 framing
and writes `threshold_results.json` / `threshold.txt`.  For target A, condition
(3) selects the *shell* (`c_t = 0`) entries, since Lemma A19.1 proves the
universal part is exactly the pin.

```
framings considered (rule 30, non-control):   56
ADMITTED as candidates by the threshold:      30
of those, surviving the exact check:            0
first break, in-range DEV holdout:      t = 20000   (holdout starts at 20000)
last  break, in-range DEV holdout:      t = 20038
first break, out-of-range TEST:         t = 200000  (TEST starts at 200000)
last  break, out-of-range TEST:         t = 200040
```

The 26 rejected framings are rejected for a stated reason, most often coverage:
`A/left-window W=2,4,8` and `B/left-window W=2,4,8` have shell coverage exactly
`0.00000` (the extraction produces nothing off the pin), and
`B/left-window W=24`, `C/…K=16`, `B/…K=16` sit at `0.0007`, `0.0007`, `0.0011`
— memorisation, which is what condition (2) is for.  Full ledger in
`threshold.txt`.

So the threshold did work: it admitted a large family, and every member of that
family died at the first opportunity.  **Not one candidate survived even into the
holdout adjacent to its own training range**, let alone out of range.  That, and
not any accuracy number, is this arm's finding.

---

## 2. What the pipeline could possibly have found — two lemmas, proved before the run

These are in `PREREG.md` and they bound the result in advance.  They are the
reason the outcome below is not a surprise, and they are the reason the pin's
survival is not evidence the pipeline can find anything.

**Lemma A19.1 (target A is exhausted by the pin).**  Rule 30 is
`c_{t+1} = s(t,-1) XOR (c_t OR s(t,1))`.  Given only the left window
`s(t,-W..0)`, the bit `s(t,1)` is free.  The value is independent of that free
bit **iff `c_t = 1`**, where it equals `NOT s(t,-1)`.  Therefore, for every
`W >= 1`, the universal (local-rule-forced) part of any extracted target-A table
is **exactly the OR-latch pin and nothing more**.

Consequence, and it is the cleanest thing in this arm: *the pipeline recovering
the pin is not evidence that it can find real structure; it is evidence that it
correctly recovers the unique available tautology.*  Rule 90 is the only genuine
detection control.

**Lemma A19.2 (target B is necessarily orbit-specific).**  No function of
`s(t,-W..0)` equals `s(t,1)` universally over rows: two Rule 30 rows can agree on
`s(t,-W..0)` and differ at `s(t,1)`, since left permutivity constrains nothing to
the right of `0`.  So every target-B candidate fails universality by
construction, which is exactly what makes its break point genuine information —
and target B is the R1-relevant framing, register row 1 being precisely "`c`
eventually periodic forces `r` eventually periodic on `{c_t = 0}`".

**Target C is a local-rule tautology off one branch.**  With
`m_t = min{ j >= 1 : s(t,j) = 1 }` (a9's quantity), the local rule gives
`m_{t+1} = f(m_t, c_t)` in all cases except `(m_t, c_t) = (1,1)`; the three-case
derivation is in `PREREG.md`.  Mining was restricted to that one branch, and the
off-branch control confirms the tautology empirically: table CONSISTENT on TRAIN,
accuracy `1.0000` at coverage `1.000` on both DEV and TEST.

---

## 3. The confirmed-and-known candidate, stated exactly

Extracted mechanically as the universal sub-table of the target-A left-window
framing at `W = 2, 4, 8` (`extract_and_check.py`, `universal_targetA`), then
verified by exhaustive enumeration of every left-window pattern:

> **For all `t`: if `s(t,0) = 1` then `s(t+1,0) = NOT s(t,-1)`.**
> Equivalently, in the general form `PATH.md` section 1 states it:
> `s(t,x) = 1 => s(t,x-1) = NOT s(t+1,x)`.

* **Universality check, exhaustive.**  At `W = 2`: **4 of 4** extracted entries
  are forced by the local rule, `0` orbit-specific, `0` contradicting.  At
  `W = 8`: **256 of 256** universal, `0` orbit-specific, `0` contradicting.
  Lemma A19.1 exactly: the extraction finds the pin and literally nothing else.
* **Exact check on TEST `[200000, 500000)`**: the universal sub-table covers
  `150,280` of `300,000` rows (`0.5009`, i.e. every `t` with `c_t = 1`),
  **`0` errors**, accuracy `1.0000`, **no break**.  The orbit-specific
  sub-table is *empty* — coverage `0.000` — so there is nothing else to refute.
* **Exhaustive identity check**, general form, all columns `x` in `[-23, 24]`,
  all `499,999` row-pairs to `t = 500000`: **`11,998,050` ones tested, `0`
  violations.**
* **Rule 90 on the same check**: `2,322` ones tested, **`2,322` violations** —
  every single one.  And Rule 90's target-A table at `W = 2` has **0 of 4**
  entries universal.  Rule 90 has no pin, exactly as `PATH.md` section 1's
  separator table says ("**90: pins on none**").

**This is not new and is not claimed as new.**  It is `PATH.md` section 1, and
section 0.5 of that document exists precisely because an earlier draft presented
the pin as new when it was already in the repo's code and proofs.  Rediscovering
it by a machine-learning route adds nothing mathematical.  What it does add is a
calibration point: it is the *only* thing the whole sweep found that survives.

It does pass the Rule 90 filter — `PATH.md` section 1 records that Rule 90
violates the same identity at all 7,227 of its ones, and the pipeline reproduces
the structural half of that here (Rule 90's target-A tables have pin-core
coverage `0.000`, there being no `t > 0` with `c_t = 1`).

---

## 4. The refutations — the actual finding

Every framing below is an *orbit-specific* claim (it fails the universality
check of section 2 by construction).  Each was extracted as an exact discrete
lookup table on TRAIN and then checked exactly.  **All numbers with the depth
split `TRAIN [0,20000) / DEV [20000,50000) / TEST [200000,500000)`.**

### 4.1 The pin core versus the accidental shell

This is the mechanical separation of signal from overfit, and it is the sharpest
table in the arm.  `core` = table entries used at `c_t = 1`; `shell` = entries
used at `c_t = 0`.

| target-A framing | TEST acc (all) | TEST cov | **core acc** | **core cov** | **shell acc** | **shell cov** | shell first break, DEV | shell first break, TEST |
|---|---|---|---|---|---|---|---|---|
| left-window `W=2` | 1.0000 | 0.501 | **1.0000** | 1.000 | n/a | 0.000 | none | none |
| left-window `W=4` | 1.0000 | 0.501 | **1.0000** | 1.000 | n/a | 0.000 | none | none |
| left-window `W=8` | 1.0000 | 0.501 | **1.0000** | 1.000 | n/a | 0.000 | none | none |
| left-window `W=12` | 0.8425 | 0.677 | **1.0000** | 0.924 | **0.5014** | 0.428 | `t = 20005` | `t = 200007` |
| left-window `W=16` | 0.7564 | 0.138 | **1.0000** | 0.142 | **0.4986** | 0.134 | `t = 20063` | `t = 200038` |
| left-window `W=20` | 0.7579 | 0.010 | **1.0000** | 0.010 | **0.5029** | 0.009 | `t = 20495` | `t = 200520` |

Read it in one line: **the core is exact at every depth and every width, because
it is a theorem; the shell is at chance and breaks within 5 to 520 steps of the
training boundary, because it is memorisation.**

**The exact break witness**, `W = 12` (`extract_results.json`,
`orbit_specific_break_witness`).  The extracted table has `5545` entries, of
which `3787` are universal (the pin) and `1758` are orbit-specific.  Split and
checked separately on TEST:

```
universal sub-table       covered 138,906 / 300,000   errors      0   acc 1.0000  no break
orbit-specific sub-table  covered  64,150 / 300,000   errors 31,985   acc 0.5014  break at t = 200007
```

and the first breaking row, in full:

```
t                                 200007
window s(t,-12..0)                0 0 0 0 1 0 1 1 0 0 1 1 0
predicted c_{t+1}                 0
actual    c_{t+1}                 1
training rows supporting it       1
```

One training row.  That is the whole mechanism of the shell: a pattern seen
once, at one depth, promoted to a rule, wrong the next time it occurs.  The
orbit-specific sub-table's accuracy of `0.5014` over 64,150 predictions is a
coin.  The overall accuracy column
(`0.8425`, `0.7564`, `0.7579`) is exactly the kind of number that must never be
reported alone — it is a mixture of a theorem at 1.0 and noise at 0.5.

### 4.2 Target B — the R1-relevant framing.  Two candidates admitted, both refuted.

Predicting `r_t = s(t,1)` on the zero-set `{c_t = 0}`, which is register row 1's
obligation.  Rows in **bold** are the two that the pre-registered threshold
admitted as candidates; the rest are rejected on coverage.

| framing | DEV acc | DEV cov | DEV break | TEST acc | TEST cov | TEST break |
|---|---|---|---|---|---|---|
| left-window `W=2,4,8` | n/a | 0.000 | — | n/a | 0.000 | — |
| **left-window `W=12`** | 0.4977 | 0.427 | `20005` | 0.5014 | 0.428 | `200007` |
| left-window `W=16` | 0.5228 | 0.131 | `20063` | 0.4986 | 0.134 | `200038` |
| left-window `W=20` | 0.5468 | 0.009 | `20495` | 0.5029 | 0.009 | `200520` |
| left-window `W=24` | 0.7778 | 0.001 | `29848` | 0.5048 | 0.001 | `205113` |
| **`W=8` + col-history `K=8`** | 0.7597 | 0.260 | `20006` | 0.7452 | 0.247 | `200005` |
| `W=8` + col-history `K=16` | 0.6667 | 0.002 | `22958` | 0.7636 | 0.001 | `217642` |

Two things a reader must not over-read.

* At `W = 2,4,8` the coverage is **zero**: every pattern that occurs in TRAIN
  carries both labels, so no candidate exists at all.  That is the extraction
  refusing to produce anything, not a failed prediction.
* At `W = 24` the table is *nearly* consistent on TRAIN (1 conflicted pattern out
  of many thousands) — and its TEST coverage is `0.001`.  **That consistency is
  vacuous**: 25 bits over 20,000 training rows gives roughly one sample per
  pattern, so unanimity is arithmetic, not structure.  This is why the
  pre-registered extraction threshold requires TEST coverage `>= 0.05`.

The `0.745` figure in the col-history rows is **not** structure either, and it
has an exact local-rule explanation, measured rather than asserted
(`extract_results.json`, `targetB_0.75_explanation`).  The local rule gives
`s(t,1) = c_{t-1} XOR (s(t-1,1) OR s(t-1,2))`, so the naive predictor
`s(t,1) := NOT c_{t-1}` — available to any framing handed the centre history —
is right exactly when `s(t-1,1) OR s(t-1,2) = 1`.  Measured on TEST restricted
to `{c_t = 0}`:

```
base rate P(s(t,1) = 1 | c_t = 0)                   0.5001736574939888   <- chance
P(s(t-1,1) OR s(t-1,2) = 1 | c_t = 0)               0.7493187282928132
acc of the naive predictor s(t,1) := NOT c_{t-1}    0.7493187282928132
logistic regression, TEST out-of-range accuracy     0.7493187282928132
```

Those last three are the **same number to sixteen digits**.  Logistic
regression, given a 33-bit feature set, learned exactly one step of the Rule 30
local rule and the local one-density, and nothing else.  A `0.75` on target B is
the CA rule looking at itself.

### 4.2.1 Where the above-chance accuracy comes from — decomposed exactly

`ceiling.py` / `ceiling_results.json`, TEST `[200000, 500000)`, restricted to
`{c_t = 0}`.  Column 3 is the exact majority (empirically Bayes-optimal) table
for that feature set; column 4 is the unanimous table, i.e. the only *discrete
candidate* the feature set admits, with its exact break.

| feature set | bits | majority table, TEST acc | unanimous table: cov / acc / **first break** |
|---|---|---|---|
| chance (base rate of `s(t,1)` on `{c_t=0}`) | — | `0.5002` | — |
| one-step local rule, `s(t,1) := NOT c_{t-1}` | — | `0.7493` | — |
| **left-window `W=16` alone** | 17 | **`0.4993`** | `0.134` / `0.4986` / `200038` |
| col-history `K=16` alone | 16 | `0.5665` | `0.251` / `0.7701` / `200026` |
| left-window `W=8` + col-history `K=8` | 17 | `0.5605` | `0.247` / `0.7452` / `200005` |
| left-window `W=16` + col-history `K=16` | 33 | `0.4998` | `0.0000134` / `0.5000` / `221139` |

The load-bearing row is the third: **the best possible predictor of `s(t,1)`
from the left window alone is at chance out of range.**  That is the R1-relevant
question, and the answer is that the left window carries no usable information
about the zero-set's right neighbour at all.  Every above-chance number in the
table comes from the centre-column history feature, and section 4.2 shows that
channel is one step of the CA rule.

The last row is the memorisation diagnostic: at 33 bits the training table is
*fully consistent* (`0` conflicted patterns) and out of range it covers
`1.3 x 10^-5` of the rows and scores `0.5000`.  Consistency at high bit count
means nothing.

One loose end, stated rather than smoothed over: the depth-6 decision tree
reaches `0.8016` out of range on the 33-bit set, above the `0.7493` one-step
rate — presumably by partially reconstructing row `t-1` from the left window,
which is again the local rule, though this arm did not decompose that residual
`0.05`.  It does not create a candidate: the tree has only **2** pure leaves on
TRAIN, they cover `3.1%` of TEST, and they **break at `t = 202318`** with 146
errors.

### 4.3 Target A from the centre column alone — an exact negative

| framing | TRAIN table | TEST acc | TEST cov | DEV break | TEST break |
|---|---|---|---|---|---|
| col-history `K=4` | **all 16 patterns conflicted** | n/a | 0.000 | — | — |
| col-history `K=8` | **all 256 patterns conflicted** | n/a | 0.000 | — | — |
| col-history `K=12` | 3416 conflicted | 0.4992 | 0.159 | `20005` | `200000` |
| col-history `K=16` | 1310 conflicted | 0.5000 | 0.243 | `20012` | `200000` |
| col-history `K=20` | 79 conflicted | 0.4931 | 0.019 | `20062` | `200038` |
| `K=8` + `t mod 2,3,4` | all patterns conflicted | n/a | 0.000 | — | — |
| `K=8` + `t mod 6` | 1533 conflicted | 0.5108 | 0.002 | `20877` | `200703` |
| `K=8` + `t mod 8` | 2014 conflicted | 0.4892 | 0.017 | `20102` | `200228` |
| `K=12` + `t mod 16` | 1323 conflicted | 0.5011 | 0.244 | `20003` | `200006` |

The `K = 4` and `K = 8` rows are the crispest statement in this section and are
exact, not statistical: **every** binary word of length 4, and **every** binary
word of length 8, that occurs in the centre column on `[0, 20000)` is followed by
both a `0` and a `1`.  The centre column is not an order-4 or order-8 Markov
process, with no exceptions to enumerate.  Adding `t mod p` for `p = 2, 3, 4`
does not create a single unanimous pattern either.

This is the finite-order-memory hypothesis dying, and it is adjacent to register
row 46 (the Ore/2-automaticity ladder).  It does **not** touch that row: an
order-`K` Markov table is a much weaker object than a `k`-state automaton, and
obstruction H applies to both.  Nothing here bounds the automaticity of A051023.

### 4.4 Targets C and D

* **C**, the one branch `(m_t, c_t) = (1,1)` that the local rule leaves
  undetermined: best framing `left-window W=12`, TEST accuracy `0.6476` at
  coverage `0.550`, first break DEV `t = 20038`, TEST `t = 200040`.  Refuted.
  The off-branch control is exact at coverage `1.000` as derived.  Declared in
  advance: `m` is a right-side quantity and P1/P2 are column-0 statements, so
  nothing on this branch could have been the headline even had it survived.
* **D**, the periodicity-break indicator `1[c_t != c_{t+p}]` for `p = 1..8`:
  the strongest is `p = 2`, left-window `W=12`, TEST accuracy `0.8796` at
  coverage `0.733`, first break DEV `t = 20005`, TEST `t = 200017`; restricted to
  the zero-set, `0.8786` at coverage `0.727`, same breaks.  All eight periods
  break within 20 steps of the start of both holdouts.  Every centre-history
  framing is at chance (`0.4986`–`0.5030`).

**A reader must not read target D as a test of a1's Lemma Z.**  Lemma Z's
predicate is conditional on the centre trace being `p`-periodic — a
counterfactual on the lone-seed orbit, where the trace is not periodic at any
`p <= 8` at any of these depths.  Target D measures a different thing: whether
`c_t != c_{t+p}` is locally predictable on the *actual* orbit.  It is not.  The
same caution applies to a2's missing lemma, whose hypothesis is a `(01)^inf`
centre trace, again not this orbit.  Neither lemma is re-fitted here and neither
is touched by these numbers.

---

## 5. Symbolic regression: an exact negative

The GF(2) stage solves for a polynomial over the feature bits with monomials of
degree `<= d` that reproduces TRAIN *exactly* (Gaussian elimination over GF(2);
an inconsistent system means no such polynomial exists, which is a proof, not a
fit quality).  Every claimed fit is re-verified against TRAIN by an assertion.

* Rule 30, targets A and B, every framing tested (`col-history K<=12`,
  `left-window W<=8`): **no exact fit exists at degree 1, 2 or 3.**
* Positive control, target A with the full window `W = 1`: exact fit at degree 2
  and 3 — the solver recovers the Rule 30 local rule itself.
* Rule 90: exact fit at degree 1 for every framing tested, as it must be, Rule 90
  being additive.

This satisfies hypothesis H4's kill condition in the pre-registration, and it is
worth more than any accuracy number in this document: it is an exact statement
about a finite algebraic search, with no depth caveat inside the training range.

---

## 6. Controls

**Rule 90 (the `PATH.md` section 0 filter).**  Identical pipeline, identical
depth split.  Every one of the 51 Rule 90 framings: table CONSISTENT on TRAIN,
DEV accuracy `1.0000` coverage `1.000`, TEST accuracy `1.0000` coverage `1.000`,
no break; GF(2) exact fit at degree 1 wherever tested.  Rule 90's lone-seed
centre column is `1` then `0` forever, so this is the trivial-structure case, and
the pipeline finds it instantly and perfectly.  Two conclusions, both needed:

1. the pipeline **can** detect real structure — it is not silently broken;
2. it reports **nothing** resembling that for Rule 30, which is the separation
   the filter is for.

Rule 90's pin-core coverage is `0.000` in every target-A framing, an independent
reproduction of `PATH.md` section 1's table entry "**90: pins on none**".

**Local-rule positive control.**  Target A with the full window `W = 1` is the
Rule 30 rule itself: table CONSISTENT, accuracy `1.0000` coverage `1.000` on DEV
and TEST, GF(2) exact at degree 2.

**Vacuity control.**  TEST coverage is reported for every framing.  Three
framings are table-CONSISTENT on TRAIN with TEST coverage `<= 0.002`; all three
are memorisation, and the pre-registered threshold excludes them.

**Model-class ceiling (accuracy only, and reported only with its exact check).**
Fitted to target B on the zero-set over `left-window W=16` + `col-history K=16`,
TRAIN `[0,20000)`, evaluated on TEST `[200000,500000)`:

| model | TRAIN acc | TEST out-of-range acc |
|---|---|---|
| chance (base rate) | — | `0.5002` |
| logistic regression | `0.7504` | `0.7493` (= the one-step local rule, to 16 digits) |
| decision tree, depth 6 | `0.8060` | `0.8016` |
| decision tree, depth 14 | `0.9992` | `0.7177` |
| random forest, 200 trees | `1.0000` | `0.7597` |
| MLP 64x64 | `0.9707` | `0.7352` |

The pattern is the ordinary one: capacity buys training accuracy (`1.0000` for
the forest) and buys nothing out of range.  The only *extractable* object among
them, the depth-6 tree's pure-leaf rule set, has **2 leaves**, covers `3.1%` of
TEST, and **breaks at `t = 202318`** (146 errors).  These numbers exist to answer
one question — is there juice the exact tables missed? — and **no conclusion in
this document rests on any of them.**

---

## 7. Single-column sensitivity (`PATH.md` 0.1)

Recorded in the pre-registration before the run, and repeated here because the
answer is "the filter does not bite the same way, and that is not a licence".

The candidates in this arm are **pointwise predictions that read column 0 and its
immediate neighbours directly**, not averages over the `~2t` cells of a row.
Overwriting column 0 with a periodic word (`discriminator.py`'s field `B`)
changes their inputs and their targets outright, so they move by `O(1)`, not
`O(1/W)`, and they pass the filter **vacuously**.  Passing it is therefore
necessary and not sufficient here, and no weight is placed on it.  The filter
retires *column-blind* quantities; it says nothing in favour of a
column-sensitive one, and the refutations in section 4 are the operative test.

---

## 8. What a reader must not over-read

1. **No prize problem moved.**  P1, P2, P3 are exactly where they were.
2. **The pin is not new.**  `PATH.md` section 1 and section 0.5.  Rediscovering
   it by an ML route is a calibration point, not a contribution.
3. **No accuracy number here is a result.**  Every one of them is either
   (i) a theorem at `1.0000` (the pin, the local rule), (ii) chance
   (`~0.50`), or (iii) a mixture of the two, or a one-step consequence of the CA
   rule leaking through the features (the `0.745` rows).  None survives an exact
   check on any orbit-specific part.
4. **Obstruction H is not evaded and cannot be.**  Everything here lives inside
   `t < 500000`.  A candidate surviving to `t = 500000` would still establish
   nothing; the only reason section 3's candidate can be asserted for all `t` is
   the separate, non-empirical universality argument, which is a proof about the
   local rule and not about depth.
5. **Target D does not test a1's Lemma Z, and target B does not test a2's
   missing lemma.**  Both of those are conditional on a periodic centre trace,
   which is a counterfactual on this orbit.  Section 4.4.
6. **Section 4.3 does not touch register row 46.**  An order-`K` Markov table is
   far weaker than a `k`-state automaton, and no automaticity bound follows.
7. **A19.1 means target A could never have produced anything else.**  The
   pipeline's reach on that target is the pin, provably, so the pin's survival
   is not evidence of detection power.  Rule 90 is the only detection control.

---

## 9. Register entry proposed

| # | Approach | Prize | Status | Why it stopped | Where |
|---|---|---|---|---|---|
| — | ML / symbolic regression as a conjecture generator for a finite-state or algebraic invariant of the centre column (row 53's unrun ML half) | 1,2 | **KILLED** | The only extracted candidate surviving an exact out-of-range check is the OR-latch pin, already `PATH.md` section 1 and provably the *unique* local-rule tautology the target-A framing can reach (Lemma A19.1); the pre-registered threshold admits 30 of 56 framings as candidates and **all 30 break inside the adjacent in-range holdout**, between `t = 20000` and `t = 20038`, i.e. within 38 steps of the training boundary, and again out of range between `t = 200000` and `t = 200040`.  The R1-relevant framing (predict `r_t` on `{c_t = 0}` from the left window) yields no candidate at all, and its empirically Bayes-optimal predictor is at chance out of range (`0.4993`).  No exact GF(2) polynomial of degree `<= 3` reproduces even the training range for any Rule 30 framing, against a degree-2 hit on the local-rule control and degree 1 on Rule 90.  Rule 90 control solves perfectly and instantly at every framing. | `a19_ml_conjecture/ml_conjecture.md` |

---

## 10. Reproduction

```
cd experiments/overnight-arms/frontier_attack/a19_ml_conjecture
uv run python substrate.py            # exactness self-test against repo ground truth
uv run python mine.py 30 90           # the sweep    -> mine_results.json
uv run python report.py               # clean table  -> report.txt
uv run python extract_and_check.py    # extraction + universality + exact check
                                      #              -> extract_results.json
uv run python ceiling.py              # target-B decomposition
                                      #              -> ceiling_results.json
uv run python threshold.py            # apply the pre-registered threshold
                                      #  -> threshold_results.json, threshold.txt
```

Artifacts: `PREREG.md`, `substrate.py`, `mine.py`, `report.py`,
`extract_and_check.py`, `ceiling.py`, `threshold.py`, `mine_results.json`
(109 records), `report.txt`, `extract_results.json`, `ceiling_results.json`,
`threshold_results.json`, `threshold.txt`, `smoke.log` (the disclosed
reduced-depth smoke test).
No model weights are kept: nothing in this arm's conclusions depends on a fitted
model, only on exact tables and exact GF(2) solves.

Fence: every write is inside this directory.  No `uv add` (packages via
`uv pip install`; the repo has no root `pyproject.toml` and none was created).
No git commits.  `experiments/rule30/` and `docs/` were read only.

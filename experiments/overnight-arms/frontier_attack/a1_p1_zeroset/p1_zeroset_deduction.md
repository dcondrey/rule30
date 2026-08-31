# NEGATIVE-NAMES-MISSING-LEMMA

**Missing lemma, named in the first line as required: LEMMA Z, the zero-phase
defect exclusion.**  R1 is, exactly and after all reductions, the statement

> **LEMMA Z.**  Let `s` be the Rule 30 space-time diagram of a nonzero finite
> configuration, `D(t,x) = s(t+p,x) XOR s(t,x)`.  If `c_t = c_{t+p}` for every
> `t >= t_0`, then `D(t,1) = 0` for every `t >= t_1` with `c_t = 0`.

Nothing below proves Lemma Z, and nothing below refutes it.  Everything below is
either a measurement of its finite shadow or a proof about a different rule.  No
route in this document reaches Lemma Z without a step of the form "for a
sufficiently long agreement window", which is precisely the missing-lemma shape
that killed register rows 19 and 21-24.

Route: R1 (`docs/rule30/PATH.md` section 4, register row 1).  Prize problem 1.
No git commit.  Modal `$0`, paid model-provider calls `$0`.

**Fence compliance.**  Every file written by this session is in this directory.
One disclosed exception, the same one register row 70 records: the read-only
imports of `experiments/overnight-arms/common/rule30.py` and
`common/ensemble_filter.py` caused CPython to write
`common/__pycache__/{rule30,ensemble_filter}.cpython-311.pyc`.  No source file
outside this directory was modified.  (`docs/rule30/PATH.md` shows as modified in
`git status`; that predates this session and is not this session's edit.)

---

## 1. STEP 0, the mandated test: the kill condition did NOT fire

**Mandated question.**  Register row 38 records that the finite rows `{0}` and
`{0,1}` have the same centre trace at every checked step.  Do they, or any small
pair of finite rows with equal centre traces, have DIFFERENT right-neighbour
columns restricted to the zero set `Z = {t : c_t = 0}`?

**Answer: no.  Not for that pair, and not for any of the 10,749 exactly
enumerated finite-seed pairs whose centre traces do not separate within the
4,000-step horizon.**

`step0_zeroset_determination.py` -> `step0_output.{txt,json}`,
`verify_infinite_collisions.py` -> `verify_infinite_collisions_output.{txt,json}`.
Both cross-validate their simulation against
`experiments/overnight-arms/common/rule30.py::simulate_seed` at every run.

Row 38's pair, `T = 4000`:

```text
seeds {0} and {0,1}: centre traces agree for all 4000 steps
  |Z| = 2018      r differences on Z = 0
  r differs anywhere at exactly 2 times, t = 0 and t = 1, both with c_t = 1
  leftmost differing column at time t: 1,1,3,3,5,5,7,7,...  (~ +t, escaping right)
  the defect front is at column <= 1 at 2 of 4000 times, last at t = 1
```

Exhaustive sweep over every finite seed supported in `[0,w)` with `s(0,0)=1`
(`verify_infinite_collisions.py`, horizon 4000, seeds grouped by their 24-step
centre prefix, then every pair scanned to the first centre separation):

| rule | `w` | pairs whose centre traces do not separate before `t = 4000` | of those, with an `r` defect at a `c_t = 0` time | with an `r` defect at a `c_t = 1` time |
|---|---:|---:|---:|---:|
| 30 | 10 | 511 (`= 2^9 - 1`) | **0** | 17 |
| 30 | 12 | 2047 (`= 2^11 - 1`) | **0** | 21 |
| 30 | 14 | 8191 (`= 2^13 - 1`) | **0** | 25 |
| 90 | 10, 12, 14 | 0 | 0 | 0 |

Total: **10,749 pairs, zero zero-set `r` disagreements.**

**These are not proved to be infinite collisions; they are collisions to the
horizon.**  Two pieces of evidence that they are nonetheless not a horizon
artifact:

* *Cap independence.*  `cap_independence.py` -> `cap_independence_output.{txt,json}`
  fixes `w = 12` and varies the cap over 400 / 4,000 / 40,000.  The count is **2047 = 2^11 - 1 at all three caps**, with 0 zero-set `r`
  defects and 21 one-phase defects at both 4,000 and 40,000.
  A cap artifact would move with the cap.
* *A recorded mechanism for one member.*  For `{0}` vs `{0,1}`,
  `RESULTS-periodicity-bridge.md` section 3 already states the moving-defect
  certificate -- "at every checked even time `t`, the two full configurations
  differ only at `x = t+1`; at every checked odd time they differ only at `x = t`
  and `x = t+1`" -- and calls it "a simple induction target".  The
  `defect_front` output above (`1,1,3,3,5,5,...`) is that invariant measured.
  Column 1 lies outside `{t, t+1}` for every `t >= 2`, so `r` agrees from `t = 2`
  with no reference to any horizon.  **That induction is recorded for this one
  pair only.  It is not proved here for the other 10,748, and this document does
  not claim it.**

Rule 30's count is exactly `2^{w-1} - 1` at every width tried, which is worth
recording on its own: the trace-collision classes partition the `2^{w-1}` seeds
into one connected family, not into scattered accidental pairs.

Two things in that table.

1. **The zero-set obligation is decidable from `c` alone across every genuine
   finite-seed trace collision reached.**  The surviving `r` disagreements sit
   *only* at `c_t = 1` times, which is exactly where the OR-latch pin absorbs
   them: `d_t(-1) = (1 XOR c_t) AND d_t(1)` makes a one-phase right defect
   invisible at column `-1`.  This is the pin doing the work PATH.md section 2
   says it does, measured rather than asserted.
2. **Rule 90's centre trace is injective on this family** (zero collisions at
   every `w`), so the Rule 90 branch is a live control that could have shown the
   collision phenomenon to be rule-generic and did not.

### 1.1 A false positive, recorded so it is not repeated

A fixed-horizon version of this sweep (`T = 400`) reported 18 "hits" at `w = 16`
and 558 at `w = 20`: pairs with equal centre traces over the window and `r`
differing on `Z`.  All of them are horizon artifacts.
`step0b_collision_detail.py` -> `collision_detail_output.txt`: every one of the
18 has its `r|Z` disagreement at `t = 399` and its centre traces separating at
`t = 400`, and **0 of 18** still have equal centre traces at `T = 40,000`.

**Superseded numbers, named so nobody reads them off the JSON.**
`step0_output.json` retains the fields `n_pairs_r_differs_on_zero_set = 18`
(`sweep_rule30_w16`) and `= 558` (`sweep_rule30_w20`).  Both are the artifact
described in this subsection.  The replacement figures are the margin histogram
below and the table in section 1.

The scale-free replacement is the **margin**

```text
A = first t with c_t(a) != c_t(b)                     (centre separation)
D = first t < A with c_t = 0 and r_t(a) != r_t(b)     (zero-set r defect)
margin = A - D
```

`step0c_margin.py` -> `margin_output.{txt,json}`, over every pair agreeing on a
24-step centre prefix:

```text
rule 30, w=14:  1,469,876 pairs; margin 1: 1,461,685; no zero-set defect: 8,191; max margin 1
rule 30, w=16: 23,582,131 pairs; margin 1: 23,549,364; no zero-set defect: 32,767; max margin 1
rule 90, w=14 and w=16: 0 pairs (no prefix agreement at all)

(the "no zero-set defect" buckets are exactly the 2^{w-1} - 1 non-separating
pairs of the table above, re-counted by a second independent script)
```

**Margin is exactly 1 in all 25.0 million cases.**  A zero-set `r` disagreement
between two distinct finite seeds of width `<= 16` never precedes the centre
separation by more than a single step.  That is the sharpest form of "step 0's
kill did not fire".

---

## 2. What DID fire: Rule 90 refutes the rule-generic form of R1

`rule90_zeroset_counterexample.py` -> `rule90_output.{txt,json}`.

Rule 90, lone seed:

* `c_t = 0` for every `1 <= t < 65536` (verified), so `c` is eventually periodic
  with period 1 and `Z` is cofinite;
* `r_t = s(t,1) = 1` **exactly** at `t in {1, 3, 7, 15, ..., 65535}`, i.e. at
  `t = 2^j - 1` (verified to `T = 65536`; consecutive gaps
  `2, 4, 8, ..., 32768`, strictly increasing).

*Proof of the second line.*  For the Rule 90 lone seed
`s(t,x) = C(t,(t+x)/2) mod 2` when `t+x` is even.  At `x = 1` this needs `t` odd;
with `t = 2m+1` it is `C(2m+1, m) mod 2`, which by Kummer's theorem is odd iff
`m AND (m+1) = 0`, i.e. iff `m = 2^j - 1`, i.e. `t = 2^{j+1} - 1`.  A binary word
with infinitely many ones and unbounded gaps between them is not eventually
periodic.  QED.  (A finite search for an eventual period of `r|Z`, all
`p <= 4096` and all onsets `t_0 <= 512`, also returns nothing; that search is a
check, the Kummer argument is the proof.)

So **Rule 90 has `c` eventually periodic and `r` provably aperiodic on the zero
set.**  That is verbatim R1's kill condition, fired on the filter rule.  Rule 90
is left-permutive, quiescent, additive, and its configuration here is the same
lone seed, so:

> **No proof of R1 can be rule-generic over the left-permutive quiescent ECAs.
> Any proof must use an ingredient Rule 90 lacks.**

The available ingredient is the OR-latch pin, and this run re-measures the
separation exactly as PATH.md section 1 records it: at `T = 300`, the identity
`s(t,x)=1 => s(t,x-1) = NOT s(t+1,x)` has **45,477 antecedents and 0 violations
for Rule 30**, and **7,227 antecedents and 7,227 violations for Rule 90**.  Rule
90 violates it at every single one of its ones.

**Consequence, and it retires step 0's own framing.**  Rule 90's centre trace is
*injective* on the finite-seed family of section 1 (zero collisions at every `w`
tried), so for Rule 90 the zero-set obligation IS decidable from `c` alone on
that family -- and the implication still fails.  Conversely, non-decidability
would not refute an implication about eventual periodicity, since two diagrams
sharing a centre trace can have `r|Z` eventually periodic with different periods.
**Decidability of `r|Z` from `c`, and the truth of R1's implication, are
logically independent in both directions.**  R1's stated kill condition ("if the
zero-set obligation is not decidable from `c` alone, R1 dies") is thus a weaker
trigger than it reads; here it did not fire, and firing it would not have settled
R1 either.

This does not weaken R1.  It is a constraint on any proof of it, and it is why
PATH.md's "R1 passes the Rule 90 filter by construction" is the right thing to
have said: the *target statement* fails for Rule 90, so passing the filter is not
optional here, it is forced.

---

## 3. The pairing R1 actually needs, and the phase of row 37's defects

R1's hypothesis is about ONE diagram whose centre is eventually periodic.  By
register row 31 that is the stroboscopic pairing: the lone-seed diagram against
its own time shift by `p`.  The distinct-seed sweep of section 1 is a different
and much more rigid object; the two disagree, and the difference is the point.

`rule30_agreement_runs.py` -> `agreement_runs_output.{txt,json}`.

**Row 37 reproduced exactly.**  Longest run with `c_t = c_{t+p}`:
`18` at `p = 148, t_0 = 1855` (`T = 4096, p <= 256`) and `24` at
`p = 110, t_0 = 13219` (`T = 16384, p <= 512`).  The defect identity
`D(t,-1) = (1 XOR c_t) AND D(t,1)` holds at **0 violations in 2,065,066 checks**.

**The question row 37 left open, answered.**  Row 37 recorded that adjacent
columns carry a defect during those runs but not the *phase* of the defect.  The
phase is what R1 turns on: a column-1 defect at `c_t = 1` is absorbed by the pin,
one at `c_t = 0` is a finite instance of R1's kill shape.

```text
T=4096,  p<=256, runs of length >= 12:  116 runs; 100 have a zero-phase r defect, 16 do not
T=16384, p<=512, runs of length >= 16:   67 runs;  57 have a zero-phase r defect, 10 do not
row 37's own 24-step run (p=110, t0=13219): 9 zero-phase times, 1 zero-phase r defect,
                                            3 one-phase r defects, first defect AT the run start
```

So on the stroboscopic pairing, zero-phase column-1 defects **do** occur, and
they occur deep inside centre-agreement windows, not at the edge.  The margin
histogram (`step0c_margin.py`, `T = 16384`, `p <= 512`, 2.06 million runs):

```text
margin: 1       2       3      4      5      6     7     8    9   10  11  12 13 14 15 16 17 18 19 20 22 24
count:  423945  213025  106577 52630  26584  13371 6704  3386 1647 764 420 196 102 53 26 14  8  5  1  1  2  1
plus 1,214,434 runs with no zero-phase r defect at all
max margin 24 (p=110, t0=13219 -- row 37's run, with the defect at its first step)
```

That is a clean geometric distribution with ratio `~1/2`, truncated at `24`.
Rule 90 control, same statistic: **max margin 4094 of a 4096-step window**, i.e.
the whole diagram, at `p = 1, 2, 3, 4, 5, ...` simultaneously.

**Summary of the contrast, which is the substantive content of this document:**

| pairing | rule | largest margin found | what an infinite margin would mean |
|---|---|---:|---|
| distinct finite seeds, width `<= 16` | 30 | **1** (25.0M pairs) | -- |
| stroboscopic, `t <-> t+p` | 30 | **24** | R1 false, P1 unresolved by this route |
| stroboscopic, `t <-> t+p` | 90 | **4094 (= the window)** | R1's analogue is false for Rule 90, proved in section 2 |

---

## 4. Why no finite search can settle it: the margin's finite shadow is the null

`run_length_scaling.py` -> `run_length_scaling_output.{txt,json}`.  The longest
centre-agreement run in Rule 30's lone-seed column, against the same statistic on
20 seeded Bernoulli(1/2) words of identical length:

| `T` | `P` | `log2(TP)` | Rule 30 longest run | Bernoulli null mean | null `[min, max]` |
|---:|---:|---:|---:|---:|---|
| 1024 | 64 | 16.00 | 15 | 15.35 | [14, 18] |
| 2048 | 128 | 18.00 | 16 | 17.15 | [15, 21] |
| 4096 | 256 | 20.00 | 18 | 19.35 | [17, 23] |
| 8192 | 256 | 21.00 | 18 | 20.65 | [18, 25] |
| 16384 | 512 | 23.00 | 24 | 22.50 | [20, 28] |
| 32768 | 512 | 24.00 | 24 | 23.05 | [21, 28] |
| 65536 | 512 | 25.00 | 24 | 24.25 | [22, 28] |

Rule 30 sits inside the null's observed range at every point, and the margin
histogram in section 3 is geometric with ratio `1/2`, which is the same fact
stated as a distribution.  Rule 90's value is the entire window at every `T`.

**Consequence.**  The largest margin obtainable by search grows like
`log2(T * P)`.  Doubling the horizon buys one more step of margin.  R1's kill
condition needs margin `= infinity`.  This is `PATH.md` obstruction H with an
exchange rate attached, and it is the reason no enlargement of section 3's search
can decide R1 in either direction.

**This is NOT a fourth instance of obstruction A, and must not be cited as one.**
Obstruction A is one-bit-per-step propagation loss, a property of the diagram.
The bound here is coincidence statistics of a single pseudorandom word: the
Bernoulli control reproduces it exactly, so it would hold for *any* word of
comparable statistics, Rule 30 or not.  It is a bound on **searching**, not a
property of Rule 30.  `PATH.md` section 3.1 is therefore right that R1 is not a
propagation-depth question; what this section adds is that R1's *finite shadow*
is nevertheless capped at `log2` of the search volume, for an unrelated and
rule-independent reason.  Same rate, different mechanism, and only the rate is
what stops the search.

---

## 5. STEP 1: declined, with the reason stated up front as required

No SAT or transducer instance was built.  The brief permits a positive
deliverable only as a core SCHEMA uniform in `p`, or an explicit statement that
the sweep found none.  This is the latter, and the reason it is the latter is
specific rather than budgetary:

* **How an instance here would have differed from register row 32's SMT
  exhaustion:** it would restrict variables to the zero-set transition logic
  (`c_t = 0 => l_t = c_{t+1} XOR r_t`) and anchor the `c_t = 1` half with the
  pin, rather than instantiating the whole causal cone.  That is a smaller
  instance of the same statement.
* **Why that difference does not help.**  Row 32 already recorded that the UNSAT
  cores have no stable one-bit conflict pattern, with both their times and their
  sizes moving with `w` and `p`.  R7 rungs 0 and 1 then retired the three levers
  that could have stabilised them -- depth `R`, the boundary pin, and the bound
  `Q` -- with `RESULTS-ladder-rung1.md` Corollary 2 proving
  `plain(R+1) ⊆ pin(R) ⊆ plain(R)`, so the pin buys strictly less than one
  column.  A smaller instance of a system whose verdict is uniform in every
  available parameter returns the same verdict.
* **What was swept instead, and the schema question it answers.**  Section 3 is a
  sweep of exactly the zero-set transition logic, over `p = 1..512` and
  `t < 16384`: 2.06 million centre-agreement runs, each one a bounded instance of
  "the zero-set obligation at period `p`".  **No `p`-uniform structure was
  found.**  The margin histogram is geometric with ratio `1/2` independent of
  `p`, the maximum tracks `log2(TP)` and not `p`, and the runs realising the
  maximum occur at unrelated periods (`110, 328, 500, 423, 306`) and unrelated
  onsets.  A `p`-uniform core schema, had one existed, would have shown up here
  as a `p`-independent structure in which runs terminate.  It did not.

---

## 6. Verdict, and what a reader must not over-read

**Verdict: NEGATIVE-NAMES-MISSING-LEMMA.**  R1 is not killed and not advanced.
Lemma Z is named in line 1 and is not proved here.

Standing filters, both applied and both passed by the *objects* reported:

* **Rule 90 filter.**  Run as a live control in every script.  It is not
  decorative here: section 2 shows R1's target statement is FALSE for Rule 90, so
  the filter bites on the statement and not merely on candidate proofs.
* **Single-column sensitivity (PATH.md 0.1).**  Every quantity in this document
  is a function of columns `-1, 0, +1` only, evaluated pointwise in `t`.
  Overwriting column 0 with a periodic word changes the margin histogram
  completely rather than by `O(1/W)`, because `Z` is defined by column 0 and the
  margin is defined by column 0's agreement times.  These statistics are not
  column-blind; that is the one structural property they have.

**Must not be over-read:**

1. **Zero zero-set disagreements across 10,749 non-separating finite-seed pairs
   is NOT evidence for R1.**  Those pairs are a degenerate family: their
   differences sit in the right band near `x ~ +t`, so left-permutive
   reconstruction from `(col_0, col_1)` forces agreement everywhere to the left
   automatically.  It is a finite window over supports of width `<= 16`, and the
   stroboscopic pairing -- the one R1 needs, with supports of size `~t` --
   already violates the same rigidity at margin 24.
2. **Margin 24 is NOT evidence against R1.**  Section 4 shows the value is
   indistinguishable from a Bernoulli(1/2) null at every horizon.  A finite
   margin, however large, is compatible with Lemma Z; only an infinite one is
   not.  Register row 37's counterexamples are 18 and 24 steps, and obstruction H
   bounds what those can mean to nothing.
3. **Section 2 does not kill R1.**  Rule 90 refutes the rule-generic form of R1's
   implication, not R1 itself.  Note also that Rule 90 has an *injective* centre
   trace on the finite-seed family of section 1 and still fails the implication:
   decidability of `r|Z` from `c` and the truth of R1's implication are
   logically independent, in both directions.  R1's stated kill condition ("if
   the zero-set obligation is not decidable from `c` alone, R1 dies") is
   therefore a weaker trigger than it reads: firing it would not by itself refute
   the implication, and here it did not fire anyway.
4. **The row 37 phase answer is new bookkeeping, not a theorem.**  That
   zero-phase column-1 defects occur inside centre-agreement runs was not
   previously recorded; it is a measurement over 2.06 million runs, and it is
   what makes the "distinct seeds vs stroboscopic" contrast in section 3
   meaningful.  It proves nothing about infinite runs.
5. **Nothing here is a Lean artifact and nothing here contains `sorry`.**

**What would move R1, stated so the next session does not repeat this one.**
Only an argument that bounds the margin *uniformly in the horizon*.  Every object
in this tree that could do so has been retired: bounded-depth propagation
(row 2), the run-of-ones wedge (row 3), the omega-automaton ladder at fixed depth
(rows 7, 54-56, obstruction F), and bounded SMT (row 32, obstruction H).  Lemma Z
needs the pin used at infinite horizon, and no mechanism in this tree does that.

---

## Reproduction

From this directory, in order.  All stdlib; `uv run python <script>`.

```bash
uv run python step0_zeroset_determination.py    # -> step0_output.{txt,json}      (~10 min)
uv run python verify_infinite_collisions.py     # -> verify_infinite_collisions_output.{txt,json}
uv run python step0b_collision_detail.py        # -> collision_detail_output.{txt,json}
uv run python step0c_margin.py                  # -> margin_output.{txt,json}      (~15 min)
uv run python rule90_zeroset_counterexample.py  # -> rule90_output.{txt,json}
uv run python rule30_agreement_runs.py          # -> agreement_runs_output.{txt,json}
uv run python run_length_scaling.py             # -> run_length_scaling_output.{txt,json}
uv run python cap_independence.py               # -> cap_independence_output.{txt,json}   (~20 min)
```

Every script cross-validates its simulator against
`experiments/overnight-arms/common/rule30.py::simulate_seed` (and, for Rule 90's
centre column, against
`experiments/overnight-arms/common/ensemble_filter.py::center_column`) before
producing any number, and aborts on mismatch.

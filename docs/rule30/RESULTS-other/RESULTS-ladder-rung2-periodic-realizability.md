# R7 rung 2: realizability from spatially periodic diagrams

Status: **realizability PROVED for `w = 01` at every `R` and `k`, and for
every `q` that is not a multiple of 420 -- unconditionally, from four finite
tori.  NOT a complete limitation theorem: the `q` divisible by 420 are not
covered, and the registered prediction that would have covered them was
REFUTED.  No `Thm(2)`, and nothing here bears on P1, P2 or P3.**

**Corrections 2026-09-09:** the conclusion for q not divisible by 420
stands, with a one-letter bridge repairing the pinned splice at its seam.
The literal splice in section 3 can fail that pin; its original checker
omitted the seam. Also, the T<=24 census does **not** imply every remaining
witness must be aperiodic: larger periods are unexcluded. The original a7
i.o. lemma is weaker than aperiodicity and already follows from the prior
five-zero theorem; the even-q gap remains. See
[the rung-3 audit](RESULTS-ladder-rung3-io-and-aperiodicity-audit.md) for
the exact witnesses, uniform splice repair, and code verification. These
corrections supersede the stronger readings in sections 5 and 8 below.

Date: 2026-09-07.  Code: `experiments/rule30/ladder-rung2/` (new; no frozen
experiment code was modified -- `experiments/rule30/ladder/ladder.py` is
imported read-only).  Modal: $0.  Paid model-provider calls: $0.

Evidence levels: `U` uniform proof, `R` reduction, `C` finite certificate,
`M` measurement, `K` kill, `I` infrastructure.

| # | Claim | Level |
|---|---|---|
| 1 | Four explicit `N x T` tori are Rule 30 diagrams with `col_0` exactly `01`-alternating and `col_{-1}` of minimal period 4, 6, 10, 14 | `C` |
| 2 | Each supplies, for **every** `R >= 1` and `k >= 1`, a word in the ladder's mode (ii) language `S_{R,k}(01,q)` for every `q` not divisible by its period | `U` (Theorem C) |
| 3 | Hence no EMPTY verdict is obtainable for `w = 01` at any depth for any `q` not a multiple of 420; `S(1..Q)` likewise for every `Q <= 13` | `U` |
| 4 | Census of alternating-centre tori: the achievable `col_{-1}` periods are exactly `{4,6,10,14}` for every even time period `T <= 24` | `C` |
| 5 | Registered "2 x prime" prediction (`T = 22` gives period 22) | `K`, refuted |
| 6 | `p = 1` control: a constant centre column forces a constant `col_{-1}` (rung 0's EMPTY, re-derived) | `U` (Lemma C1) |
| 7 | Rule 90 control: `L_90` is a bijection, so every time-periodic pair is a torus and every period is free | `U` |

## 0. What is and is not established

**Established.**  Rung 1 section 6's third ingredient -- *realizability* -- for
the tail word `01` and every `q` not divisible by 420, unconditionally and
uniformly in `R` and `k`.  The witnesses are four finite tori, each verified
against the forward rule and each fed through the unmodified ladder engine.
In particular `q = 1`, the value rungs 0 and 1 actually ran, is now proved
NONEMPTY at every depth rather than measured NONEMPTY to `R <= 7`.

**Not established.**  The complete mode (ii) limitation theorem.  The
achievable minimal periods of `col_{-1}` over *time-periodic* diagrams form,
as far as the census reaches, the finite set `{4,6,10,14}`, whose lcm is 420;
every `q` divisible by 420 is out of reach of this method, and the
prediction registered in section 2 that would have made the family unbounded
was refuted at `T = 22`.  Nothing here proves or disproves anything about
Wolfram's Problems 1, 2 or 3: a limitation theorem kills a *method*.

## 1. The gap being attacked

`docs/rule30/RESULTS-ladder-rung1.md` section 6 names the one missing
ingredient of the R7 periodicity ladder:

> For every `R`, exhibit an infinite letter word whose derived `col_0` is
> eventually `01`-periodic and whose `col_{-1}` is **not** eventually
> `q`-periodic.

Two ingredients are already in hand there (saturation of the wedge checks;
the true lone-seed prefix).  `FINDINGS.md` row 77 /
`experiments/overnight-arms/frontier_attack/a7_ladder_realizability/` closed
ladder **mode (i)** with the half-plane construction `X(k,w)` (Theorem A), and
reduced **mode (ii)** to one unproved statement about that particular object:

> **i.o. lemma (a7, unproved).**  `col_1(t) = 1` for infinitely many `t` with
> `col_0(t) = 0`, in `X(k, 01)`.

An `i.o.` statement about a single chaotic orbit is not finitely checkable, so
that route cannot be closed by certificate.  **This session attacks the same
gap with an object for which "infinitely often" is a finite check: a
spatially periodic Rule 30 diagram.**

## 2. Pre-registration

Written before any code in `experiments/rule30/ladder-rung2/` was run.

**Task.**  Decide whether some spatially periodic Rule 30 diagram supplies the
missing realizability ingredient for `w = 01`.  Concretely: let `F_N` be Rule
30 on `Z_N`.  Search the attractor cycles of `F_N` for a cell `j` whose column
`t -> F_N^t(c)[j]` is exactly `01`-alternating along the cycle (temporal
period 2), and record the minimal temporal period `T'` of the column at cell
`j-1` (which is `col_{-1}` when cell `j` is re-labelled `x = 0`).

**Why this could close the gap.**  On a cycle every column is exactly
periodic, so `col_{-1}` is not eventually `q`-periodic **iff** `T'` does not
divide `q` -- an infinite statement decided by a finite certificate.  A family
with `T' -> infinity` would give, for every `q` and every bounded-universal
`Q`, a witness at every `R` (one diagram serves all `R` at once, since letters
at depth `R` are just columns `R-1, R` of the same diagram), which is the
complete mode-(ii) limitation theorem.

**Baseline.**  (a) a7's `X(k,01)`: mode (ii) conditional on the unproved i.o.
lemma.  (b) rung 0 / rung 1: NONEMPTY at `R <= 7` by automaton search, a
finite measurement that proves nothing about all `R`.

**Metrics.**
* `M1` existence: for each `N`, the number of attractor cycles carrying an
  alternating cell.
* `M2` `T'`: minimal temporal period of the left-neighbour column, per witness.
* `M3` machine check: feed the spliced letter word (lone-seed prefix of length
  `saturate`, then the periodic tail) to the **unmodified**
  `experiments/rule30/ladder/ladder.py` `step_window`, at `R = 1..12`,
  `k = 1..4`; record rejections, derived-column mismatches, pin violations.

**Strong outcome.**  Witnesses with unbounded `T'`, machine-verified, giving:
ladder mode (ii) can never return EMPTY for `w = 01`, at any `R`, any `q`, any
`Q`, with or without the pin.  Together with row 77's mode (i) result that
closes R7 as a route to `Thm(2)`.

**Kill conditions** (registered before the run; each can fire on a plausible
negative).
* `K1` No attractor cycle of `F_N` for any `N <= N_max` carries an alternating
  cell.  Then this route is dead as stated and the session reports the
  negative, plus whatever structural reason the data suggests.
* `K2` Alternating cells exist but `T'` is bounded by some `B` over the whole
  search.  Then only `q` not divisible by the achieved periods are covered;
  the limitation theorem is partial and must be reported as partial.
* `K3` The splice is rejected by `ladder.step_window` at any `R, k`.  Then
  rung 1 section 6's saturation/prefix ingredients as I have read them are
  wrong, and this session's premise dies.
* `K4` **Soundness control (this is the one that can embarrass the pipeline).**
  Run the identical search for the `p = 1` words.  Rung 0 and rung 1 both
  report mode (ii) EMPTY for `w = 1` and for `w = 0` (`q = 1`, `R <= 2`).  So
  the search **must not** produce a periodic witness with a non-constant
  `col_{-1}` for `w = 0` or `w = 1`.  If it does, my splicing argument is
  wrong and everything here is void.
* `K5` Rule 90 control.  The rule 90 analogue is run.  Note the direction: for
  a *limitation* theorem a rule 90 witness is expected and is not a defect
  (register row 5 / a7 section 3), because mode (i)'s constraint set uses only
  left permutivity.  `K5` fires only if the rule 90 run contradicts a decided
  rule 90 verdict, which would again indicate a pipeline error.

**What this cannot do.**  Nothing here bears on P1, P2 or P3.  A complete
mode-(ii) limitation theorem *kills a method*; it says nothing about whether
the Rule 30 centre column is eventually periodic.

### 2.1 How the registered conditions came out

| condition | outcome |
|---|---|
| `K1` no alternating cell anywhere | **did not fire** -- witnesses exist at `T = 4, 6, 10, 14` |
| `K2` periods bounded | **FIRED** -- bounded by 14 over the whole census; the strong outcome (unbounded family) was not obtained, and the prediction that would have delivered it was refuted at `T = 22` |
| `K3` splice rejected by the engine | did not fire -- 0 rejections in 192 checked `(R,k)` cases, and Lemma R3 makes it uniform |
| `K4` a `p = 1` witness appears | did not fire -- provably cannot (Lemma C1), matching rung 0's EMPTY |
| `K5` rule 90 contradicts a decided verdict | did not fire -- rule 90 behaves exactly as rung 0's Calibration B requires |

So the session lands between its strong outcome and its kill: a real theorem
over a restricted set of `q`, and an explicit reason why the rest is out of
reach.

## 3. The object, and why a finite torus settles an infinite statement

Write `L_T` for the leftward transduction acting on pairs of **cyclic**
length-`T` words -- adjacent columns of a diagram that is `T`-periodic in
time:

```text
L_T(A,B) = (W,A),   W(t) = A(t+1) XOR (A(t) OR B(t))      [rule 30]
                    W(t) = A(t+1) XOR B(t)                 [rule 90]
```

**Lemma R1 (rightward extension = preimage).**  A pair `(col_x, col_{x+1})`
extends to a column `col_{x+2}` iff it has an `L_T`-preimage; by rung 1
Lemma 1 that is exactly the boundary pin `col_{x+1}(t) = 1 => col_x(t) = NOT
col_{x+1}(t+1)`, and then `col_{x+2}` is forced where `col_{x+1}(t) = 0` and
free where `col_{x+1}(t) = 1`.  *(Restated from rung 1; verified in
`test_rung2.py`.)*

**Lemma R2 (finiteness collapse).**  For a function on a finite set,
`intersection_k image(L^k)` is exactly the union of its cycles.  A
`T`-periodic column pair therefore extends rightward to **every** depth `R`
iff it lies on a cycle of `L_T` -- iff the diagram is periodic in space as
well as in time, i.e. an `N x T` torus, `N` = the cycle length.  ∎

Lemma R2 is what makes this route different from every earlier attempt at the
gap.  On a torus every column is *exactly* periodic, so

> `col_{-1}` is not eventually `q`-periodic  **iff**  `p` does not divide `q`,
> where `p` = the minimal temporal period of `col_{-1}`,

which turns rung 1's infinite quantifier ("not eventually `q`-periodic") into
arithmetic on one integer read off a finite object.  The a7 route
(`FINDINGS.md` row 77) needed the opposite: an `i.o.` statement about a single
chaotic orbit, which is not finitely checkable at all.

**Lemma R3 (splice).**  Let `X` be any Rule 30 diagram defined at every column.
Feed the ladder the true lone-seed letter word for the first
`saturate = R + 2|x_min| + 1` letters and `X`'s own letters
`(col_{R-1}(t), col_R(t))` thereafter.  Then:

1. every wedge/edge check fires at a letter time `cnt < saturate`
   (`ladder.step_window` runs no check once `cnt >= saturate`), and at those
   times the whole window consists of lone-seed letters, so the derived
   columns are the true lone-seed columns and every check passes -- the
   lone-seed diagram satisfies `col_x(t) = 0` for `t < |x|` and
   `col_x(|x|) = 1` on both edges (rule 30 sends `001 -> 1` and `100 -> 1`);
2. once the window holds only `X`-letters, the derived `col_0` and `col_{-1}`
   are exactly `X`'s columns, because the inverse transduction is exact;
3. the Buchi onset is guessed, so `col_0` need only be eventually `01`.  ∎

Ingredients 1 and 2 of rung 1 section 6 are the two halves of Lemma R3 and are
re-verified here against the real engine (`test_saturation_no_wedge_check_after_saturate`,
`test_lone_seed_prefix_is_accepted`).  Ingredient 3 is Theorem C.

## 4. THEOREM C: the four certificates

Each row is an `N x T` torus, given by its centre column `col_0 = U` and
`col_1 = V`; all other columns are generated by `L_T` and the object closes up
after `N` columns.  Every torus was re-derived from the **forward** rule alone
(`verify_torus`, all `N*T` cells) and by plain cyclic row simulation
(`test_torus_matches_independent_row_simulation`).

| `T` | `N` | `col_0` | `col_1 = V` | `col_{-1}` | minimal period `p` |
|---:|---:|---|---|---|---:|
| 4 | 7 | `0101` | `1100` | `0111` | 4 |
| 6 | 84 | `010101` | `110100` | `011111` | 6 |
| 10 | 155 | `0101010101` | `1101000100` | `0111111111` | 10 |
| 14 | 728 | `01010101010101` | `11001101000100` | `01110111111111` | 14 |

> **Theorem C.**  Let `X` be one of these tori, with `col_{-1}` of minimal
> period `p`.  For every `R >= 1`, every `k >= 1` and every `q >= 1` with
> `p` not dividing `q`, the spliced word of Lemma R3 is accepted by the R7
> ladder in mode (ii) at `(R, k, w = 01, q)`, with or without the boundary
> pin.  Hence `S_{R,k}(01,q) != empty` for **every** `R` and `k`, and no
> emptiness verdict is obtainable there at any depth.

*Proof.*  `X` is a Rule 30 diagram at every column (verified cell by cell), so
its letters exist at every `R` and the ladder's derived columns are `X`'s
columns.  Lemma R3.1 discharges the wedge and edge constraints; R3.2--3 give
`col_0` eventually `01`-periodic; `col_{-1}` is exactly `p`-periodic, so it
differs from its `q`-shift infinitely often iff `p` does not divide `q`.  The
pin holds because `X` carries a genuine `col_{R+1}` (rung 1 Lemma 1).  ∎

**Corollary C1.**  With `p in {4,6,10,14}` and `lcm(4,6,10,14) = 420`: the
ladder can never return EMPTY for `w = 01`, at any `R`, `k`, for **any `q` that
is not a multiple of 420**.  In particular `q = 1`, the value rungs 0 and 1
ran, is dead at every depth -- previously a measurement to `R <= 7`, now a
theorem.

**Corollary C2.**  The bounded-universal mode `S(1..Q)` (rung 0 section 6) is
nonempty at every `R`, `k` for every `Q <= 13`: the `T = 14` torus has
`col_{-1}` of minimal period 14, which divides no `q <= 13`.

## 5. MEASURED: the census of alternating-centre tori

Two independent implementations, agreeing exactly where they overlap:
`cycle_core.py --mode exhaustive` (functional squaring over all `4^T` states;
no undecided cases by construction) and `sweep_all.py` + `resolve.py`
(vectorised orbit test with an explicit `lambda`/`mu` resolution; reports
UNDECIDED rather than guessing).  A third, `cyclic_search.py`, enumerates the
dual object -- cyclic Rule 30 on `Z_N` for `N <= 22`, all `2^N` states, cycles
extracted by functional squaring -- and finds alternating cells only at
`N = 7, 14, 21`, all of temporal period 4 with `col_{-1}` of period 4: the
`T = 4` torus and its spatial repeats.  The `T = 6, 10, 14` tori have spatial
periods 84, 155, 728 and are invisible to that sweep, which is why organising
the search by *time* period is what made the census possible.

| `T` | 2 | 4 | 6 | 8 | 10 | 12 | 14 | 16 | 18 | 20 | 22 | 24 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| max minimal period of `col_{-1}` | -- | 4 | 6 | 4 | 10 | 6 | 14 | 4 | 6 | 10 | -- | 6 |
| cyclic core size (exhaustive) | 3 | 31 | 99 | 119 | 598 | 1159 | | | | | | |
| undecided candidates after resolution | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

`--` means no alternating-centre torus with `col_{-1}` of period `>= 3`.  For
`T <= 12` the census is over *all* periods and the exact multiset is: `T = 2`
no tori at all; `T = 4` four tori, all `p = 4`; `T = 6` six, all `p = 6`;
`T = 8` four, all `p = 4`; `T = 10` ten, all `p = 10`; `T = 12` ten, four with
`p = 4` and six with `p = 6`.  Periods 1 and 2 never occur: an alternating
centre column forces `col_{-1} = 1` on the odd phase (section 4's
`test_alternating_centre_forces_col_m1_on_the_odd_phase`), and the constant
completion of that is exactly rung 1 Lemma 4's collapse state, whose centre is
constant rather than alternating.  For `T = 14..24` the search enumerated
candidates with `p >= 3` only, since `p <= 2` witnesses are worthless (they
kill no even `q`).

`T <= 12` is exhaustive over all `4^T` states.  `T = 14..24` enumerates every
`col_1` against the alternating centre (`2^T` candidates, 4.19M at `T = 22`,
16.77M at `T = 24`), kills the pin-violating ones, and resolves every survivor
to on-cycle or not; **no candidate anywhere was left undecided**, so these are
decisions, not timeouts.

`resolve.py` sorts every candidate into **four** classes, not three, and the
four sum to the candidate count exactly:

| `T` | candidates | pin-dead | on-cycle | off-cycle | undecided |
|---|---:|---:|---:|---:|---:|
| 10 | 960 | 910 | 5 | 45 | 0 |
| 14 | 16,128 | 15,778 | 7 | 343 | 0 |
| 20 | 1,046,528 | 1,040,826 | 7 | 5,695 | 0 |
| 22 | 4,190,208 | 4,176,018 | 0 | 14,190 | 0 |
| 24 | 16,769,024 | 16,733,918 | 5 | 35,101 | 0 |

*Off-cycle* is a candidate that survives the pin for `K` steps and whose orbit
closes into a cycle within `lambda`, but a cycle it is not itself a member of:
a transient, decided and decided negative.  Earlier runs printed only three of
the four classes, so `candidates - pin_dead - on_cycle` left an unexplained
35,101 at `T = 24` that reads like an undecided residue and is not one.  The
`off_cycle` field was added so the arithmetic balances on its face; the
verdicts are unchanged.

**The registered prediction was refuted.**  Section 2 of
`experiments/rule30/ladder-rung2/PREDICTION-T22.md`, written before the
`T = 22` run was read, predicted a torus with `col_{-1}` of minimal period 22,
on the reading that new periods appear exactly at `T = 2p'` with `p'` prime
(4, 6, 10, 14 = 2 x 2,3,5,7).  `T = 22` has **zero** alternating-centre tori
with `col_{-1}` of period 11 or 22, and zero undecided candidates.  `T = 24`
then added nothing beyond 6.  So the `2 x prime` reading is dead and the
achievable period set is, as far as the census reaches, the finite set
`{4,6,10,14}`.  That is kill condition `K2` firing, and it is why
section 0 does not claim a complete limitation theorem.

**Sharper consequence, and the useful part of the negative.**  Because every
`q` divisible by 420 is a multiple of all four achievable periods, *no
time-periodic diagram of period `T <= 24` can witness those `q` at all*.  Any
escape there must have a `col_{-1}` that is not eventually periodic -- which is
exactly a7's object `X(k,01)` and exactly its unproved i.o. lemma.  The
remaining mode-(ii) question is therefore no longer "find any witness"; it is
"is there an aperiodic one", the same zero-set question as register row R1.

## 6. Controls

**`K4` -- the `p = 1` calibration, which is the one that could have fired.**
Rungs 0 and 1 both decide mode (ii) EMPTY for `w = 0` and `w = 1`.  A method
that produced a `p = 1` witness would be unsound.  This one provably cannot:

> **Lemma C1.**  Let `(U,V)` be a rule-30 column pair on a cycle of `L_T`.
> If `U = 0` then the pin forces `V(t) = 1 => V(t+1) = 1`, so `V` is
> cyclically constant, and `col_{-1} = W = V` is constant.  If `U = 1` then
> `W = rot(U) XOR (U OR V) = 1 XOR 1 = 0`, constant.  Either way `Diff_q`
> never fires and there is no witness.  ∎

Checked exhaustively over the cyclic cores for `T <= 10`: 2 tori with `w = 0`
and 1 with `w = 1` at each `T`, **0** with a non-constant `col_{-1}`.  The
ladder's `p = 1` EMPTY verdict is reproduced inside the construction, not
assumed.

**`K5` -- the Rule 90 control, and where the Rule 90 filter bites.**  For rule
90 the extendability condition is vacuous (rung 1 Lemma 1'), so `L_90` is a
**bijection** (verified: `|image| = 4^T` for `T <= 5`, and every `T <= 10`
state is on a cycle).  Every time-periodic pair is therefore a torus, and
`col_{-1} = rot(U) XOR V` can be given any word at all: rule 90 admits
witnesses of period exactly `T` for every `T` (measured 2, 4, 6, 8, 10 at
`T = 2..10`, each with a forward-rule-verified torus).  So for rule 90 the
mode-(ii) limitation is complete and trivial, while for rule 30 the same
search returns 2-10 survivors out of millions.  **That gap is the OR:** the
pin is nonvacuous exactly for rule 30, it is what kills the `p = 1` case
(Lemma C1) and what makes 22 fail, and it is why the rule 30 and rule 90
`p = 1` verdicts land on opposite sides -- EMPTY for rule 30, NONEMPTY for
rule 90 -- reproducing rung 0's Calibration A and B inside this construction.
A limitation theorem is not required to separate the rules; what the control
must show, and does, is that the machinery is not silently proving the same
thing for both by ignoring the rule.

## 7. Machine verification against the unmodified engine

`ladder_splice.py` imports `experiments/rule30/ladder/ladder.py` read-only and
drives its own `step_window` with the spliced word.

| witness | rows checked (`R = 1..12` x `k = 1..4`) | rejections | centre mismatches | `col_{-1}` mismatches | pin antecedents | pin violations |
|---|---:|---:|---:|---:|---|---:|
| `T = 4`, `N = 7` | 48 | 0 | 0 | 0 | >0 at every `R` | 0 |
| `T = 6`, `N = 84` | 48 | 0 | 0 | 0 | >0 at every `R` | 0 |
| `T = 10`, `N = 155` | 48 | 0 | 0 | 0 | >0 at every `R` | 0 |
| `T = 14`, `N = 728` | 48 | 0 | 0 | 0 | >0 at every `R` | 0 |

Pushed further as an edge check, since Theorem C claims *every* `R` and `k`:
the `T = 14` witness at `R = 1..20`, `k = 1..6`, `q = 13` (120 rows) and the
`T = 6` witness at `R = 1..25`, `k = 1..8`, `q = 4` (200 rows) -- 0 failures in
both.

This is exhaustive rather than a sample for the safety constraints: the engine
runs a wedge/edge check only while `cnt < saturate`, so feeding
`saturate + 8` letters decides all of them.  "centre/`col_{-1}` mismatches"
compare the ladder's own derived `c_val` / `m1_val` against the torus columns
at the correct delay, so the engine is provably reading the object claimed.

`Diff_q` counts on the ladder's own derived `col_{-1}`, horizon 2,000 tail
samples (`diffq.py`), fire exactly when `p` does not divide `q`, at every
witness:

```text
T= 4 (p=4)  q=1..8 : 1000, 999, 998, 0, 998, 997, 996, 0
T= 6 (p=6)  q=1..12: 666, 666, 666, 665, 664, 0, 664, 664, 664, 663, 662, 0
T=10 (p=10) q=1..20: 400 ... 398, 0, 398 ... 396, 0
T=14 (p=14) q=1..28: 570 ... 567, 0, 566 ... 563, 0
```

**Cross-check against the engine's own verdicts.**  `ladder.decide` was run
directly, unmodified, on the cases Theorem C covers and on one it does not:

| `R`,`k` | `q` | states | verdict | covered by Theorem C? |
|---|---:|---:|---|---|
| 1,1 | 1 | 132 | NONEMPTY | yes (`p=4`) |
| 2,2 | 1 | 1,445 | NONEMPTY | yes (`p=4`) |
| 2,2 | 4 | 4,121 | NONEMPTY | yes (`p=6`) |
| 2,2 | 6 | 5,913 | NONEMPTY | yes (`p=4`) |
| 2,2 | 7 | 6,809 | NONEMPTY | yes (`p=4`) |
| 1,1 | 420 | 23,592 | NONEMPTY | **no** |
| 2,2 | 420 | 376,857 | NONEMPTY | **no** |

The first five are a consistency check: had any come back EMPTY, Theorem C
would be wrong.  The last two are a *measurement*, not a theorem -- they say
the residual `q = 420` is also escaped at `R <= 2`, by a lasso whose
`col_{-1}` period does not divide 420 and which, by section 5, cannot be a
torus of time period `<= 24`.  Nothing follows for larger `R`.

`test_rung2.py`: 10 tests, all passing, covering the forward-rule check of
every witness torus, an independent row simulation, the saturation and
lone-seed-prefix ingredients against the real engine, the spliced-word
acceptance, Lemma C1, the rule 90 bijection, and the odd-phase identity
`col_0(t) = 1 => col_{-1}(t) = 1`.

## 8. Honest scope

* This is a limitation result about a *method*.  It says nothing about
  whether the Rule 30 centre column is eventually periodic, and it is not
  evidence either way for P1, P2 or P3.
* Theorem C is uniform in `R` and `k` but **not** in `q`.  The multiples of
  420 are untouched, and section 5 shows this method cannot touch them:
  a witness there must be time-aperiodic.
* The census is exact for even `T <= 24` and says nothing about `T > 24`.
  "The achievable set is `{4,6,10,14}`" is a bounded census, level `C`, not a
  theorem.  If some larger `T` did supply a new period the corollaries
  would strengthen automatically.
* a7's Theorem B (`FINDINGS.md` row 77) remains conditional on its i.o. lemma
  and is not used anywhere above.  Nothing here proves or refutes that lemma;
  section 5 only shows what an escape at the residual `q` would have to look
  like, which is what that lemma asserts.
* Corollary C2 covers `Q <= 13` for the bounded-universal mode.  Rung 0
  section 6's `N_base` artifact warning still applies to any EMPTY reported at
  large `Q`; nothing here changes that.
* The one prediction this session registered in advance was refuted.  It is
  recorded in section 5 rather than deleted.

## 9. Reproduction

```sh
cd experiments/rule30/ladder-rung2
uv run python cyclic_search.py --rule 30 --nmin 3 --nmax 16      # dual view
uv run python cycle_core.py --mode exhaustive --tmin 2 --tmax 12 # census, exact
uv run python sweep_all.py  --tmin 14 --tmax 20                  # large T
uv run python resolve.py -T 22 -K 20000 --lam 2000000            # the refutation
uv run python ladder_splice.py -T 14 -U 01010101010101 -V 11001101000100
uv run python controls.py                                        # K4 and K5
uv run python diffq.py
uv run --with pytest python -m pytest test_rung2.py -q            # 10 passed
```

## Correction, 2026-09-09

Section 5's closing sentence -- "the remaining mode-(ii) question is therefore
no longer 'find any witness'; it is 'is there an aperiodic one', the same
zero-set question as register row R1" -- is correct up to the semicolon and
wrong after it.  See `docs/rule30/RESULTS-four-convergent-statements.md` §2.3.

The two are the same *question* asked of two different universes, not the same
*statement*.  R1 is about the lone-seed diagram; mode (ii) is about `L(R,k)`,
a sound over-approximation containing non-realizable words.  Only `mode (ii)
EMPTY ==> Thm(2) ==> R1's p=2 instance` transfers.  The reverse does not, and
the relaxed form of R1's conclusion is already false at `q=1`
(`experiments/rule30/r1-zero-set-attack/RESULTS-R1-ZERO-SET-ATTACK.md` §3
extracts the witness from the unmodified `rung1.decide_pin`).

Section 1's "i.o. lemma (a7, unproved)" is also stale: it was proved in
`RESULTS-ladder-rung3-io-and-aperiodicity-audit.md` §1 from prior theorem R5.

One addition, not a correction: section 4's four tori are **proved** Rule 30
diagrams with an exactly `01`-alternating `col_0`.  They therefore supersede
the empirical `{1,4}` wallpaper of `RESULTS-alt-trace-fiber.md` as the witness
that such diagrams exist, and are the proved statement of why any argument for
the lone-seed or left-finite case must use finiteness of the seed.

# R7/R1 reconciliation: the per-witness extension test is not a valid instrument

Date: 2026-09-05.  Code: `extend_probe.py`, `left_sweep.py`,
`sampler_validity.py` (this directory).  Nothing committed.

Status: **clean negative, with the control that establishes it.**  No theorem.
`Thm(2)` is not proved, not disproved, and not moved.  What is settled is a
*method* question: the task "extract a mode-(ii) `p = 2` ladder witness and
check whether it is a genuine Rule 30 configuration" cannot decide anything,
and the reason is measured rather than argued.

## 0. The assignment, and why its premise had to be repaired first

The assignment was to reconcile two verdicts: the R7 ladder says the `p = 2`
mode-(ii) language is NONEMPTY at every decided `(R, k, Q)`
(`RESULTS-ladder-rung0.md`, `RESULTS-ladder-rung1.md`), while the 2026-09-04
finite census says `|H_r(n)| = 0` exactly for `n = 1..16`
(`RESULTS-RW-TERMINAL-DEFECT-H-POPULATION.md`).  The assignment framed these as
in tension and asked which constraint the census enforces that the ladder drops.

**They are not in tension, and the framing should not be repeated.**  This is
the object-conflation trap of `RESULTS-FIB-ABSENT-M8-M9-M10.md` in a new
costume:

* `H_r(n)` fixes a finite source word `W in {1,2}^n` and asks whether the
  **unique deterministically forced** continuation
  `literal_extension(W, c, n+r+2)` passes a local hard-core + `12a`-terminal
  filter.  `PREREGISTRATION-RW-FORCED-TERMINAL-DEFECT.md` section 2 states the
  determinism explicitly: "there is no remaining existential over `Q`."  The
  census doc itself calls the condition "strictly weaker/necessary-only."
* The ladder decides emptiness of an omega-language over column pairs with the
  **transient existentially quantified and unbounded**.

`|H_r(n)| = 0` therefore does not say "no eventually-period-2 centre column
exists."  It says one particular sufficient route (RW) has no witness of its own
narrow shape at those `n`.  A NONEMPTY ladder and an empty `H_r` are compatible
statements about different sets, and no argument should be built on their
supposed conflict.

**The range in the assignment is also wrong, and it is worth stating separately
because the two errors compound.**  The brief said "zero period-2 candidates
through `n = 24`."  Three different objects with three different horizons were
collapsed into that one figure:

* Exhaustive `|H_r(n)| = 0`: stated as `n = 1..16` in
  `RESULTS-RW-TERMINAL-DEFECT-H-POPULATION.md`, and **since extended to
  `n = 1..24`** (both `c`, all three `r`) by the concurrently running
  `overnight_census.py`, whose logs report `H0=H1=H2=0` at every `n = 17..24`.
* Complete-SAT RW exclusion: a different object, standing at `n = 28`
  (`BACKLOG.md:216`, verified directly).
* The `gamma(n)` benchmark: a third object again, now at `n = 28` for `c = 2`.

A parallel investigation independently caught the same misquote.  None of
this changes section 0's argument, which is about *what kind of statement*
`|H_r(n)| = 0` is, not how far it reaches.

What survives of the assignment is the concrete part: extract real witnesses,
try to extend them to genuine lone-seed diagrams, and see what happens.  That
was run.  The answer is that the test is invalid, and the control proves it.

## 1. The probe, and why it is finite

A ladder witness is a lasso `prefix + cycle^omega` over the alphabet
`(col_{R-1}(t), col_R(t))`.  Two extension directions, both decidable on an
ultimately periodic word:

**Left.**  `col_{x-1}(t) = col_x(t+1) XOR (col_x(t) OR col_{x+1}(t))` is
deterministic, so leftward extension is forced.  The lone-seed wedge at depth
`j` — `col_{-j}(t) = 0` for `t < j`, `col_{-j}(j) = 1` — constrains only
`t <= j`, i.e. finitely many cells per depth, all present in a long enough
unrolling.  So "does this witness extend to left depth `D`" is a finite check.
The ladder imposes it only out to `x_min = -k`.

**Right.**  By `RESULTS-ladder-rung1.md` Lemma 1, `col_{R+1}` exists iff the pin
holds, and is then forced where `col_R(t) = 0` and **free** where
`col_R(t) = 1`.  This is obstruction F.

## 2. Probe soundness: the true lone-seed word survives

The left probe run on the TRUE lone-seed letter word, `R = 2`, both rules:

| rule | left depth reached | first failure |
|---|---:|---|
| 30 | 24 (probe limit) | none |
| 90 | 24 (probe limit) | none |

So the probe does not reject genuine diagrams, and it does so for Rule 30 and
Rule 90 alike.

**The right probe is broken and none of its numbers are reported here.**  It
completes the free cells by random choice, and on the true Rule 30 lone-seed
word — which extends rightward forever by construction — it reaches only
`x = R+1` before the pin fails at the next column.  It fails its own control.
The free space at each column is exponential and random completion does not
search it.  Recorded so a future reader does not read a right-side number out
of `extend_probe.py` and believe it.

## 3. Measured: sampled `p = 2` witnesses die at the first unmodelled column

`R = 2`, `w = 01`, `q = 1`, mode (ii), 48-60 accepting lassos sampled per `k` by
randomised walks in the accepting SCC, every one passing `ladder.verify_witness`.
Deepest left column satisfying the wedge:

| k | x_min | depth reached (histogram) | failure mode |
|---:|---:|---|---|
| 1 | -1 | 1 x48 | wedge |
| 2 | -2 | 2 x60 | wedge |
| 3 | -3 | 3 x47, 4 x13 | wedge |
| 4 | -4 | 4 x60 | wedge |
| 5 | -5 | 5 x29, 6 x22, 7 x9 | wedge |

Every sampled witness fails the light cone at or just past the ladder's own
`x_min`, always as `col_{-j}(t) = 1` where the lone seed requires `0`.  Taken
alone this reads as "the `p = 2` escape is an artifact of left truncation."

**It does not survive the control.**

## 4. The control that invalidates the test

The Rule 90 ladder at `w = 0` — its true eventually-zero centre column — is a
case where the answer is known: a genuine, fully realizable member of the
language exists, because the true Rule 90 lone-seed word is one.  Per
`RESULTS-ladder-rung1.md` Lemma 1', Rule 90's own extendability condition is
vacuous, so the control is the plain ladder and Rule 30's pin is never applied
to it (`PATH.md` row 55).

Confirmed directly, not assumed (`sampler_validity.py`, `T = 300`, subset
simulation over `ladder.successors` carrying each run's commit index, plus an
independent onset recomputation from the derived centre column):

| case | safety | earliest surviving commit | onset (direct) | true-word left depth |
|---|---|---:|---:|---:|
| rule 90, `w = 0` | pass | 2 | 1 | 24 |
| rule 30, `w = 01` | pass | 299 | 298 | 24 |

Rule 90's true word genuinely commits at onset 1 and is a real accepted witness.
Rule 30's "onset 298" on a 300-letter word is the trivial end-of-word artifact,
i.e. no onset — as it must be.

Now the gap.  Best left depth over 60 sampled lassos, against the true word's 24:

| k | rule 90 sampled best | rule 90 true word | rule 30 (`p=2`) sampled best |
|---:|---:|---:|---:|
| 1 | 5 | 24 | 1 |
| 2 | 5 | 24 | 2 |
| 3 | 6 | 24 | 4 |
| 4 | 6 | 24 | 4 |

**In the case where a genuine witness provably exists, is present in the
language, has onset 1, and extends to the probe limit, the sampler never finds
anything within a factor of four of it.**  The sampler returns spurious lassos
in the control exactly as it does for Rule 30.  Therefore "the sampled Rule 30
`p = 2` witnesses are spurious" carries no information about whether the Rule 30
`p = 2` escape is spurious.  Section 3 is a fact about the sampler.

Note the direction of the gap, since it is the opposite of what a "Rule 30's
witnesses are the spurious ones" reading would want: the Rule 90 samples reach
*deeper* than the Rule 30 samples at every `k` (5,5,6,6 against 1,2,4,4), and
exceed their own `x_min` by 4,3,3,2 where Rule 30's exceed it by 0,0,1,0.  The
sampler is doing *better* in the control — and still misses the genuine witness
by a factor of four.  So the shortfall is not a Rule 30 effect.

**Why it was doomed a priori,** visible once stated: a genuine Rule 30 `p = 2`
witness needs a transient longer than the 10^9-bit prize data check, whereas
the sampler's lassos have prefix length 5-11 by construction (randomised BFS
finds short paths).  The control shows the failure is not merely the Rule 30
transient — the sampler misses a genuine witness of onset 1.

## 5. The dropped constraint, named

With the premise repaired (section 0), the honest statement of what the ladder
drops relative to any finite-configuration census is not a bolt-on constraint:

> The ladder existentially quantifies over an infinite-dimensional family of
> boundary continuations in **both** directions; a finite census quantifies over
> nothing, because a finite seed determines its entire diagram.

Concretely, the ladder never imposes the lone-seed light cone
`col_x(t) = 0 for t < |x|` outside `[-k, R]`.  On the right this is
obstruction F, already recorded (`PATH.md` ~line 795), and the freedom is a
genuine choice at every `t` with `col_R(t) = 1` (rung 1 Lemma 1).  On the left
the extension is *deterministic*, so the freedom is not in a choice — it is that
the wedge beyond depth `k` is simply never checked.  Section 3 measures that the
unchecked constraint bites immediately, at the very first unmodelled column.

The two directions look like twins at this level of description.  **They are
not**, and section 6 measures and then proves the asymmetry.  The sentence "the
free boundary has a left-hand twin" was the working hypothesis when this section
was first written; it is wrong and is retained only so the correction is legible.

## 6. PROVED: the left depth `k` cannot affect the accepting tail at all

Rung 1 section 4 measures the accepting tail system's bisimulation-class count
against the RIGHT depth `R` and finds `~R^2.75`, growing.  Rung 0 section 3
sweeps the LEFT depth `k` but reports only raw product-state counts, which rung
0 itself says prove nothing (dominated by the `4^(R+k)` alphabet factor).  **The
`k`-comparable invariant had never been computed.**  Computed here at `R = 2`
with rung 1's own `tail_language`, which accepts arbitrary `Params`:

| k | rule 30 `p=2` plain | rule 30 `p=2` pin | rule 90 control |
|---:|---:|---:|---:|
| 1 | 15 | 20 | 32 |
| 2 | 15 | 20 | 32 |
| 3 | 15 | 20 | 32 |
| 4 | 15 | 20 | 32 |
| 5 | 15 | 20 | 32 |
| 6 | 15 | 20 | 32 |
| 7 | 15 | 20 | 32 |

Not "approximately flat" — **exactly constant**, in all three cases, while raw
states go 469 -> 1,439,333 (a 3,068x range) and tail nodes go 68 -> 3,060.
Compare rung 1's `R` sweep over the same invariant, which spans the same seven
depths: 10, 15, 34, 73, 140, 229, 349.

**Left and right depth are not symmetric.  Right depth creates genuinely new
tail behaviour; left depth creates none.**

This is not a coincidence and does not need a fit.  It follows by reading
`step_window` (`ladder.py:93-126`):

**Lemma (left depth is transient-only).**  `step_window` uses the derived
columns for exactly two purposes: (a) extracting `c_val = col_0` and
`m1_val = col_{-1}`, the only two values it returns; and (b) the wedge and edge
checks.  Purpose (b) is skipped entirely once `cnt >= saturate`.  Because
`diff_q` forces `x_min <= -1` (`Params.x_min`), every column the left depth adds
beyond `k = 1` lies below `-1` and therefore feeds **only** (b).  Hence at
`cnt >= saturate` the successor relation is independent of `k`. ∎

*Verified, not assumed:* every state of the accepting SCC carries
`cnt == saturate` exactly — rule 30 at `k = 2, 4, 6` gives `cnt` values
`{7}, {11}, {15}` against `saturate = 7, 11, 15`, and rule 90 the same.  So the
whole accepting tail sits in the region where no wedge check fires.

*Scope of the Lemma, stated so it is not over-read.*  At small `cnt` the deeper
columns are not merely unchecked, they are not computed at all: `derive` breaks
when `len(up) < 2` and `step_window` skips columns with empty `vals`.  That does
not weaken the Lemma, because `saturate = R + 2|x_min| + 1` grows with `k` and
the accepting SCC lives entirely at `cnt == saturate`, where the window is full.
It does mean the Lemma constrains only the tail, and leaves one escape hatch
open, named next.

**Corollary (why "add left depth" was never going to work).**  Increasing `k`
cannot produce an EMPTY verdict by destroying the accepting tail system, since
that system's behaviour does not depend on `k`.  The only remaining route to an
EMPTY is making the accepting tail *unreachable* from the initial state — and
that is a reachability question the Lemma says nothing about.  **It is settled
by measurement, not by the Lemma:** `empty: false` at every `k = 1..7`, with
`tail_nodes` growing 68 -> 3,060 while the class count held at 15.  So the
residual escape hatch is open in principle and closed in fact over the decided
range.

*State budget, and a warning.*  These sweeps run at `max_states = 3,000,000`
and the `k = 7` plain case already reached 1,439,333.  `k = 8` will very likely
cap.  **A cap hit returns `INCONCLUSIVE`, not EMPTY, and under the Corollary it
must not be read as "the tail became unreachable."**  Rung 0 section 6 already
had to warn once that an EMPTY can be an artifact (`N_base`); this is the same
hazard on the other side.

This upgrades rung 0 section 3's *measured* `k`-independence of the verdict to a
*structural* statement, the same upgrade rung 1 Corollary 2/3 performed for the
pin.  All three of R7's levers now have proofs rather than sweeps behind their
closure: depth-left (here), the pin (rung 1 Corollary 2/3), and `Q` (rung 0
section 6's `N_base` argument).

**What this does NOT say.**  The bisimulation quotient being constant does not
mean the *language* is constant in `k`; it is not.  Section 3 exhibits `k = 2`
witnesses that violate the `k = 3` wedge, so the language genuinely shrinks —
the shrinkage is entirely in reachability, i.e. in the prefix, never in the
tail.  Bisimulation classes are also a coarser invariant than the minimized
language (rung 1 section 4's own method note) and class count is not monotone
under language inclusion (rung 1 section 4, third consequence).  **No
inverse-limit conclusion is drawn: nothing here says a genuine word exists at
every left depth.**  The rule 90 control shows the same exact constancy, so this
is a property of the encoding and separates the two rules not at all.

Restoring what the strip truncation discards is therefore not a constraint to
bolt on in either direction.  On the right it is obstruction F; on the left the
ladder's own saturation rule makes the added constraint inert past the
transient.  The thing being discarded is that a lone-seed diagram has no free
parameters at all, and that is the problem, not a missing clause.

## 7. What is NOT claimed

* No `Thm(2)`.  No `Thm(p)` for any `p >= 2`.
* Not that the `p = 2` escape is an artifact.  Section 4 is precisely the
  statement that this evidence cannot decide that.
* Not that the escape is genuine.  Nothing here predicts anything about
  `gamma(n)`.
* Nothing about Wolfram's Problem 1.
* No claim that `|H_r(n)| = 0` and the ladder's NONEMPTY conflict; section 0
  says they do not.

## 8. Remaining open items and what not to retry

* **Do not re-run the per-witness extension test.**  Section 4 is its kill
  condition, fired.  A better sampler does not repair it: the object needed is a
  witness with an astronomically long transient, which no enumeration reaches.
* **Do not re-run the ladder at larger `R`, `k`, or `Q`** — closed by rung 0
  section 3, rung 0 section 6, and rung 1 Corollary 3 respectively.  Section 6
  gives the proof for the left-depth one.
* The right probe in `extend_probe.py` needs constraint propagation, not random
  completion, if anyone wants a right-side number.  It is not obviously worth
  building: by rung 1 Corollary 2/3 the right side is depth in disguise.
* The realizability gap of rung 1 section 6.3 is untouched and remains the whole
  remaining content of R7.

## Reproduction

```sh
cd experiments/rule30/r1-zero-set-attack
uv run python extend_probe.py --mode control -R 2 -D 24
uv run python left_sweep.py -R 2 --kmax 5 -n 60 -D 24
uv run python sampler_validity.py -R 2 --kmax 4 -n 60 -D 24 -T 300
```

Outputs: `left_sweep_R2.json`, `sampler_validity_R2.json`.

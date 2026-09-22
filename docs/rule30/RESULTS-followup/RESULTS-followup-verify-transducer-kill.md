# Verification: does the Grok screen-out correctly kill the T_w periodic-trace transducer proposal?

Date: 2026-08-30. Code:
`experiments/overnight-arms/roundtable_followup/verify_transducer_kill/verify_transducer.py`.
Nothing committed. Pure computation; no model calls used to reach the verdict
below.

## Verdict

**SCREEN-OUT CONCLUSION RIGHT BUT REASONING WRONG.**

The proposal (GPT-5.6 / DeepSeek `T_w` construction) does not work and
produces no contradiction with the two-interface structure. But Grok's stated
reason — "a finite-state claim is a bounded suffix, hence a fixed-depth
strip [subject to Corollary 2's sandwich `plain(R+1) ⊆ pin(R)`]" — is a
mis-citation. Lemma 1/Corollary 2 in `RESULTS-ladder-rung1.md` are proved for
a specific object (the existential ladder emptiness-language `plain(R)`,
which has a genuinely *free*, unconstrained outer boundary at column `R+1`)
that `T_w` is not an instance of. `T_w`, correctly formalized, has no free
boundary anywhere — every cell is uniquely forced once the seed row and the
hypothesised periodic drive are fixed — so the sandwich lemma's premises do
not hold for it. The real reason the proposal is inert: its own central,
unproved conjecture ("iterating `T_w` must eventually become periodic in the
spatial tail") is false, or at least strongly disconfirmed, for the one case
that actually matters (`p = 2`, alternating word), while it only holds in a
degenerate, uninteresting case (`p = 1`, constant word) that this repo's own
Lemma 4 already explains as a collapse artifact.

## 0. What "the proposal" actually specifies, and the ambiguity in it

The prose names two different operations and conflates them:　(i) "use
left-permutivity ... iteratively to reconstruct the entire left half-plane
from the right-half-plane history", and (ii) "define an exact p-step ray map
`T_w: rho_t -> rho_{t+p}`". These are not the same map. Two honest
formalizations were implemented and tested separately, because the text does
not pin down only one:

* **Reading B (driven-boundary forward CA).** Column 0 is *forced* to the
  hypothesised word, `a_t = w_{t mod p}`, taken as given (not derived).
  Columns `i >= 1` evolve by the ordinary forward rule using only `rho_t`
  restricted to `i-1, i, i+1`, all `>= 0`. No left-half-plane reconstruction
  is needed at all to advance the ray forward, because `a_{t+1}` is asserted
  directly by the periodicity hypothesis, not computed from `u_{t,-1}`.
  **Under the P1/P2 hypothesis that column 0 really is eventually periodic,
  this driven system is not fictional: it deterministically reproduces the
  entire true right half-plane**, since rule 30's forward rule restricted to
  `x >= 0` is a closed system once column 0's trajectory is fixed.
* **Reading C (literal leftward reconstruction).** Use
  `col_{x-1}(t) = col_x(t+1) XOR (col_x(t) OR col_{x+1}(t))` (this repo's own
  `reconstruct_left_column`, `experiments/rule30/inverse_trace_probe.py:135`)
  with `col_0` replaced by the hypothesised periodic word and `col_1` (and
  deeper) taken from the true right ray, cascading left column by column.

Both were implemented and run; results below.

## 1. MEASURED: `k(t)` (reading B) is bounded, not growing, across `t in [0,200]`

Method: build the driven trajectory `D_t` from the true lone-seed row 0 for
`p = 1, 2`; then, at each sampled `t0`, flip individual bits of `rho_{t0}`
one at a time and recompute `p` forward steps, recording the largest index
`j` whose flip still changes the target cell. This is a direct perturbation
measurement of dependency radius, not an argument from locality.

| t0 | reach, p=1 (target i=8) | reach, p=2 (target i=8) |
|---:|---:|---:|
| 0 | 9 | 10 |
| 5 | 9 | 10 |
| 10 | 9 | 8 |
| 20 | 9 | 8 |
| 40 | 9 | 8 |
| 80 | 9 | 8 |
| 120 | 9 | 8 |
| 160 | 9 | 6 |
| 200 | 9 | 8 |

The reach sits at `i_target + O(p)` and **does not grow with `t`** across a
200-fold range. This is exactly what is expected once `T_w` (reading B) is
recognized as a bona fide radius-1 sliding-block code with a driven boundary
(Curtis–Hedlund–Lyndon): each output cell depends on a window of fixed width
around it in the input row, period. **So `T_w`'s own claim to be finite-state
is empirically confirmed for this formalization, not self-contradictory.**
This closes one branch of the task's step 2: `k(t)` is bounded, so the
question moves to whether the sandwich lemma actually governs a
bounded-window object of this kind (section 3) and whether the forced
periodicity conjecture holds (section 4).

Reading C gives a different, complementary measurement: reconstructing
`col_{-m}` for depth `m = 1..15` consumes exactly `m` additional future time
samples of the true right ray's column-1 series (linear, one-for-one, no
surprise growth) — confirming the standard "one future centre value is
consumed per level" identity already recorded in this repo
(`RESULTS-ladder-rung1.md` section 0.5) rather than anything new.

## 2. Is `col_0` pinned directly, making the "transducer" claim partly vacuous?

Yes, and this matters. Under reading B, `a_{t+1} = w_{(t+1) \bmod p}` is
supplied directly by the hypothesis at every step; it is never *derived* from
`rho_t` via the inverse recurrence at all. So `k(t)` for the `i = 0` output
is trivially `0` (confirmed: perturbing any `j >= 1` in `rho_t` never changed
the `i = 0` output in testing). The interesting, non-vacuous content of "does
`T_w` need a growing window" only shows up for `i >= 1`, which is what
section 1's `i_target = 8` measurement targets.

## 3. PROVED (by inspection of the actual lemma statement): Corollary 2 does not formally apply to `T_w`

`RESULTS-ladder-rung1.md` Lemma 1 and Corollary 2 are stated for `plain(R)`
and `pin(R)`, **languages of finite letter-words projected onto columns
`[x_min, R]`**, where nonemptiness means "some infinite extension beyond
column `R` exists satisfying the forward rule." The free boundary that
Corollary 2's sandwich is about is precisely this *existential slack at
column `R+1`* — the word is only required to be *extendable*, and Corollary
3 states the consequence for that existential structure: `pin(R) = ∅` forces
`plain(R+1) = ∅`.

`T_w` (reading B) has no such existential slack anywhere. Given the seed row
and the hypothesised periodic word, **every cell of every `rho_t` is uniquely
determined** — there is no column at which an unconstrained choice remains to
be quantified over. "Finite window per output cell" (a locality property of
a sliding-block code) and "free outer boundary of a truncated existential
language" (what Lemma 1/Corollary 2 are about) are different properties of
different objects, and the proof of Corollary 2 (which explicitly uses the
"a word in `plain(R+1)` carries an actual `col_{R+1}`..." existential
argument) does not go through for a single deterministic trajectory. Grok's
"a finite-state claim is a bounded suffix, hence a fixed-depth strip" is a
verbal analogy between two structurally different kinds of boundedness, not
an application of the proved lemma. **This part of the screen-out's stated
reasoning does not hold up.**

## 4. MEASURED: the proposal's own central conjecture is false in the case that matters

The whole argument depends on an unproved claim never justified in the
proposal text: that iterating `T_w` "must eventually become periodic in the
spatial tail." This was tested directly by running the driven system
(reading B) for `T = 1400` steps from the true lone-seed row, `width = 1600`,
and checking the resulting row's tail (final ~117 cells, inside the true
light cone) for periodicity up to period 40.

| case | eventually periodic (period ≤ 40, tail ≈117 cells)? | period found |
|---|---|---|
| rule 30, `w = 0` (p=1, constant) | **yes** | 2 |
| rule 30, `w = 01` (p=2, alternating) | **no** | — |
| rule 90 control, `w = 0` | yes | 1 |
| rule 90 control, `w = 01` | **yes** | 6 |

Two findings:

1. **For the nonconstant case that the original proposal actually works with
   (`p = 2`, the "01" word used as the canonical worked example), the
   driven-boundary spatial tail is not periodic** to the depth tested. Since
   reading B's driven trajectory equals the true right half-plane exactly
   *if* the P1/P2 periodicity hypothesis holds, this is a direct
   disconfirmation of the proposal's load-bearing conjecture for the
   nontrivial case: no forced periodicity, hence no contradiction with the
   two-interface structure ever materializes, hence the route produces
   nothing regardless of whether `T_w` is finite-state.
2. **The constant `p = 1` case is periodic for both rule 30 and rule 90.**
   This is not evidence for the proposal; it is a known collapse artifact.
   `RESULTS-ladder-rung1.md` Lemma 4 already proves (exhaustively, for a
   related but different periodic-tail construction) that restricting to
   time-periodic tails collapses onto trivial constant/short-cycle states.
   A constant `col_0` boundary is exactly the kind of degenerate drive that
   produces this collapse; it says nothing about the aperiodic case P1/P2
   actually needs to rule out.
3. **The rule 90 control also goes periodic for `p = 2`.** This is expected
   from linearity (a periodically-driven linear/additive CA has an
   eventually periodic response by superposition), and it is a useful
   negative control: it shows the *linear* rule's driven system does what a
   naive "finite state implies periodic" intuition would predict, while
   *rule 30's* driven system, run under the identical setup, does not. That
   is itself informative: whatever intuition motivated "a finite-state map
   must go periodic" is really an intuition about **linear** systems, and it
   fails for Rule 30's nonlinear OR-latch precisely where the section-0 Rule
   90 filter would want it to fail (an argument that works for Rule 90 too
   proves nothing about P1; here the argument doesn't even work for Rule 30,
   so it fails a stronger test than the filter demands).

**Honest scope of this measurement** (obstruction H applies): this is a
finite check to `t = 1400` over a tail window of ~117 cells and periods up to
40. It is evidence the conjecture is false or at least not the easy win the
proposal assumed; it is not a proof of non-periodicity for all `t`, and
cannot be — no finite computation could ever establish that.

## 5. Resolving the three-way question

* **Is `k(t)` bounded or unbounded?** Bounded (section 1), for the only
  formalization (reading B) that makes `T_w` a genuine, exact map from
  `rho_t` alone. The proposal's "finite-state" self-description holds up
  under direct perturbation testing.
* **Does Lemma 1/Corollary 2 formally apply to `T_w`?** No (section 3).
  Boundedness of a sliding-block code and the existential free-boundary
  structure the sandwich lemma is proved about are different properties;
  Grok cites the lemma by analogy, not by satisfying its hypotheses.
* **Does the proposal's own conjecture (forced spatial-tail periodicity)
  hold?** No, empirically, for the nonconstant case that matters (section 4).
  This is the actual reason the route is dead: it never produces the
  contradiction it promises, independent of whether `T_w` is finite-state.

So the screen-out's bottom line — this direction does not work — stands, but
"because it's a bounded suffix, hence a fixed-depth strip subject to the
sandwich lemma" is not the reason. The proposal is not killed by an analogy
to the proved ladder obstruction; it is killed because its own central claim
about forced periodicity is unsupported and measurably false in the relevant
case.

## 6. What this does and does not settle

Nothing here bears on Wolfram's Problem 1 directly. This file settles only
the narrower methodological question the task asked: whether the screen-out
of the `T_w` proposal was reasoned correctly. It was not, even though its
conclusion holds. Any future proposal along these lines should not lean on
"finite-state ⟹ subject to Corollary 2" without checking whether the
construction actually has a Corollary-2-style existential free boundary (it
usually will not, for a deterministic driven-CA construction); it should
instead be checked, as here, by directly testing whatever forced-periodicity
or forced-structure claim is doing the actual work.

## Reproduction

```sh
cd experiments/overnight-arms/roundtable_followup/verify_transducer_kill
uv run python verify_transducer.py
```

Outputs `results.json` in the same directory with the full numeric detail
behind every table above.

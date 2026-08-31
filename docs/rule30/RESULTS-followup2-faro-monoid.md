# Followup2 "faro monoid" spark: verified, and it is the pin identity in new vocabulary

Status: **DUPLICATE-OF-LADDER-AUTOMATON.**  The screen-out panelist's suspicion
is correct.  Nothing here bears on Wolfram's Problem 1 that
`RESULTS-ladder-rung1.md` does not already establish, and one piece of it
(Lemma 4's exhaustive automaton) directly and pre-emptively answers the
spark's central question ("is `s` absorbing") for the case where it is
checkable at all.

Date: 2026-08-30.  Code:
`experiments/overnight-arms/roundtable_followup2/faro_monoid/faro_monoid.py`.
Nothing committed.  Reused without modification:
`experiments/rule30/inverse_trace_probe.py` (`reconstruct_left_column`),
`experiments/rule30/periodicity_bridge_probe.py` (`evolve_rows`, `cell`,
`center_trace`), `experiments/rule30/ladder/rung1.py` (`tail_language`).

## 0. The spark, and where it lands

> "Rule 30 is a faro that sticks: whenever two face-up cards meet, they
> adhere and the move drops out of the symmetric group into a monoid ...
> Centre periodicity is the claim that this one tracked card has a cyclic
> itinerary under words in `{f,s}`. The analogy bites if `s` is absorbing on
> the singleton conjugacy class."

Formalized literally (section 1) this reduces, term for term, to objects
this repo already has names for:

| spark vocabulary | this repo's vocabulary |
|---|---|
| `f` (linear, invertible, XOR-only move) | the `g(b,0) = g(b,1)` **false** case: no pin, `PATH.md` section 1 |
| `s` (OR-saturating, information-losing "stick") | the `g(b,0) = g(b,1)` **true** case: the pin, `PATH.md` section 1, `RESULTS-ladder-rung1.md` Lemma 1 |
| "tracked card's itinerary under words in `{f,s}`" | the per-cell classification of `PATH.md`'s OR-latch identity, applied along a column |
| "is `s` absorbing on the singleton conjugacy class" | Lemma 4's exhaustive 16-state automaton (period-2 restriction) and the general-`R` bisimulation-class count (`RESULTS-ladder-rung1.md` section 4) |

This is not an analogy that happens to resemble the ladder; the defining
identity is the same equation.  Section 1 below derives `{f,s}` from the
general left-permutive-rule pin condition already stated in `PATH.md`
section 1, and it comes out **syntactically identical** to Lemma 1 of
`RESULTS-ladder-rung1.md`, substituting `x=0` for `x=R`.

## 1. Formalization, and where it deviates from a fully literal reading

Literal reading required one choice.  The spark says "the sequence of local
update types applied along the backward-in-time trajectory that the
left-permutive inverse would trace."  The repo's leftward inverse
(`inverse_trace_probe.reconstruct_left_column`) computes column `x-1` from
column `x` (center) and column `x+1` (right):

```text
s(t,x-1) = s(t+1,x) XOR (s(t,x) OR s(t,x+1))
```

For a general left-permutive rule `f(a,b,c) = a XOR g(b,c)` this generalizes
to `s(t,x-1) = s(t+1,x) XOR g(s(t,x), s(t,x+1))`.  Classify each
space-time site `(t,x)` by whether `g` saturates at the observed center
value `b = s(t,x)`:

```text
f-type  at (t,x)  iff  g(b,0) != g(b,1)   (right neighbour still matters)
s-type  at (t,x)  iff  g(b,0) == g(b,1)   (right neighbour is irrelevant: the pin)
```

**Deviation from a fully literal reading, stated explicitly.**  The
classification at `(t,x)` depends only on the single bit `s(t,x)`, not on
any accumulated "state" of a tracked card.  So the naive reading -- a card
carries a monoid element that composes as it moves -- does not produce a
nontrivial state machine by itself: the label at each site is a pure
function of one bit, with no memory.  To get a monoid with an actual
transition structure (states that can be "absorbing" or not), the tracked
object's *state* must be upgraded to something that determines admissible
*future* continuations, not just the current label.  That upgrade is not
optional embroidery on the spark -- it is required to make "absorbing" a
question with any content -- and once made, the natural minimal state is
exactly a bounded window of recent columns, which is exactly what
`RESULTS-ladder-rung1.md`'s ladder automaton already tracks (`pin(R)` /
`plain(R)`, states = admissible local windows at depth `R`). This is stated
up front so the later "duplicate" verdict is not a rhetorical sleight: the
literal per-bit reading is memoryless and trivial; the only way to make it
nontrivial is to reconstruct the ladder's state space.

`g_of` / `pins_at` in `faro_monoid.py` implement this generally and
reproduce `PATH.md` section 1's pin table fresh, from the rule's truth
table alone (not by copying the table), including rule 60 as a two-sided
control (`PATH.md` says it pins at both center values, `g(b,c)=b`):

```json
"pin_table_reproduced": {
  "30": [1], "45": [1], "75": [0], "60": [0, 1], "90": [], "150": [], "105": []
}
```

This matches `PATH.md` lines 112-120 exactly (rule 30 pins at center=1,
rule 60 pins at both, rule 90 pins nowhere), independently re-derived from
the truth table rather than trusted, and now checked on a one-sided and a
two-sided case, not just one-sided.

**A direction correction, worth stating precisely.**  The map this document
traces (`reconstruct_left_column`, `col_x, col_{x+1} -> col_{x-1}`) is
**total and deterministic for every center value** -- it never sticks, for
any rule of this form.  The nonlinearity's actual failure mode -- the thing
that is genuinely non-invertible -- lives in the *opposite* map,
`(col_{x-1}, col_x) -> col_{x+1}`: Lemma 1 of `RESULTS-ladder-rung1.md`
shows a solution exists iff the pin holds, and when it does
(`col_x(t)=1`) it is **non-unique**, not merely well-defined.  So the
spark's "sticking" is a failure of injectivity in the rightward
*extension* direction, not information loss along the backward-in-time
trajectory this section formalizes.  The backward trajectory is always
well-defined; what fails to be recoverable is the *forward* continuation
one column further out.  This does not change the verdict (section 5)
because the ladder's `pin(R)`/`plain(R)` automaton is built on exactly that
rightward-extension direction already -- it is the more precise reading,
not a different one.

## 2. MEASURED: the true lone-seed orbit, and the information-loss claim

`measure_true_orbit(T=2000)`, exact lone-seed Rule 30, `T=2000`:

* word length 2001, **978 s-type, 1023 f-type** sites (`s`-density
  0.4888 over this window; consistent with the known near-1/2 center density,
  not a new measurement of that quantity).
* **Perturbation test** (the literal check of "OR saturation discards
  information about the right neighbour"): flip `right_column[t]` by one bit
  and re-run `reconstruct_left_column` unchanged.
  * At **all 1023 f-type sites**, the reconstructed left cell changed
    (100%).
  * At **all 977 tested s-type sites**, the reconstructed left cell did
    **not** change (0%).

**This is an algebraic identity of the closed form, not new orbit-dependent
evidence, and should be read that way.**  Since
`left[t] = col0[t+1] XOR (col0[t] OR right[t])`, whether flipping `right[t]`
changes `left[t]` depends only on `col0[t]` -- it is `0` exactly when
`col0[t]=1` and `1` exactly when `col0[t]=0`, for *any* bit sequence, on any
rule of this form. Running it on the true Rule 30 orbit rather than on a
random sequence confirms the formula is applied correctly to this document's
own data (a sanity check, per `PATH.md` section 0.5's warning against
presenting a re-measurement as new content), but the 1023/1023 vs 0/977
split itself is the pin identity restated, not an independent discovery.
`s_count` (978) and the count of s-type sites whose reconstruction step
exists (977, one less because `reconstruct_left_column` consumes one future
sample) differ by exactly one, as expected.

## 3. MEASURED: Rule 90 has no `s` move, by construction and on the orbit

`pins_at(90) == []`: Rule 90's local rule `a XOR c` (no `b` dependence at
all) makes `g(b,0) == g(b,1)` false for both `b` values, so no OR-saturating
step is even expressible -- a truth-table fact, established before any
orbit is touched, and it is the whole content of the claim.  Running it on
the actual lone-seed Rule 90 orbit to `T=2000` gives **0 s-type sites, 2001
f-type sites**, but this is the truth-table fact printed 2001 times, not
2001 independent confirmations: the label at every site is `pins_at(90)`
evaluated once, so the orbit run adds nothing beyond showing the labelling
code executes on real data. This matches the spark's own "Rule 90 gut
check" and `PATH.md`'s pin table, and closes item 4 of the assignment: Rule
90's backward reconstruction never requires an information-losing step,
because its local rule contains no OR term for one to saturate.

## 4. The key test: is "`s` absorbing" a bounded/local claim or a global one?

### 4.1 The one case where it is checkable: Lemma 4's period-2 restriction

`RESULTS-ladder-rung1.md` Lemma 4 already builds exactly this automaton for
the period-2-in-time restriction, and independent reproduction here
(`lemma4_two_periodic_automaton`, exhaustive over all 16 states) confirms it
with one clarification.

State `(U,V) = (col_x, col_{x+1})`, `U=(u0,u1)`, transition
`(U,V) -> (W,U)`, `W = (u1 XOR (u0 OR v0), u0 XOR (u1 OR v1))` -- each
coordinate of `W` is exactly one `{f,s}` step (`s`-type iff `u0=1` resp.
`u1=1`).  Reproduced result:

```text
n_states = 16, max_transient = 3
15 of 16 states -> the 2-cycle ((0,0),(1,1)) <-> ((1,1),(0,0))   [Lemma 4's cycle]
1 state (the all-zero state ((0,0),(0,0))) is its own isolated fixed point
```

**Correction to `RESULTS-ladder-rung1.md`, precisely stated.**  Lemma 4
says "all 16 states reach ... the single 2-cycle."  There are in fact **two**
terminal cycles, not one: the stated 2-cycle, and the isolated fixed point
`((0,0),(0,0))`, which is reached from no state other than itself (confirmed
by exhaustive enumeration over all 16 starting states, above). The count in
the lemma's statement is off by one degenerate state. **The lemma's
conclusion is unaffected and holds for all 16 states unconditionally**: both
terminal cycles have columns constant in time (the fixed point is doubly
constant -- both columns identically zero -- and the 2-cycle is the
stated alternating-in-space, constant-in-time pair), so no state, including
the one the lemma's phrasing missed, ever produces the alternating-in-time
behaviour the tail word `01` would need.  So: **in this restricted setting,
`s` genuinely is absorbing** -- exhaustively proved here, not measured --
into one of two "wrong" terminal behaviours, never the one that would
witness a short-period escape.  This is exactly `RESULTS-ladder-rung1.md`'s
own reading of Lemma 4: it rules out short-period escapes, it does not
produce one; the off-by-one state count does not change that reading and
should be corrected in that document the next time it is touched.

### 4.2 The general case: it reduces to the ladder's automaton, not a new one

Outside the period-2 restriction, "does the tracked object ever return to a
distinguished state" requires knowing, from a bounded window of recent
columns, what future extensions remain consistent -- there is no way to
check it without that state, and that state is not a new construction: it
*is* `pin(R)` / `plain(R)`'s residual-language automaton, letter for letter.
Spot-check re-run here, from `rung1.py` directly (not re-typed from the
markdown table), `w=01, k=2, q=1`:

| R | plain bisim classes (reproduced) | pin bisim classes (reproduced) | published (`RESULTS-ladder-rung1.md`) |
|---:|---:|---:|---|
| 1 | 10 | 9 | 10 / 9 |
| 2 | 15 | 20 | 15 / 20 |
| 3 | 34 | 44 | 34 / 44 |

Exact match at all three spot-checked depths.  `RESULTS-ladder-rung1.md`
already carries this out to `R=7` and fits `~R^2.761` (plain) /
`~R^2.741` (pin), against `4^R` raw states -- i.e., **not absorbing**:
the class count is unbounded and keeps growing at general depth, only
polynomially slower than the raw encoding.  So the answer to "is `s`
absorbing" bifurcates exactly along the line the screen-out panelist
guessed:

* **Bounded/local instance (period-2 tail):** yes, absorbing, and it is
  exactly Lemma 4, already in this repo, already interpreted as a
  negative result (wrong cycle).
* **General instance (arbitrary period, arbitrary depth):** the only
  computationally checkable form of the question is a bounded local
  computation, and that computation is not merely analogous to but is
  *literally* `RESULTS-ladder-rung1.md`'s tail-language automaton; there it
  is answered NONEMPTY at every depth checked, escape growing polynomially,
  never stabilizing. Not absorbing in that regime, and this is already
  fully accounted for in section 4/6 of `RESULTS-ladder-rung1.md`.

There is no third, "genuinely global," sense of "absorbing" on offer here:
nothing in the spark specifies a state space in which absorption could be
checked except by exactly this bounded-window construction, and the
document's own author (via the panel's screen-out) already anticipated that.

## 5. Verdict

**DUPLICATE-OF-LADDER-AUTOMATON.**

* `{f,s}` = the pin / no-pin split, syntactically identical to `PATH.md`
  section 1 and `RESULTS-ladder-rung1.md` Lemma 1 (`x=0` substituted for
  `x=R`); reproduced independently here, not merely asserted.
* The information-loss content of `s` is confirmed by direct perturbation
  on the true orbit (section 2): exact, not asserted.
* Rule 90's "only `f`" claim is confirmed both structurally (no OR term
  exists in its rule at all) and on its actual orbit (section 3): 0/2001.
* The one place "is `s` absorbing" is literally checkable (the period-2
  restriction) is Lemma 4, already in this repo, already proved exhaustively,
  and already read correctly there as a negative result (absorbs to the
  wrong, constant-in-time cycle).
* The general-depth version of the same question is not a new automaton;
  independent re-run of `rung1.py` reproduces its published bisimulation
  class counts exactly at `R=1,2,3`, and the published `R=1..7` table shows
  unbounded polynomial (`~R^2.75`) growth against `4^R`, i.e. not absorbing,
  and this was already the finding of `RESULTS-ladder-rung1.md` sections 4
  and 6.

No new route survives.  The spark is the pin identity, restated with a
faro-shuffle metaphor; its one nontrivial sub-claim ("s is absorbing") is
either already proved (period-2 case, Lemma 4) or already measured and
found false at the strength that matters (general case, the `R^2.75`
growth). Nothing here should be read as evidence toward or against P1 beyond
what `RESULTS-ladder-rung1.md` already states.

**Problem 3.**  The prompt notes the spark also touches P3.  It does not
survive contact with it either: the monoid framing supplies a per-cell label
and a word, but no composition law that would let a word of length `n` be
combined or shortcut to evaluate `col_0(t)` faster than iterating `t` steps
-- it names a classification, not an algorithm, so it dies on obstruction D
(`PATH.md` section 7.3, the missing composition law) exactly as the other
P3 attempts in that register did.  Read instead as a complexity measure of a
single fixed orbit, it also dies on obstruction G (measures of a function of
*variable* inputs applied to one fixed point).  This is not developed
further here; one sentence closes the loop the assignment opened.

## Reproduction

```sh
cd experiments/overnight-arms/roundtable_followup2/faro_monoid
uv run python faro_monoid.py
```

No tests added; the script is a verification report, not new production
code, and its two nontrivial numeric claims (the rung1 spot check, the
Lemma 4 automaton) are cross-checked in-line against `rung1.py`'s live
output and against exhaustive enumeration respectively.

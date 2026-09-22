# Direction 8 follow-up: the left-permutive skew-product cocycle

Status: **KILLED-BY-REGRESSION.**  The natural completion of the fragment is
not a new construction; it is `RESULTS-ladder-rung1.md` Lemma 1 / Lemma 1'
(the boundary-pin extendability condition) restated with "base = centre
column, fibre = column 1" naming, plus `PATH.md` obstruction F (free boundary
of a fixed-depth strip) as the reason it never closes at any finite fibre
size, and obstruction A (`O(log t)` wall) as the reason the fibre cannot be
made to close by throwing more compute at it (rung 0/1 already ran that
experiment, up to `R = 7`, `p <= 8`, and it does not close). No new theorem,
no new open question. Code:
`experiments/overnight-arms/roundtable_followup/skew_product_cocycle/skew_probe.py`.
Modal: $0.

## What was given, verbatim, and what was invented

**Given (the fragment, cut off mid-sentence):**

> Direction 8 (proposal). Left-permutive skew-product cocycle over the centre
> column (P1 and a P2 reduction). Left-permutivity: `u_{t,-1} = a_{t+1} XOR
> (a_t OR u_{t,1})`. View `(a_t)_{t>=0}` as a base sequence and `r_t := u_{t,1}`
> as a fibre. This defines a skew product `Phi_a : {0,1} -> ...` [cut off]

That one relation, `u_{t,-1} = a_{t+1} XOR (a_t OR u_{t,1})`, is not new to
this document or to this repo: it is `PATH.md` section 0.5 / section 1's OR
latch pin and `reconstruct_left_column` in
`experiments/rule30/inverse_trace_probe.py:135-160`, applied at `x=0`. It
reconstructs the LEFT neighbour of the centre from the centre's own future
value and the RIGHT neighbour. The fragment names this relation and then
proposes to use `r_t = u_{t,1}` — the right neighbour appearing in it — as a
"fibre" and to define a map `Phi_a` evolving it forward. Nothing beyond that
one sentence was given. Everything below — what `Phi_a` actually is, whether
it is well defined on a finite fibre, what it would buy, and the Rule 90
comparison — was constructed here, not given.

## 1. The natural completion, worked out

Rule 30's local rule at site 1 is `s(t+1,1) = s(t,0) XOR (s(t,1) OR s(t,2))`,
i.e., in the fragment's notation,

```text
r_{t+1} = a_t XOR (r_t OR u_{t,2})
```

This is **exactly** `RESULTS-ladder-rung1.md` Lemma 1's identity
`col_R(t+1) = col_{R-1}(t) XOR (col_R(t) OR col_{R+1}(t))` at `R = 1`, with
`col_0 = a`, `col_1 = r`, `col_2 = u_{t,2}`. So the question the fragment
poses — "is `r_t` an autonomous fibre?" — is Lemma 1's extendability question,
already answered in this repo before this document existed:

* If `r_t = 0` (`col_R(t) = 0`), the OR does not saturate and `u_{t,2}` is
  **forced**: `u_{t,2} = r_{t+1} XOR a_t`. But this determines `u_{t,2}` from
  `r_{t+1}`, which is the value being computed — it is a *consistency*
  condition useful for backward/ladder search, not a forward evaluation rule.
* If `r_t = 1`, the OR saturates and `u_{t,2}` is **completely free**: `r_{t+1}
  = a_t XOR 1 = NOT a_t` regardless of `u_{t,2}`.

So `r_{t+1}` is in fact computable from `(a_t, r_t)` alone whenever `r_t = 1`
(it's `NOT a_t`), but whenever `r_t = 0`, `r_{t+1} = a_t XOR u_{t,2}` needs the
new bit `u_{t,2}`, which the base sequence `(a_t)` and `r_t` do not determine.
**Confirmed by exhaustive collision search on the true lone-seed orbit**
(`skew_probe.py`, `T = 200,000`): the 4-entry table `Phi(a_t, r_t) -> r_{t+1}`
has 49,797 collisions out of 199,999 transitions — the same `(a_t, r_t)` pair
is followed by both `0` and `1` on the real orbit, so **no function `Phi_a :
{0,1} -> {0,1}` of the form the fragment names exists, full stop, not even
approximately.** The scalar reading of the fragment is falsified in the first
200,000 steps of the one orbit the problem is about.

**Enlarging the fibre cascades and does not terminate.** Fix it by folding
`u_{t,2}` into the fibre: state `(r_t, u_{t,2})`. Advancing `u_{t,2}` one step
needs the local rule at site 2, `s(t+1,2) = s(t,1) XOR (s(t,2) OR s(t,3))`,
which introduces `u_{t,3}`. By induction this is Lemma 1 at every `R`: holding
a size-`R` fibre `(u_{t,1},...,u_{t,R})` lets you advance it to a size-`(R-1)`
fibre `(u_{t+1,1},...,u_{t+1,R-1})` for free, but recovering the lost `R`-th
component always needs one new bit, `u_{t,R+1}`, from outside the fibre. That
new bit is forced only on the fraction of steps where `u_{t,R} = 0` and free
otherwise. There is no `R` at which this stops needing new information: a
finite fibre is not closed under the forward map for any `R`. Enlarging the
fibre to the entire right half-line reproduces the full 2D space-time diagram,
which is not a reduction of anything — it's the definition of the CA.  This
**is** obstruction F, `PATH.md` 7.3: "any fixed-depth strip leaves its
outermost column unconstrained, and the phase slip ... relocates there."

**The finite-fibre truncation is not a new object either.** Truncating the
fibre at depth `R` and asking which infinite words are consistent with (a)
Rule 30, (b) a periodic base word `a`, and (c) the extendability condition at
the outer edge is precisely `pin(R)` from `RESULTS-ladder-rung1.md` section 3
— the same ladder, run in the opposite (rightward, forward-time) direction
from the leftward reconstruction the ladder actually uses, but built from the
identical Lemma 1. That construction has already been run to `R = 7` and
periods `p <= 8`: NONEMPTY at every decided cell, no `Thm(p)` for any `p >=
2`, accepting-tail bisimulation classes growing as `R^2.75` against a `4^R`
raw encoding (`RESULTS-ladder-rung1.md` section 4), i.e. `O(log t)`-wall
behaviour restated in state-count form (obstruction A). There is no reason to
expect the forward-direction fibre construction to behave differently, and no
budget was spent re-running it: rung 0/1 already measured that adding depth
or adding exactly this kind of boundary pin buys polynomially little and never
closes (`RESULTS-ladder-rung1.md` Corollary 2/3).

## 2. What proving something about it would buy — and why that's moot

The fragment tags this "P1 and a P2 reduction." Taking that seriously:

* **For P1** (nonperiodicity): a `Thm(p)`-shaped result — no admissible
  fibre-consistent word gives an eventually `p`-periodic centre column — is
  exactly what rung 0/1 already attempted from the other direction and did
  not obtain for any `p >= 2`. The skew-product framing does not add a new
  attack surface; it is the same finite-window emptiness question the ladder
  already asks, now motivated by "fibre dynamics" language instead of
  "boundary depth" language. It inherits rung 0/1's result unchanged: NONEMPTY
  at every `R <= 7`, `p <= 8`, both with and without the boundary pin.
* **For P2** (density 1/2): "unique ergodicity of the fibre dynamics
  conditional on the base" is not a meaningful question here because the
  fibre dynamics, per section 1, is not even a well-defined dynamical system
  at any finite fibre size — there is no stationary object to be uniquely
  ergodic. Retreating to "the infinite fibre" collapses this to the
  already-open R8 target (unique ergodicity of the vertical orbit closure of
  the full 2D diagram, `RESULTS-orbit-closure-diagnostic.md`), which is a
  restatement, not a reduction: the fragment would have to show the *fibre*
  is a strictly smaller/easier object than the whole right half-plane to buy
  anything on P2, and section 1 shows it provably isn't — it's exactly as big.

So even under the most charitable finite-fibre reading, "proving something
about `Phi_a`" would either (a) reproduce a result rung 0/1 already tried and
did not get, or (b) turn out to be exactly the whole-diagram orbit-closure
question R8 already asks, with no reduction in difficulty. Neither is new
leverage.

## 3. Rule 90 screen

Rule 90's relation at site 1: `s(t+1,1) = s(t,0) XOR s(t,2)`, i.e. `r_{t+1} =
a_t XOR u_{t,2}`, matching Lemma 1' (`RESULTS-ladder-rung1.md`
`col_R(t+1) = col_{R-1}(t) XOR col_{R+1}(t)`, always solvable):

```text
u_{t,2} = r_{t+1} XOR a_t     -- always, no case split, no saturation ever
```

The construction genuinely is trivial for Rule 90: given the full time series
of columns 0 and 1, every column to the right (and the left, by the same
identity run backward) is fixed by a closed-form XOR of the two, all the way
out — this is the standard exact solvability of additive CAs mod 2
(Martin-Odlyzko-Wolfram), not a new observation. So the construction *does*
correctly separate Rule 30 (nonlinear, OR saturates conditionally, fibre never
closes) from Rule 90 (linear, fibre closes in one line, unconditionally) —
this is a real pass of the section-0 filter, in the sense that an argument
built the same way genuinely fails to trivialize Rule 30.

But this is not new information either: it **is** Lemma 1 vs. Lemma 1' from
`RESULTS-ladder-rung1.md`, which already isolates the OR-nonlinearity as
exactly the thing that makes the pin nonvacuous for Rule 30 and vacuous for
Rule 90 (`PATH.md` section 1 makes the identical point about the pin
mechanism generally: "the pin is nonvacuous for rule 30 precisely because of
the OR nonlinearity, and vacuous for the additive rule"). Passing the Rule 90
filter here means passing a filter this repo already built and already used
to kill the closely related rung-1 pin-as-independent-axis hope (Corollary 3).
It confirms the completion is *faithful to the fragment's spirit* (it does
discriminate the rules) without giving it anything the ladder didn't already
have.

**A second, sharper Rule 90 check, run rather than argued.** Even though the
Rule 90 fibre is exactly solvable in closed form, that says nothing about
whether the *centre column* `(a_t)` carries useful information about it as a
"base sequence." Measured on the true Rule 90 lone-seed orbit,
`T = 200,000`: `a_t = 1` only at `t = 0` (the known eventually-zero centre
column), so every bounded window of `(a_t)` history collapses to at most 2
distinct values (`(a_0..)=1,0,0,...` vs. all-zero) for any window length
`k = 1..20`, and `r_t` (`= s(t,1)`) still shows genuine collisions against
that collapsed history at every `k` tested (13-14 residual collisions at `k =
20`, after an initial burst of ~200,000 at `k=1`). **A base sequence that is
eventually constant carries no information about its own fibre, exactly and
measurably, for the one rule where the fibre is provably solvable in closed
form.** This is obstruction C (single-column blindness) appearing inside the
fragment's own construction: driving a fibre off an eventually-constant base
cannot see the fibre's structure regardless of how simple that fibre's true
dynamics is.

## 4. Computational check on the true lone-seed orbit

`skew_probe.py`, `T = 200,000`, both rules. Full log reproduced by rerunning;
key numbers:

* **Identity sanity check** (Lemma 1 / 1' applied to the extracted columns):
  0 violations out of 199,999 transitions, both rules. This validates the
  bit-parallel column extraction; it is a regression check, not a finding.
* **Scalar map `Phi(a_t,r_t) -> r_{t+1}`:** fails immediately for both rules.
  Rule 30: 49,797 collisions / 199,999 (~25%). Rule 90: 199,965 collisions /
  199,999 (~100%, since `a_t` is almost always 0, so the table has essentially
  one live key and both `r_{t+1}` values appear under it).
* **Fraction of `t` with `r_t = 1`** (the fraction of steps at which the pin
  is FREE and a new bit is genuinely required, per Lemma 1): Rule 30,
  0.5007; Rule 90, 0.000085. Consistent with, but not proof of, the
  respective known density behaviours (P2's density-1/2 claim for Rule 30's
  *centre* column; Rule 90's sparse-but-nonzero neighbour columns).
* **Bounded-history test**, does `r_t` reduce to a function of a length-`k`
  window of `(a_{t-k+1..t})`: for Rule 30, collisions persist through `k = 20`
  (4,282 residual collisions against 181,993 distinct windows seen — the
  residual rate falls only because the aperiodic-looking base sequence stops
  repeating long windows at all, not because the map converges). For Rule 90,
  collisions persist through `k = 20` even though only 2 distinct windows ever
  occur, which is the cleanest possible demonstration that this base sequence
  carries zero bits about this fibre at any bounded history length.

None of this is a new discovery about Rule 30 dynamics; it is a from-source
regression check confirming the analytic argument in sections 1 and 3 on the
one orbit the problem is actually about, per the assignment's instruction to
attempt a cheap computational check before writing the verdict.

## 5. Verdict

**KILLED-BY-REGRESSION**, not "needs a different completion" and not
"viable." The fragment's one sentence, completed the only mathematically
natural way (fibre = the local-rule neighbour column, cocycle = the forward
CA update restricted to a strip), is:

1. Not well-defined as a scalar map on any finite fibre (section 1, both
   analytically via Lemma 1 and empirically via direct collision search).
2. Provably (not just measured) equivalent, at fibre depth `R`, to the
   `pin(R)` ladder language of `RESULTS-ladder-rung1.md`, which is already
   known — by that document's own Corollary 2/3 and by rung 0's depth sweep to
   `R = 7`, `p <= 8` — to never close and to buy only polynomial (`R^2.75`)
   state growth against exponential (`4^R`) raw encoding. This is obstruction
   A (`O(log t)` wall) and obstruction F (free strip boundary) simultaneously,
   both already named in `PATH.md` 7.3 before this document.
3. Cleanly separated from Rule 90 only in a way this repo's own Lemma 1'
   already established (OR nonlinearity vs. XOR linearity), so passing the
   Rule 90 screen here credits no new insight.
4. When retreated to the P2 / unique-ergodicity reading, collapses to the
   already-open R8 orbit-closure question with no reduction in difficulty,
   and independently trips obstruction C (single-column blindness) the moment
   the base sequence is eventually constant, as the Rule 90 measurement in
   section 3 shows directly.

Nothing here proves or disproves P1 or P2. What is contributed is narrow: the
identification that "Direction 8" is not a new proposal at all under any
reading tried — it is `RESULTS-ladder-rung1.md`'s Lemma 1 wearing different
names, and the one piece of new code (`skew_probe.py`) exists only to confirm
that on the actual orbit, not just in principle.

## Reproduction

```sh
cd /Volumes/A/researchpapers/13-rule30/experiments/overnight-arms/roundtable_followup/skew_product_cocycle
uv run python skew_probe.py 200000
```

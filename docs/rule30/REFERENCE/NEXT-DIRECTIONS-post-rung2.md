# What rung 2 changes about where to look

Memo, 2026-09-07.  Not a results doc: two small proved lemmas, one proposed
standing filter, and one target with the right logical shape.  Everything
speculative is marked as such.

## 1. PROVED: the centre column alone reaches exactly one column

From the forward rule at `x = 0`,
`c(t+1) = col_{-1}(t) XOR (c(t) OR col_1(t))`:

* `c(t) = 1`: the OR saturates and `col_{-1}(t) = NOT c(t+1)`, **independent of
  the entire right half-plane**;
* `c(t) = 0`: `col_{-1}(t) = c(t+1) XOR col_1(t)`, carrying no information the
  centre column and the right half do not jointly supply.

  The `c(t+1)` term is **not** droppable.  `col_{-1}(t) = NOT col_1(t)` holds
  only on the sub-branch `c(t+1) = 1`, and fails at 49 of the 95 `c(t) = 0`
  times with `t < 200` on the lone-seed diagram (283 of 519 with `t < 1000`);
  the open branch is not gated by `col_1` alone.

**RETRACTED 2026-09-07.  The one-column reach lemma was false, and so was the
"uniformly in `t`" strengthening drawn from it.**  The struck text is kept
below the correct statement so the error is legible.

**The "exactly when" below is FALSE and was corrected 2026-09-07 (second
correction, same day).  The implication holds; the converse does not, and the
`O(log t)` consequence drawn from it does not follow.  See "Reach is not the
run length" after the proof.**

**Lemma (run reach), sufficient direction only.**  The centre column alone
forces `col_{-k}(t)` ~~exactly~~ when `c(t) = c(t+1) = ... = c(t+k-1) = 1`,
and then

```text
col_{-k}(t) = c(t+k)       k even
col_{-k}(t) = NOT c(t+k)   k odd
```

*Proof.*  Induction on `k`.  `k = 1` is the saturating branch above.  For the
step, the rule at `x = -(k-1)` reads

```text
col_{-(k-1)}(t+1) = col_{-k}(t) XOR (col_{-(k-1)}(t) OR col_{-(k-2)}(t)),
```

and under a run of `k` ones the induction hypothesis gives both
`col_{-(k-1)}(t+1)` and the OR argument `col_{-(k-2)}(t)`, the latter equal to
`1` exactly when the run continues, which saturates the OR. ∎

*Checked two ways.*  On the lone seed to `T = 4000`, the identity holds with
zero exceptions at every depth the runs reach: `1980/1980` at `k=1`,
`1004/1004`, `494/494`, `235/235`, `115/115`, `57/57`, `23/23`, `7/7`, `3/3`
through `k = 9`.  And forcing is genuine, not an artefact of the seed:
enumerating all `2^17` window configurations and grouping by centre column,
`col_{-2}` is constant within a group for exactly 16 of the 64 length-6 centre
columns, and those 16 are precisely the ones with `c(0) = c(1) = 1`.

**Where the old proof broke.**  It asserted that `col_{-2}(t)` is forced only
if `col_{-1}(t) = 1`.  But the OR in
`col_{-1}(t+1) = col_{-2}(t) XOR (col_{-1}(t) OR c(t))` is saturated by
`c(t) = 1` just as well, and `c(t)` is part of the centre column.  The proof
checked one argument of the OR and not the other.  The accompanying
"depth-2 forced fraction exactly 0" measurement encoded the same criterion, so
it corroborated the error instead of catching it.  Credit for the catch: an
external audit, which supplied the counterexample `c(t) = c(t+1) = 1` forces
`col_{-2}(t) = c(t+2)`.

**Reach is not the run length.**  The converse of the lemma is false, and badly.
Enumerating all 256 length-8 centre words, **116 force a cell deeper than their
run-of-ones prefix**; ten words with run 0 force at depth 7.  The shortest
witness is `01010`, which forces `col_{-4} = 0` while forcing nothing at depths
1, 2, 3 — forcing is not monotone in depth, so no outward-one-column
propagation finds it.  The mechanism is a relation between two *unknown* cells:
with `b = col_1(t)`, `d = col_1(t+2)`, the right-column update gives `b*d = 0`,
and `col_{-4}(t) = c(t+4) XOR b*d = c(t+4)`.  A solver tracking each cell as
0/1/unknown loses this.  Rule 90 passes the screen: the same word `01010`
leaves `col_{-4}` free there, so this is not generic left permutivity.

**Exact reach, and the retraction of the `O(log t)` consequence.**  For a fixed
target depth `k`, exact forcing depends only on `c(0..k)` and is decided by
enumerating the `2^k` initial right rows `r_1..r_k`: evolve the right cone with
the centre pinned as its left boundary, then reconstruct leftward.  Every
complete cone with that centre arises from exactly one right word, so this is
exhaustive, and a longer centre window cannot change the verdict at that cell
(it can only expose deeper cells).  Measured maxima over the lone seed, depths
tested through 63:

```text
horizon t <     100    500   1000   2000   4096
max exact reach  15     27     27     31     31
max run           6      7      7      9      9
```

Certificates, each verified here by exhaustive enumeration of every initial
right row: `t=61` forces depth 15 (`2^15`); `t=243` depth 23 (`2^23`); `t=170`
and `t=171` depth 27 (`2^27` each); `t=1046` forces `col_{-31} = 1` and
`t=1987` forces `col_{-31} = 0`, both over all `2^31 = 2,147,483,648` right
rows.  The deepest times have run length 0 or 1, not long runs.

An earlier version of this section reported maxima 9/13/16/18/18 from a
one-step relaxation of the right column (`u(t)=1 => u(t+1)=1-c(t)`).  That
relaxation is sound but strictly weaker — it recovers **none** of the six
certificates above — so its numbers are lower bounds.  A lower bound cannot
establish an obstruction whose content is that reach is too small, and the
inference "obstruction A survives at twice the constant" was not licensed by
it.  Calibration at short windows does not bound the gap: the relaxation
recovers 90 of 90 forced entries at centre length 6 and 400 of 402 at length 8,
then misses every certificate from depth 15 on.

**Status.**  Neither table establishes an asymptotic law.  `31` at `t<2000` is
finite evidence, the depth-63 test horizon is finite, and five starting-time
horizons do not separate `O(log t)` from anything else.  **Obstruction A's
`O(log t)` reach claim is unproved, not restored.**  What survives is the
weaker and still useful statement that no *measured* centre-only propagation
has bridged a `Theta(t)` gap, and the practical routing is unchanged: the
minimal viable object is still the pair `(col_0, col_1)`, register row R1 and
a7's i.o. lemma.  Separately, individually forced cells do not bound a joint
obligation — `m` disjoint pairs each free to be `01` or `10` leave every bit
undetermined while forcing exactly `m` ones — so this table does not bear on
the period-two support-budget target either way.

*(struck)* ~~Lemma (one-column reach): no cell of `col_{-2}` is forced by the
centre column alone, for any centre column.  This is obstruction A in its
sharpest form: reach is one column, uniformly in `t`, not `O(log t)`.~~

*Unaffected by the retraction:* both branch identities were re-verified cell by
cell on the lone seed — the saturating branch `col_{-1}(t) = NOT c(t+1)` holds
105/105 for `t < 200` and 481/481 for `t < 1000`, and the open branch
`col_{-1}(t) = c(t+1) XOR col_1(t)` holds 95/95 and 519/519 on the same
horizons.

## 2. PROPOSED standing filter: seed-vacuity (saturation)

`ladder.step_window` runs no wedge or edge check once `cnt >= R + 2k + 1`.  So
the lone-seed hypothesis enters the ladder through **finitely many**
constraints, and rung 2's four tori satisfy everything the ladder imposes
forever while agreeing with the lone seed nowhere outside a bounded window.

> **Filter.**  Before running a route, ask: does the seed hypothesis fire at
> infinitely many times, or does it saturate?  If it saturates, the route
> proves a theorem about "legal finite prefix + arbitrary half-plane", which is
> a rule-generic object, and no amount of depth repairs it.

This is the same fact rung 1 section 6 recorded as *ingredient 1* (saturation
enables splicing); the proposal is only to use it as a diagnostic, applied
before the compute is spent.  The light cone is a finite-support statement, so
every column-window encoding of it saturates.  The one frame where the seed
never saturates is the diagonal frame (`D_j = 0` for `j < 0`, `D_0 = 1`), and
there the price is obstruction A: the centre reads diagonal `t` at time `t`,
which is deep inside that diagonal's transient, so the periodic regime is
never reached.  *Rate corrected 2026-09-07 by
`RESULTS-ordered-wedge-glide.md`: cite its table, not the `~2^(j/2.4)` I
originally restated here -- the `~2.4 log2 P` law is the **right** frame, and
the left frame's reach grows super-exponentially in `log2 P`
(3, 8, 29, 400, 87867, >2.1e9 for `P = 2..64`).  The conclusion for this memo
is unchanged; only my restated rate was wrong.*

## 3. STRUCK 2026-09-07: fiber rigidity is dead in its usable form

*The width-2 check on the five `T = 24` on-cycle witnesses (the item this
memo's own kill condition asked for) was run.  All five share the **same**
`U` (the alternating centre) and carry **five distinct** `V`.  So at infinite
rightward depth a periodic `col_0` does **not** determine `col_1`: the
uniqueness route to any "periodic centre forces periodic neighbour" statement
is gone, which is the same missing step that killed (Lock)
(`RESULTS-lock-driven-halfline.md`, register row 94).*

*Two further points, so this is not spun.  (i) The conjecture as literally
written ("zero entropy") is **not tested** by that census: restricting to
time-periodic diagrams makes "every fiber member is periodic" true by
construction, so the census has no content for it either way.  (ii) All five
witnesses have eventually periodic width-2 traces, so by Kopra 2023 Thm 3.5
none of them lies in `L_0`.  The tori bound the ladder and nothing else; they
are certified outside the class P1 is about.*

*What follows is the original section 3, kept only so the retraction is
legible.*

### (struck) Target with the right shape: fiber rigidity at *infinite* depth

Obstruction F says a fixed-depth strip leaves its outermost column free.  But
the boundary is free only at **finite** depth.  Rung 2 measured the infinite
depth object inside the time-periodic class: of all `4^T` column pairs with an
alternating centre, the number extendable rightward to *every* depth is 4, 6,
10, 14 -- explicitly enumerable, and 99.7% of candidates die on the pin.

> **Conjecture (fiber rigidity).**  If `col_0` is eventually periodic, the set
> of `col_1` for which `(col_0, col_1)` extends rightward to every depth has
> zero entropy.
>
> If true: `col_1` is eventually periodic, so two adjacent columns are, which
> Jen 1990 Prop. 3 / Kopra 2023 Thm 3.5 forbid.  That is P1.

Rung 2 is this conjecture verified inside the time-periodic slice; the open
part is removing time-periodicity.  It passes the Rule 90 filter by
construction: for rule 90 the same rightward map is a **bijection** (proved in
rung 2's `K5` control), so the fiber is everything and no rigidity exists.
The rigidity is entirely an OR/pin phenomenon.

**Kill condition for whoever tries it:** measure the fiber size against depth
`R` for centres that are not time-periodic.  If it grows exponentially in the
window height uniformly in `R`, the conjecture is dead and this memo's section
3 should be struck.

## 4. Constraints versus counting: how to *state* section 3, not a second route

Every mechanism class killed in the archive is a *constraint system*
(automata, SAT, transducers, conserved quantities, monoids); those saturate and
lose to free boundaries.  A *counting* statement consumes the periodicity
hypothesis globally and cannot saturate.  Morse-Hedlund makes "eventually
periodic" equivalent to "bounded factor complexity", so the conditional form

> `col_0` eventually periodic  =>  the width-2 trace `(col_0, col_1)` has
> bounded factor complexity

contradicts Kopra 2023 Thm 3.5 immediately.

**This is not an independent route, and an earlier draft of this memo wrongly
listed it as one.**  Morse-Hedlund applied to a periodic `col_0` bounds the
factor complexity of the *width-1* trace.  The width-2 trace is `(col_0,
col_1)`, and its complexity is not bounded by `col_0`'s; getting from the one
to the other is exactly the step of controlling `col_1` given `col_0`, which is
section 3's fiber-rigidity conjecture and the whole open problem.  So this
section supplies the *form* in which section 3's conclusion should be written
-- a counting statement rather than a constraint system, which is the reason it
cannot saturate -- and nothing more.  Anyone treating it as a separate line of
attack is assuming the hard step and reading off the corollary.

**Unchanged as of 2026-09-07, and one attempt on it failed.**  A glide-symmetry
argument was proposed as a replacement for the Kopra 2023 Thm 3.5 appeal and
does not work: it stays inside the ordered left region rather than advancing
toward the centre, and the aperiodicity it invoked was measured on the lone
seed, which does not satisfy the hypothesis being refuted.  Retracted in
`RESULTS-ordered-wedge-glide.md` section 5.  Kopra stays in the chain.

Note also this is **not** row 76 or `RESULTS-subword-complexity-extended.md`:
those *measure* the complexity of the real column and are limited by
obstruction H.  The conditional form assumes the thing to be refuted and needs
no finite horizon.

*Scope of the novelty claim (completed 2026-09-07).*  `docs/rule30/` and the
whole `experiments/` tree were searched for Morse-Hedlund, Kopra, and
factor/subword complexity.  Nothing states the conditional form.  The two
nearest artefacts are `experiments/rule30/factor_complexity_probe.py` and
`experiments/overnight-arms/roundtable_followup3/subword_complexity/`, both
unconditional measurements of the real column, and
`experiments/rule30/periodicity_bridge_probe.py`, which falsifies several
tempting width-2-to-centre bridges and is the closest prior work to the gap
named in the paragraph above.

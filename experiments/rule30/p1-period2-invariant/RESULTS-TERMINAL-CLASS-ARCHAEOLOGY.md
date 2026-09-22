# The needle has been sighted five times under five names, and dropped each time for a population reason

Date: 2026-09-05.  Scripts: `terminal_fiber_classes.py`, `class_edge_check.py`
(scratchpad; logs `terminal_fiber_classes_20260905.log`,
`class_edge_check_20260905.log` in this directory).  Archaeology conducted via
four read-only automated searches over `docs/rule30/` and this directory;
every citation below not independently opened and confirmed here is marked
(relayed).  Nothing committed.

## 0. What this is

Two computations run here, then a read of the whole attempt archive asking
one question: where did the same phenomenon appear before, and why was it
dropped.  The answer is that it appeared at least five times, was named
correctly at least twice, and was abandoned every time because the next
measurement was a population statistic, and the population is fine.

## 1. Calibration correction first: the thread's ceiling is a theorem, not a lemma

The brief said proving `gamma(n) >= 1` for all `n` "only kills period-2 on one
route."  The capsule's reduction chain (`PROOF-STATE-CAPSULE.md:28-51`, read
directly) is marked "proved" with `[R, OPEN]` only on its terminal node (SEP).
The period-2 archaeology pass traced every arrow to its proof file (relayed):

```text
gamma(n) >= 1  for all n
  => H_r(n) = empty for all n, r, c        RESULTS-KSTAR-GAMMA-EXTENDED.md:24-34
  => no RW witness at any (n, r, c)        BACKLOG.md:33 (collapse lemma)
  <=> DLP                                   RESULTS-DLP-ROTATED-WEDGE.md:44-57
  => SEP                                    RESULTS-LATE-PULL-DIAGONAL.md:32-57
  => (PT2)                                  PROOF-STATE-CAPSULE.md:51
  => Thm(2): lone-seed centre column is not eventually period 2
```

Every arrow is a proved uniform implication; the hypothesis is the only open
item.  `(PT2)` is the stronger same-orbit statement over all finite
configurations.  Only `n >= n0` needs a proof; the finite remainder is done
(SAT to `n=28`, exhaustive to `n=24`).  The converse fails (a `gamma`
counterexample would not refute PT2), and this is the `p=2` rung only.

So the thread's ceiling is **the first per-period exclusion theorem for this
column**, which the project's own literature survey says does not exist for
any `p`.  That changes what the thread is worth and should be stated in the
brief.

## 2. The needle, stated exactly

### 2.1 Per-class terminal fiber, exhaustive, r=0

For each `(n, c)`, the words achieving `max_survival`, grouped by the
continuation they produce.  Within a class: identical continuation, identical
killer, common suffix of length `n` minus the free prefix.

| n | c | max_surv | gamma | fiber | classes | class sizes | free prefix | killer |
|---|---|---|---|---|---|---|---|---|
| 14 | 2 | 10 | 6 | 4 | 1 | 4 | 5 | 1-after-1 |
| 14 | 3 | 8 | 8 | 8 | 3 | 4,2,2 | 2,1,1 | 3,0,0 |
| 15 | 2 | 9 | 8 | 10 | 3 | 4,4,2 | 2,2,1 | 3,0,0 |
| 15 | 3 | 8 | 9 | 9 | 3 | 4,3,2 | 2,2,1 | 3,3,0 |
| 16 | 2 | 10 | 8 | 3 | 1 | 3 | 3 | 3 |
| 16 | 3 | 10 | 8 | 18 | 2 | 10,8 | 5,4 | 3,3 |
| 17 | 2 | 11 | 8 | 10 | 1 | 10 | 6 | 3 |
| 17 | 3 | 10 | 9 | 6 | 1 | 6 | 3 | 1-after-1 |
| 18 | 2 | 12 | 8 | 16 | 2 | 8,8 | 5,3 | 3,0 |
| 18 | 3 | 11 | 9 | 12 | 1 | 12 | 5 | 0 |
| 19 | 3 | 13 | 8 | 6 | 1 | 6 | 3 | 1-after-1 |

(`n=19, c=2` pooled: 8 words, 2 classes.  `n=20, 21` in flight.)

The extremal continuations are hard-core words heavy in 2s and nearly
periodic: `22222122222`, `2222122221`, `2221221221221` = `2(221)^4`,
`2212121212` = `22(12)^4`.  The forcing is sitting in a periodic orbit of the
local map until the phase slip lands.

### 2.2 Within a class, the forcing's complete state is identical

`class_edge_check.py`, `n=14..16`, all 13 classes.  The state carried by
`literal_extension` is the dependency edge (a vector of length `2n` after the
padded word) plus the last symbol.  Reading `append_dependency_edge`
(`constant_tail_scale.py:205-218`): the new edge is `new[0] = BOUNDARY[v]`,
`new[1] = phi(prev, new[0])`, `new[j] = phi(old[j-2], new[j-1])` for
`j = 2..L`, so `old[L-1]` is **never read**.  The last cell is output, not
state.

| n range | classes | full edge identical | differ only in newest 1-2 cells |
|---|---|---|---|
| 14-16 | 13 | 10 | 3 |
| 17-19 | 8 | 4 | 4 |

Extended to `n=17..19` (`class_edge_check_20260905.log`): every terminal class
has live state **either identical or differing only in the newest one to two
cells of the edge** (the output end; at least one is the unread cut cell).  The
prefix is genuinely forgotten down to the last cell or two.  This is not "same
D8 phase, different state," which is what the PATH read predicted the check
would show (`FACT-INDEX.md:425`, relayed).  It is genuine forgetting: the
shared suffix maps those specific prefixes to one state (or one future).  This does not
contradict the no-synchronizing-word certificate (`FACT-INDEX.md:124-126`,
relayed), which says no word synchronizes *all* prefixes; here a suffix
synchronizes 3 to 12 of them.

So the terminal class is a fiber of `W -> state`, and the exact statement of
the theorem is:

> **No reachable state of the forcing at source length `n` survives `n+2`
> forced steps.**  The states that come closest number 1 to 3 per `(n, c)`.

The fast method already deduplicates by state (`RESULTS-GAMMA-PROOF-ATTEMPT.md:101-109`,
relayed: "one representative source word per distinct `(edge, endpoint_symbol)`"),
and reachable states number about `1.77^n` (`RESULTS-CLUSTER-ANATOMY.md:44-61`,
relayed).  Nobody then asked what the extremal *state* is.

## 3. Five prior sightings

1. **`RESULTS-PSI-ANCESTRY-LAW.md:174-189, 232-236`** (relayed; BWH+ object,
   the no-hard-core relative).  "The extremal set is a suffix cylinder.  All 18
   sources attaining index 15 at n=15 share the 9-symbol suffix `211212112`;
   the free prefix is 18 of the 64 six-symbol words."  And: "the survivors die
   *simultaneously* ... A shared cause kills a whole suffix cylinder at once.
   Identifying that cause is a sharper question than (PSI)."  Named exactly.
   Dropped at `:213-230` and `:238-267` for two population reasons (an
   independence-null count over all `2^n` sources; full algebraic degree of
   the defect over all sources).  `:273-277` says itself that an
   ordered-ancestry argument "is untouched by this measurement."  **Never
   re-run on the RW object.**
2. **`RESULTS-EXTINCTION-MARGIN.md:33-37`** (relayed; RW object, this
   thread).  "The finalist words at each n ... share a long common suffix,
   differing mainly in their first one or two symbols."  Its derivation
   attempt `:68-87` was killed as a generic finite-monoid argument with the
   instruction "do not retry ... without a specific candidate word family."
   The class table above is that family, per `n`.
3. **`FACT-INDEX.md:387-388`, `START-HERE.md:156-157`** (relayed).  The `n=15`
   binary-wedge falsifier "maps to `1^16 0`, explaining both its sixteen-cell
   plateau and immediate failure."  Plateau then one killer, on one extremal
   word.  "Never generalised."
4. **`RESULTS-alt-trace-fiber.md:100-199`** (read directly; row 41 of the
   register, one rung down the same chain).  Past a knee at `d/2` the survivor
   automaton is a parameter-free deterministic map with branching factor 1,
   the forced output is `L = v XOR parity(OR-word of the two stored
   diagonals)`, and the certificate level is `d/2 + (longest single orbit) + 1`
   with orbit maxima 7, 9, 16 at seed lengths 8, 12, 16.  Its own words:
   "Linear growth of the maxima means per-`d` certificates can never reach
   uniformity by themselves; the theorem must come from the map."  Its
   proposed next angle, "the dynamics of the OR-word `o` itself," is
   single-object and was **never run** (no RESULTS file; wider-docs read).
   Same shape as this thread exactly: one longest orbit decides, maxima grow
   linearly in the seed, `max/seed` in `[0.75, 1.0]` there against
   `[0.55, 0.76]` here.
5. **`START-HERE.md:279-281`** (relayed).  "The live target is to prove that
   the shortest word in `L_h` tends to infinity; its checked values jump
   through lengths 1/2, 3, 5, 10 with plateaus."  One extremal word per
   horizon, with plateaus.

## 4. Why each was dropped: the population reflex

The archive's own summary of its 142 kills, `RESULTS-CROSS-METHOD-INVARIANT-AUDIT.md:156-160`
(relayed): "the forced dynamics is statistically and algebraically
indistinguishable from maximal entropy subject only to hard-core.  That is
why ~142 routes died: every one of them searched for exploitable structure,
and the measurements collectively say there is none to find."

That sentence is true of the bulk and false of the tail.  A maximal-entropy
hard-core process does not emit `22222122222`; it does not put 10 words on one
state; it does not plateau for four steps and then kill everything at once.
The archive measured the bulk (fibers, ratios, first moments, entropy,
spectral radius, conditional block loss, window relaxation, survivor decay)
and each measurement correctly reported "nothing here."  Two files reached the
right conclusion and were not followed:

* `RESULTS-FIB-FIBER-UNIFICATION.md:106-117` (relayed): "the obstruction is
  entirely the deep regime where `S_k` is a small constant."
* `RESULTS-WINDOW-SPECTRAL-RELAXATION.md:174-223` (relayed): domination fails
  only at `S_k = 1..28`; "the shape a working proof needs is ... a split
  argument ... plus a separate finite argument once `S_k` drops below a
  constant."

Register rows killed on population/depth/boundary grounds, hence not binding
a single-state argument (PATH read, relayed; row `N` is `PATH.md` line
`580+N`): 2, 3, 4, 6, 7, 33, 34, 35, 48, 54-59.  Of these, **row 35** is the
one that matters: rows 25/26 proved "the forced half forgets the other half,
then finiteness contradicts" for the zero trace (the forced left half is an
infinite checkerboard, contradicting finite support), row 35 tried nonconstant
periods and was killed because 505-512 of 512 positions differ *across right
parts*, a population fraction.  Whether the extremal state forgets was never
measured.  Section 2.2 is that measurement: it does.

## 5. Claims in the archive that this data contradicts (relayed quotes)

1. `RESULTS-GAMMA-PROOF-ATTEMPT.md:239-240`: "No common suffix, and no
   shrinking toward a unique witness."  Pooled across finalist *states* at
   fixed `n`; within a class there is a common suffix of `n-1` to `n-6`.
   Its `:243-244` ruled out an infinite limiting word "without ever grouping
   by continuation."  Its `:394-404` predicts the proof "is more likely via a
   genuine concentration/large-deviation argument on the survival-population
   decay than via any structural combinatorial identity."  The opposite.
2. `RESULTS-CLUSTER-ANATOMY.md:31-33`: "the killer is the E-miss of the
   forced symbol ..., never a missing forced symbol and never hard-core
   alone."  Rested on four clusters.  `n=14 c=2`, `n=17 c=3`, `n=19 c=3` die
   on `1`-after-`1`.
3. `RESULTS-FIB-FIBER-UNIFICATION.md:90, 114-115`: past `k_star` the map
   "becomes essentially injective ... the forced continuation nearly
   determines the source word."  At the deciding depth it is 3-to-1 to
   12-to-1 with an identical state.
4. `RESULTS-RW-LINEAR-SLACK.md:194-196`: "Every early bit is a one-in-two
   constraint on survival."  Within a class the early bits are free (10 of 64
   at `n=17 c=2`; halving would predict 1).
5. `RESULTS-MEASURE-SUPPRESSION.md:120-127`: survivor counts "hit zero by row
   8-11 regardless of `n`."  `max_survival` is 18 at `n=30`.
6. `RESULTS-TRANSFER-DOMINATION-CHECK.md:84-88`, `RESULTS-CROSS-METHOD-INVARIANT-AUDIT.md:156-160`:
   the forced symbol "behaving as if uniformly distributed ... independent of
   history."  Not on the extremal state.

## 6. What the archive already holds for a single-state argument

* **A proof template that worked once, for exactly this reason.**
  `RESULTS-ENDPOINT-RESTART-COCYCLE.md:129-171` (relayed): fix the family
  (`2^k 12 v`), derive its autonomous finite quotient (period 32, never
  hard-core), traverse it exactly.  `PROOF-STATE-CAPSULE.md:247-248`: it
  "works because its fiber is fixed."  Section 2.2 says the extremal class's
  fiber is a single state.
* **An exact all-length identity for the killer.**
  `RESULTS-PULL-ROW-ALPHA-SUPPORT.md:54-97` (relayed): on a surviving row,
  `alpha = parity{i >= 1 : R_i != 0}` over the reversed dependency edge, and
  the E-miss is exactly `alpha: 1 -> 0`.  So "why does the extremal state die
  at step `max_survival + 1`" is a finite exact computation per `n`.
* **The forcing's algebra**, read directly here: `phi(l, .)` is a
  permutation of `{0,1,2,3}` for each `l` (`dyadic_periodicity_analyzer.py:307-309`),
  so the cut cell is a D8 product over the old edge applied to a seed
  determined by `(prev, v)`; that is why exactly one symbol is ever forced.
  The archive has the group cold (`RESULTS-CARRY.md:57-90`,
  `RESULTS-BINARY-WEDGE-HIGH-ELIMINATION.md:9-45`, relayed) and already ruled
  that it is not by itself a reduction (`RESULTS-EXTINCTION-MARGIN.md:68-87`).
* **The same recursion is Rowland's.**  The alt-trace forced output is a
  running parity of an OR of two diagonals; the identical recursion
  `E_j[t] = E_j[t-1] XOR (E_{j-1}[t-1] OR E_{j-2}[t-1])` is what makes the
  right-cone diagonals purely periodic with power-of-two period
  (`RESULTS-diagonal-periodicity.md:23-44`, Rowland 2006 Lemma 2, relayed).
  A periodic state therefore emits a periodic continuation forever; the
  wallpaper member `{1,4}` (`RESULTS-alt-trace-fiber.md:189-194`, read
  directly) is an infinite-left seed that passes every check.  Any proof must
  consume the finiteness of the seed through the map, not through a
  statistic.  Rowland's ingredient alone is rule-blind (Rule 90's diagonals
  are also purely periodic); the OR pin is where Rule 30 enters.

## 7. The walls that still bind (PATH read, relayed)

* **Obstruction D** (`PATH.md:768-774`): any window or memory rule for the
  forcing must be derived and checked, not named.
* **Closure collisions** (`FACT-INDEX.md:310-319, 420-431`): bounded summaries
  of the forcing collide (same summary, different future) at lengths 8, 9,
  13, and there is no proper contracting ideal in D8.  Any finite invariant
  must escape these.  Section 2.2 is the converse situation (different words,
  same future) and is not blocked by them, but a proof that generalises it
  to all `n` is.
* **Obstruction H**: enumeration to `n=30` proves nothing beyond `n=30`.
* **Rule 90**: `RESULTS-RW-LINEAR-SLACK.md:245-246` (relayed): "The Rule 90
  control was not run (no Rule 90 carry kernel in this arm)."
  `RESULTS-RULE90-FILTER-ON-SPECTRAL.md:15-25` (relayed): hard-core counts and
  left-permutivity are rule-blind; the only Rule-30-specific ingredient is the
  OR saturation, so a class-kill argument must route through the E-miss of
  the forced cell, not the no-`11` count.  Note three of the eleven classes
  above die on the no-`11` count.

## 8. The question this leaves, stated so it can be run

Not run here; recorded as the next thing.

1. **Is the extremal state at `n` related to the extremal state at `n+1` or
   `n+2`?**  `RESULTS-FIBER-EXTREMAL-FAMILY.md` looked for a family in the
   continuation *strings* and found none.  Nobody compared the extremal
   *states* (the `2n`-vectors of section 2.2) across `n`, nor their
   `alpha`-profiles, nor which D8 element the suffix leaves them in.  If a
   family exists there, the cocycle template of section 6 applies to it.
2. **Why does each extremal state die?**  Evaluate the `alpha` identity on
   it at the killing step.  Eleven data points exist.
3. **Rule 90 control.**  Build the Rule 90 carry kernel (linear, so `phi` is
   XOR-affine and the OR saturation is absent) and run the same census.  The
   prediction from section 7 is that Rule 90's hard-core filter does nothing
   and its `gamma` is not bounded below.  If Rule 90 also gives `gamma >= 1`,
   this thread measures the encoding.

## 9. Mechanically verified here (direct runs, not relayed)

Three claims the argument leans on, checked directly against the real
functions:

1. **Suffix lemma.**  Two words with the same suffix from index `m` and the
   same first `2m` forced symbols have identical forced continuations forever.
   `n=12`, tail 2: **16,004 matching-key pairs, 0 continuation mismatches.**
   This is the forcing-level mechanism of the needle.
2. **The OR collapse is the one Rule-30-specific ingredient.**
   `FORWARD[2] == FORWARD[3] == (3,2,1,0)`, so `cone_local(1,r) == cone_local(3,r)`
   for all `r`, and only **3** distinct left-actions exist rather than 4.  This
   is where the forcing erases history, and it is exactly the Rule 30 OR: under
   Rule 90's XOR the carry action is bijective in every argument and no collapse
   occurs.  Any theorem here must route through this, not through the no-`11`
   count (which is rule-blind).
3. The "half-window law" as I first coded it tested the wrong index coordinate
   and produced spurious violations; the suffix lemma (1) is the load-bearing
   consequence and it holds, so this is set aside, not reported as refuted.

## 10. The needle is a property of the forcing map, not the source constraint

The fourth archaeology read (relayed) claimed "the reduction only needs
hard-core sources," implying the all-`{1,2}^n` census chases a stronger
statement than the theorem needs.  **That interpretation is wrong for the
object `gamma` measures, and the correction matters.**

`RESULTS-DLP-ROTATED-WEDGE.md:54-55` (read directly): RW's first `n` symbols
"need only lie in `{1,2}`; they need not avoid `11`."  So RW / `H_r` / `gamma`
quantify over **all** `{1,2}^n`.  Recomputed margins, hard-core `W` vs all `W`
(`hc_vs_all.py`, exhaustive):

| n | c | all-W gamma | all-W extremal (has `11`?) | hard-core gamma |
|---|---|---|---|---|
| 16 | 3 | 8 | `1111112122211122` (yes) | 12 |
| 17 | 2 | 8 | `11112121111111212` (yes) | 9 |
| 17 | 3 | 9 | `11222211112212111` (yes) | 14 |

The all-W deciding words **contain `11`**, and hard-core `W` survives far fewer
steps (larger `gamma`).  So the words that come closest to breaking
`gamma >= 1` are exactly the non-hard-core ones the read proposed to discard.
You cannot restrict the RW/`gamma` object to hard-core sources; the extremum
lives outside them.

**But there are two distinct reductions, and the confusion is between them:**

* **RW / DLP / `H_r` / `gamma`** (`RESULTS-DLP-ROTATED-WEDGE.md`): source over
  all `{1,2}^n`, suffix hard-core.  Extremals non-hard-core.  This is what
  this census measures.
* **Constant-tail scale `s_c(W)`** (established in prior notes, relayed):
  `W` is a middle block of a fully hard-core endpoint, so `W` is hard-core by
  construction.  Extremals are clean periodic words.  Proven equivalent to
  (PT2) by the same chain, and the coarse bound `s_2(W) <= |W|`,
  `s_3(W) <= |W|+1` (which is `gamma >= 1`) passed finite certificates to
  length 22-23.

Both reductions close (PT2); they are different finite-word targets with
different extremal families.  The read's candidate is the second target, where
hard-core is native.

**The decisive check: the needle survives on hard-core sources too**
(`hc_terminal_classes_20260905.log`, exhaustive over hard-core `W`, `n=14..18`).
Every cell has 1-4 continuation classes with long shared suffixes and a single
killer, exactly as in the all-`{1,2}` object.  And the hard-core extremals are
the clean periodic adversaries the read predicted:

| n | c | hard-core fiber | classes | top class suffix | continuation |
|---|---|---|---|---|---|
| 17 | 2 | 2 | 1 | `2212121212121212` (16 of 17) | `2122122121` |
| 16 | 2 | 2 | 1 | `212212122122122` (15 of 16) | `2221212222` |
| 18 | 3 | 2 | 1 | `21212212222221222` (17 of 18) | `212212121` |

So **the needle is a property of the forcing map itself, robust to whether the
source is constrained hard-core.**  This is the finding that unifies the two
lines: the map degenerates to 1-4 states near extinction in both objects, and
the hard-core object is the cleaner one to attack because its extremals are
periodic (the cocycle template of section 6 wants a fixed periodic family).

## 11. The sharpest target, restated with everything above

Prove: **for hard-core `W` of length `n`, the constant-tail forced extension
`s_c(W)` reaches at most `n+1` before a defect (`gamma >= 1`).**  Everything
needed is now on the table:

* The extremal `W` at each `n` is one of 1-4 suffix classes (measured `n<=18`),
  each collapsing to a single forcing state or future (section 2.2, 9.1).
* That state emits a periodic continuation until a phase slip; the slip is an
  exact all-length event, `alpha: 1 -> 0` over the reversed edge
  (`RESULTS-PULL-ROW-ALPHA-SUPPORT.md`, relayed).
* The proof template that closed the analogous cocycle case fixes a periodic
  family and traverses its autonomous finite quotient
  (`RESULTS-ENDPOINT-RESTART-COCYCLE.md`, relayed); the hard-core extremals ARE
  a periodic family.
* Rule 90 control: the argument must use the OR collapse (section 9.2), which
  is vacuous for Rule 90, so it passes the filter by construction — but the
  control has never actually been run on this thread
  (`RESULTS-RW-LINEAR-SLACK.md:245`, relayed), and building the Rule 90 carry
  kernel and rerunning the census is the cheapest missing calibration.

The one thing not yet checked, and the concrete next step: **do the extremal
forcing states form a family across `n`** (compare the `2n`-cell states, their
`alpha`-profiles, the D8 element the shared suffix induces).  If they do, the
cocycle template applies and this is a proof route.  If they do not, it is a
per-`n` certificate at best.  `RESULTS-FIBER-EXTREMAL-FAMILY.md` looked for a
family in the continuation strings and found none; nobody has compared the
states.

## 12. Resolved / pending

* **State-family comparison across `n`: DONE, NEGATIVE** (2026-09-05,
  `../p2-needle-attack/estate_RESULTS.md`, verified independently). The extremal
  forcing states carry no cross-`n` family under prefix/suffix alignment,
  state-containment, the `2^k` cocycle signature, or alpha-support geometry, at
  strides 1/2/4, both arms, both tails. Controls reproduce this file's §2.1
  table exactly and cross-check against `literal_extension` at 100%; the
  discriminating suffix-aligned null is tight (p95 2-4 cells) and still shows no
  separation. **So the needle is a per-`n` certificate and the cocycle template
  (§6, the one concrete proof route) is NOT in range via this door.** Residual
  not tested: a survival-row-aligned or killing-row-aligned comparison — a
  later session must not read the negative as excluding that alignment.
* **Rule 90 control: DONE, census is Rule-30-specific** (2026-09-05,
  `../p2-needle-attack/r90_RESULTS.md`, verified). No Rule 90 carry kernel
  reproduces Rule 30's signature (max_survival growing at bounded gamma);
  outcome B (artifact) ruled out. Caveat the agent stated honestly: a unique
  Rule 90 kernel is not recoverable (the OR hides which neighbour Rule 90
  drops), so it enumerated all 4 candidates and the verdict is invariant.
  Two code corrections it surfaced: (a) `carry_transducer.py use_or=False` is
  the **Rule 150** kernel (`l^c^r`), not Rule 90 -- any prior "Rule 90 control"
  resting on it is void [flag: not independently reconfirmed; likely off the live
  census path]; (b) this doc's earlier relay that `RESULTS-RULE90-FILTER-ON-SPECTRAL.md`
  says no-11 "must not transfer" was WRONG -- that doc (line 17) classifies
  no-11/Fibonacci/phi as RULE-BLIND; the "must not transfer" line is
  from prior notes, about the OR-derivation of the predicate. Both are
  true in different senses (no-11 is rule-blind as a counting object; its
  correctness as the predicate derives from OR).
* **Corroboration, independent and cleaner:** `RESULTS-RULE90-FILTER-ON-SPECTRAL.md`
  shows the phi/4 machinery gives extinction for Rule 30 (q=1/4) and correctly
  refuses Rule 90 (q=1/2 -> 2*lambda=1.618>1), and that Rule 30 is the UNIQUE
  quiescent left-permutive ECA passing q<1/(2*phi). The discriminating
  ingredient is the OR nonlinearity. (That doc also states, honestly, this
  singles out the rule but does NOT prove extinction.)
* **NET VERDICT (p=2), verified both sides:** gamma>=1 is Rule-30-specific and
  passes the filter; the needle is a per-n certificate with no cocycle family;
  first-moment/spectral passes the filter but cannot close. So p=2 exclusion is
  a genuine Rule-30-specific phenomenon, empirically solid to n=30, with **no
  currently-live proof route**. The honest paper result is a structured
  negative, not a theorem.
* `terminal_fiber_classes.py` n=20/21: confirmatory, done.

# R7 logical and splice audit

Date: 2026-09-09.

Evidence: `U` uniform proof, `R` reduction, `C` finite certificate,
`M` measurement, `K` killed implication. Original engines and reports were
imported/read without edits. Reproduction:

```sh
uv run --with numpy python experiments/rule30/ladder-rung3/logic_audit.py
```

The numerical output is `logic_audit.json`. This audit does not construct an
aperiodic full diagram and does not prove its nonexistence.

## 1. The original i.o. lemma is weaker and is about a specified diagram

The primary source is
`experiments/overnight-arms/frontier_attack/a7_ladder_realizability/ladder_realizability.md`,
section 4. Its exact statement is:

> `col_1(t) = 1` for infinitely many `t` with `col_0(t) = 0`, in `X(k, 01)`.

Here `X(k,01)` is the specific greedy left-permutive construction of its
section 1, with zero initial right half and onset `2k+1`. Its Theorem B
explicitly concludes `Diff_q` for every **odd** `q`. To cover every bounded
`Q`, that theorem explicitly asks for an additional analogous **even**-`q`
statement. It does not identify the i.o. lemma with aperiodicity. Its final
paragraph calls the common zero set a structural observation, expressly
"not a reduction".

Write the alternating phase as `c(2i)=0`, `c(2i+1)=1`, after discarding a
finite prefix, and let `e(i)=col_1(2i)`. Exact Rule 30 inversion gives

```text
col_-1(2i)   = 1 XOR e(i)
col_-1(2i+1) = 1.
```

Consequently:

* `Diff_(2h)` holds infinitely often exactly when
  `e(i) != e(i-h)` infinitely often.
* `e(i)=1` infinitely often suffices for every odd `q`, and is necessary for
  any odd `q` to fire infinitely often.
* The full `col_-1` is not eventually periodic exactly when `e` is not
  eventually periodic. Any eventual period of `e` doubles to one of
  `col_-1`; an even period of `col_-1` restricts to one of `e`, and any odd
  period can first be doubled.

Thus merely ruling out eventual `e=0` does not rule out eventual nonzero
periodic `e`. In particular q=420 asks for non-210-periodicity of `e`, not
just infinitely many ones. This calculation uses the Rule 30 OR: replacing
OR by Rule 90 removes the odd-phase pin to 1.

**`C/K`: smallest supplied torus counterexample to the strengthened
implication.** The existing T=4, N=7 torus is

```text
col_0  = (0101)^omega
col_1  = (1100)^omega
col_-1 = (0111)^omega
e      = (10)^omega.
```

`torus.verify_torus` rechecked all cells from the forward Rule 30 rule;
`torus.min_period` gives 4. There is exactly one i.o. event per time period,
two Diff_1 events, and zero Diff_4 or Diff_420 events. The repaired splice
below at R=1,k=1 was also checked through the unchanged
`ladder.successors` and `ladder._sccs`, with the input letter cycle fixed:

| q | fixed-tail product states | accepting SCCs |
|---:|---:|---:|
| 1 | 12 | 1 |
| 4 | 20 | 0 |
| 420 | 1684 | 0 |

These are exact fixed-word product graph decisions, not `ladder.decide`
counts for the entire unrestricted language. The torus is not `X(k,01)`;
it disproves the claimed general implication i.o. => aperiodicity, not the
specific i.o. lemma itself. Conversely, an aperiodic diagram constructed by
some other method would not prove a claim about the particular `X(k,01)`.

**`U`: the primary i.o. lemma follows from an already proved repository
theorem.** `experiments/rule30/p1-period2-invariant/RESULTS-RIGHT-FILTERED-MORTALITY.md`
section 1 proves that every actual right trace under an alternating centre
avoids `00000` in these even samples. Therefore `e` has a 1 in every block
of five samples, for `X(k,01)` as for every actual alternating-centre
diagram. In particular the precise a7 i.o. lemma holds for every k; no
aperiodicity conjecture is needed. This is a cross-reference consequence of
the existing R5 theorem, not a new proof of aperiodicity or of all even-q
acceptance.

The old proof code was re-read and rerun, unmodified:

```sh
uv run python experiments/rule30/p1-period2-invariant/right_trace_forbidden.py --max-language 5
```

Its exact Boolean-ANF product vanishes, the independent 512-assignment
right-light-cone check has no five-zero witness for Rule 30, and the same
control under Rule 90 yields the existing counterexample mask `0x114`.
This local result excludes one fixed factor. It is not a bounded-window
test for eventual periodicity, and it leaves periodic `e=(10)^omega`
untouched. The finite witness above identifies exactly why recovering the
literal i.o. lemma does not settle the stronger requested object.

## 2. A finite census does not force an aperiodic witness

**`K`: scope error in the last paragraph of rung 2 section 5.** Its census
excludes a time-periodic torus of period at most 24 witnessing q divisible by
420. It does not exclude one of period greater than 24. It also does not
exclude a full diagram with eventually periodic `col_-1` but without a
common temporal period for every column. No claim here revives the refuted
"2 x prime" prediction or predicts a new achievable period.

For one fixed q, failure of eventual q-periodicity is weaker than failure
of every eventual period. Even a valid q=420 witness could be eventually
p-periodic for some p not dividing 420. Likewise a q=420 witness need not
witness all multiples of 420 (e.g. a hypothetical period p=8 would fail
q=840). The latter example is arithmetic only; no Rule 30 period-8
full-diagram witness is asserted.

## 3. Exact pin failure in the published splice, and uniform repair

**`C/K`: published splice fails its pin at the seam.**
`ladder_splice.run` checks wedge constraints through `ladder.step_window`.
Its pin loop checks only consecutive letters wholly inside the torus. The
pin in the actual `rung1.explore_pin` applies at every letter transition,
including the splice.

For the T=4 torus, R=1,k=1, `saturate=4`, the true seed prefix is packed
letters `[2,3,0,3]` and the torus starts with packed letter `1`. At the seam
the transition `3 -> 1` is `(1,1) -> (0,1)`. The original
`rung1.pin_ok(3,1,30)` returns false: `col_R=1` requires the next right bit
to be the complement of the previous left bit, but both bits here are 1.
This is the smallest R,k and first supplied torus, rather than a failure
requiring long horizons.

The original grids R=1..12,k=1..4 were rerun for all four tori, checking the
actual seam transition with `rung1.pin_ok`:

| T | original splice cases | seam pin failures |
|---:|---:|---:|
| 4 | 48 | 15 |
| 6 | 48 | 13 |
| 10 | 48 | 9 |
| 14 | 48 | 13 |
| total | 192 | 50 |

The plain-splice theorem is unaffected. The claimed identical pinned
splice is false as written; the nonemptiness conclusion has a simple
uniform repair.

**`U`: one-letter bridge.** Let the last prefix letter be `(a,b)` and the
first tail letter be `(a',b')`. Insert

```text
(1-b', b*(1-a)).
```

If `b=1`, its right bit is `1-a`, so the first pin holds. If the inserted
right bit is 1, its left bit is `1-b'`, so the second pin holds. When a
right bit is zero the corresponding pin is vacuous. These are all cases.

All 16 possibilities are also checked against the frozen `rung1.pin_ok`:
entries are the inserted packed letter, with packing `(left<<1)|right`.

| previous \ first | 0 | 1 | 2 | 3 |
|---|---:|---:|---:|---:|
| 0 | 2 | 0 | 2 | 0 |
| 1 | 3 | 1 | 3 | 1 |
| 2 | 2 | 0 | 2 | 0 |
| 3 | 2 | 0 | 2 | 0 |

The bridge is inserted at letter time `saturate`, so no wedge/edge check
can reject it. After the finite window flushes, the tail derived columns
are exactly the same torus columns shifted by one time unit. The guessed
periodic onset absorbs that shift; eventual Diff_q is unchanged. Prefix
and tail pins already hold internally; the two checked transitions settle
the whole seam. This proves the repaired construction works uniformly for
every R,k and every applicable q.

**`C`: repaired engine replay.** For all 192 original parameter pairs, the
bridge was added and the complete finite prefix and tail were replayed
through `ladder.successors` and `rung1.pin_ok`. The fixed periodic input was
then composed with the exact engine states and checked for an accepting
SCC by `ladder._sccs`: 192 accepting fixed-word products for q=1, zero pin
failures. This is stronger than inferring acceptance from a count of diff
events during finite simulation. In the smallest case the repaired prefix
is `[2,3,0,3,0]`, followed by cycle `[1,3,0,2]`.

**Rule 90 control.** The existing `controls.rule90_control(Tmax=6)` was
reused without modification. At T=2,4,6 it reports `L90_bijective=True`,
forward-rule-verified tori, and full minimal periods 2,4,6 respectively.
`rung1.pin_ok(...,90)` is vacuous; the bridge is specifically repairing
the nonvacuous OR pin of Rule 30. No new Rule 90 implementation was made.

## 4. Why an abstract nonexistence theorem would not itself give EMPTY

These are quantifier obstructions, not claims about new Rule 30 witnesses.

If every full diagram with eventually alternating centre had an eventually
periodic neighbour, the period could depend on the diagram. This does not
yet produce one q shared by every accepted diagram, as a fixed-q EMPTY
verdict requires. For example the already certified periods 4 and 6 alone
show why eventual periodicity does not imply eventual q-periodicity at an
arbitrarily selected q.

Even if one establishes a fixed q for all full diagrams, the next step
"therefore some finite depth is EMPTY" needs a separate argument. The
eventual-periodicity/Buchi conditions are not closed under limits. A precise
abstract counterexample to an unqualified compactness step is the nested
family `Y_R` of infinite binary words with at least R zeros between any two
ones. Each `Y_R` has the periodic word `(1 0^R)^omega`, with infinitely many
Diff_1 events. Their intersection consists of words with at most one 1;
none has infinitely many Diff_1 events. The safety constraints are nested,
closed, shift invariant, and finite-window at each R, yet accepting witnesses
do not survive the limit. This is an obstruction to that generic inference,
not a bounded-window proposal for Rule 30 and not a Rule 30 counterexample.

Thus the remaining construction task needs compatible right extensions
together with persistent Diff events, and the nonexistence-to-EMPTY task
needs a uniform period and a finite-depth liveness argument. None of these
extra obligations follows from a finite torus census or from the original
i.o. statement alone.

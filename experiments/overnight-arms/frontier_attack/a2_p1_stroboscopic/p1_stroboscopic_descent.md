# NEGATIVE-NAMES-MISSING-LEMMA — the missing lemma is: *for a nonzero finite row whose centre trace is 2-periodic, `s(t,1)` is constant on the zero-set of the trace* (equivalently `s(2s,1)` is constant in `s` for trace `(01)^inf`, `s(2s+1,1)` constant in `s` for `(10)^inf`). That lemma plus Lemma B below closes `p = 2`. It is register **row 1** (R1's zero-set obligation), still **OPEN**.

## First paragraph: how this differs from row 33 — and where it does not

**It does not, on row 33's own question.** I did not find a descent quantity for
the stroboscopic map `y -> F^2(y)`, and I am recording that as the answer rather
than dressing something up. Row 33 measured support width and defect mass and
found them flat (`min_deepest_one` within about 20 of `depth` for every `(p,W)`
swept, "no descent"); I looked at the two natural successors and both died with
stated reasons, below (§5). Under `F^2` the support of a finite row *grows* by
exactly 2 on each side (row 31's own remark, since the extremal neighbourhoods
are `001` and `100`), so no width-shaped quantity on the stroboscopic map can
decrease at all, and the defect's leftmost one sits at exactly `A - 2 - t` —
determined, linear, carrying no information. That is the same wall row 33 hit,
reached from the other side.

**What is here instead is different in kind, not in value of a metric.** The
positive content, Lemma B, is not a numeric quantity measured over a sampled
range. It is a deterministic map on a **16-element state set** — pairs of
adjacent time-2-periodic columns, each column encoded by its two phase values —
whose full transition graph is enumerated exhaustively (all 16 states, all
transitions, all cycles, `lemma_b_output.txt`). Well-foundedness is not
"some number goes down"; it is the spatial index running leftward without bound
against the finite support of `y`. So it satisfies the strictness requirement
*as an argument shape*. What it does not satisfy is sufficiency: its hypothesis
is exactly the open obligation. Read §6 before reusing anything here.

---

## 1. Lemma A (PROVED, one line): what `p = 2` actually asks

Row 31: the lone-seed centre is eventually `p`-periodic iff some nonzero finite
row `y` on the forward orbit has `Tr_0(y) = Tr_0(F^p(y))`. Since
`Tr_0(F^p(y))_t = F^{t+p}(y)_0`, that equality *is* `c_{t+p} = c_t` for all
`t >= 0`, where `c = Tr_0(y)`. For `p = 2` the 2-periodic words are exactly
`0^inf`, `1^inf`, `(01)^inf`, `(10)^inf`. Row 25 kills `0^inf` and row 26 kills
`1^inf`, for every nonzero finite row. Hence:

> **The entire `p = 2` obligation is: no nonzero finite row has centre trace
> `(01)^inf` or `(10)^inf`.**

This is bookkeeping, not a new theorem. Its value is that it removes "eventual"
and removes `p` from the statement, and it fixes `col_0` as one of the two
nonconstant elements of `{0,1}^2` — which is exactly what Lemma B needs to avoid
its degenerate state.

## 2. Lemma B (PROVED, exhaustive over 16 states)

**Statement.** Let `y` be a row of Rule 30 in which columns `x` and `x+1` are
both exactly 2-periodic in time, and the pair of columns is not identically
zero. Then infinitely many columns `x' < x` are not identically zero, and
therefore `y` or `F(y)` has infinite support. In particular `y` is not a nonzero
finite row.

**Proof.** Encode a time-2-periodic column by `(value at even t, value at odd t)`
in `{0,1}^2`. Write `U = col_x`, `V = col_{x+1}`, `W = col_{x-1}`. Rule 30's
forward equation `U(t+1) = W(t) XOR (U(t) OR V(t))` determines `W` uniquely by
left permutivity, and `W` is again 2-periodic:

```text
W = ( u1 XOR (u0 OR v0),  u0 XOR (u1 OR v1) )
```

so the leftward derivation is the map `(U,V) |-> (W,U)` on the 16-element set
`{0,1}^2 x {0,1}^2`. `lemma_b_transduction.py` enumerates it:

* the closed form above agrees with brute-force inversion of the local rule on
  **all 16 states** (so the formula is not assumed);
* the graph has exactly **two** cycles: the fixed point `((0,0),(0,0))` and the
  2-cycle `((1,1),(0,0)) <-> ((0,0),(1,1))`. This is enumerated exhaustively,
  not by a heuristic walk: on a 16-state functional graph every transient is
  shorter than 16, so the image of the whole state set under `succ^16` is
  exactly the union of all cycles. That image has **3** states, and the two
  cycles above partition it (`1 + 2 = 3`);
* `((0,0),(0,0))` is a fixed point whose **only predecessor is itself**, so it
  is unreachable from any of the other 15 states;
* all 15 other states enter the 2-cycle, with maximum transient **3** steps;
* the 2-cycle's columns are `(1,1)` — identically 1 at every time — and `(0,0)`,
  alternating as `x` decreases.

Hence from any start state other than all-zero, every second column to the left
is identically 1, forever. `y` finite is contradicted at `t = 0`. ∎

**Exhaustiveness, stated precisely.** Over **all 16 states of
`{0,1}^2 x {0,1}^2` under the Rule 30 leftward 2-periodic transduction**. Not
over rows. Not over `p`. Not over configurations. The lemma says nothing about
whether its hypothesis is ever satisfied.

**The all-zero state is the hole in rung 1's phrasing, and it is closed by
Lemma A.** `RESULTS-ladder-rung1.md` Lemma 4 says "all 16 states reach ... the
single 2-cycle". They do not: `((0,0),(0,0))` is a second cycle and reaches
nothing. If the leftward derivation could land there, every column to the left
would be identically zero — perfectly compatible with finite support, and
Lemma B would prove nothing. It is closed here by two facts checked in the
script: all-zero has no predecessor but itself, and the start state
`(col_{-1}, col_0)` has `col_0 in {(0,1),(1,0)}` by Lemma A, so `V != (0,0)`.
All **8** admissible start states avoid the all-zero cycle. This is a repair of
a statement already in the tree, not a new lemma; I flag it because a proof
artifact inheriting the loose phrasing would be false.

**Eventual vs exact.** Lemma B needs both columns exactly 2-periodic from a
common time. Row 31 already supplies that: pass to `y = F^T(x)`, which is still
finite and nonzero, and whose trace is 2-periodic from `t = 0`.

## 3. Corollary C (PROVED, immediate)

Let `y` be a nonzero finite row with 2-periodic centre trace, and let
`Z = { x : col_x is 2-periodic in time }`. Then `0 in Z`, and:

1. `Z` contains **no two adjacent integers** (Lemma B).
2. In particular `1 notin Z` and `-1 notin Z`.
3. Writing `d_t(x) = s(t+2,x) XOR s(t,x)`, the repo's defect identity under a
   periodic centre, `d_t(-1) = (1 XOR c_t) AND d_t(1)`
   (`RESULTS-eventual-period.md`), gives `-1 in Z  <=>  d_t(1) = 0 for every
   `t` with `c_t = 0`. For a 2-periodic trace the zero-set is one parity class,
   on which 2-periodicity of `s(t,1)` is the same as constancy. So

   > `-1 in Z  <=>  s(t,1)` is constant on `{t : c_t = 0}`.

   By (2) that constancy is **false** for a counterexample row; equivalently,
   *proving* it closes `p = 2`.

So the direction of the remaining work is fixed, and it is a statement about a
single column on a single parity class of times.

## 4. The missing lemma, named

> **MISSING.** For a nonzero finite row `y` whose centre trace is `(01)^inf`,
> the sequence `rho_s = s(2s, 1)` is constant in `s`. (Mirror for `(10)^inf`:
> `s(2s+1, 1)` constant in `s`.)

Lemma A + this + Lemma B is a complete proof of the `p = 2` case of row 31's
obligation. Nothing here supplies it. It is register **row 1** — R1's zero-set
obligation, `PATH.md` §2 — specialised to `p = 2`, and sharpened from "`r` is
eventually periodic on the zero-set" to "`r` is *constant* on the zero-set",
because at `p = 2` the zero-set is a single parity class.

The one thing this document adds to `PATH.md` §2 is the *closer*. §2 discharges
the obligation by citing Jen 1990 Prop. 3 / Kopra Thm 3.5 ("column `-1`
eventually periodic closes the problem"). Lemma B closes it internally, at
`p = 2`, by a 16-state enumeration with no external citation in the trust base.
That is a change of trust base, not a change of status.

## 5. The two descent candidates I ran, and why each died

**(a) A row-25-style forced-left-half invariant class. DEAD — measured, not
proved, and the measurement is negative.** Row 25's proof works because for the
trace `0^inf` the forced left half is the checkerboard `L_k = k mod 2` beyond
one index — an eventually periodic word, hence infinite. `left_half_transducer.py`
computes the exact forced left half for the nonconstant 2-periodic traces: the
quarter-plane `x >= 1` evolves autonomously from `(R, c)`, and the left half is
then forced cell by cell by left permutivity. A round-trip self-check on 200
random genuine finite rows reproduces their true left halves exactly.

Result (`left_half_output.txt`), over **all 4096 right halves `R_1..R_12` with
zero tail, depth 200**:

| rule | trace | mean density of 1s in `L` | longest 0-run | eventually periodic within the window |
|---|---|---:|---:|---|
| 30 | `(01)^inf` | 0.4925 | 15 | 3703 / 4096 **not** periodic for any `p <= 40`; the rest almost all have preperiod 187-195, i.e. an artifact of the window end |
| 30 | `(10)^inf` | 0.5083 | 16 | 3723 / 4096 **not** periodic for any `p <= 40`, same caveat |
| 90 | `(01)^inf` | 0.3450 | 12 | **4096 / 4096** periodic, `p = 6`, preperiod = support radius exactly |
| 90 | `(10)^inf` | 0.3450 | 13 | **4096 / 4096** periodic, `p = 6`, preperiod = support radius exactly |

The forced left half for Rule 30 under a nonconstant 2-periodic trace is
structureless at density 1/2. There is no invariant class to close, so the
row-25 mechanism does not generalise off the constant traces — which is
`PATH.md` row 35's verdict reached by a different measurement, and row 27's at
radius one. Note the inversion: the mechanism *does* generalise for **Rule 90**,
cleanly and uniformly. This is a **MEASUREMENT** and falls under obstruction H;
it is a reason not to spend more on this route, never evidence for the theorem.

**(b) The left-edge co-moving window. DEAD by the §0.1 single-column filter, not
by measurement.** In the frame that tracks the leftmost 1 of a finite row, the
width-`k` window is genuinely **autonomous**: with `w_j` the cell at depth `j`,
`new_j = w_{j-2} XOR (w_{j-1} OR w_j)` (`w_{-1} = w_{-2} = 0`), because the
frame's leftward shift exactly cancels Rule 30's rightward dependence. This is a
closed finite-state system on `{0,1}^k` and it is *why* Rule 30's left side is
regular. It is also useless here, and cheaply so: the left edge is at `A - t` and
recedes from column 0 at speed 1, so no fixed-width left-edge functional ever
sees column 0. That is `PATH.md` §0.1 obstruction C applied in advance, for a few
seconds of thought and zero compute. Recording it so the next session does not
rediscover the autonomy and mistake it for a lever.

## 6. Filters

**Rule 90 filter — Lemma B FAILS it, and I am not claiming otherwise.** The
script runs the identical enumeration for Rule 90's leftward 2-periodic
transduction `W = (u1 XOR v0, u0 XOR v1)`. The graphs differ a lot — Rule 90 has
four cycles, not two, and only 3 of 16 states reach Rule 30's alternating
2-cycle — but the load-bearing property is **the same for both rules**: the only
cycle all of whose columns are identically zero is the all-zero fixed point, it
is its own only predecessor, and all 8 admissible start states avoid it. So
Lemma B's conclusion holds for Rule 90 too, and Lemma B is **not** the
Rule-30-specific step. Rule-30-specificity in the `p = 2` program enters at
Lemma A, i.e. at rows 25/26, where the Rule 90 analogue is explicitly false
(Rule 90's lone-seed centre *is* eventually `0^inf`, so Rule 90 really does have
a nonzero finite row with a 2-periodic centre trace, namely `F({0}) = {-1,1}`).
Anyone reusing Lemma B must keep row 25 in the trust base or the argument proves
a false statement. (The two graphs are structurally very different even so:
Rule 30's transduction is far from injective — the image under `succ^16` is 3
of 16 states — while Rule 90's is a **permutation** of all 16. That difference
is real; it is just not the difference Lemma B rests on.)

**The filter also fires in the reverse direction, which is the most useful
thing in this document for the next session.** §5(a)'s survey says the row-25
mechanism — "the forced left half is an infinite recognisable pattern" —
*generalises off the constant traces for Rule 90 and not for Rule 30*: under a
nonconstant 2-periodic trace, Rule 90's forced left half is eventually
`p = 6`-periodic in all 4096 cases with preperiod exactly the support radius,
while Rule 30's is structureless at density 1/2 in 90% of cases. The usual
failure mode is an argument that works for both rules; this is a mechanism that
works only for the *wrong* rule. Do not try to port row 25 to nonconstant
periods.

**Single-column filter (§0.1) — not applicable, and here is why in one
sentence.** Lemma B's hypothesis is a *predicate on named columns*
(`col_x`, `col_{x+1}` are 2-periodic), not a functional of the 2D diagram, so
the "overwrite column 0 and see if the number moves" test has no target; the
predicate is discontinuous under a density-zero modification by construction —
overwriting column 0 changes its truth value outright. The two dead candidates
in §5 are the ones the filter bites: (b) is retired by it explicitly, and (a) is
a functional of the forced left half, which is precisely why its being
structureless is a negative and not a lever.

**Obstruction H.** Every number in §5's table and every "max agreement" figure
below is a bounded computation and establishes nothing about the infinite
statement. The concrete bounded control, exhaustive over all 524,287 nonzero
rows supported in `[-9,9]` to depth 24: Rule 30 reaches 17 steps of `(01)^inf`
agreement (witness support `{-8,-1,6,9}`) and 16 of `(10)^inf`; Rule 90 reaches
11 and 10. These are falsifiers that did not fire. They are not evidence.

## 7. What a reader must not over-read

1. **`p = 2` is still OPEN.** Nothing here decides it. Row 31 stays OPEN.
2. **Lemma B is a conditional whose hypothesis is the open obligation.** It is
   not progress toward satisfying the hypothesis, and it does not show the
   hypothesis is unsatisfiable either. It converts "column `-1` is 2-periodic"
   from an obligation discharged by an external citation into one discharged by
   a 16-state enumeration. That is a trust-base improvement of a step that was
   already believed.
3. **Lemma B is not Rule-30-specific.** §6.
4. **Lemma A is bookkeeping.** The `p = 2` reduction to two trace words follows
   immediately from row 31 plus rows 25 and 26; do not cite it as new.
5. **§5(a) is measurement.** "The forced left half is structureless" is a
   negative observation over 4096 right halves at depth 200, in the same family
   as row 33's flat result and subject to the same standing instruction: do not
   extend the sweep.
6. **No descent quantity was found.** The register row for this attempt should
   record that, not the lemma.
7. The rung-1 "all 16 states" phrasing is imprecise; the corrected statement is
   in §2. Whether rung 1's own conclusions depend on the gap was **not checked
   here**. What was checked: `grep` finds only two further references to
   Lemma 4 in `RESULTS-ladder-rung1.md` (lines 260 and 275), both narrative,
   and no script under `experiments/rule30/ladder/` mentions it — so nothing
   mechanised consumes it. The phrasing should not be copied forward.

## 8. Reproduction

```sh
cd experiments/overnight-arms/frontier_attack/a2_p1_stroboscopic
uv run python lemma_b_transduction.py   > lemma_b_output.txt
uv run python left_half_transducer.py   > left_half_output.txt
```

Both are stdlib-only and import the shared substrate
`experiments/overnight-arms/common/rule30.py` read-only. Nothing outside this
directory is written. No solver, no model-provider calls, no `sorry`, no proof
artifact. Runtime: about 3 s and about 8 min respectively.

Files:

* `lemma_b_transduction.py` / `lemma_b_output.txt` — Lemma B, exhaustive over
  the 16 states, for Rule 30 and Rule 90, plus the bounded finite-row control.
* `left_half_transducer.py` / `left_half_output.txt` — exact forced left half
  under a prescribed trace, with the 200-row round-trip self-check, and the
  §5(a) survey for both rules and both phases.

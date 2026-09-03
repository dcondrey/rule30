# Pre-registration: a subinvariant (Lyapunov) weight on the RW survivor graph

Date: 2026-09-03.  Written before the first run.  Route recorded in
`ROUTE-SUBINVARIANT-CERTIFICATE.md`; this file fixes the design, the metric,
and the kill condition.

## 0. Structural fact established before the design (gate 2)

The RW survivor graph is a **DAG with out-degree one**, and this is forced, not
measured.  A state is the exact endpoint `(column, diagonal)` of
`psi_kernel.Endpoint`; every append lengthens it by one, so no state recurs and
there are no cycles among live states.  Two consequences fix the whole design:

1. Vere-Jones Criterion I and the Pavlov first-return twin
   (`ROUTE-SUBINVARIANT-CERTIFICATE.md` section 6) are **inapplicable**: they
   need returns to a distinguished state, and there are none.
2. **A finite LP with free per-state weights is vacuous.**  On a DAG,
   `w(s) = rho^depth(s)` satisfies the subinvariance inequality for every
   `rho < 1`.  Any feasible answer from that LP measures nothing.  This is
   route section 3.2's "count the legal continuations" failure wearing a
   different hat.

Therefore the test is not "is a subinvariant weight feasible" but "is one
feasible **inside a fixed finitely-described class that is bounded below**".
The restriction is the experiment; without it there is no experiment.

## 1. Target

`(RW-alpha)` (`RESULTS-RW-LINEAR-SLACK.md` section 5): some `alpha < 1` and
`n0` with no admissible `f` achieving a survivor run longer than
`alpha * n + O(1)` for `n >= n0`.

In the forced regime the continuation is deterministic, so subinvariance
collapses to a Lyapunov decrease and bounds the run directly:

```text
w(s') <= rho * w(s) on every survivor edge,  w >= 1
  =>  run length <= log w(s_0) / log(1/rho).
```

So the quantity under test is

```text
alpha_hat(n) = max over admissible sources of
                 log w(s_0) / ( n * log(1/rho) ).
```

`alpha_hat < 1` is what the route must deliver.  Nothing less is a result.

## 2. The weight class, and why each restriction is there

For a state `s` with anti-diagonal `dia(s)` of length `L`,

```text
log w(s) = sum_{k < K} x[k][dia_k(s)]  +  sum_{k >= K} a[dia_k(s)]
```

with `x[k][.] >= 0` and `a[.] >= 0`, `K` a small fixed cut (default 8).

- **`x, a >= 0` forces `w >= 1`, so `inf_s w = 1` by construction.**  This
  closes route section 3.1, the failure mode where a weight decaying along the
  growing states gives a vacuous bound.  It is imposed as a hard LP constraint
  from the first run, not checked afterwards.
- **`4K + 4` parameters is a finite description**, closing route section 3.2.
- **The tail term `a` reads every position of a growing diagonal**, and the
  windowed term `x[k]` is indexed by position rather than by a window of symbol
  values.  See section 2b for exactly which coordinate escapes the refuted
  class, and section 5 for the check that the escape is real and not nominal.
- Scale invariance: multiplying `(x, a)` by `lambda > 0` scales both
  `log w(s_0)` and `log(1/rho)` by `lambda`, so `alpha_hat` is unchanged and the
  normalisation `x, a <= 1` costs nothing.

## 2b. Exactly what the killed additive class quantified over

Capsule section 5 row 1 compresses two refutations, and a third is adjacent.
Read from the primary sources before this design was fixed:

- **Farkas, localities 1--4** (`RESULTS.md` 4, `ranking_search.py`,
  `verify_negative_certificate.py`).  Features: counts of length-`L <= 4`
  windows of the aligned four-symbol **period-two macro-frontier word**
  `q_j = (A_j, B_(j-1))`, plus bounded prefix/suffix endpoint terms.  What
  varied: coefficients of that fixed feature vector; the refutation arm is
  dual and coefficient-free, so it kills all nonnegative local weights and
  arbitrary endpoint terms at once, on 1,712 to 16,066 exact reachable macro
  transitions.  Nonnegativity is not an assumption there but a **derived normal
  form**, valid for an energy "bounded below on all finite words"
  (`RESULTS.md:142-147`); the clause named as escaping it is an energy "whose
  lower bound relies on a special reachable sublanguage".
- **Radius-seven negative cycles** (`RESULTS-CORE-DISCHARGE.md` 3,
  `core_discharge.py`).  Fixed hand-derived discharging charges on the
  factor-only de Bruijn graph of the emitted append-label word `(rho, e1, e2)`;
  a negative self-loop at `n=22` and a negative alternating two-cycle at
  `n=26`.  Nothing varied and no boundedness constraint was imposed.
- **Bellman radius two** (`RESULTS-BELLMAN-RADIUS2.md`) and **divergence**
  (`RESULTS-DIVERGENCE.md` 3): radius-2 peel words and 28 radius-`<=2`
  operator/contact counts, integer Farkas UNSAT.

Every one is strictly bounded-radius, and **none is on the RW survivor graph**.
Both source reports name the unbounded direction as surviving
(`RESULTS.md:279-281`, `RESULTS-CORE-DISCHARGE.md:107-108`).

Two coordinates therefore separate this candidate from the killed class, and
the second is the load-bearing one:

1. Position indexing plus a whole-word tail count on the anti-diagonal, not a
   count of bounded windows of symbol values.
2. **The decrease is required only on survivor edges**, a reachable
   sublanguage, which is precisely the clause `RESULTS.md:142-147` names as
   outside its normal form.

Honesty note carried forward to section 5: in *form* a symbol-count of the
diagonal word is the same shape of statistic the old class refuted, on a
different word and a different graph.  If the LP comes back feasible, that
similarity is what the section 5 check has to rule out.

## 3. The LP, per `n` and per `c in {2, 3}`

Variables `x` (`4K` of them), `a` (4), and `t = log(1/rho) >= 0`.  Maximise `t`
subject to, for every survivor edge `s -> s'` of the complete census,

```text
phi(s') . (x, a)  -  phi(s) . (x, a)  <=  -t
```

where `phi` is the position/symbol count vector above.  Constraints are
deduplicated by their difference vector.  Complete census on
`psi_kernel.Endpoint`, all `2^n` binary sources, levels `0..n+3`; nothing
sampled.

Then `alpha_hat(n) = max_{s_0} phi(s_0).(x,a) / (n * t)`, the max over sources
whose survivor path is nonempty.

## 4. Outcomes, fixed before running

**Strong outcome.**  `t > 0` at `n = 10..14`; the weight fitted at `n = 14`
satisfies every survivor edge at `n = 15, 16` **with no refit**; and
`alpha_hat(n) < 1`, flat or decreasing in `n`.

**Kill (any one fires).**

1. LP infeasible or optimal `t = 0` at any `n` in range.  The class admits no
   Lyapunov weight and the route is dead the same day.
2. `alpha_hat(n) >= 1`.  A weight exists but licenses no bound better than the
   trivial one.
3. `alpha_hat(n)` drifts upward with `n`, or the `n = 14` fit is violated by an
   edge at `n = 15, 16`.  This is the exact signature that killed the
   conditional-block route (`RESULTS-CONDITIONAL-BLOCK-LOSS.md` 4b: rate
   degrading monotonically with `n`) and the column-memory route.  A per-`n`
   weight that must be refit is not a certificate.

Kill 3 can fire on a plausible negative, which is the point.

## 5. The honesty check that decides whether a green result is new

If the fitted `a` is effectively zero, or the fitted `x[k]` are constant in `k`
beyond a small `k`, then `log w` has collapsed back into a bounded-radius
statistic and the result is inside the refuted class of capsule section 5 row 1
regardless of what the LP says.  Report the fitted vector in full and state this
verdict explicitly.  A feasible LP whose weight is bounded-radius in disguise is
reported as a **rename of a killed mechanism**, not as a result.

## 6. What a green result would and would not license

It would bound the **run length** on the forced deterministic graph, which is
the `(RW-alpha)` quantity.  It would **not** bound a survivor count, and it
would not close the count-to-run-length gap of route section 5; that gap is
about the branching source graph, a different object.  The two must not be
mixed in any write-up.

## 7. Reproduction

```sh
cd experiments/rule30/p1-period2-invariant
uv run python rw_subinvariant_lp.py --min-n 10 --max-n 14 --holdout 16
```

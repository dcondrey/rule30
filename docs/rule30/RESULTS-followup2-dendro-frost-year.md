# Dendro frost year: verification of the frost-ring / Gleichlaufigkeit spark

## Status

**KILLED**, and by algebra rather than by the pre-registered cost argument.
The pre-registered kill condition ("certifying frost years needs the same
depth the `O(log t)` wall already forbids") is directionally correct but is
not the operative failure. The construction is dead before certification
cost matters: as specified, `G_p(T)` is forced to 1 by the eventual-periodicity
hypothesis itself, for *any* choice of frost-year index set, aperiodic or
not, sparse or not. Restricting a self-comparison to a subset of times cannot
manufacture a mismatch in the *values* being compared, because both values
being compared (`c_t` and `c_{t+p}`) live on column 0, and the reductio
hypothesis already asserts they are equal for all large `t`. Frost years,
whatever they are, only ever choose *which* times get scored, never *what*
gets compared.

Code: `frost_year_probe.py`, this directory. All numbers below are its
output (`uv run python frost_year_probe.py`), reproduced inline.

## 1. Precise definitions

**OR-engagement (task's literal definition, "definition A").** At Rule 30's
update `F(x)_i = x_{i-1} XOR (x_i OR x_{i+1})`, the OR at position `i`, time
`t` "fires nontrivially" iff `NOT (x_i(t)=0 AND x_{i+1}(t)=0)`, i.e. at least
one of the two right-side inputs is 1.

For the centre column specifically (`i=0`), this reduces via the pin
identity (`PATH.md` section 1, `s(t,x)=1 => s(t,x-1) = NOT s(t+1,x)`) to two
cases:

* `c_t = 1`: the OR saturates regardless of `r_t`. Fires **unconditionally**.
  This is exactly the "pin" already proved in this repo, restated: knowing
  `c_t` alone (which the periodicity hypothesis hands you for free) certifies
  the frost year with **zero** additional lookup.
* `c_t = 0`: the OR fires iff `r_t = s(t,1) = 1`. Certifying this case
  requires knowing `r_t`, which is *not* given by the hypothesized centre
  word.

**Alternate definition ("definition B", OR differs from XOR):** fires iff
`x_i(t)=1 AND x_{i+1}(t)=1`. Under B the `c_t=1` free case disappears
entirely — every frost year needs `r_t`. Both are implemented and measured
(`or_fires_A`, `or_fires_B`); the verdict below is identical under both, so
the choice of reading does not matter to the outcome (checked, not merely
asserted — see densities table).

**Cone-certified.** For a time `t` and a hypothesized-periodic centre word,
"cone-certified" is read as: derivable from the hypothesis plus already-
established Rule 30 structure, without appeal to the unknown ground truth.
Under definition A, `c_t=1` cases are certified at cost `O(1)` (the
hypothesis itself). `c_t=0` cases require `r_t`, and the only route to `r_t`
that does not simply assume the answer is one of: (i) full forward/backward
reconstruction anchored at the true zero boundary beyond the light cone,
whose width must be `Theta(t)` (measured below, section 3, and true by the
finite-propagation-speed fact underlying the whole diagram), or (ii) an
analytic law relating `r_t` to `c_t` and `p` — which is exactly this repo's
open second target ("periodic centre implies periodic adjacent column",
`RESULTS-eventual-period.md:52-55`, "No such derivation survived the tests
below"). Neither route is `O(log t)`; (i) is worse than the wall, (ii) does
not exist.

## 2. PROVED: G_p is vacuous regardless of the frost-year index set

Write `phi_t` for the frost-year indicator (either definition) and
`F = {t : phi_t = 1}`. Define

```text
G_p(T) = #{t in F, t < T : c_t = c_{t+p}} / #{t in F, t < T}
```

**Claim.** If the reductio hypothesis holds — `c_t = c_{t+p}` for all
`t >= T0` — then for *any* `F` with `F cap [T0, infinity)` infinite,
`G_p(T) -> 1` as `T -> infinity`, independent of how sparse, aperiodic, or
Beatty-like `F` is.

**Proof.** Every mismatch `c_t != c_{t+p}` counted in the numerator's
complement must have `t < T0` (by hypothesis, no mismatches occur at or
after `T0`). So the count of mismatches inside `F cap [0,T)` is bounded by
`|F cap [0,T0)|`, a fixed finite number independent of `T`. The denominator
`|F cap [0,T)|` grows without bound as `T -> infinity` whenever `F` is
infinite. A bounded numerator-deficit over an unbounded denominator forces
the ratio to 1. `F`'s aperiodicity or sparsity never enters: it can only
change *how fast* the denominator grows, never whether the deficit is
bounded. QED.

This is the precise sense in which the spark's own text is self-undermining:
"a matching of two series, one of them off-column" is not what `G_p` computes
as specified. Both series being compared (`c_t`, `c_{t+p}`) are column 0.
The frost-year rule (`OR`-engagement, defined off column 0 via `r_t`) enters
only the *index set*, never the compared values. An off-column index set
cannot inject off-column information into a same-column comparison.

**Numeric confirmation** (`verify_vacuity`, rule-agnostic — this is an
algebra fact, not a Rule-30 fact, so the check uses a synthetic sequence, not
Rule 30 dynamics): a length-300 random prefix followed by an exactly
period-148 tail, scored only at a maximally adversarial choice of frost
years — the Beatty sequence `floor(n*sqrt(2))`, sparse (density `1/sqrt(2)`)
and aperiodic by construction, the closest available stand-in for "a
Beatty-like increasingly sparse aperiodic subset" named in the spark:

| `T` | agreements | frost years scored | `G_p(T)` |
|---:|---:|---:|---:|
| 500 | 250 | 353 | 0.708 |
| 1000 | 604 | 707 | 0.854 |
| 2000 | 1311 | 1414 | 0.927 |
| 5000 | 3432 | 3535 | 0.971 |
| 10000 | 6968 | 7071 | 0.985 |
| 20000 | 14039 | 14142 | 0.993 |

The mismatch count is exactly 103 at every checkpoint (the fixed number of
Beatty points below `T0=300`); `G_p(T) -> 1` exactly as the algebra predicts,
converging like `1 - O(1/T)`. Aperiodicity of the index set bought nothing.

## 3. Consequence for step 4 (finitely-many-certified-frost-years salvage)

The task asks whether finitely many certified frost years could suffice to
break convergence, given that unboundedly many are not certifiable within
budget. The proof in section 2 answers this directly and negatively, for a
sharper reason than a density argument: **no number of frost years — finite
or infinite, certified or not — can make `G_p(T)` fail to converge to 1**,
because eventual periodicity places no constraint whatsoever on any finite
prefix `t < T0`. A finite certified set is necessarily eventually contained
in `[T0, infinity)` for `T` large enough to matter, and past `T0` there are,
by hypothesis, no mismatches left to find. The salvage does not merely fail
for lack of certification budget; it fails because the quantity it would
spend that budget on cannot detect the thing being tested, at any budget.

The only way to make a frost-restricted comparison non-vacuous is to compare
values that are *not* both drawn from column 0 — e.g. compare `phi_t` against
its own `p`-shift, `phi_t` vs `phi_{t+p}`, which needs `r_t` and `r_{t+p}`
whenever `c_t=0`. That requires exactly "periodic centre implies periodic
(or otherwise `p`-predictable) adjacent column" — the repo's open R1 target,
not resolved here, not resolved by this spark, and not something this
construction supplies a new route to. So the honest disposition is not
"KILLED by the `O(log t)` wall" alone; it is **KILLED as literally specified
(vacuous), and its only non-vacuous repair collapses to the pre-existing open
R1 target**, which independently also faces the wall (section 1, route (ii)).

## 4. MEASURED: frost-year densities (both OR readings, both rules)

`frost_densities`, lone seed, `T=4000`, single run (deterministic, so
`n=4000` time steps is the full sample, not a subsample):

| rule | density(`c_t=1`) | density(frost, def. A) | density(frost, def. B) |
|---|---:|---:|---:|
| 30 | 0.4956 | 0.7481 | 0.2539 |
| 90 | 0.00025 | 0.0030 | 0.0 |

Rule 30's frost years are *not* sparse under either reading (75% or 25% of
all times) — the opposite of the "increasingly sparse" set the spark's
argument needs to make an aperiodicity-of-the-index-set argument bite, quite
apart from section 2's proof that it wouldn't bite regardless. Rule 90's lone
seed is genuinely eventually periodic (period 1, identically 0 for `t>=1`,
reproducing the standard fact cited in `PATH.md` section 0), so its own frost
years are correspondingly near-empty after `t=0`.

## 5. Rule 90 screen: vacuous existence-pass, but an actual filter failure once tested

Per this repo's discipline about filters that pass too easily
(`PATH.md` 0.1), a pass because "the object doesn't exist for Rule 90" is
weak and was flagged as such by the spark's own author ("there are no frost
rings [...] the fake timber is genuine because there was never a scar to
mismatch"). That framing is the wrong test. The predicate "not both
right-side inputs are 0" is defined for any rule's spacetime diagram, not
just Rule 30's; OR appearing in the *update* is irrelevant to whether the
predicate can be evaluated on Rule 90's actual diagram. So the real test is:
does the mechanism, applied verbatim to Rule 90, correctly report periodicity
(i.e. does the restricted `G_p` still go to 1)?

By section 2's proof, yes, unconditionally and for a stronger reason than in
the Rule 30 case: Rule 90's lone-seed centre column is *actually* eventually
periodic (not merely hypothesized), so for any `p` that is a multiple of its
true period, `c_t = c_{t+p}` holds with **zero** exceptions for `t>=1`, and
the restricted `G_p(T)` for any frost-year set converges to exactly 1 with no
transient at all. The construction therefore does not merely fail to exist
on Rule 90 — it actively returns the same "periodic" verdict on Rule 90 that
it would need to return on Rule 30 for the argument to work, using the exact
same machinery. That is a genuine filter failure (obstruction B), not just a
vacuous non-applicability: **the mechanism does not discriminate Rule 30 from
Rule 90 at all**, because it cannot discriminate anything — section 2 already
showed it is forced to 1 whenever the hypothesis being tested is true, on any
rule, by construction, independent of the OR term entirely.

## 6. MEASURED (subordinate, and flagged as inconclusive): certification depth

`certification_depth_scan` measures, for several `T`, the smallest simulation
half-width `R` (a hard wall forcing all cells outside `[-R,R]` to 0 at every
intermediate step) that still reproduces the true `r_T = s(T,1)`:

| `T` | true `r_T` | minimal `R` reproducing it |
|---:|---:|---:|
| 10 | 1 | 1 |
| 30 | 0 | 2 |
| 60 | 0 | 2 |
| 100 | 1 | 1 |
| 200 | 0 | 2 |

**This measurement is flagged as inconclusive, not a confirmation of bounded
depth.** A hard wall at fixed `R` is a *different* dynamical system from the
true lone-seed diagram once `R` is smaller than the true light-cone radius at
that step (it deletes material that would otherwise have flowed back in), so
finding a small `R` that happens to reproduce one particular target bit
`r_T` for one particular small `T` is not evidence of a real bounded-depth
law — it is at least partly coincidence at these small sizes, and the sample
(five values of `T`, all `<=200`) is far too small to fit a growth rate to.
It does **not** contradict, and should not be read as contradicting, the
repo's already-established and much more careful measurement of the same
question: `RESULTS-diagonal-periodicity.md` shows `r_t = E_{t-1}[t]` sits on
diagonal `t-1`, whose period `Q_{t-1}` satisfies `Q_{t-1} > t-1` throughout
the unconditionally-verified range (`j` up to 64, extending to `t` up to
`2^26` under the measured-not-proved monotonicity assumption already
qualified there) — i.e. the read time never enters that diagonal's periodic
regime, so the right-boundary route to `r_t` is stuck at the same `O(log t)`
reach as the centre column itself, and the zero-boundary route (this
document's section 1, route (i)) is `Theta(t)`, strictly worse. Both routes
to certifying a `c_t=0` frost year are therefore at or past the wall; this
section's own small-`R` numbers should be read as an unreliable proxy that
happened to land inside the true structure's slack at these sizes, not as a
finding that undercuts that conclusion.

## Verdict

**KILLED.** The primary reason is section 2's proof: `G_p(T)` as specified is
forced to 1 by the eventual-periodicity hypothesis for any frost-year index
set, so the construction cannot detect nonperiodicity regardless of
certification cost. This also disposes of step 4's salvage (section 3): no
finite or infinite certified subset changes the verdict, because the
hypothesis leaves no mismatches after its onset time for any subset to find.
The pre-registered kill condition (certification needs `O(log t)`-wall depth)
is independently true wherever the construction is repaired to be
non-vacuous (comparing `phi_t` to `phi_{t+p}` instead of `c_t` to `c_{t+p}`),
but that repair is exactly the repo's open R1 target, not something new
supplied here. The Rule 90 screen (section 5) is upgraded from a vacuous
non-existence pass to an actual demonstrated filter failure: applied
verbatim to Rule 90, the mechanism returns "periodic" correctly for the
wrong reason (it would return "periodic" for anything eventually periodic,
by construction), so rule-sensitivity claims for this construction have no
basis. Section 6's depth measurement is reported but explicitly flagged as
too small and methodologically weak to bear on the growth-rate question,
which the repo's existing diagonal-periodicity result already settles more
carefully.

## Reproduction and spending

```bash
cd experiments/overnight-arms/roundtable_followup2/dendro_frost_year
uv run python frost_year_probe.py
```

Runtime: under 10 seconds. Self-contained (no imports from other experiment
directories). Modal: **$0**. Paid model-provider calls: **$0**.

# Pre-registration: `r` on the zero set at depth 3e9

Written 2026-08-30 ~20:55 PDT, **while the run is in flight and no band data
exists**. Nothing here was chosen after seeing a number from the 3e9 band.

Object: the 9-column band `x = -4..+4` of the Rule 30 lone-seed orbit to
`t = 3e9`, produced by `modal_run_band.py` on an H100. Notation follows
`docs/rule30/PATH.md` section 4 and `a1_p1_zeroset/`: `s(t,x)` is the
space-time diagram of the single 1, `c_t = s(t,0)`, `r_t = s(t,1)`, and the
zero set is `Z = {t : c_t = 0}`.

---

## 0. What this run cannot test, stated first

The handoff calls item 3 "register row 1 / R1, a1's Lemma Z". **It is not a
test of Lemma Z, and no simulation of this orbit at any depth is.** Lemma Z is

> Let `D(t,x) = s(t+p,x) XOR s(t,x)`. If `c_t = c_{t+p}` for every `t >= t_0`,
> then `D(t,1) = 0` for every `t >= t_1` with `c_t = 0`.

Its antecedent is a global periodicity hypothesis. On the lone-seed orbit that
antecedent is *false* for every `p <= 1e9` already — that is exactly what
Wolfram's dataset establishes — and this run extends the falsification, it does
not create an instance. FINDINGS.md section 1c makes the same point against
a19. Recording it here so the write-up cannot drift into claiming otherwise.

**The agreement-window shadow does not improve either, and this is worth being
explicit about because it is the tempting substitute.** For a fixed `p`, the
longest run of `c_t = c_{t+p}` is the longest run of one symbol in a Bernoulli
sequence, `~log2 n`. **Measured, not assumed** (`agreement_runs_1e9.py` ->
`agreement_runs_1e9.json`, over Wolfram's real 1e9 centre-column bits, 37
periods log-spaced from `p=1` to `p=5e8`): longest agreement run **max 35,
median 29**, and `run / log2(n) = 0.96` on average. So the honest figure is
`~1.0 log2 n`, roughly 30 at `T = 1e9` and about 31 at `T = 3e9` -- not the
`2 log2 T` a first pass suggests. Meanwhile a1's step-0 test already
obtained agreement windows of **4000 steps, exactly, by construction**, using
finite seed *pairs* with identical centre traces rather than a self-overlap.
a1 measured 10,749 such pairs. A 31-step window is **130x weaker** than what a1
already ran, and going from `1e9` to `3e9` buys about **one extra step** of
window. Depth is the wrong axis for that object; **do not spend the band on an
agreement-window sweep.**

What depth does convert into information is below. Three hypotheses, each with
a kill condition that can fire on a plausible negative.

---

## H1 — periodicity exclusion, deterministic

**Task.** By direct inspection, exclude every transient-plus-period
`<= 3e9` for each of the 9 recorded columns.

**Metric.** For column `x` and each candidate `p`, the first `t` with
`s(t,x) != s(t+p,x)`. Exclusion for `p` = that `t` exists within the recorded
range. No statistics, no sampling: this is a scan.

**Cost note (decided in advance).** Exhausting all `p <= 3e9` for all 9 columns
is `O(T^2)` and is NOT the plan. The plan is the same inspection Wolfram's data
supports — a self-overlap scan over `p` up to the point where the *remaining*
comparison length still exceeds a stated floor. State the achieved `p` range
explicitly in the results rather than implying "all periods".

**Strong outcome.** Centre-column exclusion extended from `1e9` (Wen, WDR) to
`3e9`, plus the **first published exclusion for any column other than the
centre** at any depth. No public dataset contains a non-centre column, so
columns `+-1..+-4` have no prior art to extend; that half is new rather than
incremental.

**Kill condition.** Any column exhibits a period consistent to the end of the
recorded range. For columns `+-1..+-4` this would be a genuine finding; for
the centre column at `p <= 1e9` it would instead mean **our generator is
wrong**, since WDR already excludes that range — which is why H1 runs only
after the item-1 cross-check passes.

## H2 — `r` on the zero set against a fair coin, at 30x a19's power

**Task.** a19 found the Bayes-optimal predictor of `r_t` from left-window
history alone scores 0.4993 on `Z`, i.e. chance. That is a *null*, and a null
is only as strong as its power. This run raises the sample count on `Z` from
a19's depth to `~1.5e9`, roughly 30x the resolution in absolute bias.

**Metric.** Effect sizes, not p-values — at `n = 1.5e9` every p-value is
significant. Report, each with a bootstrap CI:
1. `P(r_t = 1 | c_t = 0)` and its deviation from `1/2`.
2. Conditional bias of `r_t` on `Z` given each fixed left-window pattern
   `s(t-1..t-m, -4..0)` for `m` up to the width the band supports.
3. The same for the *right* window `s(t, 1..4)`, which no prior arm had.

**Baseline / null.** Binomial at `p = 1/2`, `n = |Z|`; standard error at
`n = 1.5e9` is `1.3e-5`, so a 5-sigma detectable bias is `~6.5e-5`.

**Pre-declared discriminant from a19's 0.7493.** a19's above-chance number
comes entirely from *centre-column* history one step back
(`s(t,1) := NOT c_{t-1}`), which the OR-pin explains and which a19 labels a
correlation, not structure. Any result here that is a function of `c_{t-1}`
alone **is that number restated at larger `n` and will be reported as such,
not as a finding.** The only outcome that counts as new is a bias that
survives conditioning on `c_{t-1}` — i.e. present within both the
`c_{t-1} = 0` and `c_{t-1} = 1` strata separately.

**Strong outcome.** A bias `>= 6.5e-5` on `Z` surviving stratification by
`c_{t-1}`, reproduced in both halves of the run (`t < 1.5e9`, `t >= 1.5e9`)
with consistent sign.

**Kill condition (fires on the likely negative).** All stratified biases lie
within `+-6.5e-5` of zero. Then a19's null is confirmed at 30x power and this
axis is closed — **write it as a strengthened negative, do not re-run deeper.**

## H3 — the a7 `i.o.` clause, measured

**Task.** FINDINGS.md section 5 records a7's gap as: `Diff_q` infinitely often
iff `col_1(t) = 1` infinitely often where `col_0(t) = 0`. The "infinitely
often" clause is not provable by simulation, but its finite density is
measurable and has never been measured past `2e6`.

**Metric.** `d(T) = |{t < T : c_t = 0 and r_t = 1}| / T`, tabulated on a log
grid to `3e9`, with the increment per decade.

**Strong outcome.** `d(T)` bounded away from 0 with a stable increment — the
i.o. clause is then empirically overwhelming, and a7's gap is isolated to the
*proof*, not to doubt about the fact. Expected value `~0.25`.

**Kill condition.** `d(T)` decaying toward 0. That would make the i.o. clause
doubtful and would be a substantive change to a7's status.

---

## Rule 90 control — mandatory, decided in advance

Every statistic in H2 and H3 is run identically on Rule 90's lone-seed orbit at
matched depth, and reported in the same table.

This is **not** a null; it is the rule for which the outcome is already known
and adverse. FINDINGS.md section 4: Rule 90's centre column is 0 for all
`t >= 1`, so its zero set is everything, and `r_t = 1` exactly when
`t = 2^j - 1` (Kummer), verified to `T = 65536`. Its gaps double forever, so
`r` on its zero set is not eventually periodic and **R1's kill condition fires
verbatim on Rule 90**.

Consequences fixed now:
- Any statistic that behaves the same on both rules is column-blind by
  `PATH.md` 0.1's filter and carries no information about P1. It gets reported
  as failing the filter, in the a16 manner, not argued around.
- Rule 90's `Z` has `|Z| = T - 1` against Rule 30's `~T/2`, and its density of
  `{c_t=0, r_t=1}` is `~log2(T)/T -> 0` against Rule 30's expected `0.25`.
  H3 therefore *should* separate; if it does not, the statistic is wrong.
- H2's stratification by `c_{t-1}` is degenerate on Rule 90 (`c_{t-1} = 0`
  almost always). Note it rather than reporting an empty stratum as agreement.

## Sequencing, fixed now

1. Item 1 cross-check (`crosscheck_wdr.py`) must pass on the band's centre
   column against WDR at `1e9` before any of H1-H3 is computed. A statistic
   from an unverified generator is worth nothing, and the failure would be
   silent.
2. H3 then H2 then H1, cheapest first.
3. Nothing from H1-H3 enters `FINDINGS.md`, `PATH.md` or the register without
   naming which hypothesis produced it and what it does not control for.

## Charter

`docs/rule30/MODAL-COMPUTE-CHARTER.md`'s exclusion list names "regenerating
published center-column prefixes", which is precisely item 1 and part of H1.
The user authorized GPU use explicitly, overriding the charter's no-GPU
admission invariant, but **that exclusion was never formally waived.** Any
write-up of item 1 or H1 must flag the charter status in the same edit.

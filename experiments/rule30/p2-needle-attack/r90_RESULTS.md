# Rule 90 soundness control for the period-2 forced-continuation census: RESULTS

Date: 2026-09-05. Method frozen in `r90_PREREG.md`
before any Rule 90 census number was produced. Self-contained code (`r90_kernel.py`,
`r90_census.py`), zero imports from `p1-period2-invariant`.

## Verdict (calibrated)

**Outcome B did NOT fire, and Outcome A holds — but by inapplicability, not by a clean
non-vacuous distinguishing curve.** Replacing the census's carry action with any of the four
genuine Rule 90 (additive) analogues destroys Rule 30's growing-survival / bounded-`gamma`
exclusion at the **admissible tails `c ∈ {2,3}`**. No Rule 90 kernel reproduces the Rule 30
signature, so the disconfirming Outcome B (Rule 90 also giving `gamma >= 1` with a matching
bounded margin) is ruled out. The p2 needle route is therefore **not shown to be rule-blind**,
and survives the control.

Three load-bearing caveats, stated up front rather than buried:

1. **No kernel was cross-checked bit-for-bit against a Rule 90 space-time diagram, because that
   is not achievable from Rule 30 ground truth.** The Rule 30 carry action's OR is symmetric, so
   it does not record which neighbour Rule 90 drops; the census cone is not the single-seed
   antidiagonal fold, so the repo's literal bridge does not port. A *unique* Rule 90 carry kernel
   does not exist to be validated. This was handled by enumerating all four candidates (K1..K4)
   and confirming the verdict is invariant across them — the declared substitute for a unique
   validated kernel, weaker than the task's Control 1 asked for but honest about why.

2. **At admissible tails the dominant route is vacuity, which is exactly Control 3's
   pre-registered escape hatch.** The `{1,2}` / no-`11` hard-core alphabet and the high-bit-1
   constant cut are Rule-30-specific; under an additive kernel the forced continuation typically
   leaves `{1,2}` on its first symbol (all 16384 words die at depth 0 for K3/K4 at c=2). So the
   census is *intrinsically Rule-30-specific by construction* and "passes the filter trivially"
   — the pre-registered `if no faithful analogue exists, that is the finding` outcome.

3. `carry_transducer.py`'s `use_or=False` "Rule 90 control" is **mislabeled: it is bit-for-bit
   Rule 150** (`l ^ c ^ r`), not Rule 90. This is a real defect in existing code; any prior use
   of it as a Rule 90 control is void.

The non-vacuous admissible-tail signal is in section 4: for two kernels (K4 c=3 n=8, K1 c=2 n=16)
the census forces a **constant-2 hard-core endpoint to the target** (`gamma=0`) — it *finds* a
period-1 Rule 90 needle it does not exclude, the opposite of the Rule 30 verdict. It is
kernel-dependent (K2, K3 never show it) and intermittent in `n` (a linear-cone artifact), so it
corroborates the verdict without being a clean distinguishing curve.

## 1. The kernel: derivation, four-way ambiguity, and what Control 1 does/does not prove

Rule 30 carry action (`carry_action(symbol,state)`, symbol bits `(a,b)`, state bits `(c,d)`):

    c' = c ^ (a|b) = f30(l=c, {a,b})      d' = d ^ (c|a) = f30(l=d, {c,a})

a double application of `f30(l,c,r) = l ^ (c OR r)`. Rule 90 is `f90 = l ^ r`: the centre cell
vanishes. OR is symmetric, so the Rule 30 form does not record which argument of each inner `g`
is centre (dropped) vs right (kept). **Four** candidate kernels result, all permutations, all
passing forced-continuation-uniqueness pre-flight:

| kernel | c' | d' | FORWARD | collapse `[2]==[3]` | cone_local rows | cone type |
|---|---|---|---|---|---|---|
| R30 | `c^(a\|b)` | `d^(c\|a)` | `(0132)(2310)(3210)(3210)` | yes | 4 distinct | **nonlinear in left** |
| K1 | `c^a` | `d^a` | `(0123)(0123)(3210)(3210)` | yes | 2 (dep. left&1) | F2-affine |
| K2 | `c^a` | `d^c` | `(0132)(0132)(2310)(2310)` | yes | 2 (dep. left&1) | F2-affine |
| K3 | `c^b` | `d^a` | `(0123)(2301)(1032)(3210)` | no | 4 distinct | F2-affine |
| K4 | `c^b` | `d^c` | `(0132)(2310)(0132)(2310)` | no | 2 (dep. left>>1) | F2-affine |

The naive OR->XOR flip in both slots gives `(0132)(2310)(3201)(1023)` = **Rule 150** double
application (verified bit-for-bit) = `carry_transducer.py`'s `use_or=False`; excluded here.

**Control 1 (all PASS) — what it establishes:**
- (1a) The two-phase local rule reproduces a direct packed CA simulation
  `step_integer(row,mask,90) = ((row<<1)^(row>>1))&mask` applied twice, over **all 32** radius-2
  neighbourhoods, for **both** rules. This grounds the Rule 90 *local dynamics* (the given `f90`)
  against a real Rule 90 finite-row diagram.
- (1b) `use_or=False` == Rule 150, and `!=` every Rule 90 kernel.
- (1c) Fresh `FORWARD_30` / `cone_local` / `BOUNDARY` reproduce the published Rule 30 tables
  exactly, so the reimplementation is faithful.

**What Control 1 does NOT establish:** it validates `f90`, which was *given*; it does not pick
which of K1..K4 is Rule 90's carry action (finding 1 in the verdict). The `cone_local` structure
is the corroborating evidence that the candidate space is right: all four Rule 90 kernels give an
**F2-affine** cone (K1/K2 depend only on `left&1`, K4 only on `left>>1`, K3 is the full affine
XOR-shift `(0123)(2301)(1032)(3210)`), whereas Rule 30's cone is genuinely **nonlinear in
left**. Affine is the correct qualitative signature for an additive rule — it just does not
single out a member.

## 2. Control 2 — Rule 30 harness reproduction (fresh code, all 8 checkpoints PASS)

| c | n=8 | n=10 | n=12 | n=14 |
|---|---|---|---|---|
| 2 | gamma 7 (msr 3) | 7 (5) | 5 (9) | 6 (10) |
| 3 | gamma 4 (msr 6) | 5 (7) | 6 (8) | 8 (8) |

Matches `RESULTS-KSTAR-GAMMA-EXTENDED.md` exactly. The fresh census is faithful. (Control 2
covers only c=2,3 — the admissible tails; c∈{0,1} in the appendix is unvalidated territory.)

## 3. The census grid at ADMISSIBLE tails (n=8..14, brute force over `{1,2}^n`), `msr`/`gamma`

`msr = max_survival_row`, `gamma = (n+2) - msr`. Rule 30's signature: `msr` **grows** with `n`
while `gamma` stays in a **bounded moderate band** — the forced hard-core continuation dies a
bounded number of rows short of the target, so the needle is excluded.

**tail c=2**

| n | R30 | K1 | K2 | K3 | K4 |
|---|---|---|---|---|---|
| 8 | 3/7 | 8/2 | 1/9 | 0/10 | 2/8 |
| 10 | 5/7 | 6/6 | 1/11 | 2/10 | 2/10 |
| 12 | 9/5 | 4/10 | 1/13 | 1/13 | 2/12 |
| 14 | 10/6 | 2/14 | 1/15 | 0/16 | 0/16 |
| 16 | 10/8 | 18/0 | 1/17 | 2/16 | 2/16 |

**tail c=3**

| n | R30 | K1 | K2 | K3 | K4 |
|---|---|---|---|---|---|
| 8 | 6/4 | 0/10 | 0/10 | 1/9 | 10/0 |
| 10 | 7/5 | 0/12 | 0/12 | 0/12 | 9/3 |
| 12 | 8/6 | 0/14 | 0/14 | 0/14 | 5/9 |
| 14 | 8/8 | 0/16 | 0/16 | 1/15 | 1/15 |
| 16 | 10/8 | 0/18 | 0/18 | 0/18 | 14/4 |

No Rule 90 kernel reproduces R30's growing-`msr` / bounded-`gamma` band. Two anti-Rule-30 modes:
- **Vacuous:** `msr` pinned at 0..2, `gamma ~ n+2` grows (K2, K3 at both tails; K1 c=3). The
  forced continuation leaves `{1,2}` on its first symbol.
- **Intermittent full/high survival (`gamma` near 0), non-monotone in n:** K1 c=2
  (`msr` 8,6,4,2,**18**) and K4 c=3 (`msr` 10,9,5,1,**14**) are non-monotone — they jump to
  high/full survival at some n and collapse at others. This is a degeneracy of their **linear**
  cones (K1's `cone_local(l,r)=r^3(l&1)` ignores `l`'s high bit; the forced continuation is a
  linear recurrence whose hard-coreness flips with the parity of `n`), not a Rule-30-like trend.
  R30's `gamma` is bounded and smooth; these are neither.

## 4. The non-vacuous admissible-tail signal: a constant-2 Rule 90 needle, sampled

Two admissible-tail `gamma=0` cases, both forcing the **constant-2 endpoint** (all 2s — a
period-1 hard-core sequence) to the target and beyond:

    K4 c=3 n=8:  W = 11111121          forced cont = (2,2,2,2,2,2,2,2,2,2)          survived = 10 = rows
    K1 c=2 n=16: W = 1111111111111111  forced cont = (2,2,...,2)  (18 twos)         survived = 18 = rows

So for these Rule 90 kernels at admissible tails the census **does not exclude** a constant-column
(period-1) Rule 90 needle — the opposite of the Rule 30 verdict, which excludes it (`gamma>=4`
everywhere; R30's best n=8 c=2 survivor `W=11222222` forces `(1,2,1,1,...)` and dies at depth 3).
The additive kernels' cones are F2-affine, so a constant hard-core endpoint can survive; Rule
30's nonlinear cone destroys it. That is a genuine reflection of the OR-vs-additive difference at
an admissible tail.

Two honesty limits on this signal: (i) it is **kernel-dependent** — K2 and K3 never produce it
(purely vacuous), and which kernel is "the" Rule 90 carry action is unknowable (finding 1); (ii)
it is **intermittent in n** (K1's parity, K4's decay, section 3), a linear-cone artifact rather
than a sustained curve. It corroborates "the census does not exclude for Rule 90 as it does for
Rule 30" without being a clean monotone distinguishing curve.

## 5. Survival-depth distribution shape (n=14, admissible tails) — the qualitative separator

Rule 30 has a smooth heavy-tailed distribution (survivors at every depth up to `msr`); every Rule
90 kernel at admissible tails is degenerate by n=14 (all mass at 0..2):

    R30  c=2: 0:10239 1:3460 2:1586 3:713 4:252 5:77 6:36 7:15 8:2 10:4   (smooth, dies by ~10)
    R30  c=3: 0:10239 1:3461 2:1612 3:665 4:262 5:103 6:17 7:17 8:8       (smooth, dies by ~8)
    K1   c=2: 0:4096 1:4096 2:8192       K2 c=2: 0:4096 1:12288
    K3   c=2: 0:16384                    K4 c=2: 0:16384
    K1   c=3: 0:16384                    K2 c=3: 0:16384
    K3   c=3: 0:4096 1:12288             K4 c=3: 0:4096 1:12288

Rule 30's "many words die at a bounded depth short of the target" is the structure that makes the
census a nontrivial exclusion. No Rule 90 kernel has it at n=14.

## 6. Pre-flight — no kernel eliminated

All four Rule 90 kernels have permutation `FORWARD[sym]` and pass forced-continuation uniqueness
(the newest-cut map is a bijection over all prefixes to length 6). So the finding is
**behavioural**, not a degeneracy of the forcing itself: the forcing is well-defined for every
kernel, and it is the *survival* that collapses.

## 7. The survival predicate, and the task brief's mischaracterization

The no-`11` hard-core predicate was transferred unchanged to Rule 90. The task brief asserted
`RESULTS-RULE90-FILTER-ON-SPECTRAL.md` says the no-11 constraint "must not be transferred to Rule
90's XOR." **That is the opposite of what the doc says**: its table reads *"hard-core counts,
Fibonacci, `phi` | the no-`11` constraint only | RULE-BLIND"*, prose *"everything on the
Fibonacci half ... is rule-blind. Rule 90 has all of it."* The predicate was therefore
transferred on the doc's own authority — the conservative choice, giving Rule 90 the same
survival test as Rule 30, so any difference is the kernel's, not the predicate's. Note, though,
that the *vacuity* in sections 3/5 is itself evidence the `{1,2}` alphabet is Rule-30-specific:
Rule 90's forced continuations largely do not live in `{1,2}`, which is closer to "no faithful
Rule 90 analogue of the predicate exists" than to "rule-blind."

## 8. What this establishes, and what it does not

Establishes (measured, complete search over `{1,2}^n` to n=16 at the admissible tails):
- **Outcome B is ruled out.** No Rule 90 kernel gives Rule 30's growing-survival / bounded-`gamma`
  exclusion. The p2 needle/census route is not shown to be rule-blind; it is not redirected.
- The census **does not transfer to Rule 90 non-vacuously in a sustained way**: at admissible
  tails and growing n it is either vacuous (encoding mismatch, Control 3's escape hatch) or gives
  intermittent (parity-artifact) survival. Two admissible-tail cases (K4 c=3 n=8; K1 c=2 n=16)
  show the census finding a constant Rule 90 needle it does not exclude.

Does NOT establish:
- That "the bounded-margin exclusion is a property of Rule 30's OR nonlinearity and not of the
  encoding." The observed vacuity under an additive kernel is *equally* consistent with the
  encoding being Rule-30-specific; the two cannot be separated by this data. (An earlier draft
  claimed the stronger statement; it is retracted.)
- A unique Rule 90 carry kernel, or a bit-for-bit kernel/diagram cross-check (finding 1). The
  four-kernel enumeration is the substitute, and the verdict is invariant across it.
- A proof of anything (obstruction H): a finite census is a lower bound on a complexity function.
  This control shows the census does not survive the substitution non-vacuously; it does not
  prove period-2 exclusion for Rule 30.

## Appendix A — the inadmissible tail c=1 (exploratory only, NOT part of the frozen construction)

The constant cut in the RW/needle construction has **high bit forced to 1**
(`late_pull_diagonal_sat.constrain_tail`: `encoder.add(high)`), so admissible tails are exactly
`{2,3}` (`build_instance` and `constant_tail_scale.scale_extension_with_padding` both reject
`tail∉{2,3}` — "the first-infinite-tail modes are exactly 2 and 3"). `c∈{0,1}` has high bit 0 and
is **outside the construction**; Control 2 does not cover it. The numbers below are the fresh
harness run out of bounds, kept only because they are suggestive, not as evidence.

At c=1, `msr`/`gamma`: R30 gives a bounded margin (msr n-4; gamma 6,6,6,6,7,9 over n=8..18), while
K1 reaches full survival (gamma=0; at n=14, 610 words fully survive) and K4 reaches the target
(gamma 0,0,0,1,4). Read naively this says "same census, same tail, Rule 30 excludes, Rule 90
does not" — but the tail is illegal, so it is a hint about a *cell-0 constant column* (Rule 90's
lone-seed centre is identically 0), not a result. **The K1 c=1 series `msr` = 8,6,4,16,18 is
non-monotone** and is explained by K1's cone being fully linear (`cone_local(l,r) = r ^
3·(l&1)`), so its forced continuation is a linear recurrence whose hard-coreness flips with the
parity of `n`; it is a degeneracy of the K1 kernel, not a trend. Nothing in the verdict rests on
this appendix.

## 9. Reproduction

    cd experiments/rule30/p2-needle-attack
    ../../../.venv/bin/python3 r90_kernel.py           # Control 1 + kernel tables + pre-flight
    ../../../.venv/bin/python3 r90_census.py control2   # Control 2 (8 checkpoints)
    ../../../.venv/bin/python3 r90_census.py grid 8 14   # 4-kernel grid, admissible c in {2,3}
    ../../../.venv/bin/python3 r90_census.py dist 14 2   # survival-depth distributions

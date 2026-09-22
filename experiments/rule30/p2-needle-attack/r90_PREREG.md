# Pre-registration: the Rule 90 soundness control for the period-2 forced-continuation census

Date: 2026-09-05. Frozen BEFORE any Rule 90 census number was produced.
Directory: `experiments/rule30/p2-needle-attack/`, files prefixed `r90_`,
self-contained (zero imports from `p1-period2-invariant`).

## 0. Why this control exists (obstruction B / the filter)

`docs/rule30/PATH.md` section 0: *"An argument that would also apply to Rule 90 proves
nothing, whatever else it does."* Rule 90 is left-permutive and its lone-seed centre column
is identically 0 (eventually periodic), which is exactly the property the P1 program is trying
to exclude for Rule 30. Any exclusion argument that fires identically on Rule 90 is therefore
unsound.

The period-2 forced-continuation census (`max_survival_row(n)`, `gamma(n) = (n+r+2) -
max_survival_row(n)`, measured for Rule 30 to n=30 with `gamma >= 1` throughout) has **never**
been run with a Rule 90 analogue. `RESULTS-RW-LINEAR-SLACK.md` section 9.5 states verbatim:
*"The Rule 90 control was not run (no Rule 90 carry kernel in this arm)."* This prereg fixes
the method that fills that gap.

## 1. Question

The census is a **pure function of the carry action** `FORWARD` (everything downstream —
`INVERSE`, `BOUNDARY = INVERSE[3]`, `cone_local(l,r) = INVERSE[swap(l)][r]`,
`append_dependency_edge`, `literal_extension`, the hard-core survival test, `gamma`) is derived
mechanically from `FORWARD`. So the control reduces to: **replace the Rule 30 carry action with
Rule 90's and re-run the identical census.**

> Does the census's `gamma >= 1` bounded-margin behaviour survive the substitution of Rule 90's
> additive local rule for Rule 30's OR-based one? I.e. is the census measuring Rule 30's
> OR-nonlinearity, or only the encoding?

## 2. The carry action and its Rule 90 derivation (the kernel)

Rule 30 carry action (`dyadic_periodicity_analyzer.carry_action`), with symbol bits `(a,b)`
and state bits `(c,d)`:

    c' = c ^ (a | b)          d' = d ^ (c | a)          state encoded 2c'+d'

Read as a double application of the left-permutive local rule `f(l,center,right) = l ^ g(center,right)`:

    c' = f(l=c, {a,b})        d' = f(l=d, {c,a})

with `g_30 = OR`. Rule 90 is `f_90(l,c,r) = l ^ r`: the **centre cell vanishes**, `g_90` keeps
only the right argument.

**Frozen fact (established pre-registration, not a result of the census):** because OR is
symmetric, the Rule 30 kernel does **not** record which of the two arguments of each `g` is the
centre (dropped by Rule 90) and which is the right (kept). This yields a **4-way ambiguity**:

    K1: c'=c^a, d'=d^a     K2: c'=c^a, d'=d^c     (both PRESERVE FORWARD[2]==FORWARD[3])
    K3: c'=c^b, d'=d^a     K4: c'=c^b, d'=d^c     (both BREAK the collapse)

The role is **not recoverable** from Rule 30 ground truth (OR-symmetry) and the repo's literal
bridge does not port (the census cone is not the single-seed antidiagonal fold). The naive
`use_or=False` substitution in `carry_transducer.py` gives `c'=c^(a^b), d'=d^(c^a)`, which is
bit-for-bit the **Rule 150** (`l^c^r`) double application, NOT Rule 90 — it is excluded.

**Method decision, frozen:** rather than guess one kernel (a wrong kernel is worse than no
control), **enumerate all four** and report the full grid. The split of behaviour across the
collapse line (K1/K2 preserve the OR-collapse, K3/K4 break it) is itself part of the reported
result.

### Pre-flight (part of the frozen method; may eliminate kernels)

For each kernel, BEFORE any census number:
1. `FORWARD[sym]` is a permutation for every symbol (else the cone is not invertible).
2. The newest-cut map `value -> append_dependency_edge(edge, prev, value)[-1]` is a bijection
   over all reachable prefixes to length ~6 (this is exactly the `len(candidates)==1`
   forced-continuation uniqueness the census asserts).

A kernel failing either is **eliminated**. If **all four fail**, Control 3's escape hatch has
fired: no faithful Rule 90 analogue of the forcing exists, which is itself the finding (the
census is intrinsically Rule-30-specific by construction, trivially passing the filter).

## 3. The survival predicate (no-11 hard-core)

The hard-core predicate — continuation symbols in `{1,2}`, no two consecutive `1`s (including
the junction with `W[-1]`) — is **transferred unchanged** to Rule 90. Justification, on the
project's own authority: `RESULTS-RULE90-FILTER-ON-SPECTRAL.md` classifies *"hard-core counts,
Fibonacci, `phi` | the no-`11` constraint only"* as **RULE-BLIND**, and states *"everything on
the Fibonacci half ... is rule-blind. Rule 90 has all of it."* (The task brief's claim that
that doc says the no-11 constraint "must not be transferred to Rule 90's XOR" is the opposite of
what the doc says; the discrepancy is recorded and the doc's plain reading is followed.)

## 4. The census (identical to the Rule 30 arm, kernel-parameterized)

For source words `W in {1,2}^n` (all of them; the source is not itself hard-core-constrained):
build the dependency edge from `(0,)*n + W`, then force a continuation of `rows = n+r+2` rows,
each row choosing the unique `value` making the newest cut symbol `== tail`. `survived(W)` = the
first row at which the forced continuation violates hard-core; `survived = rows` if it never
does. `max_survival_row(n) = max_W survived(W)`; `gamma(n) = (n+r+2) - max_survival_row(n)`.

- Range: **n = 8..18**, `r = 0` (binding; `gamma(n,r) = gamma(n,0)+r`).
- Tails: `c ∈ {2,3}` (the Rule 30 arm's choices) **plus** `c ∈ {0,1}` and `c = 3` where the
  OR-collapse is absent and the tail choice is no longer vacuous, for K3/K4.
- Method: **brute force** over `{1,2}^n` (no dedup trie); trustworthy for a control and cheap to
  n=18.

## 5. Controls (non-negotiable)

1. **Kernel cross-check against a direct Rule 90 finite-row simulation.** The two-phase macro
   rule (`F^2` at the centre, two applications of the local rule) is validated bit-for-bit
   against a direct packed Rule 90 simulation `step_integer(row,mask,90) = ((row<<1)^(row>>1))
   &mask` over all 32 radius-2 neighbourhoods, for both rules. Plus the Rule 150 mislabel table.
2. **Rule 30 harness reproduction (fresh code).** The `r90_` census, run with the Rule 30
   kernel, must reproduce the published `gamma` at eight checkpoints:
   c=2,r=0: n=8->7, 10->7, 12->5, 14->6; c=3,r=0: n=8->4, 10->5, 12->6, 14->8.
3. **Predicate justification** (section 3).

## 6. Outcomes (frozen; `gamma ∈ [0, n+2]` by construction, so "unbounded below" is impossible)

- **STRONG OUTCOME A (expected; census is Rule-30-specific; needle route sound).**
  The Rule 90 census does **not** reproduce Rule 30's moderate-margin band. Concretely either
  - **A1** `gamma_90(n) -> 0` or small (survivors reach or nearly reach the target row): the
    census correctly **refuses** to exclude the needle for Rule 90, consistent with Rule 90's
    centre column being eventually periodic; or
  - **A2** degenerate: `max_survival_90(n)` is tiny / bounded and `gamma_90(n) ~ n+2` grows: the
    `{1,2}`/no-11 encoding is near-trivially incompatible with Rule 90's dynamics, i.e. the
    census measures an encoding mismatch, not exclusion of a real Rule 90 structure.

  Either way the behaviour and the survival-depth SHAPE differ qualitatively from Rule 30 ->
  the census is Rule-30-specific -> the p2 needle route passes the Rule 90 filter.

- **STRONG OUTCOME B (disconfirming; report loudly).** Rule 90 ALSO gives `gamma_90(n) >= 1`
  with **bounded margins comparable to Rule 30's observed 5..14 band** AND a similar
  `max_survival_row(n)` growth and survival-depth distribution. That would mean the census
  measures the ENCODING, not Rule 30's nonlinearity: the p=2 needle thread would be on the wrong
  side of the Rule 90 filter — a major negative redirecting the work.

- **Kernel-split finding.** If the outcome splits along the collapse line — K1/K2
  (collapse-preserving, OR-signature retained) behaving Rule-30-like while K3/K4 (collapse-absent,
  genuinely additive) do not — that split IS the finding: the census tracks the OR-collapse, and
  the collapse-preserving kernels are not faithful Rule 90 analogues.

## 7. Pre-registered prediction

Rule 90's lone-seed centre column is eventually periodic (identically 0) and under XOR the
genuinely-additive (collapse-absent, K3/K4) carry actions lack the OR-collapse that gives Rule
30 only three distinct left-actions. Prediction: **Outcome A** for the collapse-absent kernels.
The collapse-preserving kernels (K1/K2) retain the OR-signature and may behave Rule-30-like; if
so, that supports the kernel-split reading (the census tracks the collapse, not the rule label).

Kill condition (fires on a plausible negative): if the collapse-absent, uniqueness-passing Rule
90 kernels give a `gamma` in Rule 30's 5..14 band with matching `max_survival` growth over
n=8..18, Outcome B is declared and the needle route's filter-soundness is retracted.

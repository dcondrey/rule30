# Verification: P1 "conservation law" kill and P3 "bilinear defect" kill

Independent verification of two claims from today's roundtable (DeepSeek proposals,
Grok kills). Work done in
`experiments/overnight-arms/roundtable_followup/verify_p3_and_conservation_kills/`.
Both kills were checked by hand derivation and by direct computation; neither
was taken on say-so from either model.

## Claim 1: temporal-defect "conservation law" (Direction 5, P1)

**Verdict: KILL CONFIRMED CORRECT.** DeepSeek's identity is false. Grok's stated
correction is the true identity, but it is a tautological restatement of the
local update rule, not a new conservation law, and yields nothing salvageable.

### Hand derivation

Rule 30: `F(x)_i = x_{i-1} XOR (x_i OR x_{i+1})`. At `i=0`, with `u_{t,i} :=
(F^t x)_i` and `a_t := u_{t,0}`:

```
a_{t+1} = u_{t,-1} XOR (a_t OR u_{t,1})
        = u_{t,-1} XOR a_t XOR u_{t,1} XOR (a_t AND u_{t,1})
=> a_{t+1} XOR a_t = u_{t,-1} XOR u_{t,1} XOR (a_t AND u_{t,1})
```

This is exactly Grok's corrected formula (using the LEFT interface column
`u_{t,-1}` and the AND term `a_t AND u_{t,1}`). DeepSeek's claimed identity —
`a_{t+1} XOR a_t = u_{t,1} XOR u_{t,2} XOR (u_{t,1} AND u_{t,2})` — has the
wrong stencil on both counts: it uses `u_{t,2}` (two cells right of center)
instead of `u_{t,-1}` (one cell left), and the wrong AND term. `f_30` at site 0
only ever reads `x_{-1}, x_0, x_1`; `x_2` cannot appear.

### Computational check (`verify_defect_identity.py`)

Simulated Rule 30 from a lone seed for `T=2000` steps and checked both
formulas against direct simulation at every `t`:

- DeepSeek's identity: **fails**, first failure at `t=3`, failure rate
  993/1999 = 49.7% — indistinguishable from chance, not "identically zero".
- Grok's corrected identity: **holds exactly for all 1999 checked steps**,
  zero failures.

So the derivation-level claim in the kill is right: DeepSeek's `D_t(x)=0` is
false as written, and Grok's corrected version is the true one-step identity.

### Is anything salvageable?

Attempted the telescoping argument with the CORRECT identity. Summing over
`t=0..T-1`:

```
a_T XOR a_0 = XOR_{t=0}^{T-1} [ u_{t,-1} XOR u_{t,1} XOR (a_t AND u_{t,1}) ]
```

This is a true identity, but it is exactly the local update rule rewritten as
a telescoping sum of one-step differences — true of *any* sequence generated
by *any* recursion, with zero content beyond the definition of Rule 30 itself.
If `a_t` were eventually periodic with period `p`, the constraint "the RHS sum
over one period is 0" is automatically satisfied by construction (it just says
`a_{T+p} XOR a_T = 0`, restated via the recursion) — it is not an independent
constraint on the interface columns `u_{t,-1}, u_{t,1}` that periodicity could
fail to satisfy. It cannot be violated, so it cannot be used to derive a
contradiction from an assumed periodicity. The "strong constraint on the
interface columns' asymptotic behavior" claimed in the original proposal does
not materialize: nothing is pinned down that wasn't already implied by the
CA's own recursion.

This also explains why it passes the Rule 90 filter only vacuously: applied
to Rule 90 (whose lone-seed center column IS eventually periodic — 1 followed
by all zeros, `PATH.md` section 0 / row 5, R5), the identical telescoping
argument produces the identical content-free tautology. It doesn't
distinguish Rule 30 from Rule 90 because it doesn't say anything at all. This
is the same failure mode PATH.md's R5 already closed ("anything using only
left permutivity or [purely local, rule-generic] structure" — KILLED,
row 5): a step-by-step rewriting of the local rule cannot carry P1-relevant
information that both rules don't equally have.

**Conclusion: kill confirmed correct on the algebra; the proposal is dead, and
the corrected version, while true, is vacuous and offers no route forward.**

## Claim 2: bilinear defect accumulation (Direction 2, P3)

**Verdict: KILL CONCLUSION RIGHT, PARTIALLY WRONG REASONING.** The circularity
objection (a) is correct and is the real reason the proposal fails. The
"P1/P2 claim in disguise" objection (b) overstates the case: `|I_n|` is a
genuinely distinct two-point (pairwise) density statistic, not literally a P1
or P2 statement — but it is the same *flavor* of statistical/ergodic question
this repo's R8 route already tried and left OPEN, so it doesn't rescue
Direction 2 either. Measured `|I_n|` (MEASURED, not a proof) turns out to be
comfortably superlinear, so the Omega(n) premise itself is not in doubt; the
gap is entirely in the work-lower-bound step.

### (a) Circularity

Reconstructed DeepSeek's objects exactly to check whether the "chi as oracle
query" framing is legitimate. Exact algebraic fact (verified by hand and
re-derived independently of the Claim-1 derivation):

```
f_30(a,b,c) = a XOR (b OR c) = a XOR b XOR c XOR (b AND c)
```

so, writing `L` for Rule 150 (the LINEAR three-neighbor XOR CA,
`L(x)_i = x_{i-1} XOR x_i XOR x_{i+1}`):

```
F30(x)_i = L(x)_i XOR chi(x)_i,      chi(x)_i := x_i AND x_{i+1}
```

Since `L` is GF(2)-linear, variation of parameters gives an EXACT identity
(no approximation):

```
a_n = [L^n(e)]_0  XOR  XOR_{s=0}^{n-1} XOR_i  K_{n-1-s}(i) * chi(x^{(s)})_i
```

where `K_d(i) = [L^d(delta_0)]_i` is the Rule-150 `d`-step propagator (a
trinomial-coefficient-mod-2, Sierpinski-like fractal kernel — plausibly what
DeepSeek meant by the "Sierpinski/Pascal-mod-2 kernel", modulo the Rule
90-vs-150 mislabel). `chi(x^{(s)})_i` matches DeepSeek's `chi_{s,i}` exactly.
`verify_defect_decomposition.py` verified this decomposition reproduces
direct Rule 30 simulation EXACTLY for all `n = 1..400` (zero mismatches),
confirming this reconstruction is the right object and that the underlying
algebra in Direction 2 is not fabricated — it rests on a real, checkable
identity.

Given that, the circularity charge holds: the `chi_{s,i}` bits are not
external oracle answers an algorithm must "pay" to obtain — they are
intermediate values inside the very same Rule 30 space-time diagram that
computing `a_n` by direct simulation already produces in `O(n^2)` total time,
"for free," as a byproduct of the simulation. Pairwise linear independence of
a set of bits says nothing about the cost of *computing* them when they are
all obtainable from one shared, cheap computation (the simulation itself). To
turn "the defect field looks structured/independent" into a work lower bound
requires a genuine computational model — a circuit class, a decision-tree /
communication model with a stated adversary, or (as this repo's own R9 route
does) a fixed proof system (resolution / bounded-depth Frege) with a
well-defined derivation-length metric — not an informally-invoked "oracle
query" framing that presupposes the queries can't be answered cheaply by the
same process being measured. `experiments/rule30/proof-complexity/` (R9) is
the template for how to avoid exactly this trap: it doesn't ask "how many
independent facts does an algorithm need" in the abstract, it fixes a CNF
encoding of the light cone and measures resolution/GMUS derivation length in
that concrete system, which is why its (negative) result is meaningful. Grok
is correct that Direction 2 has no analogous fix stated, and the informal
"black-box query" framing does smuggle in the question-begging assumption
that the answer isn't already computed as a side effect.

**Verdict on (a): objection is correct.**

### (b) "P1/P2 claim in disguise"?

This is an overstatement. `I_n` is defined via `chi_{s,i} = u_{s,i} AND
u_{s,i+1}`, a joint (two-point, adjacent-cell) statistic across the full 2D
space-time diagram, restricted to the fixed, IC-independent fractal support
of the Rule-150 propagator `K`. This is not:
- a P1 statement — P1 concerns only the single column `i=0` over time, and
  `I_n` ranges over all `i` in the light cone;
- a literal P2 statement — P2 is the single-cell marginal density
  (`lim` fraction of black cells overall); `I_n` is a *pairwise* correlation
  (both `u_{s,i}` and `u_{s,i+1}` equal to 1) weighted by a specific kernel,
  which subsumes single-cell density as a degenerate special case but is not
  equal to it.

So it is a genuinely distinct combinatorial object, not literally reducible
to P1 or P2 as stated. That said, Grok's instinct is not baseless: proving
`|I_n| = Omega(n)` rigorously is exactly the kind of asymptotic-density /
mixing question that requires the same ergodic-theoretic machinery this
repo's R8 route (invariant-measure classification, `PATH.md` row 8) already
attempted and left at "CONSISTENT WITH unique ergodicity, which proves
nothing." So while not literally a disguised P1/P2 claim, it is the same
difficulty class and does not give Direction 2 any new leverage independent
of that already-open problem.

**Verdict on (b): kill's specific claim ("in disguise") is too strong / not
established as stated; the weaker claim ("same open difficulty as R8-style
density questions, no new leverage") is right.**

### (c) Measured `|I_n|` (MEASURED, not a proof of anything)

Using the exact decomposition above (validated in (a)), computed `I_n :=
{(s,i) : K_{n-1-s}(i)=1 and chi_{s,i}=1}` from a real Rule 30 simulation, for
`n` up to 2000:

| n | \|support(K)\| | \|I_n\| | \|I_n\|/support | \|I_n\|/n |
|---|---|---|---|---|
| 50 | 820 | 127 | 0.155 | 2.54 |
| 100 | 2652 | 357 | 0.135 | 3.57 |
| 200 | 8584 | 1088 | 0.127 | 5.44 |
| 400 | 27776 | 3568 | 0.129 | 8.92 |
| 800 | 89888 | 11781 | 0.131 | 14.73 |
| 1200 | 167712 | 22953 | 0.137 | 19.13 |
| 1600 | 290880 | 38627 | 0.133 | 24.14 |
| 2000 | 436160 | 52184 | 0.120 | 26.09 |

Fitted log-log slope of `|I_n|` vs `n` over these 8 points: **~1.66**
(support(K) itself grows with slope ~1.69). `|I_n|/n` is clearly growing, not
converging — `|I_n|` is not just `Omega(n)`, it appears comfortably
superlinear (~`n^1.6`–`n^1.7`) in this finite range, tracking a roughly
constant ~12-15% fraction of the kernel's support.

MEASURED ONLY: 8 data points, no seed/finite-size sweep, no error bars, and
this is a fixed IC (lone seed) with no claim about behavior at scale beyond
`n=2000`. It says nothing about whether pairwise linear independence holds
(that combinatorial claim was not tested here). It only says: the size
premise `|I_n| = Omega(n)` is not the weak point of Direction 2 — the
identity that generates `I_n` is real and its count grows superlinearly. The
weak point, per (a), is entirely in the "queries → work" translation, which
has no computational model behind it.

## Summary

| Claim | Verdict |
|---|---|
| 1. Conservation-law kill (Direction 5, P1) | **KILL CONFIRMED CORRECT.** DeepSeek's identity is algebraically false (verified by hand and by simulation: ~50% failure rate, i.e. chance level). Grok's corrected identity is true but tautological (restates the local rule); telescoping it yields no non-trivial constraint on the interface columns, and the whole class was already closed by R5's Rule 90 filter. |
| 2. Bilinear-defect kill (Direction 2, P3) | **KILL CONCLUSION RIGHT, REASONING PARTIALLY WRONG.** Circularity objection (a) is correct and decisive — treating self-generated `chi` bits as paid oracle queries begs the question; R9's fixed-proof-system approach is the legitimate alternative and has no analog here. "P1/P2 in disguise" (b) is an overstatement — `I_n` is a genuinely distinct pairwise-correlation statistic — but it inherits the same open, ergodicity-flavored difficulty as R8 and offers no new leverage regardless. `|I_n|` measured (not proved) superlinear (~n^1.6-1.7) up to n=2000, so the size premise was never the weak link. |

## Files

- `experiments/overnight-arms/roundtable_followup/verify_p3_and_conservation_kills/verify_defect_identity.py`
  — hand-derivation check for Claim 1 (DeepSeek vs. corrected identity vs.
  direct Rule 30 simulation, T=2000).
- `experiments/overnight-arms/roundtable_followup/verify_p3_and_conservation_kills/verify_defect_decomposition.py`
  — exact Rule30 = Rule150 XOR chi decomposition, verified against direct
  simulation for n=1..400 (zero mismatches), then used to measure `|I_n|` up
  to n=2000.

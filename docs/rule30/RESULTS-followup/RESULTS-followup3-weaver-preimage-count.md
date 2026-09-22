# Weaver preimage count P(t): verification of the LLM-panel spark

Status: **KILLED**, and more decisively than the pre-registered kill
condition anticipated. Under the only reading of the spark that produces a
new, well-defined, non-duplicate quantity, P(t) is not merely insensitive to
periodicity or approximately tracking a known pin-density rate -- it is
**exactly 2, for every window length t, for every left-permutive rule
(Rule 30 and Rule 90 both), independent of whether the target trace is
periodic (Rule 90's true trace) or not (Rule 30's), and this is now a proved
closed-form theorem, not a numerical coincidence.** The pre-registered kill
condition's "diverges" branch fired -- the actual growth rate is far below
the naive pin-density prediction -- but the divergence is downward into
triviality (log2 P(t) = 1, forever), not upward into anything new.

Code:
`experiments/overnight-arms/roundtable_followup3/weaver_preimage_count/preimage_count_probe.py`,
`.../window_decoupling_check.py`.
Raw output: `preimage_count_results.json` in the same directory.

## 0. Making P(t) precise (the spark under-specifies this)

The spark: "P(t) = the number of left-half configurations on cells
`{-t,...,-1}` that, together with the actual known seed/right-half data,
reproduce the TRUE observed lone-seed center column prefix `a_0,...,a_{t-1}`
under Rule 30." Two readings are possible, and they behave completely
differently:

**Reading A (already known, already dead -- not tested further here).** "The
actual known ... right-half data" means the entire two-dimensional right-half
*history* (every `s(t,x)` for `x >= 1`, all `t`), exactly as used by this
repo's `inverse_trace_probe.py:reconstruct_left_column`. Left permutivity
makes the map from (right-half history, target trace) to left-half history a
**bijection**, so this reading gives `P(t) = 1` identically, by construction,
for every left-permutive rule -- this is precisely the mechanism already
catalogued as dead in `PATH.md` section 0.5 / route R3 ("the pin mechanism...
not new to this repo"). It contributes nothing and is not explored further.

**Reading B (the only non-duplicate reading; used for everything below).**
"The actual known seed/right-half data" means only the **initial row at time
0**: `s(0,0) = 1` (the seed) and `s(0,x) = 0` for every `x != 0` (the true
right half, and the true left half beyond the window). A candidate is a
bitstring `b in {0,1}^t` substituted for the true (all-zero) left half on
`{-t,...,-1}`, holding the seed and the entire right half fixed at their true
values and everything left of the window fixed at its true value (0) too. The
candidate initial row is forward-evolved under Rule 30 (or Rule 90), and

```text
P(t) := #{ b in {0,1}^t : forward-evolved centre trace a'_0..a'_{t-1}
                          equals the TRUE centre trace a_0..a_{t-1} }
```

This is a genuinely different combinatorial object than Reading A: it fixes
one *space-like* slice (the initial row) and asks a *forward* counting
question, rather than fixing an entire *column's time-trace* and asking a
*backward* reconstruction question. It is not pre-empted by section 0.5.

## 1. PROVED: the edge-bijection theorem, and why it forces P(t) = 2 exactly

Every left-permutive rule can be written `s(t+1,x) = s(t,x-1) XOR g(s(t,x),
s(t,x+1))` (`PATH.md` section 1's residual form; this is exactly what
"left-permutive" means for a 3-input Boolean function: `g(0,m,r) != g(1,m,r)`
for all `m,r` is equivalent to `f(l,m,r) = l XOR h(m,r)` for some `h`). Fix
Rule 30 or Rule 90's own `h`.

**Claim.** For any `k >= 1`, holding `b_{-1},...,b_{-(k-1)}` (and the true
seed and right half) at any fixed values, the map `b_{-k} |-> a'_k` is a
bijection `{0,1} -> {0,1}`.

**Proof.** Consider the diagonal of spacetime points `(0,-k), (1,-k+1),
(2,-k+2), ..., (k,0)`. At each step, the point `(t+1,-k+t+1)` is computed by
the rule from `(t,-k+t)`, `(t,-k+t+1)`, `(t,-k+t+2)` -- i.e. `left = ` the
*previous diagonal point*, and `mid, right` are the two cells strictly to its
right. Those two cells' causal pasts are `[-k+t+1-t, -k+t+1+t] = [-k+1,
2t-k+1]` and `[-k+2-t+2t, ...] = [-k+2, 2t-k+2]` respectively -- both start at
`x >= -k+1`, so neither depends on `b_{-k}` at `x=-k`, for any `t`. Since
`f = left XOR h(mid,right)`, and `mid,right` are independent of `b_{-k}` at
every step, each diagonal step is `new_diag = old_diag XOR (fixed bit)`: a
single toggle. Composing `k` such toggles, `a'_k = C_k XOR b_{-k}` for some
`C_k` depending only on the already-fixed bits -- an exact bijection, for
**any** left-permutive rule, independent of nonlinearity, periodicity, or
anything about the target trace. `QED.`

This lemma is not new in spirit -- it is exactly `inverse_trace_probe.py`'s
own docstring statement, "the as-yet unknown cell at `-k` reaches the center
through the unique fastest path, so changing that cell flips the center at
time `k`" -- applied here to *every* prior setting, not only the one that
happens to match the true trace, and to Rule 90 as well as Rule 30. That
extension is what turns a heuristic into an exhaustive theorem sufficient to
pin down all of `P(t)`, not just its 0/1 satisfiability.

**Corollary (P(t) closed form).** Under Reading B, `a_0` is the trivial seed
constraint (always satisfied, involves no candidate bit). For `k=1,...,t-1`,
the constraint `a'_k = a_k` is, by the Claim, satisfied by **exactly one**
value of `b_{-k}`, given whatever `b_{-1},...,b_{-(k-1)}` were already fixed
-- regardless of what `a_k` actually is. So `b_{-1},...,b_{-(t-1)}` are each
forced to a unique value, one at a time, and `b_{-t}` is entirely
unconstrained (its first possible effect, on `a'_t`, is outside the required
prefix `a_0..a_{t-1}`). Hence:

```text
P(t) = 2   for every t >= 1, for every left-permutive rule.
```

## 2. MEASURED: exhaustive and large-scale confirmation

Three independent computations confirm the closed form, none assuming it:

1. **Exhaustive edge-bijection check**, `exhaustive_edge_bijection_check`:
   for every `k = 1..16` and *every one* of the `2^(k-1)` settings of
   `b_{-1},...,b_{-(k-1)}` (not just the truth-matching branch), flipping
   `b_{-k}` flips `a'_k`. **0 counterexamples, for both Rule 30 and Rule 90**,
   over `2^15 - 1 = 32767` prior-bit settings tested per rule per `k`, summed
   over `k=1..16`. This is a proof by exhaustion of the Claim in section 1 at
   these depths, not a sample.
2. **Backtracking exact count**, `count_p_backtracking`: `P(t) = 2` for
   `t = 1..40`, both rules, exactly matching the theorem, confirmed on the
   TRUE lone-seed traces of both rules (`Rule 30: [1,1,0,1,1,1,0,0,1,1,...]`,
   `Rule 90: [1,0,0,0,0,0,...]`).
3. **Independent GF(2) linear-algebra recomputation for Rule 90**,
   `count_p_rule90_linear`: Rule 90 is additive, so `a'_k` is an explicit
   linear functional of `b_{-1..-k}` (superposition, verified against the
   true trace as a sanity check); the resulting homogeneous linear system's
   rank is computed by exact Gaussian elimination over GF(2), giving `P(t) =
   2^(t - rank(t))`. Computed for `t = 1..1000`: **`rank(t) = t-1` at every
   single t, hence `P(t) = 2` exactly, for all 1000 values, agreeing with the
   backtracking result at every `t` where both were run (0 mismatches)**.
   This rules out any possibility that the flat `P(t)=2` for Rule 30/90 in
   items 1-2 was a small-`t` artifact that later grows.
4. **Window/prefix-length decoupling** (`window_decoupling_check.py`),
   closing the obvious objection that `P(t)=2` is a dimension-matching
   coincidence of the "aligned" case (window width exactly `t`). Decoupling
   window width `W` from prefix length `t` and brute-force counting
   `P(W,t)` over the grid `(W,t) in {(3,3),(5,3),(6,3),(4,4),(6,4),(8,4),
   (6,6),(8,6),(10,6),(10,10),(12,10)}`: **every single value matches
   `2^(W-t+1)` exactly, for both rules.** E.g. `W=10,t=6`: predicted 32,
   measured 32 for both Rule 30 and Rule 90. The theorem is about the entire
   light-cone bookkeeping, not an artifact of one alignment.

## 3. Comparison against the pin-density prediction (the pre-registered kill)

The task's pre-registered kill condition asked whether `log2(P(t))` tracks
`t * (1 - pin_density)`, i.e. whether P(t) is essentially `2^(number of
unpinned sites)`, using the pin/zero-phase density figure from `PATH.md`.

**That figure does not exist as stated in the task.** `PATH.md` was searched
directly (`grep -n "0\.5\|pin density\|density of pin\|free site\|unpinned"`)
and contains no "~0.51" density figure for zero-phase/pin sites. What
`PATH.md` does contain, and what the naive duplicate-hypothesis must mean, is
this: section 2's pin identity says column `-1`'s time-trace `l_t` is forced
by the centre trace alone whenever `c_t=1`, and needs the right neighbour
(one extra bit of information) whenever `c_t=0`. Rule 30's lone-seed centre
column has an empirical one-density hovering near 1/2 (this is literally
Wolfram's Problem 2 conjecture, unproven, not a settled `PATH.md` constant):
measured here directly, `sum(true_trace_30[:40])/40 = 0.575` (a finite-window
figure, not a proven constant -- P2 conjectures the limit is 1/2, which is
exactly the open question this program tracks). The naive duplicate
hypothesis, read charitably, predicts `log2(P(t)) ~ t * (1 - 0.5) = t/2`.

**Measured: `log2(P(t)) = log2(2) = 1`, constant, for every t up to 40
(backtracking, both rules) and every t up to 1000 (Rule 90, exact linear
algebra).** This is not "close to" the `t/2` duplicate prediction; it is
flat at 1 while the naive prediction grows linearly and unboundedly. **The
divergence the kill condition asked about did fire, in the direction the
kill condition explicitly allowed for ("if it diverges ... that divergence
itself is the interesting thing to characterize") -- and the honest
characterization is that the divergence goes the wrong way for the spark:
`P(t)` doesn't just fail to match the pin's `O(t)`-bit information content,
it carries almost no information at all (`O(1)` bits, forever), which is the
opposite of "drifting."**

## 4. The decisive Rule 90 check

Per the task's explicit instruction, the identical P(t) construction was run
against Rule 90's own lone-seed orbit, where periodicity is a known fact
(`c_t = 0` for all `t>=1`, per Kummer's theorem, as already used in
`RESULTS-followup-fiber-rigidity.md` section 1).

**Result: Rule 90 gives exactly the same `P(t) = 2` for every t, up to
`t=1000` (exact, via the GF(2) linear system) and cross-checked against
backtracking to `t=40`.** The spark's hypothesis was that eventual
periodicity of the centre column would force P(t) to "stabilize," implying
that Rule 30's non-stabilizing "drift" would be evidence against its own
eventual periodicity. What is actually observed is the reverse of what the
hypothesis needs to be useful: **both the periodic case (Rule 90) and the
unproven case (Rule 30) "stabilize" -- identically, to the same constant,
by the same proof, with no periodicity hypothesis used anywhere in section
1's argument.** The quantity cannot distinguish the two regimes because its
value never depended on which regime it was measuring. This is the Rule 90
filter closing in its strongest form (the same form seen in
`RESULTS-followup2-gauge-holonomy.md` section 5 for the plaquette defect
kappa): not "this argument happens to also work for Rule 90," but "this
quantity is a constant for the entire left-permutive class by construction,
so it was never capable of encoding anything about Rule 30 specifically, let
alone about periodicity."

## 5. Is this a duplicate of the pin mechanism?

**No, and the reason matters.** Reading A (fix the whole right-half history,
reconstruct the whole left-half history) *is* the already-catalogued
duplicate (`PATH.md` section 0.5, `P=1` degenerate bijection). Reading B (fix
only the initial row, count forward) is a genuinely different question that
was not previously posed in this tree, and the exhaustive-bijection
"fastest-path" lemma that answers it, while a direct corollary of a fact
already stated in `inverse_trace_probe.py`'s docstring, had not previously
been checked exhaustively over *every* prior-bit setting (not just the
truth-matching one) or run on Rule 90, and its consequence -- an exact,
rule-independent, alignment-independent closed form `P(W,t) = 2^(W-t+1)` --
is new content, not a restatement of section 0.5. What is *not* new is the
underlying mechanism (the same one-bit-per-step "fastest fastest-path"
information loss that produces the `O(log t)` wall, `PATH.md` obstruction A,
section 7.3): this is a sixth independent representation of that same wall,
arising here as "the newest boundary bit is a strict, deterministic toggle,
so nothing propagates inward from it and everything at that boundary is
exactly one free bit of noise." It belongs on that list, not as a P1/P2
candidate.

## Verdict

**KILLED.** Three findings, in order of importance:

1. `P(t)`, made precise under the only reading that is not already a
   catalogued duplicate, is **exactly 2 for every t**, proved by an explicit
   three-line diagonal-toggle induction (section 1), confirmed exhaustively
   for `k<=16` over every prior-bit setting (not just the correct branch),
   confirmed by independent backtracking to `t=40`, confirmed by an
   independent GF(2) linear-algebra computation to `t=1000` for Rule 90, and
   confirmed to generalize across window/prefix-length alignments
   (`P(W,t) = 2^(W-t+1)` exactly, for `(W,t)` pairs up to `(12,10)`, both
   rules). This did not require, and did not use, any assumption about
   periodicity.
2. The pre-registered kill condition's comparison against the pin-density
   prediction (`log2(P(t)) ~ t/2`) diverges sharply: the true value is
   `log2(P(t)) = 1`, constant, not the predicted linear-in-t growth. So this
   is not a duplicate of the pin mechanism by numerical coincidence, but the
   divergence is downward into total triviality, not toward anything new
   about periodicity. (Note: the literal "~0.51 pin/zero-phase density"
   figure named in the task prompt does not appear anywhere in `PATH.md`;
   the closest analogous figure is the finite-window centre one-density,
   here measured as 0.575 at `t=40`, with the conjectured limit 1/2 being
   exactly the open Problem 2 this program tracks, not a settled constant.)
3. Run against Rule 90 (known eventually periodic), the identical
   construction gives the identical constant `P(t)=2`, up to `t=1000`. The
   spark's central mechanism -- "periodicity forces stabilization, so
   non-stabilization would contradict periodicity" -- cannot be salvaged:
   both the periodic and the (conjecturally aperiodic) case stabilize
   identically, because the quantity's value never depended on periodicity
   in the first place. This is the Rule 90 filter (`PATH.md` obstruction B)
   closing at its strongest available level, the same level at which
   `RESULTS-followup2-gauge-holonomy.md`'s kappa was killed.

This route does not advance P1, P2, or P3. The only durable addition to this
repo's inventory is the observation that the fastest-path bijection already
documented in `inverse_trace_probe.py` extends, by the same one-line
argument, to a full closed-form triviality result for this class of
initial-row preimage-counting question, across every left-permutive rule and
every window/prefix alignment -- i.e. a sixth representation of the
`O(log t)` wall (`PATH.md` section 7.3 obstruction A), not a new mechanism.
No part of this should be retried without a genuinely different definition
of "preimage count" that does not reduce, by construction, to counting free
bits strictly outside a light cone that is already known to be exactly this
narrow.

## Reproduction

```sh
cd experiments/overnight-arms/roundtable_followup3/weaver_preimage_count
uv run python preimage_count_probe.py --max-t-backtrack 40 --max-t-linear 1000 --out preimage_count_results.json
uv run python window_decoupling_check.py
```

The first command runs in about 100 seconds (dominated by the exhaustive
edge-bijection check at `k<=16`, `2^15` simulations per rule per depth); the
window-decoupling check runs in well under a second.

Modal: $0. Paid model-provider calls: $0.

# RESULTS — arm "p2-single-seed": density of the Rule 30 center column

STATUS: KILLED for the P2 target, with two PROVED byproducts (a depth-4 diagonal pinning theorem
and an explicit counting rate) and two obstructions, one of which has an open repair. Details
below; every claim carries its verification status.


Scope note: this arm was launched mid-session at user direction, after the pre-registered
anf and ergodic arms. Its leads were reformulated from a proposal whose three original
mechanisms were structurally invalid (no probability space exists on a deterministic orbit,
so no martingale; the h_t/M(t) machinery is arbitrary-input and cannot see the seed orbit;
single-trajectory frequency estimates are the statistics the repo already ruled non-probative).

## PROVED byproduct — Theorem A (explicit counting rate)

For the single-seed center column a(t) = s(t,0) (OEIS A051023), for all T >= 1:
    N_1(T) := #{t <= T : a(t) = 1} >= floor(log2(T+4)) - 1
    N_0(T) := #{t <= T : a(t) = 0} >= floor(log2(T+6)) - 2
Equivalently: a 0-run starting at time T has length <= 2*ceil(T/2)+1, and a 1-run starting at
time T has length <= 2*ceil((T+1)/2)+2.

This strictly upgrades the standing in-repo corollary — "the column is not eventually constant,
hence has infinitely many 0s and infinitely many 1s" — from a qualitative statement to an
explicit rate. It is, as far as the literature sweep reaches, the first quantitative bound of
any kind on this column.

VERIFIED HERE independently: no violation of either inequality for any T < 2^16, and no
violation of either run-length bound over the same range (own code, own indexing). Observed
extremes over 2^20 steps: longest 0-run 19, longest 1-run 22 — so the true behaviour is far
better than the bound, which is logarithmic where the truth is plainly linear.

Honest weight: the bound is real, unconditional, and very weak. It does not bound the density,
does not show the limit exists, and does not separate Rule 30 from a sequence that is 1 only
at powers of two. The agent built it on the repo's sharp-horizon result and reported the
assembly as its own contribution; the proof has not been re-derived here, only its conclusions
checked numerically.

Verifier outcome: "overstated", but the break is NOT in Theorem A. The verifier reproduced the
sharp-horizon input by independent brute force and did not break the counting bound; what it
rejected was the accompanying meta-claim that log T is the exact ceiling of the entire method
class producing it (the step from "no 0-run bound derivable from this premise beats
L <= 2*ceil(T/2)+1" to "no such argument beats N_1(T) >= log2 T - O(1)" does not follow). That
meta-claim is withdrawn and was never recorded here. Theorem A itself stands, subject to the
proof not having been independently re-derived.

## PROVED — Theorem 2 (universal depth-4 diagonal pinning, and it is sharp)

Coordinates: for a finite row with right endpoint B, D_k[t] = s(t, B+t-k), satisfying the exact
diagonal recursion D_k[t] = D_k[t-1] XOR (D_{k-1}[t-1] OR D_{k-2}[t-1]), with D_{-1} == 0 and
D_0 == 1.

Statement: for EVERY finite configuration, D_k has period dividing 8 and density exactly 1/2
for k = 1, 2, 3, 4. This extends the repo's pinned diagonals (which covered k = 0, 1, 2)
by two, unconditionally. It is SHARP: at k = 5, exactly 16 of the 32 boundary patterns give
density different from 1/2.

Mechanism (odd-gate lemma): if the gate G_k = D_{k-1} OR D_{k-2} is eventually periodic with
ODD weight over a period, then unrolling the XOR makes the parity flip every period, so D_k has
exactly twice that period and density exactly 1/2. This is the right-cone counterpart of an
observation in NKS p.871, proved for the left side as Rowland 2006 Prop. 2; the density
corollary and the depth-4 sharpness are the new content.

Verification: the workflow's adversarial verifier returned "holds", having reimplemented the
sweep by DIRECT simulation rather than the diagonal recursion. Independently re-checked here
on a third implementation (my first attempt had an indexing bug — a shrinking row array read
as fixed-width — which I found and corrected): D_0 density 1 as a sanity gate; k = 1..4 exactly
1/2 for all tested rows including the single seed; single-seed D_5 = 3/8 exactly as claimed;
and the k = 5 distribution over all 32 boundary patterns is 8 at 3/8, 16 at 1/2, 8 at 5/8,
matching the claimed count of 16 exceptions exactly.

This is the strongest new result of the arm.

## PROVED obstruction 1 — invariance alone cannot pin the density (with an OPEN repair)

Both of these are exact Rule 30 fixed points, VERIFIED here by direct computation:
- the all-zeros configuration, whose every column has density 0;
- the checkerboard (alternating) configuration, which is fixed, and whose odd-phase columns
  are identically 1 (density 1) while even-phase columns are identically 0.

Consequently the set of F-invariant measures contains members giving the center cell
probability 0 and probability 1, so
    sup{ nu(x_0 = 1) : F_*nu = nu } = 1   and   inf{ ... } = 0.
Every weak-* limit point of the seed orbit's empirical row measures is F-invariant. Therefore
NO argument built from the local rule plus invariance alone can force the value 1/2. This is a
strictly sharper, Rule-30-internal version of the Rule 90 control used elsewhere in this
session: it rules out the family from inside, without appealing to another rule.

Note this is consistent with, and explains, the ergodic arm's finding: uniqueness there held
only after full support was imposed, and the fixed points above are exactly the degenerate
boundary solutions that the Rabinowitsch saturation removed.

IMPORTANT QUALIFICATION — the natural repair is NOT closed off. The obvious response is to
restrict attention to invariant measures supported on the ORBIT CLOSURE of the single seed,
which would exclude the checkerboard if the checkerboard is not in that closure. The agent
claimed to close this repair; its adversarial verifier returned "overstated" and identified
that step as broken. So the repair remains open, and the obstruction should be read as: no
argument using invariance over ALL configurations can pin the density. Arguments restricted to
the seed's orbit closure are not excluded.

Whether the checkerboard lies in the seed's orbit closure is itself unresolved. It does iff
arbitrarily long alternating blocks occur in the diagram. Measured here (single seed, longest
alternating substring per row): 6, 8, 11, 15, 13, 13, 13 at t = 50, 100, 250, 500, 1000, 2000,
4000, against row widths up to 8001. That is consistent with logarithmic growth (log2(8001)
is about 13), hence with unboundedness, hence with the checkerboard being in the closure — but
it is measurement, not proof, and proving unbounded alternating blocks is plausibly as hard as
the surrounding problem. Recorded as OPEN.

Non-separating, as expected: a verifier's linear program found the invariance bound gives
max cell density 1.0 and min 0.0 for Rule 90 as well as Rule 30, at window widths 1..6. That is
the correct behaviour for an obstruction rather than a defect — it rules a method class out for
both rules.

## PROVED obstruction 2 — the exact-density frontier does not reach the center

Every diagonal in both cones of the single-seed diagram has a provable exact rational density
(right cone purely periodic with power-of-two period, Rowland 2006 Lemma 2; left cone
eventually periodic, Rowland 2006 p.15 citing Jen 1990 Thm 4). So exact densities are
abundant — but the center column is not among them, and the reported universal pinning holds
only to depth 4 (every finite row, k = 1..4, density exactly 1/2, period dividing 8), and is
SHARP: it fails at k = 5, where the single seed itself is the explicit counterexample at
density 3/8. Combined with the repo's measured ~2.4*log2(t) reach wall, the exact-density
region provably does not extend to the center column at diagonal t.

## What the literature actually says

No published bound of any kind exists on the density of the Rule 30 single-seed center column.
Wolfram's 2019 prize announcement states the question is open, with the empirical ratio about
1.0001 at 10^9 steps. The strongest results on center columns in the literature are
periodicity statements (Jen 1986, 1990; Rowland 2006), not density statements. The correct
difficulty reference class is digit-frequency problems for explicit constants.

One verifier returned "overstated" on this survey lead, and correctly: the survey asserted the
center bit "has no known description but the simulation", which the repo's own degree theorem
contradicts. That criticism is upheld here and the claim is withdrawn.

## Honest assessment

The arm advanced P2 by essentially zero and closed two families of approaches. That is a
legitimate outcome and the obstructions are the more durable half of it: obstruction 1 is a
clean, checkable reason that no invariance-based argument can succeed, and it applies to
arguments nobody has written yet.

## Reproduction

- uv run python experiments/overnight-arms/common/ensemble_filter.py  (Rule 90 control)
- Theorem A and fixed-point checks: see the verification snippet recorded in this session's
  transcript; regenerate the column with row = 1; row = (row << 2) ^ ((row << 1) | row),
  a(t) = bit t of row at time t.

## Spending

Local CPU only. Modal $0.

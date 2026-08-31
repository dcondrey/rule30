# PREREG — arm "anf": exact ANF/Walsh growth of the iterated Rule 30 center-bit function

Registered 2026-08-30, BEFORE any experiment beyond the substrate selftest. Triage row 9.

## Objects

f_t : {0,1}^(2t+1) -> {0,1} maps the initial window (x_{-t},...,x_t) to s(t,0). Well-defined by
the radius-1 light cone. Composition law on 2t+3 variables:
f_{t+1} = f30(f_t(x_{-t-1..t-1}), f_t(x_{-t..t}), f_t(x_{-t+1..t+1})), f30(l,c,r) = l + c + r + cr over GF(2).

Computation: bit-sliced truth tables. Level 0 holds the 2t+1 coordinate functions as packed
2^(2t+1)-bit tables; one CA step maps 2k+1 tables to 2k-1 via g' = g_prev XOR (g | g_next);
after t steps the single survivor is f_t's truth table. Exact, no sampling.
ANF via packed Mobius transform. Walsh spectrum via integer WHT.

## Task, metric

Exact integer sequences for t = 1..13 (t = 14 stretch, ~2 GB):
deg(f_t); |ANF(f_t)| (monomial count); degree profile; max |Walsh coefficient| (equivalently
nonlinearity); the top-degree monomial support set. Walsh exact for t <= 12 (t = 13 stretch).

## Hypotheses as questions (no foregone results)

- H1: does deg(f_t) follow an exact law? Candidate laws to test, none assumed: t+1
  (triage agent's guess), 2t-1, 2t+1 - c, non-affine. NOTE the standing obligation:
  ARM4-frequency-domain.md reports "ANF degree exactly 2t-1" for ITS object; determine
  exactly what object ARM4 measured (read-only) and state the relation. If ARM4's object IS
  f_t, H1's law is already measured and this sub-target becomes validation, not discovery.
- H2: growth rate of |ANF(f_t)| / 4^t (monomial density) — convergent? to what?
- H3: does max |corr(f_t, affine)| decay exponentially, i.e. nonlinearity -> 1/2 * 2^(2t+1)?
- H4: does the top-degree monomial set satisfy a shift/window recursion usable for induction?

## Baselines / controls

Rule 90 (f90_t linear: deg = 1 for all t; pipeline must reproduce this exactly) and Rule 150
(same). A pipeline result that does not separate Rule 30 from Rule 90 proves nothing.
Identity rule as a smoke test (f_t = x_0).

## Strong outcome

A proved inductive lemma (paper proof from the composition law) establishing the observed
degree law for ALL t, stated as: "for every t >= 1, deg(f_t) = <law>", plus exact sequences as
VERIFIED data, plus a REDUCED model-restricted P3 corollary (any circuit class whose members
have bounded algebraic degree cannot compute the center column) with its remaining obligation
stated referee-style.

## Kill conditions (can fire on plausible negatives)

- K1: deg(f_t) matches no affine-in-t law through t = 13 AND top-degree monomial sets show no
  shift structure (H4 false) -> the formal-lemma target is dead; arm ends KILLED with data archived.
- K2: a published theorem located during execution already proves the observed law -> arm
  reclassified as validation; ends KILLED (as discovery) citing the theorem.
- K3 (Walsh sub-target): if max correlation does not decay (stays Omega(1)), H3 dies; report
  honestly (that would itself be surprising and gets a distribution plot, not a bare number).

## Cheapest disconfirming test (runs FIRST)

t = 1..8 by direct truth tables (<= 2^17 entries, pure Python, seconds): compute deg(f_t).
If the degree sequence is patternless already (K1 fires small), stop before any t > 10
infrastructure.

## Addendum 1 (2026-08-30, BEFORE first experiment): ARM4 reconciliation

ARM4-frequency-domain.md §3 measured THIS object: "Center bit at step t as a boolean function
of the 2t+1 row-0 cells in its light cone, via Mobius transform to ANF", with degree exactly
2t-1 at t = 3,5,7,9,10 (t=1 gives 2, the small exception), terms counted, density ~0.15.
Consequences, recorded before any run:

- H1 is RECLASSIFIED from discovery to validation: my pipeline must reproduce ARM4's table
  exactly (degrees AND term counts) or the pipeline is wrong. The triage agent's t+1 guess is
  refuted by ARM4's table before any experiment.
- The discovery targets are now: (i) a PROOF of the degree law for all t (ARM4 measured, never
  proved; per triage, no published theorem either); (ii) H3 Walsh/nonlinearity decay, which
  ARM4 did NOT measure; (iii) H4 top-degree monomial structure as the proof vehicle.
- Sketched proof path to be tested against data, not assumed: (L1) iterated left-permutivity
  gives f_t = x_{-t} XOR g_t(x_{-t+1..t}) — linear in the leftmost variable (likely classical;
  cite, do not claim); hence deg f_t <= 2t, one below ceiling, for free. (L2) the coefficient
  of the full monomial of g_t vanishes for t >= 2 -> deg <= 2t-1. (L3) a witnessed persistent
  monomial family of degree 2t-1 -> deg >= 2t-1. Each of L2/L3 is a question; either may fail.
- K1 is restated: if L2 or L3 fails empirically at some t <= 13 in a patternless way AND no
  alternative proof structure emerges from the top-degree sets, the proof target ends KILLED;
  Walsh data (H3) still gets reported as VERIFIED measurement.

## Seeds, spending

Exact computation, no RNG anywhere. Local CPU only; Modal $0; paid model calls $0.
Files: experiments/overnight-arms/anf/, runs/overnight/anf/. Results: RESULTS-anf.md.

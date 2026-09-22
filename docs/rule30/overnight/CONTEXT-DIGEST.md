# Overnight context digest (compiled 2026-08-30, read-only survey of docs/rule30/*.md)

Purpose: settled-knowledge map for the overnight arms. Everything here is a summary of
existing repo docs; nothing in this file is a new claim. Cite the source doc, not this file,
in any RESULTS write-up.

## Arm status (existing arms, do not duplicate)

| Arm | Technique | Status | Open edge |
|---|---|---|---|
| Arm 1 | Lean/search at P1 | NOT RUN (not pre-registerable) | the theorem itself |
| Arm 2 | invariant measures for P2 | NOT RUN as discovery; Hedlund 1969 surjectivity => uniform Bernoulli invariant, a.e. density 1/2 | lone-1 IC is measure zero; asymptotic density undecidable from finite prefix |
| Arm 3 | computational-effort tournament | Ran; alpha-hat 1.9980 baseline, 1.9676 bit-parallel; no exponent improvement | decision bands n>=10^6 not yet enforced |
| Arm 4 | frequency-domain/AIR shortcut | Phase 0 disconfirmed premise: BM linear complexity maximal through 16384; ANF degree exactly 2t-1; density ~0.15 | excludes only the proposed low-degree shortcut, not nonlinear/higher-degree ones |
| Arm 5 | Rule 150 + sparse-error superposition | CLOSED: N_eff ~ n^1.68 (omega(n)); all parity cancellations at 1/2 | none claimed (geometric grammar over E "not ruled out in principle") |
| Arm 6 | 2-kernel / automaticity probe | Both kills fired: >=8191 distinct residuals depth 12; GF(2) rank 512 at depth 9 | NOT a proof of non-automaticity; proof needs residuals distinct at arbitrary depth |
| Arm 7 | dyadic spacetime tile grammar | Diagnostic structure, not a shortcut; DAG exponent 1.367 rising ~1.48; perimeter determines interior but carries Theta(scale) bits | five-point candidate contract (bounded state + exact doubling) is the acceptance gate |
| Arm 8 | center-observational quotient (ROBDD) | Exponential ~1.88/step in all 5 tested variable orders | only 5 fixed orders excluded, arbitrary-input F_h; single-seed-orbit restriction + exact doubling untried |

## Proved (in-repo, citable as settled)

- Zero-tail theorem (RESULTS-zero-tail.md, endorsed): no nonzero finitely supported config
  has identically zero center trace. Full fiber classification via one-state prefix-OR transducer.
- Triangular uniqueness ("Lemma 1 of the note"): right half + desired trace determine at most
  one left half (left permutivity, extreme path).
- All-one trace fiber = checkerboard left half (L_k = 1 iff k positive even); infinitely many ones,
  so every eventually CONSTANT lone-seed center is excluded.
- Same-forward-orbit collision reduction: eventually p-periodic center iff some nonzero finite y
  on the orbit has Tr_0(y) = Tr_0(F^p(y)); remaining obligation is Tr_0(y) != Tr_0(F^p(y)) always.
- Pinned right-cone diagonals: s(t,B+t)=1; s(t,B+t-1)=a(B-1) XOR t mod 2; s(t,B+t-2)=a(B-2) XOR t mod 2.
- Zero-set reduction + parity-checked survivor map closed form (alt-trace file; OFF-LIMITS territory).
- OR-latch pin identity s(t,x)=1 => s(t,x-1) = NOT s(t+1,x); fails for Rule 90 (the separator table
  30/45 pin on c=1, 75 on c=0, 60 both, 90/150/105 none).
- Right-diagonal power-of-two pure periodicity = Rowland 2006 Lemma 2 (re-derived, KNOWN, not a
  contribution; period sequence OEIS A094605).

## Dead ends (do not retry, do not re-measure)

prefix-OR latch through zero phases (FALSIFIED); two-zero-phase mirror symmetry (FALSIFIED);
periodic-mask contraction (FALSIFIED for any period word containing a zero); run-of-ones wedge
descent (PROVED dead); cascade descent (killed by own kill condition, 1.14% cells, zero at x>=+1);
trace-anchored O(log t) propagation (three independent representations all hit ~2.4 log2(t) reach;
any route must say why it beats O(log t)); right-boundary anchoring (closed, exponential gap);
left-permutivity/expansivity alone (closed by Rule 90); constant-trace mechanism does not extend
to nonconstant traces; bridge families (nonlinear left-permutive class, finite-delay observability,
center-trace injectivity, doubling separation s(p,0)!=s(2p,0) fails at p=4); low-degree/FFT shortcut
(no 2^m-th roots of unity in GF(2^k); composition squares degree); N_eff ~ n^1.68 sparsity route;
recompression, axial periodicity, dihedral quotients (ARM7); truncated GF(2)[x]/(x^k) transfer monoid
(dies n=5); truncated carry-polynomial matrix (dies n=2); row-parity cancellation; finite 2-kernel
automaton; left-permutive affine boundary map; inverse-diagonal transfer matrix.

## Notation (use consistently)

- Rule: s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1)); GF(2): l + c + r + c*r, degree 2, left-permutive.
- Orientation: position increases rightward; ordered boundary LEFT, chaos RIGHT (repo-pinned).
- Center column ground truth: OEIS A051023 via experiments/rule30/center_column.py (READ-ONLY).
- Trace Tr_0(x)_t = F^t(x)_0; c_t = s(t,0), r_t = s(t,1), l_t = s(t,-1); l_t = c_{t+1} XOR (c_t OR r_t).
- R_j = a(j), L_k = a(-k); support radius w; left depth d; right endpoint B; H(p,w) horizon table.
- Two diagonal indexings exist (D_k[t] = s(t,t-k) vs E_j[t] = s(t,B+t-j)); any new doc must say which.
- Status labels: PROVED / VERIFIED / KNOWN, re-derived / EXACT COMPUTATION / FALSIFIED / KILLED / OPEN.
- Rule 90 is the standing adversarial control: an argument that also applies to Rule 90 proves nothing.

## Constraints inherited by overnight arms

- ARM6 boundary language: finite computations are NOT proof of non-automaticity; Salon-style
  diagonal-of-automatic-double-sequence arguments were marked unavailable on ARM6's strength
  (cite ARM6's own narrow phrasing, not the stronger Verdict paraphrase elsewhere).
- SMT: no FiniteField sort in z3 4.16.0 here; GF(2^k) only via bitvectors and it collapses n_max
  to low tens; verification stays in GF(2); induction over unbounded rows is not an SMT query.
- Spending discipline: every RESULTS file carries Reproduction + spending lines; Modal charter
  caps paid compute; overnight arms use local CPU only.

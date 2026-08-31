# Triage: four proposed "novel framework" arms (2026-08-30)

**Verdict: 4 closed, 0 promoted. No agent was spawned to build a proof, and no
`NOVEL_PROOF_DRAFT.md` exists, because no proof exists.** The exit condition of
the requesting prompt cannot fire; the four reasons are below, two of them
measured here rather than asserted.

Method follows `PATH.md` section 0.1, which requires a proposed quantity to be
run through the single-column sensitivity filter *before anything is built on
it*. Two arms had a computable statistic and were run through the existing
discriminator harness pattern. Two are closed by standard theory at zero
compute. Scope: everything written by this arm is under
`experiments/overnight-arms/novel_frameworks/` and `runs/overnight/novel_frameworks/`;
nothing under `experiments/rule30/` or `docs/rule30/` was modified.

Probe: `triage_probe.py`. Data: `runs/overnight/novel_frameworks/{a2,a3,a4}.json`.
Reproduction: `uv run python experiments/overnight-arms/novel_frameworks/triage_probe.py`.
Spending: local CPU only. Modal $0. Paid compute $0.

---

## A1 — Drinfeld modules / arithmetic dynamics over F_2(z), for P1

**CLOSED, no compute needed. Three independent reasons.**

1. **The framework requires the additivity Rule 30 does not have, and the rules
   that do have it are the ones where P1 is false.** A Drinfeld module over an
   A-field K is a ring homomorphism phi: A -> K{tau} with
   `phi_T = gamma(T) + c_1 tau + ... + c_r tau^r`, `c_r != 0`, where K{tau} is
   the twisted polynomial ring with `tau b = b^q tau`; the map
   `sum s_i tau^i |-> sum s_i x^(q^i)` identifies K{tau} with the F_q-*linear*
   polynomials under composition, equivalently with `End_K(G_a)`, the
   endomorphisms of the additive group scheme. Additivity is therefore
   definitional, not incidental. (Precision, checked: F_q-linear is *strictly
   stronger* than additive whenever `q != p` -- additive polynomials in
   characteristic p are `sum a_i x^(p^i)`, F_q-linear ones are
   `sum a_i x^(q^i)` -- so the definition demands more than additivity, not
   less. For the case at hand, `q = p = 2`, the two coincide.)

   Rule 30 is `l + c + r + c*r` over GF(2): degree 2, and **measured
   non-additive on 62,430 of 65,536 pairs at width 8** (V1). Rule 90 is
   `l + r`: additive, **zero violations on the same 65,536 pairs**, and its
   lone-seed centre column *is* eventually periodic. So the exact class of ECAs
   that admits this formulation is the class where the desired conclusion
   fails. This is `PATH.md` obstruction **B** (the Rule 90 filter) in its
   sharpest form: not "the argument happens to also apply to Rule 90", but
   "the argument's hypothesis is Rule 90's defining property".

   There is no non-additive variant of the theory to retreat to, and the reason
   is structural rather than a gap in the literature: `phi_a` is required to be
   an endomorphism of `G_a`, and `End_K(G_a)` *is* the ring of additive
   polynomials, so a non-additive `phi_T` is not a variant of Drinfeld module
   theory but a different object. Every recognized generalization keeps
   additivity (Anderson t-modules use matrices of additive polynomials over
   `G_a^n`).
2. **Already-occupied territory.** A column of the spacetime diagram of an
   F_q-linear cellular automaton (characteristic p, any memory `d >= 1`, any
   radius) begun from initial rows eventually periodic in both directions is
   p-automatic: Litow-Dumas, Theoret. Comput. Sci. 119(2):345-354 (1993) for
   finitely-supported initial conditions, and Rowland-Yassawi, "A
   characterization of p-automatic sequences as columns of linear cellular
   automata", Adv. Appl. Math. 63:68-89 (2015), doi:10.1016/j.aam.2014.10.002,
   Theorem 3.1. Conversely every p-automatic sequence over F_q arises this way
   from a linear CA **with memory**, which is the exact characterization
   (ibid., Theorem 1.1 / 3.3). That is TRIAGE row 8's closest prior work. An
   arithmetic-geometry re-encoding of the additive case adds nothing to that
   line, and the nonlinear case is the open problem the line does not reach.

   Three corrections to the wording an earlier draft of this file used, and
   which `overnight/TRIAGE.md` row 8 also uses ("columns of LINEAR CA are
   exactly p-automatic"): the field is F_q, not F_p; the "exactly" (iff)
   direction holds only for CA **with memory** `d`, and is false for classical
   memory-1 linear CA -- Rowland-Yassawi's own Corollary 3.5 gets a genuine
   memory-1 column but the remark following it says "the cellular automaton
   constructed in Corollary 3.5 is not linear"; and the easy direction, which
   is the one this triage actually needs, is credited by Rowland-Yassawi
   themselves to Litow-Dumas. Proposed as a correction to TRIAGE row 8's
   phrasing; that file was not edited.
3. **The proposed conclusion is column-blind and, in its true form, already
   known.** A non-torsion (infinite-order) point gives aperiodicity of the
   *orbit*. The lone-seed orbit is trivially aperiodic already: the support
   grows by one cell per step, so no two rows are equal, no compute required.
   P1 asks about one column, a density-zero subset of the diagram
   (obstruction **C**). Infinite orbit order does not constrain a single
   column: Rule 90's orbit is likewise aperiodic while its centre column is
   eventually zero.

## A2 — Optimal transport, W_1(mu_t, uniform), for P2

**CLOSED. The hypothesis is false analytically, false empirically, and the
statistic is column-blind by measurement.**

The prompt's hypothesis has two readings and each dies separately: an
operator-level claim (`W_1` contracts under the Rule 30 map, closed by (i);
note `delta_0` is not on the single-seed orbit, so (i) alone does not close the
narrow reading) and an orbit-level claim (`W_1` between the time-averaged
single-seed orbit and uniform contracts, closed by (ii)).

**(i) No strict contraction exists on the space of measures.** The all-zero configuration is a fixed
point of Rule 30 (`000 -> 0`), so `delta_0` is F-invariant and
`W_1(F_* delta_0, uniform) = W_1(delta_0, uniform) = 2.5` for k=5 blocks under
Hamming cost (measured, `a2.json`). A map on measures with two distinct
invariant measures admits no strict contraction toward one of them. "Strictly
contracts under the Rule 30 map" is refuted in one line.

**(ii) The empirical single-seed curve does not contract either.**
`W_1(mu_t, uniform)` for the lone-seed orbit, k=5 blocks, W=256, sampled every
20 steps to t=500. The W=256 window is only fully inside the light cone for
`t >= 128`, and below that the histogram is dominated by all-zero blocks
outside the cone (the curve starts at 2.28, near the `delta_0` value 2.5, and
falls); that early decay is a cone-filling artifact and is discarded.
**Restricted to the filled regime `t >= 130`: 8 of the 18 consecutive steps
increase**, including 0.141 -> 0.389 at t=310 -> 330 and 0.142 -> 0.211 at
t=430 -> 450. All 8 increases survive the restriction. Not monotone, so not
even a weak empirical contraction.

**(iii) It is column-blind — the measured trap.** Discriminator fields:
A = Rule 30 lone seed; B = A with column 0 overwritten by `0101...` (P1's
answer flips, nothing else changes); C = Rule 90 lone seed.

| W | W1(A) | W1(B) | W1(C) | rel A-B | rel A-C | col-0 control A-B |
|---|---|---|---|---|---|---|
| 32 | 0.5478 | 0.5284 | 2.4122 | 3.54% | 340% | 95.6% |
| 64 | 0.3496 | 0.3573 | 2.3845 | 2.20% | 582% | 95.6% |
| 128 | 0.2509 | 0.2543 | 2.3516 | 1.36% | 837% | 95.6% |
| 256 | 0.1859 | 0.1850 | 2.3490 | 0.50% | 1163% | 95.6% |

`rel(A,B) * W` = 1.13, 1.41, 1.74, 1.28 across the four windows: flat, i.e.
the separation is `O(1/W)` and vanishes.

Re-run at higher resolution to check that the flatness is not sampling noise
(T=600, 40 sampled rows per window, W extended to 512;
`runs/overnight/novel_frameworks/a2_highres.json`):

| W | 32 | 64 | 128 | 256 | 512 |
|---|---|---|---|---|---|
| rel(A,B) | 3.94% | 0.073% | 0.74% | 0.17% | 0.098% |
| rel(A,B)·W | 1.26 | 0.047 | 0.94 | 0.44 | 0.50 |
| rel(A,C) | 326% | 537% | 838% | 1237% | **1621%** |

`rel(A,B)·W` does not grow; with more samples the column-0 separation falls
below 0.2% from W=256 on, so `O(1/W)` is if anything generous. Meanwhile the statistic separates
Rule 30 from Rule 90 by **1163%** at W=256 and the positive control that reads
column 0 moves by 95.6%. This is `GEOMETRIC-TRIAGE.md`'s recorded lesson
reproduced on a fourth statistic: **rule-sensitivity is not evidence of
P1/P2-relevance.** Had only the Rule 90 comparison been run, this arm would
have shown a false green light.

**(iv) The only non-column-blind variant is circular.** Taking `mu_t` over
blocks *of column 0* rather than of the row makes the statistic column-aware,
but `W_1(mu_t, uniform) -> 0` for that measure *is* the equidistribution
statement P2 asks for. Same circularity as obstruction **E** / TRIAGE row 6.

## A3 — Tensor-network temporal-cut bond dimension, for P3

**CLOSED. The proposed cut is degenerate; the non-degenerate cut is exactly
ARM8's ROBDD width, re-derived here; and obstruction G blocks the transfer to
P3 either way.**

All four statements below are computed in `verify_crossrefs.py`
(`runs/overnight/novel_frameworks/verify_crossrefs.json`), not asserted.

* **The lone seed makes every bond trivial.** The input set is a singleton, so
  the tensor across any cut has one row and rank **1 at every cut, at every
  depth through d=12** (`a3.json`). This is TRIAGE row 2's kill verbatim --
  "single-seed basis-state input through a permutation circuit has center-cut
  entropy identically 0" -- restated in tensor-network language. A bond
  dimension of 1 supports no lower bound on anything.
* **The HORIZONTAL (temporal) cut named in the proposal is degenerate even for
  arbitrary inputs.** The network's output is a single bit, so the tensor above
  the cut is a map into `{0,1}` and the minimal exact bond is **at most 2**;
  measured exactly 2 at h = 2, 4, 6 (V4). Real-valued SVD as the prompt
  specifies would return a numerical rank of a matrix whose exact rank is 2.
* **The non-degenerate cut is the VERTICAL one, and it is ARM8's quantity, now
  re-derived independently.** Minimal exact bond dimension across a cut in a
  variable order is the Myhill-Nerode residual count of `F_h`, i.e. ROBDD
  width. Computed from scratch here in right-to-left order:

  | horizon h | max width | reachable nodes | ARM8's table |
  |---:|---:|---:|---|
  | 2 | 2 | 7 | 2 / 7 |
  | 4 | 7 | 28 | 7 / 28 |
  | 6 | 24 | 105 | 24 / 105 |
  | 8 | 92 | 405 | 92 / 405 |

  Exact agreement on both columns at all four horizons, so the identification
  is verified rather than asserted, and the tensor-network framing **is** the
  ARM8 probe in different vocabulary. ARM8's own boundary applies unchanged:
  it excludes five fixed variable orders for the arbitrary-input `F_h`.
* **Correction to an earlier draft of this file.** It also cited ARM6's "GF(2)
  rank 512 at depth 9" as the same family of quantity. That is wrong and the
  claim is withdrawn: ARM6 measures the 2-kernel of the centre *sequence*
  `a(n)` under the decimations `n -> 2n, 2n+1` and the GF(2) rank of its
  residual-prefix matrix, which is not a cut rank of the space-time lightcone.
  Only the ARM8 identification stands.
* **Even an exponential bond does not reach P3.** Obstruction **G**: P3 fixes
  the configuration to the lone seed and varies only the index n; measures of a
  function over its whole domain of variable inputs carry no implication for
  the cost of one evaluation. Rows 63-66 died on exactly this, and rows 20/43
  are scope-bounded by it. The reachable-image counts reported in `a3.json`
  (5, 26, 106, 455, 1882, 7710, 31395, 127110, 512906 at the first cut for
  d = 1..9, ratio ~4.03 per unit depth) are a count of distinct reachable
  *states*, which is a third quantity again, neither the bond dimension nor
  ARM8's width; they are retained as data, and nothing in the verdict rests on
  them.

## A4 — S-adic morphisms and Morse-Hedlund p(n) > n, for P1

**CLOSED. Vacuous as specified.**

Morse-Hedlund states: an infinite word is eventually periodic **iff p(n) <= n
for *some* n**. A word of eventual period q satisfies `p(n) <= q + preperiod`
for all n, so verifying `p(n) > n` on a finite range `n <= 64` excludes only
eventual periods in roughly that range and says nothing about larger ones.

Measured on a 200,000-bit centre-column prefix: `p(n) > n` for every
`n <= 64`, with no exception (`a4.json`). Sample: p(1)=2, p(2)=4, p(3)=8,
p(4)=16, p(8)=256 (all blocks realized), p(16)=62,377. From about n=32 the
count is **prefix-limited, not a complexity measurement**: p(32)=199,965 of
199,969 available windows, p(64)=199,937 of 199,937, i.e. essentially every
window is distinct and the number measures the prefix length. The vacuity
argument turns on Morse-Hedlund's logical form and does not depend on those
numbers. This is a *confirmation of the
expected answer with zero exclusionary power*: the prize announcement's own
10^9-bit check already subsumes it by seven orders of magnitude, and
obstruction **H** with `RESULTS-automaticity.md` Theorem O gives the exchange
rate -- N terms buy a kernel lower bound of about N/8 and nothing more, ever.
Note the direction: had the kill condition `p(n) <= n` fired, it would have
*refuted* P1's expected answer, not supported it.

The non-vacuous target -- "the centre column is not S-adic for any finite
primitive set S of morphisms" -- is not a computation. Every infinite word is
S-adic under an unbounded morphism set; the content is entirely in bounding S,
and that is TRIAGE row 8's proof problem (residuals provably distinct at
arbitrary depth), which ARM6 already reduced to and could not close.

---

## Proposed rows for the `PATH.md` section 7 register

`docs/rule30/PATH.md` is being edited by a concurrent session
(`FENCE-COMPLIANCE.md` names it as theirs), so these are proposed here for its
owner to merge rather than written in.

| # | Technique | Filter | Verdict | Reason | Where |
|---|---|---|---|---|---|
| 73 | Drinfeld modules / arithmetic dynamics over F_2(z), torsion-point argument | 1 | **KILLED** | phi_T lands in K{tau} = End_K(G_a), so additivity is definitional and there is no non-additive variant to retreat to; the ECAs admitting the framework are exactly the additive ones, i.e. Rule 90, where P1 is false (obstruction B in its sharpest form). Measured: Rule 30 violates additivity on 62,430 of 65,536 pairs, Rule 90 on 0. Non-torsion gives orbit aperiodicity, which is trivial here (support width exactly 2t+1) and column-blind (obstruction C). Columns of F_q-linear CA from eventually-periodic initial rows are already p-automatic (Litow-Dumas 1993; Rowland-Yassawi 2015 Thm 3.1), which is TRIAGE row 8's prior art. | `novel_frameworks/TRIAGE-novel-frameworks.md` |
| 74 | Optimal transport, W_1(mu_t, uniform) contraction | 2 | **KILLED** | delta_allzero is F-invariant, so no strict contraction to uniform exists; the empirical curve rises on 8 of the 18 cone-filled steps to t=500; and the statistic is column-blind by measurement, rel(A,B)*W does not grow across W=32..512 and rel(A,B) falls below 0.2% from W=256, while the statistic separates Rule 30 from Rule 90 by 1237% at W=256 and 1621% at W=512 and the column-0 control moves 95.6%. Fourth statistic to reproduce the GEOMETRIC-TRIAGE trap. | same |
| 75 | Tensor-network temporal-cut bond dimension (PEPS/SVD) | 3 | **KILLED** | Lone seed: bond rank identically 1 at every cut through d=12 (row 49's kill in TN language). The proposed temporal cut is degenerate for arbitrary inputs too: single-bit output caps the bond at 2 (measured exactly 2). The non-degenerate vertical cut is the Myhill-Nerode residual count, i.e. ARM8's ROBDD width, re-derived from scratch here and matching ARM8's table exactly at h=2,4,6,8 (widths 2/7/24/92, nodes 7/28/105/405), so the framework is ARM8 in different vocabulary. Obstruction G blocks the transfer to P3 regardless. | same |
| 76 | S-adic decomposition + Morse-Hedlund p(n) > n | 1 | **KILLED** | Vacuous: Morse-Hedlund is "p(n) <= n for SOME n", so p(n) > n on n <= 64 excludes only periods in that range, which the prize's own 10^9-bit check subsumes (obstruction H, Theorem O). Measured p(n) > n for all n <= 64, saturating the prefix from n=32. The non-vacuous target (not S-adic for finite primitive S) is TRIAGE row 8's proof problem. | same |

---

## Verification status of every premise in this file

Written after a first draft carried three claims it had not checked. Each row
names the command that settles it.

| # | Claim | Status | Evidence |
|---|---|---|---|
| V1 | Rule 30 is not additive over GF(2); Rule 90 is | **VERIFIED** | Exhaustive over all 65,536 pairs at width 8: Rule 30 violates `F(x+y) = F(x)+F(y)` on 62,430 pairs (95.3%), Rule 90 on 0. `verify_crossrefs.py` |
| V2 | The lone-seed orbit is aperiodic for a trivial reason | **VERIFIED** | Support width is exactly `2t+1` for t < 200, strictly increasing, so no two rows coincide. Also settles that `delta_allzero` is not on the orbit. `verify_crossrefs.py` |
| V3 | The tensor-network vertical cut rank is ARM8's ROBDD width | **VERIFIED by re-derivation** | Computed from the local rule with no ARM8 code: right-to-left max widths 2, 7, 24, 92 and reachable nodes 7, 28, 105, 405 at h = 2, 4, 6, 8. Exact match on both columns against `ARM8-center-observational-quotient.md`. `verify_crossrefs.py` |
| V4 | The proposed temporal cut is degenerate | **VERIFIED** | Single-bit output, minimal exact bond measured 2 at h = 2, 4, 6. `verify_crossrefs.py` |
| V5 | ARM6's rank 512 is the same family of quantity | **REFUTED, claim withdrawn** | ARM6 measures the 2-kernel of the centre sequence under `n -> 2n, 2n+1`, not a lightcone cut rank. See the A3 correction bullet. |
| V6 | ARM6's open edge is arbitrary-depth residual distinctness | **VERIFIED against source** | `ARM6-binary-kernel.md`: "the missing ingredient is ... a family of residuals that can be shown distinct for arbitrarily large depth", and "Finite data cannot establish that the 2-kernel or its rank is unbounded". |
| V7 | Theorem O's exchange rate is N terms for about N/8 | **VERIFIED against source** | `overnight/RESULTS-automaticity.md:111-118`, restated at `PATH.md:800`. |
| V8 | The prize's 10^9-bit check subsumes an n <= 64 period exclusion | **VERIFIED against source** | `PATH.md:927`: Wen's 10^9 bits "rule out any transient-plus-period <= 10^9". 64 versus 10^9 is 7.2 orders of magnitude. |
| V9 | All reported A2/A3/A4 numbers | **VERIFIED** | Full probe re-run post-patch, exit 0, every figure in this file reproduced; the A4 centre column is asserted equal to `common/rule30.center_column_bits` at n = 5000 inside that run. |
| V10 | Rowland-Yassawi 2015 record and the p-automaticity claim | **VERIFIED WITH CORRECTION** | Bibliographic record confirmed against CrossRef and arXiv:1209.6008: Rowland & Yassawi, "A characterization of p-automatic sequences as columns of linear cellular automata", Adv. Appl. Math. 63 (2015) 68-89, doi:10.1016/j.aam.2014.10.002. The iff is genuinely theirs (Thm 1.1) but requires CA **with memory** and the field F_q, and the easy direction is Litow-Dumas 1993. Wording corrected in A1 item 2; the same imprecision in `overnight/TRIAGE.md` row 8 is flagged there, not edited. |
| V11 | Drinfeld phi_T is additive by definition | **VERIFIED WITH CORRECTION** | Papikian, "An overview of the theory of Drinfeld modules" §2.1, and Brownawell-Papanikolas, arXiv:1806.03919 §2.1/2.3: phi: A -> K{tau} a ring homomorphism, K{tau} identified with the F_q-linear polynomials, i.e. `End_K(G_a)`. Correction: "F_q-linear (i.e. additive)" was a conflation -- F_q-linear is strictly stronger than additive when `q != p`, and they coincide only at `q = p`, which is the case here (q=2). Also phi_T's constant term is `gamma(T)`, not free. Neither correction weakens the kill; the structural non-existence of a non-additive variant strengthens it. Citation caveat carried from the check: a numbered definition from Papikian GTM 296 (2023) could not be retrieved, so no definition number is asserted for the book. |

---

## Fence compliance (verified by mtime, not asserted)

`git status` cannot verify this: `13-rule30/` is untracked in the parent repo,
so no per-file state exists. Verified instead with
`find . -newermt '2026-08-30T13:35:00' -type f -not -path './.git/*'`, re-run
after the verification pass.

Written by this arm, all inside the fence:
`experiments/overnight-arms/novel_frameworks/{triage_probe.py,verify_crossrefs.py,TRIAGE-novel-frameworks.md}`
and `runs/overnight/novel_frameworks/{a2,a3,a4,all}.{json,log}`,
`a2_highres.json`, `verify_crossrefs.{json,log}`. Plus two bytecode caches
produced as a side effect of import,
`experiments/overnight-arms/novel_frameworks/__pycache__/triage_probe.cpython-311.pyc`
and `experiments/overnight-arms/common/__pycache__/rule30.cpython-311.pyc`
(the latter from the A4 validation import, which is read-only on that module).

Nothing under `experiments/rule30/` or `docs/rule30/` was created or modified
by this arm.  Disclosed separately: later in the same session, on a distinct
task, the user asked for a review of `docs/rule30/paper/` and authorized the
resulting edits, so `zero-tail-note.{tex,pdf}`, `README.md` and
`PUBLICATION-NOTES.md` in that directory carry mtimes inside the same window.
Those changes belong to that task, not to this arm, and touched no file this
arm wrote. In particular `docs/rule30/PATH.md` was not touched, which is why
rows 73-76 are proposed here rather than merged, and
`overnight/TRIAGE.md` row 8 was not edited despite the citation correction
recorded under V10. No git command that mutates the repository was run.

**Concurrent-session changes, explicitly NOT ours.** The second mtime sweep
showed further files in the window that this arm did not create, modify, or
read: `docs/rule30/PATH.md`; everything under
`experiments/overnight-arms/frontier_attack/` (a1_p1_zeroset,
a2_p1_stroboscopic, a3_p2_orbit_closure, a4_p3_resolution); and the bytecode
caches `experiments/overnight-arms/common/__pycache__/ensemble_filter.cpython-311.pyc`,
`experiments/rule30/__pycache__/alt_trace_fiber_probe.cpython-311.pyc`,
`experiments/rule30/p_geometric_attack/__pycache__/discriminator.cpython-311.pyc`,
`experiments/rule30/proof-complexity/__pycache__/mus_probe.cpython-311.pyc`.
This arm imported exactly two modules, its own `triage_probe` and
`common.rule30`; it did not import `discriminator.py`, `ensemble_filter.py`,
or anything under `experiments/rule30/`.

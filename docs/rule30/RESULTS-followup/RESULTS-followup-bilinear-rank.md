# Follow-up: bilinear-defect / Duhamel decomposition claim ("Direction 7" + P3 corollary)

Scripts: `experiments/overnight-arms/roundtable_followup/bilinear_rank/{verify_identity.py, verify_identity_corrected.py, verify_identity_corrected2.py, build_MT_rank.py, toy_counterexample.py, rule90_screen.py}`. All run via `uv run python <script>.py`. No existing repo file modified; nothing committed.

## Summary / Verdict

- The panel's identity **as literally stated** (kernel `K_n(j) = C(n,(n+j)/2) mod 2`, exponent `n = t-s`) is **REFUTED**: MEASURED 96 mismatches out of 221 checked t-values (T=220).
- A **corrected** version of the same Duhamel/variation-of-constants idea — using Rule 150's *own* propagator as the kernel (not the Rule-90/Pascal binomial kernel) and a corrected time index (`n = t-1-s`, not `t-s`) — **does hold exactly**: MEASURED 0 mismatches out of 220 (T=220). So the underlying algebraic decomposition (Rule 30 = Rule 150-linear part XOR bilinear defect, with a Duhamel-type representation of the center column) is real once the kernel and off-by-one are fixed. This is a **correctness patch to the panel's formula**, not new insight — variation of constants for a linear recurrence with a nonlinear forcing term is a standard, expected fact; it earns a MEASURED validation label, not a discovery label.
- Conjecture A (rank(M_T) → ∞) is **MEASURED true but trivial**: rank(M_T) = T exactly at every tested T (10 to 300) — full row rank, forced by the lower-triangular-like structure, independent of anything about Rule 30's actual dynamics.
- The core inference "growing/unbounded rank of M_T implies a_t cannot be eventually periodic" (used to argue Conjecture B) is **KILLED**: `toy_counterexample.py` exhibits an explicit full-rank (rank = T → ∞, same growth as the real M_T), same-shape GF(2)-linear system whose affine image contains an exactly periodic sequence. The inference is invalid in general.
- The P3 corollary ("any algorithm must materialize Ω(n) Lucas-sections") is, on inspection, **structurally the same non-result as R9**: at best it bounds the size of *this particular* variation-of-constants derivation/unfolding, not the work of all possible algorithms. It does not improve on R9's already-identified certificate-size vs. computational-complexity confusion.
- The Rule-90 screen **checks out cleanly** (MEASURED): a_t = 0 for t > 0, and the diagnostic adjacency quantity is identically 0, for T=220.
- **No part of Wolfram's Problem 1 (non-periodicity) or Problem 3 (computational effort) is resolved or advanced by this line.** The corrected identity is a true but expected algebraic fact; everything built on top of it in Conjecture B / P3 is unproven and, for the core logical step, actively refuted in general.

---

## 1. Identity verification

Setup: Rule 30 truth table confirms `u_{t+1,i} = u_{t,i-1} XOR u_{t,i} XOR u_{t,i+1} XOR (u_{t,i} AND u_{t,i+1})` exactly (verified algebraically: Rule 30 = `p XOR (q OR r)` = `p XOR q XOR r XOR (q AND r)` for left/center/right `p,q,r`). So `chi_{t,i} = u_{t,i} AND u_{t,i+1}` as stated by the panel is the correct defect term — that part of the decomposition is right.

**verify_identity.py** (T=220, width=1340, center c=670): implements the panel's literal formula, kernel `K_n(j)=C(n,(n+j)/2) mod 2` via the Lucas/Kummer submask test (`(n & p)==p`, `p=(n+j)/2`), exponent `n=t-s`.
Result: **96 mismatches out of 221 checked t-values (t=0..220)**. First mismatches at t=4,5,9,14,15,16,17,19,20,21,23,25,27,... — not an isolated edge case, roughly 43% of t-values disagree. **VERDICT: REFUTED as stated.**

Root cause identified: the panel's formula conflates two different objects. `C(n,(n+j)/2) mod 2` (Sierpinski/Pascal-mod-2) is the Green's function for a **two-neighbor** XOR rule (Rule 90 style), not for Rule 150's **three-neighbor** XOR-of-3 update. The problem statement itself gives a second, correct characterization ("K_n(j) equals the value at position j after n steps of Rule 150 evolution from a lone seed at 0") — that is a *different* function from the binomial formula, and the two disagree.

**verify_identity_corrected.py**: swaps in the true Rule 150 propagator (`K150_n(j) := u150[n, c+j]`, obtained directly by simulating Rule 150) but keeps exponent `n=t-s`. Result: **108 mismatches out of 220** — worse, confirming the kernel swap alone isn't sufficient; there is also an indexing error.

**verify_identity_corrected2.py**: true Rule 150 propagator **and** corrected exponent `n = t-1-s` (a defect injected into `u_{s+1}` at time s propagates for `t-1-s` further linear steps to reach time t, not `t-s`). Result: **0 mismatches out of 220 (T=220)**. **VERDICT: the corrected identity holds exactly** for every t=1..220 tested.

Takeaway for step 1: the panel's specific formula is wrong in two independent ways (wrong kernel family, off-by-one time index), but a corrected version of the same Duhamel-style decomposition is a true, verified algebraic identity. This is expected/standard (variation of constants for a linear map plus nonlinear forcing) and should be labeled MEASURED validation of a mechanism, not a novel result.

## 2. Rank growth measurement

`build_MT_rank.py` builds M_T using the **corrected** kernel/index convention from step 1 (rows t=1..T, columns (s,i) with 0≤s<T within the light-cone support, entries `K150_{t-1-s}(-i)`), and computes rank(M_T) over GF(2) via Gaussian elimination on bit-packed rows.

MEASURED (exact table from the run):

| T | rank(M_T) | ambient cols | rank/T | rank/ambient |
|---|---|---|---|---|
| 10 | 10 | 100 | 1.0000 | 0.100000 |
| 20 | 20 | 400 | 1.0000 | 0.050000 |
| 30 | 30 | 900 | 1.0000 | 0.033333 |
| 50 | 50 | 2500 | 1.0000 | 0.020000 |
| 75 | 75 | 5625 | 1.0000 | 0.013333 |
| 100 | 100 | 10000 | 1.0000 | 0.010000 |
| 150 | 150 | 22500 | 1.0000 | 0.006667 |
| 200 | 200 | 40000 | 1.0000 | 0.005000 |
| 250 | 250 | 62500 | 1.0000 | 0.004000 |
| 300 | 300 | 90000 | 1.0000 | 0.003333 |

**rank(M_T) = T exactly** at every tested T (full row rank, always). This is Conjecture A confirmed, but it is a **trivial** fact: M_T is lower-triangular-like by construction (row t is the first row that can "see" the column corresponding to the maximally-recent defect `(s=t-1, i=0)`, which always evaluates to `K_0(0)=1`), so full rank is essentially forced by the combinatorial shape of the construction and says nothing about Rule 30's actual dynamics — it would hold for *any* nonvanishing defect field with the same causal light-cone structure, real or fabricated.

`rank/ambient` **decays roughly as 1/T** (0.10 at T=10 down to 0.0033 at T=300; ambient ≈ T(2T-1) ≈ 2T²) — it does **not** stay near-constant. This is the opposite trend from R9's finding: R9 measured the minimal-sufficient-constraint-set fraction of the Rule 30 light cone staying near-constant at **76–82%** (exponent ~1.93) as size grows (`docs/rule30/PATH.md` §7.3, R9 row). Here, the analogous "fraction of ambient defect-space actually used" trends toward 0, not toward a constant — so even on its own terms, this construction does **not** reproduce R9's near-constant-fraction signature; it is a different (and here, decaying) quantity.

## 3. Toy counterexample / validity of core inference — KILLED

`toy_counterexample.py`: built M_T as the T×T lower-triangular all-ones GF(2) matrix (T=200) — full rank, rank(M_T)=T, same qualitative growth (rank=T→∞) as the measured Rule-30 M_T in step 2. Picked an explicit period-3 target sequence `p_t = 0,1,1,0,1,1,...` and solved (by back-substitution, since the matrix is invertible) for a driving vector `chi` such that `M_T . chi = p_t` exactly.

MEASURED result: `M_T . chi` reproduces `p_t` bit-for-bit for all t=0..199 (chi has 133 nonzero entries out of 200, i.e. a genuinely nonvanishing, non-sparse driving sequence, not a degenerate all-zero case).

**KILLED: the inference "rank(M_T) → ∞ implies a_t cannot be eventually periodic" is invalid in general.** A full-rank, unboundedly-growing GF(2)-linear system can have an affine image that contains an exactly periodic sequence, full stop — this is not a subtle edge case, it's constructible on demand for any target periodic sequence via back-substitution whenever the matrix is invertible/full-rank. Therefore, if Conjecture B is true for Rule 30's actual `chi`, it cannot be because `rank(M_T)→∞` alone — it would require some additional, specific property of Rule-30-generated `chi` that this counterexample's `chi` (or Rule 30's own) may or may not have. The panel's offered property — "infinitely many 11-adjacent-pairs" (i.e. chi never eventually vanishes) — is not sufficient on its own: the counterexample's `chi` also never vanishes (133/200 nonzero, spread throughout) and is compatible with an exactly periodic result. No quantitative property beyond "nonvanishing" was supplied by the panel, and this experiment shows "nonvanishing" is not enough.

## 4. P3 corollary vs. R9 precedent

R9's precondition probe (`docs/rule30/PATH.md` §7.3, row 9) found Rule 30's minimal sufficient constraint set (GMUS) is a near-constant 76–82% of the light cone (exponent ~1.93) at every tested size, and explicitly concluded this "is NOT evidence of a derivation-length lower bound" — a derivation of a fixed size existing (or needing most of the light cone) says nothing about whether some *other* algorithm, possibly nonconstructive or differently structured, could compute the same output with less work. This is the standard certificate-size-vs-computational-complexity confusion, and PATH.md separately notes (§8.3) that circuit lower bounds for the center column are "structurally dead" because a fixed sequence has O(1) non-uniform circuit complexity per bit by hardwiring — i.e., claims about one fixed computation DAG for growing n do not by themselves say anything about all algorithms.

The P3 corollary here ("any algorithm computing a_n must materialize Ω(n) independent Lucas-sections of chi") is the exact same shape of claim, one level removed: it is, at best, a statement about how many defect terms *this particular Duhamel/variation-of-constants unfolding* needs to touch to compute a_n via *that formula*. It says nothing about whether a different representation, exploiting redundancy or structure not visible to this unfolding (e.g. algebraic cancellation among the K-weighted chi terms, or an entirely different recurrence), could compute a_n with less than Ω(n) sequential work. No argument was offered — by the panel or independently discoverable here — that rules out such an alternative algorithm.

**Verdict: P3 does not improve on R9's situation. It is the same non-result in new notation** — a lower bound on the size of one fixed derivation/unfolding, not a lower bound on computation in general. Both share the identical logical gap (derivation-size ≠ work lower bound), and neither addresses Wolfram's actual Problem 3 (does *some* algorithm compute a_n in less than the naive O(n) or O(n²) work).

## 5. Rule-90 screen

`rule90_screen.py` (T=220, width=1340): simulated Rule 90 (`u_{t+1,i}=u_{t,i-1} XOR u_{t,i+1}`) from the same lone-seed IC.

MEASURED:
- Center column: `a_t (Rule 90) = [1,0,0,0,0,0,0,0,0,0,0]` for t=0..10; confirmed `a_t = 0` for **all** t=1..220 (`nonzero_after_0 = False`). Matches the well-known fact.
- Diagnostic quantity `chi90_{t,i} = u90[t,i] AND u90[t,i+1]`: confirmed **identically 0** for all t=0..219, all i checked.
- Since chi90 ≡ 0, any M_T built the same way from Rule 90's defect field would have a driven term `M_T . chi90 ≡ 0` for all T — the screen passes cleanly and confirms the panel's own stated Rule-90 filter reasoning: any version of this argument that vanishes when chi vanishes is consistent (not automatically void), but by the same token, any part of the argument that does NOT essentially use nonvanishing chi would apply to Rule 90 too and must be rejected (per `PATH.md` §0). Steps 2–4 above show the rank-growth fact (Conjecture A, MEASURED true) and the P3-style Ω(n) claim do NOT essentially use nonvanishing chi in a way that distinguishes Rule 30 from a generic full-rank linear system (the toy counterexample in step 3 uses a nonvanishing chi and still yields a periodic result) — so the filter is not conclusively passed by the argument as given; nonvanishing chi is necessary-looking but not shown sufficient.

## 6. Overall verdict and what would be needed to rescue the conjecture

- **PROVED**: nothing new. Rule 30's algebraic decomposition into Rule-150-linear-part XOR bilinear defect (`chi = q AND r`) is elementary and confirmed by truth-table algebra (not a discovery).
- **MEASURED**: (1) the panel's literal Duhamel identity is false (96/221 mismatches, T=220); (2) a corrected version (true Rule150 propagator, exponent `n=t-1-s`) holds exactly (0/220 mismatches, T=220) — a validated but expected mechanism; (3) rank(M_T) = T exactly for T=10..300 (trivial full rank); (4) rank/ambient decays ~1/T, unlike R9's near-constant 76-82% fraction.
- **KILLED**: the core inference "growing rank of M_T ⇒ a_t not eventually periodic" is invalid in general, by explicit constructed counterexample (`toy_counterexample.py`, T=200, exact period-3 reproduction via a full-rank system).
- P3 corollary: not killed outright (no counterexample computation attempted for it specifically) but assessed as structurally the same certificate-size-vs-work-lower-bound non-result R9 already produced; it does not advance Wolfram's Problem 3.

**What would be needed to rescue Conjecture B** (none of this was supplied by the panel and none of it was found here): a proof that Rule-30-generated `chi` has some *specific* algebraic property — beyond mere nonvanishing — that is provably incompatible with any full-rank affine GF(2) system admitting a periodic image. Candidates that would need to be established (not attempted in this task): (a) a lower bound on the "effective algebraic independence" or minimum-weight structure of the actual K-weighted defect contributions that rules out the kind of cancellation exploited in the toy counterexample; (b) a genuinely different argument not reducible to "rank grows" at all. Absent such a property, Conjecture B is unsupported, and P3 is a restatement of R9's already-identified non-result about derivation size vs. computational work. **Wolfram's Problems 1 and 3 remain open; nothing here changes that status.**

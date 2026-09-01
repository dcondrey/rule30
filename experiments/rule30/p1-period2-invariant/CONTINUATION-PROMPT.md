# Fresh-session prompt: continue the Rule 30 period-two attack

Copy everything inside the following block into a fresh Codex session whose
working directory is `/Volumes/A/researchpapers/13-rule30`.

```text
Continue the Rule 30 research in this repository autonomously. Do concrete
mathematical and computational work, not merely a plan. The worktree contains
many unrelated user changes in sibling research-paper directories: preserve
them, scope all edits and commits to `13-rule30`, and inspect current HEAD and
status before acting.

WHAT IS AND IS NOT THE TARGET

Let F be elementary cellular automaton Rule 30,

    f(left,center,right) = left XOR (center OR right).

The immediate theorem target is only the remaining period-two rung:

    For every nonzero finite configuration y,
    Tr_0(y) != Tr_0(F^2(y)),

where Tr_0(y)_t = F^t(y)_0. Constant-zero and constant-one center traces have
already been excluded. Phase 1010... reduces after one F step to 0101..., so
the sole remaining case is an exactly alternating center trace. A proof of
this target would settle p=2 only. It would NOT prove arbitrary
nonperiodicity, randomness, normality, computational irreducibility, or the
whole Rule 30 Prize Problem 1.

CURRENT BEST UNIFORM TARGET

Prove the following statement for every m, without a tested-width parameter:

    Active-core diagonal mortality.
    Every aligned core word of length m ending in terminal symbol 3 fails a
    pin or creates 11 within m+1 macrosteps.

The bilateral reduction is already exact: for an alternating center trace,

    rho_k = s(2k,1),
    rho_(k+1) = (NOT rho_k) AND (NOT s(2k,2))
                            AND (NOT s(2k+1,2)).

Hence every actually realizable rho avoids adjacent ones. Every finite left
half reaches a finite knee represented by a core of length at most `2n` for a
seed of length `n`. A UNIFORM proof of active-core diagonal mortality would
therefore give seed mortality within `2n+1` macros and prove the period-two
theorem.

A terminal-3 core of length `m` surviving `m+1` macros would kill this
particular diagonal bound, not the period-two theorem. The weaker seed-only
`2n+2` bound and the broader alternate route remain:

    If rho has no 11 and its exact reconstructed left tail L(rho) is
    eventually zero, prove rho is eventually periodic.

Then the adjacent width-two trace is eventually periodic, contradicting the
already-recorded width-two theorem. Keep this route available if the constant
2 in the linear mortality bound is false.

CANONICAL EXACT FRONTIER DYNAMICS

Do not rederive these. Read finite words shallow-to-deep, stored as
nonnegative integers. Let inverse Gray code be

    I(X) = X XOR (X>>1) XOR (X>>2) XOR ... .

At an even macro frontier (T,A,B), the forced zero-emitting/pin-passing map is

    C = I(A OR (1 OR (B<<1))),
    D = I(C OR (A<<1)),
    pin passes iff D & 1 = 1,
    (T,A,B) -> (T+2,D,C).

The one-row shallow-to-deep recurrence is

    C_1 = v,
    C_(j+1) = C_j XOR (A_j OR B_(j-1)),
    B_0 = (T-1) mod 2.

For a forced zero phase, the new deepest output is constrained to zero, which
uniquely determines v; the next rho bit is NOT v. The next pinned phase has
v=1 and must also have zero new deepest output. In code, use
`carry_transducer.py`: `wf_step`, `parity_or`, `forced_macro`, `gray_macro`,
and `seed_state`. The forced next rho is

    forced_rho(state) = 1 XOR parity_or(state).

Reject before advancing if previous_rho = forced_rho = 1; reject the macro if
the pin is zero.

EXACT SAT FORMULATION ALREADY BUILT

`M(n,H)` in `mortality_sat.py` has n semantic seed inputs and is SAT exactly
when a no-11 seed of length n survives at least H forced post-seed macros. It
Tseitin-encodes the preceding recurrence; it is not a precomputed seed truth
table. Controls and results:

- all 95 thresholds through n=16 match independent integer enumeration;
- every SAT model was decoded and replayed;
- dropping the finite-left/deep-output constraints remains SAT;
- all Fibonacci-language seeds were enumerated through n=24, with cap 512
  and no cap hit;
- maximum survival for n=1..24 is

    2,1,1,4,3,2,2,4,3,8,7,6,5,4,5,6,6,8,8,7,10,12,11,10;

- the largest is 12 at n=22, so a small universal constant bound is dead;
- the proposed H(n)=2n+2 bound survives this finite test, but finite UNSAT is
  not a proof.

Generic proof traces did not expose an induction. Primary M(n,2n+2) DRUP
proofs were independently checked through n=11; n=12 grew to 105,998 raw
lines, 65,543 additions, maximum width 154. Shortest-death proofs
M(n,max(n)+1) were checked through n=17; at n=17 they already had 22,878
additions and maximum width 130. Treat CDCL as a falsifier/certificate
generator, not the likely final proof language. Do not enlarge SAT bounds
just to collect more finite UNSAT.

LATEST FALSIFICATIONS AND UNIFORM LEMMA

Do not resume the former constant or coefficient-seven targets:

- exact joint mortality at horizon eight is false. Right mask `0x13be`
  yields `J(82,10)` SAT. The corresponding finite row has left mask
  `0xa96bfe30260597f6e6d977d63403b1304cb232655`, support `[-164,13]`, an
  alternating center through time 184, and first failure at 185;
- `7 wt(L) >= 2n-2` is false. The length-37 hard-core word
  `0101010101010101010101010101010101000` has `wt(L)=10`, so `70<72`;
- fixed-radius label discharging is already obstructed at radius seven.
  Seed `(n,seed)=(22,0x24a28)` emits `00` while following seven forced rho
  zeros. Seed `(26,0x892512)` does the same along forced rho `01010101`.
  These give a negative self-loop and alternating two-cycle when locally
  legal factors are spliced.

One new all-width lemma is available. Every input-symbol carry action is a
permutation, so a seed append can be read shallow-to-deep starting from the
prescribed carry `(1-rho,rho)`. Composing `H` such reverse transductions gives
an exact `H`-carry cascade with at most `4^H` states that recognizes every
length-`H` emitted-label block over arbitrary frontier width. Read
`RESULTS-CORE-DISCHARGE.md` and use `core_discharge.py`. This is uniform in
width for fixed `H`, but its state grows with `H`; it is not mortality.

The local diagonal CNF `C(m,H)` in `core_mortality_sat.py` asserts survival
of an arbitrary length-`m` aligned word ending in `3`; it is stronger than
the seed CNF. All 36 thresholds through `m=7` match exhaustive word replay,
dropping no-`11` makes `C(6,7)` SAT, and `C(m,m+1)` is UNSAT through `m=34`.
These are exact finite controls only. The missing proof is a symbolic corner
induction for `C(m,m+1)` or another argument uniform in `m`.

The two weaker global balances

    2 wt(L) >= wt(rho),
    2 (wt(L)+wt(rho)) >= n

remain conjectural and together would suffice. Their radius-seven factor
approximations are killed by the preceding cycles, so a proof must retain
global seed compatibility. A corrected bound such as
`7 wt(L) >= 2n-O(1)` is also unproved; changing the additive constant after a
finite sweep is not a theorem.

EXACT TRIANGULAR CORRELATION LEMMA

Let P_w be suffix XOR on width-w vectors:

    (P_w x)_k = XOR_(j>=k) x_j.

Then over F_2,

    <P_w x,P_w y> = x^T K_w y,
    (K_w)_(i,j) = (min(i,j)+1) mod 2,
    rank(K_w) = w.

The even- and odd-output pieces have ranks ceil(w/2) and floor(w/2).
Therefore inverse-Gray correlation is structured and triangular, but its
separable bilinear rank grows unboundedly. A 37-bit summary containing
T mod 16, split parities/endpoints of A,V,C,S, and every pairwise split
inverse-Gray correlation has an equal-depth reachable closure collision at

    T=32, previous rho=0,
    seed 0x200 length 15 follow 1:
        (32,1431655765,984962389)
    seed 0xa20 length 15 follow 1:
        (32,1431655765,716879189).

Both force rho=1, pass the pin, preserve no-11, and have equal current
summaries but different successor summaries. Do not retry bounded quadratic
summaries by merely adding a few more parity bits.

An immediate endpoint identity worth exploiting (verify it in the retained
checker before using it) is: when w is even and e_i=(i+1) mod 2,

    K_(w+2) = [ K_w   e   e ]
              [ e^T   1   1 ]
              [ e^T   1   0 ].

Likewise, appending deep bits a,b gives

    (P_(w+2)(x,a,b))_k = (P_w x)_k XOR a XOR b,  k<w,
    output_w = a XOR b,
    output_(w+1) = b.

The forced recurrence makes the new deepest outputs zero. The best current
hope is to turn this moving-endpoint block recurrence into a well-founded
statement tied to those zero outputs, rather than compressing K_w to a fixed
finite summary.

ORDERED-BOUNDARY OPERATOR ATTEMPT ALREADY KILLED

The exact four carry states, the eight D8 prefix actions, and D8 x carry were
tested as deterministic weighted observers. Small exact Farkas-style
multisets prove that no bounded-below additive regular edge cost on these
controls strictly decreases on every surviving macro. D8 x carry is not a
real refinement: from zero carry, carry is the current D8 action applied to
zero. The D8 x depth-parity observer was solver-inconclusive, not positive.
Do not extend it by more runtime or seed length without a new exact strategy.
Non-additive/reset/stack-like ordered certificates and a full moving-endpoint
triangular argument remain open.

OTHER RETIRED CLASSES — DO NOT REPACKAGE THEM

- fixed-local additive rankings: exact Farkas obstructions;
- finite modular/count/endpoint summaries: same-summary/different-future
  collisions;
- every fixed Hasse order: H_k(I(X))=H_k(X) XOR H_(k+1)(X), so it needs the
  next order; rich reachable equal-depth collisions also exist;
- carry contraction: all four-symbol actions are permutations generating D8;
- bounded D8 lookahead/action summaries: closure collisions;
- bounded run-length/gap projections: collisions; the full ordered gap list
  is lossless but unbounded;
- natural signed/contact/boundary counts: exact oscillating transition
  multisets;
- odd-row complement/toggle: two phases compose back to exactly F^2;
- hard-core plus fixed D8 action: closure collision;
- the 37-bit split triangular-correlation summary described above.
- the joint constant-eight/sixteen-zero-gap theorem;
- the exact coefficient-seven bound `7 wt(L)>=2n-2`;
- radius-seven emitted-label factor discharging for either weaker balance.

Do not "improve" these merely by increasing locality, moment order, endpoint
window, lookahead, seed bound, or runtime. A genuinely new attempt must
retain an unbounded ordered object with an exact proof mechanism, or give a
symbolic induction that removes n.

LOAD-BEARING CONTROLS

- Rule 30 finite row {-8,-1,6} alternates through t=14 and first fails at
  t=15. Never reject it earlier.
- The finite Rule 30 row with right mask `0x13be` and left mask
  `0xa96bfe30260597f6e6d977d63403b1304cb232655` alternates through t=184 and
  first fails at t=185. This supersedes the shallow control as the strongest
  known prefix trap.
- Rule 90 finite row {-1,1} has zero center forever. Any generic argument
  that also excludes this is invalid. Rule 30's no-11 lemma uses OR and must
  not be transferred to Rule 90's XOR.
- An infinite-left spatial-period-7 wallpaper with finite right part {1,4}
  survives the alternating fiber. Therefore finite-left support is
  essential; any invariant excluding the wallpaper has silently discarded a
  valid infinite-left control.
- Forward support expansion is not a contradiction. Any "escape" must map
  exactly to distinct nonzero cells of the fixed reconstructed initial tail
  L(rho), or prove mortality.
- Finite data can falsify a universal claim but cannot prove it.

ASSESSMENT OF THE FOUR EXOTIC FRAMEWORKS

The non-Hermitian, trans-adic, sheaf, and hyperbolic-thermodynamic proposals
were assessed. Their broad ingredients already exist in literature; their
specific Rule 30 mappings have not been established as novel. As stated:

- non-Hermitian skin-effect mapping has low merit: a state-dependent,
  changing Hilbert space is not a fixed linear operator with comparable
  spectral winding, an exceptional point is a parameter-space singularity,
  and periodicity of one observed column does not imply closure of the global
  operator orbit;
- a trajectory-dependent trans-adic metric is circular, Poincare recurrence
  does not apply without a finite invariant measure, and negative curvature
  does not forbid closed geodesics;
- hyperbolic thermodynamics lacks a proved bridge from embedding-dependent
  surface tension/conductivity to central-column periodicity or algorithmic
  complexity;
- sheaf local-to-global language has the most merit only after conversion to
  an exact constraint system. The mortality CNF is already a concrete
  version. Ordinary sheaf cohomology also needs abelian/linear stalk data,
  and nonzero H^1 does not automatically preclude H^0 global sections.

Do not pursue an exotic reformulation unless every map is canonical and the
claimed implication back to Rule 30 is proved independently; decorative
geometry is not progress.

FILES TO READ FIRST — DO NOT LOAD THE WHOLE ARCHIVE

1. `experiments/rule30/p1-period2-invariant/README.md`
2. `experiments/rule30/p1-period2-invariant/RESULTS-JOINT-MORTALITY.md`
3. `experiments/rule30/p1-period2-invariant/RESULTS-TAIL-DENSITY.md`
4. `experiments/rule30/p1-period2-invariant/RESULTS-CORE-DISCHARGE.md`
5. `experiments/rule30/p1-period2-invariant/carry_transducer.py`
6. `experiments/rule30/p1-period2-invariant/core_discharge.py`
7. `experiments/rule30/p1-period2-invariant/RESULTS-CORE-MORTALITY-SAT.md`
8. `experiments/rule30/p1-period2-invariant/core_mortality_sat.py`
9. `experiments/rule30/p1-period2-invariant/mortality_sat.py`

The matching preregistrations are the audit trail. Read another historical
result only if the compact README routes you to it.

REPRODUCTION COMMANDS

    uv run --project experiments/sygus-p3 python \
      experiments/rule30/p1-period2-invariant/mortality_sat.py \
      --validate --max-validate 16

    uv run --project experiments/sygus-p3 python \
      experiments/rule30/p1-period2-invariant/quadratic_probe.py \
      --max-width 8 --max-seed 16 --max-follow 32

    python3 experiments/rule30/p1-period2-oboc/verify_oboc_negative.py

    python3 \
      experiments/rule30/p1-period2-invariant/core_discharge.py

WORKING METHOD FOR THIS SESSION

1. Inspect current HEAD/status and read the seven routed files above.
2. Reproduce the lightweight controls before relying on them.
3. Before any substantive new search, write a dated preregistration fixing
   the candidate certificate, success criterion, controls, resource limits,
   and kill conditions.
4. Prefer a symbolic derivation. Computation should seek counterexamples,
   exact identities, or a parameterized proof schema—not a larger finite
   horizon.
5. The recommended first attack is a symbolic induction on the full
   seed-generated compatibility object. Viable forms are an unbounded
   interval grammar with a well-founded stack/multiset rank, or an
   `n`-to-`n+1` interpolant whose closure is checked independently. Use the
   reverse cascade to make fixed-horizon obligations exact, but do not promote
   another bounded factor graph: radius seven is already false. If the
   induction fails, find the smallest exact reachable collision/cycle and
   record the whole certificate class that it kills.
6. Do not claim success unless the argument quantifies over all n and the
   reduction to the alternating finite-support fiber is explicit.
7. Update the compact README and write a result report. Preserve failures as
   useful exact negatives. Run independent controls, then commit only scoped
   Rule 30 artifacts.

At the end, tell me plainly whether we proved the period-two theorem, found a
uniform intermediate lemma, or only obtained a finite/negative result. If a
uniform period-two theorem is proved, also state clearly that it is still only
the p=2 rung and not yet a full solution of Rule 30 unpredictability.
```

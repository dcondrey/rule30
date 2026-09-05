# Period-two same-orbit attempt: resumption sheet

Updated: 2026-09-01

Status: **OPEN.  No period-two theorem was proved.**

Target:

```text
For every nonzero finite y, Tr_0(y) != Tr_0(F^2(y)).
```

The constant-zero and constant-one cases are already proved elsewhere.  The
remaining trace is alternating; phase `1010...` reduces to `0101...` after one
application of `F`.  Proving this target would settle only the `p=2` rung of
Prize Problem 1.

## Read only this file first

The directory is intentionally flat because the scripts import one another by
filename and every raw report contains historical reproduction commands.
Preregistrations and result reports are retained unchanged as an audit trail.
Do not load them all into context.

Use this routing table:

| Need | Read/run |
|---|---|
| Lowest-token current proof state and exact dependency DAG | `PROOF-STATE-CAPSULE.md` |
| Exact target, `F^2`, defect, primary certificates | `RESULTS.md`; `derive_and_controls.py`; `verify_negative_certificate.py` |
| Six-route exhaustion ledger | `P1-SIX-ROUTE-PROGRAM.md`; `RESULTS-SIX-ROUTE-EXHAUSTION.md` |
| Inverse-Gray and moment hierarchy | `RESULTS-PARITY.md`; `verify_moment_negative.py` |
| Four-state operator/carry form | `RESULTS-CARRY.md`; `carry_transducer.py` |
| Run-length/boundary-gap coordinates | `RESULTS-RUNLENGTH.md`; `runlength_search.py` |
| Signed counts, touching colors, row toggle | `RESULTS-DIVERGENCE.md`; `verify_divergence_negative.py`; `toggle_phase.py` |
| Actual-right trace restrictions (`11`, `00000`) | `RESULTS-BILATERAL.md`; `RESULTS-RIGHT-FILTERED-MORTALITY.md`; `bilateral_hardcore.py`; `right_trace_forbidden.py` |
| Joint left-finite/right-realizable mortality | `PREREGISTRATION-JOINT-MORTALITY.md`; `RESULTS-JOINT-MORTALITY.md`; `joint_mortality.py` |
| Variable-seed mortality SAT and triangular correlations | `RESULTS-MORTALITY-SAT.md`; `mortality_sat.py`; `verify_drup.py`; `quadratic_probe.py` |
| Time-ordered pivot/emission audit | `RESULTS-PIVOT-EMISSION.md`; `pivot_emission_audit.py` |
| Dynamic Boolean ideal/variety trace | `RESULTS-DYNAMIC-BOOLEAN-IDEAL.md`; `ideal-variety-n4-n12.json`; `pivot_emission_audit.py` |
| Exact `n=10` plateau cofactors | `RESULTS-PLATEAU-BEZOUT.md`; `plateau_bezout.py`; `verify_plateau_bezout.py`; `plateau-bezout-n10.json` |
| Cofactor and interval-annihilator shifts | `RESULTS-COFACTOR-AUTOMATON.md`; `RESULTS-INTERVAL-ANNIHILATOR.md`; matching generators/verifiers/JSON |
| Defect/restart formula cocycle | `RESULTS-DEFECT-RESTART-COCYCLE.md`; `defect_restart_cocycle.py`; `verify_defect_restart_cocycle.py`; `defect-restart-cocycle.json` |
| OpenEvolve delay-potential search | `docs/rule30/RESULTS-openevolve-p1-cocycle.md`; `experiments/openevolve-p1-cocycle/` |
| Bilateral boundary-collision specification | `RESULTS-DEFECT-RESTART-COCYCLE.md` section 8; `docs/rule30/RESULTS-diagonal-periodicity.md`; `docs/rule30/RESULTS-followup-skew-product-cocycle.md` |
| Moving-endpoint block and literal peel obstruction | `RESULTS-ENDPOINT-PEEL.md`; `endpoint_peel.py` |
| Tail density, deep-zero/core conjugacy | `RESULTS-TAIL-DENSITY.md`; `tail_density.py` |
| Reverse fixed-horizon cascade and factor obstruction | `PREREGISTRATION-CORE-DISCHARGE.md`; `RESULTS-CORE-DISCHARGE.md`; `core_discharge.py` |
| Stronger active-core diagonal CNF | `RESULTS-CORE-MORTALITY-SAT.md`; `core_mortality_sat.py` |
| Projected cut / interpolant probe | `PREREGISTRATION-CORE-INTERPOLANT.md`; `RESULTS-CORE-INTERPOLANT.md`; `core_interpolant_probe.py` |
| Peel/Craig endpoint morph | `RESULTS-CORE-CRAIG-MORPH.md`; `core_craig_morph.py` |
| Endpoint zero/two sections and four-phase restart | `RESULTS-ENDPOINT-RESTART-COCYCLE.md`; `endpoint_restart_cocycle.py` |
| Survivor clusters are fibres of one endpoint state; state census | `RESULTS-CLUSTER-ANATOMY.md`; `cluster_anatomy.py` |
| Cartier/rationality route disposition | `RESULTS-CARTIER-ROUTE-DISPOSITION.md` |
| Dyadic-period graph audit | `RESULTS-DYADIC-PERIODICITY.md`; `dyadic_periodicity_analyzer.py` |
| Dyadic exceptional-family separator | `RESULTS-DYADIC-EXCEPTION-SEPARATOR.md`; `dyadic_exception_separator.py` |
| Dyadic route scope disposition | `RESULTS-DYADIC-ROUTE-DISPOSITION.md` |
| Rotated inverse-cone / Peel identity | `RESULTS-ROTATED-PEEL-IDENTITY.md`; `rotated_peel_identity.py` |
| Peel inverse-lift monoid | `RESULTS-PEEL-LIFT-MONOID.md`; `peel_lift_monoid.py` |
| Finite-rank descent to the rank-zero separator | `RESULTS-RANK-ZERO-REDUCTION.md`; `rank_zero_separator.py` |
| Eventual-constant-tail separator | `RESULTS-EVENTUAL-CONSTANT-TAIL.md`; `eventual_constant_tail.py`; `constant_tail_shift.py`; `constant_tail_doubling.py`; `constant_tail_scale.py` |
| Reversed-diagonal constant-tail queue | `RESULTS-CONSTANT-TAIL-QUEUE.md`; `constant_tail_queue.py` |
| Queue end-window/phase no-go theorem | `RESULTS-QUEUE-WINDOW-PHASE-NO-GO.md`; `constant_tail_queue_window_phase_no_go.py` |
| Constant-tail queue SAT minima | `RESULTS-CONSTANT-TAIL-LANGUAGE-COCYCLE.md`; `constant_tail_queue_sat.py` |
| Actual-right constant-tail refinement | `RESULTS-EVENTUAL-CONSTANT-TAIL.md` section 11; `constant_tail_right_filter.py` |
| Constant-tail regular-language cocycle | `RESULTS-CONSTANT-TAIL-LANGUAGE-COCYCLE.md`; `constant_tail_language_cocycle.py` |
| Constant-tail frontier-distance theorem | `RESULTS-CONSTANT-TAIL-FRONTIER-GRAPH.md`; `constant_tail_frontier_graph.py` |
| All-length phase-gap retreat cover | `PREREGISTRATION-PHASE-GAP-COVER-PROOF.md`; `RESULTS-PHASE-GAP-HALL.md`; `constant_tail_phase_gap_hall.py`; `constant_tail_phase_gap_proof.py` |
| Mixed budget, origin-prefix Hall, exact pull rewrites, and pull ray | `PREREGISTRATION-MIXED-RUN-RETREAT-BUDGET.md`; `PREREGISTRATION-ORIGIN-PREFIX-HALL.md`; `PREREGISTRATION-PULL-RAY.md`; `PREREGISTRATION-MACRO-EDGE-RANK.md`; `RESULTS-MIXED-ORIGIN-RETREAT.md`; `RESULTS-PULL-RAY.md`; `RESULTS-MACRO-EDGE-RANK.md`; `constant_tail_mixed_run_budget.py`; `constant_tail_origin_prefix_hall.py`; `constant_tail_pull_rewrite.py`; `constant_tail_pull_ray.py`; `constant_tail_macro_edge_rank.py`; `constant_tail_pull_potential.py` |
| Pull-coordinate falsification and hard-core root localization | `PREREGISTRATION-PULL-COORDINATE-DEPTH.md`; `PREREGISTRATION-PULL-EXHAUSTION-TRAP.md`; `RESULTS-PULL-COORDINATE-DEPTH.md`; `RESULTS-PULL-EXHAUSTION-TRAP.md`; `PREREGISTRATION-HARD-CORE-PULL-DEPTH.md`; `RESULTS-HARD-CORE-PULL-DEPTH.md`; `constant_tail_pull_coordinate_depth.py`; `constant_tail_pull_exhaustion_trap.py`; `constant_tail_hard_core_pull_depth.py` |
| Endpoint/event bridge and corrected pull-token target | `RESULTS-ENDPOINT-EVENT-BRIDGE.md`; `constant_tail_endpoint_event_bridge.py` |
| Pull-row alpha support | `PREREGISTRATION-PULL-ROW-PROJECTED-SUPPORT.md`; `PREREGISTRATION-PULL-ROW-ALPHA-SUPPORT.md`; `RESULTS-PULL-ROW-ALPHA-SUPPORT.md`; `constant_tail_pull_row_projected_support.py` |
| Nonfinal alpha-support disposition | `PREREGISTRATION-NONFINAL-ALPHA-SUPPORT.md`; `RESULTS-NONFINAL-ALPHA-SUPPORT.md`; `constant_tail_nonfinal_alpha_support.py` |
| Three-row late-pull diagonal | `PREREGISTRATION-LATE-PULL-HORIZON.md`; `PREREGISTRATION-LATE-PULL-DIAGONAL-CNF.md`; `PREREGISTRATION-DLP-SOURCE-DEFECT.md`; `RESULTS-LATE-PULL-DIAGONAL.md`; `constant_tail_late_pull_horizon.py`; `late_pull_diagonal_sat.py` |
| Rotated DLP, hard-core relaxation, and binary-wedge target | `RESULTS-DLP-ROTATED-WEDGE.md`; `PREREGISTRATION-DLP-HARD-CORE-CORE.md`; `RESULTS-DLP-HARD-CORE-CORE.md`; `PREREGISTRATION-BINARY-WEDGE-HORIZON.md`; `RESULTS-BINARY-WEDGE-HORIZON.md`; `RESULTS-BINARY-WEDGE-HIGH-ELIMINATION.md`; `dlp_rotated_wedge.py`; `late_pull_hardcore_core.py`; `binary_wedge_horizon.py`; `binary_wedge_adversary.py`; `binary_wedge_high_elimination.py` |
| Forum/informal-source audit | `RESULTS-FORUM-AUDIT-2026-09-02.md` |
| Actual-right terminal frontier audit and scope correction | `PREREGISTRATION-ACTUAL-RIGHT-FRONTIER.md`; `RESULTS-ACTUAL-RIGHT-FRONTIER.md`; `constant_tail_actual_frontier.py` |
| Scale telescoping, derivative failures, and zero-prefix greedy target | `RESULTS-SCALE-TELESCOPING.md`; `constant_tail_zero_prefix_matching.py`; `constant_tail_zero_prefix_bitsliced.py` |
| Projected diagonal support and one-credit halving targets | `RESULTS-PROJECTED-DIAGONAL-HALVING.md`; `constant_tail_right_zero_prefix_selector.py`; `constant_tail_halving_recurrence.py` |
| Projected-support algebra and route disposition | `RESULTS-PROJECTED-SUPPORT-DISPOSITION.md`; `constant_tail_projected_support_algebra.py` |
| Deterministic-halving morph obstruction | `RESULTS-HALVING-ROUTE-DISPOSITION.md`; `constant_tail_halving_morph_audit.py` |
| Moving endpoint-flip cocycle | `RESULTS-ENDPOINT-FLIP-COCYCLE.md`; `endpoint_flip_cocycle.py` |
| Single-flip pairing on RW survivor levels (killed); block halving and the counting constant `C = 3` | `RESULTS-FLIP-PAIRING.md`; `flip_pairing.py`; `block_halving.py` |
| Evolutionary rank-zero witness search | `docs/rule30/RESULTS-openevolve-p1-rank-zero.md`; `experiments/openevolve-p1-rank-zero/` |
| Start a fresh research session without rederiving history | `CONTINUATION-PROMPT.md` |
| Audit search design before interpreting a result | Matching `PREREGISTRATION*.md` only |

## Canonical exact map

Let `I` be inverse Gray code on finite bit words:

```text
I(X) = X XOR (X >> 1) XOR (X >> 2) XOR ...
```

At an even alternating-trace frontier:

```text
C = I(A OR (1 OR (B << 1)))
D = I(C OR (A << 1))
pin passes iff D & 1 = 1
(A,B) maps to (D,C).
```

Boundary-gap form:

```text
g(C)=A OR (1+zB)
g(D)=C OR zA,
g(X)=X XOR (X>>1).
```

Carry form for aligned symbol `q=(a,b)` and carry `(c,d)`:

```text
c' = c XOR (a OR b)
d' = d XOR (c OR a)
emit (d',c').
```

The four symbol actions generate `D8`, a transitive permutation group of order
eight.  The active front grows exactly one position per macrostep.

For an actual right half-plane, not an arbitrary rho boundary:

```text
rho_k=s(2k,1)
rho_(k+1)=(NOT rho_k) AND (NOT s(2k,2)) AND (NOT s(2k+1,2)),
```

so rho contains no adjacent ones.

Actual right realizability is strictly stronger.  The exact nine-cell
light-cone identity in `right_trace_forbidden.py` proves uniformly that rho
also contains no `00000`.  The realized-prefix counts are already below the
hard-core Fibonacci counts at length five.

After reversing the complete aligned word and deleting its inert leading
deep zeroes, one forced macro is exactly the active-core map

```text
v -> Transduce(v) . 3.
```

This is an all-width conjugacy, not a bounded summary.  Pin passage is final
carry `c XOR d=1`, and the next forced rho is `1 XOR c`.

## What was tried and why it stopped

| Attempt | Positive normalization | Exact kill |
|---|---|---|
| Local additive ranking | Fixed-local de Bruijn normal form | Farkas multisets for locality 1–4 |
| Modular/local quotient | Finite summaries of counts/endpoints | Same-summary, different-future collisions |
| Hasse/mixed moments | `H_k(I(X))=H_k(X) XOR H_(k+1)(X)` | Every fixed order needs the next; reachable equal-length collision |
| Carry contraction | Complete four-state subsequential transducer | All actions are permutations; no synchronizing/rejecting ideal |
| Action lookahead | Exact D8 word action | Closure fails at depths 1 and 2; further depth is horizon growth |
| Run-length digits | Lossless full boundary-gap list | Digits/list length unbounded; bounded summary collision |
| Natural gap/run ranks | Boundary count, gap excess, max gap, squares, lex orders | Each moves both ways or merely restates front growth |
| Signed left/right/contact counts | Exact tile/contact features | Two-step six-summary oscillation; 36-transition Farkas multiset |
| Odd-row toggle | Alternating OR/AND-dual rules | Two phases compose to exactly `F^2`; odd rows become cofinite |
| Hard-core rho + action | Genuine-right-half no-`11` language | Length-1/3 zero seeds share summary but have different successors |
| Variable-seed CDCL proofs | Exact mortality CNF with no free post-knee boundary | Checked finite UNSAT; proof additions and width grow sharply |
| Triangular quadratic algebra | `<Ix,Iy>=x^T K y`, `K_ij=(min(i,j)+1) mod 2` | `rank(K)=width`; 37-bit split-correlation summary has an equal-depth closure collision |
| Time-ordered kernel pivots | Exact ANF emission recurrence through three post-knee macros | `K=P^T P` is symmetric with raw diagonal `1,0,...`; a length-`n` seed starts its tail constraints at row depth `2n`; the first `n=4` post-knee pin is `1+rho_2 rho_4`, with no linear pivot |
| Dynamic Boolean ideals | Exact ANF generators and projected SAT counts for every horizon, `n=4..12` | Unit ideal reached at horizons `5,4,3,3,5,4,9,8,7`; long nonzero plateaus occur, so finite generator absorption is not immortality |
| `n=10` plateau Bezout extraction | Exact dynamic and hard-core lift cofactors in the Boolean quotient | `epsilon_8=1` already on `V_3`, `q_8=1` already on `V_5`; dynamic cofactor degree is at most 5 but support spans almost all seed positions |
| Shift-normalized cofactor automaton | Exact recurrence `C_(i+1)=C_i(1+g_i)` | Degree five fails at `n=12`; support spans the seed; the highlighted motif has a literal self-loop and is not a closed state |
| Interval annihilator | Uniform matched-extension identity on complete survivor indicators | Matched appends are exact macro shifts; an unmatched rank-five defect appears, so restart/defect states remain unclassified |
| Defect/restart cocycle | Exact advance, restart, and extension partitions on full symbolic frontier/indicator states | Uniform partition lemma proved, but strict rank contraction is false; `n=10` has an exact indicator/period-three-phase closure collision |
| Evolved plateau-delay potential | AST-restricted OpenEvolve search over exact cocycle features, followed by an external-width audit | Best OpenEvolve tuple orders 8/10 plateaus; a finite-perfect modular tuple fails at the new `n=18` plateau, and no one-/two-component separator exists in the 17,147-expression nonmodular census |
| Literal endpoint peel | Full aligned Mealy tableau and exact `K_(w+2)` endpoint block | `(n,H)->(n-1,H-2)` is semantically false: length-4 seed `0xa` survives 4, while every length-3 seed survives at most 1 |
| Coefficient-seven tail density | Exact minimum-weight falsifier and period-seven sharp control | **Killed:** length-37 rho `0101010101010101010101010101010101000` gives `wt(L)=10`, hence `70 < 72` |
| Two-factor right-filtered mortality | Uniform right-light-cone prohibition of `00000` | **Killed:** a length-30 seed avoiding `11`/`00000` survives 10; it contains the actual-right forbidden factor `101001` |
| Exact joint mortality | Direct coupling to a genuine Rule 30 right light cone | **Killed:** right mask `0x13be` gives `J(82,10)` SAT; the resulting finite row alternates through time 184 |
| Core/factor discharging | Exact reverse `H`-carry cascade over arbitrary frontier width | Width-uniform for fixed `H`, but **killed as a bounded factor proof:** seed-generated radius-seven negative self-/two-cycles exist |
| Active-core diagonal mortality | Local carry CNF `C(m,m+1)` over every length-`m` word ending in `3` | UNSAT through `m=34`; all thresholds through `m=7` match enumeration, but no induction in `m` |
| Dyadic periodicity mismatch | Fiber-monoid induction proves every finite zero-ray cascade has eventual period `2^k` | **Killed as an acceptance separator:** endpoint `2^omega` maps to the accepted cut `(12)^omega`; every eventually-`2` hard-core endpoint gives an eventually-period-two accepted cut |
| Dyadic mismatch plus reachability | Alternating-output descent through cascade width | **Uniform partial repair:** no finite zero-ray generator word reaches an eventually-`(12)` cut, so the entire eventually-`2` accepted counterfamily is excluded; non-eventually-`2` endpoints remain open |
| Rotated `phi` triangles | `P(I(sigma e))=sigma^2 I(e)`, Peel-rank drift, and last-support preservation | **Uniform reduction:** every finite-rank inverse cut over a hard-core endpoint forces that endpoint to be aperiodic; positive tail ranks grow `m,m+1,...`; aperiodic endpoints remain |
| Inverse Peel lift monoid | Four right-inverse maps close to a 13-element monoid with only 1-/2-cycles | **Uniform lemma:** a return block doubles its period iff it lies in `{0,1}*` with odd `1` parity or `{0,3}*` with odd `3` parity; the doubled child contains `2`, so strict doublings are never consecutive. Currying the other table input recovers the queue/affine `D8` action exactly |
| Endpoint prefixing plus rotated Peel | Prepending hard-core state `2` lowers every positive finite Peel rank by exactly one | **Uniform reduction:** all finite ranks reduce to the rank-zero separator: no finite-support cut may have a hard-core terminal endpoint; exhaustive through cutoff 23, proof open |
| First-infinite endpoint shift | The first infinite tail cut above a finite rank-zero cut must be eventually constant `2` or `3` | **Uniform narrowing:** it suffices to separate these two constant-tail fibers; exact census through cutoff 23 and GA controls through 96, proof open |
| Constant-tail lasso and scale block | Endpoint shift is an exact partial lasso transducer; newest-cut permutations are the eight affine triples `(alpha,beta,gamma)`; `W=e[n,2n)` forces a padding-independent block `R_c(W)=e[2n,4n)` | **Uniform reduction:** it suffices to prove `R_c(W)` cannot continue a hard-core `W`; exhaustive through `|W|=22`. The original bound `s_2<=#2` first fails at length 17; the repaired targets `s_2<=#2+1_{22}` and `s_3<=#2+3` survive the census but are unproved. The apparent six-state doubling profile is rejected by four universal `8 -> 16` profile collisions. A doubled word is uniformly unique up to rotation, but the prefix-independent exact-cycle orbit itself branches at shift 26,603, so the missing invariant must retain prefix/entry-state data |
| Zero-prefix scale telescoping | Sweep `W^(k)=0^kW[k:]`; greedily match each survival row to the first later `k` whose newest affine boundary permutation changes | **Live uniform conjecture:** zero failures through length 22 in 242,783 cases. Tail 2 matches every row; tail 3 matches every nonfinal row, giving the sufficient bounds `s_2<=|W|`, `s_3<=|W|+1`. Pointwise intervention matching and all derivative-rank variants are killed at length 21; proof of the ordered zero-prefix finite-difference lemma remains open |
| Projected diagonal support | At row `j`, retain only `(alpha,beta)` for tail 2 or `(alpha,gamma)` for tail 3 and ask for one adjacent zero-prefix change at `k>=j` | **Smaller live conjecture:** no matching is needed; the last required row gives `s_2<=|W|`, `s_3<=|W|+1`. Zero failures on the complete hard-core corpus through length 23. The temporary actual-right `22222` restriction is unnecessary; its 111,899-case held-out complement also passes. Proof open |
| Holonomy-defect closure | Use `delta_(j,k)=A_(j,k)^(-1)A_(j,k+1)` and ask whether the ordered defect word has a well-defined next-row update | **Killed as a bounded state:** defects plus an absolute phase reconstruct the complete current affine profile but have different successors at length 8; all previous endpoints still collide at length 9. A preregistered annotation retaining both queue ends passes held-out lengths 11–12 and fails at length 13. Only the complete interior dependency queues are presently closed; diagonal support itself remains live |
| Queue end windows plus total phase | Retain any fixed two-ended queue window together with length, endpoint/event data, and the exact total `D8` action | **Uniformly killed:** for every window radius and for each tail, legal families differing by the neutral interior blocks `00`/`11` have identical retained state and legal successors with different total actions. This is an all-length no-go for that state class, not a claim against every bounded quotient; the full ordered queue remains closed |
| One-credit half-word recurrence | Split `W` into halves and bound `s_c(W)` by `ceil(n/2)+1` plus the largest half-word survival over both tail modes | **Independent sufficient conjecture:** exact lengths 21–23 and 8,000 long random tail cases pass. The recurrence implies `s_c(W)<2n` by induction. Literal suffix embedding is false, so a proof must retain a conjugated frontier/boundary potential |
| Reversed constant-tail diagonal | The complete growing inverse-cone formula reverses to `S_0=c, S_i=g_(S_(i-1))(R_i)`; the final scan state exactly decodes the next hard-core endpoint and appends its boundary symbol | **Uniform stronger reduction:** mortality of every finite queue beginning in `c in {2,3}` and ending in `{1,2}` would close the constant-tail separator. The exact quotient `3 -> 1` gives ternary representatives, and every normalized successor avoids `20`, `22`, `011`; `lifetime(R)<=|R|` holds exhaustively through length 15, induction open |
| Dual colex, phase gaps, and pull ancestry | Both inherited scans strictly colex-descend; the phase-gap cover is proved for all lengths. Every nonfirst retreat has one productive pull, and every post-retreat pull is exactly `102->0021` on `p-t=N-3`. The appended-coordinate parent forest obeys `h_i=h_(i-1)+1` for pull gaps at least three and `h_i=h_(i-2)+1` for gap two, so `#pulls<=2 max h_i` | **Unrestricted feature and coordinate budgets falsified:** the length-77 sparse word kills the feature/raw reserve, while `3001 0^382 2` kills `r>=2h-1`; `m=390` reaches depth 4 from root 3. The zero-run resonance is dyadic and the abstract counterfamily is not hard-core endpoint-derived. Retain the full gap scale, restrict the theorem to endpoint-derived queues, or use eventual actual pull gaps `{2,3,4,5}` |
| Endpoint/event bridge | On every nonsingleton endpoint-derived queue, `A/B/C` are exactly future endpoint transitions `21/22/12`; the singleton `(2,)` is the boundary-credit exception | **Uniform identity plus exact correction:** `22222222` has no initial `12` but its queue executes `AC`, so literal initial-pair charging is false. A finite chain bound is enough for mortality; inject pulls into ordered zero-prefix tokens, optionally decorated by `D8`, rather than proving the stronger half-density bound |
| Pull-row alpha support | Restrict zero-prefix diagonal support to nonfinal `C` rows and the single high-translation coordinate `alpha`; on hard-core rows `alpha` is exactly the parity of active raw queue cells after the leading tail | **Sufficient conjecture, now weakened further below:** a non-eventually-`2` immortal endpoint has infinitely many pull rows, while PAS requires a token `j<=k<n` at each. Zero failures in 392,830 word/tail cases and 31,595 pull rows through length 23; proof open. `k=j` fails at length six and alpha-witness displacement reaches at least twelve |
| Nonfinal alpha support | Ask for an alpha witness at every nonfinal row rather than only at pulls | **Retired as a proof reduction:** the frozen exact holdout has zero failures in 390,944 completed word/tail cases and 107,735 nonfinal rows, but at `j=n` the empty witness interval says exactly `s_c(W)<=n+1`. It restates the required scale bound rather than explaining it; the preregistered length-128 random row was stopped after this disposition |
| Three-row late-pull diagonal | For a length-`n` scale word, exclude nonfinal pulls only at rows `n,n+1,n+2`; an absolute pull `m=3n+r` lands in exactly this window for `n=floor(m/3)` | **Smallest sufficient conjecture:** no alpha variables or early-row support are needed. No late pull occurs in the full length-23 hard-core corpus, eight aligned GA adversaries, 240,000 long random word/tail cases, or all binary source words through length 20. Exact CNFs for all six tail/residue cases are UNSAT through `n=20`, but generic conflicts and proof width grow and no induction is known |
| Rotated binary-wedge horizon | Force a constant inverse cut over an arbitrary binary source and bound the initial binary endpoint continuation by `n+1` | **Cleaner but stronger sufficient conjecture:** the preregistered bound `M_c(n)<=n` is exactly falsified by `M_3(15)=16`; the repaired sufficient bound `M_c(n)<=n+1` has zero exact failures through `n=20`. It discards hard-core and terminal-pull conditions entirely. In the related DLP CNFs, 88/90 formulas through `n=15` are already UNSAT without hard-core clauses. Proof open |
| Reverse-order and center-controlled folds | Reversing the mirrored right row is the exact right-characteristic shear; choosing the order from the center alternates the new edge between word ends and fixes adaptive XOR to zero at both endpoints | **Exact structural negative/partial:** every symmetric one-/two-step quotient is nonclosed. The `1 -> 0` phase has an all-word lex descent, but the other phase resets it; every fixed order and all 64 boundary-compatible two-half lexicographic products fail by length four. No conjugacy to the inverse-terminal queue is presently known |
| Regular survival-language cocycle | `L_(h+1)=L_0 intersect Q_c^(-1)(L_h)` constructs and minimizes the exact next survival formula | **Exact morph, negative rank result:** minimized DFA size grows from `5/6` to `17,65,257,...` rather than contracting; shortest accepted length grows `1/2,1/2,3,5,5,5,10,...`. Proving that minimum tends to infinity is now the precise language-theoretic mortality target |
| Frontier-distance cocycle | Stack `h+1` queue rows; reading symbol `a` sends `v` to `w_0=a, w_j=g_(v_j)(w_(j-1))`; terminal vertices are exactly the inverse-cone diagonals of hard-core words of length `h+1` | **Uniform graph theorem:** bare distance from `(c,...,c)` to the `F_(h+3)`-vertex terminal set gives the arbitrary-queue minimum; product with the invariant suffix DFA gives the language-cocycle minimum. Their divergence is equivalent. Height extension is a four-sheeted permutation cover whose fiber maps generate `D8`, so no fiber rank contracts. Both distances are exact through `h=12`; proving divergence remains open |
| Actual-right frontier product | Complete finite Rule 30 right-cone membership on each terminal endpoint, with exact height projection and augmented `D8` path action | **Uniform subsystem plus scope correction:** actual targets shrink from `610` to `156` at `h=12`, raising the tail-2 minimum `18 -> 23`; all eight phases remain by `h=7`. Rank descent can prepend artificial state `2`s, so whole-prefix actual-right conditioning is too strong. Apply it only beyond a proved source-ancestry prefix or in the scale block beyond both prefixes |
| Moving endpoint flips | Flipping endpoint coordinate `k` from `1` to `2` preserves hard-core legality and rewrites the inverse cut only on `[k,2k+1]` | **Uniform cocycle:** exact adaptive formula update and interval-cover condition proved; supports may still escape, so no descent yet |
| Endpoint restart and exceptional fiber | `F(0e)=r_0(e_0)F(e)` and `F(2e)=r_2(e_0)F(e)` give the exact phase cycle `12 -> 03 -> 10 -> 00 -> 12`; the only favorable zero-cut fiber has an autonomous five-symbol tail quotient | **Uniform theorem:** the quotient is a pure 32-cycle and every favorable phase is non-hard-core, improving the eventual zero-tail gap bound to `k_(i+1)<=2k_i`; a doubling defect set still satisfies the bound, so separation remains open |
| OpenEvolve/GA rank-zero witnesses | Independent exact reconstruction of every proposed hard-core prefix over a genuine zero-tail cut | **Finite negative:** GA reproduces the `T=23` optimum and reaches survival 107 at `T=96`, but finds no `2T+2` falsifier; no uniform separator follows |

Do not retry the killed fixed-summary classes merely by increasing locality,
moment order, lookahead, or endpoint window.  Their standalone certificates
are uniform negatives for the stated classes.  The variable-seed UNSAT data is
different: both the hard-core and joint sweeps are finite evidence, not a
negative or a theorem.

### Translation of geometric ideas already considered

| Informal idea | Exact version tested | Present status |
|---|---|---|
| Replace touching same-color squares by a digit | Full run-length/boundary-gap sequence | Lossless but unbounded; every tested bounded collapse has an exact collision |
| Collapse pyramids to their sizes or make each pyramid an operator | Ordered gap digits and their D8 carry actions | Basic finite operator summaries do not close; an order-sensitive unbounded offset argument remains untested |
| Subtract left-side from right-side counts | Signed mass, boundary, and contact-count features | Exact oscillating transition multiset rules out a strict additive ranking in that class |
| Count by touching colors instead of rows | Adjacent equal/unequal tiles and boundary counts | Included in the same certified negative class |
| Treat each color switch or next row as a toggle | Odd-row complement and OR/AND-dual phase rules | Exact two-phase composition returns to `F^2`; it is a change of coordinates, not a descent |
| Look for oscillation or a time-varying rule | Period-two summaries and alternating phase transducers | Useful diagnostically; a two-step summary cycle falsifies monotonicity, while the original CA rule itself remains fixed |

Thus the unspent geometric version is not another scalar count.  It would
need to retain the ordered locations of all pyramid/run boundaries and prove a
well-founded spatial statement about that unbounded sequence.

## Smallest counterexamples to remember

- Rule 90 control: finite row `{-1,1}` has zero center forever.
- Rule 30 shallow-control trap: `{-8,-1,6}` alternates through time 14 and
  fails at 15.
- Rule 30 long-control trap: right mask `0x13be` and left mask
  `0xa96bfe30260597f6e6d977d63403b1304cb232655`, supported on `[-164,13]`,
  alternate through time 184 and fail at 185.
- Natural signed summaries oscillate on
  `(2,1,1) -> (4,3,2) -> (6,5,5)` and return to their starting summary.
- Carry action closure: `(2,1,1)` and `(6,21,21)` have the same current D8
  action but different successor actions.
- Full RLE is lossless; only bounded projections are killed.  One solid OR
  run of length `m` becomes `m` unit boundary digits under inverse Gray.

## Independently checkable controls

Latest verified results:

```text
F^2 truth table                         32/32 PASS
two-orbit defect recurrence             64/64 PASS
carry local table                       16/16 PASS
carry/Gray arbitrary frontiers          34,952 PASS
moment/Hasse standalone checks          589,824 PASS
variable-seed SAT thresholds n<=16       95/95 PASS vs direct enumeration
shortest-death DRUP certificates        independently checked through n=17
triangular-correlation word pairs       87,380 PASS through width 8
moving-endpoint K block / append words      5,824 PASS through width 10
aligned endpoint tableau frontiers          34,952 PASS through width 8
Rule 30 radius-eight rows               131,071 PASS
Rule 30 adversarial trace               fail exactly at t=15
Rule 30 finite joint counterexample     alternates through t=184; fails at 185
Rule 90 {-1,1}                          zero through t=128
Rule 30 rho five-zero ANF identity      zero polynomial; 512/512 PASS
Rule 90 five-zero negative control      witness right mask 0x114 PASS
active-core conjugacy                   511 reachable macros PASS
reverse append/cascade                  4,370 / 4,247 arbitrary instances PASS
active-core CNF thresholds              36/36 PASS through core length 7
tail-density controls                   n<=24 table; fixed n=37 counterexample PASS
local-ranking negative certificates     PASS without solver
divergence negative certificate         PASS without solver
actual-right SAT/direct language        126/126 words PASS through length 6
actual-right terminal projections       equality through horizon 12 PASS
actual-right queue/right-seed replay     every reported minimum through horizon 12 PASS
actual-right D8 path action              exact augmented search through horizon 10 PASS
zero-prefix slow/bit-sliced graph         exact equality through length 7 PASS
zero-prefix ordinary/ordered/greedy       242,783 cases through length 22 PASS
zero-prefix tail-3 nonfinal-miss check     zero failures through length 22 PASS
binary-wedge literal/bit-sliced replay     6,152 generated cells PASS
binary-wedge exact census                  all 2^n sources through n=20 PASS for M<=n+1
DLP hard-core relaxation                   88/90 base-UNSAT through n=15; two checked singleton exceptions
```

Core commands:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/derive_and_controls.py
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/verify_negative_certificate.py
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/verify_moment_negative.py
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/verify_divergence_negative.py
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/bilateral_hardcore.py
uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/mortality_sat.py \
  --validate --max-validate 16
uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/quadratic_probe.py
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/endpoint_peel.py
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/right_trace_forbidden.py
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/tail_density.py
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/core_discharge.py
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/core_mortality_sat.py \
  --max-length 20 --max-validate 7
```

## Best next theorem

For a token-compressed logical audit, read `PROOF-STATE-CAPSULE.md` before
this section.  In particular, `(SEP)` is the exact remaining endpoint-orbit
separator, DLP/RW is the weakest current explicit finite-word sufficient
target, and `(BWH+)` is a cleaner but stronger sufficient target.

The cleanest current target is:

> **Binary-wedge horizon `(BWH+)`.**  For every `n>=7`, binary source
> `W in {1,2}^n`, and constant cut `c in {2,3}`, the uniquely forced
> endpoint continuation leaves `{1,2}` within its first `n+2` symbols;
> equivalently `M_c(n)<=n+1`.

This is stronger than DLP but removes both the hard-core language and the
terminal-pull predicate.  By the rotated-Peel identity it is exactly the
exclusion of a binary word `f` of length `2n+2` satisfying
`P^n(I(f))=c^(n+2)`.  The preregistered sharper bound `M_c(n)<=n` is false:
`M_3(15)=16`.  The sufficient bound has no exact failure through `n=20`.
Read `RESULTS-BINARY-WEDGE-HORIZON.md` first.

The high-bit half of this target is already eliminated uniformly.  Once the
first `n` binary source symbols are fixed, requiring high bit one on all
`n+2` wedge outputs uniquely determines the remaining `n+2` binary endpoint
symbols.  The open statement is exactly that the resulting deterministic
defect word is neither `0^(n+2)` nor `1^(n+2)`.  See
`RESULTS-BINARY-WEDGE-HIGH-ELIMINATION.md`.

The logically weaker fallback is:

> **Three-row late-pull diagonal.**  A length-`n` constant-tail scale word
> has no nonfinal endpoint pull `1 -> 2` at rows `n,n+1,n+2`.

For an absolute pull `m=3n+r`, the block `e[n:2n]` sees relative row `n+r`,
so this alone closes both constant-tail separators and the period-two rung.
It is strictly weaker than the alpha and projected-support targets: it uses
no zero-prefix scenarios and makes no claim about early rows.  It has no
failure in the complete hard-core corpus through length 23, all binary words
through length 20, or the recorded long controls.  Its exact diagonal CNFs
are UNSAT through `n=20`, but generic resolution grows and no all-length
triangular proof is known.  Moreover, 88 of the 90 tail/residue CNFs through
`n=15` are already UNSAT after all continuation no-`11` clauses are removed;
only two small instances need a singleton hard-core clause.  A hard-core
length-12 counterexample to a six-symbol tail-only proof shows that the
earlier triangle must still be summarized.  Read
`RESULTS-LATE-PULL-DIAGONAL.md` and `RESULTS-DLP-HARD-CORE-CORE.md`.

The stronger fallback is:

> **Projected diagonal-support lemma.**  At forced row `j`, some adjacent
> zero-prefix scenarios at token `k>=j` differ in `(alpha,beta)` for tail 2;
> for tail 3 the same holds in `(alpha,gamma)` through every nonfinal row.

This gives `s_2(W)<=|W|` and `s_3(W)<=|W|+1`, hence both constant-tail
separators, the rank-zero separator, and the nonconstant period-two
exclusion.  It has zero failures on the complete hard-core corpus through
`|W|=23` but no all-length proof.  The one-credit half-word recurrence is a
second sufficient target.  Read `RESULTS-PROJECTED-DIAGONAL-HALVING.md` and
`RESULTS-SCALE-TELESCOPING.md` before modifying either target.

The stronger alternate target remains **active-core diagonal mortality**:
every aligned core word of length `m` ending in terminal symbol `3` fails a
pin or creates `11` within `m+1` macros.

The exact joint constant bound is false: right mask `0x13be` yields
`J(82,10)` SAT and a finite configuration alternating through time 184.  The
same witness is far below the proposed linear allowance, so it does not
falsify linear mortality.  The coefficient-seven density inequality is also
false; the two weaker balance inequalities in `RESULTS-TAIL-DENSITY.md` remain
the main alternate target.

The active-core statement is stronger and cleaner than the seed-only linear
bound.  A length-`n` seed has active length at most `2n`, so the theorem would
give failure within `2n+1` macros.  Its local CNF `C(m,m+1)` is UNSAT through
`m=34`, but those instances do not supply the missing induction.

Why it suffices: an actual right trace has no `11`, while an infinite
alternating trace would force its finite active core to survive every number
of post-seed macros.  Any finite bound depending on core length therefore
rules it out.  This route is intentionally stronger on the right boundary
than necessary, because it uses only the uniform hard-core consequence of
actual Rule 30 realizability.

What a proof must retain:

- the full cumulative boundary offsets or triangular form, not finitely many
  gap/parity digits;
- the finite-left-support hypothesis (`L` eventually zero);
- actual right-side realizability (`rho` has no `11`), not an arbitrary
  half-plane;
- Rule 30's OR, with Rule 90 failing in the intended branch.

What would kill this exact bound: one terminal-`3` core of length `m`
surviving `m+1` macros while its forced rho avoids `11`.  That witness would
not by itself establish an immortal core or refute period-two mortality.

The exact endpoint formulas do **not** support a literal induction that peels
one seed macro at the cost of two continuation macros.  The length-4/length-3
survival spike is a solver-free obstruction to that semantic implication.
Any renewed endpoint induction must use a proved amortized credit or a
different induction parameter; increasing the local peel radius cannot fix
the false implication.

## Provenance policy

Every `PREREGISTRATION*.md` predates its substantive search.  Every
`RESULTS*.md` records exact commands, qualifications, and failures.  They are
kept for audit/publication but should be read only through the table above.
No `PATH.md` or publication claim should be changed unless the next result is
uniform and its controls plus an independent verifier pass.

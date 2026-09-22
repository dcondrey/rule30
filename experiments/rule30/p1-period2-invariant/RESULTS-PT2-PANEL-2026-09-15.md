# Four adversarially refuted angles on PT2, none reaching the separator

Date: 2026-09-15.

**No survivor. The terminal obligation `(SEP)` at `PROOF-STATE-CAPSULE.md:48` is exactly
as open after the panel as before it, and the chain at `:34-40` gained no new `[U]`
link. One negative structural result (C), two killed routes (B and E), one restatement
of the existing `[U/R]` reduction carrying two repairs (D).**

## 1. Status

Four attack agents ran independently; three were then handed to an auditor and a
reproducer. Labels are the capsule's, `PROOF-STATE-CAPSULE.md:12-18`.

| angle | verdict | refuters |
|---|---|---|
| B, left-edge permutivity | killed `[K]`, computations sound, inference false | auditor kills step 9, reproducer clears every number |
| C, algebraic certificate | negative result, content stands | auditor clears steps 1-7, reproducer finds one wrong number |
| D, `(SEP)` endpoint orbit | restatement, two repairs owed | auditor clears it bar one omission, reproducer falsifies two claims |
| E, mismatch budget at `P=2` | killed, self-reported | never run |

## 2. Angle C: exact Nullstellensatz certificates over raw seed bits

The encoded system is the alternation constraint, not `(PT2)`. For a tight seed support
`[a,b]` of width `w`, work in `B = F2[x_a..x_b]/(x_i^2+x_i)` with `x_a = x_b = 1`
substituted; with `c_t = Tr_0(y)_t` (`docs/rule30/RESULTS-eventual-period.md:25`),
`g_t = c_t + (t mod 2)` and `D_t = c_t + c_{t+2}`, the ideal is
`J_h = <c_0, c_1+1, D_0..D_{h-2}> = <g_0..g_h>`, and in `B` every ideal is a vanishing
ideal, so `1 in J_h` iff the survivor set `V_h` is empty. Each placement is thus a
finite UNSAT instance over raw seed bits refuted by a certificate `1 = sum_t h_t g_t`;
`(PT2)` is the all-width statement they do not reach.

The census is complete on its grid: all 88 placements with `w <= 11` and `a in [-w,1]`,
that is `w+2` per width with `sum_{w=1}^{11} (w+2) = 88`, die at a finite
`h*(w,a) <= 15`, the maximum `h* = 15` at `(w,a) = (9,-9)`, and every certificate
multiplies out to `1` in `B` in both formulations. `[C]` Maximal minimal multiplier
degree by `w = 1..11` is `0,0,0,1,1,1,2,2,2,3,3`, equal to `floor((w-1)/3)` on this
range, and at `w = 11` degree-3 multipliers are needed in 7 of the 11 placements with
`h* > 0`, out of 13. Part D's forced-left fiber `L_j(R)` over the zero right half is
constant at `L_4 = 0` for all `b` (`docs/rule30/RESULTS-eventual-period.md:200`),
`L_8 = 0` for `b <= 5`, `L_12 = 0` for `b <= 2`, `L_21 = 1` for `b <= 3`.

Refuter corrections, all from the reproducer. C stated `L_12 = 0` for `b <= 3`; its own
`run_w11.log` prints `constant L_j: {4: 0, 8: 0, 21: 1}` at `b = 3` with `deg L_12 = 3`,
and the refuter's independent forcing agrees, so the bound is `b <= 2`. C's "deg `L_j`
saturates at `b` or `b-1` for `j >= 7`" fails at `b <= 5, j = 8`, where `L_8 = 0`, a
constant the same step lists. C's "7 of 11" is 7 of the 11 nontrivial placements out of
13. An independent reimplementation sharing no code matched all 88 on `h*` and minimal
degree, 0 mismatches.

The conclusion is negative and narrower than "no bounded-degree certificate": the data
establishes exactly that minimal static Nullstellensatz multiplier degree is not
constant on `w <= 11` `[C]`, killing a uniform degree `<= 2` `[K]` since `w = 10` and
`w = 11` need 3. Maximum observed degree is 3, so degree `<= 3` is not refuted, and the
staircase is an 11-point observation with no mechanism claimed. Nothing here touches the
`[R, OPEN]` statement at `:48`. Named next step: polynomial-calculus refutation degree
of the same systems at `w <= 11`; only static degree was measured and PC degree can be
bounded where NS degree grows, so if it also grows the direct-seed F2 route belongs in
the capsule's killed table.

## 3. Angle B: killed

Step 9 is the fatal step. It identifies the abstract cut tails `2^omega` and `3^omega`
of `RESULTS-RANK-ZERO-REDUCTION.md:166-175` with the `D`-lines touching the left edge,
which is proved nowhere and false on the archive's own frontier
`A_j = x(T-j,-j), B_j = x(T-1-j,-j)` (`docs/rule30/RESULTS-alt-trace-fiber.md:877-878`),
the line `t-x = T`, where B's `D_delta(tau) = s(tau, a+delta-tau)` lies on
`t+x = const`. On the control seed `{-8,-1,6}` that frontier's deep carry tail is
`0^omega` at `T = 20, 30, 40`, which is rank zero; the `2^omega/3^omega` tails arise
only at the first infinite shifted cut over an artificial 2-prefix (same file,
`:178-180`). The match is also a selection: the adjacent lines `a-2..a+1` carry tails
`0,2,3,1`, every symbol of the alphabet. `[K]` Claims (1) and (3) restate the left-frame
half of the capsule's killed row "Static right-boundary penetration" at `:191`.

Verified correct: the anti-diagonal recurrence
`D_delta(tau+1) = D_{delta-2}(tau) XOR (D_{delta-1}(tau) OR D_delta(tau))` with
`D_{-1} = D_{-2} = 0` and `D_0 = 1` from `(EDGE)`
(`uc/r1-r1zero-prove-driven-lhp-column-minus-one-aperiodic-structural/PROOF.md:129-131`),
the eventual-period profile `(1,1,1,2,1,2,2,1,4)` for `delta = 0..8` on all 511 seeds of
width `<= 9`, and the single-cell onsets of eventual period 2,4,8,16 at depths
3,8,29,400, matching `:191`.

## 4. Angle E: killed, on its own evidence

E is the one angle whose refuters never ran, so the verdict is uncorroborated. The route
is the `P=2` mismatch budget of `docs/rule30/RESULTS-r1-mismatch-followup.md:20,45-48`,
budget (3) at `:54`, against the admissible zero right row `R = 0` of the driven right
half-plane. Measured: `M_2(2^20) = 224,662 = 0.2143N`, with minimum `0.0356N` at
`q* = 5` over all even lags `P <= 2048`, both linear in `N`, against a budget needing
`M_P(N) >= floor(log2((N+2)/2)) = 19` at `N = 2^20`. A contradiction needs a
sublogarithmic count, ruled out to `P <= 2048`.

The only positive output is the exclusion of 40 right rows of width `<= 10` by prefix
certificates closed under the 4-step driven map, 22 of the 28 period-4 phase01 rows and
18 of the 22 period-4 phase10 rows. `[C]` Not the zero row and not the 984 and 989
unlocked rows, so it does not narrow `(PT2)`. The route-death rests on measurement to a
finite horizon, not on an identity, so no `[K]`.

## 5. Angle D: restatement with repairs owed

D restates the existing `[U/R]` reduction, `RESULTS-CONSTANT-TAIL-QUEUE.md` section 4 at
`:118` with the frontier graph's (5) at `RESULTS-CONSTANT-TAIL-FRONTIER-GRAPH.md:60` and
(13) at `:255`: `(SEP)_c` is equivalent to "no hard-core `E` has `I(E)` eventually
constant equal to `c`". No new link.

Its correct diagnosis is the angle's value. The frontier report's named obstruction, no
state bound uniform in `d` for the `4^d` driver (same file, `:236-239`), is partly an
encoding artifact: orbit points at level `d < 43934` are eventually periodic with period
in `{1,2,4,8,16}`, leaving an `O(d)` transient plus `O(1)` universal cycle data. That
transient, which has full subword complexity, is the real obstruction, and the preperiod
bound `K_d <= 3 sum_{j<=d} p_j <= 48d` is loose by an order of magnitude, observed `K_d`
being 17 to 25 at `d = 9..15` against a bound in the hundreds.

Two errors, both from the reproducer against D's own outputs. Claim 3's `K_d` comparison
is false for `c = 3`: there `u = ()` gives `K_38 = 25` and `K_39 = 26`, above the
claimed `K_d <= 14` for `d <= 39`, and the `c = 3` witnesses give 13, 11, 23 rather than
the claimed 17 to 25; it holds only for `c = 2`. Claim 1's `(=>)` direction does not
land in `O_c` as argued: with `u_i = I(sigma^i E)_{n-i}` the word `u` contains the
symbol `3` in 314 of the 407 checked instances, while `O_c` is defined over `{0,1,2}^*`,
and `controls.py:94` asserts only `T_word(...) == col`, never the alphabet.

The repair named by the synthesis is the `g_s(1) = g_s(3)` normalization at
`RESULTS-CONSTANT-TAIL-QUEUE.md:93-102`, replacing every nonleading `3` by `1` without
changing the column, plus restating the `K_d` sentence per `c`; the refuter confirmed it
on 407 of 407 instances. D then leaves one live question, whether the `O(d)` transient
admits a bound meeting a boundary constraint; nothing in its data suggests it does.
Measured 2026-09-16 over the `2^n` reachable fibres (`RESULTS-DEMAND-TRANSIENT.md`):
the maximum pre-period of the pinned-cut recursion is `n + 9` or `n + 10` at `n = 10..15` and about
`2n` by `n = 20..22`, attained by narrow sources, so on that range no bound
`beta n + C` with `beta < 1` exists and the one-seed `K_d` above is the small end.

## 6. Reproduction

Angle C's certificate script and its width-11 log are checked in beside this report as
`pt2_panel_C_anf_cert.py` and `pt2_panel_C_run_w11.log`. It is pure standard library and
holds no scratchpad path, so it was copied unmodified; from the repository root,
`uv run --no-project python experiments/rule30/p1-period2-invariant/pt2_panel_C_anf_cert.py 1`
gives `rc=0` in 0.5 s at the smallest accepted width. The full width-11 run also
finishes inside two minutes, 16.5 s here against the 23.9 s the angle recorded, with
output identical to the checked-in log apart from the `elapsed` line. Part A's `t=1` row
prints `MISMATCH` before `control PASS` because the law checked, `deg f_t = 2t-1`
(`docs/rule30/overnight/RESULTS-anf.md`), starts at `t = 2`; that row is off-law by
construction, not a failure.

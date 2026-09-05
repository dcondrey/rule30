# Lemma backlog for Rule 30 Problem 1 via the rotated wedge

Persistent, ranked, machine-screened.  Every row is a precise statement with a
kill test.  Killed rows stay in the table so they are never re-proposed.
Status vocabulary: `untested`, `held to n=..`, `killed: <counterexample>`,
`ill-posed: <why>`, `duplicate of <id>`, `in flight: <where>`, `proved`.

Sources: `R1-ext` = the 32-entry external LLM backlog of 2026-09-02, triaged
here; `WF` = the multi-agent workflow `rule30-p1-attack` (`uc/`), merged when
it reports.  Screening scripts: `backlog_screen_r1.py` and its log.

Standing context: `uc/BRIEF.md` (exact language), `BACKLOG-PROMPT.md`
(generation prompt), `PROOF-STATE-CAPSULE.md` section 5 and `PATH.md`
section 7.3 (killed mechanisms and obstructions).

## 1. Live rows, ranked by p_true x value

| id | statement (short) | implies | kill test | status | nearest killed row | notes |
|---|---|---|---|---|---|---|
| L5-ALLORB-CONST | `N_k(n) <= 4 * 2^n * 0.47^k` for all `n, k` | RW-alpha, `alpha = 0.92` | exhaustive `N_k`, `n = 4..16` | killed: `N_8 = 6 > 4.9` at `(9,3)`, small-number tail | naive `2^(n-k)` (false, ratio 4) | This IS the rate target in counting form; a proof is the open problem, the test only calibrates the constant |
| L7-PERIODIC-SOURCE-CAP | periodic sources `s^omega`, `p <= 28`, admissible run `<= n + 2` | structured-family exclusion | all `2^p` patterns, `p <= 28`, `n <= 400`, both hard-core readings | **held to `p = 28`, `n = 400`** (`periodic_family.py`, `uc/r1-skeptic/periodic_family_p28.log`): 0 counterexamples, worst-case excess `run - (n+2) = -3` at `n = 9`, `c = 3` | bounded SAT tables | Cheap and reaches `n = 400`; a positive result forces any counterexample to be aperiodic in `W`. Prior "held to n=40, pattern 2212" citation of `fib_source_check.py` did not reproduce (that script is vacuous, see `uc/r1-skeptic/FIB-SOURCE-REPRO.md`); replaced with the actual source of this claim |
| L1-DIAG-DEGREE (corrected) | degree of `E(e_u)` in the `2n` diagonal bits is `u - n + 1` | structural | Moebius over `4^n` diagonals, `n = 3..7` | measured: `deg E(e_u) = 2u-1` for `u <= n`, then full | ANF of centre bit (inert) | As submitted it was ill-posed (`T[u][n] = c` is the constraint, not a function); corrected to the edge defect.  Source-bit degree is full; diagonal coordinates may differ, and that would matter |
| L1-DIAG-INJ-MOD | diagonal -> forced suffix `e[n:]` injective | counting transfer | all `4^n`, `n = 3..7` | killed: fiber grows to 8.2 at `n = 7` | centre-trace injectivity (killed) | `diag_to_edge` validated against the kernel first |
| L10-PERSIST-INFLUENCE | every source bit flips the hit vector w.p. `>= 1/4` | none directly | all `2^n`, all `i`, `n = 6..11` | killed: bit-0 influence 0.125 -> 0.052 over `n = 6..11` | no-forgetting probe (measurement) | The implication to a per-column entropy loss is not established; the test formalizes 9.2 of the RW doc |
| L6-COND-HIT-GAP | hit fraction given last 3 forced symbols `<= 0.44` | RW-alpha | bucketed exhaustive, `n = 8..13` | killed: 0.824 in a 34-sample bucket | BWH+ retired | Prediction before running: the E-hit is ~1/2 and hard-core is the separate 3/4 factor, so 0.44 should FAIL |
| L6-Z-DENSITY-FORCE | `|Z|/m` in `[0.17, 0.33]` on surviving columns, `u >= n+5` | none directly | exhaustive, `n = 8..14` | killed: density 0.029 to 0.429 | final local patch (killed) | Prediction: fails by fluctuation alone (`sd ~ 0.1` at `m ~ 20`) |
| L6-FORBIDDEN-FACTOR | no hard-core 6-block co-occurs with 6 consecutive hits | RW (implication broken) | census of 6-blocks inside 6-hit runs, `n = 6..12` | killed as stated; all 21 blocks occur by `n = 17` | one backward source defect | Implication is false as stated (a single forbidden factor is avoidable); kept as a census of the forced-symbol language |
| L10-FIB-TRANSFER | survivors' forced-symbol block growth `<= 1.45` vs `phi = 1.618` | weak | distinct `m`-blocks, `n = 10..13` | killed: RW block language = hard-core through length 7, ratio = phi (section 10) | none | |
| L4-TWISTED-GAP / L4-MIXING-SKEW (corrected alphabet) | twisted transfer operator on `(h,F)` has spectral radius `< 0.9` | heuristic only | 4x4 twisted matrix with empirical letter frequencies | discarded; corrected model eigenvalue 0.572, heuristic only | fixed finite quotient | Submitted with the wrong alphabet (`(1,1)` is cell 0 and common; `(1,0)` is the impossible letter).  Even corrected, the input to column `u` is column `u-1`, not i.i.d. letters, so a gap in this model implies nothing about the orbit |
| L3-QUAD-COUPLING | cross-term rank of the bilinear form between window halves `>= m/2 - 2` | RW-alpha (unsupported) | unclear | untestable as stated | holonomy-defect word | The bilinear form in letter variables is triangular of full rank trivially; the letters are not free.  Needs a precise statement about which matrix |
| L7-DIAG-SAT-UNSAT-RANGE | RW UNSAT for `n = 21..30` by SAT on the diagonal encoding | RW on a finite range | complete SAT | in flight: WF skeptic lens (`uc/*/rw_sat.py`) | bounded SAT tables | A SAT model would be an RW counterexample, the most valuable possible outcome |
| L10-SAT-CORE-SCALING | UNSAT core grows `>= exp(0.1 n)` | meta-evidence | proof-logging SAT | deferred | resolution bounds (killed for `c_n`) | Does not advance a proof; run only if SAT runs happen anyway |
| L11-RW-TERMINAL-DEFECT | `|H_r(n)| / 2^n` (the hard-core + `12a`-terminal RW candidate population) decays with `n`, `r = 0,1,2` | motivates a shrinking-population argument for RW where `(BWH+)`'s full-degree obstruction blocks the unrestricted version | exhaustive `H_r(n)` count vs `2^n`, both `c`, `r = 0,1,2` | S1'/S2 done and empty (`RESULTS-PSI-ANCESTRY-R-EXTENSION.md`). Section 4 measurement now run (`RESULTS-RW-TERMINAL-DEFECT-H-POPULATION.md`, `rw_population_h.py`): `|H_r(n)| = 0` exactly for every `n = 1..16`, every `r`, both `c` — stronger than the stated decay question, the population is already empty, not just shrinking. Exhaustive, not sampled; control #1 (two independent constructions) agreed on every word. Not yet extended past `n=16`, and no structural proof of the emptiness exists yet | full-degree `Delta` (obstruction, not kill) | `PREREGISTRATION-RW-FORCED-TERMINAL-DEFECT.md`; fires the capsule section 7 fallback; the collapse lemma (RW witness existence = `literal_extension` surviving hard-core+`12a`) is resolved by reading the code, no run needed. Next: look for why `H_r(n)` is forced empty (an invariant of `literal_extension`'s row-by-row forcing), not just extend the census |

## 2. Killed or closed on arrival (no compute needed)

| id | status | reason |
|---|---|---|
| L3-QUAD-RANK | killed: `psi_degree_20260902.log` | Assumes `E(T[u][n])` is quadratic in source bits.  Degree is `n-1` or `n` at every `n = 4..15`.  The quadratic form is in column letters |
| L3-ARF-BALANCE | killed: same | Arf invariant of a form that is not quadratic in those variables |
| L8-ZERO-PROG-DENSITY | killed: P2 data | Claims progression zero-density tends to 0; the centre column's zero density is about 1/2 (Problem 2) |
| L10-COMMUTE-GROUP | killed: `rw_margin_20260902.log` and direct substitution | `c = 2` vs `c = 3` hit counts differ at every `n` (n=15: 9 vs 8; `N_1` 12134 vs 12533); the claimed conjugation `step_{e^3} = g step_e g^-1` fails (`F + (h+1)b` vs `F + hb`) |
| L7-CYLINDER-BARRIER | killed: `rw_margin_20260902.log` | The `0.7n` cap is exceeded by the unconstrained census at `n = 9` (8) and `n = 12` (9); fixing a suffix only shrinks the set |
| L8-GLOBAL-PARITY-ODD | killed: Rule 90 filter plus coordinate conflation | Rule 90's centre column has period 1, which is odd; the entry says Rule 90 "has even-period examples", which is the wrong control.  Also uses `H` on forward cells (see next table) |
| L5-SURVIVOR-CONSTANT | duplicate of L5-ALLORB-CONST | Ratio form; at tail levels with `N_k < 5` the ratio fluctuates by small-number effects and the kill would be uninformative |
| L2-SURVIVOR-COUNT-POT | duplicate of L5-ALLORB-CONST | `V_k` decreasing is the same ratio bound with base `2^-1.1` |
| L8-JOINT-LOGDELAY | duplicate: register row 37 plus obstruction A | "Predict column 1 from a centre window of radius `K log t`" is finite-delay reconstruction (killed) with the delay allowed to grow; the kill test (train a predictor) is not a lemma test |

## 3. Ill-posed as submitted

| id | defect |
|---|---|
| L9-H-PROPAGATION, L9-ZERO-CONNECTIVITY, L9-LINEAR-RESTRICT-ZERO | `(H, E)` are coordinates on the four-state inverse-cone carry cells.  Forward-diagram cells are bits; `H(T[t][0])`, "E=0 islands" and "E-drift on zero positions" are undefined there.  A forward-diagram version needs the carry encoding stated explicitly |
| L1-DIAG-TRIANGULAR, L1-DIAG-SEPARATION, L5-ENTROPY-KHIT, L1-DIAG-DEGREE (as submitted) | In the diagonal form all `4^n` diagonals are solutions with every hit by construction; `T[u][n] = c` is the constraint, not a function of the diagonal.  The free quantity is the edge defect `E(e_u)`.  The true part of L1-DIAG-TRIANGULAR (bijective parametrization) is already verified in the brief |
| L4-DRIFT-POSITIVE | Wrong alphabet, and "drift" on `Z2 x Z2` has no meaning (no order) |
| L2-WEIGHTED-GLOBAL-POT | The hit term is added by definition; the stated bound gives hits `<= 2^(n+1)`, vacuous |
| L2-LEX-POTENTIAL | Lexicographic order on a list of hashes is arbitrary; nothing is being measured |

## 4. Rejected-ideas list carried from the generator

Matches the killed-mechanism table and the register; nothing new, nothing
wrong.  Retained in `BACKLOG-PROMPT.md` section 4.

## 5. Round log

- 2026-09-02 R1-ext: 32 entries.  6 killed on arrival, 9 ill-posed, 4
  duplicates, 1 untestable, 1 deferred, 1 in flight, 10 screened
  (`backlog_screen_r1.py`, section 6): 1 held, 1 measured, 1 inconclusive
  then killed on the thorough rerun (section 10), 7 killed.
- 2026-09-02 PDF: 35 IDs, 5 stated.  2 closed on arrival, 3 screened
  (`backlog_screen_r2.py`, section 8): 2 killed, 1 measured.

## 6. Round-1 screening results (`backlog_screen_r1_20260902.log`)

| id | verdict | evidence |
|---|---|---|
| L5-ALLORB-CONST | killed at `(n,c,k) = (9,3,8)`: `N_8 = 6 > 4.9` | small-number tail; `C = 8` would survive the same range; the statement is the rate target itself |
| L10-PERSIST-INFLUENCE | killed | influence of bit 0 is 0.125 at `n = 6`, 0.052 at `n = 11`, decreasing; the light cone reaches bit 0 through two cells of column `n-1` |
| L6-COND-HIT-GAP | killed | conditional hit fraction 0.824 (history `122`, `n = 13`, 34 samples); average is ~1/2 as predicted |
| L6-Z-DENSITY-FORCE | killed | `|Z|/m` from 0.029 to 0.429 on surviving columns |
| L1-DIAG-INJ-MOD | killed | `4^n` diagonals give `4^n / 8.2` distinct forced suffixes at `n = 7`; fiber size 1.8, 2.7, 3.8, 5.6, 8.2 for `n = 3..7`, growing |
| L7-PERIODIC-SOURCE-CAP | **held to `p = 28`, `n = 400`** (`periodic_family.py`) | forced continuation from periodic `W`, `p <= 28`: 0 counterexamples, worst-case `run - (n+2) = -3` at `n = 9`, `c = 3`; fully periodic `f`: same bound, never exceeded |
| L6-FORBIDDEN-FACTOR | killed as stated; census kept | `212121` co-occurs 12 times; absent from all 6-hit runs through `n = 12`: `121221`, `122121`, `212212` |
| L1-DIAG-DEGREE (corrected) | measured | `deg E(e_u) = 2u - 1` for `u <= n`, then `2n - 1` or `2n` (full) for `u >= n`; diagonal coordinates do not lower the degree |
| L10-FIB-TRANSFER | inconclusive | sample-limited at `n <= 13` |
| L4 transfer operator | section J discarded | the twisted-operator construction was wrong for an affine action; plain eigenvalues in round 2 |

## 7. PDF backlog of 2026-09-02 (`candidate_lemmas_for_the_rule_30_period-two_attack`, 7 pages, 35 IDs)

Only five entries carry a statement (pages 4 to 7).  The other thirty are
names in a ranking table and cannot be screened until stated: ordered-zero-w2,
cocycle-block-gap, hit-language-pressure, hard-core-fibres,
phi-rank-conditioned, cocycle-return-defect, zero-set-run-transfer,
ordered-inversion-potential, entropy-with-memory,
fibonacci-conditioned-pressure, phi-derivative-pairing, all-orbits-transfer,
cocycle-singular-value, hard-core-extension-loss, phi-arf-obstruction,
forced-orbit-lex-potential, hit-gap-renormalization, hard-core-boundary-
pressure, phi-composition-degree-drop, cocycle-word-expansion,
periodic-source-search, suffix-cylinder-extension, diagonal-sat-family,
phase-compatible-family, zero-set-cocycle, zero-set-density-transfer,
trace-to-zero-set-extension, period-uniform-separation,
inverse-cone-periodic-core, orbit-closure-zero-persistence.

| id | status | reason or test |
|---|---|---|
| diag-fiber-four | killed: `rw_margin_20260902.log` | claims `C * 4^-j * 2^n` survivors after `j` hits, i.e. two bits per hit; measured 1.35; at `n = 16, j = 5`: 765 survivors vs `4 * 65536 / 1024 = 256` |
| diagonal-prefix-rank | ill-posed / trivial | hit histories are `1^k 0^*`, image size `<= n + 3` |
| diagonal-martingale | screening: `backlog_screen_r2.py` K | count coordinates determined by the others on `S_k` |
| diagonal-cube-separation | screening: r2 L | `C_needed` over subcubes fixing 1..3 symbols |
| diagonal-permutation-cylinder | screening: r2 M | free bits per survivor, largest box, cover lower bound |

## 8. Round-2 screening results (`backlog_screen_r2_20260902.log`), PDF entries

| id | verdict | evidence |
|---|---|---|
| diagonal-martingale | measured, not established | Coordinates determined by the others on `S_k` grow with `k` (n=12, c=2: 1, 2, 5, 8, 11, 11, 12 symbols at `k = 0..6`), but per-coordinate determination is not additive and the test does not exhibit an ordering.  The entry's sequential-fiber claim needs the ordering test, not this one |
| diagonal-cube-separation | killed for `C <= 8` | `C_needed = 13.2` at `n = 8, k = 1`; 23.3 at `n = 12, k = 5`; grows with `k`.  Survivors cluster in subcubes |
| diagonal-permutation-cylinder | killed | Largest sub-box inside `S_k` has dimension `<= 3` at `k = 0` and 0 or 1 for `k >= 3`; nearly every survivor is isolated (no single bit flip stays in `S_k`).  A cylinder cover needs about `|S_k|` cylinders, which grows exponentially in `n` at fixed `k` |
| transfer operator (corrected) | heuristic number only | i.i.d.-letter model on `(h,F)`: eigenvalues 1, 0.572, 0.463, 0.463.  Says nothing about the orbit |

Two facts from this round worth keeping regardless of the entries:
`S_k` in diagonal coordinates is a set of isolated points for `k >= 3`, and it
clusters in low-codimension subcubes with a constant that grows with `k`.
Both are the diagonal-coordinate form of the no-forgetting and clustering
results already recorded in `RESULTS-RW-LINEAR-SLACK.md` and
`PREREG-psi-constraint-counting.md`.

## 9. Workflow status

`rule30-p1-attack` (`wf_1e280a58-776`) died at 59 minutes: 12 of 14 agents
hit the session usage limit (resets 23:30 PT), and the script's `compact()`
lacked a null guard on failed screens.  Two route agents (`survivors`,
`entropy`) completed and proposed lemmas; their screens did not run.  Partial
artifacts under `uc/r1-*` (4 MB).  Guard fixed in the script file; resumable
with `resumeFromRunId` after the reset.

## 10. L10-FIB-TRANSFER, thorough (`fib_transfer_screen.py`, `fib_transfer_screen_20260902.log`)

Pooled over `n = 10..17`, both `c`, every `W`, whole forced word, blocks
strictly inside the forced part.  Three languages: `H-only` (forcing alone,
the BWH+ continuation), `hit` (forcing plus every column a hit, no
hard-core), `RW` (forcing, hit, hard-core).  The log's `Fib(m+2)` column is
off by one index; the correct hard-core counts are given here.

| m | binary `2^m` | hard-core | `B_H-only` | `B_hit` | `B_RW` | RW / hard-core |
|---|---|---|---|---|---|---|
| 2 | 4 | 3 | 4 | 4 | 3 | 1.00 |
| 3 | 8 | 5 | 8 | 8 | 5 | 1.00 |
| 4 | 16 | 8 | 16 | 16 | 8 | 1.00 |
| 5 | 32 | 13 | 32 | 32 | 13 | 1.00 |
| 6 | 64 | 21 | 64 | 64 | 21 | 1.00 |
| 7 | 128 | 34 | 128 | 128 | 33 | 0.97 |
| 8 | 256 | 55 | 256 | 227 | 37 | sample-limited |

**Verdict: killed.**  The RW forced-symbol language contains every hard-core
block of length `<= 6` and 33 of 34 at length 7; its block-growth ratio is
1.60 to 1.67 over `m = 3..7`, i.e. the golden ratio, not `<= 1.45`.  The hit
constraint removes no blocks at all (`B_hit = 2^m` through `m = 7`); the only
block-level constraint on forced symbols is hard-core itself.  This is the
symbol-language form of the no-forgetting and full-degree results: the hit
constraint is global, not local, and leaves no local footprint.

The one length-7 hard-core block not seen through `n = 17` is `1221222`.  The
hit-only language contains it, so hard-core is not what removes it.  Checked
at `n = 18, 19` in `fib_absent_check_20260902.log` (result appended below).
The three length-6 blocks reported absent in round 1 section G (`n <= 12`)
all occur by `n = 17`; that absence was sampling.

**Addendum.**  `1221222` occurs 67 + 6 + 32 + 8 = 113 times in RW runs of
length `>= 7` at `n = 18, 19` (`fib_absent_check_20260902.log`).  Its absence
through `n = 17` was sampling.  Through length 7, the RW forced-symbol
language is exactly the hard-core language at block level.

## 11. Third external batch (30 entries, 2026-09-02): triage

Three recurring defects, on top of the two from earlier batches:

- **Self-defeating.** `hit-bit-polynomial-degree-n`, `fourier-uniform-bound`
  are statements about the indicator of the RW counterexample set.  Where RW
  holds that set is empty, the indicator is identically zero, and both
  statements are false exactly when the target is true.
- **Monotone hit vectors.**  An admissible run stops at its first miss, so the
  hit indicator is `1^j 0^*`.  `hit-language-window-bound` (at most `k+1`
  words), `hit-language-entropy-bound` (trivially sub-exponential),
  `hit-window-pairwise-distance` (`1^j 0` and `1^(j+1)` are at distance 1),
  `hard-core-forced-symbol-support-two` (the next symbol is forced; "at most
  one" is vacuous): trivial or dead on arrival.
- **Diagonal form, again.** `diag-determinant-full-rank`,
  `polar-form-nondegenerate`, `diag-hit-code-distance`: constant functions.
- **Wrong object.** `no-zero-period-match`, `zero-set-injective-reconstruction`,
  `zero-density-half` define the centre column as `T[t][0]` from a seed in the
  inverse-cone triangle, which is not Rule 30's centre column.  For the real
  one the first is the prize's own data check (obstruction H) and the third is
  Problem 2.

| id | status | evidence |
|---|---|---|
| half-survivor-step | killed: `backlog_screen_r2_20260902.log` K | `n = 9, c = 3`: survivors 6, 6, 6, 6 at `k = 5..8` (ratio 1.0); `n = 12, c = 2`: 2, 2.  The clusters are fibres of one endpoint state (`RESULTS-CLUSTER-ANATOMY.md`): in states the run is 1, 1, 1, 1 |
| zero-distance-affine-space | killed: `psi_structure` census | unstopped defect word is `Psi`; at `n = 15` it is `1^16 0`, distance 1 from the constant line; constants at `n = 5, 6` give distance 0 |
| hit-language-all-ones-rare | killed: `rw_margin_20260902.log` | every `n >= 9` has a run `>= 8`, so `R(N)` is linear |
| finite-exhaustion-depth | killed literally at `n = 3` (`E = 5 > 4.4`); held for `n = 4..28` | this is (RW-alpha) with `alpha = 0.8, C = 2`, restated as extinction depth; not a lemma with a proof route |
| second-half-naive-bound | vacuous | extinction precedes `k = n` at every tested `n`, so the second-half bound is `0 <= 2^(n-k)` |
| complement-pin-no-run | duplicate of RW | RW already quantifies over both `c` |
| sat-diagonal-nosolution, finite-exhaustion-r0-residual | duplicate of the census | see the SAT extension below |
| transfer-op-spectral-gap | ill-posed | prefixes of length `n` map to length `n+1`; not a square matrix.  The decay it wants is the measured 1.35 bits per column |
| same-forward-orbit-collision | duplicate of register row 31 | its kill test compares infinite traces |
| period-trace-q-finite | untestable | finite simulation cannot certify eventual periodicity |
| tri-inj-forced-suffix, forced-column-prefix-uniformity, survivor-3over4-bound, no-small-period-source, unstopped-language entropy, group-cocycle-4-cycle, affine-translation-nonzero | screening: `backlog_screen_r3.py` | results in section 12 |

## 12. RW by complete SAT to n = 30 (from the dead workflow's skeptic lens)

`uc/r1-skeptic/rw_sat.py`, logs `rw_sat_check.log`, `rw_sat_scan.log`,
`rw_sat_n29_c3.log`, `rw_sat_n30_20260903.log`, `rw_sat_r_grid_20260903.log`,
`gap_29_2_3.log`, `gap_30_{1,2}_{2,3}.log`.
The SAT encoding of RW (`r = 0`, both `c`) is gated against the census at
`n = 9..16`: satisfiable at exactly the census's deepest run and unsatisfiable
one deeper, at every `n` and both `c`.  **UNSAT at every solved cell**, no SAT
model anywhere:

- `r = 0`, both `c`, `n = 16..30` — `rw_sat_scan.log` carries `n = 16..29`
  (`c = 2` only at `n = 29`, where the 3600 s budget stopped the scan after
  11796 s), `rw_sat_n29_c3.log` the `n = 29, c = 3` cell, and
  `rw_sat_n30_20260903.log` both `n = 30` cells (10403 s and 13243 s).
- `r = 1, 2`, both `c`, `n = 6..30` — `rw_sat_r_grid_20260903.log` carries
  `n = 6..29` less the `n = 29, r = 2, c = 3` cell (budget stop at 12747 s),
  which is in `gap_29_2_3.log`; the four `n = 30` cells are in `gap_30_*.log`
  (20478 s to 27975 s).

**The RW census therefore stands at `n = 30`, for `r = 0, 1, 2` and both `c`.**
(Corrected 2026-09-05: this section previously said `n = 28` for `r = 0`, which
predated the `n = 29`/`n = 30` logs above.  Do not re-cite the `n = 28` figure.
Separately, do not conflate this with the *exhaustive* population result
`|H_r(n)| = 0` for `n = 1..16` in `RESULTS-RW-TERMINAL-DEFECT-H-POPULATION.md`:
that is a weaker, necessary-only statement over a different, smaller range.)
Obstruction H applies as always: this is a bounded horizon, not an all-`n`
proof.

## 13. Round-3 screening results (`backlog_screen_r3_20260902.log`)

| id | verdict | evidence |
|---|---|---|
| tri-inj-forced-suffix | killed | `W -> Q_n(W)` is 7.6-to-1 at `n = 16` (65536 sources, 8641 distinct continuations); restricted to hard-core `W` it is 5.4-to-1.  The forced continuation forgets most of the source |
| forced-column-prefix-uniformity | **held to n = 20** | `max N_k / 2^(n-k+2) = 0.75` at `(9,3,8)`; for `n >= 4` the constant 3 suffices, `n = 3` needs 4 |
| survivor-3over4-bound | held to `n = 20`, very slack | measured decay is `2^-1.35` per column against the claimed `3/4` |
| no-small-period-source | **held to n = 100** | 196 hard-core periodic patterns, `p <= 9`, fully periodic `f`: no run ever exceeds `0.6n` |
| hit-language entropy (unstopped reading) | killed | for fixed `k`, the set of length-`k` `Psi` prefixes fills `{0,1}^k` as `n` grows (all 256 length-8 words by `n = 13`, 1019 of 1024 length-10 by `n = 15`).  Side fact: only about `2^(0.82 n)` distinct `Psi` words arise from the `2^n` sources |
| group-cocycle-4-cycle | killed | column affine maps have orders 1, 2, 4 in proportion 13:62:25 |
| affine-translation-nonzero | killed | translation is zero on 25 percent of forced columns |

## 14. Fourth external batch (10 entries) and round-4 screening (`backlog_screen_r4_20260902.log`)

Every entry but two is stated on `I_u(x) = E(T[u][n])(x)` over diagonal
vectors, which is the constant `E(c)`.  Screened in the source reading (`W`,
unstopped defect word `Psi_n(W)`), the only reading with content.

| id | verdict | evidence |
|---|---|---|
| no-three-term-affine-relation, palindrome-free-hit-blocks, diagonal-fold-palindrome-defect | killed on arrival | `Psi_15 = 1^16 0`: window `1111` occurs, palindrome of length 16, fold weight 1.  In the stopped reading a run of `j` hits is `1^j` |
| tribonacci-survivor-recurrence | killed on arrival | `n = 9, c = 3`: `S_8 = 6 > (6+6+6)/4` |
| source-bit-toggle-sensitivity | killed | min Hamming distance between `Psi(W)` and `Psi(W with one bit flipped)` is 0 at every `n = 6..15` |
| reverse-source-hit-distance | killed | min distance under source reversal is 0 to 2 against a required `L/5` |
| complement-toggle-hit-distance | killed | min distance under `1 <-> 2` complement is 1 or 2 against `L/6` |
| reverse-affine-cancellation | killed | `A(q) o A(q^R)` is the identity on 4910 of 10272 forced columns |
| spiral-diagonal-parity-ladder | killed | longest constant run of the spiral parity is 7 to 10 against `n/4` |
| fibword-source-family-eliminated | see `fib_source_check_20260902.log` | the entry's claim that the Fibonacci word has no `11` is false (`12112...`); `backlog_screen_r4.py` section Y omitted the hard-core check and printed the known BWH+ constant at `n = 5` as a counterexample; it is not one.  Rerun with the check below |

**fibword-source-family-eliminated, corrected run** (`fib_source_check.py`):
zero hard-core factors of length `2n + 2` exist for `n = 4..100`; the Fibonacci
word contains `11` with bounded gaps, so no factor is an admissible source.
Vacuous, not a family.

## 15. Round log, cumulative

Four external batches, 77 stated entries.  Closed on arrival 41 (killed by
logs 17, ill-posed 24), duplicates 9, untestable 3, screened 24: killed 20,
held 4 (`L7-PERIODIC-SOURCE-CAP` to `p = 28, n = 400`, `no-small-period-source` to
`n = 100`, `forced-column-prefix-uniformity` to `n = 20` with constant 4,
`survivor-3over4-bound` to `n = 20`).  The four that held are all
consequences of the census, not routes to a proof.  RW itself stands at
`n = 28` by SAT.  The recurring generator defects, in order of frequency:
treating `T[u][n] = c` as a function of the diagonal; `(H, E)` on
forward-diagram bits; statements about the indicator of an empty set;
forgetting that the hit vector is monotone; forgetting that the next symbol
is forced.  Add all five to `BACKLOG-PROMPT.md` section 4 before the next
generation round.

## 16. Fifth external batch (10 entries, source reading) and round-5 screening (`backlog_screen_r5.py`, log)

The generator's own triage "kept" five round-4 entries that were already
killed; it had not seen the round-4 log.  Its lengths are still wrong
(`W` has length `n`, `Psi` has length `n + 2`).

| id | status | evidence |
|---|---|---|
| metallic-substitution-sources-eliminated, tribonacci-family-prefix-landscape | vacuous on arrival | Tribonacci-2 fixed point `121·12·…` contains `11` at its first junction; no admissible factor |
| defect-window-growing-distance-echo | ill-posed | block at `j + n + 20` lies outside `Psi` |
| reverse-affine-cancellation-source | killed: round 4 W | identity on 4910 of 10272 columns |
| source-family-entropy-expansion | killed by arithmetic | with `m = n` it reads `C_k >= |A_n| 2^(k-4)`, impossible for `k > 4`; the map is 5-to-1 on hard-core sources |
| source-first-diff-visible | killed | the alternating source `1212…` and its first-bit flip (`d = 0`) have identical `Psi` over the whole window at every `n = 7..14` |
| periodic-source-defect-oscillation | killed | `W = 22121`, `p = 5`, `n = 5`: constant `Psi` (one of the two known `n = 5` BWH+ constants) |
| boundary-read-reversal-shot | killed | every admissible pair has an equal mirrored position, `n = 6..14` |
| source-bit-haar-coefficient-decay | killed | for near-alternating sources only 1 to 3 of the `n` bits influence `Psi` at all (`n = 6..15`), against a required `n - 4` |
| klein-toggle-pair-distances | held, threshold vacuous | minimum pairwise-distance sum is 16 to 32 against a required `n/10 <= 1.5`; the minimizer is always `1212…` |

Side fact worth a register note: for the alternating source `1212…` and its
near neighbours, `Psi_n(W)` depends on only one to three source bits.  The
source-to-`Psi` map has a large kernel exactly on the checkerboard-like
sources.  Cumulative: 87 stated entries, 25 screened, 21 killed, 4 held as
census consequences, none a proof route.

## 17. Single-flip injection between survivor levels (`flip_pairing.py`, `RESULTS-FLIP-PAIRING.md`)

**RETRACTED CORRECTION (2026-09-04).** An earlier version of this note
claimed this section's `N_j(n)` was the `(BWH+)`/`Psi_n` object and NOT
`H_r(n)`, i.e. that there was a project-wide naming collision. **That claim
was false and is withdrawn.** Its stated evidence was an elementwise
comparison of `literal_extension`'s output against `forced_orbit`'s output
showing they "diverge from the first symbol". Those two outputs are
different-typed objects: `literal_extension` searches all four values and
returns the forced *edge* value (a `0` or `3` means death), while
`forced_orbit` only ever tries `{1,2}` and returns a *source symbol*.
Comparing them elementwise tests nothing, and both the original claim and
its purported independent re-verification made the same type error.

**What is actually true** (`RESULTS-MEASURE-SUPPRESSION.md` V3(b), and
re-verified directly here): the two constructions define the **same**
survivor population. `rw_population_h.survival_curve`'s `alive_after[j]`
equals `block_halving.chains`'s `src[j]` at the *same* index `j`, and the
stronger word-level check finds **0 death-level mismatches out of 7,168
words** (`n=9,10,11`, both tails, every word). So this section's `0.4^j`
rate, its `99->54->28->18` trajectories, the block-halving `k<=3`, and the
counting-line constant are all genuinely about the `H_r(n)`/DLP-RW
survival process, and may be cited as such.

The one real correction is an index shift: `|H_r(n)| <= N_{n+r+2}(n)`, not
`N_n(n)`, because `H_r(n)` adds the `terminal_pull` filter on top of
survival through row `n+r+2`. The containment is generically strict.

The one proof shape the full-degree result leaves open is an injection
`S_{j+1} -> D_j` pairing each level-`j` pass with a same-level `E` failure.
Tried with single source flips as the pairing, `n = 9..16`, both `c`.

| id | status | evidence |
|---|---|---|
| flip-pairing-injection | killed | coverage `0.97, 0.65, 0.33, 0.15, 0.07, 0` at `j = 0..5` (`n = 16`), not improving with `n`; max matching `23722/24909` at `j = 0` and `0/234` at `j = 5`; nearest partner at depth `n-1`.  Mechanism: a flip at depth `delta <= n-4` is alive at level `j` with probability `0.4^j` independent of `delta`; only `e_0, e_1, e_2` preserve earlier levels, and they do so by changing nothing |
| per-level E balance (unconditional) | false | `S_1(c) = D_0(3-c)` so strict balance fails for one `c` at level 0; against all deaths it fails at deep levels: `99 -> 54 -> 28 -> 18` (`n = 16, c = 3`), `22 -> 14 -> 12` (`n = 10, c = 3`), `6 -> 6 -> 6 -> 6` (`n = 9, c = 3`).  Only the average rate `0.4` per level is true of the data |
| block halving `N_(j+k) <= N_j / 2` | true, too weak | least `k <= 3` for all `n = 11..18`, sources and states (`block_halving.py`); rate `1/k` bit per level cannot reach the rate `1` that `(RW-alpha)` needs |
| counting line `N_j <= C 2^(n - j)` | held, `C = 3` tight at `n = 9` | `C(n, 1.0) = 1` for every `(n, c)` with `n = 10..18`; only `n = 9, c = 3` needs `C = 3` (levels 7, 8).  Slope `1.1` holds with `C = 1` on 16 of 18 cases; at slope `1.3` the constant follows the deepest plateau (`3.03` at `n = 18`) and is not visibly bounded.  The statement to prove is `N_j <= 3 * 2^(n - j)`; `C < 4` suffices for `(RW)` |

## 18. Pushdown-language representation-change candidate (proposed, not started)

Recovered verbatim from a transcript after the original proposal survived
only as a one-line name across two later handoffs (lost to `/clear` before
being written to a project file). Not vacuous, not yet run.

Motivation: every kill logged above constrains a finite-state or
finite-certificate object (DFA rank, affine subspaces, symbol congruences,
bounded weights). None touch a pushdown automaton or context-free grammar.
The dependency queue in the current formulation is already stack-shaped
(newest dependency diagonal, LIFO) — exactly the structure a PDA is built
for.

Proposal: try to show the RW survivor language is (or isn't) context-free,
using the stack to carry the D8 phase that every bounded quotient above
lost.

Kill condition: if the survivor language fails the pumping lemma for
context-free languages at a computable scale (a few hundred symbols), this
route is dead too, cheaply, before any proof effort.

**Prerequisite check (2026-09-04, `RESULTS-FIB-ABSENT-M8-M9-M10.md`,
`fib_absent_check_m8910.py`), SUPERSEDED BY THE SECTION-17 CORRECTION
ABOVE.** Checked whether the "missing hard-core blocks" signal at m=8,9,10
in `fib_transfer_screen_20260902.log` is real or the same sampling artifact
already found at m=7 (which it was, for m=7). m=8 fully resolved (0/18
still absent at `n=18..20`); m=9, m=10 left 15/65, 86/136 unresolved with
sample counts too small to call it either way. **But this whole check
reused `fib_transfer_screen.forced_words`, which forces symbols by
`psi_kernel`'s H-bit condition — the same `(BWH+)`/`Psi_n` object the
section-17 correction just identified, not `literal_extension`/`H_r(n)`.**
Section 10's `B_RW` table and this check's "RW forced-symbol language" are
therefore about `Psi_n`, already known to have full algebraic degree `n`
with no bounded-arity law (capsule section 7) — not about the actual
`literal_extension`-based survivor language section 18 asks about. The
m=8/9/10 sampling question above is a real finding about `Psi_n`'s block
language, but says nothing about section 18's premise either way. If
section 18 is pursued, the block census needs rebuilding on
`late_pull_diagonal_sat.literal_extension` outputs directly (matching
`rw_population_h.py`'s `H_r(n)` construction, not `fib_transfer_screen.py`'s),
before any absent-block or pumping-lemma question is meaningful.

Paired idea from the same note (golden-mean SFT -> rotation via the
Ostrowski/continued-fraction coding) is NOT open — it already shipped as
`sturmian_sources.py`.

## 19. Endpoint-coordinate descent, fusion of counting-line + minimal-counterexample descent (`RESULTS-ENDPOINT-COORD-DESCENT.md`)

David's proposed fix to `MEMO-RW-DESCENT-EXPLORATION.md`'s
padding-misalignment kill: move the `n -> n-1` reduction onto the
endpoint/cut coordinate `e` (holding distance-to-cut fixed) instead of the
source word `W`. Checked directly against `psi_kernel.Endpoint`
(`scratch_endpoint_coord_check.py`): dropping any one endpoint coordinate
and reading the shorter sequence's diagonal at a fixed offset reproduces the
deepest cut coordinate at a stable constant rate `13/32 = 0.4062` (best
case, drop-first), flat across `n = 3..8`, neither -> 1 (no identity) nor
-> 0 (not a vanishing coincidence). Same order as the already-recorded
0.4-per-level flip-pairing coverage rate (section 17) and block-halving's
per-level ratio — three independent codings now agree on this constant.
Killed as a descent lemma: a stable non-degenerate correlation is not an
identity. The obstruction is the same one already on record (cut coordinate
`I(e)_t`'s dependency window grows linearly with `t`, no fixed-radius
truncation, per `constant_tail_scale.py`'s own docstring) — relocating the
reduction from `W` to `e` moves where the growing window shows up, it does
not shrink it.

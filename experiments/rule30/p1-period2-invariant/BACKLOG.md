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
| L7-PERIODIC-SOURCE-CAP | periodic sources `s^omega`, `p <= 7`, admissible run `<= 0.6n + 4` | structured-family exclusion | all `2^p` patterns, `n = 6..40`, both readings (periodic `W` with forced tail; fully periodic `f`) | **held to n = 40**: max `run - 0.6n = 2.6` | bounded SAT tables | Cheap and reaches `n = 40`; a positive result forces any counterexample to be aperiodic in `W` |
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
| L7-PERIODIC-SOURCE-CAP | **held to n = 40** | forced continuation from periodic `W` (`p <= 7`): max `run - 0.6n = 2.6` at `n = 9`, pattern `2212`; fully periodic `f`: never above `0.6n` |
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
| half-survivor-step | killed: `backlog_screen_r2_20260902.log` K | `n = 9, c = 3`: survivors 6, 6, 6, 6 at `k = 5..8` (ratio 1.0); `n = 12, c = 2`: 2, 2.  The clusters survive several levels together |
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

## 12. RW by complete SAT to n = 28 (from the dead workflow's skeptic lens)

`uc/r1-skeptic/rw_sat.py`, logs `rw_sat_check.log` and `rw_sat_scan.log`.
The SAT encoding of RW (`r = 0`, both `c`) is gated against the census at
`n = 9..16`: satisfiable at exactly the census's deepest run and unsatisfiable
one deeper, at every `n` and both `c`.  Then `n = 21..28`, both `c`: **UNSAT**,
solve times 14 s to 27 min.  The RW census therefore stands at `n = 28` for
`r = 0`; `r = 1, 2` only add constraints.  Obstruction H applies as always.

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
held 4 (`L7-PERIODIC-SOURCE-CAP` to `n = 40`, `no-small-period-source` to
`n = 100`, `forced-column-prefix-uniformity` to `n = 20` with constant 4,
`survivor-3over4-bound` to `n = 20`).  The four that held are all
consequences of the census, not routes to a proof.  RW itself stands at
`n = 28` by SAT.  The recurring generator defects, in order of frequency:
treating `T[u][n] = c` as a function of the diagonal; `(H, E)` on
forward-diagram bits; statements about the indicator of an empty set;
forgetting that the hit vector is monotone; forgetting that the next symbol
is forced.  Add all five to `BACKLOG-PROMPT.md` section 4 before the next
generation round.

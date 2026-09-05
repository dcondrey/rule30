# Kill test: lemma "retained-bit-form" (a)-(e)

Date: 2026-09-03.  Status: **HOLDS on every corpus run; no assertion fired.**  This is an
identity between adjacent columns of the four-state kernel; it implies none of (RW-alpha),
(RW), (SEP), (PT2), P1.

All runs from `cd experiments/rule30/p1-period2-invariant`.  Scripts: the two prescribed
kernel scripts `uc/r1-quadratic/q2_gate.py`, `uc/r1-quadratic/q2_gate_random.py`
(forced-orbit corpus only), and `rbf_kill.py` in this directory, which tests the lemma as
STATED, i.e. for every binary prefix of length u >= n, not only forced-orbit prefixes, and
adds the letter-space form of (d) and a kernel-rule brute force of (e).

## Gates on the implementation (before any claim)

- `rbf_kill.py --gate-n 9` (`rbf_exhaustive_u18.log` line 2): 11,254 forced columns from
  `psi_kernel.Endpoint` agree with `psi_column_map.forced_columns`, `qf_common.forward_columns`,
  `qf_common.forced_orbit` and `psi_kernel.psi`.
- Check C' compares the lemma's read-out against the independently coded BRIEF section 3 set
  form of Phi on every column (passes everywhere below).
- Mutation control (`rbf_mutate.log`): with retained redefined as odd-indexed the test fires at
  the first word, `AssertionError: ('B', (1,), 1, 1, -1)`.  The test can fail.
- Letter-space check L cross-checks the kernel rule `CONE` against the 4-state Moore machine on
  all 797,160 windows in {0,1,2}^m, m <= 12, and 87,380 windows in {0..3}^m, m <= 8 (cells 1
  and 3 interchangeable), `rbf_letters_m12.log`.

## Results

| corpus | script, log | range | checks | outcome |
|---|---|---|---|---|
| forced orbits, exhaustive | `q2_gate.py --max-n 17`, `q2_gate_n17.log` | n = 1..17, c in {2,3}, u = n..2n+1, 9,437,180 columns | G1 (b), G2 (a), G3 (c), G4 (d), G5 (e, brute m <= 10, transfer m <= 40) | PASS, 400 s |
| forced orbits, random | `q2_gate_random.py --n 30 40 50 --samples 3000 --seed 1`, `q2_gate_random_n30-50.log`; `--n 80 100 --samples 1000 --seed 2`, `q2_gate_random_n80-100.log` | n = 30, 40, 50, 80, 100; 1,124,000 columns | G1..G4 | PASS |
| arbitrary binary prefixes, exhaustive | `rbf_kill.py --umax 18 --fut 4`, `rbf_exhaustive_u18.log` | every word in {1,2}^u, u <= 18, every n <= u: 8,912,898 (word, n) pairs | A, B, C, C', D1, D2, D3 (column u on [-u-1, n] plus 4 forced future symbols) | PASS, 847 s |
| arbitrary binary prefixes, random | `rbf_kill.py --rand-n 30 40 60 80 100 --samples 300 --seed 1`, `rbf_random_n30-100.log`; `--rand-n 150 200 --samples 100 --seed 2`, `rbf_random_n150-200.log` | n up to 200, u = n..2n+1, 131,400 (word, n) pairs | A, B, C, C', D1, D2, D3 | PASS |
| letter space (free column u-1) | `rbf_kill.py --letters-m 12 --letters-m4 8`, `rbf_letters_m12.log` | all {0,1,2}^m, m <= 12 | D4: 3,255,076 odd-indexed even-bit flips leave column u unchanged; 2,856,496 even-indexed flips all change it | PASS |
| relaxed balance (e) | `rbf_kill.py --balance-brute 11 --balance-transfer 80`, `rbf_balance_m80.log` | m <= 11 brute force through `CONE`; m <= 80 transfer matrix | #{Phi = 0} = (3^m + 1)/2 exactly | PASS |

## Margins and patterns

- (a)-(d) are identities: there is no slack to report, only pass/fail.  They hold on
  arbitrary binary prefixes, which is strictly more than the forced-orbit corpus the prior
  gate covered; the derivation from the (H) and (E) integrals never used forcing of earlier
  symbols, and the data agree.
- (e) holds with slack exactly one at every m: `2 * #{Phi=0} - 3^m = 1` for m = 1..80
  (`rbf_balance_m80.log`, `q2_gate_n17.log`).  The imbalance does not grow; it is one word.
- The lossy half of the Moore map is visible directly: the single pattern Z_{u-1} has fibres
  of size up to 15 on forced orbits at n <= 17 (60,684 of 1,261,696 keys ambiguous,
  `q2_gate_n17.log`) and up to 18 on arbitrary prefixes at u <= 18 (48,694 of 263,957 keys,
  `rbf_exhaustive_u18.log`); the pair (Z_{u-1}, Z_u) is single valued in every case.  The
  maximum single-pattern fibre grows with n (6 at n <= 9, 7 at n <= 12, 15 at n <= 17), so the
  forgotten odd-indexed bits are not a bounded defect.
- Number of maximal non-retained runs per column (= ceil(N/2), one per odd-indexed nonzero
  cell): mean 0.95 n on random prefixes at n = 30..200 (window length up to 2n+1 and about
  four fifths of cells nonzero), i.e. about half the even-bits of column u-1 are discarded by
  every step.

## Time

All runs together about 25 minutes wall clock on 10 cores (the longest single run was the
arbitrary-prefix exhaustive at 847 s).  Pushing further is cheap but obstruction H applies:
the lemma is derived, and these are gates on the derivation, not evidence for it.

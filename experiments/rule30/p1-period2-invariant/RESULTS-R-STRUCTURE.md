# Structure of the right trace language R: entropy at most 0.124 bits, follower sets no thinner than a random language of the same size, pumpable forbidden factors, no theorem

Date: 2026-09-16. Pre-registration `PREREGISTRATION-R-STRUCTURE.md` (written before the
runs). Scripts `r-structure/r_structure.py` (log `r_structure.log`, record
`r_structure.json`; S1, S2, S3 and a supplementary null `null_bt`), `r-structure/r_structure_null.py`
(log `r_structure_null.log`, record `r_structure_null.json`; the count-matched null seeded
with `R` through length 13). Theory panel `r-structure/theory/attempt-*.md` with one refuter
each (`refute-*.md`). All exit 0. Item 2 of the standing task list for this thread.

**`[C]` `h(R) <= log2 lambda_60 = 0.124` bits per symbol: the topological entropy of the trace
subshift is bounded by the spectral radius of the shift of finite type avoiding the 4,189
minimal forbidden factors through length 60 (63,418 live automaton states, power iteration
converged to `1e-10`, Collatz-Wielandt upper bound equal to the estimate), and the sequence
over `L = 2, 5, 13, 30, 48, 60` is `0.6942, 0.6174, 0.3335, 0.2217, 0.1309, 0.1240`, strictly
decreasing, gate at the golden mean and the no-`00000` value passed. The bound at `L = 60`
is below the finite-length growth `log2(|R_48|/|R_47|) = 0.1505` and `log2(|R_60|/|R_59|) =
0.1295`. `[C]` Follower sets: `21,389` words of length 44 have `2,631` distinct 16-step
follower sets (ratio 0.123), growing 4.2 percent per unit length on `p = 36..44`; a random
factor-closed language with the same `|R_m|` at every length has `1,788` (ratio 0.084) and
grows faster (1.60 against 1.39 over the same range), so the low ratio is a property of the
size profile, not of `R`, and (S1) is INDETERMINATE with its confirm condition failed by the
null itself. `[C]` Pumping: 267 of the 2,002 minimal forbidden factors of length 35..53 stay
minimal forbidden when a square `vv` of a period block (`01`, `001`, `00001`, `1010000`, any
rotation) is replaced by `vvv`, 13.3 percent, against 0 of 241 (seeded null) and 2 of 219
(supplementary null): a structural signal, below the pre-registered 50 percent, (S2)
INDETERMINATE. `[K]` for the theory panel as a route: three attempts (masking-channel
entropy bound, non-soficity by an explicit family, zero-entropy mechanism), each refuted at
a named step; what survives is listed in section 4 and contains no statement about `h(R)`,
soficity or `(PT2)` beyond the finite computations above.**

## 1. Objects

`R_m` is the set of words `rho_0..rho_(m-1)`, `rho_k = s(2k,1)`, of the right half-line
driven by `s(t,0) = t mod 2` over all seeds; a length-`m` prefix reads cells `1..2m-1`, so
`R` is the language of the trace subshift `X_R` and is factor-closed. Record
`uc/r1-hardcore/r_exact_language_m60.json`: `|R_m|` for `m <= 60`, 4,189 minimal forbidden
factors (MFF) through 60 (counts per length 1, 1, 1, 1 at `m = 2, 5, 6, 7`, then 8 at
`m = 19..21`, 35 at 30, 71 at 40, 135 at 50, 297 at 60, ratio about 1.1 per length), and
the 103,220 words of `R_60`. Exact fact re-derived by the panel (attempt (c), step 1)
`[U]`: `rho_(k+1) = 1` iff `s(2k, 1..3) = 000`; the trace symbol is 1 exactly when the
three cells at the wall are empty two steps earlier, which re-proves `11` forbidden.

Two nulls. The pre-registered construction (randomise every level to the size `|R_m|`) dies
at length 3 because randomising the two-symbol level leaves four candidates for five words;
that is an artifact and is recorded in `r_structure.log` lines 4 to 8. The null used for the
comparisons is seeded with `R` itself through length 13 and randomised from 14
(`r_structure_null.py`, `default_rng(20260916)`); it reaches 60 with `|null_60| = |R_60|`,
short of `|R_m|` at 22 lengths by at most 1.4 percent (length 26), factor-closed, its own
MFFs regenerate it exactly. A supplementary null `null_bt` in `r_structure.py` (backtracking
construction, defined through length 47) gives the same picture where both exist.

## 2. (S1) Follower sets

`N_p(q)` = number of distinct sets `{v in {0,1}^q : wv in R_(p+q)}` over `w in R_p`.

| `p` | `|R_p|` | `N_p(8)` | `N_p(12)` | `N_p(16)` | ratio `N_p(16)/|R_p|` | null `N_p(16)` | null ratio |
|---|---|---|---|---|---|---|---|
| 36 | 8,534 | 317 | 1,035 | 1,893 | 0.222 | 1,117 | 0.131 |
| 40 | 13,730 | 332 | 1,141 | 2,250 | 0.164 | 1,400 | 0.102 |
| 44 | 21,389 | 345 | 1,256 | 2,631 | 0.123 | 1,788 | 0.084 |

`N_p(16)` grows by 4.2 percent per unit `p` on `36..44` (max single step 5.1 percent; kill
threshold 5 percent not fired), and the ratio is far below the 0.5 the confirm needed; but
the null's ratio is lower still and its growth faster. A count-matched random language has
follower-set counts of the same order (0.6 to 0.7 of `N_p(R)`), so `N_p(q)/|R_p|` does not
distinguish `R` from noise and the pre-registered reading of (S1) is withdrawn: the
statistic measures the size profile. What does distinguish them: the null has 28 to 33
percent dead-end words at `p = 36..44` (no length-16 extension) and `R` has none, as a
trace language must. Soficity of `X_R` is untouched either way.

## 3. (S2) Minimal forbidden factors

Counts per length grow about 1.1 per unit (43, 51, 62, 76, 71, 84, 71, 95, 109 at
`m = 36..44`), the same rate as `|R_m|` itself (1.11 to 1.09). Of the 2,002 MFFs of length
35..53, all contain a square of a period block, and 267 (13.3 percent) are pumpable: the
word with `vvv` for `vv` is again a minimal forbidden factor (per block: `01` 106 of 1,793
square-containing, `001` 91 of 1,423, `00001` 58 of 1,977, `1010000` 19 of 893). In the
seeded null 0 of 241 are pumpable, in `null_bt` 2 of 219 (0.9 percent). So the forbidden
factors of `R` do carry the period blocks the trace lives in (the period-5 word is the
regime 96.9 percent of width-16 trace positions lie in, `RESULTS-RIGHT-SEED-MARGIN.md`
section 6), but 87 percent of them are not generated by that pumping; nothing here is a
rule producing the MFF set, and the pre-registered 50 percent is not reached.

## 4. (S3) Entropy bounds, and the theory panel

`h(R) <= log2 lambda_L`, `L = 2, 5, 13, 30, 48, 60`: `0.6942, 0.6174, 0.3335, 0.2217, 0.1309,
0.1240`. Each is a theorem by finite computation (`R` is contained in the SFT of its MFFs
through `L`); the last is `0.124` bits per symbol, one fifth of the golden-mean bound and
below both finite-length growth rates quoted above (which is consistent: the local ratio at
finite `m` is not bounded by `lambda`). The seeded null's own MFFs give `0.154` at its
`L = 47`. Whether `h(R) = 0` is untouched (`RESULTS-R-EXACT-GROWTH.md`: 0.04 bits and zero
inseparable below `m` about 100).

Theory panel (`r-structure/theory/`), pre-registered expectation "no attempt survives its
refuter as a proof" met:

- (a) Masking-channel bound. Refuted at step 8. Survives `[U]`: the shifts obtained by
  masking through one, two or three columns are each exactly the golden-mean shift, so
  finite-depth masking gives `log2 phi` and nothing tighter; the density-of-zeros bound
  `h <= 1 - mu(1)` is weaker; a computable nonincreasing sequence of bounds `h(S_k)` exists
  with `0.258` at `k = 12` (the SFT sequence above is sharper).
- (b) Non-soficity by an explicit family. Refuted at its own step 9 (the family is read off
  the record, not derived from the rule), with two record facts misread (the refuter's lines
  17 to 25). Survives `[U]`: `0000` forces the next odd-time trace symbol to 1; `R` regular
  implies `X_R` sofic; the chain, compactness and transplant criteria are valid sufficient
  conditions. `[C]`: `F((1000010)^n)` drops at `n = 4` and `F((1010000)^n)` at `n = 2`;
  `(1000010)^n` is in `R` for `n <= 21` from the vacuum orbit and no further.
- (c) Zero-entropy mechanism. Refuted at step 6: the attempt's "short-witness property (W)"
  is sufficient for `h(R) = 0`, not equivalent to it, and it fails at every length where its
  witness depth `D(m)` has been computed (`D(m) >= m` from `m = 12`). Survives `[U]`:
  `rho_(k+1) = [s(2k,1..3) = 000]`; an alternating block `..0101` with right end 1 blocks all
  leftward influence past it and is consumed from the left exactly one cell per step; no
  such block survives forever under the pin; `D(m) = o(m)` would imply `h(R) = 0`. Note that
  the robust shields of `RESULTS-RIGHT-SEED-MARGIN.md` section 7 are time-periodic blocks,
  not static alternating ones, and do survive forever; the attempt's transience statement is
  about the static block only.

Corrections and extensions (2026-09-17, `forward-boundary/strengthen/strengthen_5.log`,
`strengthen_6.log`). The purely periodic words of `R_60` have minimal periods 2 (2 words),
3 (3), 5 (5), 7 (7), and every period from 18 to 30 except 24 (2 to 46 words each: 18, 19,
2, 10, 44, 23 words at periods 18 to 23 and 34, 26, 27, 37, 46, 8 at periods 25 to 30; the
"18 to 46" first written here misread the log); no minimal period from 8 to 17 occurs, and
11, 13 and 17 do not occur even as non-minimal periods; the earlier "2, 3, 5, 7 only up to
12" counted periods with at least eight repetitions. `(1000010)^n` is a trace for every `n <= 36` (one CaDiCaL query
each on the complete right light cone, 839 s at `n = 36`; `n = 37` stopped by hand), so the
period-7 word's membership is not the finite phenomenon the panel's attempt (b) took it
for; whether `(1000010)^omega` is a trace is open. The joint-census columns, from the code
of `uc/r1-hardcore/r_exact_joint.py`: `LANG` is the number of forced continuation symbols
that can be appended while every prefix stays in `R` (automaton bound lowered by one SAT
query per length beyond the horizon), `E` the number of forced steps for which the outermost
cell of the forced column keeps the tail symbol `c`, and the joint run their minimum per
word.

## 5. Reading

`R` is provably thin (`0.124` bits) and provably not a subshift of finite type of low order
(the MFF count keeps growing at the rate of the language itself), and its forbidden factors
carry the period blocks the trace lives in. Against a null of its own size it shows one
structural signal, the pumpability of 13 percent of its forbidden factors, and no signal in
its follower-set counts. Nothing here is a mechanism: no rule generates the MFFs, no proof
bounds `h(R)` below the SFT value or shows it is zero, and no argument decides soficity.
Together with the margin result (the reconstructed row's zero runs are a fair coin whatever
the trace measure) this closes item 2 with "no mechanism", and the standing stop rule
applies: the deliverable is the position paper, not item 3.

## 6. Scope

Finite: the record through length 60. The entropy bounds are exact for the SFTs named and
upper bounds for `R`. The nulls are one seed each. The panel's surviving statements are
labelled by their refuters and re-read here; none was re-derived by a second implementation
beyond the checks the refuters ran.

## 7. Reproduction

From `experiments/rule30/p1-period2-invariant/`:

```sh
uv run --no-project --with numpy python r-structure/r_structure.py        # 10 s
uv run --no-project --with numpy python r-structure/r_structure_null.py   # 8 s
```

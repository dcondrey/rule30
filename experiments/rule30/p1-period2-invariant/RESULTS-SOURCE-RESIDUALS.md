# Nerode residuals of the pooled run language are the endpoint states modulo `CONE[1] = CONE[3]`

Date: 2026-09-16. Pre-registered in `PREREGISTRATION-SOURCE-RESIDUALS.md`
before the run. Scripts `source_residuals.py` (the probe) and
`source_residual_families.py` (the companion), records
`source_residuals.json`, logs `source_residuals.log`,
`source_residual_families.log`.

**`[C]` For `m = 1` and both tails, and for `m = 2` at `c = 3`, the number of
Myhill-Nerode classes of `L_m(c) = {W : rho_c(W) >= m}` among the `2^p`
prefixes of length `p`, with suffixes of length up to 9, is
`12, 20, 37, 69, 123, 219, 391, 701` at `p = 4..11`; `m = 2` at `c = 2` and
`m = 3` fall short of it by 1 to 5 at that horizon and reach the same values
at horizon 12 (section 7). The count equals at every `p` the number of
endpoint states after identifying `1` with `3` in every column and diagonal
entry other than the last symbol. That identification is a quotient of the
process (Lemma, section 3): old entries enter `peek` only as first arguments
of `CONE`, and `CONE[1] = CONE[3]`. The residuals therefore track the retained
state at 0.94 to 0.95 of the raw state count from `p = 6` with no plateau,
`(REG-m)` is killed on this range for every `m <= 3`, and a DFA for `L_1(c)`
needs at least 701 states at prefix length 11 and at least 2254 at prefix
length 13 (2255 for `c = 3`; section 4; at least 2192 for every `m <= 3`).
This is finite evidence, not a proof of non-regularity. Section 4 states the
lemma a proof needs; the independent check of section 7 reverses the reading
first given there of two families: the prefixes `1^m` are pairwise separated
through `m = 1100`, with the number of horizon-`q` classes among them
doubling with `q`, and the single-defect family supplies about `3p/4`
pairwise-separated prefixes per length, so both are finite evidence for an
infinite separated family, not against one.**

## 1. What was computed

One trie over all binary words of length at most 20; per word and tail the
wide-grammar run at scale `|W|`, capped at 3. For each prefix length
`p = 4..11` the signature of a prefix `u` is the membership vector over the
1022 suffixes of length 1..9; `S_m(p)` counts distinct signatures, `E(p)`
counts distinct `Endpoint` states `(column, diagonal)` at length `p`, and the
regular control is the same count for hard-core membership, which is 3 at
every `p` as it must be. 39 s single core. The companion recomputes `E(p)`,
the reduced count `E13(p)`, and the family data of section 4.

## 2. Result

| `p` | `E(p)` | `E13(p)` | `S_1` (`c=2` / `c=3`) | `S_2` | `S_3` | control |
|---|---|---|---|---|---|---|
| 4 | 13 | 12 | 12 / 12 | 12 / 12 | 11 / 12 | 3 |
| 5 | 23 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 3 |
| 6 | 39 | 37 | 37 / 37 | 37 / 37 | 37 / 37 | 3 |
| 7 | 73 | 69 | 69 / 69 | 68 / 69 | 66 / 67 | 3 |
| 8 | 129 | 123 | 123 / 123 | 122 / 123 | 122 / 122 | 3 |
| 9 | 232 | 219 | 219 / 219 | 218 / 219 | 217 / 217 | 3 |
| 10 | 410 | 391 | 391 / 391 | 391 / 391 | 390 / 390 | 3 |
| 11 | 742 | 701 | 701 / 701 | 701 / 701 | 696 / 698 | 3 |

`S_1(p) = E13(p)` at every `p`; `S_2` and `S_3` fall short of it by at most 5
at horizon 9 and equal it at horizon 12 for every `p <= 11` (section 7).
The pre-registered kill fires for all six `(m, c)`: `S_m(11) > S_m(10)`,
`S_m(11) >= 2 S_m(8)`, `S_m(11) >= 0.25 E(11)`, ratio 0.938 to 0.945.

Horizon check at `p = 8`, `c = 2`, `m = 1` (companion of `source_residuals.py`,
run in the session scratchpad and reproduced by the same code path): `S_1(8)`
is `39, 117, 122, 123` at suffix horizons `q = 2, 3, 4, 5` and stays 123 through
`q = 12`; the six raw state pairs still sharing a signature at `q = 12` each
differ in exactly one diagonal entry, `1` against `3`, at depth 5, 6 or 7.
Identifying `1` with `3` in the column alone changes the count only at
`p = 6` on this range (39 to 38, the pair `111222` / `112122`) and again from
`p = 14` on; the diagonal alone carries every identification for
`7 <= p <= 13` and not beyond (4013 against 4009 at `p = 14`; section 7).

## 3. The quotient

**Lemma.** Let `u`, `u'` be binary words of length `p` with endpoint states
`(C, D)`, `(C', D')` (`C` of length `p + 1` with `C[p]` the last symbol, `D` of
length `p`). If `C[p] = C'[p]`, `C[i] ~ C'[i]` for `i < p` and `D[j] ~ D'[j]` for
`j < p`, where `~` identifies `1` with `3`, then for every `s` the states after
`us` and `u's` are identical, and `uv in L_m(c)` iff `u'v in L_m(c)` for every
`v`, `m`, `c`.

*Proof.* In `Endpoint.peek` the stored entries are read only as first
arguments: `new_column[i] = CONE[C[i+1]][new_column[i+1]]` and
`new_diagonal[j+1] = CONE[D[j]][new_diagonal[j]]`, with the chain seeded by
`BOUNDARY[s]` and `new_column[0]`. `CONE[1] = CONE[3]` (both `(3, 2, 1, 0)`), so
the two chains coincide entry by entry, the appended column
`new_column + [s]` and the new diagonal are identical, and the cut cell
`new_diagonal[p]`, the hard-core check on `C[p]`, and every later step agree.
`rho` at scale `p` reads only these. ∎

Hence `S_m(p) <= E13(p)` for every `m`, `c`, horizon; the reduced process is a
deterministic automaton on reduced states; and the equality `S_1(p) = E13(p)`
at `p <= 11` says that every two distinct reachable reduced states of the
same length at most 11 are separated by a suffix of length at most 9 (at most
5 at `p = 8`); the pooled count over all prefixes of length 1 to 11, 1585
distinct horizon-9 signatures for `L_1`, the sum of the per-length counts,
extends this across lengths (section 7). The one-sided closure `CONE[1] = CONE[3]` of
`RESULTS-DIAGONAL-MEMORY.md` section 8 is therefore a full quotient of the
endpoint process, and it compresses by a factor 0.945, as that section says.

## 4. What a no-go theorem needs, and two families read twice

`L_m(c)` is regular iff its Nerode classes are finite. By section 3 and the
data, the classes at length `p` are the reduced states for `p <= 11`, and
`E13(p)` grows by 1.78 to 1.79 per symbol from `p = 8` (1.67 to 1.87 below).
A proof of non-regularity needs
either (a) separation of distinct reachable reduced states at every `p`
together with `E13(p) -> infinity`, or (b) an explicit infinite family of
pairwise-separated prefixes. Neither is proved; the DFA lower bound 701 is
what the computation gives, and each further `p` multiplies it by about 1.77.

Extension to `p = 12, 13` at suffix horizon 7 (`source_residuals.py 13 7`,
record `source_residuals_p13q7.json`, log `source_residuals_p13q7.log`; `E13`
from `source_residual_families.py 3000 13`, log
`source_residual_families_p13.log`): `E(12), E(13) = 1329, 2376`,
`E13(12), E13(13) = 1257, 2255`, `S_1 = 1256, 2254` at `c = 2` and
`1257, 2255` at `c = 3`; `S_2 = 1246, 2243` and `1251, 2242`; `S_3 = 1217, 2201`
and `1227, 2192`. The `c = 3` residuals again equal the reduced states. The
`c = 2` shortfall of one is the horizon, not the quotient: the unseparated
`c = 2` pair at `p = 12`, `111112122222` / `112211222222`, separates at suffix
length 12 and the `p = 13` pair at length 11 (section 7), so the horizon a
full separation needs jumps from 7 at `p = 11` to 12 at `p = 12`; at `q = 7`
the `c = 2` count is already 218 at `p = 9` and 389 at `p = 10`, against 219
and 391 at `q = 9`. The DFA lower bound for `L_1(c)` from this record is
therefore 2254 at `p = 13` (2255 for `c = 3`, and for `c = 2` at horizon 11),
`E13` grows by 1.79 per symbol at `p = 12, 13`, and the residual-to-state
ratio is 0.949.

The periodic drives were first read here as evidence against (b): for the
length-`m` prefixes `u_m` of `(12)^inf`, `(21)^inf`, `2^inf`, `1^inf`,
`(122)^inf`, `(1222)^inf`, `(112)^inf`, `(12222)^inf`, and for `2^m v` with `v`
in `{1, 12, 112, 121, 1121, 12212}`, the sequence `m -> [u_m in L_1(c)]` is
exactly periodic on `m <= 3000` (companion, part 2), with periods 28, 28, 2,
1, 84, 28, 84, 155 and 1 or 4, 16, 16, 32, 32, 128, preperiod 0 except 2 for
`(1222)^inf`. That inference was invalid: periodicity of the prefixes' own
membership says nothing about their Nerode classes (every `a^m` has the same
membership in `{a^n b^n}`), and the growing periods of `2^m v` as `|v|` grows
are the doubling seen from the other side. Measured directly (section 7), the
number of horizon-`q` classes of `L_1(c)` among the prefixes `1^m`,
`m <= 1100`, is `1, 4, 16, 32, 64, 128, 256, 512, 1024` for `q = 1..9` and all
1100 prefixes are distinct at `q = 10`, for both tails; among `2^m` it is
`2, 7, 32, 32, 128, 256, 256, 1024, 1100` (`c = 2`); and the prefixes of every
other drive tested are pairwise distinct by horizon 4 to 8 (`m <= 400`). A
proof of (b) along `1^m` would show that for each `k` some suffix of length
`k` has membership of period about `2^(k+1)` along `m`; the drives are the
most tractable candidates for such a family, not counter-evidence.

The single-defect family `2^a 1 2^(p-a-1)` was read the same way, and its
data say the opposite: at `p = 12, 20, 28` the prefixes with the defect at
depth `a <= 4, 6, 8` share one reduced state (the state forgets a lone early
defect once it lies below about a quarter of the depth;
`a_max = floor((p + 5) / 4)` for `8 <= p <= 40`), and every pair of distinct
reduced states in the family is separated in `L_1(c)` within 3 steps at those
three `p` (companion, part 3; the separator length grows with `p`, past 6 by
`p = 34`). So the family supplies `p - floor((p + 5) / 4)` pairwise-separated
prefixes per length, 8, 14, 20 at `p = 12, 20, 28`, unbounded in `p`, and the
pooled family over `p = 8..40` stays pairwise separated across lengths at
horizon 6 (564 of 564 at `c = 2`, 565 of 565 at `c = 3`; section 7).
Unboundedly many pairwise-separated prefixes is exactly what (b) needs. The
family does not account for the `1.77^p` count, which needs about 0.8 bits
per symbol, but (b) does not need it to.

What is proved is the direction that matters for certificates: a finite-state
invariant of the endpoint process can only see the reduced state, and through
`p = 11` the run language sees all of it. The statement left is the separation
lemma for all `p`; a proof would have to track a state difference up the
anti-diagonal chain through the masking cases `CONE[1] = CONE[3]` as first
argument and `CONE[1][x] = CONE[2][x]` for `x in {0, 1}`.

## 5. Scope

Finite, `p <= 13` (horizon 9 at `p <= 11`, 12 at `p = 8`, 7 at `p = 12, 13`;
the check of section 7 reaches horizon 12 at `p <= 11` and words of length
24), wide grammar, two implementations. The `p = 12, 13` extension and the
family class counts are post hoc, not in the pre-registration. The lemma is
uniform. Non-regularity of `L_m(c)` is not
proved, and non-regularity of `L_1` would not transfer to `L_m` in any case.
Nothing here bears on `RW`, `(RW-alpha)`, `SEP` or `PT2` except as a bound on
what a bounded-memory certificate for them can express; and even a proved
non-regular `L_m` would not exclude a regular over-approximation of the
survivors that is empty at the required depth, which is the certificate shape
`RESULTS-CONSTANT-TAIL-LANGUAGE-COCYCLE.md` uses (nonempty through horizon
20). A no-go against that shape is a separate statement.

## 6. Reproduction

From `experiments/rule30/p1-period2-invariant/`:

```sh
uv run --no-project python source_residuals.py 11 9 source_residuals.json
uv run --no-project python source_residual_families.py 3000
uv run --no-project python source_residuals.py 13 7 source_residuals_p13q7.json
uv run --no-project python source_residual_families.py 3000 13
```

39 s, 28 s, 29 s and 30 s single core.

## 7. Independent check

`crosscheck/source-residuals/` holds a second implementation written from the
definitions alone: `kernel_np.py`, a vectorised endpoint kernel gated on all
4094 words of length at most 11 against `psi_kernel`; `census.py`,
`families.py`, `defect_family.py`, `drive_classes.py`, `drive_classes2.py`,
`oracle_1m.py`, `q7.py` and `crosslength.py`, with logs and records alongside.
It reproduces every cell of sections 2 and 4, computes `E`, `E13` and the
column-only and diagonal-only variants to `p = 20`, the residual counts to
horizon 12 at `p <= 11` (where all six `S_m(p)` equal `E13(p)`), the pooled
cross-length count 1585, the separation horizons of the `p = 12, 13` pairs,
and the class counts among the drive prefixes and the single-defect family
that section 4 now reports; `oracle_1m.py` re-derives the `1^m` and `2^m`
class counts with `psi_kernel.Endpoint` alone (`m <= 64`, horizon 8). Its
findings changed sections 2, 3 and 4 as marked.

```sh
uv run --no-project --with numpy --with python-sat python crosscheck/source-residuals/drive_classes2.py 1100 10 1,2
uv run --no-project --with numpy python crosscheck/source-residuals/oracle_1m.py 64 8
```

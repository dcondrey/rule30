# A leading defect immediately before another defect is absorbable

Status: **A first class of interrupted sources reduces exactly, proved for
every k>=2 at zero padding. The general interrupted-run gap and RW/DLP
remain open.**

The [defect-cocycle report](RESULTS-rw-defect-cocycle.md) proves exact
prefix-erasure identities for a single defect (`1`) followed by enough
plain `2`s, and states plainly that "shorter or interrupted runs can
retain a nontrivial ordered correction." This note tests the simplest
interrupted case directly: a defect immediately preceding another defect.

## 1. The lemma

With `F` the endpoint morph of `rw_homogeneous_source_exclusion.py`, for
every `k>=2` and every finite four-state suffix `v`,

\[
F^{k+2}(1\,2^k\,1\,v) = F^{k+2}(2^{k+1}\,1\,v).
\]

No padding is required after the second defect, for **every** `k>=2`, not
only a tested range (section 3 below is the proof). It is also directly
cross-checked against `F` itself for `k in {2,3,5,8,13}` over 425
four-state suffixes of length 0 to 3, and against the section-machine
technique of `RESULTS-rw-defect-cocycle.md` for `k = 2` through `25`.

The lemma is a front rule. Applied to the leading `1 2^a 1` of a three-defect word `1 2^a 1 2^b 1` it gives `2^(a+1) 1 2^b 1` for every `a,b` in `2..5` checked, because the identity holds for arbitrary `v`. The same substitution after a nonempty left context is not licensed: equal suffix actions do not give equal `J` images, and the sections of the left context read the `J` image, not the suffix action.

## 2. The two boundary cases are genuinely different

`k=0` (adjacent defects, `11`) needs exactly `5` twos of padding after the
second defect before the same section-match holds; `4` or fewer fails.
`k=1` (`121`) needs exactly `1`. Both are sharp: one less padding in
either case gives a different section. Only `k>=2` needs none at all.

## 3. The all-k proof for k>=2

State `C` of the seven-state section machine is a fixed point of input
`2` (`SECTION['C'][2] = 'C'`), and reading two `2`s from either state `B`
or `C` lands on `C`. So it suffices to show `J(2^k 1)` — the diagonal
readout of a bare defect after `k` twos — begins `2, 2` for every `k>=2`.
That reduces to two facts, both proved from the raw transition tables.

**The pure-2 background is a fixed point.** `BOUNDARY[2]=1`, `PHI[2][1]=2`,
`PHI[1][2]=1`: a 2-cycle. By induction on height in `inverse_terminal`'s
recursion, its working arrays stay constant tuples alternating `1,2` (the
height-0 array is `(BOUNDARY[2],...)=(1,...)`, the height-1 array is
`(PHI[2][BOUNDARY[2]],...)=(2,...)`, and each later height is
`PHI[prev][prev-1]` of two constant arrays, hence constant). So
`inverse_terminal(2^n)` alternates `1,2,1,2,...` for every `n`. Its `peel`
reads the adjacent pairs `(1,2)` and `(2,1)` through `PHI[1][2]=1` and
`PHI[2][1]=2`, giving back the same alternating sequence one shorter —
exactly `inverse_terminal(2^(n-1))`. Since `terminal` is the exact,
asserted inverse of `inverse_terminal`, this proves

\[
\text{morph}(2^n) = 2^{n-1}\quad\text{for every }n\ge1.
\]

**Locality.** `inverse_terminal(w)[h]` depends only on `w[0..h]`: its
height-`h` entry at position `j` is built from height-`(h{-}1)` and
height-`(h{-}2)` entries at position `j+1`, so by induction the dependency
set of entry `(h,j)` is contained in `{j,...,j+h}`. The words `2^k 1` and
`2^{k+1}` (both length `k+1`) agree on positions `0..k-1` and differ only
at the last position, so their `inverse_terminal`s agree on entries
`0..k-1`. Because `peel` reads adjacent pairs, the two length-`k` peels
agree on entries `0..k-2`; because `terminal` builds its output left to
right (entry `j` from `cut[0..j]` only), the two length-`k` `morph`
outputs agree on entries `0..k-2`. For `k>=2`, position `0` is in that
range, so

\[
\text{morph}(2^k\,1)[0] = \text{morph}(2^{k+1})[0] = 2.
\]

Combined with `J(2^k 1)_0 = 2^k1[0] = 2` trivially, `J(2^k 1)` begins
`(2,2)` for **every** `k>=2`. States `B` and `C` therefore synchronize at
the same early point for every `k`, proving the lemma of section 1 for
all `k>=2`, not just the tested range.

## 4. Scope

Section 3 is a uniform, all-length proof (`U`) for `k>=2` at zero padding.
The `k=0,1` boundary values, the arbitrary-suffix cross-check, and the
chaining check remain finite exact certificates (`C`). Together they
resolve one narrow, previously undocumented case: two defects with a gap
of at least two twos reduce immediately, and the two smaller gaps reduce
with small fixed padding. It says nothing about:

- three or more defects with independently varying gaps (only chained
  applications of the same two-defect lemma were checked);
- whether every interrupted RW/DLP hard-core source eventually reduces to
  a form the existing single-defect rules already close;
- a formal reduction from this lemma to DLP, RW, or SEP.

The [route record](../REFERENCE/FORMALIZATION-LEDGER.md) for RW/DLP
interrupted runs should read this as a partial answer, not a closure.

## 5. Reproduction

```sh
cd experiments/rule30
uv run --no-project python rw_interrupted_defect_absorption.py
```

Exits normally only if every threshold, suffix, chaining, closed-form, and
induction assertion holds; any failure raises immediately with the
offending `k`/suffix. Output and source hashes are saved to
[rw-interrupted-defect-absorption.json](../../experiments/rule30/rw-interrupted-defect-absorption.json).

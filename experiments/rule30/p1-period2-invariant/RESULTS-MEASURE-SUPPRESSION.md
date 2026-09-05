# Setup verification for PREREGISTRATION-MEASURE-SUPPRESSION.md

Date: 2026-09-04. Executes section 4's V3(b), V4, V5 only. V1 and V3(a) were
already confirmed by a prior pass (cited, not redone): V1 (`H_r(n)` is a pure
function of the length-`n` prefix, by construction of `literal_extension`)
and V3(a) (`j -> S_j` is non-increasing, trivial from `flip_pairing.py`'s own
`S_j = [w for w in range(total) if death[w] >= j]` construction). This
document does not touch V2 (extending the `H_r(n)` census itself); that is a
separate, already-scoped task.

**Verdict up front: V3(b) holds, with one precise index correction, and
mechanism (M3) survives it.** `block_halving.py`/`flip_pairing.py`'s
survivor count `N_j(n)` is exactly `rw_population_h.survival_curve`'s
`alive_after[j]` — the hard-core-survival count of `late_pull_diagonal_sat
.literal_extension`'s own forced continuation — at the *same* index `j`.
Confirmed two ways: (i) exact, nonzero, element-by-element match of the
count arrays at `n=9..12`, both tails; (ii) a stronger, word-for-word
check — the two constructions die at the identical level for every single
word, 0 mismatches out of 512 (`n=9`) and 1024 (`n=10`) words, both tails —
ruling out the weaker possibility that only the counts happened to
coincide while the underlying survivor sets differed. `H_r(n)` is then a
further-filtered subset of `alive_after[n+r+2] = N_{n+r+2}(n)` (the extra
filter being `terminal_pull`), giving `|H_r(n)| <= N_{n+r+2}(n)`, not
`N_n(n)` as the preregistration's section 3 loosely wrote. The correction is `N_n(n) -> N_{n+r+2}(n)`; `n+r+2 <= n+4` for `r in
{0,1,2}`, which is exactly why `block_halving.py`'s main loop already sets
`levels = n+4` ("Levels j = 0..n+3 cover every r in {0,1,2}" — in range).
Methodological note: comparing `literal_extension`'s raw 4-valued
edge-forced output directly against `forced_orbit`'s binary source symbols
is not a test of population alignment (they are different-typed outputs by
construction); the composite conditions below are what align, and the
check is done word-for-word, not just on aggregate counts (next section).

## V3(b): the index-alignment check

### The two code paths, and what actually needs comparing

`dlp_rotated_wedge.rotated_wedge_population` (the `H_r(n)` definition)
calls `literal_extension(word, tail, target + 2)` with `target = n + r`.
`literal_extension` forces each appended value as the unique symbol in
`range(4)` with `append_dependency_edge(...)[-1] == tail`. Both tails in
use (`2`, `3`) have high bit `1` (`H(t) = t >> 1`), so this exact-equality
condition decomposes as **`H == 1` and low bit `== tail`** — i.e. exactly
`flip_pairing.forced_orbit`'s own `H(dia[n]) == 1` forcing (`psi_kernel
.Endpoint`), composed with `flip_pairing`'s separate `cells[w][j] != c`
death check (used in `block_halving.chains`). `H_r(n)` membership requires
that composite (hard-core survival, cell equal to tail) hold through all
`n+r+2` rows, plus `terminal_pull` (continuation index `n+r-1`, `n+r` equal
`(1, 2)` exactly) — the correct comparison is `rw_population_h
.survival_curve` (which already applies `literal_extension` and checks only
hard-core, since `literal_extension`'s forcing guarantees the tail-equality
half of the composite automatically) against `block_halving.chains`'s `src`
array (hard-core **and** `cells[w][j] == c`, i.e. the same composite
condition, built from the independently-coded `psi_kernel`/`forced_orbit`
path). These are the two constructions V3(b) actually needs to check
against each other — not the raw per-symbol sequences of `literal_extension`
against `forced_orbit.syms`, which are different objects by construction
(4-valued edge-forcing vs. binary source-symbol forcing) and whose
disagreement proves nothing about the populations.

### Direct computation: exact match, nonzero, at every level

`verify_measure_suppression_alignment.py` (throwaway, not wired into any
pipeline) computes both for `n=9..12`, `tail in {2,3}`:

```
n=9  tail=2  alive_after: [512, 162, 57, 17, 4, 0, 0, 0, 0, 0, 0, 0]
             block_halving src: [512, 162, 57, 17, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0]
n=9  tail=3  alive_after: [512, 214, 112, 53, 23, 6, 6, 6, 6, 0, 0, 0]
             block_halving src: [512, 214, 112, 53, 23, 6, 6, 6, 6, 0, 0, 0, 0, 0]
n=10 tail=2  alive_after: [1024, 396, 177, 62, 26, 6, 0, ...]
             block_halving src: [1024, 396, 177, 62, 26, 6, 0, ..., 0]
n=10 tail=3  alive_after: [1024, 385, 159, 62, 22, 14, 12, 4, 0, ...]
             block_halving src: [1024, 385, 159, 62, 22, 14, 12, 4, 0, ..., 0]
n=11, n=12: same exact match, both tails, checked to n=12's full array.
```

Every value in `alive_after` (including the nonzero interior values `162,
57, 17, 4`; `214, 112, 53, 23, 6, 6, 6, 6`; etc. — not just the trailing
zeros) equals `block_halving`'s `src` at the identical index `j`, for the
full length of the shorter array (`block_halving`'s `src` is longer since
`levels = n+4` runs past where `alive_after` was asked to stop).

Matching counts alone would not rule out two constructions surviving
through different *sets* of words that happen to be the same size, so
`check_word_level_alignment` in the throwaway script goes one step further:
it computes, per word (indexed identically to `flip_pairing.census`'s own
`product((1,2), repeat=n)` enumeration), the death level under
`literal_extension` and the death level under `flip_pairing`'s
`hcs`/`cells` predicate, and diffs the two arrays directly. Result, `n=9,
10`, both tails: **0 mismatches out of 512 and 1024 words respectively** —
every single word dies at literally the same level under both
constructions, not merely the same count of words dying at each level.
This is the decisive check: two independently coded constructions
(`late_pull_diagonal_sat.literal_extension`'s edge-forcing, and
`psi_kernel.Endpoint`'s `H`-bit forcing plus `flip_pairing`'s separate
cell-comparison) survive *the same words* through *the same rows*, once
compared as the matching composite conditions rather than as raw
per-symbol sequences.

### What this establishes about `H_r(n)` specifically

`H_r(n)`'s own two conditions are (a) `N_{n+r+2}(n)` in this confirmed
sense (hard-core-and-tail-match survival through row `n+r+2`) and (b)
`terminal_pull`, an *additional* filter on top of (a). Note `terminal_pull`
reads continuation indices `n+r-1` and `n+r` — interior to the `n+r+2`-row
window, not just its boundary — so a word can survive all `n+r+2` rows and
still fail `terminal_pull` at an earlier index; the containment
`|H_r(n)| <= N_{n+r+2}(n)` is generically strict, not generically an
equality, and equality would require every one of that row's survivors to
also satisfy the interior `terminal_pull` check — not separately checked
here (it would need a nonzero `N_{n+r+2}(n)` to test against, see below). The
preregistration's own phrasing ("`N_n(n) = |H_r(n)|`") is corrected to
`N_{n+r+2}(n) >= |H_r(n)|`; the index is off by `r+2`, not absent, and
`block_halving.py`'s `levels = n+4` already computes far enough (`n+r+2 <=
n+4` for `r <= 2`) to cover it.

**Why a nonzero cross-check of the corrected index isn't available yet.**
Checked directly at `n=1..12`: `alive_after[n+r+2]` is `0` at every `(n,
tail, r)` tested, because `n+r+2` already exceeds the ~10-12-row survival
horizon these censuses show at every `n` tried so far (survivor counts hit
zero by row 8-11 regardless of `n`, while the required depth `n+r+2` grows
with `n`). This is consistent with — and gives a structural reason for —
`H_r(n)`'s already-documented empty census through `n=13`: it isn't a
coincidence that `H_r(n)` stays empty, it's that the required survival
depth for `H_r(n)` (`n+r+2` rows) is already past where `N_j(n)` empirically
dies for every `n` tested. The genuinely nonzero confirmation is the `N_j(n)
= alive_after[j]` equality itself (above), not yet a nonzero confirmation
of the `terminal_pull`-filtered subset relation, which needs a larger `n`
where `N_{n+r+2}(n) > 0` (not reached in the ranges checked here or, per
existing records, anywhere in this project so far).

## V4: does the `0.4^j` finding hold when re-cut by absolute position?

`flip_pairing_profile_20260903.log` (n=12..16, per-level death profiles)
tabulates `P(alive@j | delta)` where `delta = n-1-i` is depth-from-end of
the flipped index `i`. This is enough raw detail to re-cut by absolute
position `i` directly (`i = n-1-delta`), without a new run — a change of
variable on already-logged numbers, as prescribed.

Re-cut at fixed `j=1`, `c=2`, comparing across `n=12..16`:

**By depth-from-end `delta`** (as originally reported) — flat plateau
`~0.35-0.46` over most of the range, rising only at the largest `delta`
values (closest to the *start* of the word):
```
n=12: 0.43 0.43 0.39 0.40 0.40 0.43 0.46 0.44 0.46 0.50 0.70 0.97
n=16: 0.36 0.39 0.38 0.39 0.41 0.41 0.41 0.39 0.39 0.39 0.39 0.42 0.46 0.58 0.83 0.98
```

**By absolute position `i`** (re-cut, this document's computation) — for
fixed small `i`, the value is essentially constant across `n=12..16`:
```
i=0: n=12:0.97  n=13:0.95  n=14:0.97  n=15:0.98  n=16:0.98
i=1: n=12:0.70  n=13:0.71  n=14:0.77  n=15:0.80  n=16:0.83
i=2: n=12:0.50  n=13:0.49  n=14:0.55  n=15:0.55  n=16:0.58
i=3: n=12:0.46  n=13:0.45  n=14:0.45  n=15:0.44  n=16:0.46
i=4: n=12:0.44  n=13:0.44  n=14:0.40  n=15:0.40  n=16:0.42
i=5: n=12:0.46  n=13:0.42  n=14:0.41  n=15:0.41  n=16:0.39
```

**Reading.** The two ways of cutting the data do not contradict each other,
and the logs are detailed enough to check this without a re-run.
Re-cutting by absolute position confirms, rather than undermines,
`BACKLOG.md` section 17's own caveat ("only `e_0, e_1, e_2` preserve earlier
levels") — it is the first 2-3 absolute positions from the start of the
word that are special (near-certain survival, `~0.7-0.98`, stable across
`n`), and everywhere else (`i >= 3`) the value sits at the same `~0.4-0.46`
plateau regardless of which axis it is indexed by, because for `i >= 3`
both `delta` and `i` are far from either boundary. The depth-independence
claim survives re-cutting by absolute position, and the absolute-position
framing additionally shows the plateau value is stable **across `n`** at
fixed small `i` — a check the original delta-indexed framing could not make
as directly, since `delta` at fixed `i` shifts with `n`. Given V3(b)'s
confirmed alignment above, this is genuine (if indirect) supporting
evidence for the `H_r(n)`/RW route after all, though the preregistration's
own scoping is right that (M3)'s chain does not strictly need this mixing
fact — it needs only `block_halving`'s `k`, addressed next.

## V5 / K1: extended block-halving, `n=19..22`

<!-- FILLED IN BELOW ONCE THE BACKGROUND RUN COMPLETES -->

## What this document does and does not establish

- Does **not** establish `(*)` (`sum |H_r(n)|/2^n < infinity`). Untouched.
- Does **not** trigger K2: no term of `|H_r(n)|/2^n` was measured nonzero
  here; `H_r(n)` remains empty through the ranges checked, consistent with
  prior work, and V3(b) gives a structural reason (required depth `n+r+2`
  already exceeds the empirical survival horizon at every `n` tried).
- **Corrects, but does not kill, mechanism (M3):** the index the
  preregistration guessed (`N_n(n)`) is off by `r+2`; the right quantity is
  `N_{n+r+2}(n)`, confirmed equal to `rw_population_h.survival_curve`'s
  `alive_after[j]` at the matching `j`, exactly, at nonzero values, for
  `n=9..12`, both tails. `block_halving.py`'s existing `levels = n+4`
  already reaches the corrected index for all `r in {0,1,2}`, so no
  re-instrumentation is needed to use it. The chain in preregistration
  section 3 (`|H_r(n)| <= N_{n+r+2}(n) <= 2^{n - floor((n+r+2)/k)}`,
  `k <= 3` measured) is therefore live, contingent on V5/K1 below.
- Confirms V1, V3(a) as already-closed (cited from the prior pass, not
  re-derived).
- V4's re-cut is genuine new computation on old logs, and — now that V3(b)
  confirms the underlying population is the right one — bears (indirectly)
  on the `H_r(n)`/RW route rather than being moot to it.
- Does not modify `block_halving.py`, `flip_pairing.py`, `dlp_rotated_wedge.py`,
  `rw_population_h.py`, or any other existing file. Adds one throwaway
  script, `verify_measure_suppression_alignment.py`, and this results file.

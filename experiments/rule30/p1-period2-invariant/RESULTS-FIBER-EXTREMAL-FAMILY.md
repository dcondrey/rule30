# Fiber structure, missing-block stability, and extremal continuation family

Status: COMPLETE for n=10..16, r=0, both tails. Started and finished
2026-09-04 (single session, checkpointed incrementally throughout).

Object: `H_r(n)` via `late_pull_diagonal_sat.literal_extension(W, tail, rows)`,
map `Phi_k` (source word -> length-k forced continuation prefix), `D_k =
|image(Phi_k)|` computed by `continuation_image_analysis.py` (already in
this directory, read not modified). All numbers below are freshly recomputed
by new scripts in this file's directory; nothing is taken on faith from any
external/unverified analysis.

All work below uses r=0 (residue 0) unless stated otherwise, both tails
c=2 and c=3, per the task brief.

## 0. Recomputed k_star(n) baseline (own run, not copied from memory)

Script: `fiber_extremal_scan.py` (writes `fiber_extremal_scan_summary.json`).
Confirms the task brief's warning: **k_star(n) is NOT uniformly 6 or 7**; it
varies by n and by tail. Full D_k tables, n=10..16, r=0:

c=2:
```
n=10 k_star=4  D_k(k=1..11)= 2,3,5,5,2,0,0,0,0,0,0
n=11 k_star=4  D_k(k=1..13)= 2,3,5,5,3,1,0,0,0,0,0,0,0
n=12 k_star=5  D_k(k=1..14)= 2,3,5,8,9,5,2,1,1,0,0,0,0,0
n=13 k_star=5  D_k(k=1..15)= 2,3,5,8,11,8,2,0,0,0,0,0,0,0,0
n=14 k_star=5  D_k(k=1..16)= 2,3,5,8,10,9,3,2,1,1,0,0,0,0,0,0
n=15 k_star=5  D_k(k=1..17)= 2,3,5,8,11,10,10,4,3,0,0,0,0,0,0,0,0
n=16 k_star=6  D_k(k=1..18)= 2,3,5,8,13,20,19,6,3,1,0,0,0,0,0,0,0,0
```
(the n=16,c=2 row matches the task brief's stated table exactly, k_star=6
confirmed independently.)

c=3:
```
n=10 k_star=4  D_k(k=1..12)= 2,3,5,6,4,4,1,0,0,0,0,0
n=11 k_star=5  D_k(k=1..13)= 2,3,5,8,8,5,4,0,0,0,0,0,0
n=12 k_star=5  D_k(k=1..14)= 2,3,5,8,7,2,1,1,0,0,0,0,0,0
n=13 k_star=5  D_k(k=1..15)= 2,3,5,8,9,6,3,1,1,0,0,0,0,0,0
n=14 k_star=6  D_k(k=1..16)= 2,3,5,8,13,8,7,3,0,0,0,0,0,0,0,0
n=15 k_star=6  D_k(k=1..17)= 2,3,5,8,13,17,8,3,0,0,0,0,0,0,0,0,0
n=16 k_star=6  D_k(k=1..18)= 2,3,5,8,13,18,14,7,5,2,0,0,0,0,0,0,0,0
```

k_star(n): c=2 gives 4,4,5,5,5,5,6 for n=10..16; c=3 gives 4,5,5,5,6,6,6.
Neither is constant, and c=2/c=3 disagree at several n (e.g. n=14: k_star=5
vs 6). No single k_star works for all n in this range; whatever k_star(n)
converges to as n grows is not yet visible from n<=16 alone (weakly
increasing, roughly floor-ish in n, consistent with — but not proof of — a
step tied to Fibonacci-index crossing n, see part 3 below).

Script: `fiber_full_analysis.py` (single pass per (n,tail) via
`continuation_image_analysis.d_k_table`, reused for items 1-3 below; output
in `fiber_full_analysis.json`, full run log `fiber_full_analysis_20260904.log`).

## 1. Exhaustive fiber dump at the last nonzero depths, n=10..16, both c

For each (n,tail), the last `min(4, #nonzero-D_k-depths)` values of k with
`D_k>0` were dumped in full: every continuation `C` at that depth, its
complete preimage (fiber) of source words `W`, the longest common suffix
among the fiber's words, and the "residual" `W[:len(W)-len(suffix)]`.

**Fibonacci-fiber-size hypothesis: DISCONFIRMED.** Across all fibers dumped
(n=10..16, both tails, last-4-nonzero-depths each), the observed fiber sizes
include 6, 7, 9, 10, 11, 12, 14, 15, 17, 18, 19, 20, 22, 23, 24, 25, 27, 28,
35, 40, 42, 58, 77, 81 — none of these is a Fibonacci number. Full size
histogram (size: count of fibers with that size), computed directly from
`fiber_full_analysis.json`:
```
1:11  2:63  3:24  4:78  5:1   6:15  7:3   8:14  9:5   10:11 11:8  12:5
13:3  14:10 15:3  16:8  17:2  18:2  19:2  20:3  21:2  22:3  23:1  24:1
25:2  27:1  28:1  34:3  35:1  40:2  42:1  58:1  77:1  81:1
```
Some Fibonacci values do appear (1,2,3,5,8,13,21,34) but so do many
non-Fibonacci integers, and powers of two (2,4,8,16) are also heavily
overrepresented relative to a Fibonacci-only hypothesis. Neither "fiber
sizes are Fibonacci numbers" nor "fiber sizes are powers of two" survives
as a clean closed statement; the true size distribution is richer than
either guess (see below for the partial regularity that *does* hold).

**Residual-prefix structure — the one clean partial regularity found.**
For every fiber inspected (worked example: n=16, c=2, k=7..10, full table in
`fiber_full_analysis.json` under key `n16_c2`), the residual prefixes
recovered after stripping the fiber's common suffix range over a set of
binary strings that is (a) closed under exactly the fiber-size-many
"free" bit patterns of the residual length whenever fiber size equals
2^(residual length) exactly — e.g. at n=16,c=2,k=7, `C=1222222` has fiber
size 4 with residual length 2 and residual set exactly `{11,12,21,22}` (all
four 2-bit strings, hard-core or not — note `11` occurs, so the residual is
**not** hard-core-constrained, it is genuinely free); `C=1222221` has size 2,
residual length 1, residual set `{1,2}` (both symbols, free) — **but** most
fibers do NOT have this free-full-set property: e.g. `C=1212212` (k=7) has
fiber size 16 with residual length 7 (2^7=128 possible strings, only 16
realized), so the residual is genuinely constrained there, just not by the
plain hard-core rule (sampled residuals include `1111122`, which contains an
internal `11`). Conclusion: the residual language is córrelated with fiber
size in the small-residual-length regime (fully free) but becomes a proper,
structurally opaque subset of {1,2}^m once the residual gets longer; no
single finite forbidden-block description for the residual language was
found in the time available. This is a legitimate open sub-question, not a
result — flagging it rather than forcing a guess.

Full per-fiber tables (C, fiber size, common suffix, residual set) for every
(n,tail) in 10..16 and every dumped depth are in `fiber_full_analysis.json`
(key `fibers`, keyed by k). The n=16,c=2 table (the flagship case from the
task brief) prints in full via:
```
uv run python -c "import json; d=json.load(open('fiber_full_analysis.json'));
import pprint; pprint.pprint(d['n16_c2']['fibers'])"
```

## 2. Missing-block census at k_star(n), both c, n=10..16

For each (n,tail), k_star(n,tail) was recomputed (section 0), the hard-core
words of length k_star enumerated via `rank_zero_separator.hard_core_prefixes`,
and the ones absent from `image(Phi_{k_star})` listed:

```
n10_c2 k_star=4 missing_count=3  missing=[1222, 2122, 2212]
n10_c3 k_star=4 missing_count=2  missing=[2121, 2221]
n11_c2 k_star=4 missing_count=3  missing=[1212, 1222, 2122]
n11_c3 k_star=5 missing_count=5  missing=[12121, 12122, 12212, 12222, 22221]
n12_c2 k_star=5 missing_count=4  missing=[12122, 12212, 21221, 22212]
n12_c3 k_star=5 missing_count=6  missing=[12122, 12212, 12221, 12222, 21221, 22121]
n13_c2 k_star=5 missing_count=2  missing=[12121, 12122]
n13_c3 k_star=5 missing_count=4  missing=[12122, 12212, 22121, 22222]
n14_c2 k_star=5 missing_count=3  missing=[12212, 12221, 22121]
n14_c3 k_star=6 missing_count=13 missing=[121212,121221,122121,122122,122212,
                                          122221,212121,212222,221212,221221,
                                          221222,222122,222221]
n15_c2 k_star=5 missing_count=2  missing=[12121, 12221]
n15_c3 k_star=6 missing_count=4  missing=[121222, 122122, 122222, 212121]
n16_c2 k_star=6 missing_count=1  missing=[222222]
n16_c3 k_star=6 missing_count=3  missing=[121222, 122122, 122212]
```

**Verdict: NOT stable.** Even restricting to the four n's that share
k_star=5 for c=2 (n=12,13,14,15), the missing sets are `{12122,12212,21221,
22212}`, `{12121,12122}`, `{12212,12221,22121}`, `{12121,12221}` — no common
word, no common prefix, no common suffix across all four, and the missing
count itself is not monotone (4,2,3,2). The missing-count is not even
monotone increasing in n at fixed k_star. There is no evidence in n<=16 of
an n-independent forbidden-block / regular-language description of the
image language: the missing set genuinely reshuffles as n grows rather than
stabilizing on a fixed "kind" of excluded continuation. (One mild
regularity: at c=2, the all-constant-2 word of length k_star appears in the
missing set only once in this range, at n=16 — where it is, in fact, the
*only* missing word — otherwise it is reachable. This is too thin a pattern
to call a rule; noted for completeness, not claimed as a finding.)

## 3. Extremal continuation family

Extremal continuations = the ones reaching `k_max(n,tail)`, the last depth
with `D_k>0` (matches the task's "D_k=1 or last nonzero D_k" definition —
whenever the last nonzero D_k is exactly 1 there is a unique extremal word;
otherwise there are several tied at that depth, all listed):

```
n10_c2 k_max= 5  extremal={12121, 22222}
n10_c3 k_max= 7  extremal={1222121}
n11_c2 k_max= 6  extremal={212121}
n11_c3 k_max= 7  extremal={2121212, 2121222, 2122221, 2222212}
n12_c2 k_max= 9  extremal={212222222}
n12_c3 k_max= 8  extremal={22221222}
n13_c2 k_max= 7  extremal={2221222, 2222222}
n13_c3 k_max= 9  extremal={222122121}
n14_c2 k_max=10  extremal={2122221221}
n14_c3 k_max= 8  extremal={12122221, 22212122, 22222212}
n15_c2 k_max= 9  extremal={212222121, 221221212, 222212121}
n15_c3 k_max= 8  extremal={12222121, 22122222, 22212122}
n16_c2 k_max=10  extremal={2221212222}
n16_c3 k_max=10  extremal={2121212121, 2212121212}
```

**Verdict: NO clean parametrized family found. This is a genuine negative
result, not a gap in effort.** Candidates explicitly checked against this
data and rejected:

- `2^a` (all-2 continuation): only ever extremal at n=10,c=2 (tied with
  `12121`) and n=13,c=2 (tied with `2221222`); at every other n it is either
  not extremal or not even present at k_max.
- `21·2^a` / `2^a·1·2^b` (single defect in an otherwise-constant run): fits
  `n12_c2` (`212222222` = `2`+`1`+`2^7`) and arguably `n13_c3`
  (`222122121`, two defects) but not `n11_c3` (four tied extremals, one of
  which, `2121212`, is fully alternating, not one-defect) or `n16_c3`
  (`2121212121`/`2212121212`, fully alternating up to a boundary shift).
- Pure alternation `(21)^a` or `(12)^a`: fits n11_c2 (`212121`) and one of
  the two n16_c3 extremals, but fails at n10_c2, n12_c2, n14_c2, etc.
- `k_max(n)` itself was checked for a closed form (e.g. tied to a
  Fibonacci-index crossing of n, or linear in n): observed sequence
  (c=2) 5,6,9,7,10,9,10 and (c=3) 7,7,8,9,8,8,10 for n=10..16 — neither
  monotone nor arithmetic; no fit attempted further given the extremal-word
  set itself already fails to unify.

No family closed under the forcing recursion emerged, so the planned
inductive/hand-proof step (using `append_dependency_edge`/`cone_local` to
show closure) was **not attempted** — there is no candidate family to prove
closure for. This is the honest outcome asked for in the task brief when
"nothing clean emerges": a real, checked negative, not a forced fit. If a
family is to be found, the data suggests it will not be visible from raw
extremal-continuation strings alone; the fiber-size/residual data in
section 1 (particularly the "free at short residual length" cases) is a
more promising lead for follow-up than the extremal continuations
themselves.

## 4. Two-row-back dependency check

`append_dependency_edge(edge, previous_endpoint, value)` builds `following`
by: `following[0] = BOUNDARY[value]`; `following[1] = cone_local(previous,
following[0])`; and, for `order` in `2..len(edge)`, `following[order] =
cone_local(edge[order-2], following[order-1])`. Traced directly
(`endpoint`/`edge` length growth for a concrete word, `1,2,1,2,2,1,2` with
7 leading zero-padding symbols):

```
step | value | len(edge) before | len(edge) after
   0 |   0   |        0         |       1
   1 |   0   |        1         |       2
   2 |   0   |        2         |       3      <- first order=2 loop entry (edge[0] used)
   3 |   0   |        3         |       4
   ...
```

The `edge[order-2]` ("two-row-back") reference first activates at the
**third** call to `append_dependency_edge` (`order=2` first appears in the
`range(2, len(edge)+1)` loop once `len(edge)==2`), for every word tested,
regardless of n, tail, or content. This is a fixed structural feature of
the exact diagonal recurrence (identical in shape to
`dyadic_periodicity_analyzer.inverse_cone_diagonal`'s `older[index+1]`
alignment) — it is not an event that "switches on" at some n-dependent or
content-dependent point. **Verdict: no correlation with k_star(n) was
found, because the premise does not identify a variable transition to
correlate against** — the two-back dependency is active from the third
symbol of every run, hard-core-excluded or not, long before any k_star in
the n=10..16 range (k_star>=4 always). I looked for an alternative reading
("self-referential loop" = the forced continuation's own earlier symbol
re-entering as `edge[order-2]` rather than a *source* symbol) but every
`edge[order-2]` reference already mixes information from arbitrarily far
back in the diagonal (it is a folded encoding of the whole history, by
construction of the cone recursion), so there is no clean single index at
which "the continuation starts depending on itself" either — it always
does, from the first extension row on. This item did not yield a
combinatorial explanation for k_star's location; reported as a genuine
negative, investigated concretely (not assumed).

## Summary verdict

Item 3 (extremal family) was the one flagged as highest-value if it
produced a hand-provable lemma. It did not: the extremal continuations at
n=10..16 do not fall into any single simple parametrized family, so no
inductive closure argument was attempted (there was nothing concrete to
prove). Item 1's Fibonacci-fiber-size hypothesis is cleanly disconfirmed
by counterexample; the one real partial regularity (residual prefixes are
literally the full 2^m free set exactly when fiber size is small enough,
`m` small) is reported as an open lead, not a lemma. Item 2's missing-block
set does not stabilize across n. Item 4's premise does not isolate a
variable event to test against k_star. All four investigations were run to
genuine completion on n=10..16 with fresh, from-scratch computation (no
number taken from the unverified external analysis); the honest overall
outcome tonight is negative/exploratory rather than a new lemma — reported
as such rather than forcing a fit to few data points.

Scripts written tonight (new filenames, no existing file modified):
`fiber_extremal_scan.py` (k_star/D_k baseline, writes
`fiber_extremal_scan_summary.json`), `fiber_full_analysis.py` (fibers +
missing-block + extremal census, writes `fiber_full_analysis.json`, log
`fiber_full_analysis_20260904.log`). Both are read-only over
`late_pull_diagonal_sat.py`, `continuation_image_analysis.py`,
`constant_tail_scale.py`, and `rank_zero_separator.py` — no existing file
was edited.

# Transferring the strip method to the zero-cost frontier

Date: 2026-09-09. Overnight Task 4.

**A sound finite-width relaxation exists, but the direct transfer cannot
prove mortality: the usual fixed-prefix and free-carry suffix relaxations
are total on nonempty states. The moving terminal condition is the missing
information.** This is an obstruction for two specified abstractions, not
an impossibility theorem for every possible finite summary.

| Finding | Level |
|---|---|
| Reversed-prefix evolution is exactly autonomous at every width | `U`, triangular recurrence |
| Every scan memory admits an accepting continuation of length at most two | `U/C`, all eight memories |
| The prefix abstraction therefore has no rejecting state for unbounded lengths | `U`, finite completion plus triangularity |
| A terminal suffix with arbitrary entering scan memory has four accepting memories for every word | `U`, toggling the entering u bit |
| Fixed-suffix equality does not determine the terminal test | `K`, length-two witness |
| Soundness of these relaxations established before computation | `U`, projection maps below |

## 1. Exact state and projection

Use the reversed coordinates in
[RESULTS-alt-trace-fiber.md](RESULTS-alt-trace-fiber.md), lines 532–558,
implemented by `panel/cert33.py:direct_step` and
`image-dfa/image_dfa.py:trans_step`. At length `r`, encode a state by
symbols `s_k=2*a_k+b_k`, with `a_0=1`. Scan with entering memory
`(u,v,alpha)=(0,0,0)`:

```
v' = v XOR (alpha OR b)
u' = u XOR (v' OR a)
alpha' = a
```

Emit `(u',v')`. After the **last** input symbol, survival requires `u=v`;
append `(1,1 XOR v)`. This is a partial map from length `r` to length `r+1`.

For `r>=W`, project to the first `W` input symbols. Their emitted prefix
depends only on those symbols. Hence every surviving full transition maps
to the autonomous prefix transition `f_W`. The first emitted high bit is
always one, so `f_W` maps the finite legal-prefix set into itself.
Dropping the terminal test is sound, but makes every trajectory infinite.

Even existentially retaining that test does not repair this abstraction:
after any prefix, the scan has one of eight memories. The exact completion
table in `alt-strip-transfer/results.json` gives a suffix of length at most
two that reaches `u=v` from each memory. Consequently **every** legal prefix
has some surviving finite completion, and the one-step existential
projection still contains the total map `f_W`. Completions at successive
times need not come from one common initial configuration.

## 2. Keeping the terminal end instead

Project a long state to its last `W` symbols. To keep soundness, the omitted
prefix's entering scan memory must be retained or over-approximated.
Allowing all eight memories is sound: it includes the actual one.
Scan the suffix, enforce `u=v`, append the terminal symbol, then retain the
new last `W` symbols. Every real surviving transition projects into this
relation, including the dropped first suffix symbol and new final symbol.

This relation also cannot empty a nonempty set. For fixed suffix, entering
`v` and `alpha`, toggling entering `u` toggles every emitted `u` and leaves
every `v` unchanged. Exactly one choice passes the final equality. Thus each
suffix has **four** accepted entering memories, at every width.

The smallest explicit loss of information is:

```
input symbols (2,2): scan ends at memory (0,1,1), fails
input symbols (3,2): scan ends at memory (0,0,1), survives
```

The retained one-symbol suffix is `2` in both cases. Setting the omitted
carry to zero instead of allowing its actual possibilities would be unsound.

## 3. Why the seam argument works and what remains possible

The family-seam strip keeps the observable column 1 and tests each next
rho bit at that fixed location. Allowing both exterior bits preserves those
tests. An incompatible finite observation word can therefore empty the
relation. For the zero-cost prefix, the relevant test moves out of the
window; for the free-carry suffix, the omitted carry can always satisfy it.
The obstruction is loss of the terminal test or its compatible history,
not growth alone and not the impossibility of a sound projection.

For each fixed initial length, exact finite-state images can still go
extinct as recorded in the original report. They retain the whole finite
frontier as it grows. The existing image-DFA construction also preserves
the terminal symbol and represents exact regular languages across all
lengths. Neither is the fixed-width relaxation proposed here. Nonemptiness
over all initial lengths at every horizon does not imply a single immortal
finite seed: the initial length may vary with the horizon.

A successful refinement would have to constrain the entering carry by its
actual reachable prefix/history, or preserve the moving terminal boundary
with an exact length-dependent representation. No such new closure or
mortality proof is claimed. The single-column sensitivity filter is not
applicable to these exact states; no averaged statistic is introduced.
This report proves no P1 exclusion, so the totality obstruction is not a
purported Rule-90-discriminating route. The shared unchanged Rule 90
controls are recorded in the Task 3 artifact.

## 4. Checks and reproduction

`check.py` compares 2,730 full scans at lengths 1–6 against the independent
`direct_step`, including the final acceptance and appended-symbol boundary.
It records prefix cycles at each width, all eight completion cases, the
suffix counterexample, and all free-carry suffix rows at widths 1–4.
These finite checks accompany the explicit uniform arguments above.

```
PYTHONDONTWRITEBYTECODE=1 uv run --no-project python experiments/rule30/alt-strip-transfer/check.py
```

Frozen sources are imported read-only and hashed in the JSON. No large
computation on an unproved abstraction was performed. S4 and the mortality
obligation remain open.

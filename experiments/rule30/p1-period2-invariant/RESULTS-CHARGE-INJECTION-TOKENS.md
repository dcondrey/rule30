# Charge inequality (12): the single-flip dependency graph cannot carry its charge at n = 17, the pre-registered kill fired

Date: 2026-09-16. Pre-registration `PREREGISTRATION-CHARGE-INJECTION-TOKENS.md`.
Script `charge-injection/injection_tokens.py`, log
`charge-injection/injection_tokens_n8-18.log` (exit code 0, 66 lines).
Kernel `psi_kernel.py` and `seam_history_inheritance.run`. Gate against
`charge-injection/injection_probe_n8-16.log`.

**The kill of the pre-registration fired. `[K]` The hard-core word
`W = 12212121212121212` (`n = 17`, `c = 2`, the sole slack-zero word of
inequality (12)) has `run_2(W) = 10`, and the maximum matching of its ten
forced steps into the `2`-positions of their single-flip dependency sets is
`m_2 = 8`, so `m_2 + [22 in W] - run = 8 + 1 - 10 = -1 < 0`: statement
(R-universal) is false, and the factor reading (R-factor) is false on the same
word by the same margin (`m_factor = 9`). The witness is a Hall violation by
inspection: over all ten steps the union of `2`-positions that any step depends
on is `{2, 4, 6, 8, 10, 12, 14, 16}`, eight tokens, because position 1 (the
first symbol of the `22` factor) is in no `D_j` at all. `[C]` Elsewhere the
matching carries the charge: at `n = 8..16` the new script reproduces the probe
log exactly (`min(m_2 - run) = 0` at `c = 2`, `-1, -3, -1, 0, 0, 0, 0, 0, 0` at
`c = 3`, mean `|D_j|` equal to one decimal at all eighteen `(n, c)`), at
`n = 18` and both `c` every hard-core word has `m_2 >= run` (the greedy
oldest-unused deficit of 1 at `n = 18` recorded in
`RESULTS-CHARGE-INJECTION-PROBE.md` was a greedy artefact, not a matching
deficit), and at `n = 17, c = 3` likewise. The only words with `m_2 < run`
at `n = 17, 18` are the two `c = 2` words `12212121212121212` (`m_2 = 8`) and
`22212121212121212` (`m_2 = 9`, run 10, credit used exactly). `[R]` So the
`+[22 in W]` credit of (12) is not a token the single-flip dependency graph
can reach: on the tight word the credit needs to be worth two, or the graph
needs an edge the single-flip test does not see. A proof of (12) by injection
into the token set of (12), with single-flip dependency as the adjacency, is
closed; nothing here weakens (12) itself, which remains exact to `n <= 30` by
the earlier census.**

## 1. Objects

Hard-core words `W` (no factor `11`) of length `n = 8..18`, tail `c` in
`{2, 3}`. `run_c(W)` and forced symbols `Q` are
`seam_history_inheritance.run(endpoint(W), W, n, c, "wide", n + 4)`.
`cut_j(W') = Endpoint(W' Q[:j]).peek(Q[j])[1][n]` and
`D_j(W) = {i : cut_j(W with W_i flipped) != c}`, exactly as in
`injection_probe.py` (code reused verbatim: `words`, `endpoint`, `cut`,
`max_matching`, an augmenting-path matching).

Tokens. `m_2`: steps `j < run` matched to distinct `i in D_j` with `W_i = 2`.
`credit = [22 occurs in W]` at `c = 2`, `3` at `c = 3`;
`d_univ = m_2 + credit - run`, which is the maximum matching once `credit`
universal tokens (adjacent to every step) are added, minus the run.
`m_factor`: tokens are the `2`-positions plus one token per occurrence of `22`
at `(i, i+1)`, adjacent to step `j` iff `i in D_j` or `i+1 in D_j`, plus three
universal tokens at `c = 3`; `d_factor = m_factor - run`. A credit user is a
word with `m_2 < run`.

Kill (pre-registered): any hard-core `W`, `n <= 18`, with `d_univ < 0`.

## 2. Result

Per `(n, c)`, minimum over words (log lines `n=<n> c=<c>:`; the `c = 3`
`min(m_2 - run)` column is the gate):

| `n` | `c=2` min `m_2-run` | `c=2` min `d_univ` | `c=2` min `d_factor` | `c=3` min `m_2-run` | `c=3` min `d_univ` | `c=3` min `d_factor` | mean `|D_j|` `c=2` / `c=3` | min `|D_j|` `c=2` / `c=3` |
|---|---|---|---|---|---|---|---|---|
| 8 | 0 | 1 | 0 | -1 | 2 | 0 | 4.6 / 5.0 | 3 / 1 |
| 9 | 0 | 1 | 0 | -3 | 0 | 0 | 5.7 / 4.8 | 4 / 2 |
| 10 | 0 | 0 | 0 | -1 | 2 | 0 | 6.0 / 5.9 | 3 / 3 |
| 11 | 0 | 1 | 0 | 0 | 3 | 0 | 6.8 / 6.5 | 2 / 3 |
| 12 | 0 | 0 | 0 | 0 | 3 | 0 | 7.0 / 7.7 | 3 / 4 |
| 13 | 0 | 1 | 0 | 0 | 3 | 0 | 8.4 / 7.9 | 4 / 3 |
| 14 | 0 | 0 | 0 | 0 | 3 | 0 | 8.8 / 8.7 | 4 / 3 |
| 15 | 0 | 1 | 0 | 0 | 3 | 0 | 9.4 / 9.5 | 4 / 5 |
| 16 | 0 | 0 | 0 | 0 | 3 | 0 | 9.9 / 10.1 | 3 / 5 |
| 17 | **-2** | **-1** | **-1** | 0 | 3 | 0 | 10.4 / 10.9 | 4 / 6 |
| 18 | 0 | 1 | 0 | 0 | 3 | 0 | 11.0 / 11.2 | 5 / 5 |

Gate: rows `n = 8..16` agree with `injection_probe_n8-16.log` in
`min(m_2 - run)` at both `c` and in mean `|D_j|` at every entry (log lines
1..54 against probe lines 1..22). The gate would have failed on any differing
entry, and did not.

Credit users at `n = 17, 18` (log lines 55..66): none at `c = 3`, none at
`n = 18`, two at `n = 17, c = 2`.

| `W` | run | `m_2` | `#2` | `#22` | credit | `m_factor` | `d_univ` | `d_factor` |
|---|---|---|---|---|---|---|---|---|
| `12212121212121212` | 10 | 8 | 9 | 1 | 1 | 9 | **-1** | **-1** |
| `22212121212121212` | 10 | 9 | 10 | 2 | 1 | 10 | 0 | 0 |

Witness for the kill (log line 58, recomputed independently by a scratch
script from the same kernel: forced `Q = 2122122121`, `D_j` per step):

```text
step  2-positions of D_j
0     6 10 12 14
1     2 4 6 8 12 14 16
2     2 4 6 8 12 14 16
3     2 4 6 8 10 12 14 16
4     2 4 6 8 10 12 14 16
5     4 6 8 10 14 16
6     4 6 8 10 12 14 16
7     8 10
8     6 8 10 12 14
9     8 10 12 14
```

Position 1 (the first `2` of `22`, zero-based) and position 0 are in no `D_j`.
The neighbourhood of the full step set is eight positions, so by Hall's
condition `m_2 <= 8`; the matching routine returns 8, and eight is attained
(steps 0..7 to 6, 2, 4, 10, 12, 14, 16, 8 for instance, leaving steps 8 and 9
unmatched). The `22` factor token is adjacent to steps 1..4 through position 2,
so `m_factor = 9`, still one short.

The second word `22212121212121212` differs only by a `2` at position 0, which
enters `D_0` (log line 60) and restores `m_2 = 9`; the universal credit then
makes it exactly saturating.

## 3. Reading

The single-flip dependency graph is too sparse by one token on exactly the
word where (12) has zero slack. The missing token is the first symbol of the
`22` factor: flipping it never changes any cut cell along the forced run, so no
matching-based charge can reach it. (12) gives the word one credit for `22`;
the graph needs that credit to be worth two, since it loses both the position
that (12) does not count (position 1 is a `2` that (12) counts, but the
graph cannot see it) and the one (12) compensates with `[22 in W]`. Put
differently, `#2(W) + [22 in W] = 10 = run`, and the graph reaches only 8 of
the 9 counted `2`s.

What is closed: a proof of (12) of the form "step `j` is charged to a token it
depends on under a single flip", for the token set (12) names, with either
credit reading. What is not closed: a dependency notion that is not single
flip (pairs of flips, or the full Boolean dependency of the cut on the source),
or a token set in which the `22` factor contributes two tokens, or a charge
that is not a matching. None of these is pre-registered here. The
capsule's section 6.4 phrase "phase-decorated injection into the `n` ordered
source tokens" survives only if the decoration supplies the second token; the
bare injection does not.

Where the graph does carry the charge (every other word to `n = 18`), the
greedy shortfalls of `greedy_rules_n8-18.log` at `n = 18` (1 at `c = 2`
oldest-unused, 1 at `c = 3` newest-unused) are artefacts of the greedy order:
the maximum matching saturates all of `n = 18`. At `n = 17` the greedy deficit
of 3 overshoots the true deficit of 2 by one.

`RW`, `SEP`, `PT2` untouched. (12) itself is unaffected: it remains an
empirical inequality exact to `n <= 30`.

## 4. Scope

Finite: hard-core words `n = 8..18`, wide grammar, one implementation of
`D_j` (single flip, forced prefix held fixed), one matching routine. The
independent checker named in the pre-registration,
`crosscheck/charge-injection/check_tokens.py` (written by another session,
log `check_tokens_n8-18.log`, `witness_check.log`), agrees with this script
at every `(n, c)`, `n = 8..18`, on `min(m_2 - run)`, `min d_factor`, the
number of words with `m_2 < run`, and mean `|D_j|`, and on the witness word
reproduces the ten `D_j` sets above and `m_2 = 8` by brute force
(`witness_check.log`, last line). Its `min d_univ` column differs from the
table above at `c = 2` for `n = 8, 9, 11, 13, 15, 18` only because it includes
words with `run = 0` (`d_univ = 0` there), which this script and the probe
exclude; on words with `run > 0` the two agree. The kill witness was also
recomputed by a scratch script using the same kernel. The run is
`F(19) + F(20)` words at `n = 17, 18` and completed in well under the
budgeted 15 min with four workers.

## 5. Reproduction

```sh
cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant
uv run --no-project python charge-injection/injection_tokens.py 8 18 > charge-injection/injection_tokens_n8-18.log 2>&1; echo rc=$?
uv run --no-project python charge-injection/injection_probe.py 16   # gate source, 4 min
```

A run disconfirming this document would show `min d_univ >= 0` on the
`n=17 c=2` line, or a `D_j` for the tight word containing position 1.

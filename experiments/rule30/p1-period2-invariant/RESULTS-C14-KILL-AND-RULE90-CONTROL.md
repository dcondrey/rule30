# C14 killed; the Rule 90 control on C3 is ill-posed as specified

Date: 2026-09-06. Scripts: `zero_prefix_greedy_invariant_probe.py` (C14),
`rule90_control_on_c3.py` (control).

Status: **C14 (`j in S_j`, the speed-1 claim) IS DEAD: 1,664 failures of 2,386
legal rows through length 14. The Rule 90 filter on C3 DID NOT FIRE IN EITHER
DIRECTION. Its verdict oscillates by source length (0 failures of 971 legal rows
at `n=13`, 987 of 987 at `n=15`, 0 of 3,795 at `n=16`), which is degeneracy, not
a filter result. Do not read it as "the OR is load-bearing" and do not read it
as "route (2) is dead".**

Evidence level: `K` for the C14 kill. The control is **not** assigned a level;
it is reported as a failed instrument, with the reason and the fix.

## 1. C14 is dead

> `C14`: `j in S_j`, i.e. `A_(j,j) != A_(j,j+1)`. Flips only the diagonal symbol
> `W[j]`, leaving `W[j+1:]` alone; the natural speed-1 light-cone claim, and
> strictly stronger than `C3`.

Scored on the frozen graph, same legal-row filter, both tails:

```text
length <= 12   617 failures / 964 legal rows
length <= 14  1664 failures / 2386 legal rows
first witness  W=1222, tail 2, row 0, S_j = {1,2}   (0 not in S_j)
```

The observation that motivated it — every `S_j` printed in
`RESULTS-ZERO-PREFIX-GREEDY-REDUCTION.md` happens to contain its own row index —
was true of those five printed sets and false in general. Those sets were
selected as witnesses for other candidates, so they were never a sample of
anything. Scoring it cost one line.

Consequence: the diagonal token can be silent, so `C3`'s freedom to use some
later `k > j` is load-bearing, and there is no local one-step identity to look
for. `C12` already showed the whole block can cancel; `C14` shows the adjacent
edge can vanish too. The remaining shape is the `C3''` one: classify the
shortest affine-neutral nonempty suffixes and show one of them is illegal on a
legal row.

## 2. The Rule 90 control, and why it does not decide anything

### 2.1 What had to be built

"Swap the table" is not available. The frozen pipeline carries the newest-cut
map in the D8 affine coordinates `(alpha, beta, gamma)`, and those coordinates
are Rule-30 specific: `newest_affine_bits` builds each local element from
`activity = high | low` and `not low`, which are exactly the two ORs of
`carry_action`. So the control needed an explicit-permutation rewrite, carrying
the newest-cut map as a 4-state permutation, with the carry action a parameter.

Rule 30 forces `x_(i-1) = x'_i XOR (x_i OR x_(i+1))`, i.e.
`c' = c XOR (a OR b)`, `d' = d XOR (c OR a)`. `RESULTS-COLUMN-DECOMPOSITION.md`
sec. 1a states the same reading: the carry "reads its symbol only through
`(a|b)` and `a`". Rule 90 forces `x_(i-1) = x'_i XOR x_(i+1)`, so each OR
collapses to its right argument: `c' = c XOR b`, `d' = d XOR a`.

Validation, all of it passing:

- `rule30.forward/inverse/boundary` are identical to
  `dyadic_periodicity_analyzer`'s tables, asserted at table level.
- The composition convention (`local_first=True`, forced symbol `A^-1(c)`) is
  not assumed; all four combinations are tried and the one reproducing
  `zero_prefix_bitsliced_graph` is kept. It reproduces it **exactly**, both
  `S_j` and survival, on every hard-core word to length 12, both tails. If none
  matched, the script exits refusing to report a control.
- Run through the rewrite, Rule 30 gives 2,386 legal rows and 0 `C3` failures at
  length 14, matching the frozen probe row-for-row.
- `Phi(2,.) = Phi(3,.)` holds for Rule 30 and fails for Rule 90, as the paper
  says it should.
- Newest-cut group: Rule 30 order 8, non-abelian; Rule 90 order 4, abelian.

The one step **not** inherited from the repo is `rule90_carry` itself.

### 2.2 The result, which is incoherent

`C3` failures for Rule 90, by source length, legal rows only:

```text
n     1   3   4   6   7    9   10   12   13    15     16
rows  4   3  12  16  68   67  208  296  971   987   3795
fail  4   3   0   0  34    0    0    0    0   987      0
```

`n = 2, 5, 8, 11, 14` contribute zero legal rows at all. A statistic that is
0/971 at one length, 987/987 at the next, and 0/3795 at the next is not
measuring the property in its title.

### 2.2a The failure lengths are exactly `2^r - 1`

Added 2026-09-07, prompted by an outside suggestion that Rule 90's linearity
should produce Lucas-style binomial vanishing. Tabulating every length with a
nonzero legal-row count:

```text
n      1   3   4   6   7    9   10   12   13    15     16
rows   4   3  12  16  68   67  208  296  971   987   3795
fail   4   3   0   0  34    0    0    0    0   987      0
```

Failures occur at `n = 1, 3, 7, 15` and nowhere else. Those are exactly
`2^r - 1`. Every other length carrying legal rows (4, 6, 9, 10, 12, 13, 16) has
zero. `n = 7` is exactly half, 34 of 68.

This is a real dyadic fingerprint and it is consistent with binomial-mod-2
cancellation in Rule 90's abelian order-4 group. It does **not** rescue the
control, and it refutes the stronger reading that C3 simply fails for Rule 90:
at `n = 13` and `n = 16`, on 971 and 3,795 legal rows, C3 holds. The verdict
remains length-dependent, so §2.3 stands unchanged.

### 2.3 Why, and what would fix it

Rule 90's newest-cut group is abelian of order 4 — translations — so `A_j`
depends on the source only through a pair of parities. Across a zero-prefix
chain those parities are usually constant (giving `S_j` empty or trivial) and
occasionally flip wholesale. That is the oscillation.

The deeper problem is that the control transplants Rule-30 objects onto Rule 90.
The hard-core source language (`{1,2}`, no `11`) is the invariant SFT of *Rule
30's* forcing, and the constant tails `c in {2,3}` come from "the first infinite
cut is `2^omega` or `3^omega`", also Rule 30's. Running Rule 90's carry on Rule
30's language and Rule 30's tails is not Rule 90's forcing problem. So the
instrument is ill-posed, and the numbers above are what an ill-posed instrument
produces.

A well-posed control has to derive Rule 90's own invariant SFT and its own
constant-tail values first, then score `C3` in that setting. That is real work
and it is a prerequisite before the Rule 90 filter can be applied to this route
at all. Until then, **the Rule 90 filter is untested on C3**, which is a weaker
and more accurate statement than either branch.

## 3. What this does and does not change

Unchanged: the reduction `C3 ==> (1)` (`RESULTS-ZERO-PREFIX-GREEDY-REDUCTION.md`)
and `C3`'s exhaustive survival to length 20 on Rule 30. Nothing here bears on
those.

Changed: `C14` is off the list of live targets, and the Rule 90 filter is a
known open prerequisite for route (2) rather than a passed check. Anyone
claiming a `C3` proof still owes that filter, because a proof that never uses
the OR would need to explain why it fails for Rule 90 — and right now nobody
knows whether it does.

## 4. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/zero_prefix_greedy_invariant_probe.py \
  --max-length 14      # C14 line in the candidate table

PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/rule90_control_on_c3.py \
  --max-length 14 --calibrate-length 12
```

The control takes about 100s at length 14 with calibration to 12; it is
`O(n^3)` per word before the `Fib(n+2)` word count, so length 16 is roughly a
further factor of 8.

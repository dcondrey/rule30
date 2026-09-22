# Reducing the zero-prefix greedy lemma to a per-row sensitivity-depth claim

Date: 2026-09-06. Script: `zero_prefix_greedy_invariant_probe.py`.

Status: **THE GREEDY LEMMA IS STILL NOT PROVED. What changed is the target: the
load-bearing gap is now a strictly weaker, per-row statement (`C3` below) that
implies `(1)` exactly, with no greedy frontier, no matching, and no induction
across rows. `C3` holds on all 44,205 legal rows of every hard-core word through
length 20. Five other candidate strengthenings were killed, so they need not be
retried.**

Evidence level: `R` for the reduction (`C3 ==> (1)` is a two-line argument,
given below and independent of any measurement); `K` for the candidate
census that selected it.

## 1. Pre-registration

Recorded in the script docstring, in three passes, and only the first was
recorded before any run. `C1`-`C6` were pre-registered cold. `C7`-`C9` were
added after the first pass killed `C1`, `C2`, `C5`, `C6`; `C12`-`C13` after the
second pass showed `C3` surviving under the corrected legal-row filter. Each
pass fixed its candidates and kill conditions before running, but the later
passes were chosen in light of earlier results, so they are exploratory. That is
the right label for the whole exercise: the probe selects a proof target, it
certifies nothing, and `C3`'s survival is not a confirmatory test result.

Each candidate would imply the lemma or a usable part of it; kill
condition per candidate is a single violating word/tail/row, printed with the
word, tail, row, `S_j` and the frontier. All are tested against the frozen,
already-validated sensitivity sets

```text
S_j := zero_prefix_bitsliced_graph(word, tail)[0][j]
```

from the unmodified `constant_tail_zero_prefix_bitsliced.py`. No graph is
redefined, since a new graph would be a new unverified claim rather than a test
of the existing one. `S_j` is exactly the edge set of eq. (5): the code also ORs
in differences of the forced value, but `forced_value_bits` is a function of the
affine alone, so those add nothing.

A row is **legal** exactly where the lemma claims something: for tail 2 every
hard-core row `0 <= j < s_2`, for tail 3 only the nonfinal rows `j + 1 < s_3`.
The first run of this probe got that filter wrong, counted tail 3's exempt final
row, and reported `C3` as killed by two witnesses (`W=121` and `W=221`, tail 3,
row 3) that the lemma never claimed. Both are allowed misses.

## 2. The reduction

> **Sensitivity-depth claim (`C3`).** For every nonempty hard-core `W` of length
> `n`, tail `c in {2,3}`, and every legal row `j`: `max S_j >= j`. That is, row
> `j` is sensitive to some source token of index at least `j`.

**`C3` implies (1).** Tokens are indices `0..n-1`, so `max S_j <= n-1` for every
row. For tail 2 every row `0 <= j <= s_2 - 1` is legal, so `s_2 - 1 <= n - 1`,
i.e. `s_2 <= n`. For tail 3 the legal rows are `0 <= j <= s_3 - 2`, so
`s_3 - 2 <= n - 1`, i.e. `s_3 <= n + 1`. Both are exactly the conjecture `(1)`
of `RESULTS-SCALE-TELESCOPING.md`, with no slack given away. QED

**The greedy lemma implies `C3`.** If the greedy set is nonempty at every legal
row then `g_j` exists and is strictly increasing from `g_0 >= 0`, so `g_j >= j`,
and `max S_j >= g_j >= j`. So `C3` is a weakening, and proving it is enough:
`(1)` is what the separator needs, not the frontier construction that certified
it finitely.

What the weakening drops is the entire cross-row bookkeeping. The greedy lemma
is a statement about a sequence of rows, each conditioned on the token the
previous row consumed; `C3` is a statement about one row in isolation.

### 2.1 The form to attack

`max S_j >= j` says the sequence `k -> A_(j,k)` is non-constant on `k in [j, n]`,
which since `k = n` is in that range is the same as

```text
there is some k >= j with A_(j,k) != A_(j,n).                      (C3')
```

Scenario `k` is exactly the forced trace of the length-`n` word `0^k W[k:]`
(`bitsliced_trace_states` prepends a further `n` zeros, identically for every
scenario), and scenario `n` is the all-zero word. Checked directly against the
independent `forced_trace` for every word to length 10, both tails, all `n+1`
scenarios: 7,078 matches, 0 mismatches. So `(C3')` reads:

> Among the suffixes of `W` of length at most `n - j`, at least one changes the
> row-`j` newest-cut affine away from its all-zero value.

That is the statement to prove, and it makes the failure of `C12` legible:
`C12` is `(C3')` with the choice of `k` forced to `k = j`, i.e. it demands that
the *longest* admissible suffix already move row `j`. The freedom to pick any
shorter suffix is exactly what the data says is needed.

## 3. Candidate census, exhaustive over hard-core words to length 20

46,365 words, both tails, 44,205 legal rows.

| # | Candidate | Verdict |
|---|---|---|
| `C1` | `n-1 in S_j` (row always sees the last token) | **KILLED**, 13,566 failures; first at `W=1212`, tail 2, row 0, `S_j={0,1}` |
| `C2` | `max S_j` nondecreasing in `j` | **KILLED**, 1,153 failures |
| `C3` | `max S_j >= j` | SURVIVES, 0 failures in 44,205 rows |
| `C4` | `S_j` nonempty | SURVIVES, 0 failures (implied by `C3`) |
| `C5` | `min S_j` nondecreasing in `j` | **KILLED**, 1,520 failures |
| `C6` | greedy frontier `= min S_j` | **KILLED**, 15,752 failures |
| `C7` | `S_j` is a contiguous interval | **KILLED**, 37,562 failures; first at `W=121`, tail 3, row 0, `S_j={0,2}` |
| `C8` | `max S_j > g_(j-1)` (the lemma itself) | SURVIVES, 0 failures |
| `C9` | `max S_j >= n-1` whenever `g_(j-1) >= n-2` | SURVIVES, but only 7 rows in the corpus reach that regime |
| `C12` | `A_(j,j) != A_(j,n)` | **KILLED**, 6,475 failures |
| `C13` | `A_(j,k) = A_(j,n)` for every `k > j` | **KILLED**, 44,203 failures |

`C12` is the one worth naming as dead. It would have given `C3` immediately and
had the most natural proof story behind it — a propagation argument in which
zeroing the prefix up to `j` leaves a perturbation that has reached the
newest-cut affine by row `j`. It is false: the perturbation can arrive and
cancel, so `A_(j,j)` and `A_(j,n)` can agree while some intermediate scenario
`k` in `(j, n)` differs. Any proof of `C3` has to keep the intermediate
scenarios, exactly as sec. 6 of `RESULTS-SCALE-TELESCOPING.md` warned for the
pointwise derivative. `C13` fails almost everywhere and only rules out the
sharpest possible form.

`C9` is reported with its own weakness: the dangerous regime it describes, the
frontier pressed to within one token of the end, occurs in 7 rows out of 44,205,
so its survival is close to vacuous and is not evidence for anything.

## 4. How tight `C3` is

`max S_j - j` over the 44,205 legal rows ranges from 0 to 18, and the minimum is
attained on exactly two rows in the whole corpus:

```text
W=121  tail=3  row=2  S_j={0,1,2}  greedy=2
W=221  tail=3  row=2  S_j={0,1,2}  greedy=2
```

Both are `n=3`, tail 3, with `s_3 = 4 = n + 1`: the two words that attain the
bound `(1)`. Everywhere else `C3` has slack, so the claim is only ever tight
where the conjecture it implies is tight, which is what a correct reduction
should look like.

No tail-2 row in the corpus is tight, and that is equivalent to `s_2 < n`
throughout: `s_2 = n` would force the last legal row `j = n-1` to have
`max S_j = n-1 = j`. Measured directly over every hard-core word to length 18:
`max(s_2 - n) = -1` and `max(s_3 - n) = +1`, the latter attained at `W=121`. So
tail 2's bound is never met and tail 3's is, matching the sharp tail-2 words of
`RESULTS-SCALE-TELESCOPING.md` sec. 4 (`s=10` at `n=17`, `s=12` at `n=21`).

For comparison the greedy lemma's own margin `max S_j - g_(j-1)` bottoms out at
1 on 7 rows. `C3` is the weaker claim but not by much where it counts.

## 5. What this does not do

It does not prove `(1)`, and it does not weaken the case that `(1)` is hard.
`C3` is a real reduction of the *statement*, not progress on the *algebra*: the
same recursion, the same affine coordinates, and the same absence of
monotonicity that blocked the earlier certificates are all still in the way.
The three exclusions in sec. 6 of `RESULTS-SCALE-TELESCOPING.md` (all 16 local
`2x2` patterns occur; comparing only the first remaining scenario to the
all-zero one fails; a fixed bounded frontier jump is false) apply to `C3`
unchanged, and `C12`'s death above adds a fourth.

Large random words are not a useful test corpus here, and the first version of
this probe wasted a run finding that out: at `n = 100..400` the hard-core
continuation dies after one or two rows, so 90 random words contributed 215
legal rows in total and never approached the bound. The binding instances are
the structured words with long survival, which is why the exhaustive sweep and
the three known sharp words are the corpus that matters.

## 6. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/zero_prefix_greedy_invariant_probe.py \
  --max-length 20
```

About 155s at length 20; cost grows like `Fib(n+2)` times a per-word `O(n^2)`,
so length 22 is roughly a further factor of 3. `--random-lengths` and
`--random-trials` add the (uninformative, see sec. 5) large-`n` sampling.

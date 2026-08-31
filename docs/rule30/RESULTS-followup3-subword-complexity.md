# Followup-3: subword (factor) complexity / Morse-Hedlund — killed, and not new

**Verdict: KILLED by obstruction H, independently confirmed. The candidate is
also not absent from this program's register in substance** — it already
exists, computed and killed, as A4 / row 76 in
`experiments/overnight-arms/novel_frameworks/TRIAGE-novel-frameworks.md` and
`triage_probe.py`. It is genuinely absent only from `PATH.md` itself, because
row 76 was proposed for merge there and never merged (`TRIAGE-novel-frameworks.md`
line ~242: "proposed here for its owner to merge rather than written in").

## 1. The theorem, stated precisely

**Morse-Hedlund (1938).** For an infinite word `w` over a finite alphabet,
with factor complexity `p(n) := #{distinct length-n contiguous factors of w}`:

> `w` is **eventually periodic** (there exist a preperiod `r >= 0` and period
> `q >= 1` with `w[i] = w[i+q]` for all `i >= r`) **iff** `p` is bounded **iff**
> there exists some `n` with `p(n) <= n`.

Equivalently, the non-periodicity direction used here: `w` is not eventually
periodic iff `p(n) >= n+1` for *every* `n`.

Two precisions worth pinning down since they matter for the reduction below:

- "Eventually periodic" here already subsumes "purely periodic" (preperiod
  `r=0`) as a special case; Morse-Hedlund does not distinguish them, and P1
  in this program's usage is "not eventually periodic", so no gap opens here.
- The bound is not just qualitative: if `w` has eventual period `q` and
  preperiod `r`, then `p(n) <= r + q` for **every** `n` (the factor language
  stabilizes once you're `r` symbols past the seam and cycling through `q`
  phases). This constant bound is what makes the logical reduction in §3
  exact rather than approximate.

This is standard combinatorics-on-words; the statement matches Morse & Hedlund,
*Symbolic dynamics II: Sturmian trajectories*, Amer. J. Math. 62 (1940), and is
restated identically (up to notation) in Allouche-Shallit, *Automatic
Sequences*, Theorem 10.2.6. The triage agent's statement of it was correct.

## 2. Independent computational confirmation

New script: `experiments/overnight-arms/roundtable_followup3/subword_complexity/subword_complexity.py`.
Written from scratch (not copied from `triage_probe.py`'s `a4_complexity`), to
serve as an independent check rather than a re-run of the same code.

- Ground truth: `experiments/overnight-arms/common/rule30.py:center_column_bits`
  (itself pinned against `experiments/rule30/center_column.py`).
- Independent cross-check: a from-scratch O(n^2) naive 2D grid simulator
  (`independent_naive_center_column`), agreeing bit-for-bit with the
  ground-truth generator on the first 4,000 bits.
- Factor complexity `p(n)` computed on a 200,000-bit prefix for `n = 1..24`.

Result: `p(n) > n` holds with **no exception** for every computed `n`, and the
values match the earlier `triage_probe.py` run exactly where they overlap
(`p(8)=256`, `p(16)=62377` in both). Full table in
`experiments/overnight-arms/roundtable_followup3/subword_complexity/result.json`.

A second, purely computational observation, distinct from the logical
obstruction in §3: the fraction of available length-`n` windows that are
distinct (`p(n) / (N-n+1)`) crosses 90% by `n=20` and 99% by `n=24` on this
`N=200000`-bit prefix — i.e. `p(n)` stops measuring the word's combinatorial
complexity and starts measuring prefix length once `n` approaches
`~log2(N)` (`log2(200000) ~ 17.6`). This is the same `O(log N)` wall recorded
five times over in `PATH.md` obstruction A, appearing here as a sixth
representation: even the *honest, non-vacuous* range of `n` this method can
say anything meaningful about is capped at `O(log N)`, well short of the
range `n <= 64` that was actually reported.

## 3. The obstruction-H reduction, derived precisely

Claim: no finite computation, at any word-length `N`, can certify
`p(n) > n` for all `n`; it can certify this only for `n` up to a bound
depending on `N`.

**Derivation.** Fix a computed prefix of length `N`. For any `n`, the number
of length-`n` windows available in that prefix is `N - n + 1`, so `p(n)` can
only be computed (exactly, from this prefix) for `n <= N`, and computing it
requires `n <= N` trivially just to have a window. That already bounds the
*checkable range* by `N`. But the sharper and more important point is
independent of window-counting:

Suppose, for contradiction-style reasoning, the computation confirms
`p(n) > n` for all `n <= n_max` (whatever `n_max <= N` was actually reached).
This is consistent with `w` being eventually periodic with period
`q > n_max` (and any preperiod): such a `w` has `p(n) <= r+q` for all `n`,
which is `> n` for every `n < r+q`, hence in particular for every
`n <= n_max` whenever `n_max < r+q`. So the observation "`p(n)>n` for
`n<=n_max`" is **logically compatible** with `w` being eventually periodic —
it merely excludes periods (`r+q`) at most around `n_max`. Since P1 requires

> **CORRECTION (superseded by `RESULTS-subword-complexity-extended.md`).**
> The clause "it merely excludes periods (`r+q`) at most around `n_max`" is
> **wrong, and understates this route by roughly three orders of magnitude.**
> The bound `p(n) <= r+q` holds for *every* `n`, so a single measured
> `p(n_0) = V` already forces `r+q >= V` — the exclusion tracks the largest
> measured *complexity value*, not the largest `n` reached. The correct
> exclusion is `max_n p_hat(n) = N - L` (`L` = longest repeated factor,
> empirically `~2 log_2 N`), i.e. **linear in prefix length `N`**. The
> 200,000-bit run described below therefore already excluded
> `r+q <= 199,966`, not `r+q <= 64`. Everything after this point in §2-§3
> that reasons from `n_max` as the exclusion bound inherits the same error.
> The conclusion (KILLED under obstruction H) is unaffected: a finite prefix
> still leaves all sufficiently large `r+q` open.

Since P1 requires
`p(n) > n` for **every** `n` with no exception, and a finite computation only
ever reaches finitely many `n`, no finite computation can certify the
universal statement; it can only ever rule out periods below whatever bound
it reached. This is exactly obstruction H ("finite data cannot establish an
infinite statement") in the specific vocabulary of factor complexity, and the
mechanism is the same one already given the exchange rate in
`overnight/RESULTS-automaticity.md` Theorem O for the kernel-rank statistic:
a finite check buys a lower bound on "excluded period length," not a proof of
the unbounded statement.

**Where this lands relative to what's already been checked.** The prize
announcement's own direct check of the center column already covers ~`10^9`
bits and so already excludes periods (and preperiods) up to that scale by
direct inspection — several orders of magnitude beyond `n_max=64` (or even
`n_max=24` as computed independently here, capped further by the `O(log N)`
saturation wall in §2). So this route, even run at its full stated scope, is
not just logically unable to close P1 — it is **strictly weaker**, as an
empirical exclusion, than a check this program's own register already

> **CORRECTION (superseded by `RESULTS-subword-complexity-extended.md`).**
> "Strictly weaker" is also wrong. A repeated factor of length `L` at offset
> `q` **is** a period-`q` agreement running `L` positions, so the subword
> route executed optimally *is* the direct periodicity scan restated in
> different notation — the same statement, not a weaker cousin. The
> comparison to the prize announcement's `~10^9`-bit check stands only as a
> difference in prefix length reached, not in method strength.

Continuing the (superseded) original argument, this route was taken to be
weaker than a check this program's own register already
credits as insufficient (obstruction H's own closing line: "the prize
announcement's own `10^9`-bit check cannot exclude 'a trillion-step
transient'"). The subword-complexity framing reproduces a strictly smaller
version of a bound already known to be inadequate.

**Verdict on the kill condition:** the triage's kill condition was reasoned
correctly, both directions checked (I did not find a flaw in the
equivalence, and separately confirmed the theorem statement is standard and
exact). Confirmed independently: KILLED, no leverage over existing checks.

## 4. Register-presence check

```
grep -ni "subword\|factor complexity\|morse.hedlund" docs/rule30/PATH.md
  -> no matches (confirmed genuinely absent from PATH.md itself)

grep -rni "subword\|factor complexity\|morse.hedlund" docs/rule30/
  -> no matches anywhere under docs/rule30/

grep -rni "subword\|factor complexity\|morse.hedlund" . --include=*.md --include=*.py
  -> experiments/overnight-arms/frontier_attack/a22_row46_specific_uniformity/specific_uniformity.md:73
       (passing mention, "subword complexity, etc — see §3", not a worked route)
  -> experiments/overnight-arms/novel_frameworks/triage_probe.py:17-18, 212-240
       (A4: full working implementation, `a4_complexity`)
  -> experiments/overnight-arms/novel_frameworks/TRIAGE-novel-frameworks.md:207-235
       (A4 writeup: "CLOSED. Vacuous as specified.")
  -> experiments/overnight-arms/novel_frameworks/TRIAGE-novel-frameworks.md:250
       (row 76 in the "Proposed rows for the PATH.md section 7 register" table,
        status KILLED, same reasoning, same numbers, explicitly citing
        obstruction H)
```

**Conclusion on absence:** the triage agent's claim is correct in the narrow
sense it was stated (*"this framing does not currently appear anywhere in
this program's register (PATH.md)"* — true, `PATH.md` itself has zero hits)
but is not the full picture, and reads as more novel than it is: the same
theorem, the same equivalence, the same computation (matching numbers:
`p(8)=256`, `p(16)=62377` reproduced exactly here), and the same verdict
(vacuous, killed by obstruction H) already exist in this program's working
files, complete with a proposed `PATH.md` row (76) that its author never
merged. This is a re-discovery of existing, already-triaged work, not new
territory — worth naming for the record (per the task's instruction) but not
worth crediting as a fresh find.

## 5. Recommendation

Nothing to add computationally; the existing A4/row-76 analysis already
covers this candidate correctly and this followup only independently
reproduces and confirms it. If `PATH.md` section 7 is next revised, row 76
(and its siblings 73-75) are sitting unmerged in
`TRIAGE-novel-frameworks.md` and should be folded in by whoever owns that
file, so future triage passes stop re-finding the same closed route.

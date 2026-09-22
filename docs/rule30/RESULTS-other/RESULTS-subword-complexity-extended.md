# Subword complexity, extended: a stronger measurement, and a correction to row 76

**Status: strengthened measurement. P1 remains open, and nothing here can close
it — obstruction H applies to this document exactly as it applies to row 76.**

Two things are reported. The second matters more than the first.

1. The row-76 measurement is extended from a 200,000-bit prefix to a
   **8,388,608-bit** prefix, computed with a verified bit-packed generator,
   raising the excluded-period bound to `r + q <= 8,388,564`. That bound is
   still ~119x SHORT of the ~10⁹ exclusion already public via the prize
   announcement; this extension does not advance the state of the art, and
   the number is not the point (see item 2 and §7).

   **The `p(n) > n` table is not the content, and should not be read as a
   check that could have failed.** At `N = 8,388,608`, `p̂(n) = 2ⁿ` for small
   `n` and `≈ N - n + 1` above saturation, so `p̂(n) > n` for `n <= 64` is
   satisfied by six to seven orders of magnitude at every `n`. It is reported
   because row 76 reported it, and it is now trivially true. The content of
   the extension is the exclusion bound `N - L - 1`.
2. **Row 76 reads its own data far too weakly**, claiming an exclusion of ~64
   where the same 200,000-bit run already excluded ~2×10⁵ — a factor of ~3,100
   left unclaimed. `RESULTS-followup3-subword-complexity.md` §3 then builds on
   that weak reading to conclude the route is "strictly weaker" than direct
   inspection; that conclusion is **false**, and in fact the two are the *same
   scan in different notation* (§2.2, verified by brute force). This correction
   is worth more than the extra bits.

---

## 1. What was actually measured before

Row 76 (`PATH.md` §7.1) and `RESULTS-followup3-subword-complexity.md` record:
`p(n) > n` verified for all `n <= 64` on a 200,000-bit prefix, prefix-saturated
from `n ~ 32` on, and conclude:

> "confirming `p(n) > n` up to any finite `n_max` excludes only periods below
> roughly `n_max`"

and, in §3 of the followup:

> "this route ... is **strictly weaker**, as an empirical exclusion, than a
> check this program's own register already credits as insufficient".

The first sentence is **correct but leaves the bound on the table**; the second
is **false**, and false precisely because it inherited the first's weak reading.

The distinction matters. Read as a statement about Morse-Hedlund *used as a
criterion*, sentence 1 is right: if `r+q = Q` then `p(n) <= n` first fires
around `n = Q`, so the `p(n) > n` witness as such only reaches `~n_max`. The
fault is not falsity. It is that the **quantitative** form of the same theorem
— `p(n) <= r+q` for every `n`, already stated correctly in the followup's §1 —
extracts roughly 3,100× more exclusion from the *identical data*. Sentence 2
then converts that unclaimed slack into a wrong comparative verdict.

## 2. The correction: the bound is `max_n p(n)`, not `n_max`

Morse-Hedlund's quantitative form — already stated correctly in
`RESULTS-followup3-subword-complexity.md` §1, then not used in §3 — is:

> if `w` is eventually periodic with preperiod `r` and period `q`, then
> `p(n) <= r + q` for **every** `n`.

`p(n) <= r+q` for every `n` is a statement about every `n` *individually*. So a
**single** measured value already bites:

> **Observing `p(n₀) = V` for any one `n₀` forces `r + q >= V`.**

The measured `p̂(n)` on a finite prefix is a lower bound on the infinite word's
`p(n)` (every factor counted genuinely occurs), so the inequality is safe in
the direction we need. The exclusion the measurement buys is therefore

> **`r + q >= max_n p̂(n)`**, not `r + q >~ n_max`.

Applied to the *existing* row-76 data, unchanged and re-measured here:

| prefix `N` | `max_n p̂(n)` | attained at `n` | row 76's claimed exclusion | actual exclusion |
|---|---|---|---|---|
| 200,000 | **199,967** | 34 | `r+q <= 64` | `r+q <= 199,966` |

Row 76's own numbers already excluded `r+q <= 199,966`. The
register credits them with excluding ~64. That is a factor of ~3,100 given
away for free.

### 2.1 Why: `max_n p̂(n) = N - L`, exactly

Let `L` be the **longest repeated factor** of the `N`-bit prefix. The identity
is not merely empirical; it has a two-line proof.

**Lemma.** `max_n p̂(n) = N - L`, attained at `n = L + 1`.

*Proof.* Distinct length-`n` factors are in bijection with the start positions
at which a factor **first** occurs, and there are `N - n + 1` start positions
in total.

Fix `i < j` with `w[i..i+L-1] = w[j..j+L-1]` (such a pair exists by definition
of `L`); note `j <= N - L` since the length-`L` factor at `j` fits inside the
prefix.

- **`n <= L`.** For each `k ∈ [0, L-n]` the length-`n` factor starting at
  `j + k` equals the one starting at `i + k`, and `i + k < j + k`, so `j + k`
  is *not* a first occurrence. (These are legal start positions:
  `j + k <= (N-L) + (L-n) = N - n`.) That is `L - n + 1` distinct positions
  disqualified, so
  `p̂(n) <= (N - n + 1) - (L - n + 1) = N - L`.
- **`n > L`.** No length-`n` factor repeats, so `p̂(n) = N - n + 1 <= N - L`,
  with equality exactly at `n = L + 1`. ∎

The ties observed at `n = L - 1, L` are the equality cases of the first bullet:
they occur when the length-`L` repeat is the only repeated structure at those
lengths, so the bound `N - L` is already met below `L + 1`.

Measured, exactly, at every prefix length tested (§4) — confirming the lemma
rather than standing in for it: the **value**
`max_n p̂(n) = N - L` holds with no exception. The *location* is `n = L+1`
generically but can sit a little lower when `p̂` is flat across the top: `p̂`
ties across `n = L-1, L, L+1` at several lengths (e.g. `N = 4×10⁶`, where
`p̂(42) = p̂(43) = p̂(44) = N - 43` and the first maximum is reported at
`n = 42`). The tie does not disturb the value, which is the quantity the bound
depends on.

Since the excluded set is `r + q < max_n p̂(n)`, the exclusion is
**`r + q <= N - L - 1`**.

Since `L` is empirically `~2 log₂ N` (§4), the exclusion bound is
`N - O(log N)` — i.e. **linear in the prefix length**, essentially `N` itself.

**Corollary (exact asymptotic form of P1).** Write `L(N)` for the longest
repeated factor of the `N`-bit prefix. The center column is not eventually
periodic if and only if `N - L(N) -> ∞`.

*Proof.* If the column is eventually periodic with preperiod `r` and period
`q`, then for `N >= r + q` the blocks starting at `r` and `r + q` agree for
`N - r - q` positions, so `L(N) >= N - r - q` and `N - L(N) <= r + q` for
all large `N`. Conversely, suppose `N - L(N) <= C` for infinitely many `N`.
For each such `N` pick `i < j` with `w[i..i+L-1] = w[j..j+L-1]` and
`L >= N - C`; then `j <= N - L <= C`, so `(i, j)` ranges over finitely many
pairs and some fixed pair occurs for infinitely many `N`. For that pair the
agreement length `L >= N - C` is unbounded, so `w[k] = w[k + (j - i)]` for
every `k >= i`. ∎

So `L(N) = o(N)`, and a fortiori the birthday-scale `L(N) ~ 2 log₂ N`
observed in §4, are strictly stronger sufficient targets; the exact target is
the weakest one. In this notation obstruction H reads: a deterministic bound
`L(N) <= N - f(N)` with `f -> ∞`, derived from the rule and the seed, is P1
itself rather than an approach to it, and no finite prefix supplies `f`.

### 2.2 Consequence: the route *is* the direct periodicity scan, in other notation

Not merely comparable — identical. A repeated factor
`w[i..i+L-1] = w[j..j+L-1]` with `q = j - i` is exactly a period-`q` agreement
`w[k] = w[k+q]` running `L` consecutive positions, and conversely. So

> `L` = the longest repeated factor = `max_{q>=1}` (longest run of consecutive
> `k` with `w[k] = w[k+q]`).

**Verified by brute force** (`equiv_check.c`, `O(N²)` over all offsets `q`) at
four prefix lengths, exact agreement with the sort-derived value of `L` in
every case — including, at `N = 200,000`, the exact prefix row 76 used:

| `N` | longest period-agreement run | offset `q` attaining it | `L` from `analyze.c` |
|---|---|---|---|
| 10,000 | 25 | 1,372 | 25 |
| 20,000 | 29 | 16,664 | 29 |
| 50,000 | 29 | 16,664 | 29 |
| **200,000** (row 76's prefix) | **33** | 1,324 | **33** |

The offsets `q` attaining the maximum are unremarkable mid-range values, not
near-`N` artifacts, so the equivalence is being exercised, not trivially
satisfied at the boundary.

The consequence is immediate. An `N`-bit prefix is consistent with eventual
period `(r, q)` iff the agreement `w[k] = w[k+q]` holds throughout
`k ∈ [r, N-q-1]` — a run of length `N - r - q` — which requires
`N - r - q <= L`, i.e. `r + q >= N - L`. That is the *same* bound the factor
count gives, derived from the direct scan.

So `RESULTS-followup3-subword-complexity.md` §3's "strictly weaker" verdict
should read: **the subword route, executed optimally, is the direct
periodicity scan restated.** Not weaker, not stronger, not merely
"comparable" — the same statement.

The practical consequence is the opposite of what §3 implied: the route's
ceiling is exactly the prize's own ceiling. Matching the announcement's `10⁹`
requires `10⁹` bits — no shortcut, but also no penalty.

### 2.3 What is genuinely capped at `O(log N)` — and what isn't

The followup's §2 saturation observation is correct but was applied to the
wrong quantity. Two different things scale differently, and conflating them is
what produced the error:

- The range of `n` over which `p(n)` is **informative** (not merely counting
  windows) is capped at `n ~ 2 log₂ N`. That is obstruction A, and it is real.
  At `N = 8,388,608` this range ends around `n = 43`.
- The **exclusion bound** `max_n p̂(n) = N - L` grows **linearly** in `N`. It is
  not capped by the saturation wall; saturation is precisely the regime that
  produces the bound.

Saturation is not the failure of the statistic. It *is* the statistic.

## 3. Correctness verification

No extension is worth anything if the generator is subtly wrong. Four
independent generator gates, all bit-exact, all passing
(`experiments/rule30-subword-extended/verify.py`):

| # | reference | scope | result |
|---|---|---|---|
| 1 | OEIS **A051023** b-file (Karttunen/Zumkeller), offset 0 | 100,001 bits | PASS |
| 2 | this repo's `overnight-arms/common/rule30.py:center_column_bits` | 100,001 bits | PASS |
| 3 | from-scratch naive `O(n²)` 2-D grid simulator (no frame trick, no bit packing) | 5,000 bits | PASS |
| 4 | **Wolfram's own** "A Million Bits of the Center Column of the Rule 30 Cellular Automaton", Wolfram Data Repository 2017, doi:10.24097/wolfram.25316.data, CSV export | **1,000,000 bits** | **PASS** |

Gate 4 is the strongest available for the **generator**: bit-exact agreement
with the prize-setter's own published artifact, at 10⁶ bits.

A fifth gate covers the **analyzer**, which gates 1-4 do not touch. This
repo's `ARM9-factor-complexity.md` (uncommitted at the time of writing)
computes `p(k)` through a completely independent pipeline — a numpy
bit-packed kernel reused from `a3_p2_orbit_closure/band_census.py`, with its
own distinct-factor counter. At `n = 10⁶`:

| `k` | this document (`analyze.c`, C radix sort) | ARM9 (numpy pipeline) | |
|---|---|---|---|
| 8 | 256 | 256 | PASS |
| 12 | 4,096 | 4,096 | PASS |
| 16 | 65,536 | 65,536 | PASS |
| 20 | **644,259** | **644,259** | PASS |

`p(20)` agreeing to all six digits across two independently written
implementations is the meaningful one; the saturated values below it could
agree by construction.

Additionally, the 200,000-bit prefix from the row-76 run is reproduced exactly,
and the analysis tool reproduces row 76's published numbers exactly —
`p(8) = 256`, `p(16) = 62377`, `p(24) = 198743` — before being used on anything
new. The four generator variants (scalar in-place, double-buffered,
NEON, NEON+unroll) were also checked bit-identical against each other at
3,000,000 bits.

## 4. Results

Generator: `gen30v4.c`, single-threaded, bit-packed 64 cells/word, in-place
descending NEON update on the shifted frame
`b_{t+1} = (b_t << 2) XOR ((b_t << 1) | b_t)`, center bit `c(t) = ` bit `t` of
`b_t`. Analysis: `analyze.c`, one LSD radix sort of all 64-bit windows, which
yields exact `p(n)` for all `n <= 64` simultaneously plus `L`.

| prefix `N` (bits) | `L` | `2 log₂ N` | `max_n p̂(n)` | `= N - L` | excluded `r+q <=` | all `p(n) > n`, `n<=64` | `L` capped at 64? |
|---|---|---|---|---|---|---|---|
| 10,000 | 25 | 26.6 | 9,975 | yes | **9,974** | yes | no |
| 100,000 | 33 | 33.2 | 99,967 | yes | **99,966** | yes | no |
| 200,000 | 33 | 35.2 | 199,967 | yes | **199,966** | yes | no |
| 1,000,000 | 36 | 39.9 | 999,964 | yes | **999,963** | yes | no |
| 2,000,000 | 40 | 41.9 | 1,999,960 | yes | **1,999,959** | yes | no |
| 4,000,000 | 43 | 43.9 | 3,999,957 | yes | **3,999,956** | yes | no |
| 8,388,608 | 43 | 46.0 | 8,388,565 | yes | **8,388,564** | yes | no |

`p(n) > n` holds with **no exception** for every `n` in `1..64` at every prefix
length above, extending row 76's `n <= 64` check from `N = 2×10⁵` to
`N = 8,388,608`.

`L` tracks `2 log₂ N` to within a few bits, drifting slightly below it (36 vs
39.9 at `N = 10⁶`), which is the behaviour expected for a word with no
long-range repetition structure. This is consistent with — and no
stronger than — the normality-flavoured heuristics already recorded in the
register; it is a sanity check on the data, not a finding.

### New excluded-period bound

> **The center column of Rule 30 is not eventually periodic with preperiod `r`
> and period `q` satisfying `r + q <= 8,388,564`.**

(`8,388,564 = N - L - 1`; the value `r+q = N - L` itself is *not* excluded.)

Previous register value implied by row 76 as written: ~64.
Correct value extractable from the *existing* row-76 data
(`N = 200,000`, `L = 33`): `r + q <= 199,966`.
Value after this extension: **`r + q <= 8,388,564`**.

### Why the run stopped where it did

The generator was launched targeting `10⁸` and **stopped deliberately at
`t = 10⁷`**, with `8,388,608` bits flushed to disk (the writer flushes in 1 MiB
= 8,388,608-bit blocks, so that is the largest fully written prefix).

The reason is in the measured curve, not in any failure. The local scaling
exponent kept climbing as the row outgrew cache — 2.32 over
`3×10⁶ → 6×10⁶`, 2.40 over `6×10⁶ → 8×10⁶`, **2.67 over
`9×10⁶ → 10⁷`** — so the next flush boundary (`1.68×10⁷` bits) was a further
~70 minutes away for a **2×** gain on a bound whose linearity in `N` is
already established analytically (§2.1) rather than empirically. The run was
stopped rather than left occupying a core for the 1.5–4 days that `10⁸` would
have taken.

To extend, regenerate from scratch — **there is no restore path**; checkpoints
are dumped and well-formed but no code reads them back:

```
cc -O3 -o gen30v4 gen30v4.c
./gen30v4 <steps> out.bin 1000000 gen30.ckpt
./harvest.sh out.bin results
```

## 5. Cost curve, measured

Generation is `Θ(N²)` cell updates and inherently sequential in time: step
`n+1` depends on step `n`, so there is no parallelism across time. Bit packing
divides the constant by 64 and is the only large win available.

Measured single-core throughput, **in cache**: ~1.9×10⁹ 64-bit word
updates/sec (~1.2×10¹¹ cell updates/sec). This figure does **not** hold at the
harvest size — see the exponent-2.4 finding below. Full data in
`experiments/rule30-subword-extended/benchmarks.json`.

| N | wall clock | source |
|---|---|---|
| 10⁵ | 0.07 s | measured |
| 10⁶ | 9.4 s | measured |
| 3×10⁶ | 79.6 s | measured |
| 6×10⁶ | 399 s | measured |
| 8×10⁶ | 795 s | measured |
| 1.7×10⁷ | ~80 min | measured/projected |
| 2.5×10⁷ | ~3.5 h | projected |
| 10⁸ | **~1.5 to 4 days** | projected |
| 10⁹ | **~145 days** | projected |

The measured local exponent in the 3×10⁶–8×10⁶ range is **2.3–2.4**, not 2.0:
the row is outgrowing cache, so the constant degrades on top of the `Θ(N²)`
work. The exponent should relax back toward 2.0 once the row is fully out of
cache and the run is purely bandwidth-bound, which is why the 10⁸ figure is
given as a range rather than a point. **An earlier draft of this document
projected 26 h for 10⁸ by extrapolating the in-cache constant; that was wrong
by 1.5–4×, and the cache transition is the reason.** Projections beyond
measured data are labelled as such throughout.

Vectorization was worth almost nothing, which is itself worth recording:

- double-buffering instead of in-place update: **2.3× slower** at `N=10⁶` (the
  extra write stream costs more than the removed loop-carried dependence buys);
- plain NEON: a wash (77.3 s vs 75.4 s scalar at `N=3×10⁶`);
- NEON + 4× unroll: **1.17×**, the entire vectorization payoff.

The kernel is load/store-port bound, not width bound. There is no factor of 2
sitting unclaimed in the inner loop.

### The analysis half is free

Counting `p(n)` for all `n <= 64` on the finished prefix is one `O(N)` radix
sort — seconds, and embarrassingly parallel if it ever needed to be. The
asymmetry is total: **generation is ~99.99% of the cost and is the part that
cannot be parallelized across time; analysis is the part that parallelizes
trivially and costs nothing.** Any effort spent parallelizing the analysis is
misdirected.

## 6. Is 10⁹ feasible?

**Not on this machine. Yes in the cloud, for a few hundred dollars and a
nontrivial distributed implementation. And it is not worth doing.**

**Locally: no.** Single-core projection is ~145 days. Multicore does not
rescue it: at `N = 10⁹` the row is 250 MB, far outside any cache, and the total
memory traffic is `N²/4 = 2.5×10¹⁷` bytes. At ~120 GB/s of unified memory
bandwidth that is a **~24-day floor** even with all 10 cores used perfectly.
The bound is bandwidth, not cores.

**In the cloud: yes, with real engineering.** Spatial decomposition across
workers is possible, and the naive objection (halo exchange every single step
dominates) is defeated by the standard ghost-zone trick: send a `k`-bit halo
and advance `k` steps before the next exchange, since the domain of dependence
shrinks by one cell per side per step. Communication amortizes to negligible.
The work is `1.56×10¹⁶` word-ops ≈ 2,280 core-hours at measured throughput,
realistically 5,000–10,000 core-hours after bandwidth and parallel losses —
**roughly $150–$500** at commodity spot pricing. So Modal or equivalent *would*
work here, contrary to the usual expectation for time-sequential problems, and
the reason is specifically that ghost-zone batching converts a per-step
communication into a per-`k`-step one.

**But it should not be done, for three reasons.**

1. **It has already been done.** A billion-bit center column was contributed
   to the Wolfram Data Repository by Xiangdong Wen (2019), with Wolfram
   Research as Publisher of Record; the prize announcement points at it but
   does not itself name who performed the computation. Recomputing it buys
   nothing.
2. **The result is already credited as insufficient.** Obstruction H's own
   closing line in the register is that the 10⁹-bit check "cannot exclude a
   trillion-step transient." Spending $500 to reproduce a bound the register
   already calls inadequate is spending money to move from "insufficient" to
   "the same insufficient."
3. **The bound is linear in `N`, and `P1` needs infinity.** Every doubling of
   spend doubles the excluded `r+q`. There is no `N` at which the curve turns.

Note on the data: the 10⁹-bit resource is **not** anonymously downloadable —
the Wolfram Data Repository entry exposes no direct file and the resource API
redirects to a login; it requires a Wolfram ID and a Wolfram Language client.
The 10⁶-bit resource *is* directly downloadable (used as gate 4 above). So even
the cheap path of "download rather than compute" is closed at 10⁹ without a
Wolfram account.

## 7. What this does and does not establish

**Does:** the center column of Rule 30 has no eventual periodicity with
`r + q <= 8,388,564`, verified on an independently generated prefix whose first
10⁶ bits agree bit-for-bit with Wolfram's published data.

**This bound is not the state of the art, and is not claimed to be.** The prize
announcement states plainly that "the sequence doesn't become periodic in the
first billion steps," an exclusion of `~10⁹` — **~119× larger** than the one
reached here. Row 76 already recorded that this route "falls well short of the
prize announcement's own `10⁹`-bit exclusion," and after this extension it
still does, by two orders of magnitude. The extra bits do not advance the
frontier on the bound.

What is new is not the number. It is §2 (the register was reading its own data
~3,100× too weakly), §2.1 (the lemma `max_n p̂(n) = N - L`, proved rather than
observed), and §2.2 (the subword route and the direct periodicity scan are the
same statement). **Those three apply unchanged to the `10⁹` figure**: Wolfram's
own billion-bit direct check and a subword-complexity reading of the same data
are not two independent exclusions, they are one exclusion in two notations.
That is the part of this document that survives being 119× short.

**Does not — obstruction H, in its sharpest form:**

- It says **nothing** about `r + q > 8,388,564`. In particular it does not
  exclude **period 2 with a preperiod of 10¹²**. The bound constrains the
  *sum* `r + q`, so a tiny period hiding behind a long transient is untouched.
- It is not, and cannot be, progress toward P1. P1 requires `p(n) > n` for
  **every** `n`; a finite computation reaches finitely many `n`. No prefix
  length changes this. The `Θ(N²)` cost means each additional decade of
  exclusion costs 100× the previous one, so the finite computation is not even
  cheap on its own terms.
- It does not beat, or attempt to beat, the `Θ(N²)` generation barrier.
  Finding a sub-quadratic algorithm for the center column is itself Wolfram's
  **third prize problem**; no search for one was made here.

The honest summary: this is a bigger number of the same kind, plus one real
correction to how the register reads the numbers it already had.

## 7a. Relation to `ARM9-factor-complexity.md`

`docs/rule30/ARM9-factor-complexity.md` (present but uncommitted in the working
tree) is a separate, concurrent arm on the same statistic. It is **not**
superseded by this document and does not supersede it — the two ask different
questions of `p(n)`:

| | ARM9 | this document |
|---|---|---|
| question | is `p(k)` *bounded* (Cobham / automaticity)? | how large is `max_n p(n)` (periodicity exclusion)? |
| regime of interest | small `k`, `n → ∞`, watching for a **plateau** | the **saturated** regime, `n` near `L` |
| verdict | route has no near-term computational path: informative `k` needs `n ~ 10¹⁰-10¹³` | route is the direct periodicity scan restated; bound linear in `N` |

Both conclude the route is closed, for different reasons, and neither changes
any row status. ARM9's independent `p(k)` values are used above as gate 5.

One point of ARM9's is worth carrying over verbatim, because it constrains §6
of this document: the `Θ(N²)` wall is the *same* wall as Prize Problem 3, so a
better constant (ARM9's numpy kernel, or this document's NEON kernel) closes a
factor of tens-to-hundreds, never the polynomial-degree gap.

## 8. Recommended change to `PATH.md` row 76

**Not applied here — `PATH.md` is left untouched for its owner to edit.**

Row 76's status (**KILLED**, obstruction H) is correct and should not change.
Two passages in its body should be replaced:

- Replace: *"so confirming `p(n) > n` up to any finite `n_max` excludes only
  periods below roughly `n_max`"*
  with: *"a single measured `p(n₀) = V` forces `r + q >= V`, so the exclusion
  is `max_n p̂(n) = N - L` (`L` = longest repeated factor, empirically
  `~2 log₂ N`) — linear in prefix length, not bounded by `n_max`. The original
  200,000-bit run therefore already excluded `r + q <= 199,966`, not
  `r + q <= 64`."*
- Replace the claim inherited from `RESULTS-followup3-subword-complexity.md`
  §3 that the route is *strictly weaker* than direct inspection with: *the
  subword route executed optimally **is** the direct periodicity scan in
  different notation — a repeated factor of length `L` at offset `q` is
  precisely a period-`q` agreement running `L` positions — so the two are the
  same statement, not merely comparable.*
- Extend the measurement record to: *"`p(n) > n` for all `n <= 64` verified on
  a 8,388,608-bit prefix; excluded `r+q <= 8,388,564`; generator bit-exact
  against OEIS A051023 (10⁵ bits) and Wolfram's own published million-bit
  center column (10⁶ bits)."*
- Add artifact reference: `RESULTS-subword-complexity-extended.md`;
  `experiments/rule30-subword-extended/`.

The same two corrections apply to `RESULTS-followup3-subword-complexity.md`
§2 and §3, which are the source of the error.

## 9. Artifacts

```
experiments/rule30-subword-extended/
  gen30.c        scalar in-place generator (reference implementation)
  gen30v2.c      double-buffered variant (slower; kept as negative result)
  gen30v3.c      NEON variant (a wash; kept as negative result)
  gen30v4.c      NEON + 4x unroll -- used for the long run
  analyze.c      exact p(n) for n=1..64 + longest repeated factor L
  verify.py      the four correctness gates
  equiv_check.c  brute-force check that L == longest period-agreement run (§2.2)
  harvest.sh     runs analyze over a ladder of prefix lengths
  benchmarks.json  measured throughput and the cost model
  results/       p(n) tables per prefix length (7 files, n=1..64 each)
  rule30_center_8388608.bin
                 the generated prefix itself, 1 MiB, packed LSB-first
                 (bit t of the stream is c(t)); regenerate with
                 ./gen30v4 8388608 out.bin
```

Nothing under `docs/rule30/PATH.md` was modified. The recommended row-76 edit
is in §8 for its owner to apply or reject.

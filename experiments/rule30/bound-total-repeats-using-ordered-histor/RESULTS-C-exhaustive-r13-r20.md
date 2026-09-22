# A repeat budget at every length: the node is (C), and (C) survives an exhaustive search through r=20

Date: 2026-09-19. Ladder statement: "A repeat budget at every length" (P1, `budget`).
Pre-registration: `PREREG-C-exhaustive-r13-r17.md` (committed before any engine
existed; amended to r<=20 after r<=14 ran and before r>=15 ran). Sibling to
`RESULTS-bound-total-repeats-using-ordered-histor.md`, another session's r<=10
census, which is not edited here.

## STATUS

**Open. No ladder statement changed.** Nothing is refuted. The cumulative
inequality (C), which already implies the target, has no violation on any tape
of any legal start of initial length r<=20 (733,007,751,850 starts in all, every
prefix of every tape). That is a finite certificate and says nothing past r=20.
No closed finite object or potential proving a budget at every length was found.

## 0. Witness bank

`query_witness_bank.py` on the target statement returned 0 hits at the default
threshold. At threshold 3 the nearest relevant kill is
`r30-cap18-sharp-n25-witness`, a capacity-18 family with N=25 and D=14 (N above
the capacity-17 maximum of 24, D equal to its 14); the capacity-18 open seams
reach N=35, D=22 (`r30-cap18-open-seam-lifetime-witnesses`). Both are
padded words of length above 10^6, respected below.

## 1. The node is already reduced to (C) (restated, not new)

- At a fixed r there are `2^(2r-1)` legal starts, and after r successful updates
  every surviving class is synchronized: `C_r(alpha beta)` is empty or equal to
  `C_r(alpha)` when `|alpha|>=r` (`RESULTS-weighted-history-endpoints.md`). So a
  finite B(r) exists iff every start of length r is mortal; with the proved
  `r+N+1 <= 2^(D+1)(r+2)` (`RESULTS-repeat-budget-lower-bound.md`) the budget and
  mortality statements at fixed r are the same finite fact. This is the
  `budget -> mortality` ledger edge, already kernel-checked in its abstract shape
  (`experiments/rule30/Rule30P1Reduction.lean`).
- The cumulative inequality `|C_r(alpha)| * 2^D(alpha) <= 2^(2r-1)` (C) implies
  `D <= 2r-1` on every surviving tape, hence the target, with
  `N <= 4^r(r+2)-r-1` (`RESULTS-aperiodic-mortality-audit.md` section 1, where
  the implication is proved and (C) is not). Any constants `c, eps>0` with
  `|C_r(alpha)| <= c 2^(2r-1-eps D)` also suffice; `c=1, eps=3/2` is refuted by the
  r=24 tape `00011100001111111100` (same report's weighted-history follow-up), and
  the `3^D` form by `|C_14(00001111)|=196488`.

So "a closed finite certificate charging repeats for every source" is a proof of
(C) or of a positive-rate variant at unbounded tape length. Before this run (C)
was covered on: every start with r<=12 (single implementation), every r with
tape length <=9 (`RESULTS-cumulative-history-transfer.md`), every r and tape with
D<=6 (`RESULTS-history-transfer-mixing.md`). The uncovered region was tape
length >=10 and D>=7 at r>=13.

## 2. Fatal-mechanism tests for the (C) route

- **Counting injection fails to cover: FIRES edge by edge.** Section 4 measures
  zero-cost edges of both kinds (repeat and alternating) at every r>=5 and runs
  of up to 9 consecutive zero-cost edges (r=20). No per-edge charge exists; any
  proof of (C) must be cumulative over the whole history. This is consistent with
  the recorded plateaus (`C_6(101)=...=C_6(1011100)`, eight free repeats at r=24).
- **Sharp positive constant: does not fire.** (C) is a counting bound with
  explicit constant, not a rate certificate from a named message family.
- **Explicit periodic/automatic family: fired on stronger normalizations, not on
  (C).** `c=1, eps=3/2` and `3^D` are dead (section 1); no family is known against
  the one-bit form.
- **Bounded-complexity exclusion only / claim generalised from one instance:**
  the result below is a finite range and is labelled as such.

## 3. Exhaustive census r=1..20 (computed, exhaustive over the stated class)

`tape_census.c` evolves every legal start with the update of
`panel/cert33.py` `direct_step`, 64 starts per machine word, until it dies,
and records the full successful tape of every start; `analyze_tapes.py` forms
`|C_r(alpha)|` for every prefix of every tape. A lifetime past 63 updates would
abort; none occurred.

Controls, all passing (`logs/analyze_tapes.log`):

| control | result |
|---|---|
| tape histogram equals a replay of every start through the frozen oracle `panel/cert33.py`, r<=7 | equal at every r |
| `C_3(0)=C_3(00)`; `C_6(101)=C_6(1011)=C_6(10111)` | 8, 8; 36, 36, 36 |
| recorded maxima `W(10), W(11), W(12)` | 131072, 525312, 2097152 |
| detector fires on a known false inequality (`3^D` form, `|C_14(00001111)|`) | 196488, violation reported |
| B(1..10) of the other session's census | 0,0,1,1,2,3,4,3,6,7 recomputed |

Results. `W` is the maximum of `|C_r(alpha)| 2^D(alpha)` over nonempty tapes;
the margin is `(2r-1) - log2(|C_r(alpha)| 2^D(alpha))` minimised over tapes with
D>=7, the region not previously covered.

| r | starts | distinct tapes | B(r) | N_max(r) | (C) violations | D>=r | margin, D>=7 (bits) | tape at that margin |
|---:|---:|---:|---:|---:|---:|---:|---:|:--|
| 13 | 33,554,432 | 147 | 7 | 14 | 0 | 0 | 4.99 | `000001111` |
| 14 | 134,217,728 | 190 | 7 | 13 | 0 | 0 | 5.73 | `111110000` |
| 15 | 536,870,912 | 265 | 7 | 12 | 0 | 0 | 9.85 | `01111000011` |
| 16 | 2,147,483,648 | 350 | 10 | 14 | 0 | 0 | 5.75 | `11001111111100` |
| 17 | 8,589,934,592 | 455 | 9 | 16 | 0 | 0 | 5.82 | `1001111111100` |
| 18 | 34,359,738,368 | 594 | 9 | 15 | 0 | 0 | 6.34 | `1111011001111` |
| 19 | 137,438,953,472 | 825 | 8 | 14 | 0 | 0 | 5.43 | `110111110000` |
| 20 | 549,755,813,888 | 1,076 | 11 | 19 | 0 | 0 | 6.27 | `10111110000` |

The previously uncovered region (r>=13, tape length >=10, D>=7) contains
228 distinct tape prefixes in this census: 4, 1, 2, 12, 21, 45, 59, 84 at
r=13..20. That, not the start count, is the size of what is new here.

B(r) for r=1..20: 0,0,1,1,2,3,4,3,6,7,6,7,7,7,7,10,9,9,8,11. The longest-lived
start at r=20 has tape `1001001101100010101` (N=19); the most repeats, D=11,
tape `1110110000001111`.

**Proved (exhaustive certificate, with controls):** for every r<=20, every legal
start and every prefix alpha of its tape, `|C_r(alpha)| 2^D(alpha) <= 2^(2r-1)`,
and every start has `D <= r-1`. Consequently every legal start of length
r<=20 is mortal with the B(r) and N_max(r) above. Finite range only.

**Pre-registered hypotheses.** H_C (primary): not killed. H_sharp (`D<=r-1`):
not killed. H_slack (the D>=7 margin does not shrink with r): not killed,
`m(20)=6.27` against `m(13)=4.99`; the margin is between 4.99 and 9.85 bits
on r=13..20 with no trend.

## 4. Where the margin goes, and why this range cannot stress (C) (computed; exploratory, not pre-registered)

`edge_costs.py` (`logs/edge_costs.log`) prices each edge of each tape as
`log2(|C_r(alpha)|/|C_r(alpha s)|)`:

- The cheapest repeat edge costs 0 bits at every r>=3, the cheapest
  alternating edge at every r>=5; zero-cost repeats per tape reach 5 and
  consecutive zero-cost runs reach 9 (r=20). Section 2's injection test is
  this measurement.
- For r=13..20 the smallest margin over all tapes with D>=1 is at the first
  repeat, `00` or `11`, between 2.92 and 2.99 bits (at r=9 the minimum is
  1.80 bits at `0100101111100`, so this does not hold at every r): at
  r=13..20 `|C_r(00)|` is about `2^(2r-5)`, the `4^(-n)` mixing limit at n=2.

**Synchronization.** A tape prefix longer than r lies past the r-th update,
where the class is frozen and every later repeat is free. Such prefixes occur
only at small r: 1, 2, 1, 3, 1, 6, 4, 2, 1 of them at r = 1, 5, 6, 7, 8, 9, 10,
11, 13 (at most N_max(r)-r = 4 updates past synchronization, at r=9), and none at r=12 or
14..20, where `N_max(r) < r`. So (C) was tested in the post-synchronization
regime only at small r, where it held; for r=14..20 no start reaches it. Every
known long-lived history (N=24 to 35, D=14 to 22) sits on padded words of length
above 10^6, where the mixing limit `|C_r(alpha)|/2^(2r-1) -> 4^(-N)` puts the
margin near `2N-D`, tens of bits (inferred from that limit, not computed here).
An exhaustive search in r therefore does not reach a large class followed by
many free repeats at moderate r, the configuration in which (C) could fail;
pushing it to r=21, 22 (about 1 and 4 hours on this machine) would add another
confirmation of the same kind and is not recommended.

## 5. What is refuted, what is open

- **Refuted:** nothing. No hypothesis's kill fired.
- **Open:** (C) for tapes longer than 9 with D>=7 at r>=21; any positive-rate
  variant at unbounded tape length; hence a budget at every length, all
  auxiliary frontiers die, and period two by this route.
- **Not found:** a closed finite potential or guarded quotient that charges
  repeats for every source. Section 4 shows why edge-local charging cannot work,
  and the closed per-capacity products stop closing at capacity 18
  (`../closed-finite-object-lifting-a-check-to-/`, 2,000,000-state cap at depths
  12 to 16). The live requirement is a cumulative bound that survives
  synchronization: after update r, the class size is frozen, so (C) needs every
  class at time r to carry at least as many banked bits as its remaining
  lifetime's repeats. That is the precise shape of the missing statement.

## 6. Reproduce

From this directory:

```bash
cc -O3 -march=native -o tape_census tape_census.c -lpthread
for r in $(seq 1 20); do ./tape_census $r 10 > data/tapes_r$r.txt 2> data/tapes_r$r.err; done
uv run --no-project python analyze_tapes.py 20 > logs/analyze_tapes.log   # controls, (C), B(r), margins; writes c-census.json
uv run --no-project python edge_costs.py 20 > logs/edge_costs.log         # section 4; writes edge-costs.json
```

Wall clock with 10 threads: r=18 62 s, r=19 204 s, r=20 837 s; r<=17 under 12 s
together. `*.log` and `*.err` are globally ignored; commit them with `git add -f`.

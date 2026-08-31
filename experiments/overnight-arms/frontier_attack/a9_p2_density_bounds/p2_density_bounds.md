# A9 — weaker-than-1/2 quantitative bounds on the lone-seed centre column

**NEGATIVE. No new unconditional bound. The missing lemma is: `D(T)` is bounded,
where `D(T)` is the depth to which the left half of `F^T(delta_0)` agrees with the
left half forced by the constant trace. It is implied by (not equivalent to) closing
row 47's explicitly-open orbit-closure repair — showing the checkerboard is not in the
lone seed's orbit closure. Two things are nevertheless proved and verified here: an
exact run/row identity (Identity R) that strictly implies row 47's Theorem A, and a
narrow no-go showing the row-25/26 horizon law is exactly light-cone-tight so no
restriction argument built on it can beat `gap <= 2 ceil(T/2) + 1`.**

Kill condition that fired: **the log bound was already in the register.** Row 47's
Theorem A (`docs/rule30/overnight/RESULTS-p2-single-seed.md:17-20`) already states
`N_1(T) >= floor(log2(T+4)) - 1` and `N_0(T) >= floor(log2(T+6)) - 2`, with the
equivalent run bounds; both halves re-checked here with zero violations for `T <= 3000`
(Gate 3c). The objective's stated targets — `liminf > 0`, `limsup < 1`,
or an explicit gap bound — are respectively unreachable by this mechanism, unreachable
by this mechanism, and already held.

Every number below is **EXACT COMPUTATION** and is validation of the implementation
and of two already-published tables. Under obstruction H
(`docs/rule30/PATH.md:793`), none of it is evidence for an infinite statement, and no
measured quantity is used as a premise for any claim labelled PROVED.

---

## Step 0 (mandatory read) — does row 25's mechanism give a quantitative gap bound?

**Yes, and it is linear in `t`, not sublinear. The density arm therefore dies at
step 0.**

The chain, with citations:

1. `RESULTS-zero-tail.md:160-165` gives the sharp radius law: for a nonzero row of
   support radius `w` with centre zero, the maximum `H` with `c(t) = 0` for every
   `0 <= t <= H` is `2 ceil(w/2)`, with `2^w - 1` extremal rows. Table at
   `RESULTS-zero-tail.md:181-192`.
2. `RESULTS-eventual-period.md:117-120` gives the all-one counterpart: for radius `w`
   the sharp inclusive all-one horizon is `w+1` for even `w` and `w` for odd `w`, with
   `2^w` extremizers.
3. The lone-seed row `r_T = F^T(delta_0)` has support radius exactly `T` (both extreme
   neighbourhoods `001` and `100` push the endpoints outward one cell per step —
   `RESULTS-eventual-period.md:38-41`; `RESULTS-zero-tail.md:202-206`).
4. Substituting `w = T` gives a zero-run bound `<= 2 ceil(T/2) + 1` and a one-run
   bound of the same order — **linear in `T`**.

A gap bound `g(T)` yields `t_(k+1) <= t_k + g(t_k)`. With `g` linear this gives
`t_k <= C 2^k`, hence only `N_1(T) >= log2(T) - O(1)`. Positive `liminf` density would
need `g = O(1)`; any `g(T) = O(T^alpha)` with `alpha < 1` would give
`N_1(T) >= c T^(1-alpha)`. So the sub-question posed in the brief — is `w` along the
lone-seed orbit controlled well enough — has the answer **no, `w` is exactly `T`, the
worst possible value**, and the resulting bound is exactly row 47's Theorem A. That
theorem is not re-derived as new; it is re-checked (`identity_output.txt`, Gate 3c,
zero violations for `T <= 3000`).

---

## Narrow no-go: the horizon law is exactly light-cone-tight

The obvious repair is to apply the horizon law not to `r_T` (radius `T`) but to a
restriction of `r_T` to a small window. **This fails by exactly one step, for every
window radius, and provably so.**

Let `rho = r_T` restricted to `[-w, w]` and zero outside. A cell at `|x| = w+1`
first influences the centre at time `w+1`, so `Tr_0(rho)(t) = c(T+t)` is guaranteed
only for `0 <= t <= w`. To contradict the horizon law one needs the trace of `rho` to
be constant on `0 <= t <= 2 ceil(w/2) + 1`. But

```
2 ceil(w/2) + 1  >  w      for every w >= 0,
```

so the guaranteed agreement window `[0, w]` is always strictly shorter than the window
the law needs. The same arithmetic holds for the all-one horizon (`w+1` for even `w`,
`w` for odd `w`, so `horizon + 1 > w` in both parities). Restriction therefore yields
no contradiction at any radius, and `w = T` is forced.

**Scope, stated narrowly on purpose.** This says: *no argument that applies the row-25
or row-26 horizon law to a restriction of `r_T` to a finite window beats
`gap <= 2 ceil(T/2) + 1`.* It does **not** say that no argument beats `log T`. The
broader form of that claim was raised and **withdrawn** in row 47 after its verifier
called it a non-sequitur (`RESULTS-p2-single-seed.md:38-44`); the step from "no bound
derivable from this premise beats `L <= 2 ceil(T/2)+1`" to "no argument beats
`N_1(T) >= log2 T - O(1)`" does not follow. Nothing here repeats it.

---

## PROVED — Identity R: the centre run length is a static property of one row

Let `y` be a nonzero finite Rule 30 row, `c(t) = F^t(y)_0`, `v = c(0)`, and
`R_j = y(+j)`. Define the **forced left half** `P_k`, `k >= 1`:

- `v = 0`: the prefix-OR transducer, `RESULTS-zero-tail.md:52-55`,
  `P_(2k+1) = OR(R_1..R_(2k+1))`, `P_(2k) = R_(2k) AND NOT OR(R_1..R_(2k-1))`;
- `v = 1`: `P_k = 1` iff `k` is even (`RESULTS-eventual-period.md:102-115`).

Define `D(y) = min{ k >= 1 : y(-k) != P_k }`. This is finite: if the right half is
nonzero (and always when `v = 1`), `P` has ones at every sufficiently deep position of
one parity while `y` is finitely supported; in the remaining case (`v = 0` with an
all-zero right half) the transducer gives `P_k = 0` for every `k`, and `D(y)` is finite
because `y` is nonzero and its support therefore lies on the left. Then

```
        run(y) := #{ leading t with c(t) = v }   =   D(y).
```

**Proof.**
*(necessity, `run <= D`)* Suppose `c(t) = v` for `0 <= t <= H`. Triangular uniqueness
(`RESULTS-zero-tail.md:62-79`) — two left halves first differing at depth `n` give
traces first differing at time `n`, by left permutivity along the extreme path — shows
that the constraints `c(0..H) = v` together with the full right half determine
`y(-1)..y(-H)` uniquely. The `C_m` member (`RESULTS-zero-tail.md:81-126`) for `v = 0`,
and the checkerboard-left configuration (`RESULTS-eventual-period.md:102-115`) for
`v = 1`, have the same right half and constant trace `v` forever, so they satisfy those
constraints; their left halves are exactly `P`. Hence `y(-k) = P_k` for `k <= H`, i.e.
`H < D(y)`, i.e. `run(y) <= D(y)`.

*(sufficiency, `run >= D`)* Let `H = D(y) - 1`. Then `y` agrees with the corresponding
constant-trace configuration on all of `[-H, +infinity)`. The centre value at time
`t <= H` depends only on cells in `[-t, t] subset [-H, H]`. So `c(t) = v` for
`0 <= t <= H`, i.e. `run(y) >= D(y)`. QED

**Why this is not a tautology.** It converts a question about the *future* of the orbit
into a question about a *single row read statically*: how deep the left half of `r_T`
matches an explicit pattern. It also strictly implies row 47's Theorem A — take
`w = T`, note the pattern has a one at the least odd `k > T` (resp. least even `k > T`)
while `y(-k) = 0` there, so `D <= 2 ceil(T/2) + 1` — and it is sharp where Theorem A is
lossy, since `D(T)` is typically single-digit while the Theorem A bound is `~T`.

### Verification (`run_identity.py`, output in `identity_output.txt`)

`D` is computed **from the row only** (never touching the future column) and `run`
**from the column only**; the two are then compared.

- **Gate 1.** Exhaustive over every nonzero row of radius `w <= 8` — 174,752 rows.
  Identity holds on all of them. Independently reproduces *both* published tables from
  direct simulation: zero-trace `H_max = 2 ceil(w/2)` with `2^w - 1` extremal rows
  (`RESULTS-zero-tail.md:181-192`) and all-one horizon `w+1`/`w` by parity with `2^w`
  extremizers (`RESULTS-eventual-period.md:117-120`). This is the indexing gate: row 47
  lost an implementation to a shrinking-row-read-as-fixed-width bug
  (`RESULTS-p2-single-seed.md:64-66`).
- **Gate 2.** 4,000 random finite rows of radius 1..14 — the disconfirming population,
  since the identity is claimed for *every* finite row, not just the seed. No violation.
- **Gate 3.** Lone seed, `T = 1..3000`. Row extraction cross-checked cell-by-cell
  against the independent naive simulator `simulate_seed` for `t < 300`. No violation.
- **Gate 5.** Exhaustive over all 32,766 right words of length `<= 14`.

## PROVED corollary — the right cone is inert for this criterion

Gate 5 checks exhaustively what the transducer makes immediate: writing `m` for the
least `j >= 1` with `R_j = 1`, the forced zero-trace left half is

```
P_k = 0  (k < m),   P_m = 1,   P_k = k mod 2  (k > m),
```

a function of **`m` alone**. No `R_j` with `j > m` enters. Consequently every structure
theorem about the right cone — Rowland 2006 Lemma 2's purely periodic power-of-two
diagonals, and row 47's obstruction 2 (`RESULTS-p2-single-seed.md:113-122`) — is
provably inert for the run-length question. That is a new angle on why the abundant
exact-density results in the right cone never reach the centre.

Note also that `P_m = 1` and `P_(m+1) = (m+1) mod 2`, so for **even** `m` the forced
pattern carries two adjacent ones at `m, m+1` and is *not* alternating there. The
tempting summary "the two forced patterns are the two phases of the checkerboard" is
false for `m >= 2`, and `m >= 2` is common: over the centre-zero times `T <= 3000` the
observed distribution is `m=1: 750, m=2: 386, m=3: 202, m=4: 91, m=5: 46, m=6: 21,
m=7: 13, m=8: 5, m=9: 1, m=10: 1, m=11: 1`. Any argument must use the transducer
verbatim.

---

## Where this sits relative to obstruction E

`PATH.md:750-763`. Identity R is evaluated on the actual rows `F^T(delta_0)`; it names
no measure, no ensemble, and no generic point, and its proof uses only triangular
uniqueness plus the light cone. It is a single-orbit statement and does not cross the
measure-zero gap in either direction — which is also why it yields no density: it
converts one hard single-orbit question into another (`D(T)` bounded), rather than
importing an almost-everywhere fact.

## The missing lemma, and the one-way implication to row 47's open repair

The only route from Identity R to `liminf > 0` is:

> **MISSING LEMMA.** `sup_T D(T) < infinity`.

By Identity R this is *literally equivalent* to "the lone-seed centre column has bounded
runs". Bounded runs is logically independent of density 1/2 in both directions — a
sequence with `log`-growing runs can have density exactly 1/2, which is the shape of the
register's own `2^20` data — so `D` bounded is not a weakened P2 but a *different*, and
apparently false, statement. Two consequences worth recording:

1. **The gap-bound method class cannot deliver positive density unless runs are
   bounded.** `liminf > 0` from a gap bound requires `g = O(1)`; by Identity R that is
   `D` bounded. The register's own EXACT COMPUTATION points the other way: row 47
   observed longest 0-run 19 and longest 1-run 22 over `2^20` steps
   (`RESULTS-p2-single-seed.md:29`), which tracks `log2(2^20) = 20`, the i.i.d.
   longest-run scale. Measurement, not proof (obstruction H) — but it means the method
   class is being asked to prove something that looks false.
2. **The implication to the orbit-closure repair runs one way only.** `D` unbounded
   gives arbitrarily long blocks of `r_T` agreeing with an eventually-alternating
   pattern anchored just left of centre, which by row 47's own stated criterion
   ("[the checkerboard] is in the closure iff arbitrarily long alternating blocks occur
   in the diagram", `RESULTS-p2-single-seed.md:100-106`) puts the checkerboard in the
   lone seed's orbit closure. So *closing that repair implies `D` is bounded*; the
   converse is not claimed, and the `m`-offset above means the alternating block is
   anchored, not free. Row 47 records the repair as **OPEN**
   (`RESULTS-p2-single-seed.md:92-106`), and `PATH.md:762-763` records the same.

No conditional result is asserted as a theorem anywhere in this document.

---

## Rule 90 control

Run as Gate 4.

- **Gate 4a.** Rule 90's lone-seed centre column is `1` at `t = 0` and `0` for every
  `1 <= t < 4096` (direct simulation; also Kummer, since `C(2s,s)` is even for all
  `s >= 1`). Density 0. Any argument producing a positive lower density must fail here.
- **Gate 4b.** It fails here for a structural reason, not by accident. Rule 90 has a
  nonzero finite row with identically zero centre trace, `{-1, +1}`
  (`RESULTS-zero-tail.md:274-289`, verified through `t = 256`). So Rule 90's zero-trace
  fibre is not a singleton, **no left half is forced**, and `D` is simply *undefined*
  for Rule 90. Identity R has no Rule 90 analogue and cannot leak a positive-density
  conclusion to it. The load-bearing Rule-30 fact remains
  `centre = 0 and R_1 = 1  =>  R'_1 = 1`, which for Rule 90 reads `R'_1 = R_2`.

The narrow no-go section is likewise Rule-30-specific: it is arithmetic about a horizon
law that Rule 90 does not have.

---

## What a reader must not over-read

- **No new bound.** The only quantitative bound in play is row 47's Theorem A. It is
  re-derived here as a corollary of Identity R and re-checked numerically; it is not new.
- **Identity R is not progress on P2.** It is a change of variables. It makes the
  obstruction sharper and cheaper to check; it does not remove it.
- **The no-go is narrow.** It covers restriction arguments built on the row-25/26
  horizon law. It is *not* the withdrawn row-47 claim that no argument beats `log T`.
- **`max D(T) = 12` for `T <= 3000` is EXACT COMPUTATION**, reported as a sanity scale
  only. It is not evidence that `D` is bounded, and the register's `2^20` data suggests
  the opposite growth.
- **`D` bounded is not a weaker target than P2.** By Identity R it is equivalent to
  bounded centre runs, which neither implies nor is implied by density 1/2, and which
  the register's `2^20` run data suggests is false.
- Nothing here touches nonconstant eventual periods (P1) or the exact value 1/2.

## Reproduction

```bash
cd experiments/overnight-arms/frontier_attack/a9_p2_density_bounds
PYTHONDONTWRITEBYTECODE=1 uv run python run_identity.py   # writes identity_output.txt
```

Exit status 0 iff all five gates pass. Local CPU only; Modal $0; paid model calls $0.

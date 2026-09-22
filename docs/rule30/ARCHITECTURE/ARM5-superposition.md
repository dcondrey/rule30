# Arm 5 phase 0: linear superposition and sparse error integration

Measurement report for steps 1 and 2 of the build order. The probe is
`experiments/rule30/probe/` (own `[workspace]`, matching the `wasm/` precedent).
Companions: `ARM4-frequency-domain.md` (the phase-0 probe it extends),
`SEARCH-ARCH-AIR.md` (the arm-4 grammar this brief replaces),
`PREREGISTRATION.md` (the target).

Steps 3 and 4 are not built and nothing here licenses them. **Read §0 first.**

---

## 0. Two corrections before the numbers

### 0.1 The projector is O(log n), not O(1)

Lucas' theorem gives `C(n,k) mod 2 = [k AND ~n == 0]` for the *binomial*
`(1+z)^n`. That is Rule 90, not Rule 150. Rule 150 is the *trinomial*
`(1+z+z^2)^n`, and Lucas does not apply to it.

What does apply: over GF(2), `(1+z+z^2)^(2^m) = 1 + z^(2^m) + z^(2^(m+1))`, so

```
(1+z+z^2)^d = PROD over set bits m of d of (1 + z^(2^m) + z^(2^(m+1)))
```

The coefficient of `z^k` counts assignments `c_m in {0,1,2}` with
`sum c_m 2^m = k`, mod 2. A carry DP over the bits of `k` computes that with
carry confined to `{0,1}`: `trinom_mod2` in `probe/src/main.rs`.

Cost is `O(bits(n))` carry steps, 14 at n = 10,000. Measured **35.7 ns/call**.
O(1) holds only under a fixed word width, which is the same accounting under
which Theta(n^2) forward simulation is Theta(n^2) word operations. The brief's
step 4 fuel gradient must charge the projector `log n`, not `1`.

### 0.2 Superposition here is a re-encoding, not a complexity reduction

The identity is real and is verified below:

```
s_n(0) = [A^n delta_0](0)  XOR  sum over t<n, x of  E(x,t) * [A^(n-1-t) delta_x](0)
```

with `A = z + 1 + z^-1`. But `E(x,t) = s_t(x) AND s_t(x+1)` is a function of the
Rule 30 state. The right-hand side does not compute the state cheaply; it
*presupposes* it. Nothing has been removed from the Theta(n^2) budget, only
moved.

That is the same shape as the arm-3 peephole error (a rewrite that preserves the
complexity class) and the arm-4 transform error (a basis change that preserves
the degree). The brief's "Problem 3 reduces entirely to determining the parity of
error projections" is true, and is exactly as hard as Problem 3. The open
question is unchanged: is there structure in `E` that collapses that parity sum?
§3 is the first measurement bearing on it, and it is negative.

---

## 1. Conventions, pinned

`center_column.py` convention: `new = (row<<1) ^ (row | (row>>1))`, bit `p` holds
cell `p`, position increasing rightward. Left neighbour of `p` is `p-1`, right is
`p+1`.

```
f30(l,c,r) = l ^ (c | r) = l ^ c ^ r ^ (c & r) = f150(l,c,r) ^ E
E(x,t)     = s_t(x) AND s_t(x+1)
```

`E(x,t)` is computed from row `t` and enters row `t+1` as a delta at position
`x`, so it is carried by `A^(n-1-t)`, not `A^(n-t)`. Since `A` is a symmetric
Laurent polynomial,

```
[A^d delta_x](0) = coeff of z^(|x|+d) in (1+z+z^2)^d
projects_to_center(x, t, n) = trinom_mod2(n-1-t, |x| + (n-1-t))
```

`x` is signed and relative to the initial single 1 at `x = 0`.

## 2. Verification

Three checks, independent sources, all passing at `max_n = 10000`:

1. `trinom_mod2` (carry DP) against a full bitset expansion of `(1+z+z^2)^d`,
   every coefficient: 156,692 coefficients over 314 values of `d` up to 9,999,
   including `2^m - 1`, `2^m`, `2^m + 1` for m up to 12. Plus support overrun
   (`k = 2d+1` must be 0).
2. `rule150_center(n) = trinom_mod2(n,n)` against a *direct* Rule 150
   bit-parallel simulation, every `n` in 0..4096.
3. The superposition identity itself, `s_n(0)` from the Rule 30 simulation
   against `rule150_center(n) XOR parity(projections)`, for **every** `n` in
   1..=512 and 202 banded `n` (the 1000/2000/4000 +64 challenge bands, powers of
   two +/- 1, and 10,000).

Check 3 exhaustive over a contiguous range is the one that matters: the four
plausible off-by-ones (`n-t` vs `n-1-t`, delta at `p` vs `p+1`, signed `x` vs
`|x|`, absolute vs seed-relative `x`) all produce a signature of passing at some
`n` and failing at `n+1`.

## 3. Measured geometry of E(x,t), n = 10,000

25,010,461 error events over 100,000,000 light-cone cells.

- Global density **0.250105**. Bulk (`t >= 5000`) density **0.250052**.
  This is the near-independence prediction and carries no information; it is
  reported only to rule out a surprise.

Structure is entirely in the edge diagonals. Density at depth `d` in from each
edge, over all `t`:

| d | from left edge | from right edge | from center |
|---|---|---|---|
| 0 | 0.9999 | 0.0000 | 0.1267 |
| 1 | 0.0001 | 0.5001 | 0.2493 |
| 2 | 0.0000 | 0.5001 | 0.2485 |
| 3 | 0.5001 | 0.2501 | 0.2490 |
| 4 | 0.5001 | 0.2501 | 0.2513 |
| 5 | 0.5002 | 0.2501 | 0.2502 |
| 6 | 0.0000 | 0.1876 | 0.2492 |
| 7 | 0.0000 | 0.2503 | 0.2516 |
| 8 | 0.5001 | 0.3439 | 0.2506 |
| 10 | 0.0001 | 0.2504 | 0.2501 |
| 17 | 0.0005 | 0.2502 | 0.2495 |
| 19 | 0.0006 | 0.2736 | 0.2493 |
| 23 | 0.0006 | 0.2346 | 0.2508 |

The **left** edge is the ordered one, agreeing with `ARM4` §0.1. Its diagonals
take only the values ~1, ~0.5, ~0.25 and ~0 out past depth 23: deterministic
periodic domain walls, not a density. The **right** edge is within noise of 0.25
by depth 3 and never leaves it. The center-relative histogram is flat at 0.25 at
every depth except `d = 0`, where it is 0.1267. That is the center column's own
error rate, and it is a restatement of the ~0.5 one-density of A051023
(`E = s(0) AND s(1)`, with the two near-independent).

There is no interior cluster structure to bound. The boundaries are one-sided and
confined to the ordered left wall, whose information content grows as its depth,
which is the objection `ARM4` §0.1 already recorded against exploiting an
ordered wall.

Raw `(t,x)` coordinates for `t < 1024` are dumped to
`experiments/rule30/errors-le1024.csv` (261,648 events).

## 4. The number that decides the arm

Sparsity of the raw error set is not the question. The question is how many
errors *survive* the Rule 150 kernel:

```
N_eff(n) = |{ (x,t) : E(x,t) = 1 AND projects_to_center(x,t,n) = 1 }|
```

Kill condition, stated before the run: **if `N_eff(n)` is `omega(n)`, sparsity
alone opens no `o(n)` route**, and the arm requires a structural parity collapse
over `N_eff` that step 3's grammar would have to supply and does not yet.

The sweep is a geometric grid `200 * 1.15^k`, deliberately off the power-of-two
lattice. §4.1 says why. Excerpt (37 targets measured):

| n | raw E | N_eff | eff/raw | N_eff / n^2 |
|---|---|---|---|---|
| 200 | 10,289 | 1,088 | 0.1057 | 0.0272 |
| 462 | 53,167 | 4,646 | 0.0874 | 0.0218 |
| 1070 | 285,642 | 19,203 | 0.0672 | 0.0168 |
| 2475 | 1,534,782 | 79,848 | 0.0520 | 0.0130 |
| 4328 | 4,688,571 | 200,262 | 0.0427 | 0.0107 |
| 5725 | 8,201,559 | 339,919 | 0.0415 | 0.0104 |
| 7571 | 14,337,545 | 522,094 | 0.0364 | 0.0091 |
| 8707 | 18,963,534 | 656,174 | 0.0346 | 0.0087 |
| 10000 | 25,010,461 | 834,156 | 0.0334 | 0.0083 |

Log-log fit over the non-aligned targets, and it does not depend on the window:

| fit window | points | slope | max residual (log) |
|---|---|---|---|
| n >= 200 | 29 | 1.6972 | 0.062 |
| n >= 1000 | 17 | 1.6830 | 0.040 |
| n >= 2000 | 12 | 1.6878 | 0.039 |
| n >= 4000 | 7 | 1.6819 | 0.035 |

**`N_eff ~ n^1.68`**, stable to +/- 0.015 across every window. Sub-quadratic,
since the kernel does kill 96.7% of events at n = 10,000 and the survival
fraction is still falling like roughly `n^-0.3`, but decisively `omega(n)`.

### 4.1 The power-of-two targets alias, and are excluded

The kernel `(1+z+z^2)^d` has at most `3^popcount(d)` surviving terms; this
counts the factor choices before GF(2) cancellation, not the exact support.
For example, d=3 gives five surviving terms, not nine. Survival depends on the
bit structure of `d = n-1-t`. A sweep sampled at powers of two reads that
structure rather than the trend. Measured, against the `n >= 1000` non-aligned
fit:

| n | N_eff | fit | ratio |
|---|---|---|---|
| 1024 | 16,492 | 18,127 | 0.910 |
| 2048 | 53,335 | 58,202 | 0.916 |
| 4096 | 173,108 | 186,878 | 0.926 |
| 8192 | 558,456 | 600,037 | 0.931 |

Every power of two sits 7 to 9% low, systematically. A first pass of this probe
swept only powers of two plus round decimals and got 1.67 from the full fit but
1.76 from the top two points, purely because the 4096 anchor is depressed. That
apparent plateau in `eff/raw` between 8192 (0.0333) and 10000 (0.0334) was the
same artifact: the non-aligned neighbours 7571, 8707, 10000 give 0.0364, 0.0346,
0.0334, still monotonically declining.

The exponent is 1.68. The 1.76 figure was an artifact and is retracted.

**The kill condition fires.** At n = 10,000 the parity sum has 834,156 live terms
against a target of `o(10,000)`. Two orders of magnitude, widening with n.

Per-row survival at n = 10,000, by decile of `t`:

| t range | eff/row | raw/row | survival |
|---|---|---|---|
| 0..1000 | 23.7 | 249 | 0.0948 |
| 4000..5000 | 159.5 | 2251 | 0.0709 |
| 5000..6000 | 116.0 | 2751 | 0.0422 |
| 9000..10000 | 33.5 | 4750 | 0.0071 |

Survival is *not* monotone in `t`: the 4000..5000 band survives at 2x the
5000..6000 band despite fewer raw events. That is the popcount structure of
`d = n-1-t`. The factor expansion has `3^popcount(d)` choices before
cancellation; the surviving support depends on collisions between these
choices, even at low popcount. The variation is a property
of the kernel, which is already known in closed form, not of `E`.

## 5. What this leaves open

The negative result is specific: **no bound on `N_eff` alone reaches `o(n)`.**
Two things it does not close.

1. A *cancellation* result would. `N_eff` counts live terms; the sum is a parity.
   If the surviving events organise into structures whose parities cancel in
   blocks, the count is irrelevant. Nothing here measures cancellation, because
   nothing here computes a partial sum over any structural decomposition. That is
   the first thing to measure, and it is cheap: the machinery already exists.
2. The projector is a correct, verified, 36 ns O(log n) primitive with an
   exhaustively checked identity behind it. It is reusable for (1) and worth
   keeping regardless of the outcome of this arm.

Step 3 (the geometric grammar) and step 4 (the fitness metric) should not be
built until (1) returns a number. Building an evolutionary search over spatial
predicates for `E` when the target has 834,156 live terms at n = 10,000 spends
the arm's budget on infrastructure for an unconfirmed contribution, which is the
failure mode the preregistration exists to prevent.

## 6. Cancellation is measured. It does not happen.

§5(1) called for the cancellation measurement before any of step 3. It has now
run. The result closes the escape hatch §5 left open.

Row parity is the natural first decomposition: `Probe::project` already returns
the per-row count of events surviving the kernel, so a row's contribution to the
parity sum is that count mod 2, and any block's contribution is the XOR of its
rows. A cancellation result needs the number of rows with parity 1 to be `o(n)`.

Measured on the same `200 * 1.15^k` grid, non-aligned points only:

| n | non-zero rows | fraction |
|---|---|---|
| 1070 | 523 | 0.4888 |
| 2475 | 1266 | 0.5115 |
| 4045 | 1998 | 0.4939 |
| 5725 | 2889 | 0.5046 |
| 8113 | 4028 | 0.4965 |
| 10000 | 5022 | 0.5022 |

`log(non-zero rows) = 1.0056 * log(n) - 0.7405` over the upper half of the sweep
(15 points). **Row parity survives at exactly `n/2`.** The kernel kills 96.6% of
raw events at n = 10,000 and every one of those kills lands in the count, not in
the parity: a row survives or dies on a coin flip.

Note that a per-`n` reading of `log2(nz)/log2(n)` rises monotonically from 0.80
at n = 64 to 0.925 at n = 10,000 and looks sublinear. It is not. That column is
`1 - log2(2)/log2(n)` for a constant fraction of 1/2, converging to 1 from below.
Only the fit is a statistic. The probe prints the caveat next to the column.

### 6.1 Dyadic blocks do not cancel either

XOR over contiguous blocks of `2^j` rows, n = 8113:

| block size | non-zero / total | fraction |
|---|---|---|
| 1 | 4028 / 8113 | 0.4965 |
| 2 | 2030 / 4057 | 0.5004 |
| 4 | 988 / 2029 | 0.4869 |
| 8 | 524 / 1015 | 0.5163 |
| 16 | 264 / 508 | 0.5197 |
| 32 | 120 / 254 | 0.4724 |
| 64 | 62 / 127 | 0.4882 |
| 128 | 32 / 64 | 0.5000 |
| 256 | 10 / 32 | 0.3125 |

Half the blocks are live at every scale with enough samples to read. Block sizes
at or above 512 have 16, 8, 4 and 2 samples; the `2/2` at 4096 is two coin flips,
not emergent structure, and is not evidence of anything. n = 4045 gives the same
table (0.494, 0.502, 0.482, 0.478, 0.490, ...).

A dyadic block XOR that is 1/2 at every scale is the signature of row parities
with no exploitable joint structure. There is no level at which grouping buys a
reduction.

### 6.2 The structure is uniform in `t`

§4's decile table shows `eff/raw` jumping 2.7x across `t ~ 4055` at n = 8113,
where `d = n-1-t` crosses 4096. That discontinuity is entirely in the count
domain. Row-parity survival by decile of `t`, n = 8113: 0.493, 0.514, 0.501,
0.493, 0.483, 0.473, 0.525, 0.481, 0.515, 0.485. n = 4045: 0.473, 0.522, 0.500,
0.507, 0.490, 0.525, 0.495, 0.473, 0.475, 0.479.

Every decile is 1/2 to within sampling noise. The popcount structure of `d` that
governs how many events survive does not survive into whether an odd number of
them does. There is no band of `t` a grammar could target.

### 6.3 Consequence for the arm

§5's retention of step 3 was conditional on this measurement returning something.
It returns 1/2 at every row, every dyadic scale, and every decile of `t`.

The claim that "step 3's grammar would have to supply" a structural parity
collapse is now measured false for the two decompositions that do not require a
grammar to state. A geometric grammar over spatial predicates for `E` is not
ruled out in principle, but the arm no longer has a reason to expect it: the
cheap structural handles are exhausted and both read as noise.

**Arm 5 is closed.** `N_eff ~ n^1.68` (§4) and row parity ~ `n/2` (§6). Neither
route reaches `o(n)`.

What survives the arm is the projector: `projects_to_center` is a verified
24 ns/call O(log n) primitive, and the superposition identity
`s_n(0) = rule150_center(n) XOR parity(projected errors)` is exhaustively checked
for all `n <= 512` and on 37 banded targets to n = 10,000. Both are reusable.
The `assert_eq!(all, parity)` inside the parity report is tautological (parity of
a sum is the XOR of parities) and is a guard against index errors only; the
identity check in `verify-3` is the anchor.

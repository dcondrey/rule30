# Rule 30 right-cone diagonal periodicity: a known theorem, re-derived, and why it cannot reach the center

## Status

**OPEN, and this line is closed.**  Center-column nonperiodicity is not proved
here and is not advanced here.  What this cycle establishes is a *quantitative
reason why the boundary-anchored program cannot reach it*, which is a
disposition, not a theorem about Rule 30.

1. **KNOWN, re-derived (validation, not discovery):** every right-cone diagonal
   of every finite row is *purely* periodic in time with a power-of-two period.
   Published: Rowland 2006, Lemma 2, in the stronger arbitrary-row form.  The
   citation has been checked against the paper itself.
2. **EXACT COMPUTATION:** the exact periods for the lone seed through diagonal
   64, reproducing the published sequence term for term.
3. **EXACT COMPUTATION (the verdict):** the periodic region reachable from the
   right boundary at time `t` is `~2.4 log2(t)` diagonals wide, while the
   center column at time `t` sits at diagonal `t`.  The gap is exponential and
   grows.  No amount of boundary-anchored analysis closes it.
4. **FALSIFIED:** the mechanism that proved both constant-trace cases does not
   extend to nonconstant periods.

## KNOWN: pure periodicity of the right-cone diagonals

Index a finite row `a` with right endpoint `B` by `E_j[t] = s(t, B+t-j)`, so
`E_j[0] = a(B-j)` and `E_j == 0` for `j<0`.  Rule 30 becomes

```text
E_j[t] = E_j[t-1] XOR (E_{j-1}[t-1] OR E_{j-2}[t-1]),
```

so `E_j` is the running parity of `A_j := E_{j-1} OR E_{j-2}`, offset by
`E_j[0]`.

*Re-derivation.*  `E_0 == 1` and `E_1`, `E_2` are period-two alternations; that
is the PROVED pinned-diagonal corollary of `RESULTS-right-cone.md`.  Suppose
`E_{j-1}`, `E_{j-2}` are purely periodic with power-of-two periods `Q_{j-1}`,
`Q_{j-2}`.  Then `A_j` is purely periodic with period `q = max(Q_{j-1},
Q_{j-2})`, again a power of two.  Let `S` be the weight of `A_j` over one
period.  If `S` is even the running parity returns to its starting value after
`q` steps, so `E_j` is purely periodic with period `q`.  If `S` is odd the
running parity is complemented after `q` steps and restored after `2q`, so
`E_j` is purely periodic with period `2q`.  Either way the period is a power of
two and the preperiod is zero.  QED

**This is not new, and the primary source has now been read.**  Both the
power-of-two theorem and the stronger preperiod-zero-for-every-row form are
published, in Rowland 2006.  Rowland works with rule 86, the left-right
reflected left-justified image of rule 30, precisely so that "the columns
(rather than the diagonals) are periodic" (p. 5); his columns are the `E_j`
above.

* **(A) power-of-two periods.**  Rowland p. 2: "the right diagonals are
  periodic with period lengths `2^alpha`.  (This is shown in Lemma 2.)"  The
  power of two follows from Lemma 2's divisibility bound with `l(k) = lcm(1,
  ..., k)` and `l(2) = 2`.
* **(B) preperiod exactly zero, for arbitrary rows.**  Rowland p. 6, immediately
  before Lemma 2: "A result of Jen [1, Theorem 4] guarantees the eventual
  periodicity of columns in any range `[-d, 0]` cellular automaton with a
  rightful initial condition.  *For right bijective rules, the periodicity is
  not eventual but immediate.*  Intuitively, this is because periodicity in a
  column continues uniquely backward in time.  We formalize this in the
  following result".

  > **Lemma 2.**  Let `f` be a right bijective, `k`-color, range `[-d, 0]` rule,
  > and let `R` in `[k]^Z`.  If, in the computation of `{f^t R}`, columns `m-d,
  > ..., m-1` are periodic with period lengths `p_{m-d}, ..., p_{m-1}`
  > respectively, then column `m` is periodic with period length dividing
  > `l(k) * lcm(p_{m-d}, ..., p_{m-1})`.

  Lemma 2 is proved (pp. 6-7) and quantified over arbitrary `R in [k]^Z`, not
  just the lone seed.  A finite row is *rightful* in Rowland's sense ("a row
  `R` is rightful if there exists a cell to the left of which all cells are a
  single color"), which supplies the two period-1 white base columns the `d=2`
  induction needs.  So the induction above is a re-derivation of the `k=2, d=2`
  case of Lemma 2.

  One thing the induction above states that Lemma 2 does not: Lemma 2 bounds
  `Q_j` only by *divisibility*, `Q_j | 2 * lcm(Q_{j-1}, Q_{j-2})`, and a
  divisor of `2 * max(Q_{j-1}, Q_{j-2})` may be smaller than
  `max(Q_{j-1}, Q_{j-2})`.  The induction's `q` is a period of `A_j`, not
  necessarily its *minimal* period, so it does not close that gap either.
  **Monotonicity of `Q_j` is therefore not proved here or in Lemma 2**; see the
  wall section, where it is load-bearing and is qualified accordingly.
  Brunnbauer's page asserts that right-diagonal periods cannot decrease, but
  gives no proof that was retrievable.

Two corrections to the earlier draft of this file, both from reading the source:

* The figure caption "period doublings occurring as prescribed by Proposition
  2" is Figure 9 of the same Rowland paper, and it sits in section 5, **"The
  left side of rule 30"**, where periodicity is only *eventual*.  Rowland's
  Proposition 2 is a quotation of Wolfram about *left*-side doublings.  It
  carries no weight for (A) or (B); citing it here would have been a
  miscitation.
* The 30-term period sequence should be cited to **OEIS A094605** (Rowland,
  2004), not to NKS p. 871: OEIS records that Wolfram's printed 16-term list
  drops one of the six 64s.  A094605 has offset `1,2`, so its `a(n)` is our
  `Q_{n-1}`.

Wolfram states the periodicity as an observation without proof in both places
(NKS p. 871 note (c), and the 2019 prize post's aside "At 45 degrees, it is easy
to see that any sequence must be periodic"); all three Rule 30 prizes concern
the center column, not the diagonals.  Brunnbauer's page is a personal webpage,
not a preprint, treats the lone seed only, cites neither Rowland nor Jen, and
its author writes "there is probably nothing genuinely new here"; it is not a
source for either theorem and neither verdict rests on it.

- Eric S. Rowland, "Local nested structure in rule 30", *Complex Systems* **16**
  (2006) 239-258.  <https://ericrowland.github.io/papers/Local_nested_structure_in_rule_30.pdf>
  (no arXiv version).  **The citation for both (A) and (B).**
- OEIS **A094605**, "a(n) is the period of the n-th diagonal, from the right, of
  Rule 30 (begun from an initial black cell)", Eric Rowland, 2004-05-13.
  <https://oeis.org/A094605>
- Erica Jen, "Global properties of cellular automata", *J. Stat. Phys.* **43**
  (1986) 219-242.  Rowland's ref [1] (confirmed against his bibliography, p.17);
  Theorem 4 is the eventual-periodicity result Lemma 2 strengthens.  Not
  fetched, and no preprint exists: OSTI holds only the record `biblio/5674011`,
  whose `purl` is 404.  Rowland p.13 instantiates it at Rule 30 and gets exactly
  the diagonal statement above: "A consequence of Jen's Theorem 4 [1] is that
  each left diagonal of rule 30 is eventually periodic with period length a
  power of 2."
- Stephen Wolfram, *A New Kind of Science*, 2002, p. 871 note (c).  Observation,
  no proof.  <https://www.wolframscience.com/nks/notes-2-1--rule-30/>
- Stephen Wolfram, "Announcing the Rule 30 Prizes", 2019-10-01.
  <https://writings.stephenwolfram.com/2019/10/announcing-the-rule-30-prizes/>
- Michael Brunnbauer, "Diagonals in elementary cellular automaton 30", personal
  webpage, 2019-12-09.  <https://brunni.de/findings30/>  Not cited for either
  theorem.

Nothing in this section is a contribution.  `Engine.test_periods_are_powers_of_two_and_pure`
is now a validation of the implementation against Lemma 2, not evidence for a
new claim.

## EXACT COMPUTATION: the periods

`experiments/rule30/diagonal_period_probe.py` computes `E_j` over a whole time
range in `O(log T)` bigint operations per diagonal using the doubling trick for
running parity, and computes exact periods by carrying one full period per
diagonal.  For the lone seed, `log2 Q_j` for `j = 0..64`:

```text
0 1 1 2 3 3 4 5 5 6 6 6 6 6 6 7 8 8 8 8 8 8 8 8 9 10 10 11 11 12 12 12
12 12 13 13 14 15 15 16 16 17 17 18 18 18 18 18 19 20 20 21 21 21 22 23
23 23 24 24 25 25 25 26 27
```

The first thirty periods are `1, 2, 2, 4, 8, 8, 16, 32, 32, 64, 64, 64, 64, 64,
64, 128, 256, 256, 256, 256, 256, 256, 256, 256, 512, 1024, 1024, 2048, 2048,
4096`, matching the published sequence exactly.  Test:
`PublishedOracle.test_lone_seed_periods`.

`log2(Q_j)/j` rises from 0.375 at `j=32` to 0.422 at `j=64`.  It is not
converged over the measurable range and the engine stops near `j=64` because a
single period no longer fits in memory, so treat the growth rate as measured,
not asymptotic.  Equivalently, the diagonals at which the period doubles are

```text
1 3 4 6 7 9 15 16 24 25 27 29 34 36 37 39 41 43 48 49 51 54 55 58 60 63 64
```

which is Rowland's `{a_I(n)}`, and its growth rate is the explicit open
question he closes on (p. 10): "It would be interesting to have more
information on the growth rate of this sequence if asymptotic information
cannot be obtained for `{a_R(n)}` in general."  So the non-convergence above is
not an artifact of our range; it is the same quantity the source leaves open.

## EXACT COMPUTATION: the wall

The center column at time `t` reads diagonal `t+B`: `c_t = E_{t+B}[t]`.  The
table below is the lone seed, where `B=0` and the read index is `t` itself; for
`B>0` the read index is larger while the time is unchanged, so the wall is
wider, and `Q_j > j` on the range established below gives `Q_{t+B} > t` for
every finite row over that range.
So the question is whether the read index ever enters the periodic regime of
the diagonal it reads.  It does not, and not marginally:

| `t` | diagonals with a completed period | diagonal the center reads |
|---:|---:|---:|
| `2^4` | 7 | 16 |
| `2^8` | 24 | 256 |
| `2^12` | 34 | 4096 |
| `2^16` | 41 | 65536 |
| `2^20` | 51 | 1048576 |
| `2^24` | 60 | 16777216 |
| `2^26` | 64 | 67108864 |

The ordered region anchored at the right boundary is `~2.4 log2(t)` diagonals
wide.  The center is at diagonal `t`.  Equivalently `Q_j > j`, so *the center
bit is always read strictly inside the first period of its diagonal*, where
periodicity imposes no constraint at all.

The range on which `Q_j > j` holds needs care, because it is the load-bearing
claim of this whole section and it is not proved beyond the range computed.

* **Computed:** `Q_j > j` for `3 <= j <= 64`, exactly, by the engine.  That
  already covers every row of the table above, whose largest entry is
  `t = 2^26 < Q_64 = 2^27`.  This much is unconditional.
* **Conditional on `Q_j` being nondecreasing:** `Q_64 = 2^27` would give
  `Q_j >= 2^27 > j` for every `j` in `[64, 2^27)` with no further computation,
  extending the claim to all `3 <= j < 134217728`.
* **Monotonicity is measured, not proved.**  It holds for the lone seed through
  `j = 64` and on 300 random width-17 rows through `j = 30`.  It does *not*
  follow from Rowland's Lemma 2, which bounds `Q_j` only by divisibility, nor
  from the `{q, 2q}` induction above, whose `q` need not be the minimal period
  of `A_j`.  A drop `Q_j < Q_{j-1}` is not excluded by anything written here.
* **Beyond `j = 2^27`** it is extrapolation even given monotonicity: falsifying
  it would require the period to stop doubling for more than 134 million
  consecutive diagonals, against a measured `log2(Q_j)/j` of 0.375 to 0.422,
  but no lower bound on the doubling frequency is proved here.

The disposition does not depend on the conditional parts.  Even at the
unconditional range the gap between `2.4 log2(t)` and `t` is already
exponential.

The single exception is exact and permanent rather than a limit of the range
searched: `Q_2 = 2 = j`, which is forced by the pinned-diagonal base case, so
`t=2` is the only time the center read ever wraps.  Test:
`PublishedOracle.test_period_outruns_the_center_read`.

This is the closing argument for the whole boundary-anchored line, including
`RESULTS-right-cone.md`'s sweep and the ARM series' right-cone framings.  Any
argument whose leverage comes from regularity at the right boundary has
`O(log t)` reach into a pattern whose interesting column is at distance
`Theta(t)`.

## An exact closed form, for the record

The same recursion gives, for the lone seed,

```text
c_t = parity of ( E_{t-1}[i] OR E_{t-2}[i] ) for i = 0..t-1.
```

Verified against the naive evaluator for `t <= 200`
(`PublishedOracle.test_closed_form_center`).  It is exact and it is useless in
the direction wanted: it expresses `c_t` as a *partial* parity of two purely
periodic sequences, cut off at `t`, and `t` is always far short of their common
period.  The period-doubling indicator for diagonal `t` is the same functional
evaluated over a *full* period.  Center bit and period doubling are the same
quantity read at incomparable cutoffs.

## FALSIFIED: the constant-trace proof mechanism does not extend

Both constant-trace theorems (`RESULTS-zero-tail.md` and the all-one fiber in
`RESULTS-eventual-period.md`) work because the forced left half *forgets the
right half*: beyond a short transient it is the checkerboard, identically for
every right part, hence infinite, hence no finite row.  This session confirmed
the forgetting directly for the zero target: for `k > W` the forced `a(-k)` is
`1` iff `k` is odd, identical across all `2^W` right parts, for `W <= 12` at
depth 256.

That forgetting is special to constant traces.  For nonconstant periodic
targets the forced left half depends on the right part essentially everywhere:

Deepest `k <= 512` at which the forced bit still differs across right parts,
and how many of the 512 positions differ, at depth 512:

| target | `W=4`, 16 right parts | `W=8`, 256 right parts |
|---|---:|---:|
| `(01)^inf` | 512 (507 of 512) | 512 (511 of 512) |
| `(100)^inf` | 512 (508 of 512) | 512 (510 of 512) |
| `(110)^inf` | 512 (505 of 512) | 512 (508 of 512) |
| `(001010)^inf` | 512 (510 of 512) | 512 (512 of 512) |

There is no transient after which the right half is forgotten.  So the proof
template that closed both constant cases has no nonconstant analogue, which is
a structural explanation for why the constant cases fell and the nonconstant
ones have not.

## Verdict

No path forward from this representation, and the reason is quantitative rather
than a failure of effort: the right boundary's regularity reaches
`O(log t)` diagonals and the target is at diagonal `t`.

What would reopen it, in decreasing order of plausibility:

* An argument anchored at the *left* (chaotic) boundary, or one that is not
  boundary-anchored at all.  Rule 30 is left-permutive, so the left side has no
  analogous rigidity; that is exactly why the right side was attractive and why
  it fails.
* The `periodic center => periodic adjacent column` implication, which with
  Kopra's width-two theorem closes the problem.  It is stated as the second
  exact target in `RESULTS-eventual-period.md` and nothing in the right-cone
  representation touches it: the center and its right neighbour are reads of
  the same diagonal family one time step apart, and the recursion relating them
  is just Rule 30 at `x=1`, so the representation adds no constraint.
* Prior repo work already closed the finite-2-kernel route
  (`ARM6-binary-kernel.md`: at least 8191 distinct residuals), so automaticity
  of the center column, and with it Salon-style diagonal-of-an-automatic-double-
  sequence arguments, is not available.

A fourth possibility, from the source rather than from this work: Rowland's
own open question is the growth rate of the doubling-position sequence
`{a_R(n)}`.  Note the direction.  A *lower* bound on that growth rate would
extend `Q_j > j` past `j = 2^27` and firm up the wall argument, which is
already the disposition here; it would not attack the center column.  An
*upper* bound tight enough to matter would have to show the periods grow no
faster than linearly, contradicting three decades of measurement.  Either way
it is a question about the ordered side, and the wall says the ordered side is
`O(log t)` from where the answer lives.

The problem remains open.  Recent preprints propose frameworks rather than
proofs; none were fetched or assessed here, and none should be cited without
being read.

## Reproduction and spending

From `experiments/rule30`:

```bash
uv run python -m unittest test_diagonal_period_probe.py
uv run python diagonal_period_probe.py --jmax 64
```

Runtime is under a second; the period engine replaces an `O(T)` simulation with
`O(log T)` bigint operations per diagonal.

- Modal: **$0**.  Paid model-provider calls: **$0**.  Crosstalk: not invoked.

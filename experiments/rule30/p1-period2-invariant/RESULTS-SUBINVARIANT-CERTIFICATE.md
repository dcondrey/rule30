# Subinvariant weight on the RW survivor graph: killed, with exact certificates

Date: 2026-09-03.  Scripts `rw_subinvariant_lp.py` and
`verify_subinvariant_negative.py`; logs `subinvariant_lp_20260903.log` and
`subinvariant_certificate_20260903.log`.  Complete census on the validated
kernel `psi_kernel.Endpoint`, all `2^n` binary sources, levels `0..n+3`,
`n = 10..15`, both target cells.  Nothing sampled.

Pre-registered in `PREREGISTRATION-SUBINVARIANT-CERTIFICATE.md` before the
first run; route and literature in `ROUTE-SUBINVARIANT-CERTIFICATE.md`.
Section 6 below records honestly which arms were added after registration and
why.

Status: **KILLED.**  No additive position-indexed weight on the anti-diagonal
is subinvariant along the RW survivor edges, in either encoding of the
"bounded below" requirement, at every window size tested including the one
that leaves every position free.  Arm 1 is killed with exact integer Farkas
certificates.  Arm 3 is feasible, and its only feasible direction is the
diagonal length, which restates the observed run length and proves nothing;
excluding that one direction (arm 4) returns the kill, also with exact integer
certificates.  Both `t = 0` results are certificate-level, not solver output.

## 1. The structural fact that sets the design

The survivor graph is a **DAG with out-degree one**, and this is forced rather
than measured: a state is the exact endpoint `(column, diagonal)`, every append
lengthens it by one, so no state recurs.  Two consequences:

- Vere-Jones Criterion I and the Pavlov first-return twin
  (`ROUTE-SUBINVARIANT-CERTIFICATE.md` section 6) never apply here.  They need
  returns to a distinguished state and there are none.
- A finite LP with free per-state weights is **vacuous**: `w(s) = rho^depth`
  satisfies subinvariance for every `rho < 1`.

So the experiment is the restricted weight class, never the inequality.  With

```text
log w(s) = sum_{k<K} x[k][dia_k(s)] + sum_{k>=K} a[dia_k(s)]
```

the LP maximises `t = log(1/rho)` subject to `phi(s') . z - phi(s) . z <= -t`
on every survivor edge, and `(RW-alpha)` needs

```text
alpha_hat(n) = max_{s_0} log w(s_0) / ( n * t )   <   1.
```

`K = 40` exceeds the longest diagonal in range (`15 + 19 = 34`), so that column
of every table is the class with **every position free and no tail term at
all**: the most general additive position-indexed weight there is.

## 2. Arm 1, the pre-registered class: infeasible, with certificates

`x, a >= 0`, so `w >= 1` on every state and `inf_s w = 1` by construction.

| `n` | edges (`c=2`) | edges (`c=3`) | `t`, `K=8` | `t`, `K=40` |
|---:|---:|---:|---:|---:|
| 10 | 208 | 222 | 0 | 0 / **0.00695** (`c=3`) |
| 11 | 340 | 410 | 0 | 0 |
| 12 | 721 | 707 | 0 | 0 |
| 13 | 1214 | 1226 | 0 | 0 |
| 14 | 2175 | 2201 | 0 | 0 |
| 15 | 3667 | 3826 | 0 | 0 |

`t = 0` is the LP's **optimum**, not a failure to converge: `t = 0, x = 0` is
always feasible, so a solver stall would look the same, and that is exactly why
the certificates below exist.  It means the best available weight is flat on
some survivor edge, so it bounds no run at all.  The single exception is `n = 10, c = 3` at `K >= 16`,
where `t = 0.00695` is feasible but `alpha_hat = 39.73`, far above the `1.0`
that `(RW-alpha)` needs; it does not recur at any larger `n`.  Kill condition 2
covers it and kill condition 1 covers everything else.

**Exact negative certificates.**  A returned LP optimum is not a proof, so
`verify_subinvariant_negative.py` shrinks the edge set greedily to a core that
still forces `t = 0`, extracts a nonnegative **integer** multiset `y` of
survivor edges by MIP, and verifies in exact integer arithmetic that

```text
sum_i y_i * D_i >= 0 componentwise,   sum_i y_i >= 1.
```

Any `z >= 0` then has `sum_i y_i (D_i . z) >= 0`, so some edge fails to
decrease.  Coefficient magnitude is irrelevant, exactly as in the locality-1..4
refutation of `RESULTS.md` section 4.

| `n` | `K` | `c=2` core / support | `c=3` core / support |
|---:|---:|---|---|
| 10 | 0 | 1 / 1 | 1 / 1 |
| 10 | 8 | 8 / 8 | 23 / 23 |
| 10 | 40 | 15 / 15 | feasible, see above |
| 12 | 0 | 1 / 1 | 1 / 1 |
| 12 | 8 | 19 / 19 | 20 / 20 |
| 12 | 40 | 13 / 13 | 22 / 22 |
| 14 | 0 | 1 / 1 | 1 / 1 |
| 14 | 8 | 4 / 4 | 10 / 10 |
| 14 | 40 | 27 / 27 | 26 / 26 |

All verified in exact integers.  The `K = 0` certificate is a **single survivor
edge** whose anti-diagonal symbol counts change by

```text
(#0, #1, #2, #3)  +=  (1, 0, 0, 0),
```

the same edge type at `n = 10, 12, 14` and both `c`.  One survivor step gains a
`0` in the anti-diagonal and disturbs nothing else, so every nonnegative
symbol-count weight increases across it.  At `K = 8` the certificates are more
interesting: the aggregate cancels every position-indexed coordinate exactly and
leaves only the tail counts positive, e.g. `[0]*32 + [73, 37, 0, 61]` at
`n = 12, c = 3`.

## 3. Arm 2, the diagnostic that names the binding constraint

Dropping `z >= 0` and imposing no lower bound gives `t = 1.0` at every `n`, both
`c`, attained by `x[k][s] = a[s] = -1` for all `k, s`, that is

```text
log w(s) = - (diagonal length).
```

Unbounded below, bounds nothing.  This is the same degeneracy `RESULTS.md`
lines 186-188 recorded for the signed case at locality 1 ("simply minus the word
length and tends to negative infinity").  So the binding obstruction is exactly
`inf_s w > 0`, which `ROUTE-SUBINVARIANT-CERTIFICATE.md` section 3.1 named as
"the real work" before any of this ran.  That prediction is confirmed.

## 4. Arm 3, the weaker and correct lower-bound requirement, and why its green light is empty

Arm 1's `z >= 0` is **sufficient but not necessary** for route section 3.1.  The
requirement is only `inf w > 0` over states the survivor run actually visits,
and `RESULTS.md` lines 142-147 names precisely that as the clause outside its
normal form: "an energy whose lower bound relies on a special reachable
sublanguage".  Arm 3 encodes it directly: signed coefficients, with
`log w(s) >= 0` imposed on **every survivor state of the census** rather than on
every word.

It is feasible, and at first reading it looks like the strong outcome.  The
last column is what makes it worthless, and it is measured, not asserted:

| `n` | `c` | `t` | `alpha_hat` | longest actual survivor run / `n` |
|---:|---:|---:|---:|---:|
| 10 | 2 | 1.000 | 0.5000 | 5 / 10 = 0.5000 |
| 10 | 3 | 0.889 | 0.7000 | 7 / 10 = 0.7000 |
| 11 | 2 | 0.889 | 0.5455 | 6 / 11 = 0.5455 |
| 11 | 3 | 0.800 | 0.6364 | 7 / 11 = 0.6364 |
| 12 | 2 | 0.615 | 0.7500 | 9 / 12 = 0.7500 |
| 12 | 3 | 0.667 | 0.6667 | 8 / 12 = 0.6667 |
| 13 | 2 | 0.667 | 0.5385 | 7 / 13 = 0.5385 |
| 13 | 3 | 0.571 | 0.6923 | 9 / 13 = 0.6923 |
| 14 | 2 | 0.500 | 0.7143 | 10 / 14 = 0.7143 |
| 14 | 3 | 0.571 | 0.5714 | 8 / 14 = 0.5714 |

`alpha_hat` equals the observed longest run divided by `n` in **all ten cells**.
The LP is not bounding the run; it is reading it off the census.  The `n = 14`
fit also transfers to `n = 16` with zero violated edges, which sounds like the
pre-registered holdout passing.

The fitted weight says why this is worthless.  It is symbol-independent:

```text
x[k][s] = 1  for every k < 8 and every symbol s,     a[s] = -t.
```

So `log w` is an affine function of the **diagonal length** and reads nothing
about the state.  Subinvariance is then automatic, because every step lengthens
the diagonal by one, and the LP's optimum simply sets `t` so that the weight
runs out exactly at the longest observed run: `alpha_hat` reproduces
`max run / n`, which is the quantity to be bounded.  That is route section 3.2's
vacuous weight in a third costume, and the holdout "pass" is a length identity
transferring, not a state law.

The lower bound also does not survive.  Fitted at `n = 14`, `min log w` over
survivor states is `0` by construction; carried unchanged to larger `n` it
becomes `-0.000` (`c=2`) and `-0.571` (`c=3`) at `n = 15`, then `-1.000`
(`c=2`) and `-2.286` (`c=3`) at `n = 16`.  It drifts down with `n`, so there is
no uniform `inf w > 0` even on the sublanguage.

## 5. Arm 4, the decision: exclude the length direction and the kill returns

Constrain each position block to sum to zero, `sum_s x[k][s] = 0` and
`sum_s a[s] = 0`, leaving only contrasts **between** symbols.  A positive `t`
must then come from the state rather than from the clock.  Signed coefficients
and the sublanguage lower bound are both retained, so this is strictly more
general than the pre-registered arm 1 in every respect except the one direction
that is known to be vacuous.

`t = 0` at `n = 10..14`, both `c`, at `K = 0, 8, 16, 40`.  Every cell.

**Exact certificates for this arm too**, so the kill does not rest on a
floating-point optimum.  The Farkas alternative here carries three blocks, by
Motzkin transposition: `y >= 0` over survivor edges, `u >= 0` over survivor
states, and `v` free over the `K+1` position blocks, with

```text
D^T y - S^T u + E^T v = 0,      sum y >= 1.
```

Any admissible `x` then has `sum_i y_i (D_i . x) = sum_j u_j (S_j . x) >= 0`,
since `E^T v` annihilates every contrast weight, so some survivor edge fails to
decrease.  `verify_subinvariant_negative.py --arm4` finds integer `y, u, v` by
MIP and checks the identity in exact integers.

Verified at `n = 10, 12, 14`, both `c`, at `K = 0, 8, 40`: **18 of 18**.  Every
one has `sum y = 1`, that is a **single survivor edge** `i` with

```text
D_i = S^T u - E^T v,
```

so on that one edge no contrast weight bounded below on the survivor states can
decrease at all.  The state support runs from 5 to 192; the block multipliers
`v` are the length direction the arm excludes.

That is the result.  The feasible set of arm 3 is exactly the length tautology;
once it is removed, nothing remains, and the removal is certified.

## 6. What was pre-registered and what was added

Arms 1 and 2 are as pre-registered.  Arms 3 and 4 were **added after the first
run**, and the reason is recorded rather than smoothed over: arm 1's
nonnegativity is a stronger requirement than route section 3.1 imposes, so a
kill of arm 1 alone would have been a kill of a strawman, and the sublanguage
clause is the exact escape hatch the prior refutation named.  Adding them made
the test harder to pass, not easier; arm 3 was run before its degeneracy was
known, and arm 4 was written only after the fitted arm-3 weight was inspected.
No result here rests on arm 1 alone.

## 7. Scope: what is dead and what is untouched

**Dead.**  Every weight of the form `log w(s) = sum_k f_k(dia_k(s))` on the RW
survivor graph, with `f_k` arbitrary at every position through the **full
diagonal length** (the `K = 40` column has no tail term at all in this range),
whether the coefficients are nonnegative or signed with a lower bound required
only on the survivor sublanguage.  This is a proper extension of
capsule section 5 row 1 to a new graph and to unbounded-radius statistics: the
old Farkas work covered bounded windows of the macro-frontier word, and this
covers the whole anti-diagonal, position by position.

**Untouched, and not evidence for anything.**

- Weights that are **not additive over positions**: the anti-diagonal's ordered
  gap structure, pattern occurrences, or any nonlinear functional.  Additivity,
  not radius, is what these certificates exploit.
- The count-to-run-length conversion of route section 5.  This experiment lives
  entirely on the forced deterministic graph and bounds a run; it says nothing
  about survivor counts on the branching source graph, and the two must not be
  mixed.
- `n >= 16` for the certificate arm, and the census beyond `n = 15`.
  Obstruction H applies: a complete search is a lower bound on a complexity
  function and never more.

## 8. Reproduction

```sh
cd experiments/rule30/p1-period2-invariant
uv run python rw_subinvariant_lp.py --min-n 10 --max-n 15 --K 8
uv run python rw_subinvariant_lp.py --min-n 10 --max-n 14 --K 40 --sublanguage --contrast
uv run python verify_subinvariant_negative.py --n 12 --K 40
uv run python rw_subinvariant_lp.py --min-n 10 --max-n 14 --max-run
```

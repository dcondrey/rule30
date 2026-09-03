# Route: a subinvariant weight as a finite certificate on an infinite state graph

Date: 2026-09-03.  **Not attempted.**  This file records a technique found by
literature search, states it precisely enough to implement, and marks the two
places it can fail.  Nothing here is a result.

## 1. The technique

Vere-Jones, "Ergodic properties of nonnegative matrices - I", *Pacific J. Math.*
22(2):361-386 (1967).  Open access at Project Euclid.  Section 4, p.369 defines
an **`r`-subinvariant vector** for a nonnegative matrix `T` as a nonnegative
nonzero solution of

```text
r * sum_k x_k t_kj  <=  x_j.
```

Corollary 1, p.370: there are no nontrivial `r`-subinvariant vectors for
`r > R`.  Criterion I, p.372: `R` is the greatest `r` admitting one, where `R`
is the radius of convergence of `sum_n t_ij^(n) z^n`, so path counts grow like
`R^(-n)`.

Applied here.  Build the survivor sub-automaton on endpoint states, the states
keeping the forced cell equal to `c`.  Exhibit a positive weight `w` with

```text
sum_{s -> s'} w(s')  <=  rho * w(s)      for every survivor state s.
```

Then survivor paths of length `m` from `s_0` number at most
`rho^m * w(s_0) / inf_s w`.

Why this is worth the attention of a program that has killed eleven mechanism
classes:

- The sound direction is **elementary induction and needs no irreducibility**.
  That matters, because the survivor sub-automaton is not irreducible.
  Irreducibility is needed only for Criterion I's converse, that the best `rho`
  equals the true rate.
- It applies directly to an **infinite state graph**, with no truncation and no
  monotonicity argument.  Every previous mechanism here failed by needing a
  bounded quotient of a growing state.
- It is a certificate: once `w` is written down, checking it is finite work per
  state and the induction is one line.

## 2. Its specialisation to this problem is a Lyapunov weight

In the forced regime the continuation is deterministic, so each survivor state
has exactly one successor and the sum collapses:

```text
w(s')  <=  rho * w(s)      whenever s survives to s'.
```

So a subinvariant weight here is exactly a **positive function, bounded below,
that decreases by a factor `rho < 1` along every surviving step.**  It bounds
the survivor run directly:

```text
run length  <=  ( log w(s_0) - log inf_s w ) / log(1/rho).
```

For `(RW-alpha)` we need that bound to be `alpha * n + C` with `alpha < 1`, so
we need `log w(s_0) = O(n)` and the constant `log(1/rho)` to beat the growth of
`log w(s_0)` per source symbol.  That is a sharper and more checkable target
than any rate statement this program has attempted.

## 3. The two ways it fails, stated before starting

1. **`inf_s w > 0` is not automatic on an infinite state set.**  A weight that
   decays along the growing states gives a vacuous bound.  Any candidate must
   come with a proof that it is bounded below, and that proof is the real work.
2. **The certificate is finite only if `w` has a finite description.**  A `w`
   defined by "count the legal continuations" is exactly subinvariant and
   completely useless, since it is the quantity to be bounded.

## 4. What is already dead here, so the candidate class is constrained

`PROOF-STATE-CAPSULE.md` section 5 records "fixed-radius additive energy:
Farkas contradictions for localities 1--4; radius-seven negative cycles".  Since
`log w` is an additive potential, **any subinvariant weight built from a
statistic of bounded radius is already refuted.**  Do not re-run that.

The candidate must therefore be an unbounded but finitely described statistic.
The two proved memory laws are the natural source, and they are the reason this
route is worth trying now rather than a year ago:

- `RESULTS-COLUMN-DECOMPOSITION.md` 5c: the column entry at distance `d`
  depends on the last `ceil((d+1)/2)` symbols.
- `RESULTS-DIAGONAL-MEMORY.md` 4: the diagonal entry at index `i` of a
  length-`L` word depends on the last `ceil((L+i+1)/2)` symbols.

A weight of the form `w(s) = prod_k beta_k^{[dia_k in S]}`, with `beta_k`
chosen by the memory profile rather than by a fixed radius, is outside the
refuted class.  Whether any such weight is subinvariant is untested.

## 5. The gap the literature does not close

Both this technique and its combinatorial twin bound a **count**, not a run
length.  `rho < 2` says the surviving fraction of length-`n` words is
`(rho/2)^n`, a density statement; `rho < 1` gives a constant run bound, not
`alpha n + C`.  Converting a per-depth survivor count into a per-input-symbol
run bound is exactly where the half-memory laws would do the work, since depth
`u` costs only about `u/2` input symbols and that exchange rate is the `alpha`.

**No theorem in the literature performs that conversion.**  Any write-up must
say so rather than implying the toolkit reaches the target.

## 6. The combinatorial twin

Pavlov, "On entropy and intrinsic ergodicity of coded subshifts", *Proc. AMS*
148(11):4717-4731 (2020), arXiv:1803.05966, Theorem 1.3: if `f_C(h(L_C)) > 1`
and `C` has unique decomposition, then `h(X_C)` is the unique solution of
`f_C(x) = 1`, with `f_C(alpha) = sum_j |C_j| e^(-j alpha)`; equivalently
`h = log lambda` where `sum_j |C_j| lambda^(-j) = 1`.  The hypothesis is unique
*decomposition*, weaker than unique decipherability.  The `S`-gap special case
is Climenhaga-Thompson, *Israel J. Math* 192:785-817 (2012), arXiv:1011.2780.

Directly computable from existing data: if the survivor automaton has a
distinguished state it returns to, count first-return paths by depth and solve
`sum f_m lambda^(-m) = 1`.  This is Vere-Jones' `F_ii(R) = 1` in combinatorial
clothing.

## 7. Two positioning facts from the same search

- **The memory laws have no name in the literature.**  The closest formalism is
  Kopra's Definition 3.1 (arXiv:2202.13809), the rectangle `R(h,d,w)` and left
  expansivity "with dimensions", where `h > 0` is a slope-limited determining
  region and `s < 1/h` compares spreading speed against that slope.  Rule 30 has
  `h = 0`.  Cite it as the closest formalism, not as prior art for the lemma.
- **Directional entropy is the right vocabulary and a vacuous bound here.**
  Courbage-Kaminski (arXiv:nlin/0603058) give
  `h_v <= h(sigma)(lambda_v^+ + lambda_v^-)`; for Rule 30 with `l=-1, r=1, p=2`
  in direction `(0,1)` the product `z_l z_r = -1 <= 0`, so the bound is
  `2 log 2`.  It cannot be sharpened by a half-memory claim: for a left
  permutive rule their section 3 gives `lambda_v^+ = max(-z_l, 0)` **exactly**,
  pinned at 1 by permutivity.  Do not spend time here.

## 8. Explicitly not a route

Lovasz Local Lemma, Moser-Tardos and entropy compression prove the *existence*
of a long constraint-avoiding word.  This program needs an upper bound over all
words.  Wrong direction; do not chase the citing literature.

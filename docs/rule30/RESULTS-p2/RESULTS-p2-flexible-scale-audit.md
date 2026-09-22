# P2: retain every scale and measure the limits of sign diversity

Date: 2026-09-11. **P2 remains open.** This audit addresses the unnecessary
square-root cutoff identified in the [research audit](AUDIT-p2-overlooked-implications.md).
It checks every available dyadic scale, gives an exact rational audit score,
and tests a cancellation certificate without a fixed loss threshold or fixed
waiting time. It also finds that this sign certificate misses strong late
cancellation in the actual stored singleton-seed sequence.

The scope is universal inequalities plus finite measurements. No estimate
below forces cancellation from the singleton initial condition.

## 1. A scale-independent acceptance test

On a shell of length `N=2^k`, let `M` be the largest absolute prefix sum of
the signs `z_t=1-2c_t`. For aligned length-`L=2^j` block sums define

\[
 E_j=\sum_a b_{j,a}^2,\qquad V_j=\frac{E_j}{NL}.
\]

The existing Cauchy--Schwarz estimate is

\[
 \frac MN\leq\sqrt{V_j}+\frac{L-1}{N}.
\tag{1}
\]

Instead of prespecifying a cutoff, retain the exact rational number

\[
 F=\min_{0\leq j\leq k}\left(V_j+\frac{4^j}{N^2}\right).
\tag{2}
\]

**Universal comparison.** Writing `m=M/N`,

\[
 \boxed{\frac{m^2}{2}\leq F\leq5m.}
\tag{3}
\]

For the lower bound, square (1) and use `(a+b)^2<=2(a^2+b^2)`.
For the upper bound, every block sum has magnitude at most `2M`, so
`V_j<=4M^2/L^2`. If `M<N/2`, select the dyadic `L` nearest to
`sqrt(2MN)` on a logarithmic scale. It lies in `[1,N]`, and
`x=L^2/(2MN)` lies in `[1/2,2]`. Consequently

\[
 V_j+\frac{L^2}{N^2}
 \leq2m(x+x^{-1})\leq5m.
\]

If `M>=N/2`, choose `L=N`, giving `F<=2<=4m`.

Together with the established shell-prefix equivalence, this proves

\[
 \mathrm{P2}\quad\Longleftrightarrow\quad F_k\longrightarrow0.
\]

This is an **acceptance test, not an easier conjecture**. Its advantage is
that it discards no possible cancellation scale. A minimizing scale has
both `V_j<=F` and `L/N<=sqrt(F)`. Thus the boundary penalty automatically
rejects cancellation confined to blocks comparable to the whole shell.
The proof selecting `L` from `M` establishes an equivalence; it does not
construct a predictive seed bound.

The program also reports the slightly sharper finite bound obtained by
minimizing the right side of (1). That optimization uses floating-point
square roots only for diagnostics. The score (2), its minimizer, and the
checks in (3) use exact fractions.

## 2. A larger fixed cutoff does not remove the general restriction

There is no single predetermined sublinear dyadic schedule `L_k=o(N_k)`
that captures cancellation for every sign sequence satisfying P2.

To see this, set `H_k` to the largest power of two at most
`sqrt(N_k L_k)`, and on each sufficiently large shell alternate runs of
`H_k` plus signs and `H_k` minus signs. Then

\[
 \frac{H_k}{N_k}\longrightarrow0,\qquad
 \frac{H_k}{L_k}\longrightarrow\infty.
\]

Every shell has total sum zero and maximum prefix `H_k`, so the assembled
sequence has density one-half. But all aligned blocks with length at most
`L_k` are constant, giving `V_j=1` throughout that entire prescribed range.

This artificial construction is not Rule 30. It shows why replacing
`sqrt(N)` by `N^(3/4)`, `N/log(N)`, or any other one fixed sublinear schedule
still imposes an extra hypothesis. Any such hypothesis could be correct
for the seed; failure of it would leave the unrestricted criterion intact.

## 3. Sign diversity without a fixed threshold or waiting time

For each group of four length-`2^j` blocks, count its squared energy toward
`G_j` if it has at most two positive sums and at most two negative sums.
The [previous sign-diversity lemma](RESULTS-p2-cancellation-mechanisms.md)
gives, with `Theta_j=G_j/E_j` when `E_j>0`,

\[
 V_{j+2}\leq(1-\Theta_j/2)V_j.
\tag{4}
\]

Set `Theta_j=0` if `E_j=0`. Starting with `C_0=C_1=1`, define

\[
 C_J=\min\{C_{J-1},\ C_{J-2}(1-\Theta_{J-2}/2)\}
 \quad(J\geq2).
\tag{5}
\]

Induction using monotonicity of `V` and (4) proves `V_J<=C_J`.
Equivalently, `C_J` is the smallest product of the certified survival
factors over any collection of nonoverlapping two-merge windows ending
before `J`. Adjacent starting indices cannot both be used; this avoids
counting the same merge twice.

Thus it suffices to prove seed-specific cutoffs `J_k` with
`k-J_k->infinity` and `C_(k,J_k)->0`. There is no required fixed positive
`Theta`, no requirement at every merge, and no upper bound on waiting times.
Since `0<=Theta/2<=1/2`, a product over chosen windows tends to zero exactly
when the sum of their `Theta` values diverges. This follows from
`x<=-log(1-x)<=2x` on `[0,1/2]`.

This remains a **sufficient certificate**. It cannot replace the exact
criterion (2); the following controls demonstrate the difference.

## 4. A balanced family defeats even the optimized sign certificate

Let `H=2^h`, with `h>=3` and `4H<=N`, and repeat the length-`2H` cycle

\[
 +^H\;-^{H-2}\;+^2.
\]

Take `H=2^floor(3k/4)` on successive sufficiently large shells. Direct
counting gives

\[
 S(N)=\frac{2N}{H},\qquad
 M=H+\frac{2N}{H}-4.
\]

Hence `M/N->0`. At length `2H`, every block sum is 4, so

\[
 V_{h+1}=\frac4{H^2},\qquad
 \frac MN\leq\frac2H+\frac{2H-1}{N}\longrightarrow0.
\]

However, the only nonzero sign-diversity fractions are

\[
 \Theta_0=2/H,\qquad \Theta_{h-1}=\Theta_h=1.
\]

At the first level, only the final `--++` group in each cycle is diverse.
For intermediate scales the exceptional group has at least three negative
sums; at the two transition scales the groups have at most two sums of
either sign.
Afterward all block sums are positive. The two transition windows overlap,
so (5) can use at most one. Therefore, even at the full shell scale,

\[
 \boxed{C_k=\frac12(1-1/H)\longrightarrow\frac12.}
\]

This example has **nonzero energy at every level**, so an extra rule that
recognizes exact zero energy does not repair the sign-diversity product.
The exact two-merge loss nearly annihilates energy in one step; (4) records
at most a factor one-half. The earlier balanced-run example also has
`C_k=1/2`, but its exact energy becomes zero after crossing a run boundary.

The practical correction is to keep exact contrast or energy as the main
audit quantity and treat sign diversity as an optional causal proof tool.
Neither a divergent count of contractions nor a divergent sum of bounded
sign-diversity factors is necessary for P2.

## 5. Finite singleton-seed results at every available level

The existing stored data cover shells `k=1,...,28`. The new scan computes
all **378** four-block profiles with `0<=j<=k-2`: it rechecks all 169 earlier
profiles and adds 209 beyond the previous domain. It also recomputes every
shell's total and maximum prefix directly from the stored bits.

The optimized energy bounds improve when the square-root restriction is
removed:

| k | Old best j, with j<=floor(k/2) | Old bound for M/N | Best j over all scales | New bound for M/N | Actual M/N |
|---:|---:|---:|---:|---:|---:|
| 8 | 4 | 0.318176 | 5 | 0.301966 | 0.046875 |
| 12 | 6 | 0.157087 | 8 | 0.127210 | 0.0158691 |
| 16 | 8 | 0.0696986 | 10 | 0.0468807 | 0.00559998 |
| 20 | 10 | 0.0319577 | 12 | 0.0199848 | 0.00114250 |
| 24 | 12 | 0.0160831 | 15 | 0.00759173 | 0.000315189 |
| 28 | 14 | 0.00786135 | 18 | 0.00293268 | 0.0000309311 |

At `k=28` the exact score is
`F=10511493/2199023255552`, minimized at `j=18`. The all-scale bound is about
2.68 times smaller than the earlier restricted bound, while remaining much
larger than the directly measured discrepancy. These are finite numerical
certificates and imply no limiting rate.

The old measured `Theta>=1/4` property does **not** extend to all levels:
48 active profiles fall below one-quarter. For an especially revealing
actual-seed example, at `k=28,j=26` the four block sums are

\[
 (-5906,-304,11572,-6458).
\]

Their three negative entries give `Theta=0`, yet the exact two-merge
survival fraction is

\[
 \frac{E_{28}}{4E_{26}}
 =\frac{37538}{26323775}\simeq0.001426.
\]

Thus more than **99.85%** of that normalized energy disappears while the
sign-diversity certificate records no loss. These particular blocks are
comparable to the shell, so this event by itself is not an asymptotic P2
certificate. Its role is to show, on the actual data, how much the optional
sign test can discard.

The best bound from the optimized diversity product at `k=28` is about
0.256548, compared with 0.00293268 from the exact energy. This quantitative
gap is consistent with the certificate's deliberate loss of magnitude
information. It does not disprove an eventual seed theorem about diversity.

## 6. Verification and remaining proof obligation

Run:

```sh
uv run python experiments/rule30/p2_flexible_scale_audit.py
```

- [Program](../../experiments/rule30/p2_flexible_scale_audit.py) and
  [exact records](../../experiments/rule30/p2-flexible-scale-audit.json).
- Exhaustive checks cover all 278 sign words of lengths 1, 2, 4, and 8.
  They verify the prefix inequality, rational score comparison, diversity
  inequality, and product bound using integers and fractions.
- Six artificial shells check late balanced and late nearly balanced
  cancellation, including the exact product formula above.
- All 378 measured diversity profiles satisfy (4); all 169 earlier
  profiles agree exactly. Three profiles at `(k,j)=(8,5),(28,25),(28,26)`
  are independently counted with byte population counts and agree with the
  recursively aggregated energies. The displayed four-block witness uses
  this independent counting method.
- The source-profile hash and inherited payload provenance are recorded
  in the artifact. The large CA payload is reused, not regenerated or
  independently validated at every time. No frozen engine is modified.

The scale restriction is now removed from the audit and acceptance test.
What remains is an all-scale statement that the **singleton seed itself**
makes `F_k` tend to zero, or another independently obtained sufficient
bound. Selecting a good scale from already observed energy is not that
statement. More scale profiles cannot supply the missing causal argument.

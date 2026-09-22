# P2: ordered energy loss and the remaining dynamical estimate

Date: 2026-09-09.

**P2 remains open. No requested ladder rung is established.** This follow-up
tests an inequality, rather than the exact temporal-mean closure tested in
`RESULTS-p2-temporal-mean-nonclosure.md`. Failure of exact closure does not
preclude a useful upper bound. The result below identifies a sufficient
accumulated loss and proves that exceptional steps with no loss are harmless.
It does not establish that loss for the lone seed.

The target throughout is
`T^(-1) sum_(0<=t<T) c_t -> 1/2`, where `c_t` is a bit.

## 1. Mechanism, acceptance test, and scope of rejection

Retain the signed sums of **ordered adjacent time blocks**. Merging two
blocks loses normalized squared mean by their squared contrast. The proposed
proof would establish enough of this loss on the actual seed's shells,
before the blocks become comparable in length to the shell.

Acceptance requires an all-scale, seed-specific estimate. A finite profile
is only a diagnostic. A failure of a proposed one-step inequality rejects
that inequality on the stated domain, not accumulated contraction, not the
whole energy approach, and not P2. No ensemble averages are used.

## 2. Exact loss identity [U; universal deterministic, not seed decay]

For a sign word `z` of length `N=2^k`, let `b_(j,a)` be its sum in aligned
block `a` of length `L=2^j`. Define

```text
E_j = sum_a b_(j,a)^2,
V_j = E_j / (N 2^j),
D_j = sum_a (b_(j,2a) - b_(j,2a+1))^2,       0 <= j < k.
```

Expanding `(u+v)^2 = 2u^2+2v^2-(u-v)^2` proves

```text
E_(j+1) = 2 E_j - D_j,
0 <= D_j <= 2 E_j,
V_(j+1) = V_j (1-delta_j),
delta_j = D_j/(2 E_j) when E_j>0; delta_j=0 when E_j=0.
```

When `E_j=0`, every block sum at that level vanishes, so all subsequent
energies also vanish. Thus the convention handles this case correctly.
Since `V_0=1`, the exact accumulated loss is

```text
V_j = product_(i<j) (1-delta_i).
```

The identity retains the cross term between the two ordered halves. It
uses no independence assumption and no CA property.

## 3. A single intermediate scale suffices [U/R; fixed-sequence criterion]

Let `M` be the maximum absolute prefix sum of `z`. For every `j`,

```text
M/N <= sqrt(V_j) + (2^j-1)/N.                         (1)
```

Proof: a prefix consists of `m` complete length-`L` blocks and a remainder
of at most `L-1` signs. Cauchy--Schwarz bounds the complete part by
`sqrt(m E_j) <= sqrt((N/L) E_j) = N sqrt(V_j)`. This proves (1).

Consequently, the already proved shell criterion gives the exact statement

```text
P2 iff there exist cutoffs j_k with
       2^(j_k-k) -> 0 and V_(k,j_k) -> 0.              (2)
```

Here all block sums are taken on the actual shell
`z_k(r)=1-2c_(2^k+r)`, not on arbitrary-input cones.

The sufficient direction is (1). For necessity, P2 gives `M_k/N -> 0` by
the existing shell equivalence. Every interval sum has absolute value at
most `2 M_k`, so `V_(k,j) <= 4 M_k^2/L^2`. Choose the largest dyadic `L`
not exceeding `sqrt(M_k N)`. Then

```text
L/N <= sqrt(M_k/N) -> 0,
V_(k,j) < 16 M_k/N -> 0.
```

The sign word has `M_k>=1`, so this choice always exists. This proves
necessity; it is not an independently established estimate of `M_k`.

## 4. Sparse contraction suffices [R; no seed hypothesis proved]

Fix `0<eta<1`. Let `G_(k,j)(eta)` count indices `i<j` at which
`E_(k,i)>0` and `delta_(k,i)>=eta`. The product identity gives

```text
V_(k,j) <= (1-eta)^G_(k,j)(eta),
M_k/N <= (1-eta)^(G_(k,j)(eta)/2) + 2^(j-k).          (3)
```

Thus it would suffice to prove, on the lone seed, cutoffs `j_k` satisfying

```text
k-j_k -> infinity,
G_(k,j_k)(eta) -> infinity.
```

No fixed positive proportion of scales is necessary for this sufficient
test. Arbitrarily many intervening zero-loss steps are permitted. Nor is
a power saving necessary: the right side of (3) may tend to zero slowly.

**This is a reduction, not rung 5.** The displayed condition is not claimed
to be a recognized external conjecture, and it has not been proved for the
seed. Accumulated loss can also tend to one through a few factors tending
to zero, so the count condition is sufficient, not necessary.

## 5. What the OR rule supplies, and what it does not

**[U; Rule-30-specific identity, all configurations.]** At time `t`, write
the local bits as `(l,c,r)` and use the frozen rule
`c_next = l XOR (c OR r)`. The first pair mean is exactly

```text
A = (z_t+z_(t+1))/2
  = 1_(c=0 and l=r) - 1_(c=1 and l=0).
```

For disjoint pairs, `E_1=4 sum A^2`. In the notation above,
`delta_0` is the fraction of pairs whose two centre bits differ.
The previous OR-pairing report verifies the eight truth-table cases.

**Unresolved seed-specific step:** obtain a lower bound on the accumulated
contrast of the *signed sums of these pairs* at growing temporal scales.
The OR formula fixes the first merging step. It supplies neither a
uniform count of later contractions nor a bound on their product. Keeping
the actual order preserves these quantities exactly, but is not a proof
that they are small. Equation (1) already uses the observed sums in all
blocks of a shell; it does not predict future blocks from earlier blocks.

### Actual zero-loss steps [M/C; lone seed, finite only]

In the twelve checked shells `k=1,...,12`, the only indices with
`E_j>0` and `D_j=0` are:

| shell `k` | merge level `j` | child sums | `E_j` | `D_j` |
|---:|---:|---|---:|---:|
| 2 | 0 | `(-1,-1,1,1)` | 4 | 0 |
| 11 | 10 | `(-2,-2)` | 8 | 0 |

The first witness is the centre word `c_4...c_7=1100`.
For the second, each of the intervals `[2048,3072)` and `[3072,4096)`
contains 513 ones and 511 zeros. Their signed sums coincide and are
nonzero. Hence the normalized energy has exactly no loss in that merge.

These reject a strict contraction asserted at **every** step of every
shell starting with `k=1`. They do not reject an eventual statement with
a later starting scale, and they do not reject (3). The full integer
energy/contrast profiles are saved in the artifact. This is calibration
of a proposed estimate, not new evidence of an asymptotic law.

## 6. Squaring does not repair exact mean closure [U/C; other Rule 30 rows]

The earlier period-14 witness also distinguishes squared future means.
Use the two spatially periodic initial rows

```text
X = (01110010011000)^infinity,
Y = (11001000000100)^infinity.
```

Their complete first-four-step mean fields `Phi_4` coincide. At spatial
coordinate `x=3`, both have `Phi_4=0`, while

```text
Phi_8(X)_3 = 0,
Phi_8(Y)_3 = 1/2.
```

Therefore the squared eight-step mean is also not determined by the
complete first-four-step mean field. Moreover,

```text
||Phi_4(Y)||_infinity = 1/2,
||Phi_8(Y)||_infinity = 3/4.
```

So even the supremum of absolute spatial means can increase on doubling
the time duration in a nonconstant valid Rule 30 diagram.

This does not contradict section 2: `V_j` averages over **all** blocks of
one fixed temporal word, including both halves. `Phi_4` contains only the
first half of the eight-step observation. These statements concern
different data. Neither witness is claimed to lie on the lone-seed orbit,
and neither excludes a suitable upper bound with additional information.

## 7. Rule 90 control [U/C; actual Rule 90 lone seed]

For Rule 90 the lone-seed centre equals 1 at time 0 and 0 thereafter.
Symbolically, odd times cannot reach the centre by parity. At even time
`2m>0` the centre is `binomial(2m,m) mod 2`, which is zero because
`binomial(2m,m)=2 binomial(2m-1,m-1)`.

Thus every shell in this report is the constant sign word `+1`, giving

```text
E_(k,j) = N 2^j,  V_(k,j)=1,  D_(k,j)=0,  G_(k,j)(eta)=0.
```

The algebraic reductions remain valid, but their decay hypotheses fail.
They do not prove the false Rule 90 density assertion. Any future proof
of accumulated loss must use a Rule-30-specific fact beyond the generic
energy identities. The unchanged `controls.rule90_control(Tmax=10)` is
also rerun, with all five cases passing.

## 8. Reproduction and evidence accounting

```sh
uv run python experiments/rule30/p2_ordered_energy_audit.py
```

Code: `experiments/rule30/p2_ordered_energy_audit.py`.
Artifact: `experiments/rule30/p2-ordered-energy-audit.json`.
Artifact SHA-256:
`7c3b26c3b6e90bdc515e87c080d7f187bfe64cdff35d070d14508467241aa79d`.

* **C, universal finite calibration:** all 65,814 sign words of lengths
  1, 2, 4, 8, 16; 328,762 level checks. Recursive energies are checked
  against independently summed intervals. All identities, the squared
  prefix inequality, and the sparse-loss bound for `eta=1/4,1/2,3/4`
  are checked with integers or exact fractions.
* **M/C, seed-specific:** 8,192 centre bits agree between fixed-coordinate
  and expanding-coordinate generators; the first 256 rows are checked
  with scalar frozen-engine gates. Twelve shell profiles are recorded.
* **C, periodic witnesses:** 224 frozen Rule 30 gates replay the two
  eight-step diagrams. Spatial periodicity makes these genuine
  infinite-width configurations, not truncated cones.
* **U/C, Rule 90 seed:** the symbolic control above and 8,192 computed
  bits agree; all twelve shell profiles have zero loss. Five unchanged
  Rule 90 controls pass.

The frozen ladder hash is checked before execution:
`589ab8443e8e61a604561823335d1066eeac5d6b093800a70e8d4a1f943ff96e`.
No frozen engine or terminal-period code is modified.

## 9. Honest scope

The rigorous advance here is an explicit way to tolerate bad scales in
an energy argument, and a correction to any inference that exact
mean-state nonclosure rules out energy inequalities. It is elementary
analytic bookkeeping, not the missing nonlinear estimate.

No positive density bound, Walsh saving, seed-specific sublinear
discrepancy, or claimed solution to P2 follows from the work. No result
is an a.e. theorem, and no generic measure statement is transferred to
the seed. The unresolved point is precisely the seed-specific accumulated
contrast estimate in section 5. It remains unresolved, not proved
impossible by the witnesses above.

# Period-two proof-state capsule

Updated: 2026-09-03

Status: **TOKEN-COMPRESSED SYNTHESIS.  THE NONCONSTANT PERIOD-TWO EXCLUSION
AND P1 REMAIN OPEN.**

This file is the shortest authoritative handoff for the active period-two
work.  It is an index and logical audit, not a source for publication claims.
Use the linked result reports for proofs, controls, and counterexamples.

Evidence labels:

```text
U = uniform all-length proof or identity
R = uniform reduction to a named open statement
C = finite exact certificate or exhaustive census
K = exact counterexample killing the stated mechanism
```

## 1. Exact objective and proof-state DAG

The immediate target is

```text
Tr_0(y) != Tr_0(F^2(y)) for every nonzero finite y.              (PT2)
```

The constant traces are already excluded.  The opposite alternating phase
shifts to `0101...`, so only that phase remains.  The proved reduction chain
is:

```text
(PT2) counterexample
  => alternating Gray/OR frontier with a hard-core endpoint
  => reachable inverse-terminal cut of finite Peel rank
  => rank-zero hard-core endpoint                         [U/R]
  => first infinite shifted cut with tail c^omega,
       c in {2,3}                                        [U/R]
  => endpoint-derived source orbit meets I(HC_omega).    [R, OPEN]
```

For `c in {2,3}`, let `O_c` be the orbit of `c^omega` under finite valid
endpoint shifts, retaining the complete reversed dependency frontier.  The
exact remaining separator is

```text
O_c intersect I(HC_omega) = empty,  c=2,3.                       (SEP)
```

Proving `(SEP)` closes `(PT2)`, but not arbitrary periods and not full P1.

Three later targets must not be confused with `(SEP)`:

```text
arbitrary normalized queue mortality  => SEP              stronger
binary-wedge horizon BWH+              => DLP => SEP       stronger
rotated wedge RW                       <=> DLP              equivalent
```

Thus a counterexample to arbitrary-queue mortality or `BWH+` need not refute
period-two exclusion.

## 2. Smallest sufficient statements

### DLP / rotated wedge

For `n>=1`, `r in {0,1,2}`, and `c in {2,3}`, DLP is equivalent to excluding
a binary word `f` of length `2n+r+2` such that

```text
f[n:] is hard-core across the junction,
f[-3:-1] = 12,
P^n(I(f)) = c^(n+r+2).                                           (RW)
```

The suffix condition `12a` is the nonfinal pull.  DLP is currently the
weakest explicit finite-word statement known to imply `(SEP)`.  It has no
failure in the complete hard-core corpus through length 23, all binary
sources through length 20, or the recorded long falsifiers `[C]`; it has no
all-length proof.

### Binary-wedge horizon and deterministic defect

The cleaner but stronger target is

```text
no binary f of length 2n+2 has P^n(I(f))=c^(n+2), n>=7.          (BWH+)
```

The finitely many smaller lengths are exactly decidable.  `(BWH+)` implies
DLP because a DLP witness supplies at least `n+2` binary continuation
symbols.  Its exact census has no failure through `n=20` `[C]`.

The high-bit constraint in `(BWH+)` is solved uniformly.  For each binary
source `W in {1,2}^n`, affine `D8` triangularity uniquely determines a binary
continuation `Q_n(W)` of length `n+2` making every cell of
`G_n=P^n o I` have high bit one.  Define

```text
Psi_n(W)_j = 1 + H(G_n(W Q_n(W))_j) + L(G_n(W Q_n(W))_j).
```

Then `(BWH+)` is exactly

```text
Psi_n(W) is neither 0^(n+2) nor 1^(n+2).                         (PSI)
```

There are no free suffix variables left.  `(PSI)` is the cleanest current
all-length algebraic target.

The originally preregistered sharper bound is false `[K]`:

```text
n=15, c=3, W=111122211212112,
Q=12211111122111211,
G_15(WQ)=33333333333333332,
Psi_15(W)=11111111111111110.
```

It saturates the repaired `n+1` horizon and then fails; it does not falsify
`(BWH+)`.  The word contains `11`, so it is outside the original hard-core
scale domain.

## 3. One local kernel in several coordinate systems

The apparently separate carry, Peel, queue, frontier, and affine approaches
are curries or rotations of the same four-state inverse-cone rule `phi`.
This is the main archive-wide correlation.

For state `q=(H,L)`, put `E=1+H+L`.  Binary endpoint symbols `{1,2}` have
`E=0`; equality symbols `{0,3}` have `E=1`.  The complete local rule is

```text
H(phi) = H_R + 1 + E_L + E_L H_L,
E(phi) = E_R + H_R(H_L + E_L).                                  (1)
```

The boundary action is `(H,E)->(1+H,E)`.  Fixing the queue input in `phi`
gives the eight affine `D8` permutations

```text
(h,l) -> (h+alpha, l+beta*h+gamma),
```

while fixing the Peel output gives the 13-element inverse-lift monoid with
only one- and two-cycles.  Consequences already proved uniformly:

- a new frontier coordinate is transported reversibly, not contracted;
- strict period doublings cannot occur on consecutive endpoint shifts;
- the carry/phase cannot be discarded from an induction;
- high-bit continuation is uniquely eliminable, leaving only `Psi`;
- binary source legality is exactly the zero-defect condition `E=0`.

This identifies the likely proof object: an ordered ancestry of the `E`
defect with its `D8` phase, not another scalar count.

## 4. Uniform theorem kernel worth reusing

| Result | Level | Reusable conclusion |
|---|---:|---|
| Gray/OR macro and four-state carry | `U` | Exact alternating frontier; actions generate `D8` |
| Actual-right constraints | `U` | The real endpoint avoids `11` and `00000` |
| Dyadic exceptional-family separator | `U` | Reachable zero-ray cuts are never eventually `(12)^omega`; eventually-`2` endpoints are excluded |
| Rotated Peel identity | `U` | `P(I(sigma e))=sigma^2 I(e)` with exact rank drift |
| Peel lift monoid | `U` | Exact doubling language; no consecutive strict doublings |
| Rank descent | `U/R` | Every positive finite rank reduces to rank zero |
| First-infinite shift | `U/R` | Only tails `2^omega` and `3^omega` remain |
| Endpoint event grammar | `U` | Off the singleton credit: `A=21`, `B=22`, `C=12`; finitely many pulls means eventually `2` |
| Queue/frontier construction | `U/R` | Exact endpoint-derived inverse system and target `(SEP)` |
| High-bit elimination | `U/R` | `BWH+` reduces exactly to deterministic one-bit `(PSI)` |
| Endpoint restart fiber | `U/R` | Exact mod-four restart and a pure-period-32 five-symbol quotient eliminate the extremal gap; successive zero-tail endpoint defects satisfy `k_(i+1)<=2k_i` |

## 5. Killed mechanism classes: do not rename and retry

| Lost information / mechanism | Exact obstruction |
|---|---|
| Fixed-radius additive energy | Farkas contradictions for localities 1--4; radius-seven negative cycles |
| Fixed finite quotient of the frontier | Same summary with different legal successors; carry actions are permutations |
| Raw dyadic period mismatch | `2^omega` maps to accepted `(12)^omega`; reachability is essential |
| Bare holonomy-defect word | Anchored identical profiles have different next rows at length 8; two-ended repair fails at 13 |
| Fixed queue end windows plus total phase | For every radius, the neutral interior blocks `00` and `11` give equal length, end windows, endpoint/event data, and total `D8` action but unequal successor actions |
| Static formula/DFA rank contraction | Survivor DFA size expands as `4^(h+1)+1` through the checked range |
| Literal final local patch | A hard-core length-12 DLP control survives with six constant final cut cells |
| One backward source defect | Single-coordinate four-state relaxations usually remain UNSAT; the obstruction is branched/global |
| Count pulls by initial endpoint `12` | Endpoint `22222222` has no `12` but its exact event word is `AC` |
| Count arbitrary-queue pivots/features | `3001 0^382 2` reaches pull depth 3; `3001 0^390 2` reaches depth 4 |
| Pointwise scale derivative/matching | Exact failure first appears at length 21 |
| Sharp binary-wedge bound `M_c(n)<=n` | `M_3(15)=16` witness displayed above |
| Static right-boundary penetration | Structured information reaches only `O(log t)` depth while the center is `Theta(t)` away |
| Larger bounded SAT/GA tables | They falsify candidates but cannot supply the missing all-length quantifier |
| Single-source-flip injection between RW survivor levels | A flip at any depth but the first three source symbols is a fresh coin on every forced level (`0.4^j` alive at level `j`, flat in the flip position); coverage decays like `0.4^j`, the nearest partner sits at depth `n-1`, and per-level halving is itself false at deep levels (`99 -> 54 -> 28 -> 18`, `n=16`).  `RESULTS-FLIP-PAIRING.md` |
| Exact symbol congruence on the retained state | `CONE[1] == CONE[3]`, so the append factors through `q: 3 -> 1`.  A true congruence, but a 5.7 percent constant-factor collapse: base `1.7671` against `1.7681` at `u=19`.  `RESULTS-COLUMN-DECOMPOSITION.md` 1a |
| Counting the RW levels by `F_2` rank | Branch survivor sets are not affine subspaces: 420 of 516 classes fail, and all 96 that pass have size 4 or 8.  The carry action contains an `OR`.  `RESULTS-COLUMN-DECOMPOSITION.md` 1b |
| Induction on single-position column richness | 99.3 percent of merging parents have IDENTICAL columns and differ only in the diagonal; the merge mechanism is diagonal collapse, not column variation.  `RESULTS-COLUMN-DECOMPOSITION.md` 2 |
| Column memory as a rate mechanism for RW | The `ceil((L+1)/2)` law is proved, but the column is not a sufficient statistic for survival: from `n=10` every column class contains sources with different RW death levels (spread to 10 levels), and the least augmentation restoring uniformity is the entire diagonal (`t=n`).  `RESULTS-COLUMN-DECOMPOSITION.md` 10 |
| Conditional block contraction at any exact prefix state | A uniform per-state contraction exists at each fixed `n` and `p`, but the rate DECREASES monotonically with conditioning depth (`1.121` at `p=2` to `0.231` at `p=16`, `n=17..19`) and with `n`, against the `1.0` bits per level `(RW-alpha)` needs.  The only depths clearing `1.0` have 4 and 8 states and are the aggregate in disguise.  `RESULTS-CONDITIONAL-BLOCK-LOSS.md` 4, 4b, 4c |
| Any symbol quotient of the anti-diagonal | Exhaustive over all 15 partitions of the four-state alphabet: zero nontrivial full congruences.  Only one-sided closures exist (`CONE[1]==CONE[3]` on the driving word; the high bit on the trajectory), neither of which compresses.  `RESULTS-DIAGONAL-MEMORY.md` 8 |
| Additive position-indexed weight on the anti-diagonal (subinvariant / Lyapunov certificate) | `t = 0` on the RW survivor edges for every window size through the full diagonal length, `n = 10..15`, both `c`, with exact integer Farkas certificates; the `K = 0` core is one survivor edge whose symbol counts move by `(1,0,0,0)`.  Relaxing to signed coefficients bounded below only on the survivor sublanguage is feasible, but its unique feasible direction is the diagonal LENGTH, whose `alpha_hat` equals the observed longest run over `n` in all ten cells; excluding that one direction restores `t = 0`.  `RESULTS-SUBINVARIANT-CERTIFICATE.md` |

All these failures have the same cause: a growing ordered dependency diagonal
stores phase in long gaps.  A bounded annotation loses it; a complete state
transports it reversibly and grows.

## 6. Cross-analysis: combinations that genuinely fit

1. **Peel plus source reachability.**  Dyadicity alone failed, but dyadicity
   plus the zero-ray source orbit proved the exceptional-family separator.
   This is the model successful hybrid: add a load-bearing hypothesis.

2. **Scale placement plus endpoint events.**  An absolute pull at
   `m=3n+r` is placed at row `n+r` of the block `e[n:2n]`.  This is why only
   the three DLP rows matter; earlier survival rows are dispensable.

3. **High-bit elimination plus source defect.**  Affine `D8` transport
   uniquely fixes `Q_n(W)`, while (1) identifies binary legality as `E=0`.
   The remaining obstruction is exactly whether the forced output `E` word
   can be constant.  This joins the former affine and CNF/source-core routes
   without retaining their existential variables.

4. **Pull ancestry plus ordered zero-prefix tokens.**  Any finite bound on
   one pull-chain depth suffices; the former sharp half-density bound is
   unnecessary.  A phase-decorated injection into the `n` ordered source
   tokens would close `(SEP)`.

5. **Actual-right constraints only after finite prefixes.**  Rank descent
   prepends artificial endpoint `2`s, so conditioning the entire endpoint on
   actual-right realizability is unsound.  Scale blocking moves beyond that
   prefix and is the compatible place to use exact right-cone information.

6. **Period-three equality-subgraph ranking is a transferable method, not a
   transferable invariant.**  The `011` zero-tail dual has an all-length
   lexicographically nonincreasing trigram-count vector, proved by restricting
   an exact weighted graph successively to equality edges.  This suggests the
   correct workflow for a second component after a genuine nonincrease law is
   known.  It does not apply directly to `Psi`: the period-two sequential
   residual state has not been reduced to a fixed graph.  Deriving that exact
   graph or seam law is a prerequisite, not a technicality.

7. **Craig sections plus the zero-cut fiber retain boundary phase exactly.**
   The endpoint morph has exact leading-`0` and leading-`2` sections, giving
   `12 -> 03 -> 10 -> 00 -> 12`.  In the sole phase that could attain the
   old gap bound, injectivity and row-permutativity force the entire residual
   to `T(2^omega)`.  Its five-symbol moving-tail quotient is purely periodic
   with period 32 and has no hard-core favorable state.  Hence a hypothetical
   rank-zero endpoint obeys `k_(i+1)<=2k_i`, not merely `2k_i+2`.  This is an
   exact adaptive finite quotient that works because its fiber is fixed; it
   does not justify a bounded quotient for the unrestricted growing queue.

## 7. Next proof program

Do not extend the horizon census.  Derive an exact composition/ancestry law
for the deterministic pair

```text
W -> (Q_n(W), Psi_n(W)).
```

The first target is a recursion for adjacent output defects

```text
Delta_j(W)=Psi_n(W)_j + Psi_n(W)_(j+1).
```

`(PSI)` is equivalent to `Delta(W)` containing a `1`.  A useful recursion
must retain the entering affine `D8` phase and an ordered source interval;
without those data the closure counterexamples in Section 5 apply.  Test the
derived seam law on the existing exhaustive corpus, but the deliverable must
be a symbolic two-branch induction.

If the complete-state recursion necessarily fans out, weaken immediately to
RW/DLP and retain its two facts discarded by `BWH+`: the hard-core suffix and
the terminal `12a` pull.  The proof target then becomes a forced adjacent
`E` change only at rows `n,n+1,n+2`, not for every arbitrary binary source.

An independent rank-zero continuation is to extend the exact moving-tail
quotient of `RESULTS-ENDPOINT-RESTART-COCYCLE.md` from the eliminated equality
fiber to a scale-sensitive band below equality.  A useful extension must
improve the factor `2`, not merely subtract another fixed constant; otherwise
a doubling sequence remains possible.

## 8. Minimal reading order

1. This file.
2. `RESULTS-BINARY-WEDGE-HIGH-ELIMINATION.md`.
3. `RESULTS-DLP-ROTATED-WEDGE.md`.
4. `RESULTS-LATE-PULL-DIAGONAL.md`.
5. `RESULTS-ENDPOINT-RESTART-COCYCLE.md` for the sharpest direct rank-zero
   gap theorem.
6. Read `RESULTS-ROTATED-PEEL-IDENTITY.md` and
   `RESULTS-RANK-ZERO-REDUCTION.md` only when auditing the implication back
   to period two.
7. Use `README.md` or `docs/rule30/EXPERIMENT-ATLAS.md` only to investigate a
   collision with older work.

This order replaces the chronological 800-line continuation prompt for
ordinary resumption.

# Proof of the lemma `retained-bit-form`, parts (a) to (e)

Date: 2026-09-03.  Proof style: structural-inductive.

Status: **PROVED, all five parts.**  Every step is one of: a finite exhaustive
check with script and log in this directory (three facts, F1 to F3, in
section 1); a derivation written out in full.  No step cites a numerical
verification as evidence; the exhaustive runs in section 8 are gates on the
derivation, not the proof.

The lemma is an identity between adjacent columns of the four-state kernel of
`uc/BRIEF.md` section 2.  It implies none of `(RW-alpha)`, `(RW)`, `(SEP)`,
`(PT2)`, P1, and it does not claim to.  What it establishes is a set of exact
coordinates for the forced column map: the forced symbol, the `H` profile, the
`E` pin, the zero pattern of the next column and the bits the map forgets.

Script and logs (all in this directory):

- `rbf_structural_checks.py`, the finite checks S1 to S6 described in section 8;
- `rbf_structural_checks.log`, run with `--ub 12 --u4 6 --m 10`, 9 s;
- `rbf_structural_checks_u14_m12.log`, run with `--ub 14 --u4 7 --m 12`, 58 s;
- `rbf_structural_mutate.log`, the control run with `--mutate` (retained
  redefined as odd-indexed), which fires at the first word:
  `AssertionError: ('b', (1,), 1, -1)`.

Run from the work directory:

```sh
cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant
uv run python uc/r1-quadratic-prove-retained-bit-form-structural/rbf_structural_checks.py --ub 12 --u4 6 --m 10
```

## 0. Objects and conventions

### 0.1 The kernel

Cells are `T in {0,1,2,3}` with `H(T) = T >> 1`, `Lo(T) = T & 1` and the
defect `E(T) = 1 + H(T) + Lo(T)  (mod 2)`.  So `E(1) = E(2) = 0` and
`E(0) = E(3) = 1`.  The local rule is `phi(l, r) = CONE[l][r]` of
`psi_kernel.py`.

The triangle (BRIEF section 2, taken as the definition).  For an endpoint word
`e_0, e_1, ..., e_{L-1}` in `{0..3}^L`, cells `T[u][d]` for `0 <= u < L` and
`d in [-u-1, u]` are

```text
    T[u][-u-1] = e_u
    T[u][-u]   = e_u XOR 3
    T[u][d]    = phi(T[u-1][d-1], T[u][d-1])        for -u < d <= u.
```

Column `u` has cells at depths `-u-1, ..., u`.  For `-u < d <= u` the left
parent `T[u-1][d-1]` has `d-1 in [-u, u-1]`, which is column `u-1`'s full
range, so the recurrence is well formed.  Fact F3 (section 1) checks that
`psi_kernel.Endpoint` produces exactly this array.

Letters of a cell: `a(T) = [T == 0]`, `b(T) = [Lo(T) == 0]`.  The table is
`T = 0: (1,1)`, `T = 1: (0,0)`, `T = 2: (0,1)`, `T = 3: (0,0)`.  The quotient
letter of a cell is one of three: `0` (the cell is zero), `2` (the cell equals
2), `x` (the cell is odd, 1 or 3).  The even-bit of a nonzero cell is
`w(T) = [T == 2]`.

### 0.2 The window and its ordered object

Fix `n >= 1` and a binary word `e_0 ... e_{u-1} in {1,2}^u` with `u >= n`.
Column `u-1` exists on `[-u, u-1]`; its **window** is the depth interval
`[-u, n-1]`, of length `m = n + u`, with cells `T[u-1][d]`.  The condition
`u >= n` is exactly what makes `n-1 <= u-1`, so the window lies inside the
column.  The bottom window cell is `T[u-1][-u] = e_{u-1}`, which is binary,
hence nonzero.

Write `Z` for the set of zero cells of the window, `N` for the set of nonzero
cells, `W2` for the cells equal to `2`; `|Z| + |N| = m`.  Let
`q_1 > q_2 > ... > q_{|N|}` be the nonzero cells listed from the top; then
`q_{|N|} = -u`.

**Block decomposition.**  `B_0` is the set of the `z_0 >= 0` zero cells above
`q_1`, i.e. depths in `(q_1, n-1]`.  For `1 <= i <= |N|`, `B_i` consists of
`q_i` together with the `z_i >= 0` zero cells directly below it, i.e. depths
in `(q_{i+1}, q_i]`, where `q_{|N|+1} := -u-1`.  The blocks
`B_0, B_1, ..., B_{|N|}` partition the window from the top, each is a
contiguous depth interval, `B_0` may be empty, and `z_{|N|} = 0`.  Write
`w_i = [T[u-1][q_i] == 2]` for the even-bit of the head of `B_i`.

**Retained.**  A cell is *retained* iff it lies in `B_0` or in `B_i` with `i`
even, and *non-retained* iff it lies in `B_i` with `i` odd.  This is the
lemma's definition: `q_i` is the head of `B_i`; a zero cell's nearest nonzero
cell above it is the head of its block; a zero cell with no nonzero cell above
it lies in `B_0`.

**Runs.**  Since the blocks alternate in parity and `B_0` is retained, the
maximal runs of non-retained cells are exactly the odd blocks
`R_k := B_{2k+1}`, `k = 0, ..., K-1`, `K = ceil(|N|/2)`, listed from the top.
The retained zeros are the zeros of `B_0` and of the even blocks:
`|Z_ret| = z_0 + sum_{i even, 2 <= i <= |N|} z_i`.

`c in {2,3}` does not enter (a) to (e): it selects the hit condition
`E(T[u][n]) = E(c)` and nothing below reads it.

### 0.3 Column `u` on `[-u-1, n]`

`T[u][-u-1] = e_u`, `T[u][-u] = e_u XOR 3`, and for `-u < d <= n` the cell
`T[u][d]` reads `T[u-1][d-1]` with `d-1 in [-u, n-1]`, a window cell.  So
column `u` on `[-u-1, n]` is a function of `e_u` and the window alone.  Write
`H_u(d) = H(T[u][d])`, `E_u(d) = E(T[u][d])`.  Because `E = 1 + H + Lo`, a
cell is recovered from `(H, E)` as `T = 2H + (1 + H + E mod 2)`, and

```text
    T[u][d] = 0   iff   H_u(d) = 0 and E_u(d) = 1.                        (0.1)
```

### 0.4 What is inducted on

Within a column: the state `(H_u(d), E_u(d))` as `d` increases from `-u`, with
the invariant of section 5 expressed on the ordered object of 0.2 (the block
decomposition read from the top).  Column to column: the block decomposition
of column `u`'s window is obtained from that of column `u-1`'s window
(section 6, D1), and the closure is D4: the forced future is a second-order
recursion on zero patterns.

## 1. The three finite facts

Each is an exhaustive computation in `rbf_structural_checks.py`; the counts
are in both logs.

**F1 (decoupling), check S1, all 16 pairs `(l, r)`.**

```text
    H(phi(l, r)) = H(r) + 1 + a(l)          (mod 2)
    E(phi(l, r)) = E(r) + H(r) * b(l)       (mod 2)
```

This is BRIEF section 2's decoupling, rechecked here so the proof cites its
own log.

**F2 (boundary), check S2, all 4 symbols `s`.**  `BOUNDARY[s] = s XOR 3`,
`phi(3, s) = s XOR 3` (so the wedge edge is the rule with virtual left parent
`3`), `H(s XOR 3) = 1 + H(s)`, `E(s XOR 3) = E(s)`; and for `s in {1,2}`,
`E(s) = E(s XOR 3) = 0`.

**F3 (kernel = triangle), check S3.**  For every binary word of length
`u <= 14` and every four-state word of length `u <= 7` (54,610 words,
`rbf_structural_checks_u14_m12.log`), the arrays `column` and `diagonal` of
`psi_kernel.Endpoint` after each append equal the triangle of 0.1
(`column[i] = T[u][-i]`, `diagonal[k] = T[u][k]`).  F3 ties the object of the
lemma to the kernel code.  Nothing in sections 2 to 7 uses it.

## 2. The two column integrals

**Lemma H.**  For any prefix `e_0 ... e_{u-1} in {0..3}^u`, any
`e_u in {0..3}`, and every `d in [-u, u]`,

```text
    H_u(d) = H(e_u) + (d + u + 1) + #{d' in [-u, d) : T[u-1][d'] = 0}     (mod 2).
```

*Proof, by induction on `d`.*  Base `d = -u`: `H_u(-u) = H(e_u XOR 3)
= 1 + H(e_u)` by F2, and the right side is `H(e_u) + 1 + 0`.  Step
`d -> d+1` for `-u <= d < u`: `T[u][d+1] = phi(T[u-1][d], T[u][d])`, so by F1
`H_u(d+1) = H_u(d) + 1 + a(T[u-1][d])`, and the right side increases by
exactly `1 + [T[u-1][d] = 0]`.  QED.

**Lemma E.**  Under the same hypotheses, for every `d in [-u, u]`,

```text
    E_u(d) = E(e_u) + #{d' in [-u, d) : H_u(d') = 1 and Lo(T[u-1][d']) = 0}   (mod 2).
```

*Proof, by induction on `d`.*  Base: `E_u(-u) = E(e_u XOR 3) = E(e_u)` by F2.
Step: `E_u(d+1) = E_u(d) + H_u(d) * b(T[u-1][d])` by F1, and `b = 1` iff
`Lo = 0`.  QED.

For binary `e_u` the constant in Lemma E is `0` (F2).  These are the `(H)` and
`(E)` integrals of BRIEF section 2, now derived rather than verified; check
S4 confirms both on 4,791,416 cells, all four values of `e_u`, whole columns.

## 3. Forcing, and part (a)

**Proposition A.**  For a binary prefix and `1 <= n <= u`, exactly one
`e_u in {1,2}` gives `H(T[u][n]) = 1`, and it satisfies

```text
    H(e_u) = |N|  (mod 2),      i.e.   e_u = 2  iff  |N| is odd.
```

*Proof.*  Lemma H at `d = n`: `H_u(n) = H(e_u) + (n + u + 1) + |Z|`, and
`|Z|` is a property of column `u-1` alone.  Since `H(1) = 0` and `H(2) = 1`,
the map `e_u -> H_u(n)` is a bijection `{1,2} -> {0,1}`; so exactly one binary
symbol gives `H_u(n) = 1`, and it has
`H(e_u) = 1 + (n+u+1) + |Z| = (n+u) + |Z| = m + |Z| = |N| + 2|Z| = |N|`
(mod 2), using `m = |Z| + |N|`.  QED.

This is (a).  Two rereadings: the hard-core condition `e_u = 1` is
`|Z| = n + u (mod 2)`, and BRIEF section 3's H-forcing line
`H(e_u) = 1 + (n+u+1) + |Z|` is Lemma H at `d = n`.  From now on `e_u` denotes
the forced symbol.

## 4. Lemma M: the column is a Moore run with forced start

Define the step `step(h, F, a, b) = (h + 1 + a, F + h b)` (mod 2), the
transducer of BRIEF section 2.

**Lemma M.**  Read the window letters `(a_d, b_d) = (a(T[u-1][d]),
b(T[u-1][d]))` for `d = -u, ..., n-1` in increasing `d`, starting from
`(h, F) = (1 + |N| mod 2, 0)`.  The state after reading the letters at depths
below `d` equals `(H_u(d), E_u(d))`, for every `d in [-u, n]`.

*Proof.*  Start: `H_u(-u) = 1 + H(e_u) = 1 + |N|` by F2 and Proposition A;
`E_u(-u) = E(e_u XOR 3) = 0` by F2.  Step: F1.  QED.

**Definition (letter space).**  For a word `q = (q_0, ..., q_{m-1})` in
`{0, 2, x}^m`, index `j` standing at depth `d = -u + j` (so `q_0` is the
bottom), let `|N| = #{j : q_j != 0}`, put `(h_0, F_0) = (1 + |N| mod 2, 0)`,
`(h_{j+1}, F_{j+1}) = step(h_j, F_j, a(q_j), b(q_j))`, and

```text
    Phi(q) := F_m.
```

`h_j` is the H-profile of `q`.  By Lemma M, for the letter word of a realised
window, `h_j = H_u(-u+j)`, `F_j = E_u(-u+j)` and `Phi(q) = E(T[u][n])`.  The
letter space is strictly larger than the set of realised windows (a realised
window never has `q_0 = 0`, and its letters are constrained by the earlier
columns); sections 5 and 7 are proved on the whole letter space and
specialise.  The block decomposition, `z_i`, `w_i`, retained and the runs
`R_k` are defined for letter words verbatim as in 0.2, with `q_{|N|+1} := -1`
in index terms; the one new case is `|N| = 0`, where `B_0` is the whole word.

## 5. The H-profile and part (b); the pin and part (c)

**Proposition B (H-profile).**  For every letter word with forced start and
every `0 <= j <= m`,

```text
    h_j = 1 + #{i >= j : q_i != 0}     (mod 2).
```

*Proof.*  From the step, `h_{j+1} = h_j + 1 + a(q_j) = h_j + [q_j != 0]`, so
`h_j = h_0 + #{i < j : q_i != 0} = 1 + |N| + #{i < j : q_i != 0}
= 1 + #{i >= j : q_i != 0}` (mod 2), using
`|N| = #{i < j : q_i != 0} + #{i >= j : q_i != 0}`.  QED.

At `j = m` this reads `h_m = 1`: the forced start is exactly the start that
makes the final `h` equal to `1`, which is the meaning of "forced" in the
lemma's statement of (e).

**Corollary (b).**  `h(d) = 1` iff the cell at depth `d` is retained.

*Proof.*  If `d` lies in `B_i` with `i >= 1`, the nonzero cells at or above
`d` are exactly `q_1, ..., q_i` (the head `q_i` is at or above `d` and
`q_{i+1}` lies below `B_i`), so `h(d) = 1 + i`, which is `1` iff `i` is even.
If `d` lies in `B_0` there is no nonzero cell at or above `d` and `h(d) = 1`.
Retained means "in `B_0` or in an even block".  QED.

For a realised window, Lemma M turns this into part (b):
`H(T[u][d]) = 1` iff cell `d` of column `u-1` is retained, for all
`d in [-u, n-1]`; and `H(T[u][n]) = 1` is the pin.

**Proposition C (the pin).**  For every letter word with forced start,

```text
    Phi(q) = #{j : q_j in {0, 2} and cell j retained}
           = |Z_ret| + sum_{i even, 2 <= i <= |N|} w_i
           = z_0 + sum_{i even, 2 <= i <= |N|} (z_i + w_i)        (mod 2).
```

*Proof.*  From the step, `F_{j+1} = F_j + h_j b(q_j)` with `F_0 = 0`, so
`F_m = sum_j h_j b(q_j)`.  Now `b(q_j) = 1` iff `q_j in {0, 2}`, and by
Corollary (b) `h_j = 1` iff cell `j` is retained.  The retained cells with
letter in `{0, 2}` are the retained zeros (the `z_0` zeros of `B_0` and the
`z_i` zeros of each even block) and the heads `q_i` of even blocks with
`w_i = 1`.  QED.

For a realised window this is part (c):
`E(T[u][n]) = #(retained zero cells) + #{i even : T[u-1][q_i] = 2}` (mod 2).
Given the zero pattern of the window, which fixes the blocks and all `z_i`,
the map `(w_2, w_4, ...) -> E(T[u][n])` is the affine functional with
all-ones linear part and constant term `|Z_ret|`, as the lemma states.

**Corollary C' (the set form of BRIEF section 3, derived).**  For a realised
window,

```text
    E(T[u][n]) = (|Z| + |W2|) (1 + m + |Z|) + #{(x, y) : x < y, x in N, y in Z or W2}   (mod 2).
```

*Proof.*  `E_u(n) = sum_{y in Z or W2} h(y)` (Proposition C, first line, with
`h(y) = 1` iff retained).  By Proposition B, `h(y) = 1 + #{x in N : x >= y}
= 1 + |N| + #{x in N : x < y}`.  Summing over the `|Z| + |W2|` cells `y`
gives `(|Z| + |W2|)(1 + |N|) + #{(x, y) : x in N, y in Z or W2, x < y}`, and
`1 + |N| = 1 + m + |Z|` (mod 2).  QED.

BRIEF section 3 records this set form (and the equivalent primed quadratic
form `beta (1 + alpha') + gamma'`, with `alpha' = |N|`, `beta = |Z| + |W2|`,
`gamma'` the pair count) as verified on 131,580 checks; it is now a
derivation.  With `H(e_u) = |N|`, the quadratic term equals `beta [e_u = 1]`,
which is the affine-given-the-symbol form of `RESULTS-RW-LINEAR-SLACK.md`
section 9.5.  Check S5 compares the retained-bit value against an independent
coding of the set form on every column.

## 6. The zero pattern of column `u`, and part (d)

Now a realised window (binary prefix) and column `u` on `[-u-1, n]`.  By
Lemma M and Proposition C, for every `d in [-u, n]`,

```text
    E_u(d) = #{retained cells d' < d of the window with T[u-1][d'] in {0, 2}}.   (6.1)
```

**Proposition D1 (transport of the block structure).**

1. `T[u][-u-1] = e_u != 0`.
2. Every retained cell `d` of the window has `T[u][d] != 0`.
3. On each run `R_k = B_{2k+1}`, `E_u` is constant; call its value `F_k`.
4. The zero set `Z_u` of column `u` on `[-u-1, n-1]` is the union of the runs
   `R_k` with `F_k = 1`.  So the nonzero cells of column `u` on `[-u-1, n-1]`
   are `{-u-1}`, the retained cells of the window, and the runs with
   `F_k = 0`.
5. `F_k = sum_{j > k, 2j <= |N|} (z_{2j} + w_{2j})` (mod 2), an empty sum
   being `0`.  In particular `F_{K-1} = 0` when `|N|` is odd, and we set
   `F_K := 0`.

*Proof.*  (1) `e_u` is binary.  (2) Retained gives `H_u(d) = 1` by (b), so
`T[u][d] != 0`.  (3) For `d' < d` both in `R_k`, (6.1) gives
`E_u(d) - E_u(d') = #{retained cells in [d', d) with letter in {0,2}}`; the
interval `[d', d)` lies inside the contiguous run `R_k`, all of whose cells
are non-retained, so the difference is `0`.  (4) By (0.1) a window cell is
zero in column `u` iff `H_u = 0` and `E_u = 1`, iff (by (b)) it is
non-retained and `E_u = 1`, iff it lies in some `R_k` and `F_k = 1`; by (3)
this holds for all of `R_k` or for none of it.  Together with (1) this is the
claim.  (5) The cells below `R_k = B_{2k+1}` are the blocks
`B_{2k+2}, ..., B_{|N|}`.  Among them the retained cells with letter in
`{0, 2}` are, for each even block `B_{2j}` (`j > k`, `2j <= |N|`), its
`z_{2j}` zeros and its head if `w_{2j} = 1`; the odd blocks are non-retained
and contribute nothing; and the cells of `R_k` itself below a given
`d in R_k` are non-retained.  So (6.1) gives the stated sum.  When `|N|` is
odd, `R_{K-1} = B_{|N|} = {-u}` is the last block, the sum is empty, and
indeed `T[u][-u] = e_u XOR 3 != 0`.  QED.

Part (d), first clause: `Z_u` is a union of complete maximal runs of
non-retained cells of column `u-1`.  That is D1(4).

**Proposition D2 (read-out of the even bits).**  For every even
`i = 2k + 2 <= |N|`,

```text
    w_i = F_k + F_{k+1} + z_i     (mod 2),       with F_K = 0.
```

*Proof.*  By D1(5), `F_k + F_{k+1} = z_{2k+2} + w_{2k+2}`: the two sums
differ in exactly the term `j = k + 1`.  When `2k + 2 = |N|` (so
`k + 1 = K`), `F_k` is the single term `z_{|N|} + w_{|N|}` and `F_K = 0`
matches the empty sum.  QED.

Each `F_k` is read from `Z_u` by D1(4): `F_k = [R_k subset of Z_u]`.  The
runs `R_k` and the counts `z_i` are read from the zero pattern `Z_{u-1}` of
the window.  So `(Z_{u-1}, Z_u)` determines `w_i` for every even `i`; this is
the lemma's "it determines every `w_i` with `i` even", and the explicit
formula is the one in the lemma's derivation with `E_u(run above) = F_k`,
`E_u(run below) = F_{k+1}` and the retained zeros between the two runs being
the `z_i` zeros of the even block `B_i`.

**Proposition D3 (the pair determines column `u` on `[-u-1, n]`).**
`T[u][-u-1] = e_u = 1 + [|N| odd]` with `|N| = m - |Z_{u-1}|` (Proposition A).
For `d in [-u, n]`: `H_u(d) = [d retained]` for `d < n` and `H_u(n) = 1`
(Corollary (b)); `E_u(d) = #{retained zeros below d} + sum_{i even, q_i < d}
w_i` by (6.1), all determined by `Z_{u-1}` and the even `w_i`; and
`T[u][d] = 2 H_u(d) + (1 + H_u(d) + E_u(d) mod 2)`.  QED.

**Proposition D4 (the forced future).**  Define the forced orbit from column
`u`: for `u' >= u`, `e_{u'+1}` is the unique binary symbol with
`H(T[u'+1][n]) = 1`, and column `u'+1` is read on `[-u'-2, n]`.  Then column
`u` on `[-u-1, n-1]` determines, for every `u' > u`, the symbol `e_{u'}`, the
column `u'` on `[-u'-1, n]`, and the hit `E(T[u'][n])`.

*Proof, by induction on `u'`.*  Column `u'` on `[-u'-1, n-1]` is the window
of column `u'+1` (0.2 with `u` replaced by `u'+1`; the bottom cell
`T[u'][-u'-1] = e_{u'}` is binary).  It determines `e_{u'+1}` by
Proposition A (existence and uniqueness included), and then column `u'+1` on
`[-u'-2, n]` by 0.3.  QED.

Combining D3 and D4: `(Z_{u-1}, Z_u)` determines column `u` on `[-u-1, n]`
and the whole forced future.  In particular the zero set `Z_{u+1}` of column
`u+1` on `[-u-2, n-1]` is a function `Psi(Z_{u-1}, Z_u)`, computed by D3 and
then D1(4) applied to column `u`'s window; the forced zero-pattern sequence is
a second-order recursion, and by Proposition A and Proposition C it carries
every forced symbol and every hit.

**Proposition D5 (the odd-indexed even-bits are not read).**  Consider the
map from the window of column `u-1` to `(e_u, column u on [-u-1, u])`.
Toggling the even-bit of `q_i` means replacing `T[u-1][q_i]` by a nonzero
cell with the opposite value of `[T = 2]` (`2 -> 1` or `2 -> 3`; `1 -> 2`;
`3 -> 2`).  This changes no `a`-letter and changes `b` at `q_i` only.

1. If `i` is odd, `e_u` and the whole of column `u` on `[-u-1, u]` are
   unchanged.
2. If `i` is even, `T[u][d]` changes for every `d in (q_i, n]`, in particular
   `T[u][n]`.

*Proof.*  `e_u` depends only on `|N|` (Proposition A), unchanged.  For
`d in [-u, n]`, `H_u(d)` depends only on the zero pattern (Proposition B),
unchanged.  By Lemma M, `E_u(d) = sum_{d' < d} h(d') b(d')`, which changes by
`h(q_i)` for every `d > q_i` and not at all for `d <= q_i`; and
`h(q_i) = [i even]` by Corollary (b).  So for `i` odd nothing in column `u`
on `[-u-1, n]` changes, and for `i` even `E_u(d)` flips for all
`d in (q_i, n]` while `H_u(d)` is fixed, which changes the cell.  Above `n`,
`T[u][d]` for `d > n` is computed by the recurrence from `T[u][n]` and the
cells `T[u-1][d']` with `d' >= n`, outside the window; so for `i` odd the
whole column `u` is unchanged.  QED.

If the top window cell `T[u-1][n-1]` is nonzero it is `q_1`, index `1`, odd:
its even-bit is never read.  This completes part (d).

*Remark.*  D5 is the exact reason the single pattern `Z_{u-1}` does not
determine column `u`: its fibre is parametrised by the odd-indexed even-bits
that the map discards (up to `ceil(|N|/2)` of them, which is why the fibres
grow with `n` in the screening logs), while D2 says the pair `(Z_{u-1}, Z_u)`
recovers the even-indexed ones, and D3 says nothing else is needed.

## 7. The relaxed balance, part (e)

**Theorem E.**  For every `m >= 1`,

```text
    #{q in {0, 2, x}^m : Phi(q) = 0} = (3^m + 1) / 2.
```

*Proof.*  By Proposition C, on the letter space

```text
    Phi(q) = z_0 + sum_{i even, 2 <= i <= |N|} (z_i + w_i)     (mod 2),
```

where the block data `(z_0, ..., z_{|N|})` depend only on the positions of
the nonzero letters, and `w_i` is the even-bit of the head of `B_i`.

*The involution.*  Let `S_2 = {q : |N| >= 2}` and define `tau` on `S_2` by
toggling the head of `B_2` (the letter `q_2`, second nonzero from the top)
between `2` and `x`.  `tau` preserves the positions of all nonzero letters,
hence `|N|`, every block and every `z_i`, and every `w_i` with `i != 2`; it
flips `w_2`.  So `Phi(tau q) = Phi(q) + 1`.  `tau` is an involution of `S_2`
without fixed points, so `#{q in S_2 : Phi = 0} = #{q in S_2 : Phi = 1}`.

*The remainder.*  `|N| = 0`: the all-zero word, `z_0 = m`, `Phi = m mod 2`.
`|N| = 1`: one nonzero letter (`2` choices) with `z_0 in {0, ..., m-1}` zeros
above it, and `Phi = z_0 mod 2` because there is no even index.  So

```text
    #{|N| <= 1, Phi = 0} = [m even] + 2 ceil(m/2),
    #{|N| <= 1, Phi = 1} = [m odd]  + 2 floor(m/2).
```

The difference is `1 + 0 = 1` for `m` even and `-1 + 2 = 1` for `m` odd.

Hence `N_0(m) - N_1(m) = 1` for every `m >= 1`, and with
`N_0(m) + N_1(m) = 3^m` the claim follows.  QED.

Check S6 verifies each ingredient separately for `m <= 12`: the block formula
equals the Moore `Phi` on every word, `tau` flips `Phi` on every word with
`|N| >= 2` (531,416 words at `m = 12`), the `|N| <= 1` census matches the
closed form, and `N_0 - N_1 = 1`.  `uc/r1-quadratic/q2_balance_proof.py`
gives an independent proof by the transfer matrix (characteristic polynomial
`x^4 - 2x^3 - 4x^2 + 2x + 3`, `p(1) = 0`, `d(1..4) = 1`); the involution proof
above needs no linear algebra and names the one unpaired word: for each `m`
the imbalance is carried entirely by the `|N| <= 1` words, and on `|N| >= 2`
the pin is exactly balanced by `tau`.

*What (e) does and does not say.*  It is the exact form of the "one bit for
the `E` constraint" in `RESULTS-RW-LINEAR-SLACK.md` section 8, on the relaxed
three-letter space.  Realised windows are not uniformly distributed on that
space, their bottom letter is never `0`, and their letters are constrained by
earlier columns; (e) is a statement about the functional, not about the
orbit.

## 8. Gates

All in `rbf_structural_checks.py`.  Counts are from
`rbf_structural_checks_u14_m12.log` unless stated.

| check | what | range | count | result |
|---|---|---|---|---|
| S1 | F1, decoupling of `CONE`; right-bijectivity | all pairs | 16 | PASS |
| S2 | F2, boundary facts | all symbols | 4 | PASS |
| S3 | F3, `Endpoint` = triangle | binary `u <= 14`, four-state `u <= 7` | 54,610 words | PASS |
| S4 | Lemma H, Lemma E on whole columns, all four `e_u` | same words | 4,791,416 cells | PASS |
| S5 | (a), (b), (c), C', D1, D2, D3 (with `e_{u+1}`), D5 | all binary words `u <= 14`, all `n <= u` | 425,986 `(word, n)` pairs; 32,143 pair keys, each one column; 3,534,232 odd flips invisible; 3,320,196 even flips visible | PASS |
| S6 | Theorem E, three ingredients and the total | `m <= 12` | `3^12 = 531,441` words at `m = 12` | PASS |
| control | `--mutate`, retained := odd-indexed | `u <= 6` | fires at `('b', (1,), 1, -1)` | fires (`rbf_structural_mutate.log`) |

S5 also asserts, on every `(word, n)`, that exactly one binary symbol forces
`H(T[u][n]) = 1` (Proposition A) and that the column built by the rule on the
window agrees with the triangle of the extended word (0.3).

These runs are gates on the derivation.  The proof rests on F1, F2 and the
written derivations; F3 ties the statement to the kernel code.

## 9. Position

**Implication.**  None of `(RW-alpha)`, `(RW)`, `(SEP)`, `(PT2)`, P1.  The
lemma is an identity uniform in `n` and `u`, not a bound, and makes no claim
about how long a forced orbit can stay in the hit set.

**Obstructions A to H** (BRIEF section 6).  A: not applicable, the statement
relates two adjacent columns and makes no propagation-depth claim.  B: not
applicable, it is an identity for the specific four-state rule `CONE` and
proves nothing about any centre column; a Rule 90 analogue would be a
different identity.  C: not applicable, no functional of the 2D diagram is
used.  D: evaded, the composition of the pin with the column map is derived
in full (sections 5 and 6), including the set form of BRIEF section 3 that
was previously only verified.  E: not applicable, no measure.  F: not
applicable, the window grows with `u` and the identity holds for every `u`.
G: not applicable, no complexity measure.  H: evaded, the identity is derived
from F1 and F2, which are finite by nature; the exhaustive runs are gates.

**Nearest killed row.**  BRIEF section 6, "Bare holonomy-defect word"
(identical profiles with different next rows).  This proof agrees with that
kill and makes it exact: a single zero pattern `Z_{u-1}` does not determine
column `u` because the odd-indexed even-bits are discarded (D5), and their
number `ceil(|N|/2)` is unbounded.  It differs in claiming only that the pair
`(Z_{u-1}, Z_u)` is a lossless re-encoding of column `u` on `[-u-1, n]`; it
is not a bounded quotient, nothing is discarded, and it makes no claim of
contraction.  For the same reason it is not the row "Fixed finite quotient of
the frontier".

## 10. What is established, and gaps

**Established.**  Parts (a) to (e) of the lemma exactly as stated, for every
`n >= 1`, every binary word in `{1,2}^u` with `u >= n`, and every `m >= 1`,
with `T` the triangle of 0.1 over the rule `CONE`.  Two by-products: the set
form of the pin in BRIEF section 3 is derived (Corollary C'); the two column
integrals of BRIEF section 2 hold for arbitrary four-state prefixes and
arbitrary `e_u` with constant `E(e_u)` (Lemma H, Lemma E).

**Gaps.**  None for the lemma as stated.  Three scope remarks, so that the
result is not read as more than it is:

1. The proof is about the array `T` defined by the triangle recurrence over
   `CONE`.  The identification of that array with the inverse-cone and peel
   pipeline of the earlier reports, and of the pipeline with Rule 30's
   Problem 1, is the previously proved chain of BRIEF section 1 and
   `psi_kernel.validate()`; it is not re-proved here and the lemma does not
   depend on it.
2. "The whole forced future" is made precise as D4: the sequence of forced
   symbols, the columns on `[-u'-1, n]` and the hits `E(T[u'][n])` for all
   `u' > u`.  Cells of column `u'` above depth `n` are outside that statement
   and are not determined by the pair.
3. Theorem E counts words of the relaxed letter space with the forced start.
   It is not a statement about the distribution of realised windows or about
   consecutive hits on an orbit.

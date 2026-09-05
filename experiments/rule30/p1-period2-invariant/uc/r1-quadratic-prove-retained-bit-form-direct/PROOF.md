# Direct proof of lemma `retained-bit-form`, parts (a) to (e)

Date: 2026-09-03.  Style: DIRECT, from the local rule and the column integrals.

Status: **PROVED, all five parts, uniformly in `n`, `u` and the prefix.**  The
lemma is an identity between two adjacent columns of the four-state kernel of
`uc/BRIEF.md` section 2.  It implies none of `(RW-alpha)`, `(RW)`, `(SEP)`,
`(PT2)`, P1; it supplies exact coordinates for the E-pin `Phi` and nothing
about the all-length quantifier.  Section 9 says what is and is not
established; section 10 addresses obstructions A to H.

Inputs consumed by the proof, and nothing else:

1. The definition of the triangle `T[u][d]` in `BRIEF.md` section 2 (the
   endpoint symbol at `d = -u-1`, `phi(3, .)` at `d = -u`, the recursion
   `T[u][d] = phi(T[u-1][d-1], T[u][d-1])` above), with `phi = CONE` of
   `psi_kernel.py`.
2. Three facts about the 16 values of `phi` and the 4 values of `BOUNDARY`,
   listed as (F1) to (F3) in section 1.  They are finite and are re-checked by
   gate G0 of `rbf_direct_gate.py` (`rbf_direct_gate.log` line 2).

Everything else is derived in full below.  The script `rbf_direct_gate.py`
in this directory is a bookkeeping gate on the derivation: it rebuilds the
triangle from the section 2 recursion (its own code, not the kernel's
`Endpoint`), checks that this agrees with `Endpoint`, and re-checks every
derived statement on binary prefixes, on free letter-space windows and on the
balance count.  Its logs are `rbf_direct_gate.log` (defaults, 29 s) and
`rbf_direct_gate_large.log` (larger ranges).  These are gates on the
write-up, not evidence for the lemma; obstruction H does not arise because
no step of the proof rests on them.

No em-dashes appear in this file.

## 1. Setting, notation, and the three local facts

**Cells.**  A cell is `T in {0,1,2,3}` with high bit `H(T) = T >> 1`, low bit
`Lo(T) = T & 1` and defect `E(T) = 1 + H(T) + Lo(T) (mod 2)`.  Every
congruence below is mod 2 unless it is a count.  Four elementary facts,
each a two-line check on the four values:

```text
  (C1)  T = 2 H(T) + Lo(T)  and  Lo(T) = 1 + H(T) + E(T);  so T is a function of (H(T), E(T)),
        and  T = 0  iff  (H(T), E(T)) = (0, 1).
  (C2)  E(T XOR 3) = E(T)            (XOR 3 flips both bits, their sum mod 2 is unchanged).
  (C3)  E(1) = E(2) = 0,  E(0) = E(3) = 1.
  (C4)  [Lo(T) = 0] = 1  iff  T in {0, 2};  for T != 0 it is  [T = 2].
```

**The triangle.**  Endpoint symbols `e_0, e_1, ...` in `{0..3}`.  Column `u`
occupies depths `d in [-u-1, u]`:

```text
  T[u][-u-1] = e_u,      T[u][-u] = BOUNDARY[e_u],      T[u][d] = phi(T[u-1][d-1], T[u][d-1])  for d in [-u+1, u].
```

**The three local facts** (all 16 pairs `(l, r)` and all 4 values `s`;
gate G0):

```text
  (F1)  H(phi(l, r)) = H(r) + 1 + [l = 0]
  (F2)  E(phi(l, r)) = E(r) + H(r) * [Lo(l) = 0]
  (F3)  BOUNDARY[s]  = s XOR 3
```

(F1) and (F2) are the decoupling of `BRIEF.md` section 2.  G0 also records
that the rows `CONE[1]` and `CONE[3]` coincide, i.e. the left parents `1`
and `3` are literally the same letter for `phi`; that is the 4-to-3 quotient
and it is a consequence of (F1) and (F2) (both read `l` only through
`[l = 0]` and `[Lo(l) = 0]`, which agree on `1` and `3`).

**Standing data for (a) to (d).**  Fix `n >= 1`, `u >= n` and a binary prefix
`e_0, ..., e_{u-1} in {1,2}^u`.  Column `u-1` is then a fixed word on
`[-u, u-1]` with `T[u-1][-u] = e_{u-1} in {1,2}`.  The **window** is
`Win = [-u, n-1]`, of length `m = n + u`.  For `d in Win` write

```text
  a_d = [T[u-1][d] = 0],      b_d = [Lo(T[u-1][d]) = 0] = [T[u-1][d] in {0, 2}].
```

`Z` is the set of zero cells of the window, `Nz` the set of nonzero cells,
`N = |Nz| = m - |Z|`, and `q_1 > q_2 > ... > q_N` lists `Nz` from the top.
Since `T[u-1][-u] = e_{u-1} != 0`, `N >= 1` and `q_N = -u`.  Put
`q_{N+1} := -u - 1` (one below the window).  A cell `d in Win` is
**retained** exactly as the lemma says: `d = q_i` with `i` even, or `d in Z`
whose nearest nonzero cell above is `q_i` with `i` even, or `d in Z` with no
nonzero cell above.  For `i = 1..N` put `w_i = [T[u-1][q_i] = 2]`, the
even-bit of the `i`-th nonzero cell.  The symbol `c in {2,3}` of the lemma
plays no role in (a) to (d): the forcing is `H(T[u][n]) = 1` whatever `c` is,
and `c` enters only in the hit test `E(T[u][n]) = E(c)`.

For any candidate `e_u in {0..3}` write `h(d) = H(T[u][d])` and
`F(d) = E(T[u][d])` for `d in [-u, n]`; these depend on `e_u`.

## 2. Locality: column `u` at depth at most `n` reads only the window

**Lemma 1.**  For every `e_u in {0..3}` and every `d in [-u-1, n]`, the cell
`T[u][d]` is a function of `e_u` and of `(T[u-1][d'])_{d' in Win}` alone.

*Proof.*  Induction on `d`.  `T[u][-u-1] = e_u` and `T[u][-u] = BOUNDARY[e_u]`
read nothing from column `u-1`.  For `d in [-u+1, n]`,
`T[u][d] = phi(T[u-1][d-1], T[u][d-1])` with `d - 1 in [-u, n-1] = Win`, and
`T[u][d-1]` is covered by the induction hypothesis.  QED.

Consequently the whole family `(T[v][d])_{v >= u-1, d <= n}` together with any
rule choosing `e_v` from column `v-1` on `[-v, n-1]` is a closed system: the
"forced future" of (d) is well defined at depths `<= n` and never consults a
cell deeper than `n`.

## 3. The two column integrals and the Moore form

**Lemma 2 (H integral).**  For every `e_u in {0..3}` and `d in [-u, n]`,

```text
  h(d) = 1 + H(e_u) + (d + u) + Z(<d),        Z(<d) := #{d' in [-u, d) : a_{d'} = 1}.
```

*Proof.*  At `d = -u`: `h(-u) = H(e_u XOR 3) = 1 + H(e_u)` by (F3), and
`(d + u) + Z(<d) = 0`.  Step `d -> d+1` for `d in [-u, n-1]`: by (F1) applied
to `T[u][d+1] = phi(T[u-1][d], T[u][d])`, `h(d+1) = h(d) + 1 + a_d`, which
adds `1` to `(d + u)` and `a_d` to `Z(<d)`.  QED.

This is `(H)` of `BRIEF.md` section 2 (`(d + u + 1)` there equals
`1 + (d + u)` here).

**Lemma 3 (E integral).**  For every `e_u in {1,2}` and `d in [-u, n]`,

```text
  F(d) = sum_{d' in [-u, d)} h(d') b_{d'}      (mod 2).
```

*Proof.*  At `d = -u`: `F(-u) = E(e_u XOR 3) = E(e_u) = 0` by (F3), (C2),
(C3), and the empty sum is `0`.  Step: by (F2),
`F(d+1) = F(d) + h(d) [Lo(T[u-1][d]) = 0] = F(d) + h(d) b_d`.  QED.

This is `(E)` of `BRIEF.md` section 2.  Lemmas 2 and 3 together say that
`(h(d), F(d))_{d in [-u, n]}` is the trajectory of the Moore machine
`step(h, F, a, b) = (h + 1 + a, F + h b)` started at `(1 + H(e_u), 0)` and fed
the letters `(a_d, b_d)` for `d = -u, ..., n-1` in that order; by (C1) the cell
is `T[u][d] = 2 h(d) + (1 + h(d) + F(d) mod 2)`, so the column is the state
trajectory.  Gate L checks this Moore form against the `phi` recursion on
every window in `{0,1,2}^m`, `m <= 10`, and `{0..3}^m`, `m <= 8`.

## 4. Forcing, and part (a)

**Lemma 4.**  Exactly one `e_u in {1,2}` satisfies `H(T[u][n]) = 1`, namely
the one with

```text
  H(e_u) = m + |Z| = N      (mod 2).
```

Hence `e_u = 2` iff `N` is odd, which is (a).  Equivalently `e_u = 1` iff
`|Z| = n + u (mod 2)`, the hard-core coordinate quoted in the lemma's value
field.

*Proof.*  By Lemma 2 at `d = n`, `h(n) = 1 + H(e_u) + m + |Z|`, an affine
function of `H(e_u)` with coefficient `1`; as `e_u` runs over `{1, 2}`,
`H(e_u)` runs over `{0, 1}` and `h(n)` takes both values once.  `h(n) = 1`
iff `H(e_u) = m + |Z|`, and `m + |Z| = m - |Z| = N (mod 2)`.  `H(2) = 1`,
`H(1) = 0`.  QED.

From now on `e_u` is the forced symbol.  Lemma 4 applied at every later column
shows the forced orbit stays inside `{1,2}` for ever, which is the
"high-bit elimination" of `PROOF-STATE-CAPSULE.md` section 2 re-derived.

## 5. Part (b): the H profile of column `u` is the retained set

**Lemma 5.**  With `e_u` forced, for every `d in [-u, n]`,

```text
  h(d) = 1 + #{nonzero cells of the window at depth >= d}     (mod 2).
```

In particular `h(d) = 1` iff `d` is retained, for every `d in Win`, and
`h(n) = 1`.

*Proof.*  Substitute `H(e_u) = m + |Z| = n + u + |Z|` into Lemma 2:

```text
  h(d) = 1 + (n + u + |Z|) + (d + u) + Z(<d)
       = 1 + (n - d) + (|Z| - Z(<d))                      (2u = 0 and -x = x mod 2)
       = 1 + (n - d) + Z(>=d),                            Z(>=d) := #{d' in [d, n) : a_{d'} = 1}.
```

The interval `[d, n)` has `n - d` cells, of which `Z(>=d)` are zero, so
`(n - d) - Z(>=d) = (n - d) + Z(>=d)` is the number of nonzero cells at depth
`>= d`.  This proves the display.  Now read it off cell by cell:

- `d = q_i`: the nonzero cells at depth `>= q_i` are `q_1, ..., q_i`, so
  `h(q_i) = 1 + i`, which is `1` iff `i` is even.
- `d in Z` with nearest nonzero cell above equal to `q_i`: the nonzero cells
  above `d` are exactly `q_1, ..., q_i` (since `q_{i+1} < d < q_i`), so
  `h(d) = 1 + i`, which is `1` iff `i` is even.
- `d in Z` with no nonzero cell above: the count is `0`, `h(d) = 1`.
- `d = n`: the count is `0`, `h(n) = 1`, which is the forcing.

These three cases are the three clauses of "retained".  QED.

**Corollary 5.1 (the H profile of column `u` encodes `Z`).**  For
`d in Win`, `1 + h(d) + h(d+1) = [T[u-1][d] != 0]`, because the counts in
Lemma 5 at `d` and `d+1` differ by exactly `[d in Nz]`.  So the pair
`(h(d))_{d in [-u, n]}` and the zero set `Z` of the window determine each
other.  (This is also the Moore step `h(d+1) = h(d) + 1 + a_d` read
backwards.)

## 6. Part (c): the E-pin is the all-ones affine form on the even bits

**Lemma 6.**  With `e_u` forced,

```text
  E(T[u][n]) = #(retained zero cells) + #{i even : T[u-1][q_i] = 2}     (mod 2)
             = #(retained zero cells) + sum_{i even, 1 <= i <= N} w_i.
```

*Proof.*  By Lemma 3 at `d = n`, `F(n) = sum_{d in Win} h(d) b_d`.  By Lemma
5, `h(d) = 1` exactly on the retained cells, so `F(n) = #{d retained : b_d = 1}`.
By (C4), `b_d = 1` for every zero cell, and for a nonzero cell iff it equals
`2`.  The retained nonzero cells are exactly the `q_i` with `i` even.  QED.

So `Phi` (defined in `BRIEF.md` section 3 by `E(T[u][n]) = Phi(col_{u-1})`)
is, for a fixed zero pattern `Z`, the affine functional
`w |-> const + sum_{i even} w_i` on the even-bits of the retained nonzero
cells, with all coefficients `1` and constant term the retained-zero count;
it is independent of `w_i` for `i` odd.  This is the statement of (c).

**Corollary 6.1 (the BRIEF section 3 forms follow).**  Write `N(<d)` for
the number of nonzero cells at depth `< d`, so the count in Lemma 5 is
`N - N(<d)` and `h(d) = 1 + N + N(<d)`.  Then

```text
  F(n) = sum_{d in Z or W2} (1 + N + N(<d))
       = (|Z| + |W2|) (1 + N) + #{(x, y) : x < y, x in Nz, y in Z or W2},
```

and `1 + N = 1 + m + |Z|`.  That is the set form of `BRIEF.md` section 3
(and `RESULTS-RW-LINEAR-SLACK.md` 9.3); with `alpha' = N`,
`beta = |Z| + |W2|`, `gamma' = ` the pair count, it is the primed form
`beta (1 + alpha') + gamma'`.  The BRIEF records both as verified on 131,580
checks; here they are derived.  Gate P and gate L compare the retained form
with an independently coded set form on every column (tag `c-setform`).

## 7. Part (d): zeros of column `u`, the read-out, and the lossless pair

**7.1 The run structure of the window.**  For `1 <= i <= N` let
`I_i = (q_{i+1}, q_i]` (depths strictly above `q_{i+1}`, up to and including
`q_i`), and `I_0 = (q_1, n-1]`.  These `N + 1` intervals partition `Win`:
`I_0` is the (possibly empty) block of zeros above the top nonzero cell, and
for `i >= 1` the block `I_i` consists of `q_i` together with the zeros
strictly between `q_{i+1}` and `q_i` (there is no other nonzero cell there,
by the definition of the `q_i`); for `i = N`, `I_N = (-u-1, -u] = {-u}`.

Every cell of `I_i` (`i >= 1`) has nearest nonzero cell above equal to `q_i`
or is `q_i` itself, and every cell of `I_0` has no nonzero cell above, so by
the definition of retained:

```text
  I_0 is retained;   I_i is retained for i even;   I_i is non-retained for i odd.
```

Hence the non-retained cells form the disjoint intervals `R_i := I_i`,
`i odd`, and each `R_i` is a **maximal** run of non-retained cells: its
neighbours `I_{i-1}` (above) and `I_{i+1}` (below, if `i < N`) are retained
blocks, and `I_{i-1}` for `i >= 3`, resp. `I_{i+1}` for `i < N`, is nonempty
because it contains `q_{i-1}`, resp. `q_{i+1}`; for `i = 1` the block `I_0`
above may be empty, in which case `R_1` reaches the top of the window, and
for `i = N` the run reaches the bottom.  The number of maximal non-retained
runs is the number of odd `i <= N`, i.e. `ceil(N/2)`.  Gate P and gate L
check that the maximal runs computed from the definition of retained are
exactly the `I_i`, `i odd` (tag `d-runs`).

**7.2 `F` is constant on each run; `Z_u` is a union of complete runs.**

**Lemma 7.**  With `e_u` forced:

(i) `T[u][-u-1] = e_u != 0`.

(ii) For `d in Win`, `T[u][d] = 0` iff `d` is non-retained and `F(d) = 1`.

(iii) For `i` odd, `F` is constant on `R_i`, with value

```text
  F_i := #{ d' in [-u, q_{i+1}] : d' retained and b_{d'} = 1 }     (mod 2)
```

(for `i = N`, the range `[-u, -u-1]` is empty and `F_N = 0`).

(iv) The zero set `Z_u` of column `u` on `[-u-1, n-1]` is
`union { R_i : i odd, F_i = 1 }`, a union of complete maximal non-retained
runs of column `u-1`, and `F_i = [R_i subset Z_u]` for every odd `i`.

*Proof.*  (i) is `e_u in {1,2}`.  (ii) is (C1) with Lemma 5: `h(d) = 0` iff
`d` is non-retained.  (iii): by Lemma 3, `F(d) = #{d' in [-u, d) : h(d') b_{d'} = 1}`
and by Lemma 5 the summand is `[d' retained and b_{d'} = 1]`.  For `d in R_i`,
the cells of `[q_{i+1} + 1, d)` lie in `R_i` and are non-retained, so they
contribute nothing, and `F(d) = #{d' in [-u, q_{i+1}] : ...} = F_i`.  (iv):
combine (i), (ii), (iii): a non-retained cell `d` lies in exactly one run
`R_i`, and `T[u][d] = 0` iff `F_i = 1`, independent of which cell of the run
`d` is; retained cells and `d = -u-1` are never zero.  QED.

Gate P and gate L check (iv) on every column (tags `d-bottom`, `d-partial`,
`d-outside`).  Note that when `N` is odd the bottom run is `R_N = {-u}` with
`F_N = 0`, so `T[u][-u] = 1` there; indeed `e_u = 2` and `2 XOR 3 = 1`.

**7.3 The even bits are read from `(Z_{u-1}, Z_u)`.**

**Lemma 8 (read-out).**  For every even `i` with `2 <= i <= N`,

```text
  w_i = F_{i-1} + F_{i+1} + z_i       (mod 2),
```

where `z_i` is the number of zero cells strictly between `q_{i+1}` and `q_i`,
`F_{i-1} = [R_{i-1} subset Z_u]`, and `F_{i+1} = [R_{i+1} subset Z_u]` for
`i + 1 <= N` while `F_{N+1} := 0`.  Consequently `Z_u`, together with the
zero set `Z_{u-1} = Z` of the window, determines every `w_i` with `i` even.

*Proof.*  By Lemma 7(iii), `F_{i-1}` counts the retained cells with `b = 1`
in `[-u, q_i]`, and `F_{i+1}` counts them in `[-u, q_{i+2}]` (for `i = N`,
in the empty set, giving `0`).  Their difference is the count in
`(q_{i+2}, q_i] = R_{i+1} union I_i` (for `i = N` this is `I_N = {-u}`,
since `q_{N+1} = -u-1`).  `R_{i+1}` is non-retained and contributes `0`.
`I_i` is retained and consists of the `z_i` zero cells strictly between
`q_{i+1}` and `q_i`, each with `b = 1` by (C4), and the cell `q_i`, with
`b = w_i` by (C4).  So `F_{i-1} - F_{i+1} = z_i + w_i (mod 2)`.  The
identification `F_j = [R_j subset Z_u]` for odd `j` is Lemma 7(iv).  Finally
`z_i` and the `q_i` are functions of `Z`.  QED.

Gate P and gate L check the display on every column and every even `i`
(tag `d-readout`).

**7.4 The pair determines column `u` and the forced future.**

**Lemma 9.**  Given `n` and `u`:

(i) Column `u` on `[-u-1, n]` is a function of `(Z_{u-1}, (w_i)_{i even})`,
hence by Lemma 8 of `(Z_{u-1}, Z_u)`.

(ii) Conversely column `u` on `[-u-1, n]` determines `(Z_{u-1}, Z_u)`, and
`(Z_{u-1}, Z_u)` determines `(Z_{u-1}, (w_i)_{i even})`.  So the three data
`(Z_{u-1}, Z_u)`, `(Z_{u-1}, (w_i)_{i even})` and column `u` on `[-u-1, n]`
are equivalent.  For a fixed `Z_{u-1}` the map from even-bit vectors to
`Z_u` is injective; over the free letter space (every window in
`{0,1,2}^m` admitted) every even-bit vector occurs, so exactly
`2^floor(N/2)` values of `Z_u` occur there, and on any sub-corpus, such as
the columns that binary prefixes actually produce, at most that many.

(iii) The forced future is a function of `(Z_{u-1}, Z_u)`: every forced symbol
`e_v` and every cell `T[v][d]` with `v >= u` and `d in [-v-1, n]` is
determined, and in particular `Z_{u+1}` is a function of `(Z_{u-1}, Z_u)`, so
the zero patterns obey a second-order recursion `Z_{u+1} = Psi(Z_{u-1}, Z_u)`.

*Proof.*  (i): `e_u` is given by Lemma 4 from `N = m - |Z_{u-1}|`;
`T[u][-u] = e_u XOR 3`; for `d in [-u+1, n]`, by (C1) the cell is
`2 h(d) + (1 + h(d) + F(d))`, where `h(d)` is a function of `Z_{u-1}` by Lemma
5 and, by Lemmas 3 and 5,

```text
  F(d) = #{ d' in [-u, d) : d' retained zero } + sum_{ i even, q_i < d } w_i     (mod 2),
```

a function of `Z_{u-1}` and the even bits.  (ii): `Z_u` is part of column
`u`; `Z_{u-1}` is recovered from the `h` profile by Corollary 5.1; the even
bits from `(Z_{u-1}, Z_u)` by Lemma 8.  The map from even-bit vectors to
`Z_u` (for fixed `Z_{u-1}`) is therefore injective; in the free letter space
every even-bit vector is realised by some window, so the image there has
`2^floor(N/2)` elements, `floor(N/2)` being the number of even indices in
`1..N`.  (iii): by Lemma 1 and Lemma 4 applied at column `u+1`,
`e_{u+1}` and column `u+1` on `[-u-2, n]` are functions of column `u` on
`[-u-1, n-1]`, which is part of column `u` on `[-u-1, n]`; induct on `v`.
`Z_{u+1}` is part of column `u+1`.  QED.

Gate P checks (i) and (iii) by asserting that equal keys `(n, u, Z_{u-1}, Z_u)`
always carry equal column `u` on `[-u-1, n]` and equal next three forced
symbols and hit cells (tag `d-pair`), on all binary words `u <= 12`, all
`n <= u`, and on random words at `n = 30, 60, 100` (and `150, 200` in the
large log).  Gate L checks (ii) exactly: in `{0,1,2}^m` every fixed zero
pattern has exactly `2^floor(N/2)` images `Z_u`, each `(Z_{u-1}, Z_u)` class
carries one column, and each class has exactly `2^ceil(N/2)` windows (the
odd bits free), for all `m <= 10` (tags `L-image-count`,
`L-pair-not-function`, `L-fibre`).

**7.5 The odd bits are never read.**

**Lemma 10.**  Replacing `T[u-1][q_i]` for any odd `i` by any nonzero value
(`1`, `2` or `3`) leaves `e_u`, column `u` on `[-u-1, n]`, and the whole
forced future unchanged.  In particular the even-bit of the top cell
`T[u-1][n-1]`, whenever that cell is nonzero (it is then `q_1`), is never
read.  Conversely, flipping `w_i` for an even `i` changes `T[u][n]`.

*Proof.*  Column `u` on `[-u-1, n]` is a function of `e_u` and of the letters
`(a_d, b_d)`, and it enters through `e_u` (a function of `N`), through
`h(d)` (a function of the `a`'s, Lemma 2) and through the products
`h(d) b_d` (Lemma 3).  A nonzero replacement at `q_i` keeps `a_{q_i} = 0` and
`N`, hence every `h(d)`, and `h(q_i) = 0` for `i` odd (Lemma 5), so the only
letter that changed is multiplied by zero.  The forced future depends on
column `u` on `[-u-1, n-1]` only (Lemma 9(iii)).  For the converse, flipping
`w_i` with `i` even flips the summand `h(q_i) b_{q_i} = b_{q_i}` in Lemma 3
and so flips `F(n) = E(T[u][n])` by Lemma 6.  QED.

Gate L checks Lemma 10 on every window in `{0,1,2}^m`, `m <= 10`, for every
odd-indexed nonzero cell and each of the two alternative nonzero values, and
checks that every even-indexed flip changes the column (tags `L-odd-read`,
`L-even-blind`, `L-3-vs-1`).

Parts (a), (b), (c), (d) of the lemma are Lemma 4, Lemma 5, Lemma 6 and
Lemmas 7 to 10 respectively.

## 8. Part (e): the relaxed balance, by direct count

**The relaxed space.**  A letter word is `q = (q^1, ..., q^m) in {0, 2, x}^m`
read from the bottom (`q^1`) to the top (`q^m`), where `0` is a zero cell,
`2` an even nonzero cell and `x` an odd nonzero cell (`1` or `3`; by G0 they
are the same letter).  Its letters are `a_k = [q^k = 0]`, `b_k = [q^k in {0, 2}]`.
`N` is the number of nonzero letters.  `Phi(q)` is the final `F` of the Moore
machine of section 3 run from `(h_0, 0)` with the **forced start**
`h_0 = 1 + N (mod 2)` over the `m` letters.  The bottom letter may be `0`:
this is why the space is "relaxed" relative to real windows, whose bottom
cell `e_{u-1}` is nonzero.  Retained, `q_i`, `w_i` are defined for letter
words exactly as in section 1 (positions in place of depths).

**Lemma 11 (Lemmas 5 and 6 hold on the relaxed space).**  For a letter word
`q` with the forced start, the value of `h` when letter `k` is about to be
read is `1 + #{nonzero letters at positions >= k}`, the final `h` is `1`, and

```text
  Phi(q) = #(retained zero letters) + sum_{i even} w_i     (mod 2).
```

*Proof.*  By the Moore step, `h` before letter `k` equals
`h_0 + (k - 1) + #{zeros among q^1..q^{k-1}} = 1 + N + #{nonzero among q^1..q^{k-1}}
= 1 + #{nonzero at positions >= k}` (mod 2).  After the last letter this is
`1 + 0 = 1`.  The case analysis of Lemma 5 and the argument of Lemma 6 apply
verbatim; neither used that the bottom letter is nonzero nor that the letters
came from a column.  QED.

**Lemma 12 (e).**  For every `m >= 1`,
`#{q in {0,2,x}^m : Phi(q) = 0} = (3^m + 1) / 2`.

*Proof.*  Sort the `3^m` words by their zero pattern (the set of positions of
the letter `0`), and count the words with `Phi = 0` in each class.

*Class `N >= 2`.*  Fix a zero pattern with `N >= 2` nonzero positions.  The
`2^N` words with that pattern are parametrised by the bits `w_1, ..., w_N`
(`w_i = 1` for the letter `2`, `0` for `x`), and by Lemma 11
`Phi = const + sum_{i even} w_i` with the constant depending only on the
pattern.  Since `i = 2` is available, this is a non-constant affine
functional of `w`, so exactly half of the `2^N` words have `Phi = 0`:
`2^{N-1}` of them.  Summing over the `C(m, N)` patterns with `N >= 2`:

```text
  sum_{N=2}^{m} C(m, N) 2^{N-1} = ( sum_{N=0}^{m} C(m, N) 2^N - 1 - 2m ) / 2 = (3^m - 1 - 2m) / 2.
```

*Class `N = 1`.*  The single nonzero letter sits at position `p in [1, m]` and
is `q_1`, odd-indexed, non-retained.  The zeros below it have nearest nonzero
above `q_1`, non-retained; the `m - p` zeros above it have no nonzero above,
retained.  So `Phi = m - p (mod 2)` for both letter values, and `Phi = 0` iff
`p = m (mod 2)`.  The number of `p in [1, m]` with `p = m (mod 2)` is
`ceil(m/2)`, giving `2 ceil(m/2)` words with `Phi = 0` out of `2m`.

*Class `N = 0`.*  The all-zero word: every letter retained, `Phi = m (mod 2)`,
so `[m even]` words with `Phi = 0`.

*Total.*  If `m` is even, `2 ceil(m/2) + [m even] = m + 1`; if `m` is odd,
`2 ceil(m/2) + 0 = m + 1`.  In both cases

```text
  #{Phi = 0} = (3^m - 1 - 2m) / 2 + (m + 1) = (3^m + 1) / 2.     QED.
```

Gate E checks this count by brute force through the `phi` recursion itself
(not only through the Moore machine) for `m <= 10` (`m <= 12` in the large
log), and checks the three-class decomposition: every pattern with `N >= 2`
is exactly balanced with `2^{N-1}` zeros, the `N = 1` class has
`2 ceil(m/2)` zeros out of `2m`, the `N = 0` class `[m even]` (tags
`E-total`, `E-pattern`, `E-N>=2-balanced`, `E-N=1`, `E-N=0`).

**Remark 12.1 (where the single word of imbalance lives).**  Every zero
pattern with at least two nonzero cells is exactly balanced.  The excess of
one in `2 #{Phi = 0} - 3^m = 1` is carried entirely by the patterns with
`N <= 1`: the `N = 1` class contributes `2 [m odd]` and the `N = 0` class
contributes `(-1)^m`, summing to `1` for every `m`.  On the relaxed space the
E-pin is therefore not merely "balanced to within one word" but balanced
pattern by pattern as soon as the window has two nonzero cells.

**Remark 12.2 (real windows).**  Real windows have a nonzero bottom cell.
The same count restricted to `q^1 != 0` gives, with `C(m-1, N-1)` patterns
per `N`,

```text
  #{Phi = 0, q^1 != 0} = sum_{N=2}^{m} C(m-1, N-1) 2^{N-1} + 2 [m odd] = 3^{m-1} - 1 + 2 [m odd],
```

out of `2 * 3^{m-1}` words, an imbalance of `-2` for even `m` and `+2` for
odd `m`.  Gate E checks this for `m <= 10` (tag `E-bottom-nonzero`).  This
remark is outside the lemma's statement and is recorded only because it is
the count that applies to the columns of (a) to (d).

**Independent cross-check of (e) by the transfer matrix** (the argument of
`uc/r1-quadratic/q2_balance_proof.py`, re-run here).  Let `A` be the `4 x 4`
matrix on Moore states summing the three letter permutations.  A word of
length `m` steers `(h_0, 0)` to `(1, eps)` iff `h_0 + N = 1`, i.e. iff `h_0`
is its forced start, so `#{Phi = eps} = sum_{h_0} (A^m)[(h_0,0),(1,eps)]`
and `d(m) = #{Phi = 0} - #{Phi = 1} = r^T A^m s` for fixed vectors `r, s`.
Gate E computes the characteristic polynomial of `A` exactly (Faddeev and
LeVerrier over the rationals) and finds
`x^4 - 2x^3 - 4x^2 + 2x + 3 = (x - 1)(x - 3)(x + 1)^2`; by Cayley and Hamilton
`d` satisfies the recurrence `d(m+4) = 2 d(m+3) + 4 d(m+2) - 2 d(m+1) - 3 d(m)`,
the constant sequence `1` satisfies it because `1` is a root, and
`d(1) = d(2) = d(3) = d(4) = 1` (gate E), so `d(m) = 1` for all `m >= 1` by
induction; with `#{Phi = 0} + #{Phi = 1} = 3^m` this is Lemma 12 again.
Gate E verifies `d(m) = 1` directly for `m <= 60` (`m <= 100` in the large
log).  The direct count of Lemma 12 is the proof; this paragraph is a second,
independent derivation of the same number.

## 9. What is established, and what is not

**Established (uniformly in `n >= 1`, `u >= n`, and the binary prefix):**
(a) Lemma 4; (b) Lemma 5; (c) Lemma 6, with the BRIEF section 3 set and
primed forms as Corollary 6.1; (d) Lemmas 7 to 10, including the explicit
read-out `w_i = F_{i-1} + F_{i+1} + z_i` and the equivalence of the three
descriptions of column `u` (Lemma 9(ii)); (e) Lemma 12, with the refinement
that every zero pattern with `N >= 2` is exactly balanced (Remark 12.1).

The proof uses only the definition of the triangle and the three finite
facts (F1) to (F3).  It never uses that the prefix is a forced-orbit prefix,
so the statement holds for every binary prefix.  Of the prefix, the proofs of
(a) to (d) use only that `e_u` is binary (`F(-u) = 0` by Lemma 3 and
`T[u][-u-1] != 0` in Lemma 7); `e_{u-1}` nonzero gives `q_N = -u` and is
used nowhere essential, and gate L runs (a) to (d) on windows in
`{0,1,2}^m` and `{0..3}^m` with a free bottom letter.

**Not established, and not claimed:**  nothing about `(RW-alpha)`, `(RW)`,
`(SEP)`, `(PT2)` or P1.  The lemma is an identity, not a bound.  It says how
the E-pin reads column `u-1`; it does not say the pin fails `n + r + 2` times
in a row on the forced orbit, which is the open quantifier.  The balance (e)
lives on the relaxed letter space, where every window is admissible; on the
forced orbit the windows are the specific columns the dynamics produces, and
Remark 12.2 already shows that restricting to real windows changes the
imbalance.  No independence or rate statement follows from (e).

**Gaps:** none.  Every step above is a derivation written out, a finite
check in `rbf_direct_gate.log`, or one of (F1) to (F3).

## 10. Obstructions A to H of `BRIEF.md` section 6

- **A** (`O(log t)` wall): not applicable.  The statement relates columns
  `u-1` and `u` at all depths `<= n` at once; it makes no propagation-depth
  claim.
- **B** (Rule 90 filter): not applicable.  The statement is about the
  specific rule `phi = CONE` of the four-state kernel, through (F1) to (F3);
  it proves nothing about any centre column, of Rule 30 or of Rule 90.
- **C** (single-column blindness): not applicable.  No functional of the 2D
  diagram is used.
- **D** (missing composition law): evaded.  The composition of `Phi` with the
  column map is derived (Lemmas 2 to 9), not named; the second-order
  recursion `Z_{u+1} = Psi(Z_{u-1}, Z_u)` is proved to exist (Lemma 9(iii)),
  and it is not claimed to be bounded or local.
- **E** (measure-zero orbit): not applicable.  No measure.
- **F** (free boundary of a fixed strip): not applicable.  The window grows
  with `u`; the identity holds for every `u`.
- **G** (arbitrary-input measures): not applicable.  No complexity measure.
- **H** (finite data): evaded.  The proof is uniform; the logs are gates on
  the bookkeeping of the write-up and carry no evidential weight in it.

Nearest killed row (section 6 of the BRIEF): "Bare holonomy-defect word".
Lemma 9(ii) agrees with that kill: `Z_{u-1}` alone has fibres (gate P:
`1492` of `7745` single-pattern keys at `u <= 12` carry more than one column,
largest fibre `7`, `rbf_direct_gate.log`), and the pair `(Z_{u-1}, Z_u)` is
not a bounded quotient; it is a lossless re-encoding of column `u`, of size
`2^floor(N/2)` per `Z_{u-1}`.

## 11. Gates: scripts, logs, and what each line certifies

Script: `rbf_direct_gate.py` (this directory).  Run from the work directory:

```sh
uv run python uc/r1-quadratic-prove-retained-bit-form-direct/rbf_direct_gate.py
uv run python uc/r1-quadratic-prove-retained-bit-form-direct/rbf_direct_gate.py --umax 14 --gate-n 12 \
    --rand-n 150 200 --samples 100 --seed 2 --letters-m3 12 --letters-m4 9 --balance-brute 12 --balance-transfer 100
```

Logs: `rbf_direct_gate.log` (first command, 29 s) and
`rbf_direct_gate_large.log` (second command).  Any assertion failure aborts
the run; the tuple names the tag and the witness.

| Gate | What it certifies | Range in `rbf_direct_gate.log` |
|---|---|---|
| G0 | (F1), (F2) on all 16 pairs of `CONE`; (F3) on all 4 values; (C2), (C3); `CONE[1] = CONE[3]`; `phi` right-bijective | finite |
| G1 | the triangle built here from the section 2 recursion equals `psi_kernel.Endpoint`'s columns | 2046 binary words, `u <= 10` |
| P | forcing unique; (a); (b); (c) and Corollary 6.1; runs are `I_i`, `i` odd; Lemma 7(iv); Lemma 8; Lemma 9(i),(iii) with 3 future steps | all binary words `u <= 12`, all `n <= u`, 90,114 pairs; random `n = 30, 60, 100`, 200 words each, all `u in [n, 2n+1]`, 39,200 pairs |
| L | Moore form equals the `phi` recursion; (a) to (d); Lemma 10 both directions; Lemma 9(ii) image `2^floor(N/2)` and fibre `2^ceil(N/2)` | all of `{0,1,2}^m`, `m <= 10`, 88,572 windows; all of `{0..3}^m`, `m <= 8`, 87,380 windows |
| E | Lemma 12 by brute force through `phi`, with the three-class decomposition and per-pattern balance; Remark 12.2; characteristic polynomial and `d(m) = 1` | `m <= 10` brute force; `m <= 60` transfer matrix |

The numbers quoted in this file (`1492`, `7745`, `7`, `2046`, `90,114`,
`39,200`, `88,572`, `87,380`, `29 s`) are read from `rbf_direct_gate.log`.

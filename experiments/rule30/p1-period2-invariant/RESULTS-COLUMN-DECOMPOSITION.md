# The endpoint state is an autonomous column with the diagonal as a cocycle,
# and the column forgets exactly half of its input

Date: 2026-09-03.  Scripts `column_quotient.py`, `affine_branch.py`,
`merge_anatomy.py`, `column_decomposition.py`, `column_memory.py`; logs of the
same names dated `20260903`.  Every count is a complete enumeration on the
validated kernel `psi_kernel.Endpoint`; nothing is sampled.

Status: **two mechanism classes killed, one exact structural law found.**
The law is `k(L) = ceil((L+1)/2)`: the endpoint column of a binary word of
length `L` depends on the last `ceil((L+1)/2)` symbols and on no fewer.  It
proves `|Col_L| <= 2^ceil((L+1)/2)`, a growth base of `sqrt(2)` for the
column language.  It does **not** prove the state base is below `2`; see
section 6 for exactly what is and is not delivered.

## 1. Two kills

### 1a. The exact symbol congruence is a constant factor, not a rate

`_carry_action` reads its symbol only through `(a|b)` and `a`, so symbols 2
and 3 have identical forward actions, `INVERSE[2] == INVERSE[3]`, and hence

```text
CONE[1] == CONE[3]        as full rows of the table
```

Every retained column or diagonal entry enters the next append only as the
left argument of `CONE`, so the append map factors through the quotient
`q: 0->0, 1->1, 2->2, 3->1` on the retained state.  This is a genuine
congruence, not an approximation.

Measured (`column_quotient_20260903.log`, `u = 1..19`): `|qC_u| / |C_u|`
settles at `0.941` and the growth base is unchanged (`1.7671` against
`1.7681` at `u = 19`).  The congruence is a 5.7 percent constant-factor
collapse.  **It is not the reason the base is below 2, and it does not extend
census reach.**

### 1b. Branch survivor sets are not affine subspaces: counting by F_2 rank is dead

Pre-registered in `affine_branch.py`.  Every killed mechanism to date supplied
a rate, and a rate cannot give the all-length quantifier because plateaus of
ratio `1.0` exist at deep levels (`RESULTS-FLIP-PAIRING.md` section 2).  The
untried class was a dimension count: if, along a fixed forced word
`s_0..s_{j-1}`, each level's `E`-condition were one affine equation over `F_2`
in the source bits, the branch survivor set would be an affine subspace,
`N_j` a sum of `2^(n-rank)` over live branches, and `N_j <= C 2^(n-j)` would
reduce to independence plus a branch count.

Measured (`affine_branch_20260903.log`, `n = 9..16`, both `c`, every level,
sources identified with `F_2^n` by `bit i = [W_i = 2]`, classes of size `>= 4`
tested for affine closure): **420 of 516 classes are not affine subspaces.**
Of the 96 that are, 88 have size 4 and 8 have size 8; every class above size 8
fails, including all classes above size 20 at every `n` and `c`.  The failures
are both kinds, size not a power of two and closure violated outright.

There was never a structural reason to expect otherwise: the carry action
contains an `OR`.  **Counting by `F_2` rank is dead and should not be renamed
and retried.**

## 2. What actually merges

`merge_anatomy.py`, `u = 1..17`.  The append stores the symbol literally as the
last column entry, so two states can merge only under the same appended
symbol.  For every child with more than one parent, the Hamming distance
between parents:

| `u` | `|C_u|` | merges | pairs | column distance 0 | column distance 1 | diagonal distance 1 |
|---|---|---|---|---|---|---|
| 13 | 2376 | 487 | 565 | 552 | 13 | 435 |
| 14 | 4265 | 970 | 1146 | 1112 | 34 | 894 |
| 15 | 7560 | 1738 | 2031 | 2003 | 28 | 1587 |
| 16 | 13382 | 2961 | 3459 | 3424 | 34 | 2719 |
| 17 | 23803 | 5407 | 6251 | 6202 | 43 | 4942 |

**99.3 percent of merging parents have identical columns** and differ only in
the diagonal, at Hamming distance one in 79 percent of cases.  The single
merge mechanism is diagonal collapse under a shared column.  The proposed
induction on "single-position column richness" is therefore the wrong
induction and was not run.

## 3. The decomposition

The child column is a function of the parent column and the appended symbol
alone, so the column recursion is autonomous and the diagonal is a cocycle
over it.  Counted separately (`column_decomposition_20260903.log` part 1):

| `u` | `|C_u|` | `|Col_u|` | `|Dia_u|` | `C` base | `Col` base | `C / Col` |
|---|---|---|---|---|---|---|
| 11 | 742 | 39 | 545 | 1.8098 | 1.3448 | 19.0 |
| 15 | 7560 | 129 | 5877 | 1.7726 | 1.3030 | 58.6 |
| 19 | 74613 | 410 | 56993 | 1.7681 | 1.3057 | 182.0 |

The column language is tiny and slow: 410 distinct columns at `u = 19` against
74613 states, base about `1.328` against `1.765`.  Extended alone to `L = 43`
(cheap, the recursion is autonomous) the column count reaches 411664 with base
`1.3294`.  No exact linear recurrence of order `<= 16` fits the 44 terms.

## 4. The identity and the bijection behind it

```text
|Col_{2u-1}| = |C_u|
```

holds exactly on every measured point, `u = 2..22`, values to 411664
(`column_decomposition_20260903.log` part 2; the odd rows carry the check).
It is not a coincidence.  The bijection is the **suffix map**: for every word
`w` of length `2u-1`,

```text
column(w)   determines and is determined by   state(w[-u:]),
```

the complete endpoint state (column and diagonal) of the last `u` symbols.
Verified well defined and onto `C_u` for `u = 3..10` (part 3, all `True`;
log `bij_ext_20260903.log` carries `u = 9, 10`, the latter matching a column
at length 19 against the 410 states at depth 10).
Two candidate maps that are not the bijection, and were checked and rejected:
the length-`u` prefix state, and any split of the long column into a leading
and trailing block.

Consequence: the diagonal is not independent state.  The endpoint state at
depth `u` is exactly the information carried by a single column at depth
`2u-1`, so `beta_col = sqrt(beta_state)`, which is what the two measured bases
say (`1.328^2 = 1.764`).  **There is one growth constant here, not two.**

## 5. The memory law, with proof

### 5a. Prior record in this repo

The half-slope cone itself is **not new here.**  `uc/r1-entropy/lightcone_check.py`
(concurrent session, log `lightcone_check.log`) states it as fact (1), "`T[u][d]`
depends on `e_j` only if `j >= (u-d-1)/2`", and checks it exhaustively with zero
failures for `u = 2..12`.  That script indexes by depth into the column and
covers the diagonal cells too; this one indexes by distance from the end of the
column.  The two conventions differ by at most one and were not reconciled
exactly, so treat them as the same phenomenon rather than the same formula.

What is new below is the **proof at all lengths**, the exact per-entry form,
and the counting consequence `|Col_L| <= 2^ceil((L+1)/2)`.  The observation is
theirs; the quantifier and the bound are the contribution.

### 5b. Census

`column_memory.py`, complete enumeration of `{1,2}^L` for `L = 1..18`, `k(L)`
the least `k` such that `column(w)` is a well defined function of `w[-k:]`:

```text
k(L) = ceil((L+1)/2)   for every L = 1..18, no exceptions
```

`k` is exact, not an upper bound: the script reports the least `k`.  The
per-entry profile (`--profile 14`) is sharper and is what the proof runs on.
Writing `d = L - i` for the distance of entry `i` from the end of the column,

```text
k(L, i) = ceil((d + 1) / 2),    d = L - i
```

on every `L = 1..14` and every entry, so the memory of an entry depends only
on its distance from the end of the column and not otherwise on `L`.

### 5c. Proof of the upper bound (all lengths)

Let `w` have length `L`, let `C` be its column (`L+1` entries, indices `0..L`)
and let `N` be the column of `w s` (`L+2` entries).  From `psi_kernel.peek`:

```text
N[L+1] = s
N[L]   = BOUNDARY[s]
N[i]   = CONE[C[i+1]][N[i+1]]        i = L-1, ..., 0
```

Index by distance from the end.  Entry `N[i]` sits at `d = (L+1) - i`.  It
reads `C[i+1]`, at distance `L - (i+1) = d - 2` in `C`, and `N[i+1]`, at
distance `d - 1` in `N`.

Claim: an entry at distance `d` depends only on the last `ceil((d+1)/2)`
symbols of its own word.  Double induction: outer on the word length, for the
appeal to `C`; inner on `d` within the fixed column `N`, for the appeal to
`N[i+1]`.  Both are well founded, `d` increasing as `i` decreases.

*Base.*  `d = 0` is `s` and `d = 1` is `BOUNDARY[s]`; both depend on the last
symbol alone, and `ceil(1/2) = ceil(2/2) = 1`.

*Step.*  By hypothesis `C[i+1]` depends on the last `ceil((d-1)/2)` symbols of
`w`, hence on the last `ceil((d-1)/2) + 1` symbols of `w s`, and `N[i+1]`
depends on the last `ceil(d/2)` symbols of `w s`.  So `N[i]` depends on the
last

```text
max( ceil((d-1)/2) + 1, ceil(d/2) )  =  max( ceil((d+1)/2), ceil(d/2) )
                                     =  ceil((d+1)/2)
```

symbols, which is the claim at `d`.  Both appeals are to strictly smaller
instances, `C` at a shorter word and `N[i+1]` at a smaller `d`.  QED.

Taking `i = 0`, so `d = L`, the whole column of a length-`L` word depends only
on its last `ceil((L+1)/2)` symbols.  **The endpoint column forgets the first
half of its input, at every length.**  Hence, unconditionally,

```text
|Col_L| <= 2^ceil((L+1)/2),     growth base sqrt(2) < 2.
```

The census of 5b supplies the converse, that no smaller `k` works, for
`L <= 18`; sharpness is not proved at all lengths and is not needed for the
bound.

This is the first all-length quantifier this kernel has produced.  It does not
contradict `RESULTS-RW-LINEAR-SLACK.md` 9.2 ("no effective forgetting"), which
measured survival across prefix bits of the full state, a different object;
nor `RESULTS-CLUSTER-ANATOMY.md`, which measured fibres of the source-to-state
map.  The state does not forget: by section 4 the state at `u` is a column at
`2u-1`, whose memory is `u` symbols, which is all of them.

## 6. What this delivers and what it does not

Delivered:

- `|Col_L| <= 2^ceil((L+1)/2)` for every `L`, **proved** in section 5c by
  induction on the append recursion, giving a growth base of `sqrt(2)` for the
  column language.  Measured base `1.328`, so the bound holds with slack and
  is not tight.
- One object instead of two.  Any argument about the state may be run on the
  column language at double the length, and the diagonal need not be carried.
- Two mechanism classes removed from the search: the exact symbol congruence
  and counting by `F_2` rank.

Not delivered, stated plainly:

- **The state base is not proved below 2.** Section 4 turns the state bound
  into a column bound at double the length, where the memory law gives
  `2^u` for `|C_u|`, which is trivial.  The measured `1.7648` remains
  measured.
- **The RW counting line `N_j <= 3 * 2^(n-j)` is untouched.** No result here
  bears on survivor levels; the two mechanisms tested for it were both killed.
- `(SEP)`, `(PT2)`, DLP and `(BWH+)` are exactly where they were.

## 7. Positioning

`|Col_L|` is a state count with merging, not a column-complexity count.  It
must not be confused with the two published Rule 30 counts.  NKS note 10-10
gives `p(t) = 2^t` exactly for single columns over all initial conditions, and
`{4, 12, 32, 80, 200, 496, ...}`, "roughly `2.25^t`", for adjacent column
pairs, with "there seems to be no simple characterization".  This sequence
diverges from `2^u` at `u = 4` (13 against 16), which is the clean separation.
Neither `|Col_L|` nor `|C_u|` is in OEIS (four queries, matcher verified live
on a control sequence), and no source attests the constant `1.7648` or the
entropy `0.8195` in a Rule 30 context.

The rigorous frame is soficity.  Kopra (Turku PhD 2019, Problem 3.1.13;
journal version *Theoretical Computer Science* 946 (2023) 113668,
arXiv:2202.13809, Theorem 3.5 and Corollary 3.7, Problem 3.10) makes "is
`W_30` regular" exactly the question of whether Rule 30's trace subshifts are
sofic.  A sofic column subshift forces a rational generating function, an
integer linear recurrence, and (Lind, *ETDS* 4(2):283-300, 1984) a Perron
algebraic growth constant.  The absence of any linear recurrence of order
`<= 16` over 44 terms is evidence in the non-sofic direction, in the same
direction as the width-2 data, and is a quantitative probe of an open problem.
It is evidence, not a proof, and must be written that way.

## 8. Reproduction

```sh
cd /Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant
uv run python column_quotient.py --tables --umax 19    # 30 s
uv run python affine_branch.py 9 16                    # 60 s
uv run python merge_anatomy.py --umax 17               # 40 s
uv run python column_decomposition.py                  # 90 s
uv run python column_decomposition.py --umax 2 --lmax 2 --bijmax 10   # 4 min
uv run python column_memory.py --lmax 18 --profile 14   # 90 s
```

## 9. Next

Section 5c closed the target this document originally named, so the open leads
are downstream of it.

1. **Sharpness at all lengths.**  Prove the converse of 5b, that no `k` below
   `ceil((L+1)/2)` suffices.  Census gives it to `L = 18`.  This is cosmetic
   for the bound and needed only if the exact constant is claimed.
2. **Close the gap `1.328` against `sqrt(2) = 1.414`.**  The memory law counts
   suffixes; the true column count is smaller because distinct suffixes
   collide.  A bound on that collision rate would lower the base.  This is the
   route to a base for the state language, which section 6 records as still
   unproved, since `2^u` is trivial there.
3. **Does the memory law reach the RW observable?**  The survival test reads
   the diagonal, not the column, and the state does not forget.  Whether any
   half-length statement survives the passage to the diagonal is open and
   should be measured before it is assumed.

None of these closes `(SEP)`, DLP or `(PT2)`, and the write-up must not imply
that any of them does.

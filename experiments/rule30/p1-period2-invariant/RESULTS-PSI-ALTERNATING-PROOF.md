# (PSI) on the alternating family: the closed form and the cut periodicity are proved, the pre-registered bound k_E <= 5 is false at k = 144, and the depth-seven rerun proves k_E(2) <= 3, k_E(3) <= 6 for every k >= 2

Date: 2026-09-16. Pre-registration `PREREGISTRATION-PSI-ALTERNATING-PROOF.md` (written
before the run). Script `alternating-family/psi_alternating_proof.py`, log
`alternating-family/psi_alternating_proof.log` (exit 1, 44 lines, line numbers cited
below). Witness `alternating-family/witness_k144.py`, log `alternating-family/witness_k144.log`.
Kernel `psi_kernel.py` (`Endpoint`, `psi`, `CONE`, `BOUNDARY`). Nothing here is read from
`alt_family.log`; every object is recomputed from `Endpoint`. Section 6 (same day) records
the depth-seven rerun under `PREREGISTRATION-PSI-ALTERNATING-DEPTH7.md`, which closes the
theorem.

**The kill fired. The pre-registered claim, `k_E(c) <= 5` for both tails `c` at every
`k >= 2`, is false: at `k = 144` the six forced cut cells `T[288+j][288]`, `j = 1..6`,
are `3 3 3 3 3 3`, so `k_E(3) >= 6` (`psi_alternating_proof.log` line 36, `FAIL
k_E(3)<=5`, witness list line 32: `k = 144, 368, 592, ..., 1712`), and `psi()` gives
`k_E(3) = 6` exactly there, seventh cell `2`, against `n + 2 = 290` (`witness_k144.log`
line 1) [K]. The theorem `(PSI)` on the family is therefore not claimed by this run,
and the script was not extended past its pre-registered depth of six cells. What the
run does prove. [C, then U over C] The closed form `S(k)`: with
`D = 2120030303000312031112300323` (period 28), `column[i] = D[(2k - i) mod 28]` for
`i = 0..2k` and `diagonal[j] = D[(2k + j) mod 28]` for `j = 0..2k-1`, i.e.
`T[2k-1][d] = D[(2k + d) mod 28]` on the whole endpoint state; verified directly for
`k = 2..200` (log line 6) and proved for every `k >= 2` by an induction whose step is
three checks on the two-append lockstep transducer for the column (lines 7 to 9, one
state return `sigma(28) = sigma(0)`) and fourteen for the anti-diagonal, one per
residue `k mod 14` (lines 10 to 23, each a state return after one period). [C, then U
over C] The one-period maps of the six-append lockstep transducer are permutations of
`4^6` states of order 64 at every even phase (line 25), so the six cut cells after any
fixed six-symbol pattern are `896`-periodic in `k` for every `k >= 2`, hence so are the
forced pattern and the six defect bits (`k_0 = 2`); the kernel census over
`k = 2..1793` confirms `V(k + 896) = V(k)` directly (line 29), and the exact period is
`P = 448` for the cut cells, 224 for the forced symbols, 28 for `k_E(2)` and 224 for
`k_E(3)` (lines 30, 31, 39). [U over C] `k_E(2) <= 3` for every `k >= 2` (line 35,
histogram line 33). [U over C] `k_E(3) <= 5` for every `k >= 2` with
`k != 144 (mod 224)`; on that residue the six inspected cells are constant and the run
says nothing further (histogram line 34: `k_E(3) = 6` at 8 of 1792 values). A disconfirming run for the
structure would have shown a transducer state that fails to return after one period
or a cut vector differing between `k` and `k + 896`; neither happened. The bound
failed because the census that suggested it stopped at `k = 60` and the first `k` with
six constant cells is 144.**

## 1. Objects

Conventions are those of `psi_kernel.py`, re-derived from the code, not from
`RESULTS-ALTERNATING-FAMILY.md`. After appending `e_0 .. e_{L-1}`, `Endpoint` holds
`column[i] = T[L-1][-i]` for `i = 0..L` (so `column[L]` is the last symbol and
`column[L-1] = BOUNDARY[e_{L-1}]`) and `diagonal[j] = T[L-1][j]` for `j = 0..L-1`.
`Endpoint.peek(s)` computes, for a symbol `s`,

```text
new_column[L] = BOUNDARY[s]
new_column[i] = CONE[column[i+1]][new_column[i+1]]        i = L-1 .. 0
new_diagonal[0] = new_column[0]
new_diagonal[j+1] = CONE[diagonal[j]][new_diagonal[j]]    j = 0 .. L-1
```

and `append(s)` sets `column = new_column + [s]`, `diagonal = new_diagonal`.
`CONE = ((0,1,3,2), (3,2,1,0), (3,2,0,1), (3,2,1,0))`, `BOUNDARY = (3,2,1,0)` (log line
2); every row of `CONE` is a permutation (line 3). High bit `H(c) = c >> 1`; the law
`H(CONE[L][R]) = H(R) + 1 + [L == 0] (mod 2)` holds on all 16 pairs (line 4), and
`H(BOUNDARY[1]) = 1 != 0 = H(BOUNDARY[2])` (line 5).

The source is `W = (12)^k`, `L = n = 2k`. The H-forced continuation appends, at each
step, the unique `s in {1, 2}` for which `peek(s)` gives `new_diagonal[n]` with high bit
1; the cut cell of the `m`-th forced append is `dia[2k]` of that append's `peek`, which in
this section's convention (`diagonal[j] = T[L-1][j]` after `L` appends) is `T[2k+m-1][2k]`
and is written `T[2k+m][2k]` below in the psi doc's row numbering (no computation depends
on the choice); its low bit is the defect
bit `Psi_{m-1}`, and `k_E(c)` is the least `j` with `Psi_j != c & 1` (`c = 2` is low bit
0, `c = 3` is low bit 1). `(PSI)` on `W` is `k_E(c) < n + 2` for both `c`.

**The sequence `D`.** `D = 2120 0303 0300 0312 0311 1230 0323`, indices mod 28. It is
the block of `RESULTS-ALTERNATING-FAMILY.md` rotated by four (that document's
`D'[t] = D[t + 4]`, and its window `D'[2k-4 : 4k-4]` is `D[2k .. 4k-1]`); the
document's pair cycle is `C[m] = (D[6 + 2m], D[5 + 2m])` and its "fixed bottom"
`0003030300212` is `D[12], D[11], ..., D[0]`, the column at `k = 6`. There is no
separate bottom: the column and the anti-diagonal are one periodic sequence read in
the depth coordinate.

**The induction hypothesis `S(k)`, exactly.** For `k >= 2`, after appending `(12)^k`:

```text
column[i]   = D[(2k - i) mod 28]     i = 0, 1, ..., 2k        (length 2k+1)
diagonal[j] = D[(2k + j) mod 28]     j = 0, 1, ..., 2k-1      (length 2k)
```

Equivalently `T[2k-1][d] = D[(2k + d) mod 28]` for every depth `-2k <= d <= 2k-1`.
Consequences read off `D`: `column[2k] = D[0] = 2`, `column[2k-1] = D[1] = 1`,
`column[0:2] = (D[2k mod 28], D[(2k-1) mod 28])`, `diagonal[2k-1] = D[(4k-1) mod 28]`.

**The lockstep transducer.** Running `m` consecutive appends in lockstep, with
`x_l` the value of the `l`-th new column (or new anti-diagonal) at the current index,
gives one machine on `{0,1,2,3}^m`,

```text
STEP((x_1, ..., x_m), z) = (CONE[z][x_1], CONE[x_1][x_2], ..., CONE[x_{m-1}][x_m])
```

because the `l`-th append reads the `(l-1)`-th column (resp. anti-diagonal) as its
left parent. For each `z`, `STEP(., z)` is a bijection of `{0..3}^m`: it is triangular
and every `CONE[.]` row is a permutation. The column pass reads
`z = column[2k], column[2k-1], ..., column[1]` (bottom up; `column[0]` is never read by
a column pass), the anti-diagonal pass reads `z = diagonal[0], ..., diagonal[2k-1]`
(old end first), seeded by the column pass's final state.

## 2. Result

### 2.1 The closed form, proved for every k >= 2

Base. `S(2)` holds: `column = 0 0 2 1 2 = D[4] D[3] D[2] D[1] D[0]`,
`diagonal = 0 3 0 3 = D[4..7]`. The check `S(k)_direct_k=2..200` (log line 6) compares
both lists to the closed form for every `k = 2..200` against `Endpoint` built by
appending; a wrong `D`, a wrong phase, or a wrong index direction would fail it at
`k = 2` [C].

Column step (prose a referee can follow). Fix `k >= 2` and assume `S(k)`. Append `1`
then `2`. The first append sets `new'[2k] = BOUNDARY[1] = 2` and
`new'[i] = CONE[column[i+1]][new'[i+1]]` for `i = 2k-1 .. 0`. The second sets
`new''[2k+1] = BOUNDARY[2] = 1`, `new''[2k] = CONE[1][new''[2k+1]] = CONE[1][1] = 2`
(the left parent at index `2k+1` is the appended symbol `1`), and
`new''[i] = CONE[new'[i+1]][new''[i+1]]` for `i = 2k-1 .. 0`. Put
`sigma(t) = (new'[2k-t], new''[2k-t])`, `t = 0..2k`. Then `sigma(0) = (2, 2)` and
`sigma(t+1) = STEP(sigma(t), column[2k-t]) = STEP(sigma(t), D[t mod 28])` by `S(k)`.
The input does not depend on `k`, so `sigma` is one fixed sequence, and
`column_{k+1} = new'' + [2]` has

```text
column_{k+1}[2k+2] = 2 = D[0],  column_{k+1}[2k+1] = 1 = D[1],  column_{k+1}[2k] = 2 = D[2]
column_{k+1}[2k-1-t] = sigma(t+1)_y                       t = 0 .. 2k-1
```

`S(k+1)` asks `column_{k+1}[i] = D[(2k+2-i) mod 28]`, i.e. the three bottom identities
(check `column_step_bottom_three_cells`, line 7) and `sigma(t+1)_y = D[(t+3) mod 28]`
for `t = 0..2k-1`. The check `column_step_outputs_one_period` (line 8) verifies the
latter for `t = 0..27`, and `column_step_state_return_sigma(28)=sigma(0)` (line 9)
verifies `sigma(28) = sigma(0) = (2, 2)`. Since the input `D[t mod 28]` is
28-periodic from `t = 0`, `sigma(t + 28) = sigma(t)` for all `t >= 0` by induction on
`t`, so the identity holds for every `t`, for every `k` at once [U over C].

Anti-diagonal step. The first append sets `diag'[0] = new'[0]` and
`diag'[j+1] = CONE[diagonal[j]][diag'[j]]` for `j = 0..2k-1`; the second sets
`diag''[0] = new''[0]` and `diag''[j+1] = CONE[diag'[j]][diag''[j]]` for `j = 0..2k`.
Put `tau(j) = (diag'[j], diag''[j])`. Then `tau(0) = sigma(2k) = sigma(2k mod 28)`,
`tau(j+1) = STEP(tau(j), diagonal[j]) = STEP(tau(j), D[(2k+j) mod 28])` for
`j = 0..2k-1` by `S(k)`, and the last cell `diag''[2k+1] = CONE[diag'[2k]][diag''[2k]]`
is the `y`-component of `STEP(tau(2k), z)` for any `z`. `diagonal_{k+1} = diag''` and
`S(k+1)` asks `diag''[j] = D[(2k+2+j) mod 28]` for `j = 0..2k+1`. The seed and the
input phase depend on `k` only through `r = k mod 14`. For each `r = 0..13` the check
`diagonal_step_r=rr_outputs_and_return` (lines 10 to 23) starts at
`tau_0(r) = sigma(2r mod 28)`, reads `D[(2r + j) mod 28]` for `j = 0..27`, verifies
`tau(j)_y = D[(2r + 2 + j) mod 28]` for `j = 0..28`, and verifies `tau(28) = tau_0(r)`.
By 28-periodicity of the input, `tau(j + 28) = tau(j)` for all `j`, so the identity
holds for `j = 0..2k+1` for every `k = r (mod 14)`, including the cases `2k + 1 < 28`
where the window is shorter than one period (the checked outputs are then a prefix)
[U over C]. The fourteen seeds `tau_0(r)` are printed on lines 10 to 23; all fourteen
return.

Together: `S(2)` and `S(k) => S(k+1)` for all `k >= 2`, so `S(k)` holds for every
`k >= 2` [U over C]. This is the proof `RESULTS-ALTERNATING-FAMILY.md` section 2
outlined and did not do. Note the column induction needed no phase tracking at all:
read bottom up, the column is `D` from index 0 at every `k`, and the phase lives
only in the anti-diagonal (fourteen cases).

### 2.2 The six cut cells are a function of k mod 448, for every k >= 2

Fix a pattern `S = (s_1, ..., s_6) in {1,2}^6` and append it after `(12)^k`. The
six-component lockstep column pass starts at index `2k` from
`sigma_S(0) = column_init(S)`, the values `new^(l)[2k]` for `l = 1..6`, computed from
the triangle of the six appends below index `2k`, which reads only the appended
symbols; then `sigma_S(t+1) = STEP(sigma_S(t), D[t mod 28])` for `t = 0..2k-1`. The
anti-diagonal pass starts from `tau_S(0) = sigma_S(2k)` and reads
`tau_S(j+1) = STEP(tau_S(j), D[(2k+j) mod 28])` for `j = 0..2k-1`. Its final state
`V_S(k) = tau_S(2k)` has `l`-th component `T[2k+l][2k]`, the cut cell of the `l`-th
append. That this lockstep reproduces `Endpoint.peek` is the check
`lockstep_matches_kernel_all_64_patterns_k=2..30` (line 24): all 64 patterns, all
`k = 2..30`, both the seed vector and the cut vector [C]; that it does so for all `k`
is the recurrence itself, given `S(k)` [U].

Periodicity. Let `F_phi` be the map on `{0..3}^6` given by 28 successive `STEP`s reading
`D[phi], D[phi+1], ..., D[phi+27]`. Each `STEP(., z)` is a bijection, so `F_phi` is a
permutation and every orbit is a pure cycle. The check
`one_period_map_orders_all_even_phases_m=6` (line 25) computes the order of `F_phi`
for every even `phi`: 64 at all fourteen phases [C]. For `k' = k + 14q`, the column
read `D[0..2k'-1]` is `D[0..2k-1]` followed by `q` periods from phase `2k mod 28`, so
`sigma_S(2k') = F_{2k}^q(sigma_S(2k))`; the anti-diagonal read `D[2k'..4k'-1]` has the
same phase as `D[2k..4k-1]` (`28q` is a multiple of 28) and is that word followed by
`q` periods from phase `4k mod 28`, so `V_S(k') = F_{4k}^q(h(sigma_S(2k')))` with `h`
the fixed `2k`-symbol read. With `q = 64` both `F`s are the identity, hence
`V_S(k + 896) = V_S(k)` for every pattern `S` and every `k >= 2` [U over C]. The
forced pattern is determined by these vectors: `s_1` is the `s` whose `V_(s,...)(k)_1`
has high bit 1, and given `s_1..s_{m-1}`, `s_m` is the `s` whose `V(k)_m` has high
bit 1; exactly one `s` qualifies at each step because, by the high-bit law (line 4),
`H` of every cell of the new column, and then of every cell of the new
anti-diagonal, changes by the same amount when the seed `BOUNDARY[s]` changes, and
`BOUNDARY[1]`, `BOUNDARY[2]` have opposite high bits (line 5) [U]. Hence the forced
pattern, the six cut cells and the six defect bits are `896`-periodic in `k` for
`k >= 2`: `P_0 = 896`, `k_0 = 2`, no residues excluded.

Census. `census(1793)` recomputes, from `Endpoint` alone, the six forced symbols and
six cut cells for every `k = 2..1793` (two full periods `P_0`); uniqueness of the
forced symbol is asserted at each of the `6 x 1792` steps (line 27), and the values
agree with `psi()` for `k = 2..60` (line 28, the range of `alt_family.log`) [C].
`V(k + 896) = V(k)` holds on the whole census (line 29) [C]. The minimal period of the
cut-cell vector among the divisors of 896 is `P = 448` (line 30); since `448 | 896`
and the infinite sequence is 896-periodic, a 448-periodic block of length 896 makes
the whole sequence 448-periodic [U]. The forced symbols have period 224, `k_E(2)` has
period 28 and `k_E(3)` period 224 (lines 31, 39) [C]. Spot checks at `k = 5672, 7777,
10000`, built symbol by symbol in the kernel, agree with the residue prediction
(line 42) [C].

### 2.3 The bound, and the kill

`k_E(2) <= 3` for every `k >= 2`: maximum 3, attained at `k = 22, 25 (mod 28)` (line
32, histogram `{0: 1024, 1: 256, 2: 384, 3: 128}` line 33) [U over C, via 2.2].

`k_E(3) <= 5` fails. Over `k = 2..1793` the histogram is `{0: 768, 1: 384, 2: 224, 3:
208, 4: 128, 5: 72, 6: 8}` (line 34): eight values of `k`, exactly the residue
`k = 144 (mod 224)`, have all six inspected cut cells equal to `3` (low bit 1), so
`k_E(3) >= 6` there and the check `k_E(3)<=5_all_residues_mod_448_and_k=2..1793`
fails with `max = 6` (line 36). The witness script runs `psi((12)^144)` in full: forced
prefix `21212222`, cut cells `3 3 3 3 3 3 2 3`, defect word `111111011000...`,
`k_E(2) = 0`, `k_E(3) = 6`, `n + 2 = 290` (`witness_k144.log` line 1); the residue mate
`k = 368` gives the same first seven cells (line 2) [K for the bound, C for the
values]. The first `k` with five constant cells is `k = 5` (log line 41, first
sixty values of `k_E(3)`; `witness_k144.log` line 3), matching `alt_family.log`.

The pre-registration's own kill conditions (a transducer state that does not return
after one period; a cut sequence that is no function of `k mod P` for any
`P <= 448`) did not fire: every state returns and `P = 448`. The task rule that any
failing check is the kill did fire, on the pre-registered numeric bound. The script
exits 1 and prints `KILL FIRED` (line 44); it was not modified after the run, and the
seventh cell was not added to it.

## 3. Reading

What is established is stronger structure than `RESULTS-ALTERNATING-FAMILY.md`
recorded and a weaker bound than it extrapolated. The endpoint state after `(12)^k`
is one period-28 sequence `D` indexed by `2k + d`, and appending `12` is the shift
`D[t] -> D[t+2]` on that sequence, proved by a 28-step state return for the column and
fourteen for the anti-diagonal. Six further forced appends read the same `D` through
a permutation of `4^6` states of order 64 at every phase, which is why the cut cells
are `14 x 64`-periodic and, in fact, `448`-periodic. The order 64 is `2^6` for six
components, the iterated `D8` structure the task brief predicted; the script does
not compute the orders at smaller depths and this report does not state them.

The bound `k_E <= 5` was a census artifact. `k_E(3)` has period 224 on `k >= 2`, so
the census to `k = 60` saw 59 of 224 residues; the residue `144` is the unique one
with six constant cells, and its value 6 first appears at `k = 144`. `(PSI)` on the
family is not in doubt numerically (`k_E(3) = 6` against `290` at `k = 144`), but the
pre-registered statement was `<= 5`, it is false, and this run does not replace it.
A follow-up needs a new pre-registration with the depth fixed at seven (or more) and
the bound stated before the run; the machinery here transfers verbatim
(`DEPTH = 7` gives `4^7` states, expected order 128, `P_0 = 1792`, a census to
`k = 3585`, under a minute). Whether `k_E(3) <= 6` for all `k` is then a fresh finite
question with the same shape, and the same risk that a longer period hides a larger
value; the structural guarantee is only that `k_E(c)` restricted to any fixed depth
is periodic in `k`, not that it is bounded by the depth.

Nothing here touches `RW`, `(SEP)`, `(PT2)`, or `(PSI)` off the family; the family has
measure zero among sources, and the anti-diagonal of its one-defect perturbation is a factor of the
period-28 sequence at no cell with `a <= 40`, `b <= 95` (`RESULTS-ALTERNATING-FAMILY.md` section 3: a finite grid, not a proof).

## 4. Scope

Proved for every `k >= 2` [U over C]: the closed form `S(k)`; `896`-periodicity of the
first six forced symbols, cut cells and defect bits, sharpened to `448` by the census;
`k_E(2) <= 3`; and, by the same proved 448-periodicity [U over C], `k_E(3) <= 5` on
every residue `k mod 224` except 144, hence for all `k >= 2` with `k != 144 (mod 224)`;
on `k = 144 (mod 224)` only `k_E(3) >= 6` is established by the depth-six script, and
`k_E(3) = 6` at `k = 144` and `368` by the witness. The residue 144 is closed by the
depth-seven rerun of section 6, which gives `k_E(3) <= 6` for every `k >= 2`. One implementation (`psi_kernel.py`, gated against its reference by
`validate()`; not re-implemented here). All checks are exact integer computations, no
floating point, single process, 30 seconds.

## 5. Reproduction

From `experiments/rule30/p1-period2-invariant/`:

```sh
uv run --no-project python alternating-family/psi_alternating_proof.py   # 30 s, exit 1, 44 lines
uv run --no-project python alternating-family/witness_k144.py             # 1 s, exit 0, 3 lines
```

The proof script prints every check as `PASS name` or `FAIL name [witness]`, the
rigorous period bound, the census maxima and histograms, and ends with
`ALL ... CHECKS PASS` (exit 0) or `KILL FIRED: ...` (exit 1). Its constant `D` is
asserted against `Endpoint` by the first check that uses it (`S(k)_direct`), so a
wrong `D` cannot pass silently.

## 6. Depth seven: the theorem

Pre-registered the same day in `PREREGISTRATION-PSI-ALTERNATING-DEPTH7.md` (claim
`k_E(2) <= 3`, `k_E(3) <= 6` for every `k >= 2`; kill: a residue with seven constant cut
cells `3`, or four constant cells `2`, or a state-return or census failure). Script
`alternating-family/psi_alternating_proof_depth7.py`, a copy of the depth-six script
differing only in `DEPTH = 7`, the two bound checks, and the `psi()` comparison being
truncated to `min(DEPTH, n + 2)` symbols (the `diff` is five hunks). Log
`alternating-family/psi_alternating_proof_depth7.log`, exit 0, 33 checks PASS.

**`[U over C]` For every `k >= 2`: `k_E(2) <= 3` and `k_E(3) <= 6` on `(12)^k`; hence
`(PSI)` holds on the alternating family at every `k >= 2`, with slack `2k - 4` at
`c = 3`.** The one-period map on `4^7` states has order 128 at all fourteen even phases
(log line 25), so the seven forced symbols, cut cells and defect bits are `1792`-periodic
in `k` for `k >= 2` by the argument of section 2.2 verbatim; the census over
`k = 2..3585` (two periods) confirms it (line 29), the minimal period of the seven cut
cells is `896` and of the seven forced symbols `448` (line 30), `k_E(2)` has period 28 and
`k_E(3)` period 224 as before (line 39), and the maxima over all residues are 3 and 6
(lines 35, 36; histograms lines 33, 34: `k_E(3) = 6` on 16 of 3584 values, the residue
`144 (mod 224)`, and never 7). Spot checks at `k = 6344, 7777, 10000` built in the kernel
agree with the residue prediction (line 42). The kill did not fire.

What the theorem needs from the structure is only that the first seven cut cells are a
function of `k mod 1792`, which is proved for every `k >= 2`; the bound itself is then the
finite check over one period. It is a statement about a measure-zero family and touches
nothing off it.

```sh
uv run --no-project python alternating-family/psi_alternating_proof_depth7.py   # 90 s, exit 0, 44 lines
```

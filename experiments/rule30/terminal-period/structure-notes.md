# Terminal-period structural lemmas and independent core review

Date: 2026-09-09. These notes accompany the terminal-period investigation;
they do not claim that its target theorem has been proved.

Evidence: `U` denotes a uniform mathematical argument, `R` a reduction,
`C` a finite verified check, `M` a measurement, and `K` a killed candidate.

## 1. The driven two-step boundary map (`U`, small `C` check)

Put `a_j = x(T0+2n,j)` for `j>=1`, and let `b_j` be the next row.
The centre at these two updates is respectively zero and one. Therefore

```text
b_1 = a_1 OR a_2,
b_2 = a_1 XOR (a_2 OR a_3),
rho_(n+1) = 1 XOR (b_1 OR b_2)
          = NOT(a_1 OR a_2 OR a_3).
```

The last identity follows by splitting on `a_1`: when it is one the first
OR input is one; when it is zero their OR is `a_2 OR a_3`.

Thus every occurrence of `rho_(n+1)=1` pins the preceding even row's first
three right cells to zero. If that preceding row starts `000uv`, its next
even row starts

```text
1, u, u OR v.
```

This is a genuine OR-dependent return mechanism, but it does not specify
the unrestricted farther-right tail. A finite-state return-map claim
must prove that tail information can be discarded or summarized.

The two-step identity was checked on all 32 five-cell seeds against the
unchanged `right_trace_forbidden.numeric_rho`. All four triple-zero reset
cases also passed the scalar update check. No longer census was run.

## 2. Exact gap reformulation of the frozen factors (`U`)

For a cyclic rho word, `11` and `00000` exclusion imply that the numbers
of zeros between successive ones belong to `{1,2,3,4}`. The remaining
five frozen factors translate exactly to forbidden cyclic gap blocks:

| Binary factor | Gap block |
|---|---|
| `101001` | `12` |
| `0100101` | `21` |
| `010010001` | `23` |
| `0101000101` | `131` |
| `0101010000` | `114` |

Any leading zero required by the binary factors is present because every
gap is positive. In the last row the terminal four zeros force gap four,
using the five-zero exclusion. Conversely each displayed binary factor
exhibits the stated gap block.

The desired terminal cyclic gap sequences are precisely

```text
1^omega, 2^omega, 4^omega, (41)^omega.
```

This is a useful representation of the desired conclusion, not an
independent proof of it. In particular neither the alphabet `{1,2,3,4}`
nor the five gap exclusions already force the terminal set.

## 3. A sparse core gives an eventual forbidden mask (`U`)

Suppose a finite right-cone CNF consists only of Rule 30 transition
clauses, the fixed alternating centre drive, and selected assertions

```text
rho_(a+d) = e_d,   d in D,
```

where `D` is finite, contains zero, and `a>=0`. If that CNF is UNSAT,
then for every actually driven infinite right half and every `p>=a`,
the assertion `rho_(p+d)=e_d` for all `d in D` is impossible.

Proof. Start the same finite cone at macro time `p-a`. Its initial right
row is the actual row at that time, which is an allowed choice because
all initial right cells in the cone are free. Its centre drive still has
zero phase because the shift is an even number of original time steps.
The selected samples would satisfy every remaining unit, contradicting
UNSAT. This proof also applies after any eventually alternating onset.

For a finite collection of such cores, `B=max a` is a common burn-in:
the entire tail `rho[B:]` avoids every normalized mask. Removing `a`
without retaining this burn-in is invalid in general: the two-step
driven map need not be onto its initial-state space.

Example. The selected core for the existing `h=4` certificate asserts
samples `[23,25,27,29,31]` equal `[1,0,1,0,1]`. Hence the normalized mask
`1?0?1?0?1` cannot start at any sample `p>=23`. With `11` excluded, all
four question marks must be zero, so consecutive gap block `33` is
eventually impossible. This excludes infinitely many periodic words,
including every periodic gap word containing `33`, without enumerating
their periods.

## 4. What a finite graph closure would really prove (`U`, conditional)

Let a finite collection of sound eventual masks be given. Expand the
masks into their finitely many concrete forbidden words and build the
usual finite suffix graph. If its only recurrent components are the
four simple cycles spelling the desired rho necklaces, then **every**
actual driven rho is eventually one of those four periodic sequences.

Proof. By the previous lemma, after a common burn-in every actual trace
is an infinite path in this finite graph. The condensation graph of its
strongly connected components is a finite DAG. An infinite path
eventually remains in one recurrent component; if that component is a
simple cycle, its labels are thereafter periodic. The onset of the final
cycle need not have a common bound, since a path can traverse a cycle
arbitrarily many times before exiting to another component.

Consequently such a graph certificate would be stronger than the stated
periodic-only target: it would also exclude the aperiodic neighbour
branch under an eventually alternating centre. This stronger conclusion
is legitimate only after actual graph closure is verified. A finite
regression through `h=15` cannot substitute for the graph proof.

Conversely a periodic-only theorem does not inherently have a uniform
finite forbidden-factor proof. An elementary abstract example is the
shift that forbids every block `1 0^a 1 0^b 1` with `b<=a`. Its only
periodic point is all zeros, but it admits a non-eventually-periodic
sequence with successive zero gaps `1,2,3,...`. Every finite subset of
its forbidden words misses `(1 0^N)^omega` for sufficiently large `N`.
Thus finite cone obstructions for every prohibited periodic word need
not have a common length bound.

## 5. Compactness and the temporal-period lifting gap (`U/R`)

For one prescribed infinite rho, let `E_n` be the set of initial right
half-rows producing its first `n` samples. Each `E_n` is a clopen cylinder
set determined by `2n-1` initial cells, and `E_(n+1)` is contained in
`E_n`. Compactness gives

```text
rho is right-realizable iff E_n is nonempty for every n.
```

Hence every unrealizable specified periodic rho has some finite
obstruction. This is pointwise compactness; it supplies no uniform bound
on cone depth over different primitive periods.

There is a related finite-strip observation. Fix width `W` and a rho of
period `h`. At each original time record the `W` right cells and time
modulo `2h`. Permit a transition exactly when the internal Rule 30
updates hold and some freely chosen exterior right cell supplies the
last update, while the prescribed rho and alternating centre constraints
hold. There are at most `2h * 2^W` states. Any genuine realization gives
an infinite path, which implies a directed cycle and a temporally
periodic realization of this width-`W` strip, with period a multiple of
`2h` and at most `2h * 2^W`.

The cycle and its period may change with `W`; its freely supplied exterior
boundary need not extend one more column. Thus this argument does not
produce a full diagram with one common temporal period, or a torus. The
missing assertion is a **uniform compatible temporal-period lifting
lemma**. Same-period spatial orbit counts cannot replace it.

## 6. Canonical prefix nonmonotonicity (`U`)

For one unrealizable periodic word of primitive period `h`, let `N_r`
be the shortest infeasible prefix length at phase `r` modulo `h`.
An infeasible prefix at phase `r+1` is a suffix of a prefix one symbol
longer at phase `r`, so

```text
N_r <= 1 + N_(r+1),
max_r N_r - min_r N_r <= h-1.
```

These inequalities explain why phase contributes to prefix-length
variation. Across different words there is no corresponding monotonicity
in `h`: onset delays, locations of a sparse contradictory pattern, and
the pattern itself can differ. The observed nonmonotone canonical
lengths are consistent with local mechanisms, but they prove neither a
shared mechanism nor a common cone-depth bound. Normalized sparse cores
are stronger evidence because their selected literals give the actual
pattern and their earliest selected index gives an explicit burn-in.

## 7. Rule 90 distinction (`U`, small `C` check)

Under Rule 90 the same two updates give

```text
rho_(n+1) = 1 XOR a_1 XOR a_3.
```

There is no three-zero OR pin. The identity was checked against the
unchanged `numeric_rho(..., rule30=False)` on the same 32 seeds.

More generally, Rule 90's finite driven evolution is affine over the
initial right cells. At time `2n` and position one, the coefficient of
initial cell `2n+1` is one: the unique ancestral path reaching that
rightmost site takes the right input at every update. Every other
initial variable in that output has index at most `2n`; the prescribed
drive contributes only a constant. Thus

```text
rho_n = x(0,2n+1) XOR H_n(x(0,1),...,x(0,2n)),
```

with affine `H_n`. Choose all even-indexed initial cells arbitrarily and
then choose each odd-indexed cell recursively to match an arbitrary
prescribed rho. This constructs an infinite right row realizing every
rho, including every primitive period. It follows directly that no
nonempty consistent sample mask can be UNSAT for Rule 90's free right
cone. The OR-dependent Rule 30 masks do not transfer to this control.

## 8. Independent review of the core extraction (`C`, source audit)

`core_analysis.py:clause_metadata` reconstructs and compares every source
clause with the scalar Rule 30 truth table and boundary bit `t%2`. It
also reconstructs exactly the rho observation units. Boundary transition
clauses have three literals and interior clauses four; initial right
variables are unrestricted. Thus selecting all clauses of length greater
than one retains exactly the transition base and removes **all** original
rho observations.

`minimal_assumptions` runs its deletion tests against that transition
base, rechecks the retained set as UNSAT, and verifies that every single
retained-unit deletion is SAT. Its initial-row models are replayed with
the unchanged `numeric_rho`, including the expected disagreement at the
deleted sample. `certify_selected_core` persists exactly the transition
base plus the selected observation units, generates a new DRUP proof,
and parses and rechecks the persisted artifacts with the frozen checker.

No hidden original rho pins, spatial wrap, temporal wrap, or farther
column periodicity was found in this independent source review. These
are deletion-minimal sample cores relative to the full transition base,
not minimum-cardinality cores and not minimal sets of transition clauses.

## Honest scope

The three-zero return, eventual-mask transfer, gap translation,
compactness, finite-strip lifting limitation, and Rule 90 surjectivity
are proved above. The sample-core extraction has a separate source audit
and finite certificate checks. A terminal-period theorem requires the
eventual-mask graph actually to close, or a further uniform argument
excluding its residual periodic cycles. These notes do not infer that
closure from the existing census or from a finite list of cone lengths.

The actual `core-factor-results.json` graph does **not** close. Its 15
normalized masks, with common burn-in 23 samples, together with the
previous factors produce 45 irredundant concrete factors and a graph
with 557 states and 718 edges. A recurrent component has 287 states,
350 internal edges, and 63 branching states. At suffix `0100100100`,
both words

```text
A = 0010000100100100,
B = 100
```

return to the same state. Therefore `A B^k` supplies periodic words
avoiding every tested eventual restriction for all `k>=0`. Their
canonical representatives are

```text
00001 00001 (001)^(k+2),  h=16+3k,
```

with cyclic gap words `[4,4,2^(k+2)]`. Each is primitive: the circular gap
word has a unique adjacent pair `44`, so any rotational symmetry fixes
that distinguished position and is trivial. The loop proof establishes
avoidance for every `k`; checking selected values is only a consistency
check. Avoidance is not right-realizability.

An independent reconstruction from the 45 concrete factors, using all
their proper prefixes and the longest-suffix transition rule, confirmed
all 557 states and all 718 allowed edges in the saved graph. It also
confirmed both displayed loops and the canonical `k=0` representative
`0000100001001001`.

The specific remaining obstruction is the **unbounded periodic-return
gap**: these necessary restrictions permit returning from a pair of
four-zero gaps through arbitrarily long runs of two-zero gaps and back.
A further argument must exclude such returns uniformly or impose enough
new constraints to eliminate the recurrent graph branches. Eliminating
one or finitely many values of `k` does not establish that statement.
This failure is fully compatible with the exact 4,720-necklace
regression through `h=15`.

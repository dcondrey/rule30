# Small active-core resolution cores and Boolean interpolants

Date: 2026-09-01

Status: **EXACT FINITE CERTIFICATES; THE TRANSLATION-STABLE MOTIF FAILS AT
THE NEXT CUT.**  This does not prove active-core mortality or the period-two
theorem.

## 1. Certified diagonal instances

For `C(4,5)`, `C(5,6)`, and `C(6,7)`, the retained artifact directory contains
the original CNF, a Glucose DRUP proof, a deletion-irreducible clause core,
and a second DRUP proof of that core.  Every proof addition is independently
checked by the repository's RUP checker.

| instance | variables | clauses | checked DRUP additions | irreducible core clauses | core-proof additions |
|---|---:|---:|---:|---:|---:|
| `C(4,5)` | 130 | 438 | 22 | 123 | 15 |
| `C(5,6)` | 192 | 651 | 56 | 171 | 21 |
| `C(6,7)` | 266 | 906 | 50 | 421 | 99 |

The clause cores are irreducible, not minimum-cardinality claims: deleting
any one retained original clause makes that guarded core satisfiable.

## 2. Craig partition and exact interpolants

For `H=m+1`, use the exact vertical-cut partition already proved in
`RESULTS-CORE-INTERPOLANT.md`:

```text
A_H = prefix cuts R_H reachable from zero by at most H-2 symbols,
B_H = inverse-terminal-cone hard-core cuts S_H.
```

The only shared variables are the high/low bits `(h_i,l_i)` of the `H` cut
states.  For each of `H=5,6,7`, the generator enumerates all prime clauses of
width at most six that are true on `R_H` and false on at least one point of
`S_H`.  Exact weighted MaxSAT then finds a CNF with the minimum number of such
clauses, breaking ties by total width.  A separate cardinality SAT check
proves that one fewer candidate clause cannot cover `S_H`.

The resulting CNF `I_H` is checked pointwise on the complete exact projections:

```text
A_H implies I_H,
B_H implies not I_H.
```

Thus `I_H` is a Craig interpolant for the cut partition.  It is deliberately
not described as the syntactic interpolant of the unlabelled DRUP trace;
DRUP does not retain the colored resolution antecedents needed for that
claim.

One deterministically selected minimum-count interpolant at each cut is:

```text
I_5 = (NOT l_0 OR l_2)
    AND (l_1 OR h_3 OR NOT l_4)
    AND (h_2 OR NOT l_2 OR l_3).

I_6 = (l_2 OR NOT l_4)
    AND (NOT l_0 OR h_2 OR NOT h_3 OR l_5)
    AND (NOT h_0 OR l_0 OR NOT h_1 OR l_1 OR NOT l_2)
    AND (h_0 OR NOT l_0 OR NOT h_1 OR NOT l_2 OR h_3).

I_7 = (l_2 OR NOT l_6)
    AND (NOT l_0 OR l_2 OR h_5 OR NOT h_6)
    AND (h_2 OR NOT l_2 OR NOT h_3 OR l_3)
    AND (NOT h_0 OR l_0 OR NOT h_1 OR l_1 OR NOT l_4)
    AND (h_0 OR NOT l_0 OR NOT h_1 OR h_3 OR NOT l_4).
```

Their clause counts are `3,4,5` and their total widths are `8,16,20`.
Minimum count does not imply uniqueness; the JSON artifacts retain the exact
chosen clauses and their accepting-set coverage.

## 3. Translation motif and exact failure

Among the enumerated width-at-most-six prime clauses, normalizing cut
positions by translation leaves exactly three templates common to
`H=5,6,7`:

```text
h_i     OR NOT h_(i+2) OR NOT l_(i+3),
NOT l_i OR NOT h_(i+1) OR     h_(i+3),
l_i     OR NOT h_(i+3) OR NOT l_(i+4).
```

The first template initially looks strongest: for `H=5,6,7` it is valid at
every position `1 <= i <= H-4`.  It does not extend.  At `H=8` every allowable
translation of every one of the three common templates is falsified by a cut
in `R_8`.  For the first template the shortest recorded witnesses include

```text
i=1: prefix 110000 -> cut 11133113,
i=2: prefix 101000 -> cut 01113311,
i=3: prefix 101000 -> cut 01113311,
i=4: prefix 101101 -> cut 00100031.
```

The manifest records a shortest prefix/cut witness for every failed
translation.  This fires the preregistered kill condition for these specific
small-width interpolant motifs.  Since the candidate clauses already fail
basic reachability at `H=8`, none can be closed under the matched-extension
identity without adding a richer, width-dependent state.

This failure does not refute a nonlocal Boolean interpolant schema or the
matched-extension lemma itself.

## 4. Scope

The calculation gives exact, independently checkable finite UNSAT artifacts
and an exact negative result for the only translation-normalized prime-clause
motifs shared by these three cuts.  It gives no induction in `m`, no uniform
intermediate lemma, and no period-two mortality theorem.

Also, the radius-two Farkas contradiction in `RESULTS-BELLMAN-RADIUS2.md`
kills that posted energy system only; it does not prove impossibility of all
finite-radius linear potentials.

## 5. Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/core_resolution_interpolants.py
```

The command regenerates all CNF, proof, core, interpolant, digest, and motif
records under `core-diagonal-interpolants/` and asserts every verification
condition before writing the final manifest.

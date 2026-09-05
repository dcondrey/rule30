# Hard-core assumptions are absent from almost every finite DLP refutation

Date: 2026-09-02

Status: **THE PREREGISTERED HELD-OUT RANGE PASSED THROUGH `n=15`.  THIS IS
FINITE EVIDENCE FOR A SIMPLER DIAGONAL EXCLUSION, NOT AN ALL-LENGTH PROOF.
PERIOD TWO AND P1 REMAIN OPEN.**

## 1. Question

The late-pull diagonal CNF originally imposes both:

1. a source word `W in {1,2}^n`; and
2. a hard-core forced continuation, meaning no adjacent `11`.

`late_pull_hardcore_core.py` guards every continuation no-`11` clause by a
separate assumption literal.  It first asks whether the formula is already
UNSAT with none of those assumptions.  Only if the relaxed formula is SAT
does it extract and deletion-minimize an assumption core.

## 2. Exact result

There are `15*2*3=90` tail/residue formulas through `n=15`.  Of these:

```text
88 are UNSAT without any continuation no-11 clause;
 2 are SAT after that relaxation and need a no-11 clause.
```

The two exceptions are exactly:

```text
n=5, tail=3, residue=1;
n=6, tail=2, residue=1.
```

In each exception an inclusion-minimal core has size one.  The selected
position is not canonical because several singleton clauses can kill the
same relaxed family.

The exploratory range was `n<=11`.  In the preregistered held-out range
`12<=n<=15`, all 24 formulas were base-UNSAT:

| `n` | tail 2 residues `0,1,2` | tail 3 residues `0,1,2` |
|---:|:---:|:---:|
| 12 | base-UNSAT, base-UNSAT, base-UNSAT | base-UNSAT, base-UNSAT, base-UNSAT |
| 13 | base-UNSAT, base-UNSAT, base-UNSAT | base-UNSAT, base-UNSAT, base-UNSAT |
| 14 | base-UNSAT, base-UNSAT, base-UNSAT | base-UNSAT, base-UNSAT, base-UNSAT |
| 15 | base-UNSAT, base-UNSAT, base-UNSAT | base-UNSAT, base-UNSAT, base-UNSAT |

Lengths 16--20 were not run.  Runtime rose sharply at 15, and extending a
bounded SAT table does not address the missing induction.

## 3. Consequence and limit

The data say that, outside two small exceptions, the binary source and the
constant-cut equalities themselves appear to prevent the terminal late
pull.  The actual-right hard-core condition is probably not the mechanism
behind the diagonal contradiction.

This matters because it moves the proof search away from forbidden-factor
automata and toward the triangular binary-source boundary.  It does **not**
permit dropping hard-core from the theorem: the observation has only been
checked at finite lengths.

The independent binary-wedge experiment in
`RESULTS-BINARY-WEDGE-HORIZON.md` makes the same simplification more sharply.

## 4. Controls and reproduction

For every nonempty assumption core the program verifies that the base
formula is SAT, the core is UNSAT, every one-clause deletion is SAT, and the
relaxed model replays literally with an adjacent-`11` violation.

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/late_pull_hardcore_core.py \
  --first-n 1 --last-n 15
```

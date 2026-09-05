# Preregistration: variable-seed mortality certificates

Date: 2026-09-01

## Exact theorem target

Prove that every finite hard-core rho seed in the alternating Rule 30 fiber
eventually violates either the right-column `no 11` constraint or a forced
left pin.  Together with the exact bilateral reduction already established,
this would exclude the two nonconstant period-two center traces for every
nonzero finite configuration.

## New combination being tested

Combine two previously separate attempts:

1. the exact Gray-OR forced-frontier recurrence, which removes every free
   boundary choice after a finite rho seed; and
2. proof-complexity instrumentation, now applied to a variable-input UNSAT
   statement rather than a fixed seed whose output is forced by unit
   propagation.

For seed length `n` and continuation horizon `H`, construct a CNF
`M(n,H)` whose free inputs are the `n` rho bits.  It asserts:

- the seed contains no adjacent ones;
- the exact two-row frontier is constructed from that seed;
- each of the next `H` forced macrosteps has zero at both new deep-left
  boundary cells (equivalently, the forced zero phase and pin phase pass);
- the forced rho bit at every continuation preserves `no 11`.

Thus `M(n,H)` is satisfiable exactly when some hard-core seed of length `n`
survives at least `H` post-seed macrosteps.

## Registered primary sweep

- `n = 1,...,24`;
- primary horizon `H(n) = 2n+2`;
- complete threshold cross-check for `n <= 16`: SAT at `H <= maximum
  survival`, UNSAT at `H = maximum survival + 1`;
- Glucose DRUP proof capture for primary UNSAT instances, with the raw proof
  checked by an independent RUP/DRAT checker implemented separately from the
  encoder;
- direct transducer enumeration used as an independent semantic oracle for
  every `n <= 16` threshold instance.

The values 24 and `2n+2` are fixed before the substantive sweep.  Enlarging
them later will be labeled exploratory.

## Structural measurements

For every instance record variables, clauses, solver decisions,
propagations, conflicts, wall time, proof lines, and maximum proof-clause
width.  Also normalize every non-deletion proof clause by its frontier layer
and search only for exact repeated clause templates across consecutive `n`.

The intended success is not a short list of UNSAT answers.  It is one of:

- a bounded collection of layer-normalized clauses forming an inductive
  mortality certificate;
- a recurrence that mechanically expands the certificate for `n` to the
  certificate for `n+1`; or
- a closed finite algebra of parity/correlation observables explaining the
  repeated clauses.

Any such schema must be verified for symbolic `n`, or reduced to a fixed
finite transition table whose entries are checked exhaustively.

## Quadratic-form side probe

Instrument the inverse-Gray correlation explicitly.  If `P` is suffix XOR,
then over `F_2`

```text
<P x, P y> = x^T K y,
K[i,j] = (min(i,j)+1) mod 2.
```

Check this identity exhaustively at small widths and track whether the pin
recurrence closes over parity split by index parity plus the corresponding
upper/lower triangular correlations.  This probe succeeds only if the
observable family has size bounded independently of width.  Growth in
degree, rank, or the number of necessary triangular forms is a registered
negative.

## Controls

- Compare CNF satisfiability with `hard_core_survival` for every seed through
  length 16 and every threshold through the first failure.
- Decode every SAT model back to its seed and replay it with the independent
  integer transducer.
- Check every captured UNSAT proof independently; solver status alone is not
  a certificate.
- Dropping the post-seed deep-left zero constraints must admit models, so the
  harness does not manufacture mortality solely from seed hard-core clauses.
- Preserve the existing Rule 90 finite constant-zero-trace counterexample;
  no conclusion may be transferred from OR to XOR.
- Preserve the known infinite-left spatial-period-seven survivor as evidence
  that finite-left support is an essential hypothesis, not a cosmetic one.

## Kill conditions

Record a negative rather than moving the goalposts if:

- the CNF and direct transducer disagree on any threshold instance;
- a primary instance is SAT (this kills `H(n)=2n+2`, not the theorem);
- proof checking fails;
- proof size or normalized template count grows without an exact recurrence;
- all refutations reduce to a whole-instance propagation chain and reveal no
  reusable intermediate lemma;
- the quadratic observable family grows with width;
- a claimed invariant also excludes the infinite-left survivor or the Rule
  90 control.

## Interpretation boundary

Finite UNSAT results, even through `n=24`, do not prove the Rule 30 theorem.
A solution requires a uniform certificate for all finite seed lengths and a
fully checked reduction from a periodic center trace to this mortality
statement.  Conversely, a SAT result here only refutes the registered linear
horizon; it need not produce an immortal seed.

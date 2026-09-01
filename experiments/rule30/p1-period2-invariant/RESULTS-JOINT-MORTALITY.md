# Joint left-finite/right-realizable mortality

Date: 2026-09-01

Status: **OPEN.  THE EXACT JOINT HORIZON-EIGHT CNF IS UNSAT THROUGH SEED
LENGTH 31, BUT NO UNIFORM PROOF IS KNOWN.**  Finite forbidden-factor
approximations produce moving counterexamples, so neither finite UNSAT nor a
fixed short list of right factors is being promoted to a theorem.

## 1. Exact coupled statement

For a seed length `n` and post-knee horizon `H`, `J(n,H)` combines two exact
constructions.

1. The first `n` rho bits build the forced alternating-center left frontier.
   Each later macro must emit a zero at both new deepest cells and pass the
   center pin.
2. All `n+H` rho bits are equated to the even-time column-one trace of an
   independently Tseitin-encoded genuine Rule 30 right light cone with center
   boundary `0101...`.

Consequently `J(n,H)` is SAT exactly when an arbitrary genuine right
half-plane can be joined to a left half that is zero beyond depth `2n` and
whose center alternates for `H` additional macros.  In direct spacetime
language, the initial row is zero strictly left of `-2n` and its center
alternates through the additional times `2n+1,...,2n+2H`.

The encoding uses Rule 30 gates directly on both sides.  It does not replace
right realizability by a finite forbidden-factor approximation.

## 2. Exact finite result

At `H=8`, every instance `J(n,8)` for `1 <= n <= 31` is UNSAT.  At smaller
horizons the exact SAT widths through 20 are:

```text
H=1: n=1..20
H=2: n=1,4..20
H=3: n=4,5,8..20
H=4: n=4,8,10,11,12,13,15,19,20
H=5: n=10,11,12
H=6: n=10,11
H=7: n=10
H=8: none
```

Every decoded SAT trace was replayed through the independent integer frontier
recurrence.  The width sweep is falsification evidence only.  It supplies no
induction in `n` and therefore does not prove constant-eight joint mortality.

## 3. Why short forbidden factors do not explain the result

The old filter retained only the uniform forbidden factors `11` and `00000`.
Its first retained counterexample has seed

```text
010101001010101010101000100010
```

and survives ten macros, but contains the actual-right forbidden factor
`101001`.

Adding every exact minimal forbidden right factor through length 18 removes
all horizon-eight witnesses through width 35.  At width 36, however, the
finite-type approximation admits

```text
00001010000100100001000010101000100001001001
10001010000100100001000010101000100001001001
```

Both are killed by the same length-24 minimal forbidden factor

```text
010000100100001000010101.
```

Adding every exact minimal forbidden factor through length 24 again moves the
first finite-type witness, this time to width 42.  Its complete rho word has
the suffix

```text
00010001000100010001000101000100001010101010100010
```

and contains the length-25 minimal forbidden factor

```text
0010001000100010001010001.
```

These are exact counterexamples to the finite-factor approximations, not
counterexamples to `J(n,8)`.  They show that the apparent constant bound is
tracking the moving boundary of the actual right trace language.  A proof
must give a parameterized obstruction or a coupled layer induction; extending
the forbidden list one length at a time is not uniform.

## 4. Geometric reformulation

Each seed macro reconstructs two initial cells on the left.  Eight accepted
post-seed macros therefore assert sixteen consecutive zeros immediately past
the reconstructed left endpoint.  The candidate theorem is equivalently a
bounded-gap assertion:

> Along an actual alternating-center Rule 30 right trace, the uniquely
> reconstructed initial left tail cannot have sixteen consecutive zero cells
> after any even endpoint.

This formulation removes the artificial knee vocabulary and identifies the
remaining proof object: a fixed-width zero block coupled to an arbitrarily
large Rule 30 light-cone layer.  No layer-peeling identity has yet been proved.

## 5. Consequence

If `J(n,8)` were proved UNSAT for every `n`, every left-finite alternating
fiber would die within sixteen time steps after its initial left endpoint
enters the reconstruction.  This would exclude the period-two same-orbit
trace for finite configurations.  It would not prove arbitrary-period P1,
P2, or P3.

At present the period-two theorem remains open.

## 6. Reproduction

The exact joint sweep requires the PySAT environment already used by
`mortality_sat.py`:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/joint_mortality.py \
  --max-n 20 --horizon 8

PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/right_filtered_mortality.py \
  --max-length 24
```

The first command rebuilds both Tseitin triangles and reports each exact
finite status.  The second independently replays the retained two-factor
counterexample.

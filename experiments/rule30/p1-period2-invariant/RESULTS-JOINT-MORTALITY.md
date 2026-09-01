# Joint left-finite/right-realizable mortality

Date: 2026-09-01

Status: **THE JOINT CONSTANT-EIGHT CANDIDATE IS FALSE.**  It is UNSAT through
seed length 40, but a genuine finite right half gives a seed-length-82 witness
that accepts ten post-knee macros.  The resulting finite Rule 30 configuration
alternates at the center through time 184 and first fails at time 185.  This is
a long finite prefix, not an infinite period-two counterexample.

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

At `H=8`, every instance `J(n,8)` for `1 <= n <= 31` is UNSAT; a separate
strategic check also found `J(40,8)` UNSAT.  At smaller horizons the exact SAT
widths through 20 are:

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
recurrence.  The width sweep was falsification evidence only.  It supplied no
induction in `n`; Section 4 gives the later exact counterexample.

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
010000100100001000010101
```

Adding every exact minimal forbidden factor through length 24 again moves the
first finite-type witness, this time to width 42.  Its complete rho word has
the suffix

```text
00010001000100010001000101000100001010101010100010
```

and contains the length-25 minimal forbidden factor

```text
0010001000100010001010001
```

Adding every exact minimal forbidden factor through length 25 still does not
close the horizon-eight finite-type approximation.  Its first witness is at
width 44; one complete seed-plus-continuation word is

```text
0000100010100001001000010010010000100001001000010010
```

and its first unrealizable actual-right factor has length 29:

```text
01001000010010010000100001001
```

These are exact counterexamples to the finite-factor approximations, not
counterexamples to `J(n,8)`.  They show that the apparent constant bound is
tracking the moving boundary of the actual right trace language.  A proof
must give a parameterized obstruction or a coupled layer induction; extending
the forbidden list one length at a time is not uniform.

## 4. Exact counterexample to the bounded-gap theorem

Exhaustive bit-parallel enumeration of every finite right half of width 16 to
depth 512 found right mask

```text
0x13be
```

whose reconstructed left tail has the zero block `L_165,...,L_184`, bracketed
by `L_164=L_185=1`.  Aligning the knee at `n=82`, its actual rho trace agrees
with ten forced continuation macros; macro 11 disagrees and the pin fails.
Thus `J(82,8)` and `J(82,10)` are SAT.

Truncating at that zero block gives the finite initial row with support
`[-164,13]`, right mask `0x13be`, and left mask

```text
0xa96bfe30260597f6e6d977d63403b1304cb232655
```

An independent direct set-valued Rule 30 evolution verifies

```text
s(t,0) = t mod 2 for 0 <= t <= 184,
s(185,0) = 0.
```

This finite row is now a load-bearing control: any proposed proof that forces
failure before time 185 is wrong.  It is not an infinite alternating trace.

## 5. Consequence

The counterexample kills the fixed sixteen-zero theorem and every smaller
constant bound.  It does not kill period-two mortality: the witness dies at
time 185.  Any proof must now control an unbounded quantity, for example a
linear mortality bound, a global tail-density inequality, or an eventual
periodicity obstruction.  The period-two theorem remains open, and even a
proof of it would not settle arbitrary-period P1, P2, or P3.

## 6. Reproduction

The exact joint sweep requires the PySAT environment already used by
`mortality_sat.py`:

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/joint_mortality.py \
  --max-n 20 --horizon 8

PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/right_filtered_mortality.py \
  --max-length 25
```

The first command independently replays the finite time-184 counterexample,
then rebuilds both Tseitin triangles and reports each exact finite status.  The
second independently replays the retained two-factor counterexample.

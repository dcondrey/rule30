# Actual-right trace factors and filtered mortality

Date: 2026-09-01

Status: **A NEW UNIFORM LOCAL LEMMA IS PROVED: an actual alternating-center
Rule 30 right trace `rho` contains neither `11` nor `00000`.**  Adding the
five-zero prohibition reduces the longest measured post-knee survival to
eight through seed length 24, but constant-eight mortality remains open.  It
is seed-specific: a legal arbitrary frontier survives ten macros.

## 1. Uniform five-zero theorem

Assume the center column is

```text
c_(2k)=0, c_(2k+1)=1,
```

and put `rho_k=s(2k,1)`.  Then every actual right half-plane satisfies

```text
rho_k rho_(k+1) != 11,
rho_k...rho_(k+4) != 00000                         (R5)
```

for every `k`.  The first line is the previously recorded two-row identity.
For the second, time translation reduces every `k` to zero.  The five even
samples through time eight depend only on the nine initial cells at positions
`1,...,9`.  Symbolically evolve those variables with

```text
f(l,c,r)=l XOR (c OR r)
```

and call the resulting Boolean polynomials `r_0,...,r_4`.  Exact Boolean-ANF
reduction gives

```text
(1+r_0)(1+r_1)(1+r_2)(1+r_3)(1+r_4) = 0.           (1)
```

The left side of (1) is precisely the indicator of five zero samples, so (1)
proves (R5).  This is a finite local identity applied at an arbitrary time;
there is no tested-width parameter.

As an independent proof check, a second integer implementation evaluates all
512 assignments of the nine-cell light cone and finds no `00000`.  Four
zeros are possible, so five is the first such constant.  Under Rule 90 the
same ANF product is nonzero and initial right mask `0x114` realizes five
zeros; the lemma uses Rule 30's OR as intended.

There is also a compact forced fragment behind (1).  If the first four rho
bits are zero, the first eight values of column 2 are uniquely

```text
11011100.
```

Its last `00` pair forces the fifth rho bit to one by the exact right-column
identity.  The ANF product and complete truth table are retained as the less
error-prone certificate.

## 2. The actual right language is substantially smaller

The number of length-`n` rho prefixes realized by arbitrary initial right
light cones begins

```text
n:       1  2  3  4  5  6  7  8  9 10
count:   2  3  5  8 12 17 25 36 50 68.
```

Because shifting an alternating spacetime by two time steps preserves the
phase, every forbidden prefix is a forbidden factor.  Exact light-cone
enumeration gives the first minimal forbidden factors:

```text
length 2:   11
length 5:   00000
length 6:   101001
length 7:   0100101
length 9:   010010001
length 10:  0101000101, 0101010000.
```

Only `11` and `00000` are used in the filtered mortality conjecture.  The
longer list is finite language data, not a finite presentation of the full
right trace shift.

## 3. Filtered mortality falsification

Restrict both a rho seed and its forced zero-output continuation to avoid
`11` and `00000`.  Exact replay of every legal seed through length 24 gives
maximum accepted continuation lengths

```text
2,1,1,4,3,2,2,4,3,8,7,6,5,4,5,5,6,6,8,7,7,8,7,7.
```

No seed survives nine macros.  Exact CNF queries at horizon nine are also
UNSAT for `n=10,16,22,24,25`; these are falsification instances, not a proof
schema.  The candidate uniform statement is therefore:

> Every seed-generated frontier whose complete rho history avoids `11` and
> `00000` fails within eight post-knee macros.

If proved, (R5) would make it sufficient for the period-two theorem.

## 4. Why an arbitrary-core automaton is insufficient

The fixed horizon can be composed into nine cascaded four-carry transducers,
but the resulting finite automaton accepts non-seed frontiers.  The explicit
state

```text
(T,A,B)=(12,81,658),  prior rho history 0001
```

passes ten forced macros before producing a forbidden right-language factor.
It is not any length-six `seed_state` satisfying `11`/`00000` avoidance.

Thus a proof over all aligned words is false.  The missing invariant is the
seed-generated triangular language, exactly as in the matched-extension and
interval-annihilator audits.  A successful constant proof must recognize
that language or give indexed Boolean-ideal rewrites; a D8/carry endpoint
automaton alone cannot do it.

## 5. Consequence

The five-zero theorem is a genuine strengthening of the bilateral reduction
and is already uniform.  Constant-eight mortality, reconstructed-tail
density, and the period-two theorem are **not** proved.  Prize Problem 1 is
unchanged beyond this local lemma.

## 6. Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/right_trace_forbidden.py \
  --max-language 10

PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/p1-period2-invariant/right_filtered_mortality.py \
  --max-length 24
```

The first command verifies (1), the independent 512-row proof, Rule 90, and
the finite language table.  The second reproduces every filtered mortality
maximum and the arbitrary-core counterexample.

# Stored residuals rule out eight starting scales for the absolute margin

Date: 2026-09-16. **Exact finite exclusions, using existing data only.**
This audit narrows one sufficient certificate for inherited Thue-Morse
growth. It supplies no estimate for the weaker live target: unbounded,
sublinear third-frequency sums on the singleton orbit.

Use the notation of the
[four-adic scale report](RESULTS-third-frequency-scale-target.md):

```
omega = exp(-2*pi*i/3),
F_k = sum_(t<4^k) (-1)^c_t * omega^t,
D_k = F_(k+1)-3*F_k.
```

The data below are the already stored exact Eisenstein pairs for
F_0,...,F_10 and D_0,...,D_9. No larger prefix is read or generated.

## 1. The absolute-tail certificate fails at starts zero through seven

The proposed sufficient margin at a starting scale h is

```
sum_(j>=h) |D_j|/3^(j-h+1) < |F_h|.                    (1)
```

It would establish a nonzero limit of F_k/3^k. The earlier report
excluded h=0. Existing later data exclude every h through seven:

| h | Last defect used | Certified lower bound on partial left side | Certified upper bound on \|F_h\| |
|---:|---:|---:|---:|
| 0 | 1 | 11/9 | 1 |
| 1 | 4 | 259/81 | 3 |
| 2 | 4 | 124/27 | 3 |
| 3 | 4 | 70/9 | 3 |
| 4 | 4 | 58/3 | 5 |
| 5 | 6 | 445/9 | 47 |
| 6 | 7 | 352/3 | 86 |
| 7 | 7 | 129 | 45 |

Each lower bound strictly exceeds its upper bound. The certificates use
only integer square roots: replace each defect magnitude by the floor
of the square root of its integer norm, and the starting magnitude by
the corresponding ceiling. Thus no floating-point comparison is needed.

Starts h=8 and h=9 are **not refuted by the stored partial tails**.
Their partial budgets have certified upper bounds 2887/9 and 2281/3,
respectively, below starting-amplitude lower bounds 492 and 1302.
These are not infinite-tail estimates. The unobserved defects remain
uncontrolled, and no positive certificate at either start is inferred.

This finite exclusion also does not disprove absolute summability,
a nonzero scaled limit proved by a different argument, or unbounded
sublinear growth with another scale. The weaker P1 target does not
require the strict margin (1) or the exponent log_4(3).

## 2. The exact radial energy term is usually negative in the stored scales

Put E_k=|F_k|^2. Squaring the exact recurrence gives

```
E_(k+1) = 9*E_k + 6*Re(F_k*conj(D_k)) + |D_k|^2.       (2)
```

For Eisenstein pairs `F=a+b*omega`, `D=c+d*omega`, the cross term is
computed without numerical complex arithmetic:

```
2*Re(F*conj(D)) = 2*a*c-a*d-b*c+2*b*d.
```

The exact values of Re(F_k*conj(D_k)) at k=0,...,9 are

```
-1, -14, -15, -12, -250, -3019, -18842,
12457, -88360, -2940427.
```

Thus a nonnegative radial-coupling premise already fails at nine of
these ten scales. Nonzero residual energy does not by itself imply
radial growth. Even monotone amplitude growth fails on the actual seed:
E_6=7231 whereas E_7=1963. These are finite counterexamples to those
specific proposed inequalities, not claims about every later scale or
about long-term growth.

## 3. Nonvanishing at four-adic endpoints is automatic

There is a separate arithmetic trap. For any binary sign sequence and
N=4^k, write the three residue sums as A_0,A_1,A_2. Then

```
F_k = (A_0-A_2)+(A_1-A_2)*omega.
```

For k>=1 the numbers of terms in these sums have parities even, odd,
odd. Since every sign is odd, the first Eisenstein coefficient is odd
and the second is even. The same coefficient parities hold at k=0.
Therefore F_k is never zero, for every binary input sequence whatsoever.
This establishes only |F_k|>=1. The constant sign sequence has F_k=-1
at all these endpoints, so nonvanishing supplies no unboundedness.

The exact recurrence and these arithmetic controls do not derive a
seed-specific growth mechanism. A useful further theorem must bound
the accumulated cancellation or force actual escape of the Fourier
sums, without importing either conclusion from the arbitrary-sequence
identity.

## 4. Reproduction and scope

The [standard-library verifier](../../experiments/rule30/third_frequency_residual_margin_audit.py)
reads the existing
[scale artifact](../../experiments/rule30/third-frequency-scale-audit.json),
checks all ten recurrences and integer energy identities, and verifies
the rational certificates above. It records the source-artifact hash
and verifier hash in its
[JSON output](../../experiments/rule30/third-frequency-residual-margin-audit.json).
It does not independently regenerate the cached seed prefix; the
source report states that validation's scope.

```sh
uv run --offline --no-project python experiments/rule30/third_frequency_residual_margin_audit.py
```

Pass `--output PATH` to additionally write the JSON record.
